from __future__ import annotations
from typing import Sequence, List, Tuple, TypeVar

# Hablo de pseudo-encriptación porque nada sobre esto usa criptografía
# me siento rompiendo la primera ley de la criptografía,
# never roll your own crypto.

# También noto que manualmente estoy sobre-escribiendo la convención de
# nombre de variables de PEP8 en base a la convención usada en el enunciado (A, B, C, n)
# la siguiente linea permite que el código pase por mi chequeo automático :P
# flake8: noqa: N806

SeqVal = TypeVar("SeqVal")


def zigzag(
    sequence: Sequence[SeqVal],
) -> tuple[Sequence[SeqVal], Sequence[SeqVal], Sequence[SeqVal]]:
    """Converts a sequence to three lists grouping alternating items."""
    sequences = [], [], []
    for index, value in enumerate(sequence):
        sequences[index % 3].append(value)
    return sequences


def replace_3_5(plain_bytes: bytes) -> bytes:
    """Receives a byte sequence and replaces all \x03s with \x05s and viceversa"""
    plain_bytearray = bytearray(plain_bytes)
    # Using replace would be more elegant,
    # but I couldn't quite solve the temp variable problem.
    for index, byte in enumerate(plain_bytearray):
        if byte == 3:
            plain_bytearray = (
                plain_bytearray[:index] + b"\x05" + plain_bytearray[index + 1 :]
            )
        elif byte == 5:
            plain_bytearray = (
                plain_bytearray[:index] + b"\x03" + plain_bytearray[index + 1 :]
            )

    return bytes(plain_bytearray)


def pseudo_encrypt(plain_bytes: bytes) -> bytes:
    """Receives a byte sequence and encodes it using our protocol.
    We do not expect length to be included.
    We return a byte sequence in thes 'A B C n' or 'B A C n' format."""
    assert len(plain_bytes) >= 1
    A, B, C = map(bytes, zigzag(plain_bytes))
    if B[0] > C[0]:
        # Not sure if we're supposed to replace literal 3s to literal 5s
        # or their numeric representations.
        A, B, C = map(replace_3_5, (A, B, C))
        n = b"\x00"
        return A + B + C + n
    else:
        n = b"\x01"
        return B + A + C + n


def pseudo_decrypt(cipher_bytes: bytes) -> bytes:
    """Receives a pseudo-encrypted byte sequence and decodes it using our protocol.
    Notably, we expect the sequence to have the 'A B C n' or 'B A C n' format."""
    assert len(cipher_bytes) >= 2
    n = cipher_bytes[-1]
    if n == 0:
        A, B, C = map(bytes, zigzag(cipher_bytes[:-1]))
        A, B, C = map(replace_3_5, (A, B, C))
        return A + B + C
    elif n == 1:
        B, A, C = map(bytes, zigzag(cipher_bytes[:-1]))
        return B + A + C
    else:
        raise ValueError("Invalid n value")


# Testing
if __name__ == "__main__":
    # From the homework description
    example = b"\x05\x08\x03\x02\x04\x03\x05\x09"

    example_A = b"\x05\x02\x05"
    example_B = b"\x08\x04\t"
    example_C = b"\x03\x03"

    example_rep_A = b"\x03\x02\x03"
    example_rep_B = b"\x08\x04\t"
    example_rep_C = b"\x05\x05"

    example_encrypted = b"\x03\x02\x03\x08\x04\t\x05\x05\x00"

    # Test zigzag
    assert tuple(map(bytes, zigzag(example))) == (example_A, example_B, example_C)
    # Test replace_3_to_5
    assert replace_3_5(example_A) == example_rep_A
    assert replace_3_5(example_B) == example_rep_B
    assert replace_3_5(example_C) == example_rep_C
    # Test pseudo_encrypt
    assert pseudo_encrypt(example) == example_encrypted
    # Test pseudo_decrypt
    assert pseudo_decrypt(example_encrypted) == example
