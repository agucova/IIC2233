import os
import sys
from random import choice

from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication

# Agrego esto porque el código del enunciado
# Rompe la guía de descuentos y mi linter no me deja hacer el commit
# flake8: noqa: N802, N806


class VentanaPrincipal(QWidget):

    # Aquí debes crear una señal que usaras para enviar la jugada al back-end
    senal_enviar_jugada = pyqtSignal(dict)

    def __init__(self, *args):
        super().__init__(*args)
        self.crear_pantalla()
        # Valor de las cartas
        self.carta_infanteria = None
        self.carta_rango = None
        self.carta_artilleria = None

    def crear_pantalla(self):
        # Aquí deben crear la ventana vacia.
        self.setWindowTitle("DCCuent")
        # Es decir, agregar y crear labels respectivos a datos del juego, pero sin contenido
        # Si usas layout recuerda agregar los labels al layout y finalmente setear el layout
        # en la ventana.
        # Nombre de usuario
        self.label_usuario = QLabel()
        # Victorias y derrotas
        self.label_victorias = QLabel()
        self.label_derrotas = QLabel()
        # Teclas asociada a las cartas
        self.label_tecla_infanteria = QLabel()
        self.label_tecla_infanteria.setText("Q")
        self.label_tecla_rango = QLabel()
        self.label_tecla_rango.setText("W")
        self.label_tecla_artilleria = QLabel()
        self.label_tecla_artilleria.setText("E")
        # Cartas
        self.label_carta_infanteria = QLabel()
        self.label_carta_rango = QLabel()
        self.label_carta_artilleria = QLabel()
        # Definir tamaños de las cartas a 248x452
        self.label_carta_infanteria.setFixedSize(248, 452)
        self.label_carta_rango.setFixedSize(248, 452)
        self.label_carta_artilleria.setFixedSize(248, 452)
        # Layouts
        # Nombre de usuario, victorias y derrotas
        self.layout_info = QHBoxLayout()
        self.layout_info.addWidget(self.label_usuario)
        self.layout_info.addWidget(self.label_victorias)
        self.layout_info.addWidget(self.label_derrotas)
        # Teclas
        self.layout_teclas = QHBoxLayout()
        self.layout_teclas.addWidget(self.label_tecla_infanteria)
        self.layout_teclas.addWidget(self.label_tecla_rango)
        self.layout_teclas.addWidget(self.label_tecla_artilleria)
        # Cartas
        self.layout_cartas = QHBoxLayout()
        self.layout_cartas.addWidget(self.label_carta_infanteria)
        self.layout_cartas.addWidget(self.label_carta_rango)
        self.layout_cartas.addWidget(self.label_carta_artilleria)
        # Layout principal
        self.layout_principal = QVBoxLayout()
        self.layout_principal.addLayout(self.layout_info)
        self.layout_principal.addLayout(self.layout_teclas)
        self.layout_principal.addLayout(self.layout_cartas)
        # Setear el layout
        self.setLayout(self.layout_principal)

    def actualizar(self, datos):
        # Esta es la funcion que se encarga de actualizar el contenido de la ventana y abrirla
        # Recibe las nuevas cartas y la puntuación actual en un diccionario
        # Info
        self.label_usuario.setText(datos["usuario"])
        self.label_victorias.setText(str(datos["victorias"]))
        self.label_derrotas.setText(str(datos["derrotas"]))
        # Cartas
        self.label_carta_infanteria.setPixmap(QPixmap(datos["infanteria"]["ruta"]))
        self.label_carta_rango.setPixmap(QPixmap(datos["rango"]["ruta"]))
        self.label_carta_artilleria.setPixmap(QPixmap(datos["artilleria"]["ruta"]))
        # Valores de las cartas
        self.carta_infanteria = datos["infanteria"]
        self.carta_rango = datos["rango"]
        self.carta_artilleria = datos["artilleria"]

        # Al final, se muestra la ventana.
        self.show()

    def keyPressEvent(self, evento):
        # Aquí debes capturar la techa apretara,
        # y enviar la carta que es elegida

        # Si presionas la tecla Q, enviar la carta infanteria
        if None not in (self.carta_artilleria, self.carta_rango, self.carta_infanteria):
            if evento.key() == Qt.Key_Q:
                self.senal_enviar_jugada.emit(self.carta_infanteria)
                self.hide()
            # Si presionas la tecla W, enviar la carta rango
            elif evento.key() == Qt.Key_W:
                self.senal_enviar_jugada.emit(self.carta_rango)
                self.hide()
            # Si presionas la tecla E, enviar la carta artilleria
            elif evento.key() == Qt.Key_E:
                self.senal_enviar_jugada.emit(self.carta_artilleria)
                self.hide()


class VentanaCombate(QWidget):

    # Esta señal es para volver a la VentanaPrincipal con los datos actualizados
    senal_regresar = pyqtSignal(dict)
    # Esta señal envia a la ventana final con el resultado del juego
    senal_abrir_ventana_final = pyqtSignal(str)

    def __init__(self, *args):
        super().__init__(*args)
        self.crear_pantalla()

    def crear_pantalla(self):
        self.setWindowTitle("DCCuent")
        self.vbox = QVBoxLayout()
        self.layout_principal = QHBoxLayout()
        self.label_carta_usuario = QLabel()
        self.label_victoria = QLabel()
        self.label_carta_enemiga = QLabel()
        self.boton_regresar = QPushButton("Regresar")

        self.layout_principal.addWidget(self.label_carta_usuario)
        self.layout_principal.addWidget(self.label_victoria)
        self.layout_principal.addWidget(self.label_carta_enemiga)

        self.boton_regresar.clicked.connect(self.regresar)
        self.vbox.addLayout(self.layout_principal)
        self.vbox.addWidget(self.boton_regresar)

        self.setLayout(self.vbox)

    def mostrar_resultado_ronda(self, datos):
        self.datos = datos
        mensaje = datos["mensaje"]
        carta_enemiga = datos["enemigo"]
        carta_jugador = datos["jugador"]
        self.label_carta_usuario.setPixmap(
            QPixmap(carta_jugador["ruta"]).scaled(238, 452)
        )
        self.label_carta_enemiga.setPixmap(
            QPixmap(carta_enemiga["ruta"]).scaled(238, 452)
        )
        self.label_victoria.setText(mensaje)
        self.show()

    def regresar(self):
        resultado = self.datos["resultado"]
        if resultado == "victoria" or resultado == "derrota":
            self.senal_abrir_ventana_final.emit(resultado)
        else:
            self.senal_regresar.emit(self.datos)
        self.hide()


if __name__ == "__main__":

    def hook(type, value, traceback):
        print(type)
        print(traceback)

    sys.__excepthook__ = hook

    a = QApplication(sys.argv)
    ventana_principal = VentanaPrincipal()

    ventana_principal.show()
    sys.exit(a.exec())
