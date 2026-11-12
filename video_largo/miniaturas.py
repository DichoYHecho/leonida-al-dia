"""Miniaturas de YouTube (1280x720) de los vídeos 5, 6 y 7: tres por vídeo (A principal, B y C para «Probar y
comparar»). Uso: python miniaturas.py DIR_FUENTES DIR_FONDOS DIR_SALIDA   (DIR_FONDOS contiene también vi.png)

Estilo (13 nov 2026, pedido del usuario): sin el nombre del canal, sin contorno negro en los textos, títulos con el
degradado del logo de GTA VI (magenta → rosa → naranja). Para que se lean sin contorno, cada texto lleva una sombra
suave difuminada. Fondos más claros que en la versión anterior. Fondos: fotogramas de los tráileres oficiales de
GTA VI; logo: vi.png de rockstargames.com/VI. Fuentes: Bebas Neue y Montserrat (OFL)."""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

W, H = 1280, 720
BLANCO, NEGRO = (255, 255, 255), (0, 0, 0)
# Colores del logo de GTA VI, de arriba abajo
DEGRADADO = [(0.0, (214, 70, 214)), (0.45, (255, 84, 150)), (1.0, (255, 170, 72))]
DIR_F, DIR_B, SAL = (pathlib.Path(a) for a in sys.argv[1:4])
SAL.mkdir(parents=True, exist_ok=True)
BANDAS = (0, 220, 3840, 1940)  # t2_*: 3840x2160 con bandas negras arriba y abajo


def bebas(t):
    return ImageFont.truetype(str(DIR_F / "BebasNeue.ttf"), t)


def mont(t, peso=900):
    f = ImageFont.truetype(str(DIR_F / "Montserrat.ttf"), t)
    f.set_variation_by_axes([peso])
    return f


def fondo(nombre, brillo=1.0, lado="izq", fuerza=0.5, recorte=None, ancho=0.65):
    """Fotograma a 1280x720, con un velo oscuro suave solo por el lado del texto (fuerza 0 = sin velo)."""
    im = Image.open(DIR_B / nombre).convert("RGB")
    if recorte:
        im = im.crop(recorte)
    im = ImageOps.fit(im, (W, H), Image.LANCZOS)
    im = ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(brillo)).enhance(1.1)
    im = ImageEnhance.Color(im).enhance(1.15)
    if lado == "centro":  # velo uniforme, para textos centrados
        g = Image.new("L", (W, H), int(255 * (1 - fuerza)))
        return Image.composite(im, Image.new("RGB", (W, H), NEGRO), g)
    g = Image.linear_gradient("L").rotate(90 if lado == "izq" else -90, expand=True).resize((W, H))
    # 255 = imagen tal cual; por el lado del texto baja hasta 255*(1-fuerza) y desde «ancho» ya no oscurece
    g = g.point(lambda v: int(255 - (255 - min(255, v / ancho)) * fuerza))
    return Image.composite(im, Image.new("RGB", (W, H), NEGRO), g)


def _degradado(w, h):
    tira = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        for (a, ca), (b, cb) in zip(DEGRADADO, DEGRADADO[1:]):
            if a <= t <= b:
                k = (t - a) / (b - a)
                tira.putpixel((0, y), tuple(int(ca[i] + (cb[i] - ca[i]) * k) for i in range(3)))
                break
    return tira.resize((w, h))


