"""Configuración del proyecto «Leónida al Día» (GTA 6). Sin claves: las claves van como secrets de GitHub."""
import os
from datetime import date
from zoneinfo import ZoneInfo

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
MADRID = ZoneInfo("Europe/Madrid")

# Airtable (cuenta de adria.sanandreas, base «Panel GTA 6»)
BASE = "appLYUwqO5EjDfQtX"
T_PUB = "Publicaciones"
T_DATOS = "Datos"

# Buffer (segunda cuenta Free, la de adria.sanandreas)
CANAL_IG = "6ad768d7778b240e2f697abc"
CANAL_TT = "6ad7696b778b240e2f69823a"
CANAL_YT = "6ae49b912f1f5ed648202118"  # canal nuevo @LeonidaalDiaGTA6 (30 oct 2026)
YT_CATEGORIA = "20"  # Videojuegos

# Gemini
MODELOS_TEXTO = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite"]
MODELOS_VOZ = ["gemini-3.8-flash-tts", "gemini-3.8-flash-lite-tts"]
VOZ = "Orus"  # 9 nov: la misma voz que los vídeos largos en todos los vídeos (antes Mako, estilo «Promote»)
# 2 nov: la voz se pasaba al inglés a mitad de algunos vídeos; se le pide español de España de principio a fin
ESTILO_VOZ = ("Habla todo el texto en español de España, de principio a fin, sin pasar nunca al inglés "
              "(los nombres en inglés se dicen tal cual, sin cambiar de idioma). "
              "Relaxed, friendly Spanish gaming YouTuber telling a funny story to a friend. "
              "Native Castilian Spanish accent from Spain. Warm and close, light humour, natural pauses "
              "between sentences, lively but never rushed, never sounds like an advert or a radio announcer.")
VELOCIDAD_VOZ = 1.12  # +12 %, como en los vídeos largos

# Calendario
LANZAMIENTO = date(2026, 11, 19)
ARRANQUE = date(2026, 10, 21)   # primera publicación (adelantada el 21 oct; antes, el 26)

# Contenido
HASHTAGS_FIJOS = ["#GTA6", "#GTAVI", "#Videojuegos"]
PIE_POST = "Imágenes: Rockstar Games. Cuenta de fans, sin relación con Rockstar Games."
CADUCA_HORAS = 36            # una noticia sin publicar en 36 h pasa a «Caducada»
MAX_NOTICIAS_MANANA = 3
MAX_NOTICIAS_TARDE = 2
DATOS_EN_COLA = 3            # datos pendientes (por revisar o aprobados) que tiene que haber siempre (3 publicaciones al día)

UA = "LeonidaAlDiaBot/1.0 (cuenta de fans de GTA 6; https://www.youtube.com/@leonidaaldia) GitHubActions"

FUENTES_RSS = [
    ("Vandal", "https://vandal.elespanol.com/xml.cgi"),
    ("3DJuegos", "https://www.3djuegos.com/feedburner.xml"),
    ("VGC", "https://www.videogameschronicle.com/feed/"),
    ("Push Square", "https://www.pushsquare.com/feeds/latest"),
    ("Take-Two", "https://ir.take2games.com/rss/news-releases.xml"),
]
OFICIALES = {"Rockstar Games", "Take-Two"}

# Rockstar Newswire: la web carga las noticias de su API pública con consultas guardadas.
# Si Rockstar cambia estas huellas, el paso avisa y se sigue con el resto de fuentes.
GRAPH = "https://graph.rockstargames.com/"
HASH_LISTA = "7ec00215aecc70de257b0719a1dfcfa84fe57fdc7bf5c10ec2e8f377defede58"
HASH_POST = "555658813abe5acc8010de1a1feddd6fd8fddffbdc35d3723d4dc0fe4ded6810"

# Material oficial
ZIP_CAPTURAS = "https://media-rockstargames-com.akamaized.net/VI/downloads/screenshots/GTAVI_Screenshots.zip"
# «Una mirada extendida» (27 ago 2026), el único vídeo largo de Rockstar en MP4: de ahí salen los trozos (trozos.csv)
VIDEO_OFICIAL = "https://videos-rockstargames-com.akamaized.net/v4/rk721912/flv/es-es-1080p.mp4"
CACHE = os.path.join(RAIZ, "cache")


def cuenta_atras(dia):
    """Texto de la pastilla rosa según el día de publicación."""
    n = (LANZAMIENTO - dia).days
    if n > 1:
        return f"FALTAN {n} DÍAS"
    if n == 1:
        return "¡MAÑANA SALE!"
    if n == 0:
        return "¡HOY SALE GTA 6!"
    return f"DÍA {-n + 1} DE GTA 6"
