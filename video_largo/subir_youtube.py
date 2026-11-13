"""Sube un vídeo largo a YouTube EN PRIVADO y PROGRAMADO (publishAt), con el título, la descripción y las etiquetas de
su publicar.md y la miniatura A. Pedido por el usuario el 13 nov 2026 (vídeos 5-7: 14, 15 y 16 nov).

Uso: python subir_youtube.py PUBLICAR_MD VIDEO_MP4 MINIATURA_JPG PUBLICAR_EN_UTC   (p. ej. 2026-11-14T17:00:00Z)
Variables: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_YT_REFRESH_TOKEN (permiso del canal). PRUEBA=1 solo lee
publicar.md y enseña lo que subiría, sin tocar YouTube.

- Si ya hay un vídeo del canal con el mismo título, no sube otro (se puede relanzar sin duplicar).
- «Probar y comparar» (miniaturas B y C), el comentario fijado y la encuesta no tienen API: se hacen en YouTube Studio.
Gasto de cupo: unas 1.700 unidades por vídeo de las 10.000 diarias gratis."""
import json
import os
import re
import sys

try:
    import requests
except ImportError:  # la PRUEBA no lo necesita
    requests = None

API = "https://www.googleapis.com/youtube/v3"
CATEGORIA = "20"  # Gaming


def leer_publicar(ruta):
    t = open(ruta, encoding="utf-8").read().replace("\r", "")
    titulo = re.search(r"\*\*Título\*\*[^\n]*\n(.+)", t).group(1).strip()
    desc = re.search(r"\*\*Descripción:\*\*\s*\n(.*?)\n\*\*Etiquetas:\*\*", t, re.S).group(1).strip()
    etiquetas = [e.strip() for e in re.search(r"\*\*Etiquetas:\*\*\s*\n(.+)", t).group(1).split(",") if e.strip()]
    desc = desc.replace("<", "‹").replace(">", "›")  # YouTube no acepta < ni > en la descripción
    assert 0 < len(titulo) <= 100, f"título de {len(titulo)} caracteres"
    assert len(desc.encode("utf-8")) <= 5000, f"descripción de {len(desc.encode('utf-8'))} bytes"
    while len(",".join(etiquetas)) > 480:
        etiquetas.pop()
    return titulo, desc, etiquetas


def token():
    r = requests.post("https://oauth2.googleapis.com/token", timeout=30, data={
        "client_id": os.environ["GOOGLE_CLIENT_ID"], "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
        "refresh_token": os.environ["GOOGLE_YT_REFRESH_TOKEN"], "grant_type": "refresh_token"})
    r.raise_for_status()
    return r.json()["access_token"]


def api(metodo, ruta, tok, **kw):
    r = requests.request(metodo, f"{API}/{ruta}", headers={"Authorization": f"Bearer {tok}"}, timeout=120, **kw)
    if r.status_code >= 400:
        raise RuntimeError(f"YouTube {r.status_code}: {r.text[:500]}")
    return r.json() if r.text else {}


def ya_subido(tok, titulo):
    canal = api("GET", "channels", tok, params={"part": "contentDetails", "mine": "true"})["items"][0]
    lista = canal["contentDetails"]["relatedPlaylists"]["uploads"]
    items = api("GET", "playlistItems", tok, params={"part": "snippet,contentDetails", "playlistId": lista,
                                                     "maxResults": 50})["items"]
    return next((i["contentDetails"]["videoId"] for i in items if i["snippet"]["title"].strip() == titulo), None)


def subir(tok, mp4, cuerpo):
    tam = os.path.getsize(mp4)
    r = requests.post("https://www.googleapis.com/upload/youtube/v3/videos", timeout=120,
                      params={"uploadType": "resumable", "part": "snippet,status", "notifySubscribers": "true"},
                      headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=UTF-8",
                               "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(tam)},
                      data=json.dumps(cuerpo))
    if r.status_code >= 400:
        raise RuntimeError(f"YouTube {r.status_code}: {r.text[:500]}")
    url, hecho, trozo = r.headers["Location"], 0, 64 * 1024 * 1024
    with open(mp4, "rb") as f:
        while hecho < tam:
            f.seek(hecho)
            datos = f.read(trozo)
            fin = hecho + len(datos) - 1
            r = requests.put(url, data=datos, timeout=600, headers={
                "Authorization": f"Bearer {tok}", "Content-Range": f"bytes {hecho}-{fin}/{tam}"})
            if r.status_code in (200, 201):
                return r.json()
            if r.status_code != 308:
                raise RuntimeError(f"Subida {r.status_code}: {r.text[:500]}")
            rango = r.headers.get("Range")
            hecho = int(rango.split("-")[1]) + 1 if rango else 0
            print(f"  subido {hecho * 100 // tam} %", flush=True)
    raise RuntimeError("la subida terminó sin respuesta de YouTube")


def main():
    md, mp4, mini, cuando = sys.argv[1:5]
    titulo, desc, etiquetas = leer_publicar(md)
    print(f"Título: {titulo}\nEtiquetas ({len(etiquetas)}): {', '.join(etiquetas)}\nSe publica: {cuando}\n"
          f"Descripción ({len(desc)} caracteres):\n{desc}\n", flush=True)
    if os.environ.get("PRUEBA") == "1":
        print("PRUEBA: no se toca YouTube")
        return
    tok = token()
    vid = ya_subido(tok, titulo)
    if vid:
        print(f"Ya estaba subido: https://youtu.be/{vid} (no se sube otro)")
    else:
        cuerpo = {"snippet": {"title": titulo, "description": desc, "tags": etiquetas, "categoryId": CATEGORIA,
                              "defaultLanguage": "es", "defaultAudioLanguage": "es"},
                  "status": {"privacyStatus": "private", "publishAt": cuando, "selfDeclaredMadeForKids": False,
                             "embeddable": True, "license": "youtube"}}
        vid = subir(tok, mp4, cuerpo)["id"]
        print(f"Subido: https://youtu.be/{vid}", flush=True)
    with open(mini, "rb") as f:
        r = requests.post("https://www.googleapis.com/upload/youtube/v3/thumbnails/set", params={"videoId": vid},
                          headers={"Authorization": f"Bearer {tok}", "Content-Type": "image/jpeg"}, data=f.read(),
                          timeout=120)
    print("Miniatura:", "puesta" if r.status_code < 400 else f"NO ({r.status_code}: {r.text[:300]})", flush=True)
    v = api("GET", "videos", tok, params={"part": "status,snippet", "id": vid})["items"][0]
    st = v["status"]
    print("Estado en YouTube:", json.dumps(st, ensure_ascii=False))
    resumen = os.environ.get("GITHUB_STEP_SUMMARY")
    linea = (f"- {titulo}: https://youtu.be/{vid} · {st.get('privacyStatus')} · se publica {st.get('publishAt')} · "
             f"subida {st.get('uploadStatus')}\n")
    if resumen:
        open(resumen, "a", encoding="utf-8").write(linea)
    if st.get("privacyStatus") != "private" or not st.get("publishAt"):
        sys.exit("⚠️ YouTube no ha guardado la programación: revisar en YouTube Studio")


if __name__ == "__main__":
    main()
