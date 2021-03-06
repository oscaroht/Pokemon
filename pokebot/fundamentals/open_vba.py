import os
from time import sleep
from pygetwindow import getWindowsWithTitle, PyGetWindowException

def open_vba():
    '''' Calls the Pokemon Blue.gb file and opens with default application.

    Set class variable for width and height. Ideally this is not changed for the entire project
    The game used tiles of which there are 10 in the width and 9 in the height. Ash is centered 5,5 .
    In addition the native pixel size is 16x16 per tile. So ideally we set the size to multiples of
    160x144.'''

    try:

        base_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')) # 2 folder up from here
        os.startfile(os.path.join(base_dir, 'Pokemon Blue.gb')) # make sure to associate .gb with the vba.exe. Now the startfile command opens
                                                    # with assosiated program
        sleep(2)
        vb = getWindowsWithTitle('VisualBoyAdvance')[0]
        vb.moveTo(-8,0)  # move the window to the upper corner
        #vb.resizeTo(w, h)
        vb.activate() # also possible to uncheck 'Pause when inactive' in vba settings
    except PyGetWindowException: # windows returns code 0 when everything is successful. Unfortunately this is handled as an error
        pass

if __name__ == "__main__":
    open_vba()