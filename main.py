from flask import Flask, jsonify, request, render_template

import conexion_BD

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/paciente')
def paciente():
    return render_template('paciente.html')

# Rutas adicionales para otras secciones
@app.route('/doctor')
def doctor():
    return render_template('doctor.html')

@app.route('/administrativo')
def administrativo():
    return render_template('administrativo.html')

@app.route('/buscar-especialista')
def buscar_especialista():
    # Lógica para buscar especialista
    return render_template('buscar_especialista.html')

@app.route('/consultar-especialistas')
def consultar_especialistas():
    # Lógica para consultar especialistas disponibles
    return render_template('consultar_especialistas.html')

@app.route("/user/<name>")
def user_account(name):
    user = {'Nombre': name, 'Edad': 20, 'Rut': '22.066.527-5'}
    query = request.args.get('query')
    if query:
        user['query'] = query

    return jsonify(user), 200

#codigo para buscar horarios, especialidades y especialistas. También precios.

@app.route('/obtener_especialidades')
def obtener_especialidades_ruta():
    try:
        especialidades = conexion_BD.obtener_especialidades()  # Llama a la función desde conexion_BD
        return jsonify(especialidades)
    except Exception as ex:
        print(ex)
        return jsonify({'error': 'Error al obtener las especialidades'}), 500

@app.route('/obtener_doctores')
def obtener_doctores_ruta():
    try:
        doctores = conexion_BD.obtener_doctores()  # Llama a la función desde conexion_BD
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
        horarios = conexion_BD.obtener_horarios(especialidad, dia, hora, doctor)  # Llama a la función desde conexion_BD

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
        costo = conexion_BD.obtener_costo_atencion(rut_especialista)  # Llama a la función en conexion_BD.py
        return jsonify(costo)

    except Exception as ex:
        print(ex)
        return jsonify({'error': 'Error al obtener el costo de atención'}), 500

if __name__ == "__main__":
    app.run(debug=True)