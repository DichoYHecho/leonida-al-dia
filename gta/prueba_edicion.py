"""Prueba de la edición V2 (25 oct 2026): monta 3 vídeos con render2 SIN publicar ni cambiar Airtable (solo lee).

- Noticia: la publicación de Airtable cuyo titular contiene NOTICIA (por defecto «teletrabajo»).
- Dato: la publicación cuyo titular contiene DATO (por defecto «Boobie Ike»).
- Encuadre inteligente (encuadre.py): Gemini dice dónde están las caras o lo importante de cada imagen (1 vez por
  imagen; se guarda en la caché).
- Cuenta atrás de hoy, más corta: gancho, precarga, «Y el dato del día:», el dato y la pregunta (el mismo dato que
  elegiría la de las 17:00). Gasta 1 audio de Gemini; la noticia y el dato reutilizan su voz de la caché.
Deja los vídeos y una hoja de fotogramas en salida_edicion/."""
import os, random, shutil, sys, tempfile
from datetime import date, datetime
import numpy as np, soundfile as sf
from PIL import Image
import airtable, cuenta_atras as ca, encuadre, medios, render2, video, voz
from config import MADRID, T_PUB, cuenta_atras as pastilla_cuenta

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "salida_edicion")
INICIO_FOTOS = date(2026, 10, 21)


def foto_del_dia(dia):
    """Una captura principal distinta cada día (73: no se repite hasta después del lanzamiento)."""
    lista = sorted(n for n, c in medios.CAPTURAS.items() if c["tipo"] == "captura" and c["uso"] == "principal")
    random.Random(6).shuffle(lista)
    return lista[(dia - INICIO_FOTOS).days % len(lista)]


def palabras_whisper(wav, trozos):
    """Tiempos de cada palabra del guion (como las cuenta render2.tokens), con Whisper. None si no se puede."""
    try:
        from faster_whisper import WhisperModel
        import difflib
        x, sr = sf.read(wav, dtype="float32")
        if x.ndim > 1:
            x = x.mean(1)
        x16 = np.interp(np.linspace(0, len(x) - 1, int(len(x) * 16000 / sr)), np.arange(len(x)), x).astype(np.float32)
        segs, _ = WhisperModel("base", device="cpu", compute_type="int8").transcribe(x16, language="es", word_timestamps=True)
        oidas, t_oidas = [], []
        for s in segs:
            for w in s.words or []:
                for tok in voz.norm(w.word):
                    oidas.append(tok)
                    t_oidas.append((w.start, w.end))
        guion, de_pal = [], []
        palabras = [p for t in trozos for p in render2.tokens(t)]
        for i, p in enumerate(palabras):
            for tok in voz.norm(p):
                guion.append(tok)
                de_pal.append(i)
        tiempos = [None] * len(guion)
        for blk in difflib.SequenceMatcher(None, guion, oidas, autojunk=False).get_matching_blocks():
            for q in range(blk.size):
                tiempos[blk.a + q] = t_oidas[blk.b + q]
        if sum(t is not None for t in tiempos) < len(guion) * 0.6:
            return None
        conocidos = [i for i, t in enumerate(tiempos) if t]
        for i in range(len(guion)):
            if tiempos[i] is None:
                a = max((j for j in conocidos if j < i), default=None)
                b = min((j for j in conocidos if j > i), default=None)
                ta = tiempos[a][1] if a is not None else tiempos[b][0]
                tb = tiempos[b][0] if b is not None else ta
                tiempos[i] = (ta, tb)
        out = []
        for i, p in enumerate(palabras):
            idx = [k for k, d in enumerate(de_pal) if d == i]
            if idx:
                out.append((p, tiempos[idx[0]][0], tiempos[idx[-1]][1]))
            else:
                prev = out[-1][2] if out else 0.0
                out.append((p, prev, prev))
        return out
    except Exception as e:
        print(f"  (sin tiempos por palabra: {str(e)[:150]})", flush=True)
        return None


