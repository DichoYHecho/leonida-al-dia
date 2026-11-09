"""Voces del vídeo largo (Orus, estilo relajado): un audio por bloque del guion, con la clave GEMINI_API_KEY_VIDEO.

Reanuda: lo que ya está en la caché no se vuelve a pedir. Si se acaba el cupo del día (error 429) en los dos
modelos, se para y se sigue otro día. Deja los audios en «salida_voces/» (MP3 para escucharlos) y un informe."""
import base64
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import wave

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import guion_vl  # noqa: E402

CLAVE = os.environ.get("GEMINI_API_KEY", "").strip()
MODELOS = ["gemini-3.8-flash-lite-tts", "gemini-3.8-flash-tts"]
VOZ = "Orus"
ESTILO = (
    "Relaxed, friendly Spanish gaming YouTuber telling a funny story to a friend. "
    "Native Castilian Spanish accent from Spain. Warm and close, light humour, natural pauses "
    "between sentences, lively but never rushed, never sounds like an advert or a radio announcer."
)
VOCES = pathlib.Path(os.environ.get("CACHE_VOZ", "cache/voz_vl"))
SALIDA = pathlib.Path("salida_voces")
VOCES.mkdir(parents=True, exist_ok=True)
SALIDA.mkdir(exist_ok=True)


def pedir(modelo, texto):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
    cuerpo = {
        "contents": [{"role": "user", "parts": [{"text": f"## Style:\n{ESTILO}\n\n## Transcript:\n{texto}"}]}],
        "generationConfig": {"temperature": 1, "responseModalities": ["AUDIO"],
                             "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOZ}}}},
    }
    pet = urllib.request.Request(url, data=json.dumps(cuerpo).encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json", "x-goog-api-key": CLAVE})
    with urllib.request.urlopen(pet, timeout=300) as resp:
        datos = json.loads(resp.read().decode("utf-8"))
    parte = datos["candidates"][0]["content"]["parts"][0]["inlineData"]
    frec = 24000
    m = re.search(r"rate=(\d+)", parte.get("mimeType", ""))
    if m:
        frec = int(m.group(1))
    return base64.b64decode(parte["data"]), frec


def ruta_wav(b):
    texto = b.get("voz") or b["texto"]
    h = hashlib.sha1((VOZ + ESTILO + texto).encode("utf-8")).hexdigest()[:10]
    return VOCES / f"{b['id']}_{h}.wav"


def main():
    if not CLAVE:
        print("Falta el secret GEMINI_API_KEY_VIDEO.")
        sys.exit(1)
    informe, agotado, pedidas = [], False, 0
    for b in guion_vl.BLOQUES:
        destino = ruta_wav(b)
        texto = b.get("voz") or b["texto"]
        if destino.exists():
            informe.append(f"{b['id']}: ya estaba")
            continue
        if agotado:
            informe.append(f"{b['id']}: PENDIENTE (cupo agotado)")
            continue
        hecho = False
        for modelo in MODELOS:
            try:
                if pedidas:
                    time.sleep(21)  # máximo 3 audios por minuto
                pcm, frec = pedir(modelo, texto)
                pedidas += 1
                with wave.open(str(destino), "wb") as f:
                    f.setnchannels(1)
                    f.setsampwidth(2)
                    f.setframerate(frec)
                    f.writeframes(pcm)
                informe.append(f"{b['id']}: hecho con {modelo} ({len(pcm) / 2 / frec:.1f} s)")
                print(informe[-1], flush=True)
                hecho = True
                break
            except urllib.error.HTTPError as e:
                cuerpo = e.read().decode("utf-8", "ignore")[:200]
                print(f"{b['id']} {modelo}: HTTP {e.code} {cuerpo}", flush=True)
                if e.code != 429:
                    informe.append(f"{b['id']}: ERROR {modelo} HTTP {e.code}")
            except Exception as e:  # noqa: BLE001
                print(f"{b['id']} {modelo}: {type(e).__name__} {e}", flush=True)
                informe.append(f"{b['id']}: ERROR {modelo} {type(e).__name__}")
        if not hecho:
            if not any(x.startswith(b["id"] + ": ERROR") for x in informe):
                agotado = True
                informe.append(f"{b['id']}: PENDIENTE (cupo agotado en los dos modelos)")
            else:
                informe.append(f"{b['id']}: PENDIENTE (falló; se reintenta la próxima vez)")
    # MP3 para escucharlos
    for b in guion_vl.BLOQUES:
        w = ruta_wav(b)
        if w.exists():
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(w), "-codec:a", "libmp3lame", "-q:a", "3",
                            str(SALIDA / f"{b['id']}.mp3")], check=False)
    hechos = sum(1 for b in guion_vl.BLOQUES if ruta_wav(b).exists())
    informe.insert(0, f"Voces listas: {hechos} de {len(guion_vl.BLOQUES)} (esta vez se pidieron {pedidas})")
    texto_inf = "\n".join(informe)
    (SALIDA / "informe.txt").write_text(texto_inf, encoding="utf-8")
    print(texto_inf)
    resumen = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumen:
        with open(resumen, "a", encoding="utf-8") as f:
            f.write("### Voces del vídeo largo\n\n" + texto_inf.replace("\n", "  \n") + "\n")


if __name__ == "__main__":
    main()
