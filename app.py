from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# IMPORTS: asegúrate de que los módulos estén en backend_python/modulos/
# y que los archivos se llamen exactamente 'validar_contrasena.py' y 'actualizar_contrasena.py'
from modulos.validar_contrasena import verificar_contrasena
from modulos.actualizar_contrasena import actualizar_contrasena

app = Flask(__name__)
CORS(app)


@app.route('/actualizar_contrasena', methods=['POST'])
def endpoint_actualizar_contrasena():
    """
    Endpoint que recibe JSON:
    {
      "correo": "usuario@demo.com",
      "nueva_contrasena": "A..a1!",
      "confirmar_contrasena": "A..a1!"
    }
    Valida y actualiza la contraseña en la BD.
    """
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "JSON inválido"}), 400

    correo = data.get('correo')
    nueva = data.get('nueva_contrasena')
    confirmar = data.get('confirmar_contrasena')

    # Validaciones básicas
    if not correo or not nueva or not confirmar:
        return jsonify({"error": "Todos los campos son requeridos"}), 400

    if nueva != confirmar:
        return jsonify({"error": "Las contraseñas no coinciden"}), 400

    # Validar reglas de seguridad usando tu módulo
    try:
        es_valida = verificar_contrasena(nueva)
    except Exception as e:
        return jsonify({"error": f"Error en la validación: {str(e)}"}), 500

    if not es_valida:
        return jsonify({"error": "La contraseña no cumple con los requisitos de seguridad"}), 400

    # Actualizar en la base de datos usando tu módulo
    try:
        exito, mensaje = actualizar_contrasena(correo, nueva)
    except Exception as e:
        return jsonify({"error": f"Error al actualizar contraseña: {str(e)}"}), 500

    if exito:
        return jsonify({"mensaje": mensaje}), 200
    else:
        return jsonify({"error": mensaje}), 400


if __name__ == '__main__':
    # Forzar que la BD exista en el mismo directorio donde corre app.py
    # (esto no crea tablas; asumo que ya tienes script para crear la tabla)
    print(f"Iniciando Flask en PID {os.getpid()}")
    app.run(debug=True, host='127.0.0.1', port=5000)
