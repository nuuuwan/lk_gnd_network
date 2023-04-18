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
                r=self.styler.RADIUS * (n_neighbors + 1),
            ),
        )

    def draw_node_text(self, id, sx, sy):
        return _(
            'text',
            id,
            self.styler.node_text
            | dict(
                x=sx + self.styler.RADIUS * 2,
                y=sy,
            ),
        )

    def draw_node(self, id, x, y, t, n_neighbors):
        sx, sy = t(x, y)
        return _(
            'g',
            [
                self.draw_node_circle(sx, sy, n_neighbors),
                self.draw_node_text(id, sx, sy),
            ],
        )
