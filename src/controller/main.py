from src.view.ventanaInicio import VentanaInicio
from src.view.ventanaRegistro import VentanaRegistro

class Controlador:
    def __init__(self):
        self.ventana_inicio = VentanaInicio(self.mostrar_registro)
        self.ventana_registro = VentanaRegistro()

    def mostrar_inicio(self):
        self.ventana_registro.hide()
        self.ventana_inicio.show()

    def mostrar_registro(self):
        self.ventana_inicio.hide()
        self.ventana_registro.show()
