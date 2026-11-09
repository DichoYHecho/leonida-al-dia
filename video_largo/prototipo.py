"""Prototipo del vídeo largo de «Leónida al Día» (fase V-L3). 16:9, 1080p.

Solo se lanza a mano y NO publica nada. Une: voz de Gemini (Orus, estilo relajado), trozos oficiales
en 4K (sin su sonido, salvo un momento con sonido original), música hecha con código que baja con la voz,
contador de curiosidad, subtítulos palabra a palabra (Whisper) y rótulos. Deja el MP4 de revisión y una hoja
de fotogramas en «salida_prototipo/» y el MP4 de alta calidad en «salida_hq/».

Modo de prueba local: DRY=1 (sin Gemini ni descargas; usa imágenes de relleno).
"""
import base64
import csv
import difflib
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.request
import wave

import numpy as np

DRY = os.environ.get("DRY") == "1"
SOLO_AUDIO = os.environ.get("SOLO_AUDIO") == "si"  # prueba rápida: solo la mezcla de audio, sin vídeo
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
    # «Una mirada extendida» existe en 4K (2160p): de ahí salen los planos y el sonido original
    "Mirada": "https://videos-rockstargames-com.akamaized.net/v4/rk721912/flv/es-es-2160p.mp4",
    "Trailer_1": _V + "GTAVI_Trailer_1/GTAVI_Trailer_1.mp4",
    "Trailer_2": _V + "GTAVI_Trailer_2/GTAVI_Trailer_2.mp4",
    "Lanzamiento": _V + "GTAVI_Launch_Trailer/GTAVI_Launch_Trailer.mp4",
}
W, H, FPS, SR = 1920, 1080, 30, 48000
AQUI = pathlib.Path(__file__).resolve().parent
TMP = pathlib.Path(os.environ.get("TMP_DIR", "tmp_proto"))
OUT = pathlib.Path("salida_prototipo")
HQ = pathlib.Path("salida_hq")
VOCES = pathlib.Path(os.environ.get("CACHE_VOZ", "cache/voz"))
for d in (TMP, OUT, VOCES):
    d.mkdir(parents=True, exist_ok=True)

