"""Reparte planos en los guiones de los vídeos 5 a 7 para que ningún bloque se quede corto ni repita trozos.

Uso (desde video_largo, con las tablas de trozos al lado): python repartir_planos.py guion_13a [guion_pol ...]
- Un plano con nombre sale una sola vez en el vídeo: si se repite, se quita (o, si está anclado a una palabra,
  se cambia por un trozo del grupo del bloque).
- Cada bloque se rellena con «@Grupo:N» del tema del bloque (TEMAS) hasta cubrir la voz estimada (3,4 palabras/s,
  más los huecos de canciones), y si el grupo se agota, con GTA6_Mirada.
Reescribe solo las listas «planos» y «planos_en» del archivo del guion."""
import importlib.util
import math
import os
import pathlib
import sys

os.environ.setdefault("TMP_DIR", "tmp_comprobar")
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import montaje as M  # noqa: E402

PAL_S = 3.4
MARGEN = 1.15  # un 15 % de más: la voz real a veces va más lenta
RESERVA = "@GTA6_Mirada"
TEMAS = {
    "guion_13a": {"hook": "GTA6_Mirada", "p01": "GTA5_2013", "p02": "GTA_Online", "p03": "GTA_Online",
                  "p04": "GTA5_2013", "p05": "GTA_Online", "p06": "RDR2_2018", "p07": "Historia_GTA",
                  "p08": "Historia_GTA", "p09": "Historia_GTA", "p10": "GTA3_2001", "p11": "GTA6_Mirada",
                  "p12": "GTA6_Mirada", "p13": "GTA6_T1", "p14": "GTA6_T2", "p15": "GTA6_Mirada",
                  "p16": "GTA6_Lanzamiento", "p17": "GTA6_Mirada", "cierre": "GTA6_Mirada"},
    "guion_pol": {"hook": "Historia_GTA", "p01": "GTA1_1997", "p02": "GTA3_2001", "p03": "Vice_City_2002",
                  "p04": "SA_2004", "p05": "SA_2004", "p06": "Historia_GTA", "p07": "LCS_2005", "p08": "GTA5_2013",
                  "p09": "GTA5_2013", "p10": "GTA5_2013", "p11": "GTA5_2013", "p12": "GTA_Online",
                  "p13": "Vice_City_2002", "p14": "GTA_Online", "p15": "GTA6_Mirada", "p16": "Historia_GTA",
                  "cierre": "GTA6_Mirada"},
    "guion_rad": {"hook": "Historia_GTA", "p01": "GTA1_1997", "p02": "GTA2_1999", "p03": "GTA3_2001",
                  "p04": "Vice_City_2002", "p05": "Vice_City_2002", "p06": "SA_2004", "p07": "LCS_2005",
                  "p08": "GTA4_2008", "p09": "GTA4_2008", "p10": "GTA5_2013", "p11": "GTA_Online",
                  "p12": "VCS_2006", "p13": "GTA_Online", "p14": "GTA6_T2", "p15": "GTA6_Mirada",
                  "cierre": "GTA6_Mirada"},
}


def spans(texto, clave):
    """(inicio, fin) de cada lista «clave»: [...] del archivo, con los corchetes emparejados."""
    out, i = [], 0
    marca = f'"{clave}": ['
    while (i := texto.find(marca, i)) >= 0:
        j, prof = i + len(marca) - 1, 0
        while True:
            c = texto[j]
            if c == "[":
                prof += 1
            elif c == "]":
                prof -= 1
                if prof == 0:
                    break
            elif c == '"':  # salta cadenas
                j = texto.index('"', j + 1)
            j += 1
        out.append((i + len(marca) - 1, j + 1))
        i = j
    return out


def fmt(lista):
    if lista and isinstance(lista[0], dict):
        return "[" + ",\n                   ".join(
            "{" + ", ".join(f'"{k}": "{v}"' for k, v in d.items()) + "}" for d in lista) + "]"
    return "[" + ", ".join(f'"{p}"' for p in lista) + "]"


