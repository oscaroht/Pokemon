
'''''We are going to take a screen image, cut the player out and compare that with the shrunk cpo version of the map.
Maybe we can even store the shrunk cpo versions. Maybe this improves performance.'''


import numpy as np
import cv2

from walk.templates import temp_list
from fundamentals.screen import screen_grab

class LocationNotFound(Exception):
    pass

class Position:

    map_name = None
    cor_id = -1
    x = -1
    y = -1

    position = (map_name, cor_id, x, y)

    @classmethod
    def _set_position(cls,map,id,x,y):
        cls.map_name = map
        cls.cor_id = id
        cls.x = x
        cls.y = y

        cls.position = ((map, id, x, y))

    @classmethod
    def _get_current_map(cls,map):
        ''''This is a temporary function used to to take the current map from the the temp_list'''

        if isinstance(map,str):
            ''''Need better way to navigate the data structure. Maybe indexing.'''
            for t in temp_list:
                if t.name == map: # 'pellet_town':
                    return t.img
            # maybe it is a group
            list=[]
            for t in temp_list:
                if t.group == map:
                    list.append(t)
            if list != []:
                return list

        elif isinstance(map,int):
            ''''Need better way to navigate the data structure. Maybe indexing.'''
            for t in temp_list:
                if t.id == map: # 'pellet_town':
                    return t.id

    @classmethod
    def _cpo(cls,img, tile_size):
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

    @classmethod
    def _map_to_cor(cls,im): # im is a large map
        ''''The idea is to iterate over the image using the same iterator as was used to create the coordinates tables for
        the database. The ids will be the same as long as the map is made with care.'''
        mapping = {}
        h, w = im.shape
        id = 1
        for y in range(int(h / 16) - 8):
            for x in range(int(w / 16) - 9):
                mapping[id] = {'img' :cls._cpo(im[y * 16:(y * 16 + 144), x * 16:(x * 16 + 160)], 16), 'x':x, 'y':y}

                id += 1
        return mapping  # a dict with img, x, y as keys

    @classmethod
    def _get_position_in_map(cls,mapping, screen):
        ''''This function returns the node0_id where the player is at this very moment.'''

        screen_cpo = cls._cpo(screen, 16 * 4)

        # testing
        # cv2.imshow('screen_cpo', screen_cpo)
        # cv2.waitKey()

        h, w = mapping[1]['img'].shape
        screen_cpo = cv2.resize(screen_cpo, (w, h))

        res_max = 0
        node0_id = None
        best_id, best_x, best_y = None, None, None
        for id in range(1, len(mapping)+1):                 # +1 because database id starts at 1
            screen = cv2.resize(screen_cpo, (w, h))
            #TODO check the match function
            res = cv2.matchTemplate(screen, mapping[id]['img'], cv2.TM_CCOEFF_NORMED)  # CCOEFF_NORMED) # CCORR_NORMED
            if np.max(res)>res_max: # TODO maybe if match is higher than 90% or so break from the loop if performance is an issue
                res_max = res
                best_id = id

        if res_max < 0.5:
            print('threshold of 0.5 not passed')
            return None

        best_x = mapping[best_id]['x']
        best_y = mapping[best_id]['y']
        return best_id, best_x , best_y

    @classmethod
    def get_position(cls):
        ''''
        map: int or str '''
        cor = (cls.map_name, cls.x, cls.y)

        '''' if a map name or id is given is given than check if we find a coordinate. If not move on to all templates'''
        if cls.map_name != None:
            cor = cls._get_position_in_map(cls._map_to_cor(cls._get_current_map(cls.map_name)), screen_grab())
            if cor != None:                     # if cor is not None than this was indeed the map
                return (cls.map_name, *cor)

        '''' no map name was given or no cor was found for the given map name. Lets look in all templates and find the
         position  '''
        for t in temp_list:
            # iterate over all map templates
            if t.group == 'map':
                print(f' trying {t.name}')
                cor = cls._get_position_in_map(cls._map_to_cor(cls._get_current_map(t.name)), screen_grab())
                if cor != None:
                    print('found')
                    cls._set_position(t.name, *cor)
                    return (t.name , *cor)
        raise LocationNotFound


def main():
    Position.get_position()
    print(Position.position)

if __name__ == '__main__':

    main()
