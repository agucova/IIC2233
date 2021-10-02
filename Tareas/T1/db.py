from __future__ import annotations
from typing import NamedTuple
from model import (
    Ambiente,
    Arena,
    Evento,
    Objeto,
    Tributo,
    Arma,
    Especial,
    Consumible,
    Bosque,
    Playa,
    Montana,
)

PROJECT_PATH = "."
RUTA_TRIBUTOS = f"{PROJECT_PATH}/tributos.csv"
RUTA_ARENAS = f"{PROJECT_PATH}/arenas.csv"
RUTA_AMBIENTES = f"{PROJECT_PATH}/ambientes.csv"
RUTA_OBJETOS = f"{PROJECT_PATH}/objetos.csv"

DatosCSV = NamedTuple(
    "DatosCSV", [("cabecera", "list[str]"), ("lineas", "list[list[str]]")]
)


def cargar_csv(ruta: str, n_columnas: int = -1) -> DatosCSV:
    """Carga un archivo CSV y retorna un objeto DatosCSV para facilitar su procesamiento.
    Toma un argumento opcional de n_columnas para casos
    donde haya columnas literales que incluyan comas."""
    # Idealmente filepath sería Union[str, Path],
    # pero no tengo ganas de solicitar soporte a pathlib
    with open(ruta, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    assert len(lineas) > 0
    lineas = [line.strip().split(",", n_columnas - 1) for line in lineas]
    return DatosCSV(cabecera=lineas[0], lineas=lineas[1:])


def cargar_tributos(ruta: str = RUTA_TRIBUTOS) -> list[Tributo]:
    """Carga un archivo CSV de tributos y retorna una lista de objetos Tributo."""
    datos = cargar_csv(ruta)
    tributos = [
        Tributo(
            line[0],
            line[1],
            int(line[2]),
            int(line[3]),
            int(line[4]),
            int(line[5]),
            int(line[6]),
            int(line[7]),
            int(line[8]),
        )
        for line in datos.lineas
    ]
    return tributos


def cargar_objetos(ruta: str = RUTA_OBJETOS) -> list[Objeto]:
    datos = cargar_csv(ruta)
    objetos: list[Objeto] = []
    for linea in datos.lineas:
        nombre = linea[0]
        tipo = linea[1]
        peso = int(linea[2])

        assert tipo in ["arma", "especial", "consumible"]

        if tipo == "arma":
            objetos.append(Arma(nombre, peso))
        elif tipo == "consumible":
            objetos.append(Consumible(nombre, peso))
        elif tipo == "especial":
            objetos.append(Especial(nombre, peso))

    assert len(objetos) > 0
    return objetos


def cargar_ambientes(ruta: str = RUTA_AMBIENTES) -> list[Ambiente]:
    datos = cargar_csv(ruta)
    ambientes: list[Ambiente] = []
    for linea in datos.lineas:
        nombre = linea[0]
        eventos = [evento.split(";") for evento in linea[1:4]]
        eventos = [Evento(evento[0], int(evento[1])) for evento in eventos]

        assert nombre in ["bosque", "montaña", "playa"]
        if nombre == "bosque":
            ambientes.append(Bosque(nombre, eventos))
        elif nombre == "playa":
            ambientes.append(Playa(nombre, eventos))
        elif nombre == "montaña":
            ambientes.append(Montana(nombre, eventos))

    assert len(ambientes) > 0
    return ambientes


def cargar_arenas(ambientes: list[Ambiente], ruta: str = RUTA_ARENAS) -> list[Arena]:
    assert len(ambientes) > 0

    datos = cargar_csv(ruta)
    arenas: list[Arena] = []
    for linea in datos.lineas:
        nombre = linea[0]
        dificultad = linea[1]
        riesgo = float(linea[2])
        arenas.append(Arena(nombre, dificultad, riesgo, ambientes))

    assert len(arenas) > 0
    return arenas


tributos = cargar_tributos()
objetos = cargar_objetos()
ambientes = cargar_ambientes()
arenas = cargar_arenas(ambientes)
