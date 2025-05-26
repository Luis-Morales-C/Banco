from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QPushButton, QVBoxLayout, QLineEdit, QFormLayout
)
from PyQt5.QtGui import QFont, QColor, QCursor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from src.model.cliente import Cliente
from src.view.ventanaPortalCliente import PortalBancario
from src.view.ventanaError import VentanaError


import sys

class VentanaLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Banco")
        self.setFixedSize(650, 650)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(25)

        # Título
        titulo = QLabel("Login")
        titulo.setFont(QFont("Segoe UI", 26, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color: #573b8a;")
        layout.addWidget(titulo)

        # Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        estilo_input = """
            QLineEdit {
                background: #e0dede;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 15px;
                color: #333;
            }
        """

        self.documento_input = QLineEdit()
        self.documento_input.setPlaceholderText("Documento")
        self.documento_input.setStyleSheet(estilo_input)

        self.contrasena_input = QLineEdit()
        self.contrasena_input.setPlaceholderText("Contraseña")
        self.contrasena_input.setEchoMode(QLineEdit.Password)
        self.contrasena_input.setStyleSheet(estilo_input)

        form_layout.addRow(self.documento_input)
        form_layout.addRow(self.contrasena_input)

        layout.addLayout(form_layout)

        # Botón Login
        boton_login = QPushButton("Iniciar sesión")
        boton_login.setCursor(QCursor(Qt.PointingHandCursor))
        boton_login.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: white;
                font-weight: bold;
                font-size: 16px;
                padding: 12px;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)
        boton_login.clicked.connect(self.iniciar_sesion)

        sombra_boton = QGraphicsDropShadowEffect()
        sombra_boton.setBlurRadius(15)
        sombra_boton.setXOffset(0)
        sombra_boton.setYOffset(5)
        sombra_boton.setColor(QColor(0, 0, 0, 120))
        boton_login.setGraphicsEffect(sombra_boton)

        layout.addWidget(boton_login)

        central_widget.setStyleSheet("""
            QWidget {
                background-color: #f4f0fa;
                border-radius: 12px;
            }
        """)

        central_widget.setLayout(layout)

    def iniciar_sesion(self):
        documento = self.documento_input.text().strip()
        contrasena = self.contrasena_input.text().strip()

        if documento and contrasena:
           if Cliente.verificar_credenciales(documento, contrasena):
            self.portal = PortalBancario()
            self.portal.show()
            self.close()
           else:
            VentanaError.mostrar_error(self, "Documento o contraseña incorrectos.")
        else:
          VentanaError.mostrar_error(self, "Por favor, complete todos los campos.")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaLogin()
    ventana.show()
    sys.exit(app.exec_())
