import svgpathtools
from utils import Log
from utils.xmlx import _

from lgn.utils import color_utils

log = Log(__name__)


class DrawLine:
    def draw_line(self, i_edge, n_edges, id1, id2, t):
        x1, y1 = self.network.node_idx[id1]['centroid']
        x2, y2 = self.network.node_idx[id2]['centroid']
        dx, dy = x2 - x1, y2 - y1

        min_dx_dy = min(abs(dx), abs(dy)) 
        dx1 = min_dx_dy * dx / abs(dx)
        dy1 = min_dx_dy * dy / abs(dy)

        x3, y3 = x1 + dx1, y1 + dy1


        sx1, sy1 = t(x1, y1)
        sx3, sy3 = t(x3, y3)
        sx2, sy2 = t(x2, y2)

        p = 1 - (i_edge + 1) / (n_edges)
        color = color_utils.p_to_color(p)

        d = ' '.join(
            [
                f'M {sx1} {sy1}',
                f'L {sx3} {sy3}',
                f'L {sx2} {sy2}',
            ]
        )
        path = svgpathtools.parse_path(d)
        smoothed_path = svgpathtools.smoothed_path(
            path, 
        )
        d = smoothed_path.d()

        return _(
            'path',
            None,
            self.styler.line
            | dict(
                d=d,
                stroke=color,
            ),
        )
