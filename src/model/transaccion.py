# transaccion.py
from datetime import datetime
import string
import random
from src.conexion.conexion import conectar_db

def generar_codigo_retiro(longitud=8):
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choices(caracteres, k=longitud))

class Transaccion:
    def __init__(self, id_transaccion, monto, id_cuenta, tipo_transaccion, fecha, descripcion, estado):
        self.id_transaccion = id_transaccion
        self.monto = monto
        self.id_cuenta = id_cuenta
        self.tipo_transaccion = tipo_transaccion
        self.fecha = fecha
        self.descripcion = descripcion
        self.estado = estado

    @staticmethod
    def crear_transaccion(monto, id_cuenta, tipo_transaccion, descripcion, **kwargs):
        conn = None
        try:
            conn = conectar_db()
            if conn:
                conn.autocommit = False
                cursor = conn.cursor()
                fecha = datetime.now()

                # Validar saldo para Transferencias y Retiros
                if tipo_transaccion in ['Transferencia', 'Retiro']:
                    cursor.execute("SELECT saldo FROM Cuenta WHERE id_cuenta = ?", (id_cuenta,))
                    saldo_actual = cursor.fetchone()[0]
                    if saldo_actual < monto:
                        raise Exception("Saldo insuficiente para realizar la transacción")

                # Determinar estado inicial
                estado = 'Pendiente' if tipo_transaccion == 'Retiro' else 'Exitosa'

                # Insertar transacción
                cursor.execute("""
                    INSERT INTO Transaccion (monto, id_cuenta, tipo_transaccion, fecha_transaccion, descripcion, estado)
                    OUTPUT INSERTED.id_transaccion
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (monto, id_cuenta, tipo_transaccion, fecha, descripcion, estado))

                id_transaccion = cursor.fetchone()[0]

                # Procesar según tipo de transacción
                if tipo_transaccion == 'Deposito':
                    cursor.execute("""
                        UPDATE Cuenta 
                        SET saldo = saldo + ?
                        WHERE id_cuenta = ?
                    """, (monto, id_cuenta))
                    cursor.execute("INSERT INTO Deposito (id_transaccion) VALUES (?)", (id_transaccion,))

                elif tipo_transaccion == 'Transferencia':
                    cuenta_destino = kwargs.get('cuentaDestino')
                    cursor.execute("SELECT id_cuenta FROM Cuenta WHERE num_cuenta = ?", (cuenta_destino,))
                    resultado = cursor.fetchone()
                    if not resultado:
                        raise Exception(f"La cuenta destino '{cuenta_destino}' no existe")
                    id_cuenta_destino = resultado[0]

                    # Actualizar saldos
                    cursor.execute("""
                        UPDATE Cuenta 
                        SET saldo = saldo - ?
                        WHERE id_cuenta = ?
                    """, (monto, id_cuenta))

                    cursor.execute("""
                        UPDATE Cuenta 
                        SET saldo = saldo + ?
                        WHERE id_cuenta = ?
                    """, (monto, id_cuenta_destino))

                    cursor.execute("INSERT INTO Transferencia (id_transaccion, cuenta_destino) VALUES (?, ?)",
                                   (id_transaccion, id_cuenta_destino))

                elif tipo_transaccion == 'Retiro':
                    codigo = kwargs.get('codigoRetiro')
                    cursor.execute("INSERT INTO Retiro (id_transaccion, codigo_seguridad) VALUES (?, ?)",
                                   (id_transaccion, codigo))

                conn.commit()
                return True

        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    @staticmethod
    def obtener_por_cliente(id_cliente):
        try:
            conn = conectar_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT t.id_transaccion, t.tipo_transaccion, c.num_cuenta, t.monto, 
                           t.fecha_transaccion, t.estado, tr.cuenta_destino
                    FROM Transaccion t
                    INNER JOIN Cuenta c ON t.id_cuenta = c.id_cuenta
                    LEFT JOIN Transferencia tr ON t.id_transaccion = tr.id_transaccion
                    WHERE c.id_cliente = ?
                    ORDER BY t.fecha_transaccion DESC
                """, (id_cliente,))

                transacciones = []
                for fila in cursor.fetchall():
                    cuenta_destino_str = ""
                    if fila[1] == 'Transferencia' and fila[6]:
                        cursor_destino = conn.cursor()
                        cursor_destino.execute("SELECT num_cuenta FROM Cuenta WHERE id_cuenta = ?", (fila[6],))
                        num_cuenta_destino = cursor_destino.fetchone()[0]
                        cuenta_destino_str = f"{num_cuenta_destino} (ID: {fila[6]})"

                    transacciones.append({
                        'id': fila[0],
                        'tipo': fila[1],
                        'cuenta_origen': fila[2],
                        'cuenta_destino': cuenta_destino_str,
                        'monto': fila[3],
                        'fecha': fila[4],
                        'estado': fila[5]
                    })
                return transacciones
        except Exception as e:
            print("Error al obtener transacciones:", e)
            return []