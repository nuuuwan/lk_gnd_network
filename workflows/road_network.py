from gig import EntType

from lgn import Draw, Network, Styler
from lgn.custom_edges import road_network

if __name__ == '__main__':
    network = Network.from_type(EntType.DSD)
    network = road_network.rebuild(network)

    styler = Styler()
    draw = Draw(network, styler)
    draw.draw('workflow_media/region.png')
