from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QMessageBox, QFormLayout,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt, pyqtSignal
from datetime import datetime
from src.model.cuenta import Cuenta


class MisCuentasWidget(QWidget):
    cuenta_creada = pyqtSignal()

    def __init__(self, id_cliente):
        super().__init__()
        self.id_cliente = id_cliente
        self.init_ui()
        self.tabla = QTableWidget()

    def actualizar_datos(self):
        print("Actualizando tabla de cuentas...")


    def actualizar_tabla(self):
        self.cargar_cuentas()

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

        layout.addWidget(QLabel("Cuentas creadas:"))
        self.tabla_cuentas = QTableWidget()
        self.tabla_cuentas.setColumnCount(5)
        self.tabla_cuentas.setHorizontalHeaderLabels(["Número", "Tipo", "Estado", "Fecha Apertura", "Saldo"])
        self.tabla_cuentas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabla_cuentas)

        self.setLayout(layout)

        self.cargar_cuentas()

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

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            num_cuenta = f"C{timestamp}"

            # Estado por defecto 'Activa'
            exito = Cuenta.crear(num_cuenta, tipo, monto_float, self.id_cliente, estado='Activa')

            if exito:
                QMessageBox.information(self, "Cuenta creada", "La cuenta ha sido creada exitosamente.")
                self.monto_inicial.clear()
                self.descripcion.clear()
                self.cargar_cuentas()
                self.cuenta_creada.emit()
            else:
                QMessageBox.critical(self, "Error", "Ocurrió un error al crear la cuenta.")
        except Exception as e:
            QMessageBox.critical(self, "Error inesperado", f"Ocurrió un error:\n{e}")

    def cargar_cuentas(self):
        self.tabla_cuentas.setRowCount(0)
        cuentas = Cuenta.obtener_por_cliente(self.id_cliente)  # Usamos obtener_por_cliente, no obtener_por_documento
        for cuenta in cuentas:
            num_cuenta = cuenta[1]
            tipo = cuenta[2]
            estado = cuenta[3]
            fecha = cuenta[4].strftime('%Y-%m-%d %H:%M')
            saldo = f"${cuenta[5]:,.2f}"

            row_position = self.tabla_cuentas.rowCount()
            self.tabla_cuentas.insertRow(row_position)
            self.tabla_cuentas.setItem(row_position, 0, QTableWidgetItem(num_cuenta))
            self.tabla_cuentas.setItem(row_position, 1, QTableWidgetItem(tipo))
            self.tabla_cuentas.setItem(row_position, 2, QTableWidgetItem(estado))
            self.tabla_cuentas.setItem(row_position, 3, QTableWidgetItem(fecha))
            self.tabla_cuentas.setItem(row_position, 4, QTableWidgetItem(saldo))
