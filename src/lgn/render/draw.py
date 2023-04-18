import os
import webbrowser
from functools import cache

from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
from utils import Log
from utils.xmlx import _

from lgn.utils import shape_utils
from lgn.render.draw_line import DrawLine
from lgn.render.draw_node import DrawNode

log = Log(__name__)


class Draw(DrawNode, DrawLine):
    def __init__(self, network, styler):
        self.network = network
        self.styler = styler

    @cache
    def get_t(self):
        return shape_utils.get_t(self.styler, self.network.loc_list)

    def draw_nodes(self):
        t = self.get_t()
        junction_set = self.network.junction_set
        nodes = []
        for id, node in self.network.node_idx.items():
            x, y = node['centroid']
            is_junction = id in junction_set
            nodes.append(self.draw_node(id, x, y, t, is_junction))
        return nodes

    def draw_lines(self):
        t = self.get_t()
        lines = []
        for id1, id2 in self.network.edge_pair_list:
            lines.append(self.draw_line(id1, id2, t))
        return lines

    def draw(self, png_path, do_open=True):
        svg = _(
            'svg',
            self.draw_lines() + self.draw_nodes(),
            self.styler.svg,
        )
        svg_path = png_path[:-3] + 'svg'
        svg.store(svg_path)
        log.debug(f'Saved {svg_path}')

        png_path = Draw.convert_svg_to_png(svg_path)
        if do_open:
            webbrowser.open(os.path.abspath(png_path))
        return png_path

    @staticmethod
    def convert_svg_to_png(svg_path):
        png_path = svg_path[:-3] + 'png'

        drawing = svg2rlg(svg_path)
        renderPM.drawToFile(drawing, png_path, fmt="PNG")
        log.info(f'Saved {png_path}')

        return png_path
