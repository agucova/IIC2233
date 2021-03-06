"""
Este módulo implementa el procesador que gestiona todas las transiciones de estado del juego
y se asegura que el servidor y el cliente estén en sincronización.

Está diseñado para que la vasta mayoría del estado resida en el servidor.
"""

from __future__ import annotations

from typing import Any, Optional

from calamarlib.entities import Player
from PyQt5.QtCore import QObject, pyqtSignal

from client import Client


class GameProcessor(QObject):
    def __init__(self, client: Client):
        super().__init__()
        self.client = client
        self.username = None
        self.birthdate = None

    def check_user_data(self, username: str, birthdate: str):
        response = self.client.send_command(
            "check_user_data", username=username, birthdate=birthdate
        )
        if response is not None:
            return response["result"] is True

    def register_user(self, username: str, birthdate: str):
        self.username = username
        self.birthdate = birthdate
        response = self.client.send_command(
            "register_user", username=username, birthdate=birthdate
        )
        if response is not None:
            return response["result"] is True
        return False

    def get_players(self) -> Optional[list[dict[str, Any]]]:
        response = self.client.send_command("get_players")
        if response is not None:
            return response["result"]

    def challenge_player(self, username: str):
        response = self.client.send_command(
            "challenge_player", challenger=self.username, challenged=username
        )
        if response is not None:
            return response["result"] is True
