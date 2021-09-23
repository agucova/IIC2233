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
        super().__init__(name=f"{nombre} (Tienda)", daemon=True)
        # Nota: Además el enunciado dice
        # "deberás completarla de modo que su ejecución termine con el resto del programa".
        # Si bien no veo por qué esto tendría que ser así
        # (al menos que la tienda sea abierta externamente),
        # esto entra en conflicto con que el __init__ esté bajo no modificar.
        # De todas formas agregué daemon=True, aunque parece funcionar con o sin esto.

    def ingresar_pedido(self, pedido: Pedido, shopper: Shopper):
        if self.abierta:
            with self.lock_cola:
                self.cola_pedidos.append((pedido, shopper))
            shopper.asignar_pedido(pedido)
        else:
            # Esto es comportamiento indefinido
            raise (Exception("La tienda está cerrada y recibió un pedido"))

    def preparar_pedido(self, pedido: Pedido):
        assert not pedido.evento_pedido_listo.is_set()
        assert not pedido.entregado

        tiempo_a_completar = randint(1, 10)
        print(
            f"El pedido {pedido.id_} para {self.nombre} se demorará {tiempo_a_completar}."
        )
        sleep(tiempo_a_completar)
        print(f"El pedido {pedido.id_} en {self.nombre} está listo para ser retirado.")

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
                print(f"La tienda {self.nombre} se tomará un descanso de {descanso}.")
                sleep(descanso)
