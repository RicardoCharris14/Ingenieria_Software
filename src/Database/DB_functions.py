import sqlite3


def modificar_disponibilidad_horario(id_horario, disponibilidad):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        cursor.execute("UPDATE Horario_Atencion SET disponible = ? WHERE id = ?", (disponibilidad, id_horario))

        connection.commit()

    except Exception as ex:
        print(ex)
    finally:
        connection.close() 

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

def obtener_horarios_disponibles(especialidad, primer_dia, ultimo_dia, hora, doctor):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        # Construir la consulta SQL con filtros
        query = "SELECT H.dia, E.nombre, H.hora_inicio, H.precio, P.nombre " \
                "FROM Especialista E " \
                "LEFT JOIN Horario_Atencion H ON H.rut_especialista = E.rut " \
                "WHERE H.disponible = 1"

        params = []
        if especialidad:
            query += " AND E.especialidad = ?"
            params.append(especialidad)
        if primer_dia:
            query += " AND H.dia > ?"
            params.append(primer_dia)
        if ultimo_dia:
            query += " AND H.dia < ?"
            params.append(ultimo_dia)
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

#Funcion nuevas
def obtener_horarios_especialistas(rut_especialista):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()
        
        query = """
        SELECT e.nombre AS especialista, h.fecha, h.hora_inicio, h.hora_fin, h.disponible
        FROM Especialista e
        INNER JOIN Horario_Atencion h ON e.rut = h.rut_especialista
        WHERE e.rut = ?
        """
        cursor.execute(query, (rut_especialista,))
        horarios = cursor.fetchall()

        connection.close()
        return horarios
    except Exception as ex:
        print(ex)
        return None  #Devuelve O, un valor por defecto en caso de error
    finally:
        connection.close()

