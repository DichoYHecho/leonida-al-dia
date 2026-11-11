"""Pronunciación común de los vídeos largos (se reutiliza en cada guion nuevo).

Uso en un guion:  from fonetica_comun import voz
                  _b["voz"] = voz(_b["texto"], {"Palabra": "Pronunciación"})   # extra solo de ese vídeo
Cambia palabra por palabra (misma cantidad de palabras que el texto, para que cuadren los subtítulos).
"""
import re

FONETICA = {'Advance': 'Advans',
 'Anywhere': 'Énigüer',
 'Ballad': 'Bálad',
 'Bellic': 'Bélic',
 'Boy': 'Boi',
 'Bronx': 'Bronks',
 'CJ': 'Siyéi',
 'Chinatown': 'Cháinataun',
 'City': 'Siti',
 'Claude': 'Clod',
 'Coffee': 'Cófi',
 'Damned': 'Dámd',
 'Definitive': 'Définitiv',
 'Design': 'Disáin',
 'Dundee': 'Dandí',
 'Edition.': 'Edíshon.',
 'Euphoria': 'Iufória',
 'Franklin,': 'Fránklin,',
 'Game': 'Guéim',
 'Gay': 'Guei',
 'Hot': 'Jot',
 'Houser': 'Jáuser',
 'III': '3',
 'IV': '4',
 'Jackson': 'Yákson',
 'Johnson,': 'Yónson,',
 'L.': 'El',
 'Lemmings': 'Lémings',
 'Leonida': 'Leónida',
 'Liberty': 'Líberti',
 'Liotta': 'Lióta',
 'London': 'Lóndon',
 'Lost': 'Lost',
 'Love': 'Lov',
 'Metacritic': 'Métacritic',
 'Michael': 'Máikel',
 'North': 'Norz',
 'Online': 'Onlain',
 'Petty': 'Péti',
 'Pointer': 'Póinter',
 'Queens,': 'Kuins,',
 'RAGE': 'Reich',
 "Race'n'Chase": 'Réisenchéis',
 'Ray': 'Rei',
 'Road.': 'Roud.',
 'Roman': 'Róman',
 'Samuel': 'Sámuel',
 'Sisters.': 'Sísters.',
 'Stories': 'Stóris',
 'Tenpenny': 'Tenpeni',
 'Together,': 'Tuguéder,',
 'Tommy': 'Tomi',
 'Tony': 'Toni',
 'Trevor,': 'Trévor,',
 'V': '5',
 'VI': '6',
 'Vercetti': 'Verchéti',
 'Wars': 'Uors'}


def voz(texto, extra=None):
    tabla = {**FONETICA, **(extra or {})}
    salida = []
    for w in texto.split():
        if w in tabla:
            salida.append(tabla[w])
            continue
        a, nucleo, z = re.match(r"^([¿¡(«]*)(.*?)([.,;:!?»)…]*)$", w).groups()
        salida.append(a + tabla.get(nucleo, nucleo) + z)
    return " ".join(salida)
