from __future__ import annotations

from datetime import datetime
from typing import Set, List
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
    value: int
    # Just in case we go international!
    currency: str = "CLP"


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
