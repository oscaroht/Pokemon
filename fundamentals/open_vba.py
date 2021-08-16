
import os
from time import sleep
import pygetwindow as gw

from fundamentals.config import config

def open_vba():
    '''' Set class variable for width and height. Ideally this is not changed for the entire project
    The game used tiles of which there are 10 in the width and 9 in the height. Ash is centered 5,5 .
    In addition the native pixel size is 16x16 per tile. So ideally we set the size to multiples of
    160x144.'''

    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    base_dir = config('../settings.ini','dirs','base_dir')

    os.startfile( base_dir + 'Pokemon Blue.gb') # make sure to associate .gb with the vba.exe. Now the startfile command opens
                                                # with assosiated program
    sleep(2)
    vb = gw.getWindowsWithTitle('VisualBoyAdvance')[0]
    vb.moveTo(-8,0)  # move the window to the upper corner
    #vb.resizeTo(w, h)
    vb.activate() # also possible to uncheck 'Pause when inactive' in vba settings


if __name__ == "__main__":
    open_vba()