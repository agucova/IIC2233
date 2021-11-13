from __future__ import annotations

import parametros as p
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QObject, pyqtSignal
from random import choice


class Froggy:
    def __init__(self, usuario: str):
        self.vida: int = p.VIDA_INICIO
        self.posicion = (0, 0)
        self.usuario = usuario

    def mover(self, direccion: str):
        assert direccion in ["arriba", "abajo", "izquierda", "derecha"]

        if direccion == "arriba":
            self.posicion = (self.posicion[0], self.posicion[1] - 1)
        elif direccion == "abajo":
            self.posicion = (self.posicion[0], self.posicion[1] + 1)
        elif direccion == "izquierda":
            self.posicion = (self.posicion[0] - 1, self.posicion[1])
        elif direccion == "derecha":
            self.posicion = (self.posicion[0] + 1, self.posicion[1])


class Game:
    def __init__(self) -> None:
        self.froggy: Froggy = None


class RoadGame(QObject):
    paint_car_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.car_spawn_period = p.PERIODO_AUTOS * 1000
        self.car_spawner = QTimer()
        self.car_spawner.timeout.connect(self.spawn_car)
        self.car_spawner.start(self.car_spawn_period)

    def spawn_car(self):
        print(f"[DEBUG] Spawned car.")
        self.paint_car_signal.emit(choice(("left", "right")))
