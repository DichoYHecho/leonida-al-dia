"""Material oficial de rockstargames.com/VI/media para el fondo de los vídeos.

- Capturas (99 en 15 grupos), revisadas una a una el 20 oct. `capturas.csv`: qué se ve, el foco
  (0 = izquierda, 1 = derecha) para el recorte vertical y si se usa. Se descargan del archivo oficial
  «Descargar todo» y se guardan reducidas en la caché de GitHub (no se suben al repositorio).
- Trozos de vídeo de «Una mirada extendida» (`trozos.csv`, revisados uno a uno el 21 oct, sin destripes):
  se cortan del MP4 oficial ya en vertical y se guardan en la caché de GitHub. Se usan SIN su sonido (con nuestra
  música), porque es diálogo de misiones con tacos o canciones con derechos (decidido el 21 oct).
  Para dejar de usarlos (por ejemplo, si llega una reclamación), basta con poner «no usar» en `trozos.csv`."""
import csv, hashlib, io, os, re, subprocess, zipfile
import requests
from PIL import Image
from config import AQUI, CACHE, ZIP_CAPTURAS, UA, VIDEO_OFICIAL
import clips, imagenes

DIR = os.path.join(CACHE, "capturas")
DIR_TROZOS = os.path.join(CACHE, "trozos")
ALTO = 2048  # el vídeo usa 1920 × 1,06


def tabla():
    with open(os.path.join(AQUI, "capturas.csv"), encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    return {r["Captura"]: {"grupo": r["Grupo"], "que": r["Qué se ve"], "foco": float(r["Foco (0 izquierda - 1 derecha)"]),
                           "plano": r["Plano"], "uso": r["Uso"], "notas": r["Notas"], "tipo": "captura"} for r in filas}


def con_sonido_csv(r):
    return (r.get("Sonido") or "no").strip().lower() in ("si", "sí")


def tabla_trozos(archivo="trozos.csv"):
    p = os.path.join(AQUI, archivo)
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    return {r["Trozo"]: {"grupo": r["Grupo"], "que": r["Qué se ve"], "foco": float(r["Foco (0 izquierda - 1 derecha)"]),
                         "plano": "vídeo con sonido" if con_sonido_csv(r) else "vídeo", "uso": r["Uso"],
                         "notas": r["Notas"], "tipo": "trozo", "sonido": con_sonido_csv(r),
                         "inicio": float(r["Inicio (s)"]), "dur": float(r["Duración (s)"])} for r in filas}


CAPTURAS = tabla()
GRUPOS = sorted({c["grupo"] for c in CAPTURAS.values()})
TROZOS = {n: t for n, t in tabla_trozos().items() if t["grupo"] in GRUPOS}
CAPTURAS.update(TROZOS)  # para Airtable, un trozo es una «captura» más (con nombre propio)


def es_trozo(nombre):
    return CAPTURAS.get(nombre, {}).get("tipo") == "trozo"


def con_sonido(nombre):
    """Trozo que se usa con su sonido oficial (columna «Sonido» = si). Por ahora, ninguno (decidido el 21 oct)."""
    return bool(CAPTURAS.get(nombre, {}).get("sonido"))


def preparar():
    """Deja las capturas y los trozos en la caché (solo descarga lo que falte)."""
    preparar_trozos()
    faltan = [n for n, c in CAPTURAS.items() if c["tipo"] == "captura" and not os.path.exists(os.path.join(DIR, n + ".jpg"))]
    if not faltan:
        return 0
    os.makedirs(DIR, exist_ok=True)
    print(f"Descargando las capturas oficiales (faltan {len(faltan)})…", flush=True)
    r = requests.get(ZIP_CAPTURAS, headers={"User-Agent": UA}, timeout=600)
    r.raise_for_status()
    hechas = 0
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        for info in z.infolist():
            m = re.search(r"([A-Za-z_]+?_\d\d)\.(jpe?g|png)$", os.path.basename(info.filename), re.I)
            if not m:
                continue
            nombre = next((n for n, c in CAPTURAS.items() if c["tipo"] == "captura"
                           and (m.group(1).endswith(n) or n.endswith(m.group(1)))), None)
            if not nombre:
                continue
            im = Image.open(io.BytesIO(z.read(info))).convert("RGB")
            if im.height > ALTO:
                im = im.resize((round(im.width * ALTO / im.height), ALTO), Image.LANCZOS)
            im.save(os.path.join(DIR, nombre + ".jpg"), quality=90)
            hechas += 1
    print(f"Capturas preparadas: {hechas}", flush=True)
    return hechas


def cortar(nombre, t, destino):
    """Corta un trozo del MP4 oficial (solo descarga ese trozo) en vertical, centrado en su foco, con sonido."""
    x = f"min(max(0\\,{t['foco']:.3f}*iw-540)\\,iw-1080)"
    tmp = destino + ".tmp.mp4"
    for _ in range(3):
        r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t['inicio']:.2f}", "-t", f"{t['dur']:.2f}",
                            "-user_agent", UA, "-reconnect", "1", "-reconnect_on_network_error", "1",
                            "-reconnect_delay_max", "10", "-i", VIDEO_OFICIAL,
                            "-vf", f"scale=-2:1920,crop=1080:1920:{x}:0,fps=30", "-c:v", "libx264", "-crf", "18",
                            "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-ar", "44100",
                            "-ac", "2", tmp])
        if r.returncode == 0 and os.path.getsize(tmp) > 10000:
            os.replace(tmp, destino)
            return True
    print(f"  ⚠️ No se pudo cortar el trozo {nombre}", flush=True)
    return False


