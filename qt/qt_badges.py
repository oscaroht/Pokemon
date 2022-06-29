# from pokebot.gameplay.item import Items
# from qt.qt_dashboard import Window
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
import cv2
import logging
from datetime import datetime


class QBadges(QWidget):

    def __init__(self, win):
        self.badge_list = list()
        for b in ['bolder_badge', 'cascade_badge', 'thunder_badge', 'rainbow_badge', 'soul_badge', 'marsh_badge', 'volcano_badge', 'earth_badge']:
            self.badge_list.append(QBadge(win, b))
        self.groupbox = self.set_groupbox(win)

    def set_groupbox(self, win):
        badges_groupbox = QGroupBox(win.tr("Badges"))
        badges_layout = QGridLayout()
        for i in range(8):
            badges_layout.addWidget(self.badge_list[i].badge_label, int(i / 4 + 1), i % 4 + 1)
        badges_groupbox.setLayout(badges_layout)
        return badges_groupbox

    def update(self):
        for b in self.badge_list:
            b.update()

class QBadge(QWidget):

    def __init__(self, win, badge_filename):
        self.badge_filename = badge_filename
        self.badge_name = badge_filename.replace('_',' ')
        self.badge_label = QLabel(win)
        img = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\dashboard\\assets\\' + badge_filename + '.png',
                         cv2.IMREAD_UNCHANGED)
        self.pixmap = self.convert_cv_qt_pixelmap(img)
        self.pixmap.scaled(128, 128)

        self.pixmap_shadow = self.convert_cv_qt_pixelmap(self.shadow_image(img))
        self.pixmap_shadow.scaled(128, 128)

        self.badge_label.setPixmap(self.pixmap_shadow)

    def have(self):
        from pokebot.gameplay.item import Items
        return Items.do_i_have(self.badge_name)  # bool

    def update(self):
        from pokebot.gameplay.item import Items
        if Items.do_i_have(self.badge_name):  # bool
            self.badge_label.setPixmap(self.pixmap)
        else:
            self.badge_label.setPixmap(self.pixmap_shadow)

    @staticmethod
    def shadow_image(img):
        ''''Takes and returns a cv2 image with black color but opacity intact.

        It is used to shade the badges that are not yet obtained by the player.'''
        h = img.shape[0]
        w = img.shape[0]
        for y in range(h):
            for x in range(w):
                if img[y, x, 3] != 0:  # where the opacity is 0 (so not the background)
                    img[y, x, :3] = [0, 0, 0]  # set the color to black (nor the opacity to 0!)
        return img

    @staticmethod
    def convert_cv_qt_pixelmap(cv_img):
        ''''Converts a open cv image to a qt pixmap.'''

        h, w, ch = cv_img.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format_RGBA8888)
        return QPixmap.fromImage(convert_to_Qt_format)

