"""Montaje V2 de los vídeos de «Leónida al Día» (prototipo del 25 oct 2026).

Cambios frente a render.py (plantilla estática):
- Tipografía de tráiler (Anton, licencia libre OFL) para el gancho, el número y la pregunta; Inter Display Black
  para los subtítulos.
- Subtítulos de 1 a 3 palabras; la palabra que suena va sobre una pastilla del color del tipo.
- Movimiento de cámara con zoom y paneo suaves (hacia el foco de la captura) y transiciones (barrido o zoom con
  destello) cuando cambia la imagen, con un «whoosh» en la música.
- Primer fotograma pensado como portada: el gancho entero y grande desde el fotograma 0.
- Intro de marca (destello de luz al empezar) y cierre de marca (logo y @) en el último segundo.
- Barra de progreso arriba.
- Cuenta atrás (cfg["cuenta"]): número gigante que baja del de ayer al de hoy con impacto, y luego «DATO DEL DÍA».

Entrada: igual que render.montar (trozos, tiempos, voz, capturas, etiqueta, tipo, personaje, cuenta, pie, salida,
semilla, tmp) más, opcionales: «palabras» [(texto, ini, fin)] de Whisper y «cuenta_atras» (ver montar).
"""
import math, os, re, subprocess
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
AQUI = os.path.dirname(os.path.abspath(__file__))
FA = os.path.join(AQUI, "fuentes", "Anton-Regular.ttf")
INTER = "/usr/share/fonts/opentype/inter"
FB, FSB = f"{INTER}/InterDisplay-Black.otf", f"{INTER}/InterDisplay-SemiBold.otf"
PINK, TEAL, AMBER, WHITE, NOCHE = (255, 64, 129), (46, 230, 214), (255, 196, 76), (255, 255, 255), (10, 14, 38)
COLOR_TIPO = {"Noticia": TEAL, "Dato": AMBER, "Prensa": WHITE}
MAX_MB = 4.7
TRANS = 0.30          # duración de una transición (s)
CUENTA_IMPACTO = 0.80 # momento en que el número de hoy «cae»

_fuentes = {}


def fuente(p, s):
    k = (p, int(s))
    if k not in _fuentes:
        _fuentes[k] = ImageFont.truetype(p, int(s))
    return _fuentes[k]


def suave(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def sale(x):  # ease-out con rebote ligero
    x = min(max(x, 0.0), 1.0)
    c1, c3 = 1.4, 2.4
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


# ---------------------------------------------------------------- sonido
def musica_base(dur, semilla):
    try:
        import render
        return render.musica(dur, semilla)
    except Exception:  # prototipo fuera del repositorio
        sr = 44100
        t = np.arange(int(dur * sr)) / sr
        L = 0.05 * np.sin(2 * np.pi * 55 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * t / 0.6) ** 2)
        return np.stack([L, L], 1).astype(np.float32), sr


def whoosh(sr, largo=0.45, seed=1):
    n = int(largo * sr)
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(n).astype(np.float32)
    t = np.linspace(0, 1, n, dtype=np.float32)
    # filtro paso banda que sube: suavizado variable
    out = np.zeros(n, np.float32)
    acc = 0.0
    for i in range(n):
        a = 0.02 + 0.5 * t[i] ** 2
        acc += a * (x[i] - acc)
        out[i] = acc
    env = np.sin(np.pi * t) ** 2 * (0.4 + 0.6 * t)
    out = out * env
    return out / (np.max(np.abs(out)) + 1e-6)


def golpe(sr, largo=0.9):
    n = int(largo * sr)
    t = np.arange(n) / sr
    f = 38 + 90 * np.exp(-t * 18)
    x = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t * 4.5)
    x += np.random.default_rng(2).standard_normal(n) * np.exp(-t * 30) * 0.25
    return (x / np.max(np.abs(x))).astype(np.float32)


