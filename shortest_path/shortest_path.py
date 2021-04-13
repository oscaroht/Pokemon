

''''This file is used to make a graphical representation of a graph. It is ment to resemble the screen. It is used for
debugging'''

from sqlalchemy import create_engine
import networkx as nx
import matplotlib.pyplot as plt
import threading

import os
from time import sleep


from orientation import get_orientation
from location import get_position_wrapper

from fundamentals.config import config
from fundamentals.controls import *


class WrongStep(Exception):
    pass

def path_interpreter(cor_list):
    ori_current = get_orientation()

    for num in range(len(cor_list)-1):
        (x_current, y_current) = cor_list[num]
        (x_next, y_next) = cor_list[num+1]

        print(x_current,y_current)
        print(f'want to go to {(x_next, y_next)}')

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



def path_interpreter_multi_t(cor_list, node1_id):

    # this has to be an inmutable object
    ori = []
    ori.append(get_orientation())
    status = []
    status.append(True)

    node0_id = df_edges_lvl1[(df_edges_lvl1['from_id'] == node1_id)].iloc[0]['from_name']

    #current = (*cor_list[0],ori[0])
    for num in range(len(cor_list)-1):
        # (x_current, y_current) = cor_list[num]
        # (x_next, y_next) = cor_list[num+1]

        # print(x_current,y_current)
        # print(f'want to go to {(x_next, y_next)}')

        current = (node0_id,*cor_list[num], ori[0])

        # check if current is the same as previous next
        sleep(0.01)
        t_check = threading.Thread(target=check, args=(current,status))
        print(f'check expect: {current} ')
        t_check.start()
        sleep(0.01)

        # do next
        t_step = threading.Thread(target=next_step, args=(current, cor_list[num+1],ori ))
        t_step.start()


        # maybe we can use a Exception and catch it in the main (this) thread

        # we did a miss step. Lets break
        if status[0] == False:
            raise WrongStep

        # waiting for both to be done
        t_step.join()
        t_check.join()

        previous_next = current




def next_step(current, next, ori):
    (node0_id, x_current, y_current, ori_current) = current
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
    ori[0]=ori_current

def check(current, status):
    id, x, y = get_position_wrapper(current[0])
    if (x, y) != (current[1], current[2]):
        status[0] = False
        #raise WrongStep('Not right step')

def load_graph(*args):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    password = config('../users.ini', 'postgres', 'password')
    engine = create_engine(f'postgresql+psycopg2://postgres:{password}@localhost/pokemon')

    if 'G_lvl1' not in globals() or 'df_edges_lvl1' not in globals():
        import pandas as pd
        global G_lvl1
        global df_edges_lvl1
        G_lvl1 = nx.Graph()
        with engine.connect() as con:
            edges = con.execute(f"select * from mappings.edges_lvl1;")
            df_edges_lvl1 = pd.read_sql_table('edges_lvl1', con=con, schema='mappings')
        for row in edges:
            G_lvl1.add_edge(row['from_id'], row['to_id'])

    # load level 0 graph of a specific node
    if len(args) == 1:
        node1_id = args[0]

        # G is the local graph. It can be reloaded depending on the current location
        global G_current_lvl0
        G_current_lvl0 = nx.Graph()
        with engine.connect() as con:
            edges = con.execute(f"select * from mart.edges_lvl0 where node1_id = {node1_id}; ")
            nodes = con.execute(f'select node0_id, x, y from mart.nodes_lvl0 where node1_id = {node1_id};')
        for row in nodes:
            G_current_lvl0.add_node(row[0], x=row[1], y=row[2])
        for row in edges:
            # item = row.items()
            G_current_lvl0.add_edge(row['node0_id_from'], row['node0_id_to'])





def get_shortest_path(node1_start,to_id, node1_end = None,return_type='cor_list'):

    map_name = df_edges_lvl1[df_edges_lvl1['from_id'] == node1_start].iloc[0]['from_name']

    from_id, x, y = get_position_wrapper(map_name)
    load_graph(node1_start)

    if node1_end != None:
        if node1_end != node1_start:
            # we need to go to a different map
            path = nx.dijkstra_path(G_lvl1, node1_start, node1_end)
            # the first in path is the start, the second is set to the goal
            exit_node0_id = df_edges_lvl1[ (df_edges_lvl1['from_id'] == path[0]) & (df_edges_lvl1['to_id'] == path[1]) ].loc[0]['exit_node0_id']
            return get_shortest_path(node1_start, exit_node0_id, return_type=return_type)

    path = nx.dijkstra_path(G_current_lvl0, from_id, to_id)

    if return_type == 'node_list':
        return path
    elif return_type == 'cor_list':
        cor_list=[]
        for node_id in path:
            cor_list.append((G_current_lvl0.nodes[node_id]['x'], G_current_lvl0.nodes[node_id]['y']))
        return cor_list

if __name__ == '__main__':

    start_node1 = 1

    load_graph(start_node1)
    goal_id = 195  # mom_lvl1 56, pellet_town 195
    #goal_cor = (G_current_lvl0.nodes[goal_id]['x'], G_current_lvl0.nodes[goal_id]['y'])
    while True:
        try:
            cor_list = get_shortest_path(start_node1, goal_id, return_type='cor_list')
            print(cor_list)
            path_interpreter_multi_t(cor_list, start_node1)
            #current_id = cor_list[0]
        except WrongStep:
            print('lost')
            pass

