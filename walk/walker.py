

#from position import Position
from stepper import Stepper, WrongStep, LocationNotFound
from path import Path
from position import Position
from fundamentals.controls import turnright, turndown, turnleft,turnup, btnB, btnA
from fundamentals import StateController
# from fight.pokemon import OwnPokemon, OwnMove
import time

class Walker():
    '''' this class combines the path with the stepper to execute the path. It loops over the
     get_shortest_path and the stepper while the goal is not reached (and the state is still "walk"). It breaks when the
     state is changed. It wont remember the goal. We fix that somewhere else because maybe we need to do other stuff
     after e.g. the battle '''

    class GameplayException(Exception):
        '''' Sometimes we need to skip the current job in a game. Use this class to quietly escape from an task '''
        pass

    @classmethod
    def reached_goal(cls, goal_cor):
        from walk.orientation import get_orientation
        ori = get_orientation()
        if len(goal_cor) > 2:
            return Position.position[:2] == goal_cor[:2] and ori == goal_cor[2]
        elif len(goal_cor) == 2:
            return Position.position[:2] == goal_cor[:2]

    @classmethod
    def go(cls, goal_cor):
        '''' goal_cor: tuple like ('mom_lvl1, 58) '''
        from walk.orientation import get_orientation
        from time import sleep

        def set_orientation():
            if len(goal_cor) > 2:
                ori = get_orientation()
                while ori != goal_cor[2]:
                    if goal_cor[2] == 'right':
                        turnright()
                    elif goal_cor[2] == 'left':
                        turnleft()
                    elif goal_cor[2] == 'up':
                        turnup()
                    elif goal_cor[2] == 'down':
                        turndown()
                    ori = get_orientation()


        #print('eval position')
        Position.eval_position() # call it so the position gets determined and stored in the Position attributes
                                # we do not need to call it because the position is always stored. At initialization it

        # will take the default which is fine because it is not the goal. Later, in creating the path variable the
        # Position.position is set
        #print(f'position: {Stepper.position} from walker go')
        StateController.eval_state()
        sn = StateController.state_name()
        # if Stepper.position[:len(goal_cor)] == goal_cor:
        #     cls.goal_not_reached = False
        print(f"walker go state {sn}")

        while not cls.reached_goal(goal_cor) and sn in ['walk','none_state']:
            try:
                path = Path(goal_cor)
                last_map = False
                for key, value in path.cor_dict.items():
                    if list(path.cor_dict)[-1] == int(key): # last item
                        last_map = True
                    path.start_map = int(key)

                    Stepper.path_interpreter(int(key), value, last_map=last_map)
                    sleep(2.5) # wait to go to the next map
                    if not last_map:
                        next_map_id = list(path.cor_dict)[list(path.cor_dict).index(int(key))+1]
                        Position.set_map_by_id(next_map_id)  # some maps are similar so we need to actively set the map instead of doing the loop in finding the map because then the first map in the list gets foound

                set_orientation()
                # ori = get_orientation()

            except (WrongStep, LocationNotFound):
                print('walk: WRONG STEP or LOCATION NOT FOUND. recalculate route')
            StateController.eval_state()
            sn = StateController.state_name()


    @classmethod
    def handle_talk(cls):
        # fore example a trainer starts talking to me
        from fundamentals.ocr import OCR

        sn = StateController.state_name()
        while sn in ['walk_talk']:
            text = OCR.read_bar()
            print(text)
            if text is not None:
                if 'fire' in text and 'CHARMANDER?' in text:
                    btnA()
                    time.sleep(0.1)
                    print("Starter CHARMANDER picked")
                    from fight.pokemon import OwnPokemon, OwnMove
                    moves = [OwnMove.create_own_move_by_name('scratch'), OwnMove.create_own_move_by_name('growl')]
                    OwnPokemon(4,'charmander','fire','-', {'hp':20, 'atk': 11, 'def':10, 'spe':12, 'spd':10, 'spa':10},
                               1,'charmander', 5, moves, current_hp=20, in_party=True)
                elif 'water' in text and 'SQUIRTLE?' in text:
                    btnA()
                    time.sleep(0.1)
                    print("Starter SQUIRTLE picked")
                    from fight.pokemon import OwnPokemon, OwnMove
                    moves = [OwnMove.create_own_move_by_name('tackle'), OwnMove.create_own_move_by_name('tail whip')]
                    OwnPokemon(4,'squirtle','water','-', {'hp':19, 'atk': 10, 'def':11, 'spe':10, 'spd':11, 'spa':11},
                               1,'squirtle', 5, moves, current_hp=19, in_party=True)
                elif 'plant' in text and 'BULBASAUR?' in text:
                    btnA()
                    time.sleep(0.1)
                    print("Starter BULBASAUR picked")
                    from fight.pokemon import OwnPokemon, OwnMove
                    moves = [OwnMove.create_own_move_by_name('tackle'), OwnMove.create_own_move_by_name('growl')]
                    OwnPokemon(4,'bulbasaur','grass','poison', {'hp':21, 'atk': 10, 'def':10, 'spe':10, 'spd':12, 'spa':12},
                               1,'bulbasaur', 5, moves, current_hp=21, in_party=True)
                elif 'nickname' in text:
                    print("Nickname functionality not yet implemented choose NO")
                    btnB()
                elif 'OAK:Hey!Dontgoawayyet!' in text:
                    btnB()
                    raise cls.GameplayException("Skip current task and go the the next task.")
                elif 'heal' in text and 'POKéMON' in text:
                    # heal at a pokecenter
                    from fight.pokemon import OwnPokemon
                    OwnPokemon.party.heal_party()
                    btnA()
                elif 'quickrest' in text:
                    # heal at mom
                    from fight.pokemon import OwnPokemon
                    OwnPokemon.party.heal_party()
                    btnA()
                else:
                    btnA()
            sn = StateController.eval_state()


if __name__ == '__main__':
    from fundamentals.ocr import OCR
    from fight.pokemon import OwnPokemon, OwnMove
    print(OwnPokemon.party[0].level)
    print(Walker.handle_talk())
    print(OwnPokemon.party[1].level)

    print(OwnPokemon.all)

    # Walker.go(('mom_lvl1', 56))