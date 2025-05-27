from ..conexion.conexion import conectar_db

class Cuenta:
    def __init__(self, id_cuenta, num, tipo_cuenta, estado, fecha_apertura, saldo):
        self.id_cuenta = id_cuenta
        self.num = num
        self.tipo_cuenta = tipo_cuenta
        self.estado = estado
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
    def crear(num_cuenta, tipo_cuenta, monto, id_cliente, estado='Activa'):
        try:
            conn = conectar_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Cuenta (num_cuenta, tipo_cuenta, estado, fecha_apertura, saldo, id_cliente)
                    VALUES (?, ?, ?, GETDATE(), ?, ?)
                """, (num_cuenta, tipo_cuenta, estado, monto, id_cliente))
                conn.commit()
                conn.close()
                return True
        except Exception as e:
            print("Error al crear cuenta:", e)
        return False

    @staticmethod
    def obtener_por_cliente(id_cliente):
        try:
            conn = conectar_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id_cuenta, num_cuenta, tipo_cuenta, estado, fecha_apertura, saldo 
                    FROM Cuenta WHERE id_cliente = ?
                """, (id_cliente,))
                cuentas = cursor.fetchall()
                conn.close()
                return cuentas
        except Exception as e:
            print("Error al obtener cuentas por cliente:", e)
        return []

    @staticmethod
    def validar_cuenta(num_cuenta):
        try:
            conn = conectar_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM Cuenta WHERE num_cuenta = ?", (num_cuenta,))
                existe = cursor.fetchone()[0]
                conn.close()
                return existe > 0
        except Exception as e:
            print("Error al validar cuenta:", e)
        return False

    @staticmethod
    def obtener_id_por_numero(num_cuenta):
        try:
            conn = conectar_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id_cuenta FROM Cuenta WHERE num_cuenta = ?", (num_cuenta,))
                resultado = cursor.fetchone()
                conn.close()
                if resultado:
                    return resultado[0]
                else:
                    return None
        except Exception as e:
            print(f"Error al obtener id de cuenta por número: {e}")
            return None