# transaccion.py
import string
import random
from src.conexion.conexion import conectar_db
from src.model.cuenta import Cuenta

def generar_codigo_retiro(longitud=8):
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choices(caracteres, k=longitud))

class Transaccion:
    @staticmethod
    def crear_transaccion(tipo_transaccion, id_cuenta, monto, **kwargs):
        conn = None
        try:
            conn = conectar_db()
            cursor = conn.cursor()

            # Todos los tipos inician como exitosos excepto retiros
            estado = 'Exitosa' if tipo_transaccion in ['Deposito', 'Transferencia'] else 'Pendiente'

            # Validar saldo para Transferencia/Retiro
            if tipo_transaccion in ['Transferencia', 'Retiro']:
                cursor.execute("SELECT saldo FROM Cuenta WHERE id_cuenta = ?", (id_cuenta,))
                saldo_actual = cursor.fetchone()[0]
                if saldo_actual < monto:
                    raise ValueError("Saldo insuficiente")

            # Insertar transacción
            cursor.execute("""
                INSERT INTO Transaccion (tipo_transaccion, id_cuenta, monto, fecha_transaccion, estado)
                OUTPUT INSERTED.id_transaccion
                VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?)
            """, (tipo_transaccion, id_cuenta, monto, estado))

            id_transaccion = cursor.fetchone()[0]

            # Lógica para Transferencia
            if tipo_transaccion == 'Transferencia':
                num_destino = kwargs.get('cuentaDestino')
                if not num_destino:
                    raise ValueError("Cuenta destino requerida")

                id_destino = Cuenta.obtener_id_por_numero(num_destino)
                if not id_destino:
                    raise ValueError("Cuenta destino no existe")

                # Restar de origen y sumar a destino
                cursor.execute("UPDATE Cuenta SET saldo = saldo - ? WHERE id_cuenta = ?", (monto, id_cuenta))
                cursor.execute("UPDATE Cuenta SET saldo = saldo + ? WHERE id_cuenta = ?", (monto, id_destino))
                cursor.execute("INSERT INTO Transferencia (id_transaccion, cuenta_destino) VALUES (?, ?)",
                               (id_transaccion, id_destino))

            # Lógica para Depósito
            elif tipo_transaccion == 'Deposito':
                cursor.execute("UPDATE Cuenta SET saldo = saldo + ? WHERE id_cuenta = ?", (monto, id_cuenta))

            # Lógica para Retiro
            elif tipo_transaccion == 'Retiro':
                codigo = generar_codigo_retiro()
                cursor.execute("INSERT INTO Retiro (id_transaccion, codigo_seguridad) VALUES (?, ?)",
                               (id_transaccion, codigo))

            conn.commit()
            return True

        except Exception as e:
            if conn: conn.rollback()
            raise e
        finally:
            if conn: conn.close()

    @staticmethod
    def obtener_por_cliente(id_cliente):
        conn = None
        try:
            conn = conectar_db()
            if not conn:
                raise ConnectionError("No se pudo conectar a la base de datos")

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
                    resultado = cursor_destino.fetchone()
                    if resultado:
                        cuenta_destino_str = resultado[0]

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
        finally:
            if conn:
                conn.close()

    @staticmethod
    def validar_retiro(codigo_seguridad):
        conn = None
        try:
            conn = conectar_db()
            if not conn:
                raise ConnectionError("No se pudo conectar a la base de datos")

            cursor = conn.cursor()
            cursor.execute("""
                SELECT t.id_transaccion, t.monto, t.id_cuenta, t.estado
                FROM Transaccion t
                INNER JOIN Retiro r ON t.id_transaccion = r.id_transaccion
                WHERE r.codigo_seguridad = ?
                AND t.tipo_transaccion = 'Retiro'
                AND t.estado = 'Pendiente'
            """, (codigo_seguridad,))

            resultado = cursor.fetchone()
            if not resultado:
                raise ValueError("Código de retiro inválido o ya utilizado")

            return {
                'id_transaccion': resultado[0],
                'monto': resultado[1],
                'id_cuenta': resultado[2],
                'estado': resultado[3]
            }

        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

    @staticmethod
    def confirmar_retiro(codigo_seguridad):
        conn = None
        try:
            conn = conectar_db()
            if not conn:
                raise ConnectionError("No se pudo conectar a la base de datos")

            # Desactivar autocommit para manejar transacciones manualmente
            # En pyodbc se hace con: conn.autocommit = False
            conn.autocommit = False
            cursor = conn.cursor()

            retiro = Transaccion.validar_retiro(codigo_seguridad)

            # Descontar saldo usando método de Cuenta, pasando el cursor para que participe en la transacción
            Cuenta.descontar_saldo(retiro['id_cuenta'], retiro['monto'], cursor)

            cursor.execute("""
                UPDATE Transaccion
                SET estado = 'Exitosa'
                WHERE id_transaccion = ?
            """, (retiro['id_transaccion'],))

            conn.commit()
            return True

        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()