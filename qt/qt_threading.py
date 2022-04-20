import sys
from time import sleep
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap
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

# https://www.pythonguis.com/tutorials/creating-your-own-custom-widgets/

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


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicksCount = 0
        self.setupUi()
        self.setupTimer()

    def partyBox(self):
        partyGroupBox = QGroupBox(self.tr("Party"))
        grid_layout = QGridLayout()
        for i, p in enumerate(['charmander', 'bulbasaur']): # , 'vulpix', 'pidgey'
            col_num = i%2
            row_num = int(i/2+1)
            widget = self.pokeBox(p)
            grid_layout.addWidget(widget, row_num, col_num)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)
        return partyGroupBox.setLayout(grid_layout)

    def pokeBox(self, pokemon_name):
        print(f"Adding {pokemon_name}")
        pokemonGroupBox = QGroupBox(self.tr(pokemon_name))
        layout = QHBoxLayout()

        layout.addWidget(self.pokemon_label, stretch=1)
        layout.addWidget(self.pbar, stretch=6)
        return pokemonGroupBox.setLayout(layout)


    def setupUi(self):
        self.setWindowTitle("Freezing GUI")
        self.setGeometry(300, 100, 900, 1000) # x0, y0, width, height


        # Create and connect widgets
        self.clicksLabel = QLabel("Pokemon", self)
        # self.clicksLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.countBtn = QPushButton("Update image", self)
        # self.countBtn.setGeometry(20, 15, 10, 40)
        self.countBtn.clicked.connect(self.update_image)

        # self.openvbaBtn = QPushButton("Start VBA", self)
        # self.openvbaBtn.clicked.connect(self.start_vba)

        self.stepLabel = QLabel("Start New Game")
        # self.stepLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.longRunningBtn = QPushButton("Start New Game!", self)
        self.longRunningBtn.setGeometry(20, 15, 10, 40)
        self.longRunningBtn.clicked.connect(self.runLongTask)

        self.pokemonLabels = list()
        for i in range(6):
            pokemon_label = QLabel(self)
            pixmap = QPixmap('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\dashboard\\assets\\' + 'poke_ball.png')
            pixmap.scaled(128, 128)
            pokemon_label.setPixmap(pixmap)
            self.pokemonLabels.append(pokemon_label)

        # self.pokemon_label = QLabel(self)
        # pixmap = QPixmap('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\dashboard\\assets\\' + 'poke_ball.png')
        # pixmap.scaled(128, 128)
        # self.pokemon_label.setPixmap(pixmap)
        #
        # self.pokemon_label2 = QLabel(self)
        # pixmap = QPixmap('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\dashboard\\assets\\' + 'poke_ball.png')
        # pixmap.scaled(128, 128)
        # self.pokemon_label2.setPixmap(pixmap)
        #
        # self.pokemon_label3 = QLabel(self)
        # pixmap = QPixmap('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\dashboard\\assets\\' + 'poke_ball.png')
        # pixmap.scaled(128, 128)
        # self.pokemon_label3.setPixmap(pixmap)
        #
        # self.pokemon_label4 = QLabel(self)
        # pixmap = QPixmap('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\dashboard\\assets\\' + 'poke_ball.png')
        # pixmap.scaled(128, 128)
        # self.pokemon_label4.setPixmap(pixmap)

        # self.setCentralWidget(label)
        # self.resize(pixmap.width(), pixmap.height())

        self.progressBars = list()
        for i in range(6):
            pbar = QProgressBar(self)
            pbar.setStyleSheet(
                " QProgressBar { text-align: center; } QProgressBar::chunk {background-color: #3add36; width: 1px;}")
            pbar.setValue(50)
            pbar.adjustSize()
            self.progressBars.append(pbar)

        # self.pbar = QProgressBar(self)
        # self.pbar.setStyleSheet(" QProgressBar { text-align: center; } QProgressBar::chunk {background-color: #3add36; width: 1px;}")
        # self.pbar.setValue(50)
        # self.pbar.adjustSize()
        #
        # self.pbar2 = QProgressBar(self)
        # self.pbar2.setStyleSheet(
        #     " QProgressBar { text-align: center; } QProgressBar::chunk {background-color: #3add36; width: 1px;}")
        # self.pbar2.setValue(50)
        # self.pbar2.adjustSize()
        #
        # self.pbar3 = QProgressBar(self)
        # self.pbar3.setStyleSheet(
        #     " QProgressBar { text-align: center; } QProgressBar::chunk {background-color: #3add36; width: 1px;}")
        # self.pbar3.setValue(50)
        # self.pbar3.adjustSize()
        #
        # self.pbar4 = QProgressBar(self)
        # self.pbar4.setStyleSheet(
        #     " QProgressBar { text-align: center; } QProgressBar::chunk {background-color: #3add36; width: 1px;}")
        # self.pbar4.setValue(50)
        # self.pbar4.adjustSize()

        # self.label_1 = QLabel("new border ", self)
        # # moving position
        # self.label_1.move(100, 100)
        # self.label_1.setStyleSheet("border :3px solid black;")

        # Set the layout
        # layout = QVBoxLayout()
        # layout2 = QHBoxLayout()
        # # layout.addWidget(self.clicksLabel)
        # # layout.addWidget(self.countBtn)
        # layout.addStretch()
        # # layout.addWidget(self.openvbaBtn)
        # layout.addStretch()
        # layout.addWidget(self.stepLabel)
        # layout.addWidget(self.longRunningBtn)
        # layout2.addWidget(self.pokemon_label)
        # # layout.addWidget(self.label_1)
        # # layout2.addWidget(self.pbar)
        # self.centralWidget.setLayout(layout)
        # self.centralWidget.setLayout(layout2)

        buttonGroupBox = QGroupBox(self.tr("Button options"))
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.countBtn)
        button_layout.addWidget(self.longRunningBtn)
        buttonGroupBox.setLayout(button_layout)

        self.pokemonGroups = list()
        for i in range(6):
            pokemonGroupBox = QGroupBox(self.tr(f"Pokemon {i}"))
            layout = QHBoxLayout()
            layout.addWidget(self.pokemonLabels[i], stretch=1)
            # layout.addLayout(self.pokemon_label, 1)
            layout.addWidget(self.progressBars[i], stretch=8)
            # layout.addLayout(self.pbar, 3)
            pokemonGroupBox.setLayout(layout)
            self.pokemonGroups.append(pokemonGroupBox)
        #
        # pokemonGroupBox = QGroupBox(self.tr("Pokemon 1"))
        # layout = QHBoxLayout()
        # layout.addWidget(self.pokemon_label, stretch=1)
        # # layout.addLayout(self.pokemon_label, 1)
        # layout.addWidget(self.pbar, stretch=8)
        # # layout.addLayout(self.pbar, 3)
        # pokemonGroupBox.setLayout(layout)
        #
        # pokemonGroupBox2 = QGroupBox(self.tr("Pokemon 2"))
        # layout2 = QHBoxLayout()
        # layout2.addWidget(self.pokemon_label2, stretch=1)
        # layout2.addWidget(self.pbar2, stretch=8)
        # pokemonGroupBox2.setLayout(layout2)
        #
        # pokemonGroupBox3 = QGroupBox(self.tr("Pokemon 3"))
        # layout3 = QHBoxLayout()
        # layout3.addWidget(self.pokemon_label3, stretch=1)
        # layout3.addWidget(self.pbar3, stretch=8)
        # pokemonGroupBox3.setLayout(layout3)
        #
        # pokemonGroupBox4 = QGroupBox(self.tr("Pokemon 4"))
        # layout4 = QHBoxLayout()
        # layout4.addWidget(self.pokemon_label4, stretch=1)
        # layout4.addWidget(self.pbar4, stretch=8)
        # pokemonGroupBox4.setLayout(layout4)

        # pokemonGroupBox5 = QGroupBox(self.tr("Pokemon 5"))
        # layout5 = QHBoxLayout()
        # layout5.addWidget(self.pokemon_label5, stretch=1)
        # layout5.addWidget(self.pbar5, stretch=8)
        # pokemonGroupBox5.setLayout(layout5)
        #
        # pokemonGroupBox6 = QGroupBox(self.tr("Pokemon 6"))
        # layout6 = QHBoxLayout()
        # layout6.addWidget(self.pokemon_label6, stretch=1)
        # layout6.addWidget(self.pbar6, stretch=8)
        # pokemonGroupBox6.setLayout(layout6)

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

        mainLayout = QVBoxLayout()
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
        path = 'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\dashboard\\assets\\'

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

            party_names = ['charmander', 'bulbasaur', 'vulpix', 'pidgey', 'arbok', 'abra' ]
            # labels = [self.pokemon_label, self.pokemon_label2, self.pokemon_label3, self.pokemon_label4]
            for i, (name, label) in enumerate(zip(party_names, self.pokemonLabels)):
                label.setPixmap(QPixmap(path + str(name) + '.png').scaled(128, 128))
                self.pokemonGroups[i].setTitle(name)

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
    win = Window()
    win.show()
    # timer = QTimer(win)
    # timer.timeout.connect(win.update_gui)
    # timer.start(500)
    sys.exit(app.exec())