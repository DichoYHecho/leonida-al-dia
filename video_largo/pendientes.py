"""Tarjetas «PENDIENTE» para los planos NUEVO_ que aún no existen, para poder montar previas ya.

Uso: python pendientes.py DIR_FUENTES DIR_GUIONES DIR_SALIDA TABLA_CSV
Lee los guiones (guion_13a, guion_pol, guion_rad), busca los planos NUEVO_ que no están en la tabla,
dibuja una tarjeta gris con el nombre y lo que hay que capturar (de edicion.md si se encuentra) y
añade su fila a la tabla con el grupo «Pendientes_57». Cuando exista la captura real, se cambia esa fila."""
import csv
import importlib.util
import pathlib
import re
import sys

from PIL import Image, ImageDraw, ImageFont

DIR_F, DIR_G, SALIDA, TABLA = (pathlib.Path(a) for a in sys.argv[1:5])
SALIDA.mkdir(parents=True, exist_ok=True)
URL = "https://raw.githubusercontent.com/DichoYHecho/leonida-al-dia/videos-5-7/video_largo/imagenes/pendientes/"


def mont(tam, peso):
    f = ImageFont.truetype(str(DIR_F / "Montserrat.ttf"), tam)
    f.set_variation_by_axes([peso])
    return f


def que_se_ve(nombre):
    """Descripción del plano sacada de los edicion.md de las carpetas de vídeo (si está)."""
    for md in DIR_G.parent.glob("video_*/edicion.md"):
        for linea in md.read_text(encoding="utf-8").splitlines():
            if linea.startswith("|") and nombre in linea.split("|")[1]:
                celdas = [c.strip() for c in linea.strip("|").split("|")]
                return next((c for c in celdas[1:] if not re.fullmatch(r"[\d, ]+", c)), "")
    return ""


existentes = set()
with open(TABLA, encoding="utf-8") as f:
    existentes = {r["Trozo"] for r in csv.DictReader(f)}

pendientes = {}
for g in ("guion_13a", "guion_pol", "guion_rad"):
    spec = importlib.util.spec_from_file_location(g, DIR_G / f"{g}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    for b in m.BLOQUES:
        for p in list(b.get("planos", [])) + [r["plano"] for r in b.get("planos_en", [])]:
            if p.startswith("NUEVO_") and p not in existentes:
                pendientes.setdefault(p, g)

filas = []
for nombre, g in sorted(pendientes.items()):
    img = Image.new("RGB", (1920, 1080), (38, 38, 44))
    d = ImageDraw.Draw(img)
    for x in range(-1080, 1920, 90):  # rayas diagonales: que se note que es provisional
        d.line([(x, 0), (x + 1080, 1080)], fill=(48, 48, 56), width=30)
    d.text((160, 200), "PLANO PENDIENTE", font=mont(96, 900), fill=(255, 196, 0))
    d.text((160, 340), nombre, font=mont(64, 800), fill=(255, 255, 255))
    texto = que_se_ve(nombre) or "Captura por conseguir"
    y = 460
    for i in range(0, len(texto), 60):
        d.text((160, y), texto[i:i + 60], font=mont(42, 600), fill=(200, 200, 210))
        y += 60
    d.text((160, 690), f"{g} · previa provisional", font=mont(32, 600), fill=(140, 140, 150))
    img.save(SALIDA / f"{nombre}.png", optimize=True)
    filas.append([nombre, "Pendientes_57", "0", "4", f"PENDIENTE: {texto}", "0.5", "principal", "no",
                  "Provisional: cambiar por la captura real", f"Imagen:{URL}{nombre}.png", "1"])

with open(TABLA, "a", encoding="utf-8", newline="") as f:
    csv.writer(f, lineterminator="\n").writerows(filas)
print(len(filas), "tarjetas pendientes:", ", ".join(n for n, *_ in filas))
