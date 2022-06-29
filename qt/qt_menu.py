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
from datetime import datetime
import random

import logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
                    handlers=[logging.FileHandler(f"C:\\Users\\oscar\\PycharmProjects\\Pokemon\\qt\\log\\{datetime.utcnow().strftime('%Y-%m-%dT%H_%M_%S')}.log"),
                              logging.StreamHandler()])
logger = logging.getLogger(__name__)

# new idea create object that extends QMenubar and assign it in the Main Window

class CustomMenuBar(QMenuBar):

    VBA_DIR = "C:\\Users\\oscar\\PycharmProjects\\Pokemon"

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.create_actions()
        self._create_menubar()
        self._connectActions()


    def _create_menubar(self):
        # File menu
        fileMenu = self.addMenu("&File")
        fileMenu.addAction(self.newAction)
        # fileMenu.addAction(win.newAction)
        self.load_menu = fileMenu.addMenu("Load saved game...")
        self.save_menu = fileMenu.addMenu("Save game...")
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)
        # Edit menu
        editMenu = self.addMenu("&Edit")
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)

        # Help menu
        helpMenu = self.addMenu("&Help")
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)

    def create_actions(self):
        import os
        # Creating action using the first constructor
        self.newAction = QAction(self.parent)
        self.newAction.setText("&New")
        # Creating actions using the second constructor
        self.saveAction = QAction("&Save", self.parent)
        self.exitAction = QAction("&Exit", self.parent)
        self.copyAction = QAction("&Copy", self.parent)
        self.pasteAction = QAction("&Paste", self.parent)
        self.cutAction = QAction("&Cut", self.parent)
        self.helpContentAction = QAction("&Help Content", self.parent)
        self.aboutAction = QAction("&About", self.parent)

    def _connectActions(self):
        # Connect File actions
        self.load_menu.aboutToShow.connect(self.populate_load_menu)
        self.save_menu.aboutToShow.connect(self.populate_save_menu)
        self.newAction.triggered.connect(self.new)

    def new(self):
        print(f"New clicked")

    def get_number(self,f):
        return int(''.join([s for s in f if s.isdigit()]))

    def populate_save_menu(self):
        import os, functools
        self.save_menu.clear()
        filenames = [filename for filename in os.listdir(self.VBA_DIR) if filename.endswith('sgm')]

        opt = {}
        for i in range(10):
            opt[i + 1] = '--'
        actions = []
        for filename in filenames:
            index = self.get_number(filename)
            opt[index] = filename
        for key,value in opt.items():
            action = QAction(value, self.parent)
            action.triggered.connect(functools.partial(self.save_this_file, key))
            actions.append(action)
        self.save_menu.addActions(actions)


    def populate_load_menu(self):
        import os, functools
        self.load_menu.clear()
        filenames = [filename for i, filename in enumerate(os.listdir(self.VBA_DIR)) if filename.endswith('sgm')]
        filenames.sort(key=self.get_number)

        actions = []
        print(filenames)
        for f in filenames:
            action = QAction(f, self)
            action.triggered.connect(functools.partial(self.load_this_file, f))
            actions.append(action)
        self.load_menu.addActions(actions)


    def load_this_file(self, f):
        from pokebot.fundamentals.load_game import load_game
        # VBA LOAD
        from pokebot.fundamentals.controls import btnF
        from pygetwindow import getWindowsWithTitle, PyGetWindowException
        try:
            vb = getWindowsWithTitle('VisualBoyAdvance')[0]
            vb.activate()  # also possible to uncheck 'Pause when inactive' in vba settings
            num = ''.join([s for s in f if s.isdigit()])
            btnF(int(num))
        except PyGetWindowException:  # windows returns code 0 when everything is successful. Unfortunately this is handled as an error
            pass

        # DATABASE LOAD
        try:
            load_game(f)
        except Exception:
            logger.error('Err: ', exc_info=True)

    def save_this_file(self, slot):
        # VBA SAVE
        from pokebot.fundamentals.controls import btn_save
        from pygetwindow import getWindowsWithTitle, PyGetWindowException
        try:
            vb = getWindowsWithTitle('VisualBoyAdvance')[0]
            vb.activate()  # also possible to uncheck 'Pause when inactive' in vba settings
            btn_save(slot)
        except PyGetWindowException:  # windows returns code 0 when everything is successful. Unfortunately this is handled as an error
            pass

        f = f"Pokemon Blue{slot}.sgm"
        if f != '--':
            print("Are you sure you want to overwrite this file")
        print(f"saving on {f}")
        try:
            from pokebot.fundamentals.save_game import save_game
            save_game(f, slot)
        except Exception:
            logger.error("Err: ", exc_info=True)

if __name__ == '__main__':
    class Window(QMainWindow):
        """Main Window."""

        def __init__(self, parent=None):
            """Initializer."""
            super().__init__(parent)
            self.setWindowTitle("Menus & Toolbars")
            self.resize(400, 200)
            self.centralWidget = QLabel("Central Widget")
            self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setCentralWidget(self.centralWidget)

            menu_bar = CustomMenuBar(self)
            self.setMenuBar(menu_bar)

    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
