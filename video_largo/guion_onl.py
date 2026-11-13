"""Guion del vídeo largo «GTA Online: de 2013 a GTA VI» de «Leónida al Día» (GTA VI sale el 19 nov 2026).

Mismo formato que guion_rad.py. Datos y fuentes: video_online/investigacion.md. Guion legible: video_online/guion.md.

Campo «canciones»: vacío en todos los bloques (no hay canciones en este vídeo).
Los datos posteriores al 19-nov están marcados con «REVISAR tras el 19-nov» (bloque p_post). Son los únicos que
cambian: si cambian, hay que regrabar su voz.
Versión 2 (coordinador, tras revisor-guion): citas comprobadas en las transcripciones de Take-Two del 21 may, 7 ago
y 9 nov 2026; sin «a día de hoy»: lo posterior al 19 nov va con fecha («cerramos este guion el 13 de noviembre»);
fuera las frases sin fuente y el relleno; planos solo de GTA V / GTA Online cuando se habla de GTA Online.
Bloques marcados con «# REVISAR tras el 19-nov»: hook, p_post y cierre.
No importa fuentes_sg. VIDEOS_EXTRA vacío: no hay URLs oficiales de vídeo verificadas en esta sesión.
"""
import re

VIDEOS_EXTRA = {}
RECORTES = {}
MARCO = True

PLANOS_FIJOS = {"Mirada_Logo", "VL_Atardecer_Final", "Portada_Animada", "Lanz_Final_19N"}

# Música por época (hecha con código en el propio montaje: sin pistas con licencia)
MUSICA = {"hook": "synthwave", "p01": "chiptune", "p03": "breakbeat", "p06": "hiphop", "p07": "synthwave", "p10": "synthwave",
          "p_post": "synthwave"}

# Línea de tiempo de abajo
LINEA_ANIMADA = True
LINEA = [(2013, "GTA ONLINE"), (2014, "PS4 Y XBOX ONE"), (2015, "GOLPES"), (2020, "CAYO PERICO"),
         (2021, "THE CONTRACT"), (2022, "GTA PLUS"), (2026, "KORTZ · GTA VI")]

