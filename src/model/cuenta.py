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

    @staticmethod
    def crear(num_cuenta, tipo_cuenta, monto, documento_cliente):
      try:
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Cuenta (numCuenta, tipoCuenta, fechaApertura, saldo, documentoCliente)
                VALUES (?, ?, GETDATE(), ?, ?)
            """, (num_cuenta, tipo_cuenta, monto, documento_cliente))
            conn.commit()
            conn.close()
            return True
      except Exception as e:
        print("Error al crear cuenta:", e)
        return False


