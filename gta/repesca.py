"""Repesca (12:30): rehace los vídeos de las propuestas que he cambiado en Airtable (guion, etiqueta,
capturas o fuente) o que se quedaron sin vídeo, para que pueda verlos antes de que se publiquen.
El día 1 de cada mes, además, quita los vídeos de las publicaciones de hace más de 30 días."""
import os, tempfile
from datetime import date, datetime, timedelta, timezone
import airtable, video
from config import MADRID, T_PUB
from publicar import CAMPOS

LIMITE = int(os.environ.get("LIMITE") or 5)


def limpiar():
    formula = ("AND(OR({Estado}='Publicado', {Estado}='Descartado', {Estado}='Caducada'), "
               "IS_BEFORE({Creada}, DATEADD(NOW(), -30, 'days')), {Vídeo}!='')")
    regs = airtable.listar(T_PUB, ["Titular"], formula=formula)
    airtable.actualizar(T_PUB, [(r["id"], {"Vídeo": []}) for r in regs])
    print(f"Limpieza: vídeos quitados de {len(regs)} publicaciones antiguas")


def main():
    hoy = datetime.now(MADRID).date()
    if hoy.day == 1 or os.environ.get("LIMPIAR") == "true":
        limpiar()
    regs = airtable.listar(T_PUB, CAMPOS, formula="OR({Estado}='Por Revisar', {Estado}='Aprobado')")
    hechos = 0
    for r in regs:
        f = r["fields"]
        guardado = date.fromisoformat(f["Para el día"]) if f.get("Para el día") else None
        if f.get("Vídeo") and guardado and f.get("Huella vídeo") == video.huella_video(f, guardado):
            continue  # nada ha cambiado desde que se hizo
        dia = max(guardado or hoy, hoy)
        if hechos >= LIMITE:
            break
        try:
            ruta, info, cambios = video.montar(f, dia, r["id"], tempfile.mkdtemp())
            nuevo = video.subir(r["id"], ruta)
            cambios["Vídeo"] = [{"id": nuevo["id"]}] if nuevo and nuevo.get("id") else []
            cambios["Avisos"] = cambios.get("Avisos", "")
            airtable.actualizar(T_PUB, [(r["id"], cambios)])
            hechos += 1
            print(f"✅ Rehecho: {f.get('Titular')} ({info})", flush=True)
        except Exception as e:
            airtable.actualizar(T_PUB, [(r["id"], {"Avisos": f"No se pudo rehacer el vídeo: {str(e)[:300]}"})])
            print(f"⚠️ {f.get('Titular')}: {e}", flush=True)
    print(f"Vídeos rehechos: {hechos}. Llamadas a Airtable: {airtable.LLAMADAS}")


if __name__ == "__main__":
    main()
