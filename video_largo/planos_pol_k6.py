"""Vídeo 6 (guion_pol), 15 nov 2026: planos nuevos con material oficial 4K, capturas propias, tarjetas y fotos de Commons.
Genera trozos_pol_4k.csv (prefijo K6_) y comprueba que cada bloque tiene imagen suficiente para su voz.
Uso: python planos_pol_k6.py  (escribe trozos_pol_4k.csv junto a este archivo)"""
import ast, csv, pathlib, sys

AQUI = pathlib.Path(__file__).parent
RAW = "https://raw.githubusercontent.com/DichoYHecho/leonida-al-dia/videos-5-7/video_largo/"
V4 = "https://videos-rockstargames-com.akamaized.net/v4/{}/flv/en-us-2160p.mp4"
FUENTES = {  # clave: (url, sin bandas)
    "Trilogy_4K": (V4.format("8ta2r546"), False),
    "Bully_Aniv": ("https://videos-rockstargames-com.akamaized.net/v4/totcka8o/flv/en-us-1080p.mp4", True),
    "GTAV_PS5_4K": (V4.format("r3too449"), False),
    "GTAO_CE_4K": (V4.format("8rakra67"), True),
    "GTAO_PS5_4K": (V4.format("1s626s55"), True),
    "GTAO_Safehouse_4K": (V4.format("to78rk1o"), False),
    "GTAO_Cluckin_4K": (V4.format("r3175t5r"), False),
    "GTAO_Vigero_4K": (V4.format("k1t75kk6"), True),
    "GTAO_Kanjo_4K": (V4.format("3ra4t562"), True),
    "GTAO_Bounties_4K": (V4.format("oa46rs8r"), False),
    "GTAO_Sabotage_4K": (V4.format("r50k6mmg"), False),
    "GTAO_Pizza_4K": (V4.format("aro34sg4"), True),
    "GTAO_Luiva_4K": (V4.format("203as2rs"), False),
}
# trozos de vídeo: nombre -> (fuente, inicio, fin, qué se ve)
VID = {
    "K6_Tril_Vinewood": ("Trilogy_4K", 20.25, 21.38, "The Trilogy: el cartel de Vinewood con un helicóptero"),
    "K6_Tril_Coche_Lluvia": ("Trilogy_4K", 27.15, 28.35, "The Trilogy: un coche bajo la lluvia"),
    "K6_Tril_CJ_Coche": ("Trilogy_4K", 36.12, 37.31, "The Trilogy: CJ junto a un coche blanco en el bosque"),
    "K6_Tril_Coche_Vuela": ("Trilogy_4K", 47.92, 49.15, "The Trilogy: un coche salta por los aires bajo la lluvia"),
    "K6_Bully_Logo": ("Bully_Aniv", 10.10, 11.83, "Bully: Anniversary Edition, logo"),
    "K6_GTAV_Logo_Ciudad": ("GTAV_PS5_4K", 4.20, 7.20, "Logo de GTA V sobre Los Santos de noche"),
    "K6_GTAV_Avion_Montes": ("GTAV_PS5_4K", 32.40, 33.50, "GTA V: una avioneta sobre los montes"),
    "K6_GTAV_Trevor_Casa": ("GTAV_PS5_4K", 45.80, 46.80, "GTA V: Trevor y Michael en una casa"),
    "K6_GTAO_Aereo_LS": ("GTAO_CE_4K", 0.30, 4.80, "Los Santos desde el aire"),
    "K6_GTAO_Skyline_Atardecer": ("GTAO_CE_4K", 6.20, 8.00, "Skyline de Los Santos al atardecer"),
    "K6_GTAO_Autopista": ("GTAO_CE_4K", 10.40, 12.20, "Atasco en la autopista con el centro detrás"),
    "K6_GTAO_Torre_Palmera": ("GTAO_CE_4K", 23.40, 24.40, "Un rascacielos y una palmera en contrapicado"),
    "K6_GTAO_Barcos_Puente": ("GTAO_CE_4K", 28.50, 30.00, "Lanchas junto a un puente al atardecer"),
    "K6_GTAO_Helicoptero_Carga": ("GTAO_CE_4K", 36.40, 37.60, "Un helicóptero levanta un contenedor"),
    "K6_GTAO_Coche_Calavera": ("GTAO_CE_4K", 41.00, 42.10, "Un coche con una calavera de noche"),
    "K6_GTAO_Hangar": ("GTAO_PS5_4K", 15.30, 16.60, "Un hangar con un camión"),
    "K6_GTAO_Lowriders": ("GTAO_PS5_4K", 26.60, 27.60, "Tres lowriders por una avenida"),
    "K6_GTAO_Faro": ("GTAO_PS5_4K", 32.10, 33.30, "Un faro junto al mar"),
    "K6_GTAO_Puente_Ciudad": ("GTAO_PS5_4K", 46.30, 48.00, "Un puente de hierro con el centro detrás"),
    "K6_GTAO_Casa_Colinas": ("GTAO_Safehouse_4K", 2.10, 4.00, "Una casa en las colinas"),
    "K6_GTAO_Villa": ("GTAO_Safehouse_4K", 6.30, 7.40, "Entrada de una villa"),
    "K6_GTAO_Barco_Atardecer": ("GTAO_Safehouse_4K", 25.60, 26.80, "Un barco al atardecer"),
    "K6_GTAO_Michael": ("GTAO_Safehouse_4K", 37.20, 38.50, "Michael De Santa sentado"),
    "K6_GTAO_Calle_Noche": ("GTAO_Safehouse_4K", 41.50, 44.50, "Un coche por una calle mojada de noche"),
    "K6_GTAO_Moto_Agua": ("GTAO_Safehouse_4K", 45.80, 46.80, "Una moto de agua"),
    "K6_GTAO_Taxis": ("GTAO_Safehouse_4K", 50.00, 51.10, "Taxis por una calle"),
    "K6_GTAO_Policia_Camion": ("GTAO_Safehouse_4K", 51.40, 52.80, "Un coche de policía y un camión"),
    "K6_GTAO_Policia_Charla": ("GTAO_Cluckin_4K", 7.70, 9.10, "Un policía habla con unos jugadores"),
    "K6_GTAO_Todoterreno": ("GTAO_Cluckin_4K", 13.70, 14.80, "Un todoterreno rojo"),
    "K6_GTAO_Fila_Policias": ("GTAO_Cluckin_4K", 15.00, 16.60, "Policías en fila"),
    "K6_GTAO_Calle_Coche": ("GTAO_Vigero_4K", 3.70, 5.00, "Calle de Los Santos con un coche"),
    "K6_GTAO_Derrape": ("GTAO_Vigero_4K", 6.80, 8.00, "Un coche rojo derrapa"),
    "K6_GTAO_Tunel": ("GTAO_Vigero_4K", 11.30, 12.90, "Dos coches en un túnel"),
    "K6_GTAO_Coche_Atardecer": ("GTAO_Kanjo_4K", 3.60, 5.20, "Un coche por una calle al atardecer"),
    "K6_GTAO_Derrape_Noche": ("GTAO_Kanjo_4K", 9.80, 11.80, "Dos coches derrapan de noche"),
    "K6_GTAO_Garaje_Noche": ("GTAO_Bounties_4K", 2.10, 3.50, "Coches de noche junto a un local"),
    "K6_GTAO_Persecucion": ("GTAO_Bounties_4K", 10.00, 11.30, "Una persecución por un barrio al atardecer"),
    "K6_GTAO_Conversacion": ("GTAO_Sabotage_4K", 5.50, 6.70, "Dos personajes hablan en una calle"),
    "K6_GTAO_Calle_Palmeras": ("GTAO_Pizza_4K", 7.60, 8.80, "Una calle con palmeras y gente"),
    "K6_GTAO_Desierto": ("GTAO_Luiva_4K", 7.60, 8.80, "Un coche por la carretera del desierto al atardecer"),
}
# imágenes: nombre -> (carpeta, archivo, segundos máximos, qué se ve)
I4, I2 = "imagenes_4k", "imagenes_2k"
IMG = {}
for n in ["Tril_GTA3_Policia", "Tril_GTA3_Lanzallamas", "Tril_GTA3_Persecucion_Lluvia", "Tril_GTA3_Coche_Puente",
          "Tril_VC_Tommy_OceanView", "Tril_VC_Hotel_Lluvia", "Tril_VC_Tommy_Moto", "Tril_VC_Tommy_Lance",
          "Tril_SA_Coche_Noche", "Tril_SA_Grove", "Tril_SA_CJ_Lancha", "Tril_SA_CJ_Moto",
          "GTAV_Helicoptero", "GTAV_Ciudad_Palmeras", "GTAO_Personajes", "GTAO_Coche_Garaje", "GTAO_Coche_Rayas",
          "VI_Descapotable", "VI_Buzo_Cayos", "VI_Hidrodeslizador", "VI_Playa", "VI_Fiesta_Piscina", "VI_Minigolf",
          "VI_Jason_Moto", "VI_Jason_Coche", "VI_Bar", "VI_Lucia_Coche", "VI_Raul", "VI_Conversacion", "VI_Estudio",
          "VI_Jason_Conduce", "VI_Bosque"]:
    IMG["K6_Img_" + n] = (I4, f"K6_{n}.jpg", 8, "Imagen oficial 4K de Rockstar: " + n.replace("_", " "))
