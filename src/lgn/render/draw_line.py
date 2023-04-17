import svgpathtools
from utils import Log
from utils.xmlx import _

log = Log(__name__)


class DrawLine:

    def draw_line(self, id1, id2, t):
        x1, y1 = self.network.node_idx[id1]['centroid']
        x2, y2 = self.network.node_idx[id2]['centroid']
        sx1, sy1 = t(x1, y1)
        sx2, sy2 = t(x2, y2)
        return _(
            'line',
            None,
            dict(
                x1=sx1,
                y1=sy1,
                x2=sx2,
                y2=sy2,

            ) | self.styler.line,
        )
