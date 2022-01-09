

#from position import Position
from stepper import Stepper, WrongStep, LocationNotFound
from fundamentals.controls import turnright, turndown, turnleft,turnup, btnB, btnA
from fundamentals import StateController

class Walker(Stepper):

    '''' this class combines the path with the stepper to execute the path. It loops over the
     get_shortest_path and the stepper while the goal is not reached (and the state is still "walk"). It breaks when the
     state is changed. It wont remember the goal. We fix that somewhere else because maybe we need to do other stuff
     after e.g. the battle '''

    # goal_not_reached = True

    @classmethod
    def go(cls, goal_cor):
        '''' goal_cor: tuple like ('mom_lvl1, 58) '''

        from walk.orientation import get_orientation
        from path import Path
        #from stepper import Stepper, WrongStep

        from time import sleep

        def reached_goal():
            if len(goal_cor) > 2:
                return Stepper.position[:2] == goal_cor[:2] and ori == goal_cor[2]
            elif len(goal_cor) == 2:
                return Stepper.position[:2] == goal_cor[:2]


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
        Stepper.eval_position() # call it so the position gets determined and stored in the Position attributes
                                # we do not need to call it because the position is always stored. At initialization it
        ori = get_orientation()
        # will take the default which is fine because it is not the goal. Later, in creating the path variable the
        # Position.position is set
        #print(f'position: {Stepper.position} from walker go')
        StateController.eval_state()
        sn = StateController.state_name()
        # if Stepper.position[:len(goal_cor)] == goal_cor:
        #     cls.goal_not_reached = False
        print(f"walker go state {sn}")
        print(F"{not (Stepper.position[:2] == goal_cor[:2] and ori == goal_cor[2])}, {sn in ['walk','none_state']}")

        while not reached_goal() and sn in ['walk','none_state']:
            print(f'Stepper.position: {Stepper.position[:len(goal_cor)]} != {goal_cor}' )
            try:
                path = Stepper(goal_cor)
                for key, value in path.cor_dict.items():

                    path.start_map = int(key)

                    Stepper.path_interpreter(value, int(key))
                    sleep(2) # wait to go to the next map
                    Stepper.set_map_by_id(int(
                        key))  # some maps are similar so we need to actively set the map instead of doing the loop in finding the map because then the first map in the list gets foound

                set_orientation()
                ori = get_orientation()
                # print(f'ori {ori}, goal_ore = {goal_cor[-1]}')
                # print(
                #     F"{not (Stepper.position[:2] == goal_cor[:2] and ori == goal_cor[2])}, {sn in ['walk', 'none_state']}")

            except (WrongStep, LocationNotFound):
                print('walk: WRONG STEP or LOCATION NOT FOUND. recalculate route')
            StateController.eval_state()
            sn = StateController.state_name()

    # @classmethod
    # def get_position(cls):
    #     return Stepper.get_position()

    @classmethod
    def handle_talk(cls):
        # fore example a trainer starts talking to me
        from fundamentals.ocr import OCR

        sn = StateController.state_name()
        while sn in ['walk_talk']:
            text = OCR.read_bar()
            print(text)
            if text is not None:
                if 'example' in text:
                    print("do something")
                elif 'nickname' in text:
                    print("Nickname functionality not yet inplemented choose NO")
                    btnB()
                else:
                    btnA()
            sn = StateController.eval_state()


if __name__ == '__main__':

    Walker.go(('mom_lvl1', 56))