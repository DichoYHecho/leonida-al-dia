"""Guion del vídeo largo 4 de «Leónida al Día»: «Jason y Lucía: todo lo que sabemos» (sale el mié 18 nov 2026, 18:00).

Mismo formato que guion_sg.py (se elige con GUION=guion_jl). Novedades del vídeo 4 (pedidas por mí el 10 y 11 nov):
  carteles      -> los del centro, a pantalla completa con fondo liso; los que empiezan por «@» son etiquetas
                   pequeñas de personaje arriba a la izquierda (nombre|papel) mientras sale su clip oficial.
  subtítulos    -> sin cartel detrás; sin barra de progreso; vídeo final en 2K (2560x1440).
  CRISTAL = True -> grafismo de cristal estilo Apple con colores Miami (cristal.py): subtítulos en pastilla,
                    carteles en tarjeta de cristal, cartelas sobre un fotograma quieto y difuminado, barra de progreso.
  planos largos  -> trozos de 2 a 6 s (fuentes_jl.py) para que el vídeo tenga más calma.
  sin repetir    -> ningún trozo dos veces y, en trozos-jl, sin tomas casi iguales entre vídeos (DEDUP).
Sin línea de tiempo (no es un vídeo de épocas). Guion, datos y fuentes: doc «Guion · Vídeo largo 4»
(https://claude.ai/artifact/CyN9h1WHtbwpGPbpkgxHW7), comprobados el 10 nov 2026.
"""
import re

from fuentes_jl import FUENTES as _FUENTES

VIDEOS_EXTRA = {k: v["url"] for k, v in _FUENTES.items()}
from fuentes_sg import FUENTES as _FUENTES_SG  # noqa: E402  (GTA 1 y GTA V, rama trozos-sg)
from fuentes_vc import FUENTES as _FUENTES_VC  # noqa: E402  (Vice City 2002, rama trozos-vc)

VIDEOS_EXTRA.update({k: v["url"] for k, v in _FUENTES_SG.items() if k not in VIDEOS_EXTRA})
VIDEOS_EXTRA.update({k: v["url"] for k, v in _FUENTES_VC.items() if k not in VIDEOS_EXTRA})

RECORTES = {k: 0.075 for k in _FUENTES_SG if k.startswith(("V_Juego", "ON_Juego"))}  # marca de agua arriba
MARCO = True       # partidas antiguas de 360p: en un marco sobre una copia borrosa
CRISTAL = True
LINEA_ANIMADA = False
LINEA = None

PLANOS_FIJOS = {"Portada_Animada"}

# Música: cambia en cada acto (sin música del juego)
MUSICA = {"hook": "synthwave", "p01": "hiphop", "p05": "breakbeat", "p08": "synthwave", "p11b": "breakbeat",
          "p14": "hiphop"}

