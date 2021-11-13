import sys
from random import choice
from typing import Optional
from datetime import datetime, timedelta

from PyQt5 import uic
from PyQt5.Qt import Qt
from PyQt5.QtCore import QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QKeyEvent, QPainter, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsItem,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsView,
    QMainWindow,
)

import parametros as p
from game_state import Car, Froggy, RoadGame


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


class FroggyView(QObject):
    game_started = pyqtSignal()

    def __init__(
        self,
        username: str,
        scene: QGraphicsScene,
        scene_x: int,
        scene_y: int,
        scene_width: int,
        scene_height: int,
    ):
        super().__init__()
        self.player = Froggy(username)
        self.scene = scene
        self.scene_x = scene_x
        self.scene_y = scene_y
        self.scene_width = scene_width
        self.scene_height = scene_height
        self.color = choice(p.COLORES_PERSONAJE)

        self.pressed_once = False

        self.spawn_froggy()

        self.last_collision_time: Optional[datetime] = None

    def spawn_froggy(self):
        # Load initial still image
        self.image = QPixmap(f"sprites/Personajes/{self.color}/still.png")
        self.image = self.image.scaledToHeight(50)
        self.item = QGraphicsPixmapItem(self.image)
        # Place at the bottom
        self.item.setOffset(self.scene_x + 500, self.scene_y + 500)
        # Add to the scene
        self.scene.addItem(self.item)
        # Connect to our key handler
        self.item.setFlags(self.item.GraphicsItemFlag.ItemIsFocusable)
        self.scene.setFocusItem(self.item)
        self.item.keyPressEvent = self.key_press_handler
        self.item.mousePressEvent = lambda event: self.game_started.emit()

    def to_start(self):
        self.item.setOffset(self.scene_x + 500, self.scene_y + 500)
        self.item.setPos(0, 0)

    def key_press_handler(self, event: QKeyEvent):
        self.pressed_once or self.game_started.emit()
        if event.key() in (Qt.Key_Up, Qt.Key_W):
            self.move("up")
        elif event.key() in (Qt.Key_Down, Qt.Key_S):
            self.move("down")
        elif event.key() in (Qt.Key_Left, Qt.Key_A):
            self.move("left")
        elif event.key() in (Qt.Key_Right, Qt.Key_D):
            self.move("right")
        elif event.key() == Qt.Key_Space:
            self.update_image("jump")

    def move(self, direction: str):
        assert direction in ("up", "down", "right", "left")
        speed = p.VELOCIDAD_CAMINAR
        x = speed if direction == "right" else -speed if direction == "left" else 0
        y = speed if direction == "down" else -speed if direction == "up" else 0
        self.update_image(direction)
        self.item.moveBy(x, y)
        # TODO: Add timeout
        # self.update_image("still")

    def update_image(self, state: str):
        assert state in ("up", "down", "right", "left", "jump", "still")
        if state != "still":
            self.image = QPixmap(
                f"sprites/Personajes/{self.color}/{state}_{choice(range(1, 4))}.png"
            )
        else:
            self.image = QPixmap(f"sprites/Personajes/{self.color}/{state}.png")
        self.image = self.image.scaledToHeight(50)
        self.item.setPixmap(self.image)

    def car_collision(self):
        lct = self.last_collision_time
        time_now = datetime.now()
        if lct is None or (time_now - lct > timedelta(seconds=1)):
            self.player.lifes -= 1
            self.last_collision_time = time_now
            self.to_start()


class RoadGameView(QObject):
    collision_signal = pyqtSignal()

    def __init__(
        self,
        scene: QGraphicsScene,
        scene_x: int,
        scene_y: int,
        scene_width: int,
        scene_height: int,
        level: str,
    ):
        super().__init__()

        self.scene = scene
        self.scene_x: int = scene_x
        self.scene_y: int = scene_y
        self.scene_width: int = scene_width
        self.scene_height: int = scene_height
        self.level: str = level
        self.player: Optional[QGraphicsPixmapItem] = None
        self.init_road()

    def init_road(self):
        self.game = RoadGame(self.level)
        self.game.paint_car_signal.connect(self.spawn_car)
        self.cars: list[tuple[Car, QGraphicsPixmapItem]] = []

        self.car_move_frequency = 50  # ms
        assert 2 <= self.car_move_frequency <= 100
        self.car_mover = QTimer()
        self.car_mover.timeout.connect(self.move_cars)
        self.car_mover.start(self.car_move_frequency)

    def get_car_starting_position(self, level: str, lane: int, direction: str):
        lane_positions: dict[tuple[str, int, str], tuple[int, int]] = {
            ("up", 0, "right"): (self.scene_x + -120, self.scene_y + 27),
            ("up", 1, "right"): (self.scene_x + -120, self.scene_y + 27 + 45),
            ("up", 2, "right"): (self.scene_x + -120, self.scene_y + 27 + 90),
            ("up", 0, "left"): (self.scene_x + 150 + 900, self.scene_y + 25),
            ("up", 1, "left"): (self.scene_x + 150 + 900, self.scene_y + 25 + 45),
            ("up", 2, "left"): (self.scene_x + 150 + 900, self.scene_y + 25 + 90),
        }

        x, y = lane_positions[("up", lane, direction)]
        # Use the symmetry of the first road to calculate the second one
        return x, y if level == "up" else y + 362

    def spawn_car(self, car: Car):
        # Choose a color
        color = choice(p.COLORES_AUTOS)
        # Load image
        img = QPixmap(f"sprites/Mapa/autos/{color}_{car.direction}.png").scaledToHeight(
            40
        )
        car_item = QGraphicsPixmapItem(img)
        # Get starting position from our dictionary
        x, y = self.get_car_starting_position(car.level, car.lane, car.direction)
        car_item.setOffset(x, y)
        # Add to the scene
        self.scene.addItem(car_item)
        # Add to the list of cars
        self.cars.append((car, car_item))

    def move_cars(self):
        def left_scene(car: Car, item: QGraphicsPixmapItem):
            # TODO: Implement car removal for performance reasons.
            return False

        for car, item in self.cars:
            item.moveBy(-7 if car.direction == "left" else 7, 0)
            if self.player is not None and item.collidesWithItem(self.player):
                self.collision_signal.emit()
            if left_scene(car, item):
                self.scene.removeItem(item)
                self.cars.remove((car, item))


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
