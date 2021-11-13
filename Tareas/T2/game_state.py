from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import parametros as p
from PyQt5.QtCore import QTimer, QObject, pyqtSignal
from random import choice


class Froggy(QObject):
    # Signals
    updated_lifes_signal = pyqtSignal(str)
    updated_level_signal = pyqtSignal(str)
    updated_score_signal = pyqtSignal(str)
    updated_coins_signal = pyqtSignal(str)
    updated_time_signal = pyqtSignal(str)
    game_over_signal = pyqtSignal()

    def __init__(self, username: str):
        super().__init__()

        self.username = username

        self._lifes: int = p.VIDAS_INICIO
        self._level = 1
        self._score = 0
        self._coins = 0
        self._time_left = 60

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value: int):
        self._level = value
        self.updated_level_signal.emit(str(value))

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, value: int):
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
            self.game_over_signal.emit()

    @property
    def time_left(self):
        return self._time_left

    @time_left.setter
    def time_left(self, value):
        self._time_left = value
        self.updated_time_signal.emit(str(value))


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
