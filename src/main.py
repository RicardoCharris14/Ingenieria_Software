from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, session
#import pywhatkit as kit
import datetime
import threading
from Database import DB_functions


# def inicializar_recordatorios():
#     recordatorios = DB_functions.obtener_recordatorios()
    
#     for recordatorio in recordatorios:
#         print(recordatorio)
#         id_horario, numero_paciente, mensaje, fecha_envio = recordatorio

#         fecha_hora_envio = datetime.datetime.strptime(fecha_envio, '%Y-%m-%d %H:%M:%S')
     
#         diferencia = (fecha_hora_envio - datetime.datetime.now()).total_seconds()
        
#         if diferencia > 0:
#             enviar_recordatorio(numero_paciente, mensaje, fecha_hora_envio)
#         else:
#             print(f"El recordatorio para {numero_paciente} a las {fecha_hora_envio} ya pasó.")

# def enviar_recordatorio(numero, mensaje, tiempo_envio):
#     """Función para programar el envío de un recordatorio en el momento indicado."""
#     diferencia = (tiempo_envio - datetime.datetime.now()).total_seconds()
#     if diferencia > 0:
#         threading.Timer(diferencia, lambda: kit.sendwhatmsg_instantly(numero, mensaje)).start()
#         print(f"Recordatorio programado para {numero} en {tiempo_envio}.")
#         return True
#     else:
#         return False

app = Flask(__name__)
app.secret_key = 'IngSoftware'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logPaciente')
def logPaciente():
    return render_template('logPaciente.html')

@app.route('/login_paciente', methods=['POST'])
def login_paciente():
    rut = request.form.get('rut')
    password = request.form.get('password')
    if not rut or not password:
        flash('RUT o contraseña no ingresados', 'danger')
        return redirect(url_for('logPaciente'))

    # Verificar si el RUT y la contraseña pertenecen a un paciente
    paciente = DB_functions.buscar_paciente(rut, password)
    if paciente:
        session['rut_paciente'] = rut
        return redirect(url_for('paciente'))

    flash('RUT o contraseña incorrectos', 'danger')
    return redirect(url_for('logPaciente'))

@app.route('/crear_cuenta_paciente', methods=['GET', 'POST'])
def crear_cuenta_paciente():
    if request.method == 'POST':
        rut = request.form.get('rut')
        nombre = request.form.get('nombre')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        telefono = request.form.get('telefono')
        correo = request.form.get('correo')
        password = request.form.get('password')

        # Verificar si el RUT ya existe en la base de datos
        if DB_functions.buscar_paciente_por_rut(rut):
            flash('El RUT ya está registrado', 'danger')
            return render_template('crear_cuenta_paciente.html', rut=rut, nombre=nombre, fecha_nacimiento=fecha_nacimiento, telefono=telefono, correo=correo)

        # Crear la cuenta del paciente
        try:
            DB_functions.crear_cuenta_paciente(rut, nombre, password, fecha_nacimiento, telefono, correo)
            flash('Cuenta creada exitosamente', 'success')
            return redirect(url_for('logPaciente'))
        except Exception as ex:
            print(ex)
            flash('Error al crear la cuenta', 'danger')
            return render_template('crear_cuenta_paciente.html', rut=rut, nombre=nombre, fecha_nacimiento=fecha_nacimiento, telefono=telefono, correo=correo)
    return render_template('crear_cuenta_paciente.html')

@app.route('/paciente')
def paciente():
    return render_template('paciente.html')

@app.route('/paciente/citas')
def citas_paciente():
    rut_paciente = session.get('rut_paciente')
    paciente = DB_functions.get_datos_paciente(rut_paciente)
    citas = DB_functions.get_citas_paciente(rut_paciente)
    return render_template('citas_paciente.html', rut_paciente = rut_paciente, citas = citas, paciente = paciente)

@app.route('/eliminar_cita/<int:id_horario>', methods=['DELETE'])
def eliminar_cita(id_horario):
    try:
        DB_functions.eliminar_cita(id_horario)
        DB_functions.modificar_disponibilidad_horario(id_horario, '1')
        return jsonify({'success': True})
    except Exception as ex:
        print(ex)
        return jsonify({'success': False, 'error': str(ex)})

# Rutas adicionales para otras secciones
@app.route('/<rutE>/doctor')
def doctor(rutE):
    especialista = DB_functions.obtener_doctores(rutE)
    horarios = DB_functions.obtener_horarios_especialistas(rutE)  # Usamos rut para obtener los horarios
    especialista_horarios = {
        'especialista': especialista,
        'horarios': horarios
    }
    
    #Fin Cambio
    return render_template('doctor.html', especialista_horarios=especialista_horarios)

@app.route('/logAdmin')
def logAdmin():
    return render_template('logAdmin.html')

@app.route('/admin_login', methods=['POST'])
def admin_login():
    admin_password = DB_functions.get_admin_password()
    password = request.form.get('password')
    if password == admin_password:
        flash('Inicio de sesion exitoso', 'success')
        return redirect(url_for('administrativo'))
    else:
        flash('Contraseña incorrecta', 'danger')
        return redirect(url_for('logAdmin'))

