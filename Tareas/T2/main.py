import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsItem,
    QGraphicsScene,
    QGraphicsView,
    QMainWindow,
    QWidget,
    QGraphicsPixmapItem,
)

from juego import RoadGame


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
    def __init__(self, usuario):
        super(VentanaJuego, self).__init__()
        self.init_ui()
        self.init_road()

    def init_ui(self):
        uic.loadUi("ventanas/juego.ui", self)

        self.scene_x = 30
        self.scene_y = 350
        self.scene_width = 1240
        self.scene_height = 500

        self.scene = QGraphicsScene(
            self.scene_x, self.scene_y, self.scene_width, self.scene_height
        )

        view = QGraphicsView(self.scene, self)
        view.setRenderHint(QPainter.Antialiasing)

        self.layout_view.addWidget(view)

        self.show()

    def paint_scene_background(self, path):
        """Scales and adds the given background to the Graphics Scene."""
        background = QGraphicsPixmapItem(
            QPixmap(path).scaled(self.scene_width, self.scene_height)
        )
        background.setOffset(self.scene_x, self.scene_y)
        self.scene.addItem(background)

    ###########################
    # Roads Game (Carreteras) #
    ###########################
    def init_road(self):
        self.scene.clear()
        self.paint_scene_background("sprites/Mapa/areas/carretera.png")

        self.game = RoadGame()
        self.game.paint_car_signal.connect(self.spawn_car)

    def spawn_car(self, side):
        assert side in ("left", "right")
        car = QGraphicsPixmapItem(QPixmap("sprites/Mapa/autos/morado_left.png"))
        car.setOffset(self.scene_x + 20, self.scene_y + 20)
        self.scene.addItem(car)


class VentanaRanking(QMainWindow):
    def __init__(self):
        super(VentanaRanking, self).__init__()
        uic.loadUi("ventanas/ranking.ui", self)
        self.show()


class VentanaPostNivel(QMainWindow):
    pass


if __name__ == "__main__":
    # def hook(type, value, traceback):
    #     print(type)
    #     print(traceback)
    # sys.__excepthook__ = hook

    app = QApplication([])
    inicio = VentanaInicio()

    sys.exit(app.exec_())
