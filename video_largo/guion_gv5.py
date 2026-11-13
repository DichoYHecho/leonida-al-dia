"""Guion del vídeo 9 «GTA V: el juego que hizo esperar a GTA VI» de «Leónida al Día» (se publica el 19-21 nov 2026,
el día del lanzamiento de GTA VI).

Mismo formato que guion_rad.py. Datos y fuentes con fecha: video_gtav\\investigacion.md. Planos nuevos: trozos_810_gv5.csv.

Versión 2 (12 nov 2026, coordinador): reescrito tras el informe de revisor-guion. Guinness ya con fuente primaria
(guinnessworldrecords.com, 8 oct 2013 y 2023); sold-in según el glosario de Take-Two; gasto recurrente con la definición
del glosario; 230 M de agosto 2026 corroborada por dos fuentes; primera persona de 2014 (GameSpot, nov 2014).
Fuera: la cifra de copias del primer día de Guinness (Take-Two no la confirmó) y el total de la saga.

Ángulo: GTA V como vara de medir de GTA VI. Sin mecánicas (vídeo 8), sin GTA Online a fondo (vídeo 10), sin repetir
por qué GTA VI tardó trece años (vídeo 5) y sin polémicas. No se predicen ventas de GTA VI.
Sin deícticos que fallen si se publica el 19, el 20 o el 21.
"""
import re

VIDEOS_EXTRA = {}
RECORTES = {}
MARCO = True

PLANOS_FIJOS = {"N9_Captura_GameInformer_Records", "N9_Captura_MCV_45M", "N9_Captura_Transcripcion_Sold_In",
                "N9_Captura_Webull_230_Agosto", "N9_Logo_GTA5", "NUEVO_Reediciones_Logos",
                "NUEVO_Cuentas_TakeTwo", "NUEVO_Zelnick_Captura", "NUEVO_Estanteria_Tienda", "VL_Fecha"}

# Música: sin pistas con licencia; solo música de fondo generada en el montaje
MUSICA = {"hook": "synthwave", "p01": "chiptune", "p04": "breakbeat", "p07": "hiphop", "p10": "synthwave",
          "cierre": "synthwave"}

# Línea de tiempo de abajo
LINEA_ANIMADA = True
LINEA = [(2013, "GTA V"), (2014, "PS4 · ONE"), (2015, "PC"), (2022, "PS5 · SERIES"), (2026, "GTA VI")]

