"""Guion del vídeo largo «Qué cambió en cada GTA» de «Leónida al Día» (publicación prevista 14-18 nov 2026; GTA VI sale el 19 nov 2026).

Recorre las entregas principales de la saga, de GTA (1997) a GTA V (2013), y después lo que Rockstar ha mostrado
oficialmente de GTA VI. Cambios en mecánicas, cámara, mapa, estructura y tecnología.
Vice City y San Andreas tienen vídeo propio: aquí solo sus cambios de mecánica. GTA V se trata solo en mecánicas
(sin ventas ni récords: eso es del vídeo 9).

Datos y fuentes: video_evolucion\\investigacion.md. Los datos sin fuente abierta no aparecen como hechos.
No importa fuentes_sg. VIDEOS_EXTRA vacío: no hay URLs oficiales de vídeo verificadas en esta sesión.
«canciones» vacío en todos los bloques (no hay canciones en este vídeo).
"""
import re

VIDEOS_EXTRA = {}
RECORTES = {}
MARCO = True

PLANOS_FIJOS = {"IMG_GTA1", "IMG_GTA1_Caja", "N8_Foto_Monitor_CRT", "N8_Captura_RockstarVI"}

# Música por época (hecha con código en el propio montaje: sin pistas con licencia)
MUSICA = {"hook": "synthwave", "p01": "chiptune", "p03": "breakbeat", "p05": "chiptune", "p06": "synthwave",
          "p09": "hiphop", "p12": "synthwave"}

# Línea de tiempo de abajo
LINEA_ANIMADA = True
LINEA = [(1997, "GTA"), (1999, "GTA 2"), (2001, "GTA III"), (2002, "VICE CITY"), (2004, "SAN ANDREAS"),
         (2005, "PSP"), (2008, "GTA IV"), (2009, "EPISODIOS"), (2013, "GTA V"), (2026, "GTA VI")]

