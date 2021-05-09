



class Walker:


    '''' this class combines the path with the stepper to execute the path (Walker.path.execute). It loops over the
     get_shortest_path and the stepper while the goal is not reached (and the state is still "walk"). It breaks when the
     state is changed. It wont remember the goal. We fix that somewhere else because maybe we need to do other stuff
     after e.g. the battle '''

    @classmethod
    def go(cls, goal_cor):
        from fundamentals import StateController
        from path import Path
        from stepper import Stepper, WrongStep
        from time import sleep

        while StateController.state_name() == 'walk': # and while location != goal_cor
            try:
                path = Path(goal_cor)
                for key, value in path.cor_dict.items():
                    path.start_map = int(key)

                    Stepper.path_interpreter(value, int(key))
                    sleep(1)
            except WrongStep:
                print('lost')
                pass


if __name__ == '__main__':

    Walker.go(('mom_lvl1', 56))