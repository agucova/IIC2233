import sys

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

from parametros import ruta_logo


class VentanaInicial(QWidget):

    # Esta señal es para enviar un intento de nombre de usuario
    senal_revisar_nombre = pyqtSignal(str)

    def __init__(self, *args):
        super().__init__(*args)
        self.crear_pantalla()

    def crear_pantalla(self):
        self.setWindowTitle("Ventana Inicial DCCuent")
        # Layout principal
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        # Logo
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap(ruta_logo))
        # Texto de instrucciones
        self.texto_ingrese = QLabel("Ingrese su nombre de usuario:")
        # Input del usuario
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Debe ser alfanumérico")
        # Botón de ingreso
        self.boton_ingresar = QPushButton("Ingresar")
        self.boton_ingresar.clicked.connect(self.revisar_input)

        # Conectamos el return del input a ingresar para mejorar la UX
        self.input_usuario.returnPressed.connect(self.revisar_input)

        # Layout del texto y la caja de input
        hbox = QHBoxLayout()
        hbox.addWidget(self.texto_ingrese)
        hbox.addWidget(self.input_usuario)

        # Ahora agrego todo al layout principal
        vbox.addWidget(self.logo)
        vbox.addLayout(hbox)
        vbox.addWidget(self.boton_ingresar)

        # Ahora muestro la ventana
        self.show()

    def revisar_input(self):
        # Aquí deben enviar el nombre de usuario, para verificar si es un usuario valido
        # Para esto utilizar senal_revisar_nombre
        self.senal_revisar_nombre.emit(self.input_usuario.text())

    def recibir_revision(self, error):
        # Resetea la ventana si es que ocurre algun error,en caso contrario comienza el juego
        # IMPORTANTE la caja de text debe llamarse input_usuario
        if error:
            self.input_usuario.clear()
            self.input_usuario.setPlaceholderText("¡Inválido! Debe ser alfa-numérico.")
        else:
            usuario = self.input_usuario.text()
            self.hide()


if __name__ == "__main__":

    def hook(type, value, traceback):
        print(type)
        print(traceback)

    sys.__excepthook__ = hook

    a = QApplication(sys.argv)
    ventana_inicial = VentanaInicial()

    ventana_inicial.show()
    sys.exit(a.exec())