# Pronunciación para la voz (una palabra por palabra: no cambia el número de palabras)
FONETICA = {
    "Jason": "Yéison", "Duval.": "Duvál.", "Duval,": "Duvál,", "Rob": "Rob", "Nelson,": "Nélson,", "Nelson": "Nélson",
    "North,": "Norz,", "North": "Norz", "Brian": "Bráian", "Heder,": "Jéder,", "Cal": "Cal", "Hampton,": "Jámpton,",
    "Arthur": "Árzur", "Morgan": "Mórgan", "Morgan.": "Mórgan.", "Red": "Red", "Dead": "Ded",
    "Redemption": "Ridémpshon", "IGN": "Aiyién", "IGN,": "Aiyién,", "TroisCouleurs": "Truacúler",
    "Bloomberg": "Blúmberg", "Bloomberg,": "Blúmberg,", "ChatGPT.": "Chatyipití.", "Guinness": "Guínes",
    "YouTube": "Yutub", "PS5": "PeEseCinco", "Online,": "Onlain,", "Online": "Onlain", "Ocean": "Óushen",
    "View": "Viú", "Tommy": "Tomi", "Vercetti": "Verchéti", "Divine,": "Diváin,", "Katie,": "Kéiti,",
    "Mikki": "Míki", "TGG": "Tiyiyí", "Deadpool": "Dédpul", "Vice": "Váis", "City": "Siti", "Boobie": "Búbi", "Ike": "Áik",
    "Dre'Quan": "Dricuán", "Priest": "Príst", "Only": "Ónli", "Raw": "Ro", "Records,": "Récords,", "Real": "Rial",
    "Dimez,": "Dáims,", "New": "Niú", "York": "York", "Times": "Táims", "Schreier,": "Sráier,", "Bonnie": "Bóni", "Clyde.": "Cláid.", "Netflix": "Nétflix",
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


BLOQUES = [
    # ---------------------------------------------------------------- GANCHO
    {"id": "hook", "num": None, "titulo": "", "overlay": "", "capitulo": "Introducción",
     "texto": ("Mañana, a esta hora, medio mundo estará jugando con dos personas a las que todavía no conoce de "
               "verdad. Él es Jason Duval. Ella, Lucía Caminos. Llevamos casi tres años viéndolos en tráileres, "
               "capturas y entrevistas, y Rockstar ha soltado bastantes más pistas de las que parece. Así que hoy "
               "juntamos todo lo que se sabe de ellos. Sin filtraciones y sin inventos. Ponte cómodo, que empezamos "
               "por ella."),
     "rotulos": [{"t": 0.0, "dur": 2.6, "negro": True, "texto": "JASON Y LUCÍA|TODO LO QUE SABEMOS"}],
     "nombres": ["jason", "lucía"],
     "planos": ["T2_18", "LZ_04", "MI_91", "MI_46", "MI_29", "T1_02"],
     "planos_en": [{"en": "jason", "plano": "LZ_02"}, {"en": "lucía", "plano": "MI_32"}]},

    # ---------------------------------------------------------------- ACTO I · ELLA
    {"id": "p01", "num": None, "titulo": "", "overlay": "", "capitulo": "Ella",
     "cartela": {"anio": "01", "acto": "ACTO I", "titulo": "ELLA"},
     "texto": ("El cuatro de diciembre de dos mil veintitrés, lo primero que vimos de GTA VI no fue una persecución "
               "ni una explosión. Fue a Lucía, con ropa de presa, en una entrevista dentro de la cárcel. Ese tráiler "
               "pasó de noventa millones de visitas en YouTube en veinticuatro horas, y Guinness lo apuntó como la "
               "presentación de un videojuego más vista de la plataforma en su primer día. O sea, que Lucía batió un "
               "récord mundial sin salir de la celda. Ya quisieran muchos."),
     "rotulos": [{"en": "noventa", "texto": "90,4 MILLONES|DE VISITAS EN 24 H"}],
     "nombres": ["lucía"],
     "planos": ["T1_04", "T1_07", "T1_05", "MI_87", "T1_11", "MI_99", "MI_27"],
     "planos_en": [{"en": "lucía", "plano": "T1_03"}]},

    {"id": "p02", "num": None, "titulo": "", "overlay": "", "capitulo": "Quién es Lucía",
     "texto": ("Según su ficha oficial, su padre la enseñó a pelear casi antes de que supiera andar, y desde entonces "
               "la vida no le ha dado ni un respiro. Acabó en la Penitenciaría de Leónida por defender a su familia y, "
               "con algo de suerte, ha conseguido salir. Ahora tiene un plan para que las cosas por fin le salgan bien, "
               "y no lo va a soltar cueste lo que cueste. Por eso en las capturas la ves en el gimnasio, con los "
               "guantes puestos. No es postureo: es su historia. Y en ese plan entra Jason: según Rockstar, Lucía ve "
               "en una vida con él su manera de salir de todo esto."),
     "rotulos": [{"en": "penitenciaría", "texto": "@LUCÍA CAMINOS|RECIÉN SALIDA DE PRISIÓN"}],
     "nombres": ["gimnasio"],
     "planos": ["CL_Lucia", "LZ_07", "T2_10", "MI_90", "MI_30", "T2_17", "MI_48"],
     "planos_en": [{"en": "gimnasio", "plano": "T2_06"}, {"en": "penitenciaría", "plano": "MI_96"}]},

    {"id": "p03", "num": None, "titulo": "", "overlay": "", "capitulo": "El grillete",
     "texto": ("Fíjate en su tobillo. En varias imágenes oficiales Lucía lleva un grillete electrónico, y no está ahí "
               "de adorno. Rob Nelson, uno de los jefes de Rockstar North, ha contado que forma parte de la trama y de "
               "la manera en que se juntan Jason y Lucía. Traducido: la libertad de Lucía viene con letra pequeña, y "
               "esa letra pequeña va a pesar."),
     "rotulos": [{"en": "grillete", "texto": "EL GRILLETE|ES PARTE DE LA TRAMA"}],
     "nombres": ["tobillo"],
     "planos": ["MI_49", "MI_111"],
     "planos_en": [{"en": "tobillo", "plano": "MI_31"}, {"en": "jason", "plano": "MI_95"}]},

    {"id": "p04", "num": None, "titulo": "", "overlay": "", "capitulo": "Una primera vez",
     "texto": ("Y ahora, un dato que se repite mucho pero que hay que contar bien. En el primer GTA, el de mil "
               "novecientos noventa y siete, podías elegir entre ocho personajes, y cuatro eran mujeres: Divine, "
               "Katie, Mikki y Ulrika. Pero eran un nombre y una cara en el menú, sin historia ni voz. Lucía es la "
               "primera mujer protagonista fija de la saga principal, con historia propia y voz propia. Ha tardado "
               "casi treinta años, pero ha llegado por la puerta grande."),
     "rotulos": [{"en": "ocho", "texto": "GTA 1 (1997)|8 PERSONAJES, 4 MUJERES"},
                 {"en": "fija", "texto": "PRIMERA PROTAGONISTA|FIJA DE LA SAGA"}],
     "nombres": ["primer", "lucía"],
     "planos": ["MI_104", "MI_128", "@GTA1_1997:2"],
     "planos_en": [{"en": "primer", "plano": "@GTA1_1997"}, {"en": "lucía", "plano": "MI_89"}]},

    # ---------------------------------------------------------------- ACTO II · ÉL
    {"id": "p05", "num": None, "titulo": "", "overlay": "", "capitulo": "Él",
     "cartela": {"anio": "02", "acto": "ACTO II", "titulo": "ÉL"},
     "texto": ("Jason es la otra cara de la moneda. Según Rockstar, lo único que quiere es una vida tranquila, pero "
               "cada día se le complica un poco más. Creció rodeado de timadores y delincuentes, entró en el ejército "
               "para salir de ese ambiente, y al volver acabó trabajando para traficantes de los Cayos de Leónida. "
               "Plan de vida impecable, como ves. Su ficha añade que conocer a Lucía puede ser lo mejor o lo peor "
               "que le ha pasado. Él sabe cómo le gustaría que acabara. Nosotros, todavía no."),
     "rotulos": [{"en": "jason", "texto": "@JASON DUVAL|EXMILITAR"}],
     "nombres": ["jason", "cayos"],
     "planos": ["MI_26", "T2_03", "T2_08", "T2_09", "T2_02", "MI_38"],
     "planos_en": [{"en": "jason", "plano": "CL_Jason"}, {"en": "cayos", "plano": "LZ_01"}]},

    {"id": "p06", "num": None, "titulo": "", "overlay": "", "capitulo": "El tráiler de lanzamiento",
     "texto": ("Ese pasado militar no es relleno. El tráiler de lanzamiento, que salió el quince de octubre, arranca "
               "justo con Jason hablando de su etapa en el ejército, hasta que le suena el teléfono: es Lucía, "
               "llamando desde la cárcel. Son unos noventa segundos, grabados en una PS5 normal, y dejan clarísimo de "
               "qué va esto. De ellos dos."),
     "rotulos": [{"en": "lanzamiento", "texto": "TRÁILER DE LANZAMIENTO|15 OCT 2026"}],
     "nombres": ["teléfono"],
     "planos": ["LZ_09", "LZ_06", "LZ_08", "MI_130"],
     "planos_en": [{"en": "teléfono", "plano": "LZ_03"}]},

    {"id": "p07", "num": None, "titulo": "", "overlay": "", "capitulo": "Su gente en los Cayos",
     "texto": ("Su jefe es Brian Heder, casero y contrabandista veterano de los Cayos. Sí, el que le cobra el "
               "alquiler es el mismo que le da trabajo; escapatoria, poca. Y su mejor amigo es Cal Hampton, un tipo "
               "que se pasa las tardes escuchando las comunicaciones de la Guardia Costera con unas cervezas, "
               "convencido de que alguien nos vigila a todos."),
     "rotulos": [{"en": "jefe", "texto": "@BRIAN HEDER|CASERO Y CONTRABANDISTA"},
                 {"en": "amigo", "texto": "@CAL HAMPTON|SU MEJOR AMIGO"}],
     "nombres": ["jefe", "amigo"],
     "planos": ["T2_05", "T2_13", "MI_55", "MI_122"],
     "planos_en": [{"en": "jefe", "plano": "CL_Brian"}, {"en": "casero", "plano": "T2_01"}, {"en": "amigo", "plano": "CL_Cal"}, {"en": "tardes", "plano": "T2@81.2+3.4"}, {"en": "cervezas", "plano": "T2_16"}]},

    {"id": "p07b", "num": None, "titulo": "", "overlay": "", "capitulo": "El resto del reparto",
     "texto": ("Y no son los únicos. Rockstar ha presentado a seis personajes más, y todos tienen pinta de cruzarse en "
               "su camino. Raúl Bautista es un atracador de bancos veterano que siempre anda buscando talento nuevo, y "
               "le gusta arriesgar más de la cuenta. Boobie Ike tiene inmuebles, un club y un estudio de grabación. "
               "Dre'Quan Priest quiere triunfar con su sello, Only Raw Records, y acaba de fichar a Real Dimez, un dúo "
               "de rap que arrasa en redes. Eso sí: Rockstar no ha contado todavía qué pinta cada uno en la historia "
               "de Jason y Lucía."),
     "rotulos": [{"en": "raúl", "texto": "@RAÚL BAUTISTA|ATRACADOR DE BANCOS"},
                 {"en": "inmuebles", "texto": "@BOOBIE IKE|INMUEBLES, CLUB Y ESTUDIO"},
                 {"en": "triunfar", "texto": "@DRE'QUAN PRIEST|ONLY RAW RECORDS"},
                 {"en": "fichar", "texto": "@REAL DIMEZ|DÚO DE RAP"}],
     "nombres": ["raúl", "inmuebles", "triunfar", "fichar"],
     "planos": ["T2_11", "T2_12", "T2_15", "MI_106", "MI_107"],
     "planos_en": [{"en": "raúl", "plano": "CL_Raul"}, {"en": "inmuebles", "plano": "CL_Boobie"}, {"en": "triunfar", "plano": "CL_DreQuan"}, {"en": "fichar", "plano": "CL_Real"}]},

    # ---------------------------------------------------------------- ACTO III · JUNTOS
    {"id": "p08", "num": None, "titulo": "", "overlay": "", "capitulo": "Juntos",
     "cartela": {"anio": "03", "acto": "ACTO III", "titulo": "JUNTOS"},
     "texto": ("¿Y cómo se mete esta pareja en un lío de este tamaño? Rockstar lo resume así: los dos saben desde "
               "siempre que tienen las de perder, pero un golpe que parecía fácil sale mal y acaban metidos en una "
               "conspiración que recorre todo el estado de Leónida. A partir de ahí, o se apoyan el uno en el otro o "
               "no salen vivos. Rob Nelson lo dijo sin rodeos en una entrevista: son una pareja, son Bonnie y Clyde. "
               "Ese planteamiento llegó con el segundo tráiler, el seis de mayo de dos mil "
               "veinticinco, que según Rockstar sumó cuatrocientos setenta y cinco millones de visitas en "
               "veinticuatro horas entre todas las plataformas. Más que el tráiler de Deadpool y Lobezno, que se "
               "quedó en trescientos sesenta y cinco."),
     "rotulos": [{"en": "cuatrocientos", "texto": "475 MILLONES|EN 24 H"}],
     "nombres": ["golpe"],
     "planos": ["MI_64", "MI_65", "MI_81", "MI_82", "T2_14", "MI_83", "MI_79"],
     "planos_en": [{"en": "golpe", "plano": "MI_63"}, {"en": "cuatrocientos", "plano": "MI_125"}]},

    {"id": "p09", "num": None, "titulo": "", "overlay": "", "capitulo": "Casi fueron cuatro",
     "texto": ("Y pudieron no ser dos. Rob Nelson le contó a IGN que, después de los tres protagonistas de GTA V, en "
               "Rockstar se plantearon subir a cuatro. Lo descartaron porque cada personaje habría tenido menos tiempo "
               "de juego, y les costaría más que te encariñaras con ellos. Así que se quedaron con dos, y bien atados. "
               "Según Bloomberg, la historia de Jason y Lucía ya estaba esbozada a finales de dos mil diecinueve: "
               "llevan casi siete años esperándonos."),
     "rotulos": [{"en": "cuatro", "texto": "¿CUATRO PROTAGONISTAS?|DESCARTADO"},
                 {"en": "diecinueve", "texto": "HISTORIA ESBOZADA|A FINALES DE 2019"}],
     "nombres": ["tres"],
     "planos": ["MI_66", "MI_67", "MI_62", "@GTA5_2013:2"],
     "planos_en": [{"en": "tres", "plano": "@GTA5_2013"}, {"en": "dos", "plano": "MI_61"}]},

    {"id": "p10", "num": None, "titulo": "", "overlay": "", "capitulo": "Cambiar de personaje",
     "texto": ("En la mirada extendida, que se estrenó en Netflix el veintisiete de agosto, ya vimos cómo se juega con los dos. Puedes pasar de uno a otro cuando "
               "quieras, también fuera de las misiones. Por ejemplo: Jason conduce, cambias a Lucía y ella dispara "
               "desde el asiento de al lado. Eso sí, en algunos momentos de la historia el cambio se bloquea, porque "
               "la escena se vive desde uno de los dos. Si uno está en apuros, puede llamar al otro para que le "
               "ayude. Y mientras manejas a uno, el otro sigue con su vida. Tanto "
               "que, en una demostración para IGN, Nelson cambió a Jason y lo pilló en la ducha. Intimidad, cero. Y "
               "que los dos vayan juntos a todas partes por su cuenta no fue sencillo: Nelson contó a Bloomberg que "
               "les llevó años de trabajo con la inteligencia artificial de los personajes, la de toda la vida en los "
               "videojuegos. Nada de ChatGPT."),
     "nombres": ["conduce"],
     "planos": ["MI_68", "MI_70", "MI_77", "MI_78", "MI_41", "MI_42", "MI_84", "MI_85", "MI_33", "MI_86"],
     "planos_en": [{"en": "conduce", "plano": "MI_69"}, {"en": "netflix", "plano": "MI_43"}, {"en": "ducha", "plano": "MI_50"}]},

    {"id": "p11", "num": None, "titulo": "", "overlay": "", "capitulo": "La relación la decides tú",
     "texto": ("Aquí viene lo más nuevo. Según Nelson, el romance entre Jason y Lucía es completamente opcional. Si "
               "quieres que sean pareja, tienes que cuidarlo: pasar tiempo juntos, contestar sus mensajes, hasta darse "
               "la mano al pasear, que en la demostración salía como opción. Si pasas de todo eso, se quedan en socios "
               "del crimen. Pero socios siempre: pase lo que pase, se cubren las espaldas. Cuando van cada uno por su "
               "lado, se escriben, aunque sea para decir que se van a dormir, y si ignoras esos mensajes la relación "
               "se resiente. Jason Schreier, de Bloomberg, que vio una partida, los describe como dos personas a las "
               "que de verdad les gusta pasar tiempo juntas. Raro en un GTA, la verdad."),
     "rotulos": [{"en": "opcional", "texto": "¿PAREJA O SOCIOS?|TÚ DECIDES"}],
     "nombres": ["mano"],
     "planos": ["MI_112", "MI_113", "MI_114", "MI_115", "MI_44", "MI_131"],
     "planos_en": [{"en": "mano", "plano": "MI_51"}]},

    {"id": "p11b", "num": None, "titulo": "", "overlay": "", "capitulo": "Qué clase de criminal eres",
     "texto": ("Y ojo, que el juego también se fija en cómo trabajan. Nelson le explicó a IGN que hay un perfil "
               "criminal, una especie de heredero del honor de Red Dead Redemption 2. No te castiga por delinquir, que "
               "esto es GTA, sino por la violencia gratuita y repetida. Y cada uno tiene el suyo: Lucía puede ir de "
               "profesional mientras Jason va por ahí liándola."),
     "rotulos": [{"en": "perfil", "texto": "PERFIL CRIMINAL|UNO PARA CADA UNO"}],
     "nombres": ["perfil"],
     "planos": ["MI_22", "MI_23", "MI_24", "MI_121"],
     "planos_en": [{"en": "perfil", "plano": "MI_21"}]},

    {"id": "p12", "num": None, "titulo": "", "overlay": "", "capitulo": "Comer, dormir, entrenar",
     "texto": ("Aquí Rockstar se ha puesto muy de vida real. Nelson le explicó al youtuber TGG que el móvil de los dos "
               "trae una app de salud que dice si han descansado bien, y que dormir poco hace que algunos atributos se "
               "recuperen más despacio. Si comen de más, engordan, aunque hay que comer bastante para que se note. Y "
               "el músculo se gana en el gimnasio, y se pierde si lo dejas. En la partida que vio Bloomberg, Lucía "
               "corría en la cinta mientras Jason hacía sentadillas. Pareja que entrena unida… Y si pasan días sin dormir, de huida o de fiesta, se "
               "les nota en la cara. Ojeras incluidas."),
     "rotulos": [{"en": "app", "texto": "APP DE SALUD|SUEÑO, PESO Y MÚSCULO"}],
     "nombres": ["gimnasio"],
     "planos": ["MI_98", "MI_94", "MI_88"],
     "planos_en": [{"en": "app", "plano": "MI_97"}, {"en": "gimnasio", "plano": "MI_47"}, {"en": "comen", "plano": "MI_34"}, {"en": "dormir", "plano": "MI_35"}]},

    {"id": "p13", "num": None, "titulo": "", "overlay": "", "capitulo": "La meta: Arthur Morgan",
     "texto": ("El listón que se ha puesto Rockstar es alto. Nelson dijo a la revista francesa TroisCouleurs que "
               "quieren que sientas por Jason y Lucía lo mismo que por Arthur Morgan en Red Dead Redemption 2. Por eso "
               "habrá ratos tranquilos en su piso, del día a día, para que los momentos duros peguen más. Su ejemplo: "
               "Lucía se cae por unas escaleras, cambias a Jason, y ya no la oyes. Angustia de la buena. Y hasta la estructura mira a "
               "Red Dead: la historia irá por capítulos, como la de Arthur."),
     "rotulos": [{"en": "arthur", "texto": "@ARTHUR MORGAN|RED DEAD REDEMPTION 2"}],
     "nombres": ["arthur", "piso"],
     "planos": ["RDR2_02", "RDR2_04", "MI_36", "MI_37"],
     "planos_en": [{"en": "sientas", "plano": "Mirada_Terraza"}, {"en": "arthur", "plano": "RDR2@25.6+3.4"},
                   {"en": "piso", "plano": "MI_116"}, {"en": "escaleras", "plano": "MI_129"}]},

    {"id": "p13b", "num": None, "titulo": "", "overlay": "", "capitulo": "Ochenta horas con ellos",
     "texto": ("¿Y cuánto tiempo vamos a pasar con esta pareja? Nelson le contó al New York Times que su última "
               "partida, en febrero, le llevó unas ochenta horas, con la historia principal y algunos objetivos "
               "opcionales que cambian cosas de la trama. Ojo: es la partida de una persona, no una duración oficial. "
               "Pero da una idea. Ochenta horas con Jason y Lucía. Más vale que te caigan bien."),
     "rotulos": [{"en": "ochenta", "texto": "≈ 80 HORAS|LA PARTIDA DE NELSON"}],
     "nombres": ["horas"],
     "planos": ["MI_92", "MI_93", "MI_105", "MI_45"],
     "planos_en": [{"en": "ochenta", "plano": "MI_72"}, {"en": "horas", "plano": "MI_71"}]},

    # ---------------------------------------------------------------- ACTO IV · LO QUE AÚN NO SABEMOS
    {"id": "p14", "num": None, "titulo": "", "overlay": "", "capitulo": "Lo que aún no sabemos",
     "cartela": {"anio": "04", "acto": "ACTO IV", "titulo": "LO QUE FALTA"},
     "texto": ("Con todo esto, todavía hay mucho que Rockstar no ha contado. No ha dicho oficialmente quién pone la "
               "voz a Jason ni a Lucía. No sabemos qué hizo exactamente Lucía para acabar presa. Y, sobre todo, no "
               "sabemos cómo acaba esto. Lo último que hemos visto son las treinta y nueve capturas nuevas del cinco "
               "de noviembre, y fíjate: trece son de los dos juntos. Rockstar sabe perfectamente a quién quieres ver."),
     "rotulos": [{"en": "voz", "texto": "¿VOCES? ¿FINAL?|SIN CONFIRMAR"},
                 {"en": "trece", "texto": "39 CAPTURAS NUEVAS|13 DE LOS DOS"}],
     "nombres": ["capturas"],
     "planos": ["MI_101", "MI_117", "MI_118", "MI_73"],
     "planos_en": [{"en": "trece", "plano": "T1_12"}, {"en": "voz", "plano": "MI_108"}, {"en": "capturas", "plano": "MI_102"}]},

    # ---------------------------------------------------------------- TRES EXTRA
    {"id": "e1", "num": None, "titulo": "", "overlay": "", "capitulo": "Tres extra de regalo",
     "texto": ("Tres extra de regalo. El primero: en una captura oficial, Jason posa delante del hotel Ocean View con "
               "una camisa que recuerda muchísimo a la de Tommy Vercetti en el Vice City de dos mil dos. Rockstar no ha "
               "dicho que sea un guiño, pero tampoco hace falta."),
     "rotulos": [{"en": "tommy", "texto": "@TOMMY VERCETTI|VICE CITY (2002)"}],
     "nombres": ["tommy", "camisa"],
     "planos": ["MI_40", "MI_75", "@Vice_City_2002:1"],
     "planos_en": [{"en": "tommy", "plano": "@Vice_City_2002"}, {"en": "camisa", "plano": "MI_39"}]},

    {"id": "e2", "num": None, "titulo": "", "overlay": "", "capitulo": "Una cara de GTA Online",
     "texto": ("El segundo: en la mirada extendida aparece Valentina, un personaje que ya conocían los jugadores de "
               "GTA Online, y es quien les ofrece a Jason y Lucía un trabajo de escoltas en la fiesta de Megamundo, una cadena de televisión en español. Es el primer personaje de "
               "GTA Online que salta a GTA VI."),
     "rotulos": [{"en": "valentina", "texto": "@VALENTINA|DE GTA ONLINE A GTA VI"}],
     "nombres": ["valentina"],
     "planos": ["MI_56", "MI_57", "MI_58", "MI_59", "MI_60"],
     "planos_en": [{"en": "valentina", "plano": "MI_103"}]},

    {"id": "e3", "num": None, "titulo": "", "overlay": "", "capitulo": "No empiezan de cero",
     "texto": ("Y el tercero: Jason y Lucía no se acaban de conocer, tienen pasado. Nelson ha contado que la historia "
               "arranca con los dos queriendo darle otra oportunidad a lo suyo. Y en una partida que enseñó a la "
               "prensa, se ponen a recordar el día que la madre de Lucía se enfadó con Jason. Suegras, también en "
               "Leónida."),
     "rotulos": [{"en": "oportunidad", "texto": "OTRA OPORTUNIDAD"}],
     "nombres": ["recordar"],
     "planos": ["MI_110", "MI_74", "MI_76"],
     "planos_en": [{"en": "recordar", "plano": "T2_07"}]},

    # ---------------------------------------------------------------- CIERRE
    {"id": "cierre", "num": None, "titulo": "", "overlay": "", "capitulo": "Cierre",
     "texto": ("Mañana, diecinueve de noviembre, Jason y Lucía dejan de ser un tráiler y pasan a ser tuyos. La gran "
               "pregunta es tuya: ¿pareja o solo socios? Déjamelo en los comentarios. Y si quieres seguir el "
               "lanzamiento día a día, aquí en Leónida al Día lo vamos contando. Nos vemos en Leónida."),
     "rotulos": [{"en": "pareja", "texto": "¿PAREJA|O SOLO SOCIOS?"}],
     "nombres": ["comentarios"],
     "planos": ["MI_52", "MI_53", "MI_54", "MI_80"],
     "planos_en": [{"en": "pareja", "plano": "MI_119"}, {"en": "comentarios", "plano": "MI_120"}, {"en": "leónida", "plano": "Portada_Animada"}]},
]

for _b in BLOQUES:
    _b["voz"] = _voz(_b["texto"])

T = len(BLOQUES)
