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

W, H = 1920, 1080        # coordenadas del montaje (y del .ass)
SALIDA = (2560, 1440)    # vídeo final en 2K (11 nov): YouTube lo sirve con más calidad
TINTE = "&H230E14&"          # (20, 14, 35) en orden azul-verde-rojo
A_TARJETA = "&H94&"          # 42 % de opacidad
A_PASTILLA = "&H73&"         # 55 %: los subtítulos se leen siempre
A_PANTALLA = "&H70&"         # cartel a pantalla completa (antes, fondo negro)
BORDE = "\\bord2\\3c&HFFFFFF&\\3a&HD1&\\shad0"   # blanco al 18 %
ROSA = "&H882EFF&"           # #ff2e88
TURQUESA = "&HFFE500&"       # #00e5ff
SUB_TAM, SUB_LINEA, SUB_MV = 50, 62, 92

ESTILOS = {  # campos de «Style:» que cambian: 1 letra, 2 tamaño, 3 color, 7 negrita, 16 borde, 17 sombra
    "Sub": {1: "Inter", 2: "56", 3: "&H00FFFFFF", 5: "&H50140E23", 6: "&H90000000", 7: "-1", 16: "2.6", 17: "1.5"},
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


def _caja_texto(tx):
    """Texto de un cartel a pantalla completa: centrado en la tarjeta de cristal, grande pero con aire."""
    tx = re.sub(r"\\pos\(\d+,\d+\)", r"\\pos(960,575)", tx)
    tx = re.sub(r"\\fs(\d+)", lambda m: "\\fs" + str(min(132, round(int(m.group(1)) * (1.35 if int(m.group(1)) < 100 else 1.06)))), tx)
    return tx.replace("\\c&H0000D7FF&", "\\c&HFFFFFF&").replace("\\fad(150,200)", "\\fad(250,250)")


CONGELAR = []  # (ini, fin) de los carteles a pantalla completa: fondo = fotograma quieto y difuminado


def retocar(ruta, total):
    """Cambios del 11 nov: subtítulos sin pastilla y con borde suave; sin barra de progreso; los carteles del
    centro pasan a tarjeta a pantalla completa (fondo liso, sin vídeo detrás, texto grande); los que empiezan por
    «@» son etiquetas pequeñas arriba a la izquierda (nombre y papel de quien sale en pantalla)."""
    CONGELAR.clear()
    ruta = pathlib.Path(ruta)
    txt = ruta.read_text(encoding="utf-8")
    cab, cuerpo = txt.split("[Events]", 1)
    cab = _estilos(cab)
    lineas = cuerpo.split("\n")
    etiquetas = set()  # (ini, fin) de las etiquetas: su caja negra se quita
    for ln in lineas:
        if ln.startswith("Dialogue: "):
            capa, a, z, est, *_r, tx = _partir(ln)
            if est == "Dato" and _limpio(tx).lstrip().startswith("@"):
                etiquetas.add((a, z))
    nuevas, extra, paneles = [], [], []
    for ln in lineas:
        if not ln.startswith("Dialogue: "):
            nuevas.append(ln)
            continue
        capa, a, z, est, nom, ml, mr, mv, ef, tx = _partir(ln)
        if est == "SubSombra":
            continue
        if est == "Sub":
            ln = f"Dialogue: 11,{a},{z},{est},{nom},{ml},{mr},{mv},{ef},{{\\blur0.6}}{tx}"
        elif est == "Dibujo" and "\\c&H000000&" in tx:
            caja = re.search(r"m 0 0 l (\d+) 0 \1 (\d+) 0 \2", tx)
            if not caja:
                nuevas.append(ln)
                continue
            if (a, z) in etiquetas:
                continue
            # 11 nov (2.ª versión): pantalla completa en estilo cristal. Fondo = fotograma quieto y muy difuminado
            # (lo hace filtros() con CONGELAR + panel de toda la pantalla), velo oscuro y tarjeta de cristal en el centro.
            t0, t1 = s_ass(a), s_ass(z)
            CONGELAR.append((t0, t1))
            paneles.append((0, 0, W, H, t0, t1))
            fad = "\\fad(250,250)"
            ln = (f"Dialogue: 8,{a},{z},Dibujo,,0,0,0,,{{\\pos(0,0)\\c{TINTE}\\1a&H78&\\bord0\\shad0{fad}\\p1}}"
                  f"m 0 0 l {W} 0 {W} {H} 0 {H}")
            cx, cy, cw, ch = 300, 330, 1320, 420
            extra.append(tarjeta(9, a, z, cx, cy, cw, ch, alfa="&HA0&", r=48, fad=fad))
            extra.append(f"Dialogue: 9,{a},{z},Dibujo,,0,0,0,,{{\\pos({cx + 48},{cy + 2})\\c&HFFFFFF&\\1a&HC8&\\bord0\\shad0{fad}\\p1}}"
                         f"m 0 0 l {cw - 96} 0 {cw - 96} 2 0 2")  # brillo de la arista de arriba
            extra.append(f"Dialogue: 10,{a},{z},Dato,,0,0,0,,{{\\an5\\pos(960,{cy + 62})\\fs28\\fsp6\\c{TURQUESA}{fad}}}"
                         "● LEÓNIDA AL DÍA")
        elif est == "Dato":
            limpio = _limpio(tx).lstrip()
            if limpio.startswith("@"):
                filas = limpio[1:].split("\\N")
                nombre, papel = filas[0].strip(), (filas[1].strip() if len(filas) > 1 else "")
                w = int(max(len(nombre) * 46 * 0.62, len(papel) * 28 * 0.6)) + 72
                x, y, h = 64, 70, 118 if papel else 82
                extra.append(tarjeta(9, a, z, x, y, w, h, r=24, fad="\\fad(200,250)"))
                ln = (f"Dialogue: 10,{a},{z},Dato,,0,0,0,,{{\\an7\\pos({x + 36},{y + 18})\\fad(200,250)\\fs46\\c&HFFFFFF&}}"
                      f"{nombre}" + (f"\\N{{\\fs28\\c{TURQUESA}}}{papel}" if papel else ""))
            else:
                ln = f"Dialogue: 10,{a},{z},{est},{nom},{ml},{mr},{mv},{ef},{_caja_texto(tx)}"
        elif est == "CartAnio":  # tarjeta detrás de cada cartela de acto (el fondo ya es un fotograma difuminado)
            extra.append(tarjeta(4, a, z, 510, 215, 900, 540, r=36, fad="\\fad(120,160)"))
        nuevas.append(ln)
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
    escala = f"scale={SALIDA[0]}:{SALIDA[1]}:flags=lanczos"
    partes, cur = [], entrada
    for k, (t0, t1) in enumerate(CONGELAR):  # fondo quieto en los carteles a pantalla completa
        f0, f1 = int(round(t0 * fps)), int(round(t1 * fps))
        partes.append(f"[{cur}]split[fz{k}a][fz{k}b];[fz{k}a][fz{k}b]freezeframes=first={f0}:last={f1}:replace={f0}[fz{k}];")
        cur = f"fz{k}"
    if not paneles:
        return [], "".join(partes) + f"[{cur}]{escala}[{salida}];"
    args = []
    for i, (x, y, w, h, t0, t1) in enumerate(paneles):
        x, y = max(0, x - x % 2), max(0, y - y % 2)  # medidas pares: el vídeo es yuv420p
        w, h = min(W - x, w + w % 2), min(H - y, h + h % 2)
        r = 0 if (w, h) == (W, H) else min(36 if h > 400 else 28, h // 2)
        m = pathlib.Path(tmp) / f"mascara_{i:03d}.png"
        mascara(m, w, h, r)
        d = max(0.1, t1 - t0)
        args += ["-loop", "1", "-framerate", str(fps), "-t", f"{d:.2f}", "-i", str(m)]
        sig = 40 if (w, h) == (W, H) else 22
        sal = "crfin" if i == len(paneles) - 1 else f"cr{i}"
        partes.append(
            f"[{cur}]split[c{i}][s{i}];"
            f"[s{i}]trim=start={t0:.3f}:end={t1:.3f},setpts=PTS-STARTPTS,crop={w}:{h}:{x}:{y},"
            f"gblur=sigma={sig},eq=brightness=-0.05:saturation=1.15[b{i}];"
            f"[{idx0 + i}:v]format=gray[m{i}];"
            f"[b{i}][m{i}]alphamerge,setpts=PTS+{t0:.3f}/TB[g{i}];"
            f"[c{i}][g{i}]overlay={x}:{y}:eof_action=pass[{sal}];")
        cur = sal
    partes.append(f"[crfin]{escala}[{salida}];")
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
