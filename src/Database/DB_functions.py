import sqlite3

def obtener_especialidades():
    try:
        connection = sqlite3.connect("./src/Database/bd")
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
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()
        cursor.execute("SELECT rut, nombre, especialidad FROM Especialista")
        doctores = [{'rut': row[0], 'nombre': row[1], 'especialidad': row[2]} for row in cursor.fetchall()]
        return doctores
    except Exception as ex:
        print(ex)
        return []
    finally:
        connection.close()

def obtener_horarios(especialidad, dia, hora, doctor):
    try:
        connection = sqlite3.connect("./src/Database/bd")
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
        connection = sqlite3.connect("./src/Database/bd")
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
