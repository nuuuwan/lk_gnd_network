import colorsys


def p_to_color(p):
    h = p * 120 / 360.0
    l = 0.4 + 0.5 * p
    s = 1 - p

    (r, g, b) = [int(x * 255) for x in colorsys.hls_to_rgb(h, l, s)]
    hex = f'#{r:02x}{g:02x}{b:02x}'
    return hex
