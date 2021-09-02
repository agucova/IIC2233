from typing import List, Type, Union
from mascota import Perro, Gato, Conejo, Mascota


# En la tarea a veces uso type hints para ayudarme a captar errores con Pylance
# Esas son las anotaciones en la definición de cada función y algunas variables
# Son parte estándar de Python y no alteran la funcionalidad del programa


def cargar_mascotas(archivo_mascotas: str) -> List[Union[Type[Mascota], Mascota]]:
    """Carga las mascotas a una lista con los tipos adecuados."""
    with open(archivo_mascotas, "r") as f:
        lines = [line.strip().split(",") for line in f.readlines()]

    lista_mascotas: List[Union[Type[Mascota], Mascota]] = []
    for line in lines[1:]:
        try:
            propiedades = line[0], line[2], line[3], int(line[4]), int(line[5])
        except ValueError:
            raise ValueError(
                "No se pudo convertir los enteros en el .csv adecuadamente."
            )

        if line[1] == "perro":
            mascota = Perro(*propiedades)
        elif line[1] == "gato":
            mascota = Gato(*propiedades)
        elif line[1] == "conejo":
            mascota = Conejo(*propiedades)
        else:
            mascota = Mascota(*propiedades)
            print(f"Alerta: Especie no reconocida {line[1]} en la mascota {line[0]}")
            print("Utilizando mascota genérica")

        lista_mascotas.append(mascota)

    return lista_mascotas


if __name__ == "__main__":
    lista_mascotas = cargar_mascotas("mascotas.csv")
    for mascota in lista_mascotas:
        print(mascota)
