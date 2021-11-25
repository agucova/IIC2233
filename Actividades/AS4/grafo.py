from __future__ import annotations

from collections import deque
from typing import Optional

from usuario import Usuario


class NodoGrafo:
    # Holi agregué solo type hints (PEP 484) para entender el código
    # No modifiqué nada funcional
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

    def __repr__(self):
        return f"{self.usuario}"


def recomendar_amistades(
    nodo_inicial: NodoGrafo, max_profundidad: int
) -> list[NodoGrafo]:
    """
    Recibe un NodoGrafo inicial y una profundidad de busqueda, retorna una
    lista de nodos NodoGrafo recomendados como amistad a esa profundidad.
    """
    assert max_profundidad > 0

    # BFS
    # Queue also stores depth
    profundidad = 0
    queue: deque[tuple[int, NodoGrafo]] = deque([(profundidad, nodo_inicial)])
    visitados = set()
    recomendados = []
    while queue:
        if profundidad == max_profundidad:
            break

        assert profundidad >= 0
        # print(f"queue: {queue}, prof: {profundidad}")

        nueva_profundidad, nodo = queue.popleft()
        profundidad = (
            nueva_profundidad if nueva_profundidad > profundidad else profundidad
        )

        if nodo not in visitados:
            visitados.add(nodo)
            for amistad in nodo.amistades or []:
                if amistad not in visitados:
                    queue.append((profundidad + 1, amistad))
                    if (
                        amistad not in recomendados
                        and amistad not in nodo_inicial.amistades
                    ):
                        recomendados.append(amistad)
                        # print(
                        # f"recomendado encontrado: {amistad} (profundidad: {profundidad})"
                        # )

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
