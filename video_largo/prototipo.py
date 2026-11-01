"""Prototipo del vídeo largo de «Leónida al Día» (fase V-L3). 16:9, 1080p, unos 75 s.

Solo se lanza a mano y NO publica nada. Une: voz de Gemini (Orus, estilo relajado), trozos oficiales
(sin su sonido, salvo un momento con sonido original), música hecha con código que baja con la voz,
contador de curiosidad, subtítulos y rótulos. Deja el MP4 y una hoja de fotogramas en «salida_prototipo/».

Modo de prueba local: DRY=1 (sin Gemini ni descargas; usa imágenes de relleno).
"""
import base64
import csv
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

import numpy as np

DRY = os.environ.get("DRY") == "1"
CLAVE = os.environ.get("GEMINI_API_KEY", "").strip()
MODELO = os.environ.get("MODELO_TTS", "gemini-3.8-flash-lite-tts").strip()
VOZ = "Orus"
ESTILO = (
    "Relaxed, friendly Spanish gaming YouTuber telling a funny story to a friend. "
    "Native Castilian Spanish accent from Spain. Warm and close, light humour, natural pauses "
    "between sentences, lively but never rushed, never sounds like an advert or a radio announcer."
)
UA = "LeonidaAlDiaBot/1.0 (cuenta de fans de GTA 6) GitHubActions"
_V = "https://media-rockstargames-com.akamaized.net/VI/downloads/videos/"
VIDEOS = {
    "Mirada": "https://videos-rockstargames-com.akamaized.net/v4/rk721912/flv/es-es-1080p.mp4",
    "Trailer_1": _V + "GTAVI_Trailer_1/GTAVI_Trailer_1.mp4",
    "Trailer_2": _V + "GTAVI_Trailer_2/GTAVI_Trailer_2.mp4",
    "Lanzamiento": _V + "GTAVI_Launch_Trailer/GTAVI_Launch_Trailer.mp4",
}
W, H, FPS, SR = 1920, 1080, 30, 48000
AQUI = pathlib.Path(__file__).resolve().parent
TMP = pathlib.Path(os.environ.get("TMP_DIR", "tmp_proto"))
OUT = pathlib.Path("salida_prototipo")
VOCES = pathlib.Path(os.environ.get("CACHE_VOZ", "cache/voz"))
for d in (TMP, OUT, VOCES):
    d.mkdir(parents=True, exist_ok=True)

BLOQUES = [
    {
        "id": "hook", "num": None, "titulo": "",
        "overlay": "TIRAR LA BASURA = MEJOR REPUTACIÓN",
        "texto": ("Rockstar ha tardado trece años en hacer GTA 6. Trece. Y entre todo lo que han "
                  "metido, hay un detalle que me tiene obsesionado: en este juego puedes mejorar tu "
                  "reputación criminal... tirando la basura al contenedor. Sí. Has oído bien."),
        "planos": ["Lanz_Paseo", "Lanz_Descapotable", "T1_Autopista", "Mirada_Skyline_Azotea", "Lanz_Playa",
                   "T1_Neones", "Mirada_Autopista_1", "Lanz_Balcon", "T2_Jason_Conduce"],
    },
    {
        "id": "c10", "num": 10, "titulo": "EL PRIMER COCHE", "overlay": "",
        "texto": ("Número diez: el primer coche. En el Extended Look, el primero en el que se suben "
                  "Jason y Lucía es un descapotable alemán de los ochenta. Parece la versión de "
                  "Rockstar de un BMW Serie 3 clásico, aunque eso es suposición de la prensa: Rockstar "
                  "nunca pone marcas reales. Y por dentro, los coches tienen tanto detalle que "
                  "podrías pasar la ITV."),
        "planos": ["Mirada_Descapotable_1", "Mirada_Descapotable_2", "Mirada_Autopista_2",
                   "Mirada_Coche_Clasico", "Mirada_Calles_2", "Mirada_Furgoneta"],
    },
    {
        "id": "c12", "num": 12, "titulo": "CARRERAS", "overlay": "",
        "texto": ("Número doce: carreras. El Extended Look enseña una pista de asfalto, otra de tierra "
                  "y una carrera callejera que recuerda a Midnight Club, esa saga de carreras de "
                  "Rockstar que lleva siglos dormida. Suma motos de cross, motos de agua y lanchas, "
                  "y tienes el paraíso de cualquiera al que le guste hacer ruido."),
        "planos": ["Mirada_Moto_Calle", "Mirada_Motocross", "Mirada_Hidrodeslizador",
                   "Mirada_Mar_Atardecer", "Lanz_Moto_Salto", "T1_Lancha_Rapida"],
        "original": "Mirada_Carrera",
    },
]
TOTAL_CURIOSIDADES = 20
TEMPO_VOZ = float(os.environ.get("TEMPO_VOZ", "1.12"))  # más ritmo sin cambiar el tono
HQ = pathlib.Path("salida_hq")


