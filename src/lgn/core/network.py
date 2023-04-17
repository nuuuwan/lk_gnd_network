from gig import Ent, EntType
from utils import List, Log

log = Log('network')


def point_to_key(point):
    lng, lat = point
    return f'{lng:.2f}_{lat:.2f}'


def build_node_idx(ent_list):
    node_idx = {}
    for ent in ent_list:
        print(ent.d)
        node_idx[ent.name] = dict(
            centroid=ent.centroid,
            population=ent.population,
        )
    return node_idx

def build_key_to_ent_set(ent_list):
    key_to_ent_set = {}
    for ent in ent_list:
        raw_geo = ent.get_raw_geo()
        point_list = List(raw_geo).flatten()
        key_list = [point_to_key(point) for point in point_list]
        ent_id = ent.name
        for key in key_list:
            if key not in key_to_ent_set:
                key_to_ent_set[key] = set()
            key_to_ent_set[key].add(ent_id)
    return key_to_ent_set

def buiid_neighbor_idx(key_to_ent_set):
    neighbor_idx = {}
    for key, ent_set in key_to_ent_set.items():
        if len(ent_set) == 1:
            continue

        for ent_id in ent_set:
            if ent_id not in neighbor_idx:
                neighbor_idx[ent_id] = set()
            neighbor_idx[ent_id] |= ent_set
    return neighbor_idx

def build_edge_pair_list(neighbor_idx):
    edge_pair_list = []
    for id, id_set in neighbor_idx.items():
        for id2 in id_set:
            edge_pair_list.append([id, id2])
    return edge_pair_list

class Network:
    def __init__(self, node_idx, edge_pair_list):
        self.node_idx = node_idx
        self.edge_pair_list = edge_pair_list

    @staticmethod
    def from_type(ent_type: str):
        ent_list = Ent.list_from_type(ent_type)
        node_idx = build_node_idx(ent_list)
        key_to_ent_set = build_key_to_ent_set(ent_list)
        neighbor_idx = buiid_neighbor_idx(key_to_ent_set)
        edge_pair_list = build_edge_pair_list(neighbor_idx)
        return Network(node_idx, edge_pair_list)

    @property
    def d(self):
        return dict(node_idx=self.node_idx, edge_pair_list=self.edge_pair_list)

    def __str__(self):
        return str(self.d)

    @property
    def loc_list(self):
        return [node['centroid'] for node in self.node_idx.values()]
