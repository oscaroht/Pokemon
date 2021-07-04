
''' This file describes how to push the buttons to execute moves, change pokemon, accept newly learned moves, ect.'''
from templates import f_temp_list
from fight import Fight
from fundamentals import screen_grab, goleft, goup, godown, goright, btnB, btnA, state_check, FightState

import time
import cv2


class Selector:

    state = 'menu'

    @classmethod
    def _get_cursor_position(cls, group, threshold=0.01):
        screen = screen_grab(resize=True)

        # put the cursor on the right spot
        best_score = 1
        for t in f_temp_list:
            #print(t.name)
            if t.group == group:
                #print('in menu group:' + t.name)
                if t.mask is not None:
                    res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED, mask=t.mask)
                else:
                    res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                print(f'{t.option} with {min_val}')
                if min_val < best_score:  # lowest score is the best for SQDIFF
                    best_score = min_val
                    t_best = t
                    print(f'new best is {t_best.option}')
        if best_score > threshold:  # lowest score is the best for SQDIFF
            print('No fight template found.')
            print(f'class state stays {cls.state}')
            return None
        #print(f'{t_best.name} with a score of {best_score}')
        cls.state = t_best.option
        return t_best.option

    @classmethod
    #@state_check(FightState)
    def eval_fight_states(cls):
        return cls._get_cursor_position('states')


    @classmethod
    def _set_menu_cursor(cls, to):
        cursor = cls._get_cursor_position('menu')
        if cursor == None:
            return
        tries = 0
        while cursor != to and tries < 5:
            tries += 1
            if to == 'move':
                if cursor == 'pkmn':
                    goleft()
                    cursor = cls._get_cursor_position('menu')
                elif cursor == 'run':
                    goleft()
                    goup()
                    cursor = cls._get_cursor_position('menu')
                elif cursor == 'item':
                    goup()
                    cursor = cls._get_cursor_position('menu')
            elif to == 'pkmn':
                if cursor == 'move':
                    goright()
                    cursor = cls._get_cursor_position('menu')
                elif cursor == 'run':
                    goup()
                    cursor = cls._get_cursor_position('menu')
                elif cursor == 'item':
                    goup()
                    goleft()
                    cursor = cls._get_cursor_position('menu')
            elif to == 'run':
                if cursor == 'move':
                    goright()
                    godown()
                    cursor = cls._get_cursor_position('menu')
                elif cursor == 'pkmn':
                    godown()
                    cursor = cls._get_cursor_position('menu')
                elif cursor == 'item':
                    goleft()
                    cursor = cls._get_cursor_position('menu')
            elif to == 'item':
                if cursor == 'move':
                    godown()
                    cursor = cls._get_cursor_position('menu')
                elif cursor == 'pkmn':
                    godown()
                    goleft()
                    cursor = cls._get_cursor_position('menu')
                elif cursor == 'run':
                    goright()
                    cursor = cls._get_cursor_position('menu')

    @classmethod
    def _set_move_cursor(cls,move_idx):
        move_num = move_idx + 1
        cursor = cls._get_cursor_position('move')
        if cursor == None:
            return
        cursor = int( cursor )
        while cursor != move_num:
            if cursor < move_num:
                godown(move_num - cursor)
                cursor = int(cls._get_cursor_position('move'))
            elif cursor > move_num:
                goup(cursor - move_num)
                cursor = int(cls._get_cursor_position('move'))

    @classmethod
    def _go_to(cls, menu_name):
        from fundamentals import StateController
        ''' in the menu chose 'move', 'item', 'pkmn', 'run' '''
        if cls.state != 'menu':
            cls._go_to_menu()
        elif cls.state == None:
            return
        cls._set_menu_cursor(menu_name)
        btnA()
        time.sleep(0.5)
        StateController.eval_state()


    @classmethod
    def _go_to_menu(cls):
        ''' from any fight state we can get to the menu by pressing btnB'''
        from fundamentals import StateController
        btnB()
        time.sleep(0.5)
        StateController.eval_state()

    @classmethod
    def select_move_by_idx(cls, move_idx):
        from fundamentals import StateController
        # if not in move menu go to menu first
        if cls.state != 'move':
            cls._go_to('move')
        cls._set_move_cursor(move_idx)
        btnA()
        time.sleep(3)
        StateController.eval_state()
        pass

    @classmethod
    def change_pokemon(cls, new_pkmn):
        cls._go_to('pkmn')
        ''' in the pkmn section chose a new pokemon'''

    @classmethod
    def swap_move(cls, drop_move_idx):
        pass

    @classmethod
    def run(cls):
        cls._go_to('run') # in the _go_to we already check/set state to 'menu'

    @classmethod
    def skip_text(cls):
        btnA()

    @classmethod
    def use_item(cls, item_name):
        pass

    @classmethod
    def init_fight(cls):
        import time
        from fundamentals import StateController
        # read the text
        print('click A to start')
        btnA()
        time.sleep(2.5) # time for the animation
        StateController.eval_state() # after every Selector function that could change the state we should evaluate the state
        # maybe return text or something


if __name__ == '__main__':
    Selector.eval_fight_states()