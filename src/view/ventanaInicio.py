from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QPushButton, QVBoxLayout, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QColor, QCursor
from PyQt5.QtCore import Qt
import sys

class VentanaInicio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Portal Banco")
        self.setFixedSize(700, 800)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(25)

        # Título
        titulo = QLabel("Portal Banco")
        titulo.setFont(QFont("Segoe UI", 26, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Botón Login
        boton_login = QPushButton("Login")
        boton_login.setObjectName("card")
        layout.addWidget(boton_login)

        # Botón Registrar
        boton_registrar = QPushButton("Registrar")
        boton_registrar.setObjectName("card")
        layout.addWidget(boton_registrar)

        # Enlace de recuperación
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
                color: white;  /* Color blanco para el enlace */
                font-size: 15px;
                text-decoration: none;  /* Sin subrayado */
            }

            QLabel#enlace:link, QLabel#enlace:visited {
                color: white;  /* Color blanco para el enlace en cualquier estado */
                text-decoration: none;  /* Asegura que no se subraye */
            }

            QLabel#enlace:hover {
                color: #f7ba2b;  /* Cambia color cuando pasa el mouse */
                text-decoration: underline;  /* Subraya cuando pasa el mouse */
            }

            QPushButton#card {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #f7ba2b, stop: 1 #ea5358
                );
                border: none;
                color: #181818;
                font-weight: bold;
                letter-spacing: 1px;
                border-radius: 14px;
                padding: 15px;
                font-size: 16px;
                min-width: 200px;
            }

            QPushButton#card:hover {
                color: #f7ba2b;
                background: #181818;
                border: 2px solid #f7ba2b;
            }
        """)

        # Sombra a los botones
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