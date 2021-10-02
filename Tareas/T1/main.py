from db import cargar_tributos, cargar_objetos, cargar_ambientes, cargar_arenas
from menus import menu_inicio
import colorama

if __name__ == "__main__":

    colorama.init()

    # Cargar datos
    tributos = cargar_tributos()
    objetos = cargar_objetos()
    ambientes = cargar_ambientes()
    arenas = cargar_arenas(ambientes)

    # Mostrar el menú de inicio
    menu_inicio(tributos, objetos, arenas)
