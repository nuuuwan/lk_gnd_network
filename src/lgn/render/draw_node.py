import math

from utils import Log
from utils.xmlx import _

log = Log(__name__)


class DrawNode:
    def draw_node_circle(self, sx, sy, n_neighbors):
        if n_neighbors in [0, 2]:
            return None
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
        fill = self.styler.node_text['fill']
        if n_neighbors in [0, 2]:
            fill = 'lightgrey'
        k_font_size = 0.75
        if n_neighbors in [0,2]:
            k_font_size = 0.5
        if n_neighbors > 2:
            k_font_size = 1
        
        font_size=k_font_size * self.styler.node_text['font_size']
        return _(
            'text',
            label,
            self.styler.node_text
            | dict(
                font_size=font_size,
                x=sx + self.styler.RADIUS  +  font_size,
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
