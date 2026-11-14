"""Guion del vídeo largo «Todas las polémicas de GTA, de 1997 a GTA VI» (Leónida al Día).

Mismo formato que guion_sg.py (se elige con GUION=guion_pol). Datos comprobados el 11 nov 2026: ver investigacion.md
(cada dato con su URL). Solo entra en el texto hablado lo confirmado; lo no confirmado queda en investigacion.md.
No importa fuentes_sg. VIDEOS_EXTRA vacío: no hay URLs oficiales verificadas todavía (ver edicion.md).
Los planos NUEVO_ se describen en edicion.md.
"""
import re

VIDEOS_EXTRA = {}  # sin URLs oficiales verificadas

RECORTES = {}
MARCO = False

PLANOS_FIJOS = {"GTA_15_01", "GTA_15_02", "GTA_15_03", "IMG_GTA1", "IMG_GTA1_Caja", "IMG_RaceNChase", "IMG_VC_Portada",
                "VCA_Logo", "Mirada_Logo", "VL_Fecha", "Portada_Animada",
                "NUEVO_Recorte_Prensa_1997", "NUEVO_Captura_ESRB_AO", "NUEVO_Captura_Clasificacion_AU",
                "NUEVO_Mazo_Juez", "NUEVO_Tribunal_Florida", "NUEVO_Tribunal_NY", "NUEVO_Bully_Portada", "NUEVO_Bully_Captura",
                "NUEVO_Titular_Prensa_2013", "NUEVO_Pantalla_Texto_Hack",
                "NUEVO_Estanteria_Tienda", "NUEVO_Captura_Peticion", "NUEVO_Captura_Steam_Resenas",
                "NUEVO_Captura_Entrevista", "NUEVO_Captura_Disculpa_Rockstar"}

# Música por acto: cambia con cada cartela
# 14 nov: estas voces se hicieron con gemini-3.8-flash-tts (suena distinto); se rehacen con flash-lite
VOZ_REHACER = ["p06", "p07", "p08", "p09", "p10", "p11", "p12", "p16", "cierre"]
MUSICA = {"hook": "synthwave", "p01": "chiptune", "p02": "breakbeat", "p04": "hiphop", "p08": "synthwave",
          "p13": "breakbeat"}

# Línea de tiempo de abajo
LINEA_ANIMADA = True
LINEA = [(1997, "GTA"), (2001, "GTA III"), (2002, "VICE CITY"), (2004, "SAN ANDREAS"), (2006, "BULLY"),
         (2008, "GTA IV"), (2013, "GTA V"), (2026, "GTA VI")]