@app.route('/administrativo')
def administrativo():
    return render_template('administradores.html')

@app.route('/anadir_especialista', methods=['GET', 'POST'])
def anadir_especialista():
    if request.method == 'POST':
        rut = request.form.get('rut')
        nombre = request.form.get('nombre')
        especialidad = request.form.get('especialidad')
        valor_atencion = request.form.get('valor_atencion')
        telefono = request.form.get('telefono')
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')

        try:
            DB_functions.anadir_especialista(rut, nombre, contraseña, especialidad, valor_atencion, telefono, correo)
            flash('Especialista añadido exitosamente', 'success')
            return redirect(url_for('administrativo'))
        except Exception as ex:
            print(ex)
            flash('Error al añadir el especialista', 'danger')
            return render_template('anadir_especialista.html', rut=rut, nombre=nombre, especialidad=especialidad, valor_atencion=valor_atencion, telefono=telefono, correo=correo, contraseña=contraseña)
    return render_template('anadir_especialista.html')

@app.route('/administrativo/gestionar_especialistas')
def gestionar_especialistas():
    #Inicio Cambio
    especialistas = DB_functions.obtener_doctores("")
    especialistas_horarios = []
    for especialista in especialistas:
        # Obtener los horarios para cada especialista
        horarios = DB_functions.obtener_horarios_especialistas(especialista['rut'])  # Usamos rut para obtener los horarios
        especialistas_horarios.append({
            'especialista': especialista,
            'horarios': horarios
        })

    return render_template('gestionar_especialistas.html', especialistas_horarios=especialistas_horarios)

@app.route('/administrativo/gestionar_horarios')
def gestionar_horarios():
    rut_especialista = session.get('rut_especialista')
    especialista = DB_functions.buscar_doctor(rut_especialista)
    citas = DB_functions.obtener_citas_especialista(rut_especialista)
    horarios = DB_functions.obtener_horarios_especialistas(rut_especialista)
    return render_template('gestionar_horarios.html', especialista=especialista, citas=citas, horarios=horarios)

@app.route('/administrativo/gestionar_horarios', methods=['POST'])
def post_gestionar_horarios():
    rut_especialista = request.form.get('rut_especialista')
    session['rut_especialista'] = rut_especialista
    return redirect(url_for('gestionar_horarios'))

@app.route('/agregar_horario', methods=['POST'])
def agregar_horario():
    rut_especialista = request.form.get('rut_especialista')
    fecha = request.form.get('fecha')
    hora_inicio = request.form.get('hora_inicio')
    hora_fin = request.form.get('hora_fin')

    try:
        DB_functions.agregar_horario(rut_especialista, fecha, hora_inicio, hora_fin)
        flash('Horario agregado exitosamente', 'success')
    except Exception as ex:
        print(ex)
        flash('Error al agregar el horario', 'danger')

    return redirect(url_for('gestionar_horarios'))

@app.route('/eliminar_horario/<int:id>', methods=['DELETE'])
def eliminar_horario(id):
    try:
        DB_functions.eliminar_horario(id)
        return jsonify({'success': True})
    except Exception as ex:
        print(ex)
        return jsonify({'success': False, 'error': str(ex)})


@app.route('/administrativo/configuraciones')
def configuraciones():
    return render_template('configuraciones.html')

@app.route('/cambiar_contraseña_admin', methods=['POST'])
def cambiar_contraseña_admin():
    nueva_contraseña = request.form.get('nueva_contraseña')
    if not nueva_contraseña:
        flash('La nueva contraseña no puede estar vacía', 'danger')
        return redirect(url_for('configuraciones'))

    try:
        DB_functions.cambiar_contraseña_admin(nueva_contraseña)
        flash('Contraseña cambiada exitosamente', 'success')
    except Exception as ex:
        print(ex)
        flash('Error al cambiar la contraseña', 'danger')

    return redirect(url_for('configuraciones'))

@app.route('/cambiar_fechas', methods=['POST'])
def cambiar_fechas():
    fecha_inicial = request.form.get('fecha_inicial')
    fecha_final = request.form.get('fecha_final')
    if not fecha_inicial or not fecha_final:
        flash('Las fechas no pueden estar vacías', 'danger')
        return redirect(url_for('configuraciones'))

    try:
        DB_functions.cambiar_fechas(fecha_inicial, fecha_final)
        flash('Fechas modificadas exitosamente', 'success')
    except Exception as ex:
        print(ex)
        flash('Error al modificar las fechas', 'danger')

    return redirect(url_for('configuraciones'))

@app.route('/buscar_especialistas')
def buscar_especialistas():
    # Lógica para buscar especialista
    especialistas = DB_functions.obtener_doctores("")
    return render_template('buscar_especialistas.html', especialistas=especialistas)

