
import pytesseract

import os
import cv2
from fundamentals.config import config
from fundamentals.screen import screen_grab

os.chdir(os.path.dirname(os.path.realpath(__file__)))
path = config('../settings.ini', 'tesseract', 'path')
w = int(config('../settings.ini', 'window_size', 'native_w'))
h = int(config('../settings.ini', 'window_size', 'native_h'))
pytesseract.pytesseract.tesseract_cmd = path

screen = screen_grab(resize=True)
screen_large = screen_grab()

roi_bar = screen_large[int(103 * h * 4 / 144):int(138 * h * 4 / 144), int(7 * w * 4 / 160):int(144 * w * 4 / 160)]

cv2.imshow('bar',roi_bar)
cv2.waitKey()

""""Page segmentation modes:
  0    Orientation and script detection (OSD) only.
  1    Automatic page segmentation with OSD.
  2    Automatic page segmentation, but no OSD, or OCR.
  3    Fully automatic page segmentation, but no OSD. (Default)
  4    Assume a single column of text of variable sizes.
  5    Assume a single uniform block of vertically aligned text.
  6    Assume a single uniform block of text.
  7    Treat the image as a single text line.
  8    Treat the image as a single word.
  9    Treat the image as a single word in a circle.
 10    Treat the image as a single character.
 11    Sparse text. Find as much text as possible in no particular order.
 12    Sparse text with OSD.
 13    Raw line. Treat the image as a single text line,
                        bypassing hacks that are Tesseract-specific."""


"""" Does not appear to work super well. Maybe try to make a traineddata file myself. Also check out if it kan use 
language (english) elements as well and add pokemon names and terms"""

# psm 3,4,6 work well as well as 11
text = pytesseract.image_to_string(roi_bar, lang='Pokemon', config='--oem 1 --psm 11 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890.!' )

test=1