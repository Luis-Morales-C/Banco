# src/view/ventanaPrincipal.py
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.setWindowTitle("Ventana Principal")
        self.setGeometry(100, 100, 400, 300)  # Tamaño de la ventana

        # Crear un widget central
        widget = QWidget(self)
        self.setCentralWidget(widget)

        # Crear un layout para la ventana principal
        layout = QVBoxLayout()

        # Crear un QLabel (puedes agregar más widgets según sea necesario)
        label = QLabel("Bienvenido a la ventana principal", self)
        layout.addWidget(label)

        # Establecer el layout para el widget central
        widget.setLayout(layout)
