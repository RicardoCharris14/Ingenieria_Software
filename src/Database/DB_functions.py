import sqlite3
from datetime import datetime, timedelta


def obtener_recordatorios():
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        query = """
        SELECT id, numero_paciente, mensaje, tiempo_envio 
        FROM Recordatorios
        """
        cursor.execute(query)
        recordatorios = cursor.fetchall()

        return recordatorios

    except Exception as ex:
        print(f"Error al obtener recordatorios: {ex}")
        return []
    finally:
        connection.close()

def obtener_horario(id_horario):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        query = """
        SELECT id, fecha, hora_inicio, hora_fin, rut_especialista
        FROM Horario_Atencion
        WHERE id = ?
        """
        cursor.execute(query, (id_horario,))
        horario = cursor.fetchone()

        if horario:
            return horario
        return None 
    except Exception as ex:
        print(f"Error al obtener el horario: {ex}")
        return None
    finally:
        connection.close()

def guardar_recordatorio(id_cita, numero_paciente, mensaje, tiempo_envio):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()
   
        cursor.execute(
            """
            INSERT INTO recordatorios (id, numero_paciente, mensaje, tiempo_envio) VALUES (?, ?, ?, ?)
            """, (id_cita, numero_paciente, mensaje, tiempo_envio)
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
        instruction = "SELECT rut, nombre, especialidad FROM Especialista "
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

        cursor.execute("""SELECT rut, nombre, contraseña, especialidad, valor_atencion FROM Especialista WHERE rut = ?""", (rut_especialista,))
        
        row = cursor.fetchone()
        
        if not row:
            return None

        doctor = {'rut': row[0], 'nombre': row[1], 'contraseña': row[2], 'especialidad': row[3], 'valor_atencion': row[4]}
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
        horarios = [{'especialista': row[0], 'fecha': datetime.strptime(row[1], '%Y-%m-%d').strftime('%d-%m-%Y'), 'hora_inicio': row[2], 'hora_fin': row[3], 'id':row[4]} for row in cursor.fetchall()]
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
        params = cursor.fetchone()
        parametros = {'fecha_inicio': params[0], 'fecha_final': params[1]}
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
        SELECT h.id, e.nombre AS especialista, h.fecha, h.hora_inicio, h.hora_fin, h.disponible
        FROM Especialista e
        INNER JOIN Horario_Atencion h ON e.rut = h.rut_especialista
        WHERE e.rut = ?
        ORDER BY h.fecha ASC, h.hora_inicio ASC
        """
        cursor.execute(query, (rut_especialista,))
        horarios = cursor.fetchall()

        horarios = [{'id': horario[0], 'fecha': datetime.strptime(horario[2], '%Y-%m-%d').strftime('%d-%m-%Y'), 'hora_inicio': horario[3], 'hora_fin': horario[4], 'disponible': horario[5]} for horario in horarios]

        connection.close()
        return horarios
    except Exception as ex:
        print(ex)
        return []
    finally:
        connection.close()

def agregar_horario(rut_especialista, fecha, hora_inicio, hora_fin):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO Horario_Atencion (fecha, hora_inicio, hora_fin, rut_especialista, disponible)
            VALUES (?, ?, ?, ?, 1)
        """, (fecha, hora_inicio, hora_fin, rut_especialista))

        connection.commit()
    except Exception as ex:
        print(ex)
        raise ex
    finally:
        connection.close()

