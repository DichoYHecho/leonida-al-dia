"""Guion del vídeo largo 2 de «Leónida al Día»: «Toda la historia de Vice City desde 2002 hasta GTA 6».

Mismo formato que guion_vl.py (se elige con GUION=guion_vc). Claves nuevas, opcionales:
  total     -> número total del contador (18 en vez de 20)
  capitulo  -> texto del capítulo en capitulos.txt (si no, el título en minúsculas)
  rotulos   -> datos grandes en el centro: {"en": palabra que dice la voz, "n": vez que sale, "texto": "LÍNEA 1|LÍNEA 2"}
  cta       -> cartel de «Suscríbete» durante ese bloque
Con sonido original de los tráileres (pedido por mí, aunque sus canciones tienen derechos).
Planos de Vice City 2002 (VCA_..., VCC_...) en trozos_vc.csv, de los vídeos oficiales de Rockstar.
"""

# Vídeos oficiales de Rockstar de Vice City (rockstargames.com/videos/tror41c2 y /videos/ao1c441c)
VIDEOS_EXTRA = {
    "VC_Aniv": "https://videos-rockstargames-com.akamaized.net/v4/tror41c2/flv/en-us-720p.mp4",
    "VC_Comp": "https://videos-rockstargames-com.akamaized.net/v4/ao1c441c/flv/en-us-1080p60.mp4",
    "VC_Tril": "https://videos-rockstargames-com.akamaized.net/v4/8ta2r546/flv/en-us-1080p60.mp4",
}
from fuentes_vc import FUENTES as _FUENTES  # noqa: E402  (tráileres y gameplays de archivo de cada juego)

VIDEOS_EXTRA.update({k: v["url"] for k, v in _FUENTES.items() if k not in VIDEOS_EXTRA})

# Logos y carteles que van quietos (sin movimiento de cámara)
PLANOS_FIJOS = {"VCA_Logo", "GTA_15_01", "GTA_15_02", "GTA_15_15", "VC02_Trailer3_02", "VC02_Trailer3_15", "IMG_GTA1", "IMG_GTA1_Caja", "IMG_RaceNChase", "VCA_Welcome", "VCA_Welcome_Son", "VCA_Aniversario", "VCA_Rockstar_North", "Mirada_Logo",
                "VL_Fecha", "VL_Rotulo_PS5", "Portada_Animada", "Lanz_Final_19N", "T1_Letras_Vice"}

# Música: el estilo cambia al empezar estos bloques (4 estilos, ver ESTILOS_MUSICA en montaje.py)
MUSICA = {"hook": 0, "p03": 1, "p07": 0, "p11": 2, "p13": 3, "p16": 1, "e1": 2, "cierre": 3}

T = 18

