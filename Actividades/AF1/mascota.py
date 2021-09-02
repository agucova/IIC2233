import random
import parametros as p
from comida import Comida


class Mascota:
    def __init__(
        self, nombre: str, raza: str, dueno: str, saciedad: int, entretencion: int
    ):
        self.nombre = nombre
        self.raza = raza
        self.dueno = dueno

        # Los siguientes valores están en %.
        self._saciedad = saciedad
        self._entretencion = entretencion

        self.especie = "Forma platónica de un animal"

    @property
    def saciedad(self):
        return self._saciedad

    @saciedad.setter
    def saciedad(self, nueva_saciedad):
        if nueva_saciedad > 100:
            self._saciedad = 100
        elif nueva_saciedad < 0:
            self._saciedad = 0
        else:
            self._saciedad = nueva_saciedad

    @property
    def entretencion(self):
        return self._entretencion

    @entretencion.setter
    def entretencion(self, nueva_entretencion):
        if nueva_entretencion > 100:
            self._entretencion = 100
        elif nueva_entretencion < 0:
            self._entretencion = 0
        else:
            self._entretencion = nueva_entretencion

    @property
    def satisfaccion(self):
        return self.saciedad // 2 + self.entretencion // 2

    def comer(self, comida: Comida):
        if random.random() < comida.probabilidad_vencer:
            # Comida vencida
            print(
                f"La comida {comida.nombre} estaba vencida! {self.nombre} perdió saciedad :("
            )
            self.saciedad -= comida.calorias
        else:
            print(f"{self.nombre} comió {comida.nombre}!")
            self.saciedad += comida.calorias

    def pasear(self):
        self.entretencion += p.ENTRETENCION_PASEAR
        self.saciedad += p.SACIEDAD_PASEAR

    def __str__(self):
        return f"{self.nombre} - {self.especie} ({self.raza})\nSAC: {self.saciedad}\nENT: {self.entretencion}\nSAT: {self.saciedad}"


class Perro(Mascota):
    def __init__(
        self, nombre: str, raza: str, dueno: str, saciedad: int, entretencion: int
    ):
        super().__init__(nombre, raza, dueno, saciedad, entretencion)
        self.especie = "PERRO"

    def saludar(self):
        print(f"{self.nombre} dice WOOF!")


class Gato(Mascota):
    def __init__(
        self, nombre: str, raza: str, dueno: str, saciedad: int, entretencion: int
    ):
        super().__init__(nombre, raza, dueno, saciedad, entretencion)
        self.especie = "GATO"

    def saludar(self):
        print(f"{self.nombre} maulla")


class Conejo(Mascota):
    def __init__(
        self, nombre: str, raza: str, dueno: str, saciedad: int, entretencion: int
    ):
        super().__init__(nombre, raza, dueno, saciedad, entretencion)
        self.especie = "CONEJO"

    def saludar(self):
        print(f"{self.nombre} salta en emoción")
