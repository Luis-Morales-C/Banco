from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QPushButton, QVBoxLayout, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QColor, QCursor
from PyQt5.QtCore import Qt
import sys

class VentanaInicio(QMainWindow,):
    def __init__(self,mostrar_registro_callback,mostrar_login_callback):
        super().__init__()
        self.setWindowTitle("Portal Banco")
        self.setFixedSize(700, 800)
        self.mostrar_registro_callback = mostrar_registro_callback
        self.mostrar_login_callback = mostrar_login_callback
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(25)

        titulo = QLabel("Portal Banco")
        titulo.setFont(QFont("Segoe UI", 26, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)


        boton_login = QPushButton("Login")
        boton_login.setObjectName("card")
        boton_login.clicked.connect(self.mostrar_login_callback)
        layout.addWidget(boton_login)


        boton_registrar = QPushButton("Registrar")
        boton_registrar.clicked.connect(self.mostrar_registro_callback)
        boton_registrar.setObjectName("card")
        layout.addWidget(boton_registrar)


        label_olvide = QLabel("<a href='#'>¿Se te olvidó tu contraseña?</a>")
        label_olvide.setAlignment(Qt.AlignCenter)
        label_olvide.setTextFormat(Qt.RichText)
        label_olvide.setTextInteractionFlags(Qt.TextBrowserInteraction)
        label_olvide.setOpenExternalLinks(False)
        label_olvide.setObjectName("enlace")
        label_olvide.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(label_olvide)

        # Estilo general
        self.setStyleSheet("""
    QWidget {
        background-color: #181818;
    }

    QLabel {
        color: white;
    }

    QLabel#enlace {
        color: white;
        font-size: 15px;
        text-decoration: none;
    }

    QLabel#enlace:link, QLabel#enlace:visited {
        color: white;
        text-decoration: none;
    }

    QLabel#enlace:hover {
        color: #f7ba2b;
        text-decoration: underline;
    }

    QPushButton#card {
        background: qlineargradient(
            x1: 1, y1: 0, x2: 0, y2: 0,
            stop: 0 #9b59b6, stop: 1 #a5c1e7
        );
        border-radius: 16px;
        padding: 20px;
        font-size: 15px;
        font-weight: bold;
        letter-spacing: 2px;
        color: white;
        min-width: 200px;
        border: none;
    }

    QPushButton#card:hover {
        color: #a5c1e7;
        background: white;
        transition: color 1s;
    }
""")


        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 180))

        boton_login.setGraphicsEffect(shadow)
        boton_registrar.setGraphicsEffect(shadow)

        central_widget.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaInicio()
    ventana.show()
    sys.exit(app.exec_())