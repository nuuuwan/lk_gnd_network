from utils import Log

log = Log('single_segments')


def rebuild(network, n_segments):
    node_list = network.node_list
    n = len(node_list)

    score_list = []
    for i in range(n-1):
        node_i = node_list[i]
        population_i = network.node_idx[node_i]['population']
        xi, yi = network.node_idx[node_i]['centroid']

        for j in range(i+1, n):
            node_j = node_list[j]
            population_j = network.node_idx[node_j]['population']
            xj, yj = network.node_idx[node_j]['centroid']

            distance = ((xi - xj) ** 2 + (yi - yj) ** 2) ** 0.5
            score = (population_i * population_j) / distance 
            
            score_list.append([score, node_i, node_j])


    score_list_sorted = sorted(score_list, key=lambda x: x[0], reverse=True)
    edge_pair_list = []
    for i in range(0, n_segments):
        score, node_i, node_j = score_list_sorted[i]
        edge_pair_list.append([node_i, node_j])

    network.edge_pair_list = edge_pair_list
    return network