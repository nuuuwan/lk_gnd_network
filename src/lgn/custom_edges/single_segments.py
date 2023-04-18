from utils import Log
import random
from lgn.utils import shape_utils

log = Log('single_segments')

SPEED_TRAIN = 60
SPEED_WALK = 4


def format_time(t_hours_f):
    t_day = (int)(t_hours_f / 24)
    t_hours = (int)(t_hours_f % 24)
    t_minutes = (int)((t_hours_f % 1) * 60 + 0.5)

    if t_day > 0:
        return f'{t_day}d{t_hours}h{t_minutes}m'
    elif t_hours > 0:
        return f'{t_hours}h{t_minutes}m'
    else:
        return f'{t_minutes}m'


def compute_average_meet_time(network):
    node_list = network.node_list
    n = len(node_list)
    distance_matrix = network.distance_matrix
    # for node1, node2_to_dist in distance_matrix.items():
    #     for node2, dist in node2_to_dist.items():
    #         if dist != float('inf') and dist != 0:
    #             print(f'{dist:.2f}km {node1} - {node2}')
    # print('.' *32)

    sum_pop = 0
    sum_pop_times_meet_time = 0
    for i in range(n - 1):
        node_i = node_list[i]
        population_i = network.node_idx[node_i]['population']
        xi, yi = network.node_idx[node_i]['centroid']
        for j in range(i, n):
            node_j = node_list[j]
            population_j = network.node_idx[node_j]['population']
            xj, yj = network.node_idx[node_j]['centroid']

            distance = distance_matrix[node_i][node_j]

            if distance == float('inf'):
                distance = shape_utils.compute_distance((xi, yi), (xj, yj))
                meet_time = distance / SPEED_WALK
            else:
                meet_time = distance / SPEED_TRAIN

            pop = population_i * population_j
            # if node_i != node_j:
            #     log.debug(f'{pop * meet_time / 1000000000000:.4f}\t{pop / 1000000000000:.4f}\t{node_i} - {node_j}')

            sum_pop_times_meet_time += pop * meet_time
            sum_pop += pop

    average_meet_time = sum_pop_times_meet_time / sum_pop
    # log.debug(f'{sum_pop_times_meet_time / 1000000000000:.4f}\t{sum_pop / 1000000000000:.4f}\tSUM')
    return average_meet_time


def rebuild_greedy(network, n_segments):
    node_list = network.node_list
    n = len(node_list)

    score_list = []
    for i in range(n - 1):
        node_i = node_list[i]
        population_i = network.node_idx[node_i]['population']
        xi, yi = network.node_idx[node_i]['centroid']

        for j in range(i + 1, n):
            node_j = node_list[j]
            population_j = network.node_idx[node_j]['population']
            xj, yj = network.node_idx[node_j]['centroid']

            distance = shape_utils.compute_distance((xi, yi), (xj, yj))
            score = (population_i * population_j) / distance

            score_list.append([score, node_i, node_j])

    score_list_sorted = sorted(score_list, key=lambda x: x[0], reverse=True)
    edge_pair_list = []
    for i in range(0, n_segments):
        score, node_i, node_j = score_list_sorted[i]
        edge_pair_list.append([node_i, node_j])

    network.edge_pair_list = edge_pair_list
    average_meet_time = compute_average_meet_time(network)
    log.info(f'average_meet_time = {format_time(average_meet_time)}')
    return network


def rebuild_random(network, n_segments):
    edge_pair_list = []
    for i in range(n_segments):
        edge_pair_list.append(random.choice(network.edge_pair_list))
    network.edge_pair_list = edge_pair_list
    average_meet_time = compute_average_meet_time(network)
    log.info(f'average_meet_time = {format_time(average_meet_time)}')
    return network


def get_best_incr(network):
    before_average_meet_time = compute_average_meet_time(network)
    node_list = network.node_list
    n = len(node_list)
    best_d_per_distance = 0
    best_edge_pair = None
    for i in range(n - 1):
        node_i = node_list[i]
        for j in range(i + 1, n):
            node_j = node_list[j]
            edge_pair = [node_i, node_j]
            if edge_pair in network.edge_pair_list:
                continue
            distance = shape_utils.compute_distance(
                network.node_idx[node_i]['centroid'],
                network.node_idx[node_j]['centroid'],
            )
            previous_edge_pair_list = network.edge_pair_list
            network.edge_pair_list = network.edge_pair_list + [edge_pair]
            average_meet_time = compute_average_meet_time(network)
            d_average_meet_time = before_average_meet_time - average_meet_time
            d_per_distance = d_average_meet_time / distance

            if d_per_distance > best_d_per_distance:
                best_d_per_distance = d_per_distance
                best_edge_pair = edge_pair

            network.edge_pair_list = previous_edge_pair_list

    return best_edge_pair


def rebuild_incr(network, n_segments):
    network.edge_pair_list = []
    prev_network_length = 0
    prev_average_meet_time = compute_average_meet_time(network)
    for i_segment in range(n_segments):
        best_edge_pair = get_best_incr(network)
        network.edge_pair_list.append(best_edge_pair)
        average_meet_time = compute_average_meet_time(network)
        network_length = network.network_length

        d_network_length = network_length - prev_network_length
        d_average_meet_time = prev_average_meet_time - average_meet_time
        reduction = 60 * d_average_meet_time / d_network_length

        log.debug(
            f'rebuild_incr: { i_segment + 1}/{n_segments} {format_time(average_meet_time)} {network_length:.1f}km {reduction:.1f}min/km {best_edge_pair}'
        )

        prev_network_length = network_length
        prev_average_meet_time = average_meet_time

    average_meet_time = compute_average_meet_time(network)
    log.info(f'average_meet_time = {format_time(average_meet_time)}')
    return network


def expand(*node_list):
    edge_pair_list = []
    for i in range(len(node_list) - 1):
        edge_pair_list.append([node_list[i], node_list[i + 1]])
    return edge_pair_list


def rebuild_actual(network):
    network.edge_pair_list = expand(
        'Colombo', 'Gampaha', 'Kegalle', 'Kandy', "Nuwara Eliya", "Badulla"
    ) + expand('Colombo', 'Kalutara', "Galle", "Matara", "Hambantota")
    return network
