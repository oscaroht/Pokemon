
''''First a naive graph is created. This is a graph for a area without any obstacles'''

from sqlalchemy import create_engine
from fundamentals.config import config

password = config('../users','postgres','password')
engine = create_engine(f'postgresql+psycopg2://postgres:{password}@localhost/pokemon')

## add a lvl1 node
# with engine.connect() as con:
#     con.execute("insert into mart.nodes_lvl1 (node_name) values ('pellet_town');")
#     result = con.execute("select * from mart.nodes_lvl1;")
#     print(result)

def insert_edges(id, x, y, con):
    con.execute(f"insert into stage.edges_lvl0 (node0_id_from, node1_id, x_to, y_to) values({id},{1},{x+1},{y}); ")
    con.execute(f"insert into stage.edges_lvl0 (node0_id_from, node1_id, x_to, y_to) values({id},{1},{x-1},{y}); ")
    con.execute(f"insert into stage.edges_lvl0 (node0_id_from, node1_id, x_to, y_to) values({id},{1},{x},{y+1}); ")
    con.execute(f"insert into stage.edges_lvl0 (node0_id_from, node1_id, x_to, y_to) values({id},{1},{x},{y-1}); ")

def naive_creator(w,h):
    ''''Input is the number of tiles in the width and number of tiles in height'''
    with engine.connect() as con:
        id = 1
        for y in range(h):
            for x in range(w):
                con.execute(f"insert into stage.naive_nodes_lvl0 (node0_id, node1_id, x, y) values({id},{1},{x},{y}); ")
                insert_edges(id, x, y, con)
                id += 1

## create pellet town w = 18, and h = 16
#naive_creator(18,16)                       # uncheck to write to database

