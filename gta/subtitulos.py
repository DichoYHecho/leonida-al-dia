"""Subtítulos siempre legibles (fase E1, 28-29 oct 2026). Lo usa render2.montar cuando cfg["subs"] == "e1".

- Zona segura: los subtítulos van en el tercio central-bajo, con el ancho limitado y algo desplazados a la izquierda,
  para no caer bajo los botones (derecha) ni bajo el título y el canal (abajo) de Shorts, Reels y TikTok.
- Capa siempre encima: se pintan los últimos (después de rótulos, logo, destellos de las transiciones…).
- Contraste: borde negro grueso + sombra y, si el fondo que hay detrás es claro o tiene mucho detalle (p. ej. el logo
  de GTA VI de los trozos oficiales), una banda oscura semitransparente detrás. Se mide el trozo de imagen.
- No solape: por cada tramo de fondo se elige la zona (media, baja o alta) con el fondo más limpio; la alta nunca
  mientras se ve el gancho. El primer subtítulo espera a que el gancho se haya ido si el gancho está abajo.
- Control: cada grupo queda anotado (zona, banda, nota del fondo) y si ni con la banda queda limpio, se avisa
  («Subtítulo tapado»).
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

W, H = 1080, 1920
CX = 510           # centro horizontal (30 px a la izquierda: botones de la derecha)
ANCHO = 800        # ancho máximo del texto (de 110 a 910 px)
ALTO_ZONA = 200    # alto que se mide alrededor de la línea
ZONAS = (("media", 1180, 0.0), ("baja", 1360, 0.02), ("alta", 440, 0.06))  # nombre, centro y, penalización
LIMPIO = 0.18      # por debajo, el fondo no molesta: zona media y sin banda
BANDA_MAX = 0.78   # opacidad máxima de la banda oscura
CAMBIAR = 0.40     # la zona solo cambia si la media pasa de esto…
MEJORA = 0.15      # …y la otra es al menos esto más limpia
TAPADO = 0.85      # nota tan alta que ni con la banda se garantiza la lectura → aviso
ENCOGER_LOGO = (0.56, -420)  # trozos con el logo de GTA VI: tamaño y desplazamiento vertical (sube). 4 nov: el logo queda por encima de los subtítulos


def es_logo(ruta):
    """Trozo oficial con el logo grande de GTA VI (p. ej. Mirada_Logo.mp4)."""
    return "logo" in os.path.basename(str(ruta)).lower()


def encoger(img, s, dy):
    """Encoge el fotograma y lo sube, sobre una versión borrosa y oscura de sí mismo: el logo deja libre la zona de
    los subtítulos y el gancho."""
    fondo = img.resize((W // 8, H // 8), Image.BILINEAR).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR)
    fondo = ImageEnhance.Brightness(fondo).enhance(0.35)
    pw, ph = int(W * s), int(H * s)
    fondo.paste(img.resize((pw, ph), Image.BILINEAR), ((W - pw) // 2, (H - ph) // 2 + dy))
    return fondo


def nota_fondo(rgb, cy, caja=None):
    """Nota de 0 (fondo oscuro y liso) a ~1,5 (claro, de colores vivos y con mucho detalle) del trozo de imagen
    donde iría el subtítulo (o de la caja x0, y0, x1, y1). rgb: array (H, W, 3) uint8."""
    y0, y1 = int(max(0, cy - ALTO_ZONA / 2)), int(min(H, cy + ALTO_ZONA / 2))
    x0, x1 = CX - ANCHO // 2, CX + ANCHO // 2
    if caja:
        x0, y0, x1, y1 = (int(min(max(v, 0), m)) for v, m in zip(caja, (W, H, W, H)))
    a = rgb[y0:y1:4, x0:x1:4].astype(np.float32) / 255
    lum = a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114
    claro = float((lum > 0.6).mean())
    g = np.zeros_like(lum)
    g[:, 1:] = np.abs(np.diff(lum, axis=1))
    g[1:, :] = np.maximum(g[1:, :], np.abs(np.diff(lum, axis=0)))
    detalle = float((g > 0.10).mean())
    mx, mn = a.max(2), a.min(2)
    vivo = float((((mx - mn) / (mx + 1e-4) > 0.45) & (mx > 0.55)).mean())
    return round(0.5 * claro + 0.8 * detalle + 0.5 * vivo, 3)


def banda_para(nota):
    if nota <= LIMPIO:
        return 0.0
    return round(float(np.clip(0.35 + (nota - LIMPIO) / 0.4 * (BANDA_MAX - 0.35), 0.35, BANDA_MAX)), 2)


def intervalos(grupos, t_pregunta):
    """(inicio, fin) de cada grupo, como en el montaje anterior."""
    out = []
    for g_i, g in enumerate(grupos):
        a = g[0][2] - 0.06
        b = grupos[g_i + 1][0][2] - 0.06 if g_i + 1 < len(grupos) else g[-1][3] + 0.3
        if g[-1][0] != (grupos[g_i + 1][0][0] if g_i + 1 < len(grupos) else None):
            b = min(b, g[-1][3] + 0.35)
        out.append((a, min(b, t_pregunta)))
    return out


def planificar(grupos, t_pregunta, fondo_rgb, tramo_de, gancho=None):
    """Decide zona y banda de cada grupo.
    fondo_rgb(t): fotograma de fondo (con la viñeta) en el instante t, array (H, W, 3).
    tramo_de(t): índice del tramo de fondo en t (la zona se elige por tramo, para que no salte de un grupo a otro).
    gancho: (fin, y_centro) del gancho grande o None.
    Devuelve (plan, avisos); plan = [{a, b, zona, cy, banda, nota}]."""
    ints = intervalos(grupos, t_pregunta)
    muestras = []  # por grupo: {zona: nota máxima}
    por_tramo = {}  # por tramo de fondo: {zona: nota máxima de las muestras tomadas en ese tramo}
    for a, b in ints:
        notas = {}
        if b > a:
            for f in (0.2, 0.5, 0.8):
                t = a + (b - a) * f
                rgb = fondo_rgb(t)
                d = por_tramo.setdefault(tramo_de(t), {})
                for nombre, cy, _ in ZONAS:
                    n = nota_fondo(rgb, cy)
                    notas[nombre] = max(notas.get(nombre, 0.0), n)
                    d[nombre] = max(d.get(nombre, 0.0), n)
        muestras.append(notas)
    # zona por tramo: la de menor nota (peor caso del tramo), con preferencia por la media
    zona_tramo = {}
    for k, notas in por_tramo.items():
        mejor = min(ZONAS, key=lambda z: notas[z[0]] + z[2])
        cambia = notas["media"] >= CAMBIAR and notas[mejor[0]] + mejor[2] <= notas["media"] - MEJORA
        zona_tramo[k] = mejor[0] if cambia else "media"
    cy_de = {n: cy for n, cy, _ in ZONAS}
    plan, avisos = [], []
    for i, ((a, b), notas) in enumerate(zip(ints, muestras)):
        zona = zona_tramo.get(tramo_de((a + b) / 2), "media") if notas else "media"
        if gancho and a < gancho[0]:
            if zona == "alta":  # nunca encima del gancho
                zona = "media" if notas.get("media", 0) <= notas.get("baja", 0) + 0.02 else "baja"
            if gancho[1] > 900:  # gancho abajo: esperar a que se vaya
                a = gancho[0]
        nota = notas.get(zona, 0.0)
        banda = banda_para(nota)
        plan.append({"a": a, "b": b, "zona": zona, "cy": cy_de[zona], "banda": banda, "nota": nota})
        if nota >= TAPADO:
            texto = " ".join(p[1] for p in grupos[i])
            avisos.append(f"Subtítulo tapado ({a:.1f} s, «{texto}», fondo {nota:.2f})")
    return plan, avisos


def plan_gancho(fondo_rgb, caja, salida, abajo):
    """Banda detrás del gancho (portada) si el fondo lo pide. caja: (x0, y0, x1, y1) del texto del gancho."""
    if not caja:
        return None
    nota = max(nota_fondo(fondo_rgb(t), 0, caja) for t in (0.0, salida * 0.5, max(salida - 0.05, 0.0)))
    banda = banda_para(nota)
    return {"caja": caja, "banda": banda, "nota": nota, "salida": salida, "dura": 0.15 if abajo else 0.22}


def dibujar_banda_gancho(img, t, pg):
    """Banda oscura detrás del gancho; se apaga cuando el gancho se va."""
    if not pg or pg["banda"] <= 0:
        return
    e = 0.0
    if t > pg["salida"]:
        x = min(max((t - pg["salida"]) / pg["dura"], 0.0), 1.0)
        e = x * x * (3 - 2 * x)
    if e >= 1:
        return
    x0, y0, x1, y1 = pg["caja"]
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(capa).rounded_rectangle([max(x0 - 36, 20), y0 - 24, min(x1 + 36, W - 20), y1 + 24], 40,
                                           fill=(10, 14, 38, int(255 * pg["banda"] * (1 - e))))
    img.alpha_composite(capa)


def dibujar(img, t, plan, grupos, f, acento, r):
    """Pinta el subtítulo que toca en t (si hay). r: el módulo render2 (poner_palabras, partir_lineas, sale)."""
    for p, g in zip(plan, grupos):
        if not (p["a"] <= t < p["b"]):
            continue
        cy = p["cy"]
        capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        lineas = r.partir_lineas([(w, x, y) for _, w, x, y in g], f, ANCHO)
        r.poner_palabras(capa, lineas, cy, f, acento, t, borde=10)
        if p["banda"] > 0:
            caja = capa.getbbox()
            if caja:
                fondo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                x0, y0, x1, y1 = caja
                ImageDraw.Draw(fondo).rounded_rectangle([x0 - 26, y0 - 10, x1 + 26, y1 + 6], 34,
                                                        fill=r.NOCHE + (int(255 * p["banda"]),))
                fondo.alpha_composite(capa)
                capa = fondo
        e = r.sale((t - p["a"]) / 0.12)
        if e < 1:
            esc = 0.8 + 0.2 * e
            capa = capa.transform((W, H), Image.AFFINE, (1 / esc, 0, W / 2 * (1 - 1 / esc), 0, 1 / esc,
                                                         cy * (1 - 1 / esc)), resample=Image.BILINEAR)
        img.alpha_composite(capa, (0, 0), (W // 2 - CX, 0))  # desplazado a la izquierda (zona segura)
        return


def informe(plan):
    """Resumen corto para el registro."""
    from collections import Counter
    z = Counter(p["zona"] for p in plan)
    con_banda = sum(p["banda"] > 0 for p in plan)
    peor = max((p["nota"] for p in plan), default=0)
    return f"{len(plan)} subtítulos · zonas {dict(z)} · con banda {con_banda} · peor fondo {peor:.2f}"
