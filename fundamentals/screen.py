
from PIL import ImageGrab
import numpy as np
import cv2
import os

from fundamentals.config import config

def screen_grab(resize=False, test = False):

    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    param = config('../settings.ini', 'window_size')
    w = int(param['w'])
    h = int(param['h'])
    vertical_offset = int(param['vertical_menu_offset'])
    horizontal_offset = int(param['horizontal_offset'])

    # So the pillow image grab object uses the scale and layout zoom factor in windows -> settings -> display
    # To make the program display independent we need to multiply by this factor
    screen_scale_factor = 1
    screen1 = np.array(ImageGrab.grab(bbox=( 0, int(vertical_offset*screen_scale_factor), int(w*screen_scale_factor), int((h+vertical_offset)*screen_scale_factor)))) # x1,y1,x2,y2 +140, +150
    screen = cv2.cvtColor(screen1, cv2.COLOR_BGR2GRAY)
    screen = cv2.resize(screen, (w, h)) # resize so it has the same size as the window

    if resize == True:
        x = int(config('../settings.ini', 'window_size','x'))
        screen = np.where(screen == 0, 1, screen)
        return cv2.resize(screen, (0, 0),fx=1/x,fy=1/x)

    # testing
    if test:
        cv2.imshow('screen',screen)
        cv2.waitKey()

    return screen

# def read_bar():
#     import pytesseract
#
#     os.chdir(os.path.dirname(os.path.realpath(__file__)))
#     param = config('../settings.ini', 'window_size')
#     w = int(param['w'])
#     h = int(param['h'])
#     tesseract_path = config('../settings.ini', 'tesseract', 'path')
#
#     screen = screen_grab()
#
#     pytesseract.pytesseract.tesseract_cmd = tesseract_path
#
#     roi_bar = screen[int(103 * h / 144):int(138 * h / 144), int(8 * w / 160):int(153 * w / 160)]
#
#     text = pytesseract.image_to_string(roi_bar, lang='Pokemon')
#     return text


if __name__ == '__main__':
    screen_grab(test=True)


