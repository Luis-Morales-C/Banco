from ..conexion.conexion import conectar_db

class Cuenta:
    def __init__(self, id_cuenta, num, tipo_cuenta, fecha_apertura, saldo):
        self.id_cuenta = id_cuenta
        self.num = num
        self.tipo_cuenta = tipo_cuenta
        self.fecha_apertura = fecha_apertura
        self.saldo = saldo

    @staticmethod
    def obtener_todas():
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Cuenta")
            cuentas = cursor.fetchall()
            conn.close()
            return cuentas
        return []
