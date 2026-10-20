"""Montaje del vídeo vertical (1080×1920, 30 fps) con el diseño aprobado en la fase G3 (20 oct 2026):
cabecera «LEÓNIDA / AL DÍA», cuenta atrás en rosa, etiqueta con el tema (color según el tipo),
gancho grande arriba, subtítulos abajo, pregunta final en amarillo, pie con la fuente y
«Imágenes: Rockstar Games». Fondo: capturas oficiales con un paneo suave centrado en su foco."""
import os, subprocess
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont
from scipy.signal import butter, lfilter

W, H, FPS = 1080, 1920, 30
FUENTES = "/usr/share/fonts/opentype/inter"
FB, FBO, FSB = (f"{FUENTES}/InterDisplay-Black.otf", f"{FUENTES}/InterDisplay-Bold.otf",
                f"{FUENTES}/InterDisplay-SemiBold.otf")
PINK, TEAL, AMBER, WHITE, NOCHE = (255, 64, 129), (46, 230, 214), (255, 196, 76), (255, 255, 255), (10, 14, 38)
COLOR_TIPO = {"Noticia": TEAL, "Dato": AMBER, "Prensa": WHITE}
COLOR_PERSONAJE = PINK
MAX_MB = 4.7


def fuente(p, s):
    return ImageFont.truetype(p, s)


