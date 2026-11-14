"""Revisión automática del vídeo final (14 nov 2026): lo que antes se hacía a mano bajando el MP4.

Uso: python3 revisar_video.py salida_hq/video_largo.mp4 salida_montaje
Comprueba resolución, fotogramas frente a duración, huecos en los tiempos (saltos de más de 1,5 fotogramas),
congelaciones largas y hace hojas de contactos (un fotograma cada 2,5 s) en salida_montaje/hojas/.
Escribe el resumen en el del run (GITHUB_STEP_SUMMARY). Sale con 8 si hay huecos o falta imagen."""
import os
import re
import subprocess
import sys

video, salida = sys.argv[1], sys.argv[2]
hojas = os.path.join(salida, "hojas")
os.makedirs(hojas, exist_ok=True)


def ffprobe(*a):
    return subprocess.run(["ffprobe", "-v", "error", *a, video], capture_output=True, text=True).stdout.strip()


ancho, alto, fps = ffprobe("-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate",
                           "-of", "csv=p=0").split(",")
num, den = fps.split("/")
fps = int(num) / int(den)
dur_audio = float(ffprobe("-select_streams", "a:0", "-show_entries", "stream=duration", "-of", "csv=p=0") or 0)

r = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-map", "0:v", "-c", "copy", "-f", "framemd5", "-"],
                   capture_output=True, text=True)
filas = [l.split(",") for l in r.stdout.splitlines() if l.strip() and not l.startswith("#")]
pts = sorted(int(c[2]) for c in filas)
paso = int(filas[0][3]) if filas else 1
tb = next((l.split(":")[1].strip() for l in r.stdout.splitlines() if l.startswith("#tb")), "1/1")
tb = int(tb.split("/")[0]) / int(tb.split("/")[1])
huecos = [(pts[i] * tb, (pts[i + 1] - pts[i]) / paso) for i in range(len(pts) - 1) if pts[i + 1] - pts[i] > 1.5 * paso]
esperados = round(dur_audio * fps)

fr = subprocess.run(["ffmpeg", "-hide_banner", "-i", video, "-map", "0:v", "-vf", "scale=640:-2,freezedetect=n=0.0005:d=0.25",
                     "-f", "null", "-"], capture_output=True, text=True, errors="replace").stderr
ini = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", fr)]
dur = [float(x) for x in re.findall(r"freeze_duration: ([\d.]+)", fr)]

subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf",
                "fps=1/2.5,scale=512:-2,tile=5x4", os.path.join(hojas, "hoja_%02d.jpg")])

def hms(s):
    return f"{int(s // 60)}:{s % 60:05.2f}"


lineas = ["## Revisión automática del vídeo",
          f"- Resolución: {ancho}x{alto} a {fps:g} fps" + ("" if (ancho, alto) == ("2560", "1440") else " ⚠️ no es 2560x1440"),
          f"- Fotogramas: {len(pts)} de {esperados} esperados por la duración del audio ({hms(dur_audio)})"
          + ("" if abs(len(pts) - esperados) <= fps else " ⚠️"),
          f"- Huecos en los tiempos (saltos de más de 1,5 fotogramas): {len(huecos)}" + (" ⚠️" if huecos else ""),
          *[f"    - {hms(t)}: salto de {n:.0f} fotogramas" for t, n in huecos[:20]],
          f"- Imagen quieta 0,25 s o más: {len(ini)} tramos, {sum(dur):.1f} s en total (cartelas, logos y pantalla final"
          " son normales); los más largos:",
          *[f"    - {hms(a)} durante {d:.1f} s" for a, d in sorted(zip(ini, dur), key=lambda x: -x[1])[:8]],
          f"- Hojas de contactos (un fotograma cada 2,5 s): carpeta `hojas/` de la rama del montaje"]
texto = "\n".join(lineas)
print(texto)
resumen = os.environ.get("GITHUB_STEP_SUMMARY")
if resumen:
    with open(resumen, "a", encoding="utf-8") as f:
        f.write(texto + "\n")
with open(os.path.join(salida, "revision.md"), "w", encoding="utf-8") as f:
    f.write(texto + "\n")
if huecos or abs(len(pts) - esperados) > fps:
    sys.exit(8)
