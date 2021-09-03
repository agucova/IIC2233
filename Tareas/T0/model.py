from __future__ import annotations

from datetime import datetime
from typing import List
from dataclasses import dataclass


@dataclass()
class User:
    username: str
    publications: List[int]

    def add_publication(self, pub_id: int):
        assert pub_id >= 0
        self.publications.append(pub_id)

    def remove_publication(self, pub_id: int):
        try:
            self.publications.remove(pub_id)
        except KeyError:
            raise KeyError(f"Publication {pub_id} not found for user {self.username}")


@dataclass(repr=True, frozen=True)
class Price:
    value: float
    # Just in case we go international!
    currency: str = "CLP"

    def __str__(self):
        # Reverts usual float formatting as it works
        # in the chilean locale
        display_value = (
            f"{self.value:,.2f}".replace(",", "%temp%")
            .replace(".", ",")
            .replace("%temp%", ".")
        )
        return f"${display_value} ({self.currency})"


@dataclass(repr=True)
class Publication:
    pub_id: int
    name: str
    description: str
    price: Price
    seller_username: str
    creation_date: datetime
    comments: List[Comment]


@dataclass(repr=True)
class Comment:
    pub_id: int
    username: str
    body: str
    creation_date: datetime
