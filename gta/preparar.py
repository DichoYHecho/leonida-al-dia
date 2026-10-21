"""Prepara propuestas para revisar en Airtable («Por Revisar»), cada una con su vídeo.

- Noticias (08:00 y 19:00): lee las fuentes, Gemini elige las que merecen vídeo (sin repetir lo ya
  propuesto) y escribe el guion solo con lo que dice la fuente. Como mucho 3 por la mañana y 2 por la tarde.
- Datos (08:00): mantiene siempre 2 datos del banco pendientes de publicar.
- Además pasa a «Caducada» las noticias que llevan más de 36 horas sin publicarse.

Variables: QUE (noticias, datos o todo), MAX (máximo de noticias; por defecto según la hora)."""
import csv, json, os, sys, tempfile, time
from datetime import datetime, timedelta, timezone, date
import airtable, fuentes, guion, medios, video
from config import (AQUI, MADRID, T_PUB, CADUCA_HORAS, MAX_NOTICIAS_MANANA, MAX_NOTICIAS_TARDE, DATOS_EN_COLA,
                    OFICIALES, ARRANQUE)
import gemini

AHORA = datetime.now(MADRID)
HOY = AHORA.date()
RESUMEN = []


def nota(txt):
    print(txt, flush=True)
    RESUMEN.append(txt)


def recientes():
    """Publicaciones de los últimos 10 días (1 llamada) para no repetir y para caducar."""
    formula = "IS_AFTER({Creada}, DATEADD(NOW(), -10, 'days'))"
    return airtable.listar(T_PUB, ["Titular", "Tipo", "Estado", "Enlace", "Creada", "Orden dato"], formula=formula)


def caducar(regs):
    limite = datetime.now(timezone.utc) - timedelta(hours=CADUCA_HORAS)
    cambios = []
    for r in regs:
        f = r["fields"]
        if f.get("Tipo") == "Noticia" and f.get("Estado") in ("Por Revisar", "Aprobado") and f.get("Creada"):
            if datetime.fromisoformat(f["Creada"].replace("Z", "+00:00")) < limite:
                cambios.append((r["id"], {"Estado": "Caducada"}))
    if cambios:
        airtable.actualizar(T_PUB, cambios)
        nota(f"Noticias caducadas (más de {CADUCA_HORAS} h sin publicar): {len(cambios)}")


