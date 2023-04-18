from utils import Log
from utils.xmlx import _

log = Log(__name__)


class DrawNode:
    def draw_node_circle(self, sx, sy, is_junction):
        if not is_junction:
            return _('g')
        
        return _(
            'circle',
            None,
            self.styler.node_circle
            | dict(
                cx=sx,
                cy=sy,
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

    def draw_node(self, id, x, y, t, is_junction):
        sx, sy = t(x, y)
        return _(
            'g',
            [
                self.draw_node_circle(sx, sy, c),
                self.draw_node_text(id, sx, sy),
            ],
        )
