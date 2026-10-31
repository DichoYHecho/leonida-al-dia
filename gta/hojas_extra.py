"""Hojas para elegir material nuevo del stock (31 oct): los 9 clips oficiales (zip de vídeos) y el arte oficial
(zip de arte y fondos). Saca una fila de fotogramas por clip y una lámina con las miniaturas del arte, con su nombre,
tamaño y duración. No toca Airtable ni publica nada."""
import io, os, subprocess, sys, tempfile, zipfile
import requests
from PIL import Image, ImageDraw, ImageFont
from config import UA

ZIP_CLIPS = "https://media-rockstargames-com.akamaized.net/VI/downloads/videos/GTAVI_Videos.zip"
ZIP_ARTE = "https://media-rockstargames-com.akamaized.net/VI/downloads/artwork_wallpapers/GTAVI_Artwork_Wallpapers.zip"
SALIDA = "salida_extra"
LETRA = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"


def bajar(url):
    r = requests.get(url, headers={"User-Agent": UA}, timeout=1200)
    r.raise_for_status()
    return zipfile.ZipFile(io.BytesIO(r.content))


def probe(p):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height:format=duration", "-of", "default=nw=1", p]).decode()
    d = dict(l.split("=", 1) for l in out.split() if "=" in l)
    return int(d.get("width", 0)), int(d.get("height", 0)), float(d.get("duration", 0) or 0)


def clips(letra):
    z = bajar(ZIP_CLIPS)
    tmp = tempfile.mkdtemp()
    filas, info = [], []
    for i in z.infolist():
        if not i.filename.lower().endswith((".mp4", ".mov", ".m4v")) or "__MACOSX" in i.filename:
            continue
        nombre = os.path.basename(i.filename)
        p = os.path.join(tmp, nombre)
        with open(p, "wb") as f:
            f.write(z.read(i))
        w, h, dur = probe(p)
        info.append(f"{nombre}\t{w}x{h}\t{dur:.2f} s\t{i.file_size / 1e6:.1f} MB")
        n = 10
        fs = []
        for k in range(n):
            t = dur * (k + 0.5) / n
            q = os.path.join(tmp, f"f{k}.jpg")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", p, "-frames:v", "1",
                            "-vf", "scale=240:-2", q], check=True)
            fs.append((t, Image.open(q).convert("RGB")))
        th = max(im.height for _, im in fs)
        fila = Image.new("RGB", (260 + n * 244, th + 26), (20, 20, 20))
        d = ImageDraw.Draw(fila)
        d.text((4, 4), nombre[:30], font=letra, fill=(255, 255, 255))
        d.text((4, 24), f"{w}x{h} · {dur:.2f} s", font=letra, fill=(200, 200, 200))
        for k, (t, im) in enumerate(fs):
            x = 260 + k * 244
            fila.paste(im, (x, 22))
            d.text((x + 2, 4), f"{t:.2f} s", font=letra, fill=(200, 200, 200))
        filas.append(fila)
    if filas:
        W = max(f.width for f in filas)
        hoja = Image.new("RGB", (W, sum(f.height + 4 for f in filas)), (0, 0, 0))
        y = 0
        for f in filas:
            hoja.paste(f, (0, y))
            y += f.height + 4
        hoja.save(os.path.join(SALIDA, "clips.jpg"), quality=85)
    open(os.path.join(SALIDA, "clips.txt"), "w", encoding="utf-8").write("\n".join(info) + "\n")
    print(f"Clips: {len(info)}", flush=True)


def arte(letra):
    z = bajar(ZIP_ARTE)
    items, info = [], []
    for i in sorted(z.infolist(), key=lambda x: x.filename):
        if not i.filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")) or "__MACOSX" in i.filename:
            continue
        im = Image.open(io.BytesIO(z.read(i))).convert("RGB")
        nombre = os.path.basename(i.filename)
        info.append(f"{nombre}\t{im.width}x{im.height}\t{i.file_size / 1e6:.1f} MB")
        im.thumbnail((360, 300))
        items.append((nombre, im))
    col, cw, ch = 5, 372, 340
    for parte in range(0, len(items), 20):
        trozo = items[parte:parte + 20]
        filas = (len(trozo) + col - 1) // col
        hoja = Image.new("RGB", (col * cw, filas * ch), (20, 20, 20))
        d = ImageDraw.Draw(hoja)
        for k, (nombre, im) in enumerate(trozo):
            x, y = (k % col) * cw + 6, (k // col) * ch + 4
            hoja.paste(im, (x, y + 30))
            d.text((x, y + 4), f"{parte + k + 1}. {nombre[:34]}", font=letra, fill=(255, 255, 255))
        hoja.save(os.path.join(SALIDA, f"arte_{parte // 20 + 1}.jpg"), quality=85)
    open(os.path.join(SALIDA, "arte.txt"), "w", encoding="utf-8").write(
        "\n".join(f"{k + 1}. {l}" for k, l in enumerate(info)) + "\n")
    print(f"Arte: {len(info)}", flush=True)


def main():
    os.makedirs(SALIDA, exist_ok=True)
    letra = ImageFont.truetype(LETRA, 15)
    errores = 0
    for paso in (clips, arte):
        try:
            paso(letra)
        except Exception as e:  # que un zip que falla no impida el otro
            print(f"⚠️ {paso.__name__}: {e}", flush=True)
            errores += 1
    sys.exit(1 if errores == 2 else 0)


if __name__ == "__main__":
    main()
