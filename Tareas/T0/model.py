from __future__ import annotations

from datetime import datetime
from typing import Set
from dataclasses import dataclass


class User:
    def __init__(self, username: str, is_anonymous: bool):
        self.username = username
        self.is_anonymous = is_anonymous
        self.publications: Set[int] = set()

    def __repr__(self) -> str:
        return f"User({self.username}): {len(self.publications)} publications."

    def add_publication(self, pub_id: int):
        self.publications.add(pub_id)

    def remove_publication(self, pub_id: str):
        try:
            self.publications.remove(pub_id)
        except KeyError:
            raise KeyError(f"Publication not found for user {self.username}")


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
    seller: User
    creation_date: datetime


@dataclass(repr=True)
class Comment:
    publication: Publication
    user: User
    body: str
    creation_date: datetime
