"""Guiones con Gemini, siempre a partir de un texto comprobado (la noticia o el dato del banco).

Reglas (apartado 5 del plan): nada que no diga la fuente; «Rockstar confirma» solo si es oficial;
nada de filtraciones, rumores como hechos ni destripes; sin enlaces para comprar; parafrasear."""
import re, unicodedata
import gemini
from config import HASHTAGS_FIJOS, PIE_POST, OFICIALES
from medios import GRUPOS

REGLAS = """Eres el guionista de «Leónida al Día», una cuenta de fans de GTA 6 en español de España.
Escribes vídeos verticales de 15 a 30 segundos (unas 45-75 palabras en total) que lee una voz sintética.
Reglas que no se pueden saltar:
- Usa SOLO la información del TEXTO DE LA FUENTE. No añadas datos, cifras, fechas ni opiniones que no estén ahí.
- Si la fuente no es oficial (Rockstar Games o Take-Two), atribúyelo: «Según {medio}…». «Rockstar confirma» solo si lo dice Rockstar o Take-Two.
- Nada de filtraciones (material filtrado), rumores presentados como hechos ni destripes de la historia.
- No copies frases literales de la fuente: cuéntalo con tus palabras.
- No invites a comprar ni a reservar, y no pongas enlaces.
- Frases cortas y claras, tono cercano y con energía, sin exagerar ni engañar. Nada de mayúsculas sostenidas ni emojis.
- Escribe los números como se dicen si es raro leerlos («GTA 6», «19 de noviembre», «30 euros»).
"""

FORMATO = """Devuelve SOLO un JSON con estos campos:
{
  "titular": "resumen de la noticia en menos de 70 caracteres",
  "etiqueta": "tema en mayúsculas, máximo 16 caracteres (un personaje como LUCÍA, un lugar como VICE CITY, o el asunto: PRECIO, TRÁILER, FECHA, MÚSICA, VENTAS…)",
  "es_personaje": true o false (si la etiqueta es un personaje),
  "grupo_capturas": "uno de: %s",
  "gancho": "primera frase, que enganche y diga de qué va, máximo 80 caracteres",
  "cuerpo": ["3 a 6 trozos de máximo 45 caracteres cada uno, que se leen seguidos"],
  "cierre": "pregunta final para comentar, máximo 60 caracteres",
  "texto_post": "2 o 3 frases para el texto de la publicación (sin hashtags)",
  "hashtags": ["1 o 2 hashtags del tema, sin tildes, p. ej. #ViceCity o #Lucia"],
  "titulo_youtube": "título para YouTube de menos de 90 caracteres, que diga lo que cuenta el vídeo, sin engañar"
}""" % ", ".join(GRUPOS)

AYUDA_GRUPOS = """Grupos de capturas oficiales (elige el que mejor case con lo que se cuenta; si es algo general como fechas, precio, ventas o tráileres, usa Jason_and_Lucia o Vice_City):
Jason_and_Lucia (los dos protagonistas), Jason_Duval, Lucia_Caminos, Vice_City (la ciudad), Leonida_Keys (los cayos),
Grassrivers (humedales), Port_Gellhorn, Ambrosia, Mount_Kalaga_National_Park, y personajes: Boobie_Ike, Brian_Heder,
Cal_Hampton, DreQuan_Priest, Raul_Bautista, Real_Dimez."""


def _limpiar(t, maximo):
    t = re.sub(r"\s+", " ", (t or "")).strip().strip('"«»')
    if len(t) > maximo:
        t = t[:maximo].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    return t


def hashtags(extra):
    out = list(HASHTAGS_FIJOS)
    for h in extra or []:
        h = unicodedata.normalize("NFKD", str(h)).encode("ascii", "ignore").decode()
        h = "#" + re.sub(r"[^A-Za-z0-9]", "", h)
        if len(h) > 2 and h.lower() not in {x.lower() for x in out} and h.lower() not in {"#gta", "#gta6", "#gtavi", "#rockstar"}:
            out.append(h)
    return " ".join(out[:5])


def validar(j):
    """Comprueba y recorta lo que devuelve Gemini. Lanza un error si falta lo esencial."""
    cuerpo = [_limpiar(c, 60) for c in (j.get("cuerpo") or []) if str(c).strip()]
    if not j.get("gancho") or len(cuerpo) < 2 or not j.get("cierre"):
        raise RuntimeError("Gemini devolvió un guion incompleto")
    grupo = j.get("grupo_capturas") if j.get("grupo_capturas") in GRUPOS else "Vice_City"
    return {
        "titular": _limpiar(j.get("titular"), 90),
        "etiqueta": _limpiar(j.get("etiqueta"), 18).upper().rstrip("…") or "GTA 6",
        "personaje": bool(j.get("es_personaje")),
        "grupo": grupo,
        "trozos": [_limpiar(j["gancho"], 95)] + cuerpo[:6] + [_limpiar(j["cierre"], 75)],
        "texto_post": _limpiar(j.get("texto_post"), 600),
        "hashtags": hashtags(j.get("hashtags")),
        "titulo": _limpiar(j.get("titulo_youtube"), 95),
    }


def caption(g, fuente, oficial, voz_reserva=False):
    linea = f"Fuente: {fuente}" + ("" if oficial else " (según medios)")
    extra = "\nVoz: sharvard (CC BY 3.0)" if voz_reserva else ""
    return f"{g['texto_post']}\n\n{linea}\n{PIE_POST}{extra}\n\n{g['hashtags']}"


def de_dato(dato):
    """Guion a partir de un dato del banco (columnas del CSV / tabla Datos)."""
    oficial = dato.get("Estado") == "Oficial"
    prompt = (REGLAS + "\n" + AYUDA_GRUPOS + "\n\nVas a contar un DATO o CURIOSIDAD de GTA 6.\n"
              f"Tema: {dato.get('Tema')}\nFuente: {dato.get('Fuente')} ({'oficial' if oficial else 'no oficial: atribúyelo'})\n"
              f"Grupo de capturas recomendado: {dato.get('Imagen sugerida')}\n\nTEXTO DE LA FUENTE:\n{dato.get('Dato')}\n\n" + FORMATO)
    g = validar(gemini.texto_json(prompt))
    if dato.get("Imagen sugerida") in GRUPOS:
        g["grupo"] = dato["Imagen sugerida"]  # la imagen la decide el banco (regla de G2)
    return g


def de_noticia(medio, titulo, texto):
    oficial = medio in OFICIALES
    prompt = (REGLAS + "\n" + AYUDA_GRUPOS + "\n\nVas a contar una NOTICIA de hoy sobre GTA 6.\n"
              f"Medio: {medio} ({'oficial' if oficial else 'no oficial: di «Según ' + medio + '»'})\n"
              f"Titular original: {titulo}\n\nTEXTO DE LA FUENTE:\n{texto[:7000]}\n\n" + FORMATO)
    return validar(gemini.texto_json(prompt))


def guion_a_texto(trozos):
    return "\n".join(trozos)


def texto_a_guion(texto):
    return [l.strip() for l in (texto or "").splitlines() if l.strip()]
