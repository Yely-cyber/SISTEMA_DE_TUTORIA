# modulos/verificar_usuario.py

usuarios = {
    "admin@unsaac.edu.pe": {
        "password": "Admin1234@unsaac",
        "habilitado": True,
        "rol": "Administrador"
    },
    "usuario@unsaac.edu.pe": {
        "password": "Usuario2025@unsaac",
        "habilitado": True,
        "rol": "Estudiante"
    },
    "bloqueado@unsaac.edu.pe": {
        "password": "Bloqueado@2025!",
        "habilitado": False,
        "rol": "Tutor"
    }
}

def verificar_usuario(email):
    """Verifica si el correo existe."""
    return email in usuarios

def obtener_usuario(email):
    """Devuelve los datos completos del usuario."""
    return usuarios.get(email)
