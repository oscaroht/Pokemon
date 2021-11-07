
''' This file describes how to push the buttons to execute moves, change pokemon, accept newly learned moves, ect.'''
from .templates import f_temp_list
from fundamentals import screen_grab, goleft, goup, godown, goright, btnB, btnA, state_check, FightState,StateController, btnStart

import time
import cv2


class Selector:

    state = 'menu'

    @classmethod
    def eval_pokemon_stats_by_idx(cls, idx):
        cls.state = cls.eval_fight_states()
        if cls.state != 'stats_page_stats':
            cls._in_switch_or_stats_choose(idx, option= 'stats')
        print("read stats!")


        print("cal function to read stats")


    @classmethod
    def _in_switch_or_stats_choose(cls,idx,option):
        if option not in ['switch', 'stats']:
            return Exception('Invalid input args')

        cls.state = cls.eval_fight_states()
        if cls.state != 'stats_or_switch':
            cls._in_party_menu_choose_pokemon_by_idx(idx)

        cls._set_stats_switch_cursor(option)
        btnA()
        time.sleep(0.5)
        cls.state = cls.eval_fight_states()


    @classmethod
    def _set_stats_switch_cursor(cls, to):
        cursor = cls._get_cursor_position('party_menu')
        if cursor == None:
            return
        tries = 0
        while cursor != to and tries < 5:
            tries += 1
            if to == 'stats':
                godown()
                cursor = cls._get_cursor_position('game_menu')
            elif to == 'switch':
                goup()
                cursor = cls._get_cursor_position('game_menu')

    @classmethod
    def _in_party_menu_choose_pokemon_by_idx(cls, idx, option= 'stats'):
        #cls.state = cls.eval_fight_states()
        if cls.state not in ['stats_or_switch','pkmn']:
            cls._in_game_menu_choose('gm_pokemon')

        if cls.state == 'pkmn':
            if idx == 0:
                btnA()
                time.sleep(0.5)
                cls.state = cls.eval_fight_states()
                #cls._in_switch_or_stats_choose(idx, option=option)
            else:
                raise Exception(f"Only idx 0 can be used for now")
        elif cls.state == 'stats_or_switch':
            cls._in_switch_or_stats_choose(option)

    @classmethod
    def _go_to_party_menu(cls):
        if cls.state != 'pkmn':
            cls._in_game_menu_choose('gm_pokemon')

    @classmethod
    def _in_game_menu_choose(cls, option):
        ''' in the game menu chose 'gm_pokedex','gm_pokoemon' 'gm_item',ect. '''
        if option not in ['gm_pokedex', 'gm_pokemon', 'gm_item', 'gm_save', 'gm_player_name', 'gm_option']:
            raise Exception(f"Invalid input argument option {option}")
        cls.state = cls.eval_fight_states()
        if cls.state != 'game_menu':
            cls._go_to_game_menu()
        elif cls.state == None:
            return
        cls._set_game_menu_cursor(option)
        btnA()
        time.sleep(0.5)
        cls.state = cls.eval_fight_states()

    @classmethod
    def _go_to_game_menu(cls):
        # not done yet but for lack of something better we start with this
        btnB()
        time.sleep(0.3)
        btnB()
        time.sleep(0.3)
        btnStart()
        time.sleep(0.5)
        cls.state = cls.eval_fight_states()


    @classmethod
    def _set_game_menu_cursor(cls, to):
        cursor = cls._get_cursor_position('game_menu')
        if cursor == None:
            return
        tries = 0
        while cursor != to and tries < 5:
            tries += 1
            if to == 'gm_pokedex':
                goup()
                cursor = cls._get_cursor_position('game_menu')
            elif to == 'gm_pokemon':
                if cursor == 'gm_pokedex':
                    godown()
                else:
                    goup()
                cursor = cls._get_cursor_position('game_menu')
            elif to == 'gm_item':
                if cursor in ['gm_pokedex', 'gm_pokemon']:
                    godown()
                else:
                    goup()
                cursor = cls._get_cursor_position('game_menu')
            elif to == 'gm_player_name':
                if cursor in ['gm_pokedex', 'gm_pokemon', 'gm_item']:
                    godown()
                else:
                    goup()
                cursor = cls._get_cursor_position('game_menu')
            elif to == 'gm_save':
                if cursor in ['gm_pokedex', 'gm_pokemon', 'gm_item', 'gm_player_name']:
                    godown()
                else:
                    goup()
                cursor = cls._get_cursor_position('game_menu')
            elif to == 'gm_option':
                if cursor in ['gm_pokedex', 'gm_pokemon', 'gm_item', 'gm_player_name', 'gm_save']:
                    godown()
                else:
                    goup()
                cursor = cls._get_cursor_position('game_menu')



    @classmethod
    def _get_cursor_position(cls, group, threshold=0.01):
        screen = screen_grab(resize=True)

        # put the cursor on the right spot
        best_score = 1
        for t in f_temp_list:
            #print(t.name)x
            if t.group == group:
                #print('in menu group:' + t.name)
                if t.mask is not None:
                    res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED, mask=t.mask)
                else:
                    res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                #print(f'{t.option} with {min_val}')
                if min_val < best_score:  # lowest score is the best for SQDIFF
                    best_score = min_val
                    t_best = t
                    #print(f'new best is {t_best.option}')
        if best_score > threshold:  # lowest score is the best for SQDIFF
            #('No fight template found.')x
            #print(f'class state stays {cls.state}')
            return None
        #print(f'{t_best.name} with a score of {best_score}')
        cls.state = t_best.option
        return t_best.option

    @classmethod
    #@state_check(FightState)
    def eval_fight_states(cls):
        state = cls._get_cursor_position('states')
        print(f"State is {state}")
        return state


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
    def _in_fight_menu_choose(cls, menu_name):
        #from fundamentals import StateController
        ''' in the menu chose 'move', 'item', 'pkmn', 'run' '''
        if cls.state != 'menu':
            cls._go_to_fight_menu()
        elif cls.state == None:
            return
        cls._set_menu_cursor(menu_name)
        btnA()
        time.sleep(0.5)
        StateController.eval_state()


    @classmethod
    def _go_to_fight_menu(cls):
        ''' from any fight state we can get to the menu by pressing btnB'''
        #from fundamentals import StateController
        btnB()
        time.sleep(0.5)
        StateController.eval_state()

    @classmethod
    def select_move_by_idx(cls, move_idx):
        cls.state = cls.eval_fight_states()
        #from fundamentals import StateController
        # if not in move menu go to menu first
        if cls.state != 'move':
            cls._in_fight_menu_choose('move')
        cls._set_move_cursor(move_idx)
        btnA()
        time.sleep(3)
        StateController.eval_state()
        pass

    @classmethod
    def change_pokemon(cls, new_pkmn):
        cls._in_fight_menu_choose('pkmn')
        ''' in the pkmn section chose a new pokemon'''

    @classmethod
    def swap_move(cls, drop_move_idx):
        pass

    @classmethod
    def run(cls):
        cls._in_fight_menu_choose('run') # in the _go_to we already check/set state to 'menu'

    @classmethod
    def skip_text(cls):
        btnA()

    @classmethod
    def use_item(cls, item_name):
        import time
        if cls.state != 'item':
            cls._in_fight_menu_choose('item')
            time.sleep(0.3)
        btnA()

    @classmethod
    def init_fight(cls):
        import time
        #from fundamentals import StateController
        # read the text
        print('click A to start')
        btnA()
        time.sleep(2.5) # time for the animation
        StateController.eval_state() # after every Selector function that could change the state we should evaluate the state
        # maybe return text or something


if __name__ == '__main__':
    time.sleep(1)
    Selector.eval_pokemon_stats_by_idx(0)