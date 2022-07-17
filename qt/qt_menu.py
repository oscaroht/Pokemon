import sys
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, QTimer, pyqtSlot
from PyQt5.QtGui import QPixmap, QColor, QImage, QFont, QFontDatabase
from PyQt5.QtWidgets import *
from datetime import datetime
from functools import partial, wraps
from typing import List

import logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
                    handlers=[logging.FileHandler(f"C:\\Users\\oscar\\PycharmProjects\\Pokemon\\qt\\log\\{datetime.utcnow().strftime('%Y-%m-%dT%H_%M_%S')}.log"),
                              logging.StreamHandler()])
logger = logging.getLogger(__name__)

from pokebot.fundamentals.vba import VBA_controller
from qt.qt_worker import Worker

# had some issues with passing args to functions called with triggered.connect
# espacially the decorators did not work with *args and **kwargs
# https://stackoverflow.com/questions/68728433/how-can-i-use-a-decorator-on-a-pyqt-signal

def saves_action(func):
    """"
    Sets the parent's unsaved changes attribute to False.
    """
    @wraps(func)  # otherwise multiple uses of the decorator are confused
    def wrapper(self,  *args, **kwargs):
        logger.debug(f"Call {func} with args {args} and kwargs {kwargs}")
        func(self, *args, **kwargs)
        logger.debug(f"Set unsaved_actions to False")
        self.parent.unsaved_actions = False
    return wrapper


def discards_changes(func):
    """"
    Prior to function execution opens the discard changes dialog.
    """
    @wraps(func)  # otherwise multiple uses of the decorator are confused
    def wrapper(self, *args, **kwargs):
        if self.parent.unsaved_actions:
            logger.debug(f"Create discards changes dialog")
            sd = DiscardChangesDialog(self)
            logger.debug(f"Execute discards changes dialog")
            sd.exec()
            if not sd.passed:
                logger.debug(f"Discards changes dialog not passed")
                return
        logger.debug(f"Call {func} called from decorator with args {args} and kwargs {kwargs}")
        func(self, *args, **kwargs)
    return wrapper


class CustomMenuBar(QMenuBar):

    VBA_DIR = "C:\\Users\\oscar\\PycharmProjects\\Pokemon"

    vba = VBA_controller()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.create_actions()
        self._create_menubar()
        self._connectActions()

    def _create_menubar(self):
        """"
        Create the menu dropdowns and set the right actions in every dropdown.
        """
        # File menu
        fileMenu = self.addMenu("&File")
        fileMenu.addAction(self.new_game_action)
        # fileMenu.addAction(win.newAction)
        self.load_menu = fileMenu.addMenu("Load saved game...")
        self.save_menu = fileMenu.addMenu("Save game...")
        fileMenu.addAction(self.open_vba_action)
        fileMenu.addAction(self.exit_action)
        # Edit menu
        editMenu = self.addMenu("&Edit")
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)

        # Help menu
        helpMenu = self.addMenu("&Help")
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)

    def create_actions(self) -> None:
        """"
        Create the actions and set the text.
        """
        import os
        # Creating action using the first constructor
        self.new_game_action = QAction(self.parent)
        self.new_game_action.setText("&New game")
        # Creating actions using the second constructor
        self.open_vba_action = QAction("&Open VBA", self.parent)
        self.exit_action = QAction("&Exit", self.parent)
        self.copyAction = QAction("&Copy", self.parent)
        self.pasteAction = QAction("&Paste", self.parent)
        self.cutAction = QAction("&Cut", self.parent)
        self.helpContentAction = QAction("&Help Content", self.parent)
        self.aboutAction = QAction("&About", self.parent)

    def _connectActions(self):
        """"
        Add the actions that happen when a option in the menu is clicked.
        """
        # Connect File actions
        self.load_menu.aboutToShow.connect(self.populate_load_menu)
        self.save_menu.aboutToShow.connect(self.populate_save_menu)
        self.new_game_action.triggered.connect(self.new_game)
        self.open_vba_action.triggered.connect(self.open_vba)
        self.exit_action.triggered.connect(self.exit)

    def open_vba(self):
        self.vba.open_vba_window_if_not_exists()

    @discards_changes
    def exit(self):
        """"
        Exits the VBA and QT window.
        """
        logger.debug(f"Exit called")
        self.vba.close()
        return super().close(self.parent)  # close the window

    @discards_changes
    def new_game(self, _called: bool) -> None:
        """"
        Starts a new game
        """
        dw = NewGameDialog(self)
        logger.debug(f"Execute dialog")
        dw.exec()
        if dw.passed:
            logger.debug(f"Dialog window passed")
            from pokebot.game_plan import Gameplan
            from pokebot.fight.pokemon import OwnPokemon
            from pokebot.gameplay.item import Items
            from pokebot.combiner import go_to

            logger.debug(f"Reset objects to new game settings")
            Gameplan.set_new_game()
            OwnPokemon.new_game()
            Items.new_game()
            logger.debug(f"VBA reset")
            self.vba.reset_game()

            logger.debug(f"Spin off new thread")
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = Worker()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            self.thread.started.connect(partial(self.worker.run2, go_to, ('mom_lvl2', 44)))
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            # self.worker.progress.connect(self.reportProgress)
            # Step 6: Start the thread
            self.thread.start()

            self.new_game_action.setEnabled(False)
            self.thread.finished.connect(
                lambda: self.new_game_action.setEnabled(True)
            )

    def get_number(self,f: str) -> int:
        """"
        Return the numbers in a string as int
        """
        return int(''.join([s for s in f if s.isdigit()]))

    def populate_save_menu(self):
        """"
        Display a list of all saved files in the menu
        """
        self.save_menu.clear()
        filenames = self.saved_games_list()  # [filename for filename in os.listdir(self.VBA_DIR) if filename.endswith('sgm')]

        opt = {}
        for i in range(10):
            opt[i + 1] = '--'
        actions = []
        for filename in filenames:
            index = self.get_number(filename)
            opt[index] = filename
        for key,value in opt.items():
            action = QAction(value, self.parent)
            action.triggered.connect(partial(self.save_this_file, key))
            actions.append(action)
        self.save_menu.addActions(actions)


    def populate_load_menu(self):
        """"
        Dynamically populates the actions for the load submenu.
        """
        self.load_menu.clear()  # clear the list before load
        filenames = self.saved_games_list()
        filenames.sort(key=self.get_number)

        actions = []
        for f in filenames:
            action = QAction(f, self)
            action.triggered.connect(partial(self.load_this_file, f))
            actions.append(action)
        self.load_menu.addActions(actions)

    @discards_changes
    @saves_action
    def load_this_file(self, f: str, _called: bool):
        """"
        Loads a specific saved game, file and database record.
        """
        try:
            from pokebot.fundamentals.load_game import load_game_in_database
            logger.debug(f"Loading file {f}")
            # file
            num: int = self.get_number(f)  # int(''.join([s for s in f if s.isdigit()]))
            self.vba.load_game(num)
            # database
            load_game_in_database(f)
        except Exception:
            logger.error('Err: ', exc_info=True)

    def saved_games_list(self) -> List[str]:
        """"
        Returns list of all saved files.
        """
        import os
        return [filename for i, filename in enumerate(os.listdir(self.VBA_DIR)) if filename.endswith('sgm')]

    @saves_action
    def save_this_file(self, slot: int, _called: bool) -> None:
        """"
        Saves a game to file and database.
        """
        try:
            f = f"Pokemon Blue{slot}.sgm"
            if f in self.saved_games_list():
                logger.debug(f"{f} already in saved games")
                od = OverwriteDialog()
                od.exec()
                if not od.passed:
                    logger.debug(f"cancel save")
                    return

            logger.debug(f"Save file on slot {slot}")
            from pokebot.fundamentals.save_game import save_game_in_database
            self.vba.save_game(slot)
            save_game_in_database(f, slot)
        except Exception:
            logger.error("Err: ", exc_info=True)



class NewGameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.passed = False

        self.setWindowTitle('New game')

        self.first = QLineEdit(self)
        self.second = QLineEdit(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        # self.ash_label = QLabel()
        # self.pixmap = QPixmap('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\dashboard\\assets\\' + 'ash' + '.png')
        # self.ash_label.setPixmap(self.pixmap)

        layout = QFormLayout(self)
        layout.setVerticalSpacing(20)
        layout.addRow("Player name", self.first)
        layout.setVerticalSpacing(20)
        layout.addRow("Rival name", self.second)
        layout.setVerticalSpacing(20)
        layout.addWidget(buttonBox)
        # question_gb = QGroupBox()
        # question_gb.setLayout(layout)
        #
        # gb = QHBoxLayout()
        # gb.addWidget(self.ash_label)
        # gb.addWidget(question_gb)
        # self.setLayout(gb)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    # def getInputs(self):
    #     return (self.first.text(), self.second.text())

    def accept(self) -> None:
        from pokebot.game_plan import Gameplan
        if self.first.text() and self.second.text():
            # if there is any input
            p: bool = Gameplan.set_player_name(self.first.text())
            r: bool = Gameplan.set_rival_name(self.second.text())
            self.passed = True
        super().accept()

    def reject(self) -> None:
        self.passed = False
        super().reject()

    @staticmethod
    def convert_cv_qt_pixelmap(cv_img):
        ''''
        Converts a open cv image to a qt pixmap.
        '''
        h, w, ch = cv_img.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format_RGBA8888)
        return QPixmap.fromImage(convert_to_Qt_format)



class OverwriteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.passed = False

        self.setWindowTitle("Overwrite existing game?")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("You already have a game at this slot.\nClick OK if you want to overwrite it.")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        self.passed = True
        super().accept()


class DiscardChangesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.passed = False

        self.setWindowTitle("Unsaved changes")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("You have unsaved changes.\nIf you want to discard these changes click OK")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self):
        logger.debug(f"OK clicked. Accepted function started")
        self.passed = True
        logger.debug(f"Call super accept function")
        super(DiscardChangesDialog, self).accept()
        logger.debug(f"Super accept done")





if __name__ == '__main__':
    class Window(QMainWindow):
        """Main Window."""

        def __init__(self, parent=None):
            """Initializer."""
            super().__init__(parent)

            self.unsaved_actions = True

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
