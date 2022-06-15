'''''We are going to take a screen image, cut the player out and compare that with the shrunk cpo version of the map.
Maybe we can even store the shrunk cpo versions. Maybe this improves performance.'''

import numpy as np
import cv2
import logging
logger = logging.getLogger(__name__)

from ..fundamentals import screen_grab, Templates
from .graphs import G


class LocationNotFound(Exception):
    pass


class Position():
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
        cls.position = (cls.map_name, cls.cor_id, cls.x, cls.y)

    @classmethod
    def _get_map_template_by_name(cls, map):
        ''''This is a temporary function used to to take the current map from the the temp_list'''

        if isinstance(map, str):
            ''''Need better way to navigate the data structure. Maybe indexing.'''
            for t in Templates.group('map'):
                if t.name == map:  # 'pellet_town':
                    return t
            # maybe it is a group
            list = []
            for t in Templates.group('map'):
                if t.group == map:
                    list.append(t)
            if list:
                return list

        # elif isinstance(map, int):
        #     ''''Need better way to navigate the data structure. Maybe indexing.'''
        #     for t in Templates.group('map'):
        #         if t.id == map:  # 'pellet_town':
        #             return t.id

    @classmethod
    def _get_map_window_from_cor(cls, t, x, y):
        ''''This function gets a map image given an x and y coordinate '''
        return {'img': t.img[y * 16:(y * 16 + 144), x * 16:(x * 16 + 160)], 'x': x, 'y': y, 'mask': t.mask}

    @classmethod
    def _get_all_cor_id_window_pairs(cls, t):  # im is a large map
        ''''The idea is to iterate over the image using the same iterator as was used to create the coordinates tables for
        the database. The ids will be the same as long as the map is made with care.'''
        mapping = {}
        h, w = t.img.shape
        cor_id = 1
        for y in range(int(h / 16) - 8):
            for x in range(int(w / 16) - 9):
                mapping[cor_id] = cls._get_map_window_from_cor(t, x, y)
                cor_id += 1
        return mapping  # a dict with img, x, y as keys

    @classmethod
    def _specific_match_function(cls, img, template, mask=None, match_type='ccorr'):
        if match_type == 'sqdiff':
            return cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED, mask=mask)  # CCOEFF_NORMED) # CCORR_NORMED
        elif match_type == 'ccorr':
            return np.subtract(1, cv2.matchTemplate(img, template, cv2.TM_CCORR_NORMED, mask=mask))

    @classmethod
    def _get_position_in_map(cls, mapping, screen,
                             threshold=0.06):  # 0.06 was good but we are very strickt now 0.07 is too high
        ''''This function returns the node0_id where the player is at this very moment.'''

        # screen_cpo = cls._cpo(screen, 16 * 4)

        # testing
        # cv2.imshow('screen_cpo', screen_cpo)
        # cv2.waitKey()

        h, w = mapping[1]['img'].shape
        screen = cv2.resize(screen, (w, h))

        res_max = 1
        best_id, best_x, best_y = None, None, None
        for id in mapping:  # +1 because database id starts at 1

            res = np.max(cls._specific_match_function(screen, mapping[id]['img'], mask=mapping[id]['mask']))
            if res < res_max:
                res_max = res
                best_id = id

        if res_max > threshold:
            logger.debug(f'threshold of >{threshold} not passed')
            return None

        best_x = mapping[best_id]['x']
        best_y = mapping[best_id]['y']
        return best_id, best_x, best_y

    @classmethod
    def eval_position(cls):
        ''''
        map: int or str '''

        def map_name_to_id(map_name):
            try:
                return int(G.df_edges_lvl1[G.df_edges_lvl1['from_name'] == map_name].iloc[0]['from_id'])
            except:
                logger.warning(f"Unable to find {map_name} in G.df_edges_lvl1")

        def template_order():
            from .path import Path
            p = Path.path
            if p is None:
                return Templates.group('map')

            new_order = []
            '''' first add the maps in the path '''
            for map_id in p:
                for t in Templates.group('map'):
                    if map_name_to_id(t.name) == map_id:
                        # this is always found 1 time
                        break  # break from the inner loop
                new_order.append(t)  # the first element of p should be the first of t
            '''' now add every map that is not in the path '''
            for t in Templates.group('map'):
                if t not in new_order:
                    new_order.append(t)
            return new_order

        '''' if a map name or id is given than check if we find a coordinate. If not move on to all templates'''
        if cls.map_name != None:
            cor = cls._get_position_in_map(cls._get_all_cor_id_window_pairs(cls._get_map_template_by_name(cls.map_name)), screen_grab())
            if cor != None:  # if cor is not None than this was indeed the map
                cls._set_position(cls.map_name, *cor)
                return cls.map_name, *cor

        '''' no map name was given or no cor was found for the given map name. Lets look in all templates and find the
         position  '''
        '''' if two maps are similar, like mom_lvl1 and mom_lvl2 this is problematic because the first one will be 
        found'''
        temp_order = template_order()
        logger.debug(f"Template check order: {[t.name for t in temp_order]}")

        for t in temp_order:
            # iterate over all map templates
            logger.debug(f' trying map {t.name}')
            cor = cls._get_position_in_map(cls._get_all_cor_id_window_pairs(t), screen_grab())
            if cor is not None:
                logger.debug(f'position found in {t.name}')
                cls._set_position(t.name, *cor)
                return t.name, *cor
        raise LocationNotFound

    @classmethod
    def is_position(cls, map_name, x, y, threshold=0.05):  # 0.05 not tested
        t = cls._get_map_template_by_name(map_name)  # get the template for the current map name
        window = cls._get_map_window_from_cor(t, x, y)  # get the window of this template, x, y

        screen = screen_grab()
        h, w = window['img'].shape
        screen = cv2.resize(screen, (w, h))

        # # for testing
        # cv2.imshow('resized screen', screen)
        # cv2.waitKey()
        # cv2.imshow('window of template', window['img'])
        # cv2.waitKey()

        res = cls._specific_match_function(screen, window['img'], mask=window['mask'])
        logger.debug(f"The match result in is_position is {res[0][0]}")
        if res[0][0] > threshold:
            return False
        return True



def main():
    import time
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
                        handlers=[logging.StreamHandler()])
    Position.map_name = 'mount_moon1'
    start = time.time()
    # Position.is_position(4, 4)
    print(f'is_position took {time.time()-start}')
    start = time.time()
    Position.eval_position()
    print(f'is_position took {time.time()-start}')
    print(Position.get_position())

if __name__ == '__main__':
    main()
