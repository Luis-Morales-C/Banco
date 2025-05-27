from ..conexion.conexion import conectar_db
from datetime import datetime

class Usuario:
    def __init__(self, id_usuario, nombre, correo, contrasena, fecha_registro, estado, id_rol):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.fecha_registro = fecha_registro
        self.estado = estado
        self.id_rol = id_rol

    @staticmethod
    def registrar(nombre, correo, contrasena, estado="activo", id_rol=3):
        
        conn = conectar_db()
        if conn:
            try:
                cursor = conn.cursor()
                fecha_registro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute("""
                    INSERT INTO Usuario (nombre, correo, contrasena, fecha_registro, estado, id_rol)
                    OUTPUT INSERTED.id_usuario
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (nombre, correo, contrasena, fecha_registro, estado, id_rol))
                id_insertado = cursor.fetchone()[0]
                conn.commit()
                conn.close()
                return id_insertado
            except Exception as e:
                print("Error al registrar usuario:", e)
                conn.close()
        return None
