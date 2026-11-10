"""Grafismo de cristal para el vídeo largo (16:9), estilo Apple con colores Miami (pedido el 10 nov 2026).

Mismo estilo que los Reels (gta/grafismo.py de la rama shorts-valor): cristal oscuro al 42 %, borde blanco fino
al 18 %, letra Inter, rosa Miami y turquesa. Sin animación de marca: el protagonismo es de las imágenes.

Se activa con CRISTAL = True en el guion. montaje.py llama a:
  retocar(ass, total)            -> cambia el .ass ya escrito (subtítulos, carteles, cartelas, barra de progreso)
                                    y devuelve los «paneles»: zonas que van con desenfoque real detrás.
  filtros(paneles, idx0, tmp, fps, entrada, salida)
                                 -> entradas extra de ffmpeg (máscaras redondeadas) y el trozo de filter_complex
                                    que difumina esas zonas solo mientras se ven (trim: no gasta fuera de su tiempo).
  fotograma_cartela(...)         -> fondo de las cartelas: un fotograma quieto y difuminado del propio vídeo.
Los subtítulos van en pastilla de cristal teñida (sin desenfoque: serían cientos de zonas)."""
import pathlib
import re
import subprocess

from PIL import Image, ImageDraw

W, H = 1920, 1080
TINTE = "&H230E14&"          # (20, 14, 35) en orden azul-verde-rojo
A_TARJETA = "&H94&"          # 42 % de opacidad
A_PASTILLA = "&H73&"         # 55 %: los subtítulos se leen siempre
A_PANTALLA = "&H70&"         # cartel a pantalla completa (antes, fondo negro)
BORDE = "\\bord2\\3c&HFFFFFF&\\3a&HD1&\\shad0"   # blanco al 18 %
ROSA = "&H882EFF&"           # #ff2e88
TURQUESA = "&HFFE500&"       # #00e5ff
SUB_TAM, SUB_LINEA, SUB_MV = 50, 62, 92

ESTILOS = {  # campos de «Style:» que cambian: 1 letra, 2 tamaño, 3 color, 7 negrita, 16 borde, 17 sombra
    "Sub": {1: "Inter", 2: str(SUB_TAM), 3: "&H00FFFFFF", 7: "-1", 16: "0", 17: "0"},
    "Dato": {1: "Inter", 7: "-1", 16: "0", 17: "0"},
    "Marca": {1: "Inter", 2: "30", 7: "-1"},
    "CartAnio": {1: "Inter", 2: "190", 3: "&H00FFFFFF", 7: "-1", 13: "0"},
    "CartActo": {1: "Inter", 2: "40", 3: "&H00" + TURQUESA[2:-1], 7: "-1", 13: "6"},
    "CartTit": {1: "Inter", 2: "92", 3: "&H00FFFFFF", 7: "-1", 13: "2"},
}


def redondo(w, h, r):
    """Rectángulo de esquinas redondeadas en dibujo ASS (curvas de Bézier)."""
    k = round(0.4477 * r)
    return (f"m {r} 0 l {w - r} 0 b {w - k} 0 {w} {k} {w} {r} l {w} {h - r} b {w} {h - k} {w - k} {h} {w - r} {h} "
            f"l {r} {h} b {k} {h} 0 {h - k} 0 {h - r} l 0 {r} b 0 {k} {k} 0 {r} 0")


def t_ass(s):
    s = max(0.0, s)
    return f"{int(s // 3600)}:{int(s % 3600 // 60):02d}:{s % 60:05.2f}"


def s_ass(t):
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def tarjeta(capa, a, z, x, y, w, h, alfa=A_TARJETA, r=28, fad="\\fad(150,200)"):
    return (f"Dialogue: {capa},{a},{z},Dibujo,,0,0,0,,{{\\pos({x},{y})\\c{TINTE}\\1a{alfa}{BORDE}{fad}\\p1}}"
            + redondo(w, h, r))


