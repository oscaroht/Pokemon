


# idea for states
# https://www.geeksforgeeks.org/state-method-python-design-patterns/
# https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_state.htm

class State:

    def switch(self,state):
        if self.__class__ != state:
            self.__class__ = state
            print(f'state switched to: {state}')

class NoneState(State):
    def __init__(self):
        self.name = 'none_state'
    def __str__(self):
        return 'none_state'

class WalkState(State):
    def __init__(self):
        self.name = 'walk'
    def __str__(self):
        return 'walk'

class WalkTalkState(WalkState):
    def __init__(self):
        self.name = 'walk_talk'
    def __str__(self):
        return 'walk_talk'

class WalkEvalStats(WalkState):
    def __init__(self):
        self.name = 'walk_evalstats'
    def __str__(self):
        return 'walk_evalstats'



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
class FightInitTrainerState(State):
    def __init__(self):
        self.name = 'fight_init_trainer'
    def __str__(self):
        return 'fight_init_trainer'
class FightChangePokemonState(State):
    def __init__(self):
        self.name = 'fight_change_pokemon'
    def __str__(self):
        return 'fight_change_pokemon'

class FightLevelUpState(State):
    def __init__(self):
        self.name = 'fight_level_up'
    def __str__(self):
        return 'fight_level_up'
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
        from walk.walk_rec import WalkRec

        def _set_state():
            state_name = Selector.eval_fight_states() # if this returns None than we still assume it is the same state as last time. Not sure if this is desired
            if state_name == 'wait_arrow':
                StateController.state.switch(FightWaitArrowState)
                # no return because this is a general arrow
            elif state_name == 'menu':
                StateController.state.switch(FightMenuState)
                return
            elif state_name == 'move':
                StateController.state.switch(FightMoveState)
                return
            elif state_name == 'init':
                StateController.state.switch(FightInitState)
                return
            elif state_name == 'init_trainer':
                StateController.state.switch(FightInitTrainerState)
                return
            elif state_name == 'level_up':
                StateController.state.switch(FightLevelUpState)
                return
            elif state_name == 'pokedex':
                StateController.state.switch(FightPokedex)
                return
            elif state_name == 'change_pokemon':
                StateController.state.switch(FightChangePokemonState)
                return
            # else:
            #     StateController.state.switch(FightState) #TODO remove so we can get into a walk state
            # get orientation also has a @state_check so we do not have to set something. Just to make sure

            print("Check orientation")
            ori = get_orientation()
            if ori != None:
                bar_is_present = WalkRec.bar_present()
                yn = WalkRec.yn_and_bar_present()
                if yn:
                    print("HANDLE YN IN BAR. PRESS A FOR NOW FIX LATER")
                    cls.state.switch(WalkTalkState)
                    return
                elif bar_is_present:
                    cls.state.switch(WalkTalkState)
                    return
                # player visible and free (not talk)
                if OwnPokemon.party.stats_need_evaluation():
                    cls.state.switch(WalkEvalStats)
                    return
                else:
                    cls.state.switch(WalkState)
                    return
            elif state_name == 'wait_arrow':
                StateController.state.switch(FightWaitArrowState)
                # so it is the fight wait arrow but it is already set to this state
                return
            else:
                # none state or senario state
                StateController.state.switch(NoneState)
                # Position.get_position()     # position class gets forgotten in main after walking is done so we need to set the position again. Otherwise if we are at the end the main will not know

        _set_state()
        while cls.state == None: # this never happens. I do not know why I put this here
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

if __name__ == '__main__':
    StateController.eval_state()
