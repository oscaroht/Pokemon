

import cv2
import numpy as np

file = 'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\templates\\orientation\\down\\template_down_x1.png'

img = cv2.imread(file)
img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
# cv2.imshow('img',img)
# cv2.waitKey()

# size is 18, 16
mask = np.zeros(img.shape[:2], dtype="uint8")
cv2.rectangle(mask, (1, 1), (14, 16), 255, -1)
# cv2.imshow('mask',mask)
# cv2.waitKey()

''''DOWN mask for the down position'''
mask[1][1] = 0
mask[1][2] = 0
mask[1][3] = 0
mask[1][4] = 0
mask[1][14] = 0
mask[1][13] = 0
mask[1][12] = 0
mask[1][11] = 0

mask[2][1] = 0
mask[2][2] = 0
mask[2][3] = 0
mask[2][14] = 0
mask[2][13] = 0
mask[2][12] = 0

mask[3][1] = 0
mask[3][2] = 0
mask[3][ 13] = 0
mask[3][14] = 0

mask[4][1] = 0
mask[4][2] = 0
mask[4][13] = 0
mask[4][14] = 0

mask[5][1] = 0
mask[5][14] = 0

mask[6][1] = 0
mask[6][14] = 0

mask[13][1] = 0
mask[13][14] = 0

mask[14][1] = 0
mask[14][2] = 0
mask[14][13] = 0
mask[14][14] = 0

mask[15][1] = 0
mask[15][2] = 0
mask[15][13] = 0
mask[15][14] = 0

mask[16][1] = 0
mask[16][2] = 0
mask[16][3] = 0

mask[16][7] = 0
mask[16][8] = 0

mask[16][12] = 0
mask[16][13] = 0
mask[16][14] = 0

masked = cv2.bitwise_and(img, img, mask=mask)
masked = cv2.resize(masked, (500,500), interpolation = cv2.INTER_AREA)

cv2.imshow("Mask Applied to Image", masked)
cv2.waitKey(0)
cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\templates\\orientation\\down\\mask_down.jpg', mask)


test = 1