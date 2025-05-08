import sys
from PyQt5.QtWidgets import QApplication
from controller.main import Controlador

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controlador = Controlador()
    controlador.mostrar_inicio()
    sys.exit(app.exec_())
