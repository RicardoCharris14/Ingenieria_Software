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

def obtener_doctores(rutE):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()
        instruction = "SELECT rut, nombre, especialidad FROM Especialista" \
                      ""
        parameters = []
        if rutE:
            instruction += "WHERE rut = ?"
            parameters.append(rutE)

        cursor.execute(instruction, parameters)
        doctores = [{'rut': row[0], 'nombre': row[1], 'especialidad': row[2]} for row in cursor.fetchall()]
        return doctores
    except Exception as ex:
        print(ex)
        return []
    finally:
        connection.close()


def buscar_doctor(rut_especialista):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        cursor.execute("""SELECT rut, nombre, especialidad, valor_atencion FROM Especialista WHERE rut = ?""", (rut_especialista,))
        
        row = cursor.fetchone()
        
        if not row:
            return None

        doctor = {'rut': row[0],'nombre': row[1],'especialidad': row[2],'valor_atencion': row[3]}
        return doctor
    except Exception as ex:
        print(f"Error al buscar el doctor: {ex}")
        return None
    finally:
        connection.close()

def obtener_horarios_disponibles(especialidad, primer_dia, ultimo_dia, hora, doctor):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        # Construir la consulta SQL con filtros
        query = "SELECT E.nombre, H.fecha, H.hora_inicio, H.hora_fin, H.id " \
                "FROM Especialista E " \
                "LEFT JOIN Horario_Atencion H ON H.rut_especialista = E.rut " \
                "WHERE H.disponible = 1"

        params = []
        if especialidad:
            query += " AND E.especialidad = ?"
            params.append(especialidad)
        if primer_dia:
            query += " AND H.fecha >= ?"
            params.append(primer_dia)
        if ultimo_dia:
            query += " AND H.fecha <= ?"
            params.append(ultimo_dia)
        if hora:
            query += " AND H.hora_inicio = ?"
            params.append(hora)
        if doctor:
            query += " AND E.rut = ?"
            params.append(doctor)

        query += " ORDER BY H.fecha ASC"

        cursor.execute(query, tuple(params))
        horarios = [{'especialista': row[0], 'fecha': row[1], 'hora_inicio': row[2], 'hora_fin': row[3], 'id':row[4]} for row in cursor.fetchall()]
        return horarios
    except Exception as ex:
        print(ex)
        return []
    finally:
        connection.close()

def obtener_periodo_temporal():
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT fecha_inicio, fecha_final FROM Parametro
            """
        )
        parametros = [{'fecha_inicio': row[0], 'fecha_final': row[1]} for row in cursor.fetchall()]
        return parametros
    except Exception as ex:
        print(ex)
        return []
    finally:
        connection.close()

def reservar_horario(rutPaciente, rutEspecialista, idHorario):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO Cita (id_horario, rut_paciente, rut_especialista) VALUES (?, ?, ?)
            """, (idHorario, rutPaciente, rutEspecialista)
        )
        connection.commit()

        if cursor.rowcount == 0:
            return 0
        else:
            return 1
    except Exception as ex:
        print(ex)
    finally:
        connection.close()



def bloquear_horario(id):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE Horario_Atencion
            SET disponible = 0
            WHERE id = ?
            """,(id,)
            )
        connection.commit()
    except Exception as ex:
        print(ex)
    finally:
        connection.close()

#Modificar pues valor se movio a especialista
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

def obtener_citas_especialista(rut_especialista):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        query = """
        SELECT P.nombre AS paciente_nombre, P.rut AS paciente_rut, C.id_horario, H.fecha, H.hora_inicio, H.hora_fin
        FROM Cita C
        JOIN Paciente P ON C.rut_paciente = P.rut
        JOIN Horario_Atencion H ON C.id_horario = H.id
        WHERE C.rut_especialista = ?
        """
        cursor.execute(query, (rut_especialista,))
        citas = cursor.fetchall()

        return [{'nombre_paciente': row[0], 'rut_paciente': row[1], 'fecha': row[3], 'hora_inicio': row[4], 'hora_fin': row[5]} for row in citas]
    except Exception as ex:
        print(ex)
        return []
    finally:
        connection.close()

# * modificar obtener_costo_atencion

def obtener_previsiones_especialista(rut_especialista):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        query = """
                SELECT E.nombre, PE.nombre_prevision
                FROM Especialista E
                JOIN Prevision_Especialista PE ON E.rut = PE.rut_especialista
                """
        params = []
        if rut_especialista:
            query += " WHERE E.rut = ?"
            params.append(rut_especialista)

        cursor.execute(query, params)  
        especialistas_con_previsiones = [{'especialista': row[0], 'prevision': row[1]} for row in cursor.fetchall()] 

        return especialistas_con_previsiones
    except Exception as ex:
        print(ex)
        return []
    finally:
        connection.close()

def obtener_previsiones():
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT nombre FROM Prevision
            """
        ) 
        previsiones = cursor.fetchall()

        return previsiones
    
    except Exception as ex:
        print(ex)
        return []
    finally:
        connection.close()

def get_admin_password():
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT contraseña_admin FROM Parametro
            """
        )

        password = cursor.fetchall()
        password = password[0][0]
        return password
    
    except Exception as ex:
        print(ex)
        return []
    finally:
        connection.close()

