"""Montaje del vídeo vertical (1080×1920, 30 fps) con el diseño aprobado en la fase G3 (20 oct 2026):
cabecera «LEÓNIDA / AL DÍA», cuenta atrás en rosa, etiqueta con el tema (color según el tipo),
gancho grande arriba, subtítulos abajo, pregunta final en amarillo, pie con la fuente y
«Imágenes: Rockstar Games». Fondo: capturas oficiales con un paneo suave centrado en su foco."""
import os, subprocess
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageFont
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
def palabras(txt):
    """Palabras para partir líneas sin separar «GTA 6» ni dejar «y», «a» u «o» al final de una línea."""
    out = []
    for p in txt.split():
        if out and (out[-1].endswith("GTA") or (len(out[-1]) == 1 and out[-1].isalpha())):
            out[-1] += " " + p
        else:
            out.append(p)
    return out


def envolver(txt, f, ancho, d):
    lineas, cur = [], ""
    for p in palabras(txt):
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


def sin_bordes(im):
    """Quita los márgenes lisos (blancos, negros o de un color) que traen algunas imágenes de las noticias, para que
    la foto llene la pantalla de verdad y no quede pequeña en el centro (23 oct)."""
    from PIL import ImageChops
    for _ in range(2):
        fondo = Image.new("RGB", im.size, im.getpixel((2, 2)))
        caja = ImageChops.difference(im, fondo).convert("L").point(lambda v: 255 if v > 24 else 0).getbbox()
        if not caja or caja == (0, 0, im.width, im.height):
            break
        if (caja[2] - caja[0]) < im.width * 0.3 or (caja[3] - caja[1]) < im.height * 0.3:
            break  # casi todo es fondo (un logotipo): mejor no tocar
        im = im.crop(caja)
    return im


def componer_imagen(path):
    """Imagen que no es una captura del juego (un producto, una persona, una portada…). Desde el 22 oct ocupa
    toda la pantalla (lo pedí yo): se amplía hasta cubrirla y el vídeo la recorre de lado a lado, para que se vea
    entera sin quedar pequeña en el centro."""
    im = sin_bordes(Image.open(path).convert("RGB"))
    s = max(H * 1.06 / im.height, W * 1.06 / im.width)
    return im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)


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


# ---------------------------------------------------------------- trozos de vídeo oficiales
def es_video(ruta):
    return ruta.lower().endswith(".mp4")


def duracion_video(ruta):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                          "csv=p=0", ruta]).decode().strip())


def sonido_video(ruta, msr):
    out = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", ruta, "-vn", "-f", "f32le", "-ac", "2", "-ar", str(msr), "-"],
                         capture_output=True).stdout
    return np.frombuffer(out, np.float32).reshape(-1, 2).copy()


class Lector:
    """Lee los fotogramas de un trozo (ya en 1080 × 1920); si se acaba, repite el último."""
    def __init__(self, ruta):
        self.p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", ruta, "-f", "rawvideo", "-pix_fmt", "rgb24",
                                   "-s", f"{W}x{H}", "-r", str(FPS), "-"], stdout=subprocess.PIPE)
        self.ultimo = bytes(W * H * 3)

    def fotograma(self):
        raw = self.p.stdout.read(W * H * 3)
        if len(raw) == W * H * 3:
            self.ultimo = raw
        return Image.frombytes("RGB", (W, H), self.ultimo)

    def cerrar(self):
        self.p.kill()
        self.p.wait()


