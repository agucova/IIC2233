from menus import initial_menu
from db import load_users
import colorama

if __name__ == "__main__":
    colorama.init()
    users = load_users()
    initial_menu(users)