@app.route('/seleccionar_especialista')
def seleccionar_especialista():
    especialistas = DB_functions.obtener_doctores("")
    return render_template('seleccionar_especialista.html', especialistas=especialistas)

@app.route('/paciente/seleccionar_especialista/agendar_hora/<rutE>')
def agendar_hora(rutE):
    rutP = session.get('rut_paciente')
    intervalo = DB_functions.obtener_periodo_temporal()
    horarios = DB_functions.obtener_horarios_disponibles("", intervalo['fecha_inicio'], intervalo['fecha_final'],"", rutE)
    especialista = DB_functions.buscar_doctor(rutE)
    previsiones = DB_functions.obtener_previsiones_especialista(rutE)
    print(previsiones)

    fechas = []
    for horario in horarios:
        if horario['fecha'] not in fechas:
            fechas.append(horario['fecha'])
    participantes = {'paciente': rutP, 'especialista': rutE}
    return render_template('agendar_hora.html', participantes=participantes, horarios=horarios, fechas=fechas, especialista=especialista, previsiones=previsiones)

@app.route('/reservar_cita', methods=['POST'])
def reservar():
    data = request.get_json()
    id = int(data.get('id'))
    rutP = data.get('rutPaciente')
    rutE = data.get('rutEspecialista')
    print(f"id: {id}, rut paciente: {rutP}, rut especialista: {rutE}")
    try:
        if(DB_functions.reservar_horario(rutP, rutE, id)):
            DB_functions.bloquear_horario(id)
            
            horario = DB_functions.obtener_horario(id)
            id_horario, fecha, hora_inicio, hora_fin, rut_especialista = horario
            numero_paciente = "+56984450039"
            mensaje = f"Hola, recuerde su cita con el especialista {rut_especialista} el día {fecha} a las {hora_inicio}."
            fecha_hora_envio = datetime.datetime.strptime(f"{fecha} {hora_inicio}", '%Y-%m-%d %H:%M') - datetime.timedelta(minutes=1)
            
            #if(enviar_recordatorio(numero_paciente, mensaje, fecha_hora_envio)):
            #  DB_functions.guardar_recordatorio(id, numero_paciente, mensaje, fecha_hora_envio)
    
        return jsonify({'success': True})
    except Exception as ex:
        print(ex)
        return jsonify({'success': False, 'error': str(ex)})
    

#codigo para buscar horarios, especialidades y especialistas. También precios.

@app.route('/obtener_especialidades')
def obtener_especialidades_ruta():
    try:
        especialidades = DB_functions.obtener_especialidades()  # Llama a la función desde DB_functions
        return jsonify(especialidades)
    except Exception as ex:
        print(ex)
        return jsonify({'error': 'Error al obtener las especialidades'}), 500

@app.route('/obtener_doctores')
def obtener_doctores_ruta():
    try:
        doctores = DB_functions.obtener_doctores("")  # Llama a la función desde DB_functions
        return jsonify(doctores)
    except Exception as ex:
        print(ex)
        return jsonify({'error': 'Error al obtener los doctores'}), 500

@app.route('/buscar_horarios', methods=['GET'])
def buscar_horarios():
    try:
        # Obtener los parámetros de la solicitud
        especialidad = request.args.get('especialidad')
        dia = request.args.get('dia')
        hora = request.args.get('hora')
        doctor = request.args.get('doctor')

        # Obtener los horarios de la base de datos
        horarios = DB_functions.obtener_horarios(especialidad, dia, hora, doctor)  # Llama a la función desde DB_functions

        # Formatear los horarios para la respuesta JSON
        horarios_formateados = []
        for horario in horarios:
            horarios_formateados.append([
                horario[0],  # día
                horario[1],  # nombre del especialista
                horario[2],  # hora de inicio de la cita
                horario[3],  # precio (se implementará en un futuro)
                horario[4]   # nombre de la previsión
            ])

        return jsonify(horarios_formateados)

    except Exception as ex:
        print(ex)
        return jsonify({'error': 'Error al obtener los horarios'}), 500
@app.route('/obtener_costo_atencion')
def obtener_costo_atencion():
    try:
        rut_especialista = request.args.get('rut')
        costo = DB_functions.obtener_costo_atencion(rut_especialista)  # Llama a la función en DB_functions.py
        return jsonify(costo)

    except Exception as ex:
        print(ex)
        return jsonify({'error': 'Error al obtener el costo de atención'}), 500

@app.route('/obtener_previsiones')
def obtener_previsiones():
    try:
        previsiones = DB_functions.obtener_previsiones()
        return jsonify(previsiones)
    except Exception as ex:
        print(ex)
        return jsonify({'error': 'Error al obtener las previsiones'}), 500

@app.route('/obtener_medios_pago')
def obtener_medios_pago():
    try:
        medios_pago = DB_functions.obtener_medios_pago()
        return jsonify(medios_pago)
    except Exception as ex:
        print(ex)
        return jsonify({'error': 'Error al obtener los medios de pago'}), 500


if __name__ == "__main__":
    #inicializar_recordatorios()
    app.run(debug=True)