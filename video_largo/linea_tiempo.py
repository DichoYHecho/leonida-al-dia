"""Línea de tiempo animada del vídeo 3 (se hace aparte y el montaje la pone encima, por debajo de los subtítulos).

Es una franja transparente de 1920 x 200 px para la parte de abajo del vídeo (y = 880 a 1080):
  - al empezar, la línea se dibuja de izquierda a derecha y van apareciendo los hitos (un juego por punto);
  - en cada bloque con «anio», el cabezal rosa viaja al año nuevo con aceleración suave, deja una estela
    de luz, y cada hito que cruza se enciende con un pequeño rebote y una onda;
  - a la izquierda, el año gira como un cuentakilómetros (1997 → 1998 → 1999…);
  - encima del cabezal, el nombre del juego entra subiendo y se va desvaneciendo;
  - el cabezal respira con un halo suave mientras está quieto;
  - al llegar a 2026, un brillo recorre toda la línea.
Nada mueve la cámara ni los carteles: solo se anima la propia línea.

Uso suelto (demo):  python3 linea_tiempo.py demo salida.mov
En el montaje:      render(eventos, total, ruta) con eventos = [(segundo, año, nombre), ...]
"""
import math
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, ALTO, Y0 = 1920, 200, 880          # franja: de y = 880 a 1080
YC = 1062 - Y0                         # altura de la línea dentro de la franja (pegada al borde de abajo)
X0, X1 = 70, W - 70                    # primer y último año (la línea va de punta a punta: de 0 a W)
TAM_ANIO = 34                          # tamaño del año que gira (va encima del cabezal, con el nombre del juego)
FPS = 30
ROSA = np.array([255, 79, 163], np.float32) / 255
ROSA_OSCURO = np.array([194, 24, 120], np.float32) / 255
ROSA_CLARO = np.array([255, 170, 210], np.float32) / 255
BLANCO = np.array([1, 1, 1], np.float32)
FUENTE_NUM = "/usr/share/fonts/opentype/bebas-neue/BebasNeue-Bold.otf"
FUENTE_TXT = "/usr/share/fonts/opentype/montserrat/Montserrat-ExtraBold.otf"
D_VIAJE = 1.15                         # segundos del viaje del cabezal


# ---------------------------------------------------------------- utilidades
def suave(x):  # ease in-out cúbica
    x = min(1.0, max(0.0, x))
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def salida_suave(x):  # ease out cúbica
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


def rebote(x):  # ease out back (pasa un poco de largo y vuelve)
    x = min(1.0, max(0.0, x))
    c1, c3 = 1.9, 2.9
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def pegar(lienzo, sprite, cx, cy, alfa=1.0):
    """Mezcla un sprite RGBA premultiplicado (float) centrado en (cx, cy), con posición subpíxel."""
    if alfa <= 0.003:
        return
    h, w = sprite.shape[:2]
    fx, fy = cx - w / 2, cy - h / 2
    ix, iy = int(math.floor(fx)), int(math.floor(fy))
    dx, dy = fx - ix, fy - iy
    if dx > 0.02 or dy > 0.02:  # desplazamiento subpíxel bilineal
        s = np.zeros((h + 1, w + 1, 4), np.float32)
        s[:h, :w] += sprite * (1 - dx) * (1 - dy)
        s[:h, 1:] += sprite * dx * (1 - dy)
        s[1:, :w] += sprite * (1 - dx) * dy
        s[1:, 1:] += sprite * dx * dy
        sprite, h, w = s, h + 1, w + 1
    a0, b0 = max(0, iy), max(0, ix)
    a1, b1 = min(lienzo.shape[0], iy + h), min(lienzo.shape[1], ix + w)
    if a1 <= a0 or b1 <= b0:
        return
    trozo = sprite[a0 - iy:a1 - iy, b0 - ix:b1 - ix] * alfa
    destino = lienzo[a0:a1, b0:b1]
    destino *= (1 - trozo[..., 3:4])
    destino += trozo


def sprite_de(img):
    a = np.asarray(img, np.float32) / 255
    a[..., :3] *= a[..., 3:4]
    return a