def mezclar(cfg, dur, cortes, impactos):
    voz, sr = sf.read(cfg["voz"], dtype="float32")
    if voz.ndim > 1:
        voz = voz.mean(1)
    voz = voz / (np.max(np.abs(voz)) + 1e-6) * 0.9
    m, msr = musica_base(dur, cfg.get("semilla", 3))
    n = len(m)
    v = np.interp(np.linspace(0, len(voz) - 1, int(len(voz) * msr / sr)), np.arange(len(voz)), voz)
    mezcla = m * 0.15
    w = whoosh(msr)
    for c in cortes:
        i0 = int((c - 0.30) * msr)
        if 0 <= i0 < n:
            seg = w[:n - i0] * 0.22
            mezcla[i0:i0 + len(seg)] += seg[:, None]
    g = golpe(msr)
    for c in impactos:
        i0 = int(c * msr)
        if 0 <= i0 < n:
            seg = g[:n - i0] * 0.55
            mezcla[i0:i0 + len(seg)] += seg[:, None]
    mezcla[:len(v)] += v[:n, None] * 0.95
    mezcla = mezcla / max(1.0, np.max(np.abs(mezcla)) / 0.95)
    ruta = os.path.join(cfg["tmp"], "mezcla.wav")
    sf.write(ruta, mezcla.astype(np.float32), msr)
    return ruta


# ---------------------------------------------------------------- palabras y tiempos
def tokens(txt):
    """Palabras del guion, sin separar «GTA 6»."""
    out = []
    for p in txt.split():
        if out and out[-1].upper().endswith("GTA") and re.match(r"^(6|VI)\b", p):
            out[-1] += " " + p
        else:
            out.append(p)
    return out


def tiempos_palabras(trozos, tiempos, palabras=None):
    """[(trozo, palabra, ini, fin)]. Con «palabras» (de Whisper) se usan sus tiempos; si no, se reparten los del
    trozo según la longitud de cada palabra."""
    out = []
    for k, (txt, (a, b)) in enumerate(zip(trozos, tiempos)):
        ws = tokens(txt)
        L = [len(w) + 2 for w in ws]
        tot, acc = sum(L), 0
        for w, l in zip(ws, L):
            ini = a + (b - a) * acc / tot
            acc += l
            out.append([k, w, ini, a + (b - a) * acc / tot])
    if palabras:
        # palabras de Whisper ya alineadas al guion, en el mismo orden (mismo número)
        if len(palabras) == len(out):
            for o, (_, i, f) in zip(out, palabras):
                o[2], o[3] = i, f
    return [tuple(o) for o in out]


def grupos_subtitulos(pals, trozos_sub, f, ancho=860, maximo=3):
    """Agrupa las palabras de los trozos de subtítulo en bloques de 1 a 3 palabras que quepan en una línea."""
    d = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    grupos = []
    for k in trozos_sub:
        ws = [p for p in pals if p[0] == k]
        cur = []
        for p in ws:
            prueba = " ".join(x[1] for x in cur + [p]).upper()
            if cur and (len(cur) >= maximo or d.textlength(prueba, font=f) > ancho or re.search(r"[.,;:?!]$", cur[-1][1])):
                # no dejar una palabra corta colgando al final
                if len(cur) > 1 and len(cur[-1][1]) <= 2:
                    pasa = cur.pop()
                    grupos.append(cur)
                    cur = [pasa]
                else:
                    grupos.append(cur)
                    cur = []
            cur.append(p)
        if cur:
            grupos.append(cur)
    return grupos


# ---------------------------------------------------------------- imágenes de fondo
class Fondo:
    def __init__(self, ruta, foco=0.5, plano="retrato", estilo=0):
        im = Image.open(ruta).convert("RGB")
        s = max(W / im.width, H / im.height) * 1.22
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        a = np.asarray(im).astype(np.float32) / 255
        # gradación «Vice»: algo más de contraste y color, sombras hacia azul y luces hacia cálido
        gris = a.mean(2, keepdims=True)
        a = gris + (a - gris) * 1.15
        a = (a - 0.5) * 1.07 + 0.5
        a += np.array([0.0, 0.0, 0.035]) * (1 - gris) + np.array([0.03, 0.01, -0.01]) * gris
        self.im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
        self.foco = foco
        self.plano = plano
        self.estilo = estilo  # 0 acercar, 1 alejar, 2 barrido

    def ventana(self, p, extra=1.0):
        """Ventana (x0, y0, ancho, alto) en la imagen para el progreso p (0-1) del tramo."""
        bw, bh = self.im.size
        z0, z1 = (1.0, 1.13) if self.estilo == 0 else (1.13, 1.0) if self.estilo == 1 else (1.06, 1.06)
        q = 0.15 * suave(p) + 0.85 * p
        z = (z0 + (z1 - z0) * q) * extra
        sh = bh / z
        sw = sh * W / H
        if sw > bw:
            sw = bw
            sh = sw * H / W
        cx_f = self.foco * bw
        if self.estilo == 2 or self.plano == "panorámica":
            rango = min(bw - sw, bw * 0.22)
            c0 = np.clip(cx_f - rango / 2, sw / 2, bw - sw / 2)
            cx = c0 + rango * q
        else:
            cx = cx_f + (bw / 2 - cx_f) * 0.15 * (1 - q)
        cx = float(np.clip(cx, sw / 2, bw - sw / 2))
        cy = bh / 2
        return cx - sw / 2, cy - sh / 2, sw, sh

    def fotograma(self, p, extra=1.0, dx=0.0):
        x0, y0, sw, sh = self.ventana(p, extra)
        x0 -= dx * sw / W
        return self.im.transform((W, H), Image.AFFINE, (sw / W, 0, x0, 0, sh / H, y0), resample=Image.BILINEAR)


