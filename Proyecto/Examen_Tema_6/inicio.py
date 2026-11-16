import streamlit as st
import pandas as pd
from base_datos import ver_todos_empleados, buscar_por_dni, buscar_por_nombre

COLUMNAS = ["id", "dni", "nombre_apellido", "cargo", "area",
            "salario", "fecha_ingreso", "estado"]


def pagina_inicio():
    st.header("Inicio")

    # PREGUNTA 7: Buscador de empleados

    st.subheader("Buscar")
    modo = st.radio("Buscar por:", ["DNI (exacto)", "Nombre (parcial)"], horizontal=True)

    if modo == "DNI (exacto)":
        texto = st.text_input("DNI")
    else:
        texto = st.text_input("Nombre")

    if st.button("Buscar"):
        if texto.strip() == "":
            st.warning("Escribe un valor para buscar.")
        else:
            if modo == "DNI (exacto)":
                resultados = buscar_por_dni(texto.strip())
            else:
                resultados = buscar_por_nombre(texto.strip())

            if resultados:
                st.success(f"Se encontraron {len(resultados)} resultado(s).")
                st.dataframe(pd.DataFrame(resultados, columns=COLUMNAS), hide_index=True)
            else:
                st.info("No se encontraron empleados.")

    # PREGUNTA 6: Listado de empleados
    
    st.subheader("Listado de empleados")
    df = pd.DataFrame(ver_todos_empleados(), columns=COLUMNAS)

    if df.empty:
        st.info("No hay empleados registrados.")
    else:
        st.dataframe(df, hide_index=True)
