from menus import initial_menu
from db import load_comments, load_publications, load_users
import colorama

if __name__ == "__main__":
    colorama.init()
    users = load_users()
    publications, users = load_publications(users)
    publications = load_comments(users, publications)

    initial_menu(users, publications)
