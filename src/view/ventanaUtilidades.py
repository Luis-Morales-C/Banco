from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QMessageBox, QCalendarWidget
)
from PyQt5.QtCore import Qt
import os
import platform

from src.view.ventanaRetiro import VentanaRetiro

class UtilidadesWidget(QWidget):
    def __init__(self, id_cliente):
        super().__init__()
        self.id_cliente = id_cliente
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)


        titulo = QLabel("Herramientas y Utilidades")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #573b8a;")
        layout.addWidget(titulo, alignment=Qt.AlignTop)


        btn_calculadora = QPushButton("Abrir Calculadora del Sistema")
        btn_calculadora.clicked.connect(self.abrir_calculadora)
        layout.addWidget(btn_calculadora)


        lbl_calendario = QLabel("Calendario")
        lbl_calendario.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(lbl_calendario)

        self.calendario = QCalendarWidget()
        layout.addWidget(self.calendario)


        btn_retiro = QPushButton("Abrir Simulador de Retiro")
        btn_retiro.clicked.connect(self.abrir_ventana_retiro)
        layout.addWidget(btn_retiro)

        self.setLayout(layout)

    def abrir_calculadora(self):
        sistema = platform.system()
        try:
            if sistema == "Windows":
                os.system("start calc")
            elif sistema == "Linux":
                os.system("gnome-calculator &")
            elif sistema == "Darwin":
                os.system("open -a Calculator")
            else:
                QMessageBox.warning(self, "Error", "Sistema no compatible.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir la calculadora:\n{e}")

    def abrir_ventana_retiro(self):
        self.ventana_retiro = VentanaRetiro(self.id_cliente)
        self.ventana_retiro.show()
