"""Miniatura minimalista del vídeo largo de «Leónida al Día» (1280 × 720, menos de 2 MB). No publica nada.

Dos modos:
- Candidatos: FRAMES = «vídeo:segundo» separados por comas -> hoja numerada para elegir primeros planos.
- Miniatura: IZQ y DER = «vídeo:segundo:x:y:zoom» (x e y = dónde está la cara, de 0 a 1; zoom = acercamiento).
  Lucía a la izquierda, Jason a la derecha, un «20» grande en el centro y el texto debajo, sin bordes.
Vídeos: Lanzamiento, Trailer_1, Trailer_2, Mirada (1080p) y Mirada4K (4K, para la miniatura)."""
import os
import pathlib
import subprocess
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

SALIDA = pathlib.Path("salida_miniatura2")
SALIDA.mkdir(exist_ok=True)
FUENTES = pathlib.Path(os.environ.get("DIR_FUENTES", "fuentes_min2"))
FUENTES.mkdir(exist_ok=True)
UA = "LeonidaAlDiaBot/1.0 (cuenta de fans de GTA 6) GitHubActions"
_V = "https://media-rockstargames-com.akamaized.net/VI/downloads/videos/"
_M = "https://videos-rockstargames-com.akamaized.net/v4/rk721912/flv/"
VIDEOS = {
    "Mirada": _M + "es-es-1080p.mp4",
    "Mirada4K": _M + "es-es-2160p.mp4",
    "Trailer_1": _V + "GTAVI_Trailer_1/GTAVI_Trailer_1.mp4",
    "Trailer_2": _V + "GTAVI_Trailer_2/GTAVI_Trailer_2.mp4",
    "Lanzamiento": _V + "GTAVI_Launch_Trailer/GTAVI_Launch_Trailer.mp4",
}
CARPETA = "/usr/share/fonts/truetype/montserrat/"
ROSA = (255, 79, 163)
BLANCO = (255, 255, 255)
FONDO = (9, 7, 18)
W, H, SS = 1280, 720, 2  # SS: se compone al doble y se reduce, para que todo salga limpio
PRUEBA = os.environ.get("PRUEBA") == "1"


def fuente(video):
    destino = FUENTES / (video + ".mp4")
    if not destino.exists() or destino.stat().st_size == 0:
        for i in range(8):
            r = subprocess.run(["curl", "-sSfL", "-A", UA, "-C", "-", "-o", str(destino), VIDEOS[video]],
                               capture_output=True)
            if r.returncode == 0:
                break
            print("  descarga cortada, se reanuda", i + 1, flush=True)
    return destino


def sacar(video, t, destino, escala=None):
    """Un fotograma sin recortar (escala=None: tamaño original; si no, ancho:alto)."""
    if PRUEBA:
        im = Image.new("RGB", (1920, 1080), (50 + int(t) % 120, 80, 130))
        d = ImageDraw.Draw(im)
        d.ellipse((760, 200, 1160, 700), fill=(215, 160, 130))
        im.save(destino, quality=95)
        return
    vf = ["-vf", f"scale={escala}"] if escala else []
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", str(fuente(video)), "-frames:v", "1",
                        *vf, "-q:v", "1", str(destino)], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-300:])


