from __future__ import annotations
import datetime
from typing import Any, Optional

from calamarlib.protocol import VALID_COMMANDS
from calamarlib.entities import Player


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

    def check_username(self, username: str) -> bool:
        already_used = [player.username for player in self.players]
        return len(username) > 1 and username.isalnum() and username not in already_used

    @staticmethod
    def check_date(date_str: str) -> bool:
        return GameProcessor.str_to_date(date_str) is not None

    def check_user_data(self, username: str, birthdate: str) -> bool:
        return self.check_username(username) and GameProcessor.check_date(birthdate)

    def register_user(self, username: str, birthdate: str) -> bool:
        if self.check_user_data(username, birthdate):
            player = Player(username, GameProcessor.str_to_date(birthdate))  # type: ignore
            self.players.append(player)
            print(f"[INFO] Se registró al jugador {player.username}.")
            return True
        return False

    def get_players(self) -> list[dict[str, Any]]:
        return [
            {"username": player.username, "currently_playing": player.currently_playing}
            for player in self.players
        ]

    def get_player(self, username: str) -> Optional[Player]:
        for player in self.players:
            if player.username == username:
                return player
        return None

    def challenge_player(self, challenger: str, challenged: str) -> bool:
        print(
            f"[INFO] El jugador {challenger} está desafiando al jugador {challenged}."
        )
        challenger_player = self.get_player(challenger)
        challenged_player = self.get_player(challenged)
        if challenger_player is None or challenged_player is None:
            return False
        if challenger_player.currently_playing or challenged_player.currently_playing:
            return False
        challenger_player.playing_with = challenged_player
        challenged_player.playing_with = challenger_player
        return True

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
            elif command == "get_players":
                return {"result": self.get_players()}
            elif command == "challenge_player":
                return {"result": self.challenge_player(**arguments)}
            else:
                return {"error": "Command not implemented."}
        except (TypeError, ValueError) as e:
            print(f"[WARNING] El comando {command} no se pudo ejecutar.")
            return {"error": str(e)}
