from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, session

from Database import DB_functions



app = Flask(__name__)
app.secret_key = 'IngSoftware'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/paciente')
def paciente():
    return render_template('paciente.html')

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

#FUNCION NUEVA
@app.route('/ver_horarios/<rut_especialista>')
def ver_horarios(rut_especialista):
    horarios = DB_functions.obtener_horarios_especialistas(rut_especialista)
    if horarios is None:
        return jsonify({'error': 'No se pudieron obtener los horarios'}), 500
    return render_template('ver_horarios.html', horarios=horarios)

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
    return render_template('gestionar_horarios.html', especialista=especialista, citas=citas)

@app.route('/administrativo/gestionar_horarios', methods=['POST'])
def post_gestionar_horarios():
    rut_especialista = request.form.get('rut_especialista')
    session['rut_especialista'] = rut_especialista
    return redirect(url_for('gestionar_horarios'))

@app.route('/administrativo/configuraciones')
def configuraciones():
    return

@app.route('/buscar_especialistas')
def buscar_especialistas():
    # Lógica para buscar especialista
    especialistas = DB_functions.obtener_doctores("")
    return render_template('buscar_especialistas.html', especialistas=especialistas)

@app.route('/seleccionar_especialista')
def seleccionar_especialista():
    especialistas = DB_functions.obtener_doctores("")
    return render_template('seleccionar_especialista.html', especialistas=especialistas)

@app.route('/<rutP>/paciente/seleccionar_especialista/agendar_hora/<rutE>')
def agendar_hora(rutP, rutE):
    intervalo = DB_functions.obtener_periodo_temporal()
    horarios = DB_functions.obtener_horarios_disponibles("", intervalo[0]['fecha_inicio'], intervalo[0]['fecha_final'],"", rutE)
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
    app.run(debug=True)