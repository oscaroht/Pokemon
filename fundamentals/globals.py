
import os
import cv2
import networkx as nx
from sqlalchemy import create_engine

from fundamentals.config import config

class Template:

    extension = 'tmp'
    tile_size = 16

    def __init__(self, filename, path, group, option, version, img_gray,mask):
        self.name = filename.replace('.'+self.extension,'')  # filename without extension
        self.filename = filename                    # filename without extension
        self.path = path                        # path from the templates folder
        self.group = group                      # use group or folder on the filesystem
        self.option = option                    # option of the group
        self.version = version                  # if there are more templates
        self.img = img_gray                     # array image of the template
        self.mask = mask

class Map(Template):

    def __init__(self, filename, path, group, option, version, img_gray,mask, map_name ):
        super(Map, self).__init__(self, filename, path, group, option, version, img_gray,mask)
        load_graph(map_name)



class OrientationTemplate(Template):
    def __init__(self, orientation, *args, **kwargs):
        super(OrientationTemplate, self).__init__( *args, **kwargs)
        self.orientation = orientation


def load_graph(*args):

    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    password = config('../users.ini', 'postgres', 'password')
    engine = create_engine(f'postgresql+psycopg2://postgres:{password}@localhost/pokemon')

    import pandas as pd
    G_lvl1 = nx.Graph()
    with engine.connect() as con:
        edges = con.execute(f"select * from mappings.edges_lvl1;")
        df_edges_lvl1 = pd.read_sql_table('edges_lvl1', con=con, schema='mappings')
    for row in edges:
        G_lvl1.add_edge(row['from_id'], row['to_id'])

    G_lvl0 = {}
    with engine.connect() as con:
        distinct_node1 = con.execute(f"select distinct node1_id from mart.nodes_lvl0;")
        for row in distinct_node1:
            G_current = nx.Graph()
            node1_id = row['node1_id']
            print(f'Loading.. graph {node1_id}')
            edges = con.execute(f"select * from mart.edges_lvl0 where node1_id = {node1_id}; ")
            nodes = con.execute(f'select node0_id, x, y from mart.nodes_lvl0 where node1_id = {node1_id};')
            for roww in nodes:
                G_current.add_node(roww[0], x=roww[1], y=roww[2])
            for roww in edges:
                # item = row.items()
                G_current.add_edge(roww['node0_id_from'], roww['node0_id_to'])
            G_lvl0[node1_id] = G_current

    return G_lvl1, G_lvl0, df_edges_lvl1

def load_templates():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    param = config('../settings.ini', 'dirs')
    templates_folder = param['base_dir'] + param['templates'] # this is the root of the templates folder

    os.chdir(templates_folder)
    global temp_list
    temp_list = []
    for path, subdirs, files in os.walk(templates_folder):
        # if the folder contains a mask, use the mask for all templates
        mask = None
        for filename in files:
            if filename.endswith('.msk'):
                mask = cv2.cvtColor(cv2.imread(os.path.join(path, filename)), cv2.COLOR_RGB2GRAY)
        for filename in files:
            if filename.endswith('.tmp'):
                # TODO change to logger
                print( 'Loading.. template' + filename)

                subdir = path.replace(templates_folder,'')
                group = subdir.split('\\')[0]
                option = subdir.replace(group+'\\','')

                version = None

                temp_list.append(Template(filename, path, group, option, version,
                                          cv2.cvtColor(cv2.imread(os.path.join(path, filename)), cv2.COLOR_RGB2GRAY)
                                          ,mask))

    return temp_list


temp_list = load_templates()
G_lvl1, G_lvl0, df_edges_lvl1 = load_graph()
