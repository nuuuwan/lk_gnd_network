from gig import EntType

from lgn import Draw, Network, Styler

if __name__ == '__main__':
    network = Network.from_type(EntType.DISTRICT)
    styler = Styler()
    draw = Draw(network, styler)
    draw.draw('workflow_media/region.png')
