"""Imagen de lo que cuenta una noticia cuando no es algo que se vea en las capturas del juego (un producto,
una persona, una portada, un evento…). Decidido el 22 oct:

1. Primero, la imagen oficial de quien lo anuncia: la página oficial enlazada desde la noticia (Rockstar,
   Take-Two, PlayStation, Xbox…) o la propia noticia si es de Rockstar Newswire.
2. Si no hay, la imagen principal de la noticia del medio (Vandal, 3DJuegos…), con su crédito.
3. Si no hay ninguna, el vídeo sale con capturas del juego y un aviso en «Avisos».

Desde el 23 oct: si la noticia nombra varias cosas reales (p. ej. dos restaurantes), se busca una imagen de CADA
una (buscar_todas): Gemini mira las imágenes candidatas (la oficial y las de la noticia) y dice cuál enseña cada cosa.
Si falta la imagen de alguna, la noticia no se propone (decidido el 23 oct: no puede salir un vídeo así).

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
NO_FOTO = re.compile(r"logo|avatar|icon|sprite|favicon|badge|banner-ad|/ads?/|pixel|1x1|placeholder|\.svg|\.gif", re.I)
NAVEGACION = re.compile(r"legal|privacy|privacidad|terms|support|soporte|store|tienda|login|account|cookies|/tag/|/category/", re.I)


class _Pagina(HTMLParser):
    """Saca la imagen principal (og:image / twitter:image) y los enlaces del cuerpo de la página."""
    def __init__(self):
        super().__init__()
        self.imagen, self.enlaces, self.fotos = None, [], []

    @staticmethod
    def _mayor(srcset):
        mejor, ancho = None, -1
        for parte in (srcset or "").split(","):
            trozos = parte.strip().split()
            if not trozos:
                continue
            w = int(re.sub(r"\D", "", trozos[1]) or 0) if len(trozos) > 1 and trozos[1].endswith("w") else 0
            if w >= ancho:
                mejor, ancho = trozos[0], w
        return mejor

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta" and not self.imagen:
            clave = (a.get("property") or a.get("name") or "").lower()
            if clave in ("og:image", "og:image:secure_url", "twitter:image", "twitter:image:src") and a.get("content"):
                self.imagen = a["content"].strip()
        elif tag == "a" and a.get("href"):
            self.enlaces.append(a["href"].strip())
        elif tag in ("img", "source"):  # las fotos del cuerpo de la noticia (23 oct)
            src = (self._mayor(a.get("srcset") or a.get("data-srcset")) or a.get("data-src") or a.get("data-lazy-src")
                   or a.get("data-original") or a.get("src"))
            if src and not src.startswith("data:") and not NO_FOTO.search(src):
                self.fotos.append(src.strip())


def _pagina(url):
    r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    p = _Pagina()
    p.feed(r.text[:2_000_000])
    return p


def _leer(url):
    p = _pagina(url)
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


def cosas_de(guion):
    """Las cosas reales que nombra un guion ya hecho y que hay que enseñar con su imagen (para la repesca)."""
    import gemini
    j = gemini.texto_json("De este guion de un vídeo sobre GTA 6, lista cada cosa REAL y concreta que se nombra y que "
                          "NO sale en el juego (un restaurante, un producto, una persona, una tienda, un evento…), con su "
                          "nombre propio y una por elemento. Si no hay ninguna, lista vacía.\n"
                          f"GUION:\n{guion}\n\nDevuelve SOLO un JSON: {{\"cosas\": [\"…\"]}}", 0.1)
    return [str(c).strip()[:60] for c in j.get("cosas", []) if str(c).strip()][:3]


def buscar_todas(c, cosas):
    """Una imagen para CADA cosa de «cosas» (decidido el 23 oct). c = noticia (medio, enlace).
    Devuelve ([(url, crédito, 'oficial'|'medio')] en el orden de «cosas», [cosas sin imagen])."""
    import gemini
    cands = []  # (url, crédito, origen)
    oficial = buscar(c)  # la oficial de siempre (o la principal de la noticia)
    if oficial:
        cands.append(oficial)
    try:
        p = _pagina(c["enlace"])
        medio = credito_oficial(c["enlace"]) or credito_medio(c["enlace"], c.get("medio"))
        origen = "oficial" if credito_oficial(c["enlace"]) else "medio"
        for u in ([p.imagen] if p.imagen else []) + p.fotos:
            u = urljoin(c["enlace"], u)
            if all(u != x[0] for x in cands):
                cands.append((u, medio, origen))
    except Exception as e:
        print(f"  No se pudieron leer las fotos de la noticia: {str(e)[:120]}", flush=True)
    buenas = []
    for u, cr, o in cands:
        if len(buenas) >= 12:
            break
        r = descargar(u)
        if r:
            buenas.append((u, cr, o, r))
    if not buenas:
        return [], list(cosas)
    lista = "\n".join(f"{i}. {x}" for i, x in enumerate(cosas, 1))
    prompt = (f"Estas son imágenes de una noticia. Para cada una de estas cosas reales:\n{lista}\n"
              "di qué imagen la enseña de verdad y con claridad (una foto o imagen de ESA cosa concreta, no de otra "
              "parecida; ni logotipos sueltos, ni mapas, ni capturas de pantalla de webs, ni anuncios). "
              "Una imagen distinta para cada cosa. Si ninguna la enseña, pon null.\n"
              f'Devuelve SOLO un JSON con una lista de {len(cosas)} elementos, en el mismo orden que las cosas: '
              '{"imagenes": [número de imagen o null, …]}')
    try:
        j = gemini.imagenes_json(prompt, [b[3] for b in buenas])
    except Exception as e:
        print(f"  Gemini no pudo mirar las imágenes: {str(e)[:150]}", flush=True)
        return [], list(cosas)
    elegidas, faltan, usadas = [], [], set()
    numeros = j.get("imagenes") if isinstance(j.get("imagenes"), list) else []
    for k, cosa in enumerate(cosas):
        n = numeros[k] if k < len(numeros) else None
        try:
            n = int(n)
        except (TypeError, ValueError):
            n = None
        if n and 1 <= n <= len(buenas) and n not in usadas:
            usadas.add(n)
            elegidas.append(buenas[n - 1][:3])
        else:
            faltan.append(cosa)
    return elegidas, faltan


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
