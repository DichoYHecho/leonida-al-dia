"""Encuadre inteligente (25 oct 2026): qué hay que enseñar de cada imagen en el vídeo vertical.

El vídeo vertical solo enseña una franja estrecha de una imagen apaisada (un 30 % del ancho). Antes se centraba en
el «foco» de capturas.csv (o en el centro, en las imágenes de las noticias) y a veces salía, por ejemplo, el hombro
de Jason en vez de las caras. Ahora Gemini mira la imagen y dice dónde están las caras (o lo importante), y el
vídeo encuadra eso: si cabe todo, se acerca a ello; si no cabe (Jason a un lado y Lucía al otro), la cámara va de
uno a otro.

- Se pregunta 1 vez por imagen y se guarda en la caché de GitHub (cache/voces/encuadres/<huella>.json).
- Si Gemini falla, no se guarda nada y el vídeo usa el foco de siempre."""
import hashlib, json, os
from config import CACHE

DIR = os.path.join(CACHE, "voces", "encuadres")  # dentro de la caché de las voces, que guardan todas las tareas
VERSION = "2"

PROMPT = """Esta imagen va a salir de fondo en un vídeo vertical (9:16) que solo enseña una franja estrecha de ella.
Dime qué tiene que verse para que la imagen se entienda y sea interesante:
- Si hay personas o personajes, sus CARAS: la caja de cada persona es SOLO su cabeza (de la coronilla a la barbilla),
  aunque se vea el cuerpo entero. Todas las caras que se vean bien.
- Si no hay caras, el objeto, vehículo, edificio, animal o cartel principal.
{contexto}
Devuelve SOLO este JSON, como mucho 4 sujetos, el más importante primero:
{{"sujetos": [{{"que": "descripción corta", "box_2d": [ymin, xmin, ymax, xmax]}}]}}
Las coordenadas van de 0 a 1000 respecto al alto (y) y al ancho (x) de la imagen."""


def huella(ruta):
    h = hashlib.sha1(VERSION.encode())
    with open(ruta, "rb") as f:
        h.update(f.read())
    return h.hexdigest()[:20]


def sujetos(ruta, contexto=""):
    """[{"que", "caja": (x0, y0, x1, y1) de 0 a 1}] o [] si no se sabe."""
    try:
        os.makedirs(DIR, exist_ok=True)
        cache = os.path.join(DIR, huella(ruta) + ".json")
        if os.path.exists(cache):
            return json.load(open(cache))
        import gemini
        ctx = f"Contexto: la imagen acompaña a esta noticia o dato: «{contexto[:300]}»." if contexto else ""
        d = gemini.imagenes_json(PROMPT.format(contexto=ctx), [ruta])
        out = []
        for s in (d.get("sujetos") or [])[:4]:
            b = s.get("box_2d") or []
            if len(b) != 4:
                continue
            y0, x0, y1, x1 = [min(max(float(v) / 1000, 0.0), 1.0) for v in b]
            if x1 - x0 < 0.01 or y1 - y0 < 0.01:
                continue
            out.append({"que": str(s.get("que", ""))[:80], "caja": (x0, y0, x1, y1)})
        json.dump(out, open(cache, "w"), ensure_ascii=False)
        return out
    except Exception as e:
        print(f"  (encuadre sin Gemini: {str(e)[:150]})", flush=True)
        return []
