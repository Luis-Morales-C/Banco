from unicodedata import decimal

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit,
    QPushButton, QMessageBox, QFormLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from src.model.cuenta import Cuenta  # asumiendo la ruta y estructura
from src.model.transaccion import Transaccion
from decimal import Decimal, InvalidOperation

class VentanaRetiro(QWidget):
    retiro_exitoso = pyqtSignal()
    def __init__(self, id_cliente):
        super().__init__()
        self.setWindowTitle("Simulador de Retiro")
        self.setFixedSize(350, 250)
        self.id_cliente = id_cliente

        self.cuentas = []  # guardará datos con la estructura de la tupla SQL
        self.init_ui()
        self.cargar_cuentas()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.combo_cuentas = QComboBox()
        form_layout.addRow("Selecciona cuenta:", self.combo_cuentas)

        self.input_monto = QLineEdit()
        self.input_monto.setPlaceholderText("Ej: 100.00")
        form_layout.addRow("Monto a retirar:", self.input_monto)

        self.input_codigo = QLineEdit()
        self.input_codigo.setEchoMode(QLineEdit.Password)
        self.input_codigo.setPlaceholderText("Código de seguridad")
        form_layout.addRow("Código seguridad:", self.input_codigo)

        layout.addLayout(form_layout)

        btn_retirar = QPushButton("Retirar")
        btn_retirar.clicked.connect(self.validar_retiro)
        layout.addWidget(btn_retirar, alignment=Qt.AlignCenter)

        self.lbl_saldo = QLabel("")
        self.lbl_saldo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_saldo)

        self.setLayout(layout)

    def cargar_cuentas(self):
        self.combo_cuentas.clear()
        self.cuentas = Cuenta.obtener_por_cliente(self.id_cliente)
        if not self.cuentas:
            QMessageBox.warning(self, "Aviso", "No se encontraron cuentas para este cliente.")
            return

        for c in self.cuentas:
            # c = (id_cuenta, num_cuenta, tipo_cuenta, estado, fecha_apertura, saldo)
            texto = f"{c[1]} ({c[2]}) - Saldo: ${c[5]:.2f}"
            self.combo_cuentas.addItem(texto, c[0])

        self.actualizar_saldo_mostrar()
        self.combo_cuentas.currentIndexChanged.connect(self.actualizar_saldo_mostrar)

    def actualizar_saldo_mostrar(self):
        idx = self.combo_cuentas.currentIndex()
        if idx < 0:
            self.lbl_saldo.setText("")
            return
        saldo = self.cuentas[idx][5]
        self.lbl_saldo.setText(f"Saldo actual: ${saldo:.2f}")

    def validar_retiro(self):
        idx = self.combo_cuentas.currentIndex()
        if idx < 0:
          QMessageBox.warning(self, "Error", "Seleccione una cuenta.")
          return

        monto_str = self.input_monto.text().strip()
        codigo = self.input_codigo.text().strip()

        try:
          monto = Decimal(monto_str)
          if monto <= 0:
              raise ValueError
        except ValueError:
          QMessageBox.warning(self, "Error", "Monto inválido. Debe ser un número positivo.")
          return

        try:

          datos_retiro = Transaccion.validar_retiro(codigo)


          id_cuenta_seleccionada = self.cuentas[idx][0]
          if datos_retiro['id_cuenta'] != id_cuenta_seleccionada:
              QMessageBox.warning(self, "Error", "El código de seguridad no corresponde a la cuenta seleccionada.")
              return
          if monto != datos_retiro['monto']:
              QMessageBox.warning(self, "Error", "El monto ingresado no coincide con la transacción pendiente.")
              return

          if Transaccion.confirmar_retiro(codigo):
              self.retiro_exitoso.emit()
              nuevo_saldo = self.cuentas[idx][5] - monto
              c = list(self.cuentas[idx])
              c[5] = nuevo_saldo
              self.cuentas[idx] = tuple(c)
              self.actualizar_saldo_mostrar()

              QMessageBox.information(self, "Éxito", f"Retiro de ${monto:.2f} realizado correctamente.")
              self.input_monto.clear()
              self.input_codigo.clear()

        except Exception as e:
          QMessageBox.warning(self, "Error", str(e))