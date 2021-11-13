from __future__ import annotations

from dataclasses import dataclass
from operator import le
from typing import Optional

import parametros as p
from PyQt5.QtCore import QTimer, QObject, pyqtSignal
from random import choice


class Procesador(QObject):
    # Signals
    updated_lifes_signal = pyqtSignal(str)
    level_ended_signal = pyqtSignal()
    updated_score_signal = pyqtSignal(str)
    updated_coins_signal = pyqtSignal(str)
    updated_time_signal = pyqtSignal(str)
    game_started_signal = pyqtSignal()

    def __init__(self, username: str):
        super().__init__()

        self.username = username

        self._lifes: int = p.VIDAS_INICIO
        self._level = 1
        self._score = 0
        self.last_score = 0
        self._coins = 0
        self._time_left = 60
        self._car_speed = p.VELOCIDAD_AUTOS
        self._log_speed = p.VELOCIDAD_TRONCOS
        self.timer = QTimer()
        self.timer.timeout.connect(self.handle_time_left)
        self.game_started_signal.connect(self.start)

    # Start signal
    def start(self):
        self._time_left = 60
        self.timer.start(1000)

    def pause(self):
        self.timer.stop()

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value: int):
        assert value == self._level + 1
        self._level = value
        self._car_speed *= 2 / (1 + p.PONDERADOR_DIFICULTAD)
        self._log_speed *= 2 / (1 + p.PONDERADOR_DIFICULTAD)

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, value: int):
        self.last_score = self._score
        self._score = value
        self.updated_score_signal.emit(str(value))

    @property
    def coins(self) -> int:
        return self._coins

    @coins.setter
    def coins(self, value: int):
        self._coins = value
        self.updated_coins_signal.emit(str(value))

    @property
    def lifes(self):
        return self._lifes

    @lifes.setter
    def lifes(self, lifes):
        self.updated_lifes_signal.emit(str(lifes))
        self._lifes = lifes
        if self._lifes <= 0:
            self.pause()
            self.update_score()
            self.level_ended_signal.emit()

    @property
    def time_left(self):
        return self._time_left

    @time_left.setter
    def time_left(self, value):
        self._time_left = value
        self.updated_time_signal.emit(str(value))

    def update_score(self):
        self.score = (self.lifes * 100 + self.time_left * 50) * self.level

    def handle_time_left(self):
        self.time_left -= 1
        if self.time_left == 0:
            self.pause()
            self.update_score()
            self.level_ended_signal.emit()


class Car:
    def __init__(self, lane, direction, level):
        assert lane in (0, 1, 2)
        assert direction in ("left", "right")
        assert level in ("up", "down")

        self.lane: int = lane
        self.direction: str = direction
        self.position: Optional[tuple[int, int]] = None
        self.level: str = level


class RoadGame(QObject):
    paint_car_signal = pyqtSignal(Car)

    def __init__(self, level: str):
        assert level in ("up", "down")

        super().__init__()
        self.car_spawn_period = 1000 * p.PERIODO_AUTOS
        self.car_spawner = QTimer()
        self.car_spawner.timeout.connect(self.spawn_car)
        self.car_spawner.start(self.car_spawn_period)

        self.speed = p.VELOCIDAD_AUTOS

        self.level = level
        # The directions of each lane are chosen randomly on each game
        self.lane_directions = [choice(("left", "right")) for _ in range(3)]
        self.lanes: list[list[Car]] = [[], [], []]

    def spawn_car(self):
        lane = choice((0, 1, 2))
        direction = self.lane_directions[lane]
        car = Car(lane, direction, self.level)
        self.lanes[car.lane].append(car)

        # Ask the front-end to draw the car in the screen
        self.paint_car_signal.emit(car)