def candidatos():
    pares = [x.strip() for x in os.environ.get("FRAMES", "").split(",") if x.strip()]
    cols, ancho, alto = 4, 400, 225
    filas = (len(pares) + cols - 1) // cols
    hoja = Image.new("RGB", (cols * ancho, filas * alto), (0, 0, 0))
    f = ImageFont.truetype(CARPETA + "Montserrat-ExtraBold.ttf", 15)
    for i, p in enumerate(pares):
        v, t = p.split(":")
        tmp = SALIDA / f"c_{i}.jpg"
        sacar(v, float(t), tmp, "800:450")
        im = Image.open(tmp).convert("RGB").resize((ancho, alto))
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 190, 22), fill=(0, 0, 0))
        d.text((5, 3), f"{i + 1}  {v}:{t}", font=f, fill=(255, 255, 0))
        hoja.paste(im, ((i % cols) * ancho, (i // cols) * alto))
        tmp.unlink()
    hoja.save(SALIDA / "candidatos.jpg", quality=90)
    print("candidatos:", len(pares), flush=True)


def panel(param, ancho, alto):
    """Primer plano de una cara: recorta alrededor de (x, y) con el zoom indicado y lo lleva a ancho × alto."""
    v, t, x, y, zoom = param.split(":")
    tmp = SALIDA / f"panel_{v}_{t}.png"
    sacar(v, float(t), tmp)
    im = Image.open(tmp).convert("RGB")
    tmp.unlink()
    x, y, zoom = float(x), float(y), float(zoom)
    rel = ancho / alto
    ch = im.height / zoom
    cw = ch * rel
    if cw > im.width:
        cw = im.width
        ch = cw / rel
    x0 = min(max(x * im.width - cw / 2, 0), im.width - cw)
    y0 = min(max(y * im.height - ch / 2, 0), im.height - ch)
    return im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((ancho, alto), Image.LANCZOS)


def degradado_h(ancho, alto, sentido, desde=0.55):
    """Máscara horizontal: opaca hasta «desde» y se desvanece hacia el borde (sentido 1: a la derecha)."""
    m = Image.new("L", (ancho, alto), 0)
    px = m.load()
    for xx in range(ancho):
        u = xx / (ancho - 1) if sentido == 1 else 1 - xx / (ancho - 1)
        a = 255 if u <= desde else int(255 * (1 - (u - desde) / (1 - desde)) ** 1.6)
        for yy in range(alto):
            px[xx, yy] = a
    return m


def texto_ancho(font, s, tracking):
    return sum(font.getlength(c) for c in s) + tracking * (len(s) - 1)


def texto(capa, cx, y, s, font, color, tracking=0, sombra=True):
    """Texto centrado en cx, sin bordes; solo una sombra muy suave para que se lea sobre las caras."""
    ancho = texto_ancho(font, s, tracking)
    x = cx - ancho / 2
    if sombra:
        sc = Image.new("RGBA", capa.size, (0, 0, 0, 0))
        dx = x
        for c in s:
            ImageDraw.Draw(sc).text((dx, y + 6 * SS), c, font=font, fill=(0, 0, 0, 120))
            dx += font.getlength(c) + tracking
        capa.alpha_composite(sc.filter(ImageFilter.GaussianBlur(14 * SS)))
    d = ImageDraw.Draw(capa)
    for c in s:
        d.text((x, y), c, font=font, fill=color)
        x += font.getlength(c) + tracking


def miniatura():
    w, h = W * SS, H * SS
    base = Image.new("RGB", (w, h), FONDO)
    ancho_p = int(w * 0.58)
    izq = panel(os.environ["IZQ"], ancho_p, h)
    der = panel(os.environ["DER"], ancho_p, h)
    base.paste(izq, (0, 0), degradado_h(ancho_p, h, 1, 0.50))
    base.paste(der, (w - ancho_p, 0), degradado_h(ancho_p, h, 0, 0.50))
    im = base.convert("RGBA")
    # columna central un poco más oscura para que el «20» y el texto se lean limpios
    sombra = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).ellipse((w * 0.5 - 520 * SS, h * 0.5 - 420 * SS, w * 0.5 + 520 * SS, h * 0.5 + 420 * SS),
                                   fill=(6, 5, 14, 175))
    im.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(90 * SS)))
    f20 = ImageFont.truetype(CARPETA + "Montserrat-Black.ttf", 500 * SS)
    f1 = ImageFont.truetype(CARPETA + "Montserrat-ExtraBold.ttf", 64 * SS)
    f2 = ImageFont.truetype(CARPETA + "Montserrat-Bold.ttf", 38 * SS)
    cx = w / 2
    texto(im, cx, -56 * SS, "20", f20, ROSA, tracking=-8 * SS)
    texto(im, cx, 470 * SS, "CURIOSIDADES", f1, BLANCO, tracking=7 * SS)
    texto(im, cx, 572 * SS, "DE GTA 6", f2, ROSA, tracking=11 * SS, sombra=False)
    rgb = im.convert("RGB").resize((W, H), Image.LANCZOS)
    rgb = ImageEnhance.Contrast(rgb).enhance(1.06)
    destino = SALIDA / "miniatura_nueva.jpg"
    calidad = 96
    while True:
        rgb.save(destino, quality=calidad, subsampling=0, optimize=True)
        if destino.stat().st_size < 1_900_000 or calidad <= 80:
            break
        calidad -= 3
    print("miniatura_nueva.jpg", f"{destino.stat().st_size / 1e3:.0f} KB", flush=True)


if __name__ == "__main__":
    if os.environ.get("IZQ") and os.environ.get("DER"):
        miniatura()
    else:
        candidatos()
