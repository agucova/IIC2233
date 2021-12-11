import os
import sys

from calamarlib.helpers import load_config
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QMessageBox, QPushButton

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

        # Signals
        self.processor.client.server_disconnect_signal.connect(self.server_disconnect)

    def open_game(self):
        usuario: str = self.usuario.text()
        fecha_de_nacimiento: str = self.fecha_de_nacimiento.text()
        checked = self.processor.check_user_data(usuario, fecha_de_nacimiento)
        if not checked and checked is not None:
            error = f"El usuario debe ser alfanumérico, único y no puede estar vacío."
            QMessageBox.warning(self, "Error", error)
        else:
            self.processor.register_user(usuario, fecha_de_nacimiento)
            self.hide()
            self.sala_espera = SalaEspera(self.processor)

    def server_disconnect(self):
        QMessageBox.warning(self, "Error", "No se pudo conectar con el servidor.")
        self.close()
        sys.exit(1)


class SalaEspera(QMainWindow):
    # REF: T2
    def __init__(self, processor: GameProcessor):
        super(SalaEspera, self).__init__()
        uic.loadUi(f"{CURRENT_DIR}/ventanas/sala_espera.ui", self)
        self.processor = processor
        self.show()
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.update_players)
        self.refresh_timer.start(1500)

    def update_players(self):
        players = self.processor.get_players()
        if players is not None:
            # Remove all players
            for i in reversed(range(self.lista_jugadores.count())):
                self.lista_jugadores.itemAt(i).widget().setParent(None)
            # Add them back updated
            for player in players:
                name = QLabel(player["username"])
                if player["currently_playing"]:
                    name.setStyleSheet("color: red;")
                    self.lista_jugadores.addRow(name, QLabel("En juego"))
                elif player["username"] == self.processor.username:
                    name.setStyleSheet("color: green;")
                    self.lista_jugadores.addRow(name, QLabel("(tú)"))
                else:
                    name.setStyleSheet("color: green;")
                    challenge_button = QPushButton()
                    challenge_button.setText("Retar")
                    challenge_button.clicked.connect(
                        lambda: self.processor.challenge_player(player["username"])
                    )
                    self.lista_jugadores.addRow(name, challenge_button)


if __name__ == "__main__":
    host, port = load_config("cliente/parametros.json")

    client = Client(host, port)
    app = QApplication([])
    processor = GameProcessor(client)
    inicio = VentanaInicio(processor)

    sys.exit(app.exec_())
