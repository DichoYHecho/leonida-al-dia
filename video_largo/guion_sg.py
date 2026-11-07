"""Guion del vídeo largo 3 de «Leónida al Día»: «Toda la historia de GTA: de 1997 a GTA 6» (sale el vie 13 nov 2026).

Mismo formato que guion_vc.py (se elige con GUION=guion_sg). Novedades del vídeo 3 (ver montaje.py):
  cartela        -> cartela quieta de cada acto (año, acto y título) con golpe de sonido
  intro_original -> 2-3 s de un tráiler con su sonido después de la cartela (se añade al ver los trozos)
  anio           -> año del bloque en la línea de tiempo de abajo (LINEA); etiqueta_linea si es un periodo
  nombres        -> palabras del texto que nombran un juego, personaje, lugar o dato: tienen que salir en pantalla
                    (un plano en planos_en o un cartel en rotulos con esa palabra); lo comprueba comprobar_guion.py
  voz            -> se genera sola con FONETICA (palabras inglesas como se pronuncian y números romanos en cifra)
Datos comprobados el 6 nov 2026 (fuentes en el doc del guion y en el apartado Fuentes de la descripción).
"""
import re

from fuentes_sg import FUENTES as _FUENTES

VIDEOS_EXTRA = {k: v["url"] for k, v in _FUENTES.items()}
from fuentes_vc import FUENTES as _FUENTES_VC  # noqa: E402  (trozos de 1997-2006 del vídeo 2, rama trozos-vc)

VIDEOS_EXTRA.update({k: v["url"] for k, v in _FUENTES_VC.items() if k not in VIDEOS_EXTRA})
VIDEOS_EXTRA.update({
    "VC_Aniv": "https://videos-rockstargames-com.akamaized.net/v4/tror41c2/flv/en-us-720p.mp4",
    "VC_Comp": "https://videos-rockstargames-com.akamaized.net/v4/ao1c441c/flv/en-us-1080p60.mp4",
})

# Partidas con la marca de agua del canal arriba («GTASERIESVIDEOS.COM»): se recorta esa franja (fracción de la altura)
RECORTES = {k: 0.075 for k in _FUENTES if k.startswith(("LON_PC", "IV_PC", "TLAD_PC", "TBOGT_PC", "V_Juego", "ON_Juego"))}
MARCO = True  # las partidas de 360p van en un marco sobre una copia borrosa (no estiradas a pantalla completa)

PLANOS_FIJOS = {"GTA_15_01", "GTA_15_02", "GTA_15_15", "IMG_GTA1", "IMG_GTA1_Caja", "IMG_RaceNChase", "IMG_VC_Portada",
                "IMG_VCS_Portada", "VCA_Logo", "VCA_Rockstar_North", "VCA_Welcome", "Mirada_Logo", "T1_Letras_Vice",
                "Portada_Animada", "VL_Fecha", "VL_Rotulo_PS5", "Lanz_Final_19N"}

# Música por época: cambia con cada cartela (ninguna pista más de 3,5 min: el montaje cambia de variante)
MUSICA = {"hook": "synthwave", "p01": "chiptune", "p03": "breakbeat", "p07": "hiphop", "p11": "synthwave"}

# Línea de tiempo de abajo
LINEA_ANIMADA = True  # línea de tiempo animada aparte (linea_tiempo.py), aprobada por mí el 7 nov
LINEA = [(1997, "GTA"), (1999, "GTA 2"), (2001, "GTA III"), (2002, "VICE CITY"), (2004, "SAN ANDREAS"),
         (2008, "GTA IV"), (2013, "GTA V"), (2026, "GTA VI")]

