import os
import webbrowser
from functools import cache

import imageio
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
from utils import Log
from utils.xmlx import _

from lgn.render.draw_line import DrawLine
from lgn.render.draw_node import DrawNode
from lgn.utils import shape_utils
from lgn.utils.color_utils import p_to_color
from lgn.utils.format_utils import format_distance, format_time

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
        neighbor_idx = self.network.neighbor_idx
        nodes = []
        for node in self.network.node_list:
            x, y = node.centroid
            n_neighbors = len(neighbor_idx.get(node.i, []))
            nodes.append(self.draw_node(node.name, x, y, t, n_neighbors))
        return nodes

    def draw_lines(self):
        t = self.get_t()
        lines = []
        n_edges = self.network.n_edges
        for i_edge, [id1, id2] in enumerate(reversed(self.network.edge_list)):
            lines.append(self.draw_line(i_edge, n_edges, id1, id2, t))
        return lines

    def draw_text(self):
        return [
            _('text', 'Sri Lanka', self.styler.text_supertitle),
            _(
                'text',
                'Population Optimized Hypothetical Railway Network',
                self.styler.text_title,
            ),
            _(
                'text',
                'music by @bensound ~ visualization by @nuuuwan',
                self.styler.text_footer,
            ),
            _(
                'text',
                'Network Length',
                self.styler.text_network_length
                | dict(
                    y=self.styler.text_network_length['y']
                    - self.styler.text_network_length['font_size'],
                    font_size=self.styler.text_network_length['font_size']
                    * 0.5,
                ),
            ),
            _(
                'text',
                format_distance(self.network.network_length),
                self.styler.text_network_length,
            ),
            _(
                'text',
                'Mean Travel Time',
                self.styler.text_network_att
                | dict(
                    y=self.styler.text_network_att['y']
                    - self.styler.text_network_att['font_size'],
                    font_size=self.styler.text_network_att['font_size'] * 0.5,
                ),
            ),
            _(
                'text',
                format_time(self.network.average_travel_time),
                self.styler.text_network_att,
            ),
        ]

    def draw_legend(self):
        inner_list = []
        P_LIST = [i / 10 for i in range(0, 7 + 1)]
        style = self.styler.legend_circle
        for i, p in enumerate(P_LIST):
            if i == 0:
                label = 'Highest Priority'
            elif i == len(P_LIST) - 1:
                label = 'Lowest Priority'
            else:
                label = ''

            color = p_to_color(p)
            cy = style['cy_offset'] + i * style['r'] * 2
            inner_list.append(
                _(
                    'circle',
                    '',
                    style | dict(cy=cy, fill=color),
                )
            )
            inner_list.append(
                _(
                    'text',
                    label,
                    self.styler.node_text
                    | dict(x=style['cx'] + style['r'] * 2.2, y=cy),
                )
            )
        return _('g', inner_list)

    def draw(self, png_path, do_open=True):
        svg = _(
            'svg',
            [self.draw_legend()]
            + self.draw_text()
            + self.draw_lines()
            + self.draw_nodes(),
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

    @staticmethod
    def build_animated_gif(png_path_list, gif_path):
        png_path_list.sort()
        last_png_path = png_path_list[-1]
        for i in range(0, 5):
            png_path_list.append(last_png_path)

        images = []
        for png_path in png_path_list:
            images.append(imageio.imread(png_path))
        DURATION = 55.70 / 24
        imageio.mimwrite(gif_path, images, duration=DURATION)
        log.info(f'Built {gif_path} (from {len(png_path_list)} png files)')
        webbrowser.open(os.path.abspath(gif_path))
