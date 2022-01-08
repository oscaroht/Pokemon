import numpy as np
import cv2

def right(img):
    return img[:,5*16:160]
def left(img):
    return img[:,0:4*16]

ub = 1 # number of upper black rows
db = 3 # number of lower black row
lb = 4 # left
rb = 5 # right

tile_size=16
img1=cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\walk\\templates\\map\\pewter_city_pc1.png')
img2=cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\walk\\templates\\map\\pewter_city_pc2.png')
img3=cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\walk\\templates\\map\\pewter_city_pc3.png')

img = cv2.hconcat([left(img3), right(img2), right(img1)])

cv2.imshow('joined image', img)
cv2.waitKey()

[h,w,a]=img.shape
if h/16!=int(h/16) or w/16!=int(w/16):
    raise Exception("not dev 16")

h_res=h+ub*tile_size+db*tile_size       # hight of final image

bbu=np.zeros((ub*tile_size,w,3),dtype=np.uint8)
bbd=np.zeros((db*tile_size,w,3),dtype=np.uint8)
bbr=np.zeros((h_res,rb*tile_size,3),dtype=np.uint8)
bbl=np.zeros((h_res,lb*tile_size,3),dtype=np.uint8)

im1=cv2.vconcat([bbu,img,bbd])
im2=cv2.hconcat([bbl,im1,bbr])
cv2.imshow('d',im2)
cv2.waitKey()
cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\walk\\templates\\map\\pewter_city_pc.png',im2)



