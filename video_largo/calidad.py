"""Comprobaciones de calidad del vídeo largo montado (Fase 3). Solo avisan: no paran el montaje.

Revisa lo que pide la guía de edición: pantallazos negros, carteles del centro que se pisan, cuánto es vídeo
frente a imagen quieta, cuánto dura seguida cada música y el volumen final medido.
"""
import re
import subprocess


def _seg(ts):
    h, m, s = ts.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def negros(final, cartelas, dur_cartela):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(final), "-an", "-vf",
                        "scale=320:-2,blackdetect=d=0.35:pix_th=0.08", "-f", "null", "-"], capture_output=True, text=True)
    salida = []
    for a, z in re.findall(r"black_start:([0-9.]+) black_end:([0-9.]+)", r.stderr):
        a, z = float(a), float(z)
        if any(c - 0.3 <= a and z <= c + dur_cartela + 0.3 for c in cartelas):  # las cartelas son negras a propósito
            continue
        if a < 0.3:  # arranque
            continue
        salida.append((a, z))
    return salida


def carteles_solapados(ass):
    ev = []
    for linea in open(ass, encoding="utf-8"):
        if linea.startswith("Dialogue:") and ",Dato," in linea:
            p = linea.split(",", 3)
            ev.append((_seg(p[1]), _seg(p[2])))
    ev.sort()
    return [(a1, z0) for (a0, z0), (a1, z1) in zip(ev, ev[1:]) if a1 < z0 - 0.05]


def volumen(final):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(final), "-vn", "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[0-9.]+) LUFS", r.stderr)
    return float(m[-1]) if m else None


def revisar(final, ass, bloques, tb, es_fijo, pistas, total, dur_cartela, hms):
    inf, avisos = [], []
    cartelas = [b["cartela_ini"] for b in bloques if b.get("cartela_ini") is not None]
    n = negros(final, cartelas, dur_cartela)
    inf.append(f"Pantallazos negros: {len(n)}")
    avisos += [f"negro de {z - a:.1f} s en {hms(a)}" for a, z in n]
    s = carteles_solapados(ass)
    inf.append(f"Carteles del centro que se pisan: {len(s)}")
    avisos += [f"carteles solapados en {hms(a)}" for a, _ in s]
    quieto = vid = 0.0
    for b in bloques:
        for nombre, d in b.get("plan", []):
            t = tb.get(nombre, {})
            if es_fijo(nombre) or str(t.get("video", "")).startswith("Imagen:"):
                quieto += d
            else:
                vid += d
    pct = 100 * vid / max(vid + quieto, 1e-9)
    inf.append(f"Vídeo frente a imagen quieta: {pct:.0f} % vídeo")
    if pct < 70:
        avisos.append(f"solo {pct:.0f} % es vídeo (la guía pide más vídeo que fotos)")
    if pistas:
        tramos = [(pistas[k + 1][0] if k + 1 < len(pistas) else total) - pistas[k][0] for k in range(len(pistas))]
        inf.append(f"Música: {len(pistas)} tramos, el más largo {max(tramos) / 60:.1f} min")
        if max(tramos) > 240:
            avisos.append("una música dura más de 4 min seguidos")
    lufs = volumen(final)
    if lufs is not None:
        inf.append(f"Volumen medido: {lufs:.1f} LUFS (objetivo −14)")
        if abs(lufs + 14) > 1.5:
            avisos.append(f"volumen {lufs:.1f} LUFS, lejos de −14")
    sin_tag = [b["id"] for b in bloques if not any(tb.get(nm, {}).get("etiquetas") for nm, _ in b.get("plan", []))]
    if sin_tag and any(t.get("etiquetas") for t in tb.values()):
        inf.append("Bloques sin ningún plano etiquetado: " + ", ".join(sin_tag))
    return inf, avisos
