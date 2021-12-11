from __future__ import annotations

import socket
import threading
import sys
from typing import Any

from calamarlib.encoding import encode, decode, LENGTH_SIZE


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        """
        Inicia el servidor.
        """
        print("[INFO] Inicializando servidor...")
        # We use REUSEADDR because we want to be able to restart the server
        # even if the socket is left in a TIME_WAIT state.
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.bind_and_listen()
        self.accept_connections()

    def bind_and_listen(self):
        """
        Enlaza el socket creado con el host y puerto indicado.

        Primero, se enlaza el socket y luego queda esperando
        por conexiones entrantes.
        """
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen()
        print(f"[INFO] Servidor escuchando en {self.host}:{self.port}...")

    def accept_connections(self):
        """
        Inicia el thread que aceptará clientes.

        Aunque podríamos aceptar clientes en el thread principal de la
        instancia, es útil hacerlo en un thread aparte. Esto nos
        permitirá realizar la lógica en la parte del servidor sin dejar
        de aceptar clientes. Por ejemplo, seguir procesando archivos.
        """
        thread = threading.Thread(target=self.accept_connections_thread)
        thread.start()

    def accept_connections_thread(self):
        """
        Es arrancado como thread para aceptar clientes.

        Cada vez que aceptamos un nuevo cliente, iniciamos un
        thread nuevo encargado de manejar el socket para ese cliente.
        """
        print("[INFO] Servidor aceptando conexiones...")

        while True:
            client_socket, _ = self.socket_server.accept()
            listening_client_thread = threading.Thread(
                target=self.listen_client_thread, args=(client_socket,)
            )
            listening_client_thread.start()

    @staticmethod
    def send(value: Any, sock: socket.socket):
        """
        Envía mensajes hacia algún socket cliente.

        Debemos implementar en este método el protocolo de comunicación
        donde los primeros 4 bytes indicarán el largo del mensaje.
        """
        sock.send(encode(value, encrypt=True))

    def listen_client_thread(self, client_socket: socket.socket):
        """
        Es ejecutado como thread que escuchará a un cliente en particular.

        Implementa las funcionalidades del protocolo de comunicación
        que permiten recuperar la informacion enviada.
        """
        print(f"[INFO] Recibido conexión de cliente #{client_socket.fileno()}.")

        while True:
            # The official python documentation suggests checking even
            # this kind of recv() call for full message receipt.
            # https://docs.python.org/3/library/socket.html#socket.socket.recv

            length_response = bytearray()
            while len(length_response) < LENGTH_SIZE:
                length_response.extend(client_socket.recv(LENGTH_SIZE))

            length = int.from_bytes(length_response, byteorder="big")
            response = bytearray()

            while len(response) < length:
                read_length = min(4096, length - len(response))
                response.extend(client_socket.recv(read_length))

            received = decode(response, encrypted=True)
            response = self.handle_command(received, client_socket)
            self.send(response, client_socket)

    def shutdown(self):
        """
        Cierra el socket de servidor y termina el programa.
        """
        print("[INFO] Cerrando servidor...")
        # Nos portaremos bien y haremos un shutdown primero
        self.socket_server.shutdown(socket.SHUT_RDWR)
        self.socket_server.close()
        sys.exit()

    def handle_command(self, received: dict[str, Any], client_socket: socket.socket):
        # Quien sabe, esto podria recibir URLs y empezaríamos a reimplementar HTTP
        # Hasta respondemos de forma RESTful!
        assert isinstance(received, dict), "El mensaje recibido no es un diccionario"
        assert (
            "command" in received.keys()
        ), "El mensaje recibido no tiene la clave 'command'"

        print("Comando recibido:", received["command"])
        # Este método debería ejecutar la acción y enviar una respuesta.
        return "Acción asociada a " + received["command"] + " ejecutada."