def run(cmd, **kw):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError("Fallo de " + str(cmd[0]) + ": " + r.stderr[-1500:])
    return r


def trozos():
    ruta = AQUI / "trozos.csv"
    with open(ruta, encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    return {r["Trozo"]: {"ini": float(r["Inicio (s)"]), "dur": float(r["Duración (s)"]),
                         "video": (r.get("Vídeo") or "Mirada").strip(),
                         "lento": float(r.get("Lento") or 1)} for r in filas}


# ---------------------------------------------------------------- voz
def sintetizar(texto):
    clave = hashlib.sha1((MODELO + VOZ + ESTILO + texto).encode("utf-8")).hexdigest()[:16]
    destino = VOCES / (clave + ".wav")
    if destino.exists():
        print("  voz en caché", clave, flush=True)
        return destino
    if DRY:
        n = int(24000 * (len(texto) / 15.0))
        t = np.arange(n) / 24000
        env = (np.sin(2 * np.pi * 3.2 * t) > -0.3).astype(float)
        x = 0.3 * env * np.sin(2 * np.pi * 140 * t) + 0.05 * np.random.randn(n) * env
        pcm = (x * 32767).astype("<i2").tobytes()
        frec = 24000
    else:
        time.sleep(21)  # máximo 3 audios por minuto
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent"
        cuerpo = {
            "contents": [{"parts": [{"text": f"{ESTILO}\n\n{texto}"}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOZ}}}},
        }
        pet = urllib.request.Request(url, data=json.dumps(cuerpo).encode("utf-8"), method="POST",
                                     headers={"Content-Type": "application/json", "x-goog-api-key": CLAVE})
        with urllib.request.urlopen(pet, timeout=240) as resp:
            datos = json.loads(resp.read().decode("utf-8"))
        parte = datos["candidates"][0]["content"]["parts"][0]["inlineData"]
        frec = 24000
        m = re.search(r"rate=(\d+)", parte.get("mimeType", ""))
        if m:
            frec = int(m.group(1))
        pcm = base64.b64decode(parte["data"])
    with wave.open(str(destino), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(frec)
        f.writeframes(pcm)
    return destino


def leer_wav(ruta, tempo=1.0):
    """Lee un audio cualquiera como float32 estéreo a 48 kHz (lo pasa por ffmpeg)."""
    tmp = TMP / (pathlib.Path(ruta).stem + "_48k.wav")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", ruta, "-af", f"atempo={tempo}", "-ar", SR, "-ac", 2,
         "-c:a", "pcm_s16le", tmp])
    with wave.open(str(tmp), "rb") as f:
        datos = np.frombuffer(f.readframes(f.getnframes()), dtype="<i2").astype(np.float32) / 32768
    return datos.reshape(-1, 2)