def fila(g, tipo, fuente, oficial, enlace, texto_fuente, dia, orden=None):
    cuantas = 3 if len(" ".join(g["trozos"])) > 330 else 2
    caps = g.get("capturas") or []
    if len(caps) < 2:
        caps = (caps + [c for c in medios.elegir(g["grupo"], g["titular"] + str(orden or ""), 3) if c not in caps])[:cuantas]
    caps = caps[:3]
    if caps and all(medios.es_trozo(c) for c in caps):  # al menos una captura (los trozos son cortos)
        caps = caps[:2] + [c for c in medios.elegir(g["grupo"], g["titular"], 2) if c not in caps][:1]
    texto = guion.caption(g, fuente, oficial)
    if any(medios.con_sonido(c) for c in caps):
        texto = texto.replace("Imágenes: Rockstar Games.", "Imágenes y sonido: Rockstar Games.")
    f = {"Titular": g["titular"], "Estado": "Por Revisar", "Tipo": tipo, "Info": "Oficial" if oficial else "Según medios",
         "Guion": guion.guion_a_texto(g["trozos"]), "Etiqueta": g["etiqueta"], "Personaje": g["personaje"],
         "Capturas": ", ".join(caps), "Caption": texto, "Título YouTube": g["titulo"],
         "Fuente": fuente, "Enlace": enlace, "Texto de la fuente": (texto_fuente or "")[:3000],
         "Creada": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    if orden is not None:
        f["Orden dato"] = orden
    return f


def con_video(f, dia, carpeta):
    """Monta el vídeo antes de crear la publicación (así se crea con todo en 1 llamada)."""
    ruta, info, cambios = video.montar(f, dia, video.huella(f["Titular"]), carpeta)
    f.update(cambios)
    if info["voz"].startswith("Piper"):  # crédito de la voz de reserva
        f["Caption"] = f["Caption"].replace("\n\n#", "\nVoz: sharvard (CC BY 3.0)\n\n#", 1)
    return ruta, info


def crear_con_videos(lista):
    """lista = [(campos, ruta del vídeo)] → crea las publicaciones (1 llamada) y sube los vídeos."""
    if not lista:
        return
    regs = airtable.crear(T_PUB, [f for f, _ in lista])
    for r, (f, ruta) in zip(regs, lista):
        video.subir(r["id"], ruta)
        nota(f"✅ {f['Tipo']}: {f['Titular']} ({f.get('Voz', '')})")


# ---------------------------------------------------------------- noticias
def elegir(cands, ya, maximo):
    lista = "\n".join(f"{i}. [{c['medio']}] {c['titulo']} — {c['resumen'][:220]}" for i, c in enumerate(cands))
    hechas = "\n".join(f"- {t}" for t in ya) or "(ninguna)"
    prompt = f"""Eres el editor de «Leónida al Día», cuenta de fans de GTA 6 en español.
Estas son las noticias de las últimas horas que mencionan GTA 6:
{lista}

Ya hemos propuesto estas (no repitas el mismo tema):
{hechas}

Elige como mucho {maximo} que merezcan un vídeo hoy: novedades reales sobre GTA 6 (anuncios, fechas, precios,
tráileres, cifras, análisis, declaraciones oficiales, polémicas reales). Si varias cuentan lo mismo, elige solo una,
preferiblemente la oficial (Rockstar Games o Take-Two) o la más completa.
Descarta: filtraciones o material filtrado, rumores sin confirmar, especulación, listas de opinión, ofertas para
comprar o reservar, noticias que solo mencionan GTA 6 de pasada, y destripes de la historia.
Devuelve SOLO un JSON: {{"elegidas": [{{"n": número, "motivo": "frase corta"}}]}} (lista vacía si no hay ninguna)."""
    j = gemini.texto_json(prompt, 0.2)
    out = []
    for e in j.get("elegidas", [])[:maximo]:
        try:
            out.append(cands[int(e["n"])])
        except Exception:
            pass
    return out


def noticias(regs, maximo, carpeta):
    enlaces = {(r["fields"].get("Enlace") or "").split("?")[0] for r in regs}
    ya = [r["fields"].get("Titular", "") for r in regs if r["fields"].get("Tipo") == "Noticia"]
    cands = [c for c in fuentes.candidatas() if c["enlace"].split("?")[0] not in enlaces][:25]
    nota(f"Noticias nuevas sobre GTA 6 en las fuentes: {len(cands)}")
    if not cands or maximo <= 0:
        return []
    elegidas = elegir(cands, ya, maximo)
    nota(f"Elegidas por Gemini: {len(elegidas)}")
    dia = HOY  # la de la mañana sale a las 14:00 y la de la tarde a las 21:00
    out = []
    for c in elegidas:
        try:
            texto = fuentes.texto_de(c)
            g = guion.de_noticia(c["medio"], c["titulo"], texto)
            f = fila(g, "Noticia", c["medio"], c["medio"] in OFICIALES, c["enlace"], texto, dia)
            ruta, info = con_video(f, dia, carpeta)
            out.append((f, ruta))
        except Exception as e:
            nota(f"⚠️ No se pudo preparar «{c['titulo'][:80]}»: {str(e)[:200]}")
    return out


# ---------------------------------------------------------------- datos
def banco():
    with open(os.path.join(AQUI, "banco_datos.csv"), encoding="utf-8") as f:
        return [r for r in csv.DictReader(f)]


def datos(regs_todas, carpeta):
    # Los datos pueden ser de hace más de 10 días: se consultan todos los de tipo Dato (1 llamada)
    regs = airtable.listar(T_PUB, ["Estado", "Orden dato"], formula="{Tipo}='Dato'")
    usados = {int(r["fields"]["Orden dato"]) for r in regs if r["fields"].get("Orden dato") is not None}
    pendientes = sum(1 for r in regs if r["fields"].get("Estado") in ("Por Revisar", "Aprobado"))
    falta = min(2, DATOS_EN_COLA - pendientes)
    nota(f"Datos pendientes de publicar: {pendientes}; se preparan {max(falta, 0)}")
    if falta <= 0:
        return []
    dia = max(HOY + timedelta(days=1), ARRANQUE)
    out, fallos = [], 0
    for d in banco():
        if falta <= 0 or fallos >= 3:
            break
        orden = int(d["Orden"])
        if orden in usados:
            continue
        if d.get("Válido hasta") and date.fromisoformat(d["Válido hasta"]) < dia:
            continue
        try:
            g = guion.de_dato(d)
            f = fila(g, "Dato", d["Fuente"], d["Estado"] == "Oficial", d["Enlace"], d["Dato"], dia, orden)
            ruta, info = con_video(f, dia, carpeta)
            out.append((f, ruta))
            falta -= 1
        except Exception as e:
            fallos += 1
            nota(f"⚠️ No se pudo preparar el dato {orden}: {str(e)[:200]}")
    if falta > 0:
        nota("⚠️ Quedan pocos datos en el banco: hay que añadir más a gta/banco_datos.csv")
    return out


def main():
    que = os.environ.get("QUE") or "todo"
    tarde = AHORA.hour >= 15
    maximo = int(os.environ.get("MAX") or (MAX_NOTICIAS_TARDE if tarde else MAX_NOTICIAS_MANANA))
    regs = recientes()
    caducar(regs)
    carpeta = tempfile.mkdtemp()
    lista = []
    if que in ("noticias", "todo"):
        lista += noticias(regs, maximo, carpeta)
    if que == "datos" or (que == "todo" and not tarde):
        lista += datos(regs, carpeta)
    crear_con_videos(lista)
    nota(f"Llamadas a Airtable en esta ejecución: {airtable.LLAMADAS}")
    s = os.environ.get("GITHUB_STEP_SUMMARY")
    if s:
        open(s, "a").write("## Propuestas preparadas\n\n" + "\n".join(f"- {t}" for t in RESUMEN) + "\n")


if __name__ == "__main__":
    main()
