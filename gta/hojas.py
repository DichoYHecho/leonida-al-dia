"""Hojas de contacto y transcripción de un vídeo oficial de Rockstar, para elegir trozos sin destripes.

Saca un fotograma cada CADA segundos (con su minuto y segundo encima) en hojas de 5 × 8, y transcribe
con Whisper lo que se dice (para no coger trozos con diálogos de la historia). No sube nada a ninguna red."""
import os, subprocess, sys
import numpy as np, soundfile as sf

ORIGEN = sys.argv[1] if len(sys.argv) > 1 else "oficial.mp4"
CADA = float(os.environ.get("CADA") or 4)
SALIDA = "salida_hojas"
LETRA = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"


def hms(t):
    return f"{int(t // 60):02d}:{int(t % 60):02d}"


def main():
    os.makedirs(SALIDA, exist_ok=True)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                         "csv=p=0", ORIGEN]).decode().strip())
    print(f"Duración: {hms(dur)} ({dur:.0f} s)", flush=True)
    filtro = (f"fps=1/{CADA},scale=384:-2,"
              f"drawtext=fontfile={LETRA}:text='%{{pts\\:hms}}':x=6:y=6:fontsize=22:fontcolor=white:"
              f"box=1:boxcolor=black@0.65:boxborderw=4,tile=5x8:padding=4:margin=4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", ORIGEN, "-vf", filtro, "-q:v", "4",
                    os.path.join(SALIDA, "hoja_%02d.jpg")], check=True)
    print(f"Hojas: {len([f for f in os.listdir(SALIDA) if f.startswith('hoja_')])}", flush=True)

    # Sonido: volumen cada 2 s y transcripción
    wav = "sonido.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", ORIGEN, "-vn", "-ac", "1", "-ar", "16000", wav],
                   check=True)
    x, sr = sf.read(wav, dtype="float32")
    with open(os.path.join(SALIDA, "volumen.txt"), "w") as f:
        for i in range(0, len(x), 2 * sr):
            r = np.sqrt(np.mean(x[i:i + 2 * sr] ** 2)) + 1e-9
            f.write(f"{hms(i / sr)}  {20 * np.log10(r):6.1f} dB\n")
    from faster_whisper import WhisperModel
    modelo = WhisperModel("base", device="cpu", compute_type="int8")
    segs, info = modelo.transcribe(x, language=None, vad_filter=True)
    with open(os.path.join(SALIDA, "transcripcion.txt"), "w", encoding="utf-8") as f:
        f.write(f"Idioma detectado: {info.language} ({info.language_probability:.2f})\n")
        for s in segs:
            f.write(f"[{hms(s.start)}-{hms(s.end)}] {s.text.strip()}\n")
    print("Transcripción hecha", flush=True)


if __name__ == "__main__":
    main()
