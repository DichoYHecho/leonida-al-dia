"""Guion del vídeo largo «Las radios de GTA: de 1997 a GTA VI» de «Leónida al Día» (GTA VI sale el 19 nov 2026).

Mismo formato que guion_sg.py. Datos y fuentes: investigacion.md. Edición, planos y canciones: edicion.md.

«canciones» (campo nuevo de cada bloque, lo lee montaje.py desde esta versión):
  al acabar la frase donde la voz dice «en», el montaje abre un hueco y suena «seg» segundos de la canción, con la
  música de fondo bajada. El audio lo pone el usuario en la carpeta «canciones» (por ejemplo billie_jean.mp3); con
  «desde» se elige el segundo de la canción donde empieza el fragmento. Sin archivo, el bloque se monta sin hueco.
  Ningún audio está descargado ni incluido aquí.
  Riesgo de copyright: aceptado por el usuario. Ver «Canciones y copyright» en edicion.md.

Los datos marcados como SIN CONFIRMAR en investigacion.md no aparecen en el texto como hechos.
No importa fuentes_sg. VIDEOS_EXTRA vacío: no hay URLs oficiales verificadas en esta sesión.
"""
import re

VIDEOS_EXTRA = {}
RECORTES = {}
MARCO = True

PLANOS_FIJOS = {"GTA_15_01", "Mirada_Logo", "VL_Fecha", "VCA_Logo", "Portada_Animada", "IMG_GTA1", "IMG_GTA1_Caja",
                "IMG_RaceNChase", "IMG_VC_Portada"}

# Música por época (hecha con código en el propio montaje: sin pistas con licencia)
MUSICA = {"hook": "synthwave", "p01": "chiptune", "p03": "breakbeat", "p07": "chiptune", "p09": "hiphop",
          "p12": "synthwave", "p14": "synthwave"}

# Línea de tiempo de abajo
LINEA_ANIMADA = True
LINEA = [(1997, "GTA"), (2001, "GTA III"), (2002, "VICE CITY"), (2004, "SAN ANDREAS"), (2005, "PSP"),
         (2008, "GTA IV"), (2013, "GTA V"), (2018, "LICENCIAS"), (2021, "THE CONTRACT"), (2026, "GTA VI")]

