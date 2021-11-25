from __future__ import annotations

from collections import deque
from typing import Optional

from usuario import Usuario


class NodoGrafo:
    def __init__(self, usuario):
        # No modificar
        self.usuario: Usuario = usuario
        self.amistades: Optional[list[NodoGrafo]] = None

    def formar_amistad(self, nueva_amistad):
        self.amistades = self.amistades or []
        if nueva_amistad not in self.amistades:
            self.amistades.append(nueva_amistad)
        if nueva_amistad not in nueva_amistad.amistades:
            nueva_amistad.amistades.append(self)

    def eliminar_amistad(self, ex_amistad):
        self.amistades = self.amistades or []
        if ex_amistad in self.amistades:
            self.amistades.remove(ex_amistad)
        if ex_amistad in ex_amistad.amistades:
            ex_amistad.amistades.remove(self)


def recomendar_amistades(nodo_inicial, profundidad) -> list[NodoGrafo]:
    """
    Recibe un NodoGrafo inicial y una profundidad de busqueda, retorna una
    lista de nodos NodoGrafo recomendados como amistad a esa profundidad.
    """
    # DFS
    stack = deque([nodo_inicial])
    visitados = set()
    recomendados = []
    while stack:
        nodo = stack.pop()
        if nodo not in visitados:
            visitados.add(nodo)
            if profundidad > 0:
                stack.extend(nodo.amistades or [])
                if nodo_inicial not in nodo.amistades:
                    recomendados.append(nodo)

        profundidad -= 1

    return recomendados


def busqueda_famosos(
    nodo_inicial: NodoGrafo, visitados=None, distancia_max=80
) -> tuple[int, Optional[NodoGrafo]]:
    """
    [BONUS]
    Recibe un NodoGrafo y busca en la red social al famoso mas
    cercano, retorna la distancia y el nodo del grafo que contiene
    a el usuario famoso cercano al que se encuentra.
    """
    queue = deque([nodo_inicial])
    visitados = visitados or set()
    distancia = 0
    while queue:
        if distancia > distancia_max:
            return distancia_max, None
        nodo = queue.popleft()
        if nodo not in visitados:
            visitados.add(nodo)
            if nodo.usuario.es_famoso:
                return distancia, nodo
            queue.extend(nodo.amistades or [])
            distancia += 1

    return distancia_max, None
