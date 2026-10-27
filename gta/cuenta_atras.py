"""Vídeo diario de cuenta atrás para GTA 6, a las 17:00 (decidido el 22 oct).

- Se publica solo, sin aprobación: los números los calcula GitHub y el dato del día es el texto tal cual de un
  dato del banco (textos ya aprobados), sin pasar por Gemini.
- Cuenta hasta el jueves 19 de noviembre a las 00:00, hora de España: Rockstar no ha confirmado la hora de salida.
  La precarga digital empieza el 12 de noviembre (nota de prensa de Rockstar del 24 de junio de 2026).
- El dato del día se coge empezando por el final del banco, para no pisar a los datos de cada día (que van por
  orden desde el principio). Queda en Airtable como «Publicado» (Tipo Dato, etiqueta CUENTA ATRÁS).
- Desde el 19 de noviembre ya no hay cuenta atrás: a las 17:00 se publica la aprobada, como a las otras horas.
- Desde el 25 oct (edición V2): vídeo corto con el número gigante, la precarga, «DATO DEL DÍA» y el dato, y de fondo
  una captura distinta cada día (foto_del_dia), sin repetir hasta el lanzamiento.
- Con PRUEBA = true monta el vídeo en salida_cuenta/ y no toca Airtable (solo lee) ni publica."""
import csv, os, random, shutil, tempfile
from datetime import date, datetime, timezone
import airtable, medios, publicar, video
from config import AQUI, MADRID, T_PUB, HASHTAGS_FIJOS, PIE_POST

SALIDA = datetime(2026, 11, 19, 0, 0, tzinfo=MADRID)
PRECARGA = datetime(2026, 11, 12, 0, 0, tzinfo=MADRID)
PREGUNTAS = ["¿Lo vas a jugar el primer día?", "¿Cuántas horas vas a jugar el primer día?",
             "¿Qué es lo primero que vas a hacer en Vice City?", "¿Con quién tienes más ganas de jugar, Jason o Lucía?",
             "¿Qué es lo que más ganas tienes de ver?", "¿Coche, moto o lancha para recorrer Leónida?",
             "¿Cuánto tiempo llevas esperando GTA 6?"]
DIR_PRUEBA = os.path.join(os.path.dirname(AQUI), "salida_cuenta")


def partir(texto, maximo=42):
    """Trozos de subtítulo de como mucho «maximo» caracteres, sin partir palabras ni dejar al final de un trozo
    una palabra corta («el», «de», «y»…) o un número, que pasan al trozo siguiente."""
    out, cur = [], []
    for p in texto.split():
        if cur and len(" ".join(cur + [p])) > maximo:
            resto = []
            while len(cur) > 1 and (len(cur[-1]) <= 3 or cur[-1].isdigit()):
                resto.insert(0, cur.pop())
            out.append(" ".join(cur))
            cur = resto
        cur.append(p)
    if cur:
        out.append(" ".join(cur))
    return out


def banco():
    with open(os.path.join(AQUI, "banco_datos.csv"), encoding="utf-8") as f:
        return list(csv.DictReader(f))


INICIO_FOTOS = date(2026, 10, 21)


def foto_del_dia(dia):
    """Una captura principal distinta cada día (hay 73: no se repite hasta después del lanzamiento)."""
    lista = sorted(n for n, c in medios.CAPTURAS.items() if c["tipo"] == "captura" and c["uso"] == "principal")
    random.Random(6).shuffle(lista)
    return lista[(dia - INICIO_FOTOS).days % len(lista)]


def elegir_dato(usados, hoy):
    """El dato sin usar con el número más alto que siga siendo válido hoy."""
    for d in sorted(banco(), key=lambda x: -int(x["Orden"])):
        if int(d["Orden"]) in usados:
            continue
        if d.get("Válido hasta") and date.fromisoformat(d["Válido hasta"]) < hoy:
            continue
        return d
    return None


def textos(hoy, ahora, d):
    n = (SALIDA.date() - hoy).days
    p = (PRECARGA.date() - hoy).days
    resto = SALIDA - ahora
    dias, horas = resto.days, resto.seconds // 3600
    gancho = "¡GTA 6 sale mañana!" if n == 1 else f"¡Faltan {n} días para GTA 6!"
    if p > 1:
        precarga, corta = f"La precarga digital empieza en {p} días, el 12 de noviembre.", f"Precarga: 12 de noviembre (faltan {p} días)"
    elif p == 1:
        precarga, corta = "La precarga digital empieza mañana, el 12 de noviembre.", "Precarga: mañana, 12 de noviembre"
    elif p == 0:
        precarga, corta = "¡Hoy empieza la precarga digital!", "¡Hoy empieza la precarga!"
    else:
        precarga, corta = "La precarga digital ya está abierta.", "Precarga abierta desde el 12 de noviembre"
    voz_precarga = ("La precarga digital, el 12 de noviembre." if p > 1 else "¡La precarga digital empieza mañana!" if p == 1
                    else "¡Hoy empieza la precarga digital!" if p == 0 else "La precarga digital ya está abierta.")
    trozos = [gancho, "Y el dato del día:"] # 27 oct: sin la frase de la precarga (sigue en pantalla), para ir antes al dato + partir(d["Dato"]) + [PREGUNTAS[hoy.toordinal() % len(PREGUNTAS)]]
    return n, trozos, precarga, corta