def circulo(radio, color, borde=0.0, color_borde=None, alfa=1.0, escala=4):
    r = radio * escala
    tam = int(math.ceil(radio * 2 + 4)) * escala
    img = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c = tam / 2
    col = tuple(int(v * 255) for v in color) + (int(255 * alfa),)
    if borde:
        cb = tuple(int(v * 255) for v in color_borde) + (int(255 * alfa),)
        d.ellipse([c - r, c - r, c + r, c + r], fill=cb)
        r2 = r - borde * escala
        d.ellipse([c - r2, c - r2, c + r2, c + r2], fill=col)
    else:
        d.ellipse([c - r, c - r, c + r, c + r], fill=col)
    return sprite_de(img.resize((tam // escala, tam // escala), Image.LANCZOS))


def anillo(radio, grosor, color, escala=4):
    tam = int(math.ceil(radio * 2 + grosor + 4)) * escala
    img = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c, r = tam / 2, radio * escala
    d.ellipse([c - r, c - r, c + r, c + r], outline=tuple(int(v * 255) for v in color) + (255,),
              width=max(1, int(grosor * escala)))
    return sprite_de(img.resize((tam // escala, tam // escala), Image.LANCZOS))


def halo(radio, color, fuerza=1.0):
    tam = int(radio * 4)
    yy, xx = np.mgrid[0:tam, 0:tam] - (tam - 1) / 2
    a = np.exp(-(xx ** 2 + yy ** 2) / (2 * (radio * 0.75) ** 2)).astype(np.float32) * fuerza
    s = np.zeros((tam, tam, 4), np.float32)
    s[..., :3] = color * a[..., None]
    s[..., 3] = a
    return s


def texto(txt, fuente, tam, color, espaciado=0.0, sombra=True, escala=3):
    f = ImageFont.truetype(fuente, tam * escala)
    anchos = [f.getbbox(ch)[2] - f.getbbox(ch)[0] if ch != " " else tam * escala * 0.3 for ch in txt]
    total = int(sum(anchos) + espaciado * escala * (len(txt) - 1)) + 12 * escala
    alto = int(tam * escala * 1.45)
    img = Image.new("RGBA", (total, alto), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = 6 * escala
    for ch, an in zip(txt, anchos):
        d.text((x - f.getbbox(ch)[0], int(tam * escala * 0.1)), ch, font=f, fill=tuple(int(v * 255) for v in color) + (255,))
        x += an + espaciado * escala
    img = img.resize((total // escala, alto // escala), Image.LANCZOS)
    if sombra:  # sombra suave detrás para que se lea sobre cualquier fondo
        som = Image.new("RGBA", img.size, (0, 0, 0, 0))
        som.putalpha(img.getchannel("A").filter(ImageFilter.GaussianBlur(3)).point(lambda v: int(v * 0.75)))
        base = Image.new("RGBA", (img.width + 8, img.height + 8), (0, 0, 0, 0))
        base.alpha_composite(som, (4, 6))
        base.alpha_composite(img, (4, 4))
        img = base
    return sprite_de(img)


# ---------------------------------------------------------------- la línea
class Linea:
    def __init__(self, hitos, eventos, total):
        """hitos = [(año, nombre)] de la línea; eventos = [(segundo, año, nombre)] (cambios del cabezal)."""
        self.a0, self.a1 = hitos[0][0], hitos[-1][0]
        self.hitos = hitos
        self.eventos = sorted(eventos)
        self.total = total
        self.y = np.arange(ALTO, dtype=np.float32)[:, None]
        self.x = np.arange(W, dtype=np.float32)[None, :]
        grad = np.clip(self.x / W, 0, 1)[0]
        self.col_relleno = (ROSA_OSCURO[None, :] * (1 - grad[:, None]) + ROSA[None, :] * grad[:, None])
        # sprites
        self.punto_futuro = circulo(5.0, np.array([0.08, 0.06, 0.1]), 1.6, BLANCO, alfa=0.9)
        self.punto_pasado = circulo(5.5, ROSA, 1.6, BLANCO)
        self.cabezal = circulo(10.5, BLANCO, 3.2, ROSA)
        self.halo_cab = halo(16, ROSA, 0.75)
        self.halo_punto = halo(9, ROSA, 0.6)
        self.anillos = {}
        self.cache_punto = {}
        self.nombres = {}
        self.digitos = [texto(str(i), FUENTE_NUM, TAM_ANIO, BLANCO, sombra=True) for i in range(10)]
        self.fin_txt = texto(str(self.a1), FUENTE_NUM, 22, BLANCO, sombra=True)
        self.t0 = self.eventos[0][0] if self.eventos else 0.0  # la línea aparece cuando empieza la explicación

    def xa(self, anio):
        return X0 + (X1 - X0) * (anio - self.a0) / (self.a1 - self.a0)

    def nombre_sprite(self, nombre):
        if nombre not in self.nombres:
            self.nombres[nombre] = texto(nombre.upper(), FUENTE_TXT, 15, ROSA_CLARO, espaciado=2.2)
        return self.nombres[nombre]

    def punto(self, pasado, escala):
        clave = (pasado, round(escala, 2))
        if clave not in self.cache_punto:
            base = self.punto_pasado if pasado else self.punto_futuro
            if abs(escala - 1) < 0.01:
                self.cache_punto[clave] = base
            else:
                h, w = base.shape[:2]
                img = Image.fromarray((np.clip(base, 0, 1) * 255).astype(np.uint8), "RGBA")
                tam = max(2, int(round(w * escala)))
                self.cache_punto[clave] = np.asarray(img.resize((tam, tam), Image.LANCZOS), np.float32) / 255
        return self.cache_punto[clave]

    def anillo(self, r):
        r = round(r * 2) / 2
        if r not in self.anillos:
            self.anillos[r] = anillo(r, 1.6, ROSA_CLARO)
        return self.anillos[r]

    # estado del cabezal en el segundo t
    def estado(self, t):
        prev = None
        for k, (te, anio, nombre) in enumerate(self.eventos):
            if t < te:
                break
            prev = k
        if prev is None:
            return None
        te, anio, nombre = self.eventos[prev]
        if prev == 0:
            return {"x": self.xa(anio), "anio": anio, "nombre": nombre, "desde": None, "p": 1.0, "t_ev": te,
                    "anio_ant": anio, "nombre_ant": None, "llegada": te}
        _, anio_ant, nombre_ant = self.eventos[prev - 1]
        p = suave((t - te) / D_VIAJE)
        x = self.xa(anio_ant) + (self.xa(anio) - self.xa(anio_ant)) * p
        return {"x": x, "anio": anio, "nombre": nombre, "desde": self.xa(anio_ant), "p": p, "t_ev": te,
                "anio_ant": anio_ant, "nombre_ant": nombre_ant, "llegada": te + D_VIAJE}

    def cuando_pasa(self, anio_hito):
        """Segundo en que el cabezal llega o cruza por primera vez el hito."""
        xh = self.xa(anio_hito)
        for k, (te, anio, _) in enumerate(self.eventos):
            if k == 0:
                if self.xa(anio) >= xh - 0.5:
                    return te
                continue
            xa0, xa1 = self.xa(self.eventos[k - 1][1]), self.xa(anio)
            if xa1 >= xh - 0.5 > xa0 - 0.5 and xa1 > xa0:
                # resolver suave(p) = fracción
                f = (xh - xa0) / (xa1 - xa0)
                lo, hi = 0.0, 1.0
                for _ in range(30):
                    mid = (lo + hi) / 2
                    if suave(mid) < f:
                        lo = mid
                    else:
                        hi = mid
                return te + lo * D_VIAJE
        return None

    def frame(self, t):
        L = np.zeros((ALTO, W, 4), np.float32)
        aparece = salida_suave((t - self.t0) / 0.9)  # se dibuja de izquierda a derecha al empezar la explicación
        if aparece <= 0:
            return L
        x_fin_pista = W * aparece
        # pista, de punta a punta
        cobertura = np.clip(x_fin_pista - self.x, 0, 1)
        perfil = np.clip(1.6 - np.abs(self.y - YC), 0, 1)
        a = (perfil * cobertura * 0.30)[..., None]
        L[..., :3] += BLANCO * a
        L[..., 3:4] += a
        st = self.estado(t)
        # relleno rosa con brillo
        if st:
            xr = st["x"]
            cov = np.clip(xr - self.x, 0, 1)
            nucleo = np.clip(2.3 - np.abs(self.y - YC), 0, 1)
            brillo = np.exp(-((self.y - YC) ** 2) / (2 * 4.5 ** 2)) * 0.45
            # destello que recorre la línea al llegar al final
            fin_t = self.eventos[-1][0] + D_VIAJE if st["anio"] == self.a1 else None
            extra = 0
            if fin_t is not None and t > fin_t:
                xs = -200 + (W + 400) * salida_suave((t - fin_t) / 1.6)
                extra = np.exp(-((self.x - xs) ** 2) / (2 * 60 ** 2)) * (1 - salida_suave((t - fin_t - 1.2) / 1.0))
            cuerpo = (nucleo + brillo * (1 + 1.5 * extra)) * cov
            claro = np.zeros((1, W), np.float32)
            # estela: más luz y más clara cerca del cabezal mientras viaja
            if st["desde"] is not None and st["p"] < 1:
                vel = math.sin(math.pi * st["p"])
                estela = np.exp(-np.clip(xr - self.x, 0, None) / 90.0) * cov * vel
                cuerpo = cuerpo + estela * np.exp(-((self.y - YC) ** 2) / (2 * 3.0 ** 2)) * 0.9
                claro = claro + estela * 0.8
            if isinstance(extra, np.ndarray):
                claro = claro + extra * 0.9
            cuerpo = np.clip(cuerpo, 0, 1)
            claro = np.clip(claro, 0, 1)[0][None, :, None]
            color = self.col_relleno[None, :, :] * (1 - claro) + ROSA_CLARO * claro * 0.6 + BLANCO * claro * 0.4
            a = cuerpo[..., None]
            L[..., :3] = L[..., :3] * (1 - a) + color * a
            L[..., 3:4] = L[..., 3:4] * (1 - a) + a
        # hitos
        for i, (anio, _) in enumerate(self.hitos):
            xh = self.xa(anio)
            ap = rebote((t - self.t0 - 0.2 - i * 0.09) / 0.45)
            if ap <= 0.01 or xh > x_fin_pista + 6:
                continue
            tp = self.cuando_pasa(anio)
            pasado = tp is not None and t >= tp
            esc = ap
            if pasado:
                k = (t - tp) / 0.5
                if k < 1:
                    esc = 1 + 0.9 * math.sin(math.pi * k) * (1 - k * 0.3)
                    r = 5 + 22 * salida_suave(k)
                    pegar(L, self.anillo(r), xh, YC, (1 - k) * 0.9)
                pegar(L, self.halo_punto, xh, YC, 0.5)
            pegar(L, self.punto(pasado, esc), xh, YC)
        # el año final, pequeño, encima del último hito (se aparta cuando llega el cabezal)
        if not st or st["x"] < X1 - 260:
            pegar(L, self.fin_txt, X1, YC - 24, 0.55 * aparece)
        if not st:
            return L
        # cabezal con halo que respira
        quieto = st["p"] >= 1
        resp = 0.75 + 0.25 * math.sin(2 * math.pi * (t - st["llegada"]) / 2.6) if quieto else 1.0
        entrada = rebote((t - st["t_ev"] - 0.6) / 0.5) if st["desde"] is None else 1.0
        if entrada <= 0.01:
            return L
        pegar(L, self.halo_cab, st["x"], YC, 0.9 * resp * min(1, entrada))
        cab = self.cabezal
        if entrada < 0.999:
            img = Image.fromarray((np.clip(cab, 0, 1) * 255).astype(np.uint8), "RGBA")
            tam = max(2, int(cab.shape[1] * max(0.05, entrada)))
            cab = np.asarray(img.resize((tam, tam), Image.LANCZOS), np.float32) / 255
        pegar(L, cab, st["x"], YC)
        # etiqueta encima del cabezal: el año gira como un cuentakilómetros y al lado entra el nombre del juego
        ancho_anio = 4 * (self.digitos[0].shape[1] - 15)
        w_nom = max(self.nombre_sprite(st["nombre"]).shape[1],
                    self.nombre_sprite(st["nombre_ant"]).shape[1] if st["nombre_ant"] else 0)
        total = ancho_anio + 8 + w_nom
        cx = min(max(st["x"], total / 2 + 18), W - total / 2 - 18)
        x_der = cx - total / 2 + ancho_anio
        y_et = YC - 30
        v = st["anio_ant"] + (st["anio"] - st["anio_ant"]) * st["p"]
        self.cuentakm(L, v, x_der, y_et, min(1, entrada * 1.2))
        if st["nombre_ant"] and st["p"] < 1:
            sale = salida_suave((t - st["t_ev"]) / 0.35)
            spr = self.nombre_sprite(st["nombre_ant"])
            pegar(L, spr, x_der + 8 + spr.shape[1] / 2, y_et + 2 - 8 * sale, 1 - sale)
        llega = salida_suave((t - (st["llegada"] - 0.25)) / 0.5) * min(1, entrada)
        if llega > 0:
            spr = self.nombre_sprite(st["nombre"])
            pegar(L, spr, x_der + 8 + spr.shape[1] / 2, y_et + 2 + 10 * (1 - llega), llega)
        return L

    def cuentakm(self, L, v, x_der, yc, alfa):
        alto = TAM_ANIO * 1.0
        ancho = self.digitos[0].shape[1] - 15
        cifras = []
        for p in range(4):
            # cada cifra gira solo mientras todas las de su derecha pasan de 9…9 a 0…0 (como un cuentakilómetros)
            pot = 10 ** p
            d = (v // pot) % 10 + (max(0.0, (v % pot) - (pot - 1)) if p else v % 1)
            cifras.append(d % 10)
        h_ventana = alto * 0.92
        for p, d in enumerate(cifras):
            cx = x_der - (p + 0.5) * ancho
            entero = int(math.floor(d))
            frac = d - entero
            for k, (dig, off) in enumerate(((entero % 10, -frac), ((entero + 1) % 10, 1 - frac))):
                dy = off * h_ventana
                vis = max(0.0, 1 - abs(off) * 1.15)
                if vis <= 0.01:
                    continue
                pegar(L, self.digitos[dig], cx, yc + dy, alfa * vis)


def render(hitos, eventos, total, salida, desde=0.0):
    lin = Linea(hitos, eventos, total)
    n = int(round((total - desde) * FPS))
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{ALTO}",
                             "-r", str(FPS), "-i", "-", "-c:v", "qtrle", "-pix_fmt", "argb", str(salida)],
                            stdin=subprocess.PIPE)
    previo, cache = None, None
    for i in range(n):
        t = desde + i / FPS
        L = lin.frame(t)
        a = np.clip(L[..., 3:4], 1e-6, 1)
        rgb = np.where(L[..., 3:4] > 1e-4, L[..., :3] / a, 0)
        out = np.concatenate([np.clip(rgb, 0, 1), np.clip(L[..., 3:4], 0, 1)], axis=2)
        b = (out * 255 + 0.5).astype(np.uint8).tobytes()
        proc.stdin.write(b)
    proc.stdin.close()
    proc.wait()
    return salida


DEMO_HITOS = [(1997, "GTA"), (1999, "GTA 2"), (2001, "GTA III"), (2002, "Vice City"), (2004, "San Andreas"),
              (2008, "GTA IV"), (2013, "GTA V"), (2026, "GTA VI")]
DEMO_EVENTOS = [(5.0, 1997, "GTA"), (8.5, 1999, "GTA 2"), (12.0, 2001, "GTA III"), (15.0, 2002, "Vice City"),
                (18.0, 2004, "San Andreas"), (21.0, 2004, "Portátiles"), (24.0, 2008, "GTA IV"), (27.0, 2009, "Episodios"),
                (30.0, 2013, "GTA V"), (33.0, 2013, "GTA Online"), (36.0, 2023, "El anuncio"), (40.0, 2026, "GTA VI")]

if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "demo":
        render(DEMO_HITOS, DEMO_EVENTOS, 45.0, sys.argv[2])
