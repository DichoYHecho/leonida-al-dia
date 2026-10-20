"""Comprueba en Buffer (solo lectura) que cada publicación «Publicado» salió de verdad en las 3 redes
y lo escribe en «Comprobación»: ✅ todo bien, ⚠️ con el error de Buffer, ⏳ aún enviándose."""
import json, os, re, unicodedata
from datetime import datetime, timedelta, timezone
import requests
import airtable
from config import MADRID, T_PUB, CANAL_IG, CANAL_TT, CANAL_YT

RED = {CANAL_IG: "Reel", CANAL_TT: "TikTok", CANAL_YT: "YouTube"}
ORDEN = ["Reel", "TikTok", "YouTube"]
DIAS = int(os.environ.get("DIAS") or 4)
CAMPOS = "id status channelId text sentAt dueAt createdAt error { message }"


def buffer(query):
    r = requests.post("https://api.buffer.com", timeout=60, json={"query": query},
                      headers={"Authorization": f"Bearer {os.environ['BUFFER_API_KEY']}", "Content-Type": "application/json"})
    r.raise_for_status()
    d = r.json()
    if d.get("errors"):
        raise SystemExit("Error de la API de Buffer: " + json.dumps(d["errors"], ensure_ascii=False)[:400])
    return d["data"]


def posts(desde):
    org = buffer("query { account { organizations { id } } }")["account"]["organizations"][0]["id"]
    out, after = [], None
    for _ in range(5):
        pag = f"after: {json.dumps(after)}, " if after else ""
        q = ("query { posts(first: 100, " + pag + f"input: {{ organizationId: {json.dumps(org)}, filter: {{ "
             f"status: [sent, sending, scheduled, error, draft, needs_approval], createdAt: {{ start: {json.dumps(desde)} }} }}, "
             "sort: [{ field: createdAt, direction: desc }] }) " + f"{{ edges {{ node {{ {CAMPOS} }} }} pageInfo {{ hasNextPage endCursor }} }} }}")
        p = buffer(q)["posts"]
        out += [e["node"] for e in p["edges"]]
        if not p["pageInfo"]["hasNextPage"]:
            break
        after = p["pageInfo"]["endCursor"]
    return out


def norm(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", s or "").lower()).strip()


def lista(n):
    n = [x for x in ORDEN if x in n]
    return n[0] if len(n) == 1 else ", ".join(n[:-1]) + " y " + n[-1]


def resultado(f, ps):
    cap = norm(f.get("Caption"))[:120]
    suyos = [p for p in ps if cap and norm(p.get("text")).startswith(cap[:80])]
    if not suyos:
        return None
    rango = {"sent": 3, "sending": 2, "scheduled": 2, "needs_approval": 1, "draft": 1, "error": 0}
    mejor = {}
    for p in suyos:
        c = RED.get(p.get("channelId"))
        if c and (c not in mejor or rango.get(p["status"], 0) > rango.get(mejor[c]["status"], 0)):
            mejor[c] = p
    t = (suyos[0].get("sentAt") or suyos[0].get("createdAt") or "").replace("Z", "+00:00")
    hora = datetime.fromisoformat(t).astimezone(MADRID).strftime("%d/%m %H:%M") if t else "?"
    bien = [c for c in ORDEN if c in mejor and mejor[c]["status"] == "sent"]
    enviando = [c for c in ORDEN if c in mejor and mejor[c]["status"] in ("sending", "scheduled")]
    fallos = []
    for c in ORDEN:
        p = mejor.get(c)
        if p is None:
            fallos.append(f"{c}: no está en Buffer")
        elif p["status"] in ("error", "draft", "needs_approval"):
            fallos.append(f"{c}: {((p.get('error') or {}).get('message') or p['status'])[:120]}")
    if fallos:
        txt = f"⚠️ {hora} · " + " · ".join(fallos) + (f" · Bien: {lista(bien)}" if bien else "")
    elif enviando:
        txt = f"⏳ {hora} · Aún enviándose: {lista(enviando)}"
    else:
        txt = f"✅ {hora} · {lista(bien)} publicados"
    return txt[:250]


def main():
    formula = "AND({Estado}='Publicado', OR({Comprobación}='', FIND('⏳', {Comprobación}), FIND('⚠', {Comprobación})))"
    pubs = airtable.listar(T_PUB, ["Titular", "Caption", "Comprobación"], formula=formula)
    print(f"Publicaciones por comprobar: {len(pubs)}")
    if not pubs:
        return
    desde = (datetime.now(timezone.utc) - timedelta(days=DIAS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    ps = posts(desde)
    cambios = []
    for p in pubs:
        txt = resultado(p["fields"], ps)
        print(f"- {p['fields'].get('Titular')}: {txt or 'no encontrada en Buffer'}")
        if txt and txt != p["fields"].get("Comprobación"):
            cambios.append((p["id"], {"Comprobación": txt}))
    airtable.actualizar(T_PUB, cambios)


if __name__ == "__main__":
    main()
