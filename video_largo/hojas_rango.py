"""Hojas de contacto a 1 fotograma por segundo SOLO de unos tramos de «Una mirada extendida».

Variables: RANGOS = «inicio-fin» en segundos separados por comas (por ejemplo 0-20,840-880).
Salida en «salida_hojas/»: rango_<inicio>_<n>.jpg con 12 fotogramas (4 × 3) a 480 × 270 y su minuto:segundo."""
import os
import pathlib
import subprocess
import sys

SALIDA = pathlib.Path("salida_hojas")
SALIDA.mkdir(exist_ok=True)
VIDEO = sys.argv[1] if len(sys.argv) > 1 else "oficial.mp4"
RANGOS = os.environ.get("RANGOS", "0-20")
FUENTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

for r in [x.strip() for x in RANGOS.split(",") if x.strip()]:
    ini, fin = (float(v) for v in r.split("-"))
    filtro = (f"fps=1,scale=480:270,"
              f"drawtext=fontfile={FUENTE}:text='%{{pts\\:hms\\:{ini}}}':x=8:y=h-30:fontsize=24:fontcolor=white:"
              f"box=1:boxcolor=black@0.6,tile=4x3")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", str(ini), "-i", VIDEO, "-t", str(fin - ini),
           "-vf", filtro, "-q:v", "3", str(SALIDA / f"rango_{int(ini):05d}_%02d.jpg")]
    p = subprocess.run(cmd, capture_output=True, text=True)
    print(r, "->", "ok" if p.returncode == 0 else p.stderr[-300:], flush=True)
print(sorted(x.name for x in SALIDA.glob("rango_*.jpg")))
