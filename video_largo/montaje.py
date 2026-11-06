"""Montaje completo del vídeo largo de «Leónida al Día» (hook + 20 curiosidades + cierre). No publica nada.

Reutiliza las funciones del prototipo (voz, Whisper, subtítulos, rótulos, música) y añade: bajar cada vídeo oficial una
sola vez, clips en cámara lenta, los 22 bloques del guion, un sonido original por bloque cuando toca y los capítulos.

Salidas: «salida_hq/video_largo.mp4» (alta calidad), «salida_montaje/previa_00.mp4…» (720p, en partes de 5 min), «hoja.jpg»,
«capitulos.txt», «informe.txt». Pruebas: DRY=1 (imágenes de relleno), BLOQUES_SOLO=hook,c01 (solo esos bloques)."""
import csv
import hashlib
import os
import pathlib
import subprocess
import sys
import time
import urllib.request
import wave
import zipfile
from concurrent.futures import ThreadPoolExecutor

import numpy as np

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import importlib  # noqa: E402

guion_vl = importlib.import_module(os.environ.get("GUION", "guion_vl"))  # guion_vc = vídeo 2 (Vice City)
import prototipo as P  # noqa: E402
import voces as V  # noqa: E402

DRY = P.DRY
W, H, FPS, SR = P.W, P.H, P.FPS, P.SR
TMP, OUT, HQ = P.TMP, pathlib.Path("salida_montaje"), pathlib.Path("salida_hq")
FUENTES = pathlib.Path(os.environ.get("DIR_FUENTES", "fuentes"))
SOLO = [x.strip() for x in os.environ.get("BLOQUES_SOLO", "").split(",") if x.strip()]
URL_ZIP = P._V + "GTAVI_Videos.zip"
P.VIDEOS.update(getattr(guion_vl, "VIDEOS_EXTRA", {}))  # vídeos oficiales que añade el guion
FIJOS = set(getattr(guion_vl, "PLANOS_FIJOS", ()))  # logos y carteles: sin movimiento de cámara
for d in (OUT, HQ, FUENTES):
    d.mkdir(parents=True, exist_ok=True)


def descargar(url, destino):
    for i in range(8):
        r = subprocess.run(["curl", "-sSfL", "-A", P.UA, "-C", "-", "-o", str(destino), url], capture_output=True)
        if r.returncode == 0:
            return destino
        print("  descarga cortada, se reanuda", i + 1, flush=True)
        time.sleep(5)
    raise RuntimeError("No se pudo bajar " + url)


def fuente(video):
    """Ruta local del vídeo oficial (se baja una sola vez). «Clips:<archivo>» sale del zip oficial de clips."""
    if video.startswith("Clips:"):
        carpeta = FUENTES / "clips"
        if not carpeta.exists():
            carpeta.mkdir(parents=True)
            z = FUENTES / "clips.zip"
            descargar(URL_ZIP, z)
            with zipfile.ZipFile(z) as zz:
                for info in zz.infolist():
                    if info.filename.lower().endswith(".mp4") and "__MACOSX" not in info.filename:
                        (carpeta / os.path.basename(info.filename)).write_bytes(zz.read(info))
            z.unlink()
        return carpeta / video.split(":", 1)[1]
    if video.startswith("Imagen:"):  # captura o imagen fija (se baja una vez)
        url = video.split(":", 1)[1]
        ext = os.path.splitext(url.split("?")[0])[1] or ".jpg"
        destino = FUENTES / ("img_" + hashlib.sha1(url.encode()).hexdigest()[:10] + ext)
        if not destino.exists() or destino.stat().st_size == 0:
            descargar(url, destino)
        return destino
    destino = FUENTES / (video + ".mp4")
    if not destino.exists() or destino.stat().st_size == 0:
        print("Bajando", video, flush=True)
        descargar(P.VIDEOS[video], destino)
    return destino