def plan_fondos(fondos, dur, tiempos):
    """Tramos [(fondo, inicio, fin)]. Solo capturas: todas duran lo mismo y el cambio cae en el principio de un
    subtítulo si está cerca. Con trozos: cada trozo dura lo que dura (como mucho 1,5 veces lo que le toca) y las
    capturas se reparten el resto (al menos 2,5 s cada una); si solo hay trozos, se repiten hasta llenar."""
    n = len(fondos)
    if not any(f["video"] for f in fondos):
        cortes = [0.0]
        for k in range(1, n):
            ideal = dur * k / n
            cerca = min((t0 for t0, _ in tiempos), key=lambda t0: abs(t0 - ideal))
            cortes.append(cerca if abs(cerca - ideal) < 2 else ideal)
        cortes.append(dur)
        return [(k, cortes[k], cortes[k + 1]) for k in range(n)]
    fotos = [k for k in range(n) if not fondos[k]["video"]]
    if not fotos:
        tramos, t, k = [], 0.0, 0
        while t < dur - 0.05:
            largo = min(fondos[k % n]["dur"], dur - t)
            tramos.append((k % n, t, t + largo))
            t += largo
            k += 1
        return tramos
    largos = [min(f["dur"], dur / n * 1.5) if f["video"] else 0.0 for f in fondos]
    resto = dur - sum(largos)
    if resto / len(fotos) < 2.5:
        sobra = sum(largos) - (dur - 2.5 * len(fotos))
        factor = max(0.2, (sum(largos) - sobra) / max(sum(largos), 1e-3))
        largos = [x * factor for x in largos]
        resto = dur - sum(largos)
    largos = [x if fondos[k]["video"] else resto / len(fotos) for k, x in enumerate(largos)]
    tramos, t = [], 0.0
    for k, x in enumerate(largos):
        tramos.append((k, t, dur if k == n - 1 else t + x))
        t += x
    return tramos


# ---------------------------------------------------------------- cuenta atrás
_FUENTES = {}


def f_(p, s):
    if (p, s) not in _FUENTES:
        _FUENTES[(p, s)] = fuente(p, s)
    return _FUENTES[(p, s)]


def reloj(img, cfg, t):
    """Cuenta atrás (vídeo de las 17:00, decidido el 22 oct): los días en grande y las horas, minutos y segundos
    bajando en directo, con la fecha de salida, la precarga y el aviso de que la hora no está confirmada."""
    r = cfg["reloj"]
    resto = max(0.0, r["segundos"] - t)
    d, x = divmod(int(resto), 86400)
    h, x = divmod(x, 3600)
    m, s = divmod(x, 60)
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(capa)
    dr.rounded_rectangle([80, 740, W - 80, 1215], 40, fill=(10, 14, 38, 200))
    dias = "¡ESTA NOCHE!" if d == 0 else ("1 DÍA" if d == 1 else f"{d} DÍAS")
    dr.text((W / 2, 765), dias, font=f_(FB, 150 if d else 112), fill=AMBER, anchor="ma")
    f = f_(FB, 104)
    celda = max(dr.textlength(c, font=f) for c in "0123456789")
    texto = f"{h:02d}:{m:02d}:{s:02d}"
    anchos = [celda if c.isdigit() else dr.textlength(c, font=f) for c in texto]
    x0 = W / 2 - sum(anchos) / 2
    for c, a in zip(texto, anchos):
        dr.text((x0 + a / 2, 940), c, font=f, fill=WHITE, anchor="ma")
        x0 += a
    dr.text((W / 2, 1062), r["linea"], font=f_(FSB, 36), fill=(225, 225, 235), anchor="ma")
    if r.get("precarga"):
        dr.text((W / 2, 1110), r["precarga"], font=f_(FB, 38), fill=TEAL, anchor="ma")
    aviso = "Hora de salida sin confirmar por Rockstar: contamos hasta las 00:00 (España)"
    dr.text((W / 2, 1168), aviso, font=ajustar(aviso, FSB, 24, W - 220, dr, 16), fill=(175, 175, 190), anchor="ma")
    return Image.alpha_composite(img, capa)


