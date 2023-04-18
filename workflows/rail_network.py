from gig import EntType
from utils import Log

from lgn import Draw, Network, Styler
from lgn.custom_edges import single_segments
from lgn.utils import shape_utils

log = Log('rail_network')


def is_close_enough(centroid):
    distance = shape_utils.compute_distance(centroid, [6.92, 79.86])
    return distance < 1000


if __name__ == '__main__':
    network = Network.from_type(
        EntType.DISTRICT, lambda ent: is_close_enough(ent.centroid)
    )
    network = single_segments.rebuild_actual(network)

    average_meet_time_str = single_segments.format_time(
        single_segments.compute_average_meet_time(network)
    )
    network_length = network.network_length
    log.debug(f'{average_meet_time_str} {network_length:.1f}km')

    styler = Styler()
    draw = Draw(network, styler)
    draw.draw(f'workflow_media/rail_network.single_segments.rebuild_incr.png')
