import sys

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsView,
    QMainWindow,
    QMessageBox,
)

import parametros as p
from db import load_scores
from state import GameState, Processor
from froggy_and_objects import FroggyView, SpecialObjectsView
from games import RoadGameView, RiverGameView


class VentanaInicio(QMainWindow):
    def __init__(self):
        super(VentanaInicio, self).__init__()
        uic.loadUi("ventanas/inicio.ui", self)
        self.show()
        self.start_game.clicked.connect(self.open_game)
        self.see_ranking.clicked.connect(self.open_ranking)

    def open_game(self):
        usuario: str = self.usuario.text()
        if (
            usuario
            and usuario.isalnum()
            and p.MIN_CARACTERES <= len(usuario) <= p.MAX_CARACTERES
        ):
            self.hide()
            self.juego = VentanaJuego(usuario)
        else:
            error = (
                f"El usuario debe ser alfanumérico"
                f" y tener entre {p.MIN_CARACTERES} y {p.MAX_CARACTERES} caracteres."
            )
            QMessageBox.warning(self, "Error", error)

    def open_ranking(self):
        self.hide()
        self.ranking = VentanaRanking()
        self.ranking.return_home.clicked.connect(self.close_ranking)
        self.ranking.show()

    def close_ranking(self):
        self.ranking.close()
        self.show()


class VentanaRanking(QMainWindow):
    def __init__(self):
        super(VentanaRanking, self).__init__()
        self.lista_ranking = []
        uic.loadUi("ventanas/ranking.ui", self)
        self.show()

        # Load scores, rank them and set the text in the inner, markdown label.
        scores = sorted(load_scores(p.PUNTAJES_PATH), key=lambda x: x[1], reverse=True)[
            :5
        ]
        ranking = [
            f"{i}. {username}, {score}" for i, (username, score) in enumerate(scores)
        ]
        self.texto_ranking.setText("\n".join(ranking))


