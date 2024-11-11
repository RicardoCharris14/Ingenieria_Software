import sqlite3

try:
    connection = sqlite3.connect("Database/bd")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE calendario_semanal (
        fecha_inicio TEXT NOT NULL,
        fecha_termino TEXT NOT NULL,
        rut_especialista TEXT NOT NULL
        PRIMARY KEY (fecha_inicio, fecha_termino),
        FOREIGN KEY (rut_especialista) REFERENCES especialista(rut)
    )
    """)

    # Crear tabla prevision
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prevision (
        nombre TEXT PRIMARY KEY NOT NULL
    )
    """)

    # Crear tabla prevision_especialista
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prevision_especialista (
        nombre_prevision TEXT NOT NULL,
        rut_especialista TEXT NOT NULL,
        FOREIGN KEY (nombre_prevision) REFERENCES prevision(nombre),
        FOREIGN KEY (rut_especialista) REFERENCES especialista(rut),
        PRIMARY KEY (nombre_prevision, rut_especialista)
    )
    """)

    connection.commit() #Guarda los cambios en la BD

except Exception as ex:
    print(ex)
finally:
    connection.close() #Cierra la conexion con la BD