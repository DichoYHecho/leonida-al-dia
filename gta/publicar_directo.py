"""Programa en Buffer (Instagram Reel, TikTok y YouTube Shorts) los Shorts de gameplay sacados del directo del
19 nov 2026 (pedido por el usuario el 19 nov). Los vídeos están en la release «shorts-directo» del repo y los textos
y horas (Madrid) en gta/directo_shorts.json.

Diferencias con publicar.py: no usa Airtable; el vídeo es gameplay grabado por el usuario, sin voz ni imágenes
generadas, así que va con isAiGenerated: false.

Uso: python gta/publicar_directo.py <id|todos>   (PRUEBA=true: solo enseña lo que mandaría)
"""
import json
import os
import sys
from datetime import datetime, timezone

import requests

sys.path.insert(0, os.path.dirname(__file__))
from config import CANAL_IG, CANAL_TT, CANAL_YT, MADRID, YT_CATEGORIA  # noqa: E402

REPO = os.environ.get("GITHUB_REPOSITORY", "DichoYHecho/leonida-al-dia")
URL = f"https://github.com/{REPO}/releases/download/shorts-directo/{{id}}.mp4"

BLOQUES = """
 reel: createPost(input: { text: $textq, channelId: "%(ig)s", schedulingType: automatic, MODO,
   assets: [ { video: { url: $video, metadata: { thumbnailOffset: 1000 } } } ],
   metadata: { instagram: { type: reel, shouldShareToFeed: true, isAiGenerated: false } } })
   { ... on PostActionSuccess { post { id status } } ... on MutationError { message } }
 tiktok: createPost(input: { text: $textq, channelId: "%(tt)s", schedulingType: automatic, MODO,
   assets: [ { video: { url: $video, metadata: { thumbnailOffset: 1000 } } } ],
   metadata: { tiktok: { isAiGenerated: false } } })
   { ... on PostActionSuccess { post { id status } } ... on MutationError { message } }
 youtube: createPost(input: { text: $textq, channelId: "%(yt)s", schedulingType: automatic, MODO,
   assets: [ { video: { url: $video } } ],
   metadata: { youtube: { title: $titulo, categoryId: "%(cat)s", isAiGenerated: false } } })
   { ... on PostActionSuccess { post { id status } } ... on MutationError { message } }
""" % {"ig": CANAL_IG, "tt": CANAL_TT, "yt": CANAL_YT, "cat": YT_CATEGORIA}


def mutacion(cuando_utc):
    modo = f'mode: customScheduled, dueAt: "{cuando_utc}"' if cuando_utc else "mode: shareNow"
    return "mutation Publicar($textq: String!, $video: String!, $titulo: String!) {" + BLOQUES.replace("MODO", modo) + "}"


def main():
    que = sys.argv[1] if len(sys.argv) > 1 else "todos"
    prueba = os.environ.get("PRUEBA", "true") == "true"
    with open(os.path.join(os.path.dirname(__file__), "directo_shorts.json"), encoding="utf-8") as f:
        lista = json.load(f)
    if que != "todos":
        lista = [s for s in lista if s["id"] == que]
        if not lista:
            raise SystemExit(f"No hay ningún Short «{que}» en directo_shorts.json")
    ahora = datetime.now(timezone.utc)
    resumen, fallos = [], 0
    for s in lista:
        cuando = datetime.strptime(s["cuando"], "%Y-%m-%d %H:%M").replace(tzinfo=MADRID)
        cuando_utc = cuando.astimezone(timezone.utc)
        dentro = (cuando_utc - ahora).total_seconds() / 60
        due = cuando_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z") if dentro > 5 else None
        url = URL.format(id=s["id"])
        cab = requests.head(url, allow_redirects=True, timeout=60)
        print(f"\n== {s['id']}: {s['titulo']}\n   sale: {s['cuando']} Madrid ({'ya' if not due else due})\n   vídeo: {url} → {cab.status_code}, "
              f"{int(cab.headers.get('Content-Length', 0)) // 1_000_000} MB\n   texto:\n{s['texto']}", flush=True)
        if cab.status_code != 200:
            fallos += 1
            resumen.append(f"- {s['id']}: ⚠️ el vídeo no está en la release ({cab.status_code})")
            continue
        if prueba:
            resumen.append(f"- {s['id']}: PRUEBA (no se manda) · {s['cuando']}")
            continue
        r = requests.post("https://api.buffer.com", timeout=180,
                          json={"query": mutacion(due), "variables": {"textq": s["texto"], "video": url, "titulo": s["titulo"][:100]}},
                          headers={"Authorization": f"Bearer {os.environ['BUFFER_API_KEY']}", "Content-Type": "application/json"})
        r.raise_for_status()
        d = r.json()
        res = d.get("data") or {}
        bien = [k for k in ("reel", "tiktok", "youtube") if (res.get(k) or {}).get("post")]
        mal = {k: (res.get(k) or {}).get("message") or d.get("errors") for k in ("reel", "tiktok", "youtube") if k not in bien}
        print(f"   Buffer: bien {bien}; fallos {mal}", flush=True)
        if mal:
            fallos += 1
        resumen.append(f"- {s['id']} ({s['cuando']} Madrid): bien {', '.join(bien) or '—'}" + (f"; fallos {json.dumps(mal, ensure_ascii=False)[:300]}" if mal else ""))
    texto = "\n".join(resumen)
    print("\n" + texto)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8").write("### Shorts del directo\n" + texto + "\n")
    if fallos:
        raise SystemExit(f"{fallos} Short(s) con fallos")


if __name__ == "__main__":
    main()
