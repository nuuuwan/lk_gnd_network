import time

import numpy as np
from utils import Log

from lgn.utils.console_utils import print_line, tab
from lgn.utils.format_utils import format_distance, format_time
from lgn.utils.parallel_utils import map_parallel

log = Log('single_segments')

SPEED_TRAIN = 60
SPEED_WALK = 4




def get_d_per_distance_for_edge_pair(
    network, before_average_travel_time, edge_pair, distance
):
    node_i, node_j = edge_pair
    if network.is_edge(node_i, node_j):
        return None

    network_copy = network + [edge_pair]
    average_travel_time = network_copy.average_travel_time
    d_average_travel_time = before_average_travel_time - average_travel_time
    d_per_distance = d_average_travel_time / distance
    return d_per_distance


def get_edge_pair_and_d_per_distance_list(
    network, before_average_travel_time, close_node_pairs_and_distance_list
):
    t0 = time.time()
    MAX_THREADS = 8

    def func_worker(x):
        edge_pair, distance = x
        d_per_distance = get_d_per_distance_for_edge_pair(
            network, before_average_travel_time, edge_pair, distance
        )
        return edge_pair, d_per_distance

    edge_pair_and_d_per_distance_list = map_parallel(
        func_worker,
        close_node_pairs_and_distance_list,
        max_threads=MAX_THREADS,
    )
   
    print()
    dt = time.time() - t0
    n = len(close_node_pairs_and_distance_list)
    dt_per_n = 1000.0 * dt / n
    log.debug(f'{n:,} pairs in {dt:,.1f}s ({dt_per_n:,.1f}ms per pair)')

    return edge_pair_and_d_per_distance_list


def get_best_incr(network):
    before_average_travel_time = network.average_travel_time

    best_d_per_distance = -float('inf')
    best_edge_pair = None

    max_distance = 15
    edge_pair_and_d_per_distance_list = get_edge_pair_and_d_per_distance_list(
        network, before_average_travel_time, network.get_close_node_pairs_and_distance_list(max_distance)
    )

    for edge_pair, d_per_distance in edge_pair_and_d_per_distance_list:
        if d_per_distance is None:
            continue

        if d_per_distance > best_d_per_distance:
            best_d_per_distance = d_per_distance
            best_edge_pair = edge_pair

    return best_edge_pair


def rebuild_incr(network, max_network_length, max_segments):
    n_nodes = network.n_nodes
    log.debug(f'{n_nodes=}')
    while True:
        best_edge_pair = get_best_incr(network)
        network = network + [best_edge_pair]
        average_travel_time = network.average_travel_time
        network_length = network.network_length
        n_segments = network.n_edges

        log.info(
            tab(
                f'rebuild_incr: { n_segments})',
                f'{format_time(average_travel_time)}',
                f'{format_distance(network_length)}',
                f'{network.format_edge(best_edge_pair)}',
            )
        )
        print_line()

        if any(
            [network_length >= max_network_length, n_segments >= max_segments]
        ):
            break

    return network
