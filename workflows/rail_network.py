from gig import EntType
from utils import Log

from lgn.core.network import Network
from lgn.custom_edges import single_segments
from lgn.render.draw import Draw
from lgn.render.styler import Styler
from lgn.utils import shape_utils

log = Log('rail_network')


def is_close_enough(centroid):
    distance = shape_utils.compute_distance(centroid, [6.91, 79.86])
    return distance < 2.5


def build_single():
    styler = Styler()
    max_network_length = 1048 * 2
    max_segments = 30

    network = Network.from_type(
        EntType.GND, lambda ent: is_close_enough(ent.centroid)
    )
    network.edge_pair_list = []
    network = single_segments.rebuild_incr(
        network,
        max_network_length=max_network_length,
        max_segments=max_segments,
    )

    draw = Draw(network, styler)
    draw.draw(f'workflow_media/rail_network.{max_segments}.png')


def build_animated_gif():
    styler = Styler()
    max_network_length = 1048 * 2

    network = Network.from_type(
        EntType.DISTRICT, lambda ent: is_close_enough(ent.centroid)
    )
    network.edge_pair_list = []
    png_path_list = []
    for max_segments in range(1, 51):
        network = single_segments.rebuild_incr(
            network,
            max_network_length=max_network_length,
            max_segments=max_segments,
        )

        draw = Draw(network, styler)
        png_path = draw.draw(
            f'workflow_media/rail_network.{max_segments:03d}.png',
            do_open=False,
        )
        png_path_list.append(png_path)

    gif_path = 'workflow_media/rail_network.single_segments.rebuild_incr.gif'
    Draw.build_animated_gif(png_path_list, gif_path)


if __name__ == '__main__':
    build_single()
