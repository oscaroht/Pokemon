
import os
import cv2
#
# from fundamentals import config
#
#
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
#
#
# def load_templates():
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
#                 temp_list.append(Template(filename, path, group, option, version,
#                                           cv2.cvtColor(cv2.imread(os.path.join(path, filename)), cv2.COLOR_RGB2GRAY)
#                                           , mask))
#
#     return temp_list
#
# class T:
#     temp_list = load_templates()
#
#     @classmethod
#     def which_template_in_group(cls, group, threshold=0.01):
#         from fundamentals.screen import screen_grab
#         screen = screen_grab(resize=True)
#
#         # pick the right template
#         best_score = 1
#         for t in T.temp_list:
#             if t.group == group:
#                 if t.mask is not None:
#                     res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED, mask=t.mask)
#                 else:
#                     res = cv2.matchTemplate(screen, t.img, cv2.TM_SQDIFF_NORMED)
#                 min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#                 if min_val < best_score:  # lowest score is the best for SQDIFF
#                     best_score = min_val
#                     t_best = t
#         if best_score > threshold:  # lowest score is the best for SQDIFF
#             return None
#         return t_best.option
#
#
#



















#
# import os
# import cv2
# import networkx as nx
# from sqlalchemy import create_engine
#
# from fundamentals.config import config
#
# class Template:
#
#     extension = 'tmp'
#     tile_size = 16
#
#     def __init__(self, filename, path, group, option, version, img_gray,mask):
#         self.name = filename.replace('.'+self.extension,'')  # filename without extension
#         self.filename = filename                    # filename without extension
#         self.path = path                        # path from the templates folder
#         self.group = group                      # use group or folder on the filesystem
#         self.option = option                    # option of the group
#         self.version = version                  # if there are more templates
#         self.img = img_gray                     # array image of the template
#         self.mask = mask
#
# class Map(Template):
#
#     def __init__(self, filename, path, group, option, version, img_gray,mask, map_name ):
#         super(Map, self).__init__(self, filename, path, group, option, version, img_gray,mask)
#         load_graph(map_name)
#
#
#
# class OrientationTemplate(Template):
#     def __init__(self, orientation, *args, **kwargs):
#         super(OrientationTemplate, self).__init__( *args, **kwargs)
#         self.orientation = orientation
#
#
# def load_graph(*args):
#     os.chdir(os.path.dirname(os.path.realpath(__file__)))
#     password = config('../users.ini', 'postgres', 'password')
#     engine = create_engine(f'postgresql+psycopg2://postgres:{password}@localhost/pokemon')
#
#     if 'G_lvl1' not in globals() or 'df_edges_lvl1' not in globals():
#         import pandas as pd
#         global G_lvl1
#         global df_edges_lvl1
#         G_lvl1 = nx.Graph()
#         with engine.connect() as con:
#             edges = con.execute(f"select * from mappings.edges_lvl1;")
#             df_edges_lvl1 = pd.read_sql_table('edges_lvl1', con=con, schema='mappings')
#         for row in edges:
#             G_lvl1.add_edge(row['from_id'], row['to_id'])
#
#     # load level 0 graph of a specific node
#     if len(args) == 1:
#         node1_id = args[0]
#
#         # G is the local graph. It can be reloaded depending on the current location
#         global G_current_lvl0
#         G_current_lvl0 = nx.Graph()
#         with engine.connect() as con:
#             edges = con.execute(f"select * from mart.edges_lvl0 where node1_id = {node1_id}; ")
#             nodes = con.execute(f'select node0_id, x, y from mart.nodes_lvl0 where node1_id = {node1_id};')
#         for row in nodes:
#             G_current_lvl0.add_node(row[0], x=row[1], y=row[2])
#         for row in edges:
#             # item = row.items()
#             G_current_lvl0.add_edge(row['node0_id_from'], row['node0_id_to'])
#
# def load_templates():
#     os.chdir(os.path.dirname(os.path.realpath(__file__)))
#     param = config('../settings.ini', 'dirs')
#     templates_folder = param['base_dir'] + param['templates'] # this is the root of the templates folder
#
#     os.chdir(templates_folder)
#     global temp_list
#     temp_list = []
#     for path, subdirs, files in os.walk(templates_folder):
#         # if the folder contains a mask, use the mask for all templates
#         mask = None
#         for filename in files:
#             if filename.endswith('.msk'):
#                 mask = cv2.cvtColor(cv2.imread(os.path.join(path, filename)), cv2.COLOR_RGB2GRAY)
#         for filename in files:
#             if filename.endswith('.tmp'):
#                 # TODO change to logger
#                 print( 'Loading.. ' + filename)
#
#                 subdir = path.replace(templates_folder,'')
#                 group = subdir.split('\\')[0]
#                 option = subdir.replace(group+'\\','')
#
#                 version = None
#
#                 temp_list.append(Template(filename, path, group, option, version,
#                                           cv2.cvtColor(cv2.imread(os.path.join(path, filename)), cv2.COLOR_RGB2GRAY)
#                                           ,mask))
#
#     return temp_list
#
# if __name__ == '__main__':
#     temp_list = load_templates()
#     test = 1