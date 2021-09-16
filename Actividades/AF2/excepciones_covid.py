class RiesgoCovid(Exception):
    def __init__(self, sintoma: str, nombre_invitade: str):
        self.sintoma = sintoma
        self.nombre_invitade = nombre_invitade

    def alerta_de_covid(self):
        if self.sintoma == "fiebre":
            print(
                f"La persona {self.nombre_invitade} tiene fiebre y tiene prohibido el ingreso"
            )
        elif self.sintoma == "dolor_cabeza":
            print(
                f"La persona {self.nombre_invitade} tiene dolor de cabeza y tiene prohibido el ingreso"
            )
        elif self.sintoma == "tos":
            print(
                f"La persona {self.nombre_invitade} tiene tos y tiene prohibido el ingreso"
            )
