# widget_transacciones.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QMessageBox, QFormLayout,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDoubleValidator
import random
import string

from src.model.transaccion import Transaccion
from src.model.cuenta import Cuenta

class MisTransaccionesWidget(QWidget):
    transaccion_realizada = pyqtSignal()

    def __init__(self, id_cliente):
        super().__init__()
        self.id_cliente = id_cliente
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Componentes de la interfaz
        self.tipo_transaccion = QComboBox()
        self.tipo_transaccion.addItems(["Transferencia", "Deposito", "Retiro"])
        self.tipo_transaccion.currentTextChanged.connect(self.actualizar_campos)

        self.combo_cuenta_origen = QComboBox()
        self.monto = QLineEdit()
        self.monto.setValidator(QDoubleValidator(0.01, 9999999.99, 2))
        self.descripcion = QLineEdit()
        self.campo_adicional = QLineEdit()


        form_layout = QFormLayout()
        form_layout.addRow("Tipo de transacción:", self.tipo_transaccion)
        form_layout.addRow("Cuenta origen:", self.combo_cuenta_origen)
        form_layout.addRow("Monto:", self.monto)
        form_layout.addRow("Descripción:", self.descripcion)
        form_layout.addRow(QLabel("Cuenta destino:"), self.campo_adicional)

        self.tabla_transacciones = QTableWidget()
        self.tabla_transacciones.setColumnCount(6)
        self.tabla_transacciones.setHorizontalHeaderLabels(
            ["ID", "Tipo", "Cuenta Origen", "Monto", "Fecha", "Estado"]
        )
        self.tabla_transacciones.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        boton_registrar = QPushButton("Registrar Transacción")
        boton_registrar.clicked.connect(self.registrar_transaccion)


        layout.addLayout(form_layout)
        layout.addWidget(boton_registrar)
        layout.addWidget(QLabel("Historial de Transacciones:"))
        layout.addWidget(self.tabla_transacciones)

        self.setLayout(layout)
        self.actualizar_cuentas()
        self.actualizar_campos()
        self.cargar_transacciones()

    def actualizar_campos(self):
        tipo = self.tipo_transaccion.currentText()
        self.campo_adicional.setVisible(tipo in ["Transferencia", "Retiro"])

        if tipo == "Transferencia":
            self.campo_adicional.setPlaceholderText("Número de cuenta destino")
            self.campo_adicional.setReadOnly(False)
        elif tipo == "Retiro":
            self.campo_adicional.setPlaceholderText("Código de retiro")
            self.campo_adicional.setReadOnly(True)
            self.campo_adicional.clear()
        else:
            self.campo_adicional.clear()

    def actualizar_cuentas(self):
        self.combo_cuenta_origen.clear()
        cuentas = Cuenta.obtener_por_cliente(self.id_cliente)
        for cuenta in cuentas:
            self.combo_cuenta_origen.addItem(cuenta[1], cuenta[0])

    def generar_codigo_retiro(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def registrar_transaccion(self):
        try:
            tipo = self.tipo_transaccion.currentText()
            num_cuenta_origen = self.combo_cuenta_origen.currentText()
            cuenta_origen_id = Cuenta.obtener_id_por_numero(num_cuenta_origen)
            monto = float(self.monto.text())
            descripcion = self.descripcion.text()
            extra_args = {}

            if tipo == "Transferencia":
                cuenta_destino = self.campo_adicional.text()
                if not Cuenta.validar_cuenta(cuenta_destino):
                    raise ValueError("La cuenta destino no existe")
                extra_args['cuentaDestino'] = cuenta_destino

            elif tipo == "Retiro":
                codigo = self.generar_codigo_retiro()
                self.campo_adicional.setText(codigo)
                extra_args['codigoRetiro'] = codigo
                QMessageBox.information(self, "Código de Retiro", f"Su código es: {codigo}")

            Transaccion.crear_transaccion(
                monto=monto,
                id_cuenta=cuenta_origen_id,
                tipo_transaccion=tipo,
                descripcion=descripcion,
                **extra_args
            )

            QMessageBox.information(self, "Éxito", "Transacción registrada correctamente")
            self.transaccion_realizada.emit()
            self.cargar_transacciones()
            self.monto.clear()
            self.descripcion.clear()

        except ValueError as e:
            QMessageBox.warning(self, "Error de validación", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al procesar transacción: {str(e)}")

    def cargar_transacciones(self):
        self.tabla_transacciones.setRowCount(0)
        transacciones = Transaccion.obtener_por_cliente(self.id_cliente)

        for idx, trans in enumerate(transacciones):
            self.tabla_transacciones.insertRow(idx)
            self.tabla_transacciones.setItem(idx, 0, QTableWidgetItem(str(trans['id'])))
            self.tabla_transacciones.setItem(idx, 1, QTableWidgetItem(trans['tipo']))
            self.tabla_transacciones.setItem(idx, 2, QTableWidgetItem(trans['cuenta_origen']))
            self.tabla_transacciones.setItem(idx, 3, QTableWidgetItem(f"${trans['monto']:,.2f}"))
            self.tabla_transacciones.setItem(idx, 4, QTableWidgetItem(trans['fecha'].strftime('%Y-%m-%d %H:%M')))
            self.tabla_transacciones.setItem(idx, 5, QTableWidgetItem(trans['estado']))