def _estilos(cab):
    def cambia(m):
        campos = m.group(0)[len("Style: "):].split(",")
        for i, v in ESTILOS.get(campos[0], {}).items():
            campos[i] = v
        return "Style: " + ",".join(campos)
    return re.sub(r"^Style: [^\n]+", cambia, cab, flags=re.M)


def _partir(linea):
    p = linea[len("Dialogue: "):].split(",", 9)
    return p  # capa, ini, fin, estilo, nombre, ml, mr, mv, efecto, texto


def _limpio(texto):
    return re.sub(r"\{[^}]*\}", "", texto)


def retocar(ruta, total):
    ruta = pathlib.Path(ruta)
    txt = ruta.read_text(encoding="utf-8")
    cab, cuerpo = txt.split("[Events]", 1)
    cab = _estilos(cab)
    lineas = cuerpo.split("\n")
    nuevas, extra, paneles, subs = [], [], [], []
    for ln in lineas:
        if not ln.startswith("Dialogue: "):
            nuevas.append(ln)
            continue
        capa, a, z, est, nom, ml, mr, mv, ef, tx = _partir(ln)
        t0, t1 = s_ass(a), s_ass(z)
        if est == "SubSombra":
            continue
        if est == "Sub":
            subs.append((t0, t1, _limpio(tx)))
            ln = f"Dialogue: 1,{a},{z},{est},{nom},{ml},{mr},{mv},{ef},{tx}"
        elif est == "Dibujo" and "\\c&H000000&" in tx:
            pos = re.search(r"\\pos\((\d+),(\d+)\)", tx)
            caja = re.search(r"m 0 0 l (\d+) 0 \1 (\d+) 0 \2", tx)
            if not caja:
                nuevas.append(ln)
                continue
            w, h = int(caja.group(1)), int(caja.group(2))
            if w >= W and h >= H:  # cartel a pantalla completa: cristal en toda la pantalla
                paneles.append((0, 0, W, H, t0, t1))
                ln = (f"Dialogue: {capa},{a},{z},Dibujo,,0,0,0,,{{\\pos(0,0)\\c{TINTE}\\1a{A_PANTALLA}\\fad(0,250)\\p1}}"
                      f"m 0 0 l {W} 0 {W} {H} 0 {H}")
            else:  # caja del cartel: tarjeta de cristal algo más holgada
                x, y = int(pos.group(1)) - 12, int(pos.group(2)) - 12
                w, h = w + 24, h + 24
                paneles.append((x, y, w, h, t0, t1))
                ln = tarjeta(capa, a, z, x, y, w, h)
        elif est == "Dato":
            ln = ln.replace("\\c&H0000D7FF&", "\\c&HFFFFFF&")
        elif est == "CartAnio":  # tarjeta detrás de cada cartela de acto
            x, y, w, h = 510, 215, 900, 540
            paneles.append((x, y, w, h, t0, t1))
            extra.append(tarjeta(4, a, z, x, y, w, h, r=36, fad="\\fad(120,160)"))
        nuevas.append(ln)
    # pastillas de los subtítulos: una por frase (los eventos seguidos con el mismo texto son la misma frase)
    frases = []
    for t0, t1, tx in subs:
        if frases and frases[-1][2] == tx and t0 - frases[-1][1] < 0.3:
            frases[-1][1] = max(frases[-1][1], t1)
        else:
            frases.append([t0, t1, tx])
    for t0, t1, tx in frases:
        filas = [f for f in tx.split("\\N") if f.strip()] or [tx]
        n = len(filas)
        w = int(max(len(f) for f in filas) * SUB_TAM * 0.56) + 76
        h = n * SUB_LINEA + 30
        x, y = W // 2 - w // 2, H - SUB_MV - n * SUB_LINEA - 14
        extra.append(tarjeta(0, t_ass(t0), t_ass(t1), x, y, w, h, alfa=A_PASTILLA, r=min(30, h // 2),
                             fad="\\fad(90,130)"))
    # barra de progreso: pastilla de cristal arriba en el centro, relleno rosa que avanza con el vídeo
    bx, by, bw, bh = W // 2 - 170, 30, 340, 18
    paneles.append((bx, by, bw, bh, 0.0, total))
    a, z, ms = t_ass(0), t_ass(total), int(total * 1000)
    x0, x1 = bx + 9, bx + bw - 9
    extra.append(tarjeta(6, a, z, bx, by, bw, bh, r=9, fad=""))
    extra.append(f"Dialogue: 7,{a},{z},Dibujo,,0,0,0,,{{\\pos(0,0)\\c{ROSA}\\shad0\\bord0"
                 f"\\clip({x0},{by},{x0},{by + bh})\\t(0,{ms},\\clip({x0},{by},{x1},{by + bh}))\\p1}}"
                 f"m {x0} {by + 7} l {x1} {by + 7} {x1} {by + 11} {x0} {by + 11}")
    i = next(k for k, l in enumerate(nuevas) if l.startswith("Format:"))
    nuevas[i + 1:i + 1] = extra
    ruta.write_text(cab + "[Events]" + "\n".join(nuevas), encoding="utf-8")
    return paneles


def mascara(ruta, w, h, r):
    k = 4
    im = Image.new("L", (w * k, h * k), 0)
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w * k - 1, h * k - 1), r * k, fill=255)
    im.resize((w, h), Image.LANCZOS).save(ruta)