def plan_tramos(n, dur, cortes_deseados):
    """Tramos [(fondo, ini, fin)] con los cortes en los momentos deseados (o repartidos)."""
    cortes = [0.0] + list(cortes_deseados[: n - 1]) + [dur]
    if len(cortes) < n + 1:
        cortes = [dur * k / n for k in range(n + 1)]
    return [(k, cortes[k], cortes[k + 1]) for k in range(n)]


def fondo_en(t, fondos, tramos, estilo_trans):
    """Fotograma de fondo en el instante t, con la transición si está cerca de un corte."""
    q = max(j for j in range(len(tramos)) if tramos[j][1] <= t + 1e-6)
    k, a, b = tramos[q]
    p = (t - a) / max(b - a, 1e-3)
    # ¿cerca del corte siguiente o del anterior?
    efecto, lado = 0.0, 0
    if q + 1 < len(tramos) and b - t < TRANS / 2:
        efecto, lado = 1 - (b - t) / (TRANS / 2), -1
    elif q > 0 and t - a < TRANS / 2:
        efecto, lado = 1 - (t - a) / (TRANS / 2), 1
    if efecto <= 0:
        return fondos[k].fotograma(p), 0.0
    e = efecto ** 2
    tipo = estilo_trans[q if lado < 0 else q - 1]
    if tipo == "barrido":
        desp = e * W * 0.55 * (1 if lado < 0 else -1)
        capas = [np.asarray(fondos[k].fotograma(p, dx=desp + s * e * 60), np.float32) for s in (-1.5, -0.5, 0.5, 1.5)]
        img = Image.fromarray(np.mean(capas, 0).astype(np.uint8))
    else:  # zoom
        img = fondos[k].fotograma(p, extra=1 + 0.22 * e)
        if e > 0.3:
            img = img.filter(ImageFilter.GaussianBlur(6 * e))
    return img, e * 0.55


# ---------------------------------------------------------------- capas de texto
def texto(d, xy, txt, f, color, borde=0, ancla="mm", sombra=True):
    x, y = xy
    if sombra:
        d.text((x + 5, y + 7), txt, font=f, fill=(0, 0, 0, 140), anchor=ancla, stroke_width=borde, stroke_fill=(0, 0, 0, 140))
    d.text((x, y), txt, font=f, fill=color, anchor=ancla, stroke_width=borde, stroke_fill=(0, 0, 0))


