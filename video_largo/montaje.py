"""Montaje completo del vídeo largo de «Leónida al Día» (hook + 20 curiosidades + cierre). No publica nada.

Reutiliza las funciones del prototipo (voz, Whisper, subtítulos, rótulos, música) y añade: bajar cada vídeo oficial una
sola vez, clips en cámara lenta, los 22 bloques del guion, un sonido original por bloque cuando toca y los capítulos.

Salidas: «salida_hq/video_largo.mp4» (alta calidad), «salida_montaje/previa_00.mp4…» (720p, en partes de 5 min), «hoja.jpg»,
«capitulos.txt», «informe.txt». Pruebas: DRY=1 (imágenes de relleno), BLOQUES_SOLO=hook,c01 (solo esos bloques).

Vídeo 3 (guion_sg, rama saga), todo opcional y solo si el guion lo pide:
  cartela         -> 1,6 s quieta al empezar el bloque: fondo negro, año grande y nombre del acto (con golpe de sonido)
  intro_original  -> trozo con su sonido original justo después de la cartela, antes de la voz
  anio / LINEA    -> línea de tiempo fina abajo del todo (1997 → 2026) con el punto en el año del bloque
  MUSICA          -> también acepta estilos por época: "chiptune", "breakbeat", "hiphop", "synthwave"; ninguna pista
                     suena más de MAX_PISTA s seguidos (se cambia de variante en el bloque más cercano a la mitad)
  "VIDEO@ini+dur" -> plano escrito en el propio guion (por ejemplo "IV_T2@12.5+3")
  "@Grupo:N"      -> N trozos distintos del grupo (en vez de 5)
Controles (paran el montaje): trozos repetidos (PERMITIR_REPETIDOS=1 para saltarlo) y voces cuyo final no se oye
(FORZAR_FINALES=1). SOLO_VOCES=1 hace solo el informe de finales de voz (salida_montaje/finales) y para."""
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
        url = P.VIDEOS[video]
        if "#t=" in url:  # solo un tramo de un vídeo muy largo (partidas de archive.org de varias horas)
            base, rango = url.split("#t=", 1)
            a, z = (float(x) for x in rango.split(","))
            for i in range(4):
                r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-user_agent", P.UA, "-ss", f"{a:.2f}",
                                    "-to", f"{z:.2f}", "-i", base, "-c", "copy", "-an", str(destino)], capture_output=True)
                if r.returncode == 0 and destino.exists() and destino.stat().st_size > 0:
                    break
                time.sleep(5)
            else:
                raise RuntimeError("No se pudo bajar el tramo " + url)
        else:
            descargar(url, destino)
    return destino


def tabla():
    out = {}
    for nombre in ("trozos.csv", "trozos_vl.csv", "trozos_vc.csv", "trozos_auto.csv", "trozos_auto_sg.csv"):
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
    if es_fijo(nombre):
        x = "(in_w-out_w)/2"
    vf = (f"setpts={lento}*PTS,fps={FPS},scale=2112:1188:flags=lanczos:force_original_aspect_ratio=increase,"
          f"crop={W}:{H}:x='{x}':y='(in_h-out_h)/2',format=yuv420p")
    if MARCO and not DRY and alto(fuente(t["video"])) < 600:
        # vídeo antiguo de poca resolución: se ve entero y nítido en un marco, sobre una copia borrosa y oscura
        z = "1+0.03*t/%.3f" % dur_out if not es_fijo(nombre) else "1"
        vf = (f"setpts={lento}*PTS,fps={FPS},split[a][b];"
              f"[a]scale=480:270:force_original_aspect_ratio=increase,crop=480:270,boxblur=12:2,eq=brightness=-0.32,"
              f"scale={W}:{H}[f];"
              f"[b]scale=-2:{int(H * 0.82)}:flags=lanczos,scale='trunc(iw*({z})/2)*2':'trunc(ih*({z})/2)*2':eval=frame[c];"
              f"[f][c]overlay=(W-w)/2:(H-h)/2-24,format=yuv420p")
    for _ in range(3):
        try:
            P.run(["ffmpeg", "-y", "-loglevel", "error", *pre, *entrada, "-an", "-vf", vf, "-t", f"{dur_out:.2f}",
                   "-c:v", "libx264", "-crf", "12", "-preset", "veryfast", destino])
            return
        except RuntimeError as e:
            print("  reintento", nombre, str(e)[-200:], flush=True)
            time.sleep(3)
    raise RuntimeError("No se pudo cortar " + nombre)