def repartir(nombre):
    ruta = pathlib.Path(nombre + ".py")
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    tb = M.tabla()
    grupos = {}
    for n, t in tb.items():
        grupos.setdefault(t.get("grupo", ""), []).append(t["dur"] * t["lento"])
    media = {k: sum(v) / len(v) for k, v in grupos.items()}
    libres = {k: len(v) for k, v in grupos.items()}
    nombrados = {p for b in g.BLOQUES for p in list(b["planos"]) + [r["plano"] for r in b.get("planos_en", [])]
                 if not p.startswith("@")}
    for k in libres:  # los trozos que el guion pide por su nombre no salen por grupo
        libres[k] -= sum(1 for p in nombrados if p in tb and tb[p].get("grupo") == k)
    usados, nuevos_planos, nuevos_en = set(), [], []
    for b in g.BLOQUES:
        tema = TEMAS[nombre].get(b["id"], "GTA6_Mirada")
        en = []
        for r in b.get("planos_en", []):
            r = dict(r)
            p = r["plano"]
            if not p.startswith("@"):
                if p in usados or p not in tb:
                    r["plano"] = "@" + tema
                else:
                    usados.add(p)
            en.append(r)
        anclados = {r["plano"] for r in en if not r["plano"].startswith("@")}
        planos, cubierto = [], 0.0
        for p in b["planos"]:
            if p.startswith("@"):
                grp, _, n = p.partition(":")
                n = min(int(n or 5), max(0, libres.get(grp[1:], 0)))  # nunca más trozos de los que quedan
                if n:
                    planos.append(f"{grp}:{n}")
                    cubierto += n * media.get(grp[1:], 3)
                    libres[grp[1:]] -= n
            elif p in anclados:
                planos.append(p)
                cubierto += tb[p]["dur"] * tb[p]["lento"]
            elif p not in usados and p in tb:
                planos.append(p)
                usados.add(p)
                cubierto += tb[p]["dur"] * tb[p]["lento"]
        for r in en:
            if r["plano"].startswith("@"):
                grp = r["plano"][1:].partition(":")[0]
                if libres.get(grp, 0) <= 0:  # grupo agotado: el anclaje tira de la reserva
                    grp = RESERVA[1:]
                    r["plano"] = RESERVA
                libres[grp] = libres.get(grp, 0) - 1
                cubierto += media.get(grp, 3)
            elif r["plano"] not in planos:
                cubierto += tb[r["plano"]]["dur"] * tb[r["plano"]]["lento"]
        voz = len(b["texto"].split()) / PAL_S + sum(c.get("seg", 5) + 0.7 for c in b.get("canciones", []))
        falta = voz * MARGEN + 1.5 - cubierto
        for grp in (tema, RESERVA[1:]):
            if falta <= 0:
                break
            n = min(math.ceil(falta / media.get(grp, 3)), max(0, libres.get(grp, 0)))
            if n > 0:
                planos.append(f"@{grp}:{n}")
                libres[grp] -= n
                falta -= n * media.get(grp, 3)
        if falta > 0:
            print(f"  AVISO {b['id']}: no hay trozos libres para {falta:.1f} s")
        nuevos_planos.append(planos)
        if "planos_en" in b:
            nuevos_en.append(en)
    texto = ruta.read_text(encoding="utf-8")
    sp_p, sp_e = spans(texto, "planos"), spans(texto, "planos_en")
    assert len(sp_p) == len(nuevos_planos) and len(sp_e) == len(nuevos_en), (len(sp_p), len(sp_e))
    cambios = [(a, z, fmt(v)) for (a, z), v in zip(sp_p, nuevos_planos)] + \
              [(a, z, fmt(v)) for (a, z), v in zip(sp_e, nuevos_en)]
    for a, z, v in sorted(cambios, reverse=True):
        texto = texto[:a] + v + texto[z:]
    ruta.write_text(texto, encoding="utf-8", newline="")
    agotados = [f"{k} ({v})" for k, v in libres.items() if v < 0]
    print(nombre, "listo", "· grupos pasados de su tamaño: " + ", ".join(agotados) if agotados else "")


for n in sys.argv[1:]:
    repartir(n)
