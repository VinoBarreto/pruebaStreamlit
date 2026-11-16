import streamlit as st
from base_datos import buscar_por_dni, eliminar_empleado

COLUMNAS = ["id", "dni", "nombre_apellido", "cargo", "area",
            "salario", "fecha_ingreso", "estado"]


def pagina_administrar():
    st.header("Administrar")

    # PREGUNTA 9: Eliminar empleado por DNI con confirmación

    st.subheader("Eliminar empleado")

    dni_eliminar = st.text_input("DNI del empleado a eliminar")

    if st.button("Buscar para eliminar"):
        resultado = buscar_por_dni(dni_eliminar.strip())
        if resultado:
            st.session_state.empleado_eliminar = resultado[0]
        else:
            st.session_state.empleado_eliminar = None
            st.error("No existe ningún empleado con ese DNI.")

    empleado = st.session_state.get("empleado_eliminar")

    if empleado:
        st.warning("Empleado encontrado (confirmación requerida):")
        st.json(dict(zip(COLUMNAS, empleado)))

        confirmar = st.checkbox("Confirmo que deseo eliminar este empleado.")

        if st.button("Eliminar ahora", disabled=not confirmar):
            eliminar_empleado(empleado[1])
            st.session_state.empleado_eliminar = None
            st.success(f"Empleado con DNI {empleado[1]} eliminado correctamente.")

            