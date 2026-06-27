import streamlit as st

st.title("Conclusiones")

st.subheader("Evidencia")
st.markdown("""
- El consumo crece con el plan (mediana 558 → 833 → 1081).
- Edad, inactividad, país y tickets no se asocian con el consumo (r ≈ 0, dif. < 3%).
- El PCA no reduce dimensionalidad (4 componentes ~25% c/u) ni separa perfiles.
""")

st.subheader("Interpretación")
st.markdown("""
- El único factor que estructura el comportamiento es el **plan contratado**.
- Las demás variables son estadísticamente independientes: el comportamiento del
  usuario es esencialmente aleatorio respecto de ellas.
""")

st.subheader("Conclusión / recomendación")
st.markdown("""
- **No segmentar campañas por edad ni país:** ninguna se asocia con el consumo.
- **El consumo es el diferenciador real entre planes:** los usuarios Premium
  consumen casi el doble que los Básico; conviene apalancar ese dato en la
  propuesta de valor.
""")

st.subheader("Limitaciones")
st.markdown("""
- Imputaciones (mediana) que aplanan diferencias finas.
- 472 usuarios sin fecha de login excluidos del PCA.
- Ausencia casi total de correlaciones → posible naturaleza sintética del dataset.
""")    