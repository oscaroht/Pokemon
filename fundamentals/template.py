
class IterTemplates(type):
    def __iter__(cls):
        return iter(cls.all)

class Templates(metaclass=IterTemplates):

    all = []

    @classmethod
    def group(cls, group):
        return [t for t in cls.all if t.group == group]

    @classmethod
    def which_template_in_group(cls, group, threshold=0.01):
        from fundamentals.screen import screen_grab
        import cv2
        screen = screen_grab(resize=True)

        # pick the right template
        best_score = 1
        for t in cls.all:
            if t.group == group:
                if t.mask is not None:
                    res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED, mask=t.mask)
                else:
                    res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if min_val < best_score:  # lowest score is the best for SQDIFF
                    best_score = min_val
                    t_best = t
        if best_score > threshold:  # lowest score is the best for SQDIFF
            return None
        return t_best.option


class Template:
    extension = 'tmp'
    tile_size = 16

    def __init__(self, filename, path, group, option, version, img_gray, mask):
        self.name = filename.replace('.' + self.extension, '')  # filename without extension
        self.filename = filename  # filename without extension
        self.path = path  # path from the templates folder
        self.group = group  # use group or folder on the filesystem
        self.option = option  # option of the group
        self.version = version  # if there are more templates
        self.img = img_gray  # array image of the template
        self.mask = mask
        Templates.all.append(self)

def load_templates(base_path):
    import os
    import cv2

    templates_folder = base_path + '\\templates\\'  # this is the root of the templates folder
    os.chdir(templates_folder)

    for path, subdirs, files in os.walk(templates_folder):
        # if the folder contains a mask, use the mask for all templates
        mask = None
        for filename in files:
            if filename.endswith('.msk'):
                mask = cv2.cvtColor(cv2.imread(os.path.join(path, filename)), cv2.COLOR_RGB2GRAY)
        for filename in files:
            if filename.endswith('.tmp'):
                print('Loading.. template ' + filename)

                subdir = path.replace(templates_folder, '')
                group = subdir.split('\\')[0]
                option = subdir.replace(group + '\\', '')

                version = None

                Template(filename, path, group, option, version,
                         cv2.cvtColor(cv2.imread(os.path.join(path, filename)), cv2.COLOR_RGB2GRAY), mask)
