import streamlit as st
import pandas as pd

@st.cache_data
def cargar_datos():
    return pd.read_csv('data/processed/streaming_users_clean.csv')

df = cargar_datos()

st.title("El Dataset")
st.write("Usuarios de una plataforma de streaming. Vista general tras la limpieza.")

col1, col2 = st.columns(2)
col1.metric("Usuarios", len(df))
col2.metric("Variables", df.shape[1])

st.subheader("Vista previa")
st.dataframe(df.head(20))

st.subheader("Transformaciones principales")
st.markdown("""
- Normalización de categóricas (plan, país, género) escritas de formas distintas.
- Valores imposibles (edades/minutos/tickets fuera de rango) → marcados como faltantes e imputados.
- 126 duplicados exactos eliminados y 34 user_id unificados; fechas parseadas y futuras descartadas.
- Retención estructural final: 98,04% (no se descartaron filas válidas).
""")

st.subheader("Resumen de calidad (log ETL)")
st.dataframe(pd.read_csv('logs/pipeline_log.csv'))