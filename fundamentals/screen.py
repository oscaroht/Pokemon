
from PIL import ImageGrab
import numpy as np
import cv2

from fundamentals.config import config

def screen_grab():

    param = config('./settings.ini', 'window_size')
    w = int(param['w'])
    h = int(param['h'])
    vertical_offset = int(param['vertical_menu_offset'])
    horizontal_offset = int(param['horizontal_offset'])

    #screen1 = np.array(ImageGrab.grab(bbox=(0+10,60,640+150,576+60)))

    ## for some reason the PIL and CV libs do not match in size so we need to resize
    screen1 = np.array(ImageGrab.grab(bbox=(0 + horizontal_offset, vertical_offset, w+horizontal_offset+140, h+vertical_offset+150))) # x1,y1,x2,y2
    screen = cv2.cvtColor(screen1, cv2.COLOR_BGR2GRAY)
    screen = cv2.resize(screen, (w, h))

    # testing
    # cv2.imshow('screen',screen)
    # cv2.waitKey()

    return screen