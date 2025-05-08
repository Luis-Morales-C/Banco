from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QPushButton, QVBoxLayout, QLineEdit, QFormLayout
)
from PyQt5.QtGui import QFont, QColor, QCursor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from src.model.cliente import Cliente
import sys

class VentanaRegistro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro - Banco")
        self.setFixedSize(600, 600)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(25)

        # Título
        titulo = QLabel("Register")
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

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre completo")
        self.nombre_input.setStyleSheet(estilo_input)

        self.correo_input = QLineEdit()
        self.correo_input.setPlaceholderText("Correo electrónico")
        self.correo_input.setStyleSheet(estilo_input)

        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("Teléfono")
        self.telefono_input.setStyleSheet(estilo_input)

        self.direccion_input = QLineEdit()
        self.direccion_input.setPlaceholderText("Dirección")
        self.direccion_input.setStyleSheet(estilo_input)

        form_layout.addRow(self.documento_input)
        form_layout.addRow(self.nombre_input)
        form_layout.addRow(self.correo_input)
        form_layout.addRow(self.telefono_input)
        form_layout.addRow(self.direccion_input)

        layout.addLayout(form_layout)

        # Botón Registrar
        boton_registrar = QPushButton("Registrar")
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
        boton_registrar.clicked.connect(self.registrar_cliente)

        # Sombra al botón
        sombra_boton = QGraphicsDropShadowEffect()
        sombra_boton.setBlurRadius(15)
        sombra_boton.setXOffset(0)
        sombra_boton.setYOffset(5)
        sombra_boton.setColor(QColor(0, 0, 0, 120))
        boton_registrar.setGraphicsEffect(sombra_boton)

        layout.addWidget(boton_registrar)

        # Fondo general claro
        central_widget.setStyleSheet("""
            QWidget {
                background-color: #f4f0fa;
                border-radius: 12px;
            }
        """)

        central_widget.setLayout(layout)

    def registrar_cliente(self):
     documento = self.documento_input.text()
     nombre = self.nombre_input.text()
     correo = self.correo_input.text()
     telefono = self.telefono_input.text()
     direccion = self.direccion_input.text()

     if documento and nombre and correo and telefono and direccion:
           exito = Cliente.registrar(nombre,documento, correo, telefono, direccion)
           if exito:
            print("Cliente registrado con éxito.")
            self.documento_input.clear()
            self.nombre_input.clear()
            self.correo_input.clear()
            self.telefono_input.clear()
            self.direccion_input.clear()


           else:
            print("Error al registrar el cliente.")
     else:
        print("Por favor, complete todos los campos.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaRegistro()
    ventana.show()
    sys.exit(app.exec_())
