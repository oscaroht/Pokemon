

import cv2
import numpy as np

# file = 'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\templates\\orientation\\down\\template_down_x1.png'
#file = 'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\templates\\orientation\\left\\template_left_x5.png'
# file = 'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\templates\\orientation\\right\\template_right_x1.png'
file = 'C:\\Users\\oscar\\PycharmProjects\\Pokemon\\templates\\orientation\\up\\template_up_x1.png'

img = cv2.imread(file)
img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
cv2.imshow('img',cv2.resize(img, (500,500), interpolation = cv2.INTER_AREA))
cv2.waitKey()

# size is 18, 16
mask = np.zeros(img.shape[:2], dtype="uint8")
cv2.rectangle(mask, (1, 1), (14, 16), 255, -1)

''''RIGHT'''
# mask[1][1] = 0
# mask[1][2] = 0
# mask[1][3] = 0
# mask[1][4] = 0
# mask[1][14] = 0
# mask[1][13] = 0
# mask[1][12] = 0
# mask[1][11] = 0
#
# mask[2][1] = 0
# mask[2][2] = 0
# mask[2][3] = 0
# mask[2][14] = 0
# mask[2][13] = 0
# mask[2][12] = 0
#
# mask[3][1] = 0
# mask[3][2] = 0
# mask[3][13] = 0
# mask[3][14] = 0
#
# mask[4][1] = 0
# mask[4][2] = 0
# mask[4][14] = 0
#
# mask[5][1]=0
# mask[6][1]=0
# mask[6][14]=0
# mask[7][1]=0
# mask[7][14]=0
# mask[7][13]=0
#
# mask[8][1]=0
# mask[8][2]=0
# mask[8][14]=0
# mask[8][13]=0
#
# mask[9][1]=0
# mask[9][2]=0
# mask[9][3]=0
# mask[9][14]=0
# mask[9][13]=0
#
# mask[10][1]=0
# mask[10][2]=0
# mask[10][14]=0
# mask[10][13]=0
# mask[10][12]=0
#
# mask[11][1]=0
# mask[11][2]=0
# mask[11][14]=0
# mask[11][13]=0
# mask[11][12]=0
# mask[11][11]=0
#
# mask[12][1]=0
# mask[12][2]=0
# mask[12][14]=0
# mask[12][13]=0
# mask[12][12]=0
# mask[12][11]=0
# mask[12][10]=0
#
# mask[13][1]=0
# mask[13][2]=0
# mask[13][14]=0
# mask[13][13]=0
# mask[13][12]=0
# mask[13][11]=0
# mask[13][10]=0
#
# mask[14][1]=0
# mask[14][2]=0
# mask[14][3]=0
# mask[14][14]=0
# mask[14][13]=0
# mask[14][12]=0
# mask[14][11]=0
#
# mask[15][1]=0
# mask[15][2]=0
# mask[15][3]=0
# mask[15][4]=0
# mask[15][14]=0
# mask[15][13]=0
# mask[15][12]=0
# mask[15][11]=0
#
# mask[16][1]=0
# mask[16][2]=0
# mask[16][3]=0
# mask[16][4]=0
# mask[16][5]=0
# mask[16][14]=0
# mask[16][13]=0
# mask[16][12]=0
# mask[16][11]=0
# mask[16][10]=0

