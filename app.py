from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

# -------------------- IMPORTAR MÓDULOS --------------------
# Autenticación
from INICIAR_SESION.backend.modulos.verificar_usuario import verificar_usuario, obtener_usuario
from INICIAR_SESION.backend.modulos.verificar_contrasena import verificar_contrasena
from INICIAR_SESION.backend.modulos.acceder_sistema import acceder_sistema

# Registro
from Registrarse.backend.modulos.registrar_usuario import registrar_usuario

# Recuperación de contraseña
from Olvidaste_Contrasena.backend.modulos.enviar_codigo import generar_codigo
from Olvidaste_Contrasena.backend.modulos.verificar_codigo import verificar_codigo_usuario
from Olvidaste_Contrasena.backend.modulos.reenviar_codigo import reenviar_codigo_usuario
from Recuperar_Contrasena.backend.modulos.validar_contrasena import verificar_contrasena as validar_nueva_contrasena
from Recuperar_Contrasena.backend.modulos.actualizar_contrasena import actualizar_contrasena

# Cierre de sesión
from CERRAR_SESION.backend.modulos.cerrar_sesion import cerrar_sesion
from CERRAR_SESION.backend.modulos.verificar_token import verificar_token
from CERRAR_SESION.backend.modulos.redirigir_inicio import redirigir_inicio


# -------------------- CONFIGURACIÓN DE FLASK --------------------
app = Flask(__name__, static_folder="../frontend", static_url_path="/")
CORS(app)

# -------------------- VARIABLES SIMULADAS --------------------
tokens_validos = ["token123", "token456", "token789"]


# -------------------- RUTAS GENERALES --------------------
@app.route('/')
def index():
    return send_from_directory(app.static_folder, "index.html")


# -------------------- 1. REGISTRO --------------------
@app.route('/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    resultado = registrar_usuario(
        data.get("nombre"),
        data.get("apellido"),
        data.get("email"),
        data.get("contrasena"),
        data.get("confirmar")
    )
    return jsonify(resultado)


# -------------------- 2. INICIO DE SESIÓN --------------------
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not verificar_usuario(email):
        return jsonify({"success": False, "message": "Usuario no encontrado"}), 400

    usuario = obtener_usuario(email)

    if not usuario["habilitado"]:
        return jsonify({"success": False, "message": "Usuario no autorizado"}), 403

    if not verificar_contrasena(password):
        return jsonify({"success": False, "message": "Contraseña no cumple con los requisitos"}), 401

    if password != usuario["password"]:
        return jsonify({"success": False, "message": "Contraseña incorrecta"}), 401

    token = acceder_sistema(email)
    return jsonify({
        "success": True,
        "message": "Acceso concedido",
        "token": token,
        "rol": usuario["rol"]
    })


# -------------------- 3. OLVIDASTE CONTRASEÑA --------------------
@app.route('/enviar-codigo', methods=['POST'])
def enviar_codigo_route():
    data = request.get_json()
    email = data.get('email')

    codigo, mensaje = generar_codigo(email)
    if not codigo:
        return jsonify({"mensaje": mensaje}), 400
    return jsonify({"mensaje": mensaje}), 200


@app.route('/verificar-codigo', methods=['POST'])
def verificar_codigo_route():
    data = request.get_json()
    codigo = data.get('codigo')
    respuesta, estado = verificar_codigo_usuario(codigo)
    return jsonify(respuesta), estado


@app.route('/reenviar-codigo', methods=['POST'])
def reenviar_codigo_route():
    data = request.get_json()
    email = data.get('email')
    respuesta, estado = reenviar_codigo_usuario(email)
    return jsonify(respuesta), estado


# -------------------- 4. RECUPERAR CONTRASEÑA --------------------
@app.route('/actualizar_contrasena', methods=['POST'])
def actualizar_contrasena_route():
    data = request.get_json()
    correo = data.get('correo')
    nueva = data.get('nueva_contrasena')
    confirmar = data.get('confirmar_contrasena')

    if not correo or not nueva or not confirmar:
        return jsonify({"error": "Todos los campos son requeridos"}), 400
    if nueva != confirmar:
        return jsonify({"error": "Las contraseñas no coinciden"}), 400

    if not validar_nueva_contrasena(nueva):
        return jsonify({"error": "La contraseña no cumple con los requisitos de seguridad"}), 400

    actualizar_contrasena(correo, nueva)
    return jsonify({"mensaje": "Contraseña actualizada correctamente."}), 200


# -------------------- 5. CERRAR SESIÓN --------------------
@app.route('/cerrar_sesion', methods=['POST'])
def cerrar_sesion_usuario():
    data = request.get_json()
    if not data or "token" not in data:
        return jsonify({"error": "Falta el token en la solicitud"}), 400

    token = data["token"]
    if verificar_token(token, tokens_validos):
        resultado = cerrar_sesion(token)
        redireccion = redirigir_inicio()
        return jsonify({
            "mensaje": resultado["mensaje"],
            "redirigir_a": redireccion
        })
    else:
        return jsonify({"error": "Token inválido"}), 401


# -------------------- EJECUTAR SERVIDOR --------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"✅ Servidor Flask ejecutándose en http://127.0.0.1:{port}")
    app.run(debug=True, port=port)
