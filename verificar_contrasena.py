import re

def verificar_contrasena(password):
    """
    Debe tener:
    - Una mayúscula
    - Una minúscula
    - Un número
    - Un carácter especial
    - Longitud mínima de 12 caracteres
    """
    regla = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{12,}$'
    return bool(re.match(regla, password))
