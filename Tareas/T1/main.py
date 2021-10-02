import colorama

from db import cargar_tributos, cargar_objetos, cargar_ambientes, cargar_arenas
from menus import menu_inicio

if __name__ == "__main__":

    colorama.init()

    # Mostrar el menú de inicio
    while True:
        # Cargar datos
        tributos = cargar_tributos()
        objetos = cargar_objetos()
        ambientes = cargar_ambientes()
        arenas = cargar_arenas(ambientes)
        menu_inicio(tributos, objetos, arenas)