# Pronunciación para la voz (misma cantidad de palabras que el texto: se cambia palabra por palabra)
FONETICA = {
    "III": "3", "IV": "4", "V": "5", "VI": "6", "Liberty": "Líberti", "City": "Siti", "Dundee": "Dandí",
    "Design": "Disáin", "Lemmings": "Lémings", "Race'n'Chase": "Réisenchéis", "Anywhere": "Énigüer",
    "Houser": "Jáuser", "North": "Norz", "Metacritic": "Métacritic", "Claude": "Clod", "Tommy": "Tomi",
    "Vercetti": "Verchéti", "Ray": "Rei", "Liotta": "Lióta", "Tenpenny": "Tenpeni", "Samuel": "Sámuel",
    "L.": "El", "Jackson": "Yákson", "Hot": "Jot", "Coffee": "Cófi", "Game": "Guéim", "Boy": "Boi",
    "Advance": "Advans", "Stories": "Stóris", "Chinatown": "Cháinataun", "Wars": "Uors", "Bellic": "Bélic",
    "RAGE": "Reich", "Euphoria": "Iufória", "Lost": "Lost", "Damned": "Dámd", "Ballad": "Bálad", "Gay": "Guei",
    "Tony": "Toni", "Michael": "Máikel", "Online": "Onlain", "CJ": "Siyéi", "London": "Lóndon", "Leonida": "Leónida",
}


def _voz(texto):
    salida = []
    for w in texto.split():
        if w in FONETICA:
            salida.append(FONETICA[w])
            continue
        m = re.match(r"^([¿¡(«]*)(.*?)([.,;:!?»)…]*)$", w)
        a, nucleo, z = m.groups()
        salida.append(a + FONETICA.get(nucleo, nucleo) + z)
    return " ".join(salida)


T = 12

