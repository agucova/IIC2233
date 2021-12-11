from __future__ import annotations
from dataclasses import dataclass
import datetime
from typing import Any, Optional

from calamarlib.protocol import VALID_COMMANDS


@dataclass
class Player:
    username: str
    birth_date: datetime.date


class GameProcessor:
    def __init__(self):
        self.players: list[Player] = []

    @staticmethod
    def str_to_date(date_str: str) -> Optional[datetime.date]:
        # Format is dd/MM/yyyy
        try:
            day, month, year = map(int, date_str.split("/"))
        except ValueError:
            print("[WARNING] Invalid date format received.")
            return None

        return datetime.date(year, month, day)

    @staticmethod
    def check_username(username: str) -> bool:
        return len(username) > 1 and username.isalnum()

    @staticmethod
    def check_date(date_str: str) -> bool:
        return GameProcessor.str_to_date(date_str) is not None

    @staticmethod
    def check_user_data(username: str, birthdate: str) -> bool:
        return GameProcessor.check_username(username) and GameProcessor.check_date(
            birthdate
        )

    def register_user(self, username: str, birthdate: str) -> bool:
        if GameProcessor.check_user_data(username, birthdate):
            player = Player(username, GameProcessor.str_to_date(birthdate))  # type: ignore
            self.players.append(player)
            print(f"[INFO] Se registró al jugador {player.username}.")
            return True
        return False

    def handle_command(
        self, command: str, arguments: dict["str", Any]
    ) -> dict[str, Any]:
        if command not in VALID_COMMANDS:
            return {"error": "Invalid command"}
        try:
            if command == "check_user_data":
                return {"result": self.check_user_data(**arguments)}
            elif command == "register_user":
                return {"result": self.register_user(**arguments)}
            else:
                return {"error": "Command not implemented."}
        except (TypeError, ValueError) as e:
            print(f"[WARNING] El comando {command} no se pudo ejecutar.")
            return {"error": str(e)}
