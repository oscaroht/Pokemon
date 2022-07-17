
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QPainter

from typing import List
import logging

# from pokebot.fight.pokemon import OwnPokemon, OwnMove

logger = logging.getLogger(__name__)

class QCallStack(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.calls = []
        layout = QVBoxLayout()
        for i in range(4):
            # layout.addSpacing(500)
            layout.addStretch(10)
            label = QLabel(parent)

            qp = QPainter()
            qp.begin(self)
            qp.drawRect(50, 50, 100, 10)
            qp.end()

            btn = QPushButton(f"test {1}")
            btn.setStyleSheet("""
            QPushButton:hover {
                background-color: #d7d6d5;
            }
            """)
            label.setText(f'test {i}')
            self.calls.append(btn)

            layout.addWidget(btn)

        self.setLayout(layout)





if __name__ == '__main__':
    import sys
    class Window(QMainWindow):
        """Main Window."""

        def __init__(self, parent=None):
            """Initializer."""
            super().__init__(parent)

            self.unsaved_actions = True

            self.setWindowTitle("Menus & Toolbars")
            self.resize(400, 200)
            self.centralWidget = QCallStack(self)  # QLabel("Central Widget")
            # self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setCentralWidget(self.centralWidget)



    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
