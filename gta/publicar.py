"""Publica la propuesta aprobada en Instagram (Reel), TikTok y YouTube Shorts con Buffer.

Elige: la noticia aprobada más reciente que no haya caducado; si no hay, el dato aprobado más antiguo.
Si el vídeo no es del día de hoy (la cuenta atrás cambia) o he cambiado algo en Airtable, lo vuelve a
montar antes (sin gastar voz). Si no hay nada aprobado, no publica nada."""
import json, os, re, sys, tempfile
from datetime import datetime, timedelta, timezone
import requests
import airtable, video
from config import MADRID, T_PUB, CANAL_IG, CANAL_TT, CANAL_YT, YT_CATEGORIA, CADUCA_HORAS

CAMPOS = ["Titular", "Estado", "Tipo", "Guion", "Etiqueta", "Personaje", "Capturas", "Caption", "Título YouTube",
          "Fuente", "Creada", "Orden dato", "Vídeo", "Para el día", "Huella vídeo", "Voz", "Avisos"]

MUTACION = """mutation Publicar($text: String!, $video: String!, $titulo: String!) {
 reel: createPost(input: { text: $text, channelId: "%s", schedulingType: automatic, mode: shareNow,
   assets: [ { video: { url: $video, metadata: { thumbnailOffset: 1000 } } } ],
   metadata: { instagram: { type: reel, shouldShareToFeed: true, isAiGenerated: true } } })
   { ... on PostActionSuccess { post { id status } } ... on MutationError { message } }
 tiktok: createPost(input: { text: $text, channelId: "%s", schedulingType: automatic, mode: shareNow,
   assets: [ { video: { url: $video, metadata: { thumbnailOffset: 1000 } } } ],
   metadata: { tiktok: { isAiGenerated: true } } })
   { ... on PostActionSuccess { post { id status } } ... on MutationError { message } }
 youtube: createPost(input: { text: $text, channelId: "%s", schedulingType: automatic, mode: shareNow,
   assets: [ { video: { url: $video } } ],
   metadata: { youtube: { title: $titulo, categoryId: "%s", isAiGenerated: true } } })
   { ... on PostActionSuccess { post { id status } } ... on MutationError { message } }
}""" % (CANAL_IG, CANAL_TT, CANAL_YT, YT_CATEGORIA)


def buffer(query, variables):
    clave = os.environ.get("BUFFER_API_KEY")
    if not clave:
        raise SystemExit("Falta el secret BUFFER_API_KEY")
    r = requests.post("https://api.buffer.com", timeout=120, json={"query": query, "variables": variables},
                      headers={"Authorization": f"Bearer {clave}", "Content-Type": "application/json"})
    r.raise_for_status()
    return r.json()


def elegir(regs, ahora):
    limite = ahora - timedelta(hours=CADUCA_HORAS)
    def creada(r):
        c = r["fields"].get("Creada")
        return datetime.fromisoformat(c.replace("Z", "+00:00")) if c else datetime(2000, 1, 1, tzinfo=timezone.utc)
    noticias = sorted([r for r in regs if r["fields"].get("Tipo") in ("Noticia", "Prensa") and creada(r) >= limite],
                      key=creada, reverse=True)
    datos = sorted([r for r in regs if r["fields"].get("Tipo") == "Dato"], key=creada)
    return (noticias + datos)[:1]


def main():
    ahora = datetime.now(timezone.utc)
    hoy = ahora.astimezone(MADRID).date()
    prueba = os.environ.get("PRUEBA") == "true"   # monta el vídeo pero no publica
    regs = airtable.listar(T_PUB, CAMPOS, formula="{Estado}='Aprobado'")
    elegida = elegir(regs, ahora)
    if not elegida:
        print("No hay ninguna propuesta aprobada: no se publica nada.")
        return
    r = elegida[0]
    f, rid = r["fields"], r["id"]
    print(f"Toca: {f.get('Tipo')} · {f.get('Titular')}", flush=True)

    adj = (f.get("Vídeo") or [None])[-1]
    cambios = {}
    if not adj or f.get("Huella vídeo") != video.huella_video(f, hoy):
        print("Se vuelve a montar el vídeo (día distinto o cambios en Airtable)…", flush=True)
        carpeta = tempfile.mkdtemp()
        ruta, info, cambios = video.montar(f, hoy, rid, carpeta)
        adj = video.subir(rid, ruta)
        print(f"Vídeo nuevo: {info}", flush=True)
    if not adj or not adj.get("url"):
        raise SystemExit("No hay vídeo que publicar")
    if prueba:
        print("PRUEBA: no se manda a Buffer.")
        return
    titulo = (f.get("Título YouTube") or f.get("Titular") or "GTA 6")[:100]
    d = buffer(MUTACION, {"text": f.get("Caption", ""), "video": adj["url"], "titulo": titulo})
    res = d.get("data") or {}
    bien = [k for k in ("reel", "tiktok", "youtube") if (res.get(k) or {}).get("post")]
    mal = {k: (res.get(k) or {}).get("message") or json.dumps(d.get("errors"))[:200]
           for k in ("reel", "tiktok", "youtube") if k not in bien}
    print(f"Buffer: bien {bien}; fallos {mal}", flush=True)
    if not bien:
        airtable.actualizar(T_PUB, [(rid, {"Avisos": f"Buffer rechazó la publicación: {json.dumps(mal, ensure_ascii=False)[:400]}"})])
        raise SystemExit("Buffer no aceptó la publicación en ninguna red")
    cambios.update({"Estado": "Publicado", "Publicada": ahora.isoformat(timespec="seconds"),
                    "Vídeo": [{"id": adj["id"]}] if adj.get("id") else f.get("Vídeo")})
    if mal:
        cambios["Avisos"] = f"Buffer no aceptó: {json.dumps(mal, ensure_ascii=False)[:400]}"
    airtable.actualizar(T_PUB, [(rid, cambios)])
    s = os.environ.get("GITHUB_STEP_SUMMARY")
    if s:
        open(s, "a").write(f"## Publicado\n\n- {f.get('Tipo')}: {f.get('Titular')}\n- Redes: {', '.join(bien)}\n"
                           + (f"- Fallos: {mal}\n" if mal else ""))
    print(f"Llamadas a Airtable: {airtable.LLAMADAS}")


if __name__ == "__main__":
    main()
