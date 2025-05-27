from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QMessageBox, QLineEdit, QCalendarWidget, QHBoxLayout
)
from PyQt5.QtCore import Qt
import os
import platform


class UtilidadesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.saldo = 100000  # Saldo inicial simulado
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Título
        titulo = QLabel("Herramientas y Utilidades")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #573b8a;")
        layout.addWidget(titulo, alignment=Qt.AlignTop)

        # --- CALCULADORA DEL SISTEMA ---
        btn_calculadora = QPushButton("Abrir Calculadora del Sistema")
        btn_calculadora.clicked.connect(self.abrir_calculadora)
        layout.addWidget(btn_calculadora)

        # --- CALENDARIO ---
        lbl_calendario = QLabel("Calendario")
        lbl_calendario.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(lbl_calendario)

        self.calendario = QCalendarWidget()
        layout.addWidget(self.calendario)

        # --- SIMULADOR DE CAJERO ---
        lbl_cajero = QLabel("Simulador de Cajero (Retiro)")
        lbl_cajero.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(lbl_cajero)

        self.lbl_saldo = QLabel(f"Saldo actual: ${self.saldo:,.0f}")
        layout.addWidget(self.lbl_saldo)

        caja_retiro = QHBoxLayout()
        self.input_retiro = QLineEdit()
        self.input_retiro.setPlaceholderText("Monto a retirar")
        btn_retirar = QPushButton("Retirar")
        btn_retirar.clicked.connect(self.retirar_dinero)
        caja_retiro.addWidget(self.input_retiro)
        caja_retiro.addWidget(btn_retirar)
        layout.addLayout(caja_retiro)

        self.setLayout(layout)

    def abrir_calculadora(self):
        sistema = platform.system()
        try:
            if sistema == "Windows":
                os.system("start calc")
            elif sistema == "Linux":
                os.system("gnome-calculator &")  # Puede cambiar según el entorno
            elif sistema == "Darwin":
                os.system("open -a Calculator")
            else:
                QMessageBox.warning(self, "Error", "Sistema no compatible con este comando.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir la calculadora:\n{e}")

    def retirar_dinero(self):
        try:
            monto = int(self.input_retiro.text())
            if monto <= 0:
                raise ValueError("El monto debe ser positivo.")

            if monto > self.saldo:
                QMessageBox.warning(self, "Fondos insuficientes", "No tienes suficiente saldo.")
            else:
                self.saldo -= monto
                self.lbl_saldo.setText(f"Saldo actual: ${self.saldo:,.0f}")
                QMessageBox.information(self, "Retiro exitoso", f"Has retirado ${monto:,.0f}")
                self.input_retiro.clear()
        except ValueError:
            QMessageBox.warning(self, "Entrada inválida", "Por favor ingresa un número válido.")
