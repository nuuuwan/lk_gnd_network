from utils import Log
log = Log('road_network')
def ordered_neighbor_idx(network):
    neighbor_idx = {}
    for id1, id2 in network.edge_pair_list:
        if id1 not in neighbor_idx:
            neighbor_idx[id1] = []
        neighbor_idx[id1].append(id2)

    for id, neighbors in neighbor_idx.items():
        neighbor_idx[id] = sorted(
            neighbors, key=lambda id: -network.node_idx[id]['population']
        )

    return neighbor_idx


def rebuild(network, origin_node=None):
    if not origin_node:
        origin_node = list(network.node_idx.keys())[0]
    neighbor_idx = ordered_neighbor_idx(network)

    to_visit_nodes = set()
    to_visit_nodes.add(origin_node)
    connected_nodes = set(origin_node)
    visited_nodes = set()

    new_edge_pair_list = []
    while to_visit_nodes:
        to_visit_nodes_sorted = sorted(to_visit_nodes, key=lambda node: -network.node_idx[node]['population'])
        node = to_visit_nodes_sorted[0]
        to_visit_nodes.remove(node)
        visited_nodes.add(node)

        log.debug(f'visitting: {node} ' + str(to_visit_nodes))

        neighbors = neighbor_idx[node]

        for node2 in neighbors:
            if node2 not in visited_nodes:
                to_visit_nodes.add(node2)
            if node2 not in connected_nodes:
                new_edge_pair_list.append([node, node2])
                connected_nodes.add(node2)
                
    network.edge_pair_list = new_edge_pair_list
    return network
