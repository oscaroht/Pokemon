import sys
from time import sleep
from functools import wraps

import cv2
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QColor, QImage, QFont, QFontDatabase, QStandardItemModel, QStandardItem, QFontMetrics
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
# from PyQt5 import QtWidgets, QtGui, QtCore
from functools import partial

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
from pokebot.fundamentals.vba import VBA_controller
# from pokebot.combiner import *
from qt.qt_badges import QBadgesGroupBox
from qt.qt_pokemon import QParty, QMoves
from qt.qt_menu import CustomMenuBar
from qt.qt_worker import Worker
from qt.qt_checkable_combobox import CheckableComboBox

OwnPokemon.new_game()
Items.new_game()


VBA_DIR = "C:\\Users\\oscar\\PycharmProjects\\Pokemon"



# class Pokemon(QtWidgets.QWidget):
#     pass

# def shadow_image(img):
#     ''''Takes and returns a cv2 image with black color but opacity intact.
#
#     It is used to shade the badges that are not yet obtained by the player.'''
#     h = img.shape[0]
#     w = img.shape[0]
#     for y in range(h):
#         for x in range(w):
#             if img[y, x, 3] != 0:  # where the opacity is 0 (so not the background)
#                 img[y, x, :3] = [0, 0, 0]  # set the color to black (nor the opacity to 0!)
#     return img