# Pronunciación para la voz: cada valor es UNA palabra
FONETICA = {
    "III": "3", "IV": "4", "V": "5", "VI": "6", "Online": "Onlain", "Heists": "Jeists", "Heist": "Jeist",
    "Contract": "Cóntract", "Dre": "Dréi", "Dr": "Doctor", "Zelnick": "Zélnik", "Take-Two": "Teik-Tu",
    "Rockstar": "Rókstar", "Kortz": "Kórts", "Center": "Sénter", "Plus": "Plas", "Maze": "Méis", "Bank": "Bank",
    "PlayStation": "Pléistéishon", "Xbox": "Ékbox", "Series": "Síriz", "The": "De", "single-player": "sínguel-pléier",
    "Perico": "Perico", "Cayo": "Cayo", "Los": "Los", "Santos": "Sántos", "Newswire": "Niusuáir",
    "Strauss": "Estráus", "Lainie": "Léini", "Goldstein": "Góldstain", "Doctor": "Doctor", "FiveM": "Fáiv-Em",
    "Cfx.re": "Ce-Efe-Equis-punto-Erre-E", "Twitch": "Tuich", "streamers": "estrímers", "Game": "Guéim",
    "Informer": "Infórmer", "Store": "Estor", "experience": "expíriens", "Jason": "Yéison", "Lucía": "Lucía",
    "Leónida": "Leónida", "Center": "Sénter", "Gunrunning": "Gánraning", "Tuners": "Túners",
    "Mercenaries": "Mérsenaris", "A": "a", "Safehouse": "Séifjaus", "in": "in", "Hills": "Jils",
    "Andreas": "Andréas",
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


T = 15

BLOQUES = [
    # ---------------------------------------------------------------- HOOK  # REVISAR tras el 19-nov
    {"id": "hook", "num": None, "titulo": "", "overlay": "", "capitulo": "Introducción",
     "texto": ("Trece años después de abrir sus puertas, GTA Online sigue en marcha. Y GTA VI ya está en la calle. Así "
               "que la pregunta es inevitable: ¿qué pasa ahora con el online? Repasamos su historia, de los primeros "
               "golpes a la última llamada de Take-Two. Y separamos dos cosas que en internet se mezclan mucho: lo que "
               "está confirmado por escrito y lo que solo se dice por ahí."),
     "rotulos": [{"t": 0.0, "dur": 2.4, "negro": True, "texto": "2013|→ 2026"},
                 {"en": "Trece", "texto": "13 AÑOS|DE GTA ONLINE"},
                 {"en": "confirmado", "texto": "CONFIRMADO|O SOLO SE DICE"}],
     "nombres": [],
     "canciones": [],
     "planos": ["@GTA_Online:2", "@GTA6_Mirada:3", "@GTA5_2013:2"],
     "planos_en": [{"en": "Trece", "plano": "@GTA_Online"},
                   {"en": "calle", "plano": "@GTA6_Mirada"}]},

    # ---------------------------------------------------------------- ACTO I · EL ARRANQUE (2013-2015)
    {"id": "p01", "num": 1, "total": T, "titulo": "2013 · EL ARRANQUE", "capitulo": "2013 · El arranque",
     "overlay": "", "anio": 2013, "cartela": {"anio": "2013", "acto": "ACTO I", "titulo": "EL ARRANQUE"},
     "texto": ("GTA Online se abrió el uno de octubre de dos mil trece, dos semanas después de GTA V, según la prensa "
               "de la época. El mismo Los Santos, pero con otra gente dentro. Creas tu personaje, empiezas con poco y te "
               "ganas cada dólar con trabajos, carreras y encargos. El juego dejaba de ser una historia para una persona "
               "y pasaba a ser un sitio donde quedar. Con amigos o con desconocidos, que en Los Santos viene a ser lo "
               "mismo: alguien que te puede robar el coche."),
     "rotulos": [{"en": "Online", "texto": "GTA ONLINE|1 OCT 2013"},
                 {"en": "semanas", "texto": "2 SEMANAS|DESPUÉS DE GTA V"}],
     "nombres": ["Online"],
     "canciones": [],
     "planos": ["@GTA_Online:3", "@GTA5_2013:6"],
     "planos_en": [{"en": "Online", "plano": "@GTA_Online"},
                   {"en": "semanas", "plano": "@GTA5_2013"}]},
    {"id": "p02", "num": 2, "total": T, "titulo": "2014 · LA MUDANZA", "capitulo": "2014-2015 · La mudanza",
     "overlay": "", "anio": 2014,
     "texto": ("El dieciocho de noviembre de dos mil catorce, GTA Online da el salto a PlayStation cuatro y Xbox One. "
               "Los de ordenador esperan cinco meses más, hasta abril de dos mil quince. Así empieza una costumbre que "
               "dura años: cada vez que GTA V cambia de casa, el online se muda con él, con los muebles y los vecinos. "
               "Pocas fiestas duran tanto sin que nadie apague la música."),
     "rotulos": [{"en": "dieciocho", "texto": "18 NOV 2014|PS4 Y XBOX ONE"},
                 {"en": "cinco", "texto": "5 MESES MÁS|PARA EL PC"}],
     "nombres": ["dieciocho"],
     "canciones": [],
     "planos": ["@GTA5_2013:4", "@GTA5_Oficial_810:3"],
     "planos_en": [{"en": "dieciocho", "plano": "@GTA5_2013"},
                   {"en": "cinco", "plano": "@GTA5_Oficial_810"}]},

    # ---------------------------------------------------------------- ACTO II · LOS GOLPES (2015-2021)
    {"id": "p03", "num": 3, "total": T, "titulo": "2015 · LOS GOLPES", "capitulo": "2015 · Los golpes",
     "overlay": "", "anio": 2015, "cartela": {"anio": "2015", "acto": "ACTO II", "titulo": "LOS GOLPES"},
     "texto": ("El gran cambio llega en dos mil quince: los golpes. Misiones largas para varios jugadores, con "
               "preparación, reparto de papeles y un final que puede salir fatal. Según Game Informer, el veinticuatro "
               "de febrero se supo la fecha: llegaban a las consolas el diez de marzo, y la versión de PC se iba al "
               "catorce de abril. Desde entonces, el online deja de ser solo dar vueltas por la ciudad. Hay que hacer un "
               "plan con amigos y cumplirlo. Y descubrir cuál de tus amigos es el que siempre estrella el coche de huida."),
     "rotulos": [{"en": "golpes", "texto": "LOS GOLPES|MARZO 2015"},
                 {"en": "diez", "texto": "10 MAR 2015|CONSOLAS"},
                 {"en": "catorce", "texto": "14 ABR 2015|PC"}],
     "nombres": ["golpes"],
     "canciones": [],
     "planos": ["N10_Captura_Gameinformer_2015", "@GTA_Online:4", "@GTA5_2013:4"],
     "planos_en": [{"en": "golpes", "plano": "@GTA_Online"},
                   {"en": "Informer", "plano": "N10_Captura_Gameinformer_2015"}]},
    {"id": "p04", "num": 4, "total": T, "titulo": "2020 · CAYO PERICO", "capitulo": "2020 · Cayo Perico",
     "overlay": "", "anio": 2020,
     "texto": ("En diciembre de dos mil veinte llega Cayo Perico: un golpe en una isla con mapa propio, fuera de Los "
               "Santos, que se prepara desde un submarino. Salió el quince de diciembre. Según la prensa, fue el último "
               "gran golpe hasta el de dos mil veintiséis. Un golpe grande cada seis años. A ese ritmo, el siguiente "
               "nos pilla en la residencia, planeando el asalto a la máquina del café."),
     "rotulos": [{"en": "Perico", "texto": "CAYO PERICO|15 DIC 2020"},
                 {"en": "submarino", "texto": "SUBMARINO|BASE DE OPERACIONES"}],
     "nombres": ["Perico"],
     "canciones": [],
     "planos": ["N10_Captura_Newswire_Cayo", "@GTA_Online:3", "@GTA5_Oficial_810:3"],
     "planos_en": [{"en": "Perico", "plano": "N10_Captura_Newswire_Cayo"},
                   {"en": "submarino", "plano": "@GTA_Online"}]},
    {"id": "p05", "num": 5, "total": T, "titulo": "2021 · THE CONTRACT", "capitulo": "2021 · The Contract",
     "overlay": "", "anio": 2021,
     "texto": ("Un año después, en diciembre de dos mil veintiuno, llega The Contract, según la prensa de la época. Su "
               "gran reclamo tiene nombre propio: Doctor Dre. Ocho años después del estreno, el online seguía fichando "
               "caras conocidas para meter historias nuevas en el mismo mapa. Ni juego nuevo, ni ciudad nueva: invitado "
               "nuevo. Es la receta que el online va a repetir desde entonces."),
     "rotulos": [{"en": "Contract", "texto": "THE CONTRACT|DIC 2021"},
                 {"en": "Dre", "texto": "DOCTOR DRE|EL GRAN RECLAMO"}],
     "nombres": ["Contract", "Dre"],
     "canciones": [],
     "planos": ["NUEVO_Dr_Dre_Estudio", "@GTA_Online:3", "@GTA5_2013:3"],
     "planos_en": [{"en": "Contract", "plano": "@GTA_Online"},
                   {"en": "Dre", "plano": "NUEVO_Dr_Dre_Estudio"}]},

    {"id": "p06", "num": 6, "total": T, "titulo": "2017-2025 · UNA TRAS OTRA", "capitulo": "2017-2025 · Una tras otra",
     "overlay": "", "anio": 2019,
     "texto": ("Y entre golpe y golpe, el online no para de estrenar cosas. Según la prensa especializada, en junio de dos "
               "mil diecisiete llega Gunrunning, con búnkeres y tráfico de armas. En dos mil diecinueve abre el casino, y "
               "en diciembre de ese año llega su golpe. En julio de dos mil veintiuno, Los Santos Tuners convierte el "
               "juego en una quedada de coches tuneados. En junio de dos mil veintitrés, San Andreas Mercenaries. Y en "
               "diciembre de dos mil veinticinco, A Safehouse in the Hills. Una actualización grande, más o menos, cada "
               "verano y cada Navidad. Como el turrón, pero con lanzacohetes."),
     "rotulos": [{"en": "Gunrunning", "texto": "GUNRUNNING|JUN 2017"},
                 {"en": "casino", "texto": "EL CASINO|2019"},
                 {"en": "Tuners", "texto": "LOS SANTOS TUNERS|JUL 2021"},
                 {"en": "Mercenaries", "texto": "SAN ANDREAS MERCENARIES|JUN 2023"},
                 {"en": "Safehouse", "texto": "A SAFEHOUSE IN THE HILLS|DIC 2025"}],
     "nombres": ["Gunrunning", "Tuners", "Safehouse"],
     "canciones": [],
     "planos": ["@GTA_Online:2", "@GTA5_Oficial_810:4", "@GTA5_2013:4"],
     "planos_en": [{"en": "Gunrunning", "plano": "@GTA5_Oficial_810"},
                   {"en": "Tuners", "plano": "@GTA_Online"},
                   {"en": "Safehouse", "plano": "@GTA5_2013"}]},

    # ---------------------------------------------------------------- ACTO III · EL SERVICIO VIVO (2022-2026)
    {"id": "p07", "num": 7, "total": T, "titulo": "2022 · PS5 Y GTA PLUS", "capitulo": "2022 · PS5 y GTA Plus",
     "overlay": "", "anio": 2022, "cartela": {"anio": "2022", "acto": "ACTO III", "titulo": "EL SERVICIO VIVO"},
     "texto": ("En dos mil veintidós llegan dos novedades casi a la vez. El quince de marzo, GTA V y GTA Online salen "
               "en PlayStation cinco y Xbox Series. Diez días después, Rockstar presenta GTA Plus: una suscripción de "
               "cinco dólares con noventa y nueve al mes, en su estreno solo para esas consolas. Entre otras cosas, "
               "cada mes deja quinientos mil dólares del juego en tu cuenta de Maze Bank. Desde entonces, el online se "
               "paga de dos formas: compras sueltas o cuota mensual. Como el gimnasio, pero aquí la cuota sí te da "
               "algo aunque no vayas."),
     "rotulos": [{"en": "quince", "texto": "15 MAR 2022|PS5 Y XBOX SERIES"},
                 {"en": "Plus", "texto": "GTA+|5,99 $ AL MES"},
                 {"en": "Maze", "texto": "MAZE BANK|500.000 GTA$ AL MES"}],
     "nombres": ["Plus"],
     "canciones": [],
     "planos": ["N10_Captura_Game_Informer_PS5", "NUEVO_GTAPlus_Captura", "NUEVO_Reediciones_Logos", "@GTA_Online:2",
                "@GTA5_2013:4"],
     "planos_en": [{"en": "quince", "plano": "NUEVO_Reediciones_Logos"},
                   {"en": "Plus", "plano": "NUEVO_GTAPlus_Captura"}]},
    {"id": "p08", "num": 8, "total": T, "titulo": "2023 · EL ROL", "capitulo": "2023 · El rol",
     "overlay": "", "anio": 2023,
     "texto": ("Y mientras tanto, el online crece por un sitio que nadie había planeado: el rol. Servidores donde la "
               "gente interpreta a un personaje durante horas, con sus normas, sus policías y sus atracos. Una de las "
               "herramientas para montarlos es FiveM, hecha por aficionados. Rockstar vetó a sus creadores en dos mil "
               "quince, y en agosto de dos mil veintitrés acabó comprando su empresa, Cfx.re. De echarlos a ficharlos "
               "en ocho años. Si no puedes con ellos, cómpralos."),
     "rotulos": [{"en": "rol", "texto": "SERVIDORES DE ROL|GTA V"},
                 {"en": "FiveM", "texto": "FIVEM|VETADO EN 2015"},
                 {"en": "Cfx.re", "texto": "ROCKSTAR COMPRA CFX.RE|AGO 2023"}],
     "nombres": ["FiveM", "Cfx.re"],
     "canciones": [],
     "planos": ["NUEVO_Cfx_Comunicado", "@GTA_Online:3", "@GTA5_Oficial_810:3"],
     "planos_en": [{"en": "FiveM", "plano": "@GTA_Online"},
                   {"en": "Cfx.re", "plano": "NUEVO_Cfx_Comunicado"}]},
    {"id": "p09", "num": 9, "total": T, "titulo": "2026 · LAS CUENTAS", "capitulo": "2026 · Las cuentas",
     "overlay": "", "anio": 2026,
     "texto": ("¿Y cómo le va en las cuentas? En la llamada de resultados de mayo de dos mil veintiséis, la directora "
               "financiera de Take-Two, Lainie Goldstein, cuenta que GTA Online creció y superó lo que esperaban. "
               "Zelnick lo relaciona con una actualización concreta: una casa franca en las colinas. Y lo resume en "
               "una frase: GTA Online es un negocio de servicio en vivo. Trece años, y todavía crece. Hay restaurantes "
               "que no aguantan ni la segunda temporada."),
     "rotulos": [{"en": "Goldstein", "texto": "LAINIE GOLDSTEIN|DIRECTORA FINANCIERA"},
                 {"en": "colinas", "texto": "UNA CASA FRANCA|EN LAS COLINAS"},
                 {"en": "vivo", "texto": "«SERVICIO EN VIVO»|ZELNICK, MAYO 2026"}],
     "nombres": ["Goldstein"],
     "canciones": [],
     "planos": ["NUEVO_Cuentas_TakeTwo", "@GTA_Online:2", "@GTA5_2013:3", "@GTA5_Oficial_810:3"],
     "planos_en": [{"en": "Goldstein", "plano": "NUEVO_Cuentas_TakeTwo"},
                   {"en": "colinas", "plano": "@GTA_Online"}]},

    # ---------------------------------------------------------------- ACTO IV · LO QUE HAN DICHO (2026)
    {"id": "p10", "num": 10, "total": T, "titulo": "MAYO 2026 · «PREMATURO»", "capitulo": "Mayo 2026 · «Prematuro»",
     "overlay": "", "anio": 2026, "cartela": {"anio": "2026", "acto": "ACTO IV", "titulo": "LO QUE HAN DICHO"},
     "texto": ("Vamos con lo que ha dicho la empresa, con fecha y por escrito. En esa misma llamada del veintiuno de "
               "mayo, un analista pregunta por GTA Online después de GTA VI. Strauss Zelnick, consejero delegado de "
               "Take-Two, responde que es difícil saber cómo le irá, pero que, en cualquier caso, seguirá en el mercado. "
               "Y cuando le preguntan por una versión online de GTA VI, dice que hablar de ella sería prematuro, porque "
               "no hay nada anunciado. Varias frases y ninguna fecha. Muy Take-Two."),
     "rotulos": [{"en": "Zelnick", "texto": "STRAUSS ZELNICK|CONSEJERO DELEGADO"},
                 {"en": "veintiuno", "texto": "21 MAY 2026|RESULTADOS"},
                 {"en": "mercado", "texto": "«SEGUIRÁ|EN EL MERCADO»"},
                 {"en": "prematuro", "texto": "«PREMATURO»|SIN ONLINE ANUNCIADO"}],
     "nombres": ["Zelnick"],
     "canciones": [],
     "planos": ["NUEVO_Zelnick_Captura", "N10_Captura_Transcripcion_Q4", "@GTA6_T1:4", "@GTA6_Lanzamiento:2"],
     "planos_en": [{"en": "Zelnick", "plano": "NUEVO_Zelnick_Captura"},
                   {"en": "prematuro", "plano": "N10_Captura_Transcripcion_Q4"}]},
    {"id": "p11", "num": 11, "total": T, "titulo": "AGOSTO 2026 · EL KORTZ", "capitulo": "Agosto 2026 · El Kortz",
     "overlay": "", "anio": 2026,
     "texto": ("En julio llega por fin otro golpe grande: The Kortz Center Heist, el primero de ese tamaño desde Cayo "
               "Perico, según la prensa. Take-Two lo confirma en su llamada del siete de agosto: el catorce de julio, "
               "Rockstar lanzó el golpe del Kortz Center. Y Zelnick añade dos cosas. Que trece años después la gente "
               "sigue muy enganchada, con momentos de participación récord. Y que el ritmo de actualizaciones es "
               "estable y esperan seguir apoyando GTA Online en adelante. Cifras del golpe, ninguna. La frase sí, el "
               "número no."),
     "rotulos": [{"en": "Kortz", "texto": "THE KORTZ CENTER HEIST|14 JUL 2026"},
                 {"en": "siete", "texto": "7 AGO 2026|TAKE-TWO"},
                 {"en": "récord", "texto": "PARTICIPACIÓN RÉCORD|«EN ALGUNOS MOMENTOS»"},
                 {"en": "apoyando", "texto": "«SEGUIR APOYANDO|GTA ONLINE»"}],
     "nombres": ["Kortz"],
     "canciones": [],
     "planos": ["N10_Captura_Newswire_Kortz", "N10_Captura_Transcripcion_Q1", "@GTA_Online:3", "@GTA5_2013:3",
                "@GTA5_Oficial_810:2", "@GTAO_Oficial_810:4"],
     "planos_en": [{"en": "Kortz", "plano": "N10_Captura_Newswire_Kortz"},
                   {"en": "siete", "plano": "N10_Captura_Transcripcion_Q1"}]},
    {"id": "p12", "num": 12, "total": T, "titulo": "NOVIEMBRE 2026 · LA ÚLTIMA", "capitulo": "Noviembre 2026 · La última",
     "overlay": "", "anio": 2026,
     "texto": ("La más reciente llegó el nueve de noviembre, a diez días de GTA VI. Zelnick lo dijo más claro que "
               "nunca: Rockstar seguirá apoyando GTA Online con contenido nuevo y eventos para su enorme comunidad. "
               "Contó también que los miembros de GTA Plus crecieron a doble dígito, y que se podían ganar objetos "
               "exclusivos de GTA Online viendo a ciertos streamers de rol en Twitch. Un analista le preguntó si el "
               "presupuesto de GTA VI incluía también una versión online. La respuesta: que no han hablado de "
               "presupuestos en absoluto. Esquivada de manual."),
     "rotulos": [{"en": "nueve", "texto": "9 NOV 2026|TAKE-TWO"},
                 {"en": "eventos", "texto": "«CONTENIDO NUEVO|Y EVENTOS»"},
                 {"en": "Twitch", "texto": "OBJETOS POR VER|ROL EN TWITCH"},
                 {"en": "absoluto", "texto": "«NO HEMOS HABLADO|DE PRESUPUESTOS»"}],
     "nombres": ["Twitch"],
     "canciones": [],
     "planos": ["N9_Captura_Transcripcion_Nov", "NUEVO_Twitch_Captura", "@GTA_Online:2", "@GTA6_Mirada:3",
                "@GTA6_Lanzamiento:2"],
     "planos_en": [{"en": "nueve", "plano": "N9_Captura_Transcripcion_Nov"},
                   {"en": "Twitch", "plano": "NUEVO_Twitch_Captura"}]},
    {"id": "p13", "num": 13, "total": T, "titulo": "LA FICHA DE GTA VI", "capitulo": "La ficha de GTA VI",
     "overlay": "", "anio": 2026,
     "texto": ("¿Y qué dice Rockstar del propio GTA VI? En su ficha de PlayStation Store, tal como estaba el doce de "
               "noviembre, se lee en inglés single-player experience: una experiencia para un jugador. La ficha marca "
               "un jugador y que se puede jugar sin conexión, y avisa de que las funciones en línea necesitan cuenta. "
               "Ese aviso no describe ningún modo concreto. La ficha dice una cosa clara: un jugador. Lo demás es letra "
               "pequeña."),
     "rotulos": [{"en": "single-player", "texto": "«SINGLE-PLAYER|EXPERIENCE»"},
                 {"en": "conexión", "texto": "SE PUEDE JUGAR|SIN CONEXIÓN"}],
     "nombres": ["single-player"],
     "canciones": [],
     "planos": ["N10_Captura_PS_Store", "@GTA6_Mirada:4", "@GTA6_T2:3"],
     "planos_en": [{"en": "single-player", "plano": "N10_Captura_PS_Store"}]},
    {"id": "p14", "num": 14, "total": T, "titulo": "CONFIRMADO Y LO QUE SE DICE", "capitulo": "Confirmado y lo que se dice",
     "overlay": "", "anio": 2026,
     "texto": ("Así que, separando. Confirmado, por escrito o en transcripción: GTA VI se vende como una experiencia "
               "para un jugador, y Take-Two ha dicho tres veces este año que GTA Online sigue, la última con contenido "
               "nuevo y eventos. No confirmado: que vaya a haber un GTA Online de pago aparte, o un online de GTA VI con "
               "fecha. Y ojo con una cita que circula, atribuida a Take-Two, sobre apoyar GTA Online después de GTA VI y "
               "más allá: viene de un foro, no de una transcripción. Una cita de verdad tiene fecha, nombre y frase "
               "exacta. Si le falta alguna de las tres, desconfía."),
     "rotulos": [{"en": "Confirmado", "texto": "CONFIRMADO|POR ESCRITO"},
                 {"en": "foro", "texto": "CITA DE UN FORO|DESCARTADA"}],
     "nombres": [],
     "canciones": [],
     "planos": ["@GTA6_Lanzamiento:3", "@GTA6_T2:3", "@GTA6_Mirada:3"],
     "planos_en": [{"en": "Confirmado", "plano": "@GTA6_Lanzamiento"},
                   {"en": "foro", "plano": "@GTA6_T2"}]},
    # REVISAR tras el 19-nov: si Rockstar o Take-Two anuncian algo del online, cambiar este bloque (se regraba su voz)
    {"id": "p_post", "num": 15, "total": T, "titulo": "13 DE NOVIEMBRE", "capitulo": "Lo que sabemos a 13 de noviembre",
     "overlay": "", "anio": 2026,
     "texto": ("Cerramos este guion el trece de noviembre. Hasta esa fecha, Rockstar no había anunciado ningún modo "
               "online para GTA VI, y GTA Online seguía activo, con la promesa de contenido nuevo. Si algo de esto ha "
               "cambiado desde el diecinueve, te lo contamos en el comentario fijado. Lo que no cambia es la pregunta."),
     "rotulos": [{"en": "trece", "texto": "GUION CERRADO|13 NOV 2026"},
                 {"en": "pregunta", "texto": "PREGUNTA|ABIERTA"}],
     "nombres": [],
     "canciones": [],
     "planos": ["@GTA6_Mirada:3", "@GTA6_Lanzamiento:2"],
     "planos_en": [{"en": "pregunta", "plano": "@GTA6_Lanzamiento"}]},

    # ---------------------------------------------------------------- CIERRE  # REVISAR tras el 19-nov
    {"id": "cierre", "num": None, "titulo": "", "overlay": "", "capitulo": "De 2013 a GTA VI", "anio": 2026,
     "texto": ("Trece años de GTA Online: golpes, islas, suscripciones y un invitado de lujo. Ahora te toca a ti: ¿vas "
               "a seguir en GTA Online con GTA VI ya en la calle, o te quedas con la historia de Jason y Lucía? Y si "
               "tienes que elegir una actualización: ¿Cayo Perico, The Contract o el Kortz Center? Déjamelo en los "
               "comentarios. Si te ha gustado, suscríbete. Nos vemos en Leónida."),
     "rotulos": [{"en": "comentarios", "texto": "¿CAYO PERICO, THE CONTRACT|O EL KORTZ?"},
                 {"en": "Trece", "texto": "13 AÑOS|DE GTA ONLINE"}],
     "nombres": [],
     "canciones": [],
     "planos": ["Mirada_Logo", "VL_Atardecer_Final", "Lanz_Final_19N", "@GTA6_Mirada:4", "Portada_Animada"],
     "planos_en": [{"en": "comentarios", "plano": "Mirada_Logo"},
                   {"en": "Trece", "plano": "VL_Atardecer_Final"}]},
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
