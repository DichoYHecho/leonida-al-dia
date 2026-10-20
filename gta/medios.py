"""Capturas oficiales de rockstargames.com/VI/media (99 en 15 grupos), revisadas una a una el 20 oct.

- `capturas.csv`: qué se ve, el foco (0 = izquierda, 1 = derecha) para el recorte vertical y si se usa.
- Las imágenes se descargan del archivo oficial «Descargar todo» y se guardan reducidas en la caché
  de GitHub (no se suben al repositorio)."""
import csv, hashlib, io, os, re, zipfile
import requests
from PIL import Image
from config import AQUI, CACHE, ZIP_CAPTURAS, UA

DIR = os.path.join(CACHE, "capturas")
ALTO = 2048  # el vídeo usa 1920 × 1,06


def tabla():
    with open(os.path.join(AQUI, "capturas.csv"), encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    return {r["Captura"]: {"grupo": r["Grupo"], "que": r["Qué se ve"], "foco": float(r["Foco (0 izquierda - 1 derecha)"]),
                           "plano": r["Plano"], "uso": r["Uso"], "notas": r["Notas"]} for r in filas}


CAPTURAS = tabla()
GRUPOS = sorted({c["grupo"] for c in CAPTURAS.values()})


def preparar():
    """Deja las 99 capturas en la caché (solo descarga si falta alguna)."""
    faltan = [n for n in CAPTURAS if not os.path.exists(os.path.join(DIR, n + ".jpg"))]
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
            nombre = next((n for n in CAPTURAS if m.group(1).endswith(n) or n.endswith(m.group(1))), None)
            if not nombre:
                continue
            im = Image.open(io.BytesIO(z.read(info))).convert("RGB")
            if im.height > ALTO:
                im = im.resize((round(im.width * ALTO / im.height), ALTO), Image.LANCZOS)
            im.save(os.path.join(DIR, nombre + ".jpg"), quality=90)
            hechas += 1
    print(f"Capturas preparadas: {hechas}", flush=True)
    return hechas


def ruta(nombre):
    p = os.path.join(DIR, nombre + ".jpg")
    if not os.path.exists(p):
        raise RuntimeError(f"no tengo la captura {nombre}")
    return p


def elegir(grupo, semilla, cuantas=2):
    """Capturas para un vídeo: las principales del grupo (y si no llegan, las secundarias),
    rotando según la semilla para no repetir siempre las mismas."""
    if grupo not in GRUPOS:
        grupo = "Vice_City"
    principales = sorted(n for n, c in CAPTURAS.items() if c["grupo"] == grupo and c["uso"] == "principal")
    secundarias = sorted(n for n, c in CAPTURAS.items() if c["grupo"] == grupo and c["uso"] == "secundaria")
    lista = principales or secundarias
    k = int(hashlib.sha256(str(semilla).encode()).hexdigest(), 16) % len(lista)
    orden = lista[k:] + lista[:k]
    elegidas = orden[:cuantas]
    if len(elegidas) < cuantas:
        elegidas += [s for s in secundarias if s not in elegidas][:cuantas - len(elegidas)]
    return elegidas


def validas(nombres):
    """Limpia la lista escrita en Airtable: solo capturas que existen y no están marcadas «no usar»."""
    out = []
    for n in re.split(r"[,\s]+", nombres or ""):
        n = n.strip()
        if n in CAPTURAS and CAPTURAS[n]["uso"] != "no usar" and n not in out:
            out.append(n)
    return out
