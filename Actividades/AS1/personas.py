from abc import ABC, abstractmethod
from random import randint
from typing import List


# Recuerda definir esta clase como abstracta!
class Persona(ABC):
    def __init__(self, nombre, edad, tiene_pase, juegos):
        # No modificar
        self.nombre = nombre
        self.edad = edad
        self.tiene_pase = tiene_pase
        self.juegos = juegos
        self.esperando = False
        self.__salud = None
        self.__felicidad = None

        self.definir_estados()

    @property
    def felicidad(self):
        # No modificar
        return self.__felicidad

    @felicidad.setter
    def felicidad(self, valor):
        # No modificar
        if valor <= 0:
            valor = 0
            print(", está muy triste", end="")
        self.__felicidad = valor

    @property
    def salud(self):
        # No modificar
        return self.__salud

    @salud.setter
    def salud(self, valor):
        # No modificar
        if valor <= 0:
            valor = 0
            print(", se siente muy mal", end="")
            if randint(0, 3) < 1:
                print(" y vomitó encima de todos los que estaban en el juego!")
            else:
                print(".")
        self.__salud = valor

    def revision_juegos(self) -> bool:
        return not self.esperando and len(self.juegos) >= 1

    def siguiente_juego(self) -> str:
        return self.juegos.pop(0)

    # --------------
    # Completa los métodos abstractos aqui
    # --------------

    @abstractmethod
    def definir_estados(self):
        pass

    @abstractmethod
    def actuar(self):
        pass

    def __str__(self):
        return (
            f"Soy {self.nombre}, un {self.__class__.__name__} de edad {self.edad}. "
            f"Pase de batalla: {self.tiene_pase}"
        )


# Recuerda completar la herencia!
class Adulto(Persona):
    def __init__(
        self, nombre: str, edad: int, tiene_pase: bool, juegos: List, dinero: int
    ):
        self.dinero: int = dinero
        super().__init__(nombre, edad, tiene_pase, juegos)

    # --------------
    # Completa el método abstracto aquí
    # --------------

    def definir_estados(self):
        assert self.dinero
        self.salud: int = self.edad * randint(1, 3)
        self.felicidad: int = self.edad * self.dinero

    def actuar(self):
        # No modificar
        if self.salud == 0:
            print("Toi muy viejo pa estos trotes, nos vimos")
            self.juegos = []
        elif self.felicidad < 15 and randint(0, 6) < 5:
            print("Este último juego me dejo con ganas de comer")
            print(f"{self.nombre} se comió su hamburguesa favorita y quedó feliiiiz")
            self.felicidad += 15
            self.salud += 1
        else:
            if self.juegos:
                print(
                    f"Una lavadita de cara y a seguir disfrutando, vamos por {self.juegos[0]}"
                )
                self.salud += randint(2, 15)
            else:
                print(
                    f"Nos vemoooo, tuvo bueno el dia, aunque mi salud quedo en {self.salud}"
                )


# Recuerda completar la herencia!
class Nino(Persona):
    def __init__(
        self, nombre: str, edad: int, tiene_pase: bool, juegos: List, padre: str
    ):
        self.padre = padre
        super().__init__(nombre, edad, tiene_pase, juegos)

    # --------------
    # Completa el método abstracto aquí
    # --------------

    def definir_estados(self):
        self.salud: int = self.edad * randint(1, 5)
        self.felicidad: int = len(self.padre) * 10

    def actuar(self):
        # No modificar
        if self.salud == 0 and randint(0, 2):
            print("Toi muerto, pero un colado y seguimos")
            self.salud += int(self.edad / 2)
        elif self.felicidad < 10 and randint(0, 7) < 5:
            print("Este último juego me dejo con ganas de comer")
            print(
                f"{self.nombre} se comió una KrakenBurguer y quedo listo para segui con su día"
            )
            self.felicidad += 15
            self.salud += 1
        else:
            if randint(0, 5) < 2:
                print("ESTÁ SIENDO UN DÍA FANTÁSTICOO, YUPIIII")
                self.felicidad += randint(15, 25)
            else:
                print(f"Esto de bailar no es lo mio, todos se rien de mi")
                self.felicidad -= randint(12, 16)
