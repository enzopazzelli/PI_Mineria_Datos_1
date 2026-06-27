import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

@st.cache_data
def cargar_datos():
    return pd.read_csv('data/processed/streaming_users_clean.csv')

df = cargar_datos()
st.title("Reducción de dimensionalidad (PCA)")

features = ['age', 'monthly_watch_time_mins', 'customer_support_tickets', 'dias_desde_login']
X = df[features].dropna()
X_scaled = StandardScaler().fit_transform(X)

st.write("**Variables usadas:**", ", ".join(features),
         "  ·  *(se excluye `user_id`: no es una medida, sino un identificador)*")
st.write(f"**Escalamiento:** StandardScaler. Sin escalar, las varianzas "
         f"iban de 0,7 a 714.352 y dominarían las variables de mayor unidad.")
st.write(f"**Filas usadas:** {len(X)} de {len(df)} *(se descartan los 472 sin "
         "`dias_desde_login`; faltante aleatorio → sin sesgo)*")

# --- Varianza explicada (Q7) ---
st.subheader("Varianza explicada por componente")
pca_full = PCA().fit(X_scaled)
var = pca_full.explained_variance_ratio_ * 100
tabla_var = pd.DataFrame({
    'Componente': [f'PC{i+1}' for i in range(len(var))],
    'Varianza (%)': var.round(2),
    'Acumulada (%)': var.cumsum().round(2)
})
st.dataframe(tabla_var, use_container_width=True, hide_index=True)
st.markdown("**Interpretación:** las cuatro componentes explican una proporción "
            "casi idéntica (~25% c/u). Esta uniformidad indica que las variables son "
            "**estadísticamente independientes**: el PCA no logra resumirlas. Con un "
            "umbral del 80% se necesitan las 4 componentes. **No reduce la dimensionalidad.**")

# --- Loadings ---
st.subheader("Loadings (peso de cada variable)")
pca_2d = PCA(n_components=2)
X_pca = pca_2d.fit_transform(X_scaled)
loadings = pd.DataFrame(pca_2d.components_.T, index=features, columns=['PC1', 'PC2']).round(3)
st.dataframe(loadings, use_container_width=True)
st.markdown("**Interpretación:** PC2 está dominada por `customer_support_tickets` "
            "(0,91) → eje de soporte. PC1 combina `age` y `watch_time` contra "
            "`dias_desde_login` → eje tentativo de actividad. *Como las variables están "
            "poco correlacionadas, los componentes son una rotación casi arbitraria: su "
            "significado es frágil y no tienen nombre propio.*")

# --- Proyección 2D (Q8) ---
st.subheader("Proyección sobre las 2 primeras componentes")
df_pca = pd.DataFrame(X_pca, columns=['PC1', 'PC2'])
df_pca['plan'] = df.loc[X.index, 'subscription_plan'].values
fig = px.scatter(df_pca, x='PC1', y='PC2', color='plan',
                 category_orders={'plan': ['Básico', 'Estándar', 'Premium']}, opacity=0.5,
                 labels={'PC1': f'PC1 ({var[0]:.1f}% var.)', 'PC2': f'PC2 ({var[1]:.1f}% var.)'})
st.plotly_chart(fig, use_container_width=True)
st.markdown("**Interpretación:** los tres planes se superponen sin formar "
            "clústeres: **no se distinguen perfiles de usuario separables**. El PCA, "
            "más que revelar estructura, confirma su ausencia.")