import sqlite3
from pathlib import Path

# PREGUNTA 1: Conexión segura con SQLite

RUTA_BD = Path(__file__).parent / "empleados.db"


def obtener_conexion():
    return sqlite3.connect(RUTA_BD)


def probar_conexion():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        conexion.close()
        return True
    except sqlite3.Error:
        return False


# PREGUNTA 2: Creación de la tabla empleados

def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dni TEXT UNIQUE NOT NULL,
            nombre_apellido TEXT NOT NULL,
            cargo TEXT,
            area TEXT,
            salario REAL,
            fecha_ingreso DATE,
            estado TEXT
        )
    """)
    conexion.commit()
    conexion.close()


# PREGUNTA 5: Insertar un empleado

def insertar_empleado(dni, nombre_apellido, cargo, area, salario, fecha_ingreso, estado):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "INSERT INTO empleados (dni, nombre_apellido, cargo, area, salario, fecha_ingreso, estado) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (dni, nombre_apellido, cargo, area, salario, fecha_ingreso, estado)
        )
        conexion.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conexion.close()


# PREGUNTA 6: Obtener todos los empleados

def ver_todos_empleados():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM empleados")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado


# PREGUNTA 7: Búsquedas

def buscar_por_dni(dni):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM empleados WHERE dni = ?", (dni,))
    resultado = cursor.fetchall()
    conexion.close()
    return resultado


def buscar_por_nombre(texto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM empleados WHERE nombre_apellido LIKE ?", (f"%{texto}%",))
    resultado = cursor.fetchall()
    conexion.close()
    return resultado


# PREGUNTA 8: Actualizar empleado

def actualizar_empleado(dni, cargo, area, salario, estado):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE empleados SET cargo = ?, area = ?, salario = ?, estado = ? WHERE dni = ?",
        (cargo, area, salario, estado, dni)
    )
    conexion.commit()
    conexion.close()


# PREGUNTA 9: Eliminar empleado

def eliminar_empleado(dni):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM empleados WHERE dni = ?", (dni,))
    conexion.commit()
    conexion.close()