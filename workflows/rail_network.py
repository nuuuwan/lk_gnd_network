from gig import EntType
from utils import Log

from lgn.core.network import Network
from lgn.custom_edges import single_segments
from lgn.render.draw import Draw
from lgn.render.styler import Styler
from lgn.utils import shape_utils

log = Log('rail_network')


def is_close_enough(centroid):
    distance = shape_utils.compute_distance(centroid, [6.92, 79.86])
    return distance < 40


if __name__ == '__main__':
    network = Network.from_type(
        EntType.DSD,
        lambda ent: is_close_enough(ent.centroid)
        # and ent.id in ['LK-11', 'LK-12', 'LK-13', 'LK-61', 'LK-21', 'LK-31']
    )

    # network = single_segments.rebuild_actual(network)
    # styler = Styler()
    # draw = Draw(network, styler)
    # draw.draw(f'workflow_media/rail_network.single_segments.rebuild_actual.png')

    #

    network = single_segments.rebuild_incr(network, max_network_length=100)

    average_meet_time_str = single_segments.format_time(
        single_segments.compute_average_meet_time(network)
    )
    network_length = network.network_length
    log.debug(f'{average_meet_time_str} {network_length:.1f}km')

    styler = Styler()
    draw = Draw(network, styler)
    draw.draw('workflow_media/rail_network.single_segments.rebuild_incr.png')
