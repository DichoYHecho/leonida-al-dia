"""Voz del vídeo y tiempos de los subtítulos.

- Principal: Gemini, con la voz y el estilo de config.py (desde el 9 nov, Orus, la de los vídeos largos, a +12 %),
  un solo audio con todo el guion (1 petición por vídeo).
  Los subtítulos se sincronizan con Whisper (palabra a palabra); si falla, por las pausas de la voz.
- Reserva: Piper «sharvard» (voz natural española, CC BY 3.0), trozo a trozo, con tiempos exactos."""
import difflib, json, os, re, subprocess, unicodedata
import numpy as np, soundfile as sf
import gemini
from config import VOZ, VELOCIDAD_VOZ

SR = 24000
MODELOS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "modelos")
PIPER = "vits-piper-es_ES-sharvard-medium"
# 2 nov: parte del guion que Whisper tiene que reconocer en la voz de Gemini. Si es menos, la voz se ha ido
# del texto (por ejemplo, se ha pasado al inglés a mitad del vídeo) y se pide otra.
UMBRAL = 0.8
PRON_PIPER = [(r"\bGTA 6\b", "ge te a seis"), (r"\bGTA VI\b", "ge te a seis"), (r"\bGTA\b", "ge te a"),
              (r"Rockstar", "Rocstar"), (r"Vice City", "Vais Síti"), (r"\bJason\b", "Yéison")]


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.findall(r"[a-z0-9ñ]+", s)


# ---------------------------------------------------------------- alineación
def pausas(x, minimo=0.10):
    win = int(0.02 * SR)
    e = np.array([np.sqrt(np.mean(x[i:i + win] ** 2)) for i in range(0, len(x) - win, win)])
    sil = e < max(e.max() * 0.03, 0.004)
    res, i = [], 0
    while i < len(sil):
        if sil[i]:
            j = i
            while j < len(sil) and sil[j]:
                j += 1
            if (j - i) * 0.02 >= minimo:
                res.append((i * 0.02, j * 0.02))
            i = j
        else:
            i += 1
    return res


def por_pausas(x, trozos):
    """Reparte los trozos por longitud y los ajusta a la pausa más cercana (plan B sin Whisper)."""
    p = pausas(x)
    dur = len(x) / SR
    ini = p[0][1] if p and p[0][0] == 0 else 0.0
    fin = p[-1][0] if p and p[-1][1] >= dur - 0.05 else dur
    L = [len(t.replace(" ", "")) + 3 for t in trozos]
    tot = sum(L)
    bordes, acc, ult = [ini], 0, ini
    for w in L[:-1]:
        acc += w
        e = ini + (fin - ini) * acc / tot
        cerca = [(a, b) for a, b in p if abs((a + b) / 2 - e) < 0.7 and a > ult]
        if cerca:
            a, b = min(cerca, key=lambda q: abs((q[0] + q[1]) / 2 - e))
            bordes += [a, b]
            ult = b
        else:
            bordes += [e, e]
            ult = e
    bordes.append(fin)
    return [(bordes[2 * i], bordes[2 * i + 1]) for i in range(len(trozos))]


def por_whisper(ruta, trozos):
    return _whisper(ruta, trozos)[0]


def cobertura(ruta, trozos):
    """Parte del guion (de 0 a 1) que Whisper reconoce en el audio (0 si no entiende casi nada)."""
    try:
        return _whisper(ruta, trozos)[1]
    except Exception:
        return 0.0


def _whisper(ruta, trozos):
    from faster_whisper import WhisperModel
    x, sr = sf.read(ruta, dtype="float32")
    if x.ndim > 1:
        x = x.mean(1)
    x16 = np.interp(np.linspace(0, len(x) - 1, int(len(x) * 16000 / sr)), np.arange(len(x)), x).astype(np.float32)
    modelo = WhisperModel("base", device="cpu", compute_type="int8")
    segs, _ = modelo.transcribe(x16, language="es", word_timestamps=True, vad_filter=False)
    palabras = [(w.word, w.start, w.end) for s in segs for w in (s.words or [])]
    oidas, t_oidas = [], []
    for w, a, b in palabras:
        for tok in norm(w):
            oidas.append(tok)
            t_oidas.append((a, b))
    guion, de_trozo = [], []
    for k, t in enumerate(trozos):
        for tok in norm(t):
            guion.append(tok)
            de_trozo.append(k)
    if len(oidas) < len(guion) * 0.5:
        raise RuntimeError("Whisper entendió muy poco")
    tiempos = [None] * len(guion)
    sm = difflib.SequenceMatcher(None, guion, oidas, autojunk=False)
    for blk in sm.get_matching_blocks():
        for q in range(blk.size):
            tiempos[blk.a + q] = t_oidas[blk.b + q]
    conocidos = [i for i, t in enumerate(tiempos) if t]
    if len(conocidos) < len(guion) * 0.5:
        raise RuntimeError("el guion y lo que se oye no coinciden")
    for i in range(len(guion)):  # las palabras sin pareja se interpolan
        if tiempos[i] is None:
            antes = max((j for j in conocidos if j < i), default=None)
            despues = min((j for j in conocidos if j > i), default=None)
            if antes is None:
                tiempos[i] = (tiempos[despues][0], tiempos[despues][0])
            elif despues is None:
                tiempos[i] = (tiempos[antes][1], tiempos[antes][1])
            else:
                f = (i - antes) / (despues - antes)
                t = tiempos[antes][1] + (tiempos[despues][0] - tiempos[antes][1]) * f
                tiempos[i] = (t, t)
    out = []
    for k in range(len(trozos)):
        idx = [i for i, kk in enumerate(de_trozo) if kk == k]
        out.append((tiempos[idx[0]][0], tiempos[idx[-1]][1]) if idx else (out[-1][1] if out else 0, out[-1][1] if out else 0))
    return out, len(conocidos) / len(guion)