def tabla():
    out = {}
    for nombre in ("trozos.csv", "trozos_vl.csv", "trozos_vc.csv", "trozos_auto.csv"):
        if not (AQUI / nombre).exists():
            continue
        with open(AQUI / nombre, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                out[r["Trozo"]] = {"ini": float(r["Inicio (s)"]), "dur": float(r["Duración (s)"]),
                                   "video": (r.get("Vídeo") or "Mirada").strip(), "lento": float(r.get("Lento") or 1),
                                   "grupo": (r.get("Grupo") or "").strip()}
    return out


def cortar(nombre, t, dur_out, destino, sentido):
    """Corta un trozo a 1080p con un ligero movimiento de cámara; los clips lentos se estiran a su duración final."""
    if t["video"].startswith("Imagen:") and not DRY:  # imagen: quieta, centrada y sobre fondo negro
        P.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", str(FPS), "-t", f"{dur_out:.2f}",
               "-i", str(fuente(t["video"])), "-vf",
               "scale=1600:880:force_original_aspect_ratio=decrease:flags=lanczos,"
               "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,format=yuv420p",
               "-t", f"{dur_out:.2f}", "-c:v", "libx264", "-crf", "12", "-preset", "veryfast", destino])
        return
    lento = t["lento"]
    dur_in = dur_out / lento
    if DRY:
        pre = []
        entrada = ["-f", "lavfi", "-i", f"testsrc2=size={W}x{H}:rate=30:duration={dur_in + 0.3}"]
    else:
        pre = ["-ss", f"{t['ini']:.2f}", "-t", f"{dur_in:.2f}"]
        entrada = ["-i", str(fuente(t["video"]))]
    x = f"(in_w-out_w)*t/{dur_out:.3f}" if sentido == 0 else f"(in_w-out_w)*(1-t/{dur_out:.3f})"
    if nombre in FIJOS:
        x = "(in_w-out_w)/2"
    vf = (f"setpts={lento}*PTS,fps={FPS},scale=2112:1188:flags=lanczos:force_original_aspect_ratio=increase,"
          f"crop={W}:{H}:x='{x}':y='(in_h-out_h)/2',format=yuv420p")
    for _ in range(3):
        try:
            P.run(["ffmpeg", "-y", "-loglevel", "error", *pre, *entrada, "-an", "-vf", vf, "-t", f"{dur_out:.2f}",
                   "-c:v", "libx264", "-crf", "12", "-preset", "veryfast", destino])
            return
        except RuntimeError as e:
            print("  reintento", nombre, str(e)[-200:], flush=True)
            time.sleep(3)
    raise RuntimeError("No se pudo cortar " + nombre)


def planificar(b, dur_visual, tb):
    """Lista [trozo, segundos] que cubre dur_visual. El trozo con sonido original no se repite en silencio."""
    nombres = [n for n in b["planos"] if n != b.get("original")]
    lista, resto, i = [], dur_visual, 0
    while resto > 0.05 and i < 60:
        n = nombres[i % len(nombres)]
        d = min(tb[n]["dur"] * tb[n]["lento"], resto)
        if d < 0.7 and lista:
            lista[-1][1] += d
        else:
            lista.append([n, d])
        resto -= d
        i += 1
    return lista


def momento(b, palabra, n=1):
    """Segundo (desde el inicio del bloque) en que la voz dice «palabra» (Whisper; si no, su posición en el texto)."""
    clave, vistos = P.normalizar(palabra), 0
    for w, a, _ in b.get("ws") or []:
        if P.normalizar(w).startswith(clave):
            vistos += 1
            if vistos == n:
                return b["voz_ini"] - b["ini"] + max(0.0, a - 0.2)
    pal = [P.normalizar(w) for w in b["texto"].split()]
    idx = [i for i, w in enumerate(pal) if w.startswith(clave)]
    frac = idx[min(n, len(idx)) - 1] / max(1, len(pal)) if idx else 0.0
    return b["voz_ini"] - b["ini"] + frac * b["dur_voz"]


def planificar_anclado(b, dur_visual, tb):
    """Como planificar, pero con planos que salen justo cuando la voz nombra algo (clave «planos_en» del guion)."""
    anc = sorted((momento(b, r["en"], r.get("n", 1)), r["plano"]) for r in b["planos_en"])
    relleno = [n for n in b["planos"] if n != b.get("original")]
    lista, estado = [], {"cursor": 0.0, "i": 0}

    def rellenar(hasta):
        while hasta - estado["cursor"] > 0.05:
            n = relleno[estado["i"] % len(relleno)]
            estado["i"] += 1
            d = min(tb[n]["dur"] * tb[n]["lento"], hasta - estado["cursor"])
            if d < 0.7 and lista:
                lista[-1][1] += d
            else:
                lista.append([n, d])
            estado["cursor"] += d

    for k, (t, n) in enumerate(anc):
        rellenar(min(max(t, estado["cursor"]), dur_visual))
        sig = anc[k + 1][0] if k + 1 < len(anc) else dur_visual
        d = min(tb[n]["dur"] * tb[n]["lento"], max(0.8, sig - estado["cursor"]), dur_visual - estado["cursor"])
        if d > 0.05:
            lista.append([n, d])
            estado["cursor"] += d
    rellenar(dur_visual)
    return lista


