"""Crea en la base «Panel GTA 6» la tabla Publicaciones con todos sus campos (solo hace falta una vez;
si ya existe, añade los campos que falten). La vista Kanban «Revisión» se crea a mano en Airtable."""
import requests
from airtable import TOKEN
from config import BASE, T_PUB

META = f"https://api.airtable.com/v0/meta/bases/{BASE}/tables"
EUROPEA = {"dateFormat": {"name": "european"}}
FECHA_HORA = {"dateFormat": {"name": "european"}, "timeFormat": {"name": "24hour"}, "timeZone": "Europe/Madrid"}


def sel(*opciones):
    return {"choices": [{"name": n, "color": c} for n, c in opciones]}


CAMPOS = [
    ("Titular", "singleLineText", None, "Resumen de la propuesta"),
    ("Estado", "singleSelect", sel(("Por Revisar", "yellowLight2"), ("Aprobado", "greenLight2"), ("Publicado", "grayLight2"),
                                  ("Descartado", "redLight2"), ("Caducada", "grayLight1")), "Lo cambio yo al revisar"),
    ("Tipo", "singleSelect", sel(("Noticia", "cyanLight2"), ("Dato", "orangeLight2"), ("Prensa", "purpleLight2")), None),
    ("Info", "singleSelect", sel(("Oficial", "greenLight2"), ("Según medios", "blueLight2")), "Oficial = Rockstar o Take-Two"),
    ("Vídeo", "multipleAttachments", None, "Lo hace GitHub"),
    ("Avisos", "multilineText", None, "Lo escribe GitHub si hay algo que mirar"),
    ("Guion", "multilineText", None, "1.ª línea: gancho; después, los subtítulos; última: la pregunta. Si lo cambio, el vídeo se rehace solo"),
    ("Etiqueta", "singleLineText", None, "El tema que sale arriba (LUCÍA, VICE CITY…)"),
    ("Personaje", "checkbox", {"icon": "check", "color": "pinkBright"}, "Etiqueta rosa"),
    ("Capturas", "singleLineText", None, "Nombres de las capturas oficiales, separados por comas (ver gta/capturas.csv)"),
    ("Caption", "multilineText", None, "Texto de la publicación con la fuente y los hashtags (máx. 5)"),
    ("Título YouTube", "singleLineText", None, "Máximo 100 caracteres"),
    ("Fuente", "singleLineText", None, None),
    ("Enlace", "url", None, "La noticia o la fuente del dato"),
    ("Texto de la fuente", "multilineText", None, "Lo que leyó Gemini (para comprobar)"),
    ("Orden dato", "number", {"precision": 0}, "Número del dato en gta/banco_datos.csv"),
    ("Creada", "dateTime", FECHA_HORA, None),
    ("Para el día", "date", EUROPEA, "Día de la cuenta atrás del vídeo"),
    ("Publicada", "dateTime", FECHA_HORA, None),
    ("Comprobación", "singleLineText", None, "Lo escribe GitHub después de publicar"),
    ("Voz", "singleLineText", None, None),
    ("Huella", "singleLineText", None, "Uso interno"),
    ("Huella vídeo", "singleLineText", None, "Uso interno"),
    ("Tiempos", "multilineText", None, "Uso interno: tiempos de los subtítulos"),
]


def campo(n, t, o, d):
    c = {"name": n, "type": t}
    if o:
        c["options"] = o
    if d:
        c["description"] = d
    return c


def main():
    h = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    r = requests.get(META, headers=h, timeout=60)
    r.raise_for_status()
    tablas = {t["name"]: t for t in r.json()["tables"]}
    if T_PUB not in tablas:
        r = requests.post(META, headers=h, timeout=60, json={
            "name": T_PUB, "description": "Propuestas de vídeo de «Leónida al Día»",
            "fields": [campo(*c) for c in CAMPOS]})
        if r.status_code >= 400:
            raise SystemExit(f"Airtable {r.status_code}: {r.text[:500]}")
        print(f"Tabla {T_PUB} creada con {len(CAMPOS)} campos: {r.json()['id']}")
        return
    t = tablas[T_PUB]
    existentes = {f["name"] for f in t["fields"]}
    for c in CAMPOS:
        if c[0] not in existentes:
            r = requests.post(f"{META}/{t['id']}/fields", headers=h, timeout=60, json=campo(*c))
            print(f"Campo {c[0]}: {'creado' if r.ok else r.text[:200]}")
    print(f"Tabla {T_PUB} ({t['id']}) revisada.")


if __name__ == "__main__":
    main()
