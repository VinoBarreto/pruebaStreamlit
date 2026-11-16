import streamlit as st
import pandas as pd
import plotly.express as px
from base_datos import ver_todos_empleados

COLUMNAS = ["id", "dni", "nombre_apellido", "cargo", "area",
            "salario", "fecha_ingreso", "estado"]


def pagina_analisis():
    st.header("Análisis")

    df = pd.DataFrame(ver_todos_empleados(), columns=COLUMNAS)

    if df.empty:
        st.info("No hay empleados registrados para analizar.")
        return

    tab_area, tab_cargo = st.tabs(["Por Área", "Por Cargo"])

    # PREGUNTA 11: Cantidad de empleados por área

    with tab_area:
        st.write("Cantidad de empleados por área")
        conteo_area = df["area"].value_counts().reset_index()
        conteo_area.columns = ["area", "cantidad"]

        c1, c2 = st.columns(2)
        with c1:
            st.dataframe(conteo_area, hide_index=True)
        with c2:
            fig_area = px.pie(conteo_area, names="area", values="cantidad")
            fig_area.update_traces(textinfo="percent+label")
            st.plotly_chart(fig_area, key="pie_area")

    # PREGUNTA 12: Cantidad de empleados por cargo
    
    with tab_cargo:
        st.write("Cantidad de empleados por cargo")
        conteo_cargo = df["cargo"].value_counts().reset_index()
        conteo_cargo.columns = ["cargo", "cantidad"]

        c3, c4 = st.columns(2)
        with c3:
            st.dataframe(conteo_cargo, hide_index=True)
        with c4:
            fig_cargo = px.pie(conteo_cargo, names="cargo", values="cantidad")
            fig_cargo.update_traces(textinfo="percent+label")
            st.plotly_chart(fig_cargo, key="pie_cargo")