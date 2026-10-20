"""Gemini (nivel gratuito): textos en JSON y la voz «Mako» con estilo «Promote».

Límites gratis (panel de AI Studio, 20 oct 2026): texto 3.5 Flash Lite 15/min y 500/día;
voz 3.8 Flash TTS y 3.8 Flash Lite TTS 3/min y 10/día cada uno. Un audio por vídeo."""
import base64, io, json, os, re, time, wave
import requests
from config import MODELOS_TEXTO, MODELOS_VOZ, VOZ, ESTILO_VOZ

CLAVE = os.environ.get("GEMINI_API_KEY", "")
API = "https://generativelanguage.googleapis.com/v1beta"
_ultima_voz = 0.0


def _post(url, cuerpo, timeout=180):
    if not CLAVE:
        raise SystemExit("Falta el secret GEMINI_API_KEY")
    r = requests.post(url, json=cuerpo, timeout=timeout,
                      headers={"x-goog-api-key": CLAVE, "Content-Type": "application/json"})
    if r.status_code >= 400:
        raise RuntimeError(f"Gemini {r.status_code}: {r.text[:300]}")
    return r.json()


def texto_json(prompt, temperatura=0.4):
    """Pide un JSON a Gemini. Prueba el modelo principal y, si falla, el de reserva."""
    errores = []
    for modelo in MODELOS_TEXTO:
        for intento in range(2):
            try:
                d = _post(f"{API}/models/{modelo}:generateContent", {
                    "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                    "generationConfig": {"responseMimeType": "application/json", "temperature": temperatura}})
                txt = d["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(txt)
            except Exception as e:  # 503 por saturación, JSON roto…
                errores.append(f"{modelo}: {str(e)[:160]}")
                time.sleep(8 * (intento + 1))
    raise RuntimeError("Gemini no contestó: " + " | ".join(errores))


def _esperar_cupo():
    """Como mucho 3 audios por minuto: deja 21 s entre uno y otro."""
    global _ultima_voz
    falta = 21 - (time.time() - _ultima_voz)
    if falta > 0:
        time.sleep(falta)
    _ultima_voz = time.time()


def _wav_de_pcm(pcm, sr=24000):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm)
    return buf.getvalue()


def _voz_interactions(modelo, texto):
    d = _post(f"{API}/interactions", {
        "model": modelo,
        "input": [{"type": "user_input", "content": [{
            "type": "text", "text": texto,
            "annotations": [{"type": "speech_metadata", "style": ESTILO_VOZ}]}]}],
        "response_format": {"type": "audio"},
        "generation_config": {"speech_config": [{"voice": VOZ}]}})
    audios = [c for s in d.get("steps", []) if s.get("type") == "model_output"
              for c in s.get("content", []) if c.get("type") == "audio" and c.get("data")]
    if not audios:
        raise RuntimeError("la respuesta no trae audio: " + json.dumps(d)[:200])
    datos = base64.b64decode(audios[-1]["data"])
    return datos if datos[:4] == b"RIFF" else _wav_de_pcm(datos)


def _voz_generate(modelo, texto):
    """Plan B: la llamada clásica (la que da el botón «Get code» de AI Studio)."""
    d = _post(f"{API}/models/{modelo}:generateContent", {
        "contents": [{"role": "user", "parts": [{"text": f"## Style:\n{ESTILO_VOZ}\n\n## Transcript:\n{texto}"}]}],
        "generationConfig": {"temperature": 1, "responseModalities": ["AUDIO"],
                             "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOZ}}}}})
    part = d["candidates"][0]["content"]["parts"][0]["inlineData"]
    pcm = base64.b64decode(part["data"])
    m = re.search(r"rate=(\d+)", part.get("mimeType", ""))
    return _wav_de_pcm(pcm, int(m.group(1)) if m else 24000)


def voz(texto):
    """Devuelve (wav en bytes, nombre del modelo). Lanza un error si no hay manera."""
    errores = []
    for modelo in MODELOS_VOZ:
        for forma in (_voz_interactions, _voz_generate):
            try:
                _esperar_cupo()
                return forma(modelo, texto), modelo
            except Exception as e:
                errores.append(f"{modelo}/{forma.__name__}: {str(e)[:200]}")
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    break  # cupo del día agotado en este modelo: probar el siguiente
    raise RuntimeError("Sin voz de Gemini: " + " | ".join(errores))
