import streamlit as st
import pandas as pd

st.set_page_config(page_title="Streaming — PI Minería I", layout="wide")

@st.cache_data
def cargar_datos():
    return pd.read_csv('data/processed/streaming_users_clean.csv')

st.title("Minería de Datos I - Proyecto Integrador - 2026")
st.header("Análisis de Usuarios de Streaming")
st.markdown("""

- Integrantes: *Enzo Pazzelli*, *Nombre 2*
- Comisión: *Sede Nodo - Turno Tarde*  ·  Fecha: *__/06/2026*
- Repositorio: [GitHub](https://github.com/enzopazzelli/PI_Mineria_Datos_1)
""")
st.divider()
st.write("Usá el menú lateral para recorrer **Dataset**, **EDA**, **PCA** y **Conclusiones**.")