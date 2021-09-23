from __future__ import annotations
from random import randint
from time import sleep
from pedido import Pedido
from shopper import Shopper
from tienda import Tienda
from threading import Thread


class DCComidApp(Thread):
    def __init__(
        self,
        shoppers: list[Shopper],
        tiendas: dict[str, Tienda],
        pedidos: list[tuple[str, str, str]],
    ):
        # NO MODIFICAR
        super().__init__()
        self.shoppers = shoppers
        self.pedidos = pedidos
        self.tiendas = tiendas

    def obtener_shopper(self):
        while True:
            for shopper in self.shoppers:
                if not shopper.ocupado:
                    return shopper
            print("Todos los shoppers están ocupados, esperando disponibilidad.")
            Shopper.evento_disponible.wait()

    def run(self):
        while self.pedidos:
            id_, nombre_tienda, descripcion = self.pedidos.pop(0)
            tienda: Tienda = self.tiendas[nombre_tienda]

            pedido = Pedido(id_, nombre_tienda, descripcion)

            shopper: Shopper = self.obtener_shopper()
            shopper.asignar_pedido(pedido)
            tienda.ingresar_pedido(pedido, shopper)
            trafico_de_red = randint(1, 5)
            sleep(trafico_de_red)


if __name__ == "__main__":
    pass
