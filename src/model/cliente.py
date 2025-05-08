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

    @staticmethod
    def registrar(nombre, documento, correo, telefono, direccion):
        conn = conectar_db()
        if conn:
           cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Cliente (nombre, documento, correo, telefono, direccion)
                VALUES (?, ?, ?, ?, ?)
            """, (nombre, documento, correo, telefono, direccion))
            conn.commit()
            return True
        except Exception as e:
            print("Error al registrar cliente:", e)
            return False
        finally:
            conn.close()
        return False


