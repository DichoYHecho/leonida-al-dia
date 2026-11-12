"""Variantes B y C de las miniaturas de los vídeos 5, 6 y 7, para «Probar y comparar» de YouTube Studio (hasta 3
miniaturas por vídeo; la A es la de miniaturas.py). Mismo estilo: Bebas/Montserrat, amarillo #FFD700 con contorno
negro, pastilla rosa del canal. Fondos: fotogramas de los tráileres oficiales de GTA VI, sin logos ni caras reales.
Uso: python miniaturas_variantes.py DIR_FUENTES DIR_FONDOS DIR_SALIDA"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

W, H = 1280, 720
AMARILLO, BLANCO, ROSA, ROJO, NEGRO = (255, 215, 0), (255, 255, 255), (255, 79, 163), (220, 30, 40), (0, 0, 0)
DIR_F, DIR_B, SAL = (pathlib.Path(a) for a in sys.argv[1:4])
SAL.mkdir(parents=True, exist_ok=True)


def bebas(t):
    return ImageFont.truetype(str(DIR_F / "BebasNeue.ttf"), t)


def mont(t, peso=900):
    f = ImageFont.truetype(str(DIR_F / "Montserrat.ttf"), t)
    f.set_variation_by_axes([peso])
    return f


def fondo(nombre, brillo=0.85, lado="izq", recorte=None, fuerza=0.85):
    im = Image.open(DIR_B / nombre).convert("RGB")
    if recorte:  # quita las bandas negras de los planos panorámicos
        im = im.crop(recorte)
    im = ImageOps.fit(im, (W, H), Image.LANCZOS)
    im = ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(brillo)).enhance(1.15)
    g = Image.linear_gradient("L")  # 0 arriba, 255 abajo
    g = {"izq": g.rotate(90, expand=True), "der": g.rotate(-90, expand=True), "arriba": g}[lado].resize((W, H))
    g = g.point(lambda v: int(255 - (255 - v) * fuerza))
    return Image.composite(im, Image.new("RGB", (W, H), NEGRO), g)


def texto(d, xy, s, f, color, borde=8):
    d.text(xy, s, font=f, fill=color, stroke_width=borde, stroke_fill=NEGRO)


def texto_der(d, y, s, f, color, borde=8, margen=60):
    texto(d, (W - margen - d.textlength(s, font=f), y), s, f, color, borde)


def marca(d, izq=False):
    f = mont(26, 800)
    s = "LEÓNIDA AL DÍA"
    w = d.textlength(s, font=f)
    x = 28 if izq else W - w - 64
    d.rounded_rectangle((x, 28, x + w + 36, 76), 24, fill=ROSA)
    d.text((x + 18, 36), s, font=f, fill=BLANCO)


def pastilla(d, xy, s, f, fondo_c=ROSA, color=BLANCO, der=False):
    x, y = xy
    w = d.textlength(s, font=f)
    if der:
        x = W - 60 - (w + 40)
    d.rounded_rectangle((x, y, x + w + 40, y + f.size + 22), 14, fill=fondo_c)
    d.text((x + 20, y + 8), s, font=f, fill=color)


BANDAS = (0, 220, 3840, 1940)  # t2_*: 3840x2160 con bandas negras arriba y abajo

# Vídeo 5 · B: el muelle del tráiler 2, la pregunta en grande
im = fondo("t2_muelle.jpg", 1.05, "izq", BANDAS, 0.95)
d = ImageDraw.Draw(im)
texto(d, (55, 90), "2013", bebas(170), BLANCO, 9)
texto(d, (60, 262), "→", mont(110, 900), AMARILLO, 8)  # Bebas no tiene la flecha
texto(d, (200, 235), "2026", bebas(170), AMARILLO, 9)
texto(d, (60, 430), "¿POR QUÉ", bebas(120), BLANCO, 8)
texto(d, (60, 545), "TANTO?", bebas(120), AMARILLO, 8)
marca(d)
im.save(SAL / "miniatura_13a_b.jpg", quality=92)

# Vídeo 5 · C: Vice City de noche desde el aire, el número solo
im = fondo("t1_noche_aerea.jpg", 1.1, "izq", None, 0.9)
d = ImageDraw.Draw(im)
texto(d, (50, 20), "13", bebas(460), AMARILLO, 12)
texto(d, (60, 470), "AÑOS ESPERANDO", bebas(120), BLANCO, 8)
pastilla(d, (66, 610), "La historia completa", mont(36, 800))
marca(d)
im.save(SAL / "miniatura_13a_c.jpg", quality=92)

# Vídeo 6 · B: tres palabras, cada una un caso del vídeo
im = fondo("t1_noche_aerea.jpg", 0.85, "izq", None, 0.95)
d = ImageDraw.Draw(im)
texto(d, (55, 60), "PROHIBIDO.", bebas(165), AMARILLO, 10)
texto(d, (55, 225), "DEMANDADO.", bebas(165), BLANCO, 10)
texto(d, (55, 390), "RETIRADO.", bebas(165), AMARILLO, 10)
pastilla(d, (62, 590), "GTA · 1997-2026", mont(44, 900), fondo_c=ROJO)
marca(d)
im.save(SAL / "miniatura_pol_b.jpg", quality=92)

# Vídeo 6 · C: atardecer del tráiler 2, la cifra y los casos más conocidos
im = fondo("t2_mar_atardecer.jpg", 0.8, "izq", BANDAS, 0.95)
d = ImageDraw.Draw(im)
texto(d, (55, 70), "29 AÑOS", bebas(230), AMARILLO, 11)
texto(d, (60, 320), "DE POLÉMICAS", bebas(130), BLANCO, 8)
pastilla(d, (66, 500), "Hot Coffee · Australia · Hackeo", mont(38, 800), fondo_c=ROJO)
marca(d)
im.save(SAL / "miniatura_pol_c.jpg", quality=92)

# Vídeo 7 · B: Lucía bailando en el coche (de espaldas); el texto a la derecha
im = fondo("t1_coches_noche.jpg", 1.0, "der", None, 0.95)
d = ImageDraw.Draw(im)
texto_der(d, 110, "LAS RADIOS", bebas(170), AMARILLO, 10)
texto_der(d, 270, "DE GTA", bebas(170), AMARILLO, 10)
texto_der(d, 470, "1997 → GTA VI", mont(62, 900), BLANCO, 7)
pastilla(d, (0, 580), "Y sus canciones retiradas", mont(36, 800), der=True)
marca(d, izq=True)
im.save(SAL / "miniatura_rad_b.jpg", quality=92)

# Vídeo 7 · C: el atardecer del muelle, las emisoras como dial
im = fondo("t2_mar_atardecer.jpg", 0.85, "izq", BANDAS, 0.95)
d = ImageDraw.Draw(im)
f = bebas(118)
for i, (s, c) in enumerate([("FLASH FM", AMARILLO), ("K-DST", BLANCO), ("V-ROCK", BLANCO), ("WCTR", BLANCO)]):
    texto(d, (60, 40 + i * 118), s, f, c, 8)
pastilla(d, (66, 555), "¿Cuál es la mejor radio de GTA?", mont(38, 800))
marca(d)
im.save(SAL / "miniatura_rad_c.jpg", quality=92)
print("6 variantes en", SAL)
