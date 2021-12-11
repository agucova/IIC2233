import socket
import threading
from typing import Any

from calamarlib.encoding import decode, encode


class Client:
    """
    Maneja toda la comunicación desde el lado del cliente.

    Implementa el esquema de comunicación donde los primeros 4 bytes de cada
    mensaje indicarán el largo del mensaje enviado.
    """

    def __init__(self, host, port):
        print("[INFO] Inicializando cliente...")

        self.host = host
        self.port = port
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connect_to_server()
        self.listen()

    def connect_to_server(self):
        """Crea la conexión al servidor."""

        self.socket_client.connect((self.host, self.port))
        print("Cliente conectado exitosamente al servidor.")

    def listen(self):
        """
        Inicializa el thread que escuchará los mensajes del servidor.

        Es útil hacer un thread diferente para escuchar al servidor,
        ya que de esa forma podremos tener comunicación asíncrona con este.
        Luego, el servidor nos podrá enviar mensajes sin necesidad de
        iniciar una solicitud desde el lado del cliente.
        """

        thread = threading.Thread(target=self.listen_thread, daemon=True)
        thread.start()

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

    def send_command(self, command, content):
        """
        Envía un comando al servidor.

        `command` es el comando a enviar, y `content` es el contenido del
        mensaje.
        """

        self.send({"command": command, "content": content})

    def listen_thread(self):
        while True:
            response_bytes_length = self.socket_client.recv(4)
            response_length = int.from_bytes(response_bytes_length, byteorder="big")
            response = bytearray()

            # Recibimos datos hasta que alcancemos la totalidad de los datos
            # indicados en los primeros 4 bytes recibidos.
            while len(response) < response_length:
                read_length = min(4096, response_length - len(response))
                response.extend(self.socket_client.recv(read_length))

            print(f"{decode(response, encrypted=True)}\n>>> ", end="")

    def repl(self):
        """
        Captura el input del usuario.

        Lee mensajes desde el terminal y después se pasan a `self.send()`.
        """

        print("------ Consola ------\n>>> ", end="")
        while True:
            msg = input()
            self.send({"command": "msg", "content": msg})
