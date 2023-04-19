import time

from utils import Log

from lgn.utils.console_utils import print_line, tab
from lgn.utils.format_utils import format_distance, format_time
from lgn.utils.parallel_utils import map_parallel
from lgn.utils.shape_utils import compute_distance

log = Log('single_segments')

SPEED_TRAIN = 60
SPEED_WALK = 4


def compute_average_meet_time(network):
    if len(network.edge_pair_list) == 0:
        return 0
    sum_pop_times_meet_time = 0

    for node_i, node_j, distance in network.connected_node_pairs:
        population_i = network.node_idx[node_i]['population']
        population_j = network.node_idx[node_j]['population']

        distance_walking = compute_distance(
            network.node_idx[node_i]['centroid'],
            network.node_idx[node_j]['centroid'],
        )

        meet_time = distance / SPEED_TRAIN - distance_walking / SPEED_WALK
        pop = population_i * population_j
        sum_pop_times_meet_time += pop * meet_time

    average_meet_time = sum_pop_times_meet_time / network.total_people_pairs
    return average_meet_time


def get_d_per_distance_for_edge_pair(
    network_readonly, before_average_meet_time, edge_pair
):
    network = network_readonly.deepcopy()
    node_i, node_j = edge_pair

    if [node_i, node_j] in network.edge_pair_list or [
        node_j,
        node_i,
    ] in network.edge_pair_list:
        return None

    distance = compute_distance(
        network.node_idx[node_i]['centroid'],
        network.node_idx[node_j]['centroid'],
    )

    previous_edge_pair_list = network.edge_pair_list
    network.edge_pair_list = network.edge_pair_list + [edge_pair]
    average_meet_time = compute_average_meet_time(network)
    d_average_meet_time = before_average_meet_time - average_meet_time
    d_per_distance = d_average_meet_time / distance

    network.edge_pair_list = previous_edge_pair_list
    print(
        f'get_best_incr: {edge_pair} = {d_per_distance}' + ' ' * 20, end="\r"
    )
    return d_per_distance


def get_edge_pair_and_d_per_distance_list(
    network, before_average_meet_time, edge_pair_list
):
    t0 = time.time()
    MAX_THREADS = 4
    edge_pair_and_d_per_distance_list = map_parallel(
        lambda edge_pair: (
            edge_pair,
            get_d_per_distance_for_edge_pair(
                network, before_average_meet_time, edge_pair
            ),
        ),
        edge_pair_list,
        max_threads=MAX_THREADS,
    )
    dt = time.time() - t0
    n = len(edge_pair_list)
    dt_per_n = 1000.0 * dt / n
    log.debug(
        f'get_edge_pair_and_d_per_distance_list: {n:,} pairs in {dt:,.1f}s ({dt_per_n:,.1f}ms per pair)'
    )

    return edge_pair_and_d_per_distance_list


def get_best_incr(network):
    before_average_meet_time = compute_average_meet_time(network)

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
    n_nodes = len(network.node_list)
    log.debug(f'{n_nodes=}')
    while True:
        best_edge_pair = get_best_incr(network)
        network.edge_pair_list.append(best_edge_pair)
        average_meet_time = compute_average_meet_time(network)
        network_length = network.network_length
        n_segments = len(network.edge_pair_list)

        log.info(
            tab(
                f'rebuild_incr: { n_segments})',
                f'{format_time(average_meet_time)}',
                f'{format_distance(network_length)}',
                f'{best_edge_pair[0]} -> {best_edge_pair[1]}',
            )
        )
        print_line()

        if any(
            [network_length >= max_network_length, n_segments >= max_segments]
        ):
            break

    return network
