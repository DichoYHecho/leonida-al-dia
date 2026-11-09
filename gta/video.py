"""Hace (o rehace) el vídeo de una publicación.

- La voz se guarda en la caché de GitHub (cache/voces/<huella>.wav), no en Airtable, para gastar menos
  llamadas. «Huella» = huella del guion: si cambio el guion en Airtable, se vuelve a pedir la voz.
- «Huella vídeo» = guion + etiqueta + capturas + fuente + día: si cambia algo de eso, se vuelve a montar
  el vídeo (sin gastar voz). Así puedo corregir el texto en la revisión sin borrar nada.
- Desde el 25 oct el montaje es render2 (edición V2: tipografía de tráiler, subtítulos palabra a palabra,
  encuadre de las caras con Gemini…); la «Huella vídeo» lleva también la versión de la edición (EDICION)."""
import hashlib, json, os, re, shutil, tempfile, unicodedata
from datetime import date
import airtable, medios, render, render2, voz
from config import VOZ, VELOCIDAD_VOZ  # 9 nov: la voz entra en la huella; si cambia de voz, se pide de nuevo
from config import CACHE, T_PUB, cuenta_atras

VOCES = os.path.join(CACHE, "voces")
EDICION = "v4"  # 29 oct: subtítulos siempre legibles (fase E1, subtitulos.py). v3, 27 oct: sin cierre de marca (v2, 25 oct: edición nueva (render2 + encuadre). Si cambia, la repesca rehace los vídeos sin publicar


def huella(*partes):
    return hashlib.sha256("\n§\n".join(str(p or "") for p in partes).encode()).hexdigest()[:16]


def trozos_de(f):
    return [l.strip() for l in (f.get("Guion") or "").splitlines() if l.strip()]


def huella_video(f, dia):
    return huella(EDICION, (f.get("Guion") or "").strip(), (f.get("Etiqueta") or "").strip(), (f.get("Capturas") or "").strip(),
                  (f.get("Fuente") or "").strip(), bool(f.get("Personaje")), f.get("Tipo"), dia.isoformat())


def pie(f, reserva, con_trozos=False, caps=()):
    juego = not caps or any(not medios.es_imagen(c) for c in caps)
    quien = list(dict.fromkeys([medios.credito(c) for c in caps if medios.es_imagen(c)] + (["Rockstar Games"] if juego else [])))
    rotulo = "Imagen" if len(quien) == 1 and not juego else "Imágenes"
    p = f"Fuente: {f.get('Fuente') or 'Rockstar Games'} · {rotulo}{' y sonido' if con_trozos else ''}: {' y '.join(quien)}"
    return p + (" · Voz: sharvard (CC BY 3.0)" if reserva else "")


def preparar_voz(f):
    """Devuelve (ruta del wav, tiempos, nombre de la voz, aviso, cambios para Airtable)."""
    trozos = trozos_de(f)
    if len(trozos) < 3:
        raise RuntimeError("el guion necesita al menos 3 líneas (gancho, cuerpo y pregunta final)")
    h = huella(f"{VOZ} {VELOCIDAD_VOZ} calma", (f.get("Guion") or "").strip())  # 9 nov: velocidad y estilo nuevos: se piden de nuevo
    os.makedirs(VOCES, exist_ok=True)
    wav, js = os.path.join(VOCES, h + ".wav"), os.path.join(VOCES, h + ".json")
    if os.path.exists(wav) and os.path.exists(js):
        d = json.load(open(js))
        return wav, d["tiempos"], d["voz"], d.get("aviso", ""), {"Huella": h, "Voz": d["voz"], "Tiempos": json.dumps(d["tiempos"])}
    tiempos, nombre, aviso = voz.generar(trozos, wav)
    json.dump({"tiempos": tiempos, "voz": nombre, "aviso": aviso}, open(js, "w"), ensure_ascii=False)
    return wav, tiempos, nombre, aviso, {"Huella": h, "Voz": nombre, "Tiempos": json.dumps(tiempos)}


def montar(f, dia, semilla, salida_dir, extra=None):
    """Monta el vídeo en salida_dir. Devuelve (ruta, info, cambios para Airtable).
    (La música sale siempre igual para el mismo guion; «semilla» se deja por compatibilidad.)"""
    caps = medios.validas(f.get("Capturas"))
    if not caps:
        raise RuntimeError("no hay capturas válidas en «Capturas»")
    medios.preparar()
    buenas = [c for c in caps if os.path.exists(medios.ruta_sin_comprobar(c))]  # un trozo o una imagen que falla se salta
    aviso_img = ""
    if not buenas and any(medios.es_imagen(c) for c in caps):
        buenas = medios.elegir("Jason_and_Lucia", f.get("Titular"), 2)
        aviso_img = "No se pudo descargar la imagen de la noticia: salen capturas del juego"
    caps = buenas or caps
    rutas = [medios.ruta(c) for c in caps]  # antes de gastar voz: que existan las imágenes
    wav, tiempos, nombre, aviso, cambios = preparar_voz(f)
    trozos = trozos_de(f)
    reserva = nombre.startswith("Piper")
    tmp = tempfile.mkdtemp()
    try:
        etiqueta = unicodedata.normalize("NFKD", (f.get("Etiqueta") or "gta6").lower()).encode("ascii", "ignore").decode()
        etiqueta = re.sub(r"[^a-z0-9]+", "-", etiqueta).strip("-")[:30] or "gta6"
        salida = os.path.join(salida_dir, f"leonida-{dia.isoformat()}-{etiqueta}.mp4")
        info = render2.montar({
            "trozos": trozos, "tiempos": tiempos, "voz": wav,
            "capturas": [(r, *medios.foco_plano(c)) for r, c in zip(rutas, caps)],
            "etiqueta": f.get("Etiqueta"), "tipo": f.get("Tipo"), "personaje": f.get("Personaje"),
            "cuenta": cuenta_atras(dia), "pie": pie(f, reserva, any(medios.con_sonido(c) for c in caps), caps), "salida": salida,
            "semilla": int(huella((f.get("Guion") or "").strip())[:6], 16) % 1000, "tmp": tmp,
            "subs": "e1",  # 29 oct: fase E1 (zona segura, banda oscura según el fondo, logo de GTA VI encogido)
            **(extra or {})})  # extra: p. ej. el reloj de la cuenta atrás
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    cambios.update({"Para el día": dia.isoformat(), "Huella vídeo": huella_video(f, dia)})
    aviso = "\n".join(a for a in (aviso, aviso_img, *info.get("avisos", [])) if a)  # «Subtítulo tapado» (E1)
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
