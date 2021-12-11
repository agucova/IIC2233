from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from calamarlib.helpers import load_config
import os

from client import Client


CURRENT_PATH = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_PATH)


class VentanaInicio(QMainWindow):
    # REF: T2
    def __init__(self):
        super(VentanaInicio, self).__init__()
        uic.loadUi(f"{CURRENT_DIR}/ventanas/inicio.ui", self)
        self.show()
        self.start_game.clicked.connect(self.open_game)

    def open_game(self):
        usuario: str = self.usuario.text()
        fecha_de_nacimiento: str = self.fecha_de_nacimiento.text()
        self.hide()
        pass
        # self.juego = VentanaJuego(usuario)
        # error = (
        #     f"El usuario debe ser alfanumérico"
        #     f" y tener entre {p.MIN_CARACTERES} y {p.MAX_CARACTERES} caracteres."
        # )
        # QMessageBox.warning(self, "Error", error)


if __name__ == "__main__":
    host, port = load_config("cliente/parametros.json")

    client = Client(host, port)
    app = QApplication([])
    inicio = VentanaInicio()

    sys.exit(app.exec_())
