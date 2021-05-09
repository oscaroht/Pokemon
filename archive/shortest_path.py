

''''This file is used to make a graphical representation of a graph. It is ment to resemble the screen. It is used for
debugging'''

import networkx as nx
import threading
from time import sleep


from orientation import get_orientation
from position import get_position, LocationNotFound
from fundamentals.controls import *
from fundamentals.state_controller import StateController
from walk.graphs import G_lvl0, G_lvl1, df_edges_lvl1

class WrongStep(Exception):
    pass


def path_interpreter_multi_t(cor_list, node1):

    """" Iterate over coordinates list. And check and step in parallel. Before every step the check function checks the
    previous step and throws and exception. The cor_list argument is used to do the steps, the node1_id argument is
    used to check the previous step"""

    # this has to be an immutable object
    ori = []
    ori.append(get_orientation())
    # create an immutable object to save the result of the check job
    status = []
    status.append(True)

    if isinstance(node1,int):
        # if a int (node1_id) was given transform it to an name
        node1_id = node1
        node1_name = df_edges_lvl1[(df_edges_lvl1['from_id'] == node1_id)].iloc[0]['from_name']
    else:
        node1_name = node1

    for num in range(len(cor_list)-1):

        current = (node1_name,*cor_list[num], ori[0]) # variable that represents the current position

        # check if current is the same as previous next step
        sleep(0.01)
        t_check = threading.Thread(target=check, args=(current,status))
        print(f'Check complete: {current} ')
        t_check.start()
        sleep(0.01)

        # do next
        t_step = threading.Thread(target=next_step, args=(current, cor_list[num+1],ori ))
        t_step.start()

        # we did a miss step. Lets break
        if status[0] == False:
            raise WrongStep

        # waiting for both to be done
        t_step.join()
        t_check.join()


def next_step(current, next, ori):
    """ press the buttons to perform the next turn and step. input:
     current: triple tuple (. . .)
     next: tuple (. .)
     ori: string like 'up' """

    (_, x_current, y_current, ori_current) = current # ignore map
    (x_next, y_next) = next

    if x_current < x_next:
        if ori_current != 'right':
            turnright()
            ori_current = 'right'
        goright()
    elif x_current > x_next:
        if ori_current != 'left':
            turnleft()
            ori_current = 'left'
        goleft()
    elif y_current > y_next:
        if ori_current != 'up':
            turnup()
            ori_current = 'up'
        goup()
    elif y_current < y_next:
        if ori_current != 'down':
            turndown()
            ori_current = 'down'
        godown()

    # return ori
    ori[0]=ori_current

def check(current, status):
    _, _, x, y = get_position(current[0]) # ignore map, id
    if (x, y) != (current[1], current[2]):
        status[0] = False



# def load_graph(*args):
#
#     """" Loads the lvl1 map (if not loaded yet) and/or, in case an argument is given (str or int) the graph
#         with matching name or id."""
#
#     # Database connection setup
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
#         arg = args[0]
#         # G is the local graph. It can be reloaded depending on the current location
#         global G_current_lvl0
#         G_current_lvl0 = nx.Graph()
#
#         # if it is an int query for id
#         if isinstance(arg,int):
#             node1_id = arg
#             with engine.connect() as con:
#                 edges = con.execute(f"select * from mart.edges_lvl0 where node1_id = {node1_id}; ")
#                 nodes = con.execute(f'select node0_id, x, y from mart.nodes_lvl0 where node1_id = {node1_id};')
#             for row in nodes:
#                 G_current_lvl0.add_node(row[0], x=row[1], y=row[2])
#             for row in edges:
#                 # item = row.items()
#                 G_current_lvl0.add_edge(row['node0_id_from'], row['node0_id_to'])
#
#         # if the argument is a string query for a name
#         elif isinstance(arg, str):
#             node_name = arg
#             with engine.connect() as con:
#                 edges = con.execute(f"select * from mart.edges_lvl0 a join mart.nodes_lvl1 b using(node1_id) where node_name = '{node_name}';")
#                 nodes = con.execute(f"select node0_id, x, y from mart.nodes_lvl0 a join mart.nodes_lvl1 b using(node1_id) where node_name = '{node_name}';")
#             for row in nodes:
#                 G_current_lvl0.add_node(row[0], x=row[1], y=row[2])
#             for row in edges:
#                 # item = row.items()
#                 G_current_lvl0.add_edge(row['node0_id_from'], row['node0_id_to'])
#
#         return G_current_lvl0

def add_exit_node():
    """ The exit node should only be added to the map when the exit is the goal. Otherwise the exit node might be used
    accidentally """


