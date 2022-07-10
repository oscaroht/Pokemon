import sys
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, QTimer, pyqtSlot
from PyQt5.QtGui import QPixmap, QColor, QImage, QFont, QFontDatabase
from PyQt5.QtWidgets import *
from datetime import datetime
from functools import partial
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
    @pyqtSlot()  # needed to make *args and **kwargs work
    def wrapper(self,  *args, **kwargs):
        func(self, *args, **kwargs)
        self.parent.unsaved_actions = False

    return wrapper


def discards_changes(func):
    @pyqtSlot()  # needed to make *args and **kwargs work
    def wrapper(self, *args, **kwargs):
        if self.parent.unsaved_actions:
            print(f"there are unsaved changes")
            sd = SaveDialog(self)
            sd.exec()
            if not sd.passed:
                return
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

    def create_actions(self):
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
        super().close(self.parent)  # close the window


    @discards_changes
    def new_game(self):
        print(f"New clicked")

        dw = NewGameDialog(self)
        dw.exec()
        if dw.passed:
            from pokebot.game_plan import Gameplan
            from pokebot.fight.pokemon import OwnPokemon
            from pokebot.gameplay.item import Items
            from pokebot.combiner import go_to

            Gameplan.set_new_game()
            OwnPokemon.new_game()
            Items.new_game()
            self.vba.reset_game()

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

    @discards_changes
    @saves_action
    def load_this_file(self, f):
        from pokebot.fundamentals.load_game import load_game
        print(f"Loading")
        try:
            # file
            num = int(''.join([s for s in f if s.isdigit()]))
            self.vba.load_game(num)
            # database
            load_game(f)
        except Exception:
            logger.error('Err: ', exc_info=True)

    def list_saved_games(self):
        import os
        return [filename for i, filename in enumerate(os.listdir(self.VBA_DIR)) if filename.endswith('sgm')]

    @saves_action
    def save_this_file(self, slot):
        f = f"Pokemon Blue{slot}.sgm"
        print(f"sving {f}")
        if f in self.list_saved_games():
            print(f"{f} already in saved games")
            od = OverwriteDialog()
            od.exec()
            if not od.passed:
                print(f"cancel save")
                return
        print(f"saving on {f}")

        try:
            from pokebot.fundamentals.save_game import save_game
            self.vba.save_game(slot)
            save_game(f, slot)
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


        self.ash_label = QLabel()
        self.pixmap = QPixmap('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\dashboard\\assets\\' + 'ash' + '.png')
        self.ash_label.setPixmap(self.pixmap)


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

    def getInputs(self):
        return (self.first.text(), self.second.text())

    def accept(self):
        from pokebot.game_plan import Gameplan
        if self.first.text() and self.second.text():
            # if there is any input
            p = Gameplan.set_player_name(self.first.text())
            r = Gameplan.set_rival_name(self.second.text())
            self.passed = True
        super().accept()

    def reject(self):
        self.passed = False
        super().reject()

    @staticmethod
    def convert_cv_qt_pixelmap(cv_img):
        ''''Converts a open cv image to a qt pixmap.'''

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


class SaveDialog(QDialog):
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
        self.passed = True
        super().accept()



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