BLOQUES = [
    {"id": "hook", "num": None, "titulo": "", "overlay": "",
     "rotulos": [{"t": 0.0, "dur": 2.6, "negro": True, "texto": "DE 2002|A 2026"}],
     "texto": ("El 8 de noviembre de 2002 llegó a las tiendas de España un juego con camisas hawaianas, neón y música "
               "de los ochenta. Se llamaba Vice City. Veinticuatro años después, el 19 de noviembre, Rockstar nos "
               "devuelve allí con GTA 6. Pero Vice City no nació en 2002. Nació cinco años antes, vista desde arriba, "
               "en un juego en el que al principio... ibas a ser policía. Hoy te cuento la historia entera de Vice City "
               "en 18 paradas: de 1997 a GTA 6, lo que vuelve, lo que cambia, y el guiño a Tommy Vercetti que Rockstar "
               "ha metido en las reservas. Arrancamos."),
     "voz": ("El 8 de noviembre de 2002 llegó a las tiendas de España un juego con camisas hawaianas, neón y música "
             "de los ochenta. Se llamaba Vice City. Veinticuatro años después, el 19 de noviembre, Rockstar nos "
             "devuelve allí con GTA 6. Pero Vice City no nació en 2002. Nació cinco años antes, vista desde arriba, "
             "en un juego en el que al principio... ibas a ser policía. Hoy te cuento la historia entera de Vice City "
             "en 18 paradas: de 1997 a GTA 6, lo que vuelve, lo que cambia, y el guiño a Tomi Verchéti que Rockstar "
             "ha metido en las reservas. Arrancamos."),
     "planos": ["VCA_Logo", "VCA_Tommy_Yate", "VCC_Moto_Orig", "VCA_Lanchas", "Lanz_Playa", "T1_Neones", "Mirada_Vista_Aerea", "T1_Letras_Vice", "VL_Poli_2", "Lanz_Descapotable", "Mirada_Skyline_Noche", "T1_Coches_Noche", "Mirada_Descapotable_1", "T1_Autopista", "VC02_Trailer3_09", "GTA_15_16"],
     "planos_en": [{"en": "vice", "plano": "VCA_Logo"},
                   {"en": "policía", "plano": "IMG_RaceNChase"},
                   {"en": "guiño", "plano": "VCA_Tommy_Yate"}],
     "original": "VCA_Welcome_Son"},

    # ---------------------------------------------------------------- A. 1997 · EL ORIGEN
    {"id": "p01", "num": 1, "total": T, "titulo": "1995 · IBAS A SER POLICÍA", "capitulo": "Ibas a ser policía",
     "overlay": "",
     "texto": ("Parada número uno. 1995. Dundee, Escocia. Un estudio llamado DMA Design empieza un juego que se llama "
               "Race'n'Chase. Tú eres un policía que persigue a criminales. ¿El problema? Que era un rollo. Así que le "
               "dieron la vuelta: ahora el criminal eres tú. Y ese cambio de idea es, literalmente, el origen de Grand "
               "Theft Auto."),
     "voz": ("Parada número uno. 1995. Dandí, Escocia. Un estudio llamado De Eme A Disáin empieza un juego que se "
             "llama Reis an Cheis. Tú eres un policía que persigue a criminales. ¿El problema? Que era un rollo. Así "
             "que le dieron la vuelta: ahora el criminal eres tú. Y ese cambio de idea es, literalmente, el origen de "
             "Grand Theft Auto."),
     "rotulos": [{"en": "estudio", "texto": "RACE'N'CHASE|1995 · DUNDEE"},
                 {"en": "vuelta", "texto": "AHORA EL CRIMINAL|ERES TÚ"}],
     "planos": ["GTA_15_01", "GTA_15_05", "IMG_RaceNChase", "GTA_15_06", "GTA_15_02", "IMG_GTA1"],
     "planos_en": [{"en": "persigue", "plano": "IMG_RaceNChase"},
                   {"en": "vuelta", "plano": "GTA_15_05"},
                   {"en": "origen", "plano": "GTA_15_01"}]},
    {"id": "p02", "num": 2, "total": T, "titulo": "1997 · VISTA DESDE ARRIBA", "capitulo": "Vice City, vista desde arriba",
     "overlay": "",
     "texto": ("Parada dos. 1997. El primer GTA sale en noviembre en Europa, con la cámara mirando desde el cielo y "
               "tres ciudades: Liberty City, que es Nueva York; San Andreas, que es San Francisco; y Vice City, que es "
               "Miami. Seis niveles en total: dos por ciudad. Ahí está: la primera Vice City de la historia. Cuatro píxeles. Y antes de salir ya montó "
               "polémica: se habló de prohibirlo, en Brasil lo prohibieron, y el publicista Max Clifford usó todo ese "
               "escándalo como publicidad gratis. ¿Funcionó? En 1999 ya iba por tres millones y medio. Y en 2001, por seis millones. Nada mal para un juego en el que los coches eran rectángulos vistos desde un helicóptero."),
     "voz": ("Parada dos. 1997. El primer GTA sale en noviembre en Europa, con la cámara mirando desde el cielo y "
             "tres ciudades: Líberti Siti, que es Nueva York; San Andreas, que es San Francisco; y Vice City, que es "
             "Miami. Seis niveles en total: dos por ciudad. Ahí está: la primera Vice City de la historia. Cuatro píxeles. Y antes de salir ya montó "
             "polémica: se habló de prohibirlo, en Brasil lo prohibieron, y el publicista Max Clífor usó todo ese "
             "escándalo como publicidad gratis. ¿Funcionó? En 1999 ya iba por tres millones y medio. Y en 2001, por seis millones. Nada mal para un juego en el que los coches eran rectángulos vistos desde un helicóptero."),
     "rotulos": [{"en": "nueva", "texto": "LIBERTY CITY|= NUEVA YORK"},
                 {"en": "francisco", "texto": "SAN ANDREAS|= SAN FRANCISCO"},
                 {"en": "miami", "texto": "VICE CITY|= MIAMI"},
                 {"en": "millones", "texto": "3,5 MILLONES|EN 1999"},
                 {"en": "2001", "texto": "6 MILLONES|EN 2001"}],
     "planos": ["GTA_15_06", "GTA_15_05", "IMG_GTA1", "GTA_15_02", "IMG_GTA1_Caja", "GTA_15_08"],
     "planos_en": [{"en": "cielo", "plano": "GTA_15_06"},
                   {"en": "polémica", "plano": "IMG_GTA1_Caja"}]},

    # ---------------------------------------------------------------- B. 2002 · VICE CITY
    {"id": "p03", "num": 3, "total": T, "titulo": "2002 · DIECIOCHO MESES", "capitulo": "Dieciocho meses",
     "overlay": "",
     "texto": ("Parada tres. Y ahora, sí: 2002. Rockstar viene de petarlo con GTA 3 y anuncia Vice City en el E3, el "
               "22 de mayo. Lo hace un equipo de unas 50 personas en dieciocho meses. Cuesta unos cinco millones de "
               "dólares... y en publicidad se gastan más del doble: trece. Sale el 29 de octubre en Estados Unidos y "
               "el 8 de noviembre aquí, y eso que se retrasó una semana para tener copias suficientes. Solo en PlayStation 2. Los de PC, a esperar hasta mayo de 2003."),
     "voz": ("Parada tres. Y ahora, sí: 2002. Rockstar viene de petarlo con GTA 3 y anuncia Vice City en el E tres, el "
             "22 de mayo. Lo hace un equipo de unas 50 personas en dieciocho meses. Cuesta unos cinco millones de "
             "dólares... y en publicidad se gastan más del doble: trece. Sale el 29 de octubre en Estados Unidos y "
             "el 8 de noviembre aquí, y eso que se retrasó una semana para tener copias suficientes. Solo en PlayStation 2. Los de PC, a esperar hasta mayo de 2003."),
     "rotulos": [{"en": "dieciocho", "texto": "18 MESES|~50 PERSONAS"},
                 {"en": "cinco", "texto": "5 MILLONES $|DESARROLLO"},
                 {"en": "trece", "texto": "13 MILLONES $|PUBLICIDAD"},
                 {"en": "aquí", "texto": "8 NOV 2002|EUROPA · PS2"}],
     "planos": ["GTA_15_15", "VC02_Trailer3_02", "@Vice_City_2002", "VCA_Rockstar_North", "VCA_Logo", "VCA_Coche_Aeropuerto", "VCC_Bahia_Orig", "VCA_Moto_Atardecer", "VCA_Tommy_Yate", "VCC_Moto_Orig", "VCA_Barco"],
     "planos_en": [{"en": "anuncia", "plano": "VC02_Trailer3_02"},
                   {"en": "dieciocho", "plano": "VCA_Rockstar_North"},
                   {"en": "aquí", "plano": "GTA_15_15"},
                   {"en": "playstation", "plano": "@Vice_City_2002"}]},
    {"id": "p04", "num": 4, "total": T, "titulo": "UNA PELI DE LOS OCHENTA", "capitulo": "Una peli de los ochenta",
     "overlay": "",
     "texto": ("Parada cuatro. Vice City no pasa en 2002: pasa en 1986. Y Rockstar no lo escondió. Las referencias son "
               "El precio del poder, Atrapado por su pasado y la serie Corrupción en Miami. Y hasta El padrino se cuela en algunos personajes. El Malibu Club, por "
               "ejemplo, está sacado de un sitio de El precio del poder. Es como si alguien hubiera metido los ochenta "
               "enteros en un disco... y le hubiera dado una camisa hawaiana."),
     "voz": ("Parada cuatro. Vice City no pasa en 2002: pasa en 1986. Y Rockstar no lo escondió. Las referencias son "
             "El precio del poder, Atrapado por su pasado y la serie Corrupción en Miami. Y hasta El padrino se cuela en algunos personajes. El Malibú Club, por "
             "ejemplo, está sacado de un sitio de El precio del poder. Es como si alguien hubiera metido los ochenta "
             "enteros en un disco... y le hubiera dado una camisa hawaiana."),
     "rotulos": [{"en": "pasa", "n": 2, "texto": "1986|"},
                 {"en": "precio", "texto": "EL PRECIO DEL PODER|1983"},
                 {"en": "atrapado", "texto": "ATRAPADO POR SU PASADO|1993"},
                 {"en": "serie", "texto": "CORRUPCIÓN EN MIAMI|1984-1989"}],
     "planos": ["@Vice_City_2002", "VCA_Diner", "VCA_Tommy_Yate_2", "VCA_Despacho", "VCA_Mesa", "VCA_Coches_Noche", "VCA_Salon", "VCA_Lanchas", "VCA_Tommy_Bar", "@VC_DE"],
     "planos_en": [{"en": "pasa", "plano": "VCC_Moto_Orig", "n": 2},
                   {"en": "precio", "plano": "VCA_Despacho"},
                   {"en": "camisa", "plano": "VCA_Tommy_Yate"}]},
    {"id": "p05", "num": 5, "total": T, "titulo": "TOMMY VERCETTI", "capitulo": "Tommy Vercetti", "overlay": "",
     "texto": ("Parada cinco. El protagonista: Tommy Vercetti. Se come quince años de cárcel por culpa de su jefe, "
               "Sonny Forelli, y nada más salir lo mandan a Vice City a hacer negocios con droga. El primer trato sale "
               "fatal: emboscada, y adiós dinero y mercancía. A Tommy le puso la voz Ray Liotta, el de Uno de los "
               "nuestros. Ganó un premio a la mejor interpretación por este papel, y cuando murió, en mayo de 2022, "
               "Rockstar lo despidió como la voz icónica de Tommy Vercetti."),
     "voz": ("Parada cinco. El protagonista: Tomi Verchéti. Se come quince años de cárcel por culpa de su jefe, "
             "Soni Forelli, y nada más salir lo mandan a Vice City a hacer negocios con droga. El primer trato sale "
             "fatal: emboscada, y adiós dinero y mercancía. A Tomi le puso la voz Rei Lióta, el de Uno de los "
             "nuestros. Ganó un premio a la mejor interpretación por este papel, y cuando murió, en mayo de 2022, "
             "Rockstar lo despidió como la voz icónica de Tomi Verchéti."),
     "rotulos": [{"en": "quince", "texto": "15 AÑOS|DE CÁRCEL"},
                 {"en": "emboscada", "texto": "EMBOSCADA|EN EL PRIMER TRATO"},
                 {"en": "voz", "texto": "RAY LIOTTA|LA VOZ DE TOMMY"}],
     "planos": ["@Vice_City_2002", "VCC_Tommy_Lance_Orig", "VCA_Tommy_Silla", "VCA_Barco", "VCA_Tiroteo", "VCA_Tommy_Bar", "VCA_Helicoptero", "VCA_Tommy_Yate", "VCA_Calle", "@VC_DE"],
     "planos_en": [{"en": "protagonista", "plano": "VC02_Trailer3_09"},
                   {"en": "quince", "plano": "VCA_Tommy_Silla"},
                   {"en": "emboscada", "plano": "VC02_Trailer3_07"},
                   {"en": "voz", "plano": "VCT_Tommy_Esmoquin"},
                   {"en": "despidió", "plano": "VCT_Tommy_Moto"}]},
    {"id": "p06", "num": 6, "total": T, "titulo": "UN REPARTO DE CINE", "capitulo": "Un reparto de cine", "overlay": "",
     "texto": ("Parada seis. Y Liotta no vino solo. En el reparto están Burt Reynolds, Tom Sizemore, Luis Guzmán, "
               "Danny Dyer... Pero el detalle bueno es este: Lance Vance, el socio de Tommy, lo dobla Philip Michael "
               "Thomas. ¿Te suena? Era Tubbs, el compañero de Crockett en Corrupción en Miami. O sea: Rockstar fichó a "
               "un poli de la serie de Miami... para hacer de mafioso en su Miami. Entre todos grabaron unas ocho mil frases de diálogo. Más ochentero, imposible."),
     "voz": ("Parada seis. Y Lióta no vino solo. En el reparto están Bert Rénolds, Tom Sáismor, Luis Guzmán, "
             "Dani Dáier... Pero el detalle bueno es este: Lans Vans, el socio de Tomi, lo dobla Fílip Máikel "
             "Tómas. ¿Te suena? Era Tabs, el compañero de Crókett en Corrupción en Miami. O sea: Rockstar fichó a "
             "un poli de la serie de Miami... para hacer de mafioso en su Miami. Entre todos grabaron unas ocho mil frases de diálogo. Más ochentero, imposible."),
     "rotulos": [{"en": "reparto", "texto": "BURT REYNOLDS · TOM SIZEMORE|LUIS GUZMÁN · DANNY DYER"},
                 {"en": "dobla", "texto": "LANCE VANCE|= PHILIP MICHAEL THOMAS"},
                 {"en": "compañero", "texto": "TUBBS|CORRUPCIÓN EN MIAMI"}],
     "planos": ["@Vice_City_2002", "VCA_Tommy_Lance", "VCC_Tommy_Lance_Orig", "VCA_Trio", "VCA_Mesa", "VCC_Tommy_Lance_DE", "VCA_Diner", "VCA_Tommy_Yate_2", "@VC_DE"],
     "planos_en": [{"en": "reparto", "plano": "VCT_Rosenberg"},
                   {"en": "socio", "plano": "GTA_15_18"},
                   {"en": "compañero", "plano": "GTA_15_17"},
                   {"en": "mafioso", "plano": "VCC_Tommy_Lance_DE"}]},
    {"id": "p07", "num": 7, "total": T, "titulo": "EL MAPA DE 1986", "capitulo": "El mapa de 1986", "overlay": "",
     "texto": ("Parada siete. El mapa. Dos islas grandes y unas cuantas pequeñas, casi el doble que la Liberty City de "
               "GTA 3. Al principio no puedes cruzar: los puentes están cerrados porque se acerca un huracán, Hermione. "
               "Al este, la playa: Ocean Beach, que es South Beach. En medio, Starfish Island, la copia de Star Island, "
               "la isla de las mansiones: una de ellas acabará siendo la mansión Vercetti. Y tu primera casa es el Ocean View Hotel, en Ocean Drive. Quédate con esos "
               "nombres... porque vuelven."),
     "voz": ("Parada siete. El mapa. Dos islas grandes y unas cuantas pequeñas, casi el doble que la Líberti Siti de "
             "GTA 3. Al principio no puedes cruzar: los puentes están cerrados porque se acerca un huracán, Hermáioni. "
             "Al este, la playa: Óushen Bich, que es Sauz Bich. En medio, Stárfish Áiland, la copia de Star Áiland, "
             "la isla de las mansiones: una de ellas acabará siendo la mansión Verchéti. Y tu primera casa es el Óushen Viu Hotel, en Óushen Dráiv. Quédate con esos "
             "nombres... porque vuelven."),
     "rotulos": [{"en": "doble", "texto": "x2|LA LIBERTY CITY DE GTA 3"},
                 {"en": "huracán", "texto": "HURACÁN HERMIONE|PUENTES CERRADOS"},
                 {"en": "playa", "texto": "OCEAN BEACH|= SOUTH BEACH"},
                 {"en": "medio", "texto": "STARFISH ISLAND|= STAR ISLAND"},
                 {"en": "primera", "texto": "OCEAN VIEW HOTEL|TU PRIMERA CASA"}],
     "planos": ["@Vice_City_2002", "VCC_Bahia_Orig", "VCC_Moto_Orig", "VCA_Moto_Atardecer", "VCA_Coche_Aeropuerto", "VCA_Calle", "VCA_Coches_Noche", "VCA_Barco", "VCA_Lanchas", "@VC_DE"],
     "planos_en": [{"en": "islas", "plano": "@VC_DE"},
                   {"en": "playa", "plano": "VCC_Bahia_Orig"},
                   {"en": "medio", "plano": "VCA_Despacho"},
                   {"en": "primera", "plano": "VCC_Moto_Orig"}]},
    {"id": "p08", "num": 8, "total": T, "titulo": "NUEVE HORAS DE RADIO", "capitulo": "Nueve horas de radio",
     "overlay": "",
     "texto": ("Parada ocho. Si Vice City es famoso por algo, es por la radio. Más de 113 canciones y anuncios: unas "
               "nueve horas de música. Tanta, que Epic Records sacó una caja con siete discos. En Emotion 98.3 suena "
               "Crockett's Theme, la de Corrupción en Miami. Y hay el triple de radio hablada que en GTA 3. Gente "
               "pasándose de rosca en directo, durante horas. Un clásico."),
     "voz": ("Parada ocho. Si Vice City es famoso por algo, es por la radio. Más de ciento trece canciones y anuncios: "
             "unas nueve horas de música. Tanta, que Épic Récords sacó una caja con siete discos. En Imóushon noventa "
             "y ocho punto tres suena Crókets Zim, la de Corrupción en Miami. Y hay el triple de radio hablada que en "
             "GTA 3. Gente pasándose de rosca en directo, durante horas. Un clásico."),
     "rotulos": [{"en": "canciones", "texto": "+113|CANCIONES Y ANUNCIOS"},
                 {"en": "nueve", "texto": "9 HORAS|DE MÚSICA"},
                 {"en": "caja", "texto": "7 DISCOS|EPIC RECORDS"},
                 {"en": "suena", "texto": "EMOTION 98.3|CROCKETT'S THEME"},
                 {"en": "triple", "texto": "x3|RADIO HABLADA"}],
     "planos": ["@Vice_City_2002", "VCA_Moto_Atardecer", "VCC_Moto_Orig", "VCA_Coches_Noche", "VCA_Diner", "VCA_Coche_Aeropuerto", "VCA_Calle", "VCC_Bahia_Orig", "@VC_DE"],
     "planos_en": [{"en": "radio", "plano": "VCA_Coches_Noche"},
                   {"en": "caja", "plano": "VCA_Moto_Atardecer"}]},
    {"id": "p09", "num": 9, "total": T, "titulo": "EL DUEÑO DE LA CIUDAD", "capitulo": "El dueño de la ciudad",
     "overlay": "", "cta": True,
     "texto": ("Parada nueve. Y luego está lo de comprar la ciudad. Pisos para guardar coches y partidas, pero también "
               "negocios: un estudio de cine, una empresa de taxis, clubes... Haces sus misiones y empiezan a darte "
               "dinero. Pasas de recadero a dueño. Y esa idea, la de montar tu imperio, vuelve con más fuerza dentro de "
               "dos paradas."),
     "rotulos": [{"en": "estudio", "texto": "ESTUDIO DE CINE|TAXIS · CLUBES"},
                 {"en": "recadero", "texto": "DE RECADERO|A DUEÑO"}],
     "planos": ["@Vice_City_2002", "VCA_Estudio_1", "VCA_Estudio_2", "VCA_Tommy_Silla", "VCA_Despacho", "VCA_Salon", "VCA_Mesa", "VCA_Tommy_Bar", "@VC_DE"],
     "planos_en": [{"en": "comprar", "plano": "VCA_Despacho"},
                   {"en": "estudio", "plano": "VCA_Estudio_1"},
                   {"en": "dueño", "plano": "VCA_Tommy_Silla"}]},
    {"id": "p10", "num": 10, "total": T, "titulo": "EL RÉCORD", "capitulo": "El récord", "overlay": "",
     "texto": ("Parada diez. ¿Y cómo le fue? Medio millón de copias en 24 horas. Un millón cuatrocientas mil en dos "
               "días: el juego que más rápido se había vendido hasta entonces. Fue el más vendido de 2002 en Estados "
               "Unidos, y en 2008 ya iba por diecisiete millones y medio. Solo en PlayStation 2, más de catorce millones. Nota en Metacritic: 95. Seis premios BAFTA "
               "y el Golden Joystick al juego del año. Vamos, que no salió mal."),
     "voz": ("Parada diez. ¿Y cómo le fue? Medio millón de copias en 24 horas. Un millón cuatrocientas mil en dos "
             "días: el juego que más rápido se había vendido hasta entonces. Fue el más vendido de 2002 en Estados "
             "Unidos, y en 2008 ya iba por diecisiete millones y medio. Solo en PlayStation 2, más de catorce millones. Nota en Metacrític: noventa y cinco. Seis "
             "premios Bafta y el Goulden Yóistik al juego del año. Vamos, que no salió mal."),
     "rotulos": [{"en": "medio", "texto": "500.000|EN 24 HORAS"},
                 {"en": "cuatrocientas", "texto": "1,4 MILLONES|EN 2 DÍAS"},
                 {"en": "diecisiete", "texto": "17,5 MILLONES|EN 2008"},
                 {"en": "catorce", "texto": "14,2 MILLONES|SOLO EN PS2"},
                 {"en": "nota", "texto": "95|METACRITIC"},
                 {"en": "seis", "texto": "6 PREMIOS|BAFTA"}],
     "planos": ["@Vice_City_2002", "VCA_Logo", "VCA_Trio", "VCA_Lanchas", "VCA_Helicoptero", "VCA_Grua", "VCA_Tiroteo", "VCA_Welcome", "@VC_DE"],
     "planos_en": [{"en": "medio", "plano": "VCA_Logo"},
                   {"en": "nota", "plano": "GTA_15_15"},
                   {"en": "seis", "plano": "VCA_Trio"}]},

    # ---------------------------------------------------------------- C. 2006 · VICE CITY STORIES
    {"id": "p11", "num": 11, "total": T, "titulo": "2006 · EL HERMANO DE LA EMBOSCADA",
     "capitulo": "El hermano que muere al principio", "overlay": "",
     "texto": ("Parada once. 2006. Rockstar vuelve a Vice City... en una PSP. Vice City Stories pasa en 1984, dos años "
               "antes, y su protagonista es Victor Vance, Vic, un exsoldado. Y aquí viene lo curioso: Vic sale en el "
               "Vice City original... pero poco. Es el hermano de Lance que cae en la emboscada del primer trato. O "
               "sea: le dieron un juego entero al tío al que en el otro no le da tiempo ni a saludar. Y sí: aquí "
               "montas tu imperio, negocio a negocio. Y en la PSP podías jugar con hasta cinco amigos más."),
     "voz": ("Parada once. 2006. Rockstar vuelve a Vice City... en una pe ese pe. Vice City Stóris pasa en 1984, dos "
             "años antes, y su protagonista es Víctor Vans, Vic, un exsoldado. Y aquí viene lo curioso: Vic sale en el "
             "Vice City original... pero poco. Es el hermano de Lans que cae en la emboscada del primer trato. O "
             "sea: le dieron un juego entero al tío al que en el otro no le da tiempo ni a saludar. Y sí: aquí "
             "montas tu imperio, negocio a negocio. Y en la pe ese pe podías jugar con hasta cinco amigos más."),
     "rotulos": [{"en": "vuelve", "texto": "VICE CITY STORIES|2006 · PSP"},
                 {"en": "protagonista", "texto": "VICTOR VANCE|1984"},
                 {"en": "emboscada", "texto": "EL HERMANO|DE LA EMBOSCADA"}],
     "planos": ["IMG_VCS_Portada", "@VCS_2006", "@VCS_2006"],
     "planos_en": [{"en": "vuelve", "plano": "IMG_VCS_Portada"},
                   {"en": "protagonista", "plano": "@VCS_2006"},
                   {"en": "emboscada", "plano": "VCA_Tiroteo"},
                   {"en": "imperio", "plano": "@VCS_2006"}]},
    {"id": "p12", "num": 12, "total": T, "titulo": "PHIL COLLINS EN VICE CITY", "capitulo": "Phil Collins en Vice City",
     "overlay": "",
     "texto": ("Parada doce. Y el cameo más ochentero de toda la saga: Phil Collins. Él mismo, haciendo de él mismo. En "
               "una misión tienes que protegerle de unos sicarios, antes y durante su concierto en Vice City. Vice City "
               "Stories acabó vendiendo más de siete millones. Y trajo algo que Tommy nunca tuvo: Vic sabe nadar. En el original, caer al agua era morir. Además, podías hacer de socorrista en la playa. Y quédate también con este nombre, Phil Collins, porque "
               "en la parada diecisiete... reaparece."),
     "voz": ("Parada doce. Y el cameo más ochentero de toda la saga: Fil Colins. Él mismo, haciendo de él mismo. En "
             "una misión tienes que protegerle de unos sicarios, antes y durante su concierto en Vice City. Vice City "
             "Stóris acabó vendiendo más de siete millones. Y trajo algo que Tomi nunca tuvo: Vic sabe nadar. En el original, caer al agua era morir. Además, podías hacer de socorrista en la playa. Y quédate también con este nombre, Fil Colins, porque "
             "en la parada diecisiete... reaparece."),
     "rotulos": [{"en": "cameo", "texto": "PHIL COLLINS|COMO ÉL MISMO"},
                 {"en": "concierto", "texto": "UN CONCIERTO|CON SICARIOS"},
                 {"en": "siete", "texto": "+7 MILLONES|VICE CITY STORIES"},
                 {"en": "nadar", "texto": "VIC SÍ SABE NADAR|Y HACE DE SOCORRISTA"}],
     "planos": ["IMG_VCS_Portada", "@VCS_2006", "@VCS_2006"],
     "planos_en": [{"en": "cameo", "plano": "IMG_VCS_Portada"},
                   {"en": "nadar", "plano": "VCS_MotoAgua_01"},
                   {"en": "socorrista", "plano": "@VCS_2006"}]},

    # ---------------------------------------------------------------- D. 2023-2026 · LEONIDA
    {"id": "p13", "num": 13, "total": T, "titulo": "2023 · LA VUELTA", "capitulo": "La vuelta", "overlay": "",
     "texto": ("Parada trece. Diecisiete años sin un Vice City nuevo... hasta 2023. El 5 de diciembre llega el primer "
               "tráiler de GTA 6, el que se coló antes de tiempo, que ya te contamos en el otro vídeo. Suena Tom Petty, "
               "Love Is a Long Road, de 1989. Y Rockstar lo resume en una frase que sigue en su web: Vice City, USA. "
               "El lado más oscuro del lugar más soleado de América. Volvemos."),
     "voz": ("Parada trece. Diecisiete años sin un Vice City nuevo... hasta 2023. El 5 de diciembre llega el primer "
             "tráiler de GTA 6, el que se coló antes de tiempo, que ya te contamos en el otro vídeo. Suena Tom Péti, "
             "Lov is a long róud, de 1989. Y Rockstar lo resume en una frase que sigue en su web: Vice City, Estados "
             "Unidos. El lado más oscuro del lugar más soleado de América. Volvemos."),
     "rotulos": [{"en": "diciembre", "texto": "5 DIC 2023|TRÁILER 1"},
                 {"en": "suena", "texto": "TOM PETTY|LOVE IS A LONG ROAD (1989)"},
                 {"en": "oscuro", "dur": 3.6, "texto": "THE DARKEST SIDE OF|THE SUNNIEST PLACE IN AMERICA"}],
     "planos": ["T1_Autopista", "T1_Playa_Aerea", "T1_Humedal", "T1_Lancha_Rapida", "T1_Coches_Noche", "T1_Camioneta",
                "T1_Noche_Aerea", "T1_Neones", "T1_Letras_Vice"],
     "original": "T1_Musica_Petty"},
    {"id": "p14", "num": 14, "total": T, "titulo": "DE CIUDAD A ESTADO", "capitulo": "De ciudad a estado",
     "overlay": "",
     "texto": ("Parada catorce. En 2002, Vice City era todo el juego. En GTA 6 es solo una parte. Ahora hay un estado "
               "entero: Leonida. Los cayos de Leonida, al sur; Grassrivers, el pantano de los caimanes, que Rockstar llama la joya indomable de Leonida; Port "
               "Gellhorn, la costa olvidada; Ambrosia, con su refinería de azúcar; y el monte Kalaga, al norte. Y las descripciones de Rockstar son oro: en los manglares de Grassrivers hay descubrimientos todavía más raros que los caimanes, y en los bosques del monte Kalaga viven, cito, místicos paletos y radicales paranoicos. Es la "
               "Florida de Rockstar. Y Vice City deja de ser el mapa... para ser la capital del vicio."),
     "voz": ("Parada catorce. En 2002, Vice City era todo el juego. En GTA 6 es solo una parte. Ahora hay un estado "
             "entero: Leonida. Los cayos de Leonida, al sur; Grasríver, el pantano de los caimanes, que Rockstar llama la joya indomable de Leonida; Port "
             "Guélhorn, la costa olvidada; Ambrosia, con su refinería de azúcar; y el monte Kalaga, al norte. Y las descripciones de Rockstar son oro: en los manglares de Grasríver hay descubrimientos todavía más raros que los caimanes, y en los bosques del monte Kalaga viven, cito, místicos paletos y radicales paranoicos. Es la "
             "Florida de Rockstar. Y Vice City deja de ser el mapa... para ser la capital del vicio."),
     "rotulos": [{"en": "cayos", "texto": "LEONIDA KEYS|"},
                 {"en": "pantano", "texto": "GRASSRIVERS|"},
                 {"en": "costa", "texto": "PORT GELLHORN|"},
                 {"en": "refinería", "texto": "AMBROSIA|"},
                 {"en": "monte", "texto": "MOUNT KALAGA|"},
                 {"en": "místicos", "texto": "«MÍSTICOS PALETOS Y|RADICALES PARANOICOS»"}],
     "planos": ["Mirada_Vista_Aerea", "T1_Puente_Cayos", "T2_Cayos_Aereo", "Lanz_Cartel_Keys", "T1_Humedal",
                "Mirada_Hidrodeslizador", "T2_Casa_Pilotes", "Mirada_Motocross", "Lanz_Marina", "Mirada_Atardecer"]},
    {"id": "p15", "num": 15, "total": T, "titulo": "OCEAN BEACH VUELVE", "capitulo": "Ocean Beach vuelve",
     "overlay": "",
     "texto": ("Parada quince. ¿Te acuerdas de los nombres de la parada siete? Rockstar describe en su web Ocean Beach, "
               "con hoteles art déco de colores pastel y arena blanquísima. El mismo nombre que en 2002. Hay un barrio "
               "cubano, Little Cuba, con sus panaderías, que recuerda al Little Havana del original. Y el puerto, que "
               "Rockstar llama la capital mundial de los cruceros. Y un mercadillo, el Tisha-Wocka, lleno de marcas piratas. Hasta en las reservas lo nombran: un garaje en "
               "Shore Court, a tiro de piedra de Ocean Beach."),
     "voz": ("Parada quince. ¿Te acuerdas de los nombres de la parada siete? Rockstar describe en su web Óushen Bich, "
             "con hoteles art déco de colores pastel y arena blanquísima. El mismo nombre que en 2002. Hay un barrio "
             "cubano, Lítel Cuba, con sus panaderías, que recuerda al Lítel Havana del original. Y el puerto, que "
             "Rockstar llama la capital mundial de los cruceros. Y un mercadillo, el Tisha Uóka, lleno de marcas piratas. Hasta en las reservas lo nombran: un garaje en "
             "Shor Cort, a tiro de piedra de Óushen Bich."),
     "rotulos": [{"en": "describe", "texto": "OCEAN BEACH|MISMO NOMBRE QUE EN 2002"},
                 {"en": "cubano", "texto": "LITTLE CUBA|"},
                 {"en": "cruceros", "texto": "VC PORT|CAPITAL DE LOS CRUCEROS"},
                 {"en": "mercadillo", "texto": "TISHA-WOCKA|MARCAS PIRATAS"},
                 {"en": "garaje", "texto": "SHORE COURT|JUNTO A OCEAN BEACH"}],
     "planos": ["Mirada_Playa", "Lanz_Playa", "T1_Playa_Aerea", "T2_Gimnasio_Playa", "Mirada_Descapotable_2",
                "Mirada_Puerto", "T1_Lancha_Rapida", "Mirada_Kayak"]},
    {"id": "p16", "num": 16, "total": T, "titulo": "EL GUIÑO A TOMMY", "capitulo": "El guiño a Tommy", "overlay": "",
     "texto": ("Parada dieciséis. Y ahora, el guiño gordo. El regalo por reservar GTA 6 se llama Vintage Vice City "
               "Pack. Y dentro hay un estampado para las armas inspirado... en la camisa de palmeras de Tommy Vercetti. "
               "Rockstar lo llama, tal cual, el capo original. Pero hay más: en la Ultimate Edition vienen dos "
               "revólveres sacados de la mansión Vercetti, y un Grotti Cheetah del 95 que Rockstar llama una oda a "
               "Shore Drive. Y hasta un taller para tunear coches en Vice City: Rideout Customs. ¿Sale Tommy en GTA 6? Eso Rockstar no lo ha dicho. Pero su camisa, sí."),
     "voz": ("Parada dieciséis. Y ahora, el guiño gordo. El regalo por reservar GTA 6 se llama Víntach Vice City "
             "Pak. Y dentro hay un estampado para las armas inspirado... en la camisa de palmeras de Tomi Verchéti. "
             "Rockstar lo llama, tal cual, el capo original. Pero hay más: en la Áltimet Edíshon vienen dos "
             "revólveres sacados de la mansión Verchéti, y un Grotti Chíta del 95 que Rockstar llama una oda a "
             "Shor Dráiv. Y hasta un taller para tunear coches en Vice City: Ráidaut Cástoms. ¿Sale Tomi en GTA 6? Eso Rockstar no lo ha dicho. Pero su camisa, sí."),
     "rotulos": [{"en": "regalo", "texto": "VINTAGE VICE CITY PACK|REGALO DE RESERVA"},
                 {"en": "camisa", "texto": "LA CAMISA DE PALMERAS|DE TOMMY VERCETTI"},
                 {"en": "capo", "texto": "«EL CAPO ORIGINAL»|"},
                 {"en": "mansión", "texto": "REVÓLVERES|DE LA MANSIÓN VERCETTI"},
                 {"en": "oda", "texto": "GROTTI CHEETAH '95|«UNA ODA A SHORE DRIVE»"},
                 {"en": "taller", "texto": "RIDEOUT CUSTOMS|TALLER EN VICE CITY"}],
     "planos": ["Portada_Animada", "Lanz_Descapotable", "Mirada_Coche_Clasico", "T1_Neones", "Mirada_Terraza",
                "Lanz_Balcon", "Mirada_Logo"],
     "planos_en": [{"en": "camisa", "plano": "VC02_Trailer3_09"},
                   {"en": "mansión", "plano": "VCA_Despacho"}]},
    {"id": "p17", "num": 17, "total": T, "titulo": "LOS OCHENTA SIGUEN SONANDO",
     "capitulo": "Los ochenta siguen sonando", "overlay": "",
     "texto": ("Parada diecisiete. La música. El segundo tráiler, de mayo de 2025, va con Hot Together, de las Pointer "
               "Sisters. ¿De qué año es? De 1986. El mismo año en el que pasa Vice City. Casualidad... o no. Y en la "
               "mirada extendida de agosto, la de Netflix, suena Depeche Mode, People Are People; Def Leppard, Love Bites, "
               "de 1988... y Phil Collins, Against All Odds. Sí: el mismo Phil Collins al que protegías en Vice City Stories. Y hay más clásicos: Cliff Richard, Devil Woman, o los Bellamy Brothers, Let Your Love Flow. La lista parece la emisora Emotion 98.3."),
     "voz": ("Parada diecisiete. La música. El segundo tráiler, de mayo de 2025, va con Jot Tuguéder, de las Póinter "
             "Sísters. ¿De qué año es? De 1986. El mismo año en el que pasa Vice City. Casualidad... o no. Y en la "
             "mirada extendida de agosto, la de Netflix, suena Depésh Mod, Pípol ar Pípol; Def Lépard, Lov Báits, "
             "de 1988... y Fil Colins, Eguénst ol Ods. Sí: el mismo Fil Colins al que protegías en Vice City Stóris. Y hay más clásicos: Cliff Ríchard, Dévil Gúman, o los Bélami Bráders, Let Yur Lov Flóu. La lista parece la emisora Imóushon noventa y ocho punto tres."),
     "rotulos": [{"en": "segundo", "texto": "HOT TOGETHER|POINTER SISTERS · 1986"},
                 {"en": "mismo", "texto": "VICE CITY|TAMBIÉN 1986"},
                 {"en": "netflix", "texto": "DEPECHE MODE|PEOPLE ARE PEOPLE"},
                 {"en": "protegías", "texto": "PHIL COLLINS|AGAINST ALL ODDS"},
                 {"en": "clásicos", "texto": "CLIFF RICHARD|BELLAMY BROTHERS"}],
     "planos": ["T2_Mar_Atardecer", "T2_Muelle_Atardecer", "T2_Jason_Conduce", "Mirada_Azotea", "VL_Disco_2",
                "Mirada_Jason_y_Lucia", "VL_Interior_1", "T2_Autopista"],
     "planos_en": [{"en": "protegías", "plano": "@VCS_2006"}],
     "original": "T2_Musica_Hot"},
    {"id": "p18", "num": 18, "total": T, "titulo": "LO QUE CAMBIA", "capitulo": "Lo que cambia", "overlay": "",
     "texto": ("Parada dieciocho. ¿Y qué cambia? Lo primero, la época: de 1986 a hoy, con móviles y redes sociales. Lo "
               "segundo, los protagonistas: Tommy iba solo; ahora son dos, Jason y Lucía. Y lo tercero, la escala: en "
               "2002, Vice City era una ciudad de algo más de cuatro kilómetros cuadrados en una PS2. En 2026 es la "
               "capital de un estado entero, en PS5 y Xbox Series. Y la radio: de las nueve horas de música de 2002 a los pódcast a la carta de GTA 6. Y el dinero: Vice City costó unos cinco millones; lo que ha costado GTA 6, Rockstar no lo ha dicho. Lo que no cambia: el neón, las palmeras... y que en "
               "Vice City nadie es del todo inocente."),
     "voz": ("Parada dieciocho. ¿Y qué cambia? Lo primero, la época: de 1986 a hoy, con móviles y redes sociales. Lo "
             "segundo, los protagonistas: Tomi iba solo; ahora son dos, Yéison y Lucía. Y lo tercero, la escala: en "
             "2002, Vice City era una ciudad de algo más de cuatro kilómetros cuadrados en una pe ese dos. En 2026 es "
             "la capital de un estado entero, en pe ese cinco y Xbox Series. Y la radio: de las nueve horas de música de 2002 a los pódcast a la carta de GTA 6. Y el dinero: Vice City costó unos cinco millones; lo que ha costado GTA 6, Rockstar no lo ha dicho. Lo que no cambia: el neón, las "
             "palmeras... y que en Vice City nadie es del todo inocente."),
     "rotulos": [{"en": "época", "texto": "DE 1986|A HOY"},
                 {"en": "protagonistas", "texto": "DE TOMMY|A JASON Y LUCÍA"},
                 {"en": "escala", "texto": "DE PS2|A PS5 Y XBOX SERIES"}],
     "planos": ["VCC_Moto_Orig", "Mirada_Jason_y_Lucia", "VCA_Tommy_Yate", "Lanz_Paseo", "VCC_Bahia_Orig",
                "Mirada_Skyline_Noche", "Lanz_Balcon", "Mirada_Atardecer", "T1_Neones"],
     "planos_en": [{"en": "protagonistas", "plano": "VCT_Tommy_Moto"},
                   {"en": "dos", "plano": "Mirada_Jason_y_Lucia"}]},

    # ---------------------------------------------------------------- TRES EXTRA DE REGALO
    {"id": "e1", "num": "E1", "total": 3, "titulo": "VICE CITY NUNCA SE FUE", "overlay": "",
     "texto": ("Y antes de cerrar, como has llegado hasta aquí, tres extra de regalo. Extra uno: Vice City nunca se fue "
               "del todo. Por su décimo aniversario, en diciembre de 2012, Rockstar lo sacó para móviles, con este "
               "tráiler que estás viendo. Y en 2021 llegó la Definitive Edition, con los gráficos rehechos. Mira: así "
               "era en 2002... y así quedó en la remasterización. Las mismas palmeras, veinte años después. Y en diciembre de 2023 esa remasterización llegó también a los móviles. Por cierto, las versiones para móvil de 2012 no las hizo Rockstar North, sino el estudio War Drum."),
     "voz": ("Y antes de cerrar, como has llegado hasta aquí, tres extra de regalo. Extra uno: Vice City nunca se fue "
             "del todo. Por su décimo aniversario, en diciembre de 2012, Rockstar lo sacó para móviles, con este "
             "tráiler que estás viendo. Y en 2021 llegó la Définitiv Edíshon, con los gráficos rehechos. Mira: así "
             "era en 2002... y así quedó en la remasterización. Las mismas palmeras, veinte años después. Y en diciembre de 2023 esa remasterización llegó también a los móviles. Por cierto, las versiones para móvil de 2012 no las hizo Rockstar North, sino el estudio Uor Drum."),
     "rotulos": [{"en": "aniversario", "texto": "10.º ANIVERSARIO|MÓVILES · DIC 2012"},
                 {"en": "gráficos", "texto": "DEFINITIVE EDITION|2021"},
                 {"en": "mira", "texto": "2002|ORIGINAL"},
                 {"en": "remasterización", "texto": "2021|REMASTERIZADO"}],
     "planos": ["VCA_Aniversario", "VCA_Welcome", "VCA_Trio", "VCA_Logo", "VCC_Bahia_Orig", "VCC_Bahia_DE",
                "VCC_Moto_Orig", "VCC_Moto_DE"]},
    {"id": "e2", "num": "E2", "total": 3, "titulo": "LOS FANS QUE LO DESMONTARON", "overlay": "",
     "texto": ("Extra dos: los fans que desmontaron Vice City. Un grupo de programadores reconstruyó el código de GTA 3 "
               "y de Vice City pieza a pieza, para que funcionaran en más sitios, como la Switch o la Vita. Su proyecto no llevaba ni gráficos ni sonidos de Rockstar: hacía falta "
               "tener tu propia copia del juego, pero a Take-Two no le hizo ni pizca de gracia: en 2021 denunció a "
               "catorce de ellos en California. En 2023, según NME, acabaron pactando. Moraleja: en Vice City, el código ni tocarlo."),
     "voz": ("Extra dos: los fans que desmontaron Vice City. Un grupo de programadores reconstruyó el código de GTA 3 "
             "y de Vice City pieza a pieza, para que funcionaran en más sitios, como la Suich o la Vita. Su proyecto no llevaba ni gráficos ni sonidos de Rockstar: hacía falta "
             "tener tu propia copia del juego, pero a Teik Tú no le hizo ni pizca de gracia: en 2021 denunció a "
             "catorce de ellos en California. En 2023, según Ene Eme E, acabaron pactando. Moraleja: en Vice City, el código ni tocarlo."),
     "rotulos": [{"en": "código", "texto": "RE3 Y REVC|EL CÓDIGO, PIEZA A PIEZA"},
                 {"en": "sitios", "texto": "SWITCH · WII U · VITA|"},
                 {"en": "catorce", "texto": "14 PROGRAMADORES|DEMANDADOS EN 2021"}],
     "planos": ["VCC_Tommy_Lance_Orig", "VCA_Despacho", "VCA_Tommy_Silla", "VCA_Tommy_Bar", "VCA_Tiroteo",
                "VCA_Helicoptero", "VCA_Calle"],
     "planos_en": [{"en": "código", "plano": "VCC_Tommy_Lance_Orig"}]},
    {"id": "e3", "num": "E3", "total": 3, "titulo": "MURALES DE VERDAD", "overlay": "",
     "texto": ("Extra tres: murales de verdad. Según la revista Dazed, Rockstar contó con más de cincuenta artistas "
               "callejeros reales para pintar los murales de GTA 6, en sitios como el Stockyard de Vice City, inspirado "
               "en el barrio de Wynwood de Miami. O sea, que el grafiti que vas a ver mientras huyes de la policía... lo "
               "ha pintado alguien de verdad. Y no es casualidad: Wynwood es famoso en Miami justo por sus murales al aire libre."),
     "voz": ("Extra tres: murales de verdad. Según la revista Déizd, Rockstar contó con más de cincuenta artistas "
             "callejeros reales para pintar los murales de GTA 6, en sitios como el Stokiard de Vice City, inspirado "
             "en el barrio de Güínwud de Miami. O sea, que el grafiti que vas a ver mientras huyes de la policía... lo "
             "ha pintado alguien de verdad. Y no es casualidad: Güínwud es famoso en Miami justo por sus murales al aire libre."),
     "rotulos": [{"en": "cincuenta", "texto": "+50 ARTISTAS|CALLEJEROS REALES"},
                 {"en": "barrio", "texto": "STOCKYARD|= WYNWOOD, MIAMI"}],
     "planos": ["VL_Mural", "Mirada_Calles_1", "Mirada_Calles_2", "Mirada_Camiones", "Mirada_Moto_Calle",
                "Mirada_Coche_Clasico", "Mirada_Jason_Calle"]},

    # ---------------------------------------------------------------- FINAL
    {"id": "cierre", "num": None, "titulo": "", "overlay": "", "capitulo": "Lo que Rockstar aún no ha dicho",
     "texto": ("Y para acabar, lo que todavía no sabemos. ¿Vuelve el Ocean View Hotel? Los fans creen haberlo visto en "
               "un tráiler, pero Rockstar no lo ha confirmado. ¿Vuelven Tommy, Lance o algún personaje del original? "
               "Ni una palabra. Lo que sí sabemos es la fecha: el 19 de noviembre volvemos a Vice City. Veinticuatro "
               "años después. Y si no puedes esperar: la predescarga empieza el 10 de noviembre. Y si jugaste al de 2002, cuéntame en los comentarios cuál era tu emisora: ¿Flash FM, Wave 103 o Emotion? Si te ha gustado el viaje, suscríbete, y si te perdiste las 20 curiosidades de GTA 6, "
               "tienes el vídeo aquí. Nos vemos en Leonida."),
     "voz": ("Y para acabar, lo que todavía no sabemos. ¿Vuelve el Óushen Viu Hotel? Los fans creen haberlo visto en "
             "un tráiler, pero Rockstar no lo ha confirmado. ¿Vuelven Tomi, Lans o algún personaje del original? "
             "Ni una palabra. Lo que sí sabemos es la fecha: el 19 de noviembre volvemos a Vice City. Veinticuatro "
             "años después. Y si no puedes esperar: la predescarga empieza el 10 de noviembre. Y si jugaste al de 2002, cuéntame en los comentarios cuál era tu emisora: ¿Flash Efe Eme, Uéiv ciento tres o Imóushon? Si te ha gustado el viaje, suscríbete, y si te perdiste las 20 curiosidades de GTA 6, "
             "tienes el vídeo aquí. Nos vemos en Leonida."),
     "rotulos": [{"en": "hotel", "texto": "¿OCEAN VIEW HOTEL?|SIN CONFIRMAR"},
                 {"en": "palabra", "texto": "¿VUELVE ALGUIEN?|NI UNA PALABRA"},
                 {"en": "fecha", "texto": "19 NOV|VOLVEMOS A VICE CITY"},
                 {"en": "predescarga", "texto": "PREDESCARGA|10 NOV"}],
     "planos": ["VL_Hidroavion", "VL_Atardecer_Final", "VL_Lancha_Pareja", "Mirada_Paracaidas", "Lanz_Paseo",
                "Mirada_Logo", "VL_Fecha"],
     "planos_en": [{"en": "vuelven", "plano": "VCA_Tommy_Yate"},
                   {"en": "hotel", "plano": "VCC_Moto_Orig"}],
     "original": "Lanz_Final_19N"},
]
