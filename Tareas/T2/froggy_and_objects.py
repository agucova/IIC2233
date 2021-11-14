import sys
from datetime import datetime, timedelta
from random import choice, randint
from typing import Optional

from PyQt5.Qt import Qt
from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from PyQt5.QtGui import QKeyEvent, QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QGraphicsView

import parametros as p
from state import Processor


class FroggyView(QObject):
    """Handles displaying Froggy inside the scene, as well as
    communicating collisions and other events to the back-end."""

    pause_or_unpause_signal = pyqtSignal()
    # Sent when the user won the level
    level_finished_signal = pyqtSignal()

    def __init__(
        self,
        processor: Processor,
        scene: QGraphicsScene,
        view: QGraphicsView,
        scene_x: int,
        scene_y: int,
        scene_width: int,
        scene_height: int,
    ):
        super().__init__()
        # Connect main processor
        self.processor = processor

        # Save scene parameters
        self.scene = scene
        self.view = view
        self.scene_x = scene_x
        self.scene_y = scene_y
        self.scene_width = scene_width
        self.scene_height = scene_height

        # Choose a froggy color
        self.color = choice(p.COLORES_PERSONAJE)

        # Check if Froggy was properly clicked
        self.pressed_once = False

        # Spawn froggy
        self.spawn_froggy()

        # Give it a direction
        self.direction = "still"

        # Save the last collision time to avoid multiple collisions
        self.last_collision_time: Optional[datetime] = None

        # Save keys being pressed
        self.pressed_keys = set()
        self.last_combo: datetime = datetime.now()

        # Combo clock
        self.combo_clock = QTimer()
        self.combo_clock.timeout.connect(self.combo_clock_tick)
        self.combo_clock.start(3)

    def spawn_froggy(self):
        """Do all the graphic heavylifting to spawn froggy!"""
        # Load initial still image
        self.image = QPixmap(f"sprites/Personajes/{self.color}/still.png")
        self.image = self.image.scaledToHeight(50)
        self.item = QGraphicsPixmapItem(self.image)
        self.item.setZValue(1)
        # Place at the bottom
        self.item.setOffset(self.scene_x + 500, self.scene_y + 500)
        # Add to the scene
        self.scene.addItem(self.item)
        # Connect to our key handler
        self.item.setFlags(self.item.GraphicsItemFlag.ItemIsFocusable)
        self.scene.setFocusItem(self.item)
        self.item.keyPressEvent = self.key_press_handler
        self.item.keyReleaseEvent = self.key_release_handler

        self.item.mousePressEvent = (
            lambda event: self.processor.level_start_signal.emit()
        )

    def send_to_start(self):
        """Sends froggy to its starting place."""
        self.item.setOffset(self.scene_x + 500, self.scene_y + 500)
        self.item.setPos(0, 0)

    def key_press_handler(self, event: QKeyEvent):
        self.pressed_once or self.processor.level_start_signal.emit()
        if not self.processor.is_paused:
            self.pressed_keys.add(event.key())
            if event.key() in (Qt.Key_Up, Qt.Key_W):
                self.move("up")
            elif event.key() in (Qt.Key_Down, Qt.Key_S):
                self.move("down")
            elif event.key() in (Qt.Key_Left, Qt.Key_A):
                self.move("left")
            elif event.key() in (Qt.Key_Right, Qt.Key_D):
                self.move("right")
            elif event.key() == Qt.Key_Space:
                self.move("jump")
        if event.key() == Qt.Key_P:
            self.pause_or_unpause_signal.emit()

    def key_release_handler(self, event: QKeyEvent):
        if event.key() in self.pressed_keys:
            self.pressed_keys.remove(event.key())

    def combo_clock_tick(self):
        """Detects combo keys and applies their cheatcode effects."""
        if not self.pressed_keys:
            return
        if {Qt.Key_V, Qt.Key_I, Qt.Key_D}.issubset(self.pressed_keys):
            now = datetime.now()
            if now - self.last_combo >= timedelta(seconds=1):
                self.last_combo = now
                self.processor.lives_left += p.VIDAS_TRAMPA
        elif {Qt.Key_N, Qt.Key_I, Qt.Key_V}.issubset(self.pressed_keys):
            now = datetime.now()
            if (
                now - self.last_combo >= timedelta(seconds=1)
                and not self.processor.is_paused
            ):
                self.last_combo = now
                self.level_finished_signal.emit()

    def is_inside_view(self):
        return self.item in self.view.items(self.view.viewport().rect())

    def move(self, direction: str):
        if not self.processor.is_paused:
            assert direction in ("up", "down", "right", "left", "jump")
            if not direction == "jump":
                speed = p.VELOCIDAD_CAMINAR
                x = (
                    speed
                    if direction == "right"
                    else -speed
                    if direction == "left"
                    else 0
                )
                y = speed if direction == "down" else -speed if direction == "up" else 0
                self.set_direction(direction)
            else:
                speed = p.PIXELES_SALTO
                direction = self.direction
                x = (
                    speed
                    if direction == "right"
                    else -speed
                    if direction == "left"
                    else 0
                )
                y = speed if direction == "down" else -speed if direction == "up" else 0

            self.set_direction(direction)
            self.item.moveBy(x, y)

            # Check if the player got to the top
            is_finished = self.check_finished_round()

            # Prevent player from going outside the screen
            if not self.is_inside_view() and not is_finished:
                self.processor.lives_left -= 1
                self.send_to_start()

    def set_direction(self, direction: str):
        if not self.processor.is_paused:
            assert direction in ("up", "down", "right", "left", "jump", "still")
            self.update_image(direction)
            self.direction = direction

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

    def check_finished_round(self):
        if self.item.y() <= -self.scene_height + 40 and self.processor.alive:
            self.level_finished_signal.emit()
            return True
        return False

    def collision(self):
        if not self.processor.is_paused:
            lct = self.last_collision_time
            time_now = datetime.now()
            if lct is None or (time_now - lct > timedelta(seconds=1)):
                self.processor.lives_left -= 1
                self.last_collision_time = time_now
                self.send_to_start()


