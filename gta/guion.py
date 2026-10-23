"""Guiones con Gemini, siempre a partir de un texto comprobado (la noticia o el dato del banco).

Reglas (apartado 5 del plan): nada que no diga la fuente; «Rockstar confirma» solo si es oficial;
nada de filtraciones, rumores como hechos ni destripes; sin enlaces para comprar; parafrasear."""
import re, unicodedata
import gemini
from config import HASHTAGS_FIJOS, PIE_POST, OFICIALES
from medios import GRUPOS, CAPTURAS, validas

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
- Usa bien los signos del español: «¿…?» y «¡…!». La pregunta final siempre entre «¿» y «?».
- No hagas predicciones ni especules sobre lo que pasará en el juego, en la historia ni en las ventas.
- Si la fuente cita a otro (una empresa de análisis, un periodista, un desarrollador), dilo: «Según 3DJuegos, Sensor Tower calcula…».
  Una estimación se cuenta como estimación («calcula», «estima»), nunca como un hecho.
- Da el dato concreto (cifras, nombres, fechas de la fuente) en vez de frases vagas como «millones» o «muchos».
- La pregunta final pide la opinión del público; no puede ser una apuesta ni una predicción («¿Llegará a…?»).
"""

FORMATO = """Devuelve SOLO un JSON con estos campos:
{
  "titular": "resumen de la noticia en menos de 70 caracteres",
  "etiqueta": "tema en mayúsculas, máximo 16 caracteres (un personaje como LUCÍA, un lugar como VICE CITY, o el asunto: PRECIO, TRÁILER, FECHA, MÚSICA, VENTAS…)",
  "es_personaje": true o false (si la etiqueta es un personaje),
  "grupo_capturas": "uno de: %s",
  "gancho": "primera frase, máximo 80 caracteres: el dato concreto con la palabra clave (GTA 6, Vice City, Lucía…). Varía la forma (una afirmación directa, una cifra, un contraste, una cita corta…). NUNCA empieces por «¿Sabías que» ni hagas una pregunta, y no prometas ni exageres nada que no diga la fuente",
  "cuerpo": ["3 a 6 trozos de máximo 45 caracteres cada uno, que se leen seguidos. Punto al acabar cada frase; si la frase sigue en el trozo siguiente, no pongas coma al final salvo que la gramática la pida"],
  "cierre": "pregunta final para comentar, máximo 60 caracteres",
  "texto_post": "2 o 3 frases para el texto de la publicación (sin hashtags); la primera, con «GTA 6» y el tema concreto, porque es lo que se busca",
  "cosas_reales": ["cada cosa REAL y concreta que se nombra en el guion y que NO sale en el juego (un restaurante, un producto, una persona, una portada, una tienda, un evento…), con su nombre propio tal cual, una por elemento (si se nombran dos restaurantes, son dos); [] si todo se puede enseñar con capturas del juego"],
  "imagen_del_juego": true o false (false si lo que se cuenta es algo real que NO sale en el juego y tiene su propia imagen: un producto o aparato, una persona, una portada, un evento, un anuncio, una tienda…; true si se puede enseñar con capturas del juego),
  "capturas": ["2 o 3 nombres EXACTOS del CATÁLOGO DE CAPTURAS que enseñen lo que se cuenta (el mismo personaje o lugar); si hay un trozo de VÍDEO que encaje, pon uno (como mucho dos)"],
  "hashtags": ["1 o 2 hashtags del tema, sin tildes, p. ej. #ViceCity o #Lucia"],
  "titulo_youtube": "título para YouTube de menos de 70 caracteres que empiece por «GTA 6» o por el nombre concreto (Vice City, Lucía, Jason…) y diga el dato; sin preguntas, sin exagerar y sin engañar"
}""" % ", ".join(GRUPOS)

AYUDA_GRUPOS = """Grupos de capturas oficiales (elige el que mejor case con lo que se cuenta; si es algo general como fechas, precio, ventas o tráileres, usa Jason_and_Lucia o Vice_City):
Jason_and_Lucia (los dos protagonistas), Jason_Duval, Lucia_Caminos, Vice_City (la ciudad), Leonida_Keys (los cayos),
Grassrivers (humedales), Port_Gellhorn, Ambrosia, Mount_Kalaga_National_Park, y personajes: Boobie_Ike, Brian_Heder,
Cal_Hampton, DreQuan_Priest, Raul_Bautista, Real_Dimez."""


def catalogo(grupo=None):
    """Lista «Nombre: qué se ve» de las capturas que se pueden usar (todas o las de un grupo).
    Solo las principales; las secundarias entran únicamente si el grupo tiene menos de 3 principales."""
    del_grupo = [(n, c) for n, c in sorted(CAPTURAS.items()) if grupo is None or c["grupo"] == grupo]
    principales = [(n, c) for n, c in del_grupo if c["uso"] == "principal"]
    if grupo and len(principales) < 3:
        principales = [(n, c) for n, c in del_grupo if c["uso"] in ("principal", "secundaria")]
    filas = [f"{n} (VÍDEO, {c['dur']:.0f} s): {c['que']}" if c.get("tipo") == "trozo" else f"{n}: {c['que']}"
             for n, c in principales]
    return "CATÁLOGO DE CAPTURAS (nombre: qué se ve):\n" + "\n".join(filas)


def pregunta(t):
    t = t.strip().rstrip(".")
    if not t.endswith("?"):
        t += "?"
    if "¿" not in t:
        t = "¿" + t[:1].upper() + t[1:]
    return t


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
        "trozos": [_limpiar(j["gancho"], 95)] + cuerpo[:6] + [pregunta(_limpiar(j["cierre"], 75))],
        "capturas": validas(", ".join(str(c) for c in (j.get("capturas") or []))),
        "texto_post": _limpiar(j.get("texto_post"), 600),
        "hashtags": hashtags(j.get("hashtags")),
        "titulo": _limpiar(j.get("titulo_youtube"), 95),
        "imagen_juego": j.get("imagen_del_juego") is not False and not j.get("cosas_reales"),
        "cosas": [_limpiar(str(c), 60) for c in (j.get("cosas_reales") or []) if str(c).strip()][:3],
    }


def caption(g, fuente, oficial, voz_reserva=False):
    linea = f"Fuente: {fuente}" + ("" if oficial else " (según medios)")
    extra = "\nVoz: sharvard (CC BY 3.0)" if voz_reserva else ""
    return f"{g['texto_post']}\n\n{linea}\n{PIE_POST}{extra}\n\n{g['hashtags']}"


def de_dato(dato):
    """Guion a partir de un dato del banco (columnas del CSV / tabla Datos)."""
    oficial = dato.get("Estado") == "Oficial"
    grupo = dato.get("Imagen sugerida") if dato.get("Imagen sugerida") in GRUPOS else None
    prompt = (REGLAS + "\n" + AYUDA_GRUPOS + "\n\nVas a contar un DATO o CURIOSIDAD de GTA 6. Es algo ya conocido, "
              "no una novedad: no digas que es nuevo, que se acaba de anunciar ni que Rockstar «comparte» o «revela» nada hoy.\n"
              f"Tema: {dato.get('Tema')}\nFuente: {dato.get('Fuente')} ({'oficial' if oficial else 'no oficial: atribúyelo'})\n"
              f"Grupo de capturas: {grupo or 'el que mejor case'}\n\n{catalogo(grupo)}\n\n"
              f"TEXTO DE LA FUENTE:\n{dato.get('Dato')}\n\n" + FORMATO)
    g = validar(gemini.texto_json(prompt))
    if grupo:
        g["grupo"] = grupo  # la imagen la decide el banco (regla de G2)
        g["capturas"] = [c for c in g["capturas"] if CAPTURAS[c]["grupo"] == grupo]
    return g


def de_noticia(medio, titulo, texto):
    oficial = medio in OFICIALES
    prompt = (REGLAS + "\n" + AYUDA_GRUPOS + "\n\nVas a contar una NOTICIA de hoy sobre GTA 6.\n"
              f"Medio: {medio} ({'oficial' if oficial else 'no oficial: di «Según ' + medio + '»'})\n"
              f"Titular original: {titulo}\n\n{catalogo()}\n\nTEXTO DE LA FUENTE:\n{texto[:7000]}\n\n" + FORMATO)
    g = validar(gemini.texto_json(prompt))
    if g["capturas"]:  # el grupo, el de la primera captura elegida
        g["grupo"] = CAPTURAS[g["capturas"][0]]["grupo"]
    return g


def guion_a_texto(trozos):
    return "\n".join(trozos)


def texto_a_guion(texto):
    return [l.strip() for l in (texto or "").splitlines() if l.strip()]
