import secrets

def acceder_sistema(email):
    token = secrets.token_hex(16)
    print(f"Usuario {email} accedió al sistema. Token: {token}")
    return token
