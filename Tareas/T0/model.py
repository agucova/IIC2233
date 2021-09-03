from __future__ import annotations

from datetime import datetime
from typing import Set, List
from dataclasses import dataclass


class User:
    def __init__(self, username: str):
        self.username = username
        self.publications: Set[int] = set()

    def __repr__(self) -> str:
        return f"User({self.username}): {len(self.publications)} publications."

    def add_publication(self, pub_id: int):
        self.publications.add(pub_id)

    def remove_publication(self, pub_id: int):
        try:
            self.publications.remove(pub_id)
        except KeyError:
            raise KeyError(f"Publication {pub_id} not found for user {self.username}")


@dataclass(repr=True)
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
