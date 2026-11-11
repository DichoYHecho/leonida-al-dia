"""PLANTILLA de vídeo largo de «Leónida al Día». Para un vídeo nuevo: copiar como guion_<id>.py (id corto: lc, cc…)
y, si trae vídeos nuevos, fuentes_<id>.py (mismo formato que fuentes_sg.py). Todo lo demás es común.

Campos de cada bloque (ver guion_sg.py como ejemplo completo):
  id, num, total, titulo, capitulo, overlay      -> identificación y capítulo de YouTube
  cartela {anio, acto, titulo} + intro_original  -> opcional: cartela quieta de acto + 2-3 s de sonido original
  anio / etiqueta_linea                          -> opcional: línea de tiempo de abajo (si hay LINEA)
  texto                                          -> lo que dice la voz (datos comprobados, con fuente en el doc)
  rotulos [{en: palabra, texto: "LÍNEA 1|LÍNEA 2"}] -> carteles del centro (caja negra)
  nombres                                        -> palabras que TIENEN que salir en pantalla (plano o cartel)
  planos ["Trozo", "@Grupo:N"]                   -> material del bloque, sin repetir
  planos_en [{en: palabra, plano: ...}]          -> el plano que sale justo al decir esa palabra
"""
from fonetica_comun import voz

VIDEOS_EXTRA = {}          # {"Clave": "url del vídeo"}; con fuentes_<id>.py: {k: v["url"] for k, v in FUENTES.items()}
RECORTES = {}              # {"Clave": 0.075} -> quita una franja de arriba (marcas de agua)
MARCO = True               # partidas de baja resolución en marco sobre fondo borroso
PLANOS_FIJOS = set()       # logos, carteles y fotos: siempre quietos
MUSICA = {"hook": "synthwave"}  # estilo desde ese bloque; cambia sola si una pista pasa de 3,5 min
LINEA, LINEA_ANIMADA = [], False
FONETICA_EXTRA = {}        # solo las palabras nuevas de este vídeo

T = 1
BLOQUES = [
    {"id": "hook", "num": None, "titulo": "", "overlay": "", "capitulo": "Introducción",
     "texto": "Texto del gancho.",
     "rotulos": [], "nombres": [], "planos": [], "planos_en": []},
    {"id": "cierre", "num": None, "titulo": "", "overlay": "", "capitulo": "Cierre",
     "texto": "Texto del cierre.",
     "rotulos": [], "nombres": [], "planos": [], "planos_en": []},
]

for _b in BLOQUES:
    _b["voz"] = voz(_b["texto"], FONETICA_EXTRA)
