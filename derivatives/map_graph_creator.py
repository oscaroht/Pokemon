
''''First a naive graph is created. This is a graph for a area without any obstacles'''

from sqlalchemy import create_engine
from fundamentals.config import config
import cv2

password = config('../users.ini','postgres','password')
engine = create_engine(f'postgresql+psycopg2://postgres:{password}@localhost/pokemon')

## add a lvl1 node
# with engine.connect() as con:
#     con.execute("insert into mart.nodes_lvl1 (node_name) values ('pellet_town');")
#     result = con.execute("select * from mart.nodes_lvl1;")
#     print(result)

def insert_edges(node1_id, id, x, y, con):
    con.execute(f"insert into stage.edges_lvl0 (node0_id_from, node1_id, x_to, y_to) values({id},{node1_id},{x+1},{y}); ")
    con.execute(f"insert into stage.edges_lvl0 (node0_id_from, node1_id, x_to, y_to) values({id},{node1_id},{x-1},{y}); ")
    con.execute(f"insert into stage.edges_lvl0 (node0_id_from, node1_id, x_to, y_to) values({id},{node1_id},{x},{y+1}); ")
    con.execute(f"insert into stage.edges_lvl0 (node0_id_from, node1_id, x_to, y_to) values({id},{node1_id},{x},{y-1}); ")

def naive_creator(node1_id, w,h):
    ''''Input is the number of tiles in the width and number of tiles in height'''
    with engine.connect() as con:
        id = 1
        for y in range(h):
            for x in range(w):
                con.execute(f"insert into stage.naive_nodes_lvl0 (node0_id, node1_id, x, y) values({id},{node1_id},{x},{y}); ")
                insert_edges(node1_id, id, x, y, con)
                id += 1
## do not count from zero, count the rows
## create pellet town w = 18, and h = 16
#create mom_lvl1 2, 8, 7
#create mom_lvl2 3, 8, 7
#create oaks_lab 4, 10,11
#create route1 5, 14, 43
# create viridian city (6, 32, 33)
# create route2a naive_creator(9, 12, 26)
#create viridian_forest (12, 32, 48)
# create ptb  (13, 10, 7)

# use this to calculate the w en h of the network
im = cv2.imread("C:\\Users\\oscar\\PycharmProjects\\Pokemon\\walk\\templates\\map\\viridian_forest.tmp")
cv2.imshow('bla', im)
cv2.waitKey()

# im2 = cv2.hconcat([im, im[:,365:366,:]])
# cv2.imshow('ad',im2)
# cv2.waitKey()

print(f"width: {im.shape[1]/16 - 9}\nheight: {im.shape[0]/16 - 8}") # so the number of pixels devided by 16x16 pixels per tile, minus 9 adn 8 for the edges of the image

naive_creator(12, 32, 48)