def sol(d, cx, cy, r):
    for i in range(r * 2):
        yy = cy - r + i
        f = i / (2 * r)
        c = tuple(int(AMBER[k] + (PINK[k] - AMBER[k]) * f) for k in range(3))
        dx = int((r * r - (yy - cy) ** 2) ** 0.5) if abs(yy - cy) < r else 0
        if i > r * 1.05 and (i // 4) % 2 == 1:
            continue
        d.line([(cx - dx, yy), (cx + dx, yy)], fill=c)


def pastilla(img, x, y, txt, f, fondo, color, derecha=False, alfa=1.0):
    d = ImageDraw.Draw(img)
    w = d.textlength(txt, font=f)
    h = f.size + 22
    x0 = x - w - 44 if derecha else x
    a = int(255 * alfa)
    d.rounded_rectangle([x0, y, x0 + w + 44, y + h], h // 2, fill=fondo + (a,))
    d.text((x0 + 22, y + 10), txt, font=f, fill=color + (a,))


def capa_viñeta():
    yy = np.arange(H)[:, None] / H
    xx = np.arange(W)[None, :] / W
    r = np.sqrt((xx - 0.5) ** 2 * 1.4 + (yy - 0.5) ** 2)
    a = np.clip((r - 0.35) * 1.6, 0, 1) * 150
    top = np.clip(1 - np.arange(H) / 520, 0, 1)[:, None] * 190
    bot = np.clip((np.arange(H) - 1300) / 620, 0, 1)[:, None] * 210
    alfa = np.maximum(np.maximum(a, top), bot)
    g = np.zeros((H, W, 4), np.uint8)
    g[..., 3] = np.clip(alfa, 0, 255).astype(np.uint8)
    return Image.fromarray(g, "RGBA")


def cabecera(img, t, cfg, mostrar_cuenta=True):
    """Logo y pastillas (fijos desde el fotograma 0, para que la portada lleve la marca)."""
    d = ImageDraw.Draw(img)
    e, dy = 1.0, 0
    sol(d, 92, 112 + dy, 34)
    d.text((142, 78 + dy), "LEÓNIDA", font=fuente(FB, 40), fill=WHITE)
    d.text((142, 120 + dy), "AL DÍA", font=fuente(FB, 28), fill=TEAL)
    if mostrar_cuenta and cfg.get("cuenta"):
        pastilla(img, W - 48 + int((1 - e) * 400), 86, cfg["cuenta"], fuente(FB, 30), PINK, WHITE, derecha=True)
    et = (cfg.get("etiqueta") or "GTA 6").upper()[:24]
    if et:
        e2 = 1.0
        color = PINK if cfg.get("personaje") else COLOR_TIPO.get(cfg.get("tipo"), WHITE)
        pastilla(img, 48 - int((1 - e2) * 600), 190, et, fuente(FB, 30), color, NOCHE)


def barrido_luz(img, t):
    """Destello diagonal de marca entre 0,1 y 0,6 s."""
    if not 0.1 < t < 0.6:
        return img
    p = (t - 0.1) / 0.5
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    x = -600 + p * (W + 1200)
    for i, (c, a) in enumerate(((AMBER, 50), (PINK, 70), (WHITE, 60))):
        o = i * 70
        d.polygon([(x + o, 0), (x + o + 90, 0), (x + o - 500, H), (x + o - 590, H)], fill=c + (a,))
    capa = capa.filter(ImageFilter.GaussianBlur(25))
    return Image.alpha_composite(img, capa)


def palabra_img(txt, f, color, borde, sombra=True):
    """Imagen de una palabra centrada verticalmente en su línea (para que todas queden alineadas)."""
    d = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    an = d.textlength(txt, font=f) + 2 * borde + 24
    al = int(f.size * 1.5) + 2 * borde
    im = Image.new("RGBA", (int(an) + 12, al + 12), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    c = (im.width / 2, im.height / 2)
    if sombra:
        dd.text((c[0] + 4, c[1] + 6), txt, font=f, fill=(0, 0, 0, 150), anchor="mm", stroke_width=borde, stroke_fill=(0, 0, 0, 150))
    dd.text(c, txt, font=f, fill=color, anchor="mm", stroke_width=borde, stroke_fill=(0, 0, 0))
    return im


_cache_pal = {}


def poner_palabras(img, lineas, cy, f, acento, t, borde=9, interlinea=1.12, espacio=None, caja=True):
    """Dibuja líneas de palabras centradas. La que suena: con caja=True, sobre una pastilla del color del tipo
    (texto oscuro, la pastilla «salta» al entrar); con caja=False, solo cambia de color.
    lineas: [[(palabra, ini, fin), ...], ...]"""
    d = ImageDraw.Draw(img)
    esp = espacio if espacio is not None else f.size * 0.30 + 2 * borde
    alto = f.size * interlinea
    y0 = cy - alto * (len(lineas) - 1) / 2
    for li, linea in enumerate(lineas):
        anchos = [d.textlength(w.upper(), font=f) + 2 * borde for w, _, _ in linea]
        x = W / 2 - (sum(anchos) + esp * (len(linea) - 1)) / 2
        yc = y0 + li * alto
        for (w, a, b), an in zip(linea, anchos):
            activa = a - 0.04 <= t < b + 0.02
            cx = x + an / 2
            if activa and caja:
                e = sale((t - a + 0.04) / 0.12)
                pw, ph = (an + 34) * (0.9 + 0.1 * e), f.size * 1.18 * (0.9 + 0.1 * e)
                d.rounded_rectangle([cx - pw / 2, yc - ph / 2 + 4, cx + pw / 2, yc + ph / 2 + 4], int(ph * 0.22),
                                    fill=acento + (255,))
                color, bd = NOCHE, 0
            else:
                color, bd = (acento if activa else WHITE), borde
            k = (w, f.path, f.size, color, bd)
            if k not in _cache_pal:
                _cache_pal[k] = palabra_img(w.upper(), f, color, bd, sombra=bd > 0)
            im = _cache_pal[k]
            img.alpha_composite(im, (int(cx - im.width / 2), int(yc - im.height / 2)))
            x += an + esp


def partir_lineas(ws, f, ancho):
    d = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    lineas, cur = [], []
    for w in ws:
        prueba = " ".join(x[0] for x in cur + [w]).upper()
        if cur and d.textlength(prueba, font=f) > ancho:
            lineas.append(cur)
            cur = []
        cur.append(w)
    if cur:
        lineas.append(cur)
    return lineas


def gancho(img, t, ws, acento, salida):
    """Gancho grande arriba (portada). ws: [(palabra, ini, fin)]. Sale hacia arriba al terminar."""
    tam = 132
    while tam > 84:
        f = fuente(FA, tam)
        lineas = partir_lineas(ws, f, 960)
        if len(lineas) <= 3:
            break
        tam -= 6
    e = suave((t - salida) / 0.22) if t > salida else 0.0
    if e >= 1:
        return
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    poner_palabras(capa, lineas, 470, f, acento, t, borde=0, interlinea=1.04, espacio=f.size * 0.24, caja=False)
    if e > 0:
        capa = capa.transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, 260 * e), resample=Image.BILINEAR)
        capa.putalpha(capa.getchannel("A").point(lambda v: int(v * (1 - e))))
    img.alpha_composite(capa)


def pregunta(img, t, txt, inicio, apagar=1.0):
    e = sale((t - inicio) / 0.35)
    if e <= 0 or apagar <= 0:
        return
    tam = 96
    while tam > 60:
        f = fuente(FA, tam)
        lineas = partir_lineas([(w, 0, 0) for w in tokens(txt)], f, 860)
        if len(lineas) <= 3:
            break
        tam -= 4
    alto = f.size * 1.08
    caja_h = alto * len(lineas) + 80
    y0 = 760 - caja_h / 2
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    d.rounded_rectangle([70, y0, W - 70, y0 + caja_h], 36, fill=NOCHE + (215,))
    d.rounded_rectangle([70, y0, 84, y0 + caja_h], 7, fill=PINK + (255,))
    for i, l in enumerate(lineas):
        d.text((W / 2, y0 + 40 + i * alto + alto / 2), " ".join(w for w, _, _ in l).upper(), font=f, fill=AMBER, anchor="mm")
    d.text((W / 2, y0 + caja_h + 50), "TE LEO EN COMENTARIOS", font=fuente(FB, 34), fill=WHITE, anchor="mm",
           stroke_width=4, stroke_fill=(0, 0, 0))
    esc = 0.85 + 0.15 * e
    if esc != 1:
        capa = capa.transform((W, H), Image.AFFINE, (1 / esc, 0, W / 2 * (1 - 1 / esc), 0, 1 / esc, 760 * (1 - 1 / esc)),
                              resample=Image.BILINEAR)
    capa.putalpha(capa.getchannel("A").point(lambda v: int(v * min(1, e * 1.5) * apagar)))
    img.alpha_composite(capa)


def cierre_marca(img, t, inicio):
    """Último segundo: fondo oscurecido, logo grande y @."""
    e = suave((t - inicio) / 0.3)
    if e <= 0:
        return img
    osc = Image.new("RGBA", (W, H), NOCHE + (int(200 * e),))
    img = Image.alpha_composite(img, osc)
    d = ImageDraw.Draw(img)
    a = int(255 * e)
    dy = int((1 - sale((t - inicio) / 0.45)) * 80)
    sol(d, W // 2, 735 + dy, 90)
    texto(d, (W / 2, 950 + dy), "LEÓNIDA AL DÍA", fuente(FA, 120), WHITE + (a,), sombra=False)
    texto(d, (W / 2, 1060 + dy), "@leonidaaldia", fuente(FB, 46), TEAL + (a,), sombra=False)
    texto(d, (W / 2, 1130 + dy), "Noticias y datos de GTA 6 cada día", fuente(FSB, 34), (220, 220, 230, a), sombra=False)
    return img


def barra_progreso(img, t, dur, color):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, int(W * t / dur), 7], fill=color)


