import sys
from time import sleep

import cv2
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QColor, QImage, QFont, QFontDatabase
from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import (
#     QApplication,
#     QLabel,
#     QMainWindow,
#     QPushButton,
#     QVBoxLayout,
#     QHBoxLayout,
#     QWidget,
#     QProgressBar, QGroupBox,
# )
from PyQt5.QtWidgets import *
import random

# https://www.pythonguis.com/tutorials/creating-your-own-custom-widgets/
from datetime import datetime
import logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
                    handlers=[logging.FileHandler(f"log\\{datetime.utcnow().strftime('%Y-%m-%dT%H_%M_%S')}.log"),
                              logging.StreamHandler()])
logger = logging.getLogger(__name__)

from pokebot.fight import OwnPokemon

# Step 1: Create a worker class
class Worker(QObject):
    finished = pyqtSignal()
    execute_command_arg = None  # set this variable to a command

    def run(self):
        """Long-running task."""
        try:
            import from_saved_state8
        except Exception:
            logger.info(f"Uncaught backend error: ", exc_info=True)
            raise
        self.finished.emit()  # tell the main thread that we are done

    def execute_command(self):
        from pokebot.combiner import go_to, talk
        print(f"Executing: {self.execute_command_arg}")
        try:
            exec(self.execute_command_arg)
        except Exception:
            logger.error(f"Uncaught backend error: ", exc_info=True)
        print(f"Command executed")
        self.finished.emit()  # tell the main thread that we are done



# class Pokemon(QtWidgets.QWidget):
#     pass

def shadow_image(img):
    ''''Takes and returns a cv2 image with black color but opacity intact.

    It is used to shade the badges that are not yet obtained by the player.'''
    h = img.shape[0]
    w = img.shape[0]
    for y in range(h):
        for x in range(w):
            if img[y, x, 3] != 0: # where the opacity is 0 (so not the background)
                img[y, x, :3] = [0, 0, 0]  # set the color to black (nor the opacity to 0!)
    return img




