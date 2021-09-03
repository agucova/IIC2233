import os
from typing import List, Union, Tuple
from parametros import MIN_CARACTERES, MAX_CARACTERES
from art import ART
from model import Publication, User, Comment
from datetime import datetime

# TODO: Make portable
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


def show_menu_header(title: str, body: Union[str, None]) -> None:
    clear_screen()
    print(bold(f"[{title}]"))
    print()
    if body:
        print(body)
        print()


def show_option_menu(
    title: str, options: List[str], body: Union[str, None] = None
) -> int:
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


def initial_menu(users: List[User], publications: List[Publication]):
    """Prints the initial menu."""
    option = show_option_menu(
        "Menú de inicio",
        ["Ingresar", "Registrarse", "Ingresar como usuario anónimo", "Salir"],
        body=ART,
    )
    assert isinstance(option, int) and 0 <= option <= 3

    user = None
    if option == 0:
        # Ingresar
        user = login_menu(users)
    elif option == 1:
        # Registrarse
        users, user = register_menu(users)
    elif option == 2:
        pass
    elif option == 3:
        # Salir
        print("Adiós!")
        return None

    publications_menu(user, users, publications)


def login_menu(users: List[User]) -> Union[User, None]:
    """
    Prints the login menu. Returns the user as searched in database. If not found, returns None.
    """

    while True:
        username = input("Usuario: ").strip()

        user: Union[User, None] = next(
            (u for u in users if u.username == username), None
        )

        if user:
            break

    return user


def register_menu(users: List[User]) -> Tuple[List[User], User]:
    """
    Prints the registration menu. Returns the user as created in the database.
    """

    while True:
        username = input("Usuario: ").strip()
        if username in [u.username for u in users]:
            print("El usuario ya existe.")
        elif not username:
            print("El usuario no puede estar vacío.")
        elif len(username) > MAX_CARACTERES:
            print(f"El usuario {username} es demasiado largo.")
        elif len(username) < MIN_CARACTERES:
            print(f"El usuario {username} es demasiado corto.")
        else:
            break
    user = User(username=username)
    users.append(user)

    return users, user


def publications_menu(
    user: Union[User, None], users: List[User], publications: List[Publication]
):
    """Print the publications menu."""
    while True:
        pub_option = show_option_menu(
            "Menú de Publicaciones",
            [p.name for p in publications] + ["Regresar"],
            body="Bienvenido a DCComercio. Escoge una publicación para seguir.",
        )

        if pub_option == len(publications) + 1:
            return login_menu(users)

        while True:
            publication = publications[pub_option]
            body = (
                f"Creado: {publication.creation_date}\n"
                + f"Vendedor: {publication.seller_username}\n"
                + f"Precio: ${publication.price.value} ({publication.price.currency})\n"
                + f"Descripción: {publication.description}\n"
            )

            body += "\nComentarios:\n"
            body += "\n" + "\n".join(
                [
                    f"{c.creation_date}, {c.username}: {c.body}"
                    for c in publication.comments
                ]
            )
            in_pub_option = show_option_menu(
                publication.name,
                ["Agregar comentario", "Regresar"],
                body,
            )

            if in_pub_option == 0:
                if user:
                    publication = comment_menu(user, publication)
            elif in_pub_option == 1:
                break


def comment_menu(user: User, publication: Publication):
    assert user is not None
    assert publication is not None

    show_menu_header("Agregar comentario", "Por favor se respetuoso!")
    while True:
        comentario = input("Comentario: ").strip()
        if len(comentario) >= 500:
            print("El comentario es demasiado largo.")
        elif comentario:
            break

    comment = Comment(
        pub_id=publication.pub_id,
        body=comentario,
        username=user.username,
        creation_date=datetime.now(),
    )

    publication.comments.append(comment)

    return publication