def pie(img, txt):
    d = ImageDraw.Draw(img)
    tam = 26
    while tam > 18 and d.textlength(txt, font=fuente(FSB, tam)) > W - 80:
        tam -= 2
    d.text((W / 2, 1850), txt, font=fuente(FSB, tam), fill=(215, 215, 225), anchor="ma")


# ---------------------------------------------------------------- cuenta atrás
def numero_cuenta(img, t, ca, acento):
    """Número gigante: muestra el de ayer y en CUENTA_IMPACTO cae el de hoy (con rebote, destello y temblor).
    El fotograma 0 enseña ya el de hoy (portada)."""
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    fN = fuente(FA, 600)
    cy = 900
    texto(d, (W / 2, 470), ca.get("arriba", "FALTAN"), fuente(FA, 120), WHITE, ancla="mm")
    portada = t < 1 / FPS
    t0 = CUENTA_IMPACTO - 0.32
    if portada or t >= CUENTA_IMPACTO:
        rebote = 1.0 if portada else 1 + 0.10 * math.exp(-(t - CUENTA_IMPACTO) * 9) * math.cos((t - CUENTA_IMPACTO) * 30)
        num = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dn = ImageDraw.Draw(num)
        dn.text((W / 2 + 10, cy + 14), str(ca["a"]), font=fN, fill=(0, 0, 0, 160), anchor="mm")
        dn.text((W / 2, cy), str(ca["a"]), font=fN, fill=acento, anchor="mm")
        if rebote != 1:
            num = num.transform((W, H), Image.AFFINE, (1 / rebote, 0, W / 2 * (1 - 1 / rebote), 0, 1 / rebote,
                                                       cy * (1 - 1 / rebote)), resample=Image.BILINEAR)
        capa.alpha_composite(num)
    else:
        p = suave((t - t0) / 0.32) if t > t0 else 0.0
        # como un contador mecánico: el de ayer sale por abajo y el de hoy entra por arriba, dentro de una franja
        rollo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dr = ImageDraw.Draw(rollo)
        salto = 640
        dr.text((W / 2, cy + p * salto), str(ca["de"]), font=fN, fill=WHITE, anchor="mm")
        if p > 0:
            dr.text((W / 2, cy - (1 - p) * salto), str(ca["a"]), font=fN, fill=acento, anchor="mm")
        mascara = Image.new("L", (W, H), 0)
        ImageDraw.Draw(mascara).rectangle([0, cy - 300, W, cy + 300], fill=255)
        rollo.putalpha(Image.composite(rollo.getchannel("A"), Image.new("L", (W, H), 0), mascara))
        capa.alpha_composite(rollo)
    e = sale((t - 0.25) / 0.4) if t > 0.25 else (1.0 if portada else 0.0)
    if e > 0:
        texto(d, (W / 2, 1300 + (1 - e) * 60), ca.get("abajo", "DÍAS PARA GTA 6"), fuente(FA, 118),
              PINK + (int(255 * min(1, e)),), ancla="mm")
    img.alpha_composite(capa)


