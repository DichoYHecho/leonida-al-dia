"""Prueba de voces para el vídeo largo de «Leónida al Día» (fase V-L2).

Solo se lanza a mano. Genera 5 audios con el mismo texto (la curiosidad del
perro) para elegir voz y estilo. Gasta 5 audios del modelo «lite»
(cupo aparte del modelo normal, que usan los Shorts).

No toca Airtable, Buffer ni YouTube. Deja los MP3 en la carpeta «salida/».
"""
import base64
import json
import os
import pathlib
import subprocess
import sys
import time
import urllib.error
import urllib.request
import wave

CLAVE = os.environ.get("GEMINI_API_KEY", "").strip()
MODELO = os.environ.get("MODELO_TTS", "gemini-3.8-flash-lite-tts").strip()
ESPERA = 21  # máximo 3 audios por minuto
SALIDA = pathlib.Path("salida")
SALIDA.mkdir(exist_ok=True)

TEXTO = (
    "Al principio del Extended Look, Jason se encuentra un perro, y el juego le "
    "da tres opciones: regañarlo, acariciarlo o... estudiarlo. Estudiarlo. "
    "A un perro. ... Jason lo acaricia, sale un iconito de ángel, suena una "
    "campanita... y su karma mejora. Poco después, Lucía huye de un atraco y se "
    "lleva karma negativo. Moraleja: puedes atracar una tienda, pero acaricia "
    "al perro."
)

ESTILO_RELAJADO = (
    "Relaxed, friendly Spanish gaming YouTuber telling a funny story to a "
    "friend. Native Castilian Spanish accent from Spain. Warm and close, light "
    "humour, natural pauses between sentences, lively but never rushed, never "
    "sounds like an advert or a radio announcer."
)
ESTILO_SHORTS = "High energy, elongated vowels."

# (nombre del archivo, voz de Gemini, estilo)
VARIANTES = [
    ("1_koda_relajada", "Koda", ESTILO_RELAJADO),
    ("2_ludo_relajada", "Ludo", ESTILO_RELAJADO),
    ("3_orus_relajada", "Orus", ESTILO_RELAJADO),
    ("4_mako_relajada", "Mako", ESTILO_RELAJADO),
    ("5_mako_estilo_shorts", "Mako", ESTILO_SHORTS),
]


def sintetizar(voz, estilo):
    """Pide un audio a Gemini y devuelve (bytes PCM, frecuencia)."""
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{MODELO}:generateContent"
    )
    cuerpo = {
        "contents": [{"parts": [{"text": f"{estilo}\n\n{TEXTO}"}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voz}}
            },
        },
    }
    peticion = urllib.request.Request(
        url,
        data=json.dumps(cuerpo).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": CLAVE},
        method="POST",
    )
    with urllib.request.urlopen(peticion, timeout=180) as respuesta:
        datos = json.loads(respuesta.read().decode("utf-8"))
    parte = datos["candidates"][0]["content"]["parts"][0]["inlineData"]
    frecuencia = 24000
    mime = parte.get("mimeType", "")
    if "rate=" in mime:
        try:
            frecuencia = int(mime.split("rate=")[1].split(";")[0])
        except ValueError:
            pass
    return base64.b64decode(parte["data"]), frecuencia


def guardar_mp3(pcm, frecuencia, nombre):
    wav = SALIDA / f"{nombre}.wav"
    mp3 = SALIDA / f"{nombre}.mp3"
    with wave.open(str(wav), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(frecuencia)
        f.writeframes(pcm)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav),
         "-codec:a", "libmp3lame", "-q:a", "3", str(mp3)],
        check=True,
    )
    segundos = len(pcm) / 2 / frecuencia
    wav.unlink()
    return mp3, segundos


def main():
    if not CLAVE:
        print("Falta el secret GEMINI_API_KEY (o GEMINI_API_KEY_VIDEO).")
        sys.exit(1)
    informe = [f"Modelo: {MODELO}", ""]
    hechos = 0
    for i, (nombre, voz, estilo) in enumerate(VARIANTES):
        if i:
            time.sleep(ESPERA)
        try:
            pcm, frecuencia = sintetizar(voz, estilo)
            mp3, segundos = guardar_mp3(pcm, frecuencia, nombre)
            linea = (f"OK  {nombre}: voz {voz}, {segundos:.1f} s, "
                     f"{mp3.stat().st_size / 1024:.0f} KB")
            hechos += 1
        except urllib.error.HTTPError as e:
            cuerpo = e.read().decode("utf-8", "ignore")[:300]
            linea = f"ERROR {nombre}: voz {voz}, HTTP {e.code} {cuerpo}"
            if e.code == 429:
                informe.append(linea)
                informe.append("Cupo agotado: se para aquí.")
                break
        except Exception as e:  # noqa: BLE001
            linea = f"ERROR {nombre}: voz {voz}, {type(e).__name__}: {e}"
        print(linea)
        informe.append(linea)
    texto = "\n".join(informe)
    (SALIDA / "informe.txt").write_text(texto, encoding="utf-8")
    resumen = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumen:
        with open(resumen, "a", encoding="utf-8") as f:
            f.write("### Prueba de voces del vídeo largo\n\n```\n" + texto + "\n```\n")
    if not hechos:
        sys.exit(1)


if __name__ == "__main__":
    main()
