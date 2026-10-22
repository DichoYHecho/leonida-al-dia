"""Imagen de lo que cuenta una noticia cuando no es algo que se vea en las capturas del juego (un producto,
una persona, una portada, un evento…). Decidido el 22 oct:

1. Primero, la imagen oficial de quien lo anuncia: la página oficial enlazada desde la noticia (Rockstar,
   Take-Two, PlayStation, Xbox…) o la propia noticia si es de Rockstar Newswire.
2. Si no hay, la imagen principal de la noticia del medio (Vandal, 3DJuegos…), con su crédito.
3. Si no hay ninguna, el vídeo sale con capturas del juego y un aviso en «Avisos».

En Airtable se guarda en «Capturas» como «imagen[Crédito]:https://…» (así se puede rehacer el vídeo otro día).
La imagen descargada se guarda en la caché de las voces, que se conserva entre ejecuciones."""
import hashlib, io, os, re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import requests
from PIL import Image
from config import CACHE, UA, FUENTES_RSS

DIR = os.path.join(CACHE, "voces", "imagenes")
TOKEN = re.compile(r"imagen\[([^\]]*)\]:(https?://[^\s,]+)")
OFICIALES = [("rockstargames.com", "Rockstar Games"), ("take2games.com", "Take-Two"),
             ("blog.playstation.com", "PlayStation"), ("playstation.com", "PlayStation"),
             ("news.xbox.com", "Xbox"), ("xbox.com", "Xbox"), ("nintendo.com", "Nintendo")]
MEDIOS = {urlparse(u).netloc.replace("www.", "").split(".")[-2]: m for m, u in FUENTES_RSS}
MEDIOS.update({"vandal": "Vandal", "3djuegos": "3DJuegos", "videogameschronicle": "VGC", "pushsquare": "Push Square"})
MIN_ANCHO = 600
NAVEGACION = re.compile(r"legal|privacy|privacidad|terms|support|soporte|store|tienda|login|account|cookies|/tag/|/category/", re.I)


class _Pagina(HTMLParser):
    """Saca la imagen principal (og:image / twitter:image) y los enlaces del cuerpo de la página."""
    def __init__(self):
        super().__init__()
        self.imagen, self.enlaces = None, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta" and not self.imagen:
            clave = (a.get("property") or a.get("name") or "").lower()
            if clave in ("og:image", "og:image:secure_url", "twitter:image", "twitter:image:src") and a.get("content"):
                self.imagen = a["content"].strip()
        elif tag == "a" and a.get("href"):
            self.enlaces.append(a["href"].strip())


def _leer(url):
    r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    p = _Pagina()
    p.feed(r.text[:2_000_000])
    return urljoin(url, p.imagen) if p.imagen else None, [urljoin(url, e) for e in p.enlaces]


def credito_oficial(url):
    host = urlparse(url).netloc.lower()
    return next((nombre for dominio, nombre in OFICIALES if host == dominio or host.endswith("." + dominio)), None)


def credito_medio(url, medio):
    host = urlparse(url).netloc.lower().replace("www.", "")
    clave = host.split(".")[-2] if host.count(".") else host
    return MEDIOS.get(clave) or medio


def buscar(c):
    """c = noticia (medio, enlace). Devuelve (url de la imagen, crédito, 'oficial'|'medio') o None."""
    try:
        img, enlaces = _leer(c["enlace"])
    except Exception as e:
        print(f"  No se pudo leer la noticia para buscar su imagen: {str(e)[:120]}", flush=True)
        return None
    propio = credito_oficial(c["enlace"])
    if propio and img and descargar(img):
        return img, propio, "oficial"
    vistos = set()
    for e in enlaces:  # la primera página oficial enlazada desde la noticia que tenga imagen
        e = e.split("#")[0]
        partes = [x for x in urlparse(e).path.split("/") if x]
        if e in vistos or not credito_oficial(e) or len(partes) < 2 or NAVEGACION.search(e):
            continue
        vistos.add(e)
        if len(vistos) > 4:
            break
        try:
            oimg, _ = _leer(e)
        except Exception:
            continue
        if oimg and descargar(oimg):
            return oimg, credito_oficial(e), "oficial"
    if img and descargar(img):
        return img, credito_medio(c["enlace"], c.get("medio")), "medio"
    return None


def token(url, credito):
    return f"imagen[{credito}]:{url}"


def leer_tokens(texto):
    """[(token, crédito, url)] de lo escrito en «Capturas»."""
    return [(m.group(0), m.group(1).strip() or "fuente de la noticia", m.group(2)) for m in TOKEN.finditer(texto or "")]


def ruta(url):
    return os.path.join(DIR, hashlib.sha256(url.encode()).hexdigest()[:20] + ".jpg")


def descargar(url):
    """Descarga la imagen (si no está ya) y la guarda en JPG. Devuelve la ruta, o None si no sirve."""
    p = ruta(url)
    if os.path.exists(p):
        return p
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=60)
        r.raise_for_status()
        im = Image.open(io.BytesIO(r.content))
        im.load()
    except Exception as e:
        print(f"  Imagen no válida ({url[:80]}): {str(e)[:100]}", flush=True)
        return None
    if im.width < MIN_ANCHO:
        print(f"  Imagen demasiado pequeña ({im.width}×{im.height}): {url[:80]}", flush=True)
        return None
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        fondo = Image.new("RGB", im.size, (255, 255, 255))
        fondo.paste(im, mask=im.split()[-1])
        im = fondo
    im = im.convert("RGB")
    if im.width > 2400:
        im = im.resize((2400, round(im.height * 2400 / im.width)), Image.LANCZOS)
    os.makedirs(DIR, exist_ok=True)
    im.save(p, quality=90)
    return p