for n in ["Clifford_Killscreen", "Hansard_Lores", "VC_Demanda", "ESRB_AO", "FTC_Acuerdo", "Bully_Juez", "Bully_Profesores",
          "Thompson_Cargos", "Lohan_Fortune", "Target_AFP", "OpenIV", "SharkCards_GI", "Trilogy_NME", "Hackeo_Guardian",
          "Despidos_Register", "Juicio_Aftermath", "MiamiBeach_WLRN", "Tortura_CNBC"]:
    IMG["K6_Cap_" + n] = (I2, f"K6_{n}.png", 8, "Captura propia de prensa (titular y fecha): " + n.replace("_", " "))
for n in ["Clifford", "Brasil", "11S", "HotCoffee", "Australia", "Bully_Juez", "Thompson", "Target", "OpenIV", "Despidos",
          "Miami", "Formula"]:
    IMG["K6_Tarjeta_" + n] = (I2, f"K6_Tarjeta_{n}.png", 8, "Tarjeta propia con los datos y su fuente: " + n)
IMG["K6_Panel_GTA1"] = (I2, "K6_Panel_GTA1.jpg", 8, "Carátula oficial de GTA (1997) en un panel")
for n in ["Supremo_Florida", "Juzgado_MiamiDade", "MiamiBeach_Noche"]:
    IMG["K6_Foto_" + n] = (I2, f"K6_Foto_{n}.jpg", 8, "Foto de Wikimedia Commons: " + n.replace("_", " "))