def hoja(nombre, dur, momentos):
    ims = []
    for t in momentos:
        if t < dur:
            ims.append(render2.montar.fotograma(int(t * render2.FPS)).resize((270, 480)))
    cols = 6
    filas = (len(ims) + cols - 1) // cols
    s = Image.new("RGB", (270 * cols, 480 * filas), "black")
    for i, im in enumerate(ims):
        s.paste(im, ((i % cols) * 270, (i // cols) * 480))
    s.save(os.path.join(OUT, f"hoja_{nombre}.jpg"), quality=85)


def montar(nombre, f, dia, extra=None):
    medios.preparar()
    caps, fondos = [], []
    for c in medios.validas(f.get("Capturas")):
        r = medios.ruta(c)
        if r.lower().endswith(".mp4"):  # el prototipo solo usa imágenes (los trozos y clips, más adelante)
            continue
        foco, plano = medios.foco_plano(c)
        suj = encuadre.sujetos(r, f.get("Titular") or (video.trozos_de(f) or [""])[0])
        print(f"  {nombre} · {c[:40]}: {[s['que'] for s in suj] or 'sin sujetos (foco de siempre)'}", flush=True)
        caps.append(c)
        fondos.append((r, foco, plano, [s["caja"] for s in suj]))
    if not caps:
        raise RuntimeError(f"{nombre}: sin imágenes")
    wav, tiempos, nombre_voz, _, _ = video.preparar_voz(f)
    trozos = video.trozos_de(f)
    pals = palabras_whisper(wav, trozos)
    tmp = tempfile.mkdtemp()
    try:
        cfg = {"trozos": trozos, "tiempos": tiempos, "voz": wav, "palabras": pals,
               "capturas": fondos,
               "etiqueta": f.get("Etiqueta"), "tipo": f.get("Tipo"), "personaje": f.get("Personaje"),
               "cuenta": pastilla_cuenta(dia), "pie": video.pie(f, nombre_voz.startswith("Piper"), False, caps),
               "salida": os.path.join(OUT, f"{nombre}.mp4"), "semilla": 3, "tmp": tmp}
        cfg.update(extra or {})
        info = render2.montar(cfg)
        d = info["duracion"]
        hoja(nombre, d, [0, 0.4, 0.7, 0.9, 1.5, d * 0.3, d * 0.45, d * 0.6, d * 0.75, d - 1.6, d - 0.6, d - 0.1])
        print(f"{nombre}: {info} · voz {nombre_voz} · palabras {'Whisper' if pals else 'repartidas'} · {len(caps)} imágenes", flush=True)
        return info
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def buscar(texto):
    regs = airtable.listar(T_PUB, ["Titular", "Guion", "Capturas", "Etiqueta", "Tipo", "Personaje", "Fuente", "Estado"],
                           formula=f"FIND(LOWER('{airtable.esc(texto)}'), LOWER({{Titular}}))", maximo=5)
    return regs[0]["fields"] if regs else None


def cuenta(dia):
    ahora = datetime.now(MADRID)
    regs = airtable.listar(T_PUB, ["Orden dato"], formula="{Tipo}='Dato'")
    usados = {int(r["fields"]["Orden dato"]) for r in regs if r["fields"].get("Orden dato") is not None}
    d = ca.elegir_dato(usados, dia)
    n = (ca.SALIDA.date() - dia).days
    p = (ca.PRECARGA.date() - dia).days
    gancho = "¡GTA 6 sale mañana!" if n == 1 else f"¡Faltan {n} días para GTA 6!"
    precarga = ("La precarga digital, el 12 de noviembre." if p > 1 else "¡La precarga digital empieza mañana!" if p == 1
                else "¡Hoy empieza la precarga digital!" if p == 0 else "La precarga digital ya está abierta.")
    trozos = [gancho, precarga, "Y el dato del día:"] + ca.partir(d["Dato"]) + [ca.PREGUNTAS[dia.toordinal() % len(ca.PREGUNTAS)]]
    grupo = d.get("Imagen sugerida") if d.get("Imagen sugerida") in medios.GRUPOS else "Vice_City"
    caps = medios.elegir(grupo, d["Orden"], 1)
    intro = foto_del_dia(dia)
    f = {"Guion": "\n".join(trozos), "Capturas": ", ".join(caps), "Etiqueta": "CUENTA ATRÁS", "Tipo": "Dato",
         "Personaje": False, "Fuente": d["Fuente"]}
    medios.preparar()
    extra = {"cuenta_atras": {"de": n + 1, "a": n, "fecha": "JUEVES 19 DE NOVIEMBRE",
                              "precarga": "PRECARGA: 12 DE NOVIEMBRE" if p >= 0 else "PRECARGA ABIERTA",
                              "trozos_intro": 2, "trozo_dato": 2, "fondo_intro": medios.ruta(intro),
                              "foco_intro": medios.CAPTURAS[intro]["foco"],
                              "sujetos_intro": [s["caja"] for s in encuadre.sujetos(medios.ruta(intro))]}}
    print(f"Cuenta atrás: faltan {n} · dato {d['Orden']} · foto del día {intro} · dato con {caps}", flush=True)
    return montar("cuenta_atras", f, dia, extra)


def main():
    os.makedirs(OUT, exist_ok=True)
    hoy = datetime.now(MADRID).date()
    fallos = []
    for nombre, texto in (("noticia", os.environ.get("NOTICIA") or "teletrabajo"),
                          ("dato", os.environ.get("DATO") or "Boobie Ike")):
        try:
            f = buscar(texto)
            if not f:
                raise RuntimeError(f"no encuentro en Airtable una publicación con «{texto}» en el titular")
            montar(nombre, f, hoy)
        except Exception as e:
            fallos.append(f"{nombre}: {e}")
            print(f"⚠️ {nombre}: {e}", flush=True)
    try:
        cuenta(hoy)
    except Exception as e:
        fallos.append(f"cuenta atrás: {e}")
        print(f"⚠️ cuenta atrás: {e}", flush=True)
    print(f"Llamadas a Airtable: {airtable.LLAMADAS}")
    if fallos:
        sys.exit("Fallos: " + " | ".join(fallos))


if __name__ == "__main__":
    main()
