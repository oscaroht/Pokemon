
import cv2

from walk.position import Position
from fundamentals.initialization import load_templates
from fundamentals.screen import screen_grab
from fundamentals.open_vba import open_vba
from fundamentals.config import config
from walk.orientation import get_orientation

from multiprocessing.pool import ThreadPool
from collections import deque
import threading
import os
from time import sleep

def open_debug_screen(map_name):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    w = int(config('../settings.ini', 'window_size','w'))
    h = int(config('../settings.ini', 'window_size', 'h'))

    window_name = 'debug_screen'
    cv2.moveWindow(window_name, int(w), 20)
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    while (True):
        debug_screen = screen_grab()
        debug_screen = cv2.cvtColor(debug_screen,cv2.COLOR_GRAY2RGB)
        # Write some Text

        loc = Position.eval_position(map_name)
        ori = get_orientation(0.15)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(debug_screen, str(loc), (int(w/2), int(h/2)), font, 1, (0, 125, 255), 2, cv2.LINE_AA)
        cv2.putText(debug_screen, str(ori), (int(w/2.5), int(h/2.5)), font, 1, (255, 125, 255), 2, cv2.LINE_AA)

        cv2.imshow(window_name, debug_screen)

        if cv2.waitKey(2) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

def debug_multi_t():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    w = int(config('../settings.ini', 'window_size','w'))
    h = int(config('../settings.ini', 'window_size', 'h'))

    window_name = 'debug_screen'
    cv2.moveWindow(window_name, int(w), 20)
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    result = (None,None,None,None)
    while (True):
        debug_screen = screen_grab()

        t_locori = threading.Thread(target=loc_ori, args=('pellet_town',result))
        t_imshow = threading.Thread(target=show_screen, args=(result,debug_screen, window_name,w,h))
        t_locori.start()
        t_imshow.start()
        t_locori.join()
        t_imshow.join()

def loc_ori(map, result):
    loc = Position.eval_position(map)
    ori = get_orientation(0.15)
    result = (*loc, ori)

def show_screen(result,debug_screen, window_name,w,h):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(debug_screen, str(result[:-1]), (int(w / 2), int(h / 2)), font, 1, (0, 125, 255), 2, cv2.LINE_AA)
    cv2.putText(debug_screen, str(result[-1]), (int(w / 2.5), int(h / 2.5)), font, 1, (255, 125, 255), 2, cv2.LINE_AA)

    cv2.imshow(window_name, debug_screen)

    if cv2.waitKey(2) & 0xFF == ord('q'):
        cv2.destroyAllWindows()

if __name__ == "__main__":

    #open_vba()
    if 'temp_list' not in globals():
        print('not in globals')
        global temp_list
        temp_list = load_templates()

    open_debug_screen('pellet_town')

