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

from game_state import Car, Froggy, RoadGame
import parametros as p


class FroggyView(QObject):
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
        self.item.mousePressEvent = lambda event: self.player.game_started_signal.emit()

    def to_start(self):
        self.item.setOffset(self.scene_x + 500, self.scene_y + 500)
        self.item.setPos(0, 0)

    def key_press_handler(self, event: QKeyEvent):
        self.pressed_once or self.player.game_started_signal.emit()
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
        for car, item in self.cars:
            item.moveBy(
                -self.game.speed if car.direction == "left" else self.game.speed, 0
            )
            # Emit collisions using the collision detection system of the scene
            if self.player is not None and item.collidesWithItem(self.player):
                self.collision_signal.emit()
