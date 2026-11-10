"""Vídeos para el vídeo 4 («Jason y Lucía: todo lo que sabemos», sale el mié 18 nov 2026 a las 18:00).

Solo vídeo oficial de Rockstar. Pedido por mí el 10 nov:
  - planos más largos (min_dur / max_dur): trozos de 3,5 a 6 s, para que el vídeo tenga más calma;
  - casi sin repetir: DEDUP=1 en preparar_trozos.py descarta tomas casi iguales entre fuentes
    (el tráiler de lanzamiento y la mirada extendida reutilizan tomas de los tráileres 1 y 2).
Orden = prioridad: si una toma sale en dos vídeos, se queda la de la fuente que va antes.
Las partidas de GTA 1, GTA V y Vice City 2002 ya están troceadas en trozos-sg y trozos-vc.
preparar_trozos.py (FUENTES_MOD=fuentes_jl) deja los trozos y las hojas de contactos en la rama trozos-jl."""
from fuentes_vc import RS

_V = "https://media-rockstargames-com.akamaized.net/VI/downloads/videos/"
LARGO = {"min_dur": 3.5, "max_dur": 6.0}

FUENTES = {
    "LZ": {"grupo": "GTA6_Lanzamiento", "url": _V + "GTAVI_Launch_Trailer/GTAVI_Launch_Trailer.mp4", "max": 30, **LARGO},
    "T2": {"grupo": "GTA6_T2", "url": _V + "GTAVI_Trailer_2/GTAVI_Trailer_2.mp4", "max": 35, **LARGO},
    "T1": {"grupo": "GTA6_T1", "url": _V + "GTAVI_Trailer_1/GTAVI_Trailer_1.mp4", "max": 25, **LARGO},
    "MI": {"grupo": "GTA6_Mirada", "url": RS + "rk721912/flv/es-es-1080p.mp4", "max": 90, **LARGO},
    "RDR2": {"grupo": "RDR2_2018", "url": RS + "6c8k48rr/flv/en-us-1080p.mp4", "max": 10, **LARGO},
}
