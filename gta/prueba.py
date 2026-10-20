"""Prueba completa SIN tocar Airtable ni Buffer: guion con Gemini, voz «Mako», subtítulos y vídeo.
Deja el vídeo como «artifact» de GitHub para verlo. También puede probar la lectura de noticias.
Variables: ORDEN (número del dato del banco), NOTICIAS (true para probar las fuentes y la elección)."""
import json, os
from datetime import timedelta, datetime
import guion, video, fuentes, preparar
from config import MADRID, ARRANQUE

SALIDA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "salida_prueba")
os.makedirs(SALIDA, exist_ok=True)
hoy = datetime.now(MADRID).date()
informe = []

if os.environ.get("NOTICIAS") == "true":
    cands = fuentes.candidatas(int(os.environ.get("HORAS") or 30))
    informe.append(f"Noticias de GTA 6 encontradas: {len(cands)}")
    for c in cands[:20]:
        informe.append(f"- [{c['medio']}] {c['titulo']} ({c['fecha']:%d/%m %H:%M})")
    if cands:
        eleg = preparar.elegir(cands[:25], [], 2)
        informe.append(f"Elegidas por Gemini: {[e['titulo'] for e in eleg]}")
        if eleg:
            texto = fuentes.texto_de(eleg[0])
            informe.append(f"Texto leído de la primera ({len(texto)} caracteres): {texto[:400]}")

orden = os.environ.get("ORDEN") or "5"
d = next(x for x in preparar.banco() if x["Orden"] == orden)
g = guion.de_dato(d)
f = preparar.fila(g, "Dato", d["Fuente"], d["Estado"] == "Oficial", d["Enlace"], d["Dato"], max(hoy, ARRANQUE), int(orden))
ruta, info, cambios = video.montar(f, max(hoy, ARRANQUE), video.huella(f["Titular"]), SALIDA)
informe += [f"Dato {orden}: {d['Dato']}", "", "GUION:", f["Guion"], "", f"Etiqueta: {f['Etiqueta']} · Capturas: {f['Capturas']}",
            "", "CAPTION:", f["Caption"], "", f"Título YouTube: {f['Título YouTube']}", f"Vídeo: {info}",
            f"Tiempos: {cambios.get('Tiempos')}"]
txt = "\n".join(informe)
print(txt)
open(os.path.join(SALIDA, "informe.txt"), "w").write(txt)
s = os.environ.get("GITHUB_STEP_SUMMARY")
if s:
    open(s, "a").write("## Prueba\n\n```\n" + txt + "\n```\n")
