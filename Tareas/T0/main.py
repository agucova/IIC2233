from menus import initial_menu
from db import load_users

if __name__ == "__main__":
    users = load_users()
    initial_menu(users)
