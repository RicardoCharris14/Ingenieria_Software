import sqlite3

try:
    connection = sqlite3.connect("Database/bd")
    cursor = connection.cursor()

    cursor.executescript("""
        BEGIN;
        CREATE TABLE Especialista(
            rut TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            especialidad TEXT NOT NULL,
            telefono INTEGER,
            correo TEXT
        );
        
        CREATE TABLE Calendario_semanal (
            fecha_inicio TEXT,
            fecha_termino TEXT,
            rut_especialista TEXT NOT NULL
            PRIMARY KEY (fecha_inicio, fecha_termino),
            FOREIGN KEY (rut_especialista) REFERENCES Especialista(rut)
        );                 
        
        CREATE TABLE Horario_Atencion(
            id INTEGER PRIMARY KEY,
            dia TEXT NOT NULL,
            hora_inicio INTEGER NOT NULL,
            hora_fin INTEGER NOT NULL, 
            precio INTEGER,
            disponible INTEGER NOT NULL,
            fecha_inicio TEXT NOT NULL,
            fecha_termino TEXT NOT NULL,             
            FOREIGN KEY (fecha_inicio, fecha_termino) REFERENCES Calendario_semanal(fecha_inicio, fecha_termino)
            );
                         
        CREATE TABLE IF NOT EXISTS Prevision (
            nombre TEXT PRIMARY KEY
        );
                         
        CREATE TABLE IF NOT EXISTS Prevision_especialista (
            nombre_prevision TEXT NOT NULL,
            rut_especialista TEXT NOT NULL,
            FOREIGN KEY (nombre_prevision) REFERENCES Prevision(nombre),
            FOREIGN KEY (rut_especialista) REFERENCES Especialista(rut),
            PRIMARY KEY (nombre_prevision, rut_especialista)
        );
                         
        COMMIT;
    """)


    connection.commit() #Guarda los cambios en la BD

except Exception as ex:
    print(ex)
finally:
    connection.close() #Cierra la conexion con la BD