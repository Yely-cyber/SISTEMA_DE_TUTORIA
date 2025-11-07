import sqlite3

def actualizar_contrasena(correo: str, nueva_contrasena: str):
    """
    Actualiza la contraseña de un usuario en la base de datos SQLite.
    Retorna (True, mensaje) si la actualización fue exitosa,
    o (False, mensaje_de_error) si algo falla.
    """

    try:
        conexion = sqlite3.connect("usuarios.db")
        cursor = conexion.cursor()

        # Verificar si el usuario existe
        cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
        usuario = cursor.fetchone()
        if not usuario:
            conexion.close()
            return False, "Usuario no encontrado."

        # Actualizar contraseña
        cursor.execute("UPDATE usuarios SET contrasena = ? WHERE correo = ?", 
                       (nueva_contrasena, correo))
        conexion.commit()
        conexion.close()

        return True, "Contraseña actualizada correctamente."

    except Exception as e:
        return False, f"Error al actualizar la contraseña: {str(e)}"