# ---------------------------------------------------------------- montaje
def montar(cfg):
    """cfg: trozos, tiempos [(ini, fin)], voz (wav), capturas [(ruta, foco, plano)] (una ruta .mp4 es un trozo de
    vídeo oficial), etiqueta, tipo, personaje, cuenta, pie, salida, semilla, tmp. Devuelve {duracion, mb}."""
    tmp = cfg["tmp"]
    trozos, tiempos = cfg["trozos"], cfg["tiempos"]
    voz, sr = sf.read(cfg["voz"], dtype="float32")
    if voz.ndim > 1:
        voz = voz.mean(1)
    voz = voz / (np.max(np.abs(voz)) + 1e-6) * 0.9
    dur = len(voz) / sr + 1.2
    m, msr = musica(dur, cfg.get("semilla", 3))
    v = np.interp(np.linspace(0, len(voz) - 1, int(len(voz) * msr / sr)), np.arange(len(voz)), voz)

    fondos = []
    for r, f, p in cfg["capturas"]:
        if es_video(r):
            fondos.append({"video": True, "ruta": r, "dur": duracion_video(r), "sonido": p == "vídeo con sonido"})
        elif p == "imagen":  # imagen de lo que cuenta la noticia: entera, sin recortar
            fondos.append({"video": False, "im": componer_imagen(r), "pan": (0.0, 1.0)})
        else:
            im = cargar_foto(r)
            fondos.append({"video": False, "im": im, "pan": pan_de_foco(im, f, p)})
    tramos = plan_fondos(fondos, dur, tiempos)

    # Sonido de fondo: nuestra música; solo los trozos marcados «con sonido» llevan el suyo (bajo) en su tramo
    n = len(m)
    peso = np.ones(n, np.float32)
    oficial = np.zeros((n, 2), np.float32)
    for k, a, b in tramos:
        if fondos[k]["video"] and fondos[k]["sonido"]:
            i0, i1 = int(a * msr), min(int(b * msr), n)
            peso[i0:i1] = 0
            s = sonido_video(fondos[k]["ruta"], msr)[:i1 - i0]
            if len(s):
                s = s / (np.max(np.abs(s)) + 1e-6) * 0.30
                fade = min(int(0.02 * msr), len(s) // 2)
                if fade:
                    rampa = np.linspace(0, 1, fade, dtype=np.float32)[:, None]
                    s[:fade] *= rampa
                    s[-fade:] *= rampa[::-1]
                oficial[i0:i0 + len(s)] = s
    if peso.min() < 1:
        ventana = int(0.25 * msr)
        peso = np.convolve(peso, np.ones(ventana, np.float32) / ventana, mode="same").astype(np.float32)
    mezcla = m * 0.16 * peso[:, None] + oficial * (1 - peso[:, None])
    mezcla[:len(v)] += v[:, None] * 0.95
    mezcla = mezcla / max(1.0, np.max(np.abs(mezcla)) / 0.95)
    sf.write(os.path.join(tmp, "mezcla.wav"), mezcla.astype(np.float32), msr)

    fija = capa_fija(cfg)
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
        actual, lector = None, None
        for i in range(nframes):
            t = i / FPS
            q = max(j for j in range(len(tramos)) if tramos[j][1] <= t + 1e-6)
            k, a, b = tramos[q]
            if q != actual:
                if lector:
                    lector.cerrar()
                lector = Lector(fondos[k]["ruta"]) if fondos[k]["video"] else None
                actual = q
            if lector:
                base = lector.fotograma()
            else:
                pa, pb = fondos[k]["pan"]
                base = recorte(fondos[k]["im"], pa + (pb - pa) * (t - a) / max(b - a, 1e-3))
            img = Image.alpha_composite(base.convert("RGBA"), fija)
            if cfg.get("reloj"):
                img = reloj(img, cfg, t)
            j = next((q2 for q2, (x0, x1) in enumerate(tiempos) if x0 - 0.05 <= t < x1 + 0.25), None)
            if j == 0 or t < tiempos[0][0]:
                texto_centrado(img, trozos[0], 430, fg, WHITE, caja=(10, 14, 38, 200), borde=0)
            elif (j is not None and j == len(trozos) - 1) or t >= tiempos[-1][0]:
                texto_centrado(img, trozos[-1], 560, fc, AMBER, caja=(10, 14, 38, 210), borde=0)
            elif j is not None:
                texto_centrado(img, trozos[j], 1300, fs, WHITE, borde=7)
            proc.stdin.write(img.convert("RGB").tobytes())
        if lector:
            lector.cerrar()
        proc.stdin.close()
        proc.wait()
        if proc.returncode:
            raise RuntimeError("FFmpeg no pudo montar el vídeo")
        return os.path.getsize(salida) / 1e6

    mb = codificar(1300)
    if mb > MAX_MB:  # Airtable admite como mucho 5 MB por archivo
        mb = codificar(int(1300 * MAX_MB / mb * 0.85))
    return {"duracion": round(dur, 1), "mb": round(mb, 2)}
