from datetime import datetime
from typing import NamedTuple, List, Union, Tuple
from model import Publication, User, Price, Comment
from random import randint
import os

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


def print_date(date: datetime) -> str:
    """Generates a date str in the format YYYY/MM/DD HH:MM:SS"""
    return date.strftime("%Y/%m/%d %H:%M:%S")


def load_users(filepath: str = USERS_PATH) -> List[User]:
    """Loads a user data CSV file and returns a list of User objects"""
    users: List[User] = []
    for line in load_csv(filepath, n_columns=0).lines:
        username: str = line[0]
        users.append(User(username=username, publications=[]))
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
            price = Price(value=float(line[4].strip()))
        except ValueError:
            raise ValueError("Precio inválido al cargar publicaciones.")

        # Search for the seller
        seller_search: Union[User, None] = None
        user_index: Union[int, None] = None
        for i, user in enumerate(users):
            if user.username == line[2]:
                seller_search = user
                user_index = i
                break

        if seller_search is None or user_index is None:
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
        # We're using zero indexing!
        pub_id: int = int(line[0]) - 1
        assert pub_id >= 0
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


def insert_new_user(user: User, filepath: str = USERS_PATH):
    """Inserts a newly generated user into the corresponding CSV file.
    Don't use this with users that already have made publications, since that information is not written to the database."""
    assert user is not None
    assert not user.publications

    with open(filepath, "a", encoding="utf-8") as file:
        file.write(f"{user.username}\n")


def insert_new_comment(comment: Comment, filepath: str = COMMENTS_PATH):
    """Inserts a a new comment into the corresponding CSV file."""
    assert comment is not None
    assert comment.pub_id is not None
    assert "\n" not in comment.body

    # We don't use escaping per the existing CSV file, although it's not really great
    # The + 1 in pub_id uses the 1-indexing of the CSV file
    with open(filepath, "a", encoding="utf-8") as file:
        file.write(
            f"{comment.pub_id + 1},{comment.username},{print_date(comment.creation_date)},{comment.body}\n"
        )


def insert_new_publication(publication: Publication, filepath: str = PUBLICATIONS_PATH):
    """Inserts a new publication into the corresponding CSV file.
    Don't use this for publications that already have comments in them, as this won't insert them for you."""
    assert not publication.comments
    assert publication.seller_username is not None
    assert "\n" not in publication.name and "\n" not in publication.description

    with open(filepath, "a", encoding="utf-8") as file:
        file.write(
            f"{publication.pub_id + 1},{publication.name},{publication.seller_username},{print_date(publication.creation_date)},{publication.price.value},{publication.description}\n"
        )


def delete_publication(publication: Publication, filepath: str = PUBLICATIONS_PATH):
    """Deletes a publication through an ID lookup on the CSV.
    Tries to be as fault-tolerant as possible, with the cost of significant IO performance."""

    with open(filepath, "r", encoding="utf-8") as f_original:
        lines = f_original.readlines()
        n_lines = len(lines)

    # Using a temporary files prevent a broken state or corrupted database
    # if something goes wrong in the middle of the process.
    # We can later swap once we know everything worked right.
    tmp_filepath = f".rm-{randint(0, 9999999999999999999)}.tmp"
    with open(tmp_filepath, "r+", encoding="utf-8") as f_tmp:
        # Let's start at the beginning
        f_tmp.seek(0)
        # Write everything but an exact match of the expected line.
        for line in lines:
            if (
                line
                != f"{publication.pub_id + 1},{publication.name},{publication.seller_username},{print_date(publication.creation_date)},{publication.price.value},{publication.description}\n"
            ):
                f_tmp.write(line)
        f_tmp.truncate()

    assert os.path.isfile(tmp_filepath)
    assert os.stat(tmp_filepath).st_size > 0
    with open(tmp_filepath, "r", encoding="utf-8") as f_tmp:
        lines = f_tmp.readlines()
        assert len(lines) == n_lines - 1

    # This is the crucial step
    # We swap the tmpfile for the actual file
    os.replace(tmp_filepath, filepath)


if __name__ == "__main__":
    users = load_users()
    publications, users = load_publications(users)
    publications = load_comments(users, publications)

    print("hey!")