def preparar_trozos():
    faltan = [n for n, t in TROZOS.items() if t["uso"] != "no usar"
              and not os.path.exists(os.path.join(DIR_TROZOS, n + ".mp4"))]
    if not faltan:
        return 0
    os.makedirs(DIR_TROZOS, exist_ok=True)
    print(f"Cortando los trozos del vídeo oficial (faltan {len(faltan)})…", flush=True)
    hechos = sum(cortar(n, TROZOS[n], os.path.join(DIR_TROZOS, n + ".mp4")) for n in faltan)
    print(f"Trozos preparados: {hechos}", flush=True)
    return hechos


def es_imagen(nombre):
    """«imagen[Crédito]:https://…»: imagen de lo que cuenta la noticia, que no es una captura del juego (22 oct)."""
    return bool(imagenes.TOKEN.fullmatch(nombre or ""))


def credito(nombre):
    m = imagenes.TOKEN.fullmatch(nombre or "")
    return (m.group(1).strip() or "fuente de la noticia") if m else "Rockstar Games"


def foco_plano(nombre):
    if clips.es_clip(nombre):  # tu partida (clips.py): ya está en vertical y sin sonido
        return 0.5, "vídeo"
    if es_imagen(nombre):
        return 0.5, "imagen"
    return CAPTURAS[nombre]["foco"], CAPTURAS[nombre]["plano"]


def ruta_sin_comprobar(nombre):
    if clips.es_clip(nombre):
        return clips.preparar(nombre) or clips.ruta(nombre)
    if es_imagen(nombre):
        url = imagenes.TOKEN.fullmatch(nombre).group(2)
        return imagenes.descargar(url) or imagenes.ruta(url)
    return os.path.join(DIR_TROZOS, nombre + ".mp4") if es_trozo(nombre) else os.path.join(DIR, nombre + ".jpg")


def ruta(nombre):
    p = ruta_sin_comprobar(nombre)
    if not os.path.exists(p):
        raise RuntimeError(f"no tengo la captura {nombre}")
    return p


def elegir(grupo, semilla, cuantas=2):
    """Capturas para un vídeo: las principales del grupo (y si no llegan, las secundarias),
    rotando según la semilla para no repetir siempre las mismas."""
    if grupo not in GRUPOS:
        grupo = "Vice_City"
    principales = sorted(n for n, c in CAPTURAS.items() if c["grupo"] == grupo and c["uso"] == "principal" and c["tipo"] == "captura")
    secundarias = sorted(n for n, c in CAPTURAS.items() if c["grupo"] == grupo and c["uso"] == "secundaria" and c["tipo"] == "captura")
    lista = principales or secundarias
    k = int(hashlib.sha256(str(semilla).encode()).hexdigest(), 16) % len(lista)
    orden = lista[k:] + lista[:k]
    # Hasta el lanzamiento, primero las capturas nuevas de «The Launch Gallery» (5 nov)
    nuevas = [n for n in orden if "nueva" in CAPTURAS[n]["notas"]]
    orden = nuevas + [n for n in orden if n not in nuevas]
    elegidas = orden[:cuantas]
    if len(elegidas) < cuantas:
        elegidas += [s for s in secundarias if s not in elegidas][:cuantas - len(elegidas)]
    return elegidas


def validas(nombres):
    """Limpia la lista escrita en Airtable: solo capturas que existen y no están marcadas «no usar»."""
    out = [m.group(0) for m in clips.TOKEN.finditer(nombres or "")]  # los clips de tus partidas van tal cual
    out += [t for t, _, _ in imagenes.leer_tokens(nombres)]  # las imágenes de la noticia van tal cual
    for n in re.split(r"[,\s]+", imagenes.TOKEN.sub(" ", clips.TOKEN.sub(" ", nombres or ""))):
        n = n.strip()
        if n in CAPTURAS and CAPTURAS[n]["uso"] != "no usar" and n not in out:
            out.append(n)
    return out
