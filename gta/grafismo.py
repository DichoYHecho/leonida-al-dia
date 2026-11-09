"""Grafismo de cristal (9 nov 2026): HUD y tarjeta translúcidos, estilo Apple, con colores de Miami.

- Barra de progreso: pastilla de cristal arriba en el centro, relleno rosa → turquesa.
- Crédito pequeño justo debajo de la barra.
- Tarjeta de cristal en el tercio inferior (por encima de los botones de las redes), con fundido de 0,3 s:
  línea turquesa (tipo, o «NUEVO · 5 NOV» si sale una captura de la galería nueva), título blanco y línea rosa.
Sin intro de marca ni transiciones de color: el protagonismo es de las imágenes."""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
INTER = "/usr/share/fonts/opentype/inter"
F_TIT, F_TXT = f"{INTER}/InterDisplay-Black.otf", f"{INTER}/InterDisplay-SemiBold.otf"
ROSA, TURQ, BLANCO = (255, 79, 160), (0, 229, 255), (255, 255, 255)
TINTE = (20, 14, 35, 107)        # cristal oscuro (42 %)
BORDE = (255, 255, 255, 46)      # borde fino (18 %)
TARJ_ABAJO = 1560                # borde inferior de la tarjeta; debajo quedan los botones de las redes
TARJ_X = (110, 970)
FUNDIDO = 0.3
_f, _grad = {}, {}
ACTUAL = ""  # foto o vídeo que se ve ahora mismo (lo apunta render2.fondo_en)


def fuente(p, s):
    k = (p, int(s))
    if k not in _f:
        _f[k] = ImageFont.truetype(p, int(s))
    return _f[k]


def _mezclar(img, capa, alfa):
    if alfa < 1:
        capa.putalpha(capa.getchannel("A").point(lambda v: int(v * alfa)))
    img.alpha_composite(capa)


def cristal(img, caja, radio, alfa=1.0):
    """Recuadro de cristal: desenfoca lo que hay detrás, lo oscurece un poco y le pone un borde fino."""
    x0, y0, x1, y1 = [int(v) for v in caja]
    if alfa <= 0 or x1 <= x0 or y1 <= y0:
        return
    trozo = img.crop((x0, y0, x1, y1)).convert("RGBA").filter(ImageFilter.GaussianBlur(26))
    trozo = Image.alpha_composite(trozo, Image.new("RGBA", trozo.size, TINTE))
    m = Image.new("L", trozo.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, x1 - x0 - 1, y1 - y0 - 1], radio, fill=int(255 * alfa))
    img.paste(trozo, (x0, y0), m)
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(capa).rounded_rectangle([x0, y0, x1 - 1, y1 - 1], radio, outline=BORDE, width=2)
    _mezclar(img, capa, alfa)


def degradado(ancho, alto):
    k = (ancho, alto)
    if k not in _grad:
        g = Image.new("RGB", (ancho, 1))
        for x in range(ancho):
            a = x / max(1, ancho - 1)
            g.putpixel((x, 0), tuple(int(ROSA[i] * (1 - a) + TURQ[i] * a) for i in range(3)))
        _grad[k] = g.resize((ancho, alto))
    return _grad[k]


def barra(img, t, dur):
    """Barra de progreso en una pastilla de cristal, arriba en el centro."""
    x0, x1, y0, y1 = 300, 780, 34, 86
    cristal(img, (x0, y0, x1, y1), 26)
    tx0, tx1, ty0, ty1 = x0 + 30, x1 - 30, 57, 63
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(capa).rounded_rectangle([tx0, ty0, tx1, ty1], 3, fill=(255, 255, 255, 56))
    img.alpha_composite(capa)
    ancho = int((tx1 - tx0) * min(max(t / dur, 0), 1))
    if ancho > 2:
        m = Image.new("L", (tx1 - tx0, ty1 - ty0), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, ancho, ty1 - ty0 - 1], 3, fill=255)
        img.paste(degradado(tx1 - tx0, ty1 - ty0), (tx0, ty0), m)


def credito(img, txt):
    """Crédito o fuente, pequeño, justo debajo de la barra."""
    if not txt:
        return
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    tam = 24
    while tam > 17 and d.textlength(txt, font=fuente(F_TXT, tam)) > W - 160:
        tam -= 1
    d.text((W / 2, 102), txt, font=fuente(F_TXT, tam), fill=(255, 255, 255, 200), anchor="ma",
           stroke_width=1, stroke_fill=(0, 0, 0, 90))
    img.alpha_composite(capa)


def es_nueva(ruta):
    """¿Es una captura de «The Launch Gallery» (5 nov)?"""
    try:
        import medios
        n = os.path.splitext(os.path.basename(str(ruta or "")))[0]
        return "nueva" in medios.CAPTURAS.get(n, {}).get("notas", "")
    except Exception:
        return False


def textos(cfg):
    sello = "NUEVO · 5 NOV" if es_nueva(ACTUAL) else (cfg.get("tipo") or "GTA 6").upper()
    titulo = (cfg.get("etiqueta") or "GTA 6").strip()
    return sello, titulo, (cfg.get("cuenta") or "").strip()


def alto_tarjeta(cfg):
    _, _, rosa = textos(cfg)
    return 34 + 34 + 82 + (52 if rosa else 0) + 30


def tarjeta(img, t, cfg, ini, fin):
    """Tarjeta de cristal del tercio inferior, visible de «ini» a «fin» con fundido."""
    if t < ini or t >= fin:
        return
    alfa = min(1.0, (t - ini) / FUNDIDO, (fin - t) / FUNDIDO)
    sello, titulo, rosa = textos(cfg)
    x0, x1 = TARJ_X
    y1 = TARJ_ABAJO
    y0 = y1 - alto_tarjeta(cfg)
    cristal(img, (x0, y0, x1, y1), 52, alfa)
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    cx, y = W / 2, y0 + 34
    d.text((cx, y), sello, font=fuente(F_TXT, 26),
           fill=TURQ + (255,), anchor="ma")
    y += 34
    tam = 66
    while tam > 40 and d.textlength(titulo, font=fuente(F_TIT, tam)) > (x1 - x0) - 80:
        tam -= 2
    d.text((cx, y + 4), titulo, font=fuente(F_TIT, tam), fill=BLANCO + (255,), anchor="ma")
    y += 82
    if rosa:
        tam = 36
        while tam > 24 and d.textlength(rosa, font=fuente(F_TIT, tam)) > (x1 - x0) - 80:
            tam -= 2
        d.text((cx, y + 4), rosa, font=fuente(F_TIT, tam), fill=ROSA + (255,), anchor="ma")
    _mezclar(img, capa, alfa)
