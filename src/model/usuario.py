from ..conexion.conexion import conectar_db

class Usuario:
    def __init__(self, id_usuario, nombre, correo, contrasena, fecha_registro):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.fecha_registro = fecha_registro

    @staticmethod
    def obtener_todos():
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Usuario")
            usuarios = cursor.fetchall()
            conn.close()
            return usuarios
        return []
