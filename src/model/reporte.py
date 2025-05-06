from ..conexion.conexion import conectar_db

class Reporte:
    def __init__(self, id_reporte, tipo_reporte, contenido, nombre, fecha_generacion):
        self.id_reporte = id_reporte
        self.tipo_reporte = tipo_reporte
        self.contenido = contenido
        self.nombre = nombre
        self.fecha_generacion = fecha_generacion

    @staticmethod
    def obtener_todos():
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Reporte")
            reportes = cursor.fetchall()
            conn.close()
            return reportes
        return []
