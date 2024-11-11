from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Bienvenido al Hall"

@app.route("/user/<name>")
def user_account(name):
    user = {'Nombre': name, 'Edad': 20, 'Rut': '22.066.527-5'}
    query = request.args.get('query')
    if query:
        user['query'] = query

    return jsonify(user), 200

if __name__ == "__main__":
    app.run(debug=True)