import svgpathtools
from utils import Log
from utils.xmlx import _

from lgn.utils import color_utils

log = Log('draw_line')


def elaborate_path(x1, y1, x2, y2, t):
    dx, dy = x2 - x1, y2 - y1

    min_dx_dy = min(abs(dx), abs(dy)) / 2
    dx1 = min_dx_dy * dx / abs(dx)
    dy1 = min_dx_dy * dy / abs(dy)

    x3, y3 = x1 + dx1, y1 + dy1
    x4, y4 = x2 - dx1, y2 - dy1

    sx1, sy1 = t(x1, y1)
    sx3, sy3 = t(x3, y3)
    sx4, sy4 = t(x4, y4)
    sx2, sy2 = t(x2, y2)

    d_list = []
    d_list.append(f'M {sx1} {sy1}')

    if (sx1, sy1) != (sx3, sy3):
        d_list.append(f'L {sx3} {sy3}')

    if (sx3, sy3) != (sx4, sy4) and (sx4, sy4) != (sx2, sy2):
        d_list.append(f'L {sx4} {sy4}')

    d_list.append(f'L {sx2} {sy2}')

    d = ' '.join(d_list)
    return d


def smooth_path(d):
    try:
        path = svgpathtools.parse_path(d)
        smoothed_path = svgpathtools.smoothed_path(
            path,
        )
        return smoothed_path.d()
    except BaseException:
        log.error(f'Failed to smooth path: {d}')
        return d


class DrawLine:
    def draw_line(self, i_edge, n_edges, id1, id2, t):
        x1, y1 = self.network.get_node(id1).centroid
        x2, y2 = self.network.get_node(id2).centroid

        d = elaborate_path(x1, y1, x2, y2, t)
        smoothed_d = smooth_path(d)

        p = 1 - (i_edge + 1) / (n_edges)
        color = color_utils.p_to_color(p)

        return _(
            'path',
            None,
            self.styler.line
            | dict(
                d=smoothed_d,
                stroke=color,
            ),
        )
