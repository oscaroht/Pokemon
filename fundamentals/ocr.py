import tensorflow as tf
import cv2
import numpy as np
from settings import characterlist


class OCR:

    from settings import window_size_h, window_size_w, scale_factor, native_h, native_w
    import os

    ''''
    this class encompasses the optical character recognition functionality. The output function is read_bar but this
    class is also extended in the fight package to include more functions such as read_foe_name

    to do the ocr there are a few steps:
        1. preprocess the image
        2. find the contours
        3. merge or delete contours
        4. '''

    roi_bar = [int(103 * scale_factor), # y0 upper
               int(138 * scale_factor), # y1 lower
               int(7 * scale_factor), #x0 left
               int(144 * scale_factor)] # x1 right. to include arrow: 152

    y_separator = int((roi_bar[0]+roi_bar[1])/2)+1 # +1 , we do it a little lower because otherwise the ? symbol crashes

    roi_upper = [roi_bar[0], y_separator, roi_bar[2], roi_bar[3] ]
    roi_lower = [y_separator, roi_bar[1], roi_bar[2], roi_bar[3] ]

    char = {}
    for i, ch in enumerate(characterlist):
        char[i] = ch
        char[ch] = i

    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    model = tf.keras.models.load_model('ocr_model')

    @classmethod
    def _preprocess_for_contours(cls, roi):
        # blur the image so the letter's pixels become the same contour instead of every pixel its own contour
        kernel = np.ones((5, 5), np.float32) / 22 # was 25
        img = cv2.filter2D(roi, -1, kernel)

        # threshold after blurring. Threshold is set quite high so blur does not fuse letters
        _, thresh = cv2.threshold(img, 185, 255, 0) # was 170

        # ## for testing
        # cv2.imshow('contour', thresh)
        # cv2.waitKey()

        return thresh

    @classmethod
    def _get_bbox(cls,_processed_image):
        ''''bbox is defined as the square in which the character fits but no more and no less. Because if the blurring
        preprocessing the bbox will be a little larger than the original character.

        the bbox is defined as [x0,y0,x1,y2]  so right, up, left, down '''

        contours, _ = cv2.findContours(_processed_image[:90, :], 1, 2)

        def union(a, b):
            x0 = min(a[0], b[0])
            y0 = min(a[1], b[1])
            x1 = max(a[2], b[2])
            y1 = max(a[3], b[3])

            w = max(a[0] + a[2], b[0] + b[2]) - x
            h = max(a[1] + a[3], b[1] + b[3]) - y
            return [x0, y0, x1, y1]

        def box_sort(b):
            ''''sorts using the x0 value of the box. So from left to right where is the start of the first box'''
            return b[0]

        # evaluate the contours
        bbox = list(list())
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            bbox.append([x, y, x + w, y + h])
        #del bbox[0]  # first one is empty

        ''''sort the bboxes from left to right'''
        bbox.sort(key=box_sort)
        del bbox[0]             # first box encompasses the entire screen. We do not whant that

        # TESTING
        # img_cont = _processed_image[:90, :]
        # for b in bbox:
        #     img_cont = cv2.rectangle(img_cont, (b[0], b[1]), (b[2], b[3]), (0, 0, 255),
        #                       2)
        # cv2.imshow('a', img_cont)
        # cv2.waitKey()

        ''''lets loop over all the boxes from left to right. If the next box is inside the current box (axis is x) then
        the two boxes are joined. A margin of 5 is taken so also when the next is almost inside this one'''
        bbox_copy = bbox.copy()
        bbox_out = list(list())  # [[]]
        while len(bbox_copy) > 0:
            b = bbox_copy.pop(0)

            """" if the next box's end is before this box's end. With a small margin"""
            # if len(bbox_copy) > 0:
            #     if bbox_copy[0][2] < b[2] + 5:
            #         bbox_out.append(union(b, bbox_copy[0]))
            #         bbox_copy.pop(0)
            #         continue
            # bbox_out.append(b)

            """ so check for every next bbox if it fits in the current bbox"""
            #if len(bbox_copy) > 0:
            times = 0
            for i in range(len(bbox_copy)):
                if bbox_copy[i][2] < b[2] + 5:
                    b = union(b, bbox_copy[i])
                    times += 1

            for t in range(times):
                bbox_copy.pop(0)

            bbox_out.append(b)

        # TESTING
        # img_cont = _processed_image[:90, :]
        # for b in bbox:
        #     img_cont = cv2.rectangle(img_cont, (b[0], b[1]), (b[2], b[3]), (0, 0, 255),
        #                       2)
        # cv2.imshow('a', img_cont)
        # cv2.waitKey()

        ''''output is a list of boxes so [[x0,y0,x1,y1]]'''
        return bbox_out


    @classmethod
    def _char_images(cls, roi, bboxes):
        char_img_list = [] #list()
        for box in bboxes:
            char_img_list.append ( roi[box[1]:box[3],box[0]:box[2]] )
        return char_img_list

    @classmethod
    def _read_characters(cls, char_images):

        image_list=list()

        # del bbox[0]
        for char_img in char_images:
            ''''every image that goes into the neural network needs to have the same shape [32,32]. To do this we in a 
            relatively scale invariant way a white 32, 32 image is created, past the character image in there (if it 
            does not fit reshape it.'''
            img = np.zeros([32, 32], dtype=np.uint8)
            img.fill(255)

            ## TESTING
            # cv2.imshow('read image',char_img)
            # cv2.waitKey()

            if char_img.shape[0] > img.shape[0] or char_img.shape[1] > img.shape[1]:  ##if char_img.shape > img.shape: #
                char_img = cv2.resize(char_img, img.shape)
            try:
                img[0:char_img.shape[0], 0:char_img.shape[1]] = char_img
            except ValueError as e:
                print(f"Value Exception in character rec. Probably it is inappropriate to read characters at this stage. {e}")
                return

            ''''preprocess the image with a simple filter and divide by 255 for the neural network'''
            _, img = cv2.threshold(img, 170, 255, 0)
            img = img.reshape(32, 32, 1) / 255

            image_list.append(img)

            ## use this for testing
            # cv2.imshow('read image',img)
            # cv2.waitKey()


        chr_codes = np.argmax(cls.model.predict(np.array(image_list)), axis=1)
        characters = ''.join([cls.char[int(i)] for i in chr_codes])
        return characters


    @classmethod
    def read_roi(cls,roi):
        from screen import screen_grab
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

        contours = cls._preprocess_for_contours(roi_im)   # find the rectangles around contours
        bboxes = cls._get_bbox(contours)                # get a list of bounding boxes around character

        # testing
        # roi_im = cv2.cvtColor(roi_im, cv2.COLOR_GRAY2RGB)
        # for box in bboxes:
        #     cv2.rectangle(roi_im, (box[0], box[1]), (box[2], box[3]), (255,0,0))
        # cv2.imshow('a', roi_im)
        # cv2.waitKey()
        # roi_im = cv2.cvtColor(roi_im, cv2.COLOR_RGB2GRAY)

        ''''splits the roi in images defined by the bounding boxes'''
        images_for_nn = cls._char_images(roi_im, bboxes)

        try:
            characters = cls._read_characters( images_for_nn )
        except ValueError:
            characters = "OCR ERROR unable to read characters"

        return characters


    @classmethod
    def read_bar(cls):
        from screen import screen_grab
        screen = screen_grab(resize=False)


        bar_upper = screen[cls.roi_upper[0]:cls.roi_upper[1], cls.roi_upper[2]:cls.roi_upper[3]]
        bar_lower = screen[cls.roi_lower[0]:cls.roi_lower[1], cls.roi_lower[2]:cls.roi_lower[3]]

        pro_img1 = cls._preprocess_for_contours(bar_upper)
        pro_img2 = cls._preprocess_for_contours(bar_lower)
        bboxes1 = cls._get_bbox(pro_img1)
        bboxes2 = cls._get_bbox(pro_img2)

        imgs_for_nn = cls._char_images(bar_upper, bboxes1) + cls._char_images( bar_lower, bboxes2)

        try:
            characters = cls._read_characters( imgs_for_nn )
        except ValueError:
            characters = "OCR ERROR unable to read characters"

        return characters

if __name__ == '__main__':
    text = OCR.read_bar()
    print(text)