class Window(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_timer()

        QFontDatabase.addApplicationFont('Pokemon GB.ttf')

    def convert_cv_qt_pixelmap(self, cv_img):
        ''''Converts a open cv image to a qt pixmap.'''

        h, w, ch = cv_img.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format_RGBA8888)
        return QPixmap.fromImage(convert_to_Qt_format)

    def setup_ui(self):
        self.setWindowTitle("Pokebot")
        self.setGeometry(300, 100, 900, 1000) # x0, y0, width, height

        command_groupbox = QGroupBox(self.tr("Command line"))
        self.command_textbox = QLineEdit("go_to(('route4', 902))")
        self.command_btn = QPushButton("Run command")
        self.command_btn.setFont(QFont('Pokemon GB'))
        self.command_btn.clicked.connect(self.run_command)
        textbox_layout = QVBoxLayout()
        textbox_layout.addWidget(self.command_textbox)
        textbox_layout.addWidget(self.command_btn)
        command_groupbox.setLayout(textbox_layout)

        # Initiate badge section
        self.badgesLabels = list()
        for b in ['bolder_badge', 'cascade_badge', 'thunder_badge', 'rainbow_badge', 'soul_badge', 'marsh_badge',
                  'volcano_badge', 'earth_badge']:
            badge_label = QLabel(self)
            img = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\dashboard\\assets\\' + b + '.png',
                             cv2.IMREAD_UNCHANGED)
            pixmap = self.convert_cv_qt_pixelmap(shadow_image(img))
            # pixmap = QPixmap('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\dashboard\\assets\\' + b + '.png')
            pixmap.scaled(128, 128)
            # pixmap.fill(QColor(0, 0, 0))
            badge_label.setPixmap(pixmap)
            self.badgesLabels.append(badge_label)

        # Add the badges to a box
        badges_groupbox = QGroupBox(self.tr("Badges"))
        badges_layout = QGridLayout()
        for i in range(8):
            badges_layout.addWidget(self.badgesLabels[i], int(i / 4 + 1), i % 4 + 1)
        badges_groupbox.setLayout(badges_layout)


        # Initiate button section
        self.start_vba_btn = QPushButton("Open VBA", self)
        self.start_vba_btn.setFont(QFont('Pokemon GB'))
        self.start_vba_btn.clicked.connect(self.start_vba)  # link th button to the start VBA function

        self.new_game_btn = QPushButton("Start New Game!", self)
        self.new_game_btn.setFont(QFont('Pokemon GB'))
        self.new_game_btn.setGeometry(20, 15, 10, 40)
        self.new_game_btn.clicked.connect(self.runLongTask)

        self.load_btn = QPushButton("Load saved game 8", self)
        self.load_btn.setFont(QFont('Pokemon GB'))
        self.load_btn.setGeometry(20, 15, 10, 40)
        self.load_btn.clicked.connect(self.load_game8)

        # Add buttons to a box
        buttonGroupBox = QGroupBox(self.tr("Button options"))
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.start_vba_btn)
        button_layout.addWidget(self.new_game_btn)
        button_layout.addWidget(self.load_btn)
        buttonGroupBox.setLayout(button_layout)


        # Initiate party section
        self.pokemon_labels = list()
        self.hp_bars = list()
        self.pp_bars = {}
        self.pokemon_groupboxes = []
        self.all_move_labels = {}
        for i in range(6):
            # pokemon image
            pokemon_label = QLabel(self)
            pixmap = QPixmap('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\dashboard\\assets\\' + 'poke_ball.png')
            pixmap.scaled(64, 64)
            pokemon_label.setPixmap(pixmap)
            self.pokemon_labels.append(pokemon_label)

            # pokemon hpBar
            hp_progressbar = QProgressBar(self)
            hp_progressbar.setStyleSheet(
                " QProgressBar { text-align: center; } QProgressBar::chunk {background-color: #3add36; width: 1px;}")
            hp_progressbar.setValue(100)
            hp_progressbar.setFormat('HP bar')
            hp_progressbar.adjustSize()
            self.hp_bars.append(hp_progressbar)

            # pokemon moves
            # moves_group_box = QGroupBox(self.tr("Moves"))
            moves_grid_layout = QGridLayout()
            moves = list()
            self.pp_bars[i] = []
            self.all_move_labels[i] = []
            for j in range(4):
                # PP bar
                pp_progressbar = QProgressBar(self)
                pp_progressbar.setStyleSheet(
                    " QProgressBar { text-align: center; height: 2px } QProgressBar::chunk {background-color: #7D94B0; width: 1px; height: 2px;}")
                pp_progressbar.setValue(50)
                pp_progressbar.setFormat('PP bar')
                self.pp_bars[i].append(pp_progressbar)

                single_move_layout = QVBoxLayout()
                single_move_groupbox = QGroupBox()
                m = QLabel(self)
                m.setText(f'move {j}')
                self.all_move_labels[i].append(m)
                single_move_layout.addWidget(m)
                single_move_layout.addStretch(4)
                single_move_layout.addWidget(pp_progressbar)
                single_move_layout.addStretch(1)
                single_move_groupbox.setLayout(single_move_layout)
                moves_grid_layout.addWidget(single_move_groupbox, int(j / 2 + 1), j % 2)
                moves.append(m)
            moves_grid_layout.setColumnStretch(0, 1)
            moves_grid_layout.setColumnStretch(1, 1)
            # moves_group_box.setLayout(moves_grid_layout)

            # combine progressbar and moves
            hp_and_moves_layout = QVBoxLayout()
            hp_and_moves_layout.addWidget(hp_progressbar)
            hp_and_moves_layout.addLayout(moves_grid_layout)

            # combine pokemon label, image, hp and moves
            pokemon_groupbox = QGroupBox(self.tr(f"Pokemon {i}"))
            pokemon_layout = QHBoxLayout()
            pokemon_layout.addWidget(pokemon_label, stretch=1)
            pokemon_layout.addLayout(hp_and_moves_layout, stretch=2)
            pokemon_groupbox.setLayout(pokemon_layout)
            self.pokemon_groupboxes.append(pokemon_groupbox)

        # combine to make a party box
        party_groupbox = QGroupBox(self.tr("Party"))
        grid_layout = QGridLayout()
        for i in range(6):
            row = int(i / 2 + 1)
            col = i % 2
            grid_layout.addWidget(self.pokemon_groupboxes[i], row, col)  # left -> right, up->down
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)
        party_groupbox.setLayout(grid_layout)

        # total layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(badges_groupbox, alignment=1)
        main_layout.addWidget(buttonGroupBox, alignment=1)
        main_layout.addWidget(party_groupbox, alignment=2)
        main_layout.addWidget(command_groupbox, alignment=1)

        self.central_widget = QWidget()
        self.central_widget.setLayout(main_layout)
        self.setCentralWidget(self.central_widget)


    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(500)  # set the reset frequency in milli seconds

    def update_gui(self):
        ''''Updates the gui. '''

        try:
            assets_folder = 'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\dashboard\\assets\\'

            for i in range(6):
                if i >= len(OwnPokemon.party):
                    # no pokemon choose non pokemon view
                    self.pokemon_labels[i].setPixmap(QPixmap(assets_folder + 'poke_ball' + '.png').scaled(90, 90))
                    self.pokemon_groupboxes[i].setTitle('--')

                    self.hp_bars[i].setValue(0)

                    # all moves should be none
                    for k in range(4):
                        self.pp_bars[i][k].setValue(0)
                        self.all_move_labels[i][k].setText('--')
                else:
                    pokemon = OwnPokemon.party[i]
                    self.pokemon_labels[i].setPixmap(QPixmap(assets_folder + str(pokemon.name) + '.png').scaled(128, 128))
                    self.pokemon_groupboxes[i].setTitle(pokemon.own_name + '   L:' + str(pokemon.level))
                    hp_percentage = int(100 * pokemon.current_hp / int(pokemon.stats['hp']))
                    self.hp_bars[i].setValue(hp_percentage)
                    if hp_percentage < 15:
                        self.hp_bars[i].setStyleSheet(
                            " QProgressBar { text-align: center; } QProgressBar::chunk {background-color: red;}")
                    else:
                        self.hp_bars[i].setStyleSheet(
                            " QProgressBar { text-align: center; } QProgressBar::chunk {background-color: #3add36;}")

                    for j in range(4):
                        if j >= len(pokemon.moves):
                            # no move
                            self.pp_bars[i][j].setValue(0)
                            self.all_move_labels[i][j].setText('--')
                        else:
                            move = pokemon.moves[j]
                            self.all_move_labels[i][j].setText(move.name)
                            self.pp_bars[i][j].setValue(int(100 * move.pp / move.max_pp))


            from pokebot.gameplay.item import Items
            badges = [{'name': 'bolder_badge', 'have': Items.do_i_have('bolder badge')},
                      {'name': 'cascade_badge', 'have': Items.do_i_have('cascade badge')},
                      ]

            for badge_dict, badge_label in zip(badges, self.badgesLabels):
                if badge_dict['have']:
                    badge_label.setPixmap(QPixmap(assets_folder + str(badge_dict['name']) + '.png'))

        except Exception:
            logger.error(f"Uncaught frontend error: ", exc_info=True)
            raise

    def start_vba(self):
        from pokebot.fundamentals import open_vba
        open_vba()

    def load_game8(self):
        try:
            import load_saved_game8
        except Exception:
            logger.error(f"error: ", exc_info=True)

    def run_command(self):
        # Step 2: Create a QThread object

        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        self.worker.execute_command_arg = self.command_textbox.text()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.execute_command)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.new_game_btn.setEnabled(False)
        self.command_btn.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.new_game_btn.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.command_btn.setEnabled(True)
        )


    def runLongTask(self):
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.new_game_btn.setEnabled(False)
        self.command_btn.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.new_game_btn.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.command_btn.setEnabled(True)
        )




if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())