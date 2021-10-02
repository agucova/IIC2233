from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
import parameters as p
from random import choice, random
from typing import Optional


class Tributo:
    def __init__(
        self,
        nombre: str,
        distrito: str,
        edad: int,
        _vida: int,
        energia: int,
        agilidad: int,
        fuerza: int,
        ingenio: int,
        popularidad: int,
    ):
        self.nombre = nombre
        self.distrito = distrito
        self.edad = edad
        assert 0 <= _vida <= 100
        self._vida = _vida
        assert 0 <= energia <= 100
        self.energia = energia
        self.agilidad = agilidad
        self.ingenio = ingenio
        self.popularidad = popularidad
        self.fuerza = fuerza

        self.esta_vive = True
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
                self.esta_vive = False
                self._vida = 0
                print(f"El tributo {self.nombre} ha muerto.")
            else:
                self._vida = max(valor, 100)

        def atacar(
            self, tributo: Tributo
        ) -> bool:  # TODO: Agregar logica de ataque fallido, cansancio?
            """Ataca a otro tribute. Retorna si es que el otro tribute a muerto en el ataque."""
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
            print(
                f"{self.nombre} ha atacado a {tributo.nombre}, quitándole {dano} de vida."
            )

            return not tributo.esta_vive

        def utilizar_objeto(self, objeto: Objeto, arena: Arena):
            """Utiliza el objeto entregado de la mochila del tributo. Recibe la arena para verificar atributos de riesgo."""
            assert objeto in self.mochila
            objeto.entregar_beneficio(self, arena)
            self.mochila.remove(objeto)
            print(f"{self.nombre} ha utilizado {objeto.nombre}.")

        def pedir_objeto(self, objetos: list[Objeto]) -> Optional[Objeto]:
            """Solicita un objeto a les patrocinadores, costándole popularidad al tributo. Recibe la lista de objetos existentes."""
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
            """Realiza una acción heroíca"""
            if self.energia >= p.ENERGIA_ACCION_HEROICA:
                self.energia -= p.ENERGIA_ACCION_HEROICA
                # TODO: Agregar aleatoridad?
                self.popularidad += p.POPULARIDAD_ACCION_HEROICA
                print(
                    f"{self.nombre} ha hecho una acción heroíca, impresionando a les patrocinadores."
                )
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
        assert len(eventos) == 3
        self.eventos = eventos

    @abstractmethod
    def calcular_dano(self, evento: Evento):
        pass


class Playa(Ambiente):
    def calcular_dano(self, evento: Evento):
        return max(
            [
                5,
                (0.4 * p.HUMEDAD_PLAYA + 0.2 * p.VELOCIDAD_VIENTOS_PLAYA + evento.dano)
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

    # Usamos un staticmethod cosa de que pueda ser utilizado incluso sin inicializar en el caso de Especial.
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
    def __init__(
        self,
        nombre: str,
        dificultad: str,
        riesgo: float,
        ambientes: list[Ambiente],
    ):
        self.nombre = nombre
        assert dificultad in ("principiante", "intermedio", "avanzado")
        self.dificultad = dificultad
        assert 0 <= riesgo <= 1
        self.riesgo = riesgo
        assert len(ambientes) == 3
        self.ambientes: list[Ambiente] = ambientes

        self.jugadores_cargados = False
        self.i_ambiente = 0

        @property
        def ambiente(self) -> Ambiente:
            return self.ambientes[self.i_ambiente]

        @property
        def jugadores(self) -> list[Tributo]:
            return self.tributos + [self.jugador]

        def cargar_jugadores(self, jugador: Tributo, tributos: list[Tributo]):
            assert len(tributos) > 0
            assert jugador not in tributos
            assert not self.jugadores_cargados

            self.jugador = jugador
            self.tributos: list[Tributo] = tributos
            self.jugadores_cargados = True

        def ejecutar_evento(self) -> bool:
            """Ejecuta un evento del ambiente probabilísticamente en base a los parámetros del juego. Retorna si es que se ejecutó un evento."""
            hay_evento = random() < p.PROBABILIDAD_EVENTO

            if hay_evento:
                evento = choice(self.ambiente.eventos)
                dano = evento.calcular_dano()
                print(f"Se ha producido un evento: {evento.nombre}.")
                for tributo in self.jugadores:
                    tributo.vida -= dano

            return hay_evento

        def realizar_encuentros(self):
            """Realiza los encuentros entre tributos en una partida."""
            assert len(self.tributos) > 0

            n_encuentros = self.riesgo * len(self.jugadores) // 2
            for _ in range(n_encuentros):
                t1: Tributo = choice(self.jugadores)
                while True:
                    t2: Tributo = choice(self.jugadores)
                    if t1 != t2:
                        break

                assert t1.esta_vive and t2.esta_vive
                if t1 != t2:
                    muerte = t1.atacar(t2)
                    if muerte:
                        self.tributos.remove(t2)
