from __future__ import annotations
from usuario import Usuario
from typing import Optional


class NodoFama:
    def __init__(self, usuario, padre=None):
        # No modificar
        self.usuario: Usuario = usuario
        self.padre: Optional[NodoFama] = padre
        self.hijo_izquierdo: Optional[NodoFama] = None
        self.hijo_derecho: Optional[NodoFama] = None


class ArbolBinario:
    def __init__(self):
        # No modificar
        self.raiz: Optional[NodoFama] = None

    def crear_arbol(self, nodos_fama):
        # No modificar
        for nodo in nodos_fama:
            self.insertar_nodo(nodo, self.raiz)

    def insertar_nodo(self, nuevo_nodo, padre=None):
        padre = padre or self.raiz
        if padre is None:
            self.raiz = nuevo_nodo
        else:
            if nuevo_nodo.usuario.fama <= padre.usuario.fama:
                if padre.hijo_izquierdo is None:
                    padre.hijo_izquierdo = nuevo_nodo
                else:
                    self.insertar_nodo(nuevo_nodo, padre.hijo_izquierdo)
            else:
                if padre.hijo_derecho is None:
                    padre.hijo_derecho = nuevo_nodo
                else:
                    self.insertar_nodo(nuevo_nodo, padre.hijo_derecho)

    def buscar_nodo(self, fama, padre=None):
        padre = padre or self.raiz
        if padre is None:
            return None
        if padre.usuario.fama == fama:
            return padre
        if padre.usuario.fama < fama:
            return self.buscar_nodo(fama, padre.hijo_izquierdo)
        else:
            return self.buscar_nodo(fama, padre.hijo_derecho)

    def print_arbol(self, nodo=None, nivel_indentacion=0):
        # No modificar
        indentacion = "|   " * nivel_indentacion
        if nodo is None:
            print("** DCCelebrity Arbol Binario**")
            self.print_arbol(self.raiz)
        else:
            print(f"{indentacion}{nodo.usuario.nombre}: " f"{nodo.usuario.correo}")
            if nodo.hijo_izquierdo:
                self.print_arbol(nodo.hijo_izquierdo, nivel_indentacion + 1)
            if nodo.hijo_derecho:
                self.print_arbol(nodo.hijo_derecho, nivel_indentacion + 1)
