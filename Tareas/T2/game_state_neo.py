from __future__ import annotations

from random import choice
from typing import NamedTuple, Optional

from PyQt5.QtCore import QObject, QTimer, pyqtSignal

import parametros as p


class GameState(NamedTuple):
    # Main game variables
    alive: bool
    lives_left: int
    level: int
    total_score: int
    coins: int
    is_paused: bool
    # Level specific
    level_score: int
    remaining_time: int
    # Game speeds
    car_speed: int
    log_speed: int


class Processor(QObject):
    """
    Stores the game state and coordinates the logic flow to the front-end through signals.
    """

    # Signals
    # Sent when the game state changes
    # Specifically lifes left, score, coins and time left (stored in the NamedTuple)
    parameter_change_signal = pyqtSignal(GameState)
    # Sent when a level starts and movement is unlocked
    level_start_signal = pyqtSignal()
    # Sent when the game is over because the time run out or the player lost all lifes
    game_over_signal = pyqtSignal(GameState)

    def __init__(self, username: str) -> None:
        super().__init__()
        # Store username for saving later
        # TODO: Assert validity.
        self.username = username

        # Internal game clock
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.elapsed_time = 0

        # Internal game state
        self._lifes_left = p.VIDAS_INICIO
        self._coins, self.level = 0, 0
        self.scores: list[int] = [0]
        self.alive = True

        # Precompute difficulties
        self.precompute_difficulties()

    @property
    def state(self):
        """Return a GameState object, used for communication with the front-end."""
        gstate = GameState(
            self.alive,
            self.lives_left,
            self.level,
            self.total_score,
            self.coins,
            self.is_paused,
            self.level_score,
            self.remaining_time,
            self.car_speed,
            self.log_speed,
        )
        return gstate

    @property
    def lives_left(self) -> int:
        return self._lifes_left if self._lifes_left >= 0 else 0

    @lives_left.setter
    def lives_left(self, value: int) -> None:
        self._lifes_left = value
        self.parameter_change_signal.emit(self.state)
        if value == 0:
            self.alive = False
            self.game_over_signal.emit(self.state)

    @property
    def remaining_time(self) -> int:
        return self.round_duration - self.elapsed_time

    @property
    def total_score(self) -> int:
        return sum(self.scores)

    @total_score.setter
    def total_score(self, value: int) -> None:
        print(
            "[WARNING] Modifying score through total_score. level_score should be used."
        )
        self.scores[self.level] = value

    @property
    def level_score(self) -> int:
        try:
            return self.scores[self.level]
        except IndexError:
            assert (
                len(self.scores) == self.level
            ), "A level was skipped when reading scores."
            self.scores.append(0)
            return 0

    @level_score.setter
    def level_score(self, value: int) -> None:
        try:
            self.scores[self.level] = value
        except IndexError:
            assert (
                len(self.scores) == self.level
            ), "A level was skipped when setting scores."
            self.scores.append(value)

    @property
    def coins(self) -> int:
        return self._coins

    @property
    def round_duration(self) -> int:
        return round(self.difficulties[self.level]["round_duration"])

    @property
    def car_speed(self) -> int:
        return round(self.difficulties[self.level]["car_speed"])

    @property
    def log_speed(self) -> int:
        return round(self.difficulties[self.level]["log_speed"])

    @log_speed.setter
    def log_speed(self, value: int) -> None:
        # Implemented for the skulls.
        self.difficulties[self.level]["log_speed"] = value

    @property
    def is_paused(self) -> bool:
        return not self.timer.isActive()

    @is_paused.setter
    def is_paused(self, value: bool) -> None:
        if value:
            self.timer.stop()
        else:
            self.timer.start(1000)

    def pause(self) -> None:
        """Pause the game. Convenience method for signals."""
        self.is_paused = True

    def pause_or_unpause(self) -> None:
        """
        Pause or unpause the game. Convenience method for signals.
        """
        self.is_paused = not self.is_paused

    def play_or_resume(self) -> None:
        """Resume playing or start playing by restarting the game clock.
        Convenience method for signals."""
        self.is_paused = False

    def next_level(self):
        """Do a state transition to the next level."""
        self.level += 1
        self.level_score = 0

    def tick(self) -> None:
        """
        The game clock.
        """
        self.elapsed_time += 1
        self.parameter_change_signal.emit(self.state)
        if self.remaining_time == 0:
            self.alive = False
            self.game_over_signal.emit(self.state)

    def precompute_difficulties(self) -> None:
        """
        Precompute the difficulty of the game for each level.
        """
        self.difficulties: list[dict[str, float]] = []
        round_duration: float = p.DURACION_RONDA_INICIAL
        car_speed: float = p.VELOCIDAD_AUTOS
        log_speed: float = p.VELOCIDAD_TRONCOS

        self.difficulties.append(
            {
                "round_duration": round_duration,
                "car_speed": car_speed,
                "log_speed": log_speed,
            }
        )

        for _ in range(100):
            round_duration = p.PONDERADOR_DIFICULTAD * round_duration
            car_speed = car_speed * (2 / (1 + p.PONDERADOR_DIFICULTAD))
            log_speed = log_speed * (2 / (1 + p.PONDERADOR_DIFICULTAD))
            self.difficulties.append(
                {
                    "round_duration": round_duration,
                    "car_speed": car_speed,
                    "log_speed": log_speed,
                }
            )


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
    # Signal to be sent when a car needs to spawn on the view
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


# if __name__ == "__main__":
#     # For testing
#     p = Processor("agucova")
#     print(p.state)
