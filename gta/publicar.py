"""Publica la propuesta aprobada en Instagram (Reel), TikTok y YouTube Shorts con Buffer.

Elige: la noticia aprobada más reciente que no haya caducado; si no hay, el dato aprobado más antiguo.
Si el vídeo no es del día de hoy (la cuenta atrás cambia) o he cambiado algo en Airtable, lo vuelve a
montar antes (sin gastar voz). Si no hay nada aprobado, no publica nada."""
import json, os, re, sys, tempfile
from datetime import datetime, timedelta, timezone
import requests
import airtable, aviso, video
from config import MADRID, T_PUB, CANAL_IG, CANAL_TT, CANAL_YT, YT_CATEGORIA, CADUCA_HORAS

CAMPOS = ["Titular", "Estado", "Tipo", "Guion", "Etiqueta", "Personaje", "Capturas", "Caption", "Título YouTube",
          "Fuente", "Creada", "Orden dato", "Vídeo", "Para el día", "Huella vídeo", "Voz", "Avisos"]

BLOQUES = {
    "reel": """ reel: createPost(input: { text: $textq, channelId: "%s", schedulingType: automatic, MODO,
   assets: [ { video: { url: $video, metadata: { thumbnailOffset: 1000 } } } ],
   metadata: { instagram: { type: reel, shouldShareToFeed: true, isAiGenerated: true } } })
   { ... on PostActionSuccess { post { id status } } ... on MutationError { message } }
""" % CANAL_IG,
    "tiktok": """ tiktok: createPost(input: { text: $textq, channelId: "%s", schedulingType: automatic, MODO,
   assets: [ { video: { url: $video, metadata: { thumbnailOffset: 1000 } } } ],
   metadata: { tiktok: { isAiGenerated: true } } })
   { ... on PostActionSuccess { post { id status } } ... on MutationError { message } }
""" % CANAL_TT,
    "youtube": """ youtube: createPost(input: { text: $textq, channelId: "%s", schedulingType: automatic, MODO,
   assets: [ { video: { url: $video } } ],
   metadata: { youtube: { title: $titulo, categoryId: "%s", isAiGenerated: true } } })
   { ... on PostActionSuccess { post { id status } } ... on MutationError { message } }
""" % (CANAL_YT, YT_CATEGORIA)}


def mutacion(cuando=None, redes=("reel", "tiktok", "youtube")):
    """La publicación en las redes indicadas. cuando = None publica ya; si no, la deja programada en Buffer a esa
    hora (ISO en UTC, p. ej. «2026-11-18T23:00:00.000Z»). La pregunta del final va dentro del texto en las 3 redes:
    el primer comentario de Instagram es de pago en Buffer (lo vimos el 23 oct) y en YouTube la comenta youtube.py."""
    modo = f'mode: customScheduled, dueAt: "{cuando}"' if cuando else "mode: shareNow"
    cab = "mutation Publicar($textq: String!, $video: String!" + (", $titulo: String!" if "youtube" in redes else "") + ") {\n"
    return cab + "".join(BLOQUES[r].replace("MODO", modo) for r in redes) + "}"


MUTACION = mutacion()


def variables(caption, guion, titulo, video_url, redes=("reel", "tiktok", "youtube")):
    """Variables de la mutación. La pregunta es la última línea del guion que acaba en «?»."""
    caption = caption or ""
    preg = next((l.strip() for l in reversed((guion or "").splitlines()) if l.strip().endswith("?")), "")
    textq = caption
    if preg and preg not in caption:
        partes = caption.split("\n\n")
        # Detrás del primer párrafo si es largo (comprobar.py reconoce la publicación por su principio);
        # si no, justo antes de los hashtags
        donde = 1 if len(partes[0]) >= 90 or len(partes) < 3 else len(partes) - 1
        textq = "\n\n".join(partes[:donde] + [preg] + partes[donde:])
    v = {"textq": textq, "video": video_url}
    if "youtube" in redes:
        v["titulo"] = (titulo or "GTA 6")[:100]
    return v


