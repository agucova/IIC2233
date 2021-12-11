"""
Este módulo sostiene la comunicación con el servidor en base a sockets.
Nótese que el cliente funciona de forma sincrónica.
"""

import socket
from typing import Any

from calamarlib.encoding import decode, encode
from calamarlib.protocol import VALID_COMMANDS
from PyQt5.QtCore import QObject, pyqtSignal


class Client(QObject):
    # Ref: Ejemplo de cliente en networking.ipynb
    """
    Maneja toda la comunicación desde el lado del cliente.

    Implementa el esquema de comunicación donde los primeros 4 bytes de cada
    mensaje indicarán el largo del mensaje enviado.
    """

    server_disconnect_signal = pyqtSignal()

    def __init__(self, host, port):
        super().__init__()
        print("[INFO] Inicializando cliente...")

        self.host = host
        self.port = port
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connect_to_server()
        except (ConnectionError, BrokenPipeError) as e:
            self.server_disconnect_signal.emit()

    def connect_to_server(self):
        """Crea la conexión al servidor."""
        self.socket_client.connect((self.host, self.port))
        print("[INFO] Cliente conectado exitosamente al servidor.")

    def send(self, msg: Any):
        """
        Envía mensajes al servidor.

        Implementa el mismo protocolo de comunicación que mencionamos;
        es decir, agregar 4 bytes al principio de cada mensaje
        indicando el largo del mensaje enviado.
        """
        # Nótese como nuestro paquete tienes dos LENGTH
        # Uno es el tamaño del mensaje completo, y el otro de
        # los datos contenidos en nuestro bytestream (msg)
        encoded_message = encode(msg, encrypt=True)
        length = len(encoded_message).to_bytes(4, byteorder="big")
        self.socket_client.sendall(length + encoded_message)

    def send_command(self, command, **content):
        """
        Envía un comando al servidor.

        `command` es el comando a enviar, y `content` es el contenido del
        mensaje.
        """
        assert command in VALID_COMMANDS, "Comando inválido."
        try:
            message = {"command": command, "arguments": {**content}}
            print(f"[INFO] Enviando mensaje: {message}")
            self.send(message)
            response = self.listen()
        except (ConnectionError, BrokenPipeError) as e:
            print(
                "[ERROR] El servidor se ha desconectado o no se ha podido conectarse."
            )
            self.server_disconnect_signal.emit()
            return None
        return response

    def listen(self):
        response_bytes_length = self.socket_client.recv(4)
        response_length = int.from_bytes(response_bytes_length, byteorder="big")
        response = bytearray()

        # Recibimos datos hasta que alcancemos la totalidad de los datos
        # indicados en los primeros 4 bytes recibidos.
        while len(response) < response_length:
            read_length = min(4096, response_length - len(response))
            response.extend(self.socket_client.recv(read_length))
        if response_length == 0:
            raise ConnectionError("No se recibió una respuesta del servidor.")
        message = decode(response, encrypted=True)

        print("[INFO] Recibido mensaje:", message)
        return message

    def repl(self):
        """
        Captura el input del usuario.

        Lee mensajes desde el terminal y después se pasan a `self.send()`.
        """

        print("------ Consola ------\n>>> ", end="")
        while True:
            msg = input()
            self.send({"command": "msg", "arguments": msg})
