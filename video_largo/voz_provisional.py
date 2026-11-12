"""Voz provisional (Piper, gratis y sin cupo) para las voces que aún no ha hecho Gemini. Solo para previas.

Uso: CACHE_VOZ=cache/voz_previa GUION=guion_rad python voz_provisional.py MODELO.onnx
Trabaja sobre una COPIA de la caché de voces (CACHE_VOZ): nunca escribe en cache/voz_vl, así que voces.py
sigue pidiendo a Gemini las que faltan. Usa los mismos nombres de archivo que voces.py (ruta_wav), y el
montaje las coge sin cambios. Voz: es_ES-davefx-medium (Piper, conjunto de datos CC0)."""
import os
import pathlib
import sys
import wave

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
if pathlib.Path(os.environ.get("CACHE_VOZ", "cache/voz_vl")).resolve() == pathlib.Path("cache/voz_vl").resolve():
    sys.exit("CACHE_VOZ apunta a la caché de Gemini: la voz provisional va en una copia (cache/voz_previa)")
import voces as V  # noqa: E402  (lee GUION y CACHE_VOZ)
from piper import PiperVoice  # noqa: E402

voz = PiperVoice.load(sys.argv[1])
hechas = []
for b in V.guion_vl.BLOQUES:
    destino = V.ruta_wav(b)
    if destino.exists():
        continue
    with wave.open(str(destino), "wb") as f:
        voz.synthesize_wav(b["texto"], f)
    hechas.append(b["id"])
    print(f"{b['id']}: voz provisional (Piper)", flush=True)
aviso = ("Voces provisionales (Piper) en esta previa: " + ", ".join(hechas)) if hechas else "Todas las voces son de Gemini"
print(aviso)
resumen = os.environ.get("GITHUB_STEP_SUMMARY")
if resumen:
    with open(resumen, "a", encoding="utf-8") as f:
        f.write(f"### Voz\n\n{aviso}\n")
