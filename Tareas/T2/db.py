from __future__ import annotations
from typing import Iterator


def load_scores(filepath: str) -> Iterator[tuple[str, int]]:
    """Iterator that loads scores at filepath and yields username, score tuples.
    Creates an empty score list if no file is found."""
    try:
        with open(filepath) as f:
            lines = f.readlines()
    except FileNotFoundError:
        # Create file
        with open(filepath, "w") as f:
            f.write("")
            lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        username, score = line.split(",")
        yield username, int(score)


def add_score(filepath: str, username: str, score: int):
    """Adds a score to the file at filepath."""
    try:
        with open(filepath, "a") as f:
            f.write(f"{username},{score}\n")
    except FileNotFoundError:
        with open(filepath, "w") as f:
            f.write(f"{username},{score}\n")
