from ..conexion.conexion import conectar_db

class Rol:
    def __init__(self, id_rol, nombre, descripcion):
        self.id_rol = id_rol
        self.nombre = nombre
        self.descripcion = descripcion

    @staticmethod
    def obtener_todos():
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Rol")
            roles = cursor.fetchall()
            conn.close()
            return roles
        return []
