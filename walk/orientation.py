import cv2

from fundamentals import screen_grab, Templates

def get_orientation(threshold=0.15):
    ''''Evaluates the orientation of the player and returns 'up', 'right', 'down', 'left', or None '''
    screen = screen_grab(resize=True)

    # evaluate all templates
    best_score = 1
    for t in Templates.group('orientation'):
        if t.mask is not None:
            res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED, mask=t.mask)
        else:
            res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if min_val < best_score: # lowest score is the best for SQDIFF
            best_score = min_val
            t_best = t
    if best_score > threshold: # lowest score is the best for SQDIFF
        print('No orientation found.')
        return None
    print(f'{t_best.name} with a score of {best_score}')
    return t_best.option

if __name__ == '__main__':
    t = get_orientation(0.15)
