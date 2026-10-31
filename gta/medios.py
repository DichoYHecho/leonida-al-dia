"""Material oficial de rockstargames.com/VI/media para el fondo de los vídeos.

- Capturas (99 en 15 grupos), revisadas una a una el 20 oct. `capturas.csv`: qué se ve, el foco
  (0 = izquierda, 1 = derecha) para el recorte vertical y si se usa. Se descargan del archivo oficial
  «Descargar todo» y se guardan reducidas en la caché de GitHub (no se suben al repositorio).
- Trozos de vídeo de «Una mirada extendida» (`trozos.csv`, revisados uno a uno el 21 oct, sin destripes):
  se cortan del MP4 oficial ya en vertical y se guardan en la caché de GitHub. Se usan SIN su sonido (con nuestra
  música), porque es diálogo de misiones con tacos o canciones con derechos (decidido el 21 oct).
  Para dejar de usarlos (por ejemplo, si llega una reclamación), basta con poner «no usar» en `trozos.csv`.
- 31 oct: más stock. Trozos también de los tráileres 1, 2 y de lanzamiento y de los clips oficiales (columna «Vídeo»
  de `trozos.csv`; «Lento» = 2 los pone a cámara lenta) y arte oficial en vertical (`arte.csv`, del zip de arte).
  `con_mas_video` añade trozos del grupo a los fondos para que haya más vídeo que fotos."""
import csv, hashlib, io, os, re, subprocess, tempfile, zipfile
import requests
from PIL import Image
from config import AQUI, CACHE, ZIP_CAPTURAS, UA, VIDEO_OFICIAL
import clips, imagenes

DIR = os.path.join(CACHE, "capturas")
DIR_TROZOS = os.path.join(CACHE, "trozos")
ALTO = 2048  # el vídeo usa 1920 × 1,06
ZIP_ARTE = "https://media-rockstargames-com.akamaized.net/VI/downloads/artwork_wallpapers/GTAVI_Artwork_Wallpapers.zip"
_V = "https://media-rockstargames-com.akamaized.net/VI/downloads/videos/"
VIDEOS = {"Mirada": VIDEO_OFICIAL,  # columna «Vídeo» de trozos.csv (vacía = Una mirada extendida)
          "Trailer_1": _V + "GTAVI_Trailer_1/GTAVI_Trailer_1.mp4",
          "Trailer_2": _V + "GTAVI_Trailer_2/GTAVI_Trailer_2.mp4",
          "Lanzamiento": _V + "GTAVI_Launch_Trailer/GTAVI_Launch_Trailer.mp4",
          "Clips": _V + "GTAVI_Videos.zip"}  # «Clips:<archivo>»: un clip del zip oficial
DIR_ZIP = os.path.join(tempfile.gettempdir(), "gtavi_clips")


