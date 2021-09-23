from shopper import Shopper
from pedido import Pedido
from threading import Thread, Lock
from time import sleep
from random import randint


class Tienda(Thread):
    def __init__(self, nombre):
        # NO MODIFICAR
        self.nombre = nombre
        self.cola_pedidos = []
        self.abierta = True
        # COMPLETAR DESDE AQUI
        self.lock_cola = Lock()
        # MODIFICACIÓN ADICIONAL
        # Le pongo nombre al Thread para que sea
        # legible en debugging (pedí permiso)
        super().__init__(name=f"{nombre} (Tienda)")

    def ingresar_pedido(self, pedido: Pedido, shopper: Shopper):
        with self.lock_cola:
            if self.abierta:
                self.cola_pedidos.append((pedido, shopper))
                print(
                    f"{self.nombre} recibió un pedido con el shopper {shopper.nombre}."
                )
        shopper.asignar_pedido(pedido)

    def preparar_pedido(self, pedido):
        tiempo_a_completar = randint(1, 10)
        print(f"El pedido para {self.nombre} se demorará {tiempo_a_completar}.")
        sleep(tiempo_a_completar)
        print(f"El pedido en {self.nombre} está listo para ser retirado.")

    def run(self):
        while self.abierta:
            if self.cola_pedidos:
                with self.lock_cola:
                    pedido, shopper = self.cola_pedidos.pop(0)
                self.preparar_pedido(pedido)
                pedido.evento_pedido_listo.set()
                pedido.evento_llego_repartidor.wait()
                print(
                    f"El pedido a {self.nombre} ha sido retirado por {shopper.nombre}."
                )
            else:
                descanso = randint(1, 5)
                print(f"La tienda se tomará un descanso de {descanso}.")
                sleep(descanso)