# ---------------------------------------------------------------- música synthwave hecha con código
def musica(dur, seed=3):
    sr = 44100
    n = int(dur * sr)
    t = np.arange(n) / sr
    rng = np.random.default_rng(seed)
    beat = 60 / 100
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    progs = [[[45, 52, 57, 60], [41, 48, 53, 57], [43, 50, 55, 59], [40, 47, 52, 56]],   # Am F G E
             [[45, 52, 57, 60], [43, 50, 55, 59], [41, 48, 53, 57], [43, 50, 55, 59]],   # Am G F G
             [[41, 48, 53, 57], [43, 50, 55, 59], [45, 52, 57, 60], [45, 52, 57, 60]]]   # F G Am Am
    prog = progs[seed % len(progs)]
    L = np.zeros(n)
    for c in range(int(dur / (beat * 4)) + 1):
        ac, a0 = prog[c % 4], c * beat * 4
        for s in range(8):
            a = int((a0 + s * beat / 2) * sr)
            m = min(int(beat / 2 * 0.9 * sr), n - a)
            if m <= 0:
                continue
            tt = np.arange(m) / sr
            f = hz(ac[0] - 12)
            L[a:a + m] += (2 * ((f * tt) % 1) - 1) * np.exp(-tt * 6) * 0.10
        a = int(a0 * sr)
        m = min(int(beat * 4 * sr), n - a)
        if m > 0:
            tt = np.arange(m) / sr
            env = np.minimum(tt / 0.4, 1) * np.minimum((beat * 4 - tt) / 0.4, 1)
            for nota in ac[1:]:
                for det in (-0.08, 0.08):
                    f = hz(nota + 12 + det)
                    L[a:a + m] += (2 * ((f * tt) % 1) - 1) * env * 0.025
        for s in range(4):
            a = int((a0 + s * beat) * sr)
            m = min(int(0.25 * sr), n - a)
            if m <= 0:
                continue
            tt = np.arange(m) / sr
            L[a:a + m] += np.sin(2 * np.pi * (50 + 80 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 12) * 0.25
            if s % 2 == 1:
                L[a:a + m] += rng.standard_normal(m) * np.exp(-tt * 18) * 0.06
    b, a = butter(2, 5000 / (sr / 2))
    L = lfilter(b, a, L)
    L *= np.minimum(np.minimum(t / 0.5, 1), np.minimum((dur - t) / 1.0, 1))
    L = L / (np.max(np.abs(L)) + 1e-6) * 0.8
    return np.stack([L, L], 1).astype(np.float32), sr


# ---------------------------------------------------------------- dibujo
def envolver(txt, f, ancho, d):
    lineas, cur = [], ""
    for p in txt.split():
        prueba = (cur + " " + p).strip()
        if d.textlength(prueba, font=f) <= ancho:
            cur = prueba
        else:
            if cur:
                lineas.append(cur)
            cur = p
    if cur:
        lineas.append(cur)
    return lineas


def texto_centrado(img, txt, y, f, color, ancho=920, borde=6, caja=None):
    d = ImageDraw.Draw(img)
    lineas = envolver(txt, f, ancho, d)
    alto = int(f.size * 1.12)
    if caja and lineas:
        wmax = max(d.textlength(l, font=f) for l in lineas)
        d.rounded_rectangle([W / 2 - wmax / 2 - 34, y - 26, W / 2 + wmax / 2 + 34, y + alto * len(lineas) + 18],
                            28, fill=caja)
    for i, l in enumerate(lineas):
        d.text((W / 2, y + i * alto), l, font=f, fill=color, anchor="ma", stroke_width=borde, stroke_fill=(0, 0, 0))


def ajustar(txt, f0, tam, ancho, d, minimo=34):
    """Reduce la letra hasta que el texto quepa en el ancho dado."""
    while tam > minimo and d.textlength(txt, font=fuente(f0, tam)) > ancho:
        tam -= 2
    return fuente(f0, tam)


def pastilla(d, x, y, txt, f, fondo, color=(0, 0, 0), derecha=False):
    w = d.textlength(txt, font=f)
    h = f.size + 22
    x0 = x - w - 44 if derecha else x
    d.rounded_rectangle([x0, y, x0 + w + 44, y + h], h // 2, fill=fondo)
    d.text((x0 + 22, y + 10), txt, font=f, fill=color)


def sol(d, cx, cy, r):
    for i in range(r * 2):
        yy = cy - r + i
        f = i / (2 * r)
        c = tuple(int(AMBER[k] + (PINK[k] - AMBER[k]) * f) for k in range(3))
        dx = int((r * r - (yy - cy) ** 2) ** 0.5) if abs(yy - cy) < r else 0
        if i > r * 1.05 and (i // 4) % 2 == 1:
            continue
        d.line([(cx - dx, yy), (cx + dx, yy)], fill=c)


def capa_fija(cfg):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = np.zeros((H, W, 4), np.uint8)
    top = np.clip(1 - np.arange(H) / 420, 0, 1)
    bot = np.clip((np.arange(H) - 1150) / 600, 0, 1)
    g[..., 3] = (np.maximum(top * 200, bot * 235)).astype(np.uint8)[:, None]
    img = Image.alpha_composite(img, Image.fromarray(g, "RGBA"))
    d = ImageDraw.Draw(img)
    sol(d, 92, 112, 34)
    d.text((142, 78), "LEÓNIDA", font=fuente(FB, 40), fill=WHITE)
    d.text((142, 120), "AL DÍA", font=fuente(FB, 28), fill=TEAL)
    pastilla(d, W - 48, 86, cfg["cuenta"], fuente(FB, 30), PINK, WHITE, derecha=True)
    color = COLOR_PERSONAJE if cfg.get("personaje") else COLOR_TIPO.get(cfg.get("tipo"), WHITE)
    etiqueta = (cfg.get("etiqueta") or "GTA 6").upper()[:24]
    pastilla(d, 48, 190, etiqueta, ajustar(etiqueta, FB, 30, W - 200, d, 22), color, NOCHE)
    pie = cfg["pie"]
    d.text((W / 2, 1838), pie, font=ajustar(pie, FSB, 26, W - 80, d, 18), fill=(215, 215, 225), anchor="ma")
    return img


# ---------------------------------------------------------------- fondo
def cargar_foto(path):
    im = Image.open(path).convert("RGB")
    s = H / im.height * 1.06
    return im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)


def pan_de_foco(im, foco, plano):
    """Del foco (centro del sujeto, 0-1) a la posición del recorte (0-1), con un paneo suave."""
    maxx = im.width - W
    c = (foco * im.width - W / 2) / maxx if maxx > 0 else 0.5
    rango = 0.30 if plano == "panorámica" else 0.10
    a, b = c - rango / 2, c + rango / 2
    if a < 0:
        a, b = 0, min(1, rango)
    if b > 1:
        a, b = max(0, 1 - rango), 1
    return a, b


def recorte(im, p):
    maxx = im.width - W
    x = int(np.clip(p * maxx, 0, maxx))
    y = int((im.height - H) / 2)
    return im.crop((x, y, x + W, y + H))


# ---------------------------------------------------------------- montaje
def montar(cfg):
    """cfg: trozos, tiempos [(ini, fin)], voz (wav), capturas [(ruta, foco, plano)], etiqueta, tipo,
    personaje, cuenta, pie, salida, semilla, tmp. Devuelve {duracion, mb}."""
    tmp = cfg["tmp"]
    trozos, tiempos = cfg["trozos"], cfg["tiempos"]
    voz, sr = sf.read(cfg["voz"], dtype="float32")
    if voz.ndim > 1:
        voz = voz.mean(1)
    voz = voz / (np.max(np.abs(voz)) + 1e-6) * 0.9
    dur = len(voz) / sr + 1.2
    m, msr = musica(dur, cfg.get("semilla", 3))
    v = np.interp(np.linspace(0, len(voz) - 1, int(len(voz) * msr / sr)), np.arange(len(voz)), voz)
    mezcla = m * 0.16
    mezcla[:len(v)] += v[:, None] * 0.95
    mezcla = mezcla / max(1.0, np.max(np.abs(mezcla)) / 0.95)
    sf.write(os.path.join(tmp, "mezcla.wav"), mezcla.astype(np.float32), msr)

    fija = capa_fija(cfg)
    fotos = [(cargar_foto(r), f, p) for r, f, p in cfg["capturas"]]
    # Cada captura dura lo mismo; el cambio coincide con el principio de un subtítulo si cae cerca
    n_f = len(fotos)
    cortes = [0.0]
    for k in range(1, n_f):
        ideal = dur * k / n_f
        cerca = min((t0 for t0, _ in tiempos), key=lambda t0: abs(t0 - ideal))
        cortes.append(cerca if abs(cerca - ideal) < 2 else ideal)
    cortes.append(dur)
    pans = [pan_de_foco(im, f, p) for im, f, p in fotos]

    fg, fs, fc = fuente(FB, 74), fuente(FB, 64), fuente(FB, 66)
    nframes = int(dur * FPS)
    salida = cfg["salida"]

    def codificar(maxrate):
        proc = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
             "-r", str(FPS), "-i", "-", "-i", os.path.join(tmp, "mezcla.wav"), "-c:v", "libx264",
             "-preset", "medium", "-crf", "24", "-maxrate", f"{maxrate}k", "-bufsize", f"{2 * maxrate}k",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", salida],
            stdin=subprocess.PIPE)
        for i in range(nframes):
            t = i / FPS
            k = max(j for j in range(n_f) if cortes[j] <= t)
            a, b = pans[k]
            p = a + (b - a) * (t - cortes[k]) / max(cortes[k + 1] - cortes[k], 1e-3)
            img = Image.alpha_composite(recorte(fotos[k][0], p).convert("RGBA"), fija)
            j = next((q for q, (x0, x1) in enumerate(tiempos) if x0 - 0.05 <= t < x1 + 0.25), None)
            if j == 0 or t < tiempos[0][0]:
                texto_centrado(img, trozos[0], 430, fg, WHITE, caja=(10, 14, 38, 200), borde=0)
            elif (j is not None and j == len(trozos) - 1) or t >= tiempos[-1][0]:
                texto_centrado(img, trozos[-1], 560, fc, AMBER, caja=(10, 14, 38, 210), borde=0)
            elif j is not None:
                texto_centrado(img, trozos[j], 1300, fs, WHITE, borde=7)
            proc.stdin.write(img.convert("RGB").tobytes())
        proc.stdin.close()
        proc.wait()
        if proc.returncode:
            raise RuntimeError("FFmpeg no pudo montar el vídeo")
        return os.path.getsize(salida) / 1e6

    mb = codificar(1300)
    if mb > MAX_MB:  # Airtable admite como mucho 5 MB por archivo
        mb = codificar(int(1300 * MAX_MB / mb * 0.85))
    return {"duracion": round(dur, 1), "mb": round(mb, 2)}
