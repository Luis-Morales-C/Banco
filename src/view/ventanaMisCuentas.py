from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QListWidget, QMessageBox, QFormLayout
)
from PyQt5.QtCore import Qt
from datetime import datetime
from src.model.cuenta import Cuenta

class MisCuentasWidget(QWidget):
    def __init__(self, id_cliente):
        super().__init__()
        self.id_cliente = id_cliente  # necesario para relacionar la cuenta al cliente
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)

        titulo = QLabel("Crear Nueva Cuenta")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #573b8a;")
        layout.addWidget(titulo, alignment=Qt.AlignTop)

        form_layout = QFormLayout()

        self.tipo_cuenta = QComboBox()
        self.tipo_cuenta.addItems(["Ahorros", "Corriente", "Inversiones"])

        self.monto_inicial = QLineEdit()
        self.monto_inicial.setPlaceholderText("Monto inicial")
        self.monto_inicial.setValidator(QDoubleValidator(0.00, 9999999.99, 2))

        self.descripcion = QLineEdit()
        self.descripcion.setPlaceholderText("Descripción (opcional)")

        form_layout.addRow("Tipo de cuenta:", self.tipo_cuenta)
        form_layout.addRow("Monto inicial:", self.monto_inicial)
        form_layout.addRow("Descripción:", self.descripcion)

        layout.addLayout(form_layout)

        boton_crear = QPushButton("Crear cuenta")
        boton_crear.clicked.connect(self.crear_cuenta)
        layout.addWidget(boton_crear)

        self.lista_cuentas = QListWidget()
        layout.addWidget(QLabel("Cuentas creadas:"))
        layout.addWidget(self.lista_cuentas)

        self.setLayout(layout)

    def crear_cuenta(self):
        try:
            tipo = self.tipo_cuenta.currentText()
            monto = self.monto_inicial.text().strip()

            if not monto:
                QMessageBox.warning(self, "Campos incompletos", "Por favor ingresa el monto inicial.")
                return

            try:
                monto_float = float(monto)
                if monto_float < 0:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(self, "Monto inválido", "El monto inicial debe ser un número válido y positivo.")
                return

            # Generar número de cuenta único (ejemplo con timestamp)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            num_cuenta = f"C{timestamp}"

            # Insertar en la base de datos
            exito = Cuenta.crear(num_cuenta, tipo, monto_float, self.id_cliente)

            if exito:
                cuenta_str = f"{tipo} - {num_cuenta} - ${monto}"
                self.lista_cuentas.addItem(cuenta_str)
                QMessageBox.information(self, "Cuenta creada", "La cuenta ha sido creada exitosamente.")
                self.monto_inicial.clear()
                self.descripcion.clear()
            else:
                QMessageBox.critical(self, "Error", "Ocurrió un error al crear la cuenta.")
        except Exception as e:
            QMessageBox.critical(self, "Error inesperado", f"Ocurrió un error:\n{e}")
