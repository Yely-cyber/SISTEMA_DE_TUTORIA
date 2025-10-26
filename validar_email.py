import re

def validar_email(email):
    """
    Valida que el email tenga un formato correcto:
    - Debe tener una parte antes del @
    - Debe tener un @
    - Debe tener un dominio después del @
    - Debe tener una extensión (.com, .pe, etc.)
    """
    
    # Patrón de validación de email más estricto
    patron = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(patron, email):
        return False
    
    # Validaciones adicionales
    if email.count('@') != 1:
        return False
    
    # Verificar que no empiece o termine con punto o guion
    usuario, dominio = email.split('@')
    
    if usuario.startswith('.') or usuario.endswith('.'):
        return False
    
    if dominio.startswith('.') or dominio.endswith('.'):
        return False
    
    # Verificar que el dominio tenga al menos un punto
    if '.' not in dominio:
        return False
    
    return True