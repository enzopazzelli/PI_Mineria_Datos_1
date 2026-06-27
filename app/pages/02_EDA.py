import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def cargar_datos():
    return pd.read_csv('data/processed/streaming_users_clean.csv')

df = cargar_datos()
orden_plan = ['Básico', 'Estándar', 'Premium']

st.title("Análisis Exploratorio")
st.caption("Cada gráfico responde una pregunta y lleva su interpretación.")

# ---------- UNIVARIADO 1 ----------
st.subheader("1. Distribución del tiempo de visualización")
fig = px.histogram(df, x='monthly_watch_time_mins', nbins=30,
                   labels={'monthly_watch_time_mins': 'Minutos vistos por mes'})
st.plotly_chart(fig, use_container_width=True)
st.markdown("**Interpretación:** distribución sesgada a la derecha. La barra "
            "sobre-representada en torno a la mediana corresponde en parte a los "
            "valores imputados, no a una concentración real.")

# ---------- UNIVARIADO 2 ----------
st.subheader("2. Usuarios por plan")
vc = df['subscription_plan'].value_counts().reindex(orden_plan)
fig = px.bar(x=vc.index, y=vc.values, labels={'x': 'Plan', 'y': 'Cantidad de usuarios'})
st.plotly_chart(fig, use_container_width=True)
st.markdown("**Interpretación:** Básico concentra la mayoría (45%) y Premium es el "
            "que menos tiene (19,8%). La mayoría prefiere pagar menos.")

# ---------- Q1 ----------
st.subheader("3. ¿El consumo difiere entre planes?")
fig = px.box(df, x='subscription_plan', y='monthly_watch_time_mins',
             color='subscription_plan', category_orders={'subscription_plan': orden_plan},
             labels={'subscription_plan': 'Plan', 'monthly_watch_time_mins': 'Minutos/mes'})
st.plotly_chart(fig, use_container_width=True)
st.markdown("**Interpretación:** la mediana crece de forma monótona (558 → 833 → "
            "1081): Premium casi duplica a Básico. Es la **única relación fuerte** "
            "del dataset: a mayor plan, mayor consumo por usuario.")

# ---------- Q2 ----------
st.subheader("4. ¿La edad se relaciona con el consumo?")
fig = px.scatter(df, x='age', y='monthly_watch_time_mins', opacity=0.35,
                 labels={'age': 'Edad', 'monthly_watch_time_mins': 'Minutos/mes'})
st.plotly_chart(fig, use_container_width=True)
r = df['age'].corr(df['monthly_watch_time_mins'])
st.markdown(f"**Interpretación:** correlación de Pearson ≈ {r:.3f}, prácticamente "
            "nula. La edad no se relaciona linealmente con el consumo; la nube no "
            "muestra patrón. *(correlación ≠ causalidad)*")

# ---------- Q3 ----------
st.subheader("5. ¿La inactividad se relaciona con el consumo?")
sub = df[['dias_desde_login', 'monthly_watch_time_mins']].dropna()
fig = px.scatter(sub, x='dias_desde_login', y='monthly_watch_time_mins', opacity=0.35,
                 labels={'dias_desde_login': 'Días desde el último login',
                         'monthly_watch_time_mins': 'Minutos/mes'})
st.plotly_chart(fig, use_container_width=True)
r3 = sub['dias_desde_login'].corr(sub['monthly_watch_time_mins'])
st.markdown(f"**Interpretación:** correlación ≈ {r3:.3f}, nula. La inactividad no "
            f"predice el consumo mensual. Se analizan {len(sub)} usuarios (se "
            "excluyen los 472 sin fecha de login, cuya ausencia es aleatoria).")

# ---------- Q4 ----------
st.subheader("6. ¿Qué países tienen los usuarios más activos?")
activos = (df.groupby('country')['monthly_watch_time_mins'].mean()
             .sort_values(ascending=False).round(1))
fig = px.bar(x=activos.index, y=activos.values,
             labels={'x': 'País', 'y': 'Minutos promedio/mes'})
st.plotly_chart(fig, use_container_width=True)
st.markdown("**Interpretación:** consumo casi idéntico en los siete países "
            "(diferencia < 3%). **Ningún país concentra usuarios más activos**: la "
            "ubicación no diferencia el consumo.")

# ---------- Q5 ----------
st.subheader("7. ¿La distribución de planes cambia por país?")
tabla = pd.crosstab(df['country'], df['subscription_plan'], normalize='index')[orden_plan] * 100
fig = px.bar(tabla, barmode='stack', labels={'value': '% de usuarios', 'country': 'País'})
st.plotly_chart(fig, use_container_width=True)
st.markdown("**Interpretación:** la composición de planes es prácticamente igual en "
            "todos los países (Básico ~45%, Estándar ~35%, Premium ~20%). **El plan "
            "no depende del país.**")

# ---------- Q6 ----------
st.subheader("8. ¿Los tickets de soporte se concentran en algún plan?")
fig = px.box(df, x='subscription_plan', y='customer_support_tickets',
             color='subscription_plan', category_orders={'subscription_plan': orden_plan},
             labels={'subscription_plan': 'Plan', 'customer_support_tickets': 'Tickets'})
st.plotly_chart(fig, use_container_width=True)
st.markdown("**Interpretación:** media ≈ 0,80 en los tres planes. **Los tickets no "
            "se concentran en ningún plan**: la carga de soporte es homogénea.")

# ---------- MULTIVARIADO ----------
st.subheader("9. Consumo según edad y plan (multivariado)")
fig = px.scatter(df, x='age', y='monthly_watch_time_mins', color='subscription_plan',
                 category_orders={'subscription_plan': orden_plan}, opacity=0.5,
                 labels={'age': 'Edad', 'monthly_watch_time_mins': 'Minutos/mes'})
st.plotly_chart(fig, use_container_width=True)
st.markdown("**Interpretación:** las bandas se separan en vertical por plan (Premium "
            "arriba, Básico abajo) pero son horizontales: el efecto del plan se "
            "mantiene a todas las edades. No se observa paradoja de Simpson.")