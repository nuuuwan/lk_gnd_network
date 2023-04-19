import os

from gig import EntType
from utils import Log

from lgn.core.network import Network
from lgn.custom_edges import single_segments
from lgn.render.draw import Draw
from lgn.render.styler import Styler
from lgn.utils import shape_utils

log = Log('rail_network')


def is_close_enough(centroid, max_distance):
    distance = shape_utils.compute_distance(centroid, [6.91, 79.86])
    return distance < max_distance


def build_single():
    ent_type = EntType.DSD
    max_network_length = 1048 * 1.5
    max_segments = 30
    max_distance = 100

    network = Network.from_type(
        ent_type, lambda ent: is_close_enough(ent.centroid, max_distance)
    )
    network = single_segments.rebuild_incr(
        network,
        max_network_length=max_network_length,
        max_segments=max_segments,
    )

    draw = Draw(network, Styler())
    draw.draw(
        os.path.join(
            'media',
            f'rail_network.{ent_type.name}.{max_distance}km.{max_segments}.png',
        )
    )


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
            f'media/rail_network.{max_segments:03d}.png',
            do_open=False,
        )
        png_path_list.append(png_path)

    gif_path = 'media/rail_network.single_segments.rebuild_incr.gif'
    Draw.build_animated_gif(png_path_list, gif_path)


if __name__ == '__main__':
    build_single()
