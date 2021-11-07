


# idea for states
# https://www.geeksforgeeks.org/state-method-python-design-patterns/
# https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_state.htm

class State:

    def switch(self,state):
        if self.__class__ != state:
            self.__class__ = state
            print(f'state switched to: {state}')

class WalkState(State):

    def __init__(self):
        pass

    def __str__(self):
        return 'walk'

class WalkEvalStats(WalkState):
    def __init__(self):
        pass

    def __str__(self):
        return 'walk_evalstats'


class TalkState(WalkState):

    def __str__(self):
        return 'talk'

class FightPokedex(State):
    def __init__(self):
        self.name = 'fight_pokedex'
    def __str__(self):
        return 'fight_pokedex'

class FightState(State):
    def __init__(self):
        self.name = 'fight'
    def __str__(self):
        return 'fight'
class FightInitState(State):
    def __init__(self):
        self.name = 'fight_init'
    def __str__(self):
        return 'fight_init'
class FightMenuState(State):
    def __init__(self):
        self.name = 'fight_menu'
    def __str__(self):
        return 'fight_menu'
class FightMoveState(State):
    def __init__(self):
        self.name = 'fight_move'
    def __str__(self):
        return 'fight_move'
class FightWaitArrowState(State):
    def __init__(self):
        self.name = 'fight_wait_arrow'
    def __str__(self):
        return 'fight_wait_arrow'

class StoryState(State):
    pass

class StartUpState(State):

    def __init__(self):
        test = 1

    def __str__(self):
        return 'startup'



class StateController:


    state = FightState() #eval_state()  #StartUpState() # self.get_state() # we could check but we know we start with the

    @classmethod
    def state_name(cls):
        # do checks to see whats the state
        return str(cls.state)

    @classmethod
    def eval_state(cls):
        '''' this function is meant to check what the current state is. It is used when we do not know the state anymore
         or at the startup. Unfortunately it cannot be called to set StateController.state because we do not initialize
         a class. '''
        from walk import get_orientation
        from fight import Selector
        from fight import OwnPokemon

        def _set_state():
            state_name = Selector.eval_fight_states()
            if state_name == 'wait_arrow':
                StateController.state.switch(FightWaitArrowState)
            elif state_name == 'menu':
                StateController.state.switch(FightMenuState)
            elif state_name == 'move':
                StateController.state.switch(FightMoveState)
            elif state_name == 'init':
                StateController.state.switch(FightInitState)
            elif state_name == 'pokedex':
                StateController.state.switch(FightPokedex)
            # else:
            #     StateController.state.switch(FightState) #TODO remove so we can get into a walk state


            # get orientation also has a @state_check so we do not have to set something. Just to make sure
            if get_orientation() != None:
                if OwnPokemon.party.stats_need_evaluation():
                    cls.state.switch(WalkEvalStats)
                else:
                    cls.state.switch(WalkState)
                #Position.get_position()     # position class gets forgotten in main after walking is done so we need to set the position again. Otherwise if we are at the end the main will not know

        _set_state()
        while cls.state == None:
            print('state: STATE NOT FOUND, keep looking')
            _set_state()

    # def change(self,new_state):
    #     self.state.switch(new_state)

# use like @state_check(FightState)
def state_check(state):
    def decorator(func):
        def wrapper(*args, **kwargs):
            state_bool = func(*args, **kwargs)
            if state_bool != None and StateController.state != state:
                StateController.state.switch(state)
            return state_bool
        return wrapper
    return decorator


