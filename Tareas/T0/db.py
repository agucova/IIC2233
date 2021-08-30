from datetime import datetime
from typing import NamedTuple, List, Union
from model import Publication, User, Price
from parametros import MIN_CARACTERES, MAX_CARACTERES

CSVData = NamedTuple("CSVData", [("header", List[str]), ("lines", List[List[str]])])

PROJECT_PATH = "Tareas/T0"
USERS_PATH = f"{PROJECT_PATH}/usuarios.csv"
PUBLICATIONS_PATH = f"{PROJECT_PATH}/publicaciones.csv"
COMMENTS_PATH = f"{PROJECT_PATH}/comentarios.csv"


def load_csv(filepath: str) -> CSVData:
    """Loads a csv file and returns a CSVData object"""
    # Idealmente filepath sería Union[str, Path],
    # pero no tengo ganas de solicitar soporte a pathlib
    with open(filepath, "r", encoding="utf-8") as file:
        file.readlines()

    lines = [line.strip().split(",") for line in file]
    return CSVData(header=lines[0], lines=lines[1:])


def load_users(filepath: str = USERS_PATH) -> List[User]:
    """Loads a user data CSV file and returns a list of User objects"""
    users: List[User] = []
    for line in load_csv(filepath).lines:
        username: str = line[0]
        assert MIN_CARACTERES <= len(username) <= MAX_CARACTERES
        users.append(User(username=username, is_anonymous=False))
    assert len(users) > 0
    return users


def load_publications(
    users: List[User], filepath: str = PUBLICATIONS_PATH
) -> List[Publication]:
    """Loads a publication data CSV file and returns a list of Publication objects"""
    publications: List[Publication] = []
    for line in load_csv(filepath).lines:
        name: str = line[1].strip()
        description: str = line[5].strip()

        # TODO: Figure out how to refine the Union once the check is done later.
        seller: Union[User, None] = next(
            (u for u in users if u.username == line[2].strip()), None
        )

        if seller is None:
            raise Exception(
                f"El usuario {line[2]} no fue encontrado al cargar publicaciones."
            )

        creation_date: datetime = datetime.fromisoformat(line[3].strip())

        try:
            price = Price(value=int(line[4].strip()))
        except ValueError:
            raise ValueError("Precio inválido al cargar publicaciones.")

        publications.append(
            Publication(
                name=name,
                description=description,
                seller=seller,
                price=price,
                creation_date=creation_date,
            )
        )
    assert len(publications) > 0
    return publications
