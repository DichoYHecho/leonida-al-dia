"""Hace (o rehace) el vídeo de una publicación.

- La voz se guarda en la caché de GitHub (cache/voces/<huella>.wav), no en Airtable, para gastar menos
  llamadas. «Huella» = huella del guion: si cambio el guion en Airtable, se vuelve a pedir la voz.
- «Huella vídeo» = guion + etiqueta + capturas + fuente + día: si cambia algo de eso, se vuelve a montar
  el vídeo (sin gastar voz). Así puedo corregir el texto en la revisión sin borrar nada."""
import hashlib, json, os, re, shutil, tempfile, unicodedata
from datetime import date
import airtable, medios, render, voz
from config import CACHE, T_PUB, cuenta_atras

VOCES = os.path.join(CACHE, "voces")


def huella(*partes):
    return hashlib.sha256("\n§\n".join(str(p or "") for p in partes).encode()).hexdigest()[:16]


def trozos_de(f):
    return [l.strip() for l in (f.get("Guion") or "").splitlines() if l.strip()]


def huella_video(f, dia):
    return huella((f.get("Guion") or "").strip(), (f.get("Etiqueta") or "").strip(), (f.get("Capturas") or "").strip(),
                  (f.get("Fuente") or "").strip(), bool(f.get("Personaje")), f.get("Tipo"), dia.isoformat())


def pie(f, reserva, con_trozos=False):
    p = f"Fuente: {f.get('Fuente') or 'Rockstar Games'} · Imágenes{' y sonido' if con_trozos else ''}: Rockstar Games"
    return p + (" · Voz: sharvard (CC BY 3.0)" if reserva else "")


def preparar_voz(f):
    """Devuelve (ruta del wav, tiempos, nombre de la voz, aviso, cambios para Airtable)."""
    trozos = trozos_de(f)
    if len(trozos) < 3:
        raise RuntimeError("el guion necesita al menos 3 líneas (gancho, cuerpo y pregunta final)")
    h = huella((f.get("Guion") or "").strip())
    os.makedirs(VOCES, exist_ok=True)
    wav, js = os.path.join(VOCES, h + ".wav"), os.path.join(VOCES, h + ".json")
    if os.path.exists(wav) and os.path.exists(js):
        d = json.load(open(js))
        return wav, d["tiempos"], d["voz"], d.get("aviso", ""), {"Huella": h, "Voz": d["voz"], "Tiempos": json.dumps(d["tiempos"])}
    tiempos, nombre, aviso = voz.generar(trozos, wav)
    json.dump({"tiempos": tiempos, "voz": nombre, "aviso": aviso}, open(js, "w"), ensure_ascii=False)
    return wav, tiempos, nombre, aviso, {"Huella": h, "Voz": nombre, "Tiempos": json.dumps(tiempos)}


def montar(f, dia, semilla, salida_dir):
    """Monta el vídeo en salida_dir. Devuelve (ruta, info, cambios para Airtable).
    (La música sale siempre igual para el mismo guion; «semilla» se deja por compatibilidad.)"""
    caps = medios.validas(f.get("Capturas"))
    if not caps:
        raise RuntimeError("no hay capturas válidas en «Capturas»")
    medios.preparar()
    caps = [c for c in caps if os.path.exists(medios.ruta_sin_comprobar(c))] or caps  # un trozo que no se pudo cortar se salta
    rutas = [medios.ruta(c) for c in caps]  # antes de gastar voz: que existan las imágenes
    wav, tiempos, nombre, aviso, cambios = preparar_voz(f)
    trozos = trozos_de(f)
    reserva = nombre.startswith("Piper")
    tmp = tempfile.mkdtemp()
    try:
        etiqueta = unicodedata.normalize("NFKD", (f.get("Etiqueta") or "gta6").lower()).encode("ascii", "ignore").decode()
        etiqueta = re.sub(r"[^a-z0-9]+", "-", etiqueta).strip("-")[:30] or "gta6"
        salida = os.path.join(salida_dir, f"leonida-{dia.isoformat()}-{etiqueta}.mp4")
        info = render.montar({
            "trozos": trozos, "tiempos": tiempos, "voz": wav,
            "capturas": [(r, medios.CAPTURAS[c]["foco"], medios.CAPTURAS[c]["plano"]) for r, c in zip(rutas, caps)],
            "etiqueta": f.get("Etiqueta"), "tipo": f.get("Tipo"), "personaje": f.get("Personaje"),
            "cuenta": cuenta_atras(dia), "pie": pie(f, reserva, any(medios.con_sonido(c) for c in caps)), "salida": salida,
            "semilla": int(huella((f.get("Guion") or "").strip())[:6], 16) % 1000, "tmp": tmp})
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    cambios.update({"Para el día": dia.isoformat(), "Huella vídeo": huella_video(f, dia)})
    if aviso:
        cambios["Avisos"] = aviso
    info["voz"] = nombre
    return salida, info, cambios


def subir(rec_id, ruta):
    """Sube el vídeo y devuelve la URL del nuevo adjunto (el viejo se quita después)."""
    nuevo = airtable.subir_adjunto(rec_id, "Vídeo", ruta, "video/mp4")
    if not nuevo:  # por si la respuesta no trae el adjunto: se lee la publicación (1 llamada más)
        d = airtable.pedir("GET", f"{airtable.tabla(T_PUB)}/{rec_id}")
        adj = d["fields"].get("Vídeo") or []
        nuevo = adj[-1] if adj else None
    return nuevo