def tabla():
    with open(os.path.join(AQUI, "capturas.csv"), encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    out = {r["Captura"]: {"grupo": r["Grupo"], "que": r["Qué se ve"], "foco": float(r["Foco (0 izquierda - 1 derecha)"]),
                           "plano": r["Plano"], "uso": r["Uso"], "notas": r["Notas"], "tipo": "captura"} for r in filas}
    p = os.path.join(AQUI, "arte.csv")  # 31 oct: arte oficial en vertical (zip de arte), como una captura más
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                out[r["Captura"]] = {"grupo": r["Grupo"], "que": r["Qué se ve"],
                                     "foco": float(r["Foco (0 izquierda - 1 derecha)"]), "plano": r["Plano"] or "retrato",
                                     "uso": r["Uso"], "notas": r["Notas"], "tipo": "captura", "archivo": r["Archivo"]}
    return out


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
                         "inicio": float(r["Inicio (s)"]), "dur": float(r["Duración (s)"]),
                         "video": (r.get("Vídeo") or "Mirada").strip(), "lento": float(r.get("Lento") or 1)} for r in filas}


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
    preparar_arte()
    faltan = [n for n, c in CAPTURAS.items() if c["tipo"] == "captura" and not c.get("archivo") and not os.path.exists(os.path.join(DIR, n + ".jpg"))]
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
            nombre = next((n for n, c in CAPTURAS.items() if c["tipo"] == "captura" and not c.get("archivo")
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
    src = origen(t.get("video") or "Mirada")
    lento = t.get("lento") or 1.0
    red = (["-user_agent", UA, "-reconnect", "1", "-reconnect_on_network_error", "1", "-reconnect_delay_max", "10"]
           if src.startswith("http") else [])
    audio = ["-an"] if lento != 1 else []  # a cámara lenta, sin sonido (no se usa)
    tmp = destino + ".tmp.mp4"
    for _ in range(3):
        r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t['inicio']:.2f}", "-t", f"{t['dur']:.2f}",
                            *red, "-i", src, *audio,
                            "-vf", f"setpts={lento:.3f}*PTS,scale=-2:1920,crop=1080:1920:{x}:0,fps=30", "-c:v", "libx264", "-crf", "18",
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


def origen(video):
    """URL del vídeo oficial o, para «Clips:<archivo>», el clip sacado del zip oficial de clips (se baja una vez)."""
    if not video.startswith("Clips:"):
        return VIDEOS.get(video, VIDEO_OFICIAL)
    p = os.path.join(DIR_ZIP, video.split(":", 1)[1])
    if not os.path.exists(p):
        os.makedirs(DIR_ZIP, exist_ok=True)
        r = requests.get(VIDEOS["Clips"], headers={"User-Agent": UA}, timeout=900)
        r.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            for info in z.infolist():
                if info.filename.lower().endswith(".mp4") and "__MACOSX" not in info.filename:
                    with open(os.path.join(DIR_ZIP, os.path.basename(info.filename)), "wb") as f:
                        f.write(z.read(info))
    return p


def preparar_arte():
    """Arte oficial en vertical (arte.csv): lo baja del zip de arte la primera vez y lo deja con las capturas."""
    faltan = {c["archivo"]: n for n, c in CAPTURAS.items()
              if c.get("archivo") and not os.path.exists(os.path.join(DIR, n + ".jpg"))}
    if not faltan:
        return 0
    os.makedirs(DIR, exist_ok=True)
    print(f"Descargando el arte oficial (faltan {len(faltan)})…", flush=True)
    r = requests.get(ZIP_ARTE, headers={"User-Agent": UA}, timeout=900)
    r.raise_for_status()
    hechas = 0
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        for info in z.infolist():
            n = faltan.get(os.path.basename(info.filename))
            if not n:
                continue
            im = Image.open(io.BytesIO(z.read(info))).convert("RGB")
            if im.height > ALTO:
                im = im.resize((round(im.width * ALTO / im.height), ALTO), Image.LANCZOS)
            im.save(os.path.join(DIR, n + ".jpg"), quality=90)
            hechas += 1
    print(f"Arte preparado: {hechas}", flush=True)
    return hechas


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
    elegidas = orden[:cuantas]
    if len(elegidas) < cuantas:
        elegidas += [s for s in secundarias if s not in elegidas][:cuantas - len(elegidas)]
    return elegidas


def elegir_trozos(grupo, semilla, cuantos=2):
    """Trozos de vídeo principales del grupo, en un orden distinto para cada semilla (31 oct). [] si no tiene."""
    lista = [n for n, c in CAPTURAS.items() if c["tipo"] == "trozo" and c["grupo"] == grupo and c["uso"] == "principal"]
    lista.sort(key=lambda n: hashlib.sha256((str(semilla) + n).encode()).hexdigest())
    return lista[:cuantos]


def con_mas_video(caps, grupo, semilla, maximo=5):
    """31 oct: más vídeo que fotos. A los fondos ya elegidos les añade trozos de vídeo del grupo hasta que haya más
    vídeo que fotos (como mucho «maximo» fondos y 2 fotos), alternando vídeo y foto. Si el primero es la imagen de la
    noticia o un clip de tus partidas, sigue el primero. Sin trozos en el grupo, se queda como estaba."""
    if not caps:
        return caps
    lider = caps[:1] if (es_imagen(caps[0]) or clips.es_clip(caps[0])) else []
    resto = caps[len(lider):]
    es_video = lambda c: es_trozo(c) or clips.es_clip(c)
    videos = [c for c in resto if es_video(c)]
    fotos = [c for c in resto if not es_video(c)][:2 if lider else 3]
    n_video = lambda: len(videos) + sum(es_video(c) for c in lider)
    n_foto = lambda: len(fotos) + len(lider) - sum(es_video(c) for c in lider)
    for t in elegir_trozos(grupo, semilla, maximo):
        if n_video() > n_foto() or len(lider) + len(videos) + len(fotos) >= maximo:
            break
        if t not in videos:
            videos.append(t)
    if not videos:
        return caps
    while fotos and n_foto() >= n_video() and len(fotos) > 1:
        fotos.pop()
    out = []
    for k in range(max(len(videos), len(fotos))):
        out += videos[k:k + 1] + fotos[k:k + 1]
    return lider + out


def validas(nombres):
    """Limpia la lista escrita en Airtable: solo capturas que existen y no están marcadas «no usar»."""
    out = [m.group(0) for m in clips.TOKEN.finditer(nombres or "")]  # los clips de tus partidas van tal cual
    out += [t for t, _, _ in imagenes.leer_tokens(nombres)]  # las imágenes de la noticia van tal cual
    for n in re.split(r"[,\s]+", imagenes.TOKEN.sub(" ", clips.TOKEN.sub(" ", nombres or ""))):
        n = n.strip()
        if n in CAPTURAS and CAPTURAS[n]["uso"] != "no usar" and n not in out:
            out.append(n)
    return out
