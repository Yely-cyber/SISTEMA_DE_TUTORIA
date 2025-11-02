from flask import Flask, request, jsonify
from flask_cors import CORS
from modulos.verificar_usuario import verificar_usuario, obtener_usuario
from modulos.verificar_contrasena import verificar_contrasena
from modulos.acceder_sistema import acceder_sistema

app = Flask(__name__)
CORS(app)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # 1. Verificar usuario
    if not verificar_usuario(email):
        return jsonify({"success": False, "message": "Usuario no encontrado"}), 400

    usuario = obtener_usuario(email)

    # 2. Validar si está habilitado
    if not usuario["habilitado"]:
        return jsonify({"success": False, "message": "Usuario no autorizado"}), 403

    # 3. Verificar formato de contraseña (reglas)
    if not verificar_contrasena(password):
        return jsonify({"success": False, "message": "Contraseña no cumple con los requisitos"}), 401

    # 4. Comparar contraseña ingresada con la guardada
    if password != usuario["password"]:
        return jsonify({"success": False, "message": "Contraseña incorrecta"}), 401

    # 5. Acceso concedido
    token = acceder_sistema(email)
    return jsonify({
        "success": True,
        "message": "Acceso concedido",
        "token": token,
        "rol": usuario["rol"]
    })

if __name__ == '__main__':
    app.run(debug=True, port=3000)
