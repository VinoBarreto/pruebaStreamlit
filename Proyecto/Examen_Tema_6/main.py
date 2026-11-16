import streamlit as st
from base_datos import probar_conexion, crear_tablas
from empleados import pagina_empleados
from inicio import pagina_inicio
from administrar import pagina_administrar
from acerca_de import pagina_acerca_de
from analitica import pagina_analisis

st.set_page_config(page_title="Gestión de Empleados", layout="wide")

# PREGUNTA 4: Alternar la visibilidad del menú lateral

if "mostrar_menu" not in st.session_state:
    st.session_state.mostrar_menu = True


def alternar_menu():
    st.session_state.mostrar_menu = not st.session_state.mostrar_menu


def main():
    crear_tablas()

    st.title("Sistema de Gestión de Empleados")
    estado_bd = "Conectado" if probar_conexion() else "Error de conexión"
    st.caption(f"Estado BD: {estado_bd}")

    texto_boton = "Ocultar menú" if st.session_state.mostrar_menu else "Mostrar menú"
    st.button(texto_boton, on_click=alternar_menu)

    if not st.session_state.mostrar_menu:
        st.markdown(
            """
            <style>
                section[data-testid="stSidebar"] {display: none;}
                div[data-testid="stSidebarCollapsedControl"] {display: none;}
            </style>
            """,
            unsafe_allow_html=True
        )

    # PREGUNTA 3: Menú principal en la barra lateral

    st.sidebar.title("Menú")
    menu = ["Inicio", "Empleados", "Administrar", "Analisis", "Acerca de"]
    seleccion = st.sidebar.selectbox("Ir a:", menu)

    if seleccion == "Inicio":
        pagina_inicio()
    elif seleccion == "Empleados":
        pagina_empleados()
    elif seleccion == "Administrar":
        pagina_administrar()
    elif seleccion == "Analisis":
        pagina_analisis()
    else:
        pagina_acerca_de()


main()