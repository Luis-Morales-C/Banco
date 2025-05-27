from PyQt5.QtWidgets import QTableWidgetItem
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

    @staticmethod
    def obtener_por_documento(documento_cliente):
        try:
            conn = conectar_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT idCuenta, numCuenta, tipoCuenta, fechaApertura, saldo 
                    FROM Cuenta WHERE documentoCliente = ?
                """, (documento_cliente,))
                cuentas = cursor.fetchall()
                conn.close()
                return cuentas
        except Exception as e:
            print("Error al obtener cuentas por documento:", e)
        return []

    @staticmethod
    def validar_cuenta(num_cuenta):
        try:
            conn = conectar_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM Cuenta WHERE numCuenta = ?", (num_cuenta,))
                existe = cursor.fetchone()[0]
                conn.close()
                return existe > 0
        except Exception as e:
            print("Error al validar cuenta:", e)
        return False