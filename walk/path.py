
class Path:

    def __init__(self, end_cor, start_cor = None, start_map_name = None):
        self.start_map_name = start_map_name
        self.start_cor = start_cor                                      # NOT IS USE tuple like ('mom_lvl1', 56)
        self.end_cor = end_cor                                          # tuple like ('mom_lvl1', 56)
        self.cor_dict = self.get_shortest_path(None, self.end_cor)
        self.id_path = None

    def get_shortest_path(self, start_map, end_cor):
        """ first lookup the start_map_id and start_map_name. Then get the current location and overwrite the current
        map, in case a different map is found. Then check if this is the final map (map containing the goal node1). If not
        return a function that brings you to the next map. If you are on the right map"""

        from walk.graphs import G_lvl1, G_lvl0, df_edges_lvl1
        from position import Position

        import networkx as nx
        import numpy as np

        # if isinstance(start_map, int):
        #     start_map_id = start_map
        #     start_map_name = df_edges_lvl1[df_edges_lvl1['from_id'] == start_map].iloc[0]['from_name']
        # elif isinstance(start_map, str):
        #     start_map_name = start_map
        #     start_map_id = df_edges_lvl1[df_edges_lvl1['from_name'] == start_map].iloc[0]['from_id']
        # elif start_map == None:
        #     start_map_name = None

        (start_map_name, from_id, x, y) = Position.eval_position()
        print(f"position is {(start_map_name, from_id, x, y)}")
        start_map_id = df_edges_lvl1[df_edges_lvl1['from_name'] == start_map_name].iloc[0]['from_id']

        print(f'Current is: {start_map_name}, {from_id}')

        # can be both name or id
        # load_graph()

        # GLOBAL PATH
        # if the current map is not the goal map than we need to go to the right map first

        print(f'Goal: {end_cor}')

        # find shortest path is global coordinates
        path_lvl1 = nx.dijkstra_path(G_lvl1, start_map_id,
                                     df_edges_lvl1[df_edges_lvl1['from_name'] == end_cor[0]].iloc[0]['from_id'])

        path = {}
        enter_node0_id = from_id
        ''' loop through the graphs and find the path in every graph to the next exit '''
        for idx, node_lvl1 in enumerate(path_lvl1[:-1]):  # next node is at 1
            # the first in path is the start, the second is set to the goal

            G = G_lvl0[node_lvl1]   # this is the current graph

            end_series = df_edges_lvl1[
                (df_edges_lvl1['from_id'] == path_lvl1[idx]) & (df_edges_lvl1['to_id'] == path_lvl1[idx + 1])].iloc[0]
            end_node0_id = end_series['exit_node0_id']
            end_node0_id_x = end_series['exit_x']
            end_node0_id_y = end_series['exit_y']
            if np.isnan(end_node0_id):
                end_node0_id = max(G.nodes) + 1

            '''' and exit node. Add the node, find the nodes that are 'next' to it, add an edge '''
            G.add_node(end_node0_id, x=end_node0_id_x, y=end_node0_id_y)
            ''' FOR BETTER PERFORMANCE DO NOT LOOP BUT LOOK IF THE MINUS/PLUS 1 EXISTS'''
            for id, node in G.nodes(data=True):
                ''' look for coordinates either 1 to left or right (x +- 1) and y the same, or 1 to upper of lower so
                 y +- 1 but with the x the same. So exit (3,5) has edges to (3,4) or (4,5)...'''

                try:
                    if ( abs(node['x'] - end_series['exit_x']) == 1 and node['y'] == end_series['exit_y'] ) \
                            or ( abs(node['y'] - end_series['exit_y']) == 1 and node['x'] == end_series['exit_x'] ):

                        G.add_edge(end_node0_id, id)
                except:
                    a=1

            ''' calculate the shortest path, reset the entry node (for the new map) '''
            path[node_lvl1] = nx.dijkstra_path(G, enter_node0_id, end_node0_id)
            enter_node0_id = df_edges_lvl1[
                (df_edges_lvl1['from_id'] == path_lvl1[idx]) & (df_edges_lvl1['to_id'] == path_lvl1[idx + 1])].iloc[0][
                'enter_node0_id']

        ''' if we made it here we are in the final graph. This is the graph with id last in the path_lvl1 list. 
        Calculate the path to the end node from the enter node. '''
        G = G_lvl0[int(path_lvl1[-1])]
        path[path_lvl1[-1]] = nx.dijkstra_path(G, enter_node0_id, end_cor[1])
        self.id_path = path         # save id_path, might be useful later

        ''' we have a list of node ids now. The stepper cannot interpret this so we need to translate it to x and y 
        coordinates. Then the stepper knows what to step. '''
        rt = {}
        for key, value in path.items():
            G = G_lvl0[key]
            cor_list = []
            for node_id in value:
                cor_list.append((G.nodes[node_id]['x'], G.nodes[node_id]['y']))
            rt[key] = cor_list
        return rt