# planos por bloque: (lista en orden, anclas {palabra: plano})
PLAN = {
    "hook": (["K6_GTAO_Aereo_LS", "K6_Bully_Logo", "K6_Panel_GTA1", "K6_Tril_Coche_Vuela", "K6_Img_VI_Hidrodeslizador",
              "K6_Img_VI_Descapotable", "K6_GTAO_Desierto", "K6_Img_VI_Buzo_Cayos"],
             {"publicista": "K6_Panel_GTA1", "despidos": "K6_Img_VI_Descapotable"}),
    "p01": (["K6_GTAO_Skyline_Atardecer", "K6_Tarjeta_Clifford", "K6_Cap_Clifford_Killscreen", "K6_Cap_Hansard_Lores",
             "K6_Tarjeta_Brasil", "K6_GTAO_Coche_Atardecer", "K6_GTAO_Calle_Palmeras"],
            {"clifford": "K6_Tarjeta_Clifford", "creadores": "K6_Cap_Clifford_Killscreen", "lores": "K6_Cap_Hansard_Lores",
             "brasil": "K6_Tarjeta_Brasil"}),
    "p02": (["K6_Tril_Coche_Lluvia", "K6_Img_Tril_GTA3_Lanzallamas", "K6_Tarjeta_11S", "K6_Img_Tril_GTA3_Policia",
             "K6_Img_Tril_GTA3_Coche_Puente", "K6_Img_Tril_GTA3_Persecucion_Lluvia"],
            {"septiembre": "K6_Tarjeta_11S", "policía": "K6_Img_Tril_GTA3_Policia",
             "finales": "K6_Img_Tril_GTA3_Persecucion_Lluvia"}),
    "p03": (["K6_Img_Tril_VC_Tommy_OceanView", "K6_Img_Tril_VC_Hotel_Lluvia", "K6_Cap_VC_Demanda",
             "K6_Img_Tril_VC_Tommy_Lance", "K6_Img_Tril_VC_Tommy_Moto"],
            {"vice": "K6_Img_Tril_VC_Tommy_OceanView", "haitiana": "K6_Img_Tril_VC_Hotel_Lluvia",
             "federal": "K6_Cap_VC_Demanda"}),
    "p04": (["K6_Img_Tril_SA_Grove", "K6_Cap_ESRB_AO", "K6_Tril_CJ_Coche", "K6_Tarjeta_HotCoffee", "K6_Cap_FTC_Acuerdo",
             "K6_Img_Tril_SA_Coche_Noche"],
            {"hot": "K6_Img_Tril_SA_Grove", "veinte": "K6_Cap_ESRB_AO", "veinticuatro": "K6_Tarjeta_HotCoffee",
             "federal": "K6_Cap_FTC_Acuerdo"}),
    "p05": (["K6_Img_Tril_SA_CJ_Lancha", "K6_Tarjeta_Australia", "K6_Tril_Vinewood", "K6_Img_Tril_SA_CJ_Moto",
             "K6_GTAV_Logo_Ciudad"],
            {"australia": "K6_Img_Tril_SA_CJ_Lancha", "revocó": "K6_Tarjeta_Australia", "julio": "K6_GTAV_Logo_Ciudad"}),
    "p06": (["K6_Bully_Logo_2", "K6_Foto_Juzgado_MiamiDade", "K6_Tarjeta_Bully_Juez", "K6_Cap_Bully_Juez",
             "K6_Cap_Bully_Profesores"],
            {"molestia": "K6_Foto_Juzgado_MiamiDade", "juez": "K6_Tarjeta_Bully_Juez",
             "coalición": "K6_Cap_Bully_Profesores"}),
    "p07": (["K6_Foto_Supremo_Florida", "K6_GTAO_Autopista", "K6_Img_GTAV_Helicoptero", "K6_GTAO_Puente_Ciudad",
             "K6_Tarjeta_Thompson", "K6_Cap_Thompson_Cargos"],
            {"thompson": "K6_Foto_Supremo_Florida", "veintisiete": "K6_Tarjeta_Thompson",
             "inhabilitó": "K6_Cap_Thompson_Cargos"}),
    "p08": (["K6_GTAV_Logo_Ciudad_2", "K6_GTAV_Trevor_Casa", "K6_Cap_Tortura_CNBC", "K6_Img_GTAV_Ciudad_Palmeras",
             "K6_GTAO_Torre_Palmera", "K6_GTAV_Avion_Montes", "K6_GTAO_Barcos_Puente", "K6_GTAO_Faro"],
            {"diecisiete": "K6_GTAV_Logo_Ciudad_2", "tortura": "K6_Cap_Tortura_CNBC"}),
    "p09": (["K6_Cap_Lohan_Fortune", "K6_Img_GTAO_Coche_Garaje", "K6_GTAO_Helicoptero_Carga", "K6_GTAO_Lowriders",
             "K6_GTAO_Villa", "K6_GTAO_Casa_Colinas", "K6_GTAO_Michael"],
            {"lindsay": "K6_Cap_Lohan_Fortune", "2016": "K6_GTAO_Villa"}),
    "p10": (["K6_GTAO_Calle_Noche", "K6_Cap_Target_AFP", "K6_Tarjeta_Target", "K6_GTAO_Taxis", "K6_GTAO_Calle_Coche",
             "K6_Img_GTAO_Personajes"],
            {"australia": "K6_Cap_Target_AFP", "cuarenta": "K6_Tarjeta_Target"}),
    "p11": (["K6_GTAO_Derrape", "K6_Cap_OpenIV", "K6_Tarjeta_OpenIV", "K6_GTAO_Tunel", "K6_GTAO_Derrape_Noche",
             "K6_GTAO_Garaje_Noche"],
            {"openiv": "K6_Cap_OpenIV", "reseñas": "K6_Tarjeta_OpenIV"}),
    "p12": (["K6_Img_GTAO_Coche_Rayas", "K6_Cap_SharkCards_GI", "K6_GTAO_Hangar", "K6_GTAO_Coche_Calavera",
             "K6_GTAO_Persecucion", "K6_GTAO_Barco_Atardecer"],
            {"shark": "K6_Img_GTAO_Coche_Rayas", "sarwar": "K6_Cap_SharkCards_GI"}),
    "p13": (["K6_Tril_Coche_Lluvia_2", "K6_Cap_Trilogy_NME", "K6_GTAO_Moto_Agua", "K6_Img_VI_Jason_Coche",
             "K6_GTAO_Todoterreno"],
            {"disculpas": "K6_Cap_Trilogy_NME"}),
    "p14": (["K6_Cap_Hackeo_Guardian", "K6_Img_VI_Estudio"],
            {"septiembre": "K6_Cap_Hackeo_Guardian"}),
    "p14b": (["K6_Img_VI_Raul", "K6_Cap_Despidos_Register", "K6_Tarjeta_Despidos", "K6_Cap_Juicio_Aftermath",
              "K6_Img_VI_Conversacion"],
             {"octubre": "K6_Cap_Despidos_Register", "confidencial": "K6_Tarjeta_Despidos",
              "glasgow": "K6_Cap_Juicio_Aftermath"}),
    "p15": (["K6_Img_VI_Playa", "K6_Foto_MiamiBeach_Noche", "K6_Cap_MiamiBeach_WLRN", "K6_Tarjeta_Miami",
             "K6_Img_VI_Fiesta_Piscina"],
            {"miami": "K6_Foto_MiamiBeach_Noche", "emisora": "K6_Cap_MiamiBeach_WLRN", "contrato": "K6_Tarjeta_Miami"}),
    "p16": (["K6_Img_VI_Lucia_Coche", "K6_Tarjeta_Formula", "K6_Img_VI_Bar", "K6_Img_VI_Jason_Moto", "K6_GTAO_Conversacion"],
            {"publicidad": "K6_Tarjeta_Formula"}),
    "cierre": (["K6_Img_VI_Minigolf", "K6_Img_VI_Jason_Conduce", "K6_Img_VI_Bosque", "K6_GTAO_Policia_Charla",
                "K6_GTAO_Fila_Policias", "K6_GTAO_Policia_Camion"],
               {}),
}
# segundos tramos de una misma fuente (otro trozo distinto, sin solapar)
VID["K6_Bully_Logo_2"] = ("Bully_Aniv", 0.82, 5.52, "Bully: tarjeta de clasificación ESRB «Teen» del tráiler")
VID["K6_GTAV_Logo_Ciudad_2"] = ("GTAV_PS5_4K", 4.20, 7.20, "")  # se resuelve abajo: no se puede repetir
VID["K6_Tril_Coche_Lluvia_2"] = ("Trilogy_4K", 47.92, 49.15, "")
del VID["K6_GTAV_Logo_Ciudad_2"], VID["K6_Tril_Coche_Lluvia_2"]
PLAN["p08"][0][0] = "K6_GTAV_Logo_Ciudad"; PLAN["p08"][1]["diecisiete"] = "K6_GTAV_Logo_Ciudad"
PLAN["p05"][0][-1] = "K6_GTAO_Aereo_LS_2"; PLAN["p05"][1]["julio"] = "K6_Img_Tril_SA_CJ_Moto"
VID["K6_GTAO_Aereo_LS_2"] = ("GTAO_CE_4K", 4.80, 6.00, "Los Santos desde el aire (final del plano)")
PLAN["p05"][0][-1] = "K6_GTAO_Faro"; PLAN["p08"][0].remove("K6_GTAO_Faro"); del VID["K6_GTAO_Aereo_LS_2"]
PLAN["p13"][0][0] = "K6_Tril_Coche_Vuela"; PLAN["hook"][0].remove("K6_Tril_Coche_Vuela")


