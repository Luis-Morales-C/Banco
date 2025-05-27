import string
import random

from ..conexion.conexion import conectar_db
from datetime import datetime


def generar_codigo_retiro(longitud=8):
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choices(caracteres, k=longitud))


class Transaccion:
    def __init__(self, id_transaccion, monto, cuenta_origen, tipo, fecha, descripcion, estado, cliente_id):
        self.id_transaccion = id_transaccion
        self.monto = monto
        self.cuenta_origen = cuenta_origen
        self.tipo = tipo
        self.fecha = fecha
        self.descripcion = descripcion
        self.estado = estado
        self.cliente_id = cliente_id


    @staticmethod
    def crear_transaccion(monto, cuenta_origen, tipo, descripcion, cliente_id, **kwargs):
        try:
            conn = conectar_db()
            if conn:
                cursor = conn.cursor()
                fecha = datetime.now()
                # Insertar en Transaccion
                cursor.execute("""
                    INSERT INTO Transaccion (monto, cuenta_origen, tipoTransaccion, fechaTransaccion, descripcion, estado, cliente_id)
                    VALUES (?, ?, ?, ?, ?, 'Pendiente', ?)
                """, (monto, cuenta_origen, tipo, fecha, descripcion, cliente_id))
                conn.commit()
                # Obtener idTransaccion insertado
                cursor.execute("SELECT @@IDENTITY")
                id_transaccion = cursor.fetchone()[0]

                # Insertar en tablas hijas según tipo
                if tipo == 'Deposito':
                    nombre = kwargs.get('nombre', '')
                    cursor.execute("INSERT INTO Deposito (idTransaccion, nombre) VALUES (?, ?)", (id_transaccion, nombre))
                elif tipo == 'Retiro':
                    nombre = kwargs.get('nombre', '')
                    codigo = generar_codigo_retiro()
                    fecha_exp = kwargs.get('fechaExpiracion', None)
                    cursor.execute("""
                        INSERT INTO Retiro (idTransaccion, nombre, codigoRetiro, codigoRetiroUsado, fechaExpiracion)
                        VALUES (?, ?, ?, 0, ?)
                    """, (id_transaccion, nombre, codigo, fecha_exp))
                elif tipo == 'Transferencia':
                    cuenta_destino = kwargs.get('cuentaDestino', '')
                    nombre = kwargs.get('nombre', '')
                    cursor.execute("""
                        INSERT INTO Transferencia (idTransaccion, cuentaDestino, nombre)
                        VALUES (?, ?, ?)
                    """, (id_transaccion, cuenta_destino, nombre))

                conn.commit()
                conn.close()
                return True
        except Exception as e:
            print("Error al crear transacción:", e)
        return False

    @staticmethod
    def obtener_por_cliente(cliente_id):
        try:
            conn = conectar_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT t.idTransaccion, t.monto, t.cuenta_origen, t.tipoTransaccion, t.fechaTransaccion, t.descripcion, t.estado
                    FROM Transaccion t
                    WHERE t.cliente_id = ?
                    ORDER BY t.fechaTransaccion DESC
                """, (cliente_id,))
                transacciones = cursor.fetchall()
                conn.close()
                return transacciones
        except Exception as e:
            print("Error al obtener transacciones:", e)
        return []

