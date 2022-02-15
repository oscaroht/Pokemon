from ..fundamentals import goup, godown, Templates

class WalkRec:

    # @classmethod
    # def bar_present(cls, threshold=0.01):
    #     screen = screen_grab(resize=True)
    #     for t in T.temp_list:
    #         if t.name == 'talk':
    #             if t.mask is not None:
    #                 res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED, mask=t.mask)
    #             else:
    #                 res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED)
    #             min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    #             if min_val > threshold:
    #                 return False
    #             else:
    #                 return True
    #
    # @classmethod
    # def yn_and_bar_present(cls, threshold=0.01):
    #     screen = screen_grab(resize=True)
    #     for t in T.temp_list:
    #         if t.name == 'yn_talk':
    #             if t.mask is not None:
    #                 res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED, mask=t.mask)
    #             else:
    #                 res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED)
    #             min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    #             if min_val > threshold:
    #                 return False
    #             else:
    #                 return True

    @classmethod
    def eval_states(cls):
        return Templates.which_template_in_group('walk_states')

    @classmethod
    def _set_up_down_cursor(cls, to, group):
        cursor = cls._get_cursor_position(group)
        cursor_idx = [int(s) for s in cursor if s.isdigit()][0]  # find the one and only digit
        while to != cursor_idx:
            if to > cursor_idx:
                godown(cursor_idx - to)
                cursor = cls._get_cursor_position(group)
                cursor_idx = [int(s) for s in cursor if s.isdigit()][0]  # find the one and only digit
            elif to < cursor_idx:
                goup(cursor_idx - to)
                cursor = cls._get_cursor_position(group)
                cursor_idx = [int(s) for s in cursor if s.isdigit()][0]  # find the one and only digit


if __name__ == '__main__':
    print(WalkRec.eval_states())