# 15 nov: más material para los bloques que iban cortos (GTA Online 4K, logo de The Trilogy, tarjeta de The Trilogy)
FUENTES["GTAO_MoneyFronts_4K"] = (V4.format("334ek667"), False)
FUENTES["GTAO_Kortz_4K"] = (V4.format("a0a0rre4"), False)
FUENTES["GTAO_Drift_4K"] = (V4.format("arrkr814"), False)
VID.update({
    "K6_Tril_Logo": ("Trilogy_4K", 49.92, 54.88, "Logo de GTA: The Trilogy – The Definitive Edition"),
    "K6_GTAO_Aereo_LS_2": ("GTAO_CE_4K", 4.85, 5.95, "Los Santos desde el aire (final del plano)"),
    "K6_GTAO_Moto_Callejon": ("GTAO_Pizza_4K", 0.10, 1.60, "Una moto en un callejón al atardecer"),
    "K6_GTAO_Coche_Luces": ("GTAO_Vigero_4K", 2.40, 3.40, "Un coche con luces de neón bajo un puente"),
    "K6_GTAO_Cluckin_Noche": ("GTAO_Cluckin_4K", 6.00, 7.50, "Un coche entra de noche en un almacén"),
    "K6_GTAO_Negocio_Tapadera": ("GTAO_MoneyFronts_4K", 4.00, 5.10, "Fachada de un negocio tapadera"),
    "K6_GTAO_Plan_Maqueta": ("GTAO_Kortz_4K", 4.10, 5.70, "Dos personajes planean un golpe sobre una maqueta"),
    "K6_GTAO_Ladron_Atardecer": ("GTAO_Kortz_4K", 8.90, 9.90, "Un ladrón en un tejado al atardecer"),
    "K6_GTAO_Laseres": ("GTAO_Kortz_4K", 16.10, 17.40, "Láseres de seguridad"),
    "K6_GTAO_Coches_Salida": ("GTAO_Kortz_4K", 21.10, 23.40, "Coches salen de un aparcamiento"),
    "K6_GTAO_Garaje_Drift": ("GTAO_Drift_4K", 2.10, 3.50, "Coches en un garaje"),
    "K6_GTAO_Drift_Humo": ("GTAO_Drift_4K", 6.40, 7.50, "Un coche derrapa entre humo"),
    "K6_GTAO_Calle_Drift": ("GTAO_Drift_4K", 7.80, 9.60, "Coches por una calle con semáforos"),
    "K6_GTAO_Patio_Coches": ("GTAO_Drift_4K", 16.90, 18.10, "Dos coches en un patio"),
})
for n in ["VI_Caminan", "VI_Lucia_Bar"]:
    IMG["K6_Img_" + n] = (I4, f"K6_{n}.jpg", 8, "Imagen oficial 4K de Rockstar: " + n.replace("_", " "))
