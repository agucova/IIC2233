from typing import List, Type
from mascota import Perro, Gato, Conejo, Mascota


def cargar_mascotas(archivo_mascotas: str) -> List[Type[Mascota]]:
    with open(archivo_mascotas, "r") as f:
        lines = [line.strip().split(",") for line in f.readlines()]

    lista_mascotas: List[Type[Mascota]] = []
    for line in lines:
        if line[1] == "perro":
            mascota = Perro(line[0], line[2], line[3], line[4], line[5])
        elif line[1] == "gato":
            mascota = Gato(line[0], line[2], line[3], line[4], line[5])
        elif line[1] == "conejo":
            mascota = Conejo(line[0], line[2], line[3], line[4], line[5])
        else:
            raise ValueError("tipo de mascota no reconocida")

        lista_mascotas.append(mascota)

    return lista_mascotas
