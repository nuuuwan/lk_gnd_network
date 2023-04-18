from functools import cached_property

import svglib.svglib as svglib

DEFAULT_FONT_FAMILY = 'p22'
DEFAULT_FONT_PATH = f'C:\\Windows\\Fonts\\{DEFAULT_FONT_FAMILY}.ttf'


svglib.register_font(
    DEFAULT_FONT_FAMILY, DEFAULT_FONT_PATH, weight='normal', style='regular'
)


class Styler:
    def __init__(
        self,
        RADIUS=10,
        DIM=5000,
        OPACITY=1,
        PADDING=100,
        FONT_FAMILY=DEFAULT_FONT_FAMILY,
        FONT_SIZE=30,
    ):
        self.RADIUS = RADIUS
        self.DIM = DIM
        self.OPACITY = OPACITY
        self.PADDING = PADDING
        self.FONT_FAMILY = FONT_FAMILY
        self.FONT_SIZE = FONT_SIZE

    @cached_property
    def svg(self):
        return dict(
            width=self.DIM,
            height=self.DIM,
            padding=self.PADDING,
        )

    @cached_property
    def node_circle(self):
        return dict(
            r=self.RADIUS * 2,
            fill='white',
            stroke='black',
            stroke_width=self.RADIUS * 0.5,
        )

    @cached_property
    def node_text(self):
        return dict(
            fill='black',
            stroke='none',
            font_size=self.FONT_SIZE,
            font_family=self.FONT_FAMILY,
            font_weight="100",
            text_anchor='start',
            dominant_baseline='central',
        )

    @cached_property
    def line(self):
        return dict(
            fill='none',
            stroke='red',
            stroke_width=self.RADIUS * 2,
            stroke_opacity=self.OPACITY,
        )
