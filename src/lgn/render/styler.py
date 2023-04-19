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
        RADIUS=20,
        DIM=4000,
        OPACITY=1,
        PADDING=500,
        FONT_FAMILY=DEFAULT_FONT_FAMILY,
        FONT_SIZE=60,
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
    def text_supertitle(self):
        return dict(
            x=self.DIM / 2,
            y=self.PADDING * 0.25,
            fill='gray',
            stroke='none',
            font_size=self.FONT_SIZE,
            font_family=self.FONT_FAMILY,
            text_anchor='middle',
            dominant_baseline='hanging',
        )

    @cached_property
    def text_title(self):
        return dict(
            x=self.DIM / 2,
            y=self.PADDING * 0.5,
            fill='gray',
            stroke='none',
            font_size=self.FONT_SIZE * 2,
            font_family=self.FONT_FAMILY,
            text_anchor='middle',
            dominant_baseline='hanging',
        )

    @cached_property
    def text_network_info(self):
        return dict(
            x=self.DIM * 3 / 4,
            y=self.DIM * 1 / 4,
            fill='lightgrey',
            stroke='none',
            font_size=self.FONT_SIZE * 3,
            font_family=self.FONT_FAMILY,
            text_anchor='start',
            dominant_baseline='hanging',
        )

    @cached_property
    def text_network_info2(self):
        return dict(
            x=self.DIM * 3 / 4,
            y=self.DIM * 1 / 4 + self.FONT_SIZE * 2,
            fill='lightgrey',
            stroke='none',
            font_size=self.FONT_SIZE * 1.5,
            font_family=self.FONT_FAMILY,
            text_anchor='start',
            dominant_baseline='hanging',
        )

    @cached_property
    def text_footer(self):
        return dict(
            x=self.DIM / 2,
            y=self.DIM - self.PADDING * 0.5,
            fill='gray',
            stroke='none',
            font_size=self.FONT_SIZE,
            font_family=self.FONT_FAMILY,
            text_anchor='middle',
            dominant_baseline='hanging',
        )

    @cached_property
    def node_circle(self):
        return dict(
            r=self.RADIUS * 2,
            fill='white',
            stroke='gray',
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
            stroke='white',
            stroke_width=self.RADIUS * 2,
            stroke_opacity=self.OPACITY,
        )
