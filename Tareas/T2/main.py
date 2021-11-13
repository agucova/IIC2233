import sys

from PyQt5 import uic
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsView,
    QMainWindow,
)

import parametros as p
from game_views import FroggyView, RoadGameView


class VentanaInicio(QMainWindow):
    def __init__(self):
        super(VentanaInicio, self).__init__()
        uic.loadUi("ventanas/inicio.ui", self)
        self.show()
        self.iniciar_partida.clicked.connect(self.abrir_juego)

    def abrir_juego(self):
        self.hide()
        usuario = self.usuario.text()
        self.juego = VentanaJuego(usuario)


class VentanaJuego(QMainWindow):
    def __init__(self, username):
        super(VentanaJuego, self).__init__()
        self.username = username

        self.init_ui()
        self.init_games()
        self.init_froggy()

    def init_ui(self):
        uic.loadUi("ventanas/juego.ui", self)

        self.scene_x = 20
        self.scene_y = 330
        self.scene_width = 1040
        self.scene_height = 560

        self.scene = QGraphicsScene(
            self.scene_x, self.scene_y, self.scene_width, self.scene_height
        )

        view = QGraphicsView(self.scene, self)
        view.setRenderHint(QPainter.Antialiasing)
        view.grabKeyboard()

        self.scene_container.addWidget(view)

        self.show()
        self.activateWindow()

    def init_games(self):
        self.paint_scene_background("sprites/Mapa/areas/scene_frame.png")
        self.road_game_down = RoadGameView(
            self.scene,
            self.scene_x,
            self.scene_y,
            self.scene_width,
            self.scene_height,
            "down",
        )
        self.road_game_up = RoadGameView(
            self.scene,
            self.scene_x,
            self.scene_y,
            self.scene_width,
            self.scene_height,
            "up",
        )

    def init_froggy(self):
        self.froggy = FroggyView(
            self.username,
            self.scene,
            self.scene_x,
            self.scene_y,
            self.scene_width,
            self.scene_height,
        )
        # Signals fromn the back-end
        self.froggy.player.updated_lifes_signal.connect(self.valor_vidas.setText)
        self.valor_vidas.setText(str(self.froggy.player.lifes))

        self.froggy.player.updated_score_signal.connect(self.valor_puntaje.setText)
        self.valor_puntaje.setText(str(self.froggy.player.score))

        self.froggy.player.updated_level_signal.connect(self.valor_nivel.setText)
        self.valor_nivel.setText(str(self.froggy.player.level))

        self.froggy.player.updated_coins_signal.connect(self.valor_monedas.setText)
        self.valor_monedas.setText(str(self.froggy.player.coins))

        self.froggy.player.updated_time_signal.connect(self.valor_tiempo.setText)
        self.valor_tiempo.setText(str(self.froggy.player._time_left))

        self.froggy.game_started.connect(self.empezar.hide)

        # Set up collision detection
        self.road_game_down.player = self.froggy.item
        self.road_game_up.player = self.froggy.item
        self.road_game_down.collision_signal.connect(self.froggy.car_collision)
        self.road_game_up.collision_signal.connect(self.froggy.car_collision)

    def paint_scene_background(self, path):
        """Scales and adds the given background to the Graphics Scene."""
        background = QGraphicsPixmapItem(
            QPixmap(path).scaled(self.scene_width, self.scene_height)
        )
        background.setOffset(self.scene_x, self.scene_y)
        self.scene.addItem(background)


class VentanaRanking(QMainWindow):
    def __init__(self):
        super(VentanaRanking, self).__init__()
        uic.loadUi("ventanas/ranking.ui", self)
        self.show()


class VentanaPostNivel(QMainWindow):
    pass


if __name__ == "__main__":
    app = QApplication([])
    inicio = VentanaInicio()

    sys.exit(app.exec_())
