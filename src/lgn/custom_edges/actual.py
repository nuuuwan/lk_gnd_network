def expand(*node_list):
    edge_pair_list = []
    for i in range(len(node_list) - 1):
        edge_pair_list.append([node_list[i], node_list[i + 1]])
    return edge_pair_list


def rebuild_actual_districts(network):
    network.edge_pair_list = (
        expand(
            'Colombo',
            'Gampaha',
            'Kegalle',
            'Kandy',
            "Nuwara Eliya",
            "Badulla",
        )
        + expand('Colombo', 'Kalutara', "Galle", "Matara", "Hambantota")
        + expand('Gampaha', 'Puttalam')
        + expand(
            'Kegalle',
            'Kurunegala',
            'Anuradhapura',
            'Vavuniya',
            'Kilinochchi',
            'Jaffna',
        )
        + expand('Anuradhapura', 'Polonnaruwa', 'Batticaloa')
        + expand('Polonnaruwa', 'Trincomalee')
        + expand('Anuradhapura', 'Mannar')
        + expand('Kandy', 'Matale')
    )
    return network
