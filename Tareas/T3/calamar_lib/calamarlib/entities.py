"""
Este módulo establece entidades que el cliente y
el servidor deben poder interoperar.
"""

import datetime
from typing import Optional


class Player:
    def __init__(self, username: str, birth_date: datetime.date):
        self.username = username
        self.birth_date = birth_date
        self._marbles: int = 10
        self.won: bool = False
        self.playing_with: Optional[Player] = None

    @property
    def marbles(self) -> int:
        return self._marbles

    @marbles.setter
    def marbles(self, value: int):
        if value >= 20:
            self.won = True

        self._marbles = value

    @property
    def currently_playing(self) -> bool:
        return self.playing_with is not None
