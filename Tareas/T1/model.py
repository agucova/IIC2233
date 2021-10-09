from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from random import choice, random

import parameters as p


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
    def vida(self, valor: int):
        if valor <= 0:
            self.esta_vive = False
            self._vida = 0
            print(f"El tributo {self.nombre} ha muerto.")
        else:
            self._vida = min(max(valor, 0), 100)

    def atacar(self, tributo: Tributo, es_encuentro: bool = False) -> bool:
        """Ataca a otro tributo. Si recibe es_encuentro, no se resta energía del tributo.
        Retorna si es que el otro tribute a muerto en el ataque."""
        if (self.energia >= p.ENERGIA_ATACAR) or es_encuentro:
            self.energia -= p.ENERGIA_ATACAR if not es_encuentro else 0
            dano = round(
                min(
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
            )

            tributo.vida -= dano
            if tributo.esta_vive:
                print(
                    f"{self.nombre} ha atacado a {tributo.nombre}, quitándole {dano} de vida."
                )
                return False
            else:
                self.popularidad += p.POPULARIDAD_ATACAR
                print(f"{self.nombre} ha atacado a {tributo.nombre}, matándolo.")
            return True
        else:
            print(
                f"{self.nombre} no tiene suficiente energía para atacar a {tributo.nombre}."
            )
            return False

    def utilizar_objeto(self, objeto: Objeto, arena: Arena):
        """Utiliza el objeto entregado de la mochila del tributo.
        Recibe la arena para verificar atributos de riesgo."""
        assert objeto in self.mochila
        print(f"{self.nombre} ha utilizado {objeto.nombre}.")
        objeto.entregar_beneficio(self, arena)
        self.mochila.remove(objeto)

    def pedir_objeto(self, objetos: list[Objeto]) -> bool:
        """Solicita un objeto a les patrocinadores,
        costándole popularidad al tributo. Recibe la lista de objetos existentes."""
        if self.popularidad >= p.COSTO_OBJETO:
            self.popularidad -= p.COSTO_OBJETO
            objeto = choice(objetos)
            self.mochila.append(objeto)
            print(
                f"{self.nombre} ha solicitado un objeto y les patrocinadores han respondido:"
                f" obtenido un {objeto.nombre}."
            )
            return True
        else:
            print(
                f"{self.nombre} no tiene suficiente popularidad para pedir un objeto."
            )
            return False

    def accion_heroica(self) -> bool:
        """Realiza una acción heroíca"""
        if self.energia >= p.ENERGIA_ACCION_HEROICA:
            self.energia -= p.ENERGIA_ACCION_HEROICA
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

    def hacerse_bolita(self) -> bool:
        self.energia += p.ENERGIA_BOLITA
        print(
            f"{self.nombre} se hizo bolita, recuperando {p.ENERGIA_BOLITA} de energía."
        )
        return True

    def mostrar_estado(self):
        print(f"Distrito: {self.distrito}")
        print(f"Edad: {self.edad}")
        print(f"Vida: {self.vida}")
        print(f"Energía: {self.energia}")
        print(f"Agilidad: {self.agilidad}")
        print(f"Fuerza: {self.fuerza}")
        print(f"Ingenio: {self.ingenio}")
        print(f"Popularidad: {self.popularidad}")
        if self.mochila:
            lista_objetos = ", ".join([objeto.nombre for objeto in self.mochila])
            print(f"Mochila: {lista_objetos}")
            print(f"Peso: {self.peso}")
        else:
            print("Nada en la mochila")


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
    def calcular_dano(self, evento: Evento) -> int:
        pass


class Playa(Ambiente):
    def calcular_dano(self, evento: Evento) -> int:
        return round(
            max(
                [
                    5,
                    (
                        0.4 * p.HUMEDAD_PLAYA
                        + 0.2 * p.VELOCIDAD_VIENTOS_PLAYA
                        + evento.dano
                    )
                    / 5,
                ]
            )
        )


class Bosque(Ambiente):
    def calcular_dano(self, evento: Evento) -> int:
        return round(
            max(
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
        )


class Montana(Ambiente):
    def calcular_dano(self, evento: Evento) -> int:
        return round(
            max(
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
        )


class Objeto(ABC):
    def __init__(self, nombre: str, peso: int):
        self.nombre = nombre
        self.peso = peso

    # Usamos un staticmethod cosa de que pueda ser utilizado
    # incluso sin inicializar en el caso de Especial.
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
        print(f"Su energía ha subido {p.AUMENTAR_ENERGIA} puntos.")


class Arma(Objeto):
    def __init__(self, nombre: str, peso: int):
        super().__init__(nombre, peso)
        self.tipo = "arma"

    @staticmethod
    def entregar_beneficio(tributo: Tributo, arena: Arena):
        nueva_fuerza = round(
            tributo.fuerza * (p.PONDERADOR_AUMENTAR_FUERZA * arena.riesgo + 1)
        )
        nueva_fuerza = max(min(nueva_fuerza, 100), 0)
        print(f"Su fuerza ha subido {nueva_fuerza - tributo.fuerza} puntos.")
        tributo.fuerza = nueva_fuerza


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
    def proximo_ambiente(self) -> Ambiente:
        return self.ambientes[(self.i_ambiente + 1) % 3]

    @property
    def jugadores(self) -> list[Tributo]:
        return self.tributos + [self.jugador]

    def siguiente_ambiente(self) -> Ambiente:
        """Transiciona al siguiente ambiente, limpiando cadáveres en la arena."""
        for tributo in self.tributos:
            if not tributo.esta_vive:
                self.tributos.remove(tributo)

        self.i_ambiente = (self.i_ambiente + 1) % 3
        print(f"El ambiente ha cambiado a {self.ambiente.nombre}.")
        return self.ambiente

    def cargar_jugadores(self, jugador: Tributo, tributos: list[Tributo]):
        assert jugador not in tributos
        assert len(tributos) == 11
        assert not self.jugadores_cargados

        self.jugador = jugador
        self.tributos: list[Tributo] = tributos
        self.jugadores_cargados = True

    def ejecutar_evento(self) -> bool:
        """Ejecuta un evento del ambiente probabilísticamente en base
        a los parámetros del juego. Retorna si es que se ejecutó un evento."""
        hay_evento = random() < p.PROBABILIDAD_EVENTO

        if hay_evento:
            evento = choice(self.ambiente.eventos)
            dano = self.ambiente.calcular_dano(evento)
            print(f"Se ha producido un evento: {evento.nombre}.")
            print(f"Se ha inflingido {dano} de daño a todos los tributos.")
            for tributo in self.jugadores:
                tributo.vida -= dano

        return hay_evento

    def realizar_encuentros(self) -> bool:
        """Realiza los encuentros entre tributos en una partida.
        Retorna True si muere el jugador."""
        assert len(self.tributos) > 0

        n_encuentros = round((self.riesgo * len(self.jugadores)) // 2)
        for _ in range(n_encuentros):
            t1: Tributo = choice(self.jugadores)
            while True:
                t2: Tributo = choice(self.jugadores)
                if t1 != t2:
                    break

            assert t1.esta_vive and t2.esta_vive
            if t1 != t2:
                print(
                    f"Se aproxima un encuentro entre {t1.nombre} (HEA: {t1.vida}, "
                    f"ENE: {t1.energia}) y {t2.nombre} (HEA: {t2.vida}, ENE: {t2.energia})."
                )
                muerte = t1.atacar(t2, es_encuentro=True)
                if muerte:
                    if t2 is self.jugador:
                        print(
                            f"Tu jugador {self.jugador.nombre} ha muerto"
                            f" peleando contra {t1.nombre}."
                        )
                        return True

                    else:
                        self.tributos.remove(t2)
                        print(
                            f"El encuentro ha terminado, {t1.nombre} queda con {t1.vida} de vida."
                        )
                else:
                    print(
                        f"El encuentro ha terminado, {t1.nombre} ha quedado con {t1.vida} de vida,"
                        f" y {t2.nombre} con {t2.vida} de vida."
                    )
        return False

    def mostrar_estado(self):
        print(f"Dificultad: {self.dificultad}")
        print(f"Tributos vivos:")
        tributos_vivos = "".join(
            [f"    {t.nombre}\n" for t in self.tributos if t.esta_vive]
        )
        print(tributos_vivos, end="")
        print(f"Próximo ambiente: {self.proximo_ambiente.nombre}")
