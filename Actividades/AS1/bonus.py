from atracciones import AtraccionAdrenalinica, AtraccionFamiliar
import parametros as p


# Recuerda completar la herencia!
class AtraccionTerrorifica(AtraccionAdrenalinica):
    def __init__(self, nombre: str, capacidad: int, salud_necesaria: int):
        super().__init__(nombre, capacidad, salud_necesaria)
        self.efecto_salud = p.SALUD_TERROR
        self.efecto_felicidad = p.FELICIDAD_TERROR

    def iniciar_juego(self, personas):
        for persona in personas:
            if persona.salud <= 2 * self.salud_necesaria:
                print(f"{persona.nombre} necesitará capacitación antes de jugar")
                persona.definir_estados()

        super().iniciar_juego(personas)


# Recuerda completar la herencia!
class CasaEmbrujada(AtraccionTerrorifica, AtraccionFamiliar):
    def iniciar_juego(self, personas):
        AtraccionFamiliar.iniciar_juego(self, personas)