MARCO = os.environ.get("MARCO", "1" if getattr(guion_vl, "MARCO", False) else "0") == "1"
_ALTOS = {}


def alto(ruta):
    ruta = str(ruta)
    if ruta not in _ALTOS:
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=height",
                            "-of", "csv=p=0", ruta], capture_output=True, text=True)
        try:
            _ALTOS[ruta] = int(r.stdout.strip().split()[0])
        except (ValueError, IndexError):
            _ALTOS[ruta] = 1080
    return _ALTOS[ruta]


def es_fijo(nombre):
    """Logos, carteles e imágenes van siempre quietos (sin movimiento de cámara)."""
    n = nombre.lower()
    return nombre in FIJOS or "logo" in n or n.startswith("img_") or "cartel" in n or "letras" in n


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
                return b["voz_ini"] - b.get("plan_ini", b["ini"]) + max(0.0, a - 0.2)
    pal = [P.normalizar(w) for w in b["texto"].split()]
    idx = [i for i, w in enumerate(pal) if w.startswith(clave)]
    frac = idx[min(n, len(idx)) - 1] / max(1, len(pal)) if idx else 0.0
    return b["voz_ini"] - b.get("plan_ini", b["ini"]) + frac * b["dur_voz"]


def planificar_anclado(b, dur_visual, tb):
    """Como planificar, pero con planos que salen justo cuando la voz nombra algo (clave «planos_en» del guion)."""
    anc = sorted((momento(b, r["en"], r.get("n", 1)), r["plano"]) for r in b["planos_en"])
    anclados = {n for _, n in anc}
    relleno = [n for n in b["planos"] if n != b.get("original") and n not in anclados] or \
        [n for n in b["planos"] if n != b.get("original")]
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


# ---------------------------------------------------------------- música por época (vídeo 3)
MAX_PISTA = float(os.environ.get("MAX_PISTA", "210"))  # ninguna pista más de 3,5 min seguidos
_PROG = [(0, 3, 7), (-4, 0, 3), (-7, -3, 0), (-2, 2, 5)]  # i - VI - IV - VII (en semitonos sobre la tónica)


def _nota(base, semitonos):
    return base * 2 ** (semitonos / 12)


def _bombo(n, sr, fuerza=1.0, grave=48):
    tt = np.arange(n) / sr
    return fuerza * np.sin(2 * np.pi * (grave * tt + 90 * (1 - np.exp(-tt * 30)) / 30)) * np.exp(-tt * 12)


def _ruido(n, semilla, decae):
    tt = np.arange(n) / SR
    return np.random.RandomState(semilla).randn(n) * np.exp(-tt * decae)


def _pegar(mus, a, sonido):
    if a >= len(mus):
        return
    z = min(len(mus), a + len(sonido))
    mus[a:z] += sonido[: z - a]


