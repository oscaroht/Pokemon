
from PIL import ImageGrab
import numpy as np
import cv2

from settings import vertical_offset, scale_factor, screen_scale_factor, native_w, native_h

def screen_grab(resize=False, test = False):
    ''''Takes an image of the screen.

     Depending on the screen settings in settings.py the screen  '''

    # So the pillow image grab object uses the scale and layout zoom factor in windows -> settings -> display
    # To make the program display independent we need to multiply by this factor
    screen1 = np.array(ImageGrab.grab(bbox=( 0,
                                             int(vertical_offset*screen_scale_factor),
                                             int(scale_factor*native_w*screen_scale_factor),
                                             int((scale_factor*native_h+vertical_offset)*screen_scale_factor)))) # x1,y1,x2,y2 +140, +150
    screen = cv2.cvtColor(screen1, cv2.COLOR_BGR2GRAY) # convert to gray scale
    screen = cv2.resize(screen, (scale_factor*native_w, scale_factor*native_h)) # resize so it has the same size as the window

    if resize == True:
        screen = np.where(screen == 0, 1, screen)
        return cv2.resize(screen, (0, 0),fx=1/scale_factor,fy=1/scale_factor)

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


