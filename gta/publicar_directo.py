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

BLOQUES = {
    "reel": """ reel: createPost(input: { text: $textq, channelId: "%s", schedulingType: automatic, MODO,
   assets: [ { video: { url: $video, metadata: { thumbnailOffset: 1000 } } } ],
   metadata: { instagram: { type: reel, shouldShareToFeed: true, isAiGenerated: false } } })
   { ... on PostActionSuccess { post { id status } } ... on MutationError { message } }
""" % CANAL_IG,
    "tiktok": """ tiktok: createPost(input: { text: $textq, channelId: "%s", schedulingType: automatic, MODO,
   assets: [ { video: { url: $video, metadata: { thumbnailOffset: 1000 } } } ],
   metadata: { tiktok: { isAiGenerated: false } } })
   { ... on PostActionSuccess { post { id status } } ... on MutationError { message } }
""" % CANAL_TT,
}

# YouTube va por su API y no por Buffer: Buffer solo deja programar 2 Shorts de YouTube al día y esos los usan los
# Shorts diarios (lo vimos el 19 nov). Se sube en privado con publishAt (o público si la hora ya pasó).
YT = "https://www.googleapis.com/youtube/v3"


def mutacion(cuando_utc, redes):
    modo = f'mode: customScheduled, dueAt: "{cuando_utc}"' if cuando_utc else "mode: shareNow"
    return "mutation Publicar($textq: String!, $video: String!) {\n" + "".join(BLOQUES[r].replace("MODO", modo) for r in redes) + "}"


def yt_token():
    r = requests.post("https://oauth2.googleapis.com/token", timeout=30, data={
        "client_id": os.environ["GOOGLE_CLIENT_ID"], "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
        "refresh_token": os.environ["GOOGLE_YT_REFRESH_TOKEN"], "grant_type": "refresh_token"})
    r.raise_for_status()
    return r.json()["access_token"]


def yt_ya_subido(tok, titulo):
    h = {"Authorization": f"Bearer {tok}"}
    canal = requests.get(f"{YT}/channels", headers=h, params={"part": "contentDetails", "mine": "true"}, timeout=60).json()
    lista = canal["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    items = requests.get(f"{YT}/playlistItems", headers=h, timeout=60,
                         params={"part": "snippet,contentDetails", "playlistId": lista, "maxResults": 50}).json().get("items", [])
    return next((i["contentDetails"]["videoId"] for i in items if i["snippet"]["title"].strip() == titulo.strip()), None)


def yt_subir(s, url, due):
    tok = yt_token()
    vid = yt_ya_subido(tok, s["titulo"])
    if vid:
        return f"ya estaba: https://youtu.be/{vid}"
    datos = requests.get(url, timeout=300).content
    estado = {"privacyStatus": "private", "publishAt": due} if due else {"privacyStatus": "public"}
    estado.update(selfDeclaredMadeForKids=False, embeddable=True, license="youtube")
    cuerpo = {"snippet": {"title": s["titulo"][:100], "description": s["texto"].replace("<", "‹").replace(">", "›"),
                          "tags": ["GTA 6", "GTA VI", "Grand Theft Auto VI", "gameplay GTA 6", "Leonida", "Vice City"],
                          "categoryId": YT_CATEGORIA, "defaultLanguage": "es", "defaultAudioLanguage": "es"},
              "status": estado}
    r = requests.post("https://www.googleapis.com/upload/youtube/v3/videos", timeout=120,
                      params={"uploadType": "resumable", "part": "snippet,status", "notifySubscribers": "true"},
                      headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=UTF-8",
                               "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(len(datos))},
                      data=json.dumps(cuerpo))
    r.raise_for_status()
    r = requests.put(r.headers["Location"], data=datos, timeout=900, headers={"Authorization": f"Bearer {tok}"})
    r.raise_for_status()
    vid = r.json()["id"]
    st = requests.get(f"{YT}/videos", headers={"Authorization": f"Bearer {tok}"}, params={"part": "status", "id": vid},
                      timeout=60).json()["items"][0]["status"]
    return f"https://youtu.be/{vid} · {st.get('privacyStatus')} · sale {st.get('publishAt') or 'ya'}"


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
        redes = [x.strip() for x in os.environ.get("REDES", "reel,tiktok,youtube").split(",") if x.strip()]
        bien, mal = [], {}
        en_buffer = [x for x in redes if x in BLOQUES]
        if en_buffer:
            r = requests.post("https://api.buffer.com", timeout=180,
                              json={"query": mutacion(due, en_buffer), "variables": {"textq": s["texto"], "video": url}},
                              headers={"Authorization": f"Bearer {os.environ['BUFFER_API_KEY']}", "Content-Type": "application/json"})
            r.raise_for_status()
            d = r.json()
            res = d.get("data") or {}
            bien += [k for k in en_buffer if (res.get(k) or {}).get("post")]
            mal.update({k: (res.get(k) or {}).get("message") or d.get("errors") for k in en_buffer if k not in bien})
        if "youtube" in redes:
            try:
                print(f"   YouTube: {yt_subir(s, url, due)}", flush=True)
                bien.append("youtube")
            except Exception as e:  # noqa: BLE001
                mal["youtube"] = str(e)[:300]
        print(f"   bien {bien}; fallos {mal}", flush=True)
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
