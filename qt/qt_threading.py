import sys
from time import sleep
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

# https://www.pythonguis.com/tutorials/creating-your-own-custom-widgets/

# from pokebot.fight import OwnPokemon

# Step 1: Create a worker class
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        """Long-running task."""

        # import from_new_game

        for i in range(5):
            sleep(1)
            self.progress.emit(i + 1)
        self.finished.emit()

class Pokemon(QtWidgets.QWidget):
    pass

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicksCount = 0
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Freezing GUI")
        self.setGeometry(100, 100, 600, 400)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # Create and connect widgets
        self.clicksLabel = QLabel("Counting: 0 clicks", self)
        self.clicksLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.countBtn = QPushButton("Click me!", self)
        # self.countBtn.setGeometry(20, 15, 10, 40)
        self.countBtn.clicked.connect(self.countClicks)

        self.stepLabel = QLabel("Long-Running Step: 0")
        self.stepLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.longRunningBtn = QPushButton("Long-Running Task!", self)
        self.longRunningBtn.setGeometry(20, 15, 10, 40)
        self.longRunningBtn.clicked.connect(self.runLongTask)

        self.pokemon_label = QLabel(self)
        pixmap = QPixmap('poke_ball.png')
        self.pokemon_label.setPixmap(pixmap)
        # self.setCentralWidget(label)
        # self.resize(pixmap.width(), pixmap.height())

        self.label_1 = QLabel("new border ", self)
        # moving position
        self.label_1.move(100, 100)
        self.label_1.setStyleSheet("border :3px solid black; fill :3px solid black")

        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.clicksLabel)
        layout.addWidget(self.countBtn)
        layout.addStretch()
        layout.addWidget(self.stepLabel)
        layout.addWidget(self.longRunningBtn)
        layout.addWidget(self.pokemon_label)
        layout.addWidget(self.label_1)
        self.centralWidget.setLayout(layout)



    def countClicks(self):
        self.clicksCount += 1
        self.clicksLabel.setText(f"Counter: {self.clicksCount}")

        self.pokemon_label.setPixmap(QPixmap('arbok.png'))

        # self.clicksLabel.setText(f"Party: {OwnPokemon.party}")

    def reportProgress(self, n):
        self.stepLabel.setText(f"Long-Running Step: {n}")

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
        self.worker.progress.connect(self.reportProgress)
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
    sys.exit(app.exec())