class VentanaJuego(QMainWindow):
    def __init__(self, username):
        super(VentanaJuego, self).__init__()

        # Initialize basic UI elements
        self.init_ui()
        # Initialize main processor from the back-end
        # and load initial values
        self.processor = Processor(username)
        self.update_parameters(self.processor.state)
        # Initialize the game views
        self.init_games()
        # Initialize the froggy view
        self.init_froggy_and_objects()
        # Connect signals
        self.init_signals()

    def init_ui(self):
        uic.loadUi("ventanas/juego.ui", self)

        self.scene_x = 20
        self.scene_y = 330
        self.scene_width = 1040
        self.scene_height = 560

        self.scene = QGraphicsScene(
            self.scene_x, self.scene_y, self.scene_width, self.scene_height
        )

        self.view = QGraphicsView(self.scene, self)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.grabKeyboard()

        self.scene_container.addWidget(self.view)

        self.show()
        self.activateWindow()

    def init_games(self):
        self.paint_scene_background("sprites/Mapa/areas/scene_frame.png")
        self.road_game_down = RoadGameView(
            self.scene,
            self.processor,
            self.scene_x,
            self.scene_y,
            self.scene_width,
            self.scene_height,
            "down",
        )
        self.road_game_up = RoadGameView(
            self.scene,
            self.processor,
            self.scene_x,
            self.scene_y,
            self.scene_width,
            self.scene_height,
            "up",
        )

        self.river_game = RiverGameView(
            self.processor,
            self.scene,
            self.scene_x,
            self.scene_y,
            self.scene_width,
            self.scene_height,
        )

    def init_froggy_and_objects(self):
        self.froggy = FroggyView(
            self.processor,
            self.scene,
            self.view,
            self.scene_x,
            self.scene_y,
            self.scene_width,
            self.scene_height,
        )

        self.objects = SpecialObjectsView(
            self.processor,
            self.froggy.item,
            self.scene,
            self.scene_x,
            self.scene_y,
            self.scene_width,
            self.scene_height,
        )

    def init_signals(self):
        # Wire up signals from the back-end to the front-end and vice-versa
        # Parameter update signal
        self.processor.parameter_change_signal.connect(self.update_parameters)

        # Pause-unpause signal
        self.froggy.pause_or_unpause_signal.connect(self.pause_or_unpause)

        # Level start signals
        self.processor.level_start_signal.connect(self.processor.play_or_resume)
        self.processor.level_start_signal.connect(self.empezar.hide)

        # Game over signal
        self.processor.game_over_signal.connect(self.open_post_level)

        # Collision detection signals
        self.road_game_down.player = self.froggy.item
        self.road_game_up.player = self.froggy.item
        self.river_game.player = self.froggy.item
        self.road_game_down.collision_signal.connect(self.froggy.collision)
        self.road_game_up.collision_signal.connect(self.froggy.collision)
        self.objects.collision_signal.connect(self.processor.use_special_object)
        self.river_game.fall_signal.connect(self.froggy.collision)

        # Level finished signals
        self.froggy.level_finished_signal.connect(self.processor.pause)
        self.froggy.level_finished_signal.connect(self.objects.clear_objects)
        self.froggy.level_finished_signal.connect(self.open_post_level)

        # Buttons
        self.boton_salir.clicked.connect(self.save_and_close)
        self.boton_pausar.clicked.connect(self.pause_or_unpause)

        # Note: Post-level signals are found on open_post_level.

    def update_parameters(self, state: GameState):
        self.valor_vidas.setText(str(state.lives_left))
        self.valor_puntaje.setText(str(state.total_score))
        self.valor_nivel.setText(str(state.level))
        self.valor_monedas.setText(str(state.coins))
        self.valor_tiempo.setText(str(state.remaining_time))

    def paint_scene_background(self, path):
        """Scales and adds the given background to the Graphics Scene."""
        background = QGraphicsPixmapItem(
            QPixmap(path).scaled(self.scene_width, self.scene_height)
        )
        background.setOffset(self.scene_x, self.scene_y)
        self.scene.addItem(background)

    def pause_or_unpause(self):
        self.processor.pause_or_unpause()
        if self.processor.is_paused:
            self.boton_pausar.setText("Resumir")
        else:
            self.boton_pausar.setText("Pausar")

    def open_post_level(self):
        self.processor.calculate_score()
        self.froggy.send_to_start()
        self.hide()
        self.post_nivel = VentanaPostNivel(self.processor.state)
        # Post-level signals
        # Must be wired up here due to on demand instantiation
        self.post_nivel.next_level_signal.connect(self.close_post_level)
        self.post_nivel.next_level_signal.connect(
            self.froggy.processor.level_start_signal.emit
        )
        self.post_nivel.next_level_signal.connect(self.processor.next_level)
        self.post_nivel.next_level_signal.connect(self.empezar.show)
        self.post_nivel.next_level_signal.connect(self.froggy.next_level)
        self.post_nivel.exit.clicked.connect(self.save_and_close)

    def close_post_level(self):
        self.post_nivel.close()
        self.show()

    def save_and_close(self):
        self.processor.save_total_score()
        sys.exit()


class VentanaPostNivel(QMainWindow):
    next_level_signal = pyqtSignal()

    def __init__(self, state: GameState):
        super(VentanaPostNivel, self).__init__()
        uic.loadUi("ventanas/post-nivel.ui", self)

        # Load the game state to the labels
        self.level.setText(str(state.level))
        self.total_score.setText(str(state.total_score))
        self.level_score.setText(str(state.level_score))
        self.lives_left.setText(str(state.lives_left))
        self.coins.setText(str(state.coins))

        if not state.alive:
            self.keep_playing.setText("No puedes seguir jugando, porque perdiste :(")
            self.next_level.setEnabled(False)
        else:
            self.keep_playing.setText("Pasaste este nivel. Sigue jugando!")
            self.next_level.setEnabled(True)

        self.show()

        # TODO: Check connection
        self.next_level.clicked.connect(self.next_level_signal.emit)


if __name__ == "__main__":
    app = QApplication([])
    inicio = VentanaInicio()

    sys.exit(app.exec_())
