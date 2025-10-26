import os
import json
from .validar_contrasena import validar_contrasena
from .validar_email import validar_email

# Ruta del archivo JSON
RUTA_ARCHIVO = os.path.join(os.path.dirname(__file__), "..", "usuarios.json")

def registrar_usuario(nombre, apellido, email, contrasena, confirmar):
    # Validar campos obligatorios
    if not all([nombre, apellido, email, contrasena, confirmar]):
        return {"estado": "error", "mensaje": "Todos los campos son obligatorios."}

    # Validar email
    if not validar_email(email):
        return {"estado": "error", "mensaje": "Email inválido."}

    # Validar contraseña
    ok, msg = validar_contrasena(contrasena)
    if not ok:
        return {"estado": "error", "mensaje": msg}

    # Validar coincidencia
    if contrasena != confirmar:
        return {"estado": "error", "mensaje": "Las contraseñas no coinciden."}

    # Crear archivo si no existe
    if not os.path.exists(RUTA_ARCHIVO):
        with open(RUTA_ARCHIVO, 'w') as f:
            json.dump([], f)

    # Leer usuarios existentes
    with open(RUTA_ARCHIVO, 'r') as f:
        usuarios = json.load(f)

    # Validar duplicado de email
    for u in usuarios:
        if u["email"].lower() == email.lower():
            return {"estado": "error", "mensaje": "El email ya está registrado."}

    # Registrar nuevo usuario
    nuevo_usuario = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "contrasena": contrasena
    }

    usuarios.append(nuevo_usuario)

    # Guardar
    with open(RUTA_ARCHIVO, 'w') as f:
        json.dump(usuarios, f, indent=4)

    return {"estado": "ok", "mensaje": "Usuario registrado exitosamente. Redirigiendo al inicio de sesión..."}
