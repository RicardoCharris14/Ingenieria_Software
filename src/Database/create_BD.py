import sqlite3

try:
    connection = sqlite3.connect("./src/Database/bd")
    cursor = connection.cursor()

    cursor.executescript("""
        BEGIN;
                         
        CREATE TABLE Paciente(
            rut TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            fecha_nacimiento TEXT NOT NULL,
            telefono TEXT NOT NULL,
            correo TEXT NOT NULL
        );
                         
        CREATE TABLE Especialista(
            rut TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            especialidad TEXT NOT NULL,
            valor_atencion INTEGER NOT NULL,
            telefono TEXT NOT NULL,
            correo TEXT NOT NULL
        );         
        
        CREATE TABLE Horario_Atencion(
            id INTEGER PRIMARY KEY,
            fecha TEXT NOT NULL,
            hora_inicio INTEGER NOT NULL,
            hora_fin INTEGER NOT NULL,
            rut_especialista TEXT NOT NULL,
            disponible INTEGER NOT NULL,           
            FOREIGN KEY (rut_especialista) REFERENCES Especialista(rut)
        );
        
        CREATE TABLE Citas (
            id_cita INTEGER PRIMARY KEY AUTOINCREMENT,
            rut_paciente TEXT NOT NULL,
            rut_especialista TEXT NOT NULL,
            id_horario INTEGER NOT NULL,
            asistio INTEGER NOT NULL,
            FOREIGN KEY (rut_paciente) REFERENCES Paciente(rut),
            FOREIGN KEY (rut_especialista) REFERENCES Especialista(rut),
            FOREIGN KEY (id_horario) REFERENCES Horario_Atencion(id)
        );
                         
        CREATE TABLE Prevision (
            nombre TEXT PRIMARY KEY
        );
                         
        CREATE TABLE Prevision_Especialista (
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
