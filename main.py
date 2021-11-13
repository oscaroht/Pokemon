import os
import time
import pygetwindow as gw
from fundamentals.initialization import open_vba, config, start_bot
from fundamentals.controls import *
from walker import Walker
#from walk.position import
from fundamentals.state_controller import StateController
from fight import Fighter
from stepper import WrongStep
from position import LocationNotFound


def main():
    start_bot(console_level='INFO')

if __name__ == '__main__':
    # start_bot(console_level='INFO')

    while Walker.map_name != 'mom_lvl1' and Walker.cor_id != 56:
        StateController.eval_state()
        sn = StateController.state_name() # state name
        print(F"SC in main thinks state is {StateController.state_name()}")
        if sn == 'walk':
            try:
                Walker.go(('mom_lvl1', 56))
            except (WrongStep,LocationNotFound) as e:
                print(F'ERROR: {e}')
        elif 'fight' in sn or 'none' in sn:
            Fighter.handle_fight(mode = 'catch')
        elif sn == 'walk_evalstats':
            print(f"Inside state handler")
            Fighter.eval_pokemon_stats()
    #
    #
    # while Walker.map_name != 'route1' or Walker.cor_id != 36:



