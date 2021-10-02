from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
import parameters as p
from random import choice
from typing import Optional


class Tributo:
    def __init__(
        self,
        nombre: str,
        distrito: str,
        edad: int,
        vida: int,
        energia: int,
        agilidad: int,
        fuerza: int,
        ingenio: int,
        popularidad: int,
    ):
        self.nombre = nombre
        self.distrito = distrito
        self.edad = edad
        assert 0 <= vida <= 100
        self._vida = vida
        assert 0 <= energia <= 100
        self.energia = energia
        self.agilidad = agilidad
        self.ingenio = ingenio
        self.popularidad = popularidad
        self.fuerza = fuerza

        self.esta_vivo = True
        self.mochila: list[Objeto] = []

        @property
        def peso(self):
            return sum(objeto.peso for objeto in self.mochila)

        @property
        def vida(self):
            return self._vida

        @vida.setter
        def vida(self, valor):
            if valor <= 0:
                self.esta_vivo = False
                self._vida = 0
                print(f"El tributo {self.nombre} ha muerto.")
            else:
                self._vida = max(valor, 100)

        def atacar(
            self, tributo: Tributo
        ):  # TODO: Agregar logica de ataque fallido, cansancio?
            dano = min(
                [
                    90,
                    max(
                        [
                            5,
                            (
                                60 * self.fuerza
                                + 40 * self.agilidad
                                + 40 * self.ingenio
                                - 30 * self.peso
                            )
                            / self.edad,
                        ]
                    ),
                ]
            )

            tributo.vida -= dano

            return dano

        def utilizar_objeto(self, objeto: Objeto, arena: Arena):
            assert objeto in self.mochila
            objeto.entregar_beneficio(self, arena)
            self.mochila.remove(objeto)

        def pedir_objeto(self, objetos: list[Objeto]) -> Optional[Objeto]:
            if self.popularidad >= p.COSTO_OBJETO:
                self.popularidad -= p.COSTO_OBJETO
                objeto = choice(objetos)
                self.mochila.append(objeto)
                return objeto
            else:
                print(
                    f"{self.nombre} no tiene suficiente popularidad para pedir un objeto."
                )
                return None

        def accion_heroica(self) -> bool:
            if self.energia >= p.ENERGIA_ACCION_HEROICA:
                self.energia -= p.ENERGIA_ACCION_HEROICA
                # TODO: Agregar aleatoridad?
                self.popularidad += p.POPULARIDAD_ACCION_HEROICA
                return True
            else:
                print(
                    f"{self.nombre} no tiene suficiente energía para hacer una acción heroica."
                )
                return False


@dataclass
class Evento:
    nombre: str
    dano: int


class Ambiente(ABC):
    def __init__(self, nombre: str, eventos: list[Evento]):
        self.nombre = nombre
        self.eventos = eventos

    @abstractmethod
    def calcular_dano(self, evento: Evento):
        pass


class Playa(Ambiente):
    def calcular_dano(self, evento: Evento):
        return max(
            [
                5,
                (0.4 * p.HUMEDAD_PLATA + 0.2 * p.VELOCIDAD_VIENTOS_PLATA + evento.dano)
                / 5,
            ]
        )


class Bosque(Ambiente):
    def calcular_dano(self, evento: Evento):
        return max(
            [
                5,
                (
                    0.2 * p.VELOCIDAD_VIENTOS_BOSQUE
                    + 0.1 * p.PRECIPITACIONES_BOSQUE
                    + evento.dano
                )
                / 5,
            ]
        )


class Montana(Ambiente):
    def calcular_dano(self, evento: Evento):
        return max(
            [
                5,
                (
                    0.1 * p.PRECIPITACIONES_MONTANA
                    + 0.3 * p.NUBOSIDAD_MONTANA
                    + evento.dano
                )
                / 5,
            ]
        )


class Objeto(ABC):
    def __init__(self, nombre: str, peso: int):
        self.nombre = nombre
        self.peso = peso

    @staticmethod
    @abstractmethod
    def entregar_beneficio(tributo: Tributo, arena: Arena):
        pass


class Consumible(Objeto):
    def __init__(self, nombre: str, peso: int):
        super().__init__(nombre, peso)
        self.tipo = "consumible"

    @staticmethod
    def entregar_beneficio(tributo: Tributo, arena: Arena):
        tributo.energia += p.AUMENTAR_ENERGIA


class Arma(Objeto):
    def __init__(self, nombre: str, peso: int):
        super().__init__(nombre, peso)
        self.tipo = "arma"

    @staticmethod
    def entregar_beneficio(tributo: Tributo, arena: Arena):
        nueva_fuerza = round(
            tributo.fuerza * (p.PONDERADOR_AUMENTAR_FUERZA * arena.riesgo + 1)
        )
        tributo.fuerza = max(min(nueva_fuerza, 100), 0)


class Especial(Objeto):
    def __init__(self, nombre: str, peso: int):
        super().__init__(nombre, peso)
        self.tipo = "especial"

    @staticmethod
    def entregar_beneficio(tributo: Tributo, arena: Arena):
        Arma.entregar_beneficio(tributo, arena)
        Consumible.entregar_beneficio(tributo, arena)
        tributo.agilidad += p.AUMENTAR_AGILIDAD
        tributo.ingenio += p.AUMENTAR_INGENIO


class Arena:
    def __init__(self, nombre: str, dificultad: str, riesgo: float):
        self.nombre = nombre
        assert dificultad in ("principiante", "intermedio", "avanzado")
        self.dificultad = dificultad
        assert 0 <= riesgo <= 1
        self.riesgo = riesgo

        self.tributos = []
        self.ambientos = []