class Window(QMainWindow):

    unsaved_actions = True
    vba = VBA_controller()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Create menu bar
        menu_bar = CustomMenuBar(self)
        self.setMenuBar(menu_bar)

        self.setup_ui()
        self.setup_timer()

        QFontDatabase.addApplicationFont('Pokemon GB.ttf')

    def poke_action(func):
        """"
        Decorator that sets the unsaved actions class attribute to True
        """
        @wraps(func)  # otherwise multiple uses of the decorator are confused
        def wrapper(self, *args, **kwargs):
            try:
                self.unsaved_actions = True
                self.vba.prepare_action()
                logger.debug(f"Start function")
                func(self, *args, **kwargs)
                logger.debug(f"Function done")
            except Exception:
                logger.error('', exc_info=True)
        return wrapper

    def setup_ui(self):
        self.setWindowTitle("Pokebot")
        self.setGeometry(300, 100, 900, 1000)  # x0, y0, width, height

        self.command_groupbox = QGroupBox(self.tr("Command line"))
        self.command_textbox = QLineEdit("go_to(('route4', 902))")
        self.command_btn = QPushButton("Run command")
        self.command_btn.setFont(QFont('Pokemon GB'))
        self.command_btn.clicked.connect(self.run_command)
        textbox_layout = QVBoxLayout()
        textbox_layout.addWidget(self.command_textbox)
        textbox_layout.addWidget(self.command_btn)
        self.command_groupbox.setLayout(textbox_layout)

        self.badges = QBadgesGroupBox(self)

        # # Initiate button section
        # self.start_vba_btn = QPushButton("Open VBA", self)
        # self.start_vba_btn.setFont(QFont('Pokemon GB'))
        # self.start_vba_btn.clicked.connect(self.start_vba)  # link th button to the start VBA function
        #
        # self.new_game_btn = QPushButton("Start New Game!", self)
        # self.new_game_btn.setFont(QFont('Pokemon GB'))
        # self.new_game_btn.setGeometry(20, 15, 10, 40)
        # self.new_game_btn.clicked.connect(self.runLongTask)
        #
        # self.load_btn = QPushButton("Load saved game 8", self)
        # self.load_btn.setFont(QFont('Pokemon GB'))
        # self.load_btn.setGeometry(20, 15, 10, 40)
        # self.load_btn.clicked.connect(self.load_game8)

        # Add buttons to a box
        # buttonGroupBox = QGroupBox(self.tr("Button options"))
        # button_layout = QVBoxLayout()
        # button_layout.addWidget(self.start_vba_btn)
        # button_layout.addWidget(self.new_game_btn)
        # button_layout.addWidget(self.load_btn)
        # buttonGroupBox.setLayout(button_layout)

        self.party = QParty(self)

        self.command_box = QGroupBox(self.tr("Command line"))
        self.command_layout = QHBoxLayout()
        self.confirm_btn = QPushButton('Run')
        self.confirm_btn.clicked.connect(self.run_command2)
        self.cb = QComboBox()
        self.cb.addItems(['go to', 'talk', 'train', 'catch', 'buy'])
        self.cb.currentIndexChanged.connect(self.update_command_layout)
        self.cb_options = QComboBox()
        self.cb_options.addItems(['Mom','Professor Oak'])
        self.cb_options.setEditable(True)
        self.cb.setInsertPolicy(QComboBox.NoInsert)
        self.level_textbox = QLineEdit("to what level?")  # not yet in layout
        self.catch_textbox = QLineEdit("which pokemon?")  # not yet in layout

        self.cb_train = CheckableComboBox()


        self.command_layout.addWidget(self.cb)
        self.command_layout.addWidget(self.cb_options)
        self.command_layout.addWidget(self.confirm_btn)
        self.command_box.setLayout(self.command_layout)


        # total layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.badges, 1)
        # main_layout.addWidget(buttonGroupBox, 1)
        main_layout.addWidget(self.party.groupbox, 2)
        main_layout.addWidget(self.command_groupbox, 1)
        main_layout.addWidget(self.command_box)

        self.central_widget = QWidget()
        self.central_widget.setLayout(main_layout)
        self.setCentralWidget(self.central_widget)


    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(500)  # set the reset frequency in milli seconds


    def update_gui(self):
        ''''
        Updates the gui by calling the party widget's update function and calling the badges widget's update function.
        '''
        try:
            self.party.update()
            self.badges.update()
        except Exception:
            logger.error(f"Uncaught frontend error: ", exc_info=True)
            raise


    # def start_vba(self):
    #     from pokebot.fundamentals import open_vba
    #     open_vba()
    #
    # def load_game8(self):
    #     try:
    #         import load_saved_game3
    #     except Exception:
    #         logger.error(f"error: ", exc_info=True)

    def update_command_layout(self):
        # clear all widgets from layout
        for i in reversed(range(self.command_layout.count())):
            self.command_layout.itemAt(i).widget().setParent(None)
        self.command_layout.addWidget(self.cb, 1)
        if self.cb.currentText() == 'train':
            self.command_layout.addWidget(self.level_textbox, 1)
            self.cb_train.clear()
            self.cb_train.addItems(OwnPokemon.party.list_all_own_names())
            self.command_layout.addWidget(self.cb_train, 1)

        elif self.cb.currentText() == 'catch':
            self.command_layout.addWidget(self.catch_textbox, 1)
        self.command_layout.addWidget(self.cb_options, 1)
        self.command_layout.addWidget(self.confirm_btn, 1)
        self.command_box.setLayout(self.command_layout)

        # # total layout
        # main_layout = QVBoxLayout()
        # main_layout.addWidget(self.badges, 1)
        # # main_layout.addWidget(buttonGroupBox, 1)
        # main_layout.addWidget(self.party.groupbox, 2)
        # main_layout.addWidget(self.command_groupbox, 1)
        # main_layout.addWidget(self.command_box)
        #
        # self.central_widget.setLayout(main_layout)


    def update_options_combo(self):
        self.cb_options.clear()
        map = {'catch'}

    @poke_action
    def run_command(self, _called: bool) -> None:  # need the _called arg to work with decorator and pyqt slots
        # Step 2: Create a QThread object
        try:
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
        except Exception:
            logger.error(f"Err: ", exc_info=True)

    @poke_action
    def run_command2(self, _called: bool) -> None:  # need the _called arg to work with decorator and pyqt slots
        # Step 2: Create a QThread object
        try:
            from pokebot.combiner import go_to, talk, buy, catch, train
            from pokebot.short_cuts import mom, oak
            func_map = {'go to': go_to,
                        'talk': talk,
                        'buy': buy,
                        'catch': catch,
                        'train': train}
            arg_map = {'Mom': mom,
                       'Professor Oak': oak}

            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = Worker()

            self.worker.func = func_map[self.cb.currentText()]
            self.worker.args = self.cb_options.currentText()

            # create the function that should be performed by the worker in the thread
            self.worker.partial_func = partial(func_map[self.cb.currentText()], arg_map[self.cb_options.currentText()])

            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            self.thread.started.connect(self.worker.execute_partial)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            # self.worker.progress.connect(self.reportProgress)
            # Step 6: Start the thread
            self.thread.start()

            # Final resets
            # self.new_game_btn.setEnabled(False)
            self.confirm_btn.setEnabled(False)
            self.thread.finished.connect(
                lambda: self.new_game_btn.setEnabled(True)
            )
            self.thread.finished.connect(
                lambda: self.command_btn.setEnabled(True)
            )
        except Exception:
            logger.error(f"Err: ", exc_info=True)

    @poke_action
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