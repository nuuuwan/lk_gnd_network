from functools import cache, cached_property

from scipy.sparse import csgraph, lil_matrix
from utils import Log

from lgn.utils import shape_utils

log = Log('network')


class NetworkDerived:
    @cache
    def get_distance(self, node_i, node_j):
        return shape_utils.compute_distance(
            self.get_node(node_i).centroid,
            self.get_node(node_j).centroid,
        )

    @cached_property
    def edge_and_distance_list(self):
        edge_and_distance_list = []
        for i, j in self.edge_list:
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

        for i, j in self.edge_list:
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

    @cache
    def get_close_node_pairs_and_distance_list(self, max_distance):
        x_list = []
        for i, j in self.all_node_pairs:
            distance = self.get_distance(i, j)
            if distance <= max_distance:
                x_list.append([[i, j], distance])
        return x_list

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

    @cached_property
    def all_non_edge_node_pairs(self):
        node_pairs = []
        for i, j in self.all_node_pairs:
            if not self.is_edge(i, j):
                node_pairs.append([i, j])
        return node_pairs
