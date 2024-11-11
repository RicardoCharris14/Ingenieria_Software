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
        
        CREATE TABLE citas (
        id_cita INTEGER PRIMARY KEY AUTOINCREMENT,
        rut_paciente TEXT NOT NULL,
        nombre_paciente TEXT NOT NULL,
        rut_especialista TEXT NOT NULL,
        nombre_especialista TEXT NOT NULL,
        id_horario INTEGER NOT NULL,
        fecha_cita TEXT NOT NULL,  -- Puedes agregar una fecha de la cita si es necesario
        FOREIGN KEY (rut_paciente) REFERENCES paciente(rut),
        FOREIGN KEY (nombre_paciente) REFERENCES paciente(nombre),
        FOREIGN KEY (rut_especialista) REFERENCES especialista(rut),
        FOREIGN KEY (nombre_especialista) REFERENCES especialista(nombre),
        FOREIGN KEY (id_horario) REFERENCES horario(id)
        );
                         
        CREATE TABLE Prevision (
            nombre TEXT PRIMARY KEY
        );
                         
        CREATE TABLE Prevision_especialista (
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