# Pronunciación para la voz: cada valor es UNA palabra (nombres ingleses de radios, artistas y títulos)
FONETICA = {
    "III": "3", "IV": "4", "V": "5", "VI": "6", "Liberty": "Líberti", "City": "Siti", "Miami": "Maiámi",
    "Vice": "Vais", "Anywhere": "Énigüer", "Euphoria": "Iufória", "RAGE": "Reich", "Rockstar": "Rókstar",
    "NaturalMotion": "Neturalmóushon", "PlayStation": "Pleisteishon", "Xbox": "Ékboks", "Series": "Síries",
    "Game": "Guéim", "Informer": "Infórmer", "Red": "Red", "Dead": "Ded", "Redemption": "Redempshon",
    "Chiliad": "Chílíad", "Michael": "Máikel", "Franklin": "Fránklin", "Trevor": "Trévor", "Jason": "Yéison",
    "Duval": "Duvál", "Santos": "Sántos", "Leonida": "Leónida", "Leónida": "Leónida", "Lucía": "Lucía",
    "Mirror": "Mírror", "Park": "Park", "Tom": "Tom",
    "Sam": "Sam", "Houser": "Jáuser", "Aaron": "Éron", "Garbut": "Gárbat", "North": "Norz", "Dreamcast": "Drímcast",
    "CJ": "Siyéi", "FIB": "Efe-I-Be", "GameSpot": "Guéimspot", "GPS": "Ge-Pe-Ese", "Netflix": "Nétflix",
    "Caminos": "Caminos", "Liberty": "Líberti", "Stories": "Stóris", "PSP": "Pe-Ese-Pe", "Lost": "Lost",
    "and": "and", "Damned": "Dámd", "Johnny": "Yóni", "Klebitz": "Klébits", "Ballad": "Bálad", "of": "of",
    "Gay": "Guei", "Tony": "Tóni", "Microsoft": "Máicrosoft", "PC": "Pe-Ce", "wifi": "uaifai", "Sony": "Sóni",
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


# Texto de la voz de cada bloque (v2, 13 nov 2026: relleno fuera, datos del revisor y de Game Informer/GameSpot)
T8 = {
    "hook": ("En mil novecientos noventa y siete, GTA se veía desde arriba, como un tablero. Veintinueve años después, "
             "GTA VI sale esta misma semana, y lo que Rockstar ha enseñado se parece a aquel primer juego lo que un "
             "plano de papel a un GPS. Repasamos cada GTA principal y qué cambió en cada salto: la cámara, la ciudad, "
             "la física y los protagonistas. Y al final, lo que no ha cambiado nunca."),
    "p01": ("En mil novecientos noventa y siete, el primer GTA se juega desde arriba y en dos dimensiones. La cámara "
            "mira la ciudad como un plano, sin altura ni perspectiva. El coche es una pieza pequeña que cruza calles "
            "enteras de un vistazo. La mecánica cabe en una línea: robar, huir y que la policía no te alcance. Era como "
            "jugar sobre un callejero. Un callejero con persecuciones. Parece poco, pero ahí está la semilla de todo lo "
            "que vino después: una ciudad abierta que recorres a tu manera, sin un camino marcado."),
    "p02": ("Dos años después llega GTA dos, y la cámara sigue arriba. Lo que cambia son las reglas. La ciudad, "
            "Anywhere City, se reparte entre bandas, y lo nuevo es el respeto. Cada encargo para una banda te gana su "
            "confianza, pero te enemista con sus rivales. Y si entras en un barrio donde te odian, te reciben a tiros. "
            "El mapa ya no solo se recorre: se negocia. La ciudad empieza a recordar lo que has hecho en ella, y la "
            "saga ya no soltará esa idea."),
    "p03": ("En dos mil uno llega el salto grande. Según Game Informer, Sam Houser llevaba tiempo deseando llevar GTA "
            "al 3D completo. Y el proyecto que acabó siendo GTA III ni siquiera nació como un GTA: Aaron Garbut, "
            "director de arte de Rockstar North, cuenta que decidieron reconducirlo a propósito para que lo fuera. "
            "Antes habían probado a alejar la cámara en el motor antiguo, pero no bastaba. Así que lo construyeron "
            "desde cero, con un par de kits de desarrollo de Dreamcast por el camino. El resultado: una Liberty City "
            "grande y variada, que sigue viva mientras haces una misión o lías un caos. Garbut lo resume así: GTA III "
            "marcó la plantilla de cómo hacen juegos. Salió el veintitrés de octubre de dos mil uno, en PlayStation "
            "dos. Y de repente, la ciudad te veía venir."),
    "p04": ("Vice City y San Andreas ya tienen vídeo propio. Aquí, solo qué cambió al mando. Vice City cambia el "
            "decorado, un Miami de neón y playa, pero la fórmula sigue siendo la de GTA III. San Andreas sí toca al "
            "personaje. Según las guías del juego, el músculo, el aguante y la conducción suben con la práctica, y eso "
            "cambia cómo peleas y cómo conduces. CJ pasa de flaco a cachas: hasta en Rockstar se hacen pesas. Además, "
            "la ciudad se reparte en territorios de bandas, y si invades su zona, te declaran la guerra. Tu personaje, "
            "al final, ya no es el mismo que al principio."),
    "lcs": ("Entre medias, GTA se mete en el bolsillo. En octubre de dos mil cinco llega Liberty City Stories a la "
            "PSP de Sony: la Liberty City de GTA III, en una consola portátil y en tres dimensiones. Según GameSpot, "
            "es bastante más pequeño que los de sobremesa, porque la consola no da para más. Pero la idea es la misma: "
            "una ciudad abierta que recorres a tu manera, ahora también en el autobús. Y además trae partidas entre "
            "varias consolas por wifi. Al año siguiente repite la jugada con Vice City Stories. La saga ya no "
            "necesitaba una tele para existir."),
    "episodios": ("Y GTA IV estrena otra forma de crecer: los episodios descargables. El diecisiete de febrero de dos "
                  "mil nueve sale The Lost and Damned, solo en Xbox trescientos sesenta y por descarga. Misma ciudad, "
                  "otra historia y otro protagonista: Johnny Klebitz, de la banda de moteros The Lost. En octubre llega "
                  "The Ballad of Gay Tony. Según la prensa, Microsoft pagó cincuenta millones de dólares por esa "
                  "exclusiva, que fue temporal: en dos mil diez, los dos episodios llegaron en disco a PlayStation tres "
                  "y a PC. Una ciudad, tres protagonistas. ¿Te suena? GTA V hará lo mismo, pero a la vez."),
    "p05": ("En dos mil ocho, GTA IV vuelve a Liberty City, pero cambia lo que hay debajo. Rockstar usa su motor, "
            "RAGE, y le suma una pieza de otra empresa: Euphoria, de NaturalMotion. Fue el primer juego de Rockstar que "
            "la incluyó. La idea es que los movimientos no salgan de animaciones guardadas, sino que se calculen en "
            "tiempo real. Traducido: el cuerpo reacciona a lo que le pasa. Te empujan y tropiezas, y cada caída sale "
            "distinta. En Liberty City, los peatones no se caen igual dos veces. Y tú, de vista, tampoco."),
    "p06": ("GTA IV trae otra novedad que hoy parece de lo más normal: el multijugador dentro del propio juego. Según "
            "GameSpot, se entra sacando el móvil del personaje en mitad de la partida, y en consola caben hasta "
            "dieciséis jugadores en la misma Liberty City. El teléfono, que hasta entonces era casi un adorno, se "
            "convierte en la puerta a otra gente. Liberty City ya no es solo tuya. Cinco años después, esa idea "
            "crecerá tanto que acabará teniendo vida propia."),
    "p07": ("En dos mil trece llega GTA V, con tres protagonistas en lugar de uno. Game Informer los presentó así en "
            "su avance de dos mil doce. Michael es un atracador de bancos retirado que vive a todo lujo gracias a un "
            "trato con el FIB. Franklin es un buscavidas que trabaja para un estafador que vende coches a chavales que "
            "no los pueden pagar. Y Trevor es un antiguo piloto militar que también robaba bancos y ahora malvive en "
            "los márgenes de Los Santos. Tres vidas, una ciudad, y ninguno es precisamente un ejemplo."),
    "p08": ("Y cambiar entre ellos es la gran idea. Fuera de misión puedes pasar de uno a otro cuando quieras, y en "
            "algunas misiones, en mitad del trabajo. La transición no corta en seco: la cámara hace un plano de cine "
            "para que te orientes. Eso abre la puerta a otra novedad: los golpes por fases. Según aquel avance, la "
            "historia incluye varios atracos complejos, con su preparación y el asalto en sí. Primero planificas, luego "
            "entras. Y si toca salir por el aire, Trevor tiene experiencia de vuelo: basta con encontrar un avión."),
    "p09": ("Y el mapa crece. Game Informer, en su avance de dos mil doce, decía que el mundo de Los Santos es más "
            "grande que los de GTA IV, San Andreas y Red Dead Redemption juntos. Hay playas, viñedos, una zona salvaje "
            "alrededor del monte Chiliad y colinas residenciales. Rockstar, según esa misma prensa, rehízo desde cero "
            "el disparo, la conducción y el combate cuerpo a cuerpo, y prometió más vehículos que en cualquier GTA "
            "anterior. Más mapa no significa más misiones. Pero sí más sitios donde perderse."),
    "p10": ("Y llegamos a GTA VI. Esto es lo que Rockstar ha enseñado de forma oficial. Sale el diecinueve de "
            "noviembre de dos mil veintiséis, en PlayStation cinco y Xbox Series, y la precarga digital está abierta "
            "desde el diez. Esta vez son dos protagonistas: Jason Duval y Lucía Caminos. Su web los presenta así: "
            "Jason quiere una vida fácil, pero todo se le complica. Y a Lucía su padre le enseñó a pelear en cuanto "
            "aprendió a andar. La acción transcurre en Vice City, en el estado de Leonida. Rockstar dice poco. Pero lo "
            "dice por escrito."),
    "p11": ("Ahora, lo que no sabemos. Que yo haya encontrado, Rockstar no ha confirmado que vuelva el cambio entre "
            "protagonistas. En agosto estrenó un avance largo que, según la prensa, se emitió primero en Netflix. Y en "
            "él se ve, también según la prensa, combate en tercera persona, conducción y exploración por Vice City. "
            "Game Informer enumera además actividades como pesca, kayak, saltos base, buceo y motos de agua. "
            "Pero un avance no es un manual: lo que se ve en pantalla no tiene por qué ser lo que hace el juego. Con "
            "dos protagonistas, la pregunta es obvia: ¿saltaremos de uno a otro como en GTA V? Lo sabremos el "
            "diecinueve."),
    "p12": ("Tres cosas siguen igual en veintinueve años. La primera, la ciudad como personaje: desde la vista de "
            "arriba hasta Vice City, cada GTA se construye sobre una ciudad inventada que parece de verdad. La segunda, "
            "la sátira: la publicidad, la televisión y la política siempre han sido su blanco favorito. La tercera, la "
            "libertad: el juego te pone reglas, pero el camino lo eliges tú. Cambió la cámara, cambió el motor y cambió "
            "el número de protagonistas. Esas tres cosas, no. Y una cuarta, de regalo: la policía. Desde el primer juego, "
            "en cuanto la lías, alguien con sirena viene a por ti. Lo único que cambia es el tamaño de la persecución. "
            "Esta semana sabremos si GTA VI mantiene las cuatro."),
}


T = 14

BLOQUES = [
    # ---------------------------------------------------------------- HOOK
    {"id": "hook", "num": None, "titulo": "", "overlay": "", "capitulo": "Introducción",
     "texto": T8["hook"],
     "rotulos": [{"t": 0.0, "dur": 2.4, "negro": True, "texto": "1997|→ 2026"},
                 {"en": "veintinueve", "texto": "29 AÑOS"},
                 {"en": "semana", "texto": "19 NOV 2026|SALE GTA VI"}],
     "nombres": ["veintinueve"],
     "canciones": [],
     "planos": ["@GTA1_1997:3", "@GTA2_1999:2", "@GTA3_2001:2", "@GTA4_2008:2", "@GTA5_2013:2", "@GTA6_T1:2"],
     "planos_en": [{"en": "semana", "plano": "Lanz_Playa"},
                   {"en": "veintinueve", "plano": "Mirada_Atardecer"}]},

    # ---------------------------------------------------------------- ACTO I · LA VISTA DE ARRIBA (1997-1999)
    {"id": "p01", "num": 1, "total": T, "titulo": "1997 · GTA", "capitulo": "1997 · GTA", "overlay": "",
     "anio": 1997, "etiqueta_linea": "1997 · GTA",
     "cartela": {"anio": "1997", "acto": "ACTO I", "titulo": "LA VISTA DE ARRIBA"},
     "texto": T8["p01"],
     "rotulos": [{"en": "arriba", "texto": "VISTA CENITAL|1997"},
                 {"en": "dimensiones", "texto": "DOS DIMENSIONES|SIN ALTURA"}],
     "nombres": [],
     "canciones": [],
     "planos": ["IMG_GTA1_Caja", "@GTA1_1997:12", "@GTA1_1997:2"],
     "planos_en": [{"en": "arriba", "plano": "IMG_GTA1"},
                   {"en": "callejero", "plano": "N8_Foto_Monitor_CRT"}]},
    {"id": "p02", "num": 2, "total": T, "titulo": "1999 · GTA 2", "capitulo": "1999 · GTA 2", "overlay": "",
     "anio": 1999,
     "texto": T8["p02"],
     "rotulos": [{"en": "Anywhere", "texto": "GTA 2|ANYWHERE CITY"},
                 {"en": "respeto", "texto": "RESPETO|DE LAS BANDAS"}],
     "nombres": ["Anywhere"],
     "canciones": [],
     "planos": ["@GTA2_1999:13", "@GTA1_1997:6"],
     "planos_en": [{"en": "Anywhere", "plano": "@GTA2_1999"},
                   {"en": "respeto", "plano": "N8_Captura_GTA2_Respeto"}]},

    # ---------------------------------------------------------------- ACTO II · LA CALLE EN 3D (2001-2004)
    {"id": "p03", "num": 3, "total": T, "titulo": "2001 · GTA III", "capitulo": "2001 · GTA III", "overlay": "",
     "anio": 2001, "etiqueta_linea": "2001 · GTA III",
     "cartela": {"anio": "2001", "acto": "ACTO II", "titulo": "LA CALLE EN 3D"},
     "texto": T8["p03"],
     "rotulos": [{"en": "Houser", "texto": "SAM HOUSER|QUERÍA EL 3D COMPLETO"},
                 {"en": "Garbut", "texto": "AARON GARBUT|DIRECTOR DE ARTE, ROCKSTAR NORTH"},
                 {"en": "Dreamcast", "texto": "KITS DE DREAMCAST|SEGÚN GAME INFORMER"},
                 {"en": "Liberty", "texto": "LIBERTY CITY|GRANDE Y VARIADA"},
                 {"en": "PlayStation", "texto": "PLAYSTATION 2|23 OCT 2001"}],
     "nombres": ["Liberty", "Garbut"],
     "canciones": [],
     "planos": ["@GTA3_2001:14", "@GTA3_DE:3"],
     "planos_en": [{"en": "Game", "plano": "N8_Captura_GI_GTA3"},
                   {"en": "Garbut", "plano": "@GTA3_DE"}]},
    {"id": "p04", "num": 4, "total": T, "titulo": "2002-2004 · VICE CITY Y SAN ANDREAS",
     "capitulo": "2002-2004 · Vice City y San Andreas", "overlay": "", "anio": 2004,
     "texto": T8["p04"],
     "rotulos": [{"en": "Vice", "texto": "VICE CITY|MISMA FÓRMULA"},
                 {"en": "músculo", "texto": "SAN ANDREAS|SE ENTRENA"},
                 {"en": "territorios", "texto": "TERRITORIOS|GUERRA DE BANDAS"}],
     "nombres": [],
     "canciones": [],
     "planos": ["@Vice_City_2002:8", "@SA_2004:9"],
     "planos_en": [{"en": "Vice", "plano": "@Vice_City_2002"},
                   {"en": "territorios", "plano": "@SA_2004"}]},

    {"id": "p05", "num": 5, "total": T, "titulo": "2005-2006 · GTA EN EL BOLSILLO", "capitulo": "2005-2006 · En el bolsillo",
     "overlay": "", "anio": 2005, "etiqueta_linea": "2005 · PSP",
     "texto": T8["lcs"],
     "rotulos": [{"en": "Liberty", "texto": "LIBERTY CITY STORIES|PSP · OCT 2005"},
                 {"en": "GameSpot", "texto": "MÁS PEQUEÑO|SEGÚN GAMESPOT"},
                 {"en": "Vice", "texto": "VICE CITY STORIES|2006"}],
     "nombres": ["Liberty"],
     "canciones": [],
     "planos": ["@LCS_2005:8", "@VCS_2006:6"],
     "planos_en": [{"en": "Liberty", "plano": "@LCS_2005"},
                   {"en": "Vice", "plano": "@VCS_2006"}]},

    # ---------------------------------------------------------------- ACTO III · LA FÍSICA Y LOS TRES (2008-2013)
    {"id": "p06", "num": 6, "total": T, "titulo": "2008 · GTA IV", "capitulo": "2008 · GTA IV", "overlay": "",
     "anio": 2008, "etiqueta_linea": "2008 · GTA IV",
     "cartela": {"anio": "2008", "acto": "ACTO III", "titulo": "LA FÍSICA Y LOS TRES"},
     "texto": T8["p05"],
     "rotulos": [{"en": "RAGE", "texto": "MOTOR RAGE|DE ROCKSTAR"},
                 {"en": "Euphoria", "texto": "EUPHORIA|ANIMACIÓN EN TIEMPO REAL"}],
     "nombres": ["Euphoria"],
     "canciones": [],
     "planos": ["@GTA4_2008:10", "IV_PC_1_01", "IV_PC_1_02"],
     "planos_en": [{"en": "RAGE", "plano": "N8_Captura_GTA4_Euphoria"},
                   {"en": "empujan", "plano": "@GTA4_2008"}]},
    {"id": "p07", "num": 7, "total": T, "titulo": "2008 · GTA IV, EL MULTIJUGADOR", "capitulo": "2008 · El multijugador",
     "overlay": "", "anio": 2008,
     "texto": T8["p06"],
     "rotulos": [{"en": "móvil", "texto": "EL MÓVIL|PUERTA AL MULTIJUGADOR"},
                 {"en": "dieciséis", "texto": "HASTA 16 JUGADORES|EN CONSOLA · SEGÚN GAMESPOT"}],
     "nombres": ["dieciséis"],
     "canciones": [],
     "planos": ["@GTA4_2008:12"],
     "planos_en": [{"en": "dieciséis", "plano": "@GTA4_2008"}]},
    {"id": "p08", "num": 8, "total": T, "titulo": "2009 · LOS EPISODIOS", "capitulo": "2009 · Los episodios",
     "overlay": "", "anio": 2009,
     "texto": T8["episodios"],
     "rotulos": [{"en": "Lost", "texto": "THE LOST AND DAMNED|17 FEB 2009 · XBOX 360"},
                 {"en": "Klebitz", "texto": "JOHNNY KLEBITZ|THE LOST"},
                 {"en": "Ballad", "texto": "THE BALLAD OF GAY TONY|29 OCT 2009"},
                 {"en": "cincuenta", "texto": "50 M $|SEGÚN LA PRENSA"}],
     "nombres": ["Lost", "Klebitz", "Ballad"],
     "canciones": [],
     "planos": ["@TLAD_2009:7", "@TBOGT_2009:7"],
     "planos_en": [{"en": "Lost", "plano": "@TLAD_2009"},
                   {"en": "Klebitz", "plano": "@TLAD_2009"},
                   {"en": "Ballad", "plano": "@TBOGT_2009"}]},

    {"id": "p09", "num": 9, "total": T, "titulo": "2013 · GTA V, TRES PROTAGONISTAS", "capitulo": "2013 · GTA V",
     "overlay": "", "anio": 2013, "etiqueta_linea": "2013 · GTA V",
     "texto": T8["p07"],
     "rotulos": [{"en": "tres", "texto": "TRES PROTAGONISTAS|MICHAEL, FRANKLIN Y TREVOR"},
                 {"en": "Michael", "texto": "MICHAEL|ATRACADOR RETIRADO"},
                 {"en": "Franklin", "texto": "FRANKLIN|BUSCAVIDAS"},
                 {"en": "Trevor", "texto": "TREVOR|EXPILOTO MILITAR"}],
     "nombres": ["Michael", "Franklin", "Trevor"],
     "canciones": [],
     "planos": ["@GTA5_2013:10", "@GTA6_Mirada:5"],
     "planos_en": [{"en": "Michael", "plano": "@GTA5_2013"},
                   {"en": "Franklin", "plano": "@GTA5_2013"},
                   {"en": "Trevor", "plano": "@GTA5_2013"}]},
    {"id": "p10", "num": 10, "total": T, "titulo": "2013 · GTA V, EL CAMBIO", "capitulo": "2013 · El cambio",
     "overlay": "", "anio": 2013,
     "texto": T8["p08"],
     "rotulos": [{"en": "cuando", "texto": "CAMBIO DE PROTAGONISTA|FUERA DE MISIÓN"},
                 {"en": "golpes", "texto": "GOLPES POR FASES|PREPARACIÓN Y ASALTO"},
                 {"en": "avión", "texto": "AVIÓN|TREVOR VUELA"}],
     "nombres": [],
     "canciones": [],
     "planos": ["@GTA5_2013:11", "V_Juego_2_01"],
     "planos_en": [{"en": "plano", "plano": "@GTA5_2013"},
                   {"en": "avión", "plano": "V_PS5_01"}]},
    {"id": "p11", "num": 11, "total": T, "titulo": "2013 · GTA V, EL MAPA", "capitulo": "2013 · El mapa",
     "overlay": "", "anio": 2013,
     "texto": T8["p09"],
     "rotulos": [{"en": "Santos", "texto": "LOS SANTOS|MÁS GRANDE"},
                 {"en": "Rockstar", "texto": "ROCKSTAR|REHECHO DESDE CERO"}],
     "nombres": ["Santos"],
     "canciones": [],
     "planos": ["@GTA5_2013:7", "@GTA5_Oficial_810:4", "@GTA_Online:2"],
     "planos_en": [{"en": "Game", "plano": "N8_Captura_GI_GTA5"},
                   {"en": "Santos", "plano": "@GTA5_2013"}]},

    # ---------------------------------------------------------------- ACTO IV · RUMBO A GTA VI (2026)
    {"id": "p12", "num": 12, "total": T, "titulo": "2026 · LO OFICIAL DE GTA VI", "capitulo": "2026 · Lo oficial",
     "overlay": "", "anio": 2026, "etiqueta_linea": "2026 · GTA VI",
     "cartela": {"anio": "2026", "acto": "ACTO IV", "titulo": "RUMBO A GTA VI"},
     "texto": T8["p10"],
     "rotulos": [{"en": "diecinueve", "texto": "19 NOV 2026|RUMBO A GTA VI"},
                 {"en": "Duval", "texto": "JASON DUVAL|PROTAGONISTA"},
                 {"en": "Lucía", "texto": "LUCÍA CAMINOS|PROTAGONISTA"},
                 {"en": "Leonida", "texto": "ESTADO DE LEONIDA|VICE CITY, USA"}],
     "nombres": ["Duval", "Lucía"],
     "canciones": [],
     "planos": ["@GTA6_T1:6", "@GTA6_T2:4", "@GTA6_Mirada:2"],
     "planos_en": [{"en": "diecinueve", "plano": "VL_Fecha"},
                   {"en": "Leonida", "plano": "N8_Captura_RockstarVI"},
                   {"en": "Duval", "plano": "@GTA6_T2"},
                   {"en": "Lucía", "plano": "@GTA6_T2"}]},
    {"id": "p13", "num": 13, "total": T, "titulo": "2026 · LO QUE NO SABEMOS", "capitulo": "2026 · Lo que no sabemos",
     "overlay": "", "anio": 2026,
     "texto": T8["p11"],
     "rotulos": [{"en": "cambio", "texto": "¿VUELVE EL CAMBIO?|NO CONFIRMADO"},
                 {"en": "agosto", "texto": "AVANCE LARGO|27 AGO 2026"},
                 {"en": "tercera", "texto": "TERCERA PERSONA|SEGÚN LA PRENSA"}],
     "nombres": [],
     "canciones": [],
     "planos": ["@GTA6_Mirada:6", "@GTA6_T1:4", "@GTA6_T2:3"],
     "planos_en": [{"en": "cambio", "plano": "@GTA6_Mirada"},
                   {"en": "tercera", "plano": "N8_Captura_Extended_GTA6"}]},

    # ---------------------------------------------------------------- CONSERVADO
    {"id": "p14", "num": 14, "total": T, "titulo": "Lo que se ha conservado", "capitulo": "Lo que se conserva",
     "overlay": "", "anio": 2026,
     "texto": T8["p12"],
     "rotulos": [{"en": "ciudad", "texto": "LA CIUDAD|COMO PERSONAJE"},
                 {"en": "sátira", "texto": "LA SÁTIRA|SIEMPRE"},
                 {"en": "policía", "texto": "Y LA POLICÍA|DESDE 1997"}],
     "nombres": [],
     "canciones": [],
     "planos": ["@Vice_City:5", "@GTA2_1999:3", "@GTA3_2001:3", "@GTA5_2013:3"],
     "planos_en": [{"en": "ciudad", "plano": "@Vice_City"},
                   {"en": "sátira", "plano": "@GTA4_2008"}]},

    # ---------------------------------------------------------------- CIERRE
    {"id": "cierre", "num": None, "titulo": "", "overlay": "", "capitulo": "De 1997 a 2026", "anio": 2026,
     "texto": ("Y te toca a ti. ¿Qué cambio te pareció el más grande: la vista de arriba, el salto al 3D o los "
               "tres protagonistas? Déjamelo en los comentarios, que quiero ver quién gana. Si te ha gustado, suscríbete, "
               "que el diecinueve de noviembre vamos a estar aquí. Nos vemos en Leónida."),
     "rotulos": [{"en": "cambió", "texto": "¿CUÁL TE CAMBIÓ|LA FORMA DE JUGAR?"},
                 {"en": "diecinueve", "texto": "19 NOV 2026"}],
     "nombres": [],
     "canciones": [],
     "planos": ["@Vice_City:4", "Mirada_Skyline_Noche", "Mirada_Playa", "@GTA6_Mirada:2"],
     "planos_en": [{"en": "cambió", "plano": "@GTA6_Mirada"},
                   {"en": "diecinueve", "plano": "Mirada_Coche_Clasico"}]},
]

for _b in BLOQUES:
    _b["voz"] = _voz(_b["texto"])

# ---------------------------------------------------------------- vídeos oficiales de los vídeos 2 a 4
# Los trozos de las tablas salen de esos vídeos: se toman sus direcciones, recortes de marca de agua y planos fijos.
import guion_jl as _jl  # noqa: E402
import guion_sg as _sg  # noqa: E402
import guion_vc as _vc  # noqa: E402

VIDEOS_EXTRA = dict(globals().get("VIDEOS_EXTRA", {}))
RECORTES = dict(globals().get("RECORTES", {}))
for _m in (_vc, _sg, _jl):
    for _k, _v in getattr(_m, "VIDEOS_EXTRA", {}).items():
        VIDEOS_EXTRA.setdefault(_k, _v)
    for _k, _v in getattr(_m, "RECORTES", {}).items():
        RECORTES.setdefault(_k, _v)
PLANOS_FIJOS = set(globals().get("PLANOS_FIJOS", ())) | set(_vc.PLANOS_FIJOS) | set(_sg.PLANOS_FIJOS) | set(_jl.PLANOS_FIJOS)
MARCO = True
