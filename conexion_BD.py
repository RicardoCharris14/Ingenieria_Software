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

    connection.commit() #Guarda los cambios en la BD

except Exception as ex:
    print(ex)
finally:
    connection.close() #Cierra la conexion con la BD