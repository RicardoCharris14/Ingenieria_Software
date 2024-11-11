from flask import Flask, jsonify, request, render_template

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



@app.route("/user/<name>")
def user_account(name):
    user = {'Nombre': name, 'Edad': 20, 'Rut': '22.066.527-5'}
    query = request.args.get('query')
    if query:
        user['query'] = query

    return jsonify(user), 200

if __name__ == "__main__":
    app.run(debug=True)