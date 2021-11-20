import os
import networkx as nx
from fundamentals.config import config
from sqlalchemy import create_engine
import pandas as pd

def load_graph():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    password = config('../users.ini', 'postgres', 'password')
    engine = create_engine(f'postgresql+psycopg2://postgres:{password}@localhost/pokemon')

    G_lvl1 = nx.Graph()
    edges_lvl1={}
    with engine.connect() as con:
        edges = con.execute(f"select * from mappings.edges_lvl1;")
        df_edges_lvl1 = pd.read_sql_table('edges_lvl1', con=con, schema='mappings',coerce_float=False)
    for row in edges:
        G_lvl1.add_edge(row['from_id'], row['to_id'])
        edges_lvl1[row['from_id'],row['to_id']]=dict(row)

    G_lvl0 = {}
    with engine.connect() as con:
        distinct_node1 = con.execute(f"select distinct node1_id from mart.nodes_lvl0;")
        for row in distinct_node1:
            G_current = nx.Graph()
            node1_id = row['node1_id']
            print(f'Loading.. graph node1_id: {node1_id}')
            edges = con.execute(f"select * from mart.edges_lvl0 where node1_id = {node1_id}; ")
            nodes = con.execute(f'select node0_id, x, y from mart.nodes_lvl0 where node1_id = {node1_id};')
            for roww in nodes:
                G_current.add_node(roww[0], x=roww[1], y=roww[2])
                try:
                    roww[0] + 1
                except:
                    a = 1
            for roww in edges:
                # item = row.items()
                G_current.add_edge(roww['node0_id_from'], roww['node0_id_to'])
            G_lvl0[node1_id] = G_current

    return G_lvl1, G_lvl0, df_edges_lvl1, edges_lvl1


class G:
    G_lvl1, G_lvl0, df_edges_lvl1, edges_lvl1 = load_graph()


if __name__ == '__main__':
    test=1