from ..conexion.conexion import conectar_db

class Cliente:
    def __init__(self, id_cliente, nombre, documento, correo, telefono, direccion):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        self.direccion = direccion

    @staticmethod
    def obtener_todos():
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Cliente")
            clientes = cursor.fetchall()
            conn.close()
            return clientes
        return []
