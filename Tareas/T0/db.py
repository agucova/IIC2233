from datetime import datetime
from typing import NamedTuple, List, Union, Tuple
from model import Publication, User, Price, Comment

PROJECT_PATH = "Tareas/T0"
USERS_PATH = f"{PROJECT_PATH}/usuarios.csv"
PUBLICATIONS_PATH = f"{PROJECT_PATH}/publicaciones.csv"
COMMENTS_PATH = f"{PROJECT_PATH}/comentarios.csv"


# This named tuple allows us to distinguish the header and
# the content itself when processing the files
CSVData = NamedTuple("CSVData", [("header", List[str]), ("lines", List[List[str]])])


def load_csv(filepath: str, n_columns: int = -1) -> CSVData:
    """Loads a csv file and returns a CSVData object to aid further processing. Takes an optional n_columns to prevent accidental splitting of literal commas."""
    # Idealmente filepath sería Union[str, Path],
    # pero no tengo ganas de solicitar soporte a pathlib
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    lines = [line.strip().split(",", n_columns) for line in lines]
    return CSVData(header=lines[0], lines=lines[1:])


def parse_date(date: str) -> datetime:
    """Parses a date string into a datetime object"""
    return datetime.strptime(date.strip(), "%Y/%m/%d %H:%M:%S")


def load_users(filepath: str = USERS_PATH) -> List[User]:
    """Loads a user data CSV file and returns a list of User objects"""
    users: List[User] = []
    for line in load_csv(filepath, n_columns=0).lines:
        username: str = line[0]
        users.append(User(username=username))
    assert len(users) > 0
    return users


def load_publications(
    users: List[User], filepath: str = PUBLICATIONS_PATH
) -> Tuple[List[Publication], List[User]]:
    """Loads a publication data CSV file and returns a list of Publication objects"""
    publications: List[Publication] = []
    for line in load_csv(filepath, n_columns=6).lines:
        # We move it to a zero index to ease interaction with lists
        pub_id: int = int(line[0]) - 1
        assert pub_id >= 0

        name: str = line[1]
        description: str = line[5]

        # Load the price as Price
        try:
            price = Price(value=int(line[4].strip()))
        except ValueError:
            raise ValueError("Precio inválido al cargar publicaciones.")

        # Search for the seller
        seller_search: Union[User, None] = None
        for i, user in enumerate(users):
            if user.username == line[2]:
                seller_search = user
                user_index = i
                break

        if seller_search is None:
            raise Exception(
                f"El usuario {line[2]} no fue encontrado al cargar publicaciones."
            )
        else:
            seller: User = seller_search

        creation_date: datetime = parse_date(line[3])

        publication = Publication(
            pub_id=pub_id,
            name=name,
            description=description,
            seller_username=seller.username,
            price=price,
            creation_date=creation_date,
            comments=[],
        )
        publications.append(publication)
        seller.add_publication(publication.pub_id)

        # Not sure if given pass by reference this is necessary
        users[user_index] = seller

    assert len(publications) > 0
    return publications, users


def load_comments(
    users: List[User], publications: List[Publication], filepath: str = COMMENTS_PATH
) -> List[Publication]:
    """Loads a comment data CSV file and returns an updated list of publications that include the comments."""
    comments: List[Comment] = []
    for line in load_csv(filepath, n_columns=4).lines:
        # Search for publication
        pub_id: int = int(line[0])
        publication_search: Union[Publication, None] = next(
            (p for p in publications if p.pub_id == pub_id), None
        )
        if publication_search is None:
            raise Exception(
                f"Publicación {pub_id} no encontrada al cargar comentarios."
            )
        else:
            publication: Publication = publication_search
        # Search for user
        username: str = line[1]

        user_search = next((u for u in users if u.username == username), None)
        if user_search is None:
            raise Exception(f"Usuario {username} no encontrado al cargar comentarios.")
        else:
            user: User = user_search

        # Body and creation date
        body: str = line[3]
        creation_date: datetime = parse_date(line[2])

        comments.append(
            Comment(
                pub_id=publication.pub_id,
                username=user.username,
                body=body,
                creation_date=creation_date,
            )
        )

    for comment in comments:
        publications[comment.pub_id].comments.append(comment)

    return publications


if __name__ == "__main__":
    users = load_users()
    publications = load_publications(users)
    comments = load_comments(users, publications)
    print("hey!")