IMG["K6_Tarjeta_Trilogy"] = (I2, "K6_Tarjeta_Trilogy.png", 8, "Tarjeta propia con los datos y su fuente: Trilogy")
PLAN["p05"] = (["K6_Img_Tril_SA_CJ_Lancha", "K6_Tarjeta_Australia", "K6_Tril_Vinewood", "K6_GTAO_Faro",
                "K6_GTAO_Aereo_LS_2", "K6_GTAO_Moto_Callejon", "K6_Img_Tril_SA_CJ_Moto"],
               {"australia": "K6_Img_Tril_SA_CJ_Lancha", "revocó": "K6_Tarjeta_Australia", "julio": "K6_GTAO_Aereo_LS_2"})
PLAN["p07"][0][2:2] = ["K6_GTAO_Coche_Luces", "K6_GTAO_Cluckin_Noche"]
PLAN["p08"] = (["K6_GTAV_Logo_Ciudad", "K6_GTAV_Trevor_Casa", "K6_Cap_Tortura_CNBC", "K6_GTAO_Torre_Palmera",
                "K6_GTAV_Avion_Montes", "K6_GTAO_Barcos_Puente", "K6_GTAO_Coches_Salida", "K6_GTAO_Calle_Drift",
                "K6_Img_GTAV_Ciudad_Palmeras"],
               {"diecisiete": "K6_GTAV_Logo_Ciudad", "tortura": "K6_Cap_Tortura_CNBC"})
