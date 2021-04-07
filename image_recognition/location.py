
'''''We are going to take a screen image, cut the player out and compare that with the shrunk cpo version of the map.
Maybe we can even store the shrunk cpo versions. Maybe this improves performance.'''


import numpy as np
import cv2

from fundamentals.load_templates import load_templates

from fundamentals.screen import screen_grab


def Retrive_image(curmap):
    ''''This is a temporary function used to load a test map. In future the initialization file will be used to load
    all templates to memory at once and make them global 'variables'.'''

    direc='C:\\Users\\oscar\\PycharmProjects\\Pokemon\\templates\\Map\\'
    path=direc+str(curmap)+'.png'
    img_tem=cv2.imread(path)
    img=cv2.cvtColor(img_tem, cv2.COLOR_BGR2GRAY)
    return img

def get_current_map(name):
    ''''This is a temporary function used to to take the current map from the the temp_list'''

    ''''Need better way to navigate the data structure. Maybe indexing.'''
    if 'temp_list' not in globals():
        global temp_list
        temp_list = load_templates()

    for t in temp_list:
        if t.name == name: # 'pellet_town':
            return t.img

def cpo(img, tile_size):
    ''''This function cuts the player out. It works both on the map(template) as on the screen. In case the screen is
    used the tilesize should be set to w / 16*10 or h / 16*9. In case the map is used, use the native tile size of 16
    pixels per tile.'''

    im_ul = img[0:int(3.5 * tile_size), 0:int(3.5 * tile_size)]
    im_ur = img[0:int(3.5 * tile_size), int(5.5 * tile_size):(10 * tile_size)]
    im_dl = img[int(5.5 * tile_size): (9 * tile_size), 0:int(3.5 * tile_size)]
    im_dr = img[int(5.5 * tile_size): (9 * tile_size), int(5.5 * tile_size):(10 * tile_size)]
    vis_up = np.concatenate((im_ul, im_ur), axis=1)
    vis_down = np.concatenate((im_dl, im_dr), axis=1)
    vis = np.concatenate((vis_up, vis_down), axis=0)
    return vis


def map_to_cor(im): # im is a large map
    ''''The idea is to iterate over the image using the same iterator as was used to create the coordinates tables for
    the database. The ids will be the same as long as the map is made with care.'''
    mapping = {}
    h, w = im.shape
    id = 1
    for y in range(int(h / 16) - 8):
        for x in range(int(w / 16) - 9):
            mapping[id] = {'img' :cpo(im[y*16:(y*16+144),x*16:(x*16+160)],16), 'x':x, 'y':y }

            id += 1
    return mapping

def get_position(mapping, screen):
    ''''This function returns the node0_id where the player is at this very moment.'''

    screen_cpo = cpo(screen, 16*4) ## It appears to be 16 times 4 Not sure about the 16, should check

    h, w = mapping[1]['img'].shape
    screen_cpo = cv2.resize(screen_cpo, (w, h))

    res_max = 0
    node0_id = None
    best_id = None
    for id in range(1, len(mapping)+1):                 # +1 because database id starts at 1
        screen = cv2.resize(screen_cpo, (w, h))
        #TODO check the match function
        res = cv2.matchTemplate(screen, mapping[id]['img'], cv2.TM_CCOEFF_NORMED)  # CCOEFF_NORMED) # CCORR_NORMED
        if np.max(res)>res_max: # TODO maybe if match is higher than 90% or so break from the loop
            res_max = res
            best_id = id
    return best_id, mapping[best_id]['x'], mapping[best_id]['y']

def get_position_wrapper(map_name):
    return get_position(map_to_cor(get_current_map(map_name)),screen_grab())


# Make sure to load this only once!!!
img = get_current_map('pellet_town')
mapping = map_to_cor(img)

# only this depends per coordinate!!
(id, x, y) = get_position(mapping,screen_grab())

# img = cpo(screen_grab(),16*4)
# cv2.imshow('screen',img)
# cv2.waitKey()