''''DOWN mask for the down position'''
# mask[1][1] = 0
# mask[1][2] = 0
# mask[1][3] = 0
# mask[1][4] = 0
# mask[1][14] = 0
# mask[1][13] = 0
# mask[1][12] = 0
# mask[1][11] = 0
#
# mask[2][1] = 0
# mask[2][2] = 0
# mask[2][3] = 0
# mask[2][14] = 0
# mask[2][13] = 0
# mask[2][12] = 0
#
# mask[3][1] = 0
# mask[3][2] = 0
# mask[3][ 13] = 0
# mask[3][14] = 0
#
# mask[4][1] = 0
# mask[4][2] = 0
# mask[4][13] = 0
# mask[4][14] = 0
#
# mask[5][1] = 0
# mask[5][14] = 0
#
# mask[6][1] = 0
# mask[6][14] = 0
#
# mask[13][1] = 0
# mask[13][14] = 0
#
# mask[14][1] = 0
# mask[14][2] = 0
# mask[14][13] = 0
# mask[14][14] = 0
#
# mask[15][1] = 0
# mask[15][2] = 0
# mask[15][13] = 0
# mask[15][14] = 0
#
# mask[16][1] = 0
# mask[16][2] = 0
# mask[16][3] = 0
#
# mask[16][7] = 0
# mask[16][8] = 0
#
# mask[16][12] = 0
# mask[16][13] = 0
# mask[16][14] = 0

'''Left'''
# mask[1][1]=0
# mask[1][2]=0
# mask[1][3]=0
# mask[1][4]=0
# mask[1][14]=0
# mask[1][13]=0
# mask[1][12]=0
# mask[1][11]=0
#
#
#
# mask[2][1]=0
# mask[2][2]=0
# mask[2][3]=0
# mask[2][14]=0
# mask[2][13]=0
# mask[2][12]=0
#
# mask[3][1]=0
# mask[3][2]=0
# mask[3][14]=0
# mask[3][13]=0
#
# mask[4][1]=0
# mask[4][14]=0
# mask[4][13]=0
#
# mask[5][14]=0
#
# mask[6][1]=0
# mask[6][14]=0
# mask[7][1]=0
# mask[7][2]=0
# mask[7][2]=0
# mask[7][14]=0
# mask[8][1]=0
# mask[8][2]=0
# mask[8][14]=0
# mask[8][13]=0
# mask[9][1]=0
# mask[9][2]=0
# mask[9][14]=0
# mask[9][13]=0
# mask[9][12]=0
#
# mask[10][1]=0
# mask[10][2]=0
# mask[10][3]=0
# mask[10][14]=0
# mask[10][13]=0
#
# mask[11][1]=0
# mask[11][2]=0
# mask[11][3]=0
# mask[11][4]=0
# mask[11][14]=0
# mask[11][13]=0
# mask[12][1]=0
# mask[12][2]=0
# mask[12][3]=0
# mask[12][4]=0
# mask[12][5]=0
# mask[12][14]=0
# mask[12][13]=0
# mask[13][1]=0
# mask[13][2]=0
# mask[13][3]=0
# mask[13][4]=0
# mask[13][5]=0
# mask[13][14]=0
# mask[13][13]=0
# mask[14][1]=0
# mask[14][2]=0
# mask[14][3]=0
# mask[14][4]=0
# mask[14][13]=0
# mask[14][14]=0
# mask[14][12]=0
# mask[15][1]=0
# mask[15][2]=0
# mask[15][3]=0
# mask[15][4]=0
# mask[15][13]=0
# mask[15][14]=0
# mask[15][12]=0
# mask[15][11]=0
# mask[16][1]=0
# mask[16][2]=0
# mask[16][3]=0
# mask[16][4]=0
# mask[16][5]=0
# mask[16][13]=0
# mask[16][14]=0
# mask[16][12]=0
# mask[16][11]=0
# mask[16][10]=0

''''UP'''
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

mask[9][1]=0
mask[9][14]=0
mask[10][1]=0
mask[10][14]=0

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



mask_view = cv2.resize(mask, (500,500), interpolation = cv2.INTER_AREA)
cv2.imshow('mask',mask_view)
cv2.waitKey()

masked = cv2.bitwise_and(img, img, mask=mask)
masked = cv2.resize(masked, (500,500), interpolation = cv2.INTER_AREA)

cv2.imshow("Mask Applied to Image", masked)
cv2.waitKey(0)
cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\templates\\orientation\\up\\mask_up.png', mask)


test = 1