PLAN["p09"] = (["K6_Cap_Lohan_Fortune", "K6_GTAO_Helicoptero_Carga", "K6_GTAO_Lowriders", "K6_GTAO_Villa",
                "K6_GTAO_Casa_Colinas", "K6_GTAO_Michael", "K6_GTAO_Patio_Coches", "K6_GTAO_Garaje_Drift",
                "K6_Img_GTAO_Coche_Garaje"],
               {"lindsay": "K6_Cap_Lohan_Fortune", "2016": "K6_GTAO_Villa"})
PLAN["p11"] = (["K6_GTAO_Derrape", "K6_Cap_OpenIV", "K6_GTAO_Tunel", "K6_GTAO_Derrape_Noche", "K6_GTAO_Garaje_Noche",
                "K6_GTAO_Drift_Humo", "K6_GTAO_Ladron_Atardecer", "K6_Tarjeta_OpenIV"],
               {"openiv": "K6_Cap_OpenIV", "reseñas": "K6_Tarjeta_OpenIV"})
PLAN["p12"] = (["K6_GTAO_Negocio_Tapadera", "K6_Cap_SharkCards_GI", "K6_GTAO_Hangar", "K6_GTAO_Coche_Calavera",
                "K6_GTAO_Persecucion", "K6_GTAO_Barco_Atardecer", "K6_GTAO_Plan_Maqueta", "K6_Img_GTAO_Coche_Rayas"],
               {"shark": "K6_GTAO_Negocio_Tapadera", "sarwar": "K6_Cap_SharkCards_GI"})
PLAN["p13"] = (["K6_Tril_Logo", "K6_Tril_Coche_Vuela", "K6_Cap_Trilogy_NME", "K6_GTAO_Moto_Agua", "K6_GTAO_Todoterreno",
                "K6_Tarjeta_Trilogy"],
               {"noviembre": "K6_Tril_Logo", "disculpas": "K6_Cap_Trilogy_NME", "tienda": "K6_Tarjeta_Trilogy"})
PLAN["p14"] = (["K6_Cap_Hackeo_Guardian", "K6_GTAO_Laseres", "K6_Img_VI_Estudio"],
               {"septiembre": "K6_Cap_Hackeo_Guardian"})
PLAN["cierre"] = (["K6_GTAO_Policia_Charla", "K6_GTAO_Fila_Policias", "K6_GTAO_Policia_Camion", "K6_Img_VI_Minigolf",
                   "K6_Img_VI_Jason_Conduce", "K6_Img_VI_Caminan", "K6_Img_VI_Bosque"], {})
PLAN["p16"][0].insert(-1, "K6_Img_VI_Lucia_Bar")
VID["K6_GTAO_Humo"] = ("GTAO_MoneyFronts_4K", 20.40, 21.60, "Una nube de humo sobre la carretera")
VID["K6_GTAO_Drift_Rampa"] = ("GTAO_Drift_4K", 15.10, 16.00, "Coches derrapan en una rampa")
PLAN["p02"][0].remove("K6_Img_Tril_GTA3_Coche_Puente")
PLAN["p13"][0].insert(3, "K6_Img_Tril_GTA3_Coche_Puente")
PLAN["p11"][0][-1:-1] = ["K6_GTAO_Humo", "K6_GTAO_Drift_Rampa"]
PLAN["p14"][0].insert(2, "K6_Img_VI_Jason_Coche")

# 15 nov (2): 9 capturas más y menos anclas (cada ancla recorta la imagen anterior y se pierde imagen)
for n in ["Clifford_GD", "11S_MCV", "VC_Censura", "SA_AO_GD", "Australia_Stevivor", "Thompson_Bully_GD",
          "Target_CollectiveShout", "OpenIV_PCGamer", "Trilogy_TechRadar"]:
    IMG["K6_Cap_" + n] = (I2, f"K6_{n}.png", 8, "Captura propia de prensa (titular y fecha): " + n.replace("_", " "))
for b, cap, pos in [("p01", "K6_Cap_Clifford_GD", 3), ("p02", "K6_Cap_11S_MCV", 2), ("p03", "K6_Cap_VC_Censura", 4),
                    ("p04", "K6_Cap_SA_AO_GD", 2), ("p05", "K6_Cap_Australia_Stevivor", 3),
                    ("p06", "K6_Cap_Thompson_Bully_GD", 2), ("p10", "K6_Cap_Target_CollectiveShout", 3),
                    ("p11", "K6_Cap_OpenIV_PCGamer", 3), ("p13", "K6_Cap_Trilogy_TechRadar", 4)]:
    PLAN[b][0].insert(pos, cap)
