from pokebot.gameplay.templates import GT
from pokebot.fundamentals import btnA, btnB,goleft, goright, goup, godown, StateController
import time
from pokebot.game_plan import Gameplan

import logging
logger = logging.getLogger(__name__)

class TwoWayDict(dict):
    def __setitem__(self, key, value):
        # Remove any previous connections with these values
        if key in self:
            del self[key]
        if value in self:
            del self[value]
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

class Gameplay:

    cursor_template = None

    abc_map = {'a': (0, 0),
               'b': (1, 0),
               'c': (2, 0),
               'd': (3, 0),
               'e': (4, 0),
               'f': (5, 0),
               'g': (6, 0),
               'h': (7, 0),
               'i': (8, 0),

               'j': (0, 1),
               'k': (1, 1),
               'l': (2, 1),
               'm': (3, 1),
               'n': (4, 1),
               'o': (5, 1),
               'p': (6, 1),
               'q': (7, 1),
               'r': (8, 1),

               's': (0, 2),
               't': (1, 2),
               'u': (2, 2),
               'v': (3, 2),
               'w': (4, 2),
               'x': (5, 2),
               'y': (6, 2),
               'z': (7, 2),
               ' ': (8, 2),

               '*end*': (8, 4)
               }

    @classmethod
    def handle_gameplay(cls):
        sn = StateController.state_name()
        while 'gameplay' in sn:
            if sn == 'gameplay_splash_screen':
                btnA()
                time.sleep(0.5)
                return
            elif sn == 'gameplay_start_menu':
                cls.in_start_menu_choose(Gameplan.continue_or_new_game)
                if Gameplan.continue_or_new_game == 'new_game':
                    # reset the own pokemon object holders
                    from ..fight import OwnPokemon
                    from .item import Items
                    Items.new_game()
                    OwnPokemon.new_game()
            elif sn == 'gameplay_intro':
                btnA()
                time.sleep(1)
            elif sn == 'gameplay_choose_player_name_menu':
                if Gameplan.player_name == 'blue':
                    cls.in_name_menu_choose('blue', 'player')
                else:
                    cls.in_name_menu_choose('new_name', 'player')
                    time.sleep(2)
                    cls.abc_choose(Gameplan.player_name)  # better to create a state than to assume we arrive here
            elif sn == 'gameplay_choose_rival_name_menu':
                if Gameplan.rival_name == 'red':
                    cls.in_name_menu_choose('red', 'rival')
                else:
                    cls.in_name_menu_choose('new_name', 'rival')
                    time.sleep(2)
                    cls.abc_choose(Gameplan.rival_name)  # better to create a state than to assume we arrive here

            if sn == 'gameplay_choose_player_name_abc':
                logger.error("TO BE BUILD")

            sn = StateController.eval_state()

    # @classmethod
    # def read_bar(cls):
    #     from fundamentals.ocr import OCR
    #
    #
    #     text = OCR.read_bar()

    @classmethod
    def _get_cursor_position(cls):
        import cv2
        import numpy as np
        from pokebot.fundamentals import screen_grab

        if cls.cursor_template is None:
            import pathlib
            import os
            path = pathlib.Path(__file__).parent.resolve()
            filepath = os.path.join(path, "cursor_template\\cursor.tmp")

            cls.cursor_template = cv2.cvtColor(cv2.imread(filepath), cv2.COLOR_RGB2GRAY)

            # cls.cursor_template = cv2.imread(filepath)

        screen = screen_grab(resize=True)

        res = cv2.matchTemplate(screen, cls.cursor_template, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        x = min_loc[0]
        y = min_loc[1]
        column_number = round((x-8)/16)
        row_number = round((y-40)/16)
        print((column_number, row_number))
        return (column_number, row_number)

    @classmethod
    def select_letter(cls, letter):
        x, y = cls._get_cursor_position()
        x_goal, y_goal = cls.abc_map[letter]
        print(f"Goal: {x_goal, y_goal}")
        while x_goal < x:
            goleft()
            x, y = cls._get_cursor_position()
        while x_goal > x:
            goright()
            x, y = cls._get_cursor_position()
        while y_goal < y:
            goup()
            x, y = cls._get_cursor_position()
        while y_goal > y:
            godown()
            x, y = cls._get_cursor_position()
        btnA()

    @classmethod
    def abc_choose(cls, name):
        for char in name:
            cls.select_letter(char)
        cls.select_letter('*end*')

    @classmethod
    def eval_gameplay_states(cls):
        state = GT.which_template_in_group('states')
        logger.debug(f"Eval fightstates: State is {state}")
        return state

    ''' for the start of the game '''
    @classmethod
    def in_start_menu_choose(cls, input):
        if input not in ['continue' ,'new_game', 'option']:
            raise Exception(f"Invalid input argument {input}")
        Gameplay._set_start_menu_cursor(input)
        time.sleep(0.2)
        btnA()
        time.sleep(0.5)
        StateController.eval_state()
    @classmethod
    def _set_start_menu_cursor(cls, to):
        cursor = GT.which_template_in_group('start_menu')
        if cursor == None:
            return
        tries = 0
        while cursor != to and tries < 5:
            if to == 'new_game':
                if cursor == 'continue_pre_summary':
                    godown()
                elif cursor == 'continue':
                    btnB()
            elif to == 'continue_pre_summary':
                if cursor == 'new_game':
                    goup()
                elif cursor == 'continue':
                    btnB()
            elif to == 'continue':
                if cursor == 'new_game':
                    goup()
                elif cursor == 'continue_pre_summary':
                    btnA()
            cursor = GT.which_template_in_group('start_menu')
    @classmethod
    def in_name_menu_choose(cls, to, who):
        sn = StateController.state_name()
        while sn == f'gameplay_choose_{who}_name_menu':
            if to not in ['new_name', 'blue', 'red'] or who not in ['player', 'rival']:
                logger.error(f"Invalid input argument {to}")
                raise Exception(f"Invalid input argument {to}")
            Gameplay._set_name_cursor(to, who)
            time.sleep(0.2)
            btnA()
            time.sleep(0.5)
            sn = StateController.eval_state()
    @classmethod
    def _set_name_cursor(cls, to, who):
        logger.debug(f'Set cursor to {to} for player/rival: {who}')
        cursor = GT.which_template_in_group(f'choose_{who}_name_menu')
        if to == 'new_name':
            to = f'new_{who}_name'
        logger.debug(f"cursor : {cursor},, to_temp: {to}  so   {cursor != to}")
        if cursor == None:
            return
        tries = 0
        while cursor != to and tries < 5:
            if to == f'new_{who}_name':
                goup()
            else:
                godown()
            cursor = GT.which_template_in_group(f'choose_{who}_name_menu')
            logger.debug(f'cursor is {cursor}. please exit this function')
            tries += 1


    ''' in the market to buy or sell stuff '''
    @classmethod
    def buy_item(cls, item_name, amount):
        from .item import Items
        if item_name != 'poke ball':
            raise Exception("Only item Poke Ball currently functional")
        else:
            item_idx = 1

        item = Items.get_item_by_name(item_name)

        StateController.eval_state()
        sn = StateController.state_name()
        while 'buy' in sn:
            money = cls._read_money()
            max_amount = int(money / item.buy) # how many items can I buy as a max
            amount = min(amount, max_amount)
            if amount < 0:
                logger.error(f"Not enough money to buy any of item {item_name}")
                return
            while sn != 'gameplay_buy_final':
                money = cls._read_money()
                max_amount = int(money / item.buy)  # how many items can I buy as a max
                amount = min(amount, max_amount)
                if amount < 0:
                    logger.error(f"Not enough money to buy any of item {item_name}")
                    return
                if sn == 'gameplay_buy_no_money':
                    btnB(4)
                    return
                logger.debug(f"1buy_item state: {sn}")
                cls.in_confirm_choose_yes(item_idx, amount) # 1 for the first item in the shop
                StateController.eval_state()
                sn = StateController.state_name()
                logger.debug(f"2buy_item state: {sn}")
            # the item was bought in the game. Lets us add it to our system
            item.add_amount(amount)
            btnB(4) # exit the menu
            return
    @classmethod
    def in_confirm_choose_yes(cls, item_idx, amount):
        sn = StateController.state_name()
        while 'buy' in sn:
            while sn != 'gameplay_buy_confirm': #, 'gameplay_buy_final']:
                # if sn != 'gameplay_buy_confirm':
                logger.debug(f"1in_confirm_choose_yes state: {sn}")
                cls.go_to_buy_confirm(item_idx, amount)
                StateController.eval_state()
                sn = StateController.state_name()
                logger.debug(f"2in_confirm_choose_yes state: {sn}")
                # elif sn == 'gameplay_buy_final':
                #     return
            time.sleep(0.5)
            btnA()
            return

    @classmethod
    def go_to_buy_confirm(cls, to, amount):
        sn = StateController.state_name()
        while 'buy' in sn:
            while sn != 'gameplay_buy_confirm':
                if sn == 'gameplay_buy_menu':
                    cls.go_to_buy_amount(to)
                elif sn == 'gameplay_buy_amount':
                    cls._set_up_down_cursor(amount, 'market')
                    time.sleep(0.5)
                    btnA()
                    time.sleep(2.5)
                    btnA() # "ITEM? That will be.."
                sn = StateController.eval_state()
                logger.debug(f"go_to_by_amount state: {sn}")
            return

    @classmethod
    def go_to_buy_amount(cls,to): # to is the item number
        sn = StateController.state_name()
        while 'buy' in sn:
            while sn != 'gameplay_buy_amount':
                if sn == 'gameplay_buy_menu':
                    cls._set_up_down_cursor(to, 'market')
                    btnA()
                    time.sleep(0.1)
                elif sn == 'gameplay_buy_confirm':
                    btnB()
                elif sn == 'gameplay_buy_final':
                    btnB()
                sn = StateController.eval_state()
                logger.debug(f"go_to_by_amount state: {sn}")
            return
    @classmethod
    def _read_money(cls):
        from ..fundamentals import OCR
        from pokebot.settings import scale_factor

        roi_money = [int(7*scale_factor), int(17*scale_factor), int(95*scale_factor), int(152*scale_factor)]# x0, x1, y0,y1
        m_str = OCR.read_roi(roi_money)
        if '$' in m_str:
            m_str = m_str.replace('$', '')
        if 'o' in m_str:
            m_str = m_str.replace('o', '0')
        if '!' in m_str:
            m_str = m_str.replace('!', '1')
        m_int = int(''.join([c for c in m_str if c.isdigit()]))
        return m_int


    @classmethod
    def _set_up_down_cursor(cls, to, group):
        import re
        cursor = GT.which_template_in_group(group)
        cursor_idx = int(re.search('\d+', cursor)[0])
        while to != cursor_idx:
            # print("try setting the up down")
            if to > cursor_idx:
                # print(f"try to go up by {cursor_idx - to}")
                goup(to - cursor_idx)
                cursor = GT.which_template_in_group(group)
                cursor_idx = int(re.search('\d+', cursor)[0])
            elif to < cursor_idx:
                # print(f"try to go down")
                godown(cursor_idx - to)
                cursor = GT.which_template_in_group(group)
                cursor_idx = int(re.search('\d+', cursor)[0])


if __name__ == '__main__':
    # Gameplay.buy_item('Poke Ball',9)
    Gameplay.abc_choose('oscar')
    test=1