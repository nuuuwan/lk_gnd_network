from utils import Log
from utils.xmlx import _

from lgn.utils import color_utils

log = Log(__name__)


class DrawLine:
    def draw_line(self, i_edge, n_edges, id1, id2, t):
        x1, y1 = self.network.node_idx[id1]['centroid']
        x2, y2 = self.network.node_idx[id2]['centroid']
        sx1, sy1 = t(x1, y1)
        sx2, sy2 = t(x2, y2)

        p = 1 - i_edge / (n_edges - 1)
        color = color_utils.p_to_color(p)

        return _(
            'line',
            None,
            self.styler.line
            | dict(
                x1=sx1,
                y1=sy1,
                x2=sx2,
                y2=sy2,
                stroke=color,
            ),
        )
