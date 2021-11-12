import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication


class VentanaInicio(QMainWindow):
    def __init__(self):
        super(VentanaInicio, self).__init__()
        uic.loadUi("ventanas/inicio.ui", self)
        self.show()
        self.iniciar_partida.clicked.connect(self.abrir_juego)

    def abrir_juego(self):
        self.hide()
        usuario = self.usuario.text()
        self.juego = VentanaJuego(usuario)


class VentanaJuego(QMainWindow):
    def __init__(self, usuario):
        super(VentanaJuego, self).__init__()
        uic.loadUi("ventanas/juego.ui", self)
        self.show()


class VentanaRanking(QMainWindow):
    def __init__(self):
        super(VentanaRanking, self).__init__()
        uic.loadUi("ventanas/ranking.ui", self)
        self.show()


class VentanaPostNivel(QMainWindow):
    pass


if __name__ == "__main__":
    # def hook(type, value, traceback):
    #     print(type)
    #     print(traceback)
    # sys.__excepthook__ = hook

    app = QApplication([])
    inicio = VentanaInicio()

    sys.exit(app.exec_())
