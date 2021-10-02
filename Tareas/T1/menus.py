from __future__ import annotations
from typing import Optional
from model import Arena, Objeto, Tributo
import os
import sys


def negrita(string: str) -> str:
    """Retorna un string en negrita. Debe ser utilizado con colorama
    para evitar problemas de portabilidad."""
    return f"\033[1m{string}\033[0m"


def limpiar_pantalla():
    """Clears the screen."""
    posix = os.name == "posix"
    if posix:
        # POSIX shells
        return os.system("clear")
    else:
        # For Windows
        return os.system("cls")


def mostrar_cabecera(title: str, body: Optional[str]) -> None:
    limpiar_pantalla()
    print(negrita(f"[{title}]"))
    print()
    if body:
        print(body)
        print()


def mostrar_menu_opciones(
    title: str, options: list[str], body: Optional[str] = None
) -> int:
    """
    Prints a menu with a title and a body, along with a set of options the user can choose from.
    Returns the index of the corresponding option.

    Example: `show_menu("Menú de publicaciones realizadas", ["Crear nueva publicación",
    "Eliminar publicación", "Volver"], body="Mis publicaciones:\\n - Pato de goma")`
    """
    mostrar_cabecera(title, body)

    for i, option in enumerate(options):
        print(f"[{i}] {option}")
    print()

    selection = input("Selecciona una opción: ").strip()
    while not selection.isdigit() or int(selection) not in range(len(options)):
        selection = input("Selecciona una opción (selección inválida): ").strip()
    try:
        return int(selection)
    except ValueError as e:
        print("[ERROR] Procesamiento de entero inválido.")
        raise e


def menu_inicio(tributos: list[Tributo], objetos: list[Objeto], arenas: list[Arena]):
    """Mostrar el menú inicial"""
    opcion = mostrar_menu_opciones("Menú de Inicio", ["Iniciar partida", "Salir"])

    if opcion == 0:
        # Iniciar partida
        jugador = escoger_tributo(tributos)
        tributos.remove(jugador)

        arena = escoger_arena(arenas)
        arena.cargar_jugadores(jugador, tributos)

        menu_principal(jugador, arena, tributos)
    elif opcion == 1:
        print("¡Hasta pronto!")
        sys.exit()


def escoger_tributo(tributos: list[Tributo]):
    """Escoger el tributo con el que se jugará"""
    opcion = mostrar_menu_opciones(
        "Selecciona un tributo", [f"{t.nombre} ({t.distrito})" for t in tributos]
    )
    return tributos[opcion]


def escoger_arena(arenas: list[Arena]):
    """Escoger la arena en la que se jugará"""
    opcion = mostrar_menu_opciones(
        "Selecciona una arena", [f"{a.nombre} ({a.dificultad})" for a in arenas]
    )
    return arenas[opcion]


def menu_principal(jugador: Tributo, arena: Arena, tributos: list[Tributo]):
    """Mostrar el menú principal"""
    opcion = mostrar_menu_opciones(
        "Menú Principal",
        [
            "Simulación hora",
            "Mostrar estado del tributo",
            "Utilizar objeto",
            "Resumen DCCapitolio",
            "Volver",
            "Salir",
        ],
    )

    if opcion == 0:
        simulacion_hora()
    elif opcion == 5:
        print("¡Hasta pronto!")
        sys.exit()


def simulacion_hora():
    pass