MENOS_ANCLAS = {
    "p01": {"clifford": "K6_Tarjeta_Clifford", "brasil": "K6_Tarjeta_Brasil"},
    "p02": {"septiembre": "K6_Tarjeta_11S", "policía": "K6_Img_Tril_GTA3_Policia"},
    "p03": {"haitiana": "K6_Cap_VC_Demanda"},
    "p04": {"veinte": "K6_Cap_ESRB_AO", "veinticuatro": "K6_Tarjeta_HotCoffee"},
    "p05": {"revocó": "K6_Tarjeta_Australia"},
    "p06": {"juez": "K6_Tarjeta_Bully_Juez", "coalición": "K6_Cap_Bully_Profesores"},
    "p07": {"veintisiete": "K6_Tarjeta_Thompson"},
    "p08": {"tortura": "K6_Cap_Tortura_CNBC"},
    "p09": {"lindsay": "K6_Cap_Lohan_Fortune"},
    "p10": {"cuarenta": "K6_Tarjeta_Target"},
    "p11": {"openiv": "K6_Cap_OpenIV"},
    "p12": {"sarwar": "K6_Cap_SharkCards_GI"},
    "p13": {"disculpas": "K6_Cap_Trilogy_NME"},
    "p14b": {"octubre": "K6_Cap_Despidos_Register", "glasgow": "K6_Cap_Juicio_Aftermath"},
    "p15": {"miami": "K6_Foto_MiamiBeach_Noche", "contrato": "K6_Tarjeta_Miami"},
}
for b, anc in MENOS_ANCLAS.items():
    PLAN[b] = (PLAN[b][0], anc)
PLAN["p03"][0].remove("K6_Cap_VC_Demanda"); PLAN["p03"][0].insert(2, "K6_Cap_VC_Demanda")
# 15 nov (3): reparto para los bloques cortos
for n in ["Tortura", "SharkCards"]:
    IMG["K6_Tarjeta_" + n] = (I2, f"K6_Tarjeta_{n}.png", 8, "Tarjeta propia con los datos y su fuente: " + n)
IMG["K6_Img_VI_Brian_Coche"] = (I4, "K6_VI_Brian_Coche.jpg", 8, "Imagen oficial 4K de Rockstar: VI Brian Coche")
PLAN["p03"][0].remove("K6_Img_Tril_VC_Tommy_Moto"); PLAN["p07"][0].insert(3, "K6_Img_Tril_VC_Tommy_Moto")
PLAN["p08"][0].insert(5, "K6_Tarjeta_Tortura")
PLAN["p12"][0].insert(4, "K6_Tarjeta_SharkCards")
PLAN["p16"][0].remove("K6_GTAO_Conversacion"); PLAN["p09"][0].insert(4, "K6_GTAO_Conversacion")
PLAN["p14b"][0].insert(3, "K6_Img_VI_Brian_Coche")
for b, anc in {"p06": {"juez": "K6_Tarjeta_Bully_Juez"}, "p09": {}, "p10": {}, "p12": {},
               "p14b": {"glasgow": "K6_Cap_Juicio_Aftermath"}, "p15": {"contrato": "K6_Tarjeta_Miami"}}.items():
    PLAN[b] = (PLAN[b][0], anc)
# 15 nov (3): no dejar una imagen larga justo antes de un ancla (se recorta a 1 s y falta material)
for b, mover, tras in [("p06", "K6_Cap_Thompson_Bully_GD", "K6_Tarjeta_Bully_Juez"),
                       ("p07", "K6_Cap_Thompson_Cargos", "K6_Tarjeta_Thompson"),
                       ("p08", "K6_Tarjeta_Tortura", "K6_Cap_Tortura_CNBC")]:
    PLAN[b][0].remove(mover); PLAN[b][0].insert(PLAN[b][0].index(tras) + 1, mover)
PLAN["p06"] = (PLAN["p06"][0], {}); PLAN["p07"] = (PLAN["p07"][0], {})


def lento(dur):
    return 1.25 if dur < 2.4 else 1.0


filas = []
for n, (f, a, z, que) in VID.items():
    filas.append([n, "K6_Video", f"{a:.2f}", f"{z - a:.2f}", que, "0.5", "principal", "no",
                  "vídeo 6 · fuente oficial " + FUENTES[f][0], f, lento(z - a)])
for n, (carp, arch, seg, que) in IMG.items():
    filas.append([n, "K6_Imagenes", "0", str(seg), que, "0.5", "principal", "no", "vídeo 6",
                  f"Imagen:{RAW}{carp}/{arch}", 1])