def musica_era(estilo, dur, variante=0):
    """Música hecha con código según la época del acto. variante cambia la tonalidad y el orden de los acordes."""
    if estilo == "synthwave":
        e = ESTILOS_MUSICA[(0, 3, 1)[variante % 3]]
        return musica_estilo(dur, *e)
    bpm, tonica, corte = {"chiptune": (138, 220.0, 7500), "breakbeat": (126, 110.0, 6000),
                          "hiphop": (86, 98.0, 4200)}.get(estilo, (110, 110.0, 6000))
    tonica = _nota(tonica, (0, 3, -2, 5)[variante % 4])
    prog = _PROG[variante % 4:] + _PROG[:variante % 4]
    n = int(dur * SR)
    mus = np.zeros(n)
    beat = 60 / bpm
    compas = 4 * beat
    rnd = np.random.RandomState(11 + variante)
    for k in range(int(dur / compas) + 1):
        a0 = int(k * compas * SR)
        if a0 >= n:
            break
        acorde = prog[k % 4]
        raiz = _nota(tonica, acorde[0])
        largo = int(compas * SR)
        tt = np.arange(largo) / SR
        if estilo == "chiptune":
            # arpegio de onda cuadrada (semicorcheas), bajo triangular y ruido como batería
            paso = beat / 4
            for j in range(16):
                f = _nota(tonica * 2, acorde[j % 3] + (12 if j % 8 >= 6 else 0))
                m = int(paso * SR)
                t2 = np.arange(m) / SR
                _pegar(mus, a0 + j * m, 0.10 * np.sign(np.sin(2 * np.pi * f * t2)) * np.exp(-t2 * 9))
            for j in range(8):
                m = int(beat / 2 * SR)
                t2 = np.arange(m) / SR
                f = raiz / 2 * (1 if j % 2 == 0 else 2)
                _pegar(mus, a0 + j * m, 0.22 * (2 * np.abs(2 * ((f * t2) % 1) - 1) - 1) * np.exp(-t2 * 3))
            for j in range(4):
                _pegar(mus, a0 + int(j * beat * SR), 0.5 * _bombo(int(0.12 * SR), SR, 1, 60))
                if j % 2:
                    _pegar(mus, a0 + int(j * beat * SR), 0.12 * _ruido(int(0.1 * SR), k * 4 + j, 30))
                _pegar(mus, a0 + int((j + 0.5) * beat * SR), 0.05 * _ruido(int(0.03 * SR), k * 8 + j, 90))
        elif estilo == "breakbeat":
            # bombo y caja sincopados, charles rápido, bajo de sierra y acordes cortos
            golpes = [(0, "b"), (1, "c"), (1.75, "b"), (2.5, "b"), (3, "c"), (3.75, "c2")]
            for pos, tipo in golpes:
                a = a0 + int(pos * beat * SR)
                if tipo == "b":
                    _pegar(mus, a, 0.75 * _bombo(int(0.25 * SR), SR, 1, 50))
                else:
                    f = 0.32 if tipo == "c" else 0.14
                    _pegar(mus, a, f * (_ruido(int(0.16 * SR), k * 10 + int(pos * 4), 22)
                                        + 0.5 * np.sin(2 * np.pi * 190 * np.arange(int(0.16 * SR)) / SR)
                                        * np.exp(-np.arange(int(0.16 * SR)) / SR * 25)))
            for j in range(16):
                _pegar(mus, a0 + int(j * beat / 4 * SR), (0.05 if j % 2 else 0.08) * _ruido(int(0.025 * SR), k * 16 + j, 120))
            for j in range(8):
                m = int(beat / 2 * SR)
                t2 = np.arange(m) / SR
                f = raiz / 2 * (2 if j in (3, 6) else 1)
                _pegar(mus, a0 + j * m, 0.16 * (2 * ((f * t2) % 1) - 1) * np.exp(-t2 * 5))
            for pos in (0, 1.5, 3):
                m = int(0.22 * SR)
                t2 = np.arange(m) / SR
                stab = sum(np.sign(np.sin(2 * np.pi * _nota(tonica * 2, s_) * t2)) for s_ in acorde)
                _pegar(mus, a0 + int(pos * beat * SR), 0.035 * stab * np.exp(-t2 * 10))
        else:  # hiphop: boom bap lento, piano eléctrico y bajo redondo, con un poco de swing
            sw = 0.08 * beat
            for pos in (0, 1.5, 2.25):
                _pegar(mus, a0 + int(pos * beat * SR), 0.85 * _bombo(int(0.35 * SR), SR, 1, 42))
            for pos in (1, 3):
                _pegar(mus, a0 + int(pos * beat * SR), 0.30 * _ruido(int(0.22 * SR), k * 7 + pos, 16))
            for j in range(8):
                _pegar(mus, a0 + int((j * beat / 2 + (sw if j % 2 else 0)) * SR),
                       (0.04 if j % 2 else 0.06) * _ruido(int(0.03 * SR), k * 9 + j, 100))
            for pos in (0, 2.5):
                m = int(1.4 * beat * SR)
                t2 = np.arange(m) / SR
                piano = sum(np.sin(2 * np.pi * _nota(tonica * 2, s_) * t2) * (1 + 0.3 * np.sin(2 * np.pi * 5 * t2))
                            for s_ in acorde)
                _pegar(mus, a0 + int(pos * beat * SR), 0.06 * piano * np.exp(-t2 * 2.2))
            m = int(compas * SR)
            t2 = np.arange(m) / SR
            _pegar(mus, a0, 0.20 * np.sin(2 * np.pi * raiz / 2 * t2) * np.minimum(1, t2 * 20) * np.exp(-t2 * 0.6))
            _pegar(mus, a0, 0.004 * rnd.randn(m))  # un poco de «vinilo»
    esp = np.fft.rfft(mus)
    frec = np.fft.rfftfreq(n, 1 / SR)
    esp *= 1 / (1 + (frec / corte) ** 4)
    mus = np.fft.irfft(esp, n)
    mus /= np.max(np.abs(mus)) + 1e-9
    return (mus * 0.9).astype(np.float32)


def pista(estilo, dur, variante=0):
    if isinstance(estilo, str):
        return musica_era(estilo, dur, variante)
    return musica_estilo(dur, *ESTILOS_MUSICA[(estilo + variante) % len(ESTILOS_MUSICA)])


