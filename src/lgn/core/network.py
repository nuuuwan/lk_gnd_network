import copy
from functools import cached_property

from gig import Ent
from utils import Log

from lgn.utils import distance_matrix, shape_utils

log = Log('network')


def build_node_idx(ent_list):
    node_idx = {}
    for i, ent in enumerate(ent_list):
        if i % 100 == 0:
            log.debug(f'build_node_idx: {ent.id} ({ent.name})')
        raw_geo = ent.get_raw_geo()
        area = shape_utils.compute_area(raw_geo)
        population = ent.population

        node_idx[ent.name] = dict(
            centroid=ent.centroid,
            population=population,
            area=area,
            population_density=population / area,
        )
    return node_idx


class Network:
    def __init__(self, node_idx, edge_pair_list):
        self.node_idx = node_idx
        self.edge_pair_list = edge_pair_list

    @staticmethod
    def from_type(ent_type: str, func_filter_ent=None):
        ent_list = Ent.list_from_type(ent_type)
        if func_filter_ent is not None:
            ent_list = [ent for ent in ent_list if func_filter_ent(ent)]
        node_idx = build_node_idx(ent_list)
        edge_pair_list = []
        return Network(node_idx, edge_pair_list)

    @cached_property
    def d(self):
        return dict(
            node_idx=self.node_idx, edge_pair_list=self.edge_pair_list
        )

    def __str__(self):
        return str(self.d)

    @cached_property
    def loc_list(self):
        return [node['centroid'] for node in self.node_idx.values()]

    @cached_property
    def node_list(self):
        return list(self.node_idx.keys())

    @property
    def neighbor_idx(self):
        neighbor_idx = {}
        for id1, id2 in self.edge_pair_list:
            if id1 not in neighbor_idx:
                neighbor_idx[id1] = []
            if id2 not in neighbor_idx:
                neighbor_idx[id2] = []
            neighbor_idx[id1].append(id2)
            neighbor_idx[id2].append(id1)
        return neighbor_idx

    @property
    def distance_matrix(self):
        return distance_matrix.build_distance_matrix_with_ford_warshall(self)

    @property
    def network_length(self):
        network_length = 0
        for node1, node2 in self.edge_pair_list:
            distance = shape_utils.compute_distance(
                self.node_idx[node1]['centroid'],
                self.node_idx[node2]['centroid'],
            )
            network_length += distance
        return network_length

    @cached_property
    def total_population(self):
        return sum([node['population'] for node in self.node_idx.values()])

    @cached_property
    def total_people_pairs(self):
        total_population = self.total_population
        return total_population * (total_population - 1) / 2

    @property
    def info(self):
        return f'{self.network_length:,.0f}km'

    @property
    def info2(self):
        node1, node2 = self.edge_pair_list[-1]
        return f'+ {node1} to {node2}'

    @cached_property
    def all_node_pairs(self):
        return [
            (node1, node2)
            for node1 in self.node_list
            for node2 in self.node_list
            if node1 < node2
        ]

    @property
    def connected_node_pairs(self):
        node_pairs = []
        distance_matrix = self.distance_matrix
        for node1, node2_to_distance in distance_matrix.items():
            for node2, distance in node2_to_distance.items():
                if all(
                    [
                        node1 < node2,
                        distance != 0,
                        distance != float('inf'),
                    ]
                ):
                    node_pairs.append((node1, node2, distance))
        return node_pairs

    def deepcopy(self):
        return Network(
            copy.deepcopy(self.node_idx), copy.deepcopy(self.edge_pair_list)
        )
