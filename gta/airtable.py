"""Llamadas a Airtable (la base «Panel GTA 6»). Agrupa los cambios para gastar pocas llamadas."""
import base64, os, time, urllib.parse
import requests
from config import BASE

TOKEN = os.environ.get("AIRTABLE_TOKEN", "")
API = f"https://api.airtable.com/v0/{BASE}"
LLAMADAS = 0


def pedir(method, url, **kw):
    global LLAMADAS
    if not TOKEN:
        raise SystemExit("Falta el secret AIRTABLE_TOKEN")
    for _ in range(4):
        LLAMADAS += 1
        r = requests.request(method, url, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=120, **kw)
        if r.status_code == 429:  # Airtable pide esperar 30 s
            time.sleep(31)
            continue
        if r.status_code >= 400:
            raise RuntimeError(f"Airtable {r.status_code}: {r.text[:400]}")
        return r.json() if r.text else {}
    raise RuntimeError("Airtable sigue contestando 429")


def tabla(nombre):
    return f"{API}/{urllib.parse.quote(nombre)}"


def listar(nombre, campos=None, formula=None, orden=None, desc=False, maximo=None):
    params = [("pageSize", "100")] + [("fields[]", c) for c in (campos or [])]
    if formula:
        params.append(("filterByFormula", formula))
    if orden:
        params += [("sort[0][field]", orden), ("sort[0][direction]", "desc" if desc else "asc")]
    regs, offset = [], None
    while True:
        p = params + ([("offset", offset)] if offset else [])
        d = pedir("GET", tabla(nombre), params=p)
        regs += d["records"]
        offset = d.get("offset")
        if not offset or (maximo and len(regs) >= maximo):
            return regs[:maximo] if maximo else regs


def crear(nombre, filas):
    """filas = [{campo: valor}]; devuelve los registros creados (de 10 en 10)."""
    out = []
    for i in range(0, len(filas), 10):
        d = pedir("POST", tabla(nombre), json={"records": [{"fields": f} for f in filas[i:i + 10]],
                                                "typecast": True})
        out += d["records"]
    return out


def actualizar(nombre, cambios):
    """cambios = [(rec_id, {campo: valor})], de 10 en 10."""
    for i in range(0, len(cambios), 10):
        lote = [{"id": r, "fields": f} for r, f in cambios[i:i + 10]]
        pedir("PATCH", tabla(nombre), json={"records": lote, "typecast": True})


def subir_adjunto(rec_id, campo, ruta, tipo):
    """Sube un archivo (máx. 5 MB) a un campo de adjuntos de la publicación."""
    datos = open(ruta, "rb").read()
    if len(datos) > 5_000_000:
        raise RuntimeError(f"{os.path.basename(ruta)} pesa {len(datos) / 1e6:.1f} MB (máximo 5)")
    url = f"https://content.airtable.com/v0/{BASE}/{rec_id}/{urllib.parse.quote(campo)}/uploadAttachment"
    d = pedir("POST", url, json={"contentType": tipo, "filename": os.path.basename(ruta),
                                 "file": base64.b64encode(datos).decode()})
    # La respuesta trae los adjuntos del campo (por su ID); el último es el que acabamos de subir
    listas = [v for v in (d.get("fields") or {}).values() if isinstance(v, list)]
    return listas[0][-1] if listas and listas[0] else None


def descargar(url, ruta):
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    open(ruta, "wb").write(r.content)
    return ruta


def esc(s):
    """Texto seguro dentro de una fórmula de Airtable entre comillas simples."""
    return (s or "").replace("\\", "\\\\").replace("'", "\\'")
