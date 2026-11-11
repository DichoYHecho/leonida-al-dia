# Cómo hacer un vídeo largo (plantilla única)

1. Guion: copiar `guion_plantilla.py` como `guion_<id>.py`. Si hay vídeos nuevos, `fuentes_<id>.py` (formato de `fuentes_sg.py`).
2. Todo se lanza (desde main, con `rama` = rama del código) con el workflow **«Vídeo largo (todo en uno)»** (`video` = id, `paso`):
   `comprobar` → `trozos` (solo si hay fuentes nuevas) → `voces` → `previa` (2-3 bloques) → `montaje`.
3. Resultados siempre en las mismas ramas: `trozos-<id>`, `voces-<id>`, `montaje-<id>-previa`, `montaje-<id>`
   (vídeo en alta en Releases `montaje-<id>-alta-calidad`). Revisión: `informe.txt` y `finales/` de la rama.
4. Cambios de código: workflow **«Aplicar parche»** (`git diff | gzip | base64 -w0`), que además puede lanzar el paso siguiente.
   Los archivos de `.github/workflows` se cambian a mano en GitHub.
5. La pronunciación común está en `fonetica_comun.py`; en cada guion solo van las palabras nuevas (`FONETICA_EXTRA`).
