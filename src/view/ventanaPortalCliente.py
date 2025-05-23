import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget
)
from PyQt5.QtCore import Qt

from src.view.ventanaMisCuentas import MisCuentasWidget


#from mis_cuentas import MisCuentasWidget
#from transacciones import TransaccionesWidget
#from editar_cuenta import EditarCuentaWidget
#from utilidades import UtilidadesWidget
#from soporte import SoporteWidget""

class PortalBancario(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Portal Bancario")
        self.setFixedSize(900, 600)

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # Sidebar oscuro
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: #2e1f4f;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(15)

        # Botones sidebar
        self.btn_mis_cuentas = QPushButton("Mis Cuentas")
        self.btn_transacciones = QPushButton("Transacciones")
        self.btn_editar_cuenta = QPushButton("Editar Cuenta")
        self.btn_utilidades = QPushButton("Utilidades")
        self.btn_soporte = QPushButton("Soporte")

        for btn in [self.btn_mis_cuentas, self.btn_transacciones, self.btn_editar_cuenta, self.btn_utilidades, self.btn_soporte]:
            btn.setFixedHeight(50)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    color: white;
                    font-weight: bold;
                    font-size: 16px;
                    background-color: transparent;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #4b3a82;
                }
            """)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # Área principal con stacked widgets
        self.stack = QStackedWidget()
        self.mis_cuentas_panel = MisCuentasWidget()
        # self.transacciones_panel = TransaccionesWidget()
        # self.editar_cuenta_panel = EditarCuentaWidget()
        #self.utilidades_panel = UtilidadesWidget()
        # self.soporte_panel = SoporteWidget()

        self.stack.addWidget(self.mis_cuentas_panel)      # 0
        # self.stack.addWidget(self.transacciones_panel)    # 1
        #self.stack.addWidget(self.editar_cuenta_panel)    # 2
        # self.stack.addWidget(self.utilidades_panel)       # 3
        #self.stack.addWidget(self.soporte_panel)           # 4

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)

        # Conectar botones para cambiar paneles
        self.btn_mis_cuentas.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_transacciones.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_editar_cuenta.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.btn_utilidades.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        self.btn_soporte.clicked.connect(lambda: self.stack.setCurrentIndex(4))

        self.stack.setCurrentIndex(0)  # Ventana inicial

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = PortalBancario()
    ventana.show()
    sys.exit(app.exec_())
