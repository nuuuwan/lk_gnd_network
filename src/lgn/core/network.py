import copy
from functools import cache, cached_property

from gig import Ent
from scipy.sparse import csgraph, lil_matrix
from utils import Log

from lgn.core.node import Node
from lgn.utils import shape_utils

log = Log('network')


class Network:
    def __init__(self, node_list, edge_list):
        self.__node_list = node_list
        self.__edge_list = edge_list

    @staticmethod
    def from_type(ent_type: str, func_filter_ent=None):
        ent_list = Ent.list_from_type(ent_type)
        if func_filter_ent is not None:
            ent_list = [ent for ent in ent_list if func_filter_ent(ent)]

        node_list = [Node.from_ent(x[0], x[1]) for x in enumerate(ent_list)]
        edge_list = []
        return Network(node_list, edge_list)

    @cached_property
    def loc_list(self):
        return [node.centroid for node in self.__node_list]

    @cached_property
    def __node_list(self):
        return list(self.node_idx.keys())

    @cached_property
    def n_nodes(self):
        return len(self.__node_list)

    @cached_property
    def n_edges(self):
        return len(self.__edge_list)

    @cache
    def get_distance(self, node_i, node_j):
        return shape_utils.compute_distance(
            self.get_node(node_i).centroid,
            self.get_node(node_j).centroid,
        )

    @cached_property
    def edge_and_distance_list(self):
        edge_and_distance_list = []
        for i, j in self.__edge_list:
            assert i < j
            distance = self.get_distance(i, j)
            edge_and_distance_list.append([[i, j], distance])
        return edge_and_distance_list

    @cached_property
    def neighbor_idx(self):
        neighbor_idx = {}

        def add(i, j):
            if i not in neighbor_idx:
                neighbor_idx[i] = []
            neighbor_idx[i].append(j)

        for i, j in self.__edge_list:
            assert i < j
            add(i, j)
            add(j, i)

        return neighbor_idx

    @cached_property
    def edge_dist_matrix(self):
        n = self.n_nodes
        edge_dist_matrix = lil_matrix((n, n), dtype=float)
        for i in range(n):
            edge_dist_matrix[i, i] = 0

        for [i, j], distance in self.edge_and_distance_list:
            assert i < j
            edge_dist_matrix[i, j] = distance
            edge_dist_matrix[j, i] = distance
        return edge_dist_matrix

    @cached_property
    def dist_matrix(self):
        dist_matrix = lil_matrix(
            csgraph.floyd_warshall(self.edge_dist_matrix)
        )
        return dist_matrix

    @cached_property
    def network_length(self):
        return sum([distance for _, distance in self.edge_and_distance_list])

    @cached_property
    def total_population(self):
        return sum([node.population for node in self.__node_list])

    @cached_property
    def total_people_pairs(self):
        total_population = self.total_population
        return total_population * (total_population - 1) // 2

    @cached_property
    def all_node_pairs(self):
        n = self.n_nodes
        return [(i, j) for i in range(n) for j in range(i + 1, n)]

    @cached_property
    def connected_node_pairs(self):
        node_pairs = []
        dist_matrix = self.dist_matrix
        for i, row in enumerate(dist_matrix.rows):
            for j, val in zip(row, dist_matrix.data[i]):
                if val != float('inf') and i < j:
                    node_pairs.append(([i, j], val))
        return node_pairs

    def __add__(self, edge_list):
        if not isinstance(edge_list, list):
            raise TypeError('edge_list must be a list')

        edge_list_copy = copy.deepcopy(self.__edge_list)
        edge_list_copy += edge_list
        return Network(self.__node_list, edge_list_copy)

    def __str__(self):
        lines = ['', f'NETWORK ({self.n_nodes})']
        for i, j in self.__edge_list:
            node_i = self.__node_list[i]
            node_j = self.__node_list[j]
            lines.append(f'{node_i} ↔️ {node_j}')
        lines.append('')
        return '\n'.join(lines)

    @cache
    def is_edge(self, i, j):
        return (i, j) in self.__edge_list or (j, i) in self.__edge_list

    @cache
    def get_node(self, i):
        return self.__node_list[i]

    @cached_property
    def edge_list(self):
        return self.__edge_list

    @cached_property
    def node_list(self):
        return self.__node_list

    @cache
    def format_edge(self, edge):
        i, j = edge
        node_i = self.get_node(i)
        node_j = self.get_node(j)
        return f'{node_i} ↔️ {node_j}'


if __name__ == '__main__':
    from gig import EntType

    from lgn.utils.console_utils import print_line

    network = Network.from_type(EntType.PROVINCE)
    print(network)
    print(network.loc_list)
    network = network + [(0, 2), (0, 5)]
    print(network)

    print(network.neighbor_idx)
    print_line()
    print(network.edge_dist_matrix)
    print_line()
    print(network.dist_matrix)
    print_line()
    print(network.network_length)

    print_line()
    print(network.total_population)
    print(network.total_people_pairs)
    print(network.all_node_pairs)

    print(network.connected_node_pairs)

    print(network + [(0, 8)])
