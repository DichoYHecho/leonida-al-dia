"""Busca en qué segundo suenan las canciones de los vídeos oficiales (Whisper en inglés). No publica nada.

Se ejecuta solo al subir cambios a este archivo en la rama vice-city. Deja la transcripción con tiempos en el resumen
del run y en «musica.txt», para elegir los trozos con sonido original del vídeo largo 2 (trozos_vc.csv)."""
import os
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import importlib  # noqa: E402

import prototipo as P  # noqa: E402
from faster_whisper import WhisperModel  # noqa: E402

P.VIDEOS.update(importlib.import_module("guion_vc").VIDEOS_EXTRA)

FRASES = {
    "VC_Aniv": [],
    "Trailer_1": ["love is a long road"],
    "Trailer_2": ["hot together"],
    "Lanzamiento": [],
    "Mirada": ["take a look at me now", "against all odds", "people are people", "love bites", "let your love flow"],
}


def main():
    modelo = WhisperModel(P.modelo_whisper(), device="cpu", compute_type="int8")
    inf = []
    for video, frases in FRASES.items():
        wav = pathlib.Path(f"audio_{video}.wav")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-user_agent", P.UA, "-i", P.VIDEOS[video], "-vn",
                        "-ac", "1", "-ar", "16000", str(wav)], check=True)
        segs = list(modelo.transcribe(P.audio_16k(wav), language="en", word_timestamps=True, vad_filter=False)[0])
        inf.append(f"## {video}")
        for s in segs:
            inf.append(f"{s.start:7.2f}-{s.end:7.2f} {s.text.strip()}")
        pal = [(P.normalizar(w.word), w.start, w.end) for s in segs for w in (s.words or [])]
        for f in frases:
            obj = [P.normalizar(x) for x in f.split()]
            for i in range(len(pal) - len(obj) + 1):
                if all(pal[i + k][0] == obj[k] for k in range(len(obj))):
                    inf.append(f"ENCONTRADA «{f}» en {video}: {pal[i][1]:.2f}-{pal[i + len(obj) - 1][2]:.2f} s")
        wav.unlink()
        print("\n".join(inf[-5:]), flush=True)
    texto = "\n".join(inf)
    print(texto)
    pathlib.Path("musica.txt").write_text(texto, encoding="utf-8")
    resumen = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumen:
        with open(resumen, "a", encoding="utf-8") as f:
            f.write("### Música de los vídeos oficiales\n\n```\n" + texto[:60000] + "\n```\n")


if __name__ == "__main__":
    main()
