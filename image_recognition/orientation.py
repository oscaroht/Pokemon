

from numpy import max, argmax, zeros as np
#import max, argmax, zeros from numpy as np

from cv2 import matchTemplate, TM_CCOEFF_NORMED






def PlayerRec(screen, templates_player):
    # screen = cv2.imread('Pokemon Blue_32.png')
    #rs = (700, 630)
    #screen = cv2.resize(screen, rs)
    res_max = np.zeros(len(templates_player))
    thresh = 0.62
    orientation = []
    loc = []
    #locvec = []#np.zeros(len(templates_player))
    for ori in range(len(templates_player)):
        for tem in range(len(templates_player[ori])):
            res = cv2.matchTemplate(screen, templates_player[ori][tem], cv2.TM_CCOEFF_NORMED)
            if np.max(res) > res_max[ori]:
                res_max[ori] = np.max(res)
                #min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                #locvec[ori] = np.where()# >= thresh)
    if np.max(res_max) >= thresh:
        orientation = np.argmax(res_max)+1      # zorg ervoor dat 1 omhoog is
    else: orientation = 5;
    return orientation




