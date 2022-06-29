import sys
from time import sleep

import cv2
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QColor, QImage, QFont, QFontDatabase
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import random

# https://www.pythonguis.com/tutorials/creating-your-own-custom-widgets/
from datetime import datetime
import logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
                    handlers=[logging.FileHandler(f"C:\\Users\\oscar\\PycharmProjects\\Pokemon\\qt\\log\\{datetime.utcnow().strftime('%Y-%m-%dT%H_%M_%S')}.log"),
                              logging.StreamHandler()])
logger = logging.getLogger(__name__)

from pokebot.fight import OwnPokemon
from pokebot.gameplay import Items
from qt.qt_badges import QBadges
from qt.qt_pokemon import QParty, QMoves
from qt.qt_menu import CustomMenuBar

OwnPokemon.new_game()
Items.new_game()


VBA_DIR = "C:\\Users\\oscar\\PycharmProjects\\Pokemon"


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
        # print(f"Executing: {self.execute_command_arg}")
        try:
            # exec(self.execute_command_arg)
            print(f"Executing: {self.execute_command_arg}")
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
        # Create menu bar
        menu_bar = CustomMenuBar(self)
        self.setMenuBar(menu_bar)

        self.setup_ui()
        self.setup_timer()

        QFontDatabase.addApplicationFont('Pokemon GB.ttf')


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


        self.badges = QBadges(self)


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

        self.party = QParty(self)

        # total layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.badges.groupbox, 1)
        main_layout.addWidget(buttonGroupBox, 1)
        main_layout.addWidget(self.party.groupbox, 2)
        main_layout.addWidget(command_groupbox, 1)

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
            self.party.update()
            self.badges.update()
        except Exception:
            logger.error(f"Uncaught frontend error: ", exc_info=True)
            raise


    def start_vba(self):
        from pokebot.fundamentals import open_vba
        open_vba()

    def load_game8(self):
        try:
            import load_saved_game3
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