def texto(im, xy, s, f, color=None, sombra=170, der=False, centro=False):
    """Texto sin contorno: sombra difuminada debajo y relleno blanco o con el degradado de GTA VI (color=None)."""
    d = ImageDraw.Draw(im)
    x, y = xy
    x0, y0, x1, y1 = d.textbbox((0, 0), s, font=f)
    if der:
        x = W - x - (x1 - x0) - x0
    if centro:
        x = (W - (x1 - x0)) // 2 - x0
    mascara = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mascara).text((x, y), s, font=f, fill=255)
    if sombra:
        sm = mascara.filter(ImageFilter.GaussianBlur(f.size // 14)).point(lambda v: v * sombra // 255)
        im.paste(NEGRO, (0, f.size // 30 + 2), sm)  # desplazada un poco hacia abajo
    if color is None:
        relleno = Image.new("RGB", (W, H))
        relleno.paste(_degradado(x1 - x0, y1 - y0), (x + x0, y + y0))
    else:
        relleno = Image.new("RGB", (W, H), color)
    im.paste(relleno, (0, 0), mascara)


def logo(im, xy, alto, archivo="vi.png", parte=None, centro=False):
    """Logo oficial con sombra suave. parte = (x0, x1) en fracción del ancho, para recortar un trozo del logo."""
    lg = Image.open(DIR_B / archivo).convert("RGBA")
    lg = lg.crop(lg.getbbox())
    if parte:
        lg = lg.crop((int(lg.width * parte[0]), 0, int(lg.width * parte[1]), lg.height))
        lg = lg.crop(lg.getbbox())
    lg = lg.resize((int(lg.width * alto / lg.height), alto), Image.LANCZOS)
    if centro:
        xy = ((W - lg.width) // 2, xy[1])
    sm = lg.split()[3].filter(ImageFilter.GaussianBlur(14)).point(lambda v: v * 150 // 255)
    im.paste(NEGRO, (xy[0], xy[1] + 6, xy[0] + lg.width, xy[1] + 6 + lg.height), sm)
    im.paste(lg, xy, lg)


def icono(im, centro, lado, archivo, brillo=None):
    """Logo encajado en un cuadrado de «lado» px centrado en «centro», con sombra suave (y un halo claro si brillo)."""
    lg = Image.open(DIR_B / archivo).convert("RGBA")
    lg = lg.crop(lg.getbbox())
    lg.thumbnail((lado, lado), Image.LANCZOS)
    x, y = centro[0] - lg.width // 2, centro[1] - lg.height // 2
    a = lg.split()[3]
    if brillo:  # halo blanco suave detrás, para logos oscuros sobre fondo oscuro
        halo = Image.new("L", (W, H), 0)
        halo.paste(a.filter(ImageFilter.GaussianBlur(10)).point(lambda v: v * brillo // 255), (x, y))
        im.paste(BLANCO, (0, 0), halo.filter(ImageFilter.GaussianBlur(8)))
    sm = a.filter(ImageFilter.GaussianBlur(10)).point(lambda v: v * 150 // 255)
    im.paste(NEGRO, (x, y + 5, x + lg.width, y + 5 + lg.height), sm)
    im.paste(lg, (x, y), lg)


def guardar(im, nombre):
    im.save(SAL / nombre, quality=92)


# ======================================================== Vídeo 5 · ¿Por qué GTA VI ha tardado 13 años?
# A: logo de GTA VI + «13 años de desarrollo»
im = fondo("mi_atardecer.jpg", 1.45, "der", 0.45, ancho=0.6)
logo(im, (50, 70), 420)
texto(im, (60, 150), "13 AÑOS", bebas(250), der=True)
texto(im, (60, 400), "DE DESARROLLO", bebas(112), BLANCO, der=True)
guardar(im, "miniatura_13a.jpg")

# B: «de 2013 a 2026» sobre el muelle del tráiler 2, más claro
im = fondo("t2_muelle.jpg", 1.4, "izq", 0.4, BANDAS, ancho=0.55)
texto(im, (55, 70), "DE 2013", bebas(230))
texto(im, (55, 300), "A 2026", bebas(230))
guardar(im, "miniatura_13a_b.jpg")

# C: el número solo, sin cartel, sobre Vice City de noche más clara
im = fondo("t1_noche_aerea.jpg", 1.6, "izq", 0.35, ancho=0.6)
texto(im, (50, 10), "13", bebas(480))
texto(im, (60, 480), "AÑOS ESPERANDO", bebas(125), BLANCO)
guardar(im, "miniatura_13a_c.jpg")

# ======================================================== Vídeo 6 · Todas las polémicas de GTA
# A: solo la pregunta, como título principal
im = fondo("mi_skyline_noche.jpg", 1.25, "izq", 0.55, ancho=0.75)
texto(im, (60, 40), "¿POR QUÉ", bebas(205))
texto(im, (60, 245), "ROCKSTAR", bebas(205))
texto(im, (60, 450), "SIEMPRE GANA?", bebas(205))
guardar(im, "miniatura_pol.jpg")

# B: las tres palabras con el emblema de GTA V a la derecha (Lohan y Target son casos de GTA V)
im = fondo("mi_azotea.jpg", 1.0, "izq", 0.6, ancho=0.7)  # distinto del fondo de la C del vídeo 5
texto(im, (55, 60), "PROHIBIDO.", bebas(165))
texto(im, (55, 225), "DEMANDADO.", bebas(165), BLANCO)
texto(im, (55, 390), "RETIRADO.", bebas(165))
texto(im, (62, 590), "GTA · 1997-2026", mont(46, 900), BLANCO)
logo(im, (800, 150), 400, "gta5_v.png")  # emblema sacado del SVG oficial sin la placa común (emblema_v.py)
guardar(im, "miniatura_pol_b.jpg")

# C: todo centrado; el logo de Rockstar entre «de polémicas» y los casos
im = fondo("t2_mar_atardecer.jpg", 1.1, "centro", 0.4, BANDAS)
texto(im, (0, 20), "29 AÑOS", bebas(210), centro=True)
texto(im, (0, 235), "DE POLÉMICAS", bebas(120), BLANCO, centro=True)
logo(im, (0, 385), 150, "rockstar.png", centro=True)
texto(im, (0, 575), "Hot Coffee · Australia · Hackeo", mont(42, 800), BLANCO, centro=True)
guardar(im, "miniatura_pol_c.jpg")

# ======================================================== Vídeo 7 · Las radios de GTA
im = fondo("t1_neones.jpg", 1.2, "izq", 0.5)
texto(im, (60, 70), "¿TU RADIO", bebas(200))
texto(im, (60, 260), "FAVORITA?", bebas(200))
texto(im, (66, 480), "1997 → 2026", mont(70, 900), BLANCO)
guardar(im, "miniatura_rad.jpg")

im = fondo("t1_coches_noche.jpg", 1.2, "der", 0.7, ancho=0.7)  # velo más fuerte a la derecha para el subtítulo
texto(im, (60, 90), "LAS RADIOS", bebas(170), der=True)
texto(im, (60, 250), "DE GTA", bebas(170), der=True)
texto(im, (60, 455), "1997 → GTA VI", mont(64, 900), BLANCO, der=True)
texto(im, (60, 560), "Y SUS CANCIONES", mont(50, 900), BLANCO, sombra=230, der=True)
texto(im, (60, 625), "RETIRADAS", mont(50, 900), BLANCO, sombra=230, der=True)
guardar(im, "miniatura_rad_b.jpg")

# C: cuatro emisoras en grande, cada una con su logo (logos de los juegos, de la wiki de GTA), sin la pregunta
im = fondo("t2_conduciendo.jpg", 1.2, "izq", 0.65, BANDAS, ancho=0.7)  # tráiler 2, 30,5 s: un personaje al volante
EMISORAS = [("FLASH FM", None, "logo_flashfm.png", None), ("K-DST", BLANCO, "logo_kdst.png", 120),
            ("V-ROCK", BLANCO, "logo_vrock.png", None), ("WCTR", BLANCO, "logo_wctr.png", None)]
for i, (s, c, archivo, brillo) in enumerate(EMISORAS):
    y = 12 + i * 176
    icono(im, (115, y + 86), 158, archivo, brillo)
    texto(im, (225, y + 2), s, bebas(172), c)
guardar(im, "miniatura_rad_c.jpg")
print("9 miniaturas en", SAL)
