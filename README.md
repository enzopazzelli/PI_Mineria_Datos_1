# PI Minería de Datos I — Análisis de Usuarios de Streaming

## 1. Información general
- Enzo Pazzelli
- Comisión: Sede Nodo - Turno Tarde
- Fecha: 28/06/2026

## 2. Objetivo del proyecto
Se parte de un dataset sucio de usuarios de una plataforma de streaming y se lo prepara para el análisis: limpiar los datos, explorarlos para responder preguntas sobre el consumo y evaluar con PCA si las variables numéricas se pueden resumir. El análisis completo está en los notebooks y los resultados se comunican en una app de Streamlit.

## 3. Dataset
- Archivo original: `data/raw/streaming_users_dirty.json` (8160 registros, 8 columnas).
- Cada fila es un usuario: id, edad, plan, minutos vistos por mes, país, género
  favorito, fecha de último login y tickets de soporte.
- Venía con problemas de calidad: duplicados, categorías escritas de muchas formas,
  valores imposibles (edades negativas, minutos enormes), faltantes y fechas en
  formatos mezclados.
- Tras la limpieza queda `data/processed/streaming_users_clean.csv` (8000 usuarios).

## 4. Estructura del repositorio
- `data/raw/` — dataset original (no se toca).
- `data/processed/` — dataset limpio.
- `notebooks/` — 01 inspección inicial, 02 limpieza, 03 EDA, 04 PCA, 05 conclusiones.
- `app/` — la app de Streamlit (Home + páginas).
- `logs/` — el log del pipeline de limpieza.
- `reports/` — informe final en PDF.

## 5. Preparación y calidad de datos
La limpieza está documentada paso a paso en `notebooks/02_calidad_y_limpieza.ipynb`, con cada decisión registrada en `logs/pipeline_log.csv`. En síntesis: se eliminaron duplicados, se normalizaron las categorías, los valores imposibles se marcaron como faltantes (sin borrar filas) y las numéricas se imputaron con la mediana. La retención final fue del 98,04%. El detalle y la justificación de cada paso están en el informe.

## 6. Resumen del análisis exploratorio
El EDA completo está en `notebooks/03_eda.ipynb` y de forma interactiva en la app. El hallazgo principal: el consumo crece con el plan (mediana 558 → 833 → 1081 minutos), la única relación fuerte del dataset. La edad y la inactividad no se asocian con el consumo. La interpretación de cada gráfico está en la app y el informe.

## 7. Reducción de dimensionalidad
El PCA está en `notebooks/04_pca.ipynb`. Sobre las 4 variables numéricas, escaladas con StandardScaler, las 4 componentes explican ~25% cada una: no se logra reducir la dimensionalidad y, al proyectar por plan, los grupos no se separan. El detalle y la interpretación están en el informe y la app.

## 8. Visualización interactiva
App online: [Streamlit Cloud](https://integrador-mineria-de-datos.streamlit.app/)

## 9. Cómo ejecutar localmente
1. Crear y activar el entorno: `python -m venv .venv` → `.\.venv\Scripts\Activate.ps1`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Correr la app: `streamlit run app/Home.py`

La app abre en `http://localhost:8501`.

## 10. Conclusiones
El comportamiento de los usuarios depende casi solo del plan contratado: los de Premium consumen casi el doble que los de Básico; el resto de las variables no se asocia con el consumo, lo que el PCA confirma. Las recomendaciones de negocio y las limitaciones se desarrollan en `notebooks/05_conclusiones.ipynb` y en el informe.
