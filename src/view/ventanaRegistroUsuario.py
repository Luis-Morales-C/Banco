import re
import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QPushButton, QVBoxLayout, QLineEdit, QFormLayout, QMessageBox
)
from PyQt5.QtGui import QFont, QColor, QCursor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from src.model.usuario import Usuario
from src.view.ventanaRegistroCliente import VentanaRegistroCliente
from src.view.ventanaError import VentanaError


class VentanaRegistroUsuario(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cliente_window = None
        self.setWindowTitle("Registro de Usuario")
        self.setFixedSize(500, 550)
        self.init_ui()



    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(25)

        titulo = QLabel("Crear Usuario")
        titulo.setFont(QFont("Segoe UI", 26, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color: #573b8a;")
        layout.addWidget(titulo)

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

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre de usuario")
        self.nombre_input.setStyleSheet(estilo_input)

        self.correo_input = QLineEdit()
        self.correo_input.setPlaceholderText("Correo electrónico")
        self.correo_input.setStyleSheet(estilo_input)

        self.contrasena_input = QLineEdit()
        self.contrasena_input.setPlaceholderText("Contraseña")
        self.contrasena_input.setEchoMode(QLineEdit.Password)
        self.contrasena_input.setStyleSheet(estilo_input)

        self.confirmar_contrasena_input = QLineEdit()
        self.confirmar_contrasena_input.setPlaceholderText("Confirmar contraseña")
        self.confirmar_contrasena_input.setEchoMode(QLineEdit.Password)
        self.confirmar_contrasena_input.setStyleSheet(estilo_input)

        form_layout.addRow("Nombre:", self.nombre_input)
        form_layout.addRow("Correo:", self.correo_input)
        form_layout.addRow("Contraseña:", self.contrasena_input)
        form_layout.addRow("Confirmar contraseña:", self.confirmar_contrasena_input)

        layout.addLayout(form_layout)

        boton_registrar = QPushButton("Crear usuario")
        boton_registrar.setCursor(QCursor(Qt.PointingHandCursor))
        boton_registrar.setStyleSheet("""
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
        boton_registrar.clicked.connect(self.registrar_usuario)

        sombra_boton = QGraphicsDropShadowEffect()
        sombra_boton.setBlurRadius(15)
        sombra_boton.setXOffset(0)
        sombra_boton.setYOffset(5)
        sombra_boton.setColor(QColor(0, 0, 0, 120))
        boton_registrar.setGraphicsEffect(sombra_boton)

        layout.addWidget(boton_registrar)

        central_widget.setStyleSheet("""
            QWidget {
                background-color: #f4f0fa;
                border-radius: 12px;
            }
        """)
        central_widget.setLayout(layout)

    def registrar_usuario(self):
        nombre = self.nombre_input.text().strip()
        correo = self.correo_input.text().strip()
        contrasena = self.contrasena_input.text()
        confirmar_contrasena = self.confirmar_contrasena_input.text()

        if not (nombre and correo and contrasena and confirmar_contrasena):
            VentanaError.mostrar_error(self, "Por favor, complete todos los campos.")
            return

        if len(contrasena) < 8 or len(contrasena) > 35:
            VentanaError.mostrar_error(self, "La contraseña debe tener entre 8 y 35 caracteres.")
            return

        if contrasena != confirmar_contrasena:
            VentanaError.mostrar_error(self, "Las contraseñas no coinciden.")
            return

        patron_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(patron_email, correo):
            VentanaError.mostrar_error(self, "El correo electrónico no es válido.")
            return

        id_usuario = Usuario.registrar(nombre, correo, contrasena)
        if id_usuario:
            QMessageBox.information(self, "Éxito", f"Usuario creado con éxito, ID: {id_usuario}")
            self.abrir_ventana_cliente(correo)
        else:
            VentanaError.mostrar_error(self, "Error al registrar usuario (correo ya registrado).")

    def abrir_ventana_cliente(self, correo_usuario):
        self.cliente_window = VentanaRegistroCliente(correo_usuario)
        self.cliente_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaRegistroUsuario()
    ventana.show()
    sys.exit(app.exec_())
