
''' This file describes how to push the buttons to execute moves, change pokemon, accept newly learned moves, ect.'''
from ..fundamentals import Templates
from ..fundamentals import screen_grab, goleft, goup, godown, goright, btnB, btnA,StateController, btnStart

import time
import cv2


class Selector:
    ''' The Selector class acts as an actuator. It contains functions that push the right buttons to accomplish
    something. This class does not handle the administration. E.g. this class can push the buttons to catch pokemon
    but it does not alter the OwnPokemon.all object/attribute to include the new Pokemon)

    Many of the functions have as similar structure. In order to perform some button action we need to go to the last
    screen of the action sequence. E.g. if we want to choose a move. We need to set the cursor, but first we need to go
    to the move menu, but first we need to set the cursor in the fight menu, but first we need to go to the fight menu.

     the following struture:
     if not at state 3:
        go to this state 3 (from the state2) --> if not at state 2:
                                                    go to state2 (from state1) --> if not ar state1:
                                                                                        go to state1
                                                                                    else:
                                                                                        set cursor to position
                                                                                        btnA
                                                  else:
                                                      set cursor in position
                                                      btnA
    else:
        set cursor in position
        bntA

    I call this chaining.
     '''

    state = 'menu'

    @classmethod
    def put_pokemon_idx_in_front(cls, original_idx):
        ''' this function takes the pokemon with party index idx and switches it to index 0. This is the Selector class
        so it only manages the doing it. Not the administration in the Party class.

        idx is the index of the party of the pokemon that needs to be in front
        '''
        sn = StateController.eval_state()
        while sn in ['walk','walk_evalstats','walk_game_menu','fight_move_pokemon_where','fight_choose_a_pokemon','fight_stats_or_switch']:
            while sn != 'fight_move_pokemon_where':
                cls._in_stats_or_switch_choose(original_idx, option='switch')
                sn = StateController.state_name()
            print("Move to position 0")
            cls._set_party_menu_cursor(0)
            print("press A to confirm")
            btnA()
            btnB(3)
            # after pressing a button we refresh the state
            sn = StateController.eval_state()
            return

    @classmethod
    def bring_out_or_choose_next_pokemon(cls, idx):
        sn = StateController.eval_state()
        while sn in ['fight_no_will_to_fight', 'fight_bring_out_which_pokemon', 'fight_use_next_pokemon', 'fight_choose_a_pokemon', 'fight_switch_or_stats', 'fight_already_out']:
            if sn in ['fight_bring_out_which_pokemon', 'fight_choose_a_pokemon']: # bring out next if after a my_pok is defeated
                                                                # pkmn is when you decide the change pokemon
                cls._set_party_menu_cursor(idx)
                time.sleep(0.1)
                btnA()
                time.sleep(2) # go *pokemon_name* field
                sn = StateController.eval_state()
            elif sn == 'fight_no_will_to_fight':
                btnB()
                time.sleep(1)
                sn = StateController.eval_state()
            elif sn == 'fight_use_next_pokemon':
                btnA()
                time.sleep(0.1)
                sn = StateController.eval_state()
            elif sn == 'fight_switch_or_stats':
                cls._set_up_down_cursor(0,'switch_or_stats')
                time.sleep(0.1)
                btnA()
                time.sleep(0.1)
                sn = StateController.eval_state()
            elif sn == 'fight_already_out':
                print("Apparently this pokemon is already out. Double B to continue fight")
                btnB(2)
                time.sleep(0.1)
                sn = StateController.eval_state()
        else:
            print("NOT IN CHOOSE NEXT POKEMON STATE")
            return


    # @classmethod
    # def _in_move_pokemon_where_menu_choose(cls, to):
    #     cursor = cls._get_cursor_position('move_pokemon_where')
    #     cursor_int = [int(s) for s in cursor.split() if s.isdigit()][0]  # find the one and only digit
    #     if cursor == None:
    #         return
    #     tries = 0
    #     while cursor_int != to and tries < 10:
    #         tries += 1
    #         if cursor_int < to:
    #             godown()
    #             cursor = cls._get_cursor_position('move_pokemon_where')
    #             cursor_int = [int(s) for s in cursor.split() if s.isdigit()][0]  # find the one and only digit
    #         else:
    #             goup()
    #             cursor = cls._get_cursor_position('move_pokemon_where')
    #             cursor_int = [int(s) for s in cursor.split() if s.isdigit()][0]  # find the one and only digit
    #     btnA()
    #     time.sleep(2)
    #     btnB(3)

    @classmethod
    def go_to_pokemon_stats_page_by_idx(cls, idx):
        sn = StateController.eval_state()
        while sn in ['walk','walk_evalstats', 'walk_game_menu', 'fight_choose_a_pokemon', 'fight_stats_or_switch', 'fight_stats_page_stats', 'fight_stats_page_moves']:
            while sn != 'fight_stats_page_stats':
                cls._in_stats_or_switch_choose(idx, option='stats')
                sn = StateController.state_name()
            else:
                return
        # if cls.state != 'stats_page_stats':
        #     cls._in_stats_or_switch_choose(idx, option='stats')

        # stats = FightRec.read_stat_gm_lookup()
        # hp_current, hp_max = FightRec.read_stat_gm_hp()
        # stats['hp'] = hp_max
        # return stats, hp_current

    @classmethod
    def go_to_pokemon_moves_page_by_idx(cls, idx):
        # I do not feel like making this network for the cursor since there is only one direction and 1 edge
        # only clicking A (or B) from the stats page brings you here and you cannot go back.
        sn = StateController.eval_state()

        while sn in ['walk','walk_evalstats', 'walk_game_menu', 'fight_choose_a_pokemon', 'fight_stats_or_switch',
                     'fight_stats_page_stats', 'fight_stats_page_moves']:
            while sn != 'fight_stats_page_moves':
                if sn != 'fight_stats_page_stats':
                    cls.go_to_pokemon_stats_page_by_idx(idx)
                    sn = StateController.state_name()
                else:
                    time.sleep(0.1)
                    btnB()
                    time.sleep(0.1)
                    StateController.eval_state()
                    return
                sn = StateController.eval_state()

            # assume we are there

    @classmethod
    def _in_stats_or_switch_choose(cls, idx, option):
        if option not in ['switch', 'stats']:
            return Exception('Invalid input args')

        sn = StateController.state_name()
        # while sn in ['fight_stats_or_switch', 'fight_choose_a_pokemon','walk_evalstats', 'walk', 'walk_game_menu',
        #              'fight_switch_or_stats', 'fight_stats_page_stats', 'fight_stats_page_moves']:
        if sn != 'fight_stats_or_switch':
            cls._in_party_menu_choose_pokemon_by_idx(idx)
        else:
            cls._set_stats_switch_cursor(option)
            btnA()
            time.sleep(0.1)
            sn = StateController.eval_state()
            return
        # sn = StateController.state_name()

    @classmethod
    def _set_stats_switch_cursor(cls, to):
        group = 'stats_or_switch'
        cursor = cls._get_cursor_position(group) # out of the templates in party menu where is the cursor
        if cursor == None:
            return
        tries = 0
        print(f" to: {to}, cursor: {cursor}")
        while cursor != to and tries < 5: # if the cursor is not in the desired position move it
            tries += 1
            if to == 'stats':
                goup()
                cursor = cls._get_cursor_position(group)
                print(f" to: {to}, cursor: {cursor}")
            elif to == 'switch':
                print("btn Up")
                godown()
                cursor = cls._get_cursor_position(group)
                print(f" to: {to}, cursor: {cursor}")

    @classmethod
    def _in_party_menu_choose_pokemon_by_idx(cls, idx, option= 'stats'):
        print(f"In party menu choose idx {idx}")
        print(f"state is: {StateController.state_name()}")
        #cls.state = cls.eval_fight_states()
        sn = StateController.state_name()
        if sn not in ['fight_stats_or_switch','fight_choose_a_pokemon']:
            cls._in_game_menu_choose(1) # 1 is pokemon
        if sn == 'fight_choose_a_pokemon':
            cls._set_party_menu_cursor(idx)
            print(f"Party menu cursor now set to {idx}")
            time.sleep(0.1)
            btnA()
            time.sleep(0.1)
            StateController.eval_state()
        elif sn == 'fight_stats_or_switch':
            cls._in_stats_or_switch_choose(option)

    @classmethod
    def _in_game_menu_choose(cls, option):
        ''' in the game menu chose 'gm_pokedex','gm_pokemon' 'gm_item',ect. '''
        if option not in [0,1,2,3,4,5]:
            raise Exception(f"Invalid input argument option {option}")
        print(f"In game menu choose {option}")
        sn = StateController.state_name()
        if sn in ['walk','walk_evalstats','walk_game_menu','fight_choose_a_pokemon', 'fight_stats_switch']:
            if sn in ['walk', 'walk_evalstats']:
                print("Open game menu")
                btnStart()
                time.sleep(0.5)
                StateController.eval_state()
            elif sn == 'fight_choose_a_pokemon':
                btnB()
                time.sleep(0.5)
                StateController.eval_state()
            elif sn == 'fight_stats_switch':
                btnB(2)
                time.sleep(0.5)
                StateController.eval_state()
            elif sn == 'walk_game_menu':
                cls._set_up_down_cursor(option, 'game_menu')
                btnA()
                time.sleep(0.5)
                StateController.eval_state()




    @classmethod
    def _go_to_game_menu(cls):
        # not done yet but for lack of something better we start with this
        print("Open game menu")
        # btnB()
        # time.sleep(0.3)
        # btnB()
        # time.sleep(0.3)
        btnStart()
        time.sleep(0.5)
        cls.state = cls.eval_fight_states()

    @classmethod
    def _set_party_menu_cursor(cls, to):
        cursor = cls._get_cursor_position('party_menu')
        cursor_int = [int(s) for s in cursor.split() if s.isdigit()][0] # find the one and only digit
        if cursor == None:
            return
        tries = 0
        while cursor_int != to and tries < 10:
            tries += 1
            if cursor_int < to:
                godown()
                cursor = cls._get_cursor_position('party_menu')
                cursor_int = [int(s) for s in cursor.split() if s.isdigit()][0]  # find the one and only digit
            else:
                goup()
                cursor = cls._get_cursor_position('party_menu')
                cursor_int = [int(s) for s in cursor.split() if s.isdigit()][0]  # find the one and only digit

    # @classmethod
    # def _set_game_menu_cursor(cls, to):
    #     print(f"setting cursor to {to}")
    #     cursor = cls._get_cursor_position('game_menu')
    #     if cursor == None:
    #         return
    #     # tries = 0
    #     while cursor != to:  # and tries < 10:
    #         # tries += 1
    #         if to == 'gm_pokedex':
    #             goup()
    #             cursor = cls._get_cursor_position('game_menu')
    #         elif to == 'gm_pokemon':
    #             if cursor == 'gm_pokedex':
    #                 godown()
    #             else:
    #                 goup()
    #             cursor = cls._get_cursor_position('game_menu')
    #         elif to == 'gm_item':
    #             if cursor in ['gm_pokedex', 'gm_pokemon']:
    #                 godown()
    #             else:
    #                 goup()
    #             cursor = cls._get_cursor_position('game_menu')
    #         elif to == 'gm_player_name':
    #             if cursor in ['gm_pokedex', 'gm_pokemon', 'gm_item']:
    #                 godown()
    #             else:
    #                 goup()
    #             cursor = cls._get_cursor_position('game_menu')
    #         elif to == 'gm_save':
    #             if cursor in ['gm_pokedex', 'gm_pokemon', 'gm_item', 'gm_player_name']:
    #                 godown()
    #             else:
    #                 goup()
    #             cursor = cls._get_cursor_position('game_menu')
    #         elif to == 'gm_option':
    #             if cursor in ['gm_pokedex', 'gm_pokemon', 'gm_item', 'gm_player_name', 'gm_save']:
    #                 godown()
    #             else:
    #                 goup()
    #             cursor = cls._get_cursor_position('game_menu')
    #         print(f"cursor at {cursor}")



    @classmethod
    def _get_cursor_position(cls, group, threshold=0.01):
        screen = screen_grab(resize=True)

        # put the cursor on the right spot
        best_score = 1
        for t in Templates:
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
        print(f"Eval fightstates: State is {state}")
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
        print(f"Cursor is now on {cursor}")

    @classmethod
    def _set_move_cursor(cls,move_idx: int):
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
    def _set_up_down_cursor(cls, to: int, group: str):
        cursor = cls._get_cursor_position(group)
        cursor_idx = [int(s) for s in cursor if s.isdigit()][0]  # find the one and only digit
        while to != cursor_idx:
            if to > cursor_idx:
                godown(to - cursor_idx)
                cursor = cls._get_cursor_position(group)
                cursor_idx = [int(s) for s in cursor if s.isdigit()][0]  # find the one and only digit
            elif to < cursor_idx:
                goup(cursor_idx - to)
                cursor = cls._get_cursor_position(group)
                cursor_idx = [int(s) for s in cursor if s.isdigit()][0]  # find the one and only digit

    @classmethod
    def _in_fight_menu_choose(cls, menu_name):
        ''' in the menu chose 'move', 'item', 'pkmn', 'run' '''
        if cls.state != 'menu':
            cls._go_to_fight_menu()
        elif cls.state == None:
            return
        cls._set_menu_cursor(menu_name)
        btnA()
        time.sleep(0.1)
        cls.eval_fight_states()
        StateController.eval_state()


    @classmethod
    def _go_to_fight_menu(cls):
        ''' from any fight state we can get to the menu by pressing btnB'''
        print("press B to go to fight menu")
        btnB()
        time.sleep(0.5)
        StateController.eval_state()

    @classmethod
    def select_move_by_idx(cls, move_idx):
        cls.state = cls.eval_fight_states()
        # if not in move menu go to menu first
        if cls.state != 'move':
            cls._in_fight_menu_choose('move')
        cls._set_move_cursor(move_idx)
        btnA()
        time.sleep(3)
        StateController.eval_state()
        pass

    @classmethod
    def change_pokemon(cls, new_pkmn_idx):
        cls._in_fight_menu_choose('pkmn')
        time.sleep(0.5) # takes some time to appear
        cls.bring_out_or_choose_next_pokemon(new_pkmn_idx)
        ''' in the pkmn section chose a new pokemon'''

    @classmethod
    def swap_move(cls, drop_move_idx):
        pass

    @classmethod
    def run(cls):
        cls._in_fight_menu_choose('run') # in the _go_to we already check/set state to 'menu'

    @classmethod
    def use_item(cls, item_name):
        if cls.state != 'item':
            cls._in_fight_menu_choose('item')
            time.sleep(0.1)
        # if all is correct it is now menu
        if cls.state == 'item':
            btnA()

    @classmethod
    def init_fight(cls):
        # read the text
        print('click A to start')
        time.sleep(0.5) # presses A to soon earlier, now fixed
        btnA()
        time.sleep(2.5) # time for the animation
        StateController.eval_state() # after every Selector function that could change the state we should evaluate the state
        # maybe return text or something


if __name__ == '__main__':
    time.sleep(1)
    Selector.go_to_pokemon_moves_page_by_idx(1)
    # Selector.eval_fight_states()