from gig import EntType

from lgn import Draw, Network, Styler
from lgn.custom_edges import single_segments

def is_close_enough(centroid):
    x1, y1 = centroid
    x2, y2 = [6.92, 79.86]
    distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return distance < 10

if __name__ == '__main__':
    network = Network.from_type(EntType.DISTRICT, lambda ent: is_close_enough(ent.centroid))
    network = single_segments.rebuild(network, n_segments=60)

    styler = Styler()
    draw = Draw(network, styler)
    draw.draw('workflow_media/region.png')
