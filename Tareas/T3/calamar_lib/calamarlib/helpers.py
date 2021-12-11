"""
Este módulo contiene funciones útiles para tareas comunes entre el cliente y el servidor.
"""
from __future__ import annotations

import json
import socket
from sys import exit


def load_config(filepath: str) -> tuple[str, int]:
    with open(filepath) as config_file:
        try:
            config = json.load(config_file)
        except json.JSONDecodeError:
            print("[FATAL] El archivo de configuración no es válido.")
            exit(1)

        host = config.get("host") or socket.gethostname()
        try:
            # A 4 digit port is a sane default
            port = int(config.get("port") or 4200)
        except TypeError:
            print("[FATAL] El puerto debe ser un número.")
            exit(1)

    return host, port
