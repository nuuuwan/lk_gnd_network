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
        self.node_list = node_list
        self.edge_list = edge_list

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
        return [node.centroid for node in self.node_list]

    @cached_property
    def node_list(self):
        return list(self.node_idx.keys())

    @cache
    def __len__(self):
        return len(self.node_list)

    @cached_property
    def edge_and_distance_list(self):
        edge_and_distance_list = []
        for i, j in self.edge_list:
            assert i < j
            distance = shape_utils.compute_distance(
                self.node_list[i].centroid,
                self.node_list[j].centroid,
            )
            edge_and_distance_list.append([[i, j], distance])
        return edge_and_distance_list

    @cached_property
    def neighbor_idx(self):
        neighbor_idx = {}

        def add(i, j):
            if i not in neighbor_idx:
                neighbor_idx[i] = []
            neighbor_idx[i].append(j)

        for i, j in self.edge_list:
            assert i < j
            add(i, j)
            add(j, i)

        return neighbor_idx

    @cached_property
    def edge_dist_matrix(self):
        n = len(self)
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
        return sum([node.population for node in self.node_list])

    @cached_property
    def total_people_pairs(self):
        total_population = self.total_population
        return total_population * (total_population - 1) // 2

    @cached_property
    def all_node_pairs(self):
        n = len(self)
        return [(i, j) for i in range(n) for j in range(i + 1, n)]

    @cached_property
    def connected_node_pairs(self):
        node_pairs = []
        dist_matrix = self.dist_matrix
        for i, row in enumerate(dist_matrix.rows):
            for j, val in zip(row, dist_matrix.data[i]):
                if val != float('inf') and i < j:
                    node_pairs.append((i, j))
        return node_pairs
    
    def __add__(self, edge):
        assert(type(edge) == tuple and len(edge) == 2)

        edge_list_copy = copy.deepcopy(self.edge_list)
        edge_list_copy.append(edge)                
        return Network(self.node_list, edge_list_copy)
    
    def __str__(self):
        lines = ['', f'NETWORK ({len(self)})']
        for i,j in self.edge_list:
            node_i = self.node_list[i]
            node_j = self.node_list[j]
            lines.append(f'{node_i} ↔️ {node_j}')
        lines.append('')
        return '\n'.join(lines)
        
    
if __name__ == '__main__':
    from gig import EntType

    from lgn.utils.console_utils import print_line

    network = Network.from_type(EntType.PROVINCE)
    print(network)
    print(network.loc_list)
    network.edge_list = [
        [0, 2],
        [0, 5],
    ]

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

    print(network + (0,8))