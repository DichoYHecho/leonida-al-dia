"""Tarjetas de texto de los vídeos 5 y 6 (planos NUEVO_ que no necesitan capturas). Uso: python tarjetas.py DIR_FUENTES DIR_SALIDA

Estilo de los rótulos del canal: Montserrat Black y Bebas Neue, blanco sobre negro y el rosa de la marca.
El tercio de abajo queda libre para los subtítulos. Fuentes: Montserrat y Bebas Neue (Google Fonts, licencia OFL)."""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080
ROSA, BLANCO, GRIS = (255, 79, 163), (255, 255, 255), (170, 170, 180)
DIR_F, SALIDA = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
SALIDA.mkdir(parents=True, exist_ok=True)


def mont(tam, peso):
    f = ImageFont.truetype(str(DIR_F / "Montserrat.ttf"), tam)
    f.set_variation_by_axes([peso])
    return f


def bebas(tam):
    return ImageFont.truetype(str(DIR_F / "BebasNeue.ttf"), tam)


def ajustar(d, texto, tam, peso, ancho):
    """La fuente más grande (hasta «tam») con la que el texto cabe en «ancho»."""
    while tam > 20:
        f = mont(tam, peso)
        if d.textlength(texto, font=f) <= ancho:
            return f
        tam -= 4
    return mont(tam, peso)


def tarjeta(nombre, etiqueta, titular, lineas, pie):
    img = Image.new("RGB", (W, H), (0, 0, 0))
    brillo = Image.new("RGB", (W, H), (0, 0, 0))
    ImageDraw.Draw(brillo).ellipse((360, 40, 1560, 760), fill=(62, 16, 40))
    img = Image.blend(img, brillo.filter(ImageFilter.GaussianBlur(220)), 0.9)
    d = ImageDraw.Draw(img)
    x, y, ancho = 220, 110, W - 440
    d.rectangle((x, y, x + 14, y + 64), fill=ROSA)
    d.text((x + 36, y - 6), etiqueta, font=bebas(72), fill=ROSA)
    y += 100
    for t in titular:
        f = ajustar(d, t, 100, 900, ancho)
        d.text((x, y), t, font=f, fill=BLANCO)
        y += int(f.size * 1.12)
    y += 30
    d.rectangle((x, y, x + 220, y + 6), fill=ROSA)
    y += 40
    for t in lineas:
        f = ajustar(d, t, 44, 700, ancho)
        d.text((x, y), t, font=f, fill=BLANCO)
        y += 62
    if pie:
        d.text((x, 730), pie, font=mont(30, 600), fill=GRIS)
    assert y <= 725, (nombre, y)  # nada por debajo: ahí van los subtítulos
    img.save(SALIDA / f"{nombre}.png", optimize=True)
    print(nombre, "listo")


tarjeta("NUEVO_Texto_Hechos", "SEPTIEMBRE DE 2022 · LOS HECHOS",
        ["EL ACCESO", "A ROCKSTAR"],
        ["Unos 90 clips de GTA VI en desarrollo", "Publicados en un foro el 18 de septiembre",
         "Rockstar lo confirma el 19 de septiembre"],
        "Fuentes: comunicado de Rockstar y cobertura del juicio (2023)")

tarjeta("NUEVO_Pantalla_Texto_Hack", "SEPTIEMBRE DE 2022",
        ["HACKEO", "A ROCKSTAR"],
        ["Aparece en internet material de GTA VI", "Rockstar: «el trabajo sigue según lo previsto»"],
        "Fuente: comunicado de Rockstar, 19 de septiembre de 2022")

tarjeta("NUEVO_Recorte_Prensa_1997", "REINO UNIDO · 1997",
        ["LA POLÉMICA", "COMO PUBLICIDAD"],
        ["Un publicista: Max Clifford", "Un debate en la Cámara de los Lores",
         "Medio millón de copias en Navidad, según la prensa"],
        "Recreación del canal · no es un recorte real")

tarjeta("NUEVO_Titular_Prensa_2013", "SEPTIEMBRE DE 2013 · GTA V",
        ["UNA MISIÓN", "BAJO CRÍTICA"],
        ["Keith Vaz, diputado británico: «asombrado»", "Freedom from Torture: «cruzó una línea»",
         "Los defensores: es sátira"],
        "Recreación del canal · citas resumidas de la prensa de 2013")
