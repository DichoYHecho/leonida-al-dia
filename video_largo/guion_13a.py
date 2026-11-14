"""Guion del vídeo largo «¿Por qué GTA VI ha tardado 13 años?» de «Leónida al Día» (borrador 3, 11 nov 2026).

Mismo formato que guion_sg.py (se elige con GUION=guion_13a). No importa fuentes_sg.
Datos y fuentes: investigacion.md. Planos NUEVO_ descritos en edicion.md (hay que producirlos y añadirlos a la tabla de trozos).
Sin VIDEOS_EXTRA: los vídeos oficiales se añaden cuando estén verificados.
"""
import re

VIDEOS_EXTRA = {  # 14 nov: fuentes oficiales de Rockstar en 2160p (planos_4k.md)
    "GTAO_Bounties_4K": "https://videos-rockstargames-com.akamaized.net/v4/oa46rs8r/flv/en-us-2160p.mp4",
    "GTAO_CE_4K": "https://videos-rockstargames-com.akamaized.net/v4/8rakra67/flv/en-us-2160p.mp4",
    "GTAO_Cluckin_4K": "https://videos-rockstargames-com.akamaized.net/v4/r3175t5r/flv/en-us-2160p.mp4",
    "GTAO_Kanjo_4K": "https://videos-rockstargames-com.akamaized.net/v4/3ra4t562/flv/en-us-2160p.mp4",
    "GTAO_Kortz_4K": "https://videos-rockstargames-com.akamaized.net/v4/a0a0rre4/flv/en-us-2160p.mp4",
    "GTAO_Luiva_4K": "https://videos-rockstargames-com.akamaized.net/v4/203as2rs/flv/en-us-2160p.mp4",
    "GTAO_PS5_4K": "https://videos-rockstargames-com.akamaized.net/v4/1s626s55/flv/en-us-2160p.mp4",
    "GTAO_Pizza_4K": "https://videos-rockstargames-com.akamaized.net/v4/aro34sg4/flv/en-us-2160p.mp4",
    "GTAO_Sabotage_4K": "https://videos-rockstargames-com.akamaized.net/v4/r50k6mmg/flv/en-us-2160p.mp4",
    "GTAO_Safehouse_4K": "https://videos-rockstargames-com.akamaized.net/v4/to78rk1o/flv/en-us-2160p.mp4",
    "GTAO_Vigero_4K": "https://videos-rockstargames-com.akamaized.net/v4/k1t75kk6/flv/en-us-2160p.mp4",
    "GTAO_Weevil_4K": "https://videos-rockstargames-com.akamaized.net/v4/a9233r59/flv/en-us-2160p.mp4",
    "GTAV_PC_4K": "https://videos-rockstargames-com.akamaized.net/v4/ks18e7s9/flv/en-us-2160p.mp4",
    "GTAV_PS5_4K": "https://videos-rockstargames-com.akamaized.net/v4/r3too449/flv/en-us-2160p.mp4",
    "LANoire_4K": "https://videos-rockstargames-com.akamaized.net/v4/3rr4o8so/flv/en-us-2160p.mp4",
    "Lanz": "https://media-rockstargames-com.akamaized.net/VI/downloads/videos/GTAVI_Launch_Trailer/GTAVI_Launch_Trailer.mp4",
    "Mirada4K": "https://videos-rockstargames-com.akamaized.net/v4/rk721912/flv/es-es-2160p.mp4",
    "PreLoad": "https://media-rockstargames-com.akamaized.net/VI/downloads/videos/GTAVI_Pre-Load_Now/GTAVI_Pre-Load_Now.mp4",
    "RDO_Beta_4K": "https://videos-rockstargames-com.akamaized.net/v4/r5tc99c3/flv/en-us-2160p.mp4",
    "RDO_BloodMoney_4K": "https://videos-rockstargames-com.akamaized.net/v4/3a753kct/flv/en-us-2160p.mp4",
    "RDO_Frontier_4K": "https://videos-rockstargames-com.akamaized.net/v4/c686k8ok/flv/en-us-2160p.mp4",
    "RDO_Lanz_4K": "https://videos-rockstargames-com.akamaized.net/v4/5611kt7k/flv/en-us-2160p.mp4",
    "RDO_Moonshiners_4K": "https://videos-rockstargames-com.akamaized.net/v4/57s1k75o/flv/en-us-2160p.mp4",
    "RDO_Naturalist_4K": "https://videos-rockstargames-com.akamaized.net/v4/k56k16rs/flv/en-us-2160p.mp4",
    "RDR2_4K": "https://videos-rockstargames-com.akamaized.net/v4/6c8k48rr/flv/en-us-2160p.mp4",
    "RDR2_Gameplay_4K": "https://videos-rockstargames-com.akamaized.net/v4/1ook234t/flv/en-us-2160p.mp4",
    "RDR2_PC_4K": "https://videos-rockstargames-com.akamaized.net/v4/9krr33s1/flv/en-us-2160p.mp4",
    "T1": "https://media-rockstargames-com.akamaized.net/VI/downloads/videos/GTAVI_Trailer_1/GTAVI_Trailer_1.mp4",
    "T2": "https://media-rockstargames-com.akamaized.net/VI/downloads/videos/GTAVI_Trailer_2/GTAVI_Trailer_2.mp4",
    "Trilogy_4K": "https://videos-rockstargames-com.akamaized.net/v4/8ta2r546/flv/en-us-2160p.mp4",
}
SIN_BANDAS = {'GTAO_CE_4K', 'GTAO_Kanjo_4K', 'GTAO_PS5_4K', 'GTAO_Pizza_4K', 'GTAO_Vigero_4K', 'GTAO_Weevil_4K', 'Mirada4K', 'RDR2_Gameplay_4K', 'T1'}  # sin letterbox: sin cropdetect
LENTO_MAX = {'GTAV_PC_4K': 2.0}  # 60 fps; en el resto la cámara lenta se limita a 1,25
FUENTES_REMOTAS = True  # cada tramo se lee de la URL 4K (no se baja el vídeo entero)

PLANOS_FIJOS = {"NUEVO_Absurd_Logo", "NUEVO_Foto_Houser", "NUEVO_Foto_Zelnick", "NUEVO_Texto_Hechos"}

RECORTES = {}
MARCO = True