def alinear(ruta, trozos):
    x, sr = sf.read(ruta, dtype="float32")
    if x.ndim > 1:
        x = x.mean(1)
    try:
        t = por_whisper(ruta, trozos)
        metodo = "Whisper"
    except Exception as e:
        print(f"  (alineación por pausas: {str(e)[:120]})", flush=True)
        if sr != SR:
            x = np.interp(np.linspace(0, len(x) - 1, int(len(x) * SR / sr)), np.arange(len(x)), x)
        t = por_pausas(x, trozos)
        metodo = "pausas"
    return [(round(a, 2), round(b, 2)) for a, b in t], metodo


# ---------------------------------------------------------------- voces
def acelerar(ruta, factor):
    """9 nov: misma velocidad que los vídeos largos (+12 %). atempo no cambia el tono de la voz."""
    if abs(factor - 1) < 0.01:
        return
    tmp = ruta + ".rapido.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", ruta, "-filter:a", f"atempo={factor}", tmp], check=True)
    os.replace(tmp, ruta)

def con_silencio(ruta, inicio=0.15):
    """Añade 0,15 s de silencio al principio (para que el primer fotograma ya tenga el gancho)."""
    x, sr = sf.read(ruta, dtype="float32")
    if x.ndim > 1:
        x = x.mean(1)
    x = np.concatenate([np.zeros(int(inicio * sr), np.float32), x / (np.max(np.abs(x)) + 1e-6) * 0.9])
    sf.write(ruta, x, sr, subtype="PCM_16")


def piper(trozos, ruta):
    import sherpa_onnx
    d = os.path.join(MODELOS, PIPER)
    onnx = [f for f in os.listdir(d) if f.endswith(".onnx")][0]
    tts = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
        vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=f"{d}/{onnx}", tokens=f"{d}/tokens.txt",
                                                   data_dir=f"{d}/espeak-ng-data"), num_threads=2)))
    partes, tiempos, t = [np.zeros(int(0.15 * SR), np.float32)], [], 0.15
    for txt in trozos:
        p = txt
        for a, b in PRON_PIPER:
            p = re.sub(a, b, p)
        a = tts.generate(p, sid=0, speed=1.08)
        x = np.array(a.samples, dtype=np.float32)
        if a.sample_rate != SR:
            x = np.interp(np.linspace(0, len(x) - 1, int(len(x) * SR / a.sample_rate)), np.arange(len(x)), x).astype(np.float32)
        idx = np.where(np.abs(x) > 0.012)[0]
        if len(idx):
            x = x[max(idx[0] - 300, 0):idx[-1] + 1200]
        x = x / (np.max(np.abs(x)) + 1e-6) * 0.9
        dur = len(x) / SR
        tiempos.append((round(t, 2), round(t + dur, 2)))
        partes.append(x)
        pausa = 0.32 if re.search(r"[.?!]$", txt) else 0.12
        partes.append(np.zeros(int(pausa * SR), np.float32))
        t += dur + pausa
    sf.write(ruta, np.concatenate(partes), SR, subtype="PCM_16")
    return tiempos


def generar(trozos, ruta):
    """Crea la voz en `ruta` (wav). Devuelve (tiempos, nombre de la voz, aviso o '')."""
    try:
        mejor = None
        for intento in range(2):  # 2 nov: si la voz no sigue el guion (se pasa al inglés…), se pide otra una vez
            try:
                wav, modelo = gemini.voz(" ".join(trozos))
            except Exception:
                if mejor:
                    break
                raise
            open(ruta, "wb").write(wav)
            acelerar(ruta, VELOCIDAD_VOZ)
            con_silencio(ruta)
            c = cobertura(ruta, trozos)
            if c >= UMBRAL:
                tiempos, metodo = alinear(ruta, trozos)
                return tiempos, f"Gemini {VOZ} ({modelo}, subtítulos por {metodo})", ""
            print(f"  La voz no sigue el guion (Whisper reconoce el {c:.0%}): se pide otra", flush=True)
            if mejor is None or c > mejor[0]:
                mejor = (c, wav, modelo)
        c, wav, modelo = mejor
        open(ruta, "wb").write(wav)
        acelerar(ruta, VELOCIDAD_VOZ)
        con_silencio(ruta)
        tiempos, metodo = alinear(ruta, trozos)
        return (tiempos, f"Gemini {VOZ} ({modelo}, subtítulos por {metodo})",
                f"Revisa la voz: puede pasarse al inglés o saltarse texto (Whisper solo reconoce el {c:.0%} del guion)")
    except Exception as e:
        print(f"  Voz de Gemini no disponible: {str(e)[:300]}", flush=True)
        tiempos = piper(trozos, ruta)
        return tiempos, "Piper sharvard (reserva)", "Voz de reserva (Piper): Gemini no estaba disponible"


def tiempos_json(t):
    return json.dumps(t)
