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
        max_network_length=2000,
        max_segments=100,
        max_distance=10000,
    ),
    dsd=dict(
        ent_type=EntType.DSD,
        max_network_length=1000,
        max_segments=100,
        max_distance=70,
    ),
    gnd=dict(
        ent_type=EntType.GND,
        max_network_length=2000,
        max_segments=20,
        max_distance=2,
    ),
)
CONFIG_IDX['district_3'] = CONFIG_IDX['district'] | dict(max_segments=3)


def is_close_enough(centroid, max_distance):
    distance = shape_utils.compute_distance(centroid, [6.91, 79.86])
    return distance < max_distance


def build_single(ent_type, max_network_length, max_segments, max_distance):
    network = Network.from_type(
        ent_type, lambda ent: is_close_enough(ent.centroid, max_distance)
    )
    network = step_optimizer.build(
        network,
        max_network_length=max_network_length,
        max_segments=max_segments,
    )

    draw = Draw(network, Styler())
    draw.draw(
        os.path.join(
            'media',
            f'rail_network.{ent_type.name}'
            + f'.{max_network_length}km.{max_segments}.png',
        )
    )


if __name__ == '__main__':
    config_key = 'dsd'
    build_single(*CONFIG_IDX[config_key].values())
