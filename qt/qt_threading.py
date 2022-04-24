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
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
                    handlers=[logging.FileHandler(f"log\\{datetime.utcnow().strftime('%Y-%m-%dT%H_%M_%S')}.log"),
                              logging.StreamHandler()])

from pokebot.fight import OwnPokemon

# Step 1: Create a worker class
class Worker(QObject):
    finished = pyqtSignal()
    # progress = pyqtSignal(int)

    def run(self):
        """Long-running task."""

        import from_new_game

        # for i in range(5):
        #     sleep(1)
        #     self.progress.emit(i + 1)
        # self.finished.emit()

class Pokemon(QtWidgets.QWidget):
    pass

def shadow_image(img):
    ''''cv2 image comes in and goes out '''
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
        self.clicksCount = 0
        self.setupUi()
        self.setupTimer()

        QFontDatabase.addApplicationFont('Pokemon GB.ttf')

    def convert_cv_qt_pixelmap(self, cv_img):
        h, w, ch = cv_img.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(
            cv_img.data, w, h, bytes_per_line, QImage.Format_RGBA8888
        )
        # p = convert_to_Qt_format.scaled(
        #     self.disply_width, self.display_height, Qt.KeepAspectRatio
        # )
        return QPixmap.fromImage(convert_to_Qt_format)

    # def partyBox(self):
    #     partyGroupBox = QGroupBox(self.tr("Party"))
    #     grid_layout = QGridLayout()
    #     for i, p in enumerate(['charmander', 'bulbasaur']): # , 'vulpix', 'pidgey'
    #         col_num = i%2
    #         row_num = int(i/2+1)
    #         widget = self.pokeBox(p)
    #         grid_layout.addWidget(widget, row_num, col_num)
    #     grid_layout.setColumnStretch(0, 1)
    #     grid_layout.setColumnStretch(1, 1)
    #     return partyGroupBox.setLayout(grid_layout)
    #
    # def pokeBox(self, pokemon_name):
    #     print(f"Adding {pokemon_name}")
    #     pokemonGroupBox = QGroupBox(self.tr(pokemon_name))
    #     layout = QHBoxLayout()
    #
    #     layout.addWidget(self.pokemon_label, stretch=1)
    #     layout.addWidget(self.pbar, stretch=6)
    #     return pokemonGroupBox.setLayout(layout)




    def setupUi(self):
        self.setWindowTitle("Pokebot")
        self.setGeometry(300, 100, 900, 1000) # x0, y0, width, height


        # Create and connect widgets
        # self.clicksLabel = QLabel("Pokemon", self)
        # self.clicksLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.start_vba_btn = QPushButton("Open VBA", self)
        self.start_vba_btn.setFont(QFont('Pokemon GB'))
        # self.countBtn.setGeometry(20, 15, 10, 40)
        self.start_vba_btn.clicked.connect(self.start_vba)

        # self.openvbaBtn = QPushButton("Start VBA", self)
        # self.openvbaBtn.clicked.connect(self.start_vba)

        self.stepLabel = QLabel("Start New Game")
        self.stepLabel.setFont(QFont('Pokemon GB'))
        # self.stepLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.longRunningBtn = QPushButton("Start New Game!", self)
        self.longRunningBtn.setFont(QFont('Pokemon GB'))
        self.longRunningBtn.setGeometry(20, 15, 10, 40)
        self.longRunningBtn.clicked.connect(self.runLongTask)

        self.badgesLabels = list()
        for b in ['bolder_badge', 'cascade_badge', 'thunder_badge', 'rainbow_badge', 'soul_badge', 'marsh_badge', 'volcano_badge', 'earth_badge']:
            badge_label = QLabel(self)
            img = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\dashboard\\assets\\' + b + '.png',
                             cv2.IMREAD_UNCHANGED)
            pixmap = self.convert_cv_qt_pixelmap(shadow_image(img))
            # pixmap = QPixmap('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\dashboard\\assets\\' + b + '.png')
            pixmap.scaled(128, 128)
            # pixmap.fill(QColor(0, 0, 0))
            badge_label.setPixmap(pixmap)
            self.badgesLabels.append(badge_label)

            # pixmap.createMaskFromColor()



        self.pokemonLabels = list()
        self.hpBars = list()
        self.ppBars = {}
        self.pokemonGroups = []
        self.all_move_labels = {}
        for i in range(6):
            # image
            pokemon_label = QLabel(self)
            pixmap = QPixmap('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\dashboard\\assets\\' + 'poke_ball.png')
            pixmap.scaled(64, 64)
            pokemon_label.setPixmap(pixmap)
            self.pokemonLabels.append(pokemon_label)

            # hpBar
            hpbar = QProgressBar(self)
            hpbar.setStyleSheet(
                " QProgressBar { text-align: center; } QProgressBar::chunk {background-color: #3add36; width: 1px;}")
            hpbar.setValue(100)
            hpbar.setFormat('HP bar')
            hpbar.adjustSize()
            self.hpBars.append(hpbar)


            # moves
            # moves_group_box = QGroupBox(self.tr("Moves"))
            moves_grid_layout = QGridLayout()
            moves = list()
            self.ppBars[i] = []
            self.all_move_labels[i] = []
            for j in range(4):
                # PP bar
                ppbar = QProgressBar(self)
                ppbar.setStyleSheet(
                    " QProgressBar { text-align: center; height: 2px } QProgressBar::chunk {background-color: #7D94B0; width: 1px; height: 2px;}")
                ppbar.setValue(50)
                ppbar.setFormat('PP bar')
                # ppbar.setGeometry(200, 100, 2, 5)
                # ppbar.adjustSize()
                self.ppBars[i].append(ppbar)

                single_move_layout = QVBoxLayout()
                single_move_group_box = QGroupBox()
                m = QLabel(self)
                m.setText(f'move {j}')
                self.all_move_labels[i].append(m)
                single_move_layout.addWidget(m)
                single_move_layout.addStretch(4)
                single_move_layout.addWidget(ppbar)
                single_move_layout.addStretch(1)
                single_move_group_box.setLayout(single_move_layout)
                moves_grid_layout.addWidget(single_move_group_box, int(j / 2 + 1), j % 2)
                moves.append(m)
            moves_grid_layout.setColumnStretch(0, 1)
            moves_grid_layout.setColumnStretch(1, 1)
            # moves_group_box.setLayout(moves_grid_layout)

            # combine progressbar and moves
            hp_and_moves_layout = QVBoxLayout()
            hp_and_moves_layout.addWidget(hpbar)
            hp_and_moves_layout.addLayout(moves_grid_layout)

            pokemonGroupBox = QGroupBox(self.tr(f"Pokemon {i}"))
            layout = QHBoxLayout()
            layout.addWidget(pokemon_label, stretch=1)
            layout.addLayout(hp_and_moves_layout, stretch=2)
            pokemonGroupBox.setLayout(layout)
            self.pokemonGroups.append(pokemonGroupBox)

        # self.pokemonGroups = list()
        # for i in range(6):
        #     pokemonGroupBox = QGroupBox(self.tr(f"Pokemon {i}"))
        #     layout = QHBoxLayout()
        #     layout.addWidget(self.pokemonLabels[i], stretch=1)
        #
        #     # layout.addLayout(self.pokemon_label, 1)
        #     # layout.addWidget(self.progressBars[i], stretch=8)
        #     # layout.addLayout(self.pbar, 3)
        #     pokemonGroupBox.setLayout(layout)
        #     self.pokemonGroups.append(pokemonGroupBox)

        partyGroupBox = QGroupBox(self.tr("Party"))
        grid_layout = QGridLayout()
        for i in range(6):
            col_num = i % 2
            row_num = int(i / 2 + 1)
            grid_layout.addWidget(self.pokemonGroups[i], int(i / 2 + 1), i % 2)
        # grid_layout.addWidget(pokemonGroupBox2, 1, 1)
        # grid_layout.addWidget(pokemonGroupBox3, 2, 0)
        # grid_layout.addWidget(pokemonGroupBox4, 2, 1)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)
        partyGroupBox.setLayout(grid_layout)

        # buttons
        buttonGroupBox = QGroupBox(self.tr("Button options"))
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.start_vba_btn)
        button_layout.addWidget(self.longRunningBtn)
        buttonGroupBox.setLayout(button_layout)

        # badges
        badgesGroupBox = QGroupBox(self.tr("Badges"))
        badges_layout = QGridLayout()
        for i in range(8):
            badges_layout.addWidget(self.badgesLabels[i], int(i / 4 + 1), i%4+1)
        badgesGroupBox.setLayout(badges_layout)


        mainLayout = QVBoxLayout()
        mainLayout.addWidget(badgesGroupBox, 1)
        mainLayout.addWidget(buttonGroupBox,1)
        # partyGroupBox = self.partyBox()
        mainLayout.addWidget(partyGroupBox, 2)

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(mainLayout)
        self.setCentralWidget(self.centralWidget)


    def setupTimer(self):
        # Step 2: Create a QThread object
        # self.timerThread = QThread()
        # Step 3: Create a worker object
        self.timer = QTimer()
        # Step 4: Move worker to the thread
        # self.timer.moveToThread(self.timerThread)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(500)

    def update_gui(self):
        assets_folder = 'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\dashboard\\assets\\'

        # print('take party object')
        try:
            # party = OwnPokemon.party
            # # print(party)
            # if len(party) > 0:
            #     self.pokemon_label.setPixmap(QPixmap(path + str(party[0]) + '.png').scaled(128, 128))
            #     self.clicksLabel.setText(f"1st pokemon in party: {party[0]}")
            #
            #     self.pokemon_label2.setPixmap(QPixmap(path + 'bulbasaur' + '.png').scaled(128, 128))
            #     # self.clicksLabel.setText(f"1st pokemon in party: {party[1]}")
            # else:
            #     self.pokemon_label.setPixmap(QPixmap(path + 'poke_ball.png').scaled(128, 128))
            #     self.pokemon_label2.setPixmap(QPixmap(path + 'bulbasaur' + '.png').scaled(128, 128))
            #     print(f"Nothing in party")

            for i in range(6):
                if i >= len(OwnPokemon.party):
                    # no pokemon choose non pokemon view
                    self.pokemonLabels[i].setPixmap(QPixmap(assets_folder + 'poke_ball' + '.png').scaled(90, 90))
                    self.pokemonGroups[i].setTitle('--')

                    self.hpBars[i].setValue(0)

                    # all moves should be none
                    for k in range(4):
                        self.ppBars[i][k].setValue(0)
                        self.all_move_labels[i][k].setText('--')
                else:
                    pokemon = OwnPokemon.party[i]
                    self.pokemonLabels[i].setPixmap(QPixmap(assets_folder + str(pokemon.name) + '.png').scaled(128, 128))
                    self.pokemonGroups[i].setTitle(pokemon.own_name + '   L:' + str(pokemon.level))
                    hp_percentage = int(100 * pokemon.current_hp / int(pokemon.stats['hp']))
                    self.hpBars[i].setValue(hp_percentage)
                    if hp_percentage < 15:
                        self.hpBars[i].setStyleSheet(
                            " QProgressBar { text-align: center; } QProgressBar::chunk {background-color: red;}")
                    else:
                        self.hpBars[i].setStyleSheet(
                            " QProgressBar { text-align: center; } QProgressBar::chunk {background-color: #3add36;}")

                    for j in range(4):
                        if j >= len(pokemon.moves):
                            # no move
                            self.ppBars[i][j].setValue(0)
                            self.all_move_labels[i][j].setText('--')
                        else:
                            move = pokemon.moves[j]
                            self.all_move_labels[i][j].setText(move.name)
                            self.ppBars[i][j].setValue(int(100*move.pp/move.max_pp))


            # party_names = ['abra', 'bulbasaur', 'vulpix', 'pidgey', 'arbok', 'abra' ]
            # # labels = [self.pokemon_label, self.pokemon_label2, self.pokemon_label3, self.pokemon_label4]
            # for i, (pokemon, label) in enumerate(zip(OwnPokemon.party, self.pokemonLabels)):
            #     # print(f'pokemon name {pokemon.own_name}')
            #     # print(f"path {path + str(pokemon.name) + '.png'}")
            #     label.setPixmap(QPixmap(assets_folder + str(pokemon.name) + '.png').scaled(128, 128))
            #     self.pokemonGroups[i].setTitle(pokemon.own_name)
            #     self.progressBars[i].setValue(int(100*pokemon.current_hp/int(pokemon.stats['hp'])))

                # hp = random.randint(0,100)
                # self.progressBars[i].setValue(hp)
                # if hp < 10:
                #     self.progressBars[i].setStyleSheet(" QProgressBar { text-align: center; } QProgressBar::chunk {background-color: red; width: 1px;}")
                # else:
                #     self.progressBars[i].setStyleSheet(" QProgressBar { text-align: center; } QProgressBar::chunk {background-color: #3add36; width: 1px;}")

            badges = ['bolder_badge', 'cascade_badge']
            # badges_bools = [True, True, True, False, True, False, False]
            for name, badge_label in zip(badges, self.badgesLabels):
                # todo the order is not fixed right now.
                badge_label.setPixmap(QPixmap(assets_folder + str(name) + '.png'))

        except Exception as e:
            print(f"issues: {e}")

    def start_vba(self):
        from pokebot.fundamentals import open_vba
        open_vba()

    def update_image(self):
        pass
        # self.clicksCount += 1
        # # self.clicksLabel.setText(f"Counter: {self.clicksCount}")
        #
        # path = 'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\dashboard\\assets\\'
        #
        # party = OwnPokemon.party
        # if len(party)>0:
        #     self.pokemon_label.setPixmap(QPixmap(path + str(party[0])+ '.png'))
        #     self.clicksLabel.setText(f"1st pokemon in party: {party[0]}")
        # else:
        #     self.pokemon_label.setPixmap(path + 'poke_ball.png')



    # def reportProgress(self, n):
    #     self.update_gui()
    #     self.stepLabel.setText(f"Long-Running Step: {n}")

    # def runLongTask(self):
    #     """Long-running task in 5 steps."""
    #     for i in range(5):
    #         sleep(1)
    #         self.reportProgress(i + 1)

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
        self.longRunningBtn.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.longRunningBtn.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.stepLabel.setText("Long-Running Step: 0")
        )




if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setFont('Pokemon GB')
    win = Window()
    win.show()
    # timer = QTimer(win)
    # timer.timeout.connect(win.update_gui)
    # timer.start(500)
    sys.exit(app.exec())