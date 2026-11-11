"""Comprueba un guion del vídeo largo sin voces ni descargas (lo lanza «Comprobar guion del vídeo largo»).

Errores que paran: planos que no existen, palabras de «en» que la voz no dice, nombres sin plano ni cartel,
texto y voz con distinto número de palabras y trozos que saldrían repetidos con la duración estimada.
Se elige el guion con GUION (guion_vl, guion_vc, guion_sg)."""
import collections
import importlib
import os
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
os.environ.setdefault("TMP_DIR", "tmp_comprobar")
import montaje as M  # noqa: E402
import prototipo as P  # noqa: E402

G = importlib.import_module(os.environ.get("GUION", "guion_vl"))
PAL_S = 3.4  # palabras por segundo con la voz real (Orus +12 %; medido en la previa del vídeo 3: 3,6)


def aparece(texto, palabra, n=1):
    clave = P.normalizar(palabra)
    return sum(1 for w in texto.split() if P.normalizar(w).startswith(clave)) >= n


def main():
    tb = M.tabla()
    solo = [x.strip() for x in os.environ.get("BLOQUES_SOLO", "").split(",") if x.strip()]
    bloques = [dict(b, planos=list(b["planos"]), planos_en=[dict(r) for r in b.get("planos_en", [])])
               for b in G.BLOQUES if not solo or b["id"] in solo]
    errores, avisos, palabras, t = [], [], 0, 0.0
    M.planos_en_linea(bloques, tb)
    grupos = collections.Counter(v.get("grupo", "") for v in tb.values())
    for b in bloques:
        txt = b["texto"]
        if b.get("voz") and len(b["voz"].split()) != len(txt.split()):
            avisos.append(f"{b['id']}: texto y voz tienen distinto número de palabras")
        for p in b["planos"] + [r["plano"] for r in b["planos_en"]] + [b[k] for k in ("original", "intro_original") if b.get(k)]:
            if p.startswith("@"):
                g = p[1:].partition(":")[0]
                if not grupos.get(g):
                    errores.append(f"{b['id']}: el grupo @{g} no tiene trozos")
            elif p not in tb:
                errores.append(f"{b['id']}: el plano {p} no está en los CSV de trozos")
        for r in b.get("rotulos", []) + b["planos_en"]:
            if "en" in r and not aparece(txt, r["en"], r.get("n", 1)):
                errores.append(f"{b['id']}: «{r['en']}» no está en el texto (rótulo o plano)")
        cubiertos = {(P.normalizar(r["en"]), r.get("n", 1)) for r in b.get("rotulos", []) + b["planos_en"] if "en" in r}
        for nom in b.get("nombres", []):
            en, n = (nom, 1) if isinstance(nom, str) else (nom["en"], nom.get("n", 1))
            if not aparece(txt, en, n):
                errores.append(f"{b['id']}: el nombre «{en}» no está en el texto")
            elif (P.normalizar(en), n) not in cubiertos:
                errores.append(f"{b['id']}: «{en}» se nombra pero no sale en pantalla (falta plano o cartel)")
        palabras += len(txt.split())
        b["dur_voz"] = len(txt.split()) / PAL_S
        c = (M.DUR_CARTELA if b.get("cartela") else 0) + (tb[b["intro_original"]]["dur"] if b.get("intro_original") in tb else 0)
        b["ini"], b["plan_ini"] = t, t + c
        b["voz_ini"], b["ws"] = t + c + 0.4, []
        b["voz_fin"] = b["voz_ini"] + b["dur_voz"]
        b["vis_fin"] = b["fin"] = b["voz_fin"] + 0.5
        t = b["fin"]
    try:
        M.expandir_grupos(bloques, tb)
        for b in bloques:
            b["plan"] = (M.planificar_anclado if b.get("planos_en") else M.planificar)(b, b["vis_fin"] - b["plan_ini"], tb)
        for b in bloques:
            if b.get("alargado", 0) > 1.5:
                avisos.append(f"{b['id']}: faltan planos, el último se alarga {b['alargado']:.1f} s (añade más al guion)")
        usados_v = {tb[n]["video"] for b in bloques for n, _ in b.get("plan", []) if n in tb}
        usados_v |= {tb[b[k]]["video"] for b in bloques for k in ("original", "intro_original") if b.get(k) in tb}
        sin_dir = sorted(v for v in usados_v if not v.startswith(("Clips:", "Imagen:")) and v not in P.VIDEOS)
        if sin_dir:
            errores.append("Vídeos sin dirección (añádelos a VIDEOS_EXTRA): " + ", ".join(sin_dir))
        if os.environ.get("COMPROBAR_ENLACES") == "1":  # que cada vídeo siga descargable (solo pide la cabecera)
            import urllib.request
            from concurrent.futures import ThreadPoolExecutor

            def caido(v):
                url = P.VIDEOS[v].split("#")[0]
                try:
                    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req, timeout=30) as r:
                        return None if r.status < 400 else f"{v} (HTTP {r.status})"
                except Exception as e:  # noqa: BLE001
                    return f"{v} ({type(e).__name__})"
            con_url = sorted(v for v in usados_v if v in P.VIDEOS and str(P.VIDEOS[v]).startswith("http"))
            with ThreadPoolExecutor(8) as ex:
                caidos = [x for x in ex.map(caido, con_url) if x]
            (errores if caidos else avisos).append("Vídeos que no se pueden bajar: " + ", ".join(caidos) if caidos
                                                  else f"Enlaces comprobados: {len(con_url)} bien")
        if os.environ.get("COMPROBAR_VOCES") == "1":
            import voces as V
            sin_voz = [b["id"] for b in bloques if not V.ruta_wav(b).exists()]
            if sin_voz:
                errores.append("Faltan voces: " + ", ".join(sin_voz) + " (lanza el paso «voces»)")
        rep = M.comprobar_repetidos(bloques)
        if rep:
            errores.append(f"{len(rep)} trozos saldrían repetidos: " + "; ".join(rep[:12]) + (" …" if len(rep) > 12 else ""))
    except Exception as e:  # noqa: BLE001
        errores.append(f"No se pudo simular el reparto de planos: {type(e).__name__} {e}")
    ass = pathlib.Path("prueba.ass")
    ass.write_text("[V4+ Styles]\nStyle: Dibujo,x\n\n[Events]\n", encoding="utf-8")
    M.anadir_rotulos(ass, bloques)
    rot = sum(1 for linea in ass.read_text(encoding="utf-8").splitlines() if ",Dato," in linea)
    mus = M.musica_del_guion(bloques, min(t, 40.0))
    usados = collections.Counter(tb[n].get("grupo", "") for b in bloques for n, _ in b.get("plan", []) if n in tb)
    banco = [f"{g or '(sin grupo)'}: {usados[g]} usados de {grupos[g]}" for g in sorted(usados)]
    caps = [b.get("capitulo") or b["titulo"].capitalize() for b in bloques if b["num"]]
    inf = [f"Guion: {os.environ.get('GUION', 'guion_vl')}", f"Bloques: {len(bloques)}", f"Palabras: {palabras}",
           f"Duración aproximada: {t / 60:.1f} min", f"Rótulos de datos: {rot}", f"Música de prueba: {len(mus) / M.SR:.0f} s",
           "Capítulos: " + " · ".join(caps), "", "Banco de trozos por grupo:"] + banco + [""] + avisos + (errores or ["Sin errores"])
    print("\n".join(inf))
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write("### Comprobación del guion\n\n" + "  \n".join(inf) + "\n")
    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main()
