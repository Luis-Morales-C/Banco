from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QPushButton, QVBoxLayout, QComboBox, QLineEdit, QFormLayout
)
from PyQt5.QtGui import QFont, QColor, QCursor, QDoubleValidator
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from src.model.cuenta import Cuenta
import sys

class VentanaCrearCuenta(QMainWindow):
    def __init__(self, cliente_id=None):
        super().__init__()
        self.cliente_id = cliente_id
        self.setWindowTitle("Crear Cuenta - Banco")
        self.setFixedSize(600, 500)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        titulo = QLabel("Crear Nueva Cuenta")
        titulo.setFont(QFont("Segoe UI", 24, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("color: #573b8a;")
        layout.addWidget(titulo)


        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        estilo_input = """
            QLineEdit, QComboBox {
                background: #e0dede;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 15px;
                color: #333;
            }
        """


        self.tipo_combo = QComboBox()
        self.tipo_combo.setStyleSheet(estilo_input)
        try:
            tipos = Cuenta.obtener_tipos_autoapertura()
            for tipo in tipos:

                self.tipo_combo.addItem(tipo[1], tipo[0])
        except Exception as e:
            print("Error al cargar tipos de cuenta:", e)

        # Depósito inicial
        self.deposito_input = QLineEdit()
        self.deposito_input.setPlaceholderText("Depósito inicial")
        self.deposito_input.setStyleSheet(estilo_input)
        self.deposito_input.setValidator(QDoubleValidator(0.0, 1e9, 2))

        form_layout.addRow("Tipo de Cuenta:", self.tipo_combo)
        form_layout.addRow("Depósito Inicial:", self.deposito_input)

        layout.addLayout(form_layout)


        boton_crear = QPushButton("Crear Cuenta")
        boton_crear.setCursor(QCursor(Qt.PointingHandCursor))
        boton_crear.setStyleSheet("""
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
        boton_crear.clicked.connect(self.crear_cuenta)

        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(15)
        sombra.setXOffset(0)
        sombra.setYOffset(5)
        sombra.setColor(QColor(0, 0, 0, 120))
        boton_crear.setGraphicsEffect(sombra)

        layout.addWidget(boton_crear)

        central_widget.setStyleSheet("""
            QWidget {
                background-color: #f4f0fa;
                border-radius: 12px;
            }
        """)

        central_widget.setLayout(layout)

    def crear_cuenta(self):
        tipo_id = self.tipo_combo.currentData()
        deposito_text = self.deposito_input.text()
        if tipo_id is None or deposito_text == "":
            print("Por favor, complete todos los campos.")
            return
        deposito = float(deposito_text)
        try:
            exito = Cuenta.crear(self.cliente_id, tipo_id, deposito)
            if exito:
                print("Cuenta creada con éxito.")
                self.deposito_input.clear()
            else:
                print("Error al crear la cuenta.")
        except Exception as e:
            print("Excepción al crear cuenta:", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaCrearCuenta(cliente_id=12345)
    ventana.show()
    sys.exit(app.exec_())
