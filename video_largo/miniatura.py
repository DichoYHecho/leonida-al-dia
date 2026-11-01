"""Miniaturas del vídeo largo de «Leónida al Día» (1280 × 720, menos de 2 MB cada una). No publica nada.

FRAMES = «vídeo:segundo» separados por comas (vídeos: Lanzamiento, Trailer_1, Trailer_2, Mirada).
Saca esos fotogramas (candidatos), y compone tres miniaturas con los tres primeros. Salida en «salida_miniatura/»."""
import os
import pathlib
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SALIDA = pathlib.Path("salida_miniatura")
SALIDA.mkdir(exist_ok=True)
FUENTES = pathlib.Path(os.environ.get("DIR_FUENTES", "fuentes_min"))
FUENTES.mkdir(exist_ok=True)
UA = "LeonidaAlDiaBot/1.0 (cuenta de fans de GTA 6) GitHubActions"
_V = "https://media-rockstargames-com.akamaized.net/VI/downloads/videos/"
VIDEOS = {
    "Mirada": "https://videos-rockstargames-com.akamaized.net/v4/rk721912/flv/es-es-1080p.mp4",
    "Trailer_1": _V + "GTAVI_Trailer_1/GTAVI_Trailer_1.mp4",
    "Trailer_2": _V + "GTAVI_Trailer_2/GTAVI_Trailer_2.mp4",
    "Lanzamiento": _V + "GTAVI_Launch_Trailer/GTAVI_Launch_Trailer.mp4",
}
CARPETA = "/usr/share/fonts/truetype/montserrat/"
ROSA = (255, 79, 163)
BLANCO = (255, 255, 255)
W, H = 1280, 720
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


def sacar(video, t, destino):
    if PRUEBA:
        Image.new("RGB", (W, H), (60 + int(t) % 90, 90, 140)).save(destino, quality=92)
        return
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", str(fuente(video)), "-frames:v", "1",
                        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}", "-q:v", "2",
                        str(destino)], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-300:])


def letra(tam):
    return ImageFont.truetype(CARPETA + "Montserrat-Black.ttf", tam)


def texto(im, xy, s, tam, color=BLANCO, contorno=10, ancla="la", sombra=True):
    """Texto grande con contorno negro y sombra suave (se dibuja a 2x y se reduce: bordes suaves)."""
    d = ImageDraw.Draw(im)
    if sombra:
        capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(capa).text((xy[0] + 6, xy[1] + 10), s, font=letra(tam), fill=(0, 0, 0, 200), anchor=ancla,
                                  stroke_width=contorno, stroke_fill=(0, 0, 0, 200))
        capa = capa.filter(ImageFilter.GaussianBlur(10))
        im.alpha_composite(capa)
    d = ImageDraw.Draw(im)
    d.text(xy, s, font=letra(tam), fill=color, anchor=ancla, stroke_width=contorno, stroke_fill=(0, 0, 0))


def degradado_izquierdo(im, ancho=760, fuerza=215):
    capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
    px = capa.load()
    for x in range(ancho):
        a = int(fuerza * (1 - x / ancho) ** 1.4)
        for y in range(im.size[1]):
            px[x, y] = (8, 6, 18, a)
    im.alpha_composite(capa)


def marca(im):
    d = ImageDraw.Draw(im)
    s = "LEÓNIDA AL DÍA"
    f = ImageFont.truetype(CARPETA + "Montserrat-ExtraBold.ttf", 30)
    x = W - 40 - d.textlength(s, font=f)
    d.text((x + 2, H - 52), s, font=f, fill=(0, 0, 0, 160))
    d.text((x, H - 54), s, font=f, fill=BLANCO)


def mejora(im):
    """Un poco más de contraste y color para que destaque entre las demás miniaturas."""
    from PIL import ImageEnhance
    im = ImageEnhance.Contrast(im).enhance(1.12)
    return ImageEnhance.Color(im).enhance(1.15)


def estilo_a(base):
    im = mejora(base.convert("RGB")).convert("RGBA")
    degradado_izquierdo(im)
    texto(im, (60, 120), "20", 470, ROSA, contorno=12, ancla="lt")
    texto(im, (66, 520), "CURIOSIDADES", 92, BLANCO, contorno=8, ancla="lt")
    texto(im, (66, 610), "DE GTA 6", 70, ROSA, contorno=7, ancla="lt")
    marca(im)
    return im


def estilo_b(base):
    im = mejora(base.convert("RGB")).convert("RGBA")
    degradado_izquierdo(im, 820, 225)
    texto(im, (60, 60), "20 COSAS", 128, BLANCO, contorno=9, ancla="lt")
    texto(im, (60, 190), "QUE NO", 128, BLANCO, contorno=9, ancla="lt")
    texto(im, (60, 320), "SABÍAS", 160, ROSA, contorno=11, ancla="lt")
    texto(im, (62, 560), "GTA 6", 130, BLANCO, contorno=9, ancla="lt")
    marca(im)
    return im


def estilo_c(base):
    im = mejora(base.convert("RGB")).convert("RGBA")
    capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    d.rectangle((0, H - 250, W, H), fill=(8, 6, 18, 175))
    d.rectangle((0, H - 250, W, H - 242), fill=ROSA + (255,))
    im.alpha_composite(capa)
    texto(im, (W // 2, 70), "GTA 6", 200, BLANCO, contorno=12, ancla="mt")
    texto(im, (W // 2, H - 232), "20 CURIOSIDADES", 118, ROSA, contorno=9, ancla="mt")
    texto(im, (W // 2, H - 100), "QUE NADIE TE HA CONTADO", 58, BLANCO, contorno=6, ancla="mt")
    return im


def guardar(im, nombre):
    destino = SALIDA / nombre
    rgb = im.convert("RGB")
    calidad = 92
    while True:
        rgb.save(destino, quality=calidad, optimize=True)
        if destino.stat().st_size < 1_900_000 or calidad <= 70:
            break
        calidad -= 4
    print(nombre, f"{destino.stat().st_size / 1e3:.0f} KB", flush=True)


def main():
    pares = [x.strip() for x in os.environ.get("FRAMES", "Lanzamiento:40.5,Mirada:1013,Lanzamiento:26.5").split(",")
             if x.strip()]
    candidatos = []
    for i, p in enumerate(pares):
        v, t = p.split(":")
        destino = SALIDA / f"candidato_{i + 1}_{v}_{t}.jpg"
        sacar(v, float(t), destino)
        candidatos.append(destino)
    estilos = [estilo_a, estilo_b, estilo_c]
    for i, f in enumerate(estilos):
        if i < len(candidatos):
            guardar(f(Image.open(candidatos[i])), f"miniatura_{'abc'[i]}.jpg")
    # hoja con los fotogramas candidatos
    hoja = Image.new("RGB", (3 * 480, ((len(candidatos) + 2) // 3) * 270), (0, 0, 0))
    for i, c in enumerate(candidatos):
        hoja.paste(Image.open(c).resize((480, 270)), ((i % 3) * 480, (i // 3) * 270))
    hoja.save(SALIDA / "candidatos.jpg", quality=88)


if __name__ == "__main__":
    main()
