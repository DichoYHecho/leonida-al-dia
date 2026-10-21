"""Hojas para revisar los trozos candidatos (trozos_candidatos.csv) antes de usarlos: 2 fotogramas por segundo desde 2 s antes hasta
2 s después de cada trozo (en verde, los que entran), para ver si hay cortes de plano o algo que no debe salir.
Además corta los trozos (los deja en la caché) y monta un vídeo de prueba con todos seguidos, ya en vertical.
No toca Airtable ni publica nada."""
import os, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont
import medios
from config import UA, VIDEO_OFICIAL

SALIDA = "salida_trozos"
LETRA = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
TW, TH = 160, 90


def fotogramas(inicio, dur, tmp):
    a = max(0.0, inicio - 2)
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{a:.2f}", "-t", f"{dur + 4:.2f}", "-user_agent", UA,
                    "-reconnect", "1", "-reconnect_on_network_error", "1", "-i", VIDEO_OFICIAL,
                    "-vf", f"fps=2,scale={TW}:{TH}", "-q:v", "4", os.path.join(tmp, "f_%03d.jpg")], check=True)
    return a, [os.path.join(tmp, f) for f in sorted(os.listdir(tmp))]


def main():
    os.makedirs(SALIDA, exist_ok=True)
    # Se revisan los candidatos (trozos_candidatos.csv); los buenos pasan después a trozos.csv
    medios.TROZOS = {n: t for n, t in medios.tabla_trozos(os.environ.get("TROZOS_CSV") or "trozos_candidatos.csv").items()
                     if t["grupo"] in medios.GRUPOS}
    medios.CAPTURAS.update(medios.TROZOS)
    letra = ImageFont.truetype(LETRA, 14)
    tmp = tempfile.mkdtemp()
    filas = []
    for n, t in medios.TROZOS.items():
        a, fs = fotogramas(t["inicio"], t["dur"], tmp)
        fila = Image.new("RGB", (220 + len(fs) * (TW + 2), TH + 24), (20, 20, 20))
        d = ImageDraw.Draw(fila)
        d.text((4, 4), n, font=letra, fill=(255, 255, 255))
        d.text((4, 24), f"{int(t['inicio'] // 60):02d}:{t['inicio'] % 60:04.1f} · {t['dur']:.0f} s", font=letra, fill=(200, 200, 200))
        d.text((4, 44), t["grupo"], font=letra, fill=(200, 200, 200))
        for i, p in enumerate(fs):
            ts = a + i * 0.5
            dentro = t["inicio"] <= ts < t["inicio"] + t["dur"]
            x = 220 + i * (TW + 2)
            fila.paste(Image.open(p), (x, 20))
            d.rectangle([x, 20, x + TW - 1, 20 + TH - 1], outline=(0, 220, 0) if dentro else (90, 90, 90), width=3 if dentro else 1)
            d.text((x + 2, 2), f"{int(ts // 60):02d}:{ts % 60:04.1f}", font=letra, fill=(255, 255, 255))
        filas.append(fila)
        print(f"{n}: {len(fs)} fotogramas", flush=True)
    for k in range(0, len(filas), 6):
        grupo = filas[k:k + 6]
        hoja = Image.new("RGB", (max(f.width for f in grupo), sum(f.height + 6 for f in grupo)), (0, 0, 0))
        y = 0
        for f in grupo:
            hoja.paste(f, (0, y))
            y += f.height + 6
        hoja.save(os.path.join(SALIDA, f"trozos_{k // 6 + 1:02d}.jpg"), quality=85)
    # Los trozos ya cortados en vertical, seguidos, para verlos como saldrán
    medios.preparar_trozos()
    lista = os.path.join(tmp, "lista.txt")
    rutas = [medios.ruta_sin_comprobar(n) for n in medios.TROZOS if os.path.exists(medios.ruta_sin_comprobar(n))]
    open(lista, "w").write("".join(f"file '{os.path.abspath(r)}'\n" for r in rutas))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista, "-an",
                    "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "30", os.path.join(SALIDA, "trozos_verticales.mp4")],
                   check=True)
    print(f"Trozos cortados: {len(rutas)} de {len(medios.TROZOS)}", flush=True)


if __name__ == "__main__":
    main()
