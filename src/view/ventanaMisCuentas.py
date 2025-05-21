from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget

class MisCuentasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        titulo = QLabel("Mis Cuentas")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #573b8a;")
        layout.addWidget(titulo)

        # Lista ejemplo de cuentas (puedes llenar con datos reales)
        self.lista_cuentas = QListWidget()
        self.lista_cuentas.addItems([
            "Cuenta Ahorros - 123456789",
            "Cuenta Corriente - 987654321",
            "Cuenta Inversiones - 112233445"
        ])
        layout.addWidget(self.lista_cuentas)

        self.setLayout(layout)
