import tensorflow as tf
import cv2
import numpy as np

from fundamentals.ocr import OCR
from screen import screen_grab


class FightOCR(OCR):

    from settings import scale_factor

    roi_foe_name = [0, int(8 * scale_factor), 0, int(100 * scale_factor)]  # roi screen shot size roi = screen[0:9, 0:100]

    roi_foe_level = [int( 8 * scale_factor),
                     int(18 * scale_factor),
                     int(40 * scale_factor),
                     int(60 * scale_factor)]  # roi screen shot size roi = screen[0:9, 0:100]

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

        contours = super(FightOCR,cls)._preprocess_for_contours(roi_im)   # find the rectangles around contours
        bboxes = super(FightOCR,cls)._get_bbox(contours)                # get a list of bounding boxes around character

        # testing
        # roi_im = cv2.cvtColor(roi_im, cv2.COLOR_GRAY2RGB)
        # for box in bboxes:
        #     cv2.rectangle(roi_im, (box[0], box[1]), (box[2], box[3]), (255,0,0))
        # cv2.imshow('a', roi_im)
        # cv2.waitKey()
        # roi_im = cv2.cvtColor(roi_im, cv2.COLOR_RGB2GRAY)

        ''''splits the roi in images defined by the bounding boxes'''
        images_for_nn = super(FightOCR,cls)._char_images( roi_im,bboxes )

        characters = super(FightOCR,cls)._read_characters( images_for_nn )

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
        '''' argument is of type dict containing the regions of interest of the lines attack, defense, speed and special
        '''
        return_dict = {}
        number = ''
        for key,value in cls.roi_stat_update.items():
            characters = cls._core_ocr(value)
            number = ''.join([x for x in characters if x.isdigit()])
            return_dict[key] = number
        return return_dict


if __name__ == '__main__':

    r = FightOCR.read_pp()

    pass


