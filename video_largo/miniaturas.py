"""Miniaturas de YouTube (1280x720) de los vídeos 5, 6 y 7. Uso: python miniaturas.py DIR_FUENTES DIR_FONDOS DIR_SALIDA
Fondo: un fotograma de los tráileres oficiales de GTA VI, sin logos de Rockstar ni caras reales. Texto en amarillo
(#FFD700) con contorno negro, legible a 160 px; máximo tres líneas. Fuentes: Montserrat y Bebas Neue (OFL)."""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

W, H = 1280, 720
AMARILLO, BLANCO, ROSA, NEGRO = (255, 215, 0), (255, 255, 255), (255, 79, 163), (0, 0, 0)
DIR_F, DIR_B, SAL = (pathlib.Path(a) for a in sys.argv[1:4])
SAL.mkdir(parents=True, exist_ok=True)


def bebas(t):
    return ImageFont.truetype(str(DIR_F / "BebasNeue.ttf"), t)


def mont(t, peso=900):
    f = ImageFont.truetype(str(DIR_F / "Montserrat.ttf"), t)
    f.set_variation_by_axes([peso])
    return f


def fondo(nombre, brillo=0.85, oscuro_izq=True):
    im = ImageOps.fit(Image.open(DIR_B / nombre).convert("RGB"), (W, H), Image.LANCZOS)
    im = ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(brillo)).enhance(1.15)
    if oscuro_izq:  # degradado negro a la izquierda para que el texto se lea
        g = Image.linear_gradient("L").rotate(90, expand=True).resize((W, H))
        g = g.point(lambda v: int(v * 0.85))
        im = Image.composite(im, Image.new("RGB", (W, H), NEGRO), g)
    return im


def texto(d, xy, s, f, color, borde=8):
    d.text(xy, s, font=f, fill=color, stroke_width=borde, stroke_fill=NEGRO)


def marca(d):
    f = mont(26, 800)
    s = "LEÓNIDA AL DÍA"
    w = d.textlength(s, font=f)
    d.rounded_rectangle((W - w - 64, 28, W - 28, 76), 24, fill=ROSA)
    d.text((W - w - 46, 36), s, font=f, fill=BLANCO)


def pastilla(d, xy, s, f, fondo_c=ROSA, color=BLANCO):
    x, y = xy
    w = d.textlength(s, font=f)
    d.rounded_rectangle((x, y, x + w + 40, y + f.size + 22), 14, fill=fondo_c)
    d.text((x + 20, y + 8), s, font=f, fill=color)


# Vídeo 5 · ¿Por qué GTA VI ha tardado 13 años?
im = fondo("mi_atardecer.jpg", 1.35)
d = ImageDraw.Draw(im)
texto(d, (60, 70), "13 AÑOS", bebas(300), AMARILLO, 10)
texto(d, (66, 380), "¿POR QUÉ TARDA?", bebas(118), BLANCO, 8)
pastilla(d, (70, 540), "19 NOV 2026", mont(44, 900))
marca(d)
im.save(SAL / "miniatura_13a.jpg", quality=92)

# Vídeo 6 · Todas las polémicas de GTA
im = fondo("mi_skyline_noche.jpg", 1.0)
d = ImageDraw.Draw(im)
texto(d, (60, 60), "POLÉMICAS", bebas(210), AMARILLO, 10)
texto(d, (60, 255), "DE GTA", bebas(210), AMARILLO, 10)
texto(d, (66, 470), "1997 → 2026", mont(70, 900), BLANCO, 7)
pastilla(d, (70, 590), "¿Por qué Rockstar siempre gana?", mont(36, 800))
marca(d)
im.save(SAL / "miniatura_pol.jpg", quality=92)

# Vídeo 7 · Las radios de GTA
im = fondo("t1_neones.jpg", 0.9)
d = ImageDraw.Draw(im)
texto(d, (60, 70), "¿TU RADIO", bebas(200), AMARILLO, 10)
texto(d, (60, 260), "FAVORITA?", bebas(200), AMARILLO, 10)
texto(d, (66, 480), "1997 → 2026", mont(70, 900), BLANCO, 7)
marca(d)
im.save(SAL / "miniatura_rad.jpg", quality=92)
print("3 miniaturas en", SAL)
