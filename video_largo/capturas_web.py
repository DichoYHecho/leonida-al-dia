"""Cambia en trozos_57.csv las tarjetas «PLANO PENDIENTE» que ya tienen captura web real.
Las capturas (1920x1080) están en imagenes/; cada fila pasa al grupo Capturas_57 y apunta a su imagen."""
import csv, io
from pathlib import Path

AQUI = Path(__file__).parent
BASE = "Imagen:https://raw.githubusercontent.com/DichoYHecho/leonida-al-dia/videos-5-7/video_largo/imagenes/"

CAPTURAS = {  # nombre: (qué se ve, fuente)
    "NUEVO_Captura_Disculpa_Rockstar": ("Nota de Rockstar sobre The Trilogy (Newswire, nov 2021)", "rockstargames.com/newswire"),
    "NUEVO_GTAPlus_Captura": ("Presentación de GTA+ (Newswire, 2022)", "rockstargames.com/newswire"),
    "NUEVO_RDO_Captura": ("Red Dead Online en el Newswire de Rockstar", "rockstargames.com/newswire"),
    "NUEVO_VGD_Captura": ("Comunicado de la compra de Video Games Deluxe (3 mar 2025)", "take2games.com"),
    "NUEVO_Comunicado_Rockstar": ("Cobertura: Rockstar confirma la intrusión (19 sep 2022)", "gamedeveloper.com"),
    "NUEVO_Filtracion_Foro": ("Cobertura de la filtración de 2022 (no el material robado)", "pcgamer.com"),
    "NUEVO_Cfx_Comunicado": ("Cobertura: Cfx.re se une a Rockstar (11 ago 2023)", "gameworldobserver.com"),
    "NUEVO_Houser_Captura": ("Cobertura: Dan Houser deja Rockstar (feb 2020)", "gamesradar.com"),
    "NUEVO_Captura_Steam_Resenas": ("Ficha de GTA V en Steam con el resumen de reseñas (sin usuarios)", "store.steampowered.com"),
    "NUEVO_Cuentas_TakeTwo": ("Resultados de Take-Two del año fiscal 2026: gasto recurrente y net bookings", "Business Wire (Take-Two)"),
    "NUEVO_Zelnick_Captura": ("Declaración de Strauss Zelnick en los resultados de mayo de 2026", "Business Wire (Take-Two)"),
    "NUEVO_Twitch_Captura": ("Estadísticas de GTA V en Twitch", "twitchtracker.com"),
}

ruta = AQUI / "trozos_57.csv"
texto = ruta.read_text(encoding="utf-8-sig")
filas = list(csv.reader(io.StringIO(texto)))
cab, cuerpo = filas[0], filas[1:]
iv = cab.index("Vídeo")
hechas = []
for f in cuerpo:
    if f and f[0] in CAPTURAS:
        assert (AQUI / "imagenes" / f"{f[0]}.png").exists(), f[0]
        f[1] = "Capturas_57"
        f[4] = CAPTURAS[f[0]][0]
        f[8] = f"Captura de {CAPTURAS[f[0]][1]}"
        f[iv] = BASE + f"{f[0]}.png"
        hechas.append(f[0])
salida = io.StringIO()
csv.writer(salida, lineterminator="\n").writerows([cab] + cuerpo)
ruta.write_text(salida.getvalue(), encoding="utf-8")
print(len(hechas), "capturas en la tabla:", ", ".join(hechas))
print("Faltan:", ", ".join(sorted(set(CAPTURAS) - set(hechas))) or "ninguna")
