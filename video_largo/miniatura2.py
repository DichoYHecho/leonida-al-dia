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
    # Vice City (vídeo 2)
    "VC_Tril": "https://videos-rockstargames-com.akamaized.net/v4/8ta2r546/flv/en-us-1080p60.mp4",
    "VC_Aniv": "https://videos-rockstargames-com.akamaized.net/v4/tror41c2/flv/en-us-720p.mp4",
    "VC_Comp": "https://videos-rockstargames-com.akamaized.net/v4/ao1c441c/flv/en-us-1080p60.mp4",
    "VC02_Trailer3": "https://archive.org/download/vicecity480x360_ph3/vicecity480x360_ph3.mp4",
    # Imagen oficial del bonus por reservar (Jason con el arma con el estampado de la camisa de Tommy)
    "Reserva_Jason": "https://www.rockstargames.com/VI/_next/static/media/VINTAGE_VICE_CITY_PACK_EXCLUSIVE_LOOKS_03.0au1tphsftqm5.jpg?akim=1&imdensity=1&imwidth=3840",
}
for _par in os.environ.get("AJUSTES", "").split(";"):  # p. ej. ANCHO_DER=0.7;MEZCLA=0.85;POS_LOGOS=0.18|0.74
    if "=" in _par:
        os.environ[_par.split("=", 1)[0].strip()] = _par.split("=", 1)[1].strip()
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
    if "/media/" in VIDEOS.get(video, "") or VIDEOS.get(video, "").split("?")[0].endswith((".jpg", ".png")):
        im = Image.open(fuente(video)).convert("RGB")  # imagen fija
        if escala:
            im = im.resize(tuple(int(v) for v in escala.split(":")), Image.LANCZOS)
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
    partes = param.split(":")
    v, t, x, y, zoom = partes[:5]
    gamma = float(partes[5]) if len(partes) > 5 else 1.0  # menos de 1 aclara las sombras
    tmp = SALIDA / f"panel_{v}_{t}.png"
    sacar(v, float(t), tmp)
    im = Image.open(tmp).convert("RGB")
    tmp.unlink()
    if gamma != 1.0:
        im = im.point([int(255 * (p / 255) ** gamma) for p in range(256)] * 3)
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


def degradado_h(ancho, alto, sentido, desde=0.55, curva=1.6):
    """Máscara horizontal: opaca hasta «desde» y se desvanece hacia el borde (sentido 1: a la derecha)."""
    m = Image.new("L", (ancho, alto), 0)
    px = m.load()
    for xx in range(ancho):
        u = xx / (ancho - 1) if sentido == 1 else 1 - xx / (ancho - 1)
        a = 255 if u <= desde else int(255 * (1 - (u - desde) / (1 - desde)) ** curva)
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
    ancho_p = int(w * 0.62)
    izq = panel(os.environ["IZQ"], ancho_p, h)
    ancho_d = int(w * float(os.environ.get("ANCHO_DER") or 0.62))
    der = panel(os.environ["DER"], ancho_d, h)
    base.paste(izq, (0, 0))  # Lucía entera, sin fundido: no queda franja oscura
    base.paste(der, (w - ancho_d, 0), degradado_h(ancho_d, h, 0, float(os.environ.get("MEZCLA") or 0.62), 1.0))  # Jason se funde sobre Lucía
    im = base.convert("RGBA")
    # sin sombra en el centro: las dos fotos se funden directamente (el texto lleva su propia sombra suave)
    f20 = ImageFont.truetype(CARPETA + "Montserrat-Black.ttf", 500 * SS)
    f1 = ImageFont.truetype(CARPETA + "Montserrat-ExtraBold.ttf", 64 * SS)
    f2 = ImageFont.truetype(CARPETA + "Montserrat-ExtraBold.ttf", 62 * SS)
    cx = w / 2
    logos = os.environ.get("LOGOS", "").strip()
    if logos:  # antes y después: un logo en cada mitad, abajo
        for k, url in enumerate(logos.split("|")[:2]):
            ruta = SALIDA / f"logo_{k}.png"
            subprocess.run(["curl", "-sSfL", "-A", UA, "-o", str(ruta), url.strip()], check=True)
            lg = Image.open(ruta).convert("RGBA")
            ruta.unlink()
            alto_l = int(h * float(os.environ.get("ALTO_LOGO") or 0.36))
            lg = lg.resize((max(1, int(lg.width * alto_l / lg.height)), alto_l), Image.LANCZOS)
            if lg.width > w * 0.40:
                lg = lg.resize((int(w * 0.40), max(1, int(lg.height * w * 0.40 / lg.width))), Image.LANCZOS)
            pos = [float(p) for p in (os.environ.get("POS_LOGOS") or "0.25|0.75").split("|")]
            x = int(w * pos[k] - lg.width / 2)
            y = int(h * 0.95 - lg.height)
            sombra = Image.new("RGBA", im.size, (0, 0, 0, 0))
            sombra.paste((0, 0, 0, 200), (x, y + 6 * SS, x + lg.width, y + 6 * SS + lg.height), lg.split()[3])
            im.alpha_composite(sombra.filter(ImageFilter.GaussianBlur(12 * SS)))
            im.alpha_composite(lg, (x, y))
        f_a = ImageFont.truetype(CARPETA + "Montserrat-Black.ttf", 96 * SS)
        if os.environ.get("L1"):
            texto(im, w * float((os.environ.get("POS_LOGOS") or "0.25|0.75").split("|")[0]), 30 * SS, os.environ["L1"], f_a, BLANCO, tracking=4 * SS)
        if os.environ.get("L2"):
            texto(im, w * float((os.environ.get("POS_LOGOS") or "0.25|0.75").split("|")[1]), 30 * SS, os.environ["L2"], f_a, ROSA, tracking=4 * SS)
    else:
        grande = os.environ.get("GRANDE") or "20"
        tam = int(os.environ.get("TAM") or 500)
        if tam != 500:
            f20 = ImageFont.truetype(CARPETA + "Montserrat-Black.ttf", tam * SS)
        y_grande = float(os.environ.get("Y_GRANDE") or -56)
        texto(im, cx, y_grande * SS, grande, f20, ROSA, tracking=-8 * SS)
        texto(im, cx, 452 * SS, os.environ.get("L1") or "CURIOSIDADES", f1, BLANCO, tracking=7 * SS)
        texto(im, cx, 546 * SS, os.environ.get("L2") or "DE GTA 6", f2, ROSA, tracking=9 * SS)
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
