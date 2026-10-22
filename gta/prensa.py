"""«La prensa opina» (decidido el 22 oct): vigila las notas de GTA 6 en OpenCritic y Metacritic y, cuando hay
notas nuevas, prepara una propuesta de Tipo «Prensa» para revisar (con su vídeo), como una noticia más.

- Solo usa las cifras públicas de las dos webs (nota media, número de reseñas, % que lo recomienda) y lo cuenta
  citándolas. No copia textos de las reseñas.
- Como mucho una propuesta cada 20 horas, y solo si las notas han cambiado desde la última.
- Si una web no contesta o cambia su página, se sigue con la otra (y si fallan las dos, no pasa nada).

Prueba: python gta/prensa.py  (solo enseña las notas que encuentra; no crea nada)."""
import html, json, re
from datetime import datetime, timedelta, timezone
import requests
from config import MADRID

OPENCRITIC = "https://opencritic.com/game/15398/grand-theft-auto-vi"
OPENCRITIC_ID = 15398
METACRITIC = "https://www.metacritic.com/game/grand-theft-auto-vi/"
NAVEGADOR = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/141.0 Safari/537.36", "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"}
CADA_HORAS = 20
NIVELES = {"Mighty": "Excelente («Mighty»)", "Strong": "Fuerte («Strong»)", "Fair": "Aceptable («Fair»)",
           "Weak": "Flojo («Weak»)"}


def _buscar(o, ok):
    """Recorre un JSON y devuelve el primer diccionario que cumple ok()."""
    if isinstance(o, dict):
        if ok(o):
            return o
        o = list(o.values())
    if isinstance(o, list):
        for x in o:
            r = _buscar(x, ok)
            if r is not None:
                return r
    return None


def opencritic():
    r = requests.get(OPENCRITIC, headers=NAVEGADOR, timeout=40)
    r.raise_for_status()
    m = re.search(r'<script id="serverApp-state" type="application/json">(.*?)</script>', r.text, re.S)
    if not m:
        raise RuntimeError("OpenCritic: no encuentro los datos en la página")
    t = m.group(1)
    for a, b in (("&q;", '"'), ("&s;", "'"), ("&l;", "<"), ("&g;", ">"), ("&a;", "&")):
        t = t.replace(a, b)
    juego = _buscar(json.loads(t), lambda d: d.get("id") == OPENCRITIC_ID and "topCriticScore" in d)
    if not juego:
        raise RuntimeError("OpenCritic: no encuentro GTA 6 en los datos de la página")
    nota = juego.get("topCriticScore")
    if not isinstance(nota, (int, float)) or nota < 0:
        return None  # aún sin nota
    pct = juego.get("percentRecommended")
    return {"nota": round(nota), "resenas": juego.get("numTopCriticReviews") or juego.get("numReviews") or 0,
            "total": juego.get("numReviews") or 0,
            "recomienda": round(pct) if isinstance(pct, (int, float)) and pct >= 0 else None,
            "nivel": juego.get("tier") or ""}


def metacritic():
    r = requests.get(METACRITIC, headers=NAVEGADOR, timeout=40)
    r.raise_for_status()
    for bloque in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', r.text, re.S):
        try:
            j = json.loads(html.unescape(bloque))
        except Exception:
            continue
        d = _buscar(j, lambda x: isinstance(x.get("aggregateRating"), dict))
        if d:
            a = d["aggregateRating"]
            try:
                nota = round(float(a.get("ratingValue")))
            except (TypeError, ValueError):
                return None
            plataforma = d.get("gamePlatform")
            if isinstance(plataforma, list):
                plataforma = plataforma[0] if len(plataforma) == 1 else ""
            return {"nota": nota, "resenas": int(a.get("reviewCount") or a.get("ratingCount") or 0),
                    "plataforma": plataforma or ""}
    return None


