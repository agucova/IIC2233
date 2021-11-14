from random import choice
from typing import Optional

from PyQt5.Qt import Qt
from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from PyQt5.QtGui import QBrush, QPen, QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene

import parametros as p
from state import Car, Log, Processor, RiverGame, RoadGame


class RoadGameView(QObject):
    # Signal for communicating collisions to the Froggy View, which then communicates it
    # to the back-end processor.
    collision_signal = pyqtSignal()

    def __init__(
        self,
        scene: QGraphicsScene,
        processor: Processor,
        scene_x: int,
        scene_y: int,
        scene_width: int,
        scene_height: int,
        level: str,
    ):
        super().__init__()

        self.scene = scene
        self.processor = processor
        self.scene_x: int = scene_x
        self.scene_y: int = scene_y
        self.scene_width: int = scene_width
        self.scene_height: int = scene_height
        self.level: str = level
        self.player: Optional[QGraphicsPixmapItem] = None
        self.init_road()

    def init_road(self):
        """Initialize roads."""
        self.game = RoadGame(self.level)
        self.game.paint_car_signal.connect(self.spawn_car)
        self.cars: list[tuple[Car, QGraphicsPixmapItem]] = []

        self.car_move_frequency = 50  # ms
        assert 2 <= self.car_move_frequency <= 100
        self.car_mover = QTimer()
        self.car_mover.timeout.connect(self.move_cars)
        self.car_mover.start(self.car_move_frequency)

    def get_car_starting_position(self, level: str, lane: int, direction: str):
        """Give the starting coordinates for a car in a given lane in a certain direction."""
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
        """Spawns cars randomly on the lanes."""
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
        """Moves all the cars in the scene according to their direction."""
        speed = self.processor.car_speed
        if not self.processor.is_paused:
            for car, item in self.cars:
                item.moveBy(-speed if car.direction == "left" else speed, 0)
                # Emit collisions using the collision detection system of the scene
                if self.player is not None and item.collidesWithItem(self.player):
                    self.collision_signal.emit()


class RiverGameView(QObject):
    # Signal for communicating falling from the logs
    fall_signal = pyqtSignal()

    def __init__(
        self,
        processor: Processor,
        scene: QGraphicsScene,
        scene_x: int,
        scene_y: int,
        scene_width: int,
        scene_height: int,
    ):
        super().__init__()

        self.scene = scene
        self.processor = processor
        self.scene_x: int = scene_x
        self.scene_y: int = scene_y
        self.scene_width: int = scene_width
        self.scene_height: int = scene_height
        self.player: Optional[QGraphicsPixmapItem] = None

        self.init_river()

    def init_river(self):
        """Initialize the river."""
        self.game = RiverGame()
        self.game.paint_log_signal.connect(self.spawn_log)
        self.log_img = QPixmap(f"sprites/Mapa/elementos/tronco.png").scaledToHeight(40)
        self.logs: list[tuple[QGraphicsPixmapItem, Log]] = []
        self.game.paint_log_signal.connect(self.spawn_log)

        # River bounding box
        self.river_box = self.scene.addRect(
            0,
            565,
            30 + self.scene_width,
            89,
            QPen(Qt.NoPen),
            QBrush(Qt.NoBrush),
        )

        self.log_move_frequency = 50

        # Log movement
        self.log_move_frequency = 50  # ms
        assert 2 <= self.log_move_frequency <= 100
        self.log_mover = QTimer()
        self.log_mover.timeout.connect(self.move_logs)
        self.log_mover.start(self.log_move_frequency)

    def get_log_starting_position(self, lane: int, direction: str):
        """Give the starting coordinates for a log in a given lane in a certain direction."""
        lane_positions: dict[tuple[int, str], tuple[int, int]] = {
            (0, "right"): (self.scene_x + -120, 550),
            (1, "right"): (self.scene_x + -120, 550 + 45),
            (2, "right"): (self.scene_x + -120, 550 + 90),
            (0, "left"): (self.scene_x + 150 + 900, 550),
            (1, "left"): (self.scene_x + 150 + 900, 550 + 45),
            (2, "left"): (self.scene_x + 150 + 900, 550 + 90),
        }

        x, y = lane_positions[(lane, direction)]
        return x, y

    def spawn_log(self, log: Log):
        """Spawns logs on the river."""
        if not self.processor.is_paused:
            item = QGraphicsPixmapItem(self.log_img)
            # Get and set starting position
            x, y = self.get_log_starting_position(log.lane, log.direction)
            item.setOffset(x, y)
            # Place in the scene and save in the list
            self.scene.addItem(item)
            self.logs.append((item, log))

    def move_logs(self):
        """Moves all the logs in the scene according to their direction."""
        if self.player is None:
            return
        speed = self.processor.log_speed
        if not self.processor.is_paused:
            player_floating_in_log = False
            for item, log in self.logs:
                item.moveBy(-speed if log.direction == "left" else speed, 0)
                # Move player with logs
                if item.collidesWithItem(self.player) and not player_floating_in_log:
                    self.player.moveBy(-speed if log.direction == "left" else speed, 0)
                    player_floating_in_log = True

            if (
                self.river_box.collidesWithItem(self.player)
                and not player_floating_in_log
            ):
                self.fall_signal.emit()
