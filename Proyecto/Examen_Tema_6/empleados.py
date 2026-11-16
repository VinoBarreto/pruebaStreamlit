import streamlit as st
from datetime import date
from base_datos import insertar_empleado, buscar_por_dni, actualizar_empleado


def pagina_empleados():
    
    # PREGUNTA 5: Formulario de registro de empleados 

    st.subheader("Registrar empleado")

    with st.form("form_registro", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            dni = st.text_input("DNI")
            cargo = st.text_input("Cargo")
            salario = st.number_input("Salario", min_value=0.0, step=100.0, format="%.2f")
        with c2:
            nombre_apellido = st.text_input("Nombre y Apellido")
            area = st.text_input("Área")
            estado = st.selectbox("Estado", ["Activo", "Inactivo"])
        fecha_ingreso = st.date_input("Fecha de ingreso", value=date.today())

        guardar = st.form_submit_button("Guardar")

    if guardar:
        if dni.strip() == "" or nombre_apellido.strip() == "":
            st.error("El DNI y el nombre son obligatorios.")
        elif insertar_empleado(dni.strip(), nombre_apellido.strip(), cargo.strip(),
                               area.strip(), salario, fecha_ingreso.isoformat(), estado):
            st.success(f"Empleado {nombre_apellido} registrado correctamente.")
        else:
            st.error(f"Ya existe un empleado con el DNI {dni}.")

    # PREGUNTA 8: Actualizar empleado

    st.subheader("Actualizar empleado (cargo, área, salario, estado)")

    dni_buscar = st.text_input("DNI del empleado a actualizar")

    if st.button("Buscar empleado"):
        resultado = buscar_por_dni(dni_buscar.strip())
        if resultado:
            st.session_state.empleado_editar = resultado[0]
        else:
            st.session_state.empleado_editar = None
            st.error("No existe ningún empleado con ese DNI.")

    empleado = st.session_state.get("empleado_editar")

    if empleado:
        id_emp, dni_emp, nombre_emp, cargo_emp, area_emp, salario_emp, fecha_emp, estado_emp = empleado
        st.info(f"Encontrado: {nombre_emp} | Cargo: {cargo_emp} | Área: {area_emp} | Estado: {estado_emp}")

        with st.form("form_actualizar"):
            nuevo_cargo = st.text_input("Nuevo cargo", value=cargo_emp)
            nueva_area = st.text_input("Nueva área", value=area_emp)
            nuevo_salario = st.number_input("Nuevo salario", min_value=0.0, step=100.0,
                                            format="%.2f", value=float(salario_emp))
            nuevo_estado = st.selectbox("Nuevo estado", ["Activo", "Inactivo"],
                                        index=0 if estado_emp == "Activo" else 1)
            actualizar = st.form_submit_button("Actualizar")

        if actualizar:
            actualizar_empleado(dni_emp, nuevo_cargo.strip(), nueva_area.strip(),
                                nuevo_salario, nuevo_estado)
            st.session_state.empleado_editar = None
            st.success(f"Empleado {nombre_emp} actualizado correctamente.")

            