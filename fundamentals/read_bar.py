
import pytesseract
import os
import cv2
import numpy as np
from fundamentals.config import config
from fundamentals.screen import screen_grab
from fundamentals.ocr import OCR



#from derivatives.train_ocr import model

os.chdir(os.path.dirname(os.path.realpath(__file__)))
path = config('../settings.ini', 'tesseract', 'path')
w = int(config('../settings.ini', 'window_size', 'native_w'))
h = int(config('../settings.ini', 'window_size', 'native_h'))
pytesseract.pytesseract.tesseract_cmd = path


# cv2.imshow('bar',roi_bar)
# cv2.waitKey()

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
#text = pytesseract.image_to_string(roi_bar, lang='Pokemon', config='--oem 1 --psm 11 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890.!' )


def preprocess(roi):
    # blur the image so the mega pixels get joined in on contour
    kernel = np.ones((5,5),np.float32)/25
    img = cv2.filter2D(roi,-1,kernel)

    # threshold after blurring. Set quite high so blure was effective
    _, thresh = cv2.threshold(img, 170, 255, 0)
    return thresh

# contours_1, hierarchy_1 = cv2.findContours(img[:90, :], 1, 2)
# contours_2, hierarchy_2 = cv2.findContours(img[90:,:], 1, 2)
def get_bbox(img):
    contours,_ = cv2.findContours(img[:90, :], 1, 2)

    def union(a, b):
        x0 = min(a[0], b[0])
        y0 = min(a[1], b[1])
        x1 = max(a[2], b[2])
        y1 = max(a[3], b[3])

        w = max(a[0] + a[2], b[0] + b[2]) - x
        h = max(a[1] + a[3], b[1] + b[3]) - y
        return [x0, y0, x1, y1]

    def box_sort(b):
        return b[0]

    # evaluate the contours
    bbox = list(list())
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        bbox.append([x, y, x + w, y + h])
    del bbox[0]  # first one is empty

    bbox.sort(key=box_sort)
    # del bbox[0]

    bbox_copy = bbox.copy()
    bbox_out = list(list()) # [[]]
    # for i, b in enumerate(bbox_copy):
    while len(bbox_copy) > 0:
        b = bbox_copy.pop(0)

        """" if the next box's end is before this box's end. With a small margin"""
        if len(bbox_copy) > 0:
            if bbox_copy[0][2] < b[2] + 5:
                bbox_out.append(union(b, bbox_copy[0]))
                bbox_copy.pop(0)
                continue
        bbox_out.append(b)
    return bbox_out


# testing
# cv2.imshow('img',thresh)
# cv2.waitKey()

def ocr(screen_section, bbox):

    # create white image of model shape
    img = np.zeros([32,32],dtype=np.uint8)
    img.fill(255) # or img[:] = 255
    signs = list()
    #del bbox[0]
    for b in bbox:
        # create white image of model shape
        img = np.zeros([32, 32], dtype=np.uint8)
        img.fill(255)  # or img[:] = 255
        letter = screen_section[b[1]:b[3], b[0]: b[2]]
        if letter.shape > img.shape:
            letter = cv2.resize(letter, img.shape)
        img[0:letter.shape[0], 0:letter.shape[1]] = letter
        _, img = cv2.threshold(img, 170, 255, 0)

        # prepare as model input
        img = img.reshape(32,32,1) / 255

        # cv2.imshow('a',img)
        # cv2.waitKey()

        chr_code = np.argmax(OCR.model.predict(np.array([img])), axis=1)
        character = OCR.char[int(chr_code)]
        signs.append(OCR.char[int(chr_code)])

    return signs


#     x, y, xw, yh = b
#     cv2.rectangle(thresh,(x,y),(xw,yh),(0,255,0),2)
#
#
# cv2.imshow('letters',thresh)
# cv2.waitKey()



if __name__ == '__main__':
    screen = screen_grab(resize=True)
    screen_large = screen_grab()

    roi_bar = screen_large[int(103 * h * 4 / 144):int(138 * h * 4 / 144), int(7 * w * 4 / 160):int(144 * w * 4 / 160)] # 152
    upper = roi_bar[:90, :]
    lower = roi_bar[90:, :]

    roi_bar_upper = preprocess(upper)
    roi_bar_lower = preprocess(lower)

    upper_bbox = get_bbox(roi_bar_upper)
    lower_bbox = get_bbox(roi_bar_lower)

    a = ocr(upper, upper_bbox)
    b = ocr(lower, lower_bbox)

    test  =1

