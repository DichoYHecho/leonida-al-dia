"""Guiones con Gemini, siempre a partir de un texto comprobado (la noticia o el dato del banco).

Reglas (apartado 5 del plan): nada que no diga la fuente; «Rockstar confirma» solo si es oficial;
nada de filtraciones, rumores como hechos ni destripes; sin enlaces para comprar; parafrasear."""
import csv, datetime, os, re, unicodedata
import gemini
from config import HASHTAGS_FIJOS, PIE_POST, OFICIALES
from medios import GRUPOS, CAPTURAS, validas

REGLAS = """Eres el guionista de «Leónida al Día», una cuenta de fans de GTA 6 en español de España.
Escribes vídeos verticales de 25 a 40 segundos (unas 85-115 palabras en total) que lee una voz sintética.
Cada vídeo tiene que enseñar algo de verdad: no un dato suelto, sino el dato con sus detalles y su contexto, como lo contaría
un youtuber de gaming que se lo explica a un amigo, con guasa suave. Cada frase aporta información nueva: nada de relleno,
frases hechas ni muletillas de anuncio («increíble», «sin duda», «prepárate», «no te lo vas a creer»).
Reglas que no se pueden saltar:
- Usa SOLO la información del TEXTO DE LA FUENTE (y de los DATOS RELACIONADOS, si los hay). No añadas datos, cifras, fechas ni opiniones que no estén ahí.
- Si la fuente no es oficial (Rockstar Games o Take-Two), atribúyelo: «Según {medio}…», en el primer trozo del cuerpo (nunca en el gancho). «Rockstar confirma» solo si lo dice Rockstar o Take-Two.
- Nada de filtraciones (material filtrado), rumores presentados como hechos ni destripes de la historia.
- No copies frases literales de la fuente: cuéntalo con tus palabras.
- No invites a comprar ni a reservar, y no pongas enlaces.
- Frases cortas y claras, tono cercano y natural (no de anuncio), sin exagerar ni engañar. Nada de mayúsculas sostenidas ni emojis.
- Escribe los números como se dicen si es raro leerlos («GTA 6», «19 de noviembre», «30 euros»).
- Usa bien los signos del español: «¿…?» y «¡…!». La pregunta final siempre entre «¿» y «?».
- No hagas predicciones ni especules sobre lo que pasará en el juego, en la historia ni en las ventas.
- Atribuye a quien lo dijo de verdad («según Rob Nelson, de Rockstar», «según IGN»), nunca a la web que lo copia (lo que va tras «vía»).
  Si dos datos vienen de la misma persona o medio, no repitas la atribución.
- No partas un nombre propio ni una cifra entre dos trozos; cada trozo, un bloque de sentido.
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
  "gancho": "primera frase, máximo 60 caracteres (8-10 palabras), que sale en grande en la portada: lo más llamativo y concreto del vídeo (una cifra, un nombre, un contraste) con la palabra clave (GTA 6, Vice City, Lucía…). Sin nombrar al medio ni empezar por «Según», «Repasamos», «Conoce» o «Descubre». Varía la forma (una afirmación directa, una cifra, un contraste, una cita corta…). NUNCA empieces por «¿Sabías que» ni hagas una pregunta, y no prometas ni exageres nada que no diga la fuente",
  "cuerpo": ["12 a 16 trozos de máximo 45 caracteres cada uno, que se leen seguidos. Orden: primero el dato principal con sus detalles concretos (nombres, cifras, fechas); después los DATOS RELACIONADOS que encajen, enlazados con naturalidad, como en una conversación (p. ej. «Y ojo, porque…», «Pero hay más:»), con su atribución si no son oficiales; y al final una frase que lo una todo, sin opinar ni predecir. Punto al acabar cada frase; si la frase sigue en el trozo siguiente, no pongas coma al final salvo que la gramática la pida"],
  "cierre": "pregunta final para comentar, máximo 60 caracteres",
  "texto_post": "2 o 3 frases para el texto de la publicación (sin hashtags); la primera, con «GTA 6» y el tema concreto, porque es lo que se busca; sin empezar por «Conoce», «Repasamos», «Descubre», «Te contamos» ni «Según», y con las cifras en número (50 temas, 210 GB)",
  "cosas_reales": ["cada cosa REAL y concreta que se nombra en el guion y que NO sale en el juego (un restaurante, un producto, una persona, una portada, una tienda, un evento…), con su nombre propio tal cual, una por elemento (si se nombran dos restaurantes, son dos); [] si todo se puede enseñar con capturas del juego"],
  "imagen_del_juego": true o false (false si lo que se cuenta es algo real que NO sale en el juego y tiene su propia imagen: un producto o aparato, una persona, una portada, un evento, un anuncio, una tienda…; true si se puede enseñar con capturas del juego),
  "capturas": ["2 o 3 nombres EXACTOS del CATÁLOGO DE CAPTURAS que enseñen lo que se cuenta (el mismo personaje o lugar); si hay un trozo de VÍDEO que encaje, pon uno (como mucho dos)"],
  "hashtags": ["1 o 2 hashtags del tema, sin tildes, p. ej. #ViceCity o #Lucia"],
  "titulo_youtube": "título para YouTube de menos de 70 caracteres que empiece por «GTA 6» o por el nombre concreto (Vice City, Lucía, Jason…) y diga el dato; sin preguntas, sin exagerar y sin engañar; las cifras siempre en número (50 temas, 210 GB, 2 tráileres), nunca en letra"
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


NUMEROS = {"dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10,
           "once": 11, "doce": 12, "trece": 13, "catorce": 14, "quince": 15, "dieciséis": 16, "diecisiete": 17,
           "dieciocho": 18, "diecinueve": 19, "veinte": 20, "treinta": 30, "cuarenta": 40, "cincuenta": 50,
           "sesenta": 60, "setenta": 70, "ochenta": 80, "noventa": 90, "cien": 100, "doscientos": 200,
           "trescientos": 300, "cuatrocientos": 400, "quinientos": 500}

def en_cifras(t):
    """30 oct: en títulos y textos, las cifras en número («cincuenta temas» → «50 temas»). Solo números sueltos:
    si van juntos («doscientos diez») o con «y» o «mil» («treinta y dos»), se dejan como están."""
    if not t:
        return t
    partes = re.split(r"(\w+)", t)
    pos = list(range(1, len(partes), 2))
    raro = lambda w: w.lower() in NUMEROS or w.lower() in ("y", "mil")
    for k, i in enumerate(pos):
        if partes[i].lower() not in NUMEROS:
            continue
        vecinos = [partes[pos[k - 1]] if k > 0 else "", partes[pos[k + 1]] if k + 1 < len(pos) else ""]
        if not any(raro(w) for w in vecinos):
            partes[i] = str(NUMEROS[partes[i].lower()])
    return "".join(partes)

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
        "trozos": [_limpiar(j["gancho"], 95)] + cuerpo[:18] + [pregunta(_limpiar(j["cierre"], 75))],
        "capturas": validas(", ".join(str(c) for c in (j.get("capturas") or []))),
        "texto_post": en_cifras(_limpiar(j.get("texto_post"), 600)),
        "hashtags": hashtags(j.get("hashtags")),
        "titulo": en_cifras(_limpiar(j.get("titulo_youtube"), 95)),
        "imagen_juego": j.get("imagen_del_juego") is not False and not j.get("cosas_reales"),
        "cosas": [_limpiar(str(c), 60) for c in (j.get("cosas_reales") or []) if str(c).strip()][:3],
    }


# 27 oct: en YouTube la mitad de la gente deslizaba al empezar. El gancho es lo que se ve y se oye primero:
# si es una pregunta o empieza por «Según…», «¿Sabías…», «Repasamos»… se pide otro (el texto de Gemini es barato).
GANCHO_FLOJO = re.compile(r"^\W*(sab[ií]as|seg[uú]n\b|repasamos|conoce\b|descubre\b|te contamos)", re.I)
AVISO_GANCHO = ("\n\nOJO: el gancho anterior no valía (era una pregunta o empezaba por «Según», «¿Sabías…», «Repasamos» o "
                "«Conoce»). Escribe un gancho que sea una afirmación corta con lo más llamativo del dato. El texto de la publicación tampoco puede empezar así.")

def gancho_flojo(txt):
    txt = (txt or "").strip()
    return txt.startswith("¿") or txt.endswith("?") or bool(GANCHO_FLOJO.search(txt))

def palabras(g):
    return sum(len(t.split()) for t in g["trozos"])

AVISO_CORTO = ("\n\nOJO: el guion anterior era demasiado corto ({n} palabras) y se quedaba en un dato suelto. Escribe entre 85 y 115 "
               "palabras en total y usa al menos 2 de los DATOS RELACIONADOS, cada uno en su propia frase.")

def con_buen_gancho(prompt, intentos=3, min_palabras=0, min_usados=0):
    """Pide el guion; si el gancho es flojo o (9 nov) se queda corto, lo vuelve a pedir (como mucho «intentos» veces)
    y se queda el mejor. Solo gasta texto de Gemini, no voz."""
    g, mejor, aviso = None, None, ""
    for i in range(intentos):
        j = gemini.texto_json(prompt + aviso)
        g = validar(j)
        g["usados"] = len(set(str(x) for x in (j.get("datos_usados") or [])))
        flojo = gancho_flojo(g["trozos"][0]) or bool(GANCHO_FLOJO.search(g["texto_post"] or ""))  # 30 oct: también el texto
        corto = palabras(g) < min_palabras or g["usados"] < min_usados
        if not flojo and (mejor is None or palabras(g) > palabras(mejor)):
            mejor = g
        if not flojo and not corto:
            return g
        print(f"  (guion flojo o corto, {palabras(g)} palabras: se pide otro; usa {g['usados']} datos relacionados)", flush=True)
        aviso = (AVISO_GANCHO if flojo else "") + (AVISO_CORTO.format(n=palabras(g)) if corto else "")
    return mejor or g

def caption(g, fuente, oficial, voz_reserva=False):
    linea = f"Fuente: {fuente}" + ("" if oficial else " (según medios)")
    if g.get("fuentes_extra"):  # 9 nov: las fuentes de los datos relacionados
        linea += "\nTambién: " + "; ".join(g["fuentes_extra"])
    extra = "\nVoz: sharvard (CC BY 3.0)" if voz_reserva else ""
    return f"{g['texto_post']}\n\n{linea}\n{PIE_POST}{extra}\n\n{g['hashtags']}"


BANCO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "banco_datos.csv")
GENERICOS = {"Vice_City", "Jason_and_Lucia"}  # grupos que valen para casi todo: ahí se exige también el mismo tema

def sin_via(fuente):
    """9 nov: «IGN (entrevista a X), vía GamingBolt» → «IGN (entrevista a X)»: se atribuye a quien lo dijo, no a quien lo copia."""
    return re.sub(r",?\s*vía\s.*$", "", fuente or "").strip()

def relacionados(dato, maximo=3):
    """9 nov: los vídeos se quedaban en un dato suelto. Se añaden otros datos del banco sobre lo mismo (mismo personaje
    o lugar; en los grupos genéricos, además, el mismo tema), vigentes y ya comprobados, para dar contexto.
    Así la imagen sigue casando con lo que se dice."""
    try:
        with open(BANCO, encoding="utf-8") as fh:
            filas = list(csv.DictReader(fh))
    except Exception:
        return []
    hoy = datetime.date.today().isoformat()
    img, tema, orden = dato.get("Imagen sugerida"), dato.get("Tema"), str(dato.get("Orden") or "").strip()
    out = []
    for f in filas:
        if str(f.get("Orden") or "").strip() == orden or (f.get("Válido hasta") or "9999") < hoy:
            continue
        if not img or f.get("Imagen sugerida") != img or (img in GENERICOS and f.get("Tema") != tema):
            continue
        if (f.get("Dato") or "").strip() == (dato.get("Dato") or "").strip():
            continue
        out.append(f)
    return out[:maximo]

def de_dato(dato):
    """Guion a partir de un dato del banco (columnas del CSV / tabla Datos), con sus datos relacionados."""
    oficial = dato.get("Estado") == "Oficial"
    grupo = dato.get("Imagen sugerida") if dato.get("Imagen sugerida") in GRUPOS else None
    rel = relacionados(dato)
    if rel:
        extra = ("\n\nDATOS RELACIONADOS (también comprobados; úsalos para dar contexto y detalle, cada uno con su "
                 "atribución si no es oficial). OBLIGATORIO: usa al menos 2, cada uno en su propia frase:\n" + "\n".join(
                     f"R{k}. {r['Dato']} (Fuente: {sin_via(r['Fuente'])}{'; la misma que el dato principal: no repitas la atribución' if sin_via(r['Fuente']) == sin_via(dato.get('Fuente')) else ''}; {'oficial' if r.get('Estado') == 'Oficial' else 'no oficial: atribúyelo'})"
                     for k, r in enumerate(rel, 1)) +
                 "\nAñade al JSON el campo \"datos_usados\": [\"R1\", …] con los datos relacionados que has contado.")
    else:
        extra = ("\n\nNo hay datos relacionados: cuenta el dato con todos sus detalles y no rellenes con nada que no "
                 "diga el texto; en este caso el vídeo puede ser más corto.")
    prompt = (REGLAS + "\n" + AYUDA_GRUPOS + "\n\nVas a contar un DATO o CURIOSIDAD de GTA 6. Es algo ya conocido, "
              "no una novedad: no digas que es nuevo, que se acaba de anunciar ni que Rockstar «comparte» o «revela» nada hoy.\n"
              f"Tema: {dato.get('Tema')}\nFuente: {sin_via(dato.get('Fuente'))} ({'oficial' if oficial else 'no oficial: atribúyelo'})\n"
              f"Grupo de capturas: {grupo or 'el que mejor case'}\n\n{catalogo(grupo)}\n\n"
              f"TEXTO DE LA FUENTE (dato principal):\n{dato.get('Dato')}" + extra + "\n\n" + FORMATO)
    g = con_buen_gancho(prompt, min_palabras=80 if len(rel) >= 2 else (55 if rel else 0), min_usados=min(len(rel), 2))
    if grupo:
        g["grupo"] = grupo  # la imagen la decide el banco (regla de G2)
        g["capturas"] = [c for c in g["capturas"] if CAPTURAS[c]["grupo"] == grupo]
    g["fuentes_extra"] = list(dict.fromkeys(r["Fuente"] for r in rel if r.get("Fuente") and r["Fuente"] != dato.get("Fuente")))
    return g

def de_noticia(medio, titulo, texto):
    oficial = medio in OFICIALES
    prompt = (REGLAS + "\n" + AYUDA_GRUPOS + "\n\nVas a contar una NOTICIA de hoy sobre GTA 6.\n"
              f"Medio: {medio} ({'oficial' if oficial else 'no oficial: di «Según ' + medio + '»'})\n"
              f"Titular original: {titulo}\n\n{catalogo()}\n\nTEXTO DE LA FUENTE:\n{texto[:7000]}\n\n" + FORMATO)
    g = con_buen_gancho(prompt)
    if g["capturas"]:  # el grupo, el de la primera captura elegida
        g["grupo"] = CAPTURAS[g["capturas"][0]]["grupo"]
    return g


def guion_a_texto(trozos):
    return "\n".join(trozos)


def texto_a_guion(texto):
    return [l.strip() for l in (texto or "").splitlines() if l.strip()]
