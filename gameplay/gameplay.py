from gameplay.templates import GT
from fundamentals.controls import *
from fundamentals.state_controller import StateController
import time
from game_plan import Gameplan

class Gameplay:

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
            elif sn == 'gameplay_intro':
                btnA()
                time.sleep(1)
            elif sn == 'gameplay_choose_player_name_menu':
                if Gameplan.player_name == 'blue':
                    cls.in_name_menu_choose('blue', 'player')
                else:
                    cls.in_name_menu_choose('new_name', 'player')
                    print("MAKE SOMETHING TO HANDLE NEW NAME")
            elif sn == 'gameplay_choose_rival_name_menu':
                if Gameplan.rival_name == 'red':
                    cls.in_name_menu_choose('red', 'rival')
                else:
                    cls.in_name_menu_choose('new_name', 'rival')
                    print("MAKE SOMETHING TO HANDLE NEW NAME")

            if sn == 'gameplay_choose_player_name_abc':
                print("TO BE BUILD")

            sn = StateController.eval_state()

    # @classmethod
    # def read_bar(cls):
    #     from fundamentals.ocr import OCR
    #
    #
    #     text = OCR.read_bar()


    @classmethod
    def eval_gameplay_states(cls):
        state = GT.which_template_in_group('states')
        print(f"Eval fightstates: State is {state}")
        return state

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
                print(f"Invalid input argument {to}")
                raise Exception(f"Invalid input argument {to}")
            Gameplay._set_name_cursor(to, who)
            time.sleep(0.2)
            btnA()
            time.sleep(0.5)
            sn = StateController.eval_state()

    @classmethod
    def _set_name_cursor(cls, to, who):
        print(f'Set cursor to {to} for player/rival: {who}')
        cursor = GT.which_template_in_group(f'choose_{who}_name_menu')
        if to == 'new_name':
            to = f'new_{who}_name'
        print(f"cursor : {cursor},, to_temp: {to}  so   {cursor != to}")
        if cursor == None:
            return
        tries = 0
        while cursor != to and tries < 5:
            if to == f'new_{who}_name':
                goup()
            else:
                godown()
            cursor = GT.which_template_in_group(f'choose_{who}_name_menu')
            print(f'cursor is {cursor}. please exit this function')
            tries += 1

    @classmethod
    def buy_item(cls, item_name, amount):
        from gamestats import OwnItems
        if item_name != 'Poke Ball':
            raise Exception("Only item Poke Ball currently functional")
        else:
            item_idx = 1
        StateController.eval_state()
        sn = StateController.state_name()
        while sn != 'gameplay_buy_final':
            cls.in_confirm_choose_yes(item_idx, amount) # 1 for the first item in the shop
            StateController.eval_state()
            sn = StateController.state_name()
            print(sn)
        OwnItems.add_item_by_name(item_name, amount)
        btnB(5)

    @classmethod
    def in_confirm_choose_yes(cls, item_idx, amount):
        sn = StateController.state_name()
        while sn != 'gameplay_buy_confirm':
            cls.go_to_buy_confirm(item_idx, amount)
            StateController.eval_state()
            sn = StateController.state_name()
        time.sleep(0.5)
        btnA()

    @classmethod
    def go_to_buy_confirm(cls, to, amount):
        sn = StateController.state_name()
        while sn != 'gameplay_buy_confirm':
            if sn == 'gameplay_buy_menu':
                cls.go_to_buy_amount(to)
            elif sn == 'gameplay_buy_amount':
                cls._set_up_down_cursor(amount)
                time.sleep(0.5)
                btnA(2)
            StateController.eval_state()
            sn = StateController.state_name()

    @classmethod
    def go_to_buy_amount(cls,to): # to is the item number
        sn = StateController.state_name()
        while sn != 'gameplay_buy_amount':
            if sn == 'gameplay_buy_menu':
                cls._set_up_down_cursor(to)
                btnA()
            elif sn == 'gameplay_buy_confirm':
                btnB()
            StateController.eval_state()
            sn = StateController.state_name()

    @classmethod
    def _set_up_down_cursor(cls, to):
        import re
        cursor = GT.which_template_in_group('market')
        current_amount = int(re.search('\d+', cursor)[0])
        while to != current_amount:
            if to > current_amount:
                goup()
                cursor = GT.which_template_in_group('market')
                current_amount = int(re.search('\d+', cursor)[0])
            elif to < current_amount:
                godown()
                cursor = GT.which_template_in_group('market')
                current_amount = int(re.search('\d+', cursor)[0])


if __name__ == '__main__':
    Gameplay.buy_item('Poke Ball', 5)