# Música por época: cambia con cada cartela (ninguna pista más de 3,5 min)
# 14 nov: estas voces se hicieron con gemini-3.8-flash-tts (suena distinto); se rehacen con flash-lite
VOZ_REHACER = ["p05", "p06", "p07", "p08", "p10", "p11"]
MUSICA = {"hook": "synthwave", "p01": "synthwave", "p06": "breakbeat", "p13": "hiphop", "p17": "synthwave"}

# Línea de tiempo de abajo (años de los bloques; etiqueta_linea por bloque)
LINEA_ANIMADA = True
LINEA = [(2010, "RDR 2"), (2013, "GTA V"), (2018, "RDR 2 SALE"), (2022, "FILTRACIÓN"), (2026, "GTA VI")]

# Pronunciación para la voz: cada valor es UNA palabra (misma cantidad de palabras que el texto)
FONETICA = {
    "III": "3", "IV": "4", "V": "5", "VI": "6", "City": "Siti", "Vice": "Vais",
    "Houser": "Jáuser", "Morgan": "Mórgan", "Arthur": "Árdur", "Michael": "Máikel", "Trevor": "Trévor",
    "Franklin": "Frankli", "Pointer": "Póinter", "Sisters": "Sísters", "Petty": "Péti", "Together": "Tuguéder",
    "Trilogy": "Trílogi", "Definitive": "Definitiv", "Edition": "Edishon", "Schreier": "Shráier",
    "Bloomberg": "Blúmberg", "Take-Two": "Teik-Tu", "Rockstar": "Rocstar", "PlayStation": "Pleistéishon",
    "Xbox": "Ékbox", "Series": "Síries", "Online": "Onlain", "Love": "Lov", "Road": "Roud",
    "Leonida": "Leónida", "Hot": "Jot", "Nelson": "Nélson", "IGN": "Áigen", "Red": "Red", "Redemption": "Redémption",
    "Dead": "Ded", "Arion": "Árion", "Kurtaj": "Kúrtai", "Oxford": "Óksford", "Fire": "Fáier", "Stick": "Stik",
    "Absurd": "Absurd", "Ventures": "Véntiurs", "Slack": "Eslak", "Stadia": "Stéidia", "Sam": "Sam",
    "Twitch": "Tuích", "NoPixel": "Nopíksel", "FiveM": "Fáivem", "RedM": "Redém", "Cfx.re": "Sefeixérre",
    "Plus": "Plas", "Zelnick": "Zélnik", "Strauss": "Estráus", "Ruffian": "Rúfian", "Dundee": "Dandí",
    "Crackdown": "Crákdaun", "Games": "Guéims", "Gary": "Gueri", "Liddon": "Lídon", "Billy": "Bili",
    "Thomson": "Tomson", "Brendan": "Bréndan", "McNamara": "Macnamara", "Bondi": "Bóndi", "Deluxe": "Delúx",
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
     "texto": ("Septiembre de dos mil veintidós. Aparecen en un foro noventa vídeos de un juego que nadie había visto: "
               "unos cincuenta minutos de GTA VI en desarrollo. Rockstar confirma que son reales. Y ahí empieza una "
               "pregunta que sigue en pie. Porque el juego sale el diecinueve de noviembre de dos mil veintiséis, trece "
               "años después de GTA V. ¿Qué ha hecho Rockstar todo este tiempo? ¿Y por qué tanto? Hoy lo contamos en "
               "orden, año a año."),
     "rotulos": [{"t": 0.0, "dur": 2.4, "negro": True, "texto": "SEP 2022|→ NOV 2026"},
                 {"en": "noventa", "texto": "~90 VÍDEOS|EN UN FORO"},
                 {"en": "cincuenta", "texto": "50 MINUTOS|DE GTA VI"},
                 {"en": "trece", "texto": "13 AÑOS|DESPUÉS DE GTA V"}],
     "nombres": ["noventa", "trece"],
     "planos": ["NUEVO_Filtracion_Foro", "K5_Mir_Llegada_Noche", "NUEVO_Comunicado_Rockstar", "K5_GTAV_Coche_Atardecer", "K5_Img_VC_Skyline_Helicoptero", "K5_T2_Atardecer_Aereo", "K5_Img_Leonida_Keys_Avioneta", "K5_Mir_Pasillo_Gancho", "K5_Img_Grassrivers_Hidrodeslizador", "K5_Mir_Mirilla", "K5_Mir_Coche_Conductora"],
     "planos_en": [{"en": "cincuenta", "plano": "K5_Mir_Llegada_Noche"},
              {"en": "noventa", "plano": "NUEVO_Filtracion_Foro"},
              {"en": "confirma", "plano": "NUEVO_Comunicado_Rockstar"},
              {"en": "trece", "plano": "K5_GTAV_Coche_Atardecer"},
              {"en": "noviembre", "plano": "K5_Img_VC_Skyline_Helicoptero"},
              {"en": "tiempo", "plano": "K5_T2_Atardecer_Aereo"}]},

    # ---------------------------------------------------------------- ACTO I · EL DINERO NO PARA (2013-2015)
    {"id": "p01", "num": 1, "total": T, "titulo": "2013 · GTA V", "capitulo": "2013 · GTA V",
     "overlay": "", "anio": 2013, "cartela": {"anio": "2013", "acto": "ACTO I", "titulo": "EL DINERO NO PARA"},
     "texto": ("En septiembre de dos mil trece sale GTA V. Tres protagonistas: Michael, un ladrón de bancos retirado; "
               "Franklin, un chaval de la calle; y Trevor, un tipo impredecible que vive en el desierto. Puedes cambiar "
               "entre ellos cuando quieras, incluso en mitad de un atraco. Y el juego vende muchísimo. Take-Two dice hoy "
               "que lleva casi doscientos treinta millones de copias. Ahí está el primer motivo por el que no había prisa: "
               "un juego que vende así durante años no necesita un sucesor para seguir ganando dinero."),
     "rotulos": [{"en": "septiembre", "texto": "17 SEP 2013|GTA V"},
                 {"en": "ladrón", "texto": "MICHAEL|LADRÓN RETIRADO"},
                 {"en": "doscientos", "texto": "CASI 230 MILLONES|DE COPIAS"}],
     "nombres": ["septiembre", "ladrón", "desierto", "atraco", "doscientos"],
     "planos": ["K5_GTAV_Puesta_Cables", "K5_GTAV_Michael_Tenis", "K5_GTAV_Franklin_Puerta", "K5_GTAO_Chimeneas", "K5_GTAO_Edificio_Contrapicado", "K5_Img_GTAO_Laser", "K5_GTAV_Trevor_Trio", "K5_GTAV_Puente_Rio", "K5_GTAV_Coche_Costa", "K5_Img_GTAO_Camara_Kortz", "K5_GTAO_Rascacielos", "K5_Img_GTAO_Michael_Sofa", "K5_Img_GTAO_Coche_Verde"],
     "planos_en": [{"en": "septiembre", "plano": "K5_GTAV_Puesta_Cables"},
              {"en": "Michael", "plano": "K5_GTAV_Michael_Tenis"},
              {"en": "Franklin", "plano": "K5_GTAV_Franklin_Puerta"},
              {"en": "cambiar", "plano": "K5_GTAV_Trevor_Trio"},
              {"en": "atraco", "plano": "K5_Img_GTAO_Camara_Kortz"}]},
    {"id": "p02", "num": 2, "total": T, "titulo": "2013-2026 · EL DINERO", "capitulo": "2013-2026 · El dinero",
     "overlay": "", "anio": 2013, "etiqueta_linea": "2013-2026 · DINERO",
     "texto": ("Y después está GTA Online, el modo online que se abre en octubre de dos mil trece y no se acaba nunca. En febrero de dos mil catorce, Take-Two dijo que cerca del setenta por ciento de los jugadores de GTA V con internet ya lo había probado. "
               "Take-Two no separa sus ingresos por juego, pero sí publica su gasto recurrente: compras dentro de los "
               "juegos, monedas virtuales y contenidos extra. En el último año fiscal, que cerró en marzo de dos mil "
               "veintiséis, ese gasto subió un dieciséis por ciento y supuso el setenta y ocho por ciento de los ingresos "
               "de la compañía. Ojo: esa cifra es de toda Take-Two, no solo de GTA Online. Pero GTA Online es uno de sus "
               "grandes motores. Y un juego que sigue dando dinero cada mes no tiene por qué salir pronto."),
     "rotulos": [{"en": "octubre", "texto": "1 OCT 2013|GTA ONLINE"},
                 {"en": "dieciséis", "texto": "+16% GASTO|RECURRENTE"},
                 {"en": "setenta", "n": 2, "texto": "78% DE LOS|INGRESOS"},
                 {"en": "toda", "texto": "TODA TAKE-TWO|NO SOLO GTA"}],
     "nombres": ["Online", "octubre", "toda"],
     "planos": ["K5_GTAO_Atico_Fiesta", "K5_GTAO_Atico_Ventanal", "K5_GTAO_Dos_Hombres_Casa", "K5_Img_GTAO_Derrape_Doble", "K5_GTAO_Garaje_Neon", "K5_Img_GTAO_Plan_Golpe", "K5_Img_GTAO_Vitrina_Oro", "K5_Img_GTAO_Banda", "K5_GTAO_Aereo_Kortz", "K5_GTAO_Tuning_Garaje", "K5_Img_GTAO_Coche_Neon", "NUEVO_Cuentas_TakeTwo", "K5_GTAO_Oficina_Agentes", "K5_Img_GTAO_Coches_Noche", "K5_GTAO_Dos_Personajes", "K5_Img_GTAO_Grupo_Camion"],
     "planos_en": [{"en": "online", "plano": "K5_GTAO_Atico_Fiesta"},
              {"en": "ingresos", "plano": "NUEVO_Cuentas_TakeTwo"},
              {"en": "monedas", "plano": "K5_Img_GTAO_Vitrina_Oro"},
              {"en": "contenidos", "plano": "K5_Img_GTAO_Coche_Neon"},
              {"en": "motores", "plano": "K5_GTAO_Garaje_Neon"}]},

    # ---------------------------------------------------------------- NUEVO · EL ROL (2019-2023)
    {"id": "p03", "num": 3, "total": T, "titulo": "2019-2023 · EL ROL", "capitulo": "2019-2023 · El rol",
     "overlay": "", "anio": 2019, "etiqueta_linea": "2019-2023 · EL ROL",
     "texto": ("Y hay otra razón por la que GTA V sigue vivo: el rol. En esos servidores, la gente juega a ser policía, "
               "ladrón o taxista dentro de una ciudad de mentira. Uno de ellos, NoPixel, un servidor hecho por streamers, se vuelve enorme en Twitch en dos "
               "mil diecinueve. Según datos de terceros, GTA V fue el segundo juego más visto de la plataforma en dos mil "
               "veintitrés, y el primero en dos mil veinticuatro. Esos servidores funcionan con FiveM, un proyecto de "
               "aficionados que Rockstar había prohibido en dos mil quince, por considerarlo un servicio no autorizado. Según la prensa de entonces, Take-Two llegó a mandar investigadores privados a casa de uno de sus creadores. En "
               "agosto de dos mil veintitrés, Rockstar anuncia que compra al equipo que lo hace, Cfx.re. Ocho años después, "
               "la empresa que cerró la puerta la compra. Y el propio equipo deja claro que el acuerdo va de FiveM y RedM, "
               "no de GTA VI."),
     "rotulos": [{"en": "Twitch", "texto": "TWITCH|2019 · NOPIXEL"},
                 {"en": "segundo", "texto": "2.º JUEGO MÁS VISTO|EN TWITCH · 2023"},
                 {"en": "Cfx", "texto": "CFX.RE|COMPRADO EN 2023"},
                 {"en": "quince", "texto": "PROHIBIDO|EN 2015"}],
     "nombres": ["Twitch", "Cfx"],
     "planos": ["K5_Img_GTAV_Skyline_Rol", "K5_GTAV_Persecucion_Policia", "K5_Img_GTAV_Rol_BurgerShot", "K5_GTAO_Pizza_Moto", "K5_GTAO_Pizza_Moto_2", "K5_GTAO_Lavadero", "K5_GTAV_Ruta68_Policia", "NUEVO_Twitch_Captura", "K5_Img_GTAO_Bicis", "K5_GTAO_Paso_Inferior", "K5_Img_GTAO_Policia_Comisaria", "K5_Img_GTAO_Desguace", "K5_GTAO_Carretera_Noche", "K5_GTAO_Carretera_Monte", "K5_Img_GTAO_Jugador_Noche", "K5_GTAO_Granja_Aerea", "NUEVO_Cfx_Comunicado", "K5_GTAO_Taller_Bennys", "K5_RDR2_Pueblo_Valentine", "K5_Img_GTAO_Coche_Policia", "K5_Img_GTAO_Coche_Neon_PS5"],
     "planos_en": [{"en": "rol", "plano": "K5_Img_GTAV_Rol_BurgerShot"},
              {"en": "policía", "plano": "K5_GTAV_Persecucion_Policia"},
              {"en": "taxista", "plano": "K5_GTAO_Pizza_Moto"},
              {"en": "Twitch", "plano": "NUEVO_Twitch_Captura"},
              {"en": "prohibido", "plano": "K5_GTAV_Ruta68_Policia"},
              {"en": "Cfx", "plano": "NUEVO_Cfx_Comunicado"},
              {"en": "RedM", "plano": "K5_RDR2_Pueblo_Valentine"}]},

    # ---------------------------------------------------------------- ACTO I (cont.) · REEDICIONES (2014-2022)
    {"id": "p04", "num": 4, "total": T, "titulo": "2014-2022 · REEDICIONES", "capitulo": "2014-2022 · Reediciones",
     "overlay": "", "anio": 2014, "etiqueta_linea": "2014 · REEDICIÓN",
     "texto": ("Y mientras tanto, Rockstar vuelve a vender el mismo juego. GTA V sale en dos mil catorce para la nueva "
               "generación, y otra vez en dos mil veintidós para PlayStation cinco y Xbox Series. Eso no lo dice Rockstar, "
               "pero es la lectura de este canal: si la gente sigue comprando el mismo mapa, la urgencia de hacer otro baja."),
     "rotulos": [{"en": "catorce", "texto": "2014 · PS4 · XONE"},
                 {"en": "veintidós", "texto": "2022 · PS5 · XBOX SERIES"},
                 {"en": "mismo", "texto": "MISMO MAPA|OTRA VEZ"}],
     "nombres": [],
     "planos": ["NUEVO_Reediciones_Logos", "K5_GTAO_Colinas_Amanecer", "K5_GTAO_Autopista_Bruma", "K5_GTAO_Avion_Contraluz", "K5_GTAO_Cartel_Licores", "K5_Img_GTAO_Todoterreno", "K5_Img_GTAO_Muscle", "K5_Img_GTAO_Derrape_PS5"],
     "planos_en": [{"en": "catorce", "plano": "NUEVO_Reediciones_Logos"},
              {"en": "veintidós", "plano": "K5_Img_GTAO_Todoterreno"},
              {"en": "mapa", "plano": "K5_GTAO_Colinas_Amanecer"}]},

    # ---------------------------------------------------------------- NUEVO · GTA PLUS (2022)
    {"id": "p05", "num": 5, "total": T, "titulo": "2022 · GTA PLUS", "capitulo": "2022 · GTA Plus",
     "overlay": "", "anio": 2022, "etiqueta_linea": "2022 · GTA PLUS",
     "texto": ("Y en marzo de dos mil veintidós, Rockstar prueba otra manera de ganar dinero sin juego nuevo. Se llama GTA "
               "Plus: una suscripción mensual dentro de GTA Online. Se anuncia el veinticinco de marzo y sale cuatro días "
               "después, solo para PlayStation cinco y Xbox Series. Por una cuota al mes, el jugador recibe ventajas y "
               "recompensas que cambian cada mes. Es el mismo principio de siempre: si cada mes entra dinero, ¿para qué "
               "correr a sacar otro juego? Y no es un detalle menor. En dos mil veintiséis, el gasto recurrente supone el "
               "setenta y ocho por ciento de los ingresos de Take-Two, como vimos antes."),
     "rotulos": [{"en": "marzo", "texto": "25 MAR 2022|GTA PLUS"},
                 {"en": "cuota", "texto": "SUSCRIPCIÓN|MENSUAL"}],
     "nombres": [],
     "planos": ["NUEVO_GTAPlus_Captura", "K5_Img_GTAPlus_Quedada", "K5_Img_GTAPlus_Superdeportivo", "K5_Img_GTAO_Pareja_Helicoptero", "K5_Img_GTAPlus_Oficina", "K5_Img_GTAO_Garaje_Deportivo", "K5_Img_GTAO_Hombre_Coche", "K5_Img_GTAO_Ruleta", "K5_Img_GTAO_Exposicion", "K5_Img_GTAO_Hidroavion", "K5_Img_GTAO_Deportivo_Noche"],
     "planos_en": [{"en": "marzo", "plano": "NUEVO_GTAPlus_Captura"},
              {"en": "suscripción", "plano": "K5_Img_GTAPlus_Quedada"},
              {"en": "cuota", "plano": "K5_Img_GTAPlus_Superdeportivo"},
              {"en": "recompensas", "plano": "K5_Img_GTAO_Ruleta"}]},

    # ---------------------------------------------------------------- ACTO II · EL OTRO GRAN PROYECTO (2010-2018)
    {"id": "p06", "num": 6, "total": T, "titulo": "2010-2018 · RED DEAD REDEMPTION 2",
     "capitulo": "2010-2018 · Red Dead Redemption 2", "overlay": "", "anio": 2010, "etiqueta_linea": "2010 · RDR 2",
     "cartela": {"anio": "2010", "acto": "ACTO II", "titulo": "EL OTRO GRAN PROYECTO"},
     "final_revisado": True,  # 14 nov: voz nueva (lite); Whisper small oye entero «antes de tocar otro GTA.»
     "texto": ("Rockstar tiene a la vez otro proyecto enorme: Red Dead Redemption dos. Según Rob Nelson, de Rockstar North, "
               "el desarrollo empieza en dos mil diez, unos ocho años antes de salir. Él mismo lo cuenta a IGN: el estudio "
               "junta a todos sus equipos en uno solo, y el juego se retrasa dos veces para pulirlo. Sale el veintiséis de "
               "octubre de dos mil dieciocho en PlayStation cuatro y Xbox One. Un western enorme, con Arthur Morgan y su "
               "banda. Dan Houser ha contado en un podcast que el proyecto se fue de plazos y de presupuesto más de lo que le gustaría recordar. Ese es el tamaño del trabajo que se hace antes de tocar otro GTA."),
     "rotulos": [{"en": "diez", "texto": "2010 · INICIO"},
                 {"en": "ocho", "texto": "~8 AÑOS|DE DESARROLLO"},
                 {"en": "veintiséis", "texto": "26 OCT 2018|RED DEAD 2"},
                 {"en": "morgan", "texto": "ARTHUR MORGAN"}],
     "nombres": ["Morgan", "western"],
     "planos": ["K5_RDR2_Campamento", "K5_RDR2_Desierto_Cactus", "K5_RDR2_Bosque", "K5_RDR2_Pueblo_Ocaso", "K5_RDR2_Tren_Puente", "K5_RDR2_Pantano_Garza", "K5_RDR2_Puente_Cuerda", "K5_RDR2_Paisaje_Amanecer", "K5_RDR2_Pueblo_Atardecer", "K5_RDR2_Arthur_Caballo", "K5_RDR2_Ciervo_Bosque", "K5_RDR2_Pueblo_Caballo", "K5_RDR2_Bosque_Niebla", "K5_RDR2_Saint_Denis", "K5_RDR2_Arbol_Noche", "K5_RDR2_Valle_Lago", "NUEVO_Foto_RockstarNorth"],
     "planos_en": [{"en": "Redemption", "plano": "K5_RDR2_Campamento"},
              {"en": "western", "plano": "K5_RDR2_Desierto_Cactus"},
              {"en": "Morgan", "plano": "K5_RDR2_Arthur_Caballo"},
              {"en": "banda", "plano": "K5_RDR2_Arbol_Noche"}]},
    {"id": "p07", "num": 7, "total": T, "titulo": "2018-2019 · RED DEAD ONLINE", "capitulo": "2018-2019 · Red Dead Online",
     "overlay": "", "anio": 2018, "etiqueta_linea": "2018 · RED DEAD ONLINE",
     "texto": ("Y un mes después, el veintisiete de noviembre de dos mil dieciocho, abre en beta Red Dead Online, el modo online del juego. El juego, según Take-Two, ya suma más de ochenta y cinco millones de copias. Otra vez un mundo que no se acaba, con "
               "actualizaciones y dinero que entra cada mes. Es el mismo esquema que GTA Online. Y es lo que GTA VI hereda: "
               "un juego que no es solo una historia, sino un lugar al que volver."),
     "rotulos": [{"en": "veintisiete", "texto": "27 NOV 2018|BETA"},
                 {"en": "online", "texto": "RED DEAD ONLINE|EL MODO ONLINE"},
                 {"en": "ochenta", "texto": "+85 MILLONES|RED DEAD 2"},
                 {"en": "hereda", "texto": "LO QUE HEREDA|GTA VI"}],
     "nombres": ["Online"],
     "planos": ["K5_RDO_Jinetes_Silueta", "K5_RDO_Jinetes_Galope", "K5_RDO_Cabana", "K5_RDO_Jinete_Ocaso", "K5_RDO_Ruedas_Carro", "K5_RDO_Jinete_Nieve", "K5_RDO_Bosque_Nevado", "K5_RDO_Mirador", "K5_RDO_Tren_Ocaso", "K5_RDO_Canon_Jinetes", "K5_RDO_Contrabajo", "K5_RDO_Casa_Grupo", "K5_RDO_Noche_Luna"],
     "planos_en": [{"en": "beta", "plano": "K5_RDO_Jinetes_Silueta"},
              {"en": "online", "plano": "K5_RDO_Jinetes_Galope"},
              {"en": "lugar", "plano": "K5_RDO_Mirador"}]},

    # ---------------------------------------------------------------- ACTO III · EL CAMBIO Y EL SUSTO (2020-2022)
    {"id": "p08", "num": 8, "total": T, "titulo": "2020-2023 · DAN HOUSER SE VA", "capitulo": "2020-2023 · Dan Houser se va",
     "overlay": "", "anio": 2020, "etiqueta_linea": "2020 · HOUSER",
     "final_revisado": True,  # 12 nov: Whisper oye «frente de Jarroxdar» por «Rockstar»; el final está entero
     "cartela": {"anio": "2020", "acto": "ACTO III", "titulo": "EL CAMBIO Y EL SUSTO"},
     "texto": ("En febrero de dos mil veinte, Take-Two anuncia algo que casi nadie esperaba: Dan Houser deja Rockstar. Es "
               "cofundador de la empresa y el guionista principal de GTA V y de Red Dead Redemption dos. Según la prensa, "
               "llevaba fuera del día a día desde la primavera de dos mil diecinueve. Su último día fue el once de marzo de "
               "dos mil veinte, y no hubo motivo oficial. Un año después, en dos mil veintiuno, registra Absurd Ventures. "
               "Y en junio de dos mil veintitrés lo presenta como estudio de medios: juegos, libros, series y "
               "podcasts. Su hermano Sam sigue al frente de Rockstar."),
     "rotulos": [{"en": "febrero", "texto": "FEB 2020|HOUSER SE VA"},
                 {"en": "once", "texto": "ÚLTIMO DÍA|11 MAR 2020"},
                 {"en": "absurd", "texto": "ABSURD VENTURES|REGISTRADA 2021"},
                 {"en": "junio", "texto": "JUN 2023|ESTUDIO DE MEDIOS"}],
     "nombres": ["Houser", "Absurd"],
     "planos": ["NUEVO_Houser_Captura", "K5_GTAV_Lester_Plan", "K5_RDR2_Dutch_Arthur", "K5_RDR2_Hoguera_Guitarra", "K5_RDR2_Banda_Baile", "NUEVO_Absurd_Logo", "K5_RDR2_Campamento_Hoguera", "K5_RDR2_Campamento_Charla", "K5_RDR2_Arthur_Pueblo", "K5_RDR2_Torre_Silueta", "K5_RDR2_Lago_Chimeneas", "K5_RDR2_Banda_Pueblo", "K5_Img_JL_Abrazo_Skyline", "NUEVO_Foto_Houser"],
     "planos_en": [{"en": "Houser", "plano": "NUEVO_Houser_Captura"},
              {"en": "guionista", "plano": "K5_GTAV_Lester_Plan"},
              {"en": "Redemption", "plano": "K5_RDR2_Dutch_Arthur"},
              {"en": "Absurd", "plano": "NUEVO_Absurd_Logo"},
              {"en": "Sam", "plano": "K5_Img_JL_Abrazo_Skyline"}]},

    # ---------------------------------------------------------------- NUEVO · RUFFIAN (2020)
    {"id": "p09", "num": 9, "total": T, "titulo": "2020 · RUFFIAN", "capitulo": "2020 · Rockstar Dundee",
     "overlay": "", "anio": 2020, "etiqueta_linea": "2020 · RUFFIAN",
     "texto": ("Y mientras tanto, Rockstar crece. En octubre de dos mil veinte compra Ruffian Games, un estudio de Dundee "
               "con unos cuarenta empleados. Había hecho Crackdown dos para Microsoft y llevaba un año trabajando con "
               "Rockstar. Lo renombra Rockstar Dundee, y sus dos fundadores, Gary Liddon y Billy Thomson, siguen al frente "
               "como codirectores. Según Game Developer, era la primera compra de Rockstar en años. Y ese es el punto: para "
               "un juego que tarda años en hacerse, hacen falta manos. Eso es lectura de este canal, no un comunicado."),
     "rotulos": [{"en": "octubre", "texto": "OCT 2020|RUFFIAN GAMES"},
                 {"en": "Dundee", "texto": "DUNDEE|→ ROCKSTAR DUNDEE"},
                 {"en": "cuarenta", "texto": "~40 EMPLEADOS"}],
     "nombres": ["Dundee"],
     "planos": ["NUEVO_Ruffian_Captura", "K5_Lanz_Barco_Manos", "K5_Img_VC_Ciudad_Aerea", "K5_Img_Port_Gellhorn_Ocaso", "K5_Img_Grassrivers_Skyline", "K5_Img_VC_Persecucion_Noche", "K5_Img_Kalaga_Canon", "K5_Img_VC_Concierto", "K5_Img_Ambrosia_Moteros", "NUEVO_Foto_Dundee"],
     "planos_en": [{"en": "crece", "plano": "K5_Img_VC_Ciudad_Aerea"},
              {"en": "octubre", "plano": "NUEVO_Ruffian_Captura"},
              {"en": "manos", "plano": "K5_Lanz_Barco_Manos"}]},

    {"id": "p10", "num": 10, "total": T, "titulo": "2021 · THE TRILOGY", "capitulo": "2021 · The Trilogy",
     "overlay": "", "anio": 2021, "etiqueta_linea": "2021 · TRILOGY",
     "texto": ("En noviembre de dos mil veintiuno, Rockstar saca The Trilogy: The Definitive Edition. GTA III, Vice City y "
               "San Andreas, remasterizados en un solo paquete, veinte años después de aquella primera calle. Otra vez el "
               "mismo mundo, sin GTA nuevo. La saga seguía viva, pero sin nada nuevo que enseñar."),
     "rotulos": [{"en": "noviembre", "texto": "NOV 2021|THE TRILOGY"},
                 {"en": "veinte", "texto": "20 AÑOS DESPUÉS"}],
     "nombres": ["Trilogy"],
     "planos": ["K5_Tril_SA_Desierto", "K5_Tril_GTA3_Tren", "K5_Img_Tril_VC_Calle", "K5_Tril_SA_Grove", "K5_Img_Tril_SA_Ciudad", "K5_Tril_SA_Casinos", "K5_Tril_GTA3_Lluvia", "K5_Tril_SA_Casa"],
     "planos_en": [{"en": "Trilogy", "plano": "K5_Tril_SA_Desierto"},
              {"en": "Vice", "plano": "K5_Img_Tril_VC_Calle"},
              {"en": "veinte", "plano": "K5_Tril_GTA3_Lluvia"}]},
    {"id": "p11", "num": 11, "total": T, "titulo": "2022 · CÓMO OCURRIÓ", "capitulo": "2022 · Cómo ocurrió",
     "overlay": "", "anio": 2022, "etiqueta_linea": "2022 · FILTRACIÓN",
     "texto": ("Y en septiembre de dos mil veintidós llega el susto. Entra en los sistemas de Rockstar un chico de Oxford, "
               "Arion Kurtaj. Según el tribunal, estaba en libertad bajo fianza por otros hackeos. Según la prensa, lo hizo "
               "desde un hotel, con una televisión, un Amazon Fire Stick y un teléfono. Se llevó unos noventa clips del "
               "juego. El hacker dijo que los sacó de un canal de Slack. Eso lo afirma él, no Rockstar. Y los vídeos "
               "aparecen en el foro el dieciocho de septiembre."),
     "rotulos": [{"en": "septiembre", "texto": "SEP 2022|EL SUSTO"},
                 {"en": "kurtaj", "texto": "ARION KURTAJ|OXFORD"},
                 {"en": "hotel", "texto": "HOTEL · FIRE STICK|SEGÚN LA PRENSA"},
                 {"en": "noventa", "texto": "~90 CLIPS|DEL JUEGO"}],
     "nombres": ["Kurtaj"],
     "planos": ["K5_Mir_Monitores", "K5_Mir_Vestibulo", "NUEVO_Texto_Hechos", "K5_Img_Motel_Noche", "K5_Img_Lucia_Esposada", "K5_Mir_Telefono", "K5_Mir_Pasillo", "K5_Mir_Coche_Oscuro"],
     "planos_en": [{"en": "sistemas", "plano": "K5_Mir_Monitores"},
              {"en": "fianza", "plano": "NUEVO_Texto_Hechos"},
              {"en": "hotel", "plano": "K5_Img_Motel_Noche"},
              {"en": "teléfono", "plano": "K5_Mir_Telefono"}]},
    {"id": "p12", "num": 12, "total": T, "titulo": "2022-2023 · EL MENSAJE Y EL JUICIO",
     "capitulo": "2022-2023 · El mensaje y el juicio", "overlay": "", "anio": 2022, "etiqueta_linea": "2022 · JUICIO",
     "texto": ("El diecinueve de septiembre, Rockstar lo confirma: un tercero accedió sin permiso a sus sistemas y descargó "
               "información confidencial, incluido material de desarrollo del próximo GTA. Dice que está muy decepcionado, "
               "y que el trabajo sigue como estaba previsto. "
               "En agosto de dos mil veintitrés, en Londres, un jurado da por probado que cometió "
               "delitos informáticos, chantaje y fraude. En diciembre, el juez lo condena a un internamiento hospitalario indefinido. Seguirá en un hospital de seguridad hasta que se decida que ya no es un peligro. "
               "Rockstar contó al tribunal que el ataque le costó cinco millones de dólares, y miles "
               "de horas de trabajo."),
     "rotulos": [{"en": "diecinueve", "texto": "19 SEP 2022|ROCKSTAR LO CONFIRMA"},
                 {"en": "cinco", "texto": "5 MILLONES $|Y MILES DE HORAS"}],
     "nombres": ["Londres", "cinco"],
     "planos": ["K5_Mir_Calle_Club", "K5_Img_VC_Noria_Noche", "K5_Lanz_Preparativos", "NUEVO_Juicio_Southwark", "K5_Mir_Coche_Pista", "K5_Img_JL_Conduce_Noche", "K5_Img_VC_Peluqueria", "K5_Img_VC_Gasolinera_Noche", "K5_Mir_Pista_Avion", "K5_Img_Ambrosia_Noche", "K5_Img_VC_Skyline_Noche", "NUEVO_Foto_Southwark"],
     "planos_en": [{"en": "confirma", "plano": "K5_Img_VC_Noria_Noche"},
              {"en": "trabajo", "plano": "K5_Mir_Calle_Club"},
              {"en": "Londres", "plano": "NUEVO_Juicio_Southwark"},
              {"en": "millones", "plano": "K5_Img_VC_Skyline_Noche"}]},

    # ---------------------------------------------------------------- ACTO IV · LA ESPERA (2023-2026)
    {"id": "p13", "num": 13, "total": T, "titulo": "2023 · EL PRIMER TRÁILER", "capitulo": "2023 · El primer tráiler",
     "overlay": "", "anio": 2023, "etiqueta_linea": "2023 · TRÁILER 1",
     "cartela": {"anio": "2023", "acto": "ACTO IV", "titulo": "LA ESPERA"},
     "texto": ("En diciembre de dos mil veintitrés llega el primer tráiler. Se filtra una versión de baja calidad un día "
               "antes, y Rockstar lo publica esa misma noche. Vuelve Vice City. Y de fondo suena Love Is a Long Road, de Tom "
               "Petty, una canción de los ochenta para la ciudad de los ochenta. Por fin, el juego empezaba a parecer real."),
     "rotulos": [{"en": "diciembre", "texto": "TRÁILER 1|DIC 2023"},
                 {"en": "petty", "texto": "TOM PETTY|LOVE IS A LONG ROAD"},
                 {"en": "vice", "texto": "VICE CITY"}],
     "nombres": ["Vice", "Petty"],
     "planos": ["K5_T1_Lucia_Ventana", "K5_Img_VC_Letras", "K5_T1_Playa_Paseo", "K5_Img_Lucia_Calle", "K5_Img_VC_Neones_Policia", "K5_Img_JL_Baile_Neon", "K5_PreLoad_Club_Neon", "K5_Img_VC_Coche_Rosa"],
     "planos_en": [{"en": "diciembre", "plano": "K5_T1_Lucia_Ventana"},
              {"en": "Vice", "plano": "K5_Img_VC_Letras"},
              {"en": "Petty", "plano": "K5_Img_VC_Neones_Policia"}]},
    {"id": "p14", "num": 14, "total": T, "titulo": "2025-2026 · LOS RETRASOS", "capitulo": "2025-2026 · Los retrasos",
     "overlay": "", "anio": 2025, "etiqueta_linea": "2025 · RETRASOS",
     "texto": ("Rockstar tenía fecha para el otoño de dos mil veinticinco. En mayo de ese año la mueve al veintiséis de mayo "
               "de dos mil veintiséis. Ese mismo mes llega el segundo tráiler, con The Pointer Sisters de fondo. Y en "
               "noviembre llega el segundo retraso: diecinueve de noviembre de dos mil veintiséis. Tres fechas en poco más "
               "de un año."),
     "rotulos": [{"en": "otoño", "texto": "OTOÑO 2025|PRIMERA FECHA"},
                 {"en": "veintiséis", "texto": "RETRASO|→ 26 MAY 2026"},
                 {"en": "pointer", "texto": "THE POINTER SISTERS|HOT TOGETHER"},
                 {"en": "diecinueve", "texto": "RETRASO|→ 19 NOV 2026"}],
     "nombres": ["otoño", "veintiséis", "Pointer", "diecinueve"],
     "planos": ["K5_T2_Jason_Noche", "K5_T2_Torre_Prision", "K5_T2_Reencuentro", "K5_T2_Moto_Avioneta", "K5_Img_JL_Moto_Helicoptero", "K5_Img_Jason_Noche", "K5_Img_VC_Puerto"],
     "planos_en": [{"en": "mayo", "plano": "K5_T2_Jason_Noche"},
              {"en": "Pointer", "plano": "K5_T2_Reencuentro"},
              {"en": "diecinueve", "plano": "K5_Img_VC_Puerto"}]},
    {"id": "p15", "num": 15, "total": T, "titulo": "2025 · LO QUE SE CUENTA", "capitulo": "2025 · Lo que se cuenta desde dentro",
     "overlay": "", "anio": 2025, "etiqueta_linea": "2025 · DESDE DENTRO",
     "texto": ("Jason Schreier, de Bloomberg, escribió en redes que nadie de Rockstar creía "
               "en la ventana de otoño desde hacía tiempo. Él mismo matizó después que el retraso no era inevitable sin más. "
               "Y hay informes de crunch, de horas extra y de una vuelta a la oficina cinco días a la semana. Eso es lo que "
               "cuentan periodistas y trabajadores. No es un dato oficial, y así hay que tomarlo."),
     "rotulos": [{"en": "schreier", "texto": "JASON SCHREIER|BLOOMBERG"},
                 {"en": "crunch", "texto": "INFORMES, NO|DATOS OFICIALES"},
                 {"en": "cinco", "texto": "5 DÍAS A LA SEMANA|EN OFICINA"}],
     "nombres": ["Schreier", "crunch"],
     "planos": ["NUEVO_Schreier_Bluesky", "K5_Img_Brian_Papeles", "K5_Mir_Sofa", "K5_Img_Boobie_Despacho", "K5_Img_DreQuan_Estudio", "K5_Img_Raul_Telefono", "K5_Img_Jason_Mesa", "K5_Img_Cal_Billar"],
     "planos_en": [{"en": "Schreier", "plano": "NUEVO_Schreier_Bluesky"},
              {"en": "crunch", "plano": "K5_Mir_Sofa"},
              {"en": "oficina", "plano": "K5_Img_Boobie_Despacho"}]},

    # ---------------------------------------------------------------- NUEVO · TAKE-TWO (2026)
    {"id": "p16", "num": 16, "total": T, "titulo": "2026 · TAKE-TWO", "capitulo": "2026 · Lo que dice Take-Two",
     "overlay": "", "anio": 2026, "etiqueta_linea": "2026 · TAKE-TWO",
     "texto": ("Y ¿qué dice la empresa? Strauss Zelnick, consejero delegado de Take-Two, ha dicho en otra ocasión que nunca "
               "se han arrepentido de retrasar un juego, porque buscan la perfección. En el informe de mayo de dos mil "
               "veintiséis volvió a fijar el diecinueve de noviembre, y dijo que no iba a haber otro retraso. Para el año "
               "fiscal en curso, que va de abril de dos mil veintiséis a marzo de dos mil veintisiete, habla de récords de "
               "resultados impulsados por el lanzamiento de GTA VI."),
     "rotulos": [{"en": "Zelnick", "texto": "STRAUSS ZELNICK|TAKE-TWO"},
                 {"en": "diecinueve", "texto": "19 NOV|SIN OTRO RETRASO"},
                 {"en": "récords", "texto": "RÉCORDS|AÑO FISCAL 2027"}],
     "nombres": ["Zelnick"],
     "planos": ["NUEVO_Zelnick_Captura", "K5_Img_VC_Torres_Bahia", "K5_Img_Raul_Barco", "K5_PreLoad_Yate", "K5_Img_VC_Piscina_Aerea", "K5_T2_Moto_Agua", "K5_Img_Keys_Barcos", "K5_Img_JL_Coche", "K5_Img_Jason_Pesca", "K5_Img_Lucia_Piscina", "NUEVO_Foto_Zelnick"],
     "planos_en": [{"en": "Zelnick", "plano": "NUEVO_Zelnick_Captura"},
              {"en": "perfección", "plano": "K5_Img_VC_Torres_Bahia"},
              {"en": "diecinueve", "plano": "K5_Img_JL_Coche"},
              {"en": "récords", "plano": "K5_Img_Keys_Barcos"}]},

    # ---------------------------------------------------------------- ACTO IV · HOY (2026)
    {"id": "p17", "num": 17, "total": T, "titulo": "2026 · HOY", "capitulo": "2026 · Hoy",
     "overlay": "", "anio": 2026,
     "texto": ("Y llegamos a hoy. El diecinueve de noviembre de dos mil veintiséis sale GTA VI en PlayStation cinco y Xbox "
               "Series. Trece años después de GTA V, y un juego que sigue vendiendo: casi doscientos treinta millones de "
               "copias. Take-Two prevé para el año fiscal siguiente entre ocho mil y ocho mil doscientos millones de dólares "
               "en reservas netas, con GTA VI como motor. Y en marzo de dos mil veinticinco, Rockstar compra también Video "
               "Games Deluxe, un estudio de Sídney, fundado en dos mil trece, que pasa a llamarse Rockstar Australia. Su fundador, Brendan McNamara, "
               "había dirigido Team Bondi, y el estudio ya había trabajado con Rockstar en varias reediciones. La pregunta "
               "ya no es cuándo, sino si la espera ha valido la pena."),
     "rotulos": [{"en": "diecinueve", "texto": "19 NOV 2026|PS5 · XBOX SERIES"},
                 {"en": "trece", "texto": "13 AÑOS|DESPUÉS"},
                 {"en": "doscientos", "texto": "CASI 230 MILLONES|GTA V"},
                 {"en": "Sídney", "texto": "VIDEO GAMES DELUXE|→ ROCKSTAR AUSTRALIA"}],
     "nombres": ["Sídney"],
     "planos": ["K5_Img_JL_Atardecer_Bolsas", "K5_PreLoad_Breakdance", "K5_Img_GTAO_Coche_Explosion", "K5_Img_Kalaga_Fauna", "K5_Lanz_Pantano_Siluetas", "K5_Img_Keys_Iguana", "NUEVO_VGD_Captura", "K5_LANoire_Phelps", "K5_Img_Kalaga_Helicoptero", "K5_Img_JL_Silueta_Atardecer", "K5_Img_VC_Grafiti", "K5_Img_Keys_Calle", "K5_Img_Port_Gellhorn_Coche", "K5_Img_Keys_Bar"],
     "planos_en": [{"en": "diecinueve", "plano": "K5_Img_JL_Atardecer_Bolsas"},
              {"en": "Trece", "plano": "K5_Img_GTAO_Coche_Explosion"},
              {"en": "Sídney", "plano": "NUEVO_VGD_Captura"},
              {"en": "Bondi", "plano": "K5_LANoire_Phelps"},
              {"en": "espera", "plano": "K5_Img_JL_Silueta_Atardecer"}]},

    # ---------------------------------------------------------------- CIERRE
    {"id": "cierre", "num": None, "titulo": "", "overlay": "", "capitulo": "Cierre", "anio": 2026,
     "texto": ("Y aquí cerramos. Trece años de espera: primero porque GTA V seguía dando dinero, después porque la saga tenía "
               "otros proyectos, un cambio de personas y un susto que acabó en un tribunal. ¿Tú qué crees: fue una espera "
               "justa, o demasiada? Déjamelo en los comentarios, que quiero ver qué opina la gente. Si te ha gustado, "
               "suscríbete, que el diecinueve vamos a estar por aquí. Nos vemos en Leónida."),
     "rotulos": [{"en": "trece", "texto": "13 AÑOS|DE ESPERA"},
                 {"en": "comentarios", "texto": "¿FUE UNA ESPERA|JUSTA?"}],
     "nombres": ["Trece", "comentarios"],
     "planos": ["K5_Img_JL_Arbol_Atardecer", "K5_Img_JL_Lucia_Coche", "K5_Img_Kalaga_Kayak", "K5_Img_Grassrivers_Aldea", "K5_Img_Ambrosia_Ocaso", "K5_Img_Keys_Fondo", "K5_Img_VC_Rascacielos_Bahia"],
     "planos_en": [{"en": "Trece", "plano": "K5_Img_JL_Arbol_Atardecer"},
              {"en": "comentarios", "plano": "K5_Img_JL_Lucia_Coche"}]},
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