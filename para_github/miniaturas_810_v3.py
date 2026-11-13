"""Miniaturas v3 de los vídeos 8 y 9 (13 nov 2026), dirección «cinematográfica» elegida por el usuario: una imagen
oficial de GTA VI a pantalla completa y una sola palabra o cifra grande. Sin pantallas partidas, rayas, marcos ni
logos pegados. Solo se retoca la imagen (contraste, color y viñeta) y se oscurece con suavidad la zona del texto.
Uso: python miniaturas_810_v3.py DIR_FUENTES DIR_FONDOS DIR_SALIDA"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

W, H = 1280, 720
NEGRO = (0, 0, 0)
DIR_F, DIR_B, SAL = (pathlib.Path(a) for a in sys.argv[1:4])
SAL.mkdir(parents=True, exist_ok=True)


def bebas(t):
    return ImageFont.truetype(str(DIR_F / "BebasNeue.ttf"), t)


def imagen(nombre, foco=(0.5, 0.5), zoom=1.0, brillo=1.0):
    im = Image.open(DIR_B / nombre).convert("RGB")
    if zoom > 1:  # recorte más cerrado alrededor del foco
        w, h = int(im.width / zoom), int(im.height / zoom)
        x = int(min(max(im.width * foco[0] - w / 2, 0), im.width - w))
        y = int(min(max(im.height * foco[1] - h / 2, 0), im.height - h))
        im, foco = im.crop((x, y, x + w, y + h)), (0.5, 0.5)
    im = ImageOps.fit(im, (W, H), Image.LANCZOS, centering=foco)
    im = ImageEnhance.Brightness(im).enhance(brillo)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    im = ImageEnhance.Color(im).enhance(1.12)
    # viñeta suave
    v = Image.radial_gradient("L").resize((int(W * 1.5), int(H * 1.5))).crop((W // 4, H // 4, W // 4 + W, H // 4 + H))
    im.paste(NEGRO, (0, 0), v.point(lambda p: max(0, p - 150) * 110 // 105))
    return im


def palabra(im, s, tam, xy, ancla, sombra_zona=110):
    """Una palabra grande en blanco; detrás, una sombra muy difuminada para que se lea sin cajas ni contornos."""
    f = bebas(tam)
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).text(xy, s, font=f, fill=255, anchor=ancla)
    zona = m.filter(ImageFilter.GaussianBlur(tam // 2)).point(lambda p: min(255, p * 3) * sombra_zona // 255)
    im.paste(NEGRO, (0, 0), zona)
    im.paste(NEGRO, (0, tam // 40 + 2), m.filter(ImageFilter.GaussianBlur(tam // 25)).point(lambda p: p * 150 // 255))
    im.paste((255, 255, 255), (0, 0), m)


def guardar(im, nombre):
    im.save(SAL / nombre, quality=94)


# ======================================================== Vídeo 8 · Qué cambió en cada GTA
im = imagen("Jason_and_Lucia_17.jpg", (0.5, 0.45), 1.0, 1.05)
palabra(im, "29 AÑOS", 210, (40, 30), "la")
guardar(im, "v3_miniatura_evo.jpg")

im = imagen("Vice_City_24.jpg", (0.3, 0.6), 1.25, 1.05)
palabra(im, "DE 1997", 220, (W - 40, 20), "ra")
guardar(im, "v3_miniatura_evo_b.jpg")

im = imagen("Jason_and_Lucia_16.jpg", (0.4, 0.55), 1.0, 1.0)
palabra(im, "¿QUÉ CAMBIÓ?", 190, (W // 2, H - 40), "ms")
guardar(im, "v3_miniatura_evo_c.jpg")

# ======================================================== Vídeo 9 · GTA V, la vara de medir
im = imagen("Lucia_Caminos_13.jpg", (0.4, 0.4), 1.15, 1.05)
palabra(im, "235 M", 260, (W - 50, 20), "ra")  # Take-Two, 9 nov 2026: casi 235 millones
guardar(im, "v3_miniatura_gv5.jpg")

im = imagen("Vice_City_17.jpg", (0.5, 0.5), 1.0, 1.25)
palabra(im, "EL LISTÓN", 220, (W // 2, 30), "ma")
guardar(im, "v3_miniatura_gv5_b.jpg")

im = imagen("Jason_Duval_14.jpg", (0.6, 0.5), 1.1, 1.05)
palabra(im, "7 RÉCORDS", 200, (40, H - 40), "ls")
guardar(im, "v3_miniatura_gv5_c.jpg")
print("6 miniaturas v3 en", SAL)