def momento():
    """Hora a la que tiene que salir la publicación: PARA = «HH:MM» de Madrid (la pone el workflow, que se lanza
    unos 45 minutos antes y la deja programada en Buffer; decidido el 22 oct). None = publicar ya (si no hay PARA
    o ya ha pasado esa hora porque GitHub ha ido con retraso)."""
    para = os.environ.get("PARA")
    if not para:
        return None
    h, m = map(int, para.split(":"))
    ahora = datetime.now(MADRID)
    t = ahora.replace(hour=h, minute=m, second=0, microsecond=0)
    return t if t > ahora + timedelta(minutes=2) else None


def iso(t):
    return t.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


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


def reintentar(trozo, redes):
    """A mano (23 oct): vuelve a mandar a Buffer, ya mismo, una publicación ya «Publicado» solo a las redes que
    fallaron. trozo = un trozo del titular; redes = p. ej. «reel» o «reel,tiktok»."""
    regs = airtable.listar(T_PUB, CAMPOS, formula="{Estado}='Publicado'")
    r = next((x for x in sorted(regs, key=lambda x: x["fields"].get("Creada") or "", reverse=True)
              if trozo.lower() in (x["fields"].get("Titular") or "").lower()), None)
    if not r:
        raise SystemExit(f"No encuentro ninguna publicación «Publicado» con «{trozo}» en el titular")
    f = r["fields"]
    adj = (f.get("Vídeo") or [None])[-1]
    if not adj:
        raise SystemExit("Esa publicación no tiene vídeo")
    redes = tuple(x for x in ("reel", "tiktok", "youtube") if x in redes)
    titulo = (f.get("Título YouTube") or f.get("Titular") or "GTA 6")[:100]
    d = buffer(mutacion(None, redes), variables(f.get("Caption", ""), f.get("Guion"), titulo, adj["url"], redes))
    res = d.get("data") or {}
    bien = [k for k in redes if (res.get(k) or {}).get("post")]
    mal = {k: (res.get(k) or {}).get("message") or json.dumps(d.get("errors"))[:200] for k in redes if k not in bien}
    print(f"Reintento de «{f.get('Titular')}»: bien {bien}; fallos {mal}", flush=True)
    airtable.actualizar(T_PUB, [(r["id"], {"Comprobación": "", "Avisos": f"Reenviada a mano a {', '.join(bien)}" if bien else f"Reintento fallido: {mal}"})])
    if not bien:
        raise SystemExit("Buffer no aceptó el reintento")


def main():
    if os.environ.get("REINTENTAR"):
        return reintentar(os.environ["REINTENTAR"], os.environ.get("REDES") or "reel")
    ahora = datetime.now(timezone.utc)
    hoy = ahora.astimezone(MADRID).date()
    prueba = os.environ.get("PRUEBA") == "true"   # monta el vídeo pero no publica
    regs = airtable.listar(T_PUB, CAMPOS, formula="{Estado}='Aprobado'")
    elegida = elegir(regs, ahora)
    if not elegida:
        print("No hay ninguna propuesta aprobada: no se publica nada.")
        if not prueba and os.environ.get("GITHUB_EVENT_NAME") == "schedule":
            aviso.avisar(f"No se ha publicado nada a las {os.environ.get('PARA') or ahora.astimezone(MADRID).strftime('%H:%M')}",
                         "No había ninguna propuesta aprobada. Aprueba alguna en «Por Revisar» para la próxima hora.")
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
    cuando = momento()
    d = buffer(mutacion(iso(cuando)) if cuando else MUTACION, variables(f.get("Caption", ""), f.get("Guion"), titulo, adj["url"]))
    res = d.get("data") or {}
    bien = [k for k in ("reel", "tiktok", "youtube") if (res.get(k) or {}).get("post")]
    mal = {k: (res.get(k) or {}).get("message") or json.dumps(d.get("errors"))[:200]
           for k in ("reel", "tiktok", "youtube") if k not in bien}
    print(f"Buffer ({'programada para las ' + cuando.strftime('%H:%M') if cuando else 'publicada ya'}): bien {bien}; fallos {mal}", flush=True)
    if not bien:
        airtable.actualizar(T_PUB, [(rid, {"Avisos": f"Buffer rechazó la publicación: {json.dumps(mal, ensure_ascii=False)[:400]}"})])
        raise SystemExit("Buffer no aceptó la publicación en ninguna red")
    cambios.update({"Estado": "Publicado", "Publicada": (cuando or ahora).astimezone(timezone.utc).isoformat(timespec="seconds"),
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
