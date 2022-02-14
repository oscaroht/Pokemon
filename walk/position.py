'''''We are going to take a screen image, cut the player out and compare that with the shrunk cpo version of the map.
Maybe we can even store the shrunk cpo versions. Maybe this improves performance.'''

import numpy as np
import cv2

from walk.templates import WalkTemplates
from fundamentals.screen import screen_grab
from graphs import G


class LocationNotFound(Exception):
    pass


class Position(G, WalkTemplates):
    map_name = None
    cor_id = -1
    x = -1
    y = -1

    position = (map_name, cor_id, x, y)

    @classmethod
    def get_position(cls):
        return cls.map_name, cls.cor_id, cls.x, cls.y

    @classmethod
    def _set_position(cls, map, id, x, y):
        # print(f'Position: position set to {map}, {id}, {x}, {y}')
        cls.map_name = map
        cls.cor_id = id
        cls.x = x
        cls.y = y

        cls.position = ((map, id, x, y))

    @classmethod
    def set_map_by_id(cls, map_id):
        # from graphs import G_lvl1, G_lvl0, df_edges_lvl1
        cls.map_name = G.df_edges_lvl1[G.df_edges_lvl1['from_id'] == map_id].iloc[0]['from_name']
        # print(f'Set map by id {}')
        cls.position = ((cls.map_name, cls.cor_id, cls.x, cls.y))

    @classmethod
    def _get_current_map(cls, map):
        ''''This is a temporary function used to to take the current map from the the temp_list'''

        if isinstance(map, str):
            ''''Need better way to navigate the data structure. Maybe indexing.'''
            for t in WalkTemplates.temp_list:
                if t.name == map:  # 'pellet_town':
                    return t
            # maybe it is a group
            list = []
            for t in WalkTemplates.temp_list:
                if t.group == map:
                    list.append(t)
            if list != []:
                return list

        elif isinstance(map, int):
            ''''Need better way to navigate the data structure. Maybe indexing.'''
            for t in WalkTemplates.temp_list:
                if t.id == map:  # 'pellet_town':
                    return t.id

    # Retired because we use a mask now
    # @classmethod
    # def _cpo(cls,img, tile_size):
    #     ''''This function cuts the player out. It works both on the map(template) as on the screen. In case the screen is
    #     used the tilesize should be set to w / 16*10 or h / 16*9. In case the map is used, use the native tile size of 16
    #     pixels per tile.'''
    #
    #     im_ul = img[0:int(3.5 * tile_size), 0:int(3.5 * tile_size)]
    #     im_ur = img[0:int(3.5 * tile_size), int(5.5 * tile_size):(10 * tile_size)]
    #     im_dl = img[int(5.5 * tile_size): (9 * tile_size), 0:int(3.5 * tile_size)]
    #     im_dr = img[int(5.5 * tile_size): (9 * tile_size), int(5.5 * tile_size):(10 * tile_size)]
    #     vis_up = np.concatenate((im_ul, im_ur), axis=1)
    #     vis_down = np.concatenate((im_dl, im_dr), axis=1)
    #     vis = np.concatenate((vis_up, vis_down), axis=0)
    #     return vis

    @classmethod
    def _map_to_cor(cls, t):  # im is a large map
        ''''The idea is to iterate over the image using the same iterator as was used to create the coordinates tables for
        the database. The ids will be the same as long as the map is made with care.'''
        mapping = {}
        h, w = t.img.shape
        id = 1
        for y in range(int(h / 16) - 8):
            for x in range(int(w / 16) - 9):
                mapping[id] = {'img': t.img[y * 16:(y * 16 + 144), x * 16:(x * 16 + 160)], 'x': x, 'y': y,
                               'mask': t.mask}

                id += 1
        return mapping  # a dict with img, x, y as keys

    @classmethod
    def _get_position_in_map(cls, mapping, screen,
                             threshold=0.03):  # 0.06 was good but we are very strickt now 0.07 is too high
        ''''This function returns the node0_id where the player is at this very moment.'''

        # screen_cpo = cls._cpo(screen, 16 * 4)

        # testing
        # cv2.imshow('screen_cpo', screen_cpo)
        # cv2.waitKey()

        h, w = mapping[1]['img'].shape
        # screen_cpo = cv2.resize(screen, (w, h))
        screen = cv2.resize(screen, (w, h))

        res_max = 1
        node0_id = None
        best_id, best_x, best_y = None, None, None
        for id in mapping:  # +1 because database id starts at 1

            # TODO check the match function
            res = cv2.matchTemplate(screen, mapping[id]['img'], cv2.TM_SQDIFF_NORMED,
                                    mask=mapping[id]['mask'])  # CCOEFF_NORMED) # CCORR_NORMED
            if np.max(
                    res) < res_max:  # TODO maybe if match is higher than 90% or so break from the loop if performance is an issue
                res_max = res
                best_id = id

        if res_max > threshold:
            print(f'threshold of >{threshold} not passed')
            return None

        best_x = mapping[best_id]['x']
        best_y = mapping[best_id]['y']
        return best_id, best_x, best_y

    @classmethod
    def eval_position(cls):
        ''''
        map: int or str '''
        cor = (cls.map_name, cls.x, cls.y)

        def map_name_to_id(map_name):
            from path import Path
            try:
                return int(Path.df_edges_lvl1[Path.df_edges_lvl1['from_name'] == map_name].iloc[0]['from_id'])
            except:
                test = 1

        def template_order():
            from path import Path
            p = Path.path
            if p is None:
                return WalkTemplates.temp_list

            new_list = []
            map_templates = [t for t in WalkTemplates.temp_list if t.group == 'map']
            '''' first add the maps in the path '''
            for map_id in p:
                for t in map_templates:
                    if map_name_to_id(t.name) == map_id:
                        # this is always found 1 time
                        break  # break from the inner loop
                new_list.append(t)
            '''' now add every map that is not in the path '''
            for t in map_templates:
                if t.group == 'map' and t not in new_list:
                    new_list.append(t)

            # new_list = []
            # map_templates = [t for t in T.temp_list if t.group == 'map']
            # for map_id in reversed(p):
            #     new_list.insert(0,)
            #
            # for map_id in reversed(p): # iterate over keys in reversed order. So from last to beginning of path
            #     for t in map_templates:
            #         if map_name_to_id(t.name) == map_id:
            #             new_list.insert(0, t) # if this map in in the path we add it in from
            #         else:
            #             new_list.append(t) # if it this map is not in the path we add it in the back
            return new_list

        '''' if a map name or id is given than check if we find a coordinate. If not move on to all templates'''
        if cls.map_name != None:
            cor = cls._get_position_in_map(cls._map_to_cor(cls._get_current_map(cls.map_name)), screen_grab())
            if cor != None:  # if cor is not None than this was indeed the map
                cls._set_position(cls.map_name, *cor)
                return (cls.map_name, *cor)

        '''' no map name was given or no cor was found for the given map name. Lets look in all templates and find the
         position  '''
        '''' if two maps are similar, like mom_lvl1 and mom_lvl2 this is problematic because the first one will be 
        found'''
        temp_order = template_order()
        print(f"Template list: {[t.name for t in temp_order]}")

        for t in temp_order:
            # iterate over all map templates
            if t.group == 'map':
                print(f' trying {t.name}')
                cor = cls._get_position_in_map(cls._map_to_cor(t), screen_grab())
                if cor is not None:
                    print('found')
                    cls._set_position(t.name, *cor)
                    return t.name, *cor
        raise LocationNotFound


def main():
    Position.map_name = 'pewter_city_gym'
    Position.eval_position()
    print(Position.position)


if __name__ == '__main__':
    main()
