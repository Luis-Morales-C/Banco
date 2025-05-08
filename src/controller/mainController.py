from src.view.ventanaInicio import VentanaInicio
from src.view.ventanaLogin import VentanaLogin
from src.view.ventanaRegistro import VentanaRegistro

class Controlador:
    def __init__(self):
        self.ventana_inicio = VentanaInicio(self.mostrar_registro, self.mostrar_login)
        self.ventana_registro = VentanaRegistro()
        self.ventana_login=VentanaLogin()

    def mostrar_inicio(self):
        self.ventana_registro.hide()
        self.ventana_inicio.show()

    def mostrar_registro(self):
        self.ventana_inicio.hide()
        self.ventana_registro.show()

    def mostrar_login(self):
        self.ventana_inicio.hide()
        self.ventana_login.show()