def filtros(paneles, idx0, tmp, fps, entrada, salida):
    """Entradas extra y trozo de filter_complex: desenfoque real detrás de cada panel, solo durante su tiempo."""
    if not paneles:
        return [], f"[{entrada}]null[{salida}];"
    args, partes, cur = [], [], entrada
    for i, (x, y, w, h, t0, t1) in enumerate(paneles):
        x, y = max(0, x - x % 2), max(0, y - y % 2)  # medidas pares: el vídeo es yuv420p
        w, h = min(W - x, w + w % 2), min(H - y, h + h % 2)
        r = 0 if (w, h) == (W, H) else min(36 if h > 400 else 28, h // 2)
        m = pathlib.Path(tmp) / f"mascara_{i:03d}.png"
        mascara(m, w, h, r)
        d = max(0.1, t1 - t0)
        args += ["-loop", "1", "-framerate", str(fps), "-t", f"{d:.2f}", "-i", str(m)]
        sig = 30 if (w, h) == (W, H) else 22
        sal = salida if i == len(paneles) - 1 else f"cr{i}"
        partes.append(
            f"[{cur}]split[c{i}][s{i}];"
            f"[s{i}]trim=start={t0:.3f}:end={t1:.3f},setpts=PTS-STARTPTS,crop={w}:{h}:{x}:{y},"
            f"gblur=sigma={sig},eq=brightness=-0.05:saturation=1.15[b{i}];"
            f"[{idx0 + i}:v]format=gray[m{i}];"
            f"[b{i}][m{i}]alphamerge,setpts=PTS+{t0:.3f}/TB[g{i}];"
            f"[c{i}][g{i}]overlay={x}:{y}:eof_action=pass[{sal}];")
        cur = sal
    return args, "".join(partes)


def fotograma_cartela(origen, segundo, destino, dur, fps):
    """Fondo de una cartela: un fotograma quieto del propio vídeo, difuminado y oscurecido (sin movimiento)."""
    png = pathlib.Path(destino).with_suffix(".png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{segundo:.2f}", "-i", str(origen), "-frames:v", "1",
                    "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                           "gblur=sigma=34,eq=brightness=-0.16:saturation=1.1", str(png)], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", str(fps), "-t", f"{dur:.2f}",
                    "-i", str(png), "-c:v", "libx264", "-crf", "12", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                    str(destino)], check=True)