# ---------------------------------------------------------------- subtítulos
def tiempos_palabras(ruta_wav, texto, dur):
    """Tiempo (inicio, fin) de cada palabra del guion. Whisper si está; si no, a prorrata por letras."""
    pal = texto.split()
    ws = []
    if os.environ.get("USAR_WHISPER") == "1":
        try:
            from faster_whisper import WhisperModel
            modelo = WhisperModel("base", device="cpu", compute_type="int8")
            segs, _ = modelo.transcribe(str(ruta_wav), language="es", word_timestamps=True)
            ws = [(w.start, w.end) for s in segs for w in (s.words or [])]
        except Exception as e:  # noqa: BLE001
            print("  Whisper no ha podido:", e, flush=True)
    if len(ws) >= max(3, len(pal) // 3):
        n_w, n_o = len(ws), len(pal)
        out = []
        for i in range(n_o):
            a = min(n_w - 1, int(i * n_w / n_o))
            b = min(n_w - 1, max(a, int((i + 1) * n_w / n_o) - 1))
            out.append((ws[a][0], ws[b][1]))
        return out, "Whisper"
    letras = [len(p) + 1 for p in pal]
    total = sum(letras)
    acum, out = 0, []
    for l in letras:
        out.append((dur * acum / total, dur * (acum + l) / total))
        acum += l
    return out, "a prorrata"


def tiempos_por_voz(audio, texto):
    """Tiempo de cada palabra según dónde suena la voz (salta los silencios y las pausas)."""
    x = audio.mean(axis=1)
    hop = SR // 100
    rms = np.sqrt(np.convolve(x ** 2, np.ones(hop) / hop, "same"))[::hop]
    act = rms > 0.06 * (rms.max() + 1e-9)
    segs, ini = [], None
    for i, a in enumerate(act):
        if a and ini is None:
            ini = i
        if not a and ini is not None:
            segs.append([ini / 100, i / 100])
            ini = None
    if ini is not None:
        segs.append([ini / 100, len(act) / 100])
    unidos = []
    for s in segs:
        if unidos and s[0] - unidos[-1][1] < 0.25:
            unidos[-1][1] = s[1]
        else:
            unidos.append(s)
    if not unidos:
        unidos = [[0.0, len(x) / SR]]
    total = sum(b - a for a, b in unidos)

    def real(seg):
        for a, b in unidos:
            if seg <= b - a:
                return a + seg
            seg -= b - a
        return unidos[-1][1]

    pal = texto.split()
    pesos = [len(p) + 1 for p in pal]
    suma, acum, out = sum(pesos), 0, []
    for p in pesos:
        out.append((real(total * acum / suma), real(total * (acum + p) / suma)))
        acum += p
    return out, "la voz (pausas)"


def trozos_de_subtitulo(pal, tiempos, ini):
    """Agrupa palabras en frases cortas de 2-4 palabras, cortando en la puntuación."""
    grupos, actual = [], []
    for i, p in enumerate(pal):
        actual.append(i)
        if len(actual) >= 4 or re.search(r"[.,:;?!…]$", p) and len(actual) >= 2:
            grupos.append(actual)
            actual = []
    if actual:
        grupos.append(actual)
    out = []
    for g in grupos:
        a = ini + tiempos[g[0]][0]
        b = ini + tiempos[g[-1]][1] + 0.06
        out.append((a, b, " ".join(pal[i] for i in g)))
    return out


def ass_t(t):
    t = max(0.0, t)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def escribir_ass(ruta, bloques, total):
    cab = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,DejaVu Sans,70,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,5,2,2,120,120,64,1
Style: Chip,DejaVu Sans,56,&H00FFFFFF,&H000000FF,&H00A34FFF,&H00000000,-1,0,0,0,100,100,0,0,3,16,0,7,60,0,50,1
Style: Titulo,DejaVu Sans,44,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,4,2,7,66,0,150,1
Style: Marca,DejaVu Sans,34,&H99FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,3,0,1,3,1,9,0,60,50,1
Style: Gancho,DejaVu Sans,104,&H00FFFFFF,&H000000FF,&H00A34FFF,&H00000000,-1,0,0,0,100,100,0,0,1,9,3,5,160,160,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = [f"Dialogue: 0,{ass_t(0)},{ass_t(total)},Marca,,0,0,0,,{{\\fad(400,400)}}LEÓNIDA AL DÍA"]
    for b in bloques:
        if b["num"]:
            ev.append(f"Dialogue: 0,{ass_t(b['ini'])},{ass_t(b['fin'])},Chip,,0,0,0,,"
                      f"{{\\fad(150,150)}}  {b['num']}/{TOTAL_CURIOSIDADES}  ")
            ev.append(f"Dialogue: 0,{ass_t(b['ini'])},{ass_t(b['fin'])},Titulo,,0,0,0,,"
                      f"{{\\fad(250,250)}}{b['titulo']}")
        if b["overlay"]:
            ev.append(f"Dialogue: 1,{ass_t(b['ini'] + 0.4)},{ass_t(b['ini'] + 3.6)},Gancho,,0,0,0,,"
                      f"{{\\fad(180,180)\\t(0,350,\\fscx108\\fscy108)}}{b['overlay']}")
        for a, z, txt in b["subs"]:
            ev.append(f"Dialogue: 0,{ass_t(a)},{ass_t(z)},Sub,,0,0,0,,{txt}")
    pathlib.Path(ruta).write_text(cab + "\n".join(ev) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- vídeo
def cortar_plano(nombre, t, dur, destino, sentido):
    """Corta un trozo en 16:9 a 1080p, con un ligero movimiento de cámara y sin sonido."""
    if DRY:
        fuente = ["-f", "lavfi", "-i", f"testsrc2=size=1920x1080:rate=30:duration={dur + 0.2}"]
        pre = []
    else:
        url = VIDEOS[t["video"]]
        fuente = ["-i", url]
        pre = ["-ss", f"{t['ini']:.2f}", "-t", f"{dur:.2f}", "-user_agent", UA,
               "-reconnect", "1", "-reconnect_on_network_error", "1", "-reconnect_delay_max", "10"]
    x = f"(in_w-out_w)*t/{dur:.3f}" if sentido == 0 else f"(in_w-out_w)*(1-t/{dur:.3f})"
    vf = f"scale=2112:1188:flags=lanczos,crop={W}:{H}:x='{x}':y='(in_h-out_h)/2',fps={FPS},format=yuv420p"
    for _ in range(3):
        try:
            run(["ffmpeg", "-y", "-loglevel", "error", *pre, *fuente, "-t", f"{dur:.2f}", "-an", "-vf", vf,
                 "-c:v", "libx264", "-crf", "17", "-preset", "veryfast", destino])
            return
        except RuntimeError as e:
            print("  reintento", nombre, str(e)[-200:], flush=True)
            time.sleep(3)
    raise RuntimeError("No se pudo cortar " + nombre)


def planificar(bloque, dur_visual, tabla):
    """Lista de (trozo, segundos) que cubre dur_visual, repitiendo trozos si hace falta."""
    lista, resto, i = [], dur_visual, 0
    nombres = bloque["planos"]
    while resto > 0.05 and i < 40:
        n = nombres[i % len(nombres)]
        d = min(tabla[n]["dur"], resto)
        if d < 0.7 and lista:
            lista[-1][1] += d  # un plano demasiado corto se suma al anterior (se alarga con la última imagen)
            lista[-1][2] = True
        else:
            lista.append([n, d, False])
        resto -= d
        i += 1
    return lista


def musica(dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    bpm = 104
    beat = 60 / bpm
    raices = [55.0, 43.65, 65.41, 49.0]
    acordes = [(220.0, 261.63, 329.63), (174.61, 220.0, 261.63), (261.63, 329.63, 392.0), (196.0, 246.94, 293.66)]
    mus = np.zeros(n)
    corchea = beat / 2
    for k in range(int(dur / corchea) + 1):
        a = int(k * corchea * SR)
        b = min(n, a + int(corchea * SR))
        if a >= n:
            break
        f = raices[(int(k * corchea / (4 * beat))) % 4]
        tt = np.arange(b - a) / SR
        saw = 2 * ((f * tt) % 1) - 1
        mus[a:b] += 0.30 * saw * np.exp(-tt * 7)
    for k in range(int(dur / (4 * beat)) + 1):
        a = int(k * 4 * beat * SR)
        b = min(n, int((k + 1) * 4 * beat * SR))
        if a >= n:
            break
        tt = np.arange(b - a) / SR
        pad = np.zeros(b - a)
        for f in acordes[k % 4]:
            for det in (0.995, 1.0, 1.005):
                pad += 2 * ((f * det * tt) % 1) - 1
        mus[a:b] += 0.05 * pad * np.minimum(1, tt * 4) * np.minimum(1, (4 * beat - tt) * 4)
    for k in range(int(dur / (beat / 4)) + 1):
        a = int(k * beat / 4 * SR)
        b = min(n, a + int(beat / 4 * SR))
        if a >= n:
            break
        f = acordes[(int(k * beat / 4 / (4 * beat))) % 4][k % 3] * 2
        tt = np.arange(b - a) / SR
        mus[a:b] += 0.05 * np.sign(np.sin(2 * np.pi * f * tt)) * np.exp(-tt * 14)
    for k in range(int(dur / beat) + 1):
        a = int(k * beat * SR)
        b = min(n, a + int(0.2 * SR))
        if a >= n:
            break
        tt = np.arange(b - a) / SR
        mus[a:b] += 0.55 * np.sin(2 * np.pi * (45 * tt + 75 * (1 - np.exp(-tt * 28)) / 28)) * np.exp(-tt * 14)
        a2 = int((k + 0.5) * beat * SR)
        b2 = min(n, a2 + int(0.05 * SR))
        if a2 < n:
            ruido = np.random.RandomState(k).randn(b2 - a2)
            mus[a2:b2] += 0.05 * np.diff(ruido, prepend=0) * np.exp(-np.arange(b2 - a2) / SR * 60)
    esp = np.fft.rfft(mus)
    frec = np.fft.rfftfreq(n, 1 / SR)
    esp *= 1 / (1 + (frec / 5500) ** 4)
    mus = np.fft.irfft(esp, n)
    mus /= np.max(np.abs(mus)) + 1e-9
    return (mus * 0.9).astype(np.float32)


def suavizar(env, tasa, ataque, relajo):
    out = np.zeros_like(env)
    v = 0.0
    ka = 1 - np.exp(-1 / (tasa * ataque))
    kr = 1 - np.exp(-1 / (tasa * relajo))
    for i, x in enumerate(env):
        v += (x - v) * (ka if x > v else kr)
        out[i] = v
    return out


def main():
    tabla = trozos()
    t0 = time.time()
    # 1) voz de cada bloque
    for b in BLOQUES:
        print("Voz de", b["id"], flush=True)
        b["wav"] = sintetizar(b["texto"])
        b["audio"] = leer_wav(b["wav"], TEMPO_VOZ)
        b["dur_voz"] = len(b["audio"]) / SR
        print(f"  {b['dur_voz']:.1f} s", flush=True)
    # 2) línea de tiempo
    t = 0.0
    hay_original = []
    for i, b in enumerate(BLOQUES):
        b["ini"] = t
        b["voz_ini"] = t + (0.15 if i == 0 else 0.35)
        b["voz_fin"] = b["voz_ini"] + b["dur_voz"]
        b["vis_fin"] = b["voz_fin"] + 0.4
        b["fin"] = b["vis_fin"]
        if b.get("original"):
            o = tabla[b["original"]]
            b["orig_ini"], b["orig_fin"] = b["vis_fin"], b["vis_fin"] + o["dur"]
            b["fin"] = b["orig_fin"]
            hay_original.append(b)
        t = b["fin"]
    total = t + 0.6
    # 3) planos
    carpeta = TMP / "planos"
    carpeta.mkdir(exist_ok=True)
    lista_concat, k = [], 0
    for b in BLOQUES:
        plan = planificar(b, b["vis_fin"] - b["ini"], tabla)
        b["plan"] = plan
        for nombre, dur, alargar in plan:
            k += 1
            destino = str(carpeta / f"{k:02d}_{nombre}.mp4")
            cortar_plano(nombre, tabla[nombre], dur, destino, k % 2)
            lista_concat.append(destino)
        if b.get("original"):
            k += 1
            o = tabla[b["original"]]
            destino = str(carpeta / f"{k:02d}_{b['original']}.mp4")
            cortar_plano(b["original"], o, o["dur"], destino, 0)
            lista_concat.append(destino)
            if not DRY:
                b["orig_wav"] = TMP / "original.wav"
                run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{o['ini']:.2f}", "-t", f"{o['dur']:.2f}",
                     "-user_agent", UA, "-i", VIDEOS[o["video"]], "-vn", "-ar", SR, "-ac", 2,
                     "-c:a", "pcm_s16le", b["orig_wav"]])
    (TMP / "lista.txt").write_text("".join(f"file '{pathlib.Path(p).resolve()}'\n" for p in lista_concat))
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", TMP / "lista.txt",
         "-c", "copy", TMP / "sin_audio.mp4"])
    # 4) subtítulos y rótulos
    for b in BLOQUES:
        pal = b["texto"].split()
        tiempos, metodo = tiempos_por_voz(b["audio"], b["texto"])
        b["subs"] = trozos_de_subtitulo(pal, tiempos, b["voz_ini"])
        b["metodo"] = metodo
    escribir_ass(TMP / "rotulos.ass", BLOQUES, total)
    # 5) audio: voz + música que baja con la voz + sonido original
    n = int(total * SR)
    voz = np.zeros((n, 2), np.float32)
    for b in BLOQUES:
        a = b["audio"]
        a = a / (np.max(np.abs(a)) + 1e-9) * 0.9
        i0 = int(b["voz_ini"] * SR)
        voz[i0:i0 + len(a)] += a[: n - i0]
    mus = musica(total + 1)[:n]
    hop = SR // 50
    rms = np.sqrt(np.convolve((voz.mean(axis=1)) ** 2, np.ones(hop) / hop, "same"))[::hop]
    habla = (rms > 0.02).astype(float)
    habla = suavizar(habla, 50, 0.06, 0.5)
    habla_m = np.interp(np.arange(n) / SR, np.arange(len(habla)) / 50, habla)
    ganancia = 0.30 - (0.30 - 0.085) * habla_m
    ganancia *= np.minimum(1, np.arange(n) / SR / 1.0) * np.minimum(1, (total - np.arange(n) / SR) / 1.5)
    orig = np.zeros((n, 2), np.float32)
    silencio = np.ones(n)
    for b in hay_original:
        i0, i1 = int(b["orig_ini"] * SR), int(b["orig_fin"] * SR)
        silencio[i0:i1] = 0
        if "orig_wav" in b:
            o = leer_wav(b["orig_wav"])
            orig[i0:i0 + len(o)] += o[: n - i0] * 0.95
    silencio = suavizar(silencio, SR, 0.02, 0.04)
    mezcla = voz + (mus * ganancia * silencio)[:, None] + orig
    mezcla = np.clip(mezcla, -1, 1)
    with wave.open(str(TMP / "mezcla.wav"), "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes((mezcla * 32767).astype("<i2").tobytes())
    # 6) montaje final
    HQ.mkdir(exist_ok=True)
    final = HQ / "prototipo_hq.mp4"
    vf = f"ass={TMP / 'rotulos.ass'}"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", TMP / "sin_audio.mp4", "-i", TMP / "mezcla.wav",
         "-vf", vf, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:v", "libx264", "-crf", "21",
         "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", SR,
         "-shortest", "-movflags", "+faststart", final])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", final, "-vf", "scale=1280:720", "-c:v", "libx264",
         "-crf", "27", "-preset", "veryfast", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
         OUT / "prototipo.mp4"])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", final, "-vf", "fps=1/3,scale=480:-1,tile=5x4",
         "-frames:v", "1", "-q:v", "3", OUT / "hoja.jpg"])
    dur = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", final]).stdout)
    informe = [f"Voz: {VOZ} ({MODELO})", f"Duración: {dur:.1f} s", f"Tamaño: {final.stat().st_size / 1e6:.1f} MB (alta calidad), {(OUT / 'prototipo.mp4').stat().st_size / 1e6:.1f} MB (revisión)",
               f"Tiempo de montaje: {time.time() - t0:.0f} s", ""]
    for b in BLOQUES:
        informe.append(f"{b['id']}: voz {b['dur_voz']:.1f} s, {len(b['plan'])} planos, "
                       f"subtítulos por {b['metodo']}" + (", con sonido original" if b.get("original") else ""))
    texto = "\n".join(informe)
    (OUT / "informe.txt").write_text(texto, encoding="utf-8")
    print(texto)
    resumen = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumen:
        with open(resumen, "a", encoding="utf-8") as f:
            f.write("### Prototipo del vídeo largo\n\n" + texto.replace("\n", "  \n") + "\n")


if __name__ == "__main__":
    main()
