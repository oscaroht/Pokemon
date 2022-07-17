import os
import time
import logging
from pygetwindow import getWindowsWithTitle, PyGetWindowException
from pokebot.fundamentals.controls import ctrl_plus, btnF, btn_save

logger = logging.getLogger(__name__)

class VBA_controller:

    def __init__(self):
        """"
        Creates a VBA controller.

        If a VBA window is already opened it will associate it.
        """
        self.window = None
        if self._vba_window_exists():
            self.window = self.window = getWindowsWithTitle('VisualBoyAdvance')[0]

    @classmethod
    def _vba_window_exists(cls):
        return len(getWindowsWithTitle('VisualBoyAdvance')) >= 1

    def _open_vba_window(self):
        """"
        Opens a VBA window
        """
        try:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))  # 2 folder up from here
            os.startfile(os.path.join(base_dir, 'Pokemon Blue.gb'))  # make sure to associate .gb with the vba.exe. Now the startfile command opens
            # with assosiated program
            time.sleep(2)
            self.window = getWindowsWithTitle('VisualBoyAdvance')[0]
            self.window.moveTo(-8, 0)  # move the window to the upper corner
        except PyGetWindowException:  # windows returns code 0 when everything is successful. Unfortunately this is handled as an error
            pass

    def active_window(func):
        """"
        Decorator that opens or activates the VBA window if needed.
        """
        def wrapper(self, *args, **kwargs):
            if not self._vba_window_exists():
                logger.debug(f"Opening VBA window")
                self._open_vba_window()
            if self.window is None:
                logger.debug(f"Get VBA window")
                self.window = getWindowsWithTitle('VisualBoyAdvance')[0]
            logger.debug(f"Activate VBA window")
            self.window.activate()
            # logger.debug(f"Perform function")
            func(self, *args, **kwargs)
        return wrapper

    @active_window
    def open_vba_window_if_not_exists(self):
        pass

    @active_window
    def reset_game(self):
        ctrl_plus('r')

    @active_window
    def load_game(self, slot_number: int):
        btnF(slot_number)

    @active_window
    def save_game(self, slot_number: int):
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