def notas():
    """Devuelve (oc, mc, avisos). oc/mc son None si aún no hay nota o la web no contesta."""
    out, avisos = {}, []
    for nombre, f in (("OpenCritic", opencritic), ("Metacritic", metacritic)):
        try:
            out[nombre] = f()
        except Exception as e:
            out[nombre] = None
            avisos.append(f"{nombre}: {str(e)[:150]}")
    return out["OpenCritic"], out["Metacritic"], avisos


def clave(oc, mc):
    return f"oc{oc['nota'] if oc else '-'}x{oc['resenas'] if oc else 0}-mc{mc['nota'] if mc else '-'}x{mc['resenas'] if mc else 0}"


def texto_fuente(oc, mc):
    ahora = datetime.now(MADRID)
    lineas = [f"Notas de la crítica especializada a Grand Theft Auto VI (GTA 6), consultadas el "
              f"{ahora.day} de {['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'][ahora.month - 1]}"
              f" a las {ahora:%H:%M} (hora de España). Las notas pueden cambiar a medida que se publican más análisis."]
    if mc:
        en = f" en su versión de {mc['plataforma']}" if mc.get("plataforma") else ""
        lineas.append(f"- Metacritic{en}: Metascore de {mc['nota']} sobre 100"
                      + (f", con {mc['resenas']} análisis de medios." if mc["resenas"] else "."))
    if oc:
        t = f"- OpenCritic: nota media de los críticos más destacados de {oc['nota']} sobre 100"
        t += f" ({oc['resenas']} análisis)" if oc["resenas"] else ""
        if oc["recomienda"] is not None:
            t += f"; el {oc['recomienda']} % de los críticos lo recomienda"
        if oc["nivel"]:
            t += f"; categoría {NIVELES.get(oc['nivel'], oc['nivel'])}"
        lineas.append(t + ".")
    lineas.append("Son las notas de la prensa especializada (análisis publicados por medios de videojuegos), "
                  "no de los jugadores.")
    return "\n".join(lineas)


def propuesta(regs):
    """regs = publicaciones recientes (las de preparar.recientes()). Devuelve None o el candidato para preparar:
    {"medio", "titulo", "enlace", "texto", "clave"}."""
    oc, mc, avisos = notas()
    for a in avisos:
        print(f"⚠️ La prensa opina · {a}")
    if not oc and not mc:
        print("La prensa opina: todavía no hay notas de GTA 6 en OpenCritic ni en Metacritic.")
        return None
    k = clave(oc, mc)
    prensa = sorted([r["fields"] for r in regs if r["fields"].get("Tipo") == "Prensa"],
                    key=lambda f: f.get("Creada") or "", reverse=True)
    if prensa:
        ultima = prensa[0]
        if (ultima.get("Enlace") or "").endswith("#" + k):
            print(f"La prensa opina: sin cambios desde la última propuesta ({k}).")
            return None
        creada = datetime.fromisoformat((ultima.get("Creada") or "2000-01-01T00:00:00+00:00").replace("Z", "+00:00"))
        if datetime.now(timezone.utc) - creada < timedelta(hours=CADA_HORAS):
            print(f"La prensa opina: hay notas nuevas ({k}), pero la última propuesta es de hace menos de {CADA_HORAS} h.")
            return None
    medios = " y ".join(n for n, x in (("Metacritic", mc), ("OpenCritic", oc)) if x)
    principal = mc or oc
    titulo = f"GTA 6 tiene un {principal['nota']} en {'Metacritic' if mc else 'OpenCritic'}"
    return {"medio": medios, "titulo": titulo, "enlace": (METACRITIC if mc else OPENCRITIC) + "#" + k,
            "texto": texto_fuente(oc, mc), "clave": k}


if __name__ == "__main__":
    oc, mc, avisos = notas()
    print("OpenCritic:", oc)
    print("Metacritic:", mc)
    for a in avisos:
        print("Aviso:", a)
    if oc or mc:
        print("\n" + texto_fuente(oc, mc))
