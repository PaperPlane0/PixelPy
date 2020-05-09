import pygame


def get_avg(pixel):
    return sum(pixel) / 3


def colorize(img, color):
    pixels = img
    x, y = img.get_size()
    r, g, b = color[:3]
    for i in range(x):
        for j in range(y):
            pixel = pixels.get_at((i, j))
            a = pixel[3]
            brightness = 1 - (get_avg(pixel[:3]) / 255)
            col = pygame.Color(int(r * brightness), int(g * brightness), int(b * brightness), a)
            pixels.set_at((i, j), col)


def rgba_to_rgb(RGB_background, RGBA_color):
    alpha = 1
    if len(RGBA_color) == 4:
        alpha = RGBA_color[3] / 255
    out_col = ((1 - alpha) * RGB_background[0] + alpha * RGBA_color[0],
              (1 - alpha) * RGB_background[1] + alpha * RGBA_color[1],
              (1 - alpha) * RGB_background[2] + alpha * RGBA_color[2])
    return tuple(map(int, out_col))


def lerp(start, end, t):
    return start + t * (end - start)


def diagonal_distance(p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    dx, dy = x1 - x0, y1 - y0
    return max(abs(dx), abs(dy))


def grid_snap(x, y, grid_x, grid_y, row_size, col_size):
    row = (y - grid_y) // row_size
    col = (x - grid_x) // col_size
    return row, col


def lerp_point(p0, p1, t):
    x0, y0 = p0
    x1, y1 = p1
    return lerp(x0, x1, t), lerp(y0, y1, t)


def canvas_flood_fill(canv, row, col, color, surface=None):
    px = canv.table[row][col]
    old_col = px.color
    flood_fill(px, color, old_col, surface=surface)


def flood_fill(pixel, color, old_col, surface=None):
    if color == old_col:
        return
    queue = [pixel]
    while queue:
        px = queue.pop()
        px.color = color
        if surface:
            px.draw(surface)
        for neighbor in px.neighbors:
            if neighbor.color == old_col:
                queue.append(neighbor)


def decrease_brightness(col, amt=2):
    amt = constrain(amt, 1, 255)
    return tuple([x // amt for x in col])


def constrain(val, minv, maxv):
    if val > maxv:
        return maxv
    elif val < minv:
        return minv
    return val


def map_value(val, val_min, val_max, out_min, out_max):
    return (val - val_min) * (out_max - out_min) // (val_max - val_min) + out_min
