import re

def validar_contrasena(contrasena):
    """
    Valida que la contraseña cumpla con los requisitos de seguridad:
    - Al menos 12 caracteres
    - Al menos una mayúscula
    - Al menos una minúscula
    - Al menos un número
    - Al menos un carácter especial
    """
    
    # Validar longitud mínima
    if len(contrasena) < 12:
        return False, "La contraseña debe tener al menos 12 caracteres."
    
    # Validar que tenga al menos una mayúscula
    if not re.search(r'[A-Z]', contrasena):
        return False, "La contraseña debe contener al menos una letra mayúscula."
    
    # Validar que tenga al menos una minúscula
    if not re.search(r'[a-z]', contrasena):
        return False, "La contraseña debe contener al menos una letra minúscula."
    
    # Validar que tenga al menos un número
    if not re.search(r'[0-9]', contrasena):
        return False, "La contraseña debe contener al menos un número."
    
    # Validar que tenga al menos un carácter especial
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/;~`]', contrasena):
        return False, "La contraseña debe contener al menos un carácter especial (!@#$%^&*...)."
    
    # Si pasa todas las validaciones
    return True, ""