def lineas_cuenta(img, t, ca, desde):
    e = sale((t - desde) / 0.35)
    if e <= 0:
        return
    d = ImageDraw.Draw(img)
    pastilla(img, W // 2 - int(d.textlength(ca["fecha"], font=fuente(FB, 38)) / 2) - 22, 1400 + int((1 - e) * 50),
             ca["fecha"], fuente(FB, 38), WHITE, NOCHE, alfa=min(1, e))
    if ca.get("precarga"):
        texto(d, (W / 2, 1530 + (1 - e) * 50), ca["precarga"], fuente(FB, 42), AMBER + (int(255 * min(1, e)),),
              borde=5, ancla="mm")


def sello(img, t, txt, inicio, color):
    """Rótulo grande que «estampa» (DATO DEL DÍA) y desaparece en menos de un segundo."""
    if t < inicio:
        return
    p = (t - inicio)
    f = fuente(FA, 150)
    if p < 0.9:
        esc = 1.6 - 0.6 * sale(p / 0.25)
        y = 860
        capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(capa)
        w = d.textlength(txt, font=f)
        d.rounded_rectangle([W / 2 - w / 2 - 40, y - 105, W / 2 + w / 2 + 40, y + 105], 30, fill=color + (255,))
        d.text((W / 2, y), txt, font=f, fill=NOCHE, anchor="mm")
        alfa = 1 - suave((p - 0.65) / 0.25)
        capa = capa.transform((W, H), Image.AFFINE, (1 / esc, 0, W / 2 * (1 - 1 / esc), 0, 1 / esc, y * (1 - 1 / esc)),
                              resample=Image.BILINEAR)
        capa.putalpha(capa.getchannel("A").point(lambda v: int(v * alfa * min(1, p / 0.08))))
        img.alpha_composite(capa)


