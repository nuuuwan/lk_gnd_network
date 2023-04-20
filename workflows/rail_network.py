import os

from gig import EntType
from utils import Log

from lgn.core.network import Network
from lgn.custom_edges import step_optimizer
from lgn.render.draw import Draw
from lgn.render.styler import Styler
from lgn.utils import shape_utils

log = Log('rail_network')


CONFIG_IDX = dict(
    district=dict(
        ent_type=EntType.DISTRICT,
        max_network_length=4000,
        max_segments=60,
        max_distance=10000,
        max_inter_node_distance=200,
    ),
    dsd=dict(
        ent_type=EntType.DSD,
        max_network_length=500,
        max_segments=50,
        max_distance=60,
        max_inter_node_distance=15,
    ),
    gnd=dict(
        ent_type=EntType.GND,
        max_network_length=2000,
        max_segments=20,
        max_distance=2,
        max_inter_node_distance=2,
    ),
)
CONFIG_IDX['district_0'] = CONFIG_IDX['district'] | dict(max_segments=0)
CONFIG_IDX['district_3'] = CONFIG_IDX['district'] | dict(max_segments=10)
CONFIG_IDX['dsd_0'] = CONFIG_IDX['district_0'] | dict(ent_type=EntType.DSD)
CONFIG_IDX['gnd_0'] = CONFIG_IDX['district_0'] | dict(ent_type=EntType.GND)


def is_close_enough(centroid, max_distance):
    distance = shape_utils.compute_distance(centroid, [6.91, 79.86])
    return distance < max_distance


def _init_network(ent_type, max_distance):
    return Network.from_type(
        ent_type, lambda ent: is_close_enough(ent.centroid, max_distance)
    )


def _build_helper(
    ent_type,
    max_network_length,
    max_segments,
    max_distance,
    max_inter_node_distance,
    network,
):
    network = step_optimizer.build(
        network,
        max_network_length=max_network_length,
        max_segments=max_segments,
        max_inter_node_distance=max_inter_node_distance,
    )

    draw = Draw(network, Styler())
    png_path = os.path.join(
        'media',
        f'rail_network.{ent_type.name}',
        f'{max_segments}.png',
    )
    draw.draw(png_path, do_open=max_segments % 10 == 0)

    return png_path, network


def build_single(
    ent_type,
    max_network_length,
    max_segments,
    max_distance,
    max_inter_node_distance,
):
    network = _init_network(ent_type, max_distance)
    return _build_helper(
        ent_type,
        max_network_length,
        max_segments,
        max_distance,
        max_inter_node_distance,
        network,
    )


def build_multiple(
    ent_type,
    max_network_length,
    max_segments,
    max_distance,
    max_inter_node_distance,
):
    network = _init_network(ent_type, max_distance)
    png_path_list = []
    for max_segments_i in range(0, max_segments + 1):
        png_path, network = _build_helper(
            ent_type,
            max_network_length,
            max_segments_i,
            max_distance,
            max_inter_node_distance,
            network,
        )
        png_path_list.append(png_path)

    gif_path = os.path.join(
        'media',
        f'rail_network.{ent_type.name}',
        'TIMELINE.gif',
    )

    Draw.build_animated_gif(png_path_list, gif_path)


if __name__ == '__main__':
    config_key = 'district_3'
    build_multiple(*CONFIG_IDX[config_key].values())
