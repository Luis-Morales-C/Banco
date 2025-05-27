import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget
)
from PyQt5.QtCore import Qt

from src.view.ventanaMisCuentas import MisCuentasWidget
from src.view.ventanaTransaccion import MisTransaccionesWidget
from src.view.VentanEditarCuentas import EditarInformacionPersonalWidget
from src.view.ventanaUtilidades import UtilidadesWidget
from src.view.ventanaRetiro import VentanaRetiro

class PortalBancario(QMainWindow):
    def __init__(self, cliente_id):
        super().__init__()
        self.setWindowTitle("Portal Bancario")
        self.setFixedSize(1000,600)

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        self.setCentralWidget(main_widget)


        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: #2e1f4f;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(15)


        self.btn_mis_cuentas = QPushButton("Mis Cuentas")
        self.btn_transacciones = QPushButton("Transacciones")
        self.btn_editar_cuenta = QPushButton("Editar")
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


        self.stack = QStackedWidget()

        self.editar_cliente_panel =EditarInformacionPersonalWidget(cliente_id)

        self.mis_cuentas_panel = MisCuentasWidget(cliente_id)
        self.transacciones_panel = MisTransaccionesWidget(cliente_id)
        self.utilidades_panel = UtilidadesWidget(cliente_id)
        self.retiro_panel = VentanaRetiro(cliente_id)




        self.mis_cuentas_panel.cuenta_creada.connect(self.transacciones_panel.actualizar_cuentas)
        self.transacciones_panel.transaccion_realizada.connect(self.mis_cuentas_panel.actualizar_tabla)
        self.retiro_panel.retiro_exitoso.connect(self.mis_cuentas_panel.actualizar_tabla)
        self.retiro_panel.retiro_exitoso.connect(self.transacciones_panel.actualizar_cuentas)




        self.stack.addWidget(self.mis_cuentas_panel)
        self.stack.addWidget(self.transacciones_panel)
        self.stack.addWidget(self.editar_cliente_panel)
        self.stack.addWidget(self.utilidades_panel)
        self.stack.addWidget(self.retiro_panel)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)


        self.btn_mis_cuentas.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_transacciones.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_editar_cuenta.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.btn_utilidades.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        # self.btn_soporte.clicked.connect(lambda: self.stack.setCurrentIndex(4))

        self.stack.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    #ventana = PortalBancario(cliente_id)
    #ventana.show()
    sys.exit(app.exec_())