BLOQUES = [
    {
        "id": "hook", "num": None, "titulo": "",
        "overlay": "TIRAR LA BASURA|= MEJOR REPUTACIÓN",
        "texto": ("Rockstar ha tardado trece años en hacer GTA 6. Trece. Y entre todo lo que han "
                  "metido, hay un detalle que me tiene obsesionado: en este juego puedes mejorar tu "
                  "reputación criminal... tirando la basura al contenedor. Sí. Has oído bien."),
        "planos": ["Lanz_Paseo", "Lanz_Descapotable", "T1_Autopista", "Mirada_Skyline_Azotea", "Lanz_Playa",
                   "T1_Neones", "Mirada_Autopista_1", "Lanz_Balcon", "T2_Jason_Conduce",
                   "Mirada_Descapotable_1", "Lanz_Moto_Salto", "Mirada_Calles_2", "T1_Coches_Noche"],
    },
    {
        "id": "c1", "num": 1, "titulo": "EL HERMANO MAYOR", "overlay": "",
        "texto": ("Curiosidad número uno. Para entender GTA 6 hay que mirar a su hermano mayor. GTA 5 hizo "
                  "más de 800 millones de dólares en su primer día. En un día. Y mil millones en solo "
                  "tres, algo que ninguna película ni ningún juego había conseguido tan rápido: Avatar, "
                  "por ejemplo, tardó 17 días. Hoy GTA 5 ha vendido más de 230 millones de copias. "
                  "Y GTA 6 tiene que superar eso. Ni presión ni nada."),
        "planos": ["Mirada_Vista_Aerea", "T1_Playa_Aerea", "Lanz_Cartel_Keys", "Mirada_Atardecer",
                   "T1_Noche_Aerea", "Mirada_Puerto", "T1_Letras_Vice", "Mirada_Skyline_Azotea",
                   "Mirada_Autopista_2", "T1_Neones"],
    },
    {
        "id": "c2", "num": 2, "titulo": "TRECE AÑOS", "overlay": "",
        "texto": ("Número dos: trece años de espera. GTA 5 salió en septiembre de 2013. GTA 6 sale en "
                  "noviembre de 2026. Hay gente que ha nacido, ha empezado el colegio y se ha sacado el "
                  "carné de conducir mientras esperábamos. Por el camino se retrasó dos veces: iba a "
                  "salir en 2025, luego el 26 de mayo de 2026, y al final: el 19 de noviembre. "
                  "El 26 de mayo, por cierto, Rockstar no dijo ni mu, y los fans se cabrearon bastante."),
        "planos": ["T2_Mar_Atardecer", "Lanz_Marina", "Mirada_Playa", "T2_Cayos_Aereo", "Mirada_Paracaidas",
                   "T2_Gimnasio_Playa", "T1_Puente_Cayos", "Mirada_Moto_Calle", "T2_Casa_Pilotes",
                   "Mirada_Skyline_Noche"],
        "original": "Mirada_Skyline_Noche",
    },
]
TOTAL_CURIOSIDADES = 20
TEMPO_VOZ = float(os.environ.get("TEMPO_VOZ", "1.12"))  # más ritmo sin cambiar el tono
ACENTO = "&HA34FFF&"  # rosa de la marca (ASS usa el orden azul-verde-rojo)
ALTO_DEGRADADO = 380  # franja oscura suave abajo, para que se lean bien los subtítulos
CARPETA_FUENTES = "/usr/share/fonts/truetype/montserrat/"


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
def pedir_voz(texto):
    """Pide el audio a Gemini. El estilo va en su apartado («## Style»), para que NO se lea en voz alta."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent"
    cuerpo = {
        "contents": [{"role": "user", "parts": [{"text": f"## Style:\n{ESTILO}\n\n## Transcript:\n{texto}"}]}],
        "generationConfig": {"temperature": 1, "responseModalities": ["AUDIO"],
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
    return base64.b64decode(parte["data"]), frec


def guardar_pcm(destino, pcm, frec):
    with wave.open(str(destino), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(frec)
        f.writeframes(pcm)


def sintetizar(texto):
    base = MODELO + VOZ + ESTILO + texto
    nueva = VOCES / (hashlib.sha1(("v2" + base).encode("utf-8")).hexdigest()[:16] + ".wav")
    vieja = VOCES / (hashlib.sha1(base.encode("utf-8")).hexdigest()[:16] + ".wav")  # la que leía el estilo en inglés
    if nueva.exists():
        print("  voz en caché", nueva.stem, flush=True)
        return nueva
    if DRY:
        n = int(24000 * (len(texto) / 15.0))
        t = np.arange(n) / 24000
        env = (np.sin(2 * np.pi * 3.2 * t) > -0.3).astype(float)
        x = 0.3 * env * np.sin(2 * np.pi * 140 * t) + 0.05 * np.random.randn(n) * env
        guardar_pcm(nueva, (x * 32767).astype("<i2").tobytes(), 24000)
        return nueva
    try:
        time.sleep(21)  # máximo 3 audios por minuto
        pcm, frec = pedir_voz(texto)
        guardar_pcm(nueva, pcm, frec)
        print("  voz nueva pedida a Gemini", nueva.stem, flush=True)
        return nueva
    except Exception as e:  # noqa: BLE001
        if vieja.exists():
            print("  no se ha podido pedir la voz nueva (", str(e)[:120], "): se usa la anterior y se le quita el principio", flush=True)
            return vieja
        raise


def leer_wav(ruta, tempo=1.0):
    """Lee un audio cualquiera como float32 estéreo a 48 kHz (lo pasa por ffmpeg)."""
    tmp = TMP / (pathlib.Path(ruta).stem + "_48k.wav")
    filtro = f"highpass=f=90,atempo={tempo}" if tempo != 1.0 else "anull"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", ruta, "-af", filtro, "-ar", SR, "-ac", 2,
         "-c:a", "pcm_s16le", tmp])
    with wave.open(str(tmp), "rb") as f:
        datos = np.frombuffer(f.readframes(f.getnframes()), dtype="<i2").astype(np.float32) / 32768
    return datos.reshape(-1, 2)


def fundir(x, entrada, salida):
    """Fundido de entrada y de salida (en segundos) a un audio estéreo: evita chasquidos en los cortes."""
    n = len(x)
    ne, ns = min(int(entrada * SR), n // 2), min(int(salida * SR), n // 2)
    if ne:
        x[:ne] *= (0.5 - 0.5 * np.cos(np.linspace(0, np.pi, ne)))[:, None]
    if ns:
        x[-ns:] *= (0.5 + 0.5 * np.cos(np.linspace(0, np.pi, ns)))[:, None]
    return x


def limpiar_voz(a):
    """Quita el ruido y el chasquido del principio y del final de cada audio de voz y suaviza los bordes.
    Devuelve (audio, segundos quitados del principio)."""
    a = a - a.mean(axis=0, keepdims=True)
    m = a.mean(axis=1)
    hop = SR // 100
    rms = np.sqrt(np.convolve(m ** 2, np.ones(hop) / hop, "same"))[::hop]
    act = rms > 0.06 * (rms.max() + 1e-9)
    tramos, i = [], 0
    while i < len(act):
        if act[i]:
            j = i
            while j < len(act) and act[j]:
                j += 1
            tramos.append((i, j))
            i = j
        else:
            i += 1
    largos = [t for t in tramos if t[1] - t[0] >= 10]  # solo cuenta lo que dura 100 ms o más (un chasquido corto no es voz)
    if not largos:
        return a, 0.0
    ini = max(0, int((largos[0][0] * 0.01 - 0.03) * SR))
    fin = min(len(a), int((largos[-1][1] * 0.01 + 0.15) * SR))
    return fundir(a[ini:fin].copy(), 0.03, 0.15), ini / SR


# ---------------------------------------------------------------- Whisper y tiempos de las palabras
def audio_16k(ruta):
    """Audio mono a 16 kHz como lista de números (así lo pide Whisper; evita PyAV, que daba error)."""
    r = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(ruta), "-ar", "16000", "-ac", "1",
                        "-f", "s16le", "pipe:1"], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode("utf-8", "ignore")[-300:])
    return np.frombuffer(r.stdout, dtype="<i2").astype(np.float32) / 32768


def modelo_whisper():
    """Baja el modelo de Whisper directamente (sin la librería de Hugging Face)."""
    d = pathlib.Path(os.environ.get("CACHE_WHISPER", "cache/whisper-base"))
    d.mkdir(parents=True, exist_ok=True)
    base = "https://huggingface.co/Systran/faster-whisper-base/resolve/main/"
    for nombre, obligatorio in (("config.json", True), ("tokenizer.json", True), ("model.bin", True),
                                ("vocabulary.txt", False)):
        destino = d / nombre
        if destino.exists() and destino.stat().st_size > 0:
            continue
        try:
            pet = urllib.request.Request(base + nombre, headers={"User-Agent": UA})
            with urllib.request.urlopen(pet, timeout=900) as r, open(destino, "wb") as f:
                while True:
                    bloque = r.read(1 << 20)
                    if not bloque:
                        break
                    f.write(bloque)
        except Exception:
            if destino.exists():
                destino.unlink()
            if obligatorio:
                raise
    return str(d)


_WHISPER = []


def palabras_whisper(ruta):
    """[(palabra, inicio, fin)] de lo que oye Whisper; [] si no puede."""
    if DRY or os.environ.get("USAR_WHISPER", "1") != "1":
        return []
    try:
        if not _WHISPER:
            from faster_whisper import WhisperModel
            _WHISPER.append(WhisperModel(modelo_whisper(), device="cpu", compute_type="int8"))
        segs, _ = _WHISPER[0].transcribe(audio_16k(ruta), language="es", word_timestamps=True)
        return [(w.word, w.start, w.end) for s in segs for w in (s.words or [])]
    except Exception as e:  # noqa: BLE001
        print("  Whisper no ha podido:", type(e).__name__, e, flush=True)
        return []


def normalizar(p):
    p = unicodedata.normalize("NFD", p.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in p if unicodedata.category(c) != "Mn"))


def inicio_guion(pal, ws):
    """Segundo en el que empieza el guion de verdad (por si la voz arranca diciendo otra cosa antes)."""
    if not ws:
        return 0.0
    a = [normalizar(w[0]) for w in ws]
    b = [normalizar(p) for p in pal]
    for i, j, n in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        if n >= 2 or (n >= 1 and j < 3):
            antes = sum(len(p) + 1 for p in pal[:j]) * 0.075
            return max(0.0, ws[i][1] - antes - 0.12)
    return 0.0


def fin_guion(pal, ws):
    """Segundo en el que acaba la última palabra del guion según Whisper (None si no se puede saber)."""
    if not ws:
        return None
    oidas = [normalizar(w[0]) for w in ws]
    for atras, margen in ((1, 0.0), (2, 0.45)):
        if len(pal) < atras:
            break
        buscada = normalizar(pal[-atras])
        if len(buscada) < 3:
            continue
        for i in range(len(ws) - 1, -1, -1):
            if oidas[i] == buscada:
                return ws[i][2] + margen
    return None


def alinear(pal, ws, dur):
    """Pone a cada palabra del guion el tiempo de la misma palabra en lo que ha oído Whisper
    (ws = [(texto, inicio, fin)]); las que no coinciden se reparten entre las vecinas."""
    a = [normalizar(w[0]) for w in ws]
    b = [normalizar(p) for p in pal]
    t = [None] * len(pal)
    for i, j, n in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(n):
            t[j + k] = (ws[i + k][1], ws[i + k][2])
    if sum(x is not None for x in t) < 0.4 * len(pal):
        return None
    i = 0
    while i < len(t):
        if t[i] is not None:
            i += 1
            continue
        j = i
        while j < len(t) and t[j] is None:
            j += 1
        ini = t[i - 1][1] if i > 0 else 0.0
        fin = t[j][0] if j < len(t) else dur
        fin = max(fin, ini + 0.05 * (j - i))
        pesos = [len(p) + 1 for p in pal[i:j]]
        acum = 0
        for k in range(i, j):
            p = pesos[k - i]
            t[k] = (ini + (fin - ini) * acum / sum(pesos), ini + (fin - ini) * (acum + p) / sum(pesos))
            acum += p
        i = j
    return t


def tiempos_por_voz(audio, texto):
    """Plan B sin Whisper: tiempo de cada palabra según dónde suena la voz (salta las pausas)."""
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
    return out


def frases_de_subtitulo(pal, tiempos, ini):
    """Agrupa las palabras en frases cortas de 2-5 palabras (cortando en la puntuación).
    Cada frase es una lista de (palabra, inicio, fin) ya con el desfase del bloque."""
    grupos, actual = [], []
    for i, p in enumerate(pal):
        actual.append(i)
        if len(actual) >= 5 or (re.search(r"[.,:;?!…]$", p) and len(actual) >= 2):
            grupos.append(actual)
            actual = []
    if actual:
        if grupos and len(actual) == 1:
            grupos[-1] += actual
        else:
            grupos.append(actual)
    return [[(pal[i], ini + tiempos[i][0], ini + tiempos[i][1]) for i in g] for g in grupos]


# ---------------------------------------------------------------- rótulos y subtítulos (ASS)
def ass_t(t):
    t = max(0.0, t)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def limpiar(txt):
    return txt.replace("{", "(").replace("}", ")")


def armar(palabras, corte, activa=None):
    """Texto de una frase de subtítulo; la palabra «activa» (la que suena) va en rosa."""
    partes = []
    for i, pw in enumerate(palabras):
        partes.append(f"{{\\c{ACENTO}}}{pw}{{\\c&HFFFFFF&}}" if i == activa else pw)
        if i + 1 < len(palabras):
            partes.append("\\N" if corte is not None and i + 1 == corte else " ")
    return "".join(partes)


def escribir_ass(ruta, bloques, total):
    cab = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Montserrat ExtraBold,60,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,5,0,2,220,220,92,1
Style: SubSombra,Montserrat ExtraBold,60,&H00000000,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,12,0,2,220,220,86,1
Style: Num,Montserrat Black,132,&H00A34FFF,&H000000FF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,0,4,7,0,0,0,1
Style: Total,Montserrat ExtraBold,46,&H99FFFFFF,&H000000FF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,0,3,7,0,0,0,1
Style: Titulo,Bebas Neue Bold,74,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,0,0,0,0,100,100,5,0,1,0,3,7,0,0,0,1
Style: Gancho,Montserrat Black,112,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,9,4,5,0,0,0,1
Style: Marca,Montserrat Black,40,&H00FFFFFF,&H000000FF,&H00000000,&H96000000,0,0,0,0,100,100,3,0,1,0,3,9,0,56,44,1
Style: Dibujo,Montserrat Black,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = [f"Dialogue: 1,{ass_t(0)},{ass_t(total)},Marca,,0,0,0,,{{\\fad(600,600)}}LEÓNIDA {{\\c{ACENTO}}}AL DÍA"]
    for b in bloques:
        a, z = ass_t(b["ini"]), ass_t(b["fin"])
        if b["num"]:
            ev.append(f"Dialogue: 1,{a},{z},Num,,0,0,0,,{{\\move(30,26,70,26,0,350)\\fad(250,250)}}{b['num'] if isinstance(b['num'], str) else format(b['num'], '02d')}")
            ev.append(f"Dialogue: 1,{a},{z},Total,,0,0,0,,{{\\pos(196,100)\\fad(400,250)}}/{b.get('total', TOTAL_CURIOSIDADES)}")
            ev.append(f"Dialogue: 1,{a},{z},Dibujo,,0,0,0,,{{\\pos(76,170)\\c{ACENTO}\\p1\\fad(350,250)"
                      f"\\t(0,450,\\fscx100)}}m 0 0 l 96 0 96 7 0 7")
            ev.append(f"Dialogue: 1,{a},{z},Titulo,,0,0,0,,{{\\move(40,184,76,184,0,350)\\fad(350,250)}}"
                      f"{limpiar(b['titulo'])}")
        if b["overlay"]:
            l1, l2 = (b["overlay"].split("|") + [""])[:2]
            ev.append(f"Dialogue: 2,{ass_t(b['ini'] + 0.4)},{ass_t(b['ini'] + 3.7)},Gancho,,0,0,0,,"
                      f"{{\\an5\\pos(960,470)\\fad(150,220)\\fscx72\\fscy72\\t(0,280,\\fscx100\\fscy100)}}"
                      f"{limpiar(l1)}\\N{{\\c{ACENTO}}}{limpiar(l2)}")
        for frase in b["subs"]:
            palabras = [limpiar(w) for w, _, _ in frase]
            largo = sum(len(w) + 1 for w in palabras)
            corte = None
            if largo > 30 and len(palabras) >= 3:
                acum = 0
                for i, w in enumerate(palabras):
                    acum += len(w) + 1
                    if acum >= largo / 2:
                        corte = i + 1
                        break
            for k, (w, ini, fin) in enumerate(frase):
                sig = frase[k + 1][1] if k + 1 < len(frase) else fin + 0.12
                fin_k = min(sig, fin + 0.45) if k + 1 < len(frase) else sig
                entra, sale = (90 if k == 0 else 0), (130 if k + 1 == len(frase) else 0)
                fund = f"\\fad({entra},{sale})" if entra or sale else ""
                ev.append(f"Dialogue: 0,{ass_t(ini)},{ass_t(fin_k)},SubSombra,,0,0,0,,"
                          f"{{\\blur16\\alpha&H70&{fund}}}{armar(palabras, corte)}")
                ev.append(f"Dialogue: 1,{ass_t(ini)},{ass_t(fin_k)},Sub,,0,0,0,,"
                          f"{{\\blur1.2{fund}}}{armar(palabras, corte, k)}")
    pathlib.Path(ruta).write_text(cab + "\n".join(ev) + "\n", encoding="utf-8")


def crear_degradado(ruta):
    """Franja oscura suave en la parte de abajo (transparente arriba): da profesionalidad y ayuda a leer."""
    from PIL import Image
    alfa = (np.linspace(0, 1, ALTO_DEGRADADO) ** 1.7 * 165).astype(np.uint8)
    arr = np.zeros((ALTO_DEGRADADO, W, 4), np.uint8)
    arr[..., 3] = alfa[:, None]
    Image.fromarray(arr, "RGBA").save(ruta)


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
                 "-c:v", "libx264", "-crf", "12", "-preset", "veryfast", destino])
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
            lista[-1][1] += d  # un plano demasiado corto se suma al anterior
            lista[-1][2] = True
        else:
            lista.append([n, d, False])
        resto -= d
        i += 1
    return lista


def musica(dur):
    n = int(dur * SR)
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
    # 1) voz de cada bloque (quitando lo que diga antes del guion, si lo hay) y palabras de Whisper
    for b in BLOQUES:
        print("Voz de", b["id"], flush=True)
        b["wav"] = sintetizar(b.get("voz", b["texto"]))
        b["wav48"] = TMP / (pathlib.Path(b["wav"]).stem + "_48k.wav")
        b["audio"] = leer_wav(b["wav"], TEMPO_VOZ)
        pal = b["texto"].split()
        ws = palabras_whisper(b["wav48"])
        rec = inicio_guion(pal, ws)
        b["recorte"] = rec if rec > 0.4 else 0.0
        if b["recorte"]:
            print(f"  se quitan los primeros {b['recorte']:.1f} s (no son del guion)", flush=True)
            b["audio"] = b["audio"][int(b["recorte"] * SR):]
            ws = [(w, a - b["recorte"], e - b["recorte"]) for w, a, e in ws if e > b["recorte"]]
        dur_antes = len(b["audio"]) / SR
        cola = [round(float(np.sqrt(np.mean(b["audio"][max(0, len(b["audio"]) - int((q + 1) * 0.1 * SR)):
                                                      len(b["audio"]) - int(q * 0.1 * SR)].mean(axis=1) ** 2))), 3)
                for q in range(8)]
        fin_g = fin_guion(pal, ws)
        b["cola_cortada"] = 0.0
        if fin_g is not None and fin_g + 0.3 < dur_antes:
            b["cola_cortada"] = dur_antes - (fin_g + 0.18)
            b["audio"] = b["audio"][: int((fin_g + 0.18) * SR)]
            print(f"  se quitan {b['cola_cortada']:.2f} s del final (después de la última palabra)", flush=True)
        b["cola"] = cola
        print("  final de la voz (RMS cada 100 ms, hacia atrás):", cola, flush=True)
        b["audio"], desfase = limpiar_voz(b["audio"])
        ws = [(w, a - desfase, e - desfase) for w, a, e in ws]
        b["ws"] = ws
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
            if SOLO_AUDIO:
                break
            k += 1
            destino = str(carpeta / f"{k:02d}_{nombre}.mp4")
            cortar_plano(nombre, tabla[nombre], dur, destino, k % 2)
            lista_concat.append(destino)
        if b.get("original"):
            k += 1
            o = tabla[b["original"]]
            destino = str(carpeta / f"{k:02d}_{b['original']}.mp4")
            if not SOLO_AUDIO:
                cortar_plano(b["original"], o, o["dur"], destino, 0)
                lista_concat.append(destino)
            if not DRY:
                b["orig_wav"] = TMP / "original.wav"
                run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{o['ini']:.2f}", "-t", f"{o['dur']:.2f}",
                     "-user_agent", UA, "-i", VIDEOS[o["video"]], "-vn", "-ar", SR, "-ac", 2,
                     "-c:a", "pcm_s16le", b["orig_wav"]])
    if not SOLO_AUDIO:
        (TMP / "lista.txt").write_text("".join(f"file '{pathlib.Path(p).resolve()}'\n" for p in lista_concat))
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", TMP / "lista.txt",
             "-c", "copy", TMP / "sin_audio.mp4"])
    # 4) subtítulos y rótulos
    for b in BLOQUES:
        pal = b["texto"].split()
        tiempos = alinear(pal, b["ws"], b["dur_voz"]) if b["ws"] else None
        b["metodo"] = "Whisper"
        if not tiempos:
            tiempos, b["metodo"] = tiempos_por_voz(b["audio"], b["texto"]), "la voz (pausas)"
        b["subs"] = frases_de_subtitulo(pal, tiempos, b["voz_ini"])
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
            o = fundir(leer_wav(b["orig_wav"]), 0.06, 0.15)
            orig[i0:i0 + len(o)] += o[: n - i0] * 0.95
    silencio = suavizar(silencio, SR, 0.02, 0.04)
    mezcla = voz + (mus * ganancia * silencio)[:, None] + orig
    mezcla = np.clip(mezcla, -1, 1)
    with wave.open(str(TMP / "mezcla.wav"), "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes((mezcla * 32767).astype("<i2").tobytes())
    with wave.open(str(TMP / "solo_voz.wav"), "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes((np.clip(voz, -1, 1) * 32767).astype("<i2").tobytes())
    for nombre_wav, nombre_png in (("mezcla.wav", "espectro_mezcla.png"), ("solo_voz.wav", "espectro_voz.png")):
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", TMP / nombre_wav, "-lavfi",
             "showspectrumpic=s=1920x600:legend=1:scale=log", "-frames:v", "1", OUT / nombre_png])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", TMP / "mezcla.wav", "-codec:a", "libmp3lame", "-q:a", "3",
         OUT / "audio.mp3"])
    if SOLO_AUDIO:
        informe = [f"PRUEBA SOLO AUDIO ({total:.1f} s)", ""]
        for b in BLOQUES:
            informe.append(f"{b['id']}: voz {b['dur_voz']:.2f} s, de {b['voz_ini']:.2f} s a {b['voz_fin']:.2f} s"
                           + (f"; se quitaron {b['cola_cortada']:.2f} s del final" if b["cola_cortada"] else "")
                           + f"; final (RMS/100 ms): {b['cola']}")
        (OUT / "informe.txt").write_text("\n".join(informe), encoding="utf-8")
        print("\n".join(informe))
        resumen = os.environ.get("GITHUB_STEP_SUMMARY")
        if resumen:
            with open(resumen, "a", encoding="utf-8") as f:
                f.write("### Prueba solo de audio\n\n" + "\n".join(informe).replace("\n", "  \n") + "\n")
        return
    # 6) montaje final: ligero ajuste de color y nitidez, y encima los rótulos
    HQ.mkdir(exist_ok=True)
    final = HQ / "prototipo_hq.mp4"
    crear_degradado(TMP / "degradado.png")
    grafo = (f"[0:v]eq=contrast=1.04:saturation=1.08,unsharp=5:5:0.4:5:5:0.0[v0];"
             f"[2:v]format=rgba[g];[v0][g]overlay=0:{H - ALTO_DEGRADADO}:shortest=1[v1];"
             f"[v1]ass={TMP / 'rotulos.ass'}[v]")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", TMP / "sin_audio.mp4", "-i", TMP / "mezcla.wav",
         "-loop", "1", "-framerate", FPS, "-i", TMP / "degradado.png",
         "-filter_complex", grafo, "-map", "[v]", "-map", "1:a", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
         "-c:v", "libx264", "-crf", "17",
         "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", SR,
         "-shortest", "-movflags", "+faststart", final])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", final, "-c:v", "libx264", "-crf", "23", "-maxrate", "7M",
         "-bufsize", "14M", "-preset", "fast", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
         OUT / "prototipo.mp4"])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", final, "-vf", "fps=1/3,scale=480:-1,tile=5x4",
         "-frames:v", "1", "-q:v", "3", OUT / "hoja.jpg"])
    dur = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", final]).stdout)
    informe = [f"Voz: {VOZ} ({MODELO})", f"Duración: {dur:.1f} s",
               f"Tamaño: {final.stat().st_size / 1e6:.1f} MB (alta calidad), "
               f"{(OUT / 'prototipo.mp4').stat().st_size / 1e6:.1f} MB (revisión)",
               f"Tiempo de montaje: {time.time() - t0:.0f} s", ""]
    for b in BLOQUES:
        informe.append(f"{b['id']}: voz {b['dur_voz']:.1f} s"
                       + (f" (se quitaron {b['recorte']:.1f} s del principio)" if b["recorte"] else "")
                       + (f" (se quitaron {b['cola_cortada']:.2f} s del final)" if b["cola_cortada"] else "")
                       + f", {len(b['plan'])} planos, subtítulos por {b['metodo']}"
                       + (", con sonido original" if b.get("original") else ""))
    texto = "\n".join(informe)
    (OUT / "informe.txt").write_text(texto, encoding="utf-8")
    print(texto)
    resumen = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumen:
        with open(resumen, "a", encoding="utf-8") as f:
            f.write("### Prototipo del vídeo largo\n\n" + texto.replace("\n", "  \n") + "\n")


if __name__ == "__main__":
    main()