def main():
    cuando = publicar.momento()  # la hora a la que sale (se prepara unos 45 min antes y se programa en Buffer)
    ahora = cuando or datetime.now(MADRID)
    hoy = ahora.date()
    if ahora >= SALIDA:
        print("GTA 6 ya ha salido: ya no hay cuenta atrás. A las 17:00 se publica la aprobada.")
        return publicar.main()
    prueba = os.environ.get("PRUEBA") == "true"
    regs = airtable.listar(T_PUB, ["Orden dato"], formula="{Tipo}='Dato'")
    usados = {int(r["fields"]["Orden dato"]) for r in regs if r["fields"].get("Orden dato") is not None}
    d = elegir_dato(usados, hoy)
    if not d:
        raise SystemExit("No quedan datos en el banco para la cuenta atrás")
    n, trozos, precarga, corta = textos(hoy, ahora, d)
    oficial = d["Estado"] == "Oficial"
    grupo = d.get("Imagen sugerida") if d.get("Imagen sugerida") in medios.GRUPOS else "Vice_City"
    caps = medios.elegir(grupo, d["Orden"], 1)
    caption = (f"Faltan {n} días para GTA 6: sale el jueves 19 de noviembre en PS5 y Xbox Series X|S. {precarga}\n"
               f"Dato del día: {d['Dato']}\n\n"
               "Cuenta atrás hasta las 00:00 (hora de España): Rockstar no ha confirmado la hora de salida.\n"
               f"Fuente del dato: {d['Fuente']}{'' if oficial else ' (según medios)'}\n{PIE_POST}\n\n"
               + " ".join(HASHTAGS_FIJOS + ["#CuentaAtras"]))
    f = {"Titular": f"Cuenta atrás: faltan {n} días (dato {d['Orden']})", "Estado": "Por Revisar", "Tipo": "Dato",
         "Info": "Oficial" if oficial else "Según medios", "Guion": "\n".join(trozos), "Etiqueta": "CUENTA ATRÁS",
         "Personaje": False, "Capturas": ", ".join(caps), "Caption": caption,
         "Título YouTube": f"Faltan {n} días para GTA 6: cuenta atrás y dato del día",
         "Fuente": d["Fuente"], "Enlace": d["Enlace"], "Texto de la fuente": d["Dato"], "Orden dato": int(d["Orden"]),
         "Creada": datetime.now(timezone.utc).isoformat(timespec="seconds"),
         "Avisos": "Cuenta atrás de las 17:00: se publica sola"}
    print(f"Cuenta atrás: faltan {n} días · dato {d['Orden']} · capturas {caps}", flush=True)
    carpeta = tempfile.mkdtemp()
    medios.preparar()
    intro = foto_del_dia(hoy)
    extra = {"cuenta_atras": {"de": n + 1, "a": n, "abajo": "DÍA PARA GTA 6" if n == 1 else "DÍAS PARA GTA 6",
                              "fecha": "JUEVES 19 DE NOVIEMBRE",
                              "precarga": "PRECARGA: 12 DE NOVIEMBRE" if (PRECARGA.date() - hoy).days >= 0 else "PRECARGA ABIERTA",
                              "trozos_intro": 1, "trozo_dato": 1, "fondo_intro": medios.ruta(intro),
                              "foco_intro": medios.CAPTURAS[intro]["foco"]}}
    print(f"Foto del día: {intro}", flush=True)
    ruta, info, cambios = video.montar(f, hoy, "cuenta-atras", carpeta, extra)
    if info["voz"].startswith("Piper"):
        f["Caption"] = f["Caption"].replace("\n\n#", "\nVoz: sharvard (CC BY 3.0)\n\n#", 1)
    print(f"Vídeo: {info}", flush=True)
    if prueba:
        os.makedirs(DIR_PRUEBA, exist_ok=True)
        shutil.copy(ruta, DIR_PRUEBA)
        open(os.path.join(DIR_PRUEBA, "guion.txt"), "w").write(f["Guion"] + "\n\n" + f["Caption"])
        print("PRUEBA: no se crea nada en Airtable ni se publica.")
        return
    rec = airtable.crear(T_PUB, [f])[0]
    try:
        adj = video.subir(rec["id"], ruta)
        if not adj or not adj.get("url"):
            raise RuntimeError("No se pudo subir el vídeo a Airtable")
        datos = publicar.buffer(publicar.mutacion(publicar.iso(cuando)) if cuando else publicar.MUTACION, publicar.variables(f["Caption"], f["Guion"], f["Título YouTube"], adj["url"]))
        res = datos.get("data") or {}
        bien = [k for k in ("reel", "tiktok", "youtube") if (res.get(k) or {}).get("post")]
        mal = {k: (res.get(k) or {}).get("message") or str(datos.get("errors"))[:200]
               for k in ("reel", "tiktok", "youtube") if k not in bien}
        print(f"Buffer: bien {bien}; fallos {mal}", flush=True)
        if not bien:
            raise RuntimeError(f"Buffer no aceptó la publicación: {mal}")
    except Exception as e:
        airtable.actualizar(T_PUB, [(rec["id"], {"Estado": "Descartado", "Avisos": f"Cuenta atrás no publicada: {str(e)[:300]}"})])
        raise
    cambios.update({"Estado": "Publicado", "Publicada": (cuando or datetime.now(MADRID)).astimezone(timezone.utc).isoformat(timespec="seconds"),
                    "Vídeo": [{"id": adj["id"]}] if adj.get("id") else [],
                    "Avisos": ("Cuenta atrás de las 17:00: se publica sola" + (f" · Buffer no aceptó: {mal}" if mal else ""))[:400]})
    airtable.actualizar(T_PUB, [(rec["id"], cambios)])
    s = os.environ.get("GITHUB_STEP_SUMMARY")
    if s:
        open(s, "a").write(f"## Cuenta atrás publicada\n\n- Faltan {n} días · dato {d['Orden']}\n- Redes: {', '.join(bien)}\n")
    print(f"Llamadas a Airtable: {airtable.LLAMADAS}")


if __name__ == "__main__":
    main()
