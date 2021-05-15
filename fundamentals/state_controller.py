


# idea for states
# https://www.geeksforgeeks.org/state-method-python-design-patterns/
# https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_state.htm

class State:

    def switch(self,state):
        self.__class__ = state
        print(f'state switched to: {state}')

class WalkState(State):

    def __init__(self):
        pass

    def __str__(self):
        return 'walk'


class TalkState(WalkState):

    def __str__(self):
        return 'talk'

class FightState(State):

    def __init__(self):
        self.name = 'fight'

    def __str__(self):
        return 'fight'

class StoryState(State):
    pass

class StartUpState(State):

    def __init__(self):
        test = 1

    def __str__(self):
        return 'startup'



class StateController:


    state = WalkState() #eval_state()  #StartUpState() # self.get_state() # we could check but we know we start with the

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

        # get orientation also has a @state_check so we do not have to set something. Just to make sure
        if get_orientation() != None:
            cls.state.switch(WalkState)


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


