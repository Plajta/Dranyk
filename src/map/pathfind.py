import networkx as nx
from networkx.algorithms.shortest_paths.astar import astar_path


def __add_paths_to_graphs__(data, graph, factor):
    pass


def run_pathfind(river_data, railway_data):
    G = nx.Graph()
    print(river_data)

    __add_paths_to_graphs__(river_data["features"], G, weight_factor=1)
    __add_paths_to_graphs__(railway_data["features"], G, weight_factor=2)

    start = (0, 0) # TODO
    end = (0, 0) # TODO

    shortest_path = astar_path(G, source=start, target=end, weight="weight")
    print(shortest_path) #TODO
