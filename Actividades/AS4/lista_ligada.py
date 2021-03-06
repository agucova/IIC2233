from __future__ import annotations

from json import dumps
from os import path
from random import choice, uniform

from cargar_usuarios import cargar_usuarios
from parametros import PATH_REGALOS
from usuario import Usuario


class NodoAmigoSecreto:
    # Holi agregué solo type hints (PEP 484) para entender el código
    # No modifiqué nada funcional
    def __init__(self, usuario, id, siguiente=None):
        # No modificar
        self.usuario: Usuario = usuario
        self.siguiente: NodoAmigoSecreto = siguiente or self
        self.regalo_entregado = False
        self.id = id

    def __repr__(self):
        return f"{self.usuario}"

    def insertar_amigo_secreto(
        self, nuevo_nodo: Usuario, posicion: int, posicion_actual=0
    ):
        """
        Insertar un nuevo NodoAmigoSecreto en la posicion.
        :param nuevo_nodo: instancia de Usuario que debe ser
            insertada a la lista ligada.
        :param posicion: posición anterior al nuevo usuario. La posición
        puede ser mayor al tamaño de la lista, en cuyo caso se continuará
        dando vueltas hasta alcanzar el índice pedido.
        :param posicion_actual: Posición en la lista actual.
        """
        nodo_actual = self
        while posicion_actual < posicion:
            assert nodo_actual.siguiente is not None, "Premisa de circularidad rota."

            nodo_actual = nodo_actual.siguiente
            posicion_actual += 1

        nodo_a_insertar = NodoAmigoSecreto(
            nuevo_nodo, posicion + 1, siguiente=nodo_actual.siguiente
        )
        nodo_actual.siguiente = nodo_a_insertar

    def entregar_regalos(self):
        # No modificar
        if self.regalo_entregado:
            print("Hemos dado toda la vuelta! " "Daremos fin a este amigo secreto.")
            return
        print(f"¡{self} se prepara para entregar su " f"regalo a {self.siguiente}!")
        regalo, probabilidad = escoger_regalo()
        print(f"El regalo es.... ¡{regalo}!")
        if uniform(0, 1) < probabilidad:
            print(f"A {self.siguiente} le encantó el regalo!\n")
        else:
            print(
                f"A {self.siguiente} no le gustó mucho el regalo.\n"
                f"Ya habrá otra oportunidad :("
            )
        self.regalo_entregado = True
        self.siguiente.entregar_regalos()

    def __str__(self):
        return f"Amigo Secreto {self.usuario}"

    def visualize(self):
        nodos = []
        bordes = []
        i = 0
        visitados = set()
        nodo = self
        while nodo not in visitados:
            nodos.append({"id": str(nodo), "label": str(nodo)})
            bordes.append({"from": str(nodo), "to": str(nodo.siguiente)})
            visitados.add(nodo)
            nodo = nodo.siguiente

        json_dict = {
            "kind": {"graph": True},
            "nodes": nodos,
            "edges": bordes,
        }

        return dumps(json_dict)


def escoger_regalo():
    # No modificar
    path_regalos = path.join(*PATH_REGALOS)
    with open(path_regalos, "rt", encoding="utf-8") as file:
        regalos = [line.strip().split(",") for line in file]
    regalo = choice(list(regalos))
    return regalo[0], float(regalo[1])


if __name__ == "__main__":
    # Para debugging
    info_usuarios = cargar_usuarios()
    dict_usuarios = {
        nombre: Usuario(nombre, atributos["correo"], atributos["fama"])
        for nombre, atributos in info_usuarios.items()
    }

    # Crear lista
    def crear_lista(dict_usuarios):
        usuarios = iter(dict_usuarios.values())
        lista_ligada = NodoAmigoSecreto(next(usuarios), 0)
        usuarios_recorridos = 0
        for usuario in usuarios:
            lista_ligada.insertar_amigo_secreto(usuario, usuarios_recorridos)
            usuarios_recorridos += 1
        return lista_ligada

    lista_ligada = crear_lista(dict_usuarios)
    pass
