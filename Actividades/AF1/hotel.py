from random import randint, choice
from comida import Comida
import parametros as p


class Hotel:
    def __init__(self):
        self.__energia: int = 100
        self.__dias: int = 0
        self.max_energia = p.MAXIMO_ENERGIA_HOTEL
        self.mascotas = list()
        self.funcionando = True
        self.comidas = [
            Comida("Carne con legumbres", 18, 0.3),
            Comida("Pescado con Castañas", 22, 0.2),
            Comida("Pollo y Arroz", 20, 0.1),
        ]

    @property
    def energia(self) -> int:
        return self.__energia

    @energia.setter
    def energia(self, nueva_energia: int):
        # Implementamos operaciones modulares con tal de
        # fácilmente gestionar los descuentos aleatorios
        if nueva_energia < 0:
            self.__energia = 0
        elif nueva_energia > self.max_energia:
            self.__energia = self.max_energia
        else:
            self.__energia = nueva_energia

    @property
    def dias(self) -> int:
        return self.__dias

    @dias.setter
    def dias(self, dias_act: int):
        if dias_act > 0 and dias_act - self.__dias == 1:
            self.__dias = dias_act
        else:
            raise ValueError(
                "El número de dias debe ser mayor que 0 y debe ser incremental."
            )

    def hotel_en_buen_estado(self):
        """
        Esta función verifica las condiciones de término
        del programa. Si se pierden más de dos mascotas
        en un mismo día o el Hotel se queda con menos de
        tres mascotas, el programa termina.
        """
        mascotas_perdidas = 0
        for mascota in self.mascotas:
            if mascota.satisfaccion < p.MASCOTA_SATISFACCION_MINIMO:
                self.despedir_mascota(mascota)
                mascotas_perdidas += 1
        if mascotas_perdidas > 2 or len(self.mascotas) < 3:
            return False

        return True

    def imprimir_estado(self):
        """Printea un resumen del estado del hotel."""
        print("# Estado del Hotel #")
        print(f"Día {self.dias}")
        print(f"Energía del Cuidador: {self.energia}")
        if len(self.mascotas) >= 1:
            print(
                f"Mascotas ({len(self.mascotas)}): {[mascota.nombre for mascota in self.mascotas]}"
            )
        else:
            print("No hay mascotas aún.")
        print()

    def recibir_mascota(self, mascotas):
        self.mascotas += mascotas
        for mascota in mascotas:
            mascota.saludar()
            print(
                f"""
            Ha aparecido un {mascota.especie} en la recepción,
            su nombre es {mascota.nombre}. {mascota.dueno}, su dueño
            te pide que lo cuides hasta que regrese.
            """
            )

    def despedir_mascota(self, mascota):
        self.mascotas.remove(mascota)

        print(
            f"""
        Oh no!
        {mascota.dueno}, el dueño de {mascota.nombre} se lo ha llevado.
        Huéspedes en el Hotel: {len(self.mascotas)}
        """
        )

    def imprimir_mascotas(self):
        for mascota in self.mascotas:
            print(mascota)

    def nuevo_dia(self):
        """Transiciona el estado del hotel a un nuevo día"""
        if self.hotel_en_buen_estado():
            print("# Nuevo día #")
            self.dias += 1
            self.energia = self.max_energia
            for i in range(len(self.mascotas)):
                self.mascotas[i].entretencion -= randint(0, 50)
                self.mascotas[i].saciedad -= randint(0, 50)
        else:
            self.funcionando = False
            print("# Simulación Finalizada #")
            print(f"{self.dias} dias transcurridos.")
            print()

    def revisar_energia(self):
        if self.energia >= min(p.COSTO_ENERGIA_ALIMENTAR, p.COSTO_ENERGIA_PASEAR):
            return True
        return False

    def pasear_mascota(self, mascota):
        self.energia -= p.COSTO_ENERGIA_PASEAR
        mascota.pasear()
        print(f"{mascota.nombre} salió a pasear feliz!")

    def alimentar_mascota(self, mascota):
        """Alimenta a una mascota con una de las comidas disponibles en el hotel.
        Asume que las comidas son recursos infinitos y no los elimina del inventario."""
        mascota.comer(choice(self.comidas))
        self.energia -= p.COSTO_ENERGIA_ALIMENTAR
