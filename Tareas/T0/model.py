from __future__ import annotations

from parametros import MIN_CARACTERES, MAX_CARACTERES
from datetime import datetime
from typing import Set
from dataclasses import dataclass


class User:
    def __init__(self, username: str, is_anonymous: bool):
        assert MIN_CARACTERES <= len(username) <= MAX_CARACTERES

        self.username = username
        self.is_anonymous = is_anonymous
        self.publications: Set[Publication] = set()

    def add_publication(self, publication: Publication):
        assert publication.seller == self
        self.publications.add(publication)

    def remove_publication(self, publication: Publication):
        try:
            self.publications.remove(publication)
        except KeyError:
            raise KeyError(f"Publication not found for user {self.username}")


@dataclass
class Price:
    value: int
    currency: str = "CLP"


@dataclass
class Publication:
    name: str
    description: str
    price: Price
    seller: User
    creation_date: datetime


@dataclass
class Comment:
    publication: Publication
    user: User
    body: str
    creation_date: datetime
