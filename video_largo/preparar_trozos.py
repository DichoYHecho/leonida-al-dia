"""Trozos automáticos de los vídeos de los juegos (vídeo 2: Vice City).

Baja cada fuente de fuentes_vc.py, busca los cambios de plano y elige trozos de 2-3 s que no sean
negros ni planos lisos (rótulos). Deja trozos_auto.csv y una hoja de contactos por fuente en
salida_trozos (el workflow la publica en la rama trozos-vc)."""
import csv
import os
import pathlib
import re
import subprocess
import sys
import urllib.request

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from fuentes_vc import FUENTES  # noqa: E402

TMP = pathlib.Path("tmp_trozos")
OUT = pathlib.Path("salida_trozos")
TMP.mkdir(exist_ok=True)
(OUT / "hojas").mkdir(parents=True, exist_ok=True)
CAMPOS = ["Trozo", "Grupo", "Inicio (s)", "Duración (s)", "Qué se ve", "Foco (0 izquierda - 1 derecha)", "Uso", "Sonido",
          "Notas", "Vídeo", "Lento"]


def bajar(url, destino):
    if destino.exists() and destino.stat().st_size > 0:
        return
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=600) as r, open(destino, "wb") as f:
        while True:
            trozo = r.read(1 << 20)
            if not trozo:
                break
            f.write(trozo)


def duracion(ruta):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(ruta)],
                       capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def cortes(ruta):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(ruta), "-an", "-vf",
                        "scale=320:-2,select='gt(scene,0.3)',showinfo", "-f", "null", "-"], capture_output=True, text=True)
    return [float(x) for x in re.findall(r"pts_time:([0-9.]+)", r.stderr)]


def fotograma(ruta, t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", str(ruta), "-frames:v", "1", "-vf",
                        "scale=320:180:force_original_aspect_ratio=increase,crop=320:180",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    n = 320 * 180 * 3
    return np.frombuffer(r.stdout[:n], np.uint8).reshape(180, 320, 3) if len(r.stdout) >= n else None


def vale(img):
    if img is None:
        return False
    g = img.mean(axis=2)
    return g.mean() >= 30 and g.std() >= 18


def repartir(lista, n):
    if len(lista) <= n:
        return lista
    idx = sorted(set(np.linspace(0, len(lista) - 1, n).round().astype(int)))
    return [lista[i] for i in idx]


def main():
    filas, resumen = [], []
    for clave, f in FUENTES.items():
        ruta = TMP / (clave + ".mp4")
        try:
            bajar(f["url"], ruta)
        except Exception as e:  # noqa: BLE001
            resumen.append(f"| {clave} | no se pudo bajar: {e} |")
            continue
        dur = duracion(ruta)
        desde, hasta = f.get("desde", 0.0), min(f.get("hasta") or dur, dur) - 0.3
        cs = [desde] + [c for c in cortes(ruta) if desde < c < hasta] + [hasta]
        cand = []
        for a, b in zip(cs, cs[1:]):
            t = a + 0.25
            while b - t >= 1.6:
                cand.append((t, min(3.0, b - t - 0.15)))
                t += 8.0
        cand = repartir(cand, f.get("max", 15) * 3)
        elegidos = []
        for t, d in cand:
            img = fotograma(ruta, t + d / 2)
            if vale(img):
                elegidos.append((t, d, img))
        elegidos = repartir(elegidos, f.get("max", 15))
        cols = 5
        hoja = Image.new("RGB", (cols * 320, max(1, (len(elegidos) + cols - 1) // cols) * 200), "black")
        dib = ImageDraw.Draw(hoja)
        for k, (t, d, img) in enumerate(elegidos):
            nombre = f"{clave}_{k + 1:02d}"
            x, y = (k % cols) * 320, (k // cols) * 200
            hoja.paste(Image.fromarray(img), (x, y))
            dib.text((x + 4, y + 184), f"{nombre}  ({t:.1f} s)", fill=(255, 215, 0))
            filas.append({"Trozo": nombre, "Grupo": f["grupo"], "Inicio (s)": f"{t:.2f}", "Duración (s)": f"{d:.2f}",
                          "Qué se ve": "automático", "Foco (0 izquierda - 1 derecha)": "0.5", "Uso": "principal",
                          "Sonido": "no", "Notas": f["url"], "Vídeo": clave, "Lento": "1"})
        hoja.save(OUT / "hojas" / f"{clave}.jpg", quality=80)
        resumen.append(f"| {clave} | {f['grupo']} | {dur:.0f} s | {len(cs) - 2} cortes | {len(elegidos)} trozos |")
        ruta.unlink()
    with open(OUT / "trozos_auto.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(filas)
    texto = "## Trozos automáticos\n\n| Fuente | Grupo | Duración | Cortes | Trozos |\n|---|---|---|---|---|\n" + "\n".join(resumen)
    texto += f"\n\nTotal: {len(filas)} trozos\n"
    (OUT / "informe.md").write_text(texto, encoding="utf-8")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as fh:
            fh.write(texto)
    print(texto)


if __name__ == "__main__":
    main()
