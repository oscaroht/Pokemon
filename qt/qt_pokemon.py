from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
import cv2

from pokebot.fight.pokemon import OwnPokemon, OwnMove

class QPokemon(QMainWindow):

    pixmaps = {}
    assets_folder = 'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\dashboard\\assets\\'

    def __init__(self, win):
        self.label = QLabel(win)
        self.current_pixmap_key = None

        # pokemon hpBar
        self.hp_progressbar = QProgressBar(win)
        self.hp_progressbar.setStyleSheet(
            " QProgressBar { text-align: center; } QProgressBar::chunk {background-color: #3add36; width: 1px;}")
        # self.hp_progressbar.setValue(100)
        self.hp_progressbar.setFormat('HP bar')
        self.hp_progressbar.adjustSize()

        # moves
        self.moves = QMoves(win)

        self.groupbox = self.set_groupbox(win)

        # fill it with empty pokemon
        self.default()

    def set_groupbox(self, win):

        # combine progressbar and moves
        hp_and_moves_layout = QVBoxLayout()
        hp_and_moves_layout.addWidget(self.hp_progressbar)
        hp_and_moves_layout.addLayout(self.moves.layout())

        # combine pokemon label, image, hp and moves
        pokemon_layout = QHBoxLayout()
        pokemon_layout.addWidget(self.label, stretch=1)
        pokemon_layout.addLayout(hp_and_moves_layout, stretch=2)
        pokemon_groupbox = QGroupBox(win.tr(f"Pokemon .."))
        pokemon_groupbox.setLayout(pokemon_layout)
        return pokemon_groupbox

    def default(self):
        self.groupbox.setTitle('--')
        self.set_pixmap('poke_ball')
        self.hp_progressbar.setValue(0)
        for qm in self.moves.moves_list:
            qm.empty()


    def update(self, pokemon):
        # image
        if self.current_pixmap_key is not None and pokemon.name != self.current_pixmap_key:
            #same pokemon so no need to update the image
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

    def set_pixmap(self, key):
        if key not in QPokemon.pixmaps:
            self.load_pixmap(key)
        self.label.setPixmap(QPokemon.pixmaps[key])
        self.current_pixmap_key = key

    @classmethod
    def load_pixmap(cls, name):
        print(f"Load pixmap {name}")
        pixmap = QPixmap(cls.assets_folder + name + '.png').scaled(128, 128)
        if name == 'poke_ball':
            pixmap = QPixmap(cls.assets_folder + name + '.png').scaled(90, 90)  # this image need to be smaller
        cls.pixmaps[name] = pixmap




class QMoves(QMainWindow):

    def __init__(self, win):
        self.moves_list=[]
        for i in range(4):
            self.moves_list.append(QMove(win, i))
    def layout(self):
        moves_grid_layout = QGridLayout()

        for j in range(4):
            moves_grid_layout.addWidget(self.moves_list[j].groupbox, int(j / 2 + 1), j % 2)
        moves_grid_layout.setColumnStretch(0, 1)
        moves_grid_layout.setColumnStretch(1, 1)
        return moves_grid_layout

    def update(self, moves):
        for q, m in zip(self.moves_list, moves):
            q.update(m)


class QMove(QMainWindow):

    def __init__(self, win, index):
        self.pp_progressbar = QProgressBar(win)
        self.pp_progressbar.setStyleSheet(
            " QProgressBar { text-align: center; height: 2px } QProgressBar::chunk {background-color: #7D94B0; width: 1px; height: 2px;}")
        self.pp_progressbar.setValue(50)
        self.pp_progressbar.setFormat('PP bar')

        self.label = QLabel(win)
        self.label.setText(f'move {index}')

        self.groupbox = self.groupbox()

    def groupbox(self):
        single_move_layout = QVBoxLayout()
        single_move_layout.addWidget(self.label)
        single_move_layout.addStretch(4)
        single_move_layout.addWidget(self.pp_progressbar)
        single_move_layout.addStretch(1)

        single_move_groupbox = QGroupBox()
        single_move_groupbox.setLayout(single_move_layout)
        return single_move_groupbox

    def update(self, m: OwnMove):
        self.label.setText(m.name)
        self.pp_progressbar.setValue(int(100 * m.pp / m.max_pp))
    def empty(self):
        self.label.setText('')
        self.pp_progressbar.setValue(0)

class QParty(QMainWindow):

    def __init__(self, win):
        self.all = []
        for i in range(6):
            self.all.append(QPokemon(win))
        self.groupbox = self.set_groupbox(win)

    def set_groupbox(self, win):
        # combine to make a party box
        party_groupbox = QGroupBox(win.tr("Party"))
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
        for i, q in enumerate(self.all):
            if i >= len(OwnPokemon.party):
                # clear
                q.default()
            else:
                q.update(OwnPokemon.party[i])


