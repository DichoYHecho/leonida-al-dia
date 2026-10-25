"""Noticias de GTA 6 de las últimas horas: RSS de medios fiables (aprobados en G2) y Rockstar Newswire."""
import calendar, html, json, re, time
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
import feedparser, requests
from config import FUENTES_RSS, GRAPH, HASH_LISTA, HASH_POST, UA

GTA6 = re.compile(r"\b(GTA\s?(6|VI)|Grand Theft Auto\s?(6|VI))\b", re.I)
FUERA = re.compile(r"\b(filtra\w*|leak\w*|rumou?r\w*|insider)\b", re.I)


class _Parrafos(HTMLParser):
    def __init__(self):
        super().__init__()
        self.dentro, self.ignorar, self.trozos, self.actual = 0, 0, [], []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "nav", "footer", "aside", "form"):
            self.ignorar += 1
        if tag in ("p", "h2", "h3", "li") and not self.ignorar:
            self.dentro += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "nav", "footer", "aside", "form") and self.ignorar:
            self.ignorar -= 1
        if tag in ("p", "h2", "h3", "li") and self.dentro:
            self.dentro -= 1
            t = re.sub(r"\s+", " ", "".join(self.actual)).strip()
            if len(t) > 40:
                self.trozos.append(t)
            self.actual = []

    def handle_data(self, data):
        if self.dentro and not self.ignorar:
            self.actual.append(data)


def texto_html(h):
    p = _Parrafos()
    p.feed(h or "")
    return "\n".join(p.trozos)


def texto_articulo(url, respaldo=""):
    """Texto del artículo (párrafos). Si la web no deja leerlo, se usa el resumen del RSS."""
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
        r.raise_for_status()
        t = texto_html(r.text)
        if len(t) > 300:
            return t[:8000]
    except Exception as e:
        print(f"  No se pudo leer {url}: {str(e)[:100]}")
    return respaldo


def rss(desde):
    out = []
    for medio, url in FUENTES_RSS:
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
            r.raise_for_status()
            feed = feedparser.parse(r.content)
        except Exception as e:
            print(f"RSS de {medio} no disponible: {str(e)[:100]}")
            continue
        for e in feed.entries:
            t = e.get("published_parsed") or e.get("updated_parsed")
            if not t:
                continue
            cuando = datetime.fromtimestamp(calendar.timegm(t), timezone.utc)
            titulo = html.unescape(e.get("title", "")).strip()
            resumen = texto_html(e.get("summary", "")) or re.sub(r"<[^>]+>", " ", e.get("summary", ""))
            contenido = ""
            if e.get("content"):
                contenido = texto_html(e["content"][0].get("value", ""))
            if cuando < desde or not GTA6.search(titulo + " " + resumen[:500]):
                continue
            if FUERA.search(titulo):
                continue
            out.append({"medio": medio, "titulo": titulo, "enlace": e.get("link", ""), "fecha": cuando,
                        "resumen": re.sub(r"\s+", " ", resumen)[:600], "contenido": contenido})
    return out


def _graph(op, variables, h):
    params = {"origin": "https://www.rockstargames.com", "operationName": op,
              "variables": json.dumps(variables, separators=(",", ":")),
              "extensions": json.dumps({"persistedQuery": {"version": 1, "sha256Hash": h}}, separators=(",", ":"))}
    r = requests.get(GRAPH, params=params, timeout=30,
                     headers={"User-Agent": UA, "Origin": "https://www.rockstargames.com",
                              "Referer": "https://www.rockstargames.com/"})
    r.raise_for_status()
    d = r.json()
    if d.get("errors"):
        raise RuntimeError(json.dumps(d["errors"])[:200])
    return d["data"]


def newswire(desde):
    """Noticias de GTA VI en rockstargames.com/es/newswire (en español)."""
    try:
        d = _graph("NewswireList", {"tagIdHash": "vi", "page": 1, "metaUrl": "/newswire", "limit": 20,
                                    "locale": "es_es"}, HASH_LISTA)
    except Exception as e:
        print(f"Rockstar Newswire no disponible (puede que Rockstar haya cambiado su web): {str(e)[:150]}")
        return []
    out = []
    for p in d["posts"]["results"]:
        try:
            cuando = datetime.strptime(p["created"], "%d/%m/%y %H:%M").replace(tzinfo=timezone.utc)
        except Exception:
            continue
        if cuando < desde:
            continue
        out.append({"medio": "Rockstar Games", "titulo": p["title"], "fecha": cuando, "id": p["id"],
                    "enlace": "https://www.rockstargames.com/es" + p["url"], "resumen": "", "contenido": ""})
    return out


def texto_newswire(id_hash):
    d = _graph("NewswirePost", {"locale": "es_es", "id_hash": id_hash}, HASH_POST)
    p = d["post"]
    trozos = [p.get("title", ""), p.get("subtitle", "")]

    def rec(o):
        if isinstance(o, str):
            t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", o))).strip()
            if len(t) > 40 and not re.match(r"https?:|.*\.(jpg|png|mp4)$", t):
                trozos.append(t)
        elif isinstance(o, dict):
            for v in o.values():
                rec(v)
        elif isinstance(o, list):
            for v in o:
                rec(v)

    rec(((p.get("tina") or {}).get("variables") or {}).get("keys"))
    vistos, out = set(), []
    for t in trozos:
        if t and t not in vistos:
            vistos.add(t)
            out.append(t)
    return "\n".join(out)[:8000]


def candidatas(horas=96):
    desde = datetime.now(timezone.utc) - timedelta(hours=horas)
    todas = newswire(desde) + rss(desde)
    todas.sort(key=lambda x: x["fecha"], reverse=True)
    return todas


def texto_de(c):
    if c["medio"] == "Rockstar Games" and c.get("id"):
        try:
            return texto_newswire(c["id"])
        except Exception as e:
            print(f"  No se pudo leer la noticia de Rockstar: {str(e)[:100]}")
            return c["titulo"]
    if len(c.get("contenido") or "") > 400:
        return c["contenido"][:8000]
    return texto_articulo(c["enlace"], respaldo=c.get("resumen") or c["titulo"])
