

from position import Position

class Walker(Position):

    '''' this class combines the path with the stepper to execute the path. It loops over the
     get_shortest_path and the stepper while the goal is not reached (and the state is still "walk"). It breaks when the
     state is changed. It wont remember the goal. We fix that somewhere else because maybe we need to do other stuff
     after e.g. the battle '''

    goal_not_reached = True

    @classmethod
    def go(cls, goal_cor):
        '''' goal_cor: tuple like ('mom_lvl1, 58) '''
        from fundamentals import StateController
        from path import Path
        from stepper import Stepper, WrongStep

        from time import sleep

        print('eval position')
        Position.eval_position() # call it so the position gets determined and stored in the Position attributes
        print(f'position: {Position.position} from walker go')
        if Position.position[:len(goal_cor)] == goal_cor:
            cls.goal_not_reached = False
        while Position.position[:len(goal_cor)] != goal_cor and StateController.state_name() == 'walk':
            print(f'{Position.position[:len(goal_cor)]} != {goal_cor}' )
            StateController.eval_state()
            try:
                path = Path(goal_cor)
                for key, value in path.cor_dict.items():
                    path.start_map = int(key)

                    Stepper.path_interpreter(value, int(key))
                    sleep(1) # wait to go to the next map
                    Position._set_map_by_id(int(key)) # some maps are similar so we need to actively set the map instead of doing the loop in finding the map because then the first map in the list gets foound

            except WrongStep:
                print('walk: WRONG STEP. recalculate route')
                pass

    @classmethod
    def get_position(cls):
        return Position.get_position()

if __name__ == '__main__':

    Walker.go(('mom_lvl1', 56))