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


#from this place start the test for "horarios" and "precios" and "buscador"
def obtener_especialidades():
    try:
        connection = sqlite3.connect("Database/bd")
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT especialidad FROM Especialista")
        especialidades = [row[0] for row in cursor.fetchall()]
        return especialidades
    except Exception as ex:
        print(ex)
        return []
    finally:
        connection.close()

def obtener_doctores():
    try:
        connection = sqlite3.connect("Database/bd")
        cursor = connection.cursor()
        cursor.execute("SELECT rut, nombre FROM Especialista")
        doctores = [{'rut': row[0], 'nombre': row[1]} for row in cursor.fetchall()]
        return doctores
    except Exception as ex:
        print(ex)
        return []
    finally:
        connection.close()

def obtener_horarios(especialidad, dia, hora, doctor):
    try:
        connection = sqlite3.connect("Database/bd")
        cursor = connection.cursor()

        # Construir la consulta SQL con filtros
        query = "SELECT H.dia, E.nombre, H.hora_inicio, H.precio, P.nombre " \
                "FROM Horario_Atencion H " \
                "JOIN Especialista E ON H.rut_especialista = E.rut " \
                "JOIN Prevision_especialista PE ON E.rut = PE.rut_especialista " \
                "JOIN Prevision P ON PE.nombre_prevision = P.nombre " \
                "WHERE H.disponible = 1"

        params = []
        if especialidad:
            query += " AND E.especialidad = ?"
            params.append(especialidad)
        if dia:
            query += " AND H.dia = ?"
            params.append(dia)
        if hora:
            query += " AND H.hora_inicio = ?"
            params.append(hora)
        if doctor:
            query += " AND E.rut = ?"
            params.append(doctor)

        cursor.execute(query, tuple(params))
        horarios = cursor.fetchall()
        return horarios
    except Exception as ex:
        print(ex)
        return []
    finally:
        connection.close()

def obtener_costo_atencion(rut_especialista):
    try:
        connection = sqlite3.connect("Database/bd")
        cursor = connection.cursor()

        # Obtener el costo de atención del especialista
        cursor.execute("SELECT AVG(precio) FROM Horario_Atencion WHERE rut_especialista = ?", (rut_especialista,))
        costo = cursor.fetchone()[0]

        return costo

    except Exception as ex:
        print(ex)
        return None  #Devuelve O, un valor por defecto en caso de error
    finally:
        connection.close()
