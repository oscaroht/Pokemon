
''''This file is used to make a graphical representation of a graph. It is ment to resemble the screen. It is used for
debugging'''

from sqlalchemy import create_engine
import networkx as nx
import matplotlib.pyplot as plt
from fundamentals.config import config

password = config('../users.ini','postgres','password')
engine = create_engine(f'postgresql+psycopg2://postgres:{password}@localhost/pokemon')

node1_id = 1

G = nx.Graph()

with engine.connect() as con:
    mart_edges = con.execute(f"select * from mart.edges_lvl0 where node1_id = {node1_id}; ")
    node_positions = con.execute(f'select node0_id, x, y from mart.nodes_lvl0 where node1_id = {node1_id};')

for row in mart_edges:
    #item = row.items()
    G.add_edge(row['node0_id_from'], row['node0_id_to'])

pos={}
row_num = 0
for row in node_positions:
    #print(row['node0_id'],row['x'], row['y'] )
    pos[row['node0_id']] = (row['x'], row['y'])

path = nx.dijkstra_path(G, 1, 195)

## just for visual testing
flipped_pos = {node: (x,-y) for (node, (x,y)) in pos.items()} # flip axes
nx.draw(G, pos=flipped_pos, with_labels=True, font_weight='bold',node_color = 'b')
nx.draw(G, pos=flipped_pos,nodelist=path, with_labels=True, font_weight='bold',node_color= 'r')
plt.show()

test=1

