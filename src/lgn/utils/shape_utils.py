import shapely
from utils import Log

log = Log(__name__)


DISTANCE_PER_UNIT_COORD = 110

def computer_area_for_polygon(polygon):
    return shapely.Polygon(polygon).area


def compute_area(polygon_list):
    return sum(
        [computer_area_for_polygon(polygon) for polygon in polygon_list]
    )


def compute_distance(loc1, loc2):
    x1, y1 = loc1
    x2, y2 = loc2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 * DISTANCE_PER_UNIT_COORD


def get_bbox(loc_list: list) -> tuple[float, float, float, float]:
    min_y, min_x, max_y, max_x = shapely.Polygon(loc_list).bounds
    return min_x, min_y, max_x, max_y


def get_t(styler, loc_list: list):
    min_x, min_y, max_x, max_y = get_bbox(loc_list)
    log.debug([min_x, min_y, max_x, max_y])

    x_span = max(0.00001, max_x - min_x)
    y_span = max(0.00001, max_y - min_y)
    max_span = max(x_span, y_span)
    log.debug(f'{x_span=}, {y_span=}')

    padding = styler.svg['padding']
    diagram_width = styler.svg['width'] - 2 * padding
    diagram_height = styler.svg['height'] - 2 * padding

    inner_width = diagram_width * x_span / max_span
    inner_height = diagram_height * y_span / max_span
    padding_x = (diagram_width - inner_width) / 2
    padding_y = (diagram_height - inner_height) / 2

    def t(y: float, x: float) -> list[int]:
        px = (x - min_x) / x_span
        py = (y - min_y) / y_span
        sx = int(px * inner_width + padding_x + padding)
        sy = int((1 - py) * inner_height + padding_y + padding)
        return sx, sy

    return t
