"""Informe semanal (domingos por la noche, decidido el 22 oct): cómo les ha ido a las publicaciones de los últimos
7 días en cada red, con las cifras que da Buffer (solo lectura). Queda en Airtable como una fila de Tipo «Informe»
en «Por Revisar» (márcala como «Descartado» cuando la hayas leído) y en el resumen de la tarea de GitHub.

Buffer actualiza las cifras una vez al día y no todas las redes dan todas las cifras: lo que falta se indica."""
import json, os
from datetime import datetime, timedelta, timezone
import requests
import airtable
from config import MADRID, T_PUB, CANAL_IG, CANAL_TT, CANAL_YT

RED = {CANAL_IG: "Instagram", CANAL_TT: "TikTok", CANAL_YT: "YouTube"}
CIFRAS = [("views", "visualizaciones"), ("reach", "alcance"), ("reactions", "me gusta"), ("comments", "comentarios"),
          ("shares", "compartidos"), ("saves", "guardados"), ("follows", "seguidores nuevos")]
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def buffer(query, variables=None):
    r = requests.post("https://api.buffer.com", timeout=60, json={"query": query, "variables": variables or {}},
                      headers={"Authorization": f"Bearer {os.environ['BUFFER_API_KEY']}", "Content-Type": "application/json"})
    r.raise_for_status()
    d = r.json()
    if d.get("errors") and not d.get("data"):
        raise SystemExit("Error de la API de Buffer: " + json.dumps(d["errors"], ensure_ascii=False)[:400])
    return d


def enviados(desde, hasta):
    org = buffer("query { account { organizations { id } } }")["data"]["account"]["organizations"][0]["id"]
    out, after, avisos = [], None, []
    for _ in range(5):
        pag = f"after: {json.dumps(after)}, " if after else ""
        q = ("query { posts(first: 100, " + pag + f"input: {{ organizationId: {json.dumps(org)}, filter: {{ "
             f"status: [sent], createdAt: {{ start: {json.dumps(desde)} }} }}, "
             "sort: [{ field: createdAt, direction: desc }] }) "
             "{ edges { node { id channelId text sentAt metricsUpdatedAt metrics { type value unit } } } "
             "pageInfo { hasNextPage endCursor } } }")
        d = buffer(q)
        if d.get("errors"):
            avisos.append(json.dumps(d["errors"], ensure_ascii=False)[:300])
        p = (d.get("data") or {}).get("posts") or {"edges": [], "pageInfo": {}}
        out += [e["node"] for e in p["edges"] if e and e.get("node")]
        if not p["pageInfo"].get("hasNextPage"):
            break
        after = p["pageInfo"]["endCursor"]
    return out, avisos


def numero(n):
    return f"{int(round(n)):,}".replace(",", ".")


def titulo_de(texto):
    t = " ".join((texto or "").split())
    return (t[:70].rsplit(" ", 1)[0] + "…") if len(t) > 70 else t


def informe(posts):
    lineas = []
    for canal, red in RED.items():
        suyos = [p for p in posts if p.get("channelId") == canal]
        if not suyos:
            lineas.append(f"\n{red}: ninguna publicación enviada.")
            continue
        tot, con = {}, 0
        for p in suyos:
            m = {x["type"]: x["value"] for x in (p.get("metrics") or []) if x.get("unit") != "percentage"}
            con += bool(m)
            for k, _ in CIFRAS:
                if k in m:
                    tot[k] = tot.get(k, 0) + (m[k] or 0)
        lineas.append(f"\n{red}: {len(suyos)} publicaciones")
        if not tot:
            lineas.append("  Buffer no da cifras de esta red (o aún no las ha actualizado).")
            continue
        lineas.append("  " + " · ".join(f"{numero(tot[k])} {nombre}" for k, nombre in CIFRAS if k in tot))
        if con < len(suyos):
            lineas.append(f"  (cifras de {con} de {len(suyos)} publicaciones; las más nuevas tardan hasta 24 h)")
        clave = "views" if "views" in tot else ("reach" if "reach" in tot else None)
        if clave:
            def valor(p):
                return next((x["value"] or 0 for x in (p.get("metrics") or []) if x["type"] == clave), 0)
            mejores = sorted(suyos, key=valor, reverse=True)[:3]
            lineas.append(f"  Las que más {dict(CIFRAS)[clave]} han tenido:")
            for p in mejores:
                lineas.append(f"   - {numero(valor(p))}: {titulo_de(p.get('text'))}")
            media = tot[clave] / len(suyos)
            lineas.append(f"  Media por publicación: {numero(media)} {dict(CIFRAS)[clave]}")
    return lineas


def main():
    ahora = datetime.now(timezone.utc)
    desde_dt = ahora - timedelta(days=7)
    posts, avisos = enviados(desde_dt.strftime("%Y-%m-%dT%H:%M:%SZ"), ahora.strftime("%Y-%m-%dT%H:%M:%SZ"))
    a, b = desde_dt.astimezone(MADRID), ahora.astimezone(MADRID)
    periodo = f"{a.day} {MESES[a.month - 1]} - {b.day} {MESES[b.month - 1]}"
    cuerpo = [f"Publicaciones enviadas del {periodo} (cifras de Buffer, actualizadas una vez al día)."]
    cuerpo += informe(posts)
    if avisos:
        cuerpo.append("\nBuffer avisó de esto al pedir las cifras: " + " | ".join(avisos))
    texto = "\n".join(cuerpo)
    print(texto)
    s = os.environ.get("GITHUB_STEP_SUMMARY")
    if s:
        open(s, "a").write(f"## Informe semanal ({periodo})\n\n```\n{texto}\n```\n")
    if os.environ.get("PRUEBA") == "true":
        print("PRUEBA: no se crea nada en Airtable.")
        return
    airtable.crear(T_PUB, [{"Titular": f"📊 Informe semanal ({periodo})", "Estado": "Por Revisar", "Tipo": "Informe",
                            "Etiqueta": "INFORME", "Avisos": texto[:2000], "Texto de la fuente": texto[:3000],
                            "Creada": ahora.isoformat(timespec="seconds")}])


if __name__ == "__main__":
    main()
