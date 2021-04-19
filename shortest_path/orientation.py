
from fundamentals.screen import screen_grab
from fundamentals.load_templates import load_templates
from fundamentals.config import config

from fundamentals.globals import temp_list

import numpy as np
import cv2
import os

# os.chdir(os.path.dirname(os.path.realpath(__file__)))
# x = int(config('../settings.ini', 'window_size','x'))
#
# template = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\templates\\orientation\\down\\template_down_x1.png')
# mask = cv2.imread('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\templates\\orientation\\down\\mask_down.msk')
#
# mask = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)
# template = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
#
# screen = screen_grab()
# screen = cv2.resize(screen,(0,0),fx=1/x,fy=1/x)

## make zero pixels 1 such that we can norm the SQDIFF result.
# screen = np.where(screen==0, 1, screen)
#
# res = cv2.matchTemplate(screen, template, cv2.TM_SQDIFF_NORMED, mask=mask)
# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
# top_left = (min_loc[0]*x, min_loc[1]*x)
# bottom_right = (top_left[0] + template.shape[1]*x, top_left[1] + template.shape[0]*x)
#
# debug_screen = cv2.resize(screen,(0,0),fx=x,fy=x)
# debug_screen = cv2.cvtColor(debug_screen, cv2.COLOR_GRAY2RGB)
# cv2.rectangle(debug_screen, top_left, bottom_right, (0,255,255), 2)
# print(np.min(res))
# cv2.imshow('screen',debug_screen)
# cv2.waitKey()
#
# test=1




def get_orientation(threshold=0.15):
    screen = screen_grab(resize=True)

    # if 'temp_list' not in globals():
    #     print('not in globals')
    #     global temp_list
    # temp_list  = load_templates()


    # evaluate all templates
    best_score = 1
    for t in temp_list:
        if t.group == 'orientation':
            if t.mask is not None:
                res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED, mask=t.mask)
            else:
                res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if min_val < best_score:
                best_score = min_val
                t_best = t
    if best_score > threshold:
        print('No orientation found.')
        return None
    print(f'{t_best.name} with a score of {best_score}')
    return t_best.option

if __name__ == '__main__':
    t = get_orientation(0.15)
