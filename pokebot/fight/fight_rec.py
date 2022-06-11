
import cv2
import numpy as np

from pokebot.fundamentals import OCR
from pokebot.fundamentals import screen_grab
import logging
logger = logging.getLogger(__name__)

class FightRec(OCR):

    from pokebot.settings import scale_factor

    roi_foe_name = [0, int(8 * scale_factor), 0, int(100 * scale_factor)]  # roi screen shot size roi = screen[0:9, 0:100]

    roi_foe_level = [int( 8 * scale_factor),
                     int(18 * scale_factor),
                     int(40 * scale_factor),
                     int(60 * scale_factor)]  # roi screen shot size roi = screen[0:9, 0:100]

    '''' Check the hp of our pokemon in the format 26/ 26'''
    roi_foe_hp= [int(15*scale_factor),
             int(25*scale_factor),
             int(30*scale_factor),
             int(85*scale_factor)]

    '''' The region of interest containing the pp of a move in format 35/35'''
    roi_pp = [int(87*scale_factor),
              int(98*scale_factor),
              int(35*scale_factor),
              int(81*scale_factor)]

    '''' Check the hp of our pokemon in the format 26/ 26'''
    roi_hp= [int(79*scale_factor),
             int(90*scale_factor),
             int(93*scale_factor),
             int(146*scale_factor)]

    # RETIRED
    # roi_stat_update = [int(23*scale_factor),
    #                    int(90*scale_factor),
    #                    int(80*scale_factor),
    #                    int(153*scale_factor)]

    # RETIRED
    # # both text and number
    # roi_stat_update = {
    #             'attack': [int(23*scale_factor),int(40*scale_factor),int(80*scale_factor),int(153*scale_factor)],
    #             'defense': [int(39*scale_factor),int(56*scale_factor),int(80*scale_factor),int(153*scale_factor)],
    #             'speed': [int(55*scale_factor),int(72*scale_factor),int(80*scale_factor),int(153*scale_factor)],
    #             'special': [int(71*scale_factor),int(90*scale_factor),int(80*scale_factor),int(153*scale_factor)]
    #                     }

    # number only
    roi_stat_update = {
                'attack': [int(32*scale_factor),int(40*scale_factor),int(80*scale_factor),int(153*scale_factor)],
                'defense': [int(47*scale_factor),int(56*scale_factor),int(80*scale_factor),int(153*scale_factor)],
                'speed': [int(63*scale_factor),int(72*scale_factor),int(80*scale_factor),int(153*scale_factor)],
                'special': [int(79*scale_factor),int(90*scale_factor),int(80*scale_factor),int(153*scale_factor)]
                        }

    # this one is used when a stat is looked up through the game_menu
    roi_stat_gm_lookup = {
                'atk': [int(80*scale_factor),int(88*scale_factor),int(43*scale_factor),int(72*scale_factor)],
                'def': [int(95*scale_factor),int(104*scale_factor),int(43*scale_factor),int(72*scale_factor)],
                'spe': [int(111*scale_factor),int(120*scale_factor),int(43*scale_factor),int(72*scale_factor)],
                'spa': [int(127*scale_factor),int(136*scale_factor),int(43*scale_factor),int(72*scale_factor)],
                'spd': [int(127 * scale_factor), int(136 * scale_factor), int(43 * scale_factor), int(72 * scale_factor)] # same as above because psa and spd are the same in gen1
                        }
    roi_stat_gm_hp = [int(32*scale_factor),int(40*scale_factor),int(80*scale_factor),int(153*scale_factor)]
    roi_moves_gm = {
                1: [int(71 * scale_factor), int(80 * scale_factor), int(14 * scale_factor), int(150 * scale_factor)],
                2: [int(88*scale_factor),int(96*scale_factor),int(14*scale_factor),int(150*scale_factor)],
                3: [int(104*scale_factor),int(112*scale_factor),int(14*scale_factor),int(150*scale_factor)],
                4: [int(120*scale_factor),int(130*scale_factor),int(14*scale_factor),int(150*scale_factor)]
                        }


    '''' Arrow that shows at the beginning of a fight '''
    roi_arrow=[int(85*scale_factor),
               int(97*scale_factor),
               int(70*scale_factor),
               int(85*scale_factor)]

    # for testing only
    # scale_factor = 4
    # screen = screen_grab()
    # cv2.imshow('a',screen[int(23*scale_factor),
    #                    int(90*scale_factor),
    #                    int(80*scale_factor),
    #                    int(153*scale_factor)])
    # cv2.waitKey()


    @classmethod
    def _core_ocr(cls,roi):
        screen = screen_grab()
        roi_im = screen[roi[0]: roi[1], roi[2]:roi[3]]

        # add a white part above and below the name. This makes it easier to find contours.
        h1, w1 = roi_im.shape
        white = 248 * np.ones((5, w1), dtype=np.uint8)
        roi_im = cv2.vconcat([white, roi_im, white])
        h1, w1 = roi_im.shape
        white = 248 * np.ones((h1,5), dtype=np.uint8)
        roi_im = cv2.hconcat([white, roi_im, white])

        # # for testing
        # cv2.imshow('a', roi_im)
        # cv2.waitKey()

        contours = super(FightRec, cls)._preprocess_for_contours(roi_im)   # find the rectangles around contours
        bboxes = super(FightRec, cls)._get_bbox(contours)                # get a list of bounding boxes around character

        # testing
        # roi_im = cv2.cvtColor(roi_im, cv2.COLOR_GRAY2RGB)
        # for box in bboxes:
        #     cv2.rectangle(roi_im, (box[0], box[1]), (box[2], box[3]), (255,0,0))
        # cv2.imshow('a', roi_im)
        # cv2.waitKey()
        # roi_im = cv2.cvtColor(roi_im, cv2.COLOR_RGB2GRAY)

        ''''splits the roi in images defined by the bounding boxes'''
        images_for_nn = super(FightRec, cls)._char_images(roi_im, bboxes)

        characters = super(FightRec, cls)._read_characters(images_for_nn)

        return characters

    @classmethod
    def read_foe_level(cls):
        return cls._core_ocr(cls.roi_foe_level)

    @classmethod
    def read_pp(cls):
        return cls._core_ocr(cls.roi_pp)

    @classmethod
    def read_hp(cls):
        return cls._core_ocr(cls.roi_hp)

    @classmethod
    def read_foe_name(cls):
        return cls._core_ocr(cls.roi_foe_name)

    @classmethod
    def read_stat_update(cls):
        return_dict = {}
        number = ''
        for key,value in cls.roi_stat_update.items():
            characters = cls._core_ocr(value)
            number = ''.join([x for x in characters if x.isdigit()])
            return_dict[key] = int(number)
        return return_dict

    @classmethod
    def read_stat_gm_lookup(cls):
        return_dict = {}
        number = ''
        for key,value in cls.roi_stat_gm_lookup.items():
            characters = cls._core_ocr(value)
            number = ''.join([x for x in characters if x.isdigit()])
            return_dict[key] = int(number)
        return return_dict

    @classmethod
    def read_stat_gm_hp(cls):
        txt = cls._core_ocr(cls.roi_stat_gm_hp)
        if '/' in txt:
            hp_current, hp_max = txt.split('/')
            return int(hp_current), int(hp_max)
        else:
            logger.error("Unable to read hp_current and hp_max because / is not found in raw text")

    @classmethod
    def read_moves_gm(cls):
        moves = []
        for key,value in cls.roi_moves_gm.items():
            characters = cls._core_ocr(value)
            if len(characters) > 1: # if the length is 1 or less, it is the - indicating no move
                moves.append(characters)

        scale_factor = 4
        screen = screen_grab()
        cv2.imshow('a',screen[int(cls.roi_moves_gm[1][0]):
                           int(cls.roi_moves_gm[1][1]),
                           int(cls.roi_moves_gm[1][2]):
                           int(cls.roi_moves_gm[1][3])])
        cv2.waitKey()

        return moves

    @classmethod
    def foe_hp(cls):
        # returns the hp ratio (between 1 and 0) left
        screen = screen_grab()
        roi_im = screen[cls.roi_foe_hp[0]:cls.roi_foe_hp[1],cls.roi_foe_hp[2]:cls.roi_foe_hp[3]]

        _, roi_im = cv2.threshold(roi_im,125,255, cv2.THRESH_BINARY)

        ''' to estimate the hp of the foe we look at the hp bar of the foe and estimate 'how full it is'. This is done
        by taking the sum of all pixel values in the roi (after thresholding), subtract the sum of pixel values of the
        hp container and comparing that to '''
        number_of_pixels = roi_im.shape[0]*roi_im.shape[1]
        number_of_white_pixels = np.sum(np.sum(roi_im))/255 # black pixels have value 0 so do not contribute to the sum
        number_of_black_pixels = number_of_pixels - number_of_white_pixels
        threshold = 1600 # the number of black pixels in an empty hp container

        foe_hp = (number_of_black_pixels - threshold) / (3136 - threshold)
        return foe_hp

    # @classmethod
    # def is_wait_arrow_present(cls, group = 'wait_arrow', threshold = 0.2):
    #     from .selector import Selector
    #     from .templates import f_temp_list
    #     screen = screen_grab(resize=True)
    #     # put the cursor on the right spot
    #     best_score = 1
    #     for t in f_temp_list:
    #         #print(t.name)
    #         if t.group == group:
    #             #print('in menu group:' + t.name)
    #             if t.mask is not None:
    #                 res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED, mask=t.mask)
    #             else:
    #                 res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED)
    #             min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    #             if min_val < best_score:  # lowest score is the best for SQDIFF
    #                 best_score = min_val
    #                 t_best = t
    #     if best_score > threshold:  # lowest score is the best for SQDIFF
    #         return False
    #     else:
    #         print('wait arrow present')
    #         Selector.state = 'wait_arrow'
    #         return True




if __name__ == '__main__':

    print(FightRec.read_moves_gm())
    #print(FightRec.read_stat_gm_hp())

    pass


