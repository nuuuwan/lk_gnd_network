from utils import Log

from lgn.utils import shape_utils
from lgn.utils.console_utils import print_line, tab

log = Log('single_segments')

SPEED_TRAIN = 60
SPEED_WALK = 4


def format_time(t_hours_f):
    if t_hours_f < 0:
        return '-' + format_time(-t_hours_f)

    (int)(t_hours_f / 24)
    t_hours = (int)(t_hours_f % 24)
    t_minutes = (int)((t_hours_f % 1) * 60 + 0.5)

    if t_hours > 0:
        return f'{t_hours}h{t_minutes}m'

    return f'{t_minutes}m'


def compute_average_meet_time(network):
    # print('...')
    if len(network.edge_pair_list) == 0:
        return 0
    # print(network.edge_pair_list)

    distance_matrix = network.distance_matrix
    #  print('-' * 32)
    #  print(network.edge_pair_list)
    #  print()
    #  print(distance_matrix)
    sum_pop_times_meet_time = 0
    for node_i, node_j_to_dist in distance_matrix.items():
        for node_j, distance in node_j_to_dist.items():
            if node_i >= node_j:
                continue

            population_i = network.node_idx[node_i]['population']
            population_j = network.node_idx[node_j]['population']

            distance_walking = shape_utils.compute_distance(
                network.node_idx[node_i]['centroid'],
                network.node_idx[node_j]['centroid'],
            )

            meet_time = distance / SPEED_TRAIN - distance_walking / SPEED_WALK
            pop = population_i * population_j
            sum_pop_times_meet_time += pop * meet_time

    average_meet_time = sum_pop_times_meet_time / network.total_people_pairs
    return average_meet_time


def get_fitness_for_edge_pair(network, edge_pair, before_average_meet_time):
    node_i, node_j = edge_pair
    if [node_i, node_j] in network.edge_pair_list or [
        node_j,
        node_i,
    ] in network.edge_pair_list:
        return None

    distance = shape_utils.compute_distance(
        network.node_idx[node_i]['centroid'],
        network.node_idx[node_j]['centroid'],
    )

    previous_edge_pair_list = network.edge_pair_list
    network.edge_pair_list = network.edge_pair_list + [edge_pair]
    average_meet_time = compute_average_meet_time(network)
    d_average_meet_time = before_average_meet_time - average_meet_time
    d_per_distance = d_average_meet_time / distance

    network.edge_pair_list = previous_edge_pair_list
    return d_per_distance


def get_best_incr(network):
    before_average_meet_time = compute_average_meet_time(network)
    node_list = network.node_list
    n = len(node_list)
    best_d_per_distance = -float('inf')
    best_edge_pair = None
    for i in range(n - 1):
        node_i = node_list[i]
        for j in range(i + 1, n):
            node_j = node_list[j]
            edge_pair = [node_i, node_j]

            d_per_distance = get_fitness_for_edge_pair(
                network, edge_pair, before_average_meet_time
            )
            if d_per_distance is None:
                continue

            if d_per_distance > best_d_per_distance:
                best_d_per_distance = d_per_distance
                best_edge_pair = edge_pair

    return best_edge_pair


def rebuild_incr(network, max_network_length, max_segments):
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
                f'{network_length:.1f}km',
                f'{best_edge_pair[0]} -> {best_edge_pair[1]}',
            )
        )
        print_line()

        if network_length >= max_network_length:
            break
        if n_segments >= max_segments:
            break

    return network