# Pronunciación para la voz (misma cantidad de palabras que el texto)
FONETICA = {
    "III": "3", "IV": "4", "V": "5", "VI": "6", "Liberty": "Líberti", "City": "Siti", "Vice": "Vais",
    "Claude": "Clod", "Hot": "Jot", "Coffee": "Cófi", "Walmart": "Uolmart", "Best": "Best", "Buy": "Bai",
    "Target": "Tárguet", "Take-Two": "Teik-Tu", "Rockstar": "Rókstar", "Jack": "Yak", "Thompson": "Tompson",
    "Alabama": "Alabama", "Bullworth": "Bulluorz", "Bully": "Búli", "Lohan": "Lóan", "Lindsay": "Línsei",
    "Jonas": "Yónas", "Lacey": "Léisi", "Clifford": "Clífford", "Jones": "Yóuns", "Dailly": "Déilí",
    "Lords": "Lóds", "Lores": "Lóres", "Houser": "Jáuser", "Freedom": "Fríidom", "Vaz": "Vas",
    "Lapsus": "Láptsus", "Haitian": "Jeíshan", "haitiana": "jaitiana", "haitianos": "jaitianos",
    "FTC": "efe-te-ce", "ESRB": "e-ese-erre-be", "AO": "a-o", "Miami": "Maiami",
    "Tony": "Toni", "Nueva": "Nueva", "Estados": "Estados",
    "Scholarship": "Escólarship", "Edition": "Edíshon",
    "Kmart": "Kmárt", "Collective": "Colectiv", "Shout": "Shaut", "OpenIV": "Opénaivi", "Steam": "Stim",
    "Shark": "Shárk", "Sarwar": "Sarwár", "The": "De", "Trilogy": "Trílogi", "Definitive": "Definitiv",
    "IWGB": "i-uve-doble-ge-be", "Discord": "Díscord", "Glasgow": "Glásgou",
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


T = 17

BLOQUES = [
    # ---------------------------------------------------------------- GANCHO
    {"id": "hook", "num": None, "titulo": "", "overlay": "", "capitulo": "Introducción",
     # 14 nov (revisión aprobada): gancho con el juez de Miami que revisó Bully antes de dejar que se vendiera
     "texto": ("En octubre de 2006, un juez de Miami pasó unas dos horas viendo cómo se jugaba a Bully para decidir si "
               "se podía vender. Y no es lo más raro de esta historia. En casi treinta años, GTA ha tenido un publicista "
               "de escándalos, un minijuego escondido que costó millones, demandas, retiradas de tiendas y hasta despidos "
               "a un año del estreno de GTA VI. Hoy las repasamos todas, en orden y con las fuentes delante. Y al final "
               "te pregunto cuál fue la más grave."),
     "rotulos": [{"en": "juez", "texto": "MIAMI · 2006|UN JUEZ REVISA BULLY"},
                 {"en": "publicista", "texto": "PUBLICISTA|DE ESCÁNDALOS"},
                 {"en": "despidos", "texto": "2025|DESPIDOS EN ROCKSTAR"}],
     "nombres": ["juez", "publicista", "despidos"],
     "planos": ["@GTA3_2001:2", "GTA_15_01", "Mirada_Logo", "@GTA5_2013:2", "Lanz_Playa", "T1_Noche_Aerea"],
     "planos_en": [{"en": "publicista", "plano": "IMG_GTA1"}]},  # 14 nov: planos por rehacer (paso de imagen)

    # ---------------------------------------------------------------- ACTO I · EL PUBLICISTA (1997)
    {"id": "p01", "num": 1, "total": T, "titulo": "1997 · LA CAMPAÑA DE GTA 1",
     "capitulo": "1997 · La campaña de GTA 1", "overlay": "", "anio": 1997,
     "cartela": {"anio": "1997", "acto": "ACTO I", "titulo": "EL PUBLICISTA"}, "intro_original": "G1_Demo1_01",
     "texto": ("Empecemos en 1997. GTA nace como un juego raro, visto desde arriba. Y la polémica llega con ayuda. "
               "La distribuidora BMG contrató a Max Clifford, un "
               "publicista británico famoso por campañas construidas sobre escándalos. Los creadores, David Jones y Mike "
               "Dailly, han reconocido que su trabajo fue clave para que el juego tuviera tanta atención. En mayo, antes "
               "de que saliera, un lord preguntó en la Cámara de los Lores qué pensaba hacer el Gobierno con el juego. Y la "
               "prensa británica se lanzó. Y no todo fue publicidad: en 1998, Brasil prohibió GTA 1, y su Ministerio de Justicia ordenó retirar las copias de PC. "
               "Un patrón que se repetirá durante casi treinta años."),
     "rotulos": [{"en": "clifford", "texto": "MAX CLIFFORD|PUBLICISTA"},
                 {"en": "lores", "texto": "CÁMARA DE LOS LORES|MAYO 1997"},  # Hansard, HL Deb 20 May 1997 c258
                 {"en": "creadores", "texto": "DAVID JONES|MIKE DAILLY"},
                 {"en": "brasil", "texto": "BRASIL · 1998|PROHIBIDO GTA 1"}],
     # 14 nov: quitado «medio millón de copias en Navidad» (una sola fuente, sin confirmar)
     "nombres": ["clifford", "lores", "creadores", "brasil"],
     "planos": ["@GTA1_1997:6", "IMG_GTA1_Caja", "IMG_RaceNChase", "GTA_15_03", "NUEVO_Recorte_Prensa_1997", "@GTA1_1997:2"],
     "planos_en": [{"en": "clifford", "plano": "NUEVO_Recorte_Prensa_1997"},
                   {"en": "lores", "plano": "@GTA1_1997"},
                   {"en": "creadores", "plano": "@GTA1_1997"},
                   {"en": "brasil", "plano": "@GTA1_1997"}]},

    # ---------------------------------------------------------------- ACTO II · EL SALTO AL 3D (2001-2002)
    {"id": "p02", "num": 2, "total": T, "titulo": "2001 · GTA III Y EL 11-S", "capitulo": "2001 · GTA III y el 11-S",
     "overlay": "", "anio": 2001, "cartela": {"anio": "2001", "acto": "ACTO II", "titulo": "EL SALTO AL 3D"},
     "intro_original": "G3_DE_01",
     "texto": ("Llega 2001 y la saga da el salto al 3D: por primera vez, en GTA III, bajas a la calle. Pero el 11 de "
               "septiembre cambia los planes. "
               "Rockstar retrasa el juego unas semanas, y el equipo lo revisa a toda prisa. Los coches de policía, azules "
               "con franjas blancas, se parecían demasiado a los de Nueva York: pasan a blanco y negro. Se quita una "
               "misión que hablaba de terroristas. Un avión cambia su ruta para no pasar cerca de los rascacielos. Y sale "
               "a finales de octubre, sin aquella misión."),
     # 14 nov: según Dan Houser en MCV, «un par de semanas»; la portada no aparece en la fuente, se quita
     # 14 nov: las fuentes dudan entre el 22 y el 23 de octubre de 2001: «a finales de octubre»
     "rotulos": [{"en": "septiembre", "texto": "11-S|RETRASO DE SEMANAS"},
                 {"en": "policía", "texto": "COCHES DE POLICÍA|BLANCO Y NEGRO"},
                 {"en": "terroristas", "texto": "MISIÓN|QUITADA"},
                 {"en": "finales", "texto": "OCTUBRE 2001|SALE EN EE. UU."}],
     "nombres": ["septiembre", "policía", "terroristas", "finales"],
     "planos": ["@GTA3_2001:6", "@GTA3_DE:3", "GTA_15_11", "GTA_15_12", "GTA_15_13", "GTA_15_14"],
     "planos_en": [{"en": "calle", "plano": "@GTA3_2001"},
                   {"en": "policía", "plano": "@GTA3_2001"},
                   {"en": "finales", "plano": "GTA_15_14"}]},
    {"id": "p03", "num": 3, "total": T, "titulo": "2002 · VICE CITY Y LA DEMANDA",
     "capitulo": "2002 · Vice City y la demanda", "overlay": "", "anio": 2002,
     # 14 nov: corregido el orden de la demanda (Game Developer, 2 y 28 ene 2004; Take-Two, 10 dic 2003)
     "texto": ("En 2002 llega Vice City, y con ella una polémica distinta. En diciembre de 2003, grupos de la comunidad "
               "haitiana de Florida demandan a Rockstar y a Take-Two por una frase contra los haitianos que aparecía en el "
               "juego. Sostenían que juegos como este hacían que los niños se acostumbraran a la violencia contra policías "
               "y civiles. La demanda empieza en un tribunal estatal de Florida. Rockstar la lleva a uno federal, y en "
               "enero los demandantes la retiran para volver al estatal. Mientras tanto, Take-Two acepta quitar esa frase "
               "de las copias nuevas del juego."),
     "rotulos": [{"en": "vice", "texto": "VICE CITY|= MIAMI"},
                 {"en": "haitiana", "texto": "COMUNIDAD HAITIANA|FLORIDA · DIC 2003"},
                 {"en": "federal", "texto": "ESTATAL → FEDERAL|→ ESTATAL"}],
     "nombres": ["vice", "haitiana", "federal"],
     "planos": ["@Vice_City_2002:8", "@VC_DE:3", "IMG_VC_Portada", "GTA_15_16", "GTA_15_17", "NUEVO_Tribunal_Florida"],
     "planos_en": [{"en": "vice", "plano": "@Vice_City_2002"},
                   {"en": "haitiana", "plano": "@Vice_City_2002"},
                   {"en": "federal", "plano": "NUEVO_Tribunal_Florida"}]},

    # ---------------------------------------------------------------- ACTO III · LOS TRIBUNALES (2005-2008)
    {"id": "p04", "num": 4, "total": T, "titulo": "2005 · HOT COFFEE Y LA AO", "capitulo": "2005 · Hot Coffee",
     "overlay": "", "anio": 2005, "cartela": {"anio": "2005", "acto": "ACTO III", "titulo": "LOS TRIBUNALES"},
     "final_revisado": True,  # 13 nov: Whisper corta en «Y todo acaban»; oído entero: «Y todo acaba en un acuerdo.»
     "texto": ("2005. San Andreas está en todas las tiendas. Y un aficionado descubre algo escondido en el código: un "
               "minijuego de contenido sexual, Hot Coffee. Estaba en el disco, pero bloqueado; un mod, una modificación de "
               "terceros, lo desbloquea. El veinte de julio, la ESRB, el organismo que pone las clasificaciones en Estados "
               "Unidos, retira la M de mayores de diecisiete y pone AO, solo para adultos. Walmart, Best Buy y Target lo "
               "retiran de sus tiendas. Take-Two calcula que la historia le cuesta veinticuatro millones y medio de dólares "
               "en devoluciones. Rockstar saca una versión sin la escena. Y la FTC, la agencia federal de consumo, acusa a la "
               "empresa de no avisar del contenido. Y todo acaba en un acuerdo."),
     "rotulos": [{"en": "hot", "texto": "HOT COFFEE|MINIJUEGO OCULTO"},
                 {"en": "veinte", "texto": "20 JUL 2005|M → AO"},
                 {"en": "walmart", "texto": "WALMART · BEST BUY|TARGET"},
                 {"en": "veinticuatro", "texto": "24,5 M$|EN DEVOLUCIONES"},
                 {"en": "federal", "texto": "FTC|ACUERDO"}],
     "nombres": ["hot", "veinte", "walmart", "veinticuatro", "federal"],
     "planos": ["@SA_2004:10", "@SA_DE:3", "NUEVO_Captura_ESRB_AO", "GTA_15_25", "GTA_15_26"],
     "planos_en": [{"en": "hot", "plano": "NUEVO_Captura_ESRB_AO"},
                   {"en": "tiendas", "plano": "@SA_2004"},
                   {"en": "federal", "plano": "GTA_15_26"}]},
    {"id": "p05", "num": 5, "total": T, "titulo": "2005 · AUSTRALIA Y LA CLASIFICACIÓN",
     "capitulo": "2005 · Australia", "overlay": "", "anio": 2005,
     "final_revisado": True,  # 12 nov: Whisper escribe «18» por «dieciocho»; el final está entero
     "texto": ("Y no fue solo Estados Unidos. En Australia, San Andreas tenía una clasificación de MA quince desde "
               "octubre de 2004. Tras Hot Coffee, el organismo australiano revocó esa clasificación, y el juego no se pudo "
               "vender hasta quitar el contenido. Pero el problema de fondo era otro: Australia no tenía una categoría para "
               "adultos en videojuegos. Hasta enero de 2013 no existió. Así que los juegos más fuertes, sencillamente, no "
               "podían venderse legalmente allí. Y en julio de ese mismo año, GTA V recibió por fin una clasificación para "
               "mayores de dieciocho."),
     "rotulos": [{"en": "australia", "texto": "AUSTRALIA|MA15+ · 2004"},
                 {"en": "revocó", "texto": "CLASIFICACIÓN|REVOCADA"},
                 {"en": "adultos", "texto": "SIN CATEGORÍA|PARA ADULTOS"},
                 {"en": "julio", "texto": "GTA V|MAYORES DE 18 · 2013"}],
     "nombres": ["australia", "revocó", "adultos", "julio"],
     "planos": ["@SA_2004:4", "NUEVO_Captura_Clasificacion_AU", "GTA_15_21", "GTA_15_22", "@SA_2004:3"],
     "planos_en": [{"en": "australia", "plano": "NUEVO_Captura_Clasificacion_AU"},
                   {"en": "adultos", "plano": "GTA_15_21"},
                   {"en": "julio", "plano": "@GTA5_2013"}]},
    {"id": "p06", "num": 6, "total": T, "titulo": "2006 · BULLY Y LAS QUEJAS", "capitulo": "2006 · Bully",
     "overlay": "", "anio": 2006, "etiqueta_linea": "2006 · BULLY",
     # 14 nov: el juez de Miami (The Register, 13 oct 2006; bit-tech, 16 oct 2006) y la coalición de profesores
     # (The Escapist, 4 mar 2008: piden a las tiendas que no vendan la Scholarship Edition; no es una prohibición legal)
     "texto": ("En 2006 llega Bully, un juego ambientado en un internado llamado Bullworth, donde el protagonista se mueve "
               "entre pandillas y profesores. Antes de que saliera, Jack Thompson pidió en Miami que se declarara una "
               "molestia pública. Y el juez hizo algo insólito: pasó unas dos horas viendo cómo un representante de la "
               "compañía lo jugaba. Su conclusión: no había nada que un niño no pudiera ver en la televisión en horario de "
               "máxima audiencia. En 2008, con la Scholarship Edition, una coalición de sindicatos de profesores, encabezada "
               "por la federación canadiense, pidió a las tiendas que no lo vendieran. Decían que glorificaba el acoso escolar."),
     "rotulos": [{"en": "bullworth", "texto": "BULLWORTH|INTERNADO FICTICIO"},
                 {"en": "molestia", "texto": "MIAMI · OCT 2006|¿MOLESTIA PÚBLICA?"},
                 {"en": "juez", "texto": "EL JUEZ LO REVISA|UNAS DOS HORAS"},
                 {"en": "coalición", "texto": "PROFESORES · 2008|PIDEN NO VENDERLO"}],
     "nombres": ["bullworth", "molestia", "juez", "coalición"],
     "planos": ["NUEVO_Bully_Portada", "NUEVO_Bully_Captura", "@Historia_GTA:5"],
     "planos_en": [{"en": "bullworth", "plano": "NUEVO_Bully_Captura"},
                   {"en": "federación", "plano": "NUEVO_Bully_Portada"},
                   {"en": "juez", "plano": "@Historia_GTA"}]},
    {"id": "p07", "num": 7, "total": T, "titulo": "2008 · JACK THOMPSON", "capitulo": "2008 · Jack Thompson",
     "overlay": "", "anio": 2008, "cta": True,
     "texto": ("Y Thompson no era nuevo en esto. Jack Thompson, abogado de Florida, era uno de los críticos más activos "
               "de los videojuegos violentos. En 2003, un joven aficionado a GTA mató a dos policías y a una operadora de "
               "emergencias en Alabama. En 2005, Thompson demandó a Rockstar en nombre de las familias de las víctimas, "
               "alegando que el juego había influido en el crimen. Pero su propia carrera acabó en los tribunales. El "
               "colegio de abogados investigó su conducta, y la jueza que llevó el caso recomendó declararle culpable en "
               "veintisiete de los treinta y un cargos. El veinticinco de septiembre de 2008, el Tribunal Supremo de Florida lo inhabilitó de "
               "forma permanente para ejercer la abogacía."),
     "rotulos": [{"en": "thompson", "texto": "JACK THOMPSON|ABOGADO DE FLORIDA"},
                 {"en": "alabama", "texto": "ALABAMA · 2003|2 POLICÍAS + 1"},
                 {"en": "veintisiete", "texto": "27 DE 31 CARGOS"},
                 {"en": "inhabilitó", "texto": "25 SEP 2008|INHABILITADO"}],
     "nombres": ["thompson", "alabama", "veintisiete", "inhabilitó"],
     "planos": ["NUEVO_Mazo_Juez", "@SA_2004:3", "@LCS_2005:3", "@LCS_2005:6"],
     "planos_en": [{"en": "thompson", "plano": "@LCS_2005"},
                   {"en": "alabama", "plano": "@SA_2004"},
                   {"en": "veintisiete", "plano": "NUEVO_Mazo_Juez"},
                   {"en": "inhabilitó", "plano": "@LCS_2005"}]},

    # ---------------------------------------------------------------- ACTO IV · LA ERA HD (2013-2018)
    {"id": "p08", "num": 8, "total": T, "titulo": "2013 · GTA V Y LA TORTURA", "capitulo": "2013 · GTA V y la escena de tortura",
     "overlay": "", "anio": 2013, "cartela": {"anio": "2013", "acto": "ACTO IV", "titulo": "LA ERA HD"},
     "texto": ("2013. GTA V sale el diecisiete de septiembre, con tres protagonistas. Y una misión provoca una avalancha "
               "de críticas: una escena de tortura en la que el jugador participa. El diputado británico Keith Vaz dice que "
               "se quedó asombrado por la violencia. Freedom from Torture, una ONG que atiende a víctimas de tortura, asegura "
               "que el estudio cruzó una línea. Los defensores responden que la escena muestra la crueldad de la tortura, y "
               "que es sátira. Unos la ven como una denuncia. Otros, como una línea roja. Tú decides."),
     "rotulos": [{"en": "diecisiete", "texto": "17 SEP 2013|GTA V"},
                 {"en": "tortura", "texto": "ESCENA DE TORTURA|EN LA MISIÓN"},
                 {"en": "vaz", "texto": "KEITH VAZ|DIPUTADO BRITÁNICO"},
                 {"en": "freedom", "texto": "FREEDOM FROM TORTURE|ONG"}],
     "nombres": ["diecisiete", "tortura", "vaz", "freedom"],
     "planos": ["@GTA5_2013:8", "NUEVO_Titular_Prensa_2013"],
     "planos_en": [{"en": "diecisiete", "plano": "@GTA5_2013"},
                   {"en": "tortura", "plano": "NUEVO_Titular_Prensa_2013"},
                   {"en": "freedom", "plano": "@GTA5_2013"},
                   {"en": "sátira", "plano": "@GTA5_2013"}]},
    {"id": "p09", "num": 9, "total": T, "titulo": "2014 · LINDSAY LOHAN CONTRA ROCKSTAR",
     "capitulo": "2014 · Lindsay Lohan", "overlay": "", "anio": 2014,
     "texto": ("En 2014, la polémica llega a una actriz famosa. Lindsay Lohan demanda a Rockstar porque, según su equipo, un "
               "personaje de GTA V, Lacey Jonas, era una referencia clara a ella. Rockstar defendió que el juego es ficción y "
               "sátira. En 2016 un tribunal de Nueva York desestimó la demanda: no se usaba su nombre ni su imagen. En 2018 el "
               "tribunal más alto del estado rechazó el último recurso. Así que la sátira ganó este pulso."),
     "rotulos": [{"en": "lindsay", "texto": "LINDSAY LOHAN|DEMANDA A ROCKSTAR"},
                 {"en": "jonas", "texto": "LACEY JONAS|PERSONAJE DE GTA V"},
                 {"en": "2016", "texto": "2016|DESESTIMADA"},
                 {"en": "2018", "texto": "2018|RECURSO RECHAZADO"}],
     "nombres": ["lindsay", "jonas", "2016", "2018"],
     "planos": ["NUEVO_Tribunal_NY", "@GTA5_2013:4", "@GTA5_2013:2"],
     "planos_en": [{"en": "lindsay", "plano": "NUEVO_Tribunal_NY"},
                   {"en": "jonas", "plano": "@GTA5_2013"},
                   {"en": "2016", "plano": "@GTA5_2013"},
                   {"en": "2018", "plano": "@GTA5_2013"}]},
    {"id": "p10", "num": 10, "total": T, "titulo": "2014 · GTA V FUERA DE LAS TIENDAS",
     "capitulo": "2014 · Target y Kmart en Australia", "overlay": "", "anio": 2014, "etiqueta_linea": "2014 · AUSTRALIA",
     "texto": ("Y en diciembre de 2014 llega una polémica sin tribunales. En Australia, las cadenas Target y Kmart retiran "
               "GTA V de sus tiendas. El motivo: una petición que pedía retirarlo por la violencia contra las mujeres que "
               "muestra. Más de cuarenta mil personas firmaron la campaña, impulsada por Collective Shout. La petición nombraba a Target, y Kmart lo siguió aunque no estaba en ella. "
               "El consejero delegado de Take-Two se mostró decepcionado: era un juego aclamado, que habían disfrutado "
               "decenas de millones de personas. Target de Estados Unidos aseguró que en Norteamérica seguiría vendiéndolo."),
     "rotulos": [{"en": "australia", "texto": "AUSTRALIA · 2014|TARGET Y KMART"},
                 {"en": "cuarenta", "texto": "+40.000 FIRMAS|COLLECTIVE SHOUT"},
                 {"en": "consejero", "texto": "TAKE-TWO|«DECEPCIONADOS»"}],  # Fox Business, 3 dic 2014
     "nombres": ["australia", "cuarenta", "consejero"],
     "planos": ["@GTA5_2013:4", "NUEVO_Estanteria_Tienda", "@GTA_Online:2", "@GTA5_2013:5"],
     "planos_en": [{"en": "australia", "plano": "NUEVO_Estanteria_Tienda"},
                   {"en": "cuarenta", "plano": "NUEVO_Captura_Peticion"},
                   {"en": "consejero", "plano": "@GTA5_2013"}]},
    {"id": "p11", "num": 11, "total": T, "titulo": "2017 · OPENIV Y LOS MODS", "capitulo": "2017 · OpenIV",
     "overlay": "", "anio": 2017, "etiqueta_linea": "2017 · OPENIV",
     "texto": ("Y en 2017, la polémica llega al PC. OpenIV es una herramienta gratuita con la que la comunidad crea mods para "
               "GTA V. En junio, los abogados de Take-Two envían una carta de cese y desista a sus creadores, y la herramienta "
               "deja de distribuirse. La reacción fue inmediata: una avalancha de reseñas negativas en la página del juego en "
               "Steam, y peticiones en internet. Dos semanas después, Take-Two da marcha atrás. La herramienta vuelve a estar "
               "disponible, y los mods para un jugador vuelven a estar permitidos."),
     "rotulos": [{"en": "openiv", "texto": "OPENIV|HERRAMIENTA DE MODS"},
                 {"en": "junio", "texto": "JUN 2017|CESE Y DESISTA"},
                 {"en": "reseñas", "texto": "RESEÑAS NEGATIVAS|EN STEAM"},
                 {"en": "marcha", "texto": "TAKE-TWO|DA MARCHA ATRÁS"}],
     "nombres": ["openiv", "junio", "reseñas", "marcha"],
     "planos": ["NUEVO_Captura_Steam_Resenas", "@GTA5_2013:4", "@GTA_Online:2", "@GTA5_2013:3"],
     "planos_en": [{"en": "openiv", "plano": "@GTA5_2013"},
                   {"en": "junio", "plano": "NUEVO_Captura_Steam_Resenas"},
                   {"en": "reseñas", "plano": "@GTA5_2013"},
                   {"en": "marcha", "plano": "@GTA5_2013"}]},
    {"id": "p12", "num": 12, "total": T, "titulo": "2017 · SHARK CARDS", "capitulo": "2017 · Shark Cards",
     "overlay": "", "anio": 2017, "etiqueta_linea": "2017 · SHARK CARDS",
     "texto": ("En octubre de 2017, otra discusión: el dinero. GTA Online vende las Shark Cards, paquetes de dinero del "
               "juego que se compran con dinero real. Rockstar lo defiende. Su director de diseño, Imran Sarwar, dijo en Game "
               "Informer que la gente puede jugar sin gastarse un dólar, aparte de comprar el juego, porque todas las "
               "actualizaciones son gratis. Los críticos responden que la economía del juego está pensada para empujar a "
               "comprar. Esa discusión sigue abierta."),
     "rotulos": [{"en": "shark", "texto": "SHARK CARDS|DINERO REAL"},
                 {"en": "sarwar", "texto": "IMRAN SARWAR|DIRECTOR DE DISEÑO"},
                 {"en": "gratis", "texto": "ACTUALIZACIONES|GRATIS"}],
     "nombres": ["shark", "sarwar", "gratis"],
     "planos": ["@GTA_Online:4", "NUEVO_Captura_Entrevista", "@GTA_Online:4"],
     "planos_en": [{"en": "shark", "plano": "@GTA_Online"},
                   {"en": "sarwar", "plano": "NUEVO_Captura_Entrevista"},
                   {"en": "gratis", "plano": "@GTA_Online"}]},

    # ---------------------------------------------------------------- ACTO V · RUMBO A GTA VI (2021-2026)
    {"id": "p13", "num": 13, "total": T, "titulo": "2021 · THE TRILOGY", "capitulo": "2021 · The Trilogy",
     "overlay": "", "anio": 2021, "etiqueta_linea": "2021 · TRILOGÍA",
     "cartela": {"anio": "2021", "acto": "ACTO V", "titulo": "RUMBO A GTA VI"},
     "texto": ("En noviembre de 2021, Rockstar lanza The Trilogy: Definitive Edition. Son GTA III, Vice City y San Andreas, "
               "remasterizados, con gráficos nuevos y en un solo paquete. Pero llega con problemas técnicos. Y Rockstar retira del mercado las "
               "versiones clásicas de PC de los tres juegos. Una semana después de su lanzamiento, la empresa pide disculpas "
               "y promete arreglos. Y vuelve a poner las versiones antiguas a la venta, en su propia tienda para PC. Quien comprara la trilogía antes del 30 de junio de 2022 recibiría los clásicos para PC gratis. Una "
               "remasterización también puede ser una polémica."),
     "rotulos": [{"en": "noviembre", "texto": "11 NOV 2021|THE TRILOGY"},
                 {"en": "problemas", "texto": "PROBLEMAS TÉCNICOS|AL SALIR"},
                 {"en": "disculpas", "texto": "ROCKSTAR|PIDE DISCULPAS"},
                 {"en": "tienda", "texto": "VERSIONES CLÁSICAS|DE NUEVO A LA VENTA"}],
     "nombres": ["noviembre", "disculpas", "tienda"],
     "planos": ["@GTA3_DE:1", "@VC_DE:3", "NUEVO_Captura_Disculpa_Rockstar", "@Vice_City_2002:4"],
     "planos_en": [{"en": "noviembre", "plano": "@GTA6_Mirada"},
                   {"en": "disculpas", "plano": "NUEVO_Captura_Disculpa_Rockstar"},
                   {"en": "tienda", "plano": "@GTA6_Mirada"}]},
    {"id": "p14", "num": 14, "total": T, "titulo": "2022 · EL HACKEO DE ROCKSTAR", "capitulo": "2022 · El hackeo",
     "overlay": "", "anio": 2022,
     # 14 nov: corto; la filtración y el juicio ya los cuenta el vídeo 5 (tarjeta de YouTube a ese vídeo en este bloque)
     "texto": ("Septiembre de 2022. Un hackeo saca a internet unos noventa vídeos de GTA VI en pleno desarrollo. Rockstar "
               "lo confirma al día siguiente y dice que el trabajo sigue. Esa historia, con el juicio incluido, la "
               "contamos en el vídeo de por qué GTA VI ha tardado trece años. Te lo dejo aquí arriba."),
     "tarjeta_youtube": "https://youtu.be/0wN5lX7CVvc",
     "rotulos": [{"en": "septiembre", "texto": "SEPT 2022|HACKEO A ROCKSTAR"},
                 {"en": "noventa", "texto": "~90 VÍDEOS|DE GTA VI"}],
     "nombres": ["septiembre", "noventa"],
     "planos": ["NUEVO_Pantalla_Texto_Hack", "@GTA_Online:3", "@GTA_Online:4"],
     "planos_en": [{"en": "septiembre", "plano": "NUEVO_Pantalla_Texto_Hack"}]},
    # 14 nov (revisión aprobada): bloque nuevo. Fuentes: The Register (6 nov 2025), Aftermath (10 sep 2026), TechRadar
    # (ene 2026, sin sueldo provisional). Sin nombres de trabajadores. Antes de publicar, mirar si ya hay sentencia.
    {"id": "p14b", "num": 15, "total": T, "titulo": "2025 · LOS DESPIDOS EN ROCKSTAR", "capitulo": "2025 · Los despidos",
     "overlay": "", "anio": 2025, "etiqueta_linea": "2025 · DESPIDOS",
     "texto": ("Y la polémica más reciente llega desde dentro. A finales de octubre de 2025, Rockstar despide a más de "
               "treinta empleados en Reino Unido. El sindicato IWGB dice que los echaron por organizarse en un grupo "
               "privado de Discord, y lo llama persecución sindical. Rockstar responde que compartían información "
               "confidencial en un foro público, y que no tiene nada que ver con su derecho a sindicarse. En enero de "
               "2026, el tribunal rechazó obligar a Rockstar a pagarles un sueldo provisional. Y en septiembre empezó el "
               "juicio en Glasgow, con treinta y un despedidos. A mediados de noviembre, la decisión aún no se conocía."),
     "rotulos": [{"en": "octubre", "texto": "OCT 2025|+30 DESPIDOS"},
                 {"en": "iwgb", "texto": "SINDICATO IWGB|«PERSECUCIÓN SINDICAL»"},
                 {"en": "confidencial", "texto": "ROCKSTAR|«INFORMACIÓN CONFIDENCIAL»"},
                 {"en": "glasgow", "texto": "GLASGOW · SEP 2026|JUICIO · 31 DESPEDIDOS"}],
     "nombres": ["octubre", "iwgb", "confidencial", "glasgow"],
     "planos": ["NUEVO_Despidos_Captura", "NUEVO_Juicio_Glasgow_Captura"],
     "planos_en": [{"en": "octubre", "plano": "NUEVO_Despidos_Captura"},
                   {"en": "glasgow", "plano": "NUEVO_Juicio_Glasgow_Captura"}]},
    {"id": "p15", "num": 16, "total": T, "titulo": "2026 · EL DEBATE SOBRE GTA VI",
     "capitulo": "2026 · El debate sobre GTA VI", "overlay": "", "anio": 2026,
     "final_revisado": True,  # 13 nov: la última frase está entera (36,2-37,9 s); el «No» que oye Whisper es una respiración
     # 14 nov: reescrito con lo que dice WLRN (24 sep 2026): campaña aprobada en septiembre por 3 M$ y la demanda de 2003
     "texto": ("Y llegamos a hoy. GTA VI sale el diecinueve de noviembre, con Vice City otra vez como telón de fondo. Y "
               "esta vez la relación con la ciudad real es otra. En septiembre, la comisión de Miami Beach aprobó una "
               "campaña de marketing del juego a cambio de tres millones de dólares, según la emisora WLRN. La misma "
               "emisora recordó la demanda haitiana de 2003, que se cerró cuando Rockstar cambió aquella frase. Más de "
               "veinte años después, GTA y Miami han pasado de la demanda al contrato."),
     "rotulos": [{"en": "diecinueve", "texto": "19 NOV 2026|GTA VI"},
                 {"en": "miami", "texto": "MIAMI BEACH · SEP 2026|CAMPAÑA DE GTA VI · 3 M$"},
                 {"en": "contrato", "texto": "2003 → 2026|DE LA DEMANDA AL CONTRATO"}],
     "nombres": ["diecinueve", "miami", "contrato"],
     "planos": ["T2_Jason_Tejado", "@Vice_City:4", "@Leonida_Keys:3", "@GTA6_Mirada:1"],
     "planos_en": [{"en": "vice", "plano": "@Vice_City"},
                   {"en": "miami", "plano": "T2_Autopista"},
                   {"en": "diecinueve", "plano": "@GTA6_Mirada"}]},
    {"id": "p16", "num": 17, "total": T, "titulo": "2026 · ¿POR QUÉ ROCKSTAR SIEMPRE GANA?",
     "capitulo": "¿Por qué Rockstar siempre gana?", "overlay": "", "anio": 2026,
     "texto": ("Así que la pregunta de fondo: ¿por qué Rockstar parece salir ganando siempre? Primero, la publicidad. En "
               "1997, la polémica de GTA 1 se convirtió en titulares gratis, según los propios creadores. Después, Hot "
               "Coffee le costó a Take-Two veinticuatro millones y medio de dólares en devoluciones. Pero GTA V ya roza los "
               "doscientos treinta millones de copias, según Take-Two. En los tribunales, Lindsay Lohan perdió en todas las "
               "instancias, y Jack Thompson acabó inhabilitado. Escándalo, ruido y ventas. Esa es la fórmula que se repite."),
     "rotulos": [{"en": "publicidad", "texto": "PUBLICIDAD|GRATIS"},
                 {"en": "veinticuatro", "texto": "24,5 M$|HOT COFFEE"},
                 {"en": "doscientos", "texto": "CASI 230 MILLONES|GTA V · TAKE-TWO"}],  # proxy de Take-Two, jul 2026
     "nombres": ["publicidad", "veinticuatro", "doscientos"],
     "planos": ["@GTA1_1997:2", "@GTA_Online:2", "Mirada_Terraza", "@Historia_GTA:2"],
     "planos_en": [{"en": "publicidad", "plano": "@Historia_GTA"},
                   {"en": "doscientos", "plano": "@GTA6_Mirada"}]},

    # ---------------------------------------------------------------- CIERRE
    {"id": "cierre", "num": None, "titulo": "", "overlay": "", "capitulo": "Cierre", "anio": 2026,
     "texto": ("Y aquí cerramos. En 1997, un juego de coches vistos desde arriba se convirtió en titular por una campaña y "
               "un debate en la Cámara de los Lores. Hoy, con GTA VI a la vuelta de la esquina, la polémica sigue, con otras "
               "formas. Ahora te toca a ti: ¿cuál fue la más grave? ¿Hot Coffee, la tortura de GTA V, el hackeo de 2022 o "
               "los despidos de 2025? Déjamelo en los comentarios. Si te ha "
               "gustado, suscríbete, que el diecinueve estaremos por aquí. Nos vemos en Leónida."),
     "rotulos": [{"en": "1997", "texto": "1997 → 2026"},
                 {"en": "grave", "texto": "¿CUÁL FUE|LA MÁS GRAVE?"}],
     "nombres": ["1997", "grave"],
     "planos": ["Mirada_Skyline_Noche", "VL_Atardecer_Final", "VL_Lancha_Pareja", "@Vice_City:3", "VL_Azotea_1", "@GTA6_Mirada:1"],
     "planos_en": [{"en": "1997", "plano": "GTA_15_02"},
                   {"en": "grave", "plano": "@GTA6_Mirada"}]},
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