

''''This file is used to make a graphical representation of a graph. It is ment to resemble the screen. It is used for
debugging'''

from sqlalchemy import create_engine
import networkx as nx
import matplotlib.pyplot as plt
import threading

import os


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



def path_interpreter_multi_t(cor_list):

    # this has to be an inmutable object
    ori = []
    ori.append(get_orientation())
    status = []
    status.append(True)

    #current = (*cor_list[0],ori[0])
    for num in range(len(cor_list)-1):
        # (x_current, y_current) = cor_list[num]
        # (x_next, y_next) = cor_list[num+1]

        # print(x_current,y_current)
        # print(f'want to go to {(x_next, y_next)}')

        current = (*cor_list[num], ori[0])
        t_step = threading.Thread(target=next_step, args=(current, cor_list[num+1],ori ))
        # check if current is the same as previous next
        t_check = threading.Thread(target=check, args=(current,status))

        # start both threads
        t_step.start()
        t_check.start()

        # maybe we can use a Exception and catch it in the main (this) thread

        # we did a miss step. Lets break
        if status[0] == False:
            raise WrongStep

        # waiting for both to be done
        t_step.join()
        t_check.join()

        previous_next = current




def next_step(current, next, ori):
    (x_current, y_current, ori_current) = current
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
    id, x, y = get_position_wrapper('pellet_town')
    if (x, y) != (current[0], current[1]):
        status[0] = False
        #raise WrongStep('Not right step')



def load_graph(node1_id):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    password = config('../users.ini', 'postgres', 'password')
    engine = create_engine(f'postgresql+psycopg2://postgres:{password}@localhost/pokemon')

    if 'G' not in globals():
        global G
        G = nx.Graph()

        with engine.connect() as con:
            edges = con.execute(f"select * from mart.edges_lvl0 where node1_id = {node1_id}; ")
            nodes = con.execute(f'select node0_id, x, y from mart.nodes_lvl0 where node1_id = {node1_id};')

        for row in nodes:
            G.add_node(row[0],x=row[1],y=row[2])

        for row in edges:
            # item = row.items()
            G.add_edge(row['node0_id_from'], row['node0_id_to'])


def get_shortest_path(node1_id,to_id,return_type='cor_list'):
    from_id, x, y = get_position_wrapper('pellet_town')
    load_graph(node1_id)
    path = nx.dijkstra_path(G, from_id, to_id)

    if return_type == 'node_path':
        return path
    elif return_type == 'cor_list':
        cor_list=[]
        for node_id in path:
            cor_list.append((G.nodes[node_id]['x'],G.nodes[node_id]['y']))
        return cor_list

if __name__ == '__main__':
    load_graph(1)
    goal_id = 195
    goal_cor = (G.nodes[goal_id]['x'],G.nodes[goal_id]['y'])
    while True:
        try:
            cor_list = get_shortest_path(1, goal_id)
            path_interpreter_multi_t(cor_list)
            #current_id = cor_list[0]
        except WrongStep:
            pass

