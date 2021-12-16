import cv2
from fundamentals import screen_grab, goleft, goup, godown, goright, btnB, btnA, state_check, FightState,StateController, btnStart
from templates import T

class WalkRec:

    @classmethod
    def bar_present(cls, threshold=0.01):
        screen = screen_grab(resize=True)
        for t in T.temp_list:
            if t.name == 'talk':
                if t.mask is not None:
                    res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED, mask=t.mask)
                else:
                    res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if min_val > threshold:
                    return False
                else:
                    return True

    @classmethod
    def yn_and_bar_present(cls, threshold=0.01):
        screen = screen_grab(resize=True)
        for t in T.temp_list:
            if t.name == 'yn_talk':
                if t.mask is not None:
                    res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED, mask=t.mask)
                else:
                    res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if min_val > threshold:
                    return False
                else:
                    return True