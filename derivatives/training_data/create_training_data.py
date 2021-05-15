import numpy as np
import string
from PIL import Image, ImageFont, ImageDraw, ImageOps
import random
import cv2


def get_bounded_image(img):
    img = np.array(img)
    black_rows = []
    black_cols = []
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if img[y][x] == 0:
                black_rows.append(y)
                black_cols.append(x)

    b_img = img[min(black_rows):max(black_rows),min(black_cols):max(black_cols)]

    return b_img, max(black_rows), max(black_cols)

def MakeImg(t, font, fn, img_size):
    '''
    Generate an image of text
    t:      The text to display in the image
    f:      The font to use
    fn:     The file name
    s:      The image size
    o:      The offest of the text in the image
    '''
    img = Image.new('RGB', img_size, "white")
    draw = ImageDraw.Draw(img)
    # for some reason there is a stupid offset. No idea why you would do this but taking the negative of the offset
    # fixes everything
    offset = font.getoffset(t)
    draw.text(( -offset[0],-offset[1]), t, (0, 0, 0), font=font)
    img = ImageOps.grayscale(img)

    b_img, max_y, max_x = get_bounded_image(img)
    img = np.zeros([32, 32], dtype=np.uint8)
    img.fill(255)  # or img[:] = 255

    x_off = int(random.uniform(1,32-max_x))
    y_off = int(random.uniform(1,32-max_y))

    img[y_off:b_img.shape[0]+y_off, x_off:b_img.shape[1]+x_off] = b_img

    cv2.imwrite(fn, img)



# The possible characters to use
characters = list(string.digits) + list(string.ascii_letters) + ['é','!','.','!','!','/','/','?',"'"]

# Image size
img_size = (32, 32)
Y = []
i = 0
for font_size in [30,32,34]:
    font = ImageFont.truetype("Pokemon GB.ttf", font_size)
    for char in characters:
        for count in range(20):
            MakeImg(char, font, str(i) + '.png', img_size)
            Y.append(str(i) + '.png,' + char)
            i+=1

# Write CSV file
with open('Train.csv', 'w') as F:
    F.write('\n'.join(Y))



