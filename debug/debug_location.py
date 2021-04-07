
import cv2

from image_recognition.location import get_position_wrapper
from fundamentals.initialization import load_templates
from fundamentals.screen import screen_grab
#from fundamentals.initialization import open_vba

def open_debug_screen():
    while (True):
        debug_screen = screen_grab()

        # Write some Text

        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (10, 500)
        fontScale = 1
        fontColor = (255, 255, 255)
        lineType = 2

        cv2.putText(debug_screen, 'Hello World!',
                    bottomLeftCornerOfText,
                    font,
                    fontScale,
                    fontColor,
                    lineType)

        cv2.imshow('debug_screen', debug_screen)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    #open_vba()
    if 'temp_list' not in globals():
        print('not in globals')
        global temp_list
        temp_list = load_templates()
    open_debug_screen()