def ajustar_frase_lucia(tb):
    """Afina con Whisper dónde empieza y acaba «Relationships are about communication, Jay»."""
    if DRY or "VL_Frase_Lucia" not in tb:
        return
    try:
        from faster_whisper import WhisperModel
        ini = 522.0
        tmp = TMP / "ventana_lucia.wav"
        P.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{ini}", "-t", "20", "-i", str(fuente("Mirada")), "-vn",
               "-ar", "16000", "-ac", "1", tmp])
        if not P._WHISPER:
            P._WHISPER.append(WhisperModel(P.modelo_whisper(), device="cpu", compute_type="int8"))
        segs, _ = P._WHISPER[0].transcribe(P.audio_16k(tmp), language="en", word_timestamps=True)
        pal = [(P.normalizar(w.word), w.start, w.end) for s in segs for w in (s.words or [])]
        a = next(i for i, p in enumerate(pal) if p[0].startswith("relationship"))
        j = next(i for i in range(a, len(pal)) if pal[i][0] == "jay")
        nuevo_ini = ini + pal[a][1] - 0.25
        nuevo_dur = (pal[j][2] - pal[a][1]) + 0.25 + 0.5
        print(f"Frase de Lucía: {nuevo_ini:.2f} s, {nuevo_dur:.2f} s", flush=True)
        tb["VL_Frase_Lucia"]["ini"], tb["VL_Frase_Lucia"]["dur"] = nuevo_ini, nuevo_dur
    except Exception as e:  # noqa: BLE001
        print("No se ha podido afinar la frase de Lucía:", type(e).__name__, e, flush=True)


def anadir_cta(ruta, bloques):
    """Cartel «SUSCRÍBETE A LEÓNIDA AL DÍA» arriba en el centro, a mitad del vídeo y en el cierre."""
    tramos = [(b["voz_ini"], b["voz_fin"] + 0.6) for b in bloques if b.get("cta")]
    cierre = [b for b in bloques if b["id"] == "cierre"]
    if cierre:
        tramos.append((max(cierre[0]["voz_ini"], cierre[0]["voz_fin"] - 17), cierre[0]["voz_fin"] + 0.5))
    txt = pathlib.Path(ruta).read_text(encoding="utf-8")
    estilos = ("Style: CtaTit,Montserrat Black,38,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1\n"
               "Style: CtaSub,Montserrat ExtraBold,26,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,0,0,0,1\n"
               "Style: CtaFondo,Montserrat Black,20,&H00A34FFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1\n")
    txt = txt.replace("Style: Dibujo,", estilos + "Style: Dibujo,", 1)
    forma = ("m 24 0 l 796 0 b 810 0 820 10 820 24 l 820 96 b 820 110 810 120 796 120 l 24 120 b 10 120 0 110 0 96 "
             "l 0 24 b 0 10 10 0 24 0")
    ev = []
    for t0, t1 in tramos:
        a, z = P.ass_t(t0), P.ass_t(t1)
        ev.append(f"Dialogue: 3,{a},{z},CtaFondo,,0,0,0,,{{\\pos(550,40)\\fad(350,350)\\p1}}{forma}")
        ev.append(f"Dialogue: 4,{a},{z},CtaTit,,0,0,0,,{{\\an5\\pos(960,82)\\fad(350,350)}}SUSCRÍBETE A LEÓNIDA AL DÍA")
        ev.append(f"Dialogue: 4,{a},{z},CtaSub,,0,0,0,,{{\\an5\\pos(960,124)\\fad(350,350)}}Noticias nuevas de GTA 6 cada día")
    pathlib.Path(ruta).write_text(txt.rstrip("\n") + "\n" + "\n".join(ev) + "\n", encoding="utf-8")


