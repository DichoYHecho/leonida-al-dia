"""Tus partidas de GTA 6 (PS5) como fondo de los vídeos, desde el 19 de noviembre (decidido el 22 oct).

- Subes los clips a la carpeta de Google Drive «Leónida al Día - Clips» (cuenta adria.sanandreas). El nombre del
  archivo dice qué se ve (p. ej. «Lucía en moto por Vice City.mp4»). Sin destripes de la historia ni escenas.
- Se usan SIN su sonido (con nuestra música): la radio del juego tiene canciones con derechos.
- De cada clip se cogen 8 segundos del centro, en vertical (1080×1920).
- Para dejar de usar un clip: bórralo de la carpeta o pon «NO » al principio de su nombre.
Usa el mismo acceso de Google que youtube.py (secrets GOOGLE_*, permiso de solo lectura de Drive)."""
import json, os, re, subprocess
import requests
from config import CACHE
import youtube

CARPETA = "Leónida al Día - Clips"
DIR = os.path.join(CACHE, "clips")
TOKEN = re.compile(r"clip\[([^\]]*)\]:([A-Za-z0-9_-]{10,})")
DRIVE = "https://www.googleapis.com/drive/v3"
SEGUNDOS = 8
_LISTA = None


def _cabecera():
    t = youtube.token()
    if not t:
        raise RuntimeError("sin acceso a Google Drive (faltan los secrets GOOGLE_*)")
    return {"Authorization": f"Bearer {t}"}


def lista():
    """[(id, nombre)] de los clips de la carpeta (los más antiguos primero). [] si no hay acceso o no hay carpeta."""
    global _LISTA
    if _LISTA is not None:
        return _LISTA
    _LISTA = []
    try:
        h = _cabecera()
        q = f"name = '{CARPETA}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        r = requests.get(f"{DRIVE}/files", headers=h, params={"q": q, "fields": "files(id)"}, timeout=30)
        r.raise_for_status()
        carpetas = r.json().get("files", [])
        if not carpetas:
            print(f"Clips: no encuentro la carpeta «{CARPETA}» en Google Drive")
            return _LISTA
        q = f"'{carpetas[0]['id']}' in parents and trashed = false and mimeType contains 'video/'"
        r = requests.get(f"{DRIVE}/files", headers=h, timeout=30,
                         params={"q": q, "fields": "files(id,name)", "pageSize": 200, "orderBy": "createdTime"})
        r.raise_for_status()
        for f in r.json().get("files", []):
            nombre = os.path.splitext(f["name"])[0].strip()
            if not nombre.upper().startswith("NO "):
                _LISTA.append((f["id"], nombre))
        print(f"Clips de tus partidas en Drive: {len(_LISTA)}")
    except Exception as e:
        print(f"Clips: {str(e)[:200]}")
    return _LISTA


def token(fid, nombre):
    limpio = re.sub(r"[\[\],]", " ", nombre)
    limpio = re.sub(r"\s+", " ", limpio).strip()[:60]
    return f"clip[{limpio}]:{fid}"


def es_clip(nombre):
    return bool(TOKEN.fullmatch(nombre or ""))


def ruta(nombre):
    return os.path.join(DIR, TOKEN.fullmatch(nombre).group(2) + ".mp4")


def duracion(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", p],
                       capture_output=True, text=True)
    return float(json.loads(r.stdout or "{}").get("format", {}).get("duration") or 0)


def preparar(nombre):
    """Descarga el clip de Drive y deja 8 s en vertical y sin sonido en la caché. Devuelve la ruta (o None)."""
    destino = ruta(nombre)
    if os.path.exists(destino):
        return destino
    fid = TOKEN.fullmatch(nombre).group(2)
    os.makedirs(DIR, exist_ok=True)
    original = destino + ".orig"
    try:
        with requests.get(f"{DRIVE}/files/{fid}", headers=_cabecera(), params={"alt": "media"},
                          stream=True, timeout=600) as r:
            r.raise_for_status()
            with open(original, "wb") as f:
                for b in r.iter_content(1 << 20):
                    f.write(b)
        dur = duracion(original)
        if dur < 2:
            raise RuntimeError("el clip dura menos de 2 segundos o no se puede leer")
        ini = max(0.0, dur / 2 - SEGUNDOS / 2)
        r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{ini:.2f}", "-t", str(SEGUNDOS), "-i", original,
                            "-vf", "scale=-2:1920,crop=1080:1920:(iw-1080)/2:0,fps=30", "-an", "-c:v", "libx264",
                            "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", destino])
        if r.returncode != 0 or not os.path.exists(destino):
            raise RuntimeError("FFmpeg no pudo cortar el clip")
        return destino
    except Exception as e:
        print(f"  ⚠️ No se pudo preparar el clip «{TOKEN.fullmatch(nombre).group(1)}»: {str(e)[:200]}", flush=True)
        if os.path.exists(destino):
            os.remove(destino)
        return None
    finally:
        if os.path.exists(original):
            os.remove(original)


def elegir(semilla):
    """Un clip para el vídeo (rotando según la semilla), como token para «Capturas». None si no hay."""
    cl = lista()
    if not cl:
        return None
    k = sum(ord(c) for c in str(semilla)) % len(cl)
    return token(*cl[k])
