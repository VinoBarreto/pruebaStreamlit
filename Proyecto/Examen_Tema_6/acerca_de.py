import streamlit as st


def pagina_acerca_de():

    # PREGUNTA 10: Información del estudiante

    st.header("Acerca de")

    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Información de la Aplicación")
    with c2:
        st.markdown("**Gestión Integral de Empleados**")
        st.write("Aplicación web desarrollada en Streamlit con base de datos SQLite.")

    st.divider()

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**Desarrollado por:**")
        st.write("Vinolia Barreto")
        st.markdown("**Fecha de desarrollo:**")
        st.write("12 de noviembre de 2026")
    with c4:
        st.markdown("**Curso:**")
        st.write("Aplicaciones Interactivas para Análisis de Datos e Inteligencia Artificial")
        st.markdown("**Tecnologías:**")
        st.write("Streamlit, SQLite, Python, Pandas, Plotly")

