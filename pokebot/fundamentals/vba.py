import os
import time
from pygetwindow import getWindowsWithTitle, PyGetWindowException
from pokebot.fundamentals.controls import *


class VBA_controller:

    def __init__(self):
        self.window = None
        if self._vba_window_exists():
            self.window = self.window = getWindowsWithTitle('VisualBoyAdvance')[0]

    @classmethod
    def _vba_window_exists(cls):
        return len(getWindowsWithTitle('VisualBoyAdvance')) >= 1

    def _open_vba_window(self):
        try:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))  # 2 folder up from here
            os.startfile(os.path.join(base_dir, 'Pokemon Blue.gb'))  # make sure to associate .gb with the vba.exe. Now the startfile command opens
            # with assosiated program
            time.sleep(2)
            self.window = getWindowsWithTitle('VisualBoyAdvance')[0]
            self.window.moveTo(-8, 0)  # move the window to the upper corner
        except PyGetWindowException:  # windows returns code 0 when everything is successful. Unfortunately this is handled as an error
            pass

    def is_active(func):
        def wrapper(self):
            if not self._vba_window_exists():
                self._open_vba_window()
            if self.window is None:
                self.window = getWindowsWithTitle('VisualBoyAdvance')[0]
            self.window.activate()
            func(self)
        return wrapper

    @is_active
    def open_vba_window_if_not_exists(self):
        pass

    @is_active
    def reset_game(self):
        ctrl_plus('r')

    @is_active
    def load_game(self, slot_number):
        btnF(slot_number)

    @is_active
    def save_game(self, slot_number):
        btn_save(slot_number)

    def close(self):
        if not self._vba_window_exists():
            return
        self.window.activate()
        ctrl_plus('x')

if __name__ == '__main__':
    vba = VBA_controller()
    time.sleep(5)
    vba.reset_game()