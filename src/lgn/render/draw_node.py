import math

from utils import Log
from utils.xmlx import _

log = Log(__name__)


class DrawNode:
    def draw_node_circle(self, sx, sy, n_neighbors):
        return _(
            'circle',
            None,
            self.styler.node_circle
            | dict(
                cx=sx,
                cy=sy,
                r=self.styler.RADIUS * math.sqrt(n_neighbors + 1),
            ),
        )

    def draw_node_text(self, label, sx, sy, n_neighbors):
        font_size = (
            min(1, (n_neighbors + 1) / 3) * self.styler.node_text['font_size']
        )
        fill = 'black' if n_neighbors > 1 else 'gray'
        return _(
            'text',
            label,
            self.styler.node_text
            | dict(
                font_size=font_size,
                x=sx + self.styler.RADIUS + font_size / 2,
                y=sy,
                fill=fill,
            ),
        )

    def draw_node(self, label, x, y, t, n_neighbors):
        sx, sy = t(x, y)
        if n_neighbors == 0:
            return None
        return _(
            'g',
            [
                self.draw_node_circle(sx, sy, n_neighbors),
                self.draw_node_text(label, sx, sy, n_neighbors),
            ],
        )