class SpecialObjectsView(QObject):
    # Signal for communicating collisions to the processor
    # argument correspond to the type of object that collided
    collision_signal = pyqtSignal(str)

    def __init__(
        self,
        processor: Processor,
        player: QGraphicsPixmapItem,
        scene: QGraphicsScene,
        scene_x: int,
        scene_y: int,
        scene_width: int,
        scene_height: int,
    ):
        super().__init__()
        self.processor = processor
        self.player = player
        self.scene = scene
        self.scene_x: int = scene_x
        self.scene_y: int = scene_y
        self.scene_width: int = scene_width
        self.scene_height: int = scene_height

        # Holds all the objects in the scene
        self.items: list[tuple[QGraphicsPixmapItem, str]] = []

        # Object spawn clock
        self.object_spawn_clock = QTimer()
        self.object_spawn_clock.timeout.connect(self.spawn_object)

        # Object collision clock
        self.object_collision_clock = QTimer()
        self.object_collision_clock.timeout.connect(self.check_collisions)

        # Start clocks
        self.object_spawn_clock.start(p.TIEMPO_OBJETO * 1000)
        self.object_collision_clock.start(100)

    def spawn_object(self):
        """Spawns a random special object in the scene."""
        if not self.processor.is_paused:
            # Choose a type
            object_type = choice(("Calavera", "Corazon", "Moneda", "Reloj"))
            # Choose a position
            x = randint(self.scene_x, self.scene_x + self.scene_width)
            y = randint(self.scene_y, self.scene_y + self.scene_height)
            # Load image
            img = QPixmap(f"sprites/Objetos/{object_type}.png").scaledToHeight(50)
            item = QGraphicsPixmapItem(img)
            # Place on the scene and save to self.items
            item.setOffset(x, y)
            self.scene.addItem(item)
            self.items.append((item, object_type))

    def check_collisions(self):
        """Check for player collisions with special objects."""
        if not self.processor.is_paused:
            for item, object_type in self.items:
                if self.player is not None and item.collidesWithItem(self.player):
                    self.collision_signal.emit(object_type)
                    self.scene.removeItem(item)
                    self.items.remove((item, object_type))

    def clear_objects(self):
        """Removes all the objects from the scene."""
        for item, _ in self.items:
            self.scene.removeItem(item)
        self.items.clear()
