
import os
import cv2

from fundamentals.config import config

class Template:

    extension = 'png'
    tile_size = 16

    def __init__(self, filename, path, group, option, version, img_gray):
        self.name = filename.replace('.'+self.extension,'')  # filename without extension
        self.filename = filename                    # filename without extension
        self.path = path                        # path from the templates folder
        self.group = group                      # use group or folder on the filesystem
        self.option = option                    # option of the group
        self.version = version                  # if there are more templates
        self.img = img_gray                     # array image of the template

def load_templates():
    param = config('./settings.ini', 'dirs')
    root = param['base_dir'] + param['templates'] # this is the root of the templates folder
    global temp_list
    temp_list = []
    for path, subdirs, files in os.walk(root):
        for filename in files:
            if filename.endswith('.png'):
                #print(os.path.join(path, filename))

                subdir = path.replace(root,'')
                option = subdir.replace(subdir,'').split('\\')[0]
                version = None

                temp_list.append(Template(filename, path, subdir.split('\\')[0], option, version, cv2.cvtColor(cv2.imread(os.path.join(path, filename)), cv2.COLOR_BGR2GRAY) ))

    return temp_list