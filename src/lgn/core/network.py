from utils import Log

from lgn.core.network_base import NetworkBase
from lgn.core.network_derived import NetworkDerived
from lgn.core.network_vector import NetworkVector

log = Log('network')


class Network(NetworkBase, NetworkVector, NetworkDerived):
    pass


if __name__ == '__main__':
    from gig import EntType

    from lgn.utils.console_utils import print_line

    network = Network.from_type(EntType.PROVINCE)
    print(network)
    print(network.loc_list)
    network = network + [(0, 2), (0, 5)]
    print(network)

    print(network.neighbor_idx)
    print_line()
    print(network.edge_dist_matrix)
    print_line()
    print(network.dist_matrix)
    print_line()
    print(network.network_length)

    print_line()
    print(network.total_population)
    print(network.total_people_pairs)
    print(network.all_node_pairs)

    print(network.connected_node_pairs)

    print(network + [(0, 8)])
