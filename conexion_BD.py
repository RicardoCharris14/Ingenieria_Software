import sqlite3

try:
    connection = sqlite3.connect("Database/bd")
    cursor = connection.cursor()

    cursor.executescript("""
        BEGIN;
        CREATE TABLE Especialista(
            nombre TEXT NOT NULL,
            especialidad TEXT NO NULL,
            rut TEXT NOT NULL,
            telefono INTEGER,
            correo TEXT NOT NULL);

        CREATE TABLE Horario_Atencion(
            id INTEGER PRIMARY KEY,
            dia TEXT NOT NULL,
            inicio INTEGER,
            fin INTEGER, 
            valor INTEGER,
            disponible INTEGER,
            especialista TEXT NOT NULL,
            FOREIGN KEY (especialista) REFERENCES Especialista(nombre));
        COMMIT;
    """)

    cursor.execute("""
    CREATE TABLE calendario_semanal (
        fecha_inicio TEXT NOT NULL,
        fecha_termino TEXT NOT NULL,
        rut_especialista TEXT NOT NULL
        PRIMARY KEY (fecha_inicio, fecha_termino),
        FOREIGN KEY (rut_especialista) REFERENCES Especialista(rut)
    )
    """)

    connection.commit() #Guarda los cambios en la BD

except Exception as ex:
    print(ex)
finally:
    connection.close() #Cierra la conexion con la BD