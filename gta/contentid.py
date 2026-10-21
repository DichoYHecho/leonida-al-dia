"""Prueba de Content ID (fase G4): el mismo vídeo en dos versiones, con trozos de «Una mirada extendida»
(vídeo oficial de Rockstar Games, 27 ago 2026) de fondo y nuestra voz encima:
  A) con el sonido del vídeo oficial bajo, debajo de nuestra voz;
  B) con nuestra música synthwave, sin el sonido del vídeo oficial.
Sin SUBIR=true solo se montan los vídeos (se guardan como artefacto para verlos).
Con SUBIR=true se suben EN PRIVADO a YouTube (con Buffer, solo el canal de YouTube) para ver qué dice la
comprobación de derechos de autor. No se publica nada en Instagram ni en TikTok. Cada vídeo deja una fila
«Descartado» en Airtable (Buffer descarga el vídeo desde allí). La voz es Piper (no gasta Gemini)."""
import json, os, subprocess, sys, tempfile
from datetime import datetime, timezone
import numpy as np, requests, soundfile as sf
from PIL import Image
import render, voz
from config import UA, CANAL_YT, YT_CATEGORIA, T_PUB, MADRID, cuenta_atras

FUENTE = os.environ.get("FUENTE_VIDEO") or "https://videos-rockstargames-com.akamaized.net/v4/rk721912/flv/es-es-1080p.mp4"
TROZOS = ["Prueba de sonido de Leónida al Día.", "Estas imágenes son de «Una mirada extendida»,",
          "el vídeo oficial de Rockstar Games.", "Lo usamos con nuestra voz encima.", "¿Se oye bien la voz?"]
SALIDA = "salida_contentid"
W, H, FPS = render.W, render.H, render.FPS


def entrada(src):
    """Opciones de FFmpeg para leer el vídeo oficial: si es una URL, solo se descargan los trozos que hacen falta
    (el archivo entero pesa unos 2 GB) y se reintenta si se corta la conexión."""
    if src.startswith("http"):
        return ["-user_agent", UA, "-reconnect", "1", "-reconnect_on_network_error", "1",
                "-reconnect_delay_max", "10", "-i", src]
    return ["-i", src]


def duracion(ruta):
    opciones = ["-user_agent", UA] if ruta.startswith("http") else []
    return float(subprocess.check_output(["ffprobe", "-v", "error", *opciones, "-show_entries", "format=duration",
                                          "-of", "csv=p=0", "-i", ruta]).decode().strip())


def fondo(src, dur, tmp):
    """3 trozos seguidos (al 30, 50 y 70 % del vídeo oficial), en vertical, y su sonido aparte."""
    total = duracion(src)
    largo = dur / 3
    partes = []
    for k, frac in enumerate((0.30, 0.50, 0.70)):
        p = os.path.join(tmp, f"trozo{k}.mkv")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{total * frac:.2f}", "-t", f"{largo + 0.1:.2f}",
                        *entrada(src), "-vf", f"scale=-2:{H},crop={W}:{H},fps={FPS}", "-c:v", "libx264", "-crf", "18",
                        "-preset", "veryfast", "-c:a", "pcm_s16le", "-ar", "44100", "-ac", "2", p],
                       check=True)
        partes.append(p)
    lista = os.path.join(tmp, "lista.txt")
    open(lista, "w").write("".join(f"file '{p}'\n" for p in partes))
    bg = os.path.join(tmp, "fondo.mkv")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", bg],
                   check=True)
    wav = os.path.join(tmp, "sonido_oficial.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", bg, "-vn", "-ar", "44100", "-ac", "2", wav], check=True)
    print(f"Trozos: {', '.join(f'{total * f:.0f} s' for f in (0.3, 0.5, 0.7))} de {total:.0f} s", flush=True)
    return bg, wav


def mezclar(voz_wav, dur, con_oficial, sonido_oficial, ruta):
    v, sr = sf.read(voz_wav, dtype="float32")
    if v.ndim > 1:
        v = v.mean(1)
    v = v / (np.max(np.abs(v)) + 1e-6) * 0.9
    msr = 44100
    v = np.interp(np.linspace(0, len(v) - 1, int(len(v) * msr / sr)), np.arange(len(v)), v)
    n = int(dur * msr)
    if con_oficial:
        o, osr = sf.read(sonido_oficial, dtype="float32")
        o = o if o.ndim > 1 else np.stack([o, o], 1)
        o = o[:n]
        o = np.pad(o, ((0, n - len(o)), (0, 0)))
        fondo_audio = o / (np.max(np.abs(o)) + 1e-6) * 0.30   # bajo, debajo de la voz
    else:
        m, _ = render.musica(dur, 3)
        fondo_audio = m[:n] * 0.16
    mezcla = fondo_audio.copy()
    mezcla[:len(v)] += v[:n, None] * 0.95
    mezcla = mezcla / max(1.0, np.max(np.abs(mezcla)) / 0.95)
    sf.write(ruta, mezcla.astype(np.float32), msr)


def montar(bg, audio, tiempos, salida, etiqueta, pie):
    fija = render.capa_fija({"cuenta": cuenta_atras(datetime.now(MADRID).date()), "etiqueta": etiqueta, "tipo": "Noticia", "pie": pie})
    fg, fs, fc = render.fuente(render.FB, 74), render.fuente(render.FB, 64), render.fuente(render.FB, 66)
    dur = len(sf.read(audio)[0]) / 44100
    nframes = int(dur * FPS)

    def codificar(maxrate):
        dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", bg, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                               stdout=subprocess.PIPE)
        enc = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
             "-r", str(FPS), "-i", "-", "-i", audio, "-c:v", "libx264", "-preset", "medium", "-crf", "24",
             "-maxrate", f"{maxrate}k", "-bufsize", f"{2 * maxrate}k", "-pix_fmt", "yuv420p", "-c:a", "aac",
             "-b:a", "128k", "-shortest", "-movflags", "+faststart", salida], stdin=subprocess.PIPE)
        ultimo = None
        for i in range(nframes):
            raw = dec.stdout.read(W * H * 3)
            if len(raw) == W * H * 3:
                ultimo = raw
            img = Image.frombytes("RGB", (W, H), ultimo).convert("RGBA")
            img = Image.alpha_composite(img, fija)
            t = i / FPS
            j = next((q for q, (x0, x1) in enumerate(tiempos) if x0 - 0.05 <= t < x1 + 0.25), None)
            if j == 0 or t < tiempos[0][0]:
                render.texto_centrado(img, TROZOS[0], 430, fg, render.WHITE, caja=(10, 14, 38, 200), borde=0)
            elif (j is not None and j == len(TROZOS) - 1) or t >= tiempos[-1][0]:
                render.texto_centrado(img, TROZOS[-1], 560, fc, render.AMBER, caja=(10, 14, 38, 210), borde=0)
            elif j is not None:
                render.texto_centrado(img, TROZOS[j], 1300, fs, render.WHITE, borde=7)
            enc.stdin.write(img.convert("RGB").tobytes())
        enc.stdin.close()
        enc.wait()
        dec.kill()
        if enc.returncode:
            raise RuntimeError("FFmpeg no pudo montar el vídeo")
        return os.path.getsize(salida) / 1e6

    mb = codificar(1300)
    if mb > render.MAX_MB:
        mb = codificar(int(1300 * render.MAX_MB / mb * 0.85))
    print(f"  {os.path.basename(salida)}: {dur:.1f} s, {mb:.2f} MB", flush=True)


# ---------------------------------------------------------------- subida privada a YouTube
def buffer(query, variables=None):
    clave = os.environ.get("BUFFER_API_KEY")
    if not clave:
        raise SystemExit("Falta el secret BUFFER_API_KEY")
    r = requests.post("https://api.buffer.com", timeout=120, json={"query": query, "variables": variables or {}},
                      headers={"Authorization": f"Bearer {clave}", "Content-Type": "application/json"})
    r.raise_for_status()
    return r.json()


def privado():
    """Comprueba en la propia API de Buffer cómo se dice «privado»; si no está claro, no sube nada."""
    d = buffer('{ p: __type(name: "YoutubePrivacy") { enumValues { name } } '
               'm: __type(name: "YoutubePostMetadataInput") { inputFields { name } } }')
    valores = [v["name"] for v in (((d.get("data") or {}).get("p") or {}).get("enumValues") or [])]
    campos = [c["name"] for c in (((d.get("data") or {}).get("m") or {}).get("inputFields") or [])]
    print(f"Buffer · privacidad: {valores} · campos de YouTube: {campos}", flush=True)
    priv = [v for v in valores if v.lower() == "private"]
    if not priv or "privacy" not in campos or "notifySubscribers" not in campos:
        raise SystemExit("No se pudo confirmar la opción «privado» de Buffer: no se sube nada")
    return priv[0]


def subir(videos):
    import airtable, video
    priv = privado()
    ahora = datetime.now(timezone.utc).isoformat(timespec="seconds")
    regs = airtable.crear(T_PUB, [{"Titular": f"PRUEBA Content ID {v}: {txt}", "Estado": "Descartado", "Tipo": "Noticia",
                                   "Avisos": "Prueba privada de derechos de autor en YouTube. No publicar.",
                                   "Creada": ahora} for v, txt, _ in videos])
    mutacion = """mutation P($text: String!, $video: String!, $titulo: String!) {
 youtube: createPost(input: { text: $text, channelId: "%s", schedulingType: automatic, mode: shareNow,
   assets: [ { video: { url: $video } } ],
   metadata: { youtube: { title: $titulo, categoryId: "%s", privacy: %s, notifySubscribers: false,
                          madeForKids: false, isAiGenerated: true } } })
   { ... on PostActionSuccess { post { id status } } ... on MutationError { message } }
}""" % (CANAL_YT, YT_CATEGORIA, priv)
    resumen = []
    for r, (v, txt, ruta) in zip(regs, videos):
        adj = video.subir(r["id"], ruta)
        if not adj or not adj.get("url"):
            raise SystemExit("Airtable no devolvió la URL del vídeo")
        d = buffer(mutacion, {"text": f"Prueba privada {v} ({txt}). No es una publicación.",
                              "video": adj["url"], "titulo": f"Prueba privada {v} – {txt}"})
        res = (d.get("data") or {}).get("youtube") or {}
        estado = res.get("post") or res.get("message") or json.dumps(d.get("errors"))[:300]
        print(f"YouTube (privado) {v}: {estado}", flush=True)
        resumen.append(f"- {v} ({txt}): {estado}")
    s = os.environ.get("GITHUB_STEP_SUMMARY")
    if s:
        open(s, "a").write("## Prueba de Content ID (subida en privado)\n\n" + "\n".join(resumen) +
                           "\n\nMira «Restricciones» en YouTube Studio › Contenido dentro de 15-30 minutos.\n")


def main():
    os.makedirs(SALIDA, exist_ok=True)
    tmp = tempfile.mkdtemp()
    src = FUENTE
    voz_wav = os.path.join(tmp, "voz.wav")
    tiempos = voz.piper(TROZOS, voz_wav)
    dur = len(sf.read(voz_wav)[0]) / voz.SR + 1.2
    for intento in range(3):
        try:
            bg, oficial = fondo(src, dur, tmp)
            break
        except subprocess.CalledProcessError:
            if intento == 2:
                raise
            print("  La lectura del vídeo oficial falló; se reintenta…", flush=True)
    pie = "Fuente: Rockstar Games · Imágenes y sonido: Rockstar Games · Voz: sharvard (CC BY 3.0)"
    videos = []
    for v, txt, con in (("A", "con el sonido del vídeo oficial", True), ("B", "con nuestra música", False)):
        audio = os.path.join(tmp, f"mezcla_{v}.wav")
        mezclar(voz_wav, dur, con, oficial, audio)
        salida = os.path.join(SALIDA, f"prueba-contentid-{v}.mp4")
        montar(bg, audio, tiempos, salida, "PRUEBA " + v, pie if con else pie.replace(" y sonido", ""))
        videos.append((v, txt, salida))
    if os.environ.get("SUBIR") == "true":
        subir(videos)
    else:
        print("Solo montaje (SUBIR no es true): no se sube nada.")


if __name__ == "__main__":
    main()
