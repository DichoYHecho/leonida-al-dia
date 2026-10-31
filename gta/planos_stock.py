"""Todos los planos de los tráileres (31 oct), para elegir trozos sin cortes dentro: detecta cada cambio de plano
del vídeo entero y saca un fotograma del centro de cada plano de al menos 1 s, ya recortado en vertical (lo que se
verá), con su número, inicio y duración. No toca Airtable ni publica nada."""
import os, re, subprocess
import requests
from PIL import Image, ImageDraw, ImageFont
import medios

SALIDA = "salida_planos"
LETRA = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
MINIMO = 1.0
TW, TH, COL, FIL = 160, 284, 8, 5


def bajar(url, destino):
    with requests.get(url, headers={"User-Agent": medios.UA}, stream=True, timeout=600) as r:
        r.raise_for_status()
        with open(destino, "wb") as f:
            for b in r.iter_content(1 << 20):
                f.write(b)


def main():
    os.makedirs(SALIDA, exist_ok=True)
    letra = ImageFont.truetype(LETRA, 15)
    for nombre in ("Lanzamiento", "Trailer_1", "Trailer_2"):
        mp4 = nombre + ".mp4"
        bajar(medios.VIDEOS[nombre], mp4)
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                             "csv=p=0", mp4]).decode().strip())
        r = subprocess.run(["ffmpeg", "-hide_banner", "-i", mp4, "-an", "-vf",
                            "scale=480:-2,select='gt(scene\\,0.08)',showinfo", "-f", "null", "-"],
                           capture_output=True, text=True)
        cortes = [0.0] + [float(x) for x in re.findall(r"pts_time:([\d.]+)", r.stderr)] + [dur]
        planos = [(k + 1, a, b - a) for k, (a, b) in enumerate(zip(cortes, cortes[1:])) if b - a >= MINIMO]
        with open(os.path.join(SALIDA, f"planos_{nombre}.txt"), "w") as f:
            for n, a, d in planos:
                f.write(f"{n}\t{a:.2f}\t{d:.2f}\n")
        fichas = []
        for n, a, d in planos:
            q = os.path.join(SALIDA, "f.jpg")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{a + d / 2:.2f}", "-i", mp4, "-frames:v", "1",
                            "-vf", f"scale=-2:{TH},crop={TW}:{TH}", q], check=True)
            ficha = Image.new("RGB", (TW, TH + 22), (20, 20, 20))
            ficha.paste(Image.open(q), (0, 22))
            ImageDraw.Draw(ficha).text((3, 2), f"#{n} {a:.1f}s {d:.1f}s", font=letra, fill=(255, 255, 255))
            fichas.append(ficha)
        por = COL * FIL
        for h in range(0, len(fichas), por):
            g = fichas[h:h + por]
            hoja = Image.new("RGB", (COL * (TW + 4), ((len(g) + COL - 1) // COL) * (TH + 26)), (0, 0, 0))
            for k, fi in enumerate(g):
                hoja.paste(fi, ((k % COL) * (TW + 4), (k // COL) * (TH + 26)))
            hoja.save(os.path.join(SALIDA, f"planos_{nombre}_{h // por + 1}.jpg"), quality=85)
        print(f"{nombre}: {len(cortes) - 1} planos, {len(planos)} de al menos {MINIMO} s", flush=True)
        os.remove(mp4)
    if os.path.exists(os.path.join(SALIDA, "f.jpg")):
        os.remove(os.path.join(SALIDA, "f.jpg"))


if __name__ == "__main__":
    main()
