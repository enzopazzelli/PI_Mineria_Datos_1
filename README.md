# PI Minería de Datos I — Análisis de Usuarios de Streaming

## 1. Información general
- Enzo Pazzelli
- Comisión: Sede Nodo - Turno Tarde
- Fecha: 28/06/2026

## 2. Objetivo del proyecto
Tomamos un dataset sucio de usuarios de una plataforma de streaming y lo preparamos para poder analizarlo. La idea fue limpiar los datos, explorarlos para responder algunas preguntas sobre el consumo, y ver si las variables
numéricas se podían resumir con PCA. Todo el análisis está en los notebooks y los resultados se muestran en una app de Streamlit.

## 3. Dataset
- Archivo original: `streaming_users_dirty.json` (8160 registros, 8 columnas).
- Cada fila es un usuario: id, edad, plan, minutos vistos por mes, país, género
  favorito, fecha de último login y tickets de soporte.
- Venía bastante sucio: duplicados, categorías escritas de muchas formas,
  valores imposibles (edades negativas, minutos enormes), faltantes y fechas en
  formatos mezclados.
- Después de la limpieza quedó en `streaming_users_clean.csv` (8000 usuarios).

## 4. Estructura del repositorio
- `data/raw/` — dataset original (no se toca).
- `data/processed/` — dataset limpio.
- `notebooks/` — 02 limpieza, 03 EDA, 04 PCA, 05 conclusiones.
- `app/` — la app de Streamlit (Home + páginas).
- `logs/` — el log del pipeline de limpieza.
- `reports/` — informe final en PDF.

## 5. Preparación y calidad de datos
La limpieza está en `notebooks/02_calidad_y_limpieza.ipynb` y cada paso queda
registrado en `logs/pipeline_log.csv`. Lo que hicimos:
- Eliminamos 126 filas duplicadas exactas y unificamos 34 user_id repetidos (nos quedamos con el registro más completo de cada usuario).
- Normalizamos plan, país y género, que venían escritos de muchas formas, a una forma única.
- Los valores imposibles (edades fuera de 13–100, minutos negativos o mayores a 43200, tickets raros) los marcamos como faltantes en vez de borrar la fila.
- Imputamos las numéricas con la mediana y el género faltante con "Desconocido".
- Parseamos las fechas (venían en 3 formatos) y descartamos las que daban en el futuro. La fecha faltante no se imputa.
- Retención final: 98,04% (no se descartaron filas válidas).

## 6. Resumen del análisis exploratorio
El EDA está en `notebooks/03_eda.ipynb`. Lo más importante:
- El consumo crece con el plan: la mediana de minutos pasa de 558 (Básico) a 833
  (Estándar) a 1081 (Premium). Es la única relación fuerte que encontramos.
- La edad no se relaciona con el consumo (correlación ≈ 0).
- Los días sin iniciar sesión tampoco se relacionan con el consumo.
- El consumo es parecido en todos los países (diferencia menor al 3%).
- La distribución de planes es igual en todos los países.
- Los tickets de soporte no se concentran en ningún plan.

## 7. Reducción de dimensionalidad
En `notebooks/04_pca.ipynb` hicimos PCA sobre las 4 variables numéricas, escaladas con StandardScaler (obligatorio porque las varianzas eran muy distintas). Las 4 componentes explican casi lo mismo (~25% cada una), así que el PCA no logra
resumir las variables: están poco correlacionadas.
Al proyectar en 2 componentes y colorear por plan, los grupos no se separan. El PCA confirma que no hay estructura escondida.

## 8. Visualización interactiva
La app está en `app/` y se puede ver online acá: [link a Streamlit Cloud]

## 9. Cómo ejecutar localmente
1. Crear y activar el entorno: `python -m venv .venv` → `.\.venv\Scripts\Activate.ps1`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Correr la app: `streamlit run app/Home.py`

La app abre en `http://localhost:8501`.

## 10. Conclusiones
El comportamiento de los usuarios depende casi solo del plan contratado: los de Premium consumen casi el doble que los de Básico. La edad, el país, la inactividad y los tickets no se asocian con el consumo ni entre sí, y el PCA lo confirma.
Como recomendación, no tendría sentido segmentar campañas por edad o país; el consumo es el verdadero diferenciador entre planes. 
La principal limitación es que el dataset parece sintético (casi no hay correlaciones) y que algunas imputaciones aplanan diferencias finas