
class Path:

    def __init__(self, end_cor, start_cor = None, start_map_name = None):
        self.start_map_name = start_map_name
        self.start_cor = start_cor                                      # NOT IS USE tuple like ('mom_lvl1', 56)
        self.end_cor = end_cor                                          # tuple like ('mom_lvl1', 56)
        self.cor_dict = self.get_shortest_path(None, self.end_cor)

    def get_shortest_path(self, start_map, end_cor):
        """ first lookup the start_map_id and start_map_name. Then get the current location and overwrite the current
        map, in case a different map is found. Then check if this is the final map (map containing the goal node1). If not
        return a function that brings you to the next map. If you are on the right map"""

        from walk.graphs import G_lvl1, G_lvl0, df_edges_lvl1
        import networkx as nx
        from walk.position import get_position

        if isinstance(start_map, int):
            start_map_id = start_map
            start_map_name = df_edges_lvl1[df_edges_lvl1['from_id'] == start_map].iloc[0]['from_name']
        elif isinstance(start_map, str):
            start_map_name = start_map
            start_map_id = df_edges_lvl1[df_edges_lvl1['from_name'] == start_map].iloc[0]['from_id']
        elif start_map == None:
            start_map_name = None

        (start_map_name, from_id, x, y) = get_position(start_map_name)
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
        for idx, node_lvl1 in enumerate(path_lvl1[:-1]):  # next node is at 1
            # the first in path is the start, the second is set to the goal
            # G_current_lvl0 = load_graph(int(node_lvl1))
            G_current_lvl0 = G_lvl0[node_lvl1]
            end_node0_id = df_edges_lvl1[
                (df_edges_lvl1['from_id'] == path_lvl1[idx]) & (df_edges_lvl1['to_id'] == path_lvl1[idx + 1])].iloc[0][
                'exit_node0_id']

            # add the exit node to the map

            path[node_lvl1] = nx.dijkstra_path(G_current_lvl0, enter_node0_id, end_node0_id)
            enter_node0_id = df_edges_lvl1[
                (df_edges_lvl1['from_id'] == path_lvl1[idx]) & (df_edges_lvl1['to_id'] == path_lvl1[idx + 1])].iloc[0][
                'enter_node0_id']

        # last time we are going to the goal node
        G_current_lvl0 = G_lvl0[int(path_lvl1[-1])]  # load_graph(int(path_lvl1[-1]))
        path[path_lvl1[-1]] = nx.dijkstra_path(G_current_lvl0, enter_node0_id, end_cor[1])

        rt = {}
        for key, value in path.items():
            G_current_lvl0 = G_lvl0[key]  # load_graph(int(key))
            cor_list = []
            for node_id in value:
                cor_list.append((G_current_lvl0.nodes[node_id]['x'], G_current_lvl0.nodes[node_id]['y']))
            rt[key] = cor_list
        return rt

        # # SET RETURN TYPE
        # if return_type == 'node_list':
        #     return path
        # elif return_type == 'cor_list':
        #     rt = {}
        #     for key, value in path.items():
        #         G_current_lvl0 = G_lvl0[key]  # load_graph(int(key))
        #         cor_list = []
        #         for node_id in value:
        #             cor_list.append((G_current_lvl0.nodes[node_id]['x'], G_current_lvl0.nodes[node_id]['y']))
        #         rt[key] = cor_list
        #     return rt

        def add_exit_node():
            """ The exit node should only be added to the map when the exit is the goal. Otherwise the exit node might be used
            accidentally """
