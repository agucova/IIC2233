class RiesgoCovid(Exception):
    def __init__(self, sintoma: str, nombre_invitade: str):
        assert sintoma in ("fiebre", "dolor_cabeza", "tos")
        self.sintoma = sintoma
        self.nombre_invitade = nombre_invitade
        super().__init__("Se encontró riesgo COVID-19.")

    def alerta_de_covid(self):
        if self.sintoma == "fiebre":
            print(
                f"La persona {self.nombre_invitade} tiene fiebre y tiene prohibido el ingreso"
            )
        elif self.sintoma == "dolor_cabeza":
            print(
                f"La persona {self.nombre_invitade} tiene dolor de cabeza y "
                f"tiene prohibido el ingreso"
            )
        elif self.sintoma == "tos":
            print(
                f"La persona {self.nombre_invitade} tiene tos y tiene prohibido el ingreso"
            )