def anadir_rotulos(ruta, bloques):
    """Datos grandes en el centro (clave «rotulos» del guion), sobre una caja negra para que se lean bien.

    Salen cuando la voz dice la palabra «en» (o en el segundo «t» del bloque) y no se pisan entre ellos.
    Con «negro»: True ocupan toda la pantalla en negro (para el gancho). Sin «rotulos» no cambia nada."""
    ev = []
    for b in bloques:
        if not b.get("rotulos"):
            continue
        pal_txt = [P.normalizar(w) for w in b["texto"].split()]
        ws = b.get("ws") or []
        lista = []
        for r in b["rotulos"]:
            if "t" in r:
                t0 = b["ini"] + float(r["t"])
            else:
                clave, n = P.normalizar(r["en"]), r.get("n", 1)
                t, vistos = None, 0
                for w, a, _ in ws:
                    if P.normalizar(w).startswith(clave):
                        vistos += 1
                        if vistos == n:
                            t = a
                            break
                if t is None:
                    idx = [i for i, w in enumerate(pal_txt) if w.startswith(clave)]
                    frac = idx[min(n, len(idx)) - 1] / max(1, len(pal_txt)) if idx else 0.5
                    t = frac * b["dur_voz"]
                t0 = b["voz_ini"] + max(0.0, t - 0.15)
            lista.append([t0, t0 + r.get("dur", 2.6), r])
        lista.sort(key=lambda x: x[0])
        for k in range(1, len(lista)):  # que no se pisen: el anterior se acorta o el nuevo espera
            ant = lista[k - 1]
            if lista[k][0] < ant[1] + 0.08:
                ant[1] = max(ant[0] + 1.3, lista[k][0] - 0.08)
                lista[k][0] = max(lista[k][0], ant[1] + 0.08)
                lista[k][1] = max(lista[k][1], lista[k][0] + 1.3)
        for t0, t1, r in lista:
            t1 = min(t1, b["fin"])
            if t1 - t0 < 0.8:
                continue
            l1, l2 = (r["texto"].split("|") + [""])[:2]
            negro = r.get("negro")
            g1, g2 = (124, 72) if negro else (84, 52)
            a, z = P.ass_t(t0), P.ass_t(t1)
            if negro:
                ev.append(f"Dialogue: 0,{a},{z},Dibujo,,0,0,0,,{{\\pos(0,0)\\c&H000000&\\fad(0,250)\\p1}}"
                          "m 0 0 l 1920 0 1920 1080 0 1080")
            else:
                w = min(1840, int(max(len(l1) * g1, len(l2) * g2) * 0.66) + 110)
                h = g1 + (g2 + 24 if l2 else 0) + 64
                ev.append(f"Dialogue: 2,{a},{z},Dibujo,,0,0,0,,{{\\pos({960 - w // 2},{440 - h // 2})\\c&H000000&"
                          f"\\alpha&H28&\\fad(150,200)\\p1}}m 0 0 l {w} 0 {w} {h} 0 {h}")
            linea2 = f"\\N{{\\fs{g2}\\c{P.ACENTO}}}{P.limpiar(l2)}" if l2 else ""
            ev.append(f"Dialogue: 3,{a},{z},Dato,,0,0,0,,{{\\an5\\pos(960,440)\\fad(150,200)\\fs{g1}\\c&H0000D7FF&}}"
                      f"{P.limpiar(l1)}{linea2}")
    if not ev:
        return
    txt = pathlib.Path(ruta).read_text(encoding="utf-8")
    estilo = ("Style: Dato,Montserrat Black,84,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,5,"
              "0,0,0,1\n")
    txt = txt.replace("Style: Dibujo,", estilo + "Style: Dibujo,", 1)
    pathlib.Path(ruta).write_text(txt.rstrip("\n") + "\n" + "\n".join(ev) + "\n", encoding="utf-8")


ESTILOS_MUSICA = [  # (bpm, bajos, acordes, octava del arpegio, filtro en Hz)
    (104, [55.0, 43.65, 65.41, 49.0], [(220.0, 261.63, 329.63), (174.61, 220.0, 261.63), (261.63, 329.63, 392.0),
                                       (196.0, 246.94, 293.66)], 2, 5500),
    (112, [73.42, 58.27, 87.31, 65.41], [(293.66, 349.23, 440.0), (233.08, 293.66, 349.23), (349.23, 440.0, 523.25),
                                         (261.63, 329.63, 392.0)], 2, 6500),
    (94, [41.2, 65.41, 49.0, 73.42], [(164.81, 196.0, 246.94), (130.81, 164.81, 196.0), (196.0, 246.94, 293.66),
                                      (146.83, 185.0, 220.0)], 1, 4200),
    (120, [46.25, 73.42, 55.0, 82.41], [(185.0, 220.0, 277.18), (146.83, 185.0, 220.0), (220.0, 277.18, 329.63),
                                        (164.81, 207.65, 246.94)], 2, 7000),
]


def musica_estilo(dur, bpm, raices, acordes, oct_arp, corte):
    """Como P.musica, pero con tempo, acordes y brillo propios (para cambiar de canción durante el vídeo)."""
    n = int(dur * SR)
    beat = 60 / bpm
    mus = np.zeros(n)
    corchea = beat / 2
    for k in range(int(dur / corchea) + 1):
        a = int(k * corchea * SR)
        b = min(n, a + int(corchea * SR))
        if a >= n:
            break
        f = raices[(int(k * corchea / (4 * beat))) % 4]
        tt = np.arange(b - a) / SR
        mus[a:b] += 0.30 * (2 * ((f * tt) % 1) - 1) * np.exp(-tt * 7)
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
        f = acordes[(int(k * beat / 4 / (4 * beat))) % 4][k % 3] * oct_arp
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
    esp *= 1 / (1 + (frec / corte) ** 4)
    mus = np.fft.irfft(esp, n)
    mus /= np.max(np.abs(mus)) + 1e-9
    return (mus * 0.9).astype(np.float32)


