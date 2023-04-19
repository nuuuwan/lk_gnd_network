from lgn.utils import shape_utils


def _(dist, node1, node2):
    return dist[node1].get(node2, float('inf'))


def _set_idem(dist, nodes):
    for node in nodes:
        dist[node] = {}
        dist[node][node] = 0


def _set_edges(dist, network):
    for node1, node2 in network.edge_pair_list:
        distance = shape_utils.compute_distance(
            network.node_idx[node1]['centroid'],
            network.node_idx[node2]['centroid'],
        )
        dist[node1][node2] = distance
        dist[node2][node1] = distance


def _expand(dist, nodes):
    for node2 in nodes:
        for node1 in nodes:
            for node3 in nodes:
                distance_via = _(dist, node1, node2) + _(dist, node2, node3)
                if distance_via < _(dist, node1, node3):
                    dist[node1][node3] = distance_via
    return dist


def build_distance_matrix_with_ford_warshall(network):
    nodes = network.node_list
    dist = {}
    _set_idem(dist, nodes)
    _set_edges(dist, network)
    _expand(dist, nodes)

    return dist
