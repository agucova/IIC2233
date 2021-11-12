from dataclasses import dataclass
import parametros as p
from __future__ import annotations


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


class Auto:
    def __init__(self):
        self.posicion = (0, 0)


class Carretera:
    def __init__(self):
        self.periodo_autos = p.PERIODO_AUTOS
        self.autos: list[Auto] = []
