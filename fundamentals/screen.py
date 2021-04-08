
from PIL import ImageGrab
import numpy as np
import cv2
import os

from fundamentals.config import config

def screen_grab(resize=False):

    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    param = config('../settings.ini', 'window_size')
    w = int(param['w'])
    h = int(param['h'])
    vertical_offset = int(param['vertical_menu_offset'])
    horizontal_offset = int(param['horizontal_offset'])

    ## for some reason the PIL and CV libs do not match in size so we need to resize
    screen1 = np.array(ImageGrab.grab(bbox=(0 + horizontal_offset, vertical_offset, w+horizontal_offset+140, h+vertical_offset+150))) # x1,y1,x2,y2
    screen = cv2.cvtColor(screen1, cv2.COLOR_BGR2GRAY)
    screen = cv2.resize(screen, (w, h)) # resize so it has the same size as the window

    if resize == True:
        x = int(config('../settings.ini', 'window_size','x'))
        screen = np.where(screen == 0, 1, screen)
        return cv2.resize(screen, (0, 0),fx=1/x,fy=1/x)

    # testing
    # cv2.imshow('screen',screen)
    # cv2.waitKey()

    return screen