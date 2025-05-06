from ..conexion.conexion import conectar_db

class Transaccion:
    def __init__(self, id_transaccion, monto, cuenta_destino, tipo, fecha, descripcion):
        self.id_transaccion = id_transaccion
        self.monto = monto
        self.cuenta_destino = cuenta_destino
        self.tipo = tipo
        self.fecha = fecha
        self.descripcion = descripcion

    @staticmethod
    def obtener_todas():
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Transaccion")
            transacciones = cursor.fetchall()
            conn.close()
            return transacciones
        return []
