import logging
logger = logging.getLogger(__name__)

from .graphs import G
from .position import Position, LocationNotFound

class Path():

    path = None

    def __init__(self, end_cor, start_cor=None, start_map_name=None):
        self.start_map_name = start_map_name
        self.start_cor = start_cor  # NOT IS USE tuple like ('mom_lvl1', 56)
        self.end_cor = end_cor  # tuple like ('mom_lvl1', 56)
        self.cor_dict = self.get_shortest_path(None, self.end_cor)
        self.id_path = None

    def get_shortest_path(self, start_map, end_cor):
        """ first lookup the start_map_id and start_map_name. Then get the current location and overwrite the current
        map, in case a different map is found. Then check if this is the final map (map containing the goal node1). If not
        return a function that brings you to the next map. If you are on the right map"""

        # from walk.graphs import G_lvl1, G_lvl0, df_edges_lvl1
        # from position import Position

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

        # def add_entry_node(G, start_node0_id, x, y):
        #     ''' FOR BETTER PERFORMANCE DO NOT LOOP BUT LOOK IF THE MINUS/PLUS 1 EXISTS'''
        #     for id, node in G.nodes(data=True):
        #         ''' look for coordinates either 1 to left or right (x +- 1) and y the same, or 1 to upper of lower so
        #          y +- 1 but with the x the same. So exit (3,5) has edges to (3,4) or (4,5)...'''
        #         try:
        #             if (abs(node['x'] - x) == 1 and node['y'] == y) \
        #                     or (abs(node['y'] - y) == 1 and node['x'] == x):
        #                 # add actual node
        #                 G.add_edge(start_node0_id, id)
        #         except:
        #             a = 1
        #     return G

        def add_exit_entry_node(G, x, y):
            new_node_id = max(G)+1
            G.add_node(max(G)+1, x=x, y=y)
            for id, node in G.nodes(data=True):
                ''' look for coordinates either 1 to left or right (x +- 1) and y the same, or 1 to upper of lower so
                 y +- 1 but with the x the same. So exit (3,5) has edges to (3,4) or (4,5)...'''
                try:
                    if (abs(node['x'] - x) == 1 and node['y'] == y) \
                            or (abs(node['y'] - y) == 1 and node['x'] == x):
                        # add actual node
                        G.add_edge(new_node_id, id)
                except:
                    pass
            return G, new_node_id

        def get_cor_list(gi, path):
            cor_list = []
            for p in path:
                cor_list.append((gi.nodes[p]['x'], gi.nodes[p]['y']))
            return cor_list

        # def add_exit_node(G, end_node0_id, x, y):
        #     ''' FOR BETTER PERFORMANCE DO NOT LOOP BUT LOOK IF THE MINUS/PLUS 1 EXISTS'''
        #     for id, node in G.nodes(data=True):
        #         ''' look for coordinates either 1 to left or right (x +- 1) and y the same, or 1 to upper of lower so
        #          y +- 1 but with the x the same. So exit (3,5) has edges to (3,4) or (4,5)...'''
        #         try:
        #             if (abs(node['x'] - x) == 1 and node['y'] == y) \
        #                     or (abs(node['y'] - y) == 1 and node['x'] == x):
        #                 G.add_edge(end_node0_id, id)
        #         except:
        #             a = 1
        #     return G

        (start_map_name, from_id, x, y) = Position.eval_position()
        logger.debug(f"Path: position is {(start_map_name, from_id, x, y)}")

        # get start map id using the name
        start_map_id = G.df_edges_lvl1[G.df_edges_lvl1['from_name'] == start_map_name].iloc[0]['from_id']
        # get the id of the end map using the name
        end_map_id = int(G.df_edges_lvl1[G.df_edges_lvl1['from_name'] == end_cor[0]].iloc[0]['from_id'])
        # find shortest path is global coordinates
        path_lvl1 = nx.dijkstra_path(G.G_lvl1, start_map_id, end_map_id )


        '''' Algo: 
        start = begin
        loop over entry/exit pairs: 
        [(exit_map_id,entry_map_id) for exit_map_id,entry_map_id in zip(path_lvl1,path_lvl1[1:])] 
        end = goal
        then if idx != 0
            add entry node
            start = entry_node
        then get the exit and entry nodes,
        if idx != len -1 (last map)
            do add exit 
            end = exit
        
        calculate shortest path between start and end
        '''
        path = {}
        rt = {}
        if len(path_lvl1) == 1:
            g = G.G_lvl0[start_map_id]
            if from_id not in g:  # if the start is not in the 1st map
                logger.warning(f"Start coordinate not in start Graph")
                g, start = add_exit_entry_node(g, x, y)  # add entry node
            path[start_map_id] = nx.dijkstra_path(g, from_id, end_cor[1])
            rt[start_map_id] = get_cor_list(g, path[start_map_id])
        else:
            start = from_id
            goal = end_cor[1]
            eeps = [(a,b) for a, b in zip(path_lvl1, path_lvl1[1:])] # exit entry pair
            for idx, eep in enumerate(eeps+[(eeps[-1][1],eeps[-1][0])]):
                from_map_id = eep[0] # entry map, map from where we came
                g = G.G_lvl0[from_map_id].copy() # we want to copy because se do not want to add the nodes permanently

                if idx != 0:        # exclude the first pair (entry/exit)
                    g, start = add_exit_entry_node(g,series['enter_x'], series['enter_y']) # add entry node
                else:
                    if start not in g: # if the start is not in the 1st map
                        logger.warning(f"Start coordinate not in start Graph")
                        g, start = add_exit_entry_node(g, x, y)  # add entry node
                series = G.edges_lvl1[eep]
                if idx == len(eeps + [eeps[-1]])-1: # last one
                    end = goal
                else:
                    g, end = add_exit_entry_node(g, series['exit_x'], series['exit_y'])

                # if idx != len(eeps)-1: # exclude the last pair (entry/exit)
                #     G, end = add_exit_entry_node(G, series['exit_x'], series['exit_y'])
                # else:
                #     end = goal # the last map we are not going to the exit, we are going to the goal coordinate

                current_path = nx.dijkstra_path(g, start, end)
                logger.debug(f"current_path: {current_path}")
                path[from_map_id] = current_path
                rt[from_map_id] = get_cor_list(g, current_path)


        logger.debug(f"Full path: {path}")
        self.id_path = path
        Path.path = path
        return rt

        #
        # ''' loop through the graphs and find the path in every graph to the next exit '''
        # for idx, node_lvl1 in enumerate(path_lvl1[:-1]):  # next node is at 1
        #     # the first in path is the start, the second is set to the goal
        #
        #     G = Path.G_lvl0[node_lvl1]  # this is the current graph
        #     if idx != 0: # if this is not the first map we add the entry node of the previous
        #         '''' add entry node. Does not matter is it is double I hope '''
        #         G.add_node(start_node0_id, x=int(end_series['enter_x']), y=int(end_series['enter_y']))
        #         G = add_entry_node(G, start_node0_id, int(end_series['enter_x']), int(end_series['enter_y']))
        #
        #     if idx < len(path_lvl1) - 1: # between 1st (excl.) and last (excl.)
        #         end_series = \
        #         Path.df_edges_lvl1[(Path.df_edges_lvl1['from_id'] == path_lvl1[idx]) & (Path.df_edges_lvl1['to_id'] == path_lvl1[idx + 1])].iloc[0]
        #     else:
        #         # for the last map there is no next map so we use the previous end_series
        #         end_series = \
        #         Path.df_edges_lvl1[(Path.df_edges_lvl1['from_id'] == path_lvl1[-2]) & (Path.df_edges_lvl1['to_id'] ==
        #                                                                                path_lvl1[-1])].iloc[0]
        #     end_node0_id = end_series['exit_node0_id']
        #     start_node0_id = end_series['enter_node0_id']
        #     if np.isnan(end_node0_id):
        #         end_node0_id = int(max(G.nodes) + 1)
        #     if np.isnan(start_node0_id):
        #         start_node0_id = int(max(G.nodes) + 1)
        #
        #     '''' and exit node. Add the node, find the nodes that are 'next' to it, add an edge '''
        #     G.add_node(end_node0_id, x=int(end_series['exit_x']), y=int(end_series['exit_y']))
        #     G = add_exit_node(G, end_node0_id, int(end_series['exit_x']), int(end_series['exit_y']))
        #
        #     ''' calculate the shortest path, reset the entry node (for the new map) '''
        #     print('second dijkstra')
        #     ''' not the final map so we go from enter to exit '''
        #     path[node_lvl1] = nx.dijkstra_path(G, enter_node0_id, end_node0_id)
        #     enter_node0_id = int(Path.df_edges_lvl1[
        #         (Path.df_edges_lvl1['from_id'] == path_lvl1[idx]) & (
        #                     Path.df_edges_lvl1['to_id'] == path_lvl1[idx + 1])].iloc[0][
        #         'enter_node0_id'])
        #
        # '''' final map so we go from enter to goal'''
        # G = Path.G_lvl0[int(path_lvl1[-1])]
        #
        # # we need to add the enter node
        # start_node0_id = enter_node0_id
        # if len(path_lvl1) > 1:
        #     end_series = Path.df_edges_lvl1[
        #         (Path.df_edges_lvl1['from_id'] == path_lvl1[-2]) & (Path.df_edges_lvl1['to_id'] == path_lvl1[-1])].iloc[
        #         0]
        #     start_node0_id = end_series['enter_node0_id']
        #     if np.isnan(start_node0_id):
        #         start_node0_id = max(G.nodes) + 1
        #     G.add_node(start_node0_id, x=end_series['enter_x'], y=end_series['enter_y'])
        #     G = add_entry_node(G, start_node0_id, end_series['enter_x'], end_series['enter_y'])
        #
        # # the actual path
        # path[path_lvl1[-1]] = nx.dijkstra_path(G, start_node0_id, end_cor[1])
        # self.id_path = path  # save id_path, might be useful later

        # print(f"Path: {path}")

        # ''' if we made it here we are in the final graph. This is the graph with id last in the path_lvl1 list.
        # Calculate the path to the end node from the enter node. '''
        # G = G_lvl0[int(path_lvl1[-1])]
        # ''' add exit node'''
        # end_series = df_edges_lvl1[
        #     (df_edges_lvl1['from_id'] == path_lvl1[-2]) & (df_edges_lvl1['to_id'] == path_lvl1[-1])].iloc[0]
        # for id, node in G.nodes(data=True):
        #     ''' look for coordinates either 1 to left or right (x +- 1) and y the same, or 1 to upper of lower so
        #      y +- 1 but with the x the same. So exit (3,5) has edges to (3,4) or (4,5)...'''
        #     try:
        #         if (abs(node['x'] - end_series['exit_x']) == 1 and node['y'] == end_series['exit_y']) \
        #                 or (abs(node['y'] - end_series['exit_y']) == 1 and node['x'] == end_series['exit_x']):
        #             G.add_edge(end_node0_id, id)
        #     except:
        #         pass
        #
        # path[path_lvl1[-1]] = nx.dijkstra_path(G, enter_node0_id, end_cor[1])
        # self.id_path = path         # save id_path, might be useful later

        # ''' we have a list of node ids now. The stepper cannot interpret this so we need to translate it to x and y
        # coordinates. Then the stepper knows what to step. '''
        # rt = {}
        # for key, value in path.items():
        #     G = Path.G_lvl0[key]
        #     cor_list = []
        #     for node_id in value:
        #         cor_list.append((G.nodes[node_id]['x'], G.nodes[node_id]['y']))
        #     rt[key] = cor_list
        # print(f"Coordinate list: {rt}")
        # return rt


if __name__ == '__main__':
    pass