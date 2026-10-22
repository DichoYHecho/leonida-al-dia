"""Avisos en Airtable para que se vean al revisar (decidido el 22 oct).

Se crea una fila de Tipo «Aviso» en «Por Revisar» (no se publica nunca: publicar solo coge Noticia, Prensa o Dato).
Cuando la hayas leído, márcala como «Descartado».

- Si falla una tarea programada de GitHub, el último paso del workflow ejecuta este archivo.
- publicar.py y comprobar.py llaman a avisar() cuando no hay nada aprobado o una red no publicó."""
import os
from datetime import datetime, timezone
import airtable
from config import MADRID, T_PUB


def enlace():
    s, r, i = (os.environ.get(k, "") for k in ("GITHUB_SERVER_URL", "GITHUB_REPOSITORY", "GITHUB_RUN_ID"))
    return f"{s}/{r}/actions/runs/{i}" if s and r and i else ""


def avisar(titulo, detalle, repetir_horas=6):
    """Crea el aviso salvo que ya haya uno igual sin descartar de las últimas «repetir_horas» horas."""
    try:
        titular = f"⚠️ {titulo}"[:90]
        formula = (f"AND({{Tipo}}='Aviso', {{Titular}}='{airtable.esc(titular)}', {{Estado}}='Por Revisar', "
                   f"IS_AFTER({{Creada}}, DATEADD(NOW(), -{int(repetir_horas)}, 'hours')))")
        if airtable.listar(T_PUB, ["Titular"], formula=formula, maximo=1):
            print(f"Aviso ya creado hace poco: {titular}")
            return
        url = enlace()
        airtable.crear(T_PUB, [{
            "Titular": titular, "Estado": "Por Revisar", "Tipo": "Aviso", "Etiqueta": "AVISO",
            "Avisos": (detalle + (f"\nDetalles: {url}" if url else ""))[:1000],
            "Creada": datetime.now(timezone.utc).isoformat(timespec="seconds")}])
        print(f"Aviso creado en Airtable: {titular}")
    except Exception as e:  # un aviso nunca debe romper la tarea que lo llama
        print(f"No se pudo crear el aviso en Airtable: {str(e)[:200]}")


if __name__ == "__main__":
    tarea = os.environ.get("TAREA") or os.environ.get("GITHUB_WORKFLOW") or "una tarea"
    hora = datetime.now(MADRID).strftime("%d/%m %H:%M")
    avisar(f"Ha fallado «{tarea}» ({hora})",
           "Una tarea automática de GitHub ha fallado. Si era una publicación, puede que no haya salido: "
           "mira en Buffer o en las redes. Dímelo y lo revisamos.")
