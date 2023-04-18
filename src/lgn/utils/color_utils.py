import colorsys


def p_to_color(p):
    hue = p * 120 / 360.0
    lightness = 0.4 + 0.5 * p
    saturation = 1

    (r, g, b) = [
        int(x * 255) for x in colorsys.hls_to_rgb(hue, lightness, saturation)
    ]
    hex = f'#{r:02x}{g:02x}{b:02x}'
    return hex
