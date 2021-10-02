from __future__ import annotations
from typing import Optional
import os


def bold(string: str) -> str:
    """
    Returns a string with bold formatting.
    Only works on POSIX shells which support ANSI escape sequences.
    """
    # TODO: Implement ANSI escape sequence portability
    return f"\033[1m{string}\033[0m"


def clear_screen():
    """Clears the screen."""
    # TODO: Make more robust by checking actual shell being used
    posix = os.name == "posix"
    if posix:
        # POSIX shells
        return os.system("clear")
    else:
        # For Windows
        return os.system("cls")


def show_menu_header(title: str, body: Optional[str]) -> None:
    clear_screen()
    print(bold(f"[{title}]"))
    print()
    if body:
        print(body)
        print()


def show_option_menu(title: str, options: list[str], body: Optional[str] = None) -> int:
    """
    Prints a menu with a title and a body, along with a set of options the user can choose from. Returns the index of the corresponding option.

    Example: `show_menu("Menú de publicaciones realizadas", ["Crear nueva publicación", "Eliminar publicación", "Volver"], body="Mis publicaciones:\\n - Pato de goma")`
    """
    show_menu_header(title, body)

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
