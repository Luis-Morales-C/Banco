from ..conexion.conexion import conectar_db

class Cliente:
    @staticmethod
    def registrar(nombre, documento, correo, telefono, direccion):
        conn = conectar_db()
        if conn:
            try:
                cursor = conn.cursor()

                # Buscar el ID del usuario relacionado por el correo
                cursor.execute("SELECT id_usuario FROM Usuario WHERE correo = ?", (correo,))
                resultado = cursor.fetchone()

                if not resultado:
                    print("El correo no está asociado a ningún usuario")
                    return False

                id_usuario = resultado[0]

                # Insertar el cliente
                cursor.execute("""
                    INSERT INTO Cliente (id_usuario, nombre, documento, correo, telefono, direccion)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (id_usuario, nombre, documento, correo, telefono, direccion))

                conn.commit()
                return True
            except Exception as e:
                print("Error al registrar cliente:", e)
            finally:
                conn.close()
        return False


    @staticmethod
    def verificar_credenciales(documento, contrasena):
      conn = conectar_db()
      if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.contrasena
                FROM Cliente c
                JOIN Usuario u ON c.id_usuario = u.id_usuario
                WHERE c.documento = ?
            """, (documento,))
            resultado = cursor.fetchone()
            if resultado:
                contrasena_guardada = resultado[0]
                return contrasena_guardada == contrasena
            else:
                return False
        except Exception as e:
            print("Error al verificar credenciales:", e)
        finally:
            conn.close()
      return False