def partir_pistas(cambios, inicios, total):
    """Si una pista dura más de MAX_PISTA, cambia de variante al empezar el bloque más cercano a su mitad."""
    salida = []
    for k, (t0, e) in enumerate(cambios):
        t1 = cambios[k + 1][0] if k + 1 < len(cambios) else total
        trozos, var = [(t0, e, 0)], 0
        while trozos[-1][0] < t1 and t1 - trozos[-1][0] > MAX_PISTA:
            ini = trozos[-1][0]
            mitad = ini + min(MAX_PISTA, (t1 - ini) / 2)
            opciones = [x for x in inicios if ini + 30 < x < t1 - 20]
            if not opciones:
                break
            corte = min(opciones, key=lambda x: abs(x - mitad))
            if corte - ini > MAX_PISTA:
                opciones = [x for x in opciones if x - ini <= MAX_PISTA] or opciones
                corte = max(opciones) if opciones else corte
            var += 1
            trozos.append((corte, e, var))
        salida += trozos
    return salida


def musica_del_guion(bloques, total):
    """Música que cambia de estilo donde lo diga el guion (MUSICA = {id del bloque: estilo}), con fundidos de 1,5 s."""
    estilos = getattr(guion_vl, "MUSICA", None)
    if not estilos:
        return P.musica(total + 1)
    n = int((total + 1) * SR)
    mus = np.zeros(n, np.float32)
    actual, de_bloque = None, {}
    for b in getattr(guion_vl, "BLOQUES", bloques):  # estilo de cada bloque según el guion entero (sirve en la previa)
        actual = estilos.get(b["id"], actual)
        de_bloque[b["id"]] = actual
    cambios, previo = [], object()
    for b in bloques:
        e = de_bloque.get(b["id"], estilos.get(b["id"]))
        if e is not None and e != previo:
            cambios.append((b["ini"], e))
            previo = e
    if not cambios or cambios[0][0] > 0.5:
        cambios.insert(0, (0.0, cambios[0][1] if cambios else 0))
    cambios = partir_pistas(cambios, [b["ini"] for b in bloques], total + 1)
    for k, (t0, e, var) in enumerate(cambios):
        t1 = cambios[k + 1][0] if k + 1 < len(cambios) else total + 1
        a, z = max(0, int((t0 - 0.75) * SR)), min(n, int((t1 + 0.75) * SR))
        if z <= a:
            continue
        trozo = pista(e, (z - a) / SR + 0.1, var)[: z - a]
        env = np.ones(z - a, np.float32)
        f = min(int(1.5 * SR), (z - a) // 2)
        if a > 0:
            env[:f] = np.linspace(0, 1, f)
        if z < n:
            env[-f:] = np.minimum(env[-f:], np.linspace(1, 0, f))
        mus[a:z] += trozo[: z - a] * env
    print("Música: " + ", ".join(f"{hms(t)} {e if isinstance(e, str) else 'estilo %d' % (e + 1)}"
                                 + (f" (variante {v + 1})" if v else "") for t, e, v in cambios), flush=True)
    globals()["PISTAS"] = [(t, e, v) for t, e, v in cambios]
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


def planos_en_linea(bloques, tb):
    """Planos escritos en el guion como «VIDEO@inicio+duración» (p. ej. "IV_T2@12.5+3"): se añaden a la tabla."""
    for b in bloques:
        nombres = list(b.get("planos", [])) + [r["plano"] for r in b.get("planos_en", [])]
        nombres += [b[k] for k in ("original", "intro_original") if b.get(k)]
        for n in nombres:
            if "@" in n[1:] and n not in tb:
                video, _, resto = n.partition("@")
                ini, _, dur = resto.partition("+")
                tb[n] = {"ini": float(ini), "dur": float(dur or 3), "video": video, "lento": 1.0, "grupo": ""}


def expandir_grupos(bloques, tb):
    """«@Grupo» en planos o planos_en = trozos automáticos de ese grupo, repartidos sin repetir hasta agotarlos."""
    import random
    grupos = {}
    for n in sorted(tb):
        grupos.setdefault("@" + tb[n].get("grupo", ""), []).append(n)
    for lista in grupos.values():
        random.Random(7).shuffle(lista)
    usados = {}
    explicitos = {p for b in bloques for p in list(b["planos"]) + [r["plano"] for r in b.get("planos_en", [])]
                  + [b[k] for k in ("original", "intro_original") if b.get(k)] if not p.startswith("@")}  # los planos que el guion pide por su nombre no salen también por grupo

    def siguiente(g):
        lista = grupos.get(g) or []
        if not lista:
            return None
        while usados.get(g, 0) < len(lista):  # cuando el grupo se acaba, no se repite: se usan los demás planos
            i = usados.get(g, 0)
            usados[g] = i + 1
            if lista[i] not in explicitos:
                return lista[i]
        return None

    for b in bloques:
        nuevos = []
        for p in b["planos"]:
            if p.startswith("@"):
                g, _, cuantos = p.partition(":")
                nuevos += [x for x in (siguiente(g) for _ in range(int(cuantos or 5))) if x and x not in nuevos]
            else:
                nuevos.append(p)
        b["planos"] = nuevos or [p for p in b["planos"] if not p.startswith("@")] or ["VCA_Logo"]
        for r in b.get("planos_en", []):
            if r["plano"].startswith("@"):
                r["plano"] = siguiente(r["plano"].partition(":")[0]) or b["planos"][0]
        b["planos_en"] = [r for r in b.get("planos_en", []) if r["plano"] in tb]


# ---------------------------------------------------------------- cartelas, línea de tiempo y controles (vídeo 3)
DUR_CARTELA = 1.6
LINEA = getattr(guion_vl, "LINEA", None)  # [(año, "nombre corto"), ...] para la línea de tiempo de abajo
Y_LINEA, X0_LINEA, X1_LINEA = 1046, 420, 1700
Y_SUBS_ARRIBA = 840  # por encima de aquí no llegan nunca los subtítulos (2 líneas de 60 px con MarginV 92)


def anadir_cartelas(ruta, bloques):
    """Cartela quieta de cada acto: fondo negro (lo pone el plano negro), año grande y nombre del acto."""
    ev = []
    for b in bloques:
        c = b.get("cartela")
        if not c:
            continue
        a, z = P.ass_t(b["cartela_ini"] + 0.05), P.ass_t(b["cartela_ini"] + DUR_CARTELA - 0.05)
        ev.append(f"Dialogue: 5,{a},{z},CartAnio,,0,0,0,,{{\\an5\\pos(960,470)\\fad(120,160)}}{P.limpiar(c['anio'])}")
        if c.get("acto"):
            ev.append(f"Dialogue: 5,{a},{z},CartActo,,0,0,0,,{{\\an5\\pos(960,300)\\fad(120,160)}}{P.limpiar(c['acto'])}")
        ev.append(f"Dialogue: 5,{a},{z},Dibujo,,0,0,0,,{{\\pos(900,606)\\c{P.ACENTO}\\fad(120,160)\\p1}}m 0 0 l 120 0 120 6 0 6")
        ev.append(f"Dialogue: 5,{a},{z},CartTit,,0,0,0,,{{\\an5\\pos(960,680)\\fad(120,160)}}{P.limpiar(c['titulo'])}")
    if not ev:
        return
    txt = pathlib.Path(ruta).read_text(encoding="utf-8")
    estilos = ("Style: CartAnio,Bebas Neue Bold,300,&H0000D7FF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,8,0,1,0,0,5,0,0,0,1\n"
               "Style: CartActo,Montserrat Black,44,&H00A34FFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,6,0,1,0,0,5,0,0,0,1\n"
               "Style: CartTit,Montserrat Black,70,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,2,0,1,0,0,5,0,0,0,1\n")
    txt = txt.replace("Style: Dibujo,", estilos + "Style: Dibujo,", 1)
    pathlib.Path(ruta).write_text(txt.rstrip("\n") + "\n" + "\n".join(ev) + "\n", encoding="utf-8")


def x_anio(anio, a0, a1):
    return X0_LINEA + (X1_LINEA - X0_LINEA) * (anio - a0) / max(1, a1 - a0)


def anadir_linea(ruta, bloques, total):
    """Línea de tiempo fina abajo del todo, quieta: el punto rosa salta al año de cada bloque (sin animación)."""
    if not LINEA:
        return
    a0, a1 = LINEA[0][0], LINEA[-1][0]
    ev, fin = [], P.ass_t(total)
    ev.append(f"Dialogue: 1,{P.ass_t(0)},{fin},Dibujo,,0,0,0,,{{\\pos({X0_LINEA},{Y_LINEA - 1})\\c&HFFFFFF&\\alpha&H90&\\p1}}"
              f"m 0 0 l {X1_LINEA - X0_LINEA} 0 {X1_LINEA - X0_LINEA} 3 0 3")
    for anio, _ in LINEA:
        x = int(x_anio(anio, a0, a1))
        ev.append(f"Dialogue: 1,{P.ass_t(0)},{fin},Dibujo,,0,0,0,,{{\\pos({x - 4},{Y_LINEA - 4})\\c&HFFFFFF&\\alpha&H60&\\p1}}"
                  "m 4 0 b 6 0 8 2 8 4 b 8 6 6 8 4 8 b 2 8 0 6 0 4 b 0 2 2 0 4 0")
    ev.append(f"Dialogue: 1,{P.ass_t(0)},{fin},Linea,,0,0,0,,{{\\an6\\pos({X1_LINEA + 70},{Y_LINEA})\\alpha&H60&}}{a1}")
    nombres = dict(LINEA)
    for b in bloques:
        if not b.get("anio"):
            continue
        anio = int(b["anio"])
        x = int(x_anio(anio, a0, a1))
        a, z = P.ass_t(b["ini"]), P.ass_t(b["fin"])
        ev.append(f"Dialogue: 2,{a},{z},Dibujo,,0,0,0,,{{\\pos({X0_LINEA},{Y_LINEA - 1})\\c{P.ACENTO}\\p1}}"
                  f"m 0 0 l {x - X0_LINEA} 0 {x - X0_LINEA} 3 0 3")
        ev.append(f"Dialogue: 2,{a},{z},Dibujo,,0,0,0,,{{\\pos({x - 9},{Y_LINEA - 9})\\c{P.ACENTO}\\p1}}"
                  "m 9 0 b 14 0 18 4 18 9 b 18 14 14 18 9 18 b 4 18 0 14 0 9 b 0 4 4 0 9 0")
        etiqueta = b.get("etiqueta_linea") or f"{anio} · {nombres.get(anio, '')}".rstrip(" ·")
        ev.append(f"Dialogue: 2,{a},{z},Linea,,0,0,0,,{{\\an6\\pos({X0_LINEA - 24},{Y_LINEA})}}{P.limpiar(etiqueta)}")
    txt = pathlib.Path(ruta).read_text(encoding="utf-8")
    estilo = "Style: Linea,Montserrat ExtraBold,26,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,0,0,0,0,100,100,1,0,1,0,2,6,0,0,0,1\n"
    txt = txt.replace("Style: Dibujo,", estilo + "Style: Dibujo,", 1)
    pathlib.Path(ruta).write_text(txt.rstrip("\n") + "\n" + "\n".join(ev) + "\n", encoding="utf-8")


LINEA_ANIMADA = bool(LINEA) and os.environ.get("LINEA_ANIMADA", "1" if getattr(guion_vl, "LINEA_ANIMADA", False) else "0") == "1"
if LINEA_ANIMADA:
    import linea_tiempo as LT  # noqa: E402


def empezar_linea(bloques, total):
    """Fabrica la línea de tiempo animada (linea_tiempo.py) en otro hilo mientras se cortan los planos."""
    if not LINEA_ANIMADA:
        return None
    import threading
    nombres = {a: n for a, n in LINEA}
    eventos = []
    for b in bloques:
        if b.get("anio"):
            et = b.get("etiqueta_linea")
            nombre = et.split("·", 1)[-1].strip() if et else nombres.get(int(b["anio"]), "")
            eventos.append((b["ini"], int(b["anio"]), nombre))
    if not eventos:
        return None
    destino = TMP / "linea.mov"
    estado = {"ruta": None}

    def trabajo():
        t0 = time.time()
        try:
            LT.render([(a, n) for a, n in LINEA], eventos, total + 0.1, destino)
            estado["ruta"] = destino
            print(f"Línea de tiempo animada lista ({time.time() - t0:.0f} s)", flush=True)
        except Exception as e:  # noqa: BLE001
            print("No se ha podido hacer la línea de tiempo animada:", type(e).__name__, e, flush=True)
    hilo = threading.Thread(target=trabajo, daemon=True)
    hilo.start()
    return hilo, estado


def esperar_linea(h):
    if not h:
        return None
    hilo, estado = h
    hilo.join()
    return estado["ruta"]


def golpe():
    """Golpe grave + aire para las cartelas (hecho con código)."""
    n = int(1.2 * SR)
    tt = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (38 * tt + 70 * (1 - np.exp(-tt * 18)) / 18)) * np.exp(-tt * 3.5)
    aire = np.random.RandomState(3).randn(n) * np.exp(-((tt - 0.05) ** 2) / 0.02) * 0.25
    esp = np.fft.rfft(aire)
    esp *= 1 / (1 + (np.fft.rfftfreq(n, 1 / SR) / 2500) ** 2)
    x = 0.8 * boom + np.fft.irfft(esp, n)
    x /= np.max(np.abs(x)) + 1e-9
    return np.stack([x, x], axis=1).astype(np.float32) * 0.55


