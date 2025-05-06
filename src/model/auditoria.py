from ..conexion.conexion import conectar_db

class Auditoria:
    def __init__(self, id_auditoria, fecha_hora, accion, descripcion):
        self.id_auditoria = id_auditoria
        self.fecha_hora = fecha_hora
        self.accion = accion
        self.descripcion = descripcion

    @staticmethod
    def registrar(fecha_hora, accion, descripcion):
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Auditoria (fechaHora, accion, descripcion) VALUES (?, ?, ?)",
                           (fecha_hora, accion, descripcion))
            conn.commit()
            conn.close()
