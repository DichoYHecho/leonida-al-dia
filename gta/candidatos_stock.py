"""Trozos nuevos del stock (31 oct): de `stock_nuevo.csv` (momento aproximado de cada plano, elegido en las hojas de
contacto) saca el plano exacto con la detección de cambios de plano de FFmpeg, sin cortes dentro del trozo, y deja
`trozos_candidatos_stock.csv` con el mismo formato que `trozos.csv`. Después corta cada trozo como en producción
(medios.cortar, ya en vertical) y monta hojas con 4 fotogramas de cada uno para revisarlos. No toca Airtable ni publica."""
import csv, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
import medios

ENTRADA = os.path.join(medios.AQUI, "stock_nuevo.csv")
SALIDA = "salida_candidatos"
LETRA = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
MARGEN = 0.12  # segundos que se dejan a cada lado del cambio de plano
CAMPOS = ["Trozo", "Grupo", "Inicio (s)", "Duración (s)", "Qué se ve", "Foco (0 izquierda - 1 derecha)", "Uso", "Sonido",
          "Notas", "Vídeo", "Lento"]


def red(src):
    return (["-user_agent", medios.UA, "-reconnect", "1", "-reconnect_on_network_error", "1", "-reconnect_delay_max", "10"]
            if src.startswith("http") else [])


def cortes(src, a, b):
    """Cambios de plano entre a y b (en segundos del vídeo)."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-ss", f"{a:.2f}", "-t", f"{b - a:.2f}", *red(src), "-i", src, "-an",
                        "-vf", "scale=480:-2,select='gt(scene\\,0.22)',showinfo", "-f", "null", "-"],
                       capture_output=True, text=True)
    return [a + float(x) for x in re.findall(r"pts_time:([\d.]+)", r.stderr)]


def plano(src, t, maximo):
    a, b = max(0.0, t - 8), t + 8
    cs = cortes(src, a, b)
    ini = max([c for c in cs if c <= t], default=a) + MARGEN
    fin = min([c for c in cs if c > t], default=b) - MARGEN
    if fin - ini > maximo:
        ini = max(ini, min(t - maximo / 2, fin - maximo))
        fin = ini + maximo
    return round(ini, 2), round(fin - ini, 2), cs


def duracion(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                          "csv=p=0", p]).decode().strip() or 0)


def main():
    os.makedirs(SALIDA, exist_ok=True)
    with open(ENTRADA, encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    out, log = [], []
    for r in filas:
        v = r["Vídeo"].strip()
        src = medios.origen(v)
        t, maximo = float(r["Aprox (s)"]), float(r["Máx (s)"] or 5)
        if v.startswith("Clips:"):  # clip del zip: desde «Aprox» y «Máx» segundos, tal cual
            ini, dur, cs = t, maximo, []
        else:
            ini, dur, cs = plano(src, t, maximo)
        nota = "corto" if dur * float(r["Lento"] or 1) < 1.5 else ""
        log.append(f"{r['Trozo']}: {v} {ini:.2f} + {dur:.2f} s {nota} · cortes cerca: {', '.join(f'{c:.2f}' for c in cs)}")
        print(log[-1], flush=True)
        out.append({"Trozo": r["Trozo"], "Grupo": r["Grupo"], "Inicio (s)": f"{ini:g}", "Duración (s)": f"{dur:g}",
                    "Qué se ve": r["Qué se ve"], "Foco (0 izquierda - 1 derecha)": "0.5", "Uso": r["Uso"], "Sonido": "no",
                    "Notas": f"{v} ~{t:g} s (31 oct){' · ' + nota if nota else ''}", "Vídeo": v, "Lento": r["Lento"] or "1"})
    p = os.path.join(SALIDA, "trozos_candidatos_stock.csv")
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(out)
    open(os.path.join(SALIDA, "planos.txt"), "w", encoding="utf-8").write("\n".join(log) + "\n")

    # Cortar como en producción y sacar 4 fotogramas de cada trozo (ya en vertical)
    tabla = medios.tabla_trozos(os.path.abspath(p))
    letra = ImageFont.truetype(LETRA, 15)
    fichas = []
    for n, t in tabla.items():
        mp4 = os.path.join(SALIDA, n + ".mp4")
        if not medios.cortar(n, t, mp4):
            continue
        d = duracion(mp4)
        ficha = Image.new("RGB", (4 * 184 + 8, 320 + 50), (20, 20, 20))
        dr = ImageDraw.Draw(ficha)
        dr.text((4, 4), f"{n} · {t['grupo']} · {d:.1f} s", font=letra, fill=(255, 255, 255))
        dr.text((4, 24), t["que"][:80], font=letra, fill=(190, 190, 190))
        for k, fr in enumerate((0.04, 0.35, 0.65, 0.96)):
            q = os.path.join(SALIDA, "f.jpg")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{d * fr:.2f}", "-i", mp4, "-frames:v", "1",
                            "-vf", "scale=180:320", q], check=True)
            ficha.paste(Image.open(q), (4 + k * 184, 46))
        fichas.append(ficha)
        os.remove(mp4)  # el vídeo no hace falta guardarlo
    por = 12
    for h in range(0, len(fichas), por):
        grupo = fichas[h:h + por]
        filas_h = (len(grupo) + 1) // 2
        hoja = Image.new("RGB", (2 * (grupo[0].width + 10), filas_h * (grupo[0].height + 10)), (0, 0, 0))
        for k, fi in enumerate(grupo):
            hoja.paste(fi, ((k % 2) * (fi.width + 10), (k // 2) * (fi.height + 10)))
        hoja.save(os.path.join(SALIDA, f"revision_{h // por + 1}.jpg"), quality=85)
    print(f"Trozos revisados: {len(fichas)} de {len(out)}", flush=True)
    sys.exit(0 if fichas else 1)


if __name__ == "__main__":
    main()
