
import os
import cv2

from fundamentals.template import Template, Templates


# class Template:
#     extension = 'tmp'
#     tile_size = 16
#
#     def __init__(self, filename, path, group, option, version, img_gray, mask):
#         self.name = filename.replace('.' + self.extension, '')  # filename without extension
#         self.filename = filename  # filename without extension
#         self.path = path  # path from the templates folder
#         self.group = group  # use group or folder on the filesystem
#         self.option = option  # option of the group
#         self.version = version  # if there are more templates
#         self.img = img_gray  # array image of the template
#         self.mask = mask


# class Map(Template):
#
#     def __init__(self, filename, path, group, option, version, img_gray,mask, map_name ):
#         super(Map, self).__init__(self, filename, path, group, option, version, img_gray,mask)
#         load_graph(map_name)


# class OrientationTemplate(Template):
#     def __init__(self, orientation, *args, **kwargs):
#         super(OrientationTemplate, self).__init__( *args, **kwargs)
#         self.orientation = orientation


# def load_templates():
#
#     path = os.path.dirname(os.path.abspath(__file__))
#     templates_folder = path + '\\templates\\'  # this is the root of the templates folder
#
#     os.chdir(templates_folder)
#
#     temp_list = []
#     for path, subdirs, files in os.walk(templates_folder):
#         # if the folder contains a mask, use the mask for all templates
#         mask = None
#         for filename in files:
#             if filename.endswith('.msk'):
#                 mask = cv2.cvtColor(cv2.imread(os.path.join(path, filename)), cv2.COLOR_RGB2GRAY)
#         for filename in files:
#             if filename.endswith('.tmp'):
#                 print('Loading.. template ' + filename)
#
#                 subdir = path.replace(templates_folder, '')
#                 group = subdir.split('\\')[0]
#                 option = subdir.replace(group + '\\', '')
#
#                 version = None
#
#                 Templates.append(Template(filename, path, group, option, version,
#                                           cv2.cvtColor(cv2.imread(os.path.join(path, filename)), cv2.COLOR_RGB2GRAY)
#                                           , mask))
#
#     return temp_list
#
# f_temp_list = load_templates()
#
# pass



