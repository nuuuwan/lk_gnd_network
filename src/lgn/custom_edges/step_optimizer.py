import random

from utils import Log

from lgn.utils.console_utils import tab
from lgn.utils.format_utils import format_distance, format_time

log = Log('random_optimizer')
MAX_STEPS = 1000


def optimize_step(network):
    edge_list = network.all_non_edge_node_pairs
    random.shuffle(edge_list)
    # edge_list= edge_list[:40]

    original_att = network.average_travel_time
    best_attrptlh = 0
    best_edge = None

    for edge in edge_list:
        network_copy = network + [edge]
        att = network_copy.average_travel_time
        att_reduction = original_att - att
        track_length = network.get_distance(*edge)
        attrptlh = att_reduction / track_length
        if attrptlh > best_attrptlh:
            best_attrptlh = attrptlh
            best_edge = edge
            log.debug(
                f'-{best_attrptlh * 3600:.1f}s/person/km'
                + f' ({network.format_edge(edge)})'
            )

    return best_edge


def build(network, max_network_length, max_segments):
    if network.n_edges >= max_segments:
        return network
    for i in range(0, MAX_STEPS):
        best_edge = optimize_step(network)

        if best_edge is None:
            log.warning('Could not optimize further.')
            break

        network_copy = network + [best_edge]

        att = network_copy.average_travel_time
        network_length = network_copy.network_length
        segments = network_copy.n_edges
        log.info(
            tab(
                f'{segments})',
                format_distance(network_length),
                format_time(att),
                network_copy.format_edge(best_edge),
            )
        )
        if any(
            [network_length >= max_network_length, segments >= max_segments]
        ):
            return network
        network = network_copy
    return network
