from PyQt5.QtWidgets import QMessageBox

from ..conexion.conexion import conectar_db
from ..view.ventanaError import VentanaError


class Cliente:

    @staticmethod
    def registrar(nombre, documento, correo, telefono, direccion):
        conn = conectar_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id_usuario FROM Usuario WHERE correo = ?", (correo,))
                resultado = cursor.fetchone()
                if not resultado:
                    print("El correo no está asociado a ningún usuario")
                    return None
                id_usuario = resultado[0]

                estado = 'activo'

                cursor.execute("""
                    INSERT INTO Cliente (nombre, documento, correo, telefono, direccion,estado, id_usuario)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (nombre, documento, correo, telefono, direccion, estado, id_usuario))
                conn.commit()


                cursor.execute("SELECT id_cliente FROM Cliente WHERE documento = ?", (documento,))
                id_cliente = cursor.fetchone()[0]
                return id_cliente
            except Exception as e:
                print("Error al registrar cliente:", e)
            finally:
                conn.close()
        return None

    @staticmethod
    def verificar_credenciales(documento, contrasena):
        conn = conectar_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT c.id_cliente, u.contrasena
                    FROM Cliente c
                    JOIN Usuario u ON c.id_usuario = u.id_usuario
                    WHERE c.documento = ?
                """, (documento,))
                resultado = cursor.fetchone()
                if resultado:
                    id_cliente = resultado[0]
                    contrasena_guardada = resultado[1]
                    if contrasena_guardada == contrasena:
                        return id_cliente
                return None
            except Exception as e:
                print("Error al verificar credenciales:", e)
            finally:
                conn.close()
        return None

    @staticmethod
    def existe_por_documento(documento):
      conn = conectar_db()
      if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Cliente WHERE documento = ?", (documento,))
            resultado = cursor.fetchone()
            return resultado[0] > 0
        except Exception as e:
            print(f"Error al verificar cliente por documento: {e}")
            return False
        finally:
            conn.close()
      return False




