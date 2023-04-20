import copy
from functools import cache, cached_property

from gig import Ent
from utils import Log

from lgn.core.node import Node
from lgn.utils.format_utils import format_distance

log = Log('network')


class NetworkBase:
    def __init__(self, node_list, edge_list):
        self.node_list = node_list
        self.edge_list = edge_list

    @classmethod
    def from_type(cls, ent_type: str, func_filter_ent=None):
        ent_list = Ent.list_from_type(ent_type)
        if func_filter_ent is not None:
            ent_list = [ent for ent in ent_list if func_filter_ent(ent)]

        node_list = [Node.from_ent(x[0], x[1]) for x in enumerate(ent_list)]
        edge_list = []
        return cls(node_list, edge_list)

    @cached_property
    def loc_list(self):
        return [node.centroid for node in self.node_list]

    @cached_property
    def n_nodes(self):
        return len(self.node_list)

    @cached_property
    def n_edges(self):
        return len(self.edge_list)

    @cached_property
    def total_population(self):
        return sum([node.population for node in self.node_list])

    @cached_property
    def total_people_pairs(self):
        total_population = self.total_population
        return total_population * (total_population - 1) // 2

    def __str__(self):
        lines = ['', f'NETWORK ({self.n_nodes})']
        for i, j in self.edge_list:
            node_i = self.node_list[i]
            node_j = self.node_list[j]
            lines.append(f'{node_i} ↔️ {node_j}')
        lines.append('')
        return '\n'.join(lines)

    @cache
    def is_edge(self, i, j):
        return (i, j) in self.edge_list or (j, i) in self.edge_list

    @cache
    def get_node(self, i):
        return self.node_list[i]

    def format_edge(self, edge):
        i, j = edge
        node_i = self.get_node(i)
        node_j = self.get_node(j)
        distance = self.get_distance(i, j)
        return f'{node_i} ↔️ {node_j} ({format_distance(distance)})'

    def __add__(self, edge_list):
        if not isinstance(edge_list, list):
            raise TypeError('edge_list must be a list')

        edge_list_copy = copy.deepcopy(self.edge_list)
        edge_list_copy += edge_list
        return self.__class__(self.node_list, edge_list_copy)
