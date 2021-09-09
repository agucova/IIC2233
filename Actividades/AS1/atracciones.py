from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union
import parametros as p
from personas import Adulto, Nino


# Recuerda definir esta clase como abstracta!
class Atraccion(ABC):
    def __init__(self, nombre, capacidad):
        # No modificar
        self.nombre = nombre
        self.capacidad_maxima = capacidad
        self.fila = []

    def ingresar_persona(self, persona):
        # No modificar
        print(f"** {persona.nombre} ha entrado a la fila de {self.nombre}")
        self.fila.append(persona)
        persona.esperando = True

    def nueva_ronda(self):
        # No modificar
        personas_ingresadas = 0
        lista_personas = []
        while personas_ingresadas < self.capacidad_maxima and self.fila:
            lista_personas.append(self.fila.pop(0))

        self.iniciar_juego(lista_personas)

        for persona in lista_personas:
            persona.actuar()

    def iniciar_juego(self, personas):
        # No modificar
        for persona in personas:
            print(f"*** {persona.nombre} jugó esta ronda")
            persona.esperando = False
            self.efecto_atraccion(persona)
        print()

    @abstractmethod
    def efecto_atraccion(self, persona):
        # No modificar
        pass

    def __str__(self):
        return f"Atraccion {self.nombre}"


# Recuerda completar la herencia!
class AtraccionFamiliar(Atraccion):
    def __init__(self, nombre: str, capacidad: int):
        super().__init__(nombre, capacidad)
        self.efecto_salud: int = p.SALUD_FAMILIA
        self.efecto_felicidad: int = p.FELICIDAD_FAMILIA

    def efecto_atraccion(self, persona):
        persona.felicidad += self.efecto_felicidad
        persona.salud -= self.efecto_salud


# Recuerda completar la herencia!
class AtraccionAdrenalinica(Atraccion):
    def __init__(self, nombre: str, capacidad: int, salud_necesaria: int):
        super().__init__(nombre, capacidad)
        self.salud_necesaria: int = salud_necesaria
        self.efecto_salud: int = p.SALUD_ADRENALINA
        self.efecto_felicidad: int = p.FELICIDAD_ADRENALINA

    def efecto_atraccion(self, persona):
        if persona.salud > self.salud_necesaria:
            persona.felicidad += self.efecto_felicidad
            persona.salud -= self.efecto_salud
        else:
            print(f"*** {persona.nombre} fue bajado del juego por su salud")
            persona.salud -= p.SALUD_ADRENALINA // 2
            persona.felicidad -= p.FELICIDAD_ADRENALINA // 2


# Recuerda completar la herencia!


class AtraccionAcuatica(AtraccionFamiliar):
    def __init__(self, nombre, capacidad):
        super().__init__(nombre, capacidad)
        self.efecto_felicidad = p.FELICIDAD_ACUATICA

    def ingresar_persona(self, persona: Union[Nino, Adulto]):
        if persona.tiene_pase:
            super().ingresar_persona(persona)
        else:
            print(f"*** {persona.nombre} no puede entrar sin su pase de movilidad.")


# Recuerda completar la herencia!
class MontanaAcuatica(AtraccionAdrenalinica, AtraccionAcuatica):
    def __init__(
        self, nombre: str, capacidad: int, salud_necesaria: int, dificultad: int
    ):
        super().__init__(nombre, capacidad, salud_necesaria)
        self.dificultad: int = dificultad

    def iniciar_juego(self, personas: list[Union[Nino, Adulto]]):
        for persona in personas:
            print(f"*** {persona.nombre} ha jugado en {self.nombre}")
            persona.esperando = False
            if persona.salud <= self.salud_necesaria * self.dificultad:
                print(f"*** {persona.nombre} se cayó del agua y perdió su pase")
                persona.tiene_pase = False
            self.efecto_atraccion(persona)