# Pronunciación para la voz: cada valor es UNA palabra (nombres ingleses de radios, artistas y títulos)
FONETICA = {
    "III": "3", "IV": "4", "V": "5", "VI": "6", "Liberty": "Líberti", "City": "Siti", "Miami": "Maiámi",
    "Rock": "Rok", "Radio": "Radio", "Craig": "Creig", "Conner": "Cóner", "Colin": "Cólin", "Anderson": "Ándersson",
    "Grant": "Grant", "Middleton": "Mídlton", "Gangster": "Gángster", "Friday": "Fráidei", "Slumpussy": "Slámpusi",
    "Head": "Jed", "N-CT": "Ene-Ce-Té", "Anywhere": "Énigüer", "Flashback": "Flásbac", "Chatterbox": "Chátterbox",
    "Lazlow": "Láslou", "Jones": "Yons", "Scarface": "Escárfeis", "Flash": "Flash", "V-Rock": "Vi-Rok",
    "Emotion": "Emóshon", "Wave": "Ueiv", "Wildstyle": "Uaildstáil", "Epic": "Épic", "Records": "Rékords",
    "Vice": "Vais", "Santos": "Sántos", "K-DST": "Kei-Di-Ese-Té", "Vladivostok": "Vladivóstok", "Non": "Non",
    "Stop": "Estop", "Kenny": "Quéni", "Loggins": "Lóguins", "Lab": "Láb", "Welcome": "Uélcom",
    "Alchemist": "Álquemist", "Oh": "Ou", "Trilogy": "Trílogi", "Definitive": "Definitiv", "Contract": "Cóntract",
    "Dr": "Doctor", "Dre": "Dréi", "Hit-Boy": "Jit-Boi", "Freddie": "Fredi", "Gibbs": "Guibs", "Pusha": "Púsha",
    "Kodak": "Kódak", "Big": "Big", "West": "Uest", "Coast": "Cóst", "Classics": "Clásics", "Day": "Dei",
    "MOTOMAMI": "Motomami", "Arca": "Árca", "Love": "Lov", "Long": "Long", "Road": "Roud", "Tom": "Tom",
    "Petty": "Péti", "Pointer": "Póinter", "Sisters": "Sísters", "Hot": "Jot", "Together": "Tuguéder",
    "Spotify": "Spótify", "Chamber": "Chéimber", "Cocoteo": "Cocotéo", "Dirty": "Dérti", "South": "Saus",
    "AfroBank": "Áfrobank", "Back": "Bak", "Country": "Cántri", "Coral": "Corál", "Chorus": "Corus",
    "The": "De", "On": "On", "Move": "Muv", "Ghetto": "Gueto", "Fingers": "Fíngers", "Funami": "Funámi",
    "Flymutha": "Flaimutá", "Toys": "Tois", "Are": "Ar", "Real": "Rial", "Billie": "Bili", "Jean": "Yin",
    "Africa": "África", "Toto": "Tóto", "Rush": "Rash", "Debbie": "Débi", "Harry": "Jári", "Push": "Push",
    "Limit": "Límit", "Paul": "Pol", "Engemann": "Éngueman", "Slow": "Eslou", "Ride": "Ráid", "Foghat": "Fóget",
    "Green": "Grin", "River": "Ríver", "Creedence": "Crídens", "Clearwater": "Clíarguater", "Nightmare": "Náitmer",
    "Smith": "Smit", "Axl": "Ásel", "Rose": "Ros", "Guns": "Gans", "Jailbreak": "Yéilbreik", "Thin": "Tin",
    "Lizzy": "Lísi", "Next": "Nekst", "Episode": "Épisod", "Sleepwalking": "Slípuolkin", "Chain": "Chéin",
    "Gang": "Gan", "Mirror": "Mírror", "Park": "Park",
    "G": "Yi", "Iggy": "Iguí", "Pop": "Pop", "Stooges": "Estúgues",
    "Lost": "Lost", "Damned": "Dámd", "Ballad": "Bálad", "Gay": "Guei", "Tony": "Toni", "Euphoria": "Iufória",
    "RAGE": "Reich", "Claude": "Clod", "Tommy": "Tomi", "Vercetti": "Verchéti", "Samuel": "Sámuel",
    "Liotta": "Lióta", "Tenpenny": "Tenpeni", "Jackson": "Yákson", "CJ": "Siyéi", "London": "Lóndon",
    "Leonida": "Leónida", "Leónida": "Leónida", "Michael": "Máikel", "Online": "Onlain", "Bronx": "Bronks",
    "Houser": "Jáuser", "Degenatron": "Degenatrón", "Cluckin'": "Clókin", "Bell": "Bel", "Richards": "Rítchards",
    "Stories": "Stóris", "Lips": "Lips", "Free": "Frí", "Rise": "Ráis", "Jam": "Yam", "Entertaining": "Entertenin",
    "America": "América", "WCTR": "Dábliu-Ce-Té-Erre", "Integrity": "Intégriti", "Algonquin": "Algonkin",
    "FlyLo": "Fláilo", "Flying": "Fláin", "Lotus": "Lótus", "Self": "Self", "Media": "Mídia", "Player": "Pléier",
    "Locker": "Lóquer", "Music": "Miusik", "User": "Iúser", "Diamond": "Dáimond", "MP3": "Eme-Pe-Tres",
    "PSP": "Pe-Ese-Pe", "Billy": "Bili", "Dexter": "Dékster", "Absurd": "Absurd", "Ventures": "Véntures",
    "MF": "Eme-Efe", "DOOM": "Dum", "Krayzie": "Kréisi", "Bone": "Boun",
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
    # ---------------------------------------------------------------- HOOK
    {"id": "hook", "num": None, "titulo": "", "overlay": "", "capitulo": "Introducción",
     "texto": ("Imagina que subes a un coche en mil novecientos noventa y siete y pones la radio. Suena una canción "
               "que no conoces, en una emisora que no existe. Veintinueve años después, esa radio sigue en la saga. "
               "El diecinueve de noviembre sale GTA VI. Así que hacemos un repaso que nadie te "
               "ha pedido: todas las radios de GTA, de la primera a la última. Con su música, sus locutores y las "
               "licencias que se han ido perdiendo por el camino. Y al final, te hago una pregunta."),
     "rotulos": [{"t": 0.0, "dur": 2.4, "negro": True, "texto": "1997|→ 2026"},
                 {"en": "veintinueve", "texto": "29 AÑOS"},
                 {"en": "diecinueve", "texto": "19 NOV 2026|SALE GTA VI"}],
     "nombres": ["veintinueve", "diecinueve"],
     "canciones": [],
     "planos": ["NUEVO_Dial_Coche", "@GTA1_1997:2", "@GTA3_2001:2", "@VC_DE:2", "Mirada_Logo", "T1_Noche_Aerea", "@GTA5_2013:2"],
     "planos_en": [{"en": "coche", "plano": "NUEVO_Dial_Coche"},
                   {"en": "veintinueve", "plano": "Lanz_Descapotable"}]},

    # ---------------------------------------------------------------- ACTO I · LA RADIO ORIGINAL (1997-1999)
    {"id": "p01", "num": 1, "total": T, "titulo": "1997 · GTA 1", "capitulo": "1997 · GTA 1", "overlay": "",
     "anio": 1997, "cartela": {"anio": "1997", "acto": "ACTO I", "titulo": "LA RADIO ORIGINAL"},
     "texto": ("En mil novecientos noventa y siete, GTA ya tenía radio, y no era de relleno. Las emisoras tenían "
               "canciones hechas a medida. Detrás de buena parte de esa música estaba Craig Conner, que escribió e "
               "interpretó temas para varias emisoras. Colin Anderson y Grant Middleton trabajaron en lo mismo, con "
               "otros nombres. Y el tema principal del juego, Gangster Friday, aparece acreditado a una banda que no "
               "existe: Slumpussy. Emisoras como N-CT FM, Radio setenta y seis FM o Head Radio. Escucha Radio setenta y "
               "seis FM. Ojo a Head Radio: años después volverá, en GTA III."),
     "rotulos": [{"en": "Conner", "texto": "CRAIG CONNER|MÚSICA ORIGINAL"},
                 {"en": "Slumpussy", "texto": "SLUMPUSSY|BANDA FICTICIA"},
                 {"en": "setenta", "texto": "RADIO 76 FM|1997"},
                 {"en": "Head", "texto": "HEAD RADIO|VUELVE EN GTA III"}],
     "nombres": ["Conner", "Slumpussy", "Head", "setenta", "Gangster"],
     "canciones": [{"en": "Escucha", "titulo": "On the Move", "artista": "Ghetto Fingers",
                    "emisora": "Radio '76 FM", "juego": "GTA 1 (1997)", "seg": 4}],
     "planos": ["@GTA1_1997:6", "IMG_GTA1", "IMG_GTA1_Caja", "IMG_RaceNChase", "GTA_15_05", "@GTA1_1997:2"],
     "planos_en": [{"en": "Conner", "plano": "IMG_GTA1_Caja"},
                   {"en": "Head", "plano": "@GTA1_1997"},
                   {"en": "Gangster", "plano": "IMG_GTA1"}]},
    {"id": "p02", "num": 2, "total": T, "titulo": "1999 · GTA 2", "capitulo": "1999 · GTA 2", "overlay": "",
     "anio": 1999,
     "texto": ("Dos años después llega GTA 2, en la ciudad sin nombre real que es Anywhere City. Tiene radio, claro: "
               "en Funami FM, la emisora de la banda yakuza, suena esto. Casi toda la música de GTA 2 es original, hecha para el juego. Su historia musical merece un vídeo aparte. "
               "Así que aquí la marcamos en el mapa, y seguimos."),
     "rotulos": [{"en": "Anywhere", "texto": "GTA 2|ANYWHERE CITY"},
                 {"en": "Funami", "texto": "FUNAMI FM|YAKUZA"}],
     "nombres": ["Anywhere", "Funami"],
     "canciones": [{"en": "Funami", "titulo": "Flymutha", "artista": "Toys Are Real", "emisora": "Funami FM",
                    "juego": "GTA 2 (1999)", "seg": 5}],
     "planos": ["@GTA2_1999:4", "@London_1969:2", "GTA_15_07", "@GTA2_1999:2"],
     "planos_en": [{"en": "Anywhere", "plano": "@GTA2_1999"},
                   {"en": "Funami", "plano": "@GTA2_1999"}]},

    # ---------------------------------------------------------------- ACTO II · LA RADIO EN 3D (2001-2004)
    {"id": "p03", "num": 3, "total": T, "titulo": "2001 · GTA III", "capitulo": "2001 · GTA III", "overlay": "",
     "anio": 2001, "cartela": {"anio": "2001", "acto": "ACTO II", "titulo": "LA RADIO EN 3D"},
     "texto": ("En dos mil uno, la radio cambia de piel. GTA III nos saca a la calle en tres dimensiones, y sus "
               "emisoras tienen personalidad. Flashback noventa y cinco coma seis suena a la banda sonora de los "
               "ochenta. Escucha. Y de la película Scarface, esta otra. Head Radio mezcla pop y soft rock. Y Chatterbox "
               "FM es la rareza: una emisora de charla, sin música, presentada por Lazlow. Los oyentes llaman desde "
               "Liberty City y cuentan sus cosas."),
     "rotulos": [{"en": "Flashback", "texto": "FLASHBACK 95.6|OLDIES"},
                 {"en": "Scarface", "texto": "SCARFACE|BANDA SONORA"},
                 {"en": "Chatterbox", "texto": "CHATTERBOX FM|SIN MÚSICA"},
                 {"en": "Lazlow", "texto": "LAZLOW|LOCUTOR"}],
     "nombres": ["Flashback", "Scarface", "Chatterbox", "Lazlow"],
     "canciones": [{"en": "Escucha", "titulo": "Rush Rush", "artista": "Debbie Harry", "emisora": "Flashback 95.6",
                    "juego": "GTA III (2001)", "seg": 5},
                   {"en": "Scarface", "titulo": "Scarface (Push It to the Limit)", "artista": "Paul Engemann",
                    "emisora": "Flashback 95.6", "juego": "GTA III (2001); confirmada en la lista de la Definitive Edition",
                    "seg": 5}],
     "planos": ["@GTA3_2001:4", "@GTA3_DE:2", "NUEVO_Chatterbox_Cabina", "GTA_15_11", "@GTA3_2001:4"],
     "planos_en": [{"en": "Flashback", "plano": "@GTA3_2001"},
                   {"en": "Chatterbox", "plano": "NUEVO_Chatterbox_Cabina"},
                   {"en": "Scarface", "plano": "@GTA3_2001"}]},
    {"id": "p04", "num": 4, "total": T, "titulo": "2002 · VICE CITY", "capitulo": "2002 · Vice City", "overlay": "",
     "anio": 2002,
     "texto": ("En dos mil dos, Vice City se viste de ochenta. Miami, en mil novecientos ochenta y seis. Flash FM suena "
               "a pop de la época, y ahí está Billie Jean, de Michael Jackson. V-Rock, a hard rock y heavy metal. "
               "Emotion noventa y ocho coma tres, a baladas, con Africa, de Toto. Wave ciento tres, y Wildstyle. "
               "Todo con canciones reales, con licencia. Y el veintinueve de octubre de dos mil dos, Epic Records saca "
               "una caja con siete CD, uno por emisora."),
     "rotulos": [{"en": "Miami", "texto": "VICE CITY|= MIAMI"},
                 {"en": "Flash", "texto": "FLASH FM|POP DE LA ÉPOCA"},
                 {"en": "heavy", "texto": "V-ROCK|HARD ROCK Y METAL"},
                 {"en": "Emotion", "texto": "EMOTION 98.3|BALADAS"},
                 {"en": "Wildstyle", "texto": "WAVE 103 · WILDSTYLE"},
                 {"en": "Epic", "texto": "EPIC RECORDS|29 OCT 2002"},
                 {"en": "siete", "texto": "7 CD|UNO POR EMISORA"}],
     "nombres": ["Miami", "Flash", "Emotion", "Epic", "siete", "Wildstyle"],
     "canciones": [{"en": "Billie", "titulo": "Billie Jean", "artista": "Michael Jackson", "emisora": "Flash FM",
                    "juego": "GTA Vice City (2002)", "seg": 6},
                   {"en": "Africa", "titulo": "Africa", "artista": "Toto", "emisora": "Emotion 98.3",
                    "juego": "GTA Vice City (2002)", "seg": 6}],
     "planos": ["@Vice_City_2002:6", "@VC_DE:4", "NUEVO_Caja_Vice_CD", "VCA_Logo", "IMG_VC_Portada", "@Vice_City_2002:4"],
     "planos_en": [{"en": "caja", "plano": "NUEVO_Caja_Vice_CD"},
                   {"en": "Miami", "plano": "@Vice_City_2002"}]},

    # ---------------------------------------------------------------- ANUNCIOS (2001-2004)
    {"id": "p05", "num": 5, "total": T, "titulo": "2001-2004 · LOS ANUNCIOS", "capitulo": "2001-2004 · Los anuncios",
     "overlay": "", "anio": 2001, "etiqueta_linea": "2001-2004 · ANUNCIOS",
     "texto": ("Y no solo hay música. Entre canción y canción, las emisoras meten anuncios, y están escritos con mala "
               "leche. En GTA III los escribieron Dan Houser y Lazlow, que además los produjo. Son marcas inventadas que "
               "se burlan de la publicidad de la época, y algunos de Vice City usan el anticomunismo de los ochenta. En Vice City "
               "aparece el Degenatron, una parodia de las primeras "
               "consolas, y la estatua de la salvación del pastor Richards, que se ríe de los anuncios de donativos "
               "religiosos. En San Andreas, la comida rápida tiene nombre propio: Cluckin' Bell. Rockstar copió el formato "
               "de la publicidad de verdad, y llamó a publicistas para crearla. Por eso la sátira es tan exagerada, y tan "
               "exacta."),
     "rotulos": [{"en": "Houser", "texto": "DAN HOUSER|Y LAZLOW"},
                 {"en": "Degenatron", "texto": "DEGENATRON|PARODIA DE CONSOLAS"},
                 {"en": "Cluckin'", "texto": "CLUCKIN' BELL|SAN ANDREAS"}],
     "nombres": ["Houser", "Degenatron", "Cluckin'"],
     "canciones": [],
     "planos": ["@GTA3_2001:2", "@Vice_City_2002:2", "@SA_2004:2", "GTA_15_12", "@Vice_City_2002:7"],
     "planos_en": [{"en": "Houser", "plano": "@GTA3_2001"},
                   {"en": "Degenatron", "plano": "@Vice_City_2002"},
                   {"en": "Cluckin'", "plano": "@SA_2004"}]},

    # ---------------------------------------------------------------- SAN ANDREAS (2004)
    {"id": "p06", "num": 6, "total": T, "titulo": "2004 · SAN ANDREAS", "capitulo": "2004 · San Andreas", "overlay": "",
     "anio": 2004,
     "texto": ("En dos mil cuatro, San Andreas es un estado entero, con tres ciudades y muchas emisoras. Radio Los "
               "Santos pone el hip hop de la Costa Oeste, con Julio G a los mandos. Y K-DST es de rock clásico, y su DJ, "
               "Tommy The Nightmare Smith, tiene la voz de Axl Rose, de Guns N' Roses. Ahí suena Slow Ride, de Foghat. "
               "Y Green River, de Creedence Clearwater Revival. Gran parte de la música de San Andreas es con licencia, "
               "y eso tiene consecuencias. En la edición Definitive, de dos mil veintiuno, faltan algunas canciones de "
               "sus emisoras."),
     "rotulos": [{"en": "estado", "texto": "UN ESTADO|ENTERO"},
                 {"en": "Santos", "texto": "RADIO LOS SANTOS|K-DST"},
                 {"en": "Axl", "texto": "AXL ROSE|DJ DE K-DST"},
                 {"en": "consecuencias", "texto": "LICENCIAS|CANCIONES FUERA"}],
     "nombres": ["estado", "Santos", "Axl"],
     "canciones": [{"en": "Slow", "titulo": "Slow Ride", "artista": "Foghat", "emisora": "K-DST",
                    "juego": "GTA San Andreas (2004)", "seg": 5},
                   {"en": "Green", "titulo": "Green River", "artista": "Creedence Clearwater Revival",
                    "emisora": "K-DST", "juego": "GTA San Andreas (2004)", "seg": 5}],
     "planos": ["@SA_2004:4", "@SA_DE:2", "GTA_15_25", "GTA_15_26", "NUEVO_K_DST_Menu", "@SA_2004:5"],
     "planos_en": [{"en": "estado", "plano": "@SA_DE"},
                   {"en": "Axl", "plano": "NUEVO_K_DST_Menu"},
                   {"en": "consecuencias", "plano": "NUEVO_Interfaz_Trilogy"}]},

    # ---------------------------------------------------------------- PORTÁTILES (2005-2006)
    {"id": "p07", "num": 7, "total": T, "titulo": "2005-2006 · LAS PORTÁTILES", "capitulo": "2005-2006 · Las portátiles",
     "overlay": "", "anio": 2005, "etiqueta_linea": "2005-2006 · PORTÁTILES",
     "cartela": {"anio": "2005", "acto": "ACTO III", "titulo": "EN TODAS PARTES"},
     "texto": ("Mientras tanto, la radio se mete en el bolsillo. Liberty City Stories, de dos mil cinco, en la PSP, "
               "tiene diez emisoras. Lips ciento seis, Head Radio, Rise FM, The Liberty Jam o Flashback FM. Y Chatterbox "
               "vuelve, con Lazlow otra vez al micrófono. Vice City Stories, de dos mil seis, también en PSP, tiene nueve "
               "emisoras. Ahí están Flash FM, V-Rock, Wave ciento tres, Emotion noventa y ocho coma tres, y Radio "
               "Espantoso. Las dos son de la PSP, la portátil de Sony. Dos ciudades en el bolsillo, y la misma idea: que la radio "
               "nunca se calle."),
     "rotulos": [{"en": "Stories", "texto": "LIBERTY CITY STORIES|PSP · 2005"},
                 {"en": "Lips", "texto": "LIPS 106|LIBERTY CITY STORIES"},
                 {"en": "Espantoso", "texto": "RADIO ESPANTOSO|VICE CITY STORIES"}],
     "nombres": ["Stories", "Lips", "Chatterbox"],
     "canciones": [],
     "planos": ["@LCS_2005:6", "@VCS_2006:4", "@Advance_2004:2", "GTA_15_21"],
     "planos_en": [{"en": "Lips", "plano": "@LCS_2005"},
                   {"en": "Chatterbox", "plano": "@LCS_2005"},
                   {"en": "Stories", "plano": "@VCS_2006"}]},

    # ---------------------------------------------------------------- CHARLA (2004-2008)
    {"id": "p08", "num": 8, "total": T, "titulo": "2004-2008 · LAS RADIOS DE CHARLA",
     "capitulo": "2004-2008 · Las radios de charla", "overlay": "", "anio": 2004,
     "etiqueta_linea": "2004-2008 · CHARLA",
     "texto": ("Hay un nombre que aparece en varias de estas radios: Lazlow Jones. Escribió las emisoras de GTA junto a "
               "Dan Houser, desde GTA III. En GTA III es la voz de Chatterbox, la única emisora de charla de su juego. En "
               "San Andreas, Lazlow se hace cargo de Entertaining America, un programa de WCTR, la emisora de charla de "
               "la costa oeste. Antes lo presentaba Billy Dexter, hasta que lo mata en antena un personaje del juego. "
               "Y en GTA IV aparece Integrity dos punto cero, otra emisora de charla. Aquí Lazlow sale a "
               "la calle, en Algonquin, y habla con la gente que se cruza. Tres juegos, "
               "y la misma voz al micrófono."),
     "rotulos": [{"en": "WCTR", "texto": "WCTR|CHARLA DE LA COSTA OESTE"},
                 {"en": "Integrity", "texto": "INTEGRITY 2.0|GTA IV"},
                 {"en": "Lazlow", "texto": "LAZLOW JONES|VOZ DE LA SAGA"}],
     "nombres": ["Lazlow", "WCTR", "Integrity", "Algonquin"],
     "canciones": [],
     "planos": ["@SA_2004:3", "@GTA4_2008:2", "@GTA4_2008:7"],
     "planos_en": [{"en": "WCTR", "plano": "@SA_2004"},
                   {"en": "Algonquin", "plano": "@GTA4_2008"},
                   {"en": "Lazlow", "plano": "@GTA4_2008"}]},

    # ---------------------------------------------------------------- GTA IV (2008)
    {"id": "p09", "num": 9, "total": T, "titulo": "2008 · GTA IV", "capitulo": "2008 · GTA IV", "overlay": "",
     "anio": 2008,
     "texto": ("En dos mil ocho volvemos a Liberty City, y la radio cambia de tono. Aquí está Liberty Rock Radio, "
               "noventa y siete coma ocho, con rock clásico. Y su presentador es Iggy Pop. Entre canción y canción "
               "suelta su opinión sobre lo que se le ocurre. Suena Jailbreak, de Thin Lizzy. Y en Vladivostok FM suena "
               "pop de Rusia. Guarda ese nombre, porque diez años después va a ser la emisora más golpeada por las "
               "licencias."),
     "rotulos": [{"en": "Liberty", "texto": "LIBERTY ROCK RADIO|97.8"},
                 {"en": "Iggy", "texto": "IGGY POP|SE PRESENTA A SÍ MISMO"},
                 {"en": "Vladivostok", "texto": "VLADIVOSTOK FM|POP RUSO"},
                 {"en": "diez", "texto": "10 AÑOS|DESPUÉS"}],
     "nombres": ["Liberty", "Iggy", "Vladivostok", "diez"],
     "canciones": [{"en": "Suena", "titulo": "Jailbreak", "artista": "Thin Lizzy",
                    "emisora": "Liberty Rock Radio 97.8", "juego": "GTA IV (2008)", "seg": 5}],
     "planos": ["@GTA4_2008:4", "NUEVO_Iggy_Liberty_Rock", "NUEVO_Vladivostok_Menu", "@GTA4_2008:6"],
     "planos_en": [{"en": "Iggy", "plano": "NUEVO_Iggy_Liberty_Rock"},
                   {"en": "Vladivostok", "plano": "NUEVO_Vladivostok_Menu"}]},

    # ---------------------------------------------------------------- GTA V (2013)
    {"id": "p10", "num": 10, "total": T, "titulo": "2013 · GTA V", "capitulo": "2013 · GTA V", "overlay": "",
     "anio": 2013,
     "texto": ("En dos mil trece, GTA V reparte la radio entre emisoras que parecen de verdad. Non Stop Pop FM, con "
               "éxitos de pop. Los Santos Rock Radio, con Kenny Loggins como locutor, pone rock clásico. Y The Lab emite "
               "música del disco Welcome to Los Santos, producido por The Alchemist y Oh No. En Radio Mirror Park suena "
               "Sleepwalking, de The Chain Gang of mil novecientos setenta y cuatro. Cuatro emisoras, cuatro maneras de entender la ciudad."),
     "rotulos": [{"en": "Non", "texto": "NON-STOP-POP FM|POP"},
                 {"en": "Kenny", "texto": "KENNY LOGGINS|LOS SANTOS ROCK"},
                 {"en": "Lab", "texto": "THE LAB|WELCOME TO LOS SANTOS"},
                 {"en": "Sleepwalking", "texto": "SLEEPWALKING|THE CHAIN GANG OF 1974"}],
     "nombres": ["Non", "Kenny", "Lab", "Sleepwalking"],
     "canciones": [{"en": "Sleepwalking", "titulo": "Sleepwalking", "artista": "The Chain Gang of 1974",
                    "emisora": "Radio Mirror Park", "juego": "GTA V (2013)", "seg": 6}],
     "planos": ["@GTA5_2013:4", "NUEVO_Radio_Menu_GTA5", "@GTA5_2013:5"],
     "planos_en": [{"en": "Kenny", "plano": "NUEVO_Radio_Menu_GTA5"},
                   {"en": "Lab", "plano": "@GTA5_2013"},
                   {"en": "Sleepwalking", "plano": "@GTA5_2013"}]},

    # ---------------------------------------------------------------- LA RADIO QUE ELIGES (2013-2021)
    {"id": "p11", "num": 11, "total": T, "titulo": "2013-2021 · LA RADIO QUE ELIGES",
     "capitulo": "2013-2021 · La radio que eliges", "overlay": "", "anio": 2013,
     "etiqueta_linea": "2013-2021 · TU MÚSICA",
     "texto": ("Y en GTA V, la radio también puede ser tuya. FlyLo FM es la emisora de Flying Lotus, con hip hop "
               "alternativo y electrónica, y sin anuncios ni noticias. En una edición posterior sumó temas nuevos de MF DOOM "
               "y Krayzie Bone. Y si juegas en PC, puedes meter tu propia música. "
               "Se llama Self Radio: copias tus archivos MP3 en la carpeta User Music, dentro de Documentos, y el juego "
               "crea una emisora nueva con tus canciones. Hacen falta unas cuatro, como mínimo, y puedes elegir si suenan en "
               "orden, al azar o en modo radio, con charla de DJ entre canción y canción. Eso sí, esas canciones no sirven "
               "para los clips del editor de Rockstar. Ya en GTA Online, en dos mil veintiuno llega el Media Player, "
               "con música de unos soportes repartidos por Los Santos. Y en el club Music Locker, bajo el casino Diamond, "
               "suena house, disco y techno. Tú eliges qué escuchar, y la ciudad se adapta."),
     "rotulos": [{"en": "FlyLo", "texto": "FLYLO FM|FLYING LOTUS"},
                 {"en": "Self", "texto": "SELF RADIO|SOLO PC"},
                 {"en": "Media", "texto": "MEDIA PLAYER|GTA ONLINE"},
                 {"en": "Locker", "texto": "MUSIC LOCKER|CLUB"}],
     "nombres": ["FlyLo", "Self", "Media", "Locker"],
     "canciones": [],
     "planos": ["@GTA5_2013:3", "@GTA_Online:4", "@GTA_Online:10"],
     "planos_en": [{"en": "FlyLo", "plano": "@GTA5_2013"},
                   {"en": "Self", "plano": "@GTA_Online"},
                   {"en": "Locker", "plano": "@GTA_Online"}]},

    # ---------------------------------------------------------------- ACTO IV · LAS LICENCIAS (2018-2022)
    {"id": "p12", "num": 12, "total": T, "titulo": "2018 · LAS LICENCIAS", "capitulo": "2018 · Las licencias",
     "overlay": "", "anio": 2018, "etiqueta_linea": "2018 · LICENCIAS",
     "cartela": {"anio": "2018", "acto": "ACTO IV", "titulo": "LAS LICENCIAS"},
     "texto": ("Y aquí aparece el problema: las licencias caducan. En abril de dos mil dieciocho, Rockstar quita "
               "canciones de GTA IV y de sus expansiones. Lo explica en una frase: por restricciones de licencias, hay "
               "que retirar temas del juego. Vladivostok FM es la emisora más golpeada, con muchas canciones fuera y "
               "pocas sustitutas. Y en dos mil veintiuno, la Trilogy Definitive recupera GTA III, Vice City y San Andreas "
               "con gráficos nuevos. Pero las canciones que se habían perdido por el camino siguen sin estar."),
     "rotulos": [{"en": "abril", "texto": "ABR 2018|SE RETIRAN CANCIONES"},
                 {"en": "Vladivostok", "texto": "VLADIVOSTOK FM|LA MÁS AFECTADA"},
                 {"en": "Trilogy", "texto": "TRILOGY|DEFINITIVE 2021"}],
     "nombres": ["abril", "Vladivostok", "Trilogy"],
     "canciones": [],
     "planos": ["@GTA3_DE:2", "@VC_DE:2", "@VCS_2006:5"],
     "planos_en": [{"en": "Vladivostok", "plano": "@VCS_2006"},
                   {"en": "Trilogy", "plano": "@VCS_2006"}]},
    {"id": "p13", "num": 13, "total": T, "titulo": "2021-2022 · THE CONTRACT", "capitulo": "2021-2022 · The Contract",
     "overlay": "", "anio": 2021, "etiqueta_linea": "2021 · THE CONTRACT",
     "texto": ("En diciembre de dos mil veintiuno llega GTA Online: The Contract, y la radio se pone de fiesta con Dr. "
               "Dre. Radio Los Santos añade temas exclusivos de artistas como Hit-Boy o Freddie Gibbs con Pusha T. West "
               "Coast Classics dedica un especial a Dre, y ahí suena The Next Episode. La misión gira en torno a encontrar "
               "la música filtrada de Dre. Y en dos mil veintidós llega MOTOMAMI Los Santos, presentada por ROSALÍA y "
               "Arca. La radio, otra vez, es parte del juego."),
     "rotulos": [{"en": "Contract", "texto": "THE CONTRACT|DICIEMBRE 2021"},
                 {"en": "Hit-Boy", "texto": "HIT-BOY|TEMAS EXCLUSIVOS"},
                 {"en": "Next", "texto": "THE NEXT EPISODE|WEST COAST CLASSICS"},
                 {"en": "MOTOMAMI", "texto": "MOTOMAMI LOS SANTOS|ROSALÍA Y ARCA"}],
     "nombres": ["Contract", "Hit-Boy", "Dre", "MOTOMAMI"],
     "canciones": [{"en": "Next", "titulo": "The Next Episode", "artista": "Dr. Dre",
                    "emisora": "West Coast Classics", "juego": "GTA Online: The Contract (2021)", "seg": 6}],
     "planos": ["NUEVO_Dr_Dre_Estudio", "@GTA_Online:5", "@GTA_Online:6"],
     "planos_en": [{"en": "Dre", "plano": "NUEVO_Dr_Dre_Estudio"},
                   {"en": "MOTOMAMI", "plano": "@GTA_Online"}]},

    # ---------------------------------------------------------------- ACTO V · RUMBO A GTA VI (2023-2026)
    {"id": "p14", "num": 14, "total": T, "titulo": "2023 · LOS TRÁILERES", "capitulo": "2023-2026 · Los tráileres",
     "overlay": "", "anio": 2023, "cartela": {"anio": "2023", "acto": "ACTO V", "titulo": "RUMBO A GTA VI"},
     "texto": ("Y llegamos a GTA VI. En el primer tráiler, de diciembre de dos mil veintitrés, suena Love Is a Long "
               "Road, de Tom Petty. En el segundo, del seis de mayo de dos mil veinticinco, el tema principal es Hot "
               "Together, de The Pointer Sisters, un tema de los ochenta. La prensa habla de un salto enorme en las "
               "escuchas de Spotify después del tráiler."),
     "rotulos": [{"en": "Petty", "texto": "TOM PETTY|LOVE IS A LONG ROAD"},
                 {"en": "Hot", "texto": "THE POINTER SISTERS|HOT TOGETHER"},
                 {"en": "Spotify", "texto": "SPOTIFY|SUBE EN STREAMS"}],
     "nombres": ["Petty", "Hot", "Spotify"],
     "canciones": [{"en": "Love", "titulo": "Love Is a Long Road", "artista": "Tom Petty",
                    "emisora": "Ninguna (música del tráiler 1)", "juego": "GTA VI (tráiler 1, dic. 2023)", "seg": 5},
                   {"en": "Hot", "titulo": "Hot Together", "artista": "The Pointer Sisters",
                    "emisora": "Ninguna (música del tráiler 2)", "juego": "GTA VI (tráiler 2, 6 may. 2025)", "seg": 5}],
     "planos": ["T1_Playa_Aerea", "T1_Neones", "T1_Autopista", "T1_Coches_Noche", "T2_Jason_Tejado", "T2_Cayos_Aereo", "T2_Autopista", "@Vice_City:4", "@GTA6_T2:3"],
     "planos_en": [{"en": "Petty", "plano": "T1_Playa_Aerea"},
                   {"en": "Hot", "plano": "T2_Jason_Tejado"},
                   {"en": "Spotify", "plano": "T2_Autopista"}]},
    {"id": "p15", "num": 15, "total": T, "titulo": "2026 · LAS RADIOS DE GTA VI",
     "capitulo": "2026 · Las radios de GTA VI", "overlay": "", "anio": 2026, "etiqueta_linea": "2026 · GTA VI",
     "texto": ("Y ahora, las radios de GTA VI, lo que se sabe hasta ahora. Según la prensa especializada, en octubre de "
               "dos mil veintiséis se mostraron seis emisoras: Flash FM, que vuelve de Vice City; The Chamber; Cocoteo "
               "FM; Dirty South Classics; AfroBank FM; y Back Country Radio. Se habla de más emisoras, pero no hay una "
               "lista confirmada. Lo que sí sabemos es que el diecinueve de noviembre las podremos escuchar en el juego."),
     "rotulos": [{"en": "seis", "texto": "6 EMISORAS|SEGÚN PRENSA"},
                 {"en": "Flash", "texto": "FLASH FM|VUELVE DE VICE CITY"},
                 {"en": "Chamber", "texto": "THE CHAMBER|EMISORA"},
                 {"en": "Cocoteo", "texto": "COCOTEO FM · DIRTY SOUTH|AFROBANK · BACK COUNTRY"},
                 {"en": "diecinueve", "texto": "19 NOV 2026"}],
     "nombres": ["seis", "Flash", "Chamber", "diecinueve", "Cocoteo"],
     "canciones": [],
     "planos": ["NUEVO_Rueda_Radio_GTA6", "VL_Fecha", "@GTA5_2013:2", "NUEVO_Pantalla_Emisoras", "@GTA6_Mirada:2"],
     "planos_en": [{"en": "emisoras", "plano": "NUEVO_Pantalla_Emisoras"},
                   {"en": "Flash", "plano": "NUEVO_Rueda_Radio_GTA6"},
                   {"en": "diecinueve", "plano": "VL_Fecha"}]},

    # ---------------------------------------------------------------- CIERRE
    {"id": "cierre", "num": None, "titulo": "", "overlay": "", "capitulo": "De 1997 a 2026", "anio": 2026,
     "texto": ("Veintinueve años de radios: de Craig Conner a Dr. Dre, de Iggy Pop a Lazlow. Y te toca a ti. ¿Cuál es "
               "tu radio favorita de GTA? ¿Liberty Rock, Flash FM o Chatterbox? Déjamela en los comentarios, que quiero "
               "ver cuál gana. Si te ha gustado, suscríbete, que el diecinueve de noviembre vamos a estar aquí. Nos vemos "
               "en Leónida."),
     "rotulos": [{"en": "favorita", "texto": "¿CUÁL ES|TU RADIO?"},
                 {"en": "Veintinueve", "texto": "1997 → 2026"}],
     "nombres": ["favorita", "Veintinueve"],
     "canciones": [],
     "planos": ["Mirada_Skyline_Noche", "Lanz_Paseo", "VL_Atardecer_Final", "VL_Lancha_Pareja", "Mirada_Terraza", "Portada_Animada", "@Vice_City:3"],
     "planos_en": [{"en": "favorita", "plano": "@GTA6_Mirada"},
                   {"en": "Veintinueve", "plano": "Mirada_Skyline_Noche"}]},
]

for _b in BLOQUES:
    _b["voz"] = _voz(_b["texto"])
