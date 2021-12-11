from __future__ import annotations

from calamarlib.helpers import load_config
from server import Server

if __name__ == "__main__":
    # Load parameters from configuration and pass host and port to server.
    host, port = load_config("servidor/parametros.json")

    server = Server(host, port)
    server.start()
