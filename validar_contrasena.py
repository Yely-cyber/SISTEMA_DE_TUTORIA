import re

def verificar_contrasena(contrasena: str) -> bool:
    """
    Verifica si la contraseña cumple con los requisitos de seguridad.
    Retorna True si cumple todas las condiciones, False si no.
    """

    if len(contrasena) < 12:
        return False
    if not re.search(r"[A-Z]", contrasena):
        return False
    if not re.search(r"[a-z]", contrasena):
        return False
    if not re.search(r"[0-9]", contrasena):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", contrasena):
        return False
    return True
