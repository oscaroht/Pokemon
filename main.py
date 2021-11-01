

import os
import time
import pygetwindow as gw
from fundamentals.initialization import open_vba, config, start_bot
from fundamentals.controls import *
from walker import Walker
#from walk.position import
from fundamentals.state_controller import StateController
from fight import Fighter


def main():
    start_bot(console_level='INFO')

if __name__ == '__main__':
    #start_bot(console_level='INFO')

    while Walker.map_name != 'mom_lvl1' and Walker.cor_id != 56:
        StateController.eval_state()
        if StateController.state_name() == 'walk':
            try:
                Walker.go(('mom_lvl1', 56))
            except Exception as e:
                print(F'ERROR: {e}')
        elif 'fight' or 'none' in StateController.state_name():
            Fighter.handle_fight(mode = 'catch')
    # #
    # # route1 7
    # # mom_lvl2
    # while Walker.map_name != 'route1' or Walker.cor_id != 92:
    #     StateController.eval_state()
    #     if StateController.state_name() == 'walk':
    #         try:
    #             Walker.go(('route1', 92))
    #         except Exception as e:
    #             print(e)
    #     elif 'fight' or 'none' in StateController.state_name():
    #         Fighter.handle_fight()
    #     print(f"walker copid {Walker.cor_id}")
    #
    # while Walker.map_name != 'route1' or Walker.cor_id != 36:
    #     StateController.eval_state()
    #     if StateController.state_name() == 'walk':
    #         try:
    #             Walker.go(('route1', 36))
    #         except Exception as e:
    #             print(e)
    #     elif 'fight' or 'none' in StateController.state_name():
    #         Fighter.handle_fight()


