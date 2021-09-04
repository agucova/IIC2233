import os
from typing import List, Union, Tuple, Dict
from parametros import MIN_CARACTERES, MAX_CARACTERES
from art import ART
from model import Publication, User, Comment, Price
from datetime import datetime
from db import (
    delete_publication,
    insert_new_comment,
    insert_new_user,
    insert_new_publication,
    print_date,
)


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


def initial_menu(users: List[User], publications: Dict[int, Publication]):
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

    principal_menu(user, users, publications)


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
        elif not username.isalnum():
            print(
                f"El usuario {username} contiene carácteres no esperados. Utiliza letras o números."
            )
        else:
            break

    user = User(username=username, publications=[])
    # The order here is important, in case we have a IOError when inserting
    # Expected behaviour is a crash in that case.
    insert_new_user(user)
    users.append(user)

    return users, user


def principal_menu(
    user: Union[User, None], users: List[User], publications: Dict[int, Publication]
):
    """Print the prinicipal menu for choosing between public or user publications."""
    while True:
        option = show_option_menu(
            "Menú Principal",
            [
                "Menú de Publicaciones",
                "Menú de Publicaciones Realizadas",
                "Salir",
            ],
            "Bienvenido a DCComercio. Selecciona una opción para seguir",
        )
        if option == 0:
            publications_menu(user, users, publications)
        elif option == 1:
            if user is not None:
                my_publications_menu(user, users, publications)
            else:
                print("Debes iniciar sesión para esto.")
        elif option == 2:
            break


def publications_menu(
    user: Union[User, None], users: List[User], publications: Dict[int, Publication]
):
    """Print the publications menu."""
    while True:
        pub_option = show_option_menu(
            "Menú de Publicaciones",
            [p.name for p in publications.values()] + ["Volver"],
            body="Este es el tablero público de publicaciones. Escoge una publicación para seguir.",
        )

        if pub_option == len(publications):
            return principal_menu(user, users, publications)

        while True:
            publication = publications[pub_option]
            body = (
                f"Creado: {publication.creation_date}\n"
                + f"Vendedor: {publication.seller_username}\n"
                + f"Precio: {publication.price}\n"
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
                ["Agregar comentario", "Volver"],
                body,
            )

            if in_pub_option == 0:
                if user:
                    publication = comment_menu(user, publication)
            elif in_pub_option == 1:
                break


def my_publications_menu(
    user: User, users: List[User], publications: Dict[int, Publication]
):
    assert user is not None
    while True:
        body = "Mis publicaciones:\n"
        body += "\n".join([f"- {publications[pid].name}" for pid in user.publications])
        option = show_option_menu(
            "Menú de Publicaciones Realizadas",
            ["Crear una nueva publicación", "Eliminar publicación", "Volver"],
            body,
        )
        if option == 0:
            new_publication_menu(user, users, publications)
        elif option == 1:
            user, publications = remove_publication_menu(user, users, publications)
        elif option == 2:
            break


def new_publication_menu(
    user: User, users=List[User], publications=Dict[int, Publication]
) -> Union[Publication, None]:
    show_menu_header("Crear una nueva publicación", "")
    while True:
        name = input("Nombre: ").strip().replace("\n", " ")
        if name:
            break

    description = input("Descripción: ").strip().replace("\n", " ")

    while True:
        try:
            price = Price(
                value=int(
                    input("Precio (CLP): ").strip().replace(" ", "").replace(".", "")
                ),
                currency="CLP",
            )
        except ValueError:
            print("Ingresa un número entero sin símbolos.")
        else:
            break

    print(bold("\nPublicación a crear:"))
    print(f"Nombre: {name}")
    print(f"Descripción: {description}")
    print(f"Precio: {price}\n")
    confirm = (
        input("¿Estás seguro que quieres crear esta publicación? (s/n): ")
        .strip()
        .lower()
        == "s"
    )
    if not confirm:
        return None

    creation_date = datetime.now()

    publication = Publication(
        pub_id=len(publications),
        name=name,
        description=description,
        price=price,
        creation_date=creation_date,
        seller_username=user.username,
        comments=[],
    )

    insert_new_publication(publication)
    publications[publication.pub_id] = publication
    user.add_publication(publication.pub_id)

    print(f"Publicación {publication.name} creada con éxito.")
    return publication


def remove_publication_menu(
    user: User, users: List[User], publications: Dict[int, Publication]
) -> Tuple[User, Dict[int, Publication]]:
    # TODO: Add creation_date
    publication_list = [
        f"{publications[pid].name} -- Creado el {print_date(publications[pid].creation_date)}"
        for pid in user.publications
    ]
    option = show_option_menu(
        "Remover una publicación",
        publication_list + ["Cancelar"],
        body="Elige una publicación para remover.\n\n"
        + bold("ADVERTENCIA:")
        + " Esto es permanente.",
    )

    if option == len(publication_list):
        return user, publications
    else:
        publication = publications[user.publications[option]]
        confirm = (
            input(
                f"¿Estás seguro de quieres remover la publicación {publication.name}? (s/n) "
            )
            .strip()
            .lower()
            == "s"
        )

        if not confirm:
            return user, publications

        # delete_publication is fault-tolerant, and should opt for crashing the program
        # over comprimising data integrity.
        delete_publication(publication)
        user.remove_publication(publication.pub_id)
        publications.pop(publication.pub_id)

        print(f"Publicación {publication.name} removida con éxito.")
        return user, publications


def comment_menu(user: User, publication: Publication):
    assert user is not None
    assert publication is not None

    show_menu_header("Agregar comentario", "Por favor se respetuoso!")

    # Note how we're not sanitizing the comments other than replacing newlines
    # In theory this shouldn't be a problem because of how the CVS parser
    # works, but it's worth keeping in mind.
    while True:
        comentario = input("Comentario: ").strip().replace("\n", " ")
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

    # The order here is important, in case we have a IOError when inserting
    insert_new_comment(comment)

    publication.comments.append(comment)

    return publication
