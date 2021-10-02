from typing import Union


def cargar_datos(path: str) -> list[list[str]]:
    """Carga los datos de ayudantes de un archivo y lo retorna como una lista de listas."""
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


def buscar_info_ayudante(
    nombre_ayudante: str, lista_ayudantes: list[list[str]]
) -> Union[list[str], None]:
    """Busca la información de un ayudante por su nombre en una lista dada."""
    assert len(lista_ayudantes[0]) == 4
    nombre_ayudante = nombre_ayudante.lower()
    for ayudante in lista_ayudantes:
        if ayudante[0].lower() == nombre_ayudante:
            return ayudante
    return None


def saludar_ayudante(info_ayudante: list[str]) -> str:
    """Genera un string de saludo para un ayudante en base a su información."""
    assert len(info_ayudante) == 4
    return (
        f"Hola {info_ayudante[0]}, tu cargo es {info_ayudante[1]} y eres "
        f"{info_ayudante[2]} en GitHub y {info_ayudante[3]} en Discord."
    )


if __name__ == "__main__":
    ayudantes = cargar_datos("Actividades/AP0/ayudantes.csv")
    ayudante = buscar_info_ayudante("Francisca Ibarra", ayudantes)
    print(saludar_ayudante(ayudante))
