import time

from utils import Log

from lgn.utils.console_utils import print_line, tab
from lgn.utils.format_utils import format_distance, format_time
from lgn.utils.parallel_utils import map_parallel

log = Log('single_segments')

SPEED_TRAIN = 60
SPEED_WALK = 4


def compute_average_meet_time_delta(network):
    if network.n_edges == 0:
        return 0
    sum_pop_times_meet_time = 0

    for [node_i, node_j], distance in network.connected_node_pairs:
        population_i = network.get_node(node_i).population
        population_j = network.get_node(node_j).population

        distance_walking = network.get_distance(node_i, node_j)
        meet_time = distance / SPEED_TRAIN - distance_walking / SPEED_WALK
        pop = population_i * population_j
        sum_pop_times_meet_time += pop * meet_time

    average_meet_time = sum_pop_times_meet_time / network.total_people_pairs
    return average_meet_time


def get_d_per_distance_for_edge_pair(
    network, before_average_meet_time, edge_pair
):
    node_i, node_j = edge_pair
    if network.is_edge(node_i, node_j):
        return None

    distance = network.get_distance(node_i, node_j)
    network_copy = network + [edge_pair]
    average_meet_time = compute_average_meet_time_delta(network_copy)
    d_average_meet_time = before_average_meet_time - average_meet_time
    d_per_distance = d_average_meet_time / distance
    return d_per_distance


def get_edge_pair_and_d_per_distance_list(
    network, before_average_meet_time, edge_pair_list
):
    t0 = time.time()
    MAX_THREADS = 4

    def func_worker(edge_pair):
        d_per_distance = get_d_per_distance_for_edge_pair(
            network, before_average_meet_time, edge_pair
        )
        return edge_pair, d_per_distance

    edge_pair_and_d_per_distance_list = map_parallel(
        func_worker,
        edge_pair_list,
        max_threads=MAX_THREADS,
    )
    print()
    dt = time.time() - t0
    n = len(edge_pair_list)
    dt_per_n = 1000.0 * dt / n
    log.debug(f'{n:,} pairs in {dt:,.1f}s ({dt_per_n:,.1f}ms per pair)')

    return edge_pair_and_d_per_distance_list


def get_best_incr(network):
    before_average_meet_time = compute_average_meet_time_delta(network)

    best_d_per_distance = -float('inf')
    best_edge_pair = None

    edge_pair_and_d_per_distance_list = get_edge_pair_and_d_per_distance_list(
        network, before_average_meet_time, network.all_node_pairs
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
        average_meet_time = compute_average_meet_time_delta(network)
        network_length = network.network_length
        n_segments = network.n_edges

        log.info(
            tab(
                f'rebuild_incr: { n_segments})',
                f'{format_time(average_meet_time)}',
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
