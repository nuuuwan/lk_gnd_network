import os
import tempfile
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
        i_phase = self.network.n_edges
        return [
            _(
                'text',
                'Hypothetical Railway Network',
                self.styler.text_supertitle,
            ),
            _(
                'text',
                f'Phase {i_phase}',
                self.styler.text_title,
            ),
            _(
                'text',
                'music by @bensound ~ visualization by @nuuuwan',
                self.styler.text_footer,
            ),
        ]

    def draw_info_item(self, label, value, style):
        if value is None:
            return []
        return [
            _(
                'text',
                label,
                style
                | dict(
                    y=style['y'] - style['font_size'],
                    font_size=style['font_size'] * 0.5,
                ),
            ),
            _(
                'text',
                value,
                style,
            ),
        ]

    def draw_info(self):
        BASE_MTT = 29.379542492563075
        mttpkm_str = None
        if self.network.network_length > 0:
            mttpkm = (
                3_600
                * (BASE_MTT - self.network.average_travel_time)
                / self.network.network_length
            )
            mttpkm_str = f'{mttpkm:,.0f}s/km'

        item_list = []
        for label, value, style in [
            [
                'Network Length',
                format_distance(self.network.network_length),
                self.styler.text_network_length,
            ],
            [
                'Mean Travel Time (MTT)',
                format_time(self.network.average_travel_time),
                self.styler.text_network_att,
            ],
            [
                'MTT Reduction / Track Length',
                mttpkm_str,
                self.styler.text_network_mttpkm,
            ],
        ]:
            item_list += self.draw_info_item(label, value, style)
        return item_list

    def draw_legend(self):
        inner_list = []
        N_LEGEND = 5
        P_LIST = [i / N_LEGEND for i in range(0, N_LEGEND + 1)]
        style = self.styler.legend_circle
        for i, p in enumerate(P_LIST):
            if i == 0:
                label = 'Ealier'
            elif i == len(P_LIST) - 1:
                label = 'Later'
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
                    | dict(
                        x=style['cx'] + style['r'] * 2.2,
                        y=cy + style['r'] / 2,
                    ),
                )
            )
        return _('g', inner_list)

    def draw(self, png_path, do_open=True):
        svg = _(
            'svg',
            [self.draw_legend()]
            + self.draw_text()
            + self.draw_info()
            + self.draw_lines()
            + self.draw_nodes(),
            self.styler.svg,
        )
        svg_path = tempfile.NamedTemporaryFile(
            prefix='lgn.', suffix='.svg'
        ).name
        svg.store(svg_path)
        log.debug(f'Saved {svg_path}')

        Draw.convert_svg_to_png(svg_path, png_path)
        if do_open:
            webbrowser.open(os.path.abspath(png_path))

    @staticmethod
    def convert_svg_to_png(svg_path, png_path):
        drawing = svg2rlg(svg_path)
        renderPM.drawToFile(drawing, png_path, fmt="PNG")
        log.info(f'Saved {png_path}')

    @staticmethod
    def build_animated_gif(png_path_list, gif_path):
        images = []
        for png_path in png_path_list:
            images.append(imageio.imread(png_path))
        DURATION = 55.70 / 48
        imageio.mimwrite(gif_path, images, duration=DURATION)
        log.info(f'Built {gif_path} (from {len(png_path_list)} png files)')
        webbrowser.open(os.path.abspath(gif_path))
