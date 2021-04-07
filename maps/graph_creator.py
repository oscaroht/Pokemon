
''''This file contains functions to create graphs from database tables, use the graphs to calculate the
shortest path and determines the individual steps.'''

from sqlalchemy import create_engine
import networkx as nx
import matplotlib.pyplot as plt

engine = create_engine('postgresql+psycopg2://postgres:Postoscar1@localhost/pokemon')

G = nx.Graph()

with engine.connect() as con:
    mart_edges = con.execute(f"select * from mart.edges_lvl0; ")
    node_positions = con.execute('select node0_id, x, y from stage.naive_nodes_lvl0;')

for row in mart_edges:
    G.add_edge(row['node0_id_from'], row['node0_id_to'])