def comprobar_repetidos(bloques):
    """Ningún trozo puede salir dos veces en el vídeo (se prepara material de sobra para eso)."""
    vistos, rep = {}, []
    for b in bloques:
        for nombre, _ in b["plan"]:
            vistos.setdefault(nombre, []).append(b["id"])
    for nombre, donde in vistos.items():
        if len(donde) > 1:
            rep.append(f"{nombre}: {', '.join(donde)}")
    return rep


def informe_finales(bloques):
    """Antes de montar: el final de cada voz por separado (mp3 de los últimos 2,5 s, dibujo de la onda e informe)."""
    from PIL import Image, ImageDraw
    carpeta = OUT / "finales"
    carpeta.mkdir(parents=True, exist_ok=True)
    lineas, colas = [], []
    alto_f, ancho = 120, 900
    hoja = Image.new("RGB", (ancho + 220, alto_f * len(bloques)), (16, 16, 20))
    d = ImageDraw.Draw(hoja)
    for k, b in enumerate(bloques):
        x = b["audio"] if b["audio"].ndim == 1 else b["audio"].mean(axis=1)
        cola = x[-int(2.5 * SR):]
        colas.append(cola)
        colas.append(np.zeros(int(0.7 * SR), np.float32))
        esperado = " ".join(b["texto"].split()[-3:])
        oidas = " ".join(w for w, a, _ in b["ws"] if a < b["dur_voz"])
        oidas = " ".join(oidas.split()[-3:])
        estado = "REVISAR" if b.get("aviso_final") else "bien"
        lineas.append(f"{b['id']}: {estado} · guion «{esperado}» · oído «{oidas}» · recortado {b['cola_cortada']:.2f} s")
        y0 = k * alto_f
        d.text((8, y0 + 8), b["id"], fill=(255, 215, 0))
        d.text((8, y0 + 30), estado, fill=(120, 255, 120) if estado == "bien" else (255, 90, 90))
        if len(cola):
            pasos = np.array_split(np.abs(cola), ancho)
            pico = max(1e-6, float(np.max(np.abs(cola))))
            for i, trozo in enumerate(pasos):
                h = int((float(trozo.max()) if len(trozo) else 0) / pico * (alto_f / 2 - 10))
                d.line([(220 + i, y0 + alto_f // 2 - h), (220 + i, y0 + alto_f // 2 + h)], fill=(120, 190, 255))
        d.line([(220, y0 + alto_f - 1), (220 + ancho, y0 + alto_f - 1)], fill=(60, 60, 70))
        guardar_mp3(cola, carpeta / f"{b['id']}.mp3")
    hoja.save(carpeta / "ondas_finales.png")
    if colas:
        guardar_mp3(np.concatenate(colas), carpeta / "todas_las_colas.mp3")
    (carpeta / "informe_finales.txt").write_text("\n".join(lineas), encoding="utf-8")
    print("\n".join(lineas), flush=True)
    return [b["id"] for b in bloques if b.get("aviso_final")]


def guardar_mp3(x, destino):
    tmp = TMP / "cola.wav"
    with wave.open(str(tmp), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())
    P.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-q:a", "3", str(destino)])


def hms(s):
    s = int(round(s))
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def main():
    t0 = time.time()
    tb = tabla()
    bloques = [b for b in guion_vl.BLOQUES if not SOLO or b["id"] in SOLO]
    planos_en_linea(bloques, tb)
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
    malos = informe_finales(bloques)
    if os.environ.get("SOLO_VOCES") == "1":
        print("Solo el informe de los finales de voz (SOLO_VOCES=1).")
        sys.exit(1 if malos else 0)
    if malos and os.environ.get("FORZAR_FINALES") != "1":
        print("PARADO: revisa el final de estas voces antes de montar:", ", ".join(malos))
        sys.exit(3)
    ajustar_frase_lucia(tb)
    # 2) línea de tiempo (la pausa de después compensa lo recortado del final de la voz, para mantener el ritmo)
    t = 0.0
    for i, b in enumerate(bloques):
        b["ini"] = t
        c = 0.0
        if b.get("cartela"):
            b["cartela_ini"] = t
            c += DUR_CARTELA
        if b.get("intro_original"):
            o = tb[b["intro_original"]]
            b["intro_ini"], b["intro_fin"] = t + c, t + c + o["dur"]
            c += o["dur"]
        b["plan_ini"] = t + c
        b["voz_ini"] = t + c + ((0.15 if i == 0 else 0.5) if not c else 0.3)
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
    hilo_linea = empezar_linea(bloques, total)
    # 3) planos: se cortan en paralelo
    carpeta = TMP / "planos"
    carpeta.mkdir(exist_ok=True)
    tareas, lista_concat, k = [], [], 0
    for b in bloques:
        b["plan"] = (planificar_anclado if b.get("planos_en") else planificar)(b, b["vis_fin"] - b["plan_ini"], tb)
        if b.get("cartela"):
            k += 1
            destino = str(carpeta / f"{k:03d}_cartela.mp4")
            P.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}:d={DUR_CARTELA}",
                   "-c:v", "libx264", "-crf", "12", "-preset", "veryfast", "-pix_fmt", "yuv420p", destino])
            lista_concat.append(destino)
        if b.get("intro_original"):
            k += 1
            o = tb[b["intro_original"]]
            destino = str(carpeta / f"{k:03d}_{b['intro_original'].replace('@', '_').replace('+', '_')}.mp4")
            tareas.append((b["intro_original"], o, o["dur"], destino, 0))
            lista_concat.append(destino)
            if not DRY:
                b["intro_wav"] = TMP / f"intro_{b['id']}.wav"
                P.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{o['ini']:.2f}", "-t", f"{o['dur']:.2f}",
                       "-i", str(fuente(o["video"])), "-vn", "-ar", SR, "-ac", 2, "-c:a", "pcm_s16le", b["intro_wav"]])
        for nombre, dur in b["plan"]:
            k += 1
            destino = str(carpeta / f"{k:03d}_{nombre.replace('@', '_').replace('+', '_')}.mp4")
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
    repetidos = comprobar_repetidos(bloques)
    if repetidos:
        print("Trozos repetidos:\n  " + "\n  ".join(repetidos), flush=True)
        if os.environ.get("PERMITIR_REPETIDOS") != "1":
            (OUT / "repetidos.txt").write_text("\n".join(repetidos), encoding="utf-8")
            print("PARADO: hay trozos repetidos (añade más material o planos al guion).")
            sys.exit(2)
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
    P.escribir_ass(TMP / "rotulos.ass", [dict(b, ini=b["plan_ini"]) for b in bloques], total)
    anadir_cta(TMP / "rotulos.ass", bloques)
    anadir_rotulos(TMP / "rotulos.ass", bloques)
    anadir_cartelas(TMP / "rotulos.ass", bloques)
    if not LINEA_ANIMADA:
        anadir_linea(TMP / "rotulos.ass", bloques, total)
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
        if b.get("intro_original"):
            mudo[int(b["intro_ini"] * 100):int(b["intro_fin"] * 100)] = 0
            if "intro_wav" in b:
                o = P.fundir(P.leer_wav(b["intro_wav"]), 0.06, 0.15)
                i0 = int(b["intro_ini"] * SR)
                orig[i0:i0 + len(o)] += o[: n - i0] * 0.95
        if b.get("cartela"):
            g = golpe()
            i0 = int(b["cartela_ini"] * SR)
            orig[i0:i0 + len(g)] += g[: max(0, n - i0)]
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
    linea_mov = esperar_linea(hilo_linea)
    capa_linea = (f"[3:v]format=rgba[lt];[v1][lt]overlay=0:{LT.Y0}:eof_action=pass[v1b];" if linea_mov else "")
    grafo = (f"[0:v]tpad=stop_mode=clone:stop_duration=3,eq=contrast=1.04:saturation=1.08,unsharp=5:5:0.4:5:5:0.0[v0];"
             f"[2:v]format=rgba[g];[v0][g]overlay=0:{H - P.ALTO_DEGRADADO}:shortest=1[v1];"
             + capa_linea + f"[{'v1b' if linea_mov else 'v1'}]ass={TMP / 'rotulos.ass'}[v]")
    final = HQ / "video_largo.mp4"
    P.run(["ffmpeg", "-y", "-loglevel", "error", "-i", TMP / "sin_audio.mp4", "-i", TMP / "mezcla.wav",
           "-loop", "1", "-framerate", FPS, "-i", TMP / "degradado.png", *(["-i", linea_mov] if linea_mov else []),
           "-filter_complex", grafo, "-map", "[v]",
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