BLOQUES = [
    # ---------------------------------------------------------------- HOOK
    {"id": "hook", "num": None, "titulo": "", "overlay": "", "capitulo": "Introducción",
     "texto": ("Imagina explicarle a alguien de 1997 que este juego de cochecitos vistos desde el cielo iba a acabar "
               "siendo uno de los lanzamientos más esperados de la historia. Pues aquí estamos: el diecinueve de "
               "noviembre sale GTA VI. Entre uno y otro, veintinueve años, siete grandes juegos y más de cuatrocientos "
               "setenta millones de copias. Hoy los repasamos todos, juego a juego, con lo que casi nadie recuerda de "
               "cada uno. Y fíjate bien en una ciudad del primer GTA, porque al final vuelve."),
     "rotulos": [{"t": 0.0, "dur": 2.4, "negro": True, "texto": "1997|→ 2026"},
                 {"en": "veintinueve", "texto": "29 AÑOS"},
                 {"en": "siete", "texto": "7 JUEGOS|PRINCIPALES"},
                 {"en": "copias", "texto": "+470 MILLONES|DE COPIAS"}],
     "nombres": ["cielo", "noviembre", "veintinueve", "siete", "copias", "ciudad"],
     "planos": ["GTA_15_01", "Mirada_Logo", "Lanz_Descapotable", "@GTA1_1997:3", "@GTA3_2001:2", "@SA_2004:2",
                "@GTA4_2008:2", "@GTA5_2013:2", "Lanz_Playa", "T1_Noche_Aerea"],
     "planos_en": [{"en": "cielo", "plano": "GTA_15_01"},
                   {"en": "noviembre", "plano": "Mirada_Logo"},
                   {"en": "repasamos", "plano": "@GTA3_2001"},
                   {"en": "ciudad", "plano": "@GTA1_1997"}]},

    # ---------------------------------------------------------------- ACTO I · DESDE EL CIELO (1997-1999)
    {"id": "p01", "num": 1, "total": T, "titulo": "1997 · GRAND THEFT AUTO", "capitulo": "1997 · Grand Theft Auto",
     "overlay": "", "anio": 1997,
     "cartela": {"anio": "1997", "acto": "ACTO I", "titulo": "DESDE EL CIELO"}, "intro_original": "G1_Demo1_01",
     "texto": ("Todo empieza en Escocia, en Dundee. Allí estaba DMA Design, un estudio que ya había dado el pelotazo "
               "con Lemmings, sí, los bichitos de pelo verde. Y estaban haciendo un juego de persecuciones llamado "
               "Race'n'Chase. La idea era jugar de policía. El problema: era aburrido. En las pruebas, lo divertido era "
               "ser el malo. Así que le dieron la vuelta, y nació Grand Theft Auto. Salió en Europa el veintiocho de "
               "noviembre de 1997: un juego visto desde arriba, con tres ciudades inspiradas en sitios reales. Liberty "
               "City, que es Nueva York. San Andreas, que es San Francisco. Y Vice City, que es Miami. Apúntate esta "
               "última. Para venderlo, contrataron a un publicista que convirtió la polémica por su violencia en "
               "publicidad gratis. Y vaya si funcionó: en marzo de 2001 ya llevaba seis millones de copias. Nada mal "
               "para unos coches del tamaño de una uña."),
     "rotulos": [{"en": "escocia", "texto": "DUNDEE|ESCOCIA"},
                 {"en": "estudio", "texto": "DMA DESIGN"},
                 {"en": "pelotazo", "texto": "LEMMINGS|1991"},
                 {"en": "llamado", "texto": "RACE'N'CHASE"},
                 {"en": "veintiocho", "texto": "28 NOV 1997|EUROPA"},
                 {"en": "nueva", "texto": "LIBERTY CITY|= NUEVA YORK"},
                 {"en": "francisco", "texto": "SAN ANDREAS|= SAN FRANCISCO"},
                 {"en": "miami", "texto": "VICE CITY|= MIAMI"},
                 {"en": "seis", "texto": "6 MILLONES|EN 2001"}],
     "nombres": ["escocia", "estudio", "pelotazo", "llamado", "grand", "veintiocho", "nueva", "francisco", "miami",
                 "publicista", "seis"],
     "planos": ["@GTA1_1997:28", "GTA_15_05", "GTA_15_06"],
     "planos_en": [{"en": "persecuciones", "plano": "IMG_RaceNChase"},
                   {"en": "grand", "plano": "IMG_GTA1_Caja"},
                   {"en": "arriba", "plano": "GTA_15_06"},
                   {"en": "publicista", "plano": "IMG_GTA1"}]},
    {"id": "p02", "num": 2, "total": T, "titulo": "1999 · LONDRES Y GTA 2", "capitulo": "1999 · London 1969 y GTA 2",
     "overlay": "", "anio": 1999,
     "texto": ("En 1999 la saga hace algo que no ha vuelto a repetir: salir de Estados Unidos. Con London 1969 nos vamos "
               "al Londres de los sesenta. Y ese mismo año llega GTA 2, en una ciudad sin nombre real, Anywhere City, "
               "con aire futurista y bandas que te respetan o te odian según para quién trabajes. Haces un encargo para "
               "una, y la de enfrente te recibe a tiros. Pero lo más importante de esos años no pasó dentro de un juego. "
               "En diciembre de 1998 nace en Nueva York una editora nueva: Rockstar Games. Entre sus fundadores, los "
               "hermanos Sam y Dan Houser. Y aquel estudio escocés acabaría siendo suyo: hoy se llama Rockstar North. "
               "GTA 2 fue la última vez que vimos un GTA principal desde arriba. Porque lo que venía después necesitaba "
               "otra cámara."),
     "rotulos": [{"en": "london", "texto": "LONDON 1969"},
                 {"en": "anywhere", "texto": "GTA 2|ANYWHERE CITY"},
                 {"en": "bandas", "texto": "BANDAS|RESPETO U ODIO"},
                 {"en": "diciembre", "texto": "DIC 1998|NACE ROCKSTAR GAMES"},
                 {"en": "hermanos", "texto": "SAM Y DAN HOUSER"},
                 {"en": "estudio", "texto": "DMA DESIGN|→ ROCKSTAR NORTH"}],
     "nombres": ["london", "anywhere", "bandas", "diciembre", "hermanos", "estudio", "north"],
     "planos": ["@London_1969:14", "@GTA2_1999:18", "GTA_15_07", "GTA_15_08"],
     "planos_en": [{"en": "london", "plano": "@London_1969"},
                   {"en": "anywhere", "plano": "@GTA2_1999"},
                   {"en": "bandas", "plano": "@GTA2_1999"},
                   {"en": "north", "plano": "VCA_Rockstar_North"},
                   {"en": "arriba", "plano": "GTA_15_08"}]},

    # ---------------------------------------------------------------- ACTO II · EL SALTO AL 3D (2001-2009)
    {"id": "p03", "num": 3, "total": T, "titulo": "2001 · GTA III", "capitulo": "2001 · GTA III", "overlay": "",
     "anio": 2001, "cartela": {"anio": "2001", "acto": "ACTO II", "titulo": "EL SALTO AL 3D"}, "intro_original": "G3_DE_01",
     "texto": ("Y entonces llega 2001 y todo cambia. Por primera vez, bajas a la calle. GTA III mete la saga en 3D, y "
               "Liberty City deja de ser un mapa para convertirse en una ciudad de verdad. Pero casi no sale como lo "
               "conocemos. Tras los atentados del once de septiembre, Rockstar lo retrasa tres semanas y lo repasa "
               "entero: los coches de policía, que se parecían demasiado a los de Nueva York, pasan a ser blancos y "
               "negros; un avión cambia su ruta para no pasar cerca de los rascacielos; quita una misión que hablaba de "
               "terroristas, y hasta rehace la portada. Al final sale el veintitrés de octubre en Estados Unidos, saca "
               "un noventa y siete en Metacritic y es el juego más vendido del año allí. Ah, y un detalle: su "
               "protagonista, Claude, no dice ni una palabra en todo el juego. Ni una. Quédate con eso, porque un año "
               "después cambia."),
     "rotulos": [{"en": "liberty", "texto": "LIBERTY CITY"},
                 {"en": "septiembre", "texto": "11-S|RETRASO DE 3 SEMANAS"},
                 {"en": "veintitrés", "texto": "23 OCT 2001|EE. UU."},
                 {"en": "noventa", "texto": "97|EN METACRITIC"},
                 {"en": "vendido", "texto": "MÁS VENDIDO|DE 2001 EN EE. UU."},
                 {"en": "claude", "texto": "CLAUDE|0 PALABRAS"}],
     "nombres": ["liberty", "septiembre", "policía", "avión", "portada", "veintitrés", "noventa", "vendido", "claude"],
     "planos": ["@GTA3_2001:30", "@GTA3_DE:4", "GTA_15_11", "GTA_15_12", "GTA_15_13", "GTA_15_14"],
     "planos_en": [{"en": "calle", "plano": "@GTA3_2001"},
                   {"en": "policía", "plano": "@GTA3_2001"},
                   {"en": "avión", "plano": "@GTA3_2001"},
                   {"en": "portada", "plano": "GTA_15_11"},
                   {"en": "claude", "plano": "@GTA3_DE"}]},
    {"id": "p04", "num": 4, "total": T, "titulo": "2002 · VICE CITY", "capitulo": "2002 · Vice City", "overlay": "",
     "anio": 2002,
     "texto": ("Y cambia en Vice City. Sí, la ciudad que te pedí que apuntaras. Rockstar se va a Miami en 1986: neón, "
               "trajes claros, deportivos y radios llenas de música de los ochenta. Y el protagonista, por fin, habla. "
               "Tommy Vercetti, con la voz de Ray Liotta, es el primer protagonista de la saga que habla. Hoy lo damos "
               "por hecho, pero en 2002 fue un cambio enorme: el personaje ya tenía carácter propio, no era solo el "
               "muñeco que tú movías. Vendió veinte millones de copias. Y si quieres la historia completa de esta "
               "ciudad, la tienes en el vídeo anterior del canal. Aquí solo te dejo una pista: hoy volvemos a hablar de "
               "ella."),
     "rotulos": [{"en": "miami", "texto": "VICE CITY|= MIAMI"},
                 {"en": "1986", "texto": "1986"},
                 {"en": "tommy", "texto": "TOMMY VERCETTI"},
                 {"en": "liotta", "texto": "VOZ:|RAY LIOTTA"},
                 {"en": "veinte", "texto": "20 MILLONES"}],
     "nombres": ["miami", "1986", "tommy", "liotta", "veinte", "anterior"],
     "planos": ["@Vice_City_2002:22", "@VC_DE:6", "GTA_15_16", "GTA_15_17", "GTA_15_18"],
     "planos_en": [{"en": "vice", "plano": "VCA_Logo"},
                   {"en": "neón", "plano": "VCA_Coches_Noche"},
                   {"en": "tommy", "plano": "VCA_Tommy_Yate"},
                   {"en": "carácter", "plano": "VCT_Tommy_Esmoquin"},
                   {"en": "anterior", "plano": "IMG_VC_Portada"}]},
    {"id": "p05", "num": 5, "total": T, "titulo": "2004 · SAN ANDREAS", "capitulo": "2004 · San Andreas", "overlay": "",
     "anio": 2004, "cta": True,
     "texto": ("En 2004, Rockstar se pasa de frenada. Ya no es una ciudad: es un estado entero. San Andreas, en 1992, "
               "con tres ciudades, Los Santos, San Fierro y Las Venturas, y campo, desierto y montañas entre medias. "
               "Treinta y seis kilómetros cuadrados: entre cuatro y seis veces más grande que GTA III o Vice City. Y CJ "
               "no solo conducía y disparaba: iba al gimnasio, comía, engordaba y adelgazaba. El reparto era de "
               "película: al policía corrupto, Tenpenny, le pone voz Samuel L. Jackson. También trajo la mayor polémica "
               "de la saga: un minijuego escondido en el código, Hot Coffee, por el que en Estados Unidos lo "
               "recalificaron durante un tiempo solo para adultos. Aun así, con más de diecisiete millones de copias, "
               "es el juego más vendido de PlayStation 2."),
     "rotulos": [{"en": "estado", "texto": "UN ESTADO|ENTERO"},
                 {"en": "1992", "texto": "1992"},
                 {"en": "santos", "texto": "LOS SANTOS · SAN FIERRO|LAS VENTURAS"},
                 {"en": "treinta", "texto": "36 KM²|×4 A ×6 GTA III"},
                 {"en": "tenpenny", "texto": "TENPENNY|VOZ: SAMUEL L. JACKSON"},
                 {"en": "hot", "texto": "HOT COFFEE"},
                 {"en": "diecisiete", "texto": "+17 MILLONES|EN PS2"}],
     "nombres": ["estado", "1992", "santos", "desierto", "treinta", "gimnasio", "tenpenny", "hot", "diecisiete"],
     "planos": ["@SA_2004:32", "@SA_DE:4", "GTA_15_25", "GTA_15_26", "GTA_15_27"],
     "planos_en": [{"en": "estado", "plano": "@SA_DE"},
                   {"en": "desierto", "plano": "@SA_2004"},
                   {"en": "gimnasio", "plano": "@SA_2004"},
                   {"en": "película", "plano": "@SA_DE"}]},
    {"id": "p06", "num": 6, "total": T, "titulo": "2004-2009 · PORTÁTILES", "capitulo": "2004-2009 · Las portátiles",
     "overlay": "", "anio": 2004, "etiqueta_linea": "2004-2009 · PORTÁTILES",
     "texto": ("Mientras tanto, GTA se mete en el bolsillo. GTA Advance en la Game Boy Advance. Liberty City Stories y "
               "Vice City Stories en PSP: un GTA en 3D en una consola portátil. Y Chinatown Wars en Nintendo DS, que "
               "recupera la cámara desde arriba, pero con pantalla táctil. La que más vendió fue Liberty City Stories: "
               "ocho millones de copias. Que se dice pronto, para un juego de bolsillo."),
     "rotulos": [{"en": "boy", "texto": "GTA ADVANCE|GBA · 2004"},
                 {"en": "liberty", "texto": "LIBERTY CITY STORIES|PSP · 2005"},
                 {"en": "vice", "texto": "VICE CITY STORIES|PSP · 2006"},
                 {"en": "chinatown", "texto": "CHINATOWN WARS|NINTENDO DS · 2009"},
                 {"en": "ocho", "texto": "8 MILLONES"}],
     "nombres": ["boy", "liberty", "vice", "chinatown", "ocho"],
     "planos": ["@LCS_2005:14", "@VCS_2006:12", "@Advance_2004:3", "GTA_15_21", "GTA_15_22"],
     "planos_en": [{"en": "boy", "plano": "@Advance_2004"},
                   {"en": "liberty", "plano": "@LCS_2005"},
                   {"en": "vice", "plano": "IMG_VCS_Portada"},
                   {"en": "chinatown", "plano": "GTA_15_23"},
                   {"en": "ocho", "plano": "@LCS_2005"}]},

    # ---------------------------------------------------------------- ACTO III · LA ERA HD (2008-2013)
    {"id": "p07", "num": 7, "total": T, "titulo": "2008 · GTA IV", "capitulo": "2008 · GTA IV", "overlay": "",
     "anio": 2008, "cartela": {"anio": "2008", "acto": "ACTO III", "titulo": "LA ERA HD"}, "intro_original": "IV_TV_01",
     "texto": ("El veintinueve de abril de 2008 volvemos a Liberty City, pero ya nada se parece a lo de antes. Esto es "
               "otra generación. Niko Bellic, un veterano de guerra de Europa del Este, llega buscando el sueño "
               "americano… y lo que encuentra es otra cosa. GTA IV estrena RAGE, el motor propio de Rockstar, y una "
               "física llamada Euphoria que hace que cada caída y cada atropello sean distintos. Tan difícil era de "
               "meter que los ingenieros de la empresa que la hizo se pasaron meses trabajando dentro del estudio. El "
               "tono también cambia: más serio, más gris, más de película. Costó más de cien millones de dólares, una "
               "barbaridad para la época, y lo recuperó en nada: en su primera semana facturó más de quinientos "
               "millones. Y la crítica se rindió."),
     "rotulos": [{"en": "veintinueve", "texto": "29 ABR 2008"},
                 {"en": "niko", "texto": "NIKO BELLIC"},
                 {"en": "rage", "texto": "MOTOR RAGE"},
                 {"en": "euphoria", "texto": "FÍSICA EUPHORIA"},
                 {"en": "cien", "texto": "+100 MILLONES $|DE PRESUPUESTO"},
                 {"en": "quinientos", "texto": "+500 MILLONES $|EN 1 SEMANA"},
                 {"en": "crítica", "texto": "98|EN METACRITIC"}],
     "nombres": ["liberty", "niko", "rage", "euphoria", "cien", "quinientos", "crítica"],
     "planos": ["@GTA4_2008:34"],
     "planos_en": [{"en": "liberty", "plano": "GTA_15_12"},
                   {"en": "niko", "plano": "@GTA4_2008"},
                   {"en": "caída", "plano": "@GTA4_2008"},
                   {"en": "serio", "plano": "@GTA4_2008"}]},
    {"id": "p08", "num": 8, "total": T, "titulo": "2009 · EPISODIOS DE LIBERTY CITY",
     "capitulo": "2009 · Episodios de Liberty City", "overlay": "", "anio": 2009, "etiqueta_linea": "2009 · EPISODIOS",
     "texto": ("Y Rockstar no se va de Liberty City. En 2009 llegan dos historias más en la misma ciudad: The Lost and "
               "Damned, con una banda de moteros, y The Ballad of Gay Tony, con la vida nocturna de los clubes. Lo "
               "curioso es cómo se cuentan: Niko y los dos protagonistas nuevos se cruzan en los mismos sucesos, cada "
               "uno desde su lado. Tres protagonistas en una misma historia. Apúntate esta idea, porque cuatro años "
               "después Rockstar la lleva mucho más lejos."),
     "rotulos": [{"en": "lost", "texto": "THE LOST AND DAMNED"},
                 {"en": "ballad", "texto": "THE BALLAD|OF GAY TONY"},
                 {"en": "tres", "texto": "3 PROTAGONISTAS|1 HISTORIA"}],
     "nombres": ["lost", "ballad", "tres"],
     "planos": ["@TLAD_2009:12", "@TBOGT_2009:12"],
     "planos_en": [{"en": "lost", "plano": "@TLAD_2009"},
                   {"en": "moteros", "plano": "@TLAD_2009"},
                   {"en": "ballad", "plano": "@TBOGT_2009"},
                   {"en": "nocturna", "plano": "@TBOGT_2009"}]},
    {"id": "p09", "num": 9, "total": T, "titulo": "2013 · GTA V", "capitulo": "2013 · GTA V", "overlay": "",
     "anio": 2013,
     "texto": ("Y ahí está: GTA V. El diecisiete de septiembre de 2013 conocemos a Michael, Franklin y Trevor, tres "
               "protagonistas entre los que cambias cuando quieres, incluso en mitad de un atraco. Volvemos a Los "
               "Santos, que es Los Ángeles, con todo el sur de San Andreas alrededor. Y lo de las ventas ya es de otro "
               "planeta: en tres días pasa de mil millones de dólares. Es el producto de entretenimiento que más rápido "
               "se ha vendido en la historia. No el videojuego: el producto, contando películas y discos. Pero lo más "
               "loco no es cómo empezó, sino cuánto ha durado. Salió en 2013, volvió en 2014 para la nueva generación "
               "de consolas, y otra vez en 2022. Tres generaciones con el mismo juego. Hoy lleva más de doscientos "
               "treinta millones de copias."),
     "rotulos": [{"en": "diecisiete", "texto": "17 SEP 2013"},
                 {"en": "michael", "texto": "MICHAEL · FRANKLIN|TREVOR"},
                 {"en": "ángeles", "texto": "LOS SANTOS|= LOS ÁNGELES"},
                 {"en": "planeta", "texto": "815 MILLONES $|EN 24 HORAS"},
                 {"en": "mil", "texto": "1.000 MILLONES $|EN 3 DÍAS"},
                 {"en": "historia", "texto": "7 RÉCORDS|GUINNESS"},
                 {"en": "2014", "texto": "2013 → 2014|→ 2022"},
                 {"en": "doscientos", "texto": "+230 MILLONES|DE COPIAS"}],
     "nombres": ["michael", "atraco", "ángeles", "planeta", "mil", "2014", "doscientos"],
     "planos": ["@GTA5_2013:36"],
     "planos_en": [{"en": "michael", "plano": "@GTA5_2013"},
                   {"en": "atraco", "plano": "@GTA5_2013"},
                   {"en": "santos", "plano": "@GTA5_2013"}]},
    {"id": "p10", "num": 10, "total": T, "titulo": "2013 · GTA ONLINE", "capitulo": "2013 · GTA Online", "overlay": "",
     "anio": 2013, "etiqueta_linea": "2013 · GTA ONLINE",
     "texto": ("Dos semanas después, el uno de octubre de 2013, se abre GTA Online. Y aquí está la clave de por qué "
               "llevamos tanto esperando a GTA VI. Con atracos, negocios y actualizaciones constantes, GTA Online se "
               "convirtió en un juego que no se acababa nunca. Y la gente siguió jugando, y comprando, GTA V año tras "
               "año. Resultado: trece años sin un GTA principal nuevo. El hueco más largo de toda la saga, con mucha "
               "diferencia."),
     "rotulos": [{"en": "octubre", "texto": "1 OCT 2013|GTA ONLINE"},
                 {"en": "trece", "texto": "13 AÑOS|SIN GTA NUEVO"}],
     "nombres": ["octubre", "atracos", "trece"],
     "planos": ["@GTA_Online:24"],
     "planos_en": [{"en": "online", "plano": "@GTA_Online"},
                   {"en": "atracos", "plano": "@GTA_Online"}]},

    # ---------------------------------------------------------------- ACTO IV · RUMBO A GTA 6 (2022-2026)
    {"id": "p11", "num": 11, "total": T, "titulo": "2023 · EL ANUNCIO", "capitulo": "2022-2023 · GTA VI: el anuncio",
     "overlay": "", "anio": 2023, "etiqueta_linea": "2022-2023 · EL ANUNCIO",
     "cartela": {"anio": "2022", "acto": "ACTO IV", "titulo": "RUMBO A GTA VI"}, "intro_original": "T1_Musica_Petty",
     "texto": ("El cuatro de febrero de 2022, Rockstar confirma que el siguiente GTA está en marcha. Y en diciembre de "
               "2023 llega el primer tráiler. Bueno, llega un día antes de lo previsto: el cuatro de diciembre se filtra "
               "una versión en baja calidad, y Rockstar lo publica esa misma noche. En doce horas suma cuarenta y seis "
               "millones de visitas: récord en YouTube para un vídeo que no es de música. Y en las primeras imágenes, "
               "la ciudad que te pedí que apuntaras al principio. Volvemos a Vice City."),
     "rotulos": [{"en": "febrero", "texto": "4 FEB 2022|CONFIRMADO"},
                 {"en": "tráiler", "texto": "TRÁILER 1|DICIEMBRE 2023"},
                 {"en": "cuarenta", "texto": "46 MILLONES|EN 12 HORAS"},
                 {"en": "volvemos", "texto": "VICE CITY"}],
     "nombres": ["febrero", "tráiler", "cuarenta", "volvemos"],
     "planos": ["T1_Playa_Aerea", "T1_Neones", "T1_Autopista", "T1_Noche_Aerea", "T1_Coches_Noche", "T1_Lancha_Rapida",
                "T1_Camioneta", "@Vice_City:6"],
     "planos_en": [{"en": "febrero", "plano": "Mirada_Azotea"},
                   {"en": "tráiler", "plano": "T1_Playa_Aerea"},
                   {"en": "imágenes", "plano": "T1_Neones"},
                   {"en": "volvemos", "plano": "T1_Letras_Vice"}]},
    {"id": "p12", "num": 12, "total": T, "titulo": "2026 · LA ESPERA", "capitulo": "2025-2026 · GTA VI: la espera",
     "overlay": "", "anio": 2026,
     "texto": ("El tráiler decía 2025. Spoiler: no. En mayo de 2025 se retrasa al veintiséis de mayo de 2026, y el seis "
               "de mayo llega el tráiler 2: cuatrocientos setenta y cinco millones de visitas en veinticuatro horas, "
               "sumando todas las plataformas. En noviembre de 2025, otro retraso: diecinueve de noviembre de 2026. Y "
               "esta vez, todo apunta a que sí. Jason y Lucía, el estado de Leonida… y, otra vez, Vice City."),
     "rotulos": [{"en": "veintiséis", "texto": "RETRASO|→ 26 MAY 2026"},
                 {"en": "cuatrocientos", "texto": "TRÁILER 2|475 MILLONES EN 24 H"},
                 {"en": "diecinueve", "texto": "RETRASO|→ 19 NOV 2026"},
                 {"en": "leonida", "texto": "LEONIDA"}],
     "nombres": ["veintiséis", "cuatrocientos", "diecinueve", "jason", "leonida"],
     "planos": ["T2_Jason_Tejado", "T2_Cayos_Aereo", "Lanz_Balcon", "Lanz_Marina", "T2_Autopista", "T2_Casa_Pilotes",
                "T2_Muelle_Atardecer", "Mirada_Paracaidas", "Mirada_Descapotable_2", "T2_Casa_Aerea",
                "T2_Gimnasio_Playa", "Lanz_Moto_Salto", "@Vice_City:6", "@Jason_Duval:2", "@Leonida_Keys:3"],
     "planos_en": [{"en": "diecinueve", "plano": "VL_Fecha"},
                   {"en": "jason", "plano": "Mirada_Jason_y_Lucia"},
                   {"en": "leonida", "plano": "T2_Cayos_Aereo"},
                   {"en": "vice", "plano": "Lanz_Playa"}]},

    # ---------------------------------------------------------------- CIERRE
    {"id": "cierre", "num": None, "titulo": "", "overlay": "", "capitulo": "De 1997 a 2026", "anio": 2026,
     "texto": ("Y aquí se cierra el círculo. En 1997, Vice City era un plano visto desde el cielo, con coches del tamaño "
               "de una uña. En 2026 es el corazón del juego más esperado del momento, y la gente lo estudia fotograma a "
               "fotograma. Veintinueve años, de unos cochecitos a esto. Ahora te toca a ti: ¿con qué GTA empezaste? "
               "Déjamelo en los comentarios, que tengo curiosidad por ver cuál gana. Si te ha gustado, suscríbete, que "
               "el diecinueve vamos a estar por aquí. Y si te perdiste la historia completa de Vice City, la tienes "
               "aquí mismo. Nos vemos en Leonida."),
     "rotulos": [{"en": "veintinueve", "texto": "1997 → 2026"},
                 {"en": "empezaste", "texto": "¿CON CUÁL|EMPEZASTE?"}],
     "nombres": ["1997", "2026", "empezaste"],
     "planos": ["Mirada_Skyline_Noche", "Lanz_Paseo", "Mirada_Atardecer", "VL_Atardecer_Final", "VL_Lancha_Pareja",
                "VL_Hidroavion", "Mirada_Mar_Atardecer", "Mirada_Skyline_Azotea", "VL_Descap_Cayos",
                "VL_Moto_Agua", "VL_Azotea_1", "VL_Azotea_2", "VL_Interior_1", "@Vice_City:3"],
     "planos_en": [{"en": "1997", "plano": "GTA_15_02"},
                   {"en": "2026", "plano": "Mirada_Vista_Aerea"},
                   {"en": "empezaste", "plano": "Mirada_Terraza"},
                   {"en": "suscríbete", "plano": "Portada_Animada"}]},
]

for _b in BLOQUES:
    _b["voz"] = _voz(_b["texto"])
