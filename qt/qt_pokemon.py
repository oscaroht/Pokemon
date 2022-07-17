from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from typing import List
import logging

from pokebot.fight.pokemon import OwnPokemon, OwnMove

logger = logging.getLogger(__name__)

class QPokemon(QWidget):

    pixmaps = {}
    assets_folder = 'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\dashboard\\assets\\'

    def __init__(self, parent: QMainWindow = None):
        self.label = QLabel(parent)
        self.current_pixmap_key = None

        # pokemon hpBar
        self.hp_progressbar = QProgressBar(parent)
        self.hp_progressbar.setStyleSheet(
            " QProgressBar { text-align: center; } QProgressBar::chunk {background-color: #3add36; width: 1px;}")
        # self.hp_progressbar.setValue(100)
        self.hp_progressbar.setFormat('HP bar')
        self.hp_progressbar.adjustSize()

        # moves
        self.moves = QMoves(parent)

        self.groupbox = self.set_groupbox(parent)

        # fill it with empty pokemon
        self.default()

    def set_groupbox(self, parent: QMainWindow = None) -> QGroupBox:
        """"
        Combines all pokemon partial widgets to a pokemon group box.
        """
        # combine progressbar and moves
        hp_and_moves_layout = QVBoxLayout()
        hp_and_moves_layout.addWidget(self.hp_progressbar)
        hp_and_moves_layout.addLayout(self.moves.layout())

        # combine pokemon label, image, hp and moves
        pokemon_layout = QHBoxLayout()
        pokemon_layout.addWidget(self.label, stretch=1)
        pokemon_layout.addLayout(hp_and_moves_layout, stretch=2)
        pokemon_groupbox = QGroupBox(parent.tr(f"Pokemon .."))
        pokemon_groupbox.setLayout(pokemon_layout)
        return pokemon_groupbox

    def default(self):
        """"
        Set all dashboard attributes to the default/empty state
        """
        self.groupbox.setTitle('--')
        self.set_pixmap('poke_ball')
        self.hp_progressbar.setValue(0)
        for qm in self.moves.moves_list:
            qm.empty()


    def update(self, pokemon: OwnPokemon) -> None:
        """"
        Updates 1 pokemon group box. It updates the image (pixmap), name and level (title), hp bar, and calls the
        moves update function.
        """
        # image
        if self.current_pixmap_key is not None and pokemon.name != self.current_pixmap_key:
            self.set_pixmap(pokemon.name)

        # name and level
        self.groupbox.setTitle(pokemon.own_name + '   L:' + str(pokemon.level))

        # hp bar
        hp_percentage = int(100 * pokemon.current_hp / int(pokemon.stats['hp']))
        self.hp_progressbar.setValue(hp_percentage)
        if hp_percentage < 20:
            self.hp_progressbar.setStyleSheet(
                " QProgressBar { text-align: center; } QProgressBar::chunk {background-color: red;}")
        else:
            self.hp_progressbar.setStyleSheet(
                " QProgressBar { text-align: center; } QProgressBar::chunk {background-color: #3add36;}")

        self.moves.update(pokemon.moves)

    def set_pixmap(self, key: str) -> None:
        """"
        If the key (image name) is in the pixmap dict class attribute we use that instance in the dict to set the label.
        It is loaded from disk if the image name is not in the keys.
        """
        if key not in QPokemon.pixmaps:
            self.load_pixmap(key)
        self.label.setPixmap(QPokemon.pixmaps[key])
        self.current_pixmap_key = key

    @classmethod
    def load_pixmap(cls, name: str) -> None:
        """"
        Loads the pixmap from disk and adds it to memory (pixmap dict class attribute)
        """
        logger.debug(f"Load pixmap {name}")
        pixmap = QPixmap(cls.assets_folder + name + '.png').scaled(128, 128)
        if name == 'poke_ball':
            pixmap = QPixmap(cls.assets_folder + name + '.png').scaled(90, 90)  # this image need to be smaller
        cls.pixmaps[name] = pixmap


class QMoves(QWidget):
    """"
    Wrapper for 4 move widgets.
    """
    def __init__(self, parent: QMainWindow = None):
        self.moves_list = []
        for i in range(4):
            self.moves_list.append(QMove(parent, i))

    def layout(self):
        moves_grid_layout = QGridLayout()
        for j in range(4):
            moves_grid_layout.addWidget(self.moves_list[j].groupbox, int(j / 2 + 1), j % 2)
        moves_grid_layout.setColumnStretch(0, 1)
        moves_grid_layout.setColumnStretch(1, 1)
        return moves_grid_layout

    def update(self, moves: List[OwnMove]):
        for q, m in zip(self.moves_list, moves):
            q.update(m)


class QMove(QWidget):
    """"
    Individual move widget.
    """

    progress_bar_style_string = " QProgressBar { text-align: center; height: 2px } QProgressBar::chunk " \
                                "{background-color: #7D94B0; width: 1px; height: 2px;}"

    def __init__(self, parent: QMainWindow, index: int):
        self.pp_progressbar = QProgressBar(parent)
        self.pp_progressbar.setStyleSheet(self.progress_bar_style_string)
        self.pp_progressbar.setValue(50)
        self.pp_progressbar.setFormat('PP bar')

        self.label = QLabel(parent)
        self.label.setText(f'move {index}')

        self.groupbox = self.groupbox()

    def groupbox(self) -> QGroupBox:
        """"
        Combines the single move groupbox and vertical layout for 1 move widget.
        """
        single_move_layout = QVBoxLayout()
        single_move_layout.addWidget(self.label)
        single_move_layout.addStretch(4)
        single_move_layout.addWidget(self.pp_progressbar)
        single_move_layout.addStretch(1)

        single_move_groupbox = QGroupBox()
        single_move_groupbox.setLayout(single_move_layout)
        return single_move_groupbox

    def update(self, m: OwnMove) -> None:
        """"
        Updates all 4 move widgets.
        """
        self.label.setText(m.name)
        self.pp_progressbar.setValue(int(100 * m.pp / m.max_pp))

    def empty(self) -> None:
        """"
        Empties all 4 move widgets as if there where no moves.
        """
        self.label.setText('')
        self.pp_progressbar.setValue(0)

class QParty(QWidget):
    """"
    Wrapper for 6 pokemon widgets.
    """

    def __init__(self, parent: QMainWindow = None):
        self.all = []
        for i in range(6):
            self.all.append(QPokemon(parent))
        self.groupbox = self.set_groupbox(parent)

    def set_groupbox(self, parent) -> QGroupBox:
        """"
        Creates groupbox and grid layout for 6 pokemon widgets
        """
        # combine to make a party box
        party_groupbox = QGroupBox(parent.tr("Party"))
        grid_layout = QGridLayout()
        for i in range(6):
            row = int(i / 2 + 1)
            col = i % 2
            grid_layout.addWidget(self.all[i].groupbox, row, col)  # left -> right, up->down
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)
        party_groupbox.setLayout(grid_layout)
        return party_groupbox

    def update(self):
        """"
        Updates all 6 pokemon widgets.
        """
        for i, q in enumerate(self.all):
            if i >= len(OwnPokemon.party):
                # clear
                q.default()
            else:
                q.update(OwnPokemon.party[i])


