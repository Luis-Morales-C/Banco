import sys
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtGui import QFont, QColor, QCursor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from src.model.cliente import Cliente
from src.view.ventanaError import VentanaError
from src.view.ventanaPortalCliente import PortalBancario



class VentanaRegistroCliente(QWidget):
    def __init__(self, correo_predefinido,portal=None):
        super().__init__()
        self.correo_predefinido = correo_predefinido
        self.portal = portal
        self.setWindowTitle("Registro de Cliente")
        self.setFixedSize(500, 550)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(25)

        titulo = QLabel("Registro de Cliente")
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
        self.nombre_input.setPlaceholderText("Nombre completo")
        self.nombre_input.setStyleSheet(estilo_input)

        self.documento_input = QLineEdit()
        self.documento_input.setPlaceholderText("Documento de identidad")
        self.documento_input.setStyleSheet(estilo_input)

        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("Teléfono")
        self.telefono_input.setStyleSheet(estilo_input)

        self.direccion_input = QLineEdit()
        self.direccion_input.setPlaceholderText("Dirección")
        self.direccion_input.setStyleSheet(estilo_input)

        self.correo_input = QLineEdit()
        self.correo_input.setText(self.correo_predefinido)
        self.correo_input.setReadOnly(True)
        self.correo_input.setStyleSheet(estilo_input)

        form_layout.addRow("Nombre:", self.nombre_input)
        form_layout.addRow("Documento:", self.documento_input)
        form_layout.addRow("Teléfono:", self.telefono_input)
        form_layout.addRow("Dirección:", self.direccion_input)
        form_layout.addRow("Correo (usuario):", self.correo_input)

        layout.addLayout(form_layout)

        boton_registrar = QPushButton("Registrar Cliente")
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

        sombra_boton = QGraphicsDropShadowEffect()
        sombra_boton.setBlurRadius(15)
        sombra_boton.setXOffset(0)
        sombra_boton.setYOffset(5)
        sombra_boton.setColor(QColor(0, 0, 0, 120))
        boton_registrar.setGraphicsEffect(sombra_boton)

        layout.addWidget(boton_registrar)

        self.setStyleSheet("""
            QWidget {
                background-color: #f4f0fa;
                border-radius: 12px;
            }
        """)
        self.setLayout(layout)

    def registrar_cliente(self):
        nombre = self.nombre_input.text().strip()
        documento = self.documento_input.text().strip()
        telefono = self.telefono_input.text().strip()
        direccion = self.direccion_input.text().strip()
        correo = self.correo_input.text().strip()

        if not all([nombre, documento, telefono, direccion]):
            VentanaError.mostrar_error(self, "Por favor, complete todos los campos.")
            return

        exito = Cliente.registrar(nombre, documento, correo, telefono, direccion)
        if exito:
           QMessageBox.information(self, "Éxito", "Cliente registrado correctamente.")
           self.close()

           # Crear y mostrar portal asegurando que la referencia persista
           self.portal = PortalBancario()
           self.portal.show()
        else:
           VentanaError.mostrar_error(self, "Error al registrar cliente. Verifique que el correo exista.")

    def abrir_ventana_portal(self, correo_usuario):
        self.cliente_window = VentanaRegistroCliente(correo_usuario)
        self.cliente_window.show()
        self.close()

# Solo para pruebas
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    portal = PortalBancario()
    ventana = VentanaRegistroCliente("cliente@ejemplo.com",portal=portal)
    ventana.show()
    sys.exit(app.exec_())