def eliminar_horario(id):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        cursor.execute("DELETE FROM Horario_Atencion WHERE id = ?", (id,))
        connection.commit()
    except Exception as ex:
        print(ex)
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
        ORDER BY H.fecha ASC, h.hora_inicio ASC
        """
        cursor.execute(query, (rut_especialista,))
        citas = cursor.fetchall()

        return [{'nombre_paciente': row[0], 'rut_paciente': row[1],'id_horario': row[2], 'fecha': datetime.strptime(row[3], '%Y-%m-%d').strftime('%d-%m-%Y') , 'hora_inicio': row[4], 'hora_fin': row[5]} for row in citas]
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

def get_citas_paciente(rut_paciente):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        query = """
        SELECT P.nombre AS paciente_nombre, E.nombre, C.id_horario, H.fecha, H.hora_inicio, H.hora_fin
        FROM Cita C
        JOIN Paciente P ON C.rut_paciente = P.rut
        JOIN Horario_Atencion H ON C.id_horario = H.id
        JOIN Especialista E ON C.rut_especialista = E.rut
        WHERE C.rut_paciente = ?
        ORDER BY H.fecha ASC, h.hora_inicio ASC
        """
        cursor.execute(query, (rut_paciente,))
        citas = cursor.fetchall()

        return [{'nombre_paciente': row[0], 'nombre_especialista': row[1], 'id_horario': row[2], 'fecha': datetime.strptime(row[3], '%Y-%m-%d').strftime('%d-%m-%Y') , 'hora_inicio': row[4], 'hora_fin': row[5]} for row in citas]
    except Exception as ex:
        print(ex)
        return []
    finally:
        connection.close()

def get_datos_paciente(rut_paciente):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        query = """
        SELECT P.rut, P.nombre, P.fecha_nacimiento, P.telefono, P.correo
        FROM Paciente P
        WHERE rut = ?
        """
        cursor.execute(query, (rut_paciente,))
        citas = cursor.fetchone()

        return {'rut': citas[0], 'nombre': citas[1], 'fecha_nacimiento': datetime.strptime(citas[2], '%Y-%m-%d').strftime('%d-%m-%Y') , 'telefono': citas[3], 'correo': citas[4]}
    except Exception as ex:
        print(ex)
        return []
    finally:
        connection.close()

def eliminar_cita(id_horario):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        cursor.execute("DELETE FROM Cita WHERE id_horario = ?", (id_horario,))
        connection.commit()
    except Exception as ex:
        print(ex)
        raise ex
    finally:
        connection.close()

def buscar_paciente(rut, password):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Paciente WHERE rut = ? AND contraseña = ?", (rut, password))
        paciente = cursor.fetchone()

        if paciente:
            return {'rut': paciente[0], 'nombre': paciente[1], 'fecha_nacimiento': paciente[3], 'telefono': paciente[4], 'correo': paciente[5]}
        return None
    except Exception as ex:
        print(f"Error al buscar el paciente: {ex}")
        return None
    finally:
        connection.close()

def buscar_paciente_por_rut(rut):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Paciente WHERE rut = ?", (rut,))
        paciente = cursor.fetchone()

        return paciente is not None
    except Exception as ex:
        print(f"Error al buscar el paciente por RUT: {ex}")
        return False
    finally:
        connection.close()

def crear_cuenta_paciente(rut, nombre, password, fecha_nacimiento, telefono, correo):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO Paciente (rut, nombre, contraseña, fecha_nacimiento, telefono, correo)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (rut, nombre, password, fecha_nacimiento, telefono, correo))

        connection.commit()
    except Exception as ex:
        print(f"Error al crear la cuenta del paciente: {ex}")
        raise ex
    finally:
        connection.close()

def cambiar_contraseña_admin(nueva_contraseña):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE Parametro
            SET contraseña_admin = ?
            WHERE id = 1
        """, (nueva_contraseña,))

        connection.commit()
    except Exception as ex:
        print(f"Error al cambiar la contraseña del administrador: {ex}")
        raise ex
    finally:
        connection.close()

def cambiar_fechas(fecha_inicial, fecha_final):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE Parametro
            SET fecha_inicio = ?, fecha_final = ?
            WHERE id = 1
        """, (fecha_inicial, fecha_final))

        connection.commit()
    except Exception as ex:
        print(f"Error al cambiar las fechas: {ex}")
        raise ex
    finally:
        connection.close()

def anadir_especialista(rut, nombre, contrasena, especialidad, valor_atencion, telefono, correo):
    try:
        connection = sqlite3.connect("./src/Database/bd")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO Especialista (rut, nombre, contraseña, especialidad, valor_atencion, telefono, correo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (rut, nombre, contrasena, especialidad, valor_atencion, telefono, correo))

        connection.commit()
    except Exception as ex:
        print(f"Error al añadir el especialista: {ex}")
        raise ex
    finally:
        connection.close()