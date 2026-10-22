"""YouTube con su API oficial (decidido el 22 oct). Lo que Buffer no deja hacer:
- Poner la pregunta del vídeo como primer comentario (desde el propio canal).
- Poner el idioma del vídeo y del audio en español.
(«Título del juego» no se puede poner con la API: sigue siendo a mano en YouTube Studio.)

Lo llama comprobar.py después de cada publicación; repasa los vídeos subidos en los últimos 2 días y solo hace lo que
falte (no comenta dos veces). Gasto: unas 110 unidades por vídeo de las 10.000 diarias gratis.
Necesita los secrets GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET y GOOGLE_REFRESH_TOKEN (cuenta adria.sanandreas);
si no están, no hace nada."""
import os, re, unicodedata
import requests

API = "https://www.googleapis.com/youtube/v3"


def token():
    ids = [os.environ.get(k) for k in ("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN")]
    if not all(ids):
        return None
    r = requests.post("https://oauth2.googleapis.com/token", timeout=30,
                      data={"client_id": ids[0], "client_secret": ids[1], "refresh_token": ids[2],
                            "grant_type": "refresh_token"})
    if r.status_code >= 400:
        raise RuntimeError(f"Google no dio acceso ({r.status_code}): {r.text[:200]}")
    return r.json()["access_token"]


def api(metodo, ruta, tok, **kw):
    r = requests.request(metodo, f"{API}/{ruta}", headers={"Authorization": f"Bearer {tok}"}, timeout=60, **kw)
    if r.status_code >= 400:
        raise RuntimeError(f"YouTube {r.status_code}: {r.text[:300]}")
    return r.json() if r.text else {}


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def subidos(tok, n=15):
    canal = api("GET", "channels", tok, params={"part": "id,contentDetails", "mine": "true"})["items"][0]
    lista = canal["contentDetails"]["relatedPlaylists"]["uploads"]
    items = api("GET", "playlistItems", tok, params={"part": "snippet,contentDetails", "playlistId": lista,
                                                     "maxResults": n})["items"]
    return canal["id"], [(i["contentDetails"]["videoId"], i["snippet"]["title"]) for i in items]


def comentado(tok, vid, canal):
    d = api("GET", "commentThreads", tok, params={"part": "snippet", "videoId": vid, "maxResults": 100})
    return any(t["snippet"]["topLevelComment"]["snippet"].get("authorChannelId", {}).get("value") == canal
               for t in d.get("items", []))


def en_espanol(tok, vid):
    s = api("GET", "videos", tok, params={"part": "snippet", "id": vid})["items"][0]["snippet"]
    if s.get("defaultLanguage") == "es" and s.get("defaultAudioLanguage") == "es":
        return False
    nuevo = {k: s[k] for k in ("title", "description", "categoryId", "tags") if k in s}
    nuevo.update(defaultLanguage="es", defaultAudioLanguage="es")
    api("PUT", "videos", tok, params={"part": "snippet"}, json={"id": vid, "snippet": nuevo})
    return True


def comentar(tok, vid, texto):
    api("POST", "commentThreads", tok, params={"part": "snippet"},
        json={"snippet": {"videoId": vid, "topLevelComment": {"snippet": {"textOriginal": texto}}}})


def repasar(pubs):
    """pubs = [(título de YouTube, pregunta)] de lo publicado en los últimos 2 días. Devuelve líneas de resumen."""
    tok = token()
    if not tok:
        return ["YouTube: sin acceso a la API (faltan los secrets GOOGLE_*); se salta"]
    canal, videos = subidos(tok)
    out = []
    for titulo, pregunta in pubs:
        clave = norm(titulo)[:50]
        vid = next((v for v, t in videos if clave and norm(t).startswith(clave)), None)
        if not vid:
            out.append(f"YouTube: aún no encuentro «{titulo[:60]}»")
            continue
        hecho = []
        try:
            if en_espanol(tok, vid):
                hecho.append("idioma español")
            if pregunta and not comentado(tok, vid, canal):
                comentar(tok, vid, pregunta)
                hecho.append("pregunta comentada")
        except Exception as e:
            hecho.append(f"⚠️ {str(e)[:150]}")
        out.append(f"YouTube «{titulo[:60]}»: " + (", ".join(hecho) if hecho else "ya estaba todo"))
    return out
