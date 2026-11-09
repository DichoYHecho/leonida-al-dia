"""Hojas de contacto y transcripción de «Una mirada extendida» (para elegir escenas del vídeo largo).

No publica nada. Entrada: oficial.mp4. Salida en «salida_hojas/»:
- hoja_01.jpg, hoja_02.jpg...: 24 fotogramas por hoja (uno cada 3 s), con el minuto:segundo de cada uno.
- transcripcion.txt: lo que se dice (en inglés), con su minuto:segundo."""
import os
import pathlib
import subprocess
import sys
import urllib.request

import numpy as np

SALIDA = pathlib.Path("salida_hojas")
SALIDA.mkdir(exist_ok=True)
VIDEO = sys.argv[1] if len(sys.argv) > 1 else "oficial.mp4"
CADA = float(os.environ.get("CADA", "3"))
FUENTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
UA = "LeonidaAlDiaBot/1.0 (cuenta de fans de GTA 6) GitHubActions"


def hojas():
    filtro = (f"fps=1/{CADA},scale=320:180,"
              f"drawtext=fontfile={FUENTE}:text='%{{pts\\:hms}}':x=6:y=h-24:fontsize=18:fontcolor=white:"
              f"box=1:boxcolor=black@0.6,tile=6x4")
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", VIDEO, "-vf", filtro, "-q:v", "4",
                        str(SALIDA / "hoja_%02d.jpg")], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-800:])
    print("hojas:", len(list(SALIDA.glob("hoja_*.jpg"))), flush=True)


def audio_16k(ruta):
    r = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(ruta), "-vn", "-ar", "16000", "-ac", "1",
                        "-f", "s16le", "pipe:1"], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode("utf-8", "ignore")[-300:])
    return np.frombuffer(r.stdout, dtype="<i2").astype(np.float32) / 32768


def modelo_whisper():
    d = pathlib.Path(os.environ.get("CACHE_WHISPER", "cache/whisper-base"))
    d.mkdir(parents=True, exist_ok=True)
    base = "https://huggingface.co/Systran/faster-whisper-base/resolve/main/"
    for nombre, obligatorio in (("config.json", True), ("tokenizer.json", True), ("model.bin", True),
                                ("vocabulary.txt", False)):
        destino = d / nombre
        if destino.exists() and destino.stat().st_size > 0:
            continue
        try:
            pet = urllib.request.Request(base + nombre, headers={"User-Agent": UA})
            with urllib.request.urlopen(pet, timeout=900) as r, open(destino, "wb") as f:
                while True:
                    bloque = r.read(1 << 20)
                    if not bloque:
                        break
                    f.write(bloque)
        except Exception:
            if destino.exists():
                destino.unlink()
            if obligatorio:
                raise
    return str(d)


def transcripcion():
    from faster_whisper import WhisperModel
    modelo = WhisperModel(modelo_whisper(), device="cpu", compute_type="int8")
    segs, _ = modelo.transcribe(audio_16k(VIDEO), language="en", word_timestamps=False)
    lineas = []
    for s in segs:
        m, seg = divmod(int(s.start), 60)
        lineas.append(f"{m:02d}:{seg:02d}  {s.text.strip()}")
    (SALIDA / "transcripcion.txt").write_text("\n".join(lineas), encoding="utf-8")
    print("líneas de transcripción:", len(lineas), flush=True)


if __name__ == "__main__":
    hojas()
    try:
        transcripcion()
    except Exception as e:  # noqa: BLE001
        print("Sin transcripción:", type(e).__name__, e, flush=True)
