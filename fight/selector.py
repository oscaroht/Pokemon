
''' This file describes how to push the buttons to execute moves, change pokemon, accept newly learned moves, ect.'''
from templates import f_temp_list
from fight import Fight
from fundamentals import screen_grab, goleft, goup, godown, goright, btnB, btnA

import time
import cv2


class Selector:

    @classmethod
    def select_move(cls, move_idx):
        # if not in move menu go to menu first
        if Fight.state != 'move':
            cls._go_to_move_menu()

        pass

    @classmethod
    def change_pokemon(cls, new_pkmn):
        pass

    @classmethod
    def swap_move(cls, drop_move_number):
        pass

    @classmethod
    def run(cls):
        pass

    @classmethod
    def use_item(cls, item_name):
        pass

    @classmethod
    def _item_menu(cls):
        ''' go to the item menu '''
        pass

    @classmethod
    def _get_menu_cursor_position(cls, threshold=0.5):
        screen = screen_grab(resize=True)

        # put the cursor on the right spot
        best_score = 1
        for t in f_temp_list:
            print(t.name)
            if t.group == 'menu':
                print('in menu group:' + t.name)
                if t.mask is not None:
                    res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED, mask=t.mask)
                else:
                    res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if min_val < best_score:  # lowest score is the best for SQDIFF
                    best_score = min_val
                    t_best = t
        if best_score > threshold:  # lowest score is the best for SQDIFF
            print('No orientation found.')
            return None
        print(f'{t_best.name} with a score of {best_score}')
        cls.state = t_best.option
        return t_best.option

    @classmethod
    def _move_menu_cursor(cls, to):
        cursor = cls._get_menu_cursor_position()
        while cursor != to:
            if to == 'move':
                if cursor == 'pkmn':
                    goleft()
                    cursor = cls._get_menu_cursor_position()
                elif cursor == 'run':
                    goleft()
                    goup()
                    cursor = cls._get_menu_cursor_position()
                elif cursor == 'item':
                    goup()
                    cursor = cls._get_menu_cursor_position()
            elif to == 'pkmn':
                if cursor == 'move':
                    goright()
                    cursor = cls._get_menu_cursor_position()
                elif cursor == 'run':
                    goup()
                    cursor = cls._get_menu_cursor_position()
                elif cursor == 'item':
                    goup()
                    goleft()
                    cursor = cls._get_menu_cursor_position()
            elif to == 'run':
                if cursor == 'move':
                    goright()
                    godown()
                    cursor = cls._get_menu_cursor_position()
                elif cursor == 'pkmn':
                    godown()
                    cursor = cls._get_menu_cursor_position()
                elif cursor == 'item':
                    goleft()
                    cursor = cls._get_menu_cursor_position()
            elif to == 'item':
                if cursor == 'move':
                    godown()
                    cursor = cls._get_menu_cursor_position()
                elif cursor == 'pkmn':
                    godown()
                    goleft()
                    cursor = cls._get_menu_cursor_position()
                elif cursor == 'run':
                    goright()
                    cursor = cls._get_menu_cursor_position()

    @classmethod
    def _go_to_move_menu(cls):
        ''' go to the move menu '''
        if Fight.state != 'menu':
            cls._go_to_menu()
        else:
            cls._move_menu_cursor('move')
            btnA()
            time.sleep(0.5)
            Fight.set_state()

    @classmethod
    def _pkmn_menu(cls):
        ''' go to the pkmn menu '''
        pass

    @classmethod
    def _go_to_menu(cls):
        ''' from any fight state we can get to the menu by pressing btnB'''
        btnB()
        time.sleep(0.5)
        Fight.set_state()

if __name__ == '__main__':
    Selector._go_to_move_menu()