# Pronunciación para la voz: cada valor es UNA palabra
FONETICA = {
    "III": "3", "IV": "4", "V": "5", "VI": "6", "Guinness": "Guínes", "World": "Uórld", "Records": "Rékords",
    "Take-Two": "Teik-Tu", "Strauss": "Estráus", "Zelnick": "Zélnik", "sold-in": "sóldin",
    "PlayStation": "Pléistéishon", "Xbox": "Ékbox", "One": "Uan", "Series": "Síries", "PC": "Pe-Ce",
    "MCV": "Eme-Ce-Uve", "Online": "Onlain", "Red": "Red", "Dead": "Ded", "Redemption": "Redémpshon",
    "Rockstar": "Rókstar", "Metacritic": "Metacrític", "Los": "Los", "Santos": "Sántos", "streamers": "estrímers",
    "Twitch": "Tuich", "StreamElements": "Estrímélements",
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
     "texto": ("Ochocientos quince millones de dólares en un solo día. No es la taquilla de una película: es lo que "
               "ingresó GTA V en dos mil trece, según Guinness. Trece años después, el diecinueve de noviembre, llega "
               "GTA VI, y todo el mundo lo va a comparar con ese listón. Así que vamos a medir el listón. Qué récords "
               "batió GTA V, qué cifras ha dado Take-Two y qué significa de verdad cada una. Porque no todas miden lo "
               "mismo."),
     "rotulos": [{"t": 0.0, "dur": 2.4, "negro": True, "texto": "2013|→ 2026"},
                 {"en": "Ochocientos", "texto": "815,7 M $|EN UN DÍA"},
                 {"en": "diecinueve", "texto": "19 NOV 2026|LLEGA GTA VI"}],
     "nombres": ["Ochocientos"],
     "canciones": [],
     "planos": ["N9_Logo_GTA5", "@GTA5_2013:4", "@Historia_GTA:2", "@GTA6_Mirada:2"],
     "planos_en": [{"en": "Ochocientos", "plano": "N9_Logo_GTA5"},
                   {"en": "diecinueve", "plano": "@GTA6_Mirada"}]},

    # ---------------------------------------------------------------- ACTO I · EL LANZAMIENTO (2013)
    {"id": "p01", "num": 1, "total": T, "titulo": "2013 · EL LANZAMIENTO", "capitulo": "2013 · El lanzamiento",
     "overlay": "", "anio": 2013, "cartela": {"anio": "2013", "acto": "ACTO I", "titulo": "EL LANZAMIENTO"},
     "texto": ("El diecisiete de septiembre de dos mil trece, GTA V sale a la venta en PlayStation tres y Xbox "
               "trescientos sesenta. Llega al final de aquella generación de consolas, cuando muchos ya miraban a la "
               "siguiente. Y aun así se lleva todos los focos. La crítica se rinde: en Metacritic tiene un noventa y "
               "siete en las dos consolas, con más de cien reseñas entre ambas. Es la misma nota que GTA III y solo un "
               "punto menos que GTA IV, el mejor valorado de la saga. Pero lo que convirtió a GTA V en la vara de medir "
               "no fueron las notas. Fueron las cifras de su primera semana. Y alguien las estaba apuntando."),
     "rotulos": [{"en": "diecisiete", "texto": "17 SEP 2013|PS3 · XBOX 360"},
                 {"en": "Metacritic", "texto": "METACRITIC|97 / 100"}],
     "nombres": ["Metacritic"],
     "canciones": [],
     "planos": ["@GTA5_2013:4", "@GTA5_Oficial_810:3", "@GTA_Online:2", "@Historia_GTA:2"],
     "planos_en": [{"en": "Metacritic", "plano": "@GTA5_2013"}]},
    {"id": "p02", "num": 2, "total": T, "titulo": "2013 · SIETE RÉCORDS", "capitulo": "2013 · Siete récords",
     "overlay": "", "anio": 2013,
     "texto": ("El ocho de octubre, Guinness World Records lo confirma por escrito. Su titular habla de seis récords "
               "de ventas. Entre ellos, el videojuego más vendido en veinticuatro horas, el que más dinero ingresa en "
               "un día y el producto de entretenimiento que más rápido llega a los mil millones de dólares. Ojo a eso "
               "último: ahí ya no compite con videojuegos, compite con películas y con discos. Y hay un séptimo récord "
               "que va aparte, porque ni siquiera es de ventas: el tráiler de acción y aventura más visto. Antes de "
               "salir, GTA V ya batía marcas solo con enseñarse."),
     "rotulos": [{"en": "Guinness", "texto": "GUINNESS WORLD RECORDS|8 OCT 2013"},
                 {"en": "séptimo", "texto": "6 DE VENTAS|+ 1 DE TRÁILER"}],
     "nombres": ["Guinness"],
     "canciones": [],
     "planos": ["N9_Captura_GameInformer_Records", "@GTA5_2013:3", "@GTA6_Mirada:3", "@Historia_GTA:2"],
     "planos_en": [{"en": "Guinness", "plano": "N9_Captura_GameInformer_Records"}]},
    {"id": "p03", "num": 3, "total": T, "titulo": "2013 · MIL MILLONES EN TRES DÍAS", "capitulo": "2013 · Mil millones en tres días",
     "overlay": "", "anio": 2013,
     "texto": ("Las cifras: ochocientos quince coma siete millones de dólares el primer día, según Guinness. Y mil "
               "millones en tres días, algo que Take-Two ya había anunciado el veinte de septiembre con un titular que "
               "no necesitaba adjetivos. Tres días. El juego salió un martes: no le dio tiempo ni a llegar al primer fin "
               "de semana. Eso sí, esto son dólares, no jugadores. Guinness publicó también una cifra de copias del "
               "primer día, pero, según la prensa de entonces, Take-Two no la confirmó, así que aquí no la vamos a repetir. Una cifra sin nadie que "
               "la firme se queda fuera, por bonita que sea."),
     "rotulos": [{"en": "ochocientos", "texto": "815,7 M $|PRIMER DÍA"},
                 {"en": "tres", "texto": "1.000 M $|EN TRES DÍAS"},
                 {"en": "Take-Two", "texto": "TAKE-TWO|20 SEP 2013"}],
     "nombres": ["Take-Two"],
     "canciones": [],
     "planos": ["@GTA5_2013:3", "@Historia_GTA:2", "@GTA_Online:2", "@GTA6_Mirada:2"],
     "planos_en": [{"en": "Take-Two", "plano": "@Historia_GTA"}]},

    # ---------------------------------------------------------------- ACTO II · TRES GENERACIONES (2014-2022)
    {"id": "p04", "num": 4, "total": T, "titulo": "2014 · EL SALTO", "capitulo": "2014-2015 · El salto",
     "overlay": "", "anio": 2014, "etiqueta_linea": "2014 · PS4 · ONE",
     "cartela": {"anio": "2014", "acto": "ACTO II", "titulo": "TRES GENERACIONES"},
     "texto": ("Y entonces GTA V hace algo raro: se niega a jubilarse. El dieciocho de noviembre de dos mil catorce "
               "sale en PlayStation cuatro y Xbox One. Más tráfico, más detalle, más distancia de dibujado. Y una "
               "novedad que pocos esperaban: la vista en primera persona, a pie y en los coches. El catorce de abril de "
               "dos mil quince llega a PC, después de varios retrasos. El mismo Los Santos, visto de cerca por primera "
               "vez. Y la crítica vuelve a aplaudir: noventa y siete en PlayStation cuatro y noventa y seis en PC, según "
               "Metacritic. Para mucha gente fue la segunda compra del mismo juego. Para Take-Two, el principio de una vida muy "
               "larga."),
     "rotulos": [{"en": "dieciocho", "texto": "18 NOV 2014|PS4 · XBOX ONE"},
                 {"en": "primera", "texto": "PRIMERA PERSONA|NOVEDAD DE 2014"},
                 {"en": "PC", "texto": "PC|14 ABR 2015"}],
     "nombres": ["PC"],
     "canciones": [],
     "planos": ["@GTA5_2013:4", "@GTA5_Oficial_810:3", "@GTA4_2008:2", "@GTA6_Mirada:2"],
     "planos_en": [{"en": "PC", "plano": "@GTA5_2013"},
                   {"en": "primera", "plano": "@GTA5_Oficial_810"}]},
    {"id": "p05", "num": 5, "total": T, "titulo": "2015 · CUARENTA Y CINCO MILLONES", "capitulo": "2015 · 45 millones",
     "overlay": "", "anio": 2015, "etiqueta_linea": "2015 · PC",
     "texto": ("En febrero de dos mil quince, Take-Two da una cifra que ya asusta: más de cuarenta y cinco millones de "
               "copias de GTA V enviadas a las tiendas, según recogió la revista MCV. Enviadas, que no es lo mismo que "
               "vendidas. Es como cuando te mandan diez pizzas a casa: eso no significa que te las hayas comido. Y el "
               "matiz importa, porque Take-Two sigue contando así hoy, con una palabra en inglés que veremos más "
               "adelante. Lo único seguro es que la cifra no ha parado de crecer desde entonces."),
     "rotulos": [{"en": "cuarenta", "texto": "MÁS DE 45 M|ENVIADAS · FEB 2015"},
                 {"en": "MCV", "texto": "MCV|FEBRERO 2015"},
                 {"en": "pizzas", "texto": "ENVIADAS|≠ VENDIDAS"}],
     "nombres": ["MCV"],
     "canciones": [],
     "planos": ["N9_Captura_MCV_45M", "NUEVO_Estanteria_Tienda", "@GTA5_2013:3", "NUEVO_Captura_Steam_Resenas",
                "@GTA_Online:2", "@Historia_GTA:2"],
     "planos_en": [{"en": "MCV", "plano": "N9_Captura_MCV_45M"},
                   {"en": "pizzas", "plano": "NUEVO_Estanteria_Tienda"}]},
    {"id": "p06", "num": 6, "total": T, "titulo": "2022 · LA TERCERA GENERACIÓN", "capitulo": "2022 · La tercera generación",
     "overlay": "", "anio": 2022, "etiqueta_linea": "2022 · PS5 · SERIES",
     "texto": ("El quince de marzo de dos mil veintidós llega la tercera: PlayStation cinco y Xbox Series. Un mismo "
               "juego en tres generaciones de consolas, de la PlayStation tres a la cinco. En esta saga lo normal era lo "
               "contrario: cada GTA cambiaba de ciudad, de época y de protagonista. GTA V se quedó. Eso sí, esta vez la "
               "crítica fue más fría: ochenta y uno en PlayStation cinco y setenta y nueve en Xbox Series. Competir "
               "contra tu propio noventa y siete es lo que tiene. Y la pregunta que se "
               "hacía mucha gente aquel año era sencilla: ¿y el seis, para cuándo? Faltaban todavía más de cuatro años y "
               "medio. Mientras tanto, el cinco seguía vendiendo como si nada."),
     "rotulos": [{"en": "ochenta", "texto": "METACRITIC|PS5 81 · SERIES 79"},
                 {"en": "quince", "texto": "15 MAR 2022|PS5 · XBOX SERIES"},
                 {"en": "generaciones", "texto": "3 GENERACIONES|PS3 → PS5"}],
     "nombres": ["generaciones"],
     "canciones": [],
     "planos": ["NUEVO_Reediciones_Logos", "@GTA5_2013:3", "@GTA5_Oficial_810:4", "@GTA6_Mirada:2", "@GTA4_2008:1"],
     "planos_en": [{"en": "generaciones", "plano": "NUEVO_Reediciones_Logos"}]},

    # ---------------------------------------------------------------- ACTO III · EL JUEGO QUE NO SE ACABA
    {"id": "p07", "num": 7, "total": T, "titulo": "2013 · GTA ONLINE", "capitulo": "2013 · GTA Online",
     "overlay": "", "anio": 2013, "etiqueta_linea": "2013 · ONLINE",
     "cartela": {"anio": "2013", "acto": "ACTO III", "titulo": "EL JUEGO QUE NO SE ACABA"},
     "texto": ("Volvamos un momento a dos mil trece. El uno de octubre, dos semanas después del juego, Rockstar abre "
               "GTA Online. Le dedicaremos su propio vídeo, así que aquí solo importa una idea económica. GTA V dejó de "
               "ser un producto que se compra una vez. Se convirtió en un sitio al que la gente vuelve. Y cada vuelta "
               "puede traer una compra: un coche, un negocio, una ampliación. Y el online viaja con el juego: cuando GTA V "
               "da el salto a la nueva generación en dos mil catorce, la primera persona llega también a GTA Online. "
               "Es la diferencia entre vender una entrada y montar el parque de atracciones entero."),
     "rotulos": [{"en": "Online", "texto": "GTA ONLINE|1 OCT 2013"}],
     "nombres": ["Online"],
     "canciones": [],
     "planos": ["@GTA_Online:5", "@GTA5_2013:2", "@GTA5_Oficial_810:3"],
     "planos_en": [{"en": "Online", "plano": "@GTA_Online"}]},
    {"id": "p08", "num": 8, "total": T, "titulo": "2026 · EL GASTO RECURRENTE", "capitulo": "2026 · El gasto recurrente",
     "overlay": "", "anio": 2026,
     "texto": ("Take-Two tiene un nombre para eso: gasto recurrente de los consumidores. En su glosario lo define como "
               "el dinero que entra por moneda virtual, contenido adicional, compras dentro del juego y publicidad. En "
               "su año fiscal dos mil veintiséis, que cerró en marzo, ese gasto supuso el setenta y ocho por ciento de "
               "sus reservas netas. Ojo: es la cifra de toda la empresa, no solo de GTA. Pero ayuda a entender por qué "
               "un juego de dos mil trece sigue saliendo en las presentaciones de resultados de dos mil veintiséis. La "
               "caja del primer día fue solo la entrada."),
     "rotulos": [{"en": "glosario", "texto": "GASTO RECURRENTE|MONEDA · CONTENIDO · COMPRAS"},
                 {"en": "setenta", "texto": "78 %|DE LAS RESERVAS NETAS"},
                 {"en": "Take-Two", "texto": "TAKE-TWO|AÑO FISCAL 2026"}],
     "nombres": ["Take-Two"],
     "canciones": [],
     "planos": ["NUEVO_Cuentas_TakeTwo", "@GTA_Online:3", "@GTA5_2013:2", "@GTA6_Mirada:2"],
     "planos_en": [{"en": "Take-Two", "plano": "NUEVO_Cuentas_TakeTwo"},
                   {"en": "setenta", "plano": "@GTA_Online"}]},

    {"id": "p09", "num": 9, "total": T, "titulo": "2023-2024 · EL JUEGO QUE SE VE", "capitulo": "2023-2024 · El juego que se ve",
     "overlay": "", "anio": 2024,
     "texto": ("Y hay otra forma de seguir vivo: que te miren. GTA V no se ha ido nunca de las plataformas de directos. "
               "Según datos de terceros, de la empresa StreamElements, fue el segundo juego más visto en Twitch en dos "
               "mil veintitrés y el primero en dos mil veinticuatro. Once años después de salir, era lo que más se "
               "veía. Buena parte de ese tirón viene del rol: servidores donde la gente interpreta a un personaje "
               "durante horas, con sus propias normas, sus policías y sus atracos. Tanto pesa, que en noviembre de dos mil "
               "veintiséis Take-Two contó que se podían ganar objetos exclusivos de GTA Online viendo a ciertos "
               "streamers de rol en Twitch. Gente viendo a otra gente pararse en los semáforos de Los Santos. Eso no "
               "venía en la caja."),
     "rotulos": [{"en": "Twitch", "texto": "TWITCH|2.º EN 2023 · 1.º EN 2024"},
                 {"en": "terceros", "texto": "DATOS DE TERCEROS|STREAMELEMENTS"},
                 {"en": "rol", "texto": "SERVIDORES DE ROL|EN GTA V"}],
     "nombres": ["Twitch"],
     "canciones": [],
     "planos": ["NUEVO_Twitch_Captura", "@GTA_Online:4", "@GTA5_Oficial_810:5", "@Historia_GTA:2"],
     "planos_en": [{"en": "Twitch", "plano": "NUEVO_Twitch_Captura"},
                   {"en": "rol", "plano": "@GTA_Online"}]},

    # ---------------------------------------------------------------- ACTO IV · LA VARA DE MEDIR (2026)
    {"id": "p10", "num": 10,"total": T, "titulo": "2026 · CASI 230 MILLONES", "capitulo": "2026 · Casi 230 millones",
     "overlay": "", "anio": 2026, "cartela": {"anio": "2026", "acto": "ACTO IV", "titulo": "LA VARA DE MEDIR"},
     "texto": ("Saltamos a mayo de dos mil veintiséis. En la presentación de resultados, Strauss Zelnick, consejero "
               "delegado de Take-Two, lo dice así: las ventas de GTA V siguen avanzando, con casi doscientos treinta "
               "millones de unidades sold-in. Trece años después de salir. A esas alturas, la mayoría de juegos de dos "
               "mil trece viven en la estantería de ofertas. Y en la misma llamada, Red Dead Redemption dos supera los "
               "ochenta y cinco millones. La casa tiene dos gallinas de los huevos de oro, y la más productiva ya ha "
               "cumplido trece años."),
     "rotulos": [{"en": "Zelnick", "texto": "STRAUSS ZELNICK|CONSEJERO DELEGADO"},
                 {"en": "doscientos", "texto": "CASI 230 M|SOLD-IN · MAYO 2026"},
                 {"en": "ochenta", "texto": "RED DEAD REDEMPTION 2|MÁS DE 85 M"}],
     "nombres": ["Zelnick"],
     "canciones": [],
     "planos": ["NUEVO_Zelnick_Captura", "N9_Captura_Transcripcion_Sold_In", "@GTA5_2013:3", "@RDR2_2018:2", "@GTA6_Mirada:2"],
     "planos_en": [{"en": "Zelnick", "plano": "NUEVO_Zelnick_Captura"},
                   {"en": "doscientos", "plano": "N9_Captura_Transcripcion_Sold_In"},
                   {"en": "ochenta", "plano": "@RDR2_2018"}]},
    {"id": "p11", "num": 11,"total": T, "titulo": "2026 · CASI 235 MILLONES", "capitulo": "2026 · Casi 235 millones",
     "overlay": "", "anio": 2026,
     "texto": ("En agosto, con los resultados del primer trimestre de su nuevo año fiscal, la frase cambia de casi a "
               "más de: más de doscientos treinta millones de unidades. Y el nueve de noviembre, a diez días de GTA VI, "
               "Zelnick vuelve a subirla: casi doscientos treinta y cinco millones en todo el mundo. Es la cifra más "
               "reciente antes del lanzamiento. Dicho rápido, suena a que medio continente tiene el juego en casa. Pues "
               "no exactamente. Porque aquí viene la letra pequeña, y cabe en una sola palabra: sold-in."),
     "rotulos": [{"en": "agosto", "texto": "MÁS DE 230 M|AGOSTO 2026"},
                 {"en": "nueve", "texto": "CASI 235 M|9 NOV 2026"}],
     "nombres": ["agosto"],
     "canciones": [],
     "planos": ["N9_Captura_Webull_230_Agosto", "N9_Captura_Transcripcion_Nov", "@GTA5_2013:3", "@GTA_Online:2",
                "@GTA6_Mirada:3"],
     "planos_en": [{"en": "agosto", "plano": "N9_Captura_Webull_230_Agosto"},
                   {"en": "nueve", "plano": "N9_Captura_Transcripcion_Nov"}]},
    {"id": "p12", "num": 12,"total": T, "titulo": "QUÉ SIGNIFICA SOLD-IN", "capitulo": "Qué significa sold-in",
     "overlay": "", "anio": 2026,
     "texto": ("Take-Two no define sold-in en una frase aparte, pero su glosario da la pista: habla de productos "
               "vendidos en digital o sold-in en físico. Traducido: una copia en caja cuenta cuando llega a la tienda, "
               "no cuando alguien se la lleva a casa. Así que la cifra mide unidades que han salido de la empresa, no "
               "jugadores. Quien lo compró en tres consolas cuenta tres veces. Y alguna caja habrá pasado meses en una "
               "estantería. Por eso, con este dato en la mano, nadie puede decir cuánta gente ha jugado a GTA V."),
     "rotulos": [{"en": "sold-in", "texto": "SOLD-IN|ENVÍOS, NO JUGADORES"},
                 {"en": "consolas", "texto": "3 CONSOLAS|= 3 UNIDADES"}],
     "nombres": [],
     "canciones": [],
     "planos": ["@GTA5_2013:3", "@GTA_Online:4", "@GTA6_Mirada:2"],
     "planos_en": [{"en": "sold-in", "plano": "@GTA5_2013"}]},
    {"id": "p13", "num": 13,"total": T, "titulo": "LA SAGA SIN TOTAL", "capitulo": "La saga, sin total oficial",
     "overlay": "", "anio": 2026,
     "texto": ("¿Y la saga entera? En las llamadas de mayo, agosto y noviembre, Take-Two habla de GTA V y de Red Dead, pero no "
               "da un total de todos los GTA juntos. Circulan cifras de la saga completa, pero las que hemos encontrado "
               "vienen de agregadores, no de un comunicado de la empresa. Así que aquí no van. Es menos espectacular, "
               "pero es lo honesto. Y tiene su lado bueno: cuando GTA VI dé su primera cifra oficial, sabremos "
               "exactamente con qué compararla."),
     "rotulos": [{"en": "saga", "texto": "LA SAGA ENTERA|SIN TOTAL OFICIAL EN 2026"}],
     "nombres": [],
     "canciones": [],
     "planos": ["@Historia_GTA:3", "@GTA4_2008:3", "@GTA6_Mirada:2"],
     "planos_en": [{"en": "saga", "plano": "@Historia_GTA"}]},
    {"id": "p14", "num": 14,"total": T, "titulo": "2026 · 19 DE NOVIEMBRE", "capitulo": "2026 · 19 de noviembre",
     "overlay": "", "anio": 2026, "etiqueta_linea": "2026 · GTA VI",
     "texto": ("Y así llegamos al diecinueve de noviembre de dos mil veintiséis. GTA VI sale en PlayStation cinco y Xbox "
               "Series, trece años y dos meses después de GTA V. La precarga digital ya estaba abierta desde el diez de "
               "noviembre, según anunció Rockstar. No vamos a decir cuántas copias venderá. Nadie lo sabe, "
               "y quien te dé una cifra antes de tiempo te está vendiendo humo, no juegos. Lo que sí sabemos es contra "
               "qué se va a medir. Y que su primera cifra oficial llegará, como siempre, en una presentación de "
               "resultados de Take-Two. Con su fecha y con su verbo."),
     "rotulos": [{"en": "diecinueve", "texto": "19 NOV 2026|GTA VI"},
                 {"en": "dos", "texto": "13 AÑOS Y 2 MESES|DESPUÉS DE GTA V"}],
     "nombres": ["diecinueve"],
     "canciones": [],
     "planos": ["Lanz_Final_19N", "VL_Fecha", "@GTA6_Lanzamiento:3", "@GTA6_Mirada:3"],
     "planos_en": [{"en": "diecinueve", "plano": "VL_Fecha"}]},
    {"id": "p15", "num": 15,"total": T, "titulo": "EL LISTÓN DE GTA V", "capitulo": "El listón de GTA V",
     "overlay": "", "anio": 2026, "etiqueta_linea": "2026 · LISTÓN",
     "texto": ("Así que el listón de GTA V tiene tres alturas. La primera, la del estreno: ochocientos quince millones "
               "de dólares en un día y mil millones en tres. La segunda, la del tiempo: casi doscientos treinta y cinco "
               "millones de unidades en trece años, repartidas en tres generaciones de consolas. Y la tercera, la más "
               "rara: un juego que siguió dando dinero mucho después de su estreno. La primera se mide en días. La "
               "segunda y la tercera, en años. Y eso no lo acelera ni el mejor tráiler del mundo."),
     "rotulos": [{"en": "alturas", "texto": "3 ALTURAS|ESTRENO · TIEMPO · VIDA"},
                 {"en": "días", "texto": "DÍAS|FRENTE A AÑOS"}],
     "nombres": ["alturas"],
     "canciones": [],
     "planos": ["@GTA5_2013:3", "@GTA_Online:2", "@GTA6_Mirada:3", "@Historia_GTA:2"],
     "planos_en": [{"en": "alturas", "plano": "@GTA6_Mirada"}]},

    # ---------------------------------------------------------------- CIERRE
    {"id": "cierre", "num": None, "titulo": "", "overlay": "", "capitulo": "De 2013 a 2026", "anio": 2026,
     "texto": ("Trece años, tres generaciones y casi doscientos treinta y cinco millones de unidades. Ahora te toca a ti: "
               "¿qué listón crees que le va a costar más superar a GTA VI? ¿El del primer día, el de las ventas "
               "acumuladas o el de seguir vivo trece años? Déjamelo en los comentarios, que quiero ver qué opina la "
               "gente. Y si te ha gustado, suscríbete, que esto no ha hecho más que empezar. Nos vemos en Leónida."),
     "rotulos": [{"en": "listón", "texto": "¿QUÉ LISTÓN|COSTARÁ MÁS?"},
                 {"en": "Trece", "texto": "2013 → 2026"}],
     "nombres": ["listón"],
     "canciones": [],
     "planos": ["VL_Atardecer_Final", "VL_Hidroavion", "VL_Lancha_Pareja", "@GTA6_Mirada:3"],
     "planos_en": [{"en": "listón", "plano": "@GTA6_Mirada"},
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