with open(AQUI / "trozos_pol_4k.csv", "w", encoding="utf-8", newline="") as h:
    w = csv.writer(h)
    w.writerow(["Trozo", "Grupo", "Inicio (s)", "Duración (s)", "Qué se ve", "Foco (0 izquierda - 1 derecha)", "Uso",
                "Sonido", "Notas", "Vídeo", "Lento"])
    w.writerows(filas)

# comprobación: duración disponible por bloque frente a la voz estimada
dur = {n: (z - a) * lento(z - a) for n, (f, a, z, _) in VID.items()}
dur.update({n: v[2] for n, v in IMG.items()})
guion = (AQUI / "guion_pol.py").read_text(encoding="utf-8")
lista = next(x.value for x in ast.parse(guion).body if isinstance(x, ast.Assign) and getattr(x.targets[0], "id", "") == "BLOQUES")
textos = {}
for el in lista.elts:
    d = {k.value: v for k, v in zip(el.keys, el.values)}
    textos[ast.literal_eval(d["id"])] = ast.literal_eval(d["texto"])
PALABRAS_S = float(__import__("os").environ.get("PALABRAS_S", "2.85"))  # 15 nov: calibrado con la previa real (p04, p05, p13)


def simular(b, pl, anc):
    """Copia del planificador de montaje.py (planificar_anclado + alargar_ultimo) con la voz a PALABRAS_S palabras/s:
    devuelve los segundos que faltarían."""
    pal = textos[b].split()
    dur_voz = len(pal) / PALABRAS_S
    vis = dur_voz + 1.3
    def momento(clave):
        idx = [i for i, w in enumerate(pal) if w.lower().strip("¿¡«»,.:;!?").startswith(clave.lower())]
        return 0.4 + (idx[0] / len(pal) if idx else 0) * dur_voz
    ancl = sorted((momento(a), p) for a, p in anc.items())
    relleno = [n for n in pl if n not in {p for _, p in ancl}]
    lista, cur, i, falta = [], 0.0, 0, 0.0
    def alargar(extra):
        nonlocal falta
        n, d = lista[-1]
        cabe = max(0.0, (8.0 if n in IMG else dur[n]) - d)
        lista[-1][1] += min(cabe, extra)
        falta += max(0.0, extra - cabe)
    def rellenar(hasta):
        nonlocal cur, i
        while hasta - cur > 0.05:
            if i >= len(relleno) and lista:
                alargar(hasta - cur); cur = hasta; break
            hueco = hasta - cur
            if lista and hueco < 0.7 and hasta < vis - 0.01:  # el ancla entra unas décimas antes (igual que montaje.py)
                break
            if lista and hueco < 2.0 and dur[relleno[i]] > hueco + 1.0:  # igual que montaje.py (15 nov)
                corto = next((j for j in range(i, len(relleno)) if dur[relleno[j]] <= hueco + 0.6), None)
                if corto is not None:
                    relleno[i], relleno[corto] = relleno[corto], relleno[i]
                else:
                    u, du = lista[-1]
                    if (8.0 if u in IMG else dur[u]) - du >= hueco:
                        lista[-1][1] += hueco; cur = hasta; break
            n = relleno[i]; i += 1
            d = min(dur[n], hasta - cur)
            if d < 0.7 and lista:
                lista[-1][1] += d
            else:
                lista.append([n, d])
            cur += d
    for k, (t, n) in enumerate(ancl):
        rellenar(min(max(t, cur), vis))
        sig = ancl[k + 1][0] if k + 1 < len(ancl) else vis
        d = min(dur[n], max(0.8, sig - cur), vis - cur)
        if d > 0.05:
            lista.append([n, d]); cur += d
    rellenar(vis)
    if __import__('os').environ.get('DEPURAR') == b:
        print([(n, round(d, 1)) for n, d in lista], 'anclas', [(round(t, 1), n) for t, n in ancl])
    return vis, falta


usados, mal = [], False
for b, (pl, anc) in PLAN.items():
    falt = [p for p in pl + list(anc.values()) if p not in dur]
    fuera = [a for a in anc if a.lower() not in textos[b].lower()]
    noen = [p for p in anc.values() if p not in pl]
    usados += pl
    vis, falta = simular(b, pl, anc) if not falt else (0, 99)
    cap = sum(dur.get(p, 0) for p in pl)
    estado = "OK" if falta < 0.05 and not falt and not fuera and not noen else "REVISAR"
    mal |= estado != "OK"
    print(f"{b:7s} imagen necesaria {vis:5.1f}s  disponible {cap:5.1f}s  faltan {falta:4.1f}s  {estado} {falt or ''} {fuera or ''} {noen or ''}")
rep = {p for p in usados if usados.count(p) > 1}
print("repetidos:", rep or "ninguno", "| trozos en la tabla:", len(filas), "| usados:", len(set(usados)))
sys.exit(1 if mal or rep else 0)
