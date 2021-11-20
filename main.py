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

    def go_to(map, cor_id):
        while Walker.map_name != map and Walker.cor_id != cor_id:
            StateController.eval_state()
            sn = StateController.state_name() # state name
            if sn == 'walk':
                try:
                    Walker.go((map, cor_id))
                except (WrongStep,LocationNotFound) as e:
                    print(F'ERROR: {e}')
            elif 'fight' in sn or 'none' in sn:
                Fighter.handle_fight(mode = 'max_damage')  # catch or max_damage
            elif sn == 'walk_evalstats':
                Fighter.eval_pokemon_stats()

    go_to('mom_lvl1', 3)
    go_to('route2a', 1)

    #
    #
    # while Walker.map_name != 'route1' or Walker.cor_id != 36:



