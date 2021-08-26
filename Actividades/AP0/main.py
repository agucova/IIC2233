# Debes completar esta función para que retorne la información de los ayudantes
from os import listxattr
from typing import Union


def cargar_datos(path: str) -> list[list[str]]:
    try:
        with open(path, "r") as ayudantesf:
            ayudantes = [
                ayudante.strip().split(",") for ayudante in ayudantesf.readlines()
            ]
    except FileNotFoundError as e:
        print(f"El archivo {path} no se pudo encontrar.")
        raise e

    assert len(ayudantes[0]) == 4
    return ayudantes


# Completa esta función para encontrar la información del ayudante entregado
def buscar_info_ayudante(
    nombre_ayudante: str, lista_ayudantes: list[list[str]]
) -> Union[list[str], None]:
    assert len(lista_ayudantes[0]) == 4
    nombre_ayudante = nombre_ayudante.lower()
    for ayudante in lista_ayudantes:
        if ayudante[0].lower() == nombre_ayudante:
            return ayudante
    return None


# Completa esta función para que los ayudnates puedan saludar
def saludar_ayudante(info_ayudante: list[str]) -> str:
    assert len(info_ayudante) == 4
    return f"Hola {info_ayudante[0]}, tu cargo es {info_ayudante[1]} y eres {info_ayudante[2]} en GitHub y {info_ayudante[3]} en Discord."


if __name__ == "__main__":
    pass
    # El código que aquí escribas se ejecutará solo al llamar a este módulo.
    # Aquí puedes probar tu código llamando a las funciones definidas.

    # Puede llamar a cargar_datos con el path del archivo 'ayudantes.csv'
    # para probar si obtiene bien los datos.

    # Puedes intentar buscar la lista de unos de los nombres
    # que se encuentran en el archivo con la función buscar_info_ayudante.
    # Además puedes utilizar la lista obtenida para generar su saludo.

    # Hint: la función print puede se útil para revisar
    #       lo que se está retornando.
    ayudantes = cargar_datos("Actividades/AP0/ayudanddtes.csv")
    ayudante = buscar_info_ayudante("Francisca Ibarra", ayudantes)
    print(saludar_ayudante(ayudante))
