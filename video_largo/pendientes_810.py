"""Tarjetas «PLANO PENDIENTE» para los planos nuevos de los vídeos 8-10 que todavía no tienen imagen.

Lee trozos_810_evo/gv5/onl.csv y, por cada fila con Notas «PENDIENTE…», crea la imagen con el nombre exacto que espera
la columna «Vídeo» (png o jpg). Así el montaje de la previa no se para y se ve qué captura falta.
Cuando exista la captura real, se sustituye el archivo con el mismo nombre (y se cambia la nota de la fila).
Uso: python pendientes_810.py DIR_CSV DIR_FUENTES DIR_SALIDA
Estilo de tarjetas.py: Montserrat y Bebas Neue (OFL), blanco sobre negro y el rosa del canal."""
import csv
import pathlib
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080
ROSA, BLANCO, GRIS = (255, 79, 163), (255, 255, 255), (170, 170, 180)
DIR_CSV, DIR_F, SALIDA = (pathlib.Path(a) for a in sys.argv[1:4])
SALIDA.mkdir(parents=True, exist_ok=True)


def mont(tam, peso):
    f = ImageFont.truetype(str(DIR_F / "Montserrat.ttf"), tam)
    f.set_variation_by_axes([peso])
    return f


def tarjeta(nombre, ext, que):
    img = Image.new("RGB", (W, H), (0, 0, 0))
    brillo = Image.new("RGB", (W, H), (0, 0, 0))
    ImageDraw.Draw(brillo).ellipse((360, 40, 1560, 760), fill=(62, 16, 40))
    img = Image.blend(img, brillo.filter(ImageFilter.GaussianBlur(220)), 0.9)
    d = ImageDraw.Draw(img)
    x, y = 220, 110
    d.rectangle((x, y, x + 14, y + 64), fill=ROSA)
    d.text((x + 36, y - 6), "PLANO PENDIENTE", font=ImageFont.truetype(str(DIR_F / "BebasNeue.ttf"), 72), fill=ROSA)
    y += 110
    d.text((x, y), nombre, font=mont(56, 900), fill=BLANCO)
    y += 100
    d.rectangle((x, y, x + 220, y + 6), fill=ROSA)
    y += 40
    for linea in textwrap.wrap(que, 62)[:6]:
        d.text((x, y), linea, font=mont(38, 600), fill=BLANCO)
        y += 54
    d.text((x, 730), "Provisional · se sustituye por la captura real", font=mont(30, 600), fill=GRIS)
    destino = SALIDA / f"{nombre}.{ext}"
    if ext == "jpg":
        img.save(destino, quality=88)
    else:
        img.save(destino, optimize=True)
    return destino


hechas = []
for csv_p in sorted(DIR_CSV.glob("trozos_810_*.csv")):
    for r in csv.DictReader(csv_p.read_text(encoding="utf-8-sig").splitlines()):
        if not (r.get("Notas") or "").startswith("PENDIENTE"):
            continue
        ext = r["Vídeo"].rsplit(".", 1)[-1].lower()
        hechas.append(tarjeta(r["Trozo"], ext, r["Qué se ve"]))
print(len(hechas), "tarjetas en", SALIDA)
