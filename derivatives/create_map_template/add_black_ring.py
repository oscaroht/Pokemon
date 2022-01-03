import numpy as np
import cv2

ub = 4 # number of upper black rows
db = 4 # number of lower black row
lb = 3 # left
rb = 4 # right

tile_size=16
img=cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\walk\\templates\\map\\pewter_city_gym.png')
img = img[1:225, 1:161]
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
# cv2.imshow('d',im2)
cv2.imwrite('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\walk\\templates\\map\\pewter_city_gym_b.png',im2)



