import os
import sys

from calamarlib.helpers import load_config
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from client import Client
from processor import GameProcessor

CURRENT_PATH = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(CURRENT_PATH)


class VentanaInicio(QMainWindow):
    # REF: T2
    def __init__(self, processor: GameProcessor):
        super(VentanaInicio, self).__init__()
        uic.loadUi(f"{CURRENT_DIR}/ventanas/inicio.ui", self)
        self.show()
        self.start_game.clicked.connect(self.open_game)
        self.processor = processor

    def open_game(self):
        usuario: str = self.usuario.text()
        fecha_de_nacimiento: str = self.fecha_de_nacimiento.text()
        if not self.processor.check_user_data(usuario, fecha_de_nacimiento):
            error = f"El usuario debe ser alfanumérico y no puede estar vacío."
            QMessageBox.warning(self, "Error", error)
        else:
            self.hide()
            # self.juego = VentanaJuego(usuario)


if __name__ == "__main__":
    host, port = load_config("cliente/parametros.json")

    client = Client(host, port)
    app = QApplication([])
    processor = GameProcessor(client)
    inicio = VentanaInicio(processor)

    sys.exit(app.exec_())
