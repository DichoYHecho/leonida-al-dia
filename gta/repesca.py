"""Repesca (12:30): rehace los vídeos de las propuestas que he cambiado en Airtable (guion, etiqueta,
capturas o fuente) o que se quedaron sin vídeo, para que pueda verlos antes de que se publiquen.
El día 1 de cada mes, además, quita los vídeos de las publicaciones de hace más de 30 días."""
import json, os, re, tempfile
from datetime import date, datetime, timedelta, timezone
import airtable, imagenes, video, voz
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
    # A mano (22 oct): BUSCAR_IMAGEN = un trozo del titular. Busca la imagen de esa noticia (oficial o del medio),
    # la pone en «Capturas» y en el crédito del post, y rehace el vídeo.
    buscar = (os.environ.get("BUSCAR_IMAGEN") or "").strip().lower()
    # A mano (2 nov): REVISAR_VOZ = true. Comprueba con Whisper la voz guardada de cada propuesta y, si no sigue
    # el guion (por ejemplo, se pasa al inglés a mitad), la borra de la caché y rehace el vídeo con una voz nueva.
    revisar_voz = os.environ.get("REVISAR_VOZ") == "true"
    regs = airtable.listar(T_PUB, CAMPOS + ["Enlace"], formula="OR({Estado}='Por Revisar', {Estado}='Aprobado')")
    hechos = 0
    for r in regs:
        f = r["fields"]
        nuevos = {}
        if buscar and buscar in (f.get("Titular") or "").lower() and f.get("Enlace"):
            # Desde el 23 oct: una imagen de CADA cosa real que nombra el guion (imagenes.buscar_todas)
            cosas = imagenes.cosas_de(f.get("Guion") or f.get("Titular")) or [f.get("Titular")]
            extra = (os.environ.get("PAGINAS_EXTRA") or "").split()  # webs o imágenes donde buscar, a mano
            encontradas, faltan = imagenes.buscar_todas({"medio": f.get("Fuente"), "enlace": f["Enlace"]}, cosas, extra)
            if encontradas:
                creditos = list(dict.fromkeys(cr for _, cr, _ in encontradas))
                rotulo = "Imagen" if len(encontradas) == 1 else "Imágenes"
                caption = re.sub(r"(?:Imagen|Imágenes): [^\n]*?\.(?= Cuenta de fans|\n)", f"{rotulo}: {' y '.join(creditos)}.",
                                 f.get("Caption") or "", count=1)
                nuevos = {"Capturas": ", ".join(imagenes.token(u, cr) for u, cr, _ in encontradas), "Caption": caption}
                f.update(nuevos)
                print(f"Imágenes para «{f.get('Titular')}»: " + "; ".join(f"{k} → {u}" for k, (u, _, _) in zip(cosas, encontradas)), flush=True)
            if faltan:
                nuevos["Avisos"] = f"⚠️ Falta la imagen de: {', '.join(faltan)}. No la apruebes así: descártala."
                print(f"⚠️ «{f.get('Titular')}»: falta la imagen de {', '.join(faltan)}", flush=True)
        forzar = False
        if revisar_voz and (f.get("Guion") or "").strip():
            h = video.huella(f["Guion"].strip())
            wav = os.path.join(video.VOCES, h + ".wav")
            if os.path.exists(wav):
                c = voz.cobertura(wav, video.trozos_de(f))
                print(f"Voz de «{f.get('Titular')}»: Whisper reconoce el {c:.0%} del guion", flush=True)
                if c < voz.UMBRAL:
                    for ext in (".wav", ".json"):
                        if os.path.exists(os.path.join(video.VOCES, h + ext)):
                            os.remove(os.path.join(video.VOCES, h + ext))
                    forzar = True
            else:
                print(f"Voz de «{f.get('Titular')}»: no está en la caché, no se puede comprobar", flush=True)
        guardado = date.fromisoformat(f["Para el día"]) if f.get("Para el día") else None
        if not nuevos and not forzar and f.get("Vídeo") and guardado and f.get("Huella vídeo") == video.huella_video(f, guardado):
            continue  # nada ha cambiado desde que se hizo (si se ha buscado su imagen, se rehace siempre)
        dia = max(guardado or hoy, hoy)
        if hechos >= LIMITE:
            break
        try:
            ruta, info, cambios = video.montar(f, dia, r["id"], tempfile.mkdtemp())
            nuevo = video.subir(r["id"], ruta)
            cambios["Vídeo"] = [{"id": nuevo["id"]}] if nuevo and nuevo.get("id") else []
            cambios["Avisos"] = "\n".join(a for a in (nuevos.get("Avisos"), cambios.get("Avisos")) if a)
            cambios.update({k: v for k, v in nuevos.items() if k != "Avisos"})
            airtable.actualizar(T_PUB, [(r["id"], cambios)])
            hechos += 1
            print(f"✅ Rehecho: {f.get('Titular')} ({info})", flush=True)
        except Exception as e:
            airtable.actualizar(T_PUB, [(r["id"], {"Avisos": f"No se pudo rehacer el vídeo: {str(e)[:300]}"})])
            print(f"⚠️ {f.get('Titular')}: {e}", flush=True)
    print(f"Vídeos rehechos: {hechos}. Llamadas a Airtable: {airtable.LLAMADAS}")


if __name__ == "__main__":
    main()
