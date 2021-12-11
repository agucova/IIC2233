from client import Client
from PyQt5.QtCore import QObject, pyqtSignal


class GameProcessor(QObject):
    def __init__(self, client: Client):
        super().__init__()
        self.client = client
        self.username = None
        self.birthdate = None

    def check_user_data(self, username: str, birthdate: str):
        response = self.client.send_command(
            "check_user_data", username=username, birthdate=birthdate
        )
        return response["result"] is True

    def register_user(self, username: str, birthdate: str):
        if self.check_user_data(username, birthdate):
            self.username = username
            self.birthdate = birthdate
            response = self.client.send_command(
                "register_user", username=username, birthdate=birthdate
            )
            return response["result"] is True
        return False