def musica_del_guion(bloques, total):
    """Música que cambia de estilo donde lo diga el guion (MUSICA = {id del bloque: estilo}), con fundidos de 1,5 s."""
    estilos = getattr(guion_vl, "MUSICA", None)
    if not estilos:
        return P.musica(total + 1)
    n = int((total + 1) * SR)
    mus = np.zeros(n, np.float32)
    cambios = [(b["ini"], estilos[b["id"]]) for b in bloques if b["id"] in estilos]
    if not cambios or cambios[0][0] > 0.5:
        cambios.insert(0, (0.0, cambios[0][1] if cambios else 0))
    for k, (t0, e) in enumerate(cambios):
        t1 = cambios[k + 1][0] if k + 1 < len(cambios) else total + 1
        a, z = max(0, int((t0 - 0.75) * SR)), min(n, int((t1 + 0.75) * SR))
        if z <= a:
            continue
        trozo = musica_estilo((z - a) / SR + 0.1, *ESTILOS_MUSICA[e % len(ESTILOS_MUSICA)])[: z - a]
        env = np.ones(z - a, np.float32)
        f = min(int(1.5 * SR), (z - a) // 2)
        if a > 0:
            env[:f] = np.linspace(0, 1, f)
        if z < n:
            env[-f:] = np.minimum(env[-f:], np.linspace(1, 0, f))
        mus[a:z] += trozo[: z - a] * env
    print("Música: " + ", ".join(f"{hms(t)} estilo {e + 1}" for t, e in cambios), flush=True)
    return mus


def rms_50hz(x):
    hop = SR // 50
    n = len(x) // hop
    return np.sqrt(np.mean(x[:n * hop].reshape(n, hop) ** 2, axis=1))


def fin_por_energia(x):
    """Segundo en que acaba la voz mirando el volumen (por si Whisper no oye las últimas palabras).

    Si lo último que suena es un golpe corto después de un silencio (el estallido de Gemini), no cuenta."""
    m = x if x.ndim == 1 else x.mean(axis=1)
    f = int(0.02 * SR)
    n = len(m) // f
    if n < 20:
        return None
    rms = np.sqrt((m[: n * f].reshape(n, f).astype(np.float64) ** 2).mean(axis=1))
    voz = rms >= max(0.008, 0.03 * float(np.percentile(rms, 95)))
    i = n - 1
    while i >= 0 and not voz[i]:
        i -= 1
    fin = i
    while i >= 0 and voz[i]:
        i -= 1
    ini = i + 1
    j = i
    while j >= 0 and not voz[j]:
        j -= 1
    if j > 0 and (fin - ini + 1) * 0.02 <= 0.35 and (i - j) * 0.02 >= 0.45:
        fin = j
    return (fin + 1) * 0.02


def fin_oido(b, ws):
    """Segundo en que Whisper oye acabar la última palabra del guion (texto o voz fonética); None si no la oye."""
    claves = set()
    for txt in (b["texto"], b.get("voz") or ""):
        claves |= {P.normalizar(w) for w in txt.split()[-2:]}
    claves = {c for c in claves if len(c) >= 3}
    for w, a, e in reversed(ws[-8:]):
        n = P.normalizar(w)
        if len(n) >= 3 and any(n == c or n[:4] == c[:4] for c in claves):
            return e
    return None


def silencio_tras(x, desde, margen=0.7):
    """Primer silencio de 0,12 s después de «desde»: ahí acaba de verdad la última palabra (lo de después es ruido)."""
    m = x if x.ndim == 1 else x.mean(axis=1)
    f = int(0.01 * SR)
    ini, fin = int(desde * SR), min(len(m), int((desde + margen) * SR))
    if fin - ini < 3 * f:
        return min(len(m) / SR, desde + 0.25)
    ref = float(np.percentile(np.abs(m), 99)) or 1.0
    seg = m[ini:fin]
    n = len(seg) // f
    rms = np.sqrt((seg[: n * f].reshape(n, f).astype(np.float64) ** 2).mean(axis=1))
    seguidos = 0
    for i, v in enumerate(rms < max(0.006, 0.04 * ref)):
        seguidos = seguidos + 1 if v else 0
        if seguidos >= 12:
            return desde + (i - 11) * 0.01 + 0.03
    return desde + margen


def expandir_grupos(bloques, tb):
    """«@Grupo» en planos o planos_en = trozos automáticos de ese grupo, repartidos sin repetir hasta agotarlos."""
    import random
    grupos = {}
    for n in sorted(tb):
        grupos.setdefault("@" + tb[n].get("grupo", ""), []).append(n)
    for lista in grupos.values():
        random.Random(7).shuffle(lista)
    usados = {}

    def siguiente(g):
        lista = grupos.get(g) or []
        if not lista:
            return None
        i = usados.get(g, 0)
        usados[g] = i + 1
        return lista[i % len(lista)]

    for b in bloques:
        nuevos = []
        for p in b["planos"]:
            if p.startswith("@"):
                nuevos += [x for x in (siguiente(p) for _ in range(5)) if x]
            else:
                nuevos.append(p)
        b["planos"] = nuevos or [p for p in b["planos"] if not p.startswith("@")] or ["VCA_Logo"]
        for r in b.get("planos_en", []):
            if r["plano"].startswith("@"):
                r["plano"] = siguiente(r["plano"]) or b["planos"][0]
        b["planos_en"] = [r for r in b.get("planos_en", []) if r["plano"] in tb]


def hms(s):
    s = int(round(s))
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def main():
    t0 = time.time()
    tb = tabla()
    bloques = [b for b in guion_vl.BLOQUES if not SOLO or b["id"] in SOLO]
    expandir_grupos(bloques, tb)
    faltan = [b["id"] for b in bloques if not V.ruta_wav(b).exists()]
    if faltan:
        print("Faltan voces:", faltan)
        sys.exit(1)
    # 1) voz de cada bloque (sin el estallido final ni lo que haya antes del guion) y palabras de Whisper
    for b in bloques:
        print("Voz de", b["id"], flush=True)
        b["wav"] = V.ruta_wav(b)
        b["wav48"] = TMP / (pathlib.Path(b["wav"]).stem + "_48k.wav")
        b["audio"] = P.leer_wav(b["wav"], P.TEMPO_VOZ)
        pal = b["texto"].split()
        ws = P.palabras_whisper(b["wav48"])
        rec = P.inicio_guion(pal, ws)
        b["recorte"] = rec if rec > 0.4 else 0.0
        if b["recorte"]:
            b["audio"] = b["audio"][int(b["recorte"] * SR):]
            ws = [(w, a - b["recorte"], e - b["recorte"]) for w, a, e in ws if e > b["recorte"]]
        dur_antes = len(b["audio"]) / SR
        fin_g = P.fin_guion(pal, ws)
        b["cola_cortada"] = 0.0
        oido = fin_oido(b, ws)
        if oido is not None:  # se oye la última palabra: se corta en el silencio que la sigue (fuera el ruido de después)
            fin_g = silencio_tras(b["audio"], oido) - 0.1
            print(f"  Última palabra a los {oido:.2f} s; corte en {fin_g + 0.18:.2f} s", flush=True)
        else:
            fin_e = fin_por_energia(b["audio"])
            if fin_g is not None and fin_e is not None and fin_e + 0.08 > fin_g + 0.18:
                print(f"  Whisper acaba en {fin_g:.2f} s pero la voz sigue hasta {fin_e:.2f} s", flush=True)
                fin_g = fin_e - 0.1
        if fin_g is not None and fin_g + 0.3 < dur_antes:
            b["cola_cortada"] = dur_antes - (fin_g + 0.18)
            b["audio"] = b["audio"][: int((fin_g + 0.18) * SR)]
        antes_lv = b["audio"]
        b["audio"], desfase = P.limpiar_voz(b["audio"])
        fin_lv = desfase + len(b["audio"]) / SR
        fin_real = (len(antes_lv) / SR - 0.12) if oido is not None else fin_por_energia(antes_lv)
        if fin_real and fin_real > fin_lv + 0.05:  # limpiar_voz no puede comerse la última palabra
            seg = antes_lv[int(desfase * SR):int(min(len(antes_lv) / SR, fin_real + 0.2) * SR)]
            seg = seg - seg.mean(axis=0, keepdims=True)
            f_in, f_out = int(0.01 * SR), min(int(0.12 * SR), len(seg) // 4)
            env = np.ones(len(seg))
            env[:f_in] = np.linspace(0, 1, f_in)
            env[len(seg) - f_out:] = np.linspace(1, 0, f_out)
            b["audio"] = (seg * (env[:, None] if seg.ndim == 2 else env)).astype(np.float32)
            print(f"  Final de la voz recuperado: {fin_real - fin_lv:.2f} s", flush=True)
        b["audio"] = np.array(b["audio"], dtype=np.float32)
        n_f = min(int(0.06 * SR), len(b["audio"]) // 4)
        if n_f > 0:  # final siempre suave
            env = np.linspace(1, 0, n_f, dtype=np.float32)
            b["audio"][-n_f:] *= env[:, None] if b["audio"].ndim == 2 else env
        b["ws"] = [(w, a - desfase, e - desfase) for w, a, e in ws]
        b["dur_voz"] = len(b["audio"]) / SR
        ult = [P.normalizar(w) for w in b["texto"].split()[-2:]]
        ult += [P.normalizar(w) for w in (b.get("voz") or "").split()[-2:]]
        oidas = [P.normalizar(w[0]) for w in b["ws"] if w[1] < b["dur_voz"]][-6:]
        b["aviso_final"] = bool(b["ws"]) and not any(u in oidas for u in ult if len(u) >= 3)
        if b["aviso_final"]:
            print("  AVISO: Whisper no oye el final del guion en la voz montada", flush=True)
        print(f"  {b['dur_voz']:.1f} s (final recortado {b['cola_cortada']:.2f} s)", flush=True)
    ajustar_frase_lucia(tb)
    # 2) línea de tiempo (la pausa de después compensa lo recortado del final de la voz, para mantener el ritmo)
    t = 0.0
    for i, b in enumerate(bloques):
        b["ini"] = t
        b["voz_ini"] = t + (0.15 if i == 0 else 0.5)
        b["voz_fin"] = b["voz_ini"] + b["dur_voz"]
        b["vis_fin"] = b["voz_fin"] + 0.4 + min(b["cola_cortada"], 0.5)
        b["fin"] = b["vis_fin"]
        if b.get("original"):
            o = tb[b["original"]]
            b["orig_ini"], b["orig_fin"] = b["vis_fin"], b["vis_fin"] + o["dur"]
            b["fin"] = b["orig_fin"]
        t = b["fin"]
    total = t + 0.8
    print(f"Duración total prevista: {total:.1f} s ({hms(total)})", flush=True)
    # 3) planos: se cortan en paralelo
    carpeta = TMP / "planos"
    carpeta.mkdir(exist_ok=True)
    tareas, lista_concat, k = [], [], 0
    for b in bloques:
        b["plan"] = (planificar_anclado if b.get("planos_en") else planificar)(b, b["vis_fin"] - b["ini"], tb)
        for nombre, dur in b["plan"]:
            k += 1
            destino = str(carpeta / f"{k:03d}_{nombre}.mp4")
            tareas.append((nombre, tb[nombre], dur, destino, k % 2))
            lista_concat.append(destino)
        if b.get("original"):
            k += 1
            o = tb[b["original"]]
            destino = str(carpeta / f"{k:03d}_{b['original']}.mp4")
            tareas.append((b["original"], o, o["dur"], destino, 0))
            lista_concat.append(destino)
            if not DRY:
                b["orig_wav"] = TMP / f"orig_{b['id']}.wav"
                P.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{o['ini']:.2f}", "-t", f"{o['dur']:.2f}",
                       "-i", str(fuente(o["video"])), "-vn", "-ar", SR, "-ac", 2, "-c:a", "pcm_s16le", b["orig_wav"]])
    if not DRY:
        for v in sorted({tb[n]["video"] for n, *_ in tareas}):
            fuente(v)  # baja cada vídeo oficial una vez, antes de cortar en paralelo
    with ThreadPoolExecutor(max_workers=3) as ex:
        futuros = [ex.submit(cortar, *tarea) for tarea in tareas]
        for f in futuros:
            f.result()
    print(f"{len(tareas)} planos cortados ({time.time() - t0:.0f} s)", flush=True)
    (TMP / "lista.txt").write_text("".join(f"file '{pathlib.Path(p).resolve()}'\n" for p in lista_concat))
    P.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", TMP / "lista.txt", "-c", "copy",
           TMP / "sin_audio.mp4"])
    # 4) subtítulos y rótulos
    for b in bloques:
        pal = b["texto"].split()
        tiempos = P.alinear(pal, b["ws"], b["dur_voz"]) if b["ws"] else None
        b["metodo"] = "Whisper"
        if not tiempos:
            tiempos, b["metodo"] = P.tiempos_por_voz(b["audio"], b["texto"]), "la voz (pausas)"
        b["subs"] = P.frases_de_subtitulo(pal, tiempos, b["voz_ini"])
    P.escribir_ass(TMP / "rotulos.ass", bloques, total)
    anadir_cta(TMP / "rotulos.ass", bloques)
    anadir_rotulos(TMP / "rotulos.ass", bloques)
    # 5) audio: voz + música que baja con la voz + sonidos originales
    n = int(total * SR)
    voz = np.zeros((n, 2), np.float32)
    for b in bloques:
        a = b["audio"] / (np.max(np.abs(b["audio"])) + 1e-9) * 0.9
        i0 = int(b["voz_ini"] * SR)
        voz[i0:i0 + len(a)] += a[: n - i0]
    mus = musica_del_guion(bloques, total)[:n]
    rms = rms_50hz(voz.mean(axis=1))
    habla = P.suavizar((rms > 0.02).astype(float), 50, 0.06, 0.5)
    tt = np.arange(n) / SR
    ganancia = 0.30 - (0.30 - 0.085) * np.interp(tt, np.arange(len(habla)) / 50, habla)
    ganancia *= np.minimum(1, tt / 1.0) * np.minimum(1, (total - tt) / 1.5)
    orig = np.zeros((n, 2), np.float32)
    mudo = np.ones(int(total * 100) + 2)
    for b in bloques:
        if b.get("original"):
            mudo[int(b["orig_ini"] * 100):int(b["orig_fin"] * 100)] = 0
            if "orig_wav" in b:
                o = P.fundir(P.leer_wav(b["orig_wav"]), 0.06, 0.15)
                i0 = int(b["orig_ini"] * SR)
                orig[i0:i0 + len(o)] += o[: n - i0] * 0.95
    mudo = P.suavizar(mudo, 100, 0.02, 0.04)
    silencio = np.interp(tt, np.arange(len(mudo)) / 100, mudo)
    mezcla = np.clip(voz + (mus * ganancia * silencio)[:, None] + orig, -1, 1)
    with wave.open(str(TMP / "mezcla.wav"), "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes((mezcla * 32767).astype("<i2").tobytes())
    del voz, mus, orig, mezcla
    # 6) montaje final
    P.crear_degradado(TMP / "degradado.png")
    grafo = (f"[0:v]tpad=stop_mode=clone:stop_duration=3,eq=contrast=1.04:saturation=1.08,unsharp=5:5:0.4:5:5:0.0[v0];"
             f"[2:v]format=rgba[g];[v0][g]overlay=0:{H - P.ALTO_DEGRADADO}:shortest=1[v1];"
             f"[v1]ass={TMP / 'rotulos.ass'}[v]")
    final = HQ / "video_largo.mp4"
    P.run(["ffmpeg", "-y", "-loglevel", "error", "-i", TMP / "sin_audio.mp4", "-i", TMP / "mezcla.wav",
           "-loop", "1", "-framerate", FPS, "-i", TMP / "degradado.png", "-filter_complex", grafo, "-map", "[v]",
           "-map", "1:a", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:v", "libx264", "-crf", "19", "-preset", "medium",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", SR, "-t", f"{total:.2f}", "-movflags", "+faststart",
           final])
    print(f"Vídeo final listo ({time.time() - t0:.0f} s)", flush=True)
    P.run(["ffmpeg", "-y", "-loglevel", "error", "-i", final, "-vf", "scale=1280:720", "-c:v", "libx264", "-crf", "27",
           "-maxrate", "2000k", "-bufsize", "4000k", "-preset", "fast", "-force_key_frames", "expr:gte(t,n_forced*300)",
           "-c:a", "aac", "-b:a", "112k", "-f", "segment", "-segment_time", "300", "-reset_timestamps", "1",
           "-segment_format_options", "movflags=+faststart", str(OUT / "previa_%02d.mp4")])
    P.run(["ffmpeg", "-y", "-loglevel", "error", "-i", final, "-vf", "fps=1/20,scale=320:-1,tile=6x6", "-frames:v", "1",
           "-q:v", "3", OUT / "hoja.jpg"])
    dur = float(P.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", final]).stdout)
    caps = ["0:00 Introducción"] if bloques and bloques[0]["id"] == "hook" else []
    for b in bloques:
        if b["num"] == "E1":
            caps.append(f"{hms(b['ini'])} Tres extra de regalo")
        elif isinstance(b["num"], str):
            continue
        elif b["num"]:
            caps.append(f"{hms(b['ini'])} {b['num']}. {b.get('capitulo') or b['titulo'].capitalize()}")
        elif b["id"] == "cierre":
            caps.append(f"{hms(b['ini'])} {b.get('capitulo') or 'Lo que Rockstar aún no ha contado'}")
    (OUT / "capitulos.txt").write_text("\n".join(caps), encoding="utf-8")
    informe = [f"Duración: {dur:.1f} s ({hms(dur)})", f"Tamaño: {final.stat().st_size / 1e6:.0f} MB (alta calidad), "
               f"{sum(p.stat().st_size for p in OUT.glob('previa_*.mp4')) / 1e6:.0f} MB (previa en partes de 5 min)", f"Tiempo de montaje: {time.time() - t0:.0f} s", ""]
    for b in bloques:
        informe.append(f"{b['id']}: voz {b['dur_voz']:.1f} s, {len(b['plan'])} planos, subtítulos por {b['metodo']}"
                       + (f", sonido original {b['original']}" if b.get("original") else "")
                       + (", AVISO: revisar el final de la voz" if b.get("aviso_final") else ""))
    (OUT / "informe.txt").write_text("\n".join(informe), encoding="utf-8")
    print("\n".join(informe))
    resumen = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumen:
        with open(resumen, "a", encoding="utf-8") as f:
            f.write("### Montaje del vídeo largo\n\n" + "\n".join(informe).replace("\n", "  \n")
                    + "\n\n### Capítulos\n\n" + "\n".join(caps).replace("\n", "  \n") + "\n")


if __name__ == "__main__":
    main()
