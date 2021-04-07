
import cv2

from image_recognition.location import get_position_wrapper
from fundamentals.initialization import load_templates
from fundamentals.screen import screen_grab
from fundamentals.open_vba import open_vba
from fundamentals.config import config

import os

def open_debug_screen():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    w = int(config('../settings.ini', 'window_size','w'))
    h = int(config('../settings.ini', 'window_size', 'h'))

    while (True):
        debug_screen = screen_grab()
        debug_screen = cv2.cvtColor(debug_screen,cv2.COLOR_GRAY2RGB)
        # Write some Text

        id = get_position_wrapper('pellet_town')

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(debug_screen, str(id), (int(w/2), int(h/2)), font, 1, (0, 255, 255), 2, cv2.LINE_AA)

        window_name = 'debug_screen'
        cv2.moveWindow(window_name, int(w), 20)
        cv2.imshow(window_name, debug_screen)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":

    open_vba()
    if 'temp_list' not in globals():
        print('not in globals')
        global temp_list
        temp_list = load_templates()
    open_debug_screen()
