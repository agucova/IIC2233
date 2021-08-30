import os
from typing import List, Union
from parametros import MIN_CARACTERES, MAX_CARACTERES
from art import ART
from model import User

# TODO: Make more robust by checking actual shell being used
POSIX = os.name == "posix"


def bold(string: str) -> str:
    """
    Returns a string with bold formatting.
    Only works on POSIX shells which support ANSI escape sequences.
    """
    # TODO: Implement ANSI escape sequence portability
    return f"\033[1m{string}\033[0m"


def clear_screen():
    """Clears the screen."""
    if POSIX:
        # POSIX shells
        return os.system("clear")
    else:
        # For Windows
        return os.system("cls")


def show_option_menu(
    title: str, options: List[str], body: Union[str, None] = None
) -> int:
    """
    Prints a menu with a title and a body, along with a set of options the user can choose from. Returns the index of the corresponding option.

    Example: `show_menu("Menú de publicaciones realizadas", ["Crear nueva publicación", "Eliminar publicación", "Volver"], body="Mis publicaciones:\\n - Pato de goma")`
    """
    print(bold(f"[{title}]"))
    print()
    if body:
        print(body)
        print()

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


def initial_menu(users: List[User]):
    """Prints the initial menu."""
    option = show_option_menu(
        "Menú de inicio",
        ["Ingresar", "Registrarse", "Ingresar como usuario anónimo", "Salir"],
        body=ART,
    )
    assert isinstance(option, int) and 0 <= option <= 3
    clear_screen()
    if option == 0:
        # Ingresar
        user = login_menu(users)
    elif option == 1:
        # Registrarse
        pass
    elif option == 2:
        # Ingresar como usuario anónimo
        pass
    elif option == 3:
        # Salir
        pass


def login_menu(users: List[User]) -> Union[User, None]:
    """
    Prints the login menu. Returns the user as searched in database. If not found, returns None.
    """

    username = input("Usuario: ").strip().lower()
    assert MIN_CARACTERES <= len(username) <= MAX_CARACTERES

    user: Union[User, None] = next((u for u in users if u.username == username), None)

    return user
