

import os
import time
import pygetwindow as gw
from fundamentals.initialization import open_vba, config, start_bot
from fundamentals.controls import *


# idea for states
# https://www.geeksforgeeks.org/state-method-python-design-patterns/
# https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_state.htm

class State:

    def switch(self,state):
        self.__class__ = state

class WalkState(State):
    pass

class TalkState(WalkState):
    pass

class FightState(State):
    pass

class StoryState(State):
    pass

class StartUpState(State):
    pass

class StateController:

    def get_state(self):
        # do checks to see whats the state
        pass

    def __init__(self):
        self.state = StartUpState() # self.get_state() # we could check but we know we start with the

    def change(self,new_state):
        self.state.switch(new_state)


# example
# sc = StateController()
# sc.change(FightState)




def main():
    start_bot(console_level='INFO')

if __name__ == '__main__':
    main()