def get_shortest_path(current_map, goal_cor, return_type='cor_list'):
    """ first lookup the current_map_id and current_map_name. Then get the current location and overwrite the current
    map, in case a different map is found. Then check if this is the final map (map containing the goal node1). If not
    return a function that brings you to the next map. If you are on the right map"""

    if isinstance(current_map, int):
        current_map_id = current_map
        current_map_name = df_edges_lvl1[df_edges_lvl1['from_id'] == current_map].iloc[0]['from_name']
    elif isinstance(current_map, str):
        current_map_name = current_map
        current_map_id = df_edges_lvl1[df_edges_lvl1['from_name'] == current_map].iloc[0]['from_id']

    (current_map_name, from_id, x, y) = get_position(current_map_name)
    current_map_id = df_edges_lvl1[df_edges_lvl1['from_name'] == current_map_name].iloc[0]['from_id']

    print(f'Current is: {current_map_name}, {from_id}')

    # can be both name or id
    # load_graph()

    # GLOBAL PATH
    # if the current map is not the goal map than we need to go to the right map first

    print(f'Goal: {goal_cor}')

    # find shortest path is global coordinates
    path_lvl1 = nx.dijkstra_path(G_lvl1, current_map_id, df_edges_lvl1[df_edges_lvl1['from_name'] == goal_cor[0]].iloc[0]['from_id'])

    path = {}
    enter_node0_id = from_id
    for idx, node_lvl1 in enumerate(path_lvl1[:-1]): # next node is at 1
        # the first in path is the start, the second is set to the goal
        #G_current_lvl0 = load_graph(int(node_lvl1))
        G_current_lvl0 = G_lvl0[node_lvl1]
        end_node0_id = df_edges_lvl1[(df_edges_lvl1['from_id'] == path_lvl1[idx]) & (df_edges_lvl1['to_id'] == path_lvl1[idx+1])].iloc[0]['exit_node0_id']

        # add the exit node to the map

        path[node_lvl1] = nx.dijkstra_path(G_current_lvl0, enter_node0_id, end_node0_id)
        enter_node0_id = df_edges_lvl1[(df_edges_lvl1['from_id'] == path_lvl1[idx]) & (df_edges_lvl1['to_id'] == path_lvl1[idx+1])].iloc[0]['enter_node0_id']

    # last time we are going to the goal node
    G_current_lvl0 = G_lvl0[int(path_lvl1[-1])] #load_graph(int(path_lvl1[-1]))
    path[path_lvl1[-1]] = nx.dijkstra_path(G_current_lvl0, enter_node0_id, goal_cor[1])



    # SET RETURN TYPE
    if return_type == 'node_list':
        return path
    elif return_type == 'cor_list':
        rt = {}
        for key, value in path.items():
            G_current_lvl0 = G_lvl0[key]  # load_graph(int(key))
            cor_list = []
            for node_id in value:
                 cor_list.append( (G_current_lvl0.nodes[node_id]['x'], G_current_lvl0.nodes[node_id]['y']) )
            rt[key] = cor_list
        return rt


        # cor_list = []
        # for node_id in path:
        #     cor_list.append((G_current_lvl0.nodes[node_id]['x'], G_current_lvl0.nodes[node_id]['y']))
        # return cor_list, current_map_name


# def get_shortest_path(current_map,goal_cor, return_type='cor_list'):
#
#     """ first lookup the current_map_id and current_map_name. Then get the current location and overwrite the current
#     map, in case a different map is found. Then check if this is the final map (map containing the goal node1). If not
#     return a function that brings you to the next map. If you are on the right map"""
#
#
#     if isinstance(current_map,int):
#         current_map_id = current_map
#         current_map_name = df_edges_lvl1[df_edges_lvl1['from_id'] == current_map].iloc[0]['from_name']
#     elif isinstance(current_map, str):
#         current_map_name = current_map
#         current_map_id = df_edges_lvl1[df_edges_lvl1['from_name'] == current_map].iloc[0]['from_id']
#
#     (current_map_name, from_id, x, y) = get_position_wrapper(current_map_name)
#     print(f'Current is: {current_map_name}, {from_id}')
#
#     # can be both name or id
#     load_graph(current_map_name)
#
#     # GLOBAL PATH
#     # if the current map is not the goal map than we need to go to the right map first
#
#     #TODO lets put this in a loop and create the full path
#
#     print(f'Goal: {goal_cor}')
#     exit_node0_id = goal_cor[1]
#     if current_map_name != goal_cor[0]:
#         print('Goal in different map')
#         # find shortest path is global coordinates
#         path = nx.dijkstra_path(G_lvl1, current_map_id, df_edges_lvl1[df_edges_lvl1['from_name'] == goal_cor[0]].iloc[0]['from_id'] )
#         # the first in path is the start, the second is set to the goal
#         exit_node0_id = df_edges_lvl1[ (df_edges_lvl1['from_id'] == path[0]) & (df_edges_lvl1['to_id'] == path[1]) ].iloc[0]['exit_node0_id']
#
#         # add the exit node to the map
#
#         # lets go to the next map first
#         return get_shortest_path(current_map_name, (current_map_name, exit_node0_id), return_type=return_type)
#
#     # LOCAL PATH
#     if from_id != None:
#         path = nx.dijkstra_path(G_current_lvl0, from_id, exit_node0_id)
#     else:
#         return []
#
#     # SET RETURN TYPE
#     if return_type == 'node_list':
#         return path, current_map_name
#     elif return_type == 'cor_list':
#         cor_list = []
#         for node_id in path:
#             cor_list.append((G_current_lvl0.nodes[node_id]['x'], G_current_lvl0.nodes[node_id]['y']))
#         return cor_list , current_map_name

if __name__ == '__main__':

    # set a (guess of a) starting map
    current_map = 'pellet_town'

    # load the lvl1 map
    #load_graph()

    # goal_cor as a tuple with map name and node0_id
    goal_cor = ('mom_lvl1', 56)


    while StateController.state_name() == 'walk':
        try:
            cor_list = get_shortest_path(current_map, goal_cor, return_type='cor_list')
            print(cor_list)
            for key, value in cor_list.items():
                current_map = int(key)
                path_interpreter_multi_t(value, int(key))
                sleep(1)
        except WrongStep:
            print('lost')
            pass

