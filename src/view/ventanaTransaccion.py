from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QMessageBox, QFormLayout,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
from datetime import datetime
from src.model.transaccion import Transaccion
from src.model.cuenta import Cuenta
class MisTransaccionesWidget(QWidget):
    def __init__(self, id_cliente):
        super().__init__()
        self.id_cliente = id_cliente
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)

        titulo = QLabel("Registrar Nueva Transacción")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #573b8a;")
        layout.addWidget(titulo, alignment=Qt.AlignTop)

        form_layout = QFormLayout()

        self.combo_cuenta_origen = QComboBox()
        form_layout.addRow("Cuenta Origen:", self.combo_cuenta_origen)

        self.tipo_transaccion = QComboBox()
        self.tipo_transaccion.addItems(["Transferencia", "Deposito", "Retiro"])
        self.tipo_transaccion.currentTextChanged.connect(self.cambiar_campos_adicional)
        form_layout.addRow("Tipo de Transacción:", self.tipo_transaccion)

        self.monto = QLineEdit()
        self.monto.setPlaceholderText("Monto")
        self.monto.setValidator(QDoubleValidator(0.01, 9999999.99, 2))
        form_layout.addRow("Monto:", self.monto)

        self.descripcion = QLineEdit()
        self.descripcion.setPlaceholderText("Descripción (opcional)")
        form_layout.addRow("Descripción:", self.descripcion)

        self.campo_adicional_label = QLabel("")
        self.campo_adicional_input = QLineEdit()
        form_layout.addRow(self.campo_adicional_label, self.campo_adicional_input)
        self.campo_adicional_label.hide()
        self.campo_adicional_input.hide()

        layout.addLayout(form_layout)

        boton_registrar = QPushButton("Registrar Transacción")
        boton_registrar.clicked.connect(self.registrar_transaccion)
        layout.addWidget(boton_registrar)

        layout.addWidget(QLabel("Historial de Transacciones:"))
        self.tabla_transacciones = QTableWidget()
        self.tabla_transacciones.setColumnCount(6)
        self.tabla_transacciones.setHorizontalHeaderLabels(
            ["ID", "Tipo", "Cuenta Origen", "Monto", "Fecha", "Estado"]
        )
        self.tabla_transacciones.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabla_transacciones)

        self.setLayout(layout)

        self.cambiar_campos_adicional(self.tipo_transaccion.currentText())
        self.actualizar_cuentas()
        self.cargar_transacciones()

    def cambiar_campos_adicional(self, tipo):
        if tipo == "Transferencia":
            self.campo_adicional_label.setText("Cuenta Destino:")
            self.campo_adicional_label.show()
            self.campo_adicional_input.show()
        elif tipo == "Retiro":
            self.campo_adicional_label.setText("Código Retiro:")
            self.campo_adicional_label.show()
            self.campo_adicional_input.show()
        else:
            self.campo_adicional_label.hide()
            self.campo_adicional_input.hide()
            self.campo_adicional_input.clear()

    def actualizar_cuentas(self):
        self.combo_cuenta_origen.clear()
        cuentas = Cuenta.obtener_por_documento(self.id_cliente)
        for cuenta in cuentas:
            self.combo_cuenta_origen.addItem(cuenta[1])  # numCuenta

    def registrar_transaccion(self):
        tipo = self.tipo_transaccion.currentText()
        cuenta_origen = self.combo_cuenta_origen.currentText()
        monto_text = self.monto.text().strip()
        descripcion = self.descripcion.text().strip()
        campo_adicional = self.campo_adicional_input.text().strip()

        if not monto_text:
            QMessageBox.warning(self, "Datos incompletos", "Por favor ingresa el monto.")
            return
        try:
            monto = float(monto_text)
            if monto <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Monto inválido", "Ingresa un monto válido mayor que cero.")
            return

        extra_args = {}
        if tipo == "Transferencia":
            if not campo_adicional:
                QMessageBox.warning(self, "Datos incompletos", "Ingresa la cuenta destino.")
                return
            extra_args['cuentaDestino'] = campo_adicional
            extra_args['nombre'] = "Transferencia"
        elif tipo == "Retiro":
            if not campo_adicional:
                QMessageBox.warning(self, "Datos incompletos", "Ingresa el código de retiro.")
                return
            extra_args['codigoRetiro'] = campo_adicional
            extra_args['nombre'] = "Retiro"
        elif tipo == "Deposito":
            extra_args['nombre'] = "Depósito"

        exito = Transaccion.crear_transaccion(
            monto=monto,
            cuenta_origen=cuenta_origen,
            tipo=tipo,
            descripcion=descripcion,
            cliente_id=self.id_cliente,
            **extra_args
        )

        if exito:
            QMessageBox.information(self, "Transacción registrada", "La transacción fue registrada exitosamente.")
            self.monto.clear()
            self.descripcion.clear()
            self.campo_adicional_input.clear()
            self.cargar_transacciones()
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar la transacción.")

    def cargar_transacciones(self):
        self.tabla_transacciones.setRowCount(0)
        transacciones = Transaccion.obtener_por_cliente(self.id_cliente)
        for trans in transacciones:
            row_position = self.tabla_transacciones.rowCount()
            self.tabla_transacciones.insertRow(row_position)
            self.tabla_transacciones.setItem(row_position, 0, QTableWidgetItem(str(trans['id'])))
            self.tabla_transacciones.setItem(row_position, 1, QTableWidgetItem(trans['tipo']))
            self.tabla_transacciones.setItem(row_position, 2, QTableWidgetItem(trans['cuenta_origen']))
            self.tabla_transacciones.setItem(row_position, 3, QTableWidgetItem(f"${trans['monto']:,.2f}"))
            self.tabla_transacciones.setItem(row_position, 4, QTableWidgetItem(trans['fecha'].strftime('%Y-%m-%d %H:%M')))
            self.tabla_transacciones.setItem(row_position, 5, QTableWidgetItem(trans['estado']))