# ---------------------------------------------------------------- montaje
def montar(cfg):
    """Devuelve {duracion, mb}. Claves extra opcionales:
    - palabras: [(palabra, ini, fin)] alineadas con el guion (Whisper).
    - cuenta_atras: {"de": 26, "a": 25, "fecha": "JUEVES 19 DE NOVIEMBRE", "precarga": "PRECARGA: 12 DE NOVIEMBRE",
      "trozos_intro": 2, "trozo_dato": 2, "fondo_intro": ruta, "foco_intro": 0.5}
      Los «trozos_intro» primeros trozos se ven con el número gigante (sin subtítulos); el trozo «trozo_dato» es
      «Dato del día:» y estampa el rótulo; después, subtítulos normales con las capturas del dato."""
    trozos, tiempos = cfg["trozos"], cfg["tiempos"]
    info = sf.info(cfg["voz"])
    dur = info.frames / info.samplerate + 1.3
    ca = cfg.get("cuenta_atras")
    acento = PINK if cfg.get("personaje") else COLOR_TIPO.get(cfg.get("tipo"), AMBER)
    pals = tiempos_palabras(trozos, tiempos, cfg.get("palabras"))
    ultimo = len(trozos) - 1

    # fondos y cortes
    caps = [Fondo(r, f, p, estilo=i % 3) for i, (r, f, p) in enumerate(cfg["capturas"])]
    if ca:
        intro = Fondo(ca["fondo_intro"], ca.get("foco_intro", 0.5), "retrato", estilo=0)
        fondos = [intro] + caps
        corte_dato = tiempos[ca["trozo_dato"]][0] - 0.05
        resto = caps
        cortes = [corte_dato]
        if len(resto) > 1:
            ini, fin = tiempos[ca["trozo_dato"] + 1][0], tiempos[ultimo][0]
            for j in range(1, len(resto)):
                cortes.append(_corte_cerca(ini + (fin - ini) * j / len(resto), tiempos))
    else:
        fondos = caps
        ini, fin = tiempos[1][0], tiempos[ultimo][0]
        cortes = [_corte_cerca(tiempos[1][0] - 0.05 if len(fondos) > 1 and j == 0 else ini + (fin - ini) * j / max(len(fondos) - 1, 1), tiempos)
                  for j in range(len(fondos) - 1)]
    tramos = plan_tramos(len(fondos), dur, cortes)
    estilo_trans = ["barrido" if j % 2 == 0 else "zoom" for j in range(len(tramos))]
    impactos = [CUENTA_IMPACTO] if ca else []
    audio = mezclar(cfg, dur, [b for _, _, b in tramos[:-1]], impactos)

    # subtítulos
    t_sub_ini = (ca["trozo_dato"] + 1) if ca else 1
    f_sub = fuente(FB, 90)
    grupos = grupos_subtitulos(pals, range(t_sub_ini, ultimo), f_sub)
    gancho_ws = [(w, a, b) for k, w, a, b in pals if k == 0]
    viñeta = capa_viñeta()
    salida_gancho = tiempos[0][1] + 0.12
    t_pregunta = tiempos[ultimo][0] - 0.05
    t_cierre = max(tiempos[ultimo][1] + 0.25, dur - 1.05)
    salida = cfg["salida"]

    def fotograma(i):
        t = i / FPS
        base, flash = fondo_en(t, fondos, tramos, estilo_trans)
        img = base.convert("RGBA")
        temblor = 0
        if ca and CUENTA_IMPACTO <= t < CUENTA_IMPACTO + 0.25:
            temblor = int(14 * math.exp(-(t - CUENTA_IMPACTO) * 14) * math.sin(t * 90))
            flash = max(flash, 0.6 * math.exp(-(t - CUENTA_IMPACTO) * 12))
        img = Image.alpha_composite(img, viñeta)
        en_intro = ca and t < tiempos[ca["trozo_dato"]][0] - 0.05
        if en_intro:
            img = Image.alpha_composite(img, Image.new("RGBA", (W, H), NOCHE + (90,)))
            numero_cuenta(img, t, ca, acento if acento != WHITE else AMBER)
            lineas_cuenta(img, t, ca, tiempos[1][0] - 0.1 if ca["trozos_intro"] > 1 else 0.6)
        img = barrido_luz(img, t)
        cabecera(img, t, cfg, mostrar_cuenta=not en_intro)
        if not ca:
            gancho(img, t, gancho_ws, acento, salida_gancho)
        if ca:
            sello(img, t, "DATO DEL DÍA", tiempos[ca["trozo_dato"]][0] - 0.05, AMBER)
        # subtítulos
        if t < t_pregunta:
            for g_i, g in enumerate(grupos):
                a = g[0][2] - 0.06
                b = grupos[g_i + 1][0][2] - 0.06 if g_i + 1 < len(grupos) else g[-1][3] + 0.3
                if g[-1][0] != (grupos[g_i + 1][0][0] if g_i + 1 < len(grupos) else None):
                    b = min(b, g[-1][3] + 0.35)
                if a <= t < b:
                    e = sale((t - a) / 0.12)
                    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                    lineas = partir_lineas([(w, x, y) for _, w, x, y in g], f_sub, 900)
                    poner_palabras(capa, lineas, 1180, f_sub, acento if acento != WHITE else AMBER, t)
                    if e < 1:
                        esc = 0.8 + 0.2 * e
                        capa = capa.transform((W, H), Image.AFFINE, (1 / esc, 0, W / 2 * (1 - 1 / esc), 0, 1 / esc,
                                                                     1180 * (1 - 1 / esc)), resample=Image.BILINEAR)
                    img.alpha_composite(capa)
                    break
        pregunta(img, t, trozos[ultimo], t_pregunta, 1 - suave((t - t_cierre) / 0.2))
        pie(img, cfg["pie"])
        img = cierre_marca(img, t, t_cierre)
        barra_progreso(img, t, dur, acento if acento != WHITE else AMBER)
        if flash > 0:
            img = Image.alpha_composite(img, Image.new("RGBA", (W, H), (255, 255, 255, int(255 * min(flash, 0.8)))))
        out = img.convert("RGB")
        if temblor:
            out = out.transform((W, H), Image.AFFINE, (1, 0, temblor, 0, 1, -temblor // 2), resample=Image.NEAREST)
        return out

    nframes = int(dur * FPS)

    def codificar(maxrate):
        proc = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
             "-r", str(FPS), "-i", "-", "-i", audio, "-c:v", "libx264", "-preset", "medium", "-crf", "23",
             "-maxrate", f"{maxrate}k", "-bufsize", f"{2 * maxrate}k", "-pix_fmt", "yuv420p", "-c:a", "aac",
             "-b:a", "128k", "-shortest", "-movflags", "+faststart", salida], stdin=subprocess.PIPE)
        for i in range(nframes):
            proc.stdin.write(fotograma(i).tobytes())
        proc.stdin.close()
        proc.wait()
        if proc.returncode:
            raise RuntimeError("FFmpeg no pudo montar el vídeo")
        return os.path.getsize(salida) / 1e6

    mb = codificar(1800)
    if mb > MAX_MB:  # Airtable admite como mucho 5 MB por archivo
        mb = codificar(int(1800 * MAX_MB / mb * 0.85))
    montar.fotograma = fotograma  # para sacar fotogramas sueltos en las pruebas
    return {"duracion": round(dur, 1), "mb": round(mb, 2)}


def _corte_cerca(ideal, tiempos):
    """El inicio de trozo más cercano a «ideal» si está a menos de 1,5 s."""
    cerca = min((a for a, _ in tiempos), key=lambda a: abs(a - ideal))
    return cerca - 0.05 if abs(cerca - ideal) < 1.5 else ideal
