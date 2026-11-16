import sqlite3

# PREGUNTA 1: Conexión segura con SQLite

RUTA_BD = "empleados.db"

conexion = sqlite3.connect(RUTA_BD, check_same_thread=False)
cursor = conexion.cursor()


def probar_conexion():
    try:
        cursor.execute("SELECT 1")
        cursor.fetchone()
        return True
    except sqlite3.Error:
        return False


# PREGUNTA 2: Creación de la tabla empleados

def crear_tablas():
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


# PREGUNTA 5: Insertar un empleado

def insertar_empleado(dni, nombre_apellido, cargo, area, salario, fecha_ingreso, estado):
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

# PREGUNTA 6: Obtener todos los empleados

def ver_todos_empleados():
    cursor.execute("SELECT * FROM empleados")
    return cursor.fetchall()

# PREGUNTA 7: Búsquedas

def buscar_por_dni(dni):
    cursor.execute("SELECT * FROM empleados WHERE dni = ?", (dni,))
    return cursor.fetchall()


def buscar_por_nombre(texto):
    cursor.execute("SELECT * FROM empleados WHERE nombre_apellido LIKE ?", (f"%{texto}%",))
    return cursor.fetchall()

# PREGUNTA 8: Actualizar empleado 

def actualizar_empleado(dni, cargo, area, salario, estado):
    cursor.execute(
        "UPDATE empleados SET cargo = ?, area = ?, salario = ?, estado = ? WHERE dni = ?",
        (cargo, area, salario, estado, dni)
    )
    conexion.commit()

# PREGUNTA 9: Eliminar empleado

def eliminar_empleado(dni):
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM empleados WHERE dni = ?", (dni,))
    conexion.commit()    