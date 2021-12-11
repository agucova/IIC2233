"""
Este modulo maneja la codificación y decodificación de mensajes entre el cliente y el servidor.
Valida extensamente los mensajes para evitar errores de codificación.
"""

from __future__ import annotations
from pickle import dumps, loads, UnpicklingError, PicklingError
from typing import Any, Sequence, Union
from encryption import pseudo_encrypt, pseudo_decrypt

LENGTH_SIZE = 4
N_BLOCK_SIZE = 4
CHUNK_SIZE = 80
PADDING_CHAR = b"\x00"


def chunked_read(seq, chunk_size: int):
    """Reads an arbitrary sequence in chunks of size chunk_size."""
    # REF: Thanks to https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
    # for a clean inspiration for this generator
    for i in range(0, len(seq), chunk_size):
        yield seq[i : i + chunk_size]


def estimate_size(original_length: int) -> int:
    """
    Estimate the size of the encoded message.
    (Not accounting for encryption)
    """
    n_chunks = original_length // CHUNK_SIZE + (original_length % CHUNK_SIZE > 0)
    return LENGTH_SIZE + n_chunks * (N_BLOCK_SIZE + CHUNK_SIZE)


def encode(obj: Any, encrypt=False) -> bytes:
    """
    Accepts an object and codifies it for network transmission.
    Optionally encrypting it.

    Format is:
    LENGTH (4, LE) | BLOCKS (LENGTH)

    And each block is composed as:
    N (4, BE) | DATA (80)
    with N being the length of the data, and DATA being padded with \x00 if necessary.

    """
    encoded_message = bytearray()
    # We start by encoding the Python object with Pickle
    try:
        content = dumps(obj) if not encrypt else pseudo_encrypt(dumps(obj))
    except PicklingError:
        raise ValueError("Unable to encode object, might not be serializable.")

    length = len(content)
    assert length > 0, "Empty content."

    # We then encoding the length of the message
    b_length = length.to_bytes(LENGTH_SIZE, byteorder="little")
    # Add the initial LENGTH (4, LE)
    encoded_message.extend(b_length)

    # Read the content chunk-for-chunk
    # And add each block to the encoded message
    for i, chunk in enumerate(chunked_read(content, CHUNK_SIZE)):
        # Add the number of the block
        # as N (4, BE)
        n = i.to_bytes(N_BLOCK_SIZE, byteorder="big")
        encoded_message.extend(n)

        # Add padding if necessary
        if len(chunk) < CHUNK_SIZE:
            chunk += PADDING_CHAR * (CHUNK_SIZE - len(chunk))
        # Append the chunk to the block
        encoded_message.extend(chunk)

    assert len(encoded_message) > 0, "Empty encoded message."
    assert len(encoded_message) == estimate_size(
        length
    ), "Encoded message has wrong length."
    # We make it inmutable before return
    return bytes(encoded_message)


def decode(byte_seq: Union[bytes, bytearray], encrypted=False) -> Any:
    assert len(byte_seq) > 0, "Empty byte sequence."
    assert (
        len(byte_seq) >= LENGTH_SIZE + N_BLOCK_SIZE + CHUNK_SIZE
    ), "Sequence seems too short to be a valid message."

    # We start by decoding the length of the message
    length = int.from_bytes(byte_seq[:LENGTH_SIZE], byteorder="little")
    assert (
        length <= len(byte_seq) <= length + CHUNK_SIZE - 1
    ), "The provided length is not consistent with the data."

    # We then decode the content
    content = bytearray()
    block_seq = byte_seq[LENGTH_SIZE:]

    for i, block in enumerate(chunked_read(block_seq, N_BLOCK_SIZE + CHUNK_SIZE)):
        # Read the number of the block
        n = int.from_bytes(block[:N_BLOCK_SIZE], byteorder="big")
        assert n == i, "Invalid block number."
        # Read the content of the block
        # Removing the padding if necessary
        if n * CHUNK_SIZE + CHUNK_SIZE > length:
            data = block[N_BLOCK_SIZE : N_BLOCK_SIZE + length % CHUNK_SIZE]
        else:
            data = block[N_BLOCK_SIZE:]

        content.extend(data)

    assert len(content) == length, "Invalid content length."

    # We try to decode the content with Pickle
    try:
        obj = loads(content) if not encrypted else loads(pseudo_decrypt(content))
    except UnpicklingError:
        raise ValueError("Unable to decode message, unknown encoding.")
    return obj


if __name__ == "__main__":
    # Test encoding
    print("Testing encoding...")
    obj = {"a": 1, "b": "hello", "c": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
    assert decode(encode(obj)) == obj
    assert decode(encode(obj, encrypt=True), encrypted=True) == obj
