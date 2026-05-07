import pyxel

from data import (
    SPR_KNIGHT,
    SPR_MAGE,
    SPR_VIKING,
    SPR_ASSASSIN,
    SPR_CLERIC,
    SPR_PALADIN,
    SPR_RANGER,
    SPR_PYROMANCER,
    SPR_SKELETON,
    SPR_BAT,
    SPR_GHOST,
    SPR_ZOMBIE,
    SPR_DARK_MAGE,
    SPR_SLIME,
    SPR_NECROMANCER,
    SPR_DEMON,
    SPR_BOSS,
    SPR_TILE_GRASS,
    SPR_TILE_DESERT,
    SPR_TILE_CAVE,
    SPR_TILE_CASTLE,
    SPR_HEART,
    SPR_GEM,
    SPR_XP_GEM,
)

def _canvas(size):
    return [["0" for _ in range(size)] for _ in range(size)]


def _set(canvas, x, y, color):
    if 0 <= x < len(canvas[0]) and 0 <= y < len(canvas):
        canvas[y][x] = format(color, 'x')


def _rect(canvas, x, y, width, height, color):
    for yy in range(y, y + height):
        for xx in range(x, x + width):
            _set(canvas, xx, yy, color)


def _hline(canvas, x, y, width, color):
    _rect(canvas, x, y, width, 1, color)


def _vline(canvas, x, y, height, color):
    _rect(canvas, x, y, 1, height, color)


def _diag(canvas, x0, y0, x1, y1, color):
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        _set(canvas, x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        step = 2 * err
        if step >= dy:
            err += dy
            x0 += sx
        if step <= dx:
            err += dx
            y0 += sy


def _to_data(canvas):
    return ["".join(row) for row in canvas]


def _diamond(canvas, cx, cy, radius, color):
    for yy in range(cy - radius, cy + radius + 1):
        span = radius - abs(yy - cy)
        for xx in range(cx - span, cx + span + 1):
            _set(canvas, xx, yy, color)


def _circleish(canvas, cx, cy, radius, color):
    for yy in range(cy - radius, cy + radius + 1):
        for xx in range(cx - radius, cx + radius + 1):
            if (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy) <= radius * radius:
                _set(canvas, xx, yy, color)


def _copy(canvas):
    return [row[:] for row in canvas]


def _make_character(kind, frame):
    c = _canvas(16)
    if kind == 0:
        main, accent, light, skin = 6, 12, 1, 15
        _rect(c, 5, 1, 6, 3, light)
        _rect(c, 6, 0, 4, 2, accent)
        _set(c, 4, 3, light)
        _set(c, 11, 3, light)
        _rect(c, 5, 4, 6, 4, main)
        _rect(c, 5, 8, 2, 4, light)
        _rect(c, 9, 8, 2, 4, light)
        _rect(c, 4, 5, 2, 3, light)
        _rect(c, 10, 5, 2, 3, light)
        _rect(c, 6, 12, 4, 3, main)
        _set(c, 6, 2, skin)
        _set(c, 9, 2, skin)
        _rect(c, 13 if frame == 0 else 12, 9, 2, 1, accent)
        _diag(c, 11, 9, 14, 7 if frame == 0 else 8, 4)
        _diag(c, 14, 7 if frame == 0 else 8, 15, 8 if frame == 0 else 9, 4)
    elif kind == 1:
        main, accent, light, skin = 2, 10, 13, 15
        _rect(c, 5, 0, 6, 3, accent)
        _set(c, 4, 2, accent)
        _set(c, 11, 2, accent)
        _rect(c, 6, 3, 4, 1, light)
        _rect(c, 5, 4, 6, 7, main)
        _rect(c, 4, 5, 2, 3, accent)
        _rect(c, 10, 5, 2, 3, accent)
        _rect(c, 6, 11, 4, 4, light)
        _set(c, 6, 2, skin)
        _set(c, 9, 2, skin)
        _vline(c, 12, 3, 8, accent)
        _set(c, 12, 2, light)
        _set(c, 13, 2, accent)
        if frame == 1:
            _set(c, 13, 9, accent)
            _set(c, 12, 10, light)
        else:
            _set(c, 13, 8, accent)
    elif kind == 2:
        main, accent, light, skin = 4, 8, 10, 15
        _rect(c, 5, 1, 6, 2, accent)
        _rect(c, 4, 3, 8, 4, main)
        _rect(c, 5, 0, 6, 1, light)
        _set(c, 4, 2, accent)
        _set(c, 11, 2, accent)
        _rect(c, 5, 7, 2, 4, main)
        _rect(c, 9, 7, 2, 4, main)
        _rect(c, 5, 11, 2, 2, light)
        _rect(c, 9, 11, 2, 2, light)
        _set(c, 6, 2, skin)
        _set(c, 9, 2, skin)
        _vline(c, 12, 5, 6, accent)
        _rect(c, 13 if frame == 0 else 12, 8, 2, 2, accent)
        _diag(c, 12, 10, 15, 12, 8)
        _diag(c, 12, 11, 14, 13, 8)
    elif kind == 3:
        main, accent, light, skin = 5, 0, 15, 15
        _rect(c, 5, 1, 6, 3, accent)
        _rect(c, 6, 2, 4, 1, light)
        _rect(c, 4, 4, 8, 4, main)
        _rect(c, 5, 4, 2, 2, accent)
        _rect(c, 9, 4, 2, 2, accent)
        _rect(c, 5, 8, 2, 4, main)
        _rect(c, 9, 8, 2, 4, main)
        _rect(c, 6, 12, 4, 2, light)
        _set(c, 6, 2, skin)
        _set(c, 9, 2, skin)
        _diag(c, 12, 6, 15, 4 if frame == 0 else 5, accent)
        _diag(c, 12, 7, 15, 8 if frame == 0 else 7, accent)
        _diag(c, 13, 4, 14, 1, light)
        _diag(c, 13, 8, 14, 11, light)
    elif kind == 4:
        main, accent, light, skin = 7, 10, 15, 15
        _rect(c, 5, 1, 6, 2, accent)
        _rect(c, 4, 3, 8, 6, main)
        _rect(c, 5, 4, 2, 1, light)
        _rect(c, 9, 4, 2, 1, light)
        _rect(c, 5, 9, 6, 5, light)
        _rect(c, 6, 8, 4, 1, accent)
        _rect(c, 3, 6, 2, 2, light)
        _rect(c, 11, 6, 2, 2, accent)
        _set(c, 6, 2, skin)
        _set(c, 9, 2, skin)
        _vline(c, 12, 3, 6, accent)
        _hline(c, 11, 5, 4 if frame == 0 else 5, accent)
        _set(c, 12, 4, 10)
    elif kind == 5:
        main, accent, light, skin = 7, 6, 12, 15
        _rect(c, 5, 1, 6, 3, light)
        _rect(c, 4, 4, 8, 5, main)
        _rect(c, 5, 5, 2, 2, accent)
        _rect(c, 9, 5, 2, 2, accent)
        _rect(c, 5, 9, 2, 3, accent)
        _rect(c, 9, 9, 2, 3, accent)
        _rect(c, 6, 12, 4, 3, light)
        _set(c, 6, 2, skin)
        _set(c, 9, 2, skin)
        _rect(c, 12, 6, 3, 3, light)
        _rect(c, 11, 5, 1, 5, accent)
        _set(c, 13, 5, accent)
        _diag(c, 11, 8, 15, 8 if frame == 0 else 9, 12)
        _diag(c, 13, 7, 14, 6 if frame == 0 else 5, 6)
    elif kind == 6:
        main, accent, light, skin = 11, 4, 7, 15
        _rect(c, 5, 1, 6, 3, light)
        _rect(c, 4, 4, 8, 5, main)
        _rect(c, 5, 4, 2, 1, accent)
        _rect(c, 9, 4, 2, 1, accent)
        _rect(c, 4, 8, 3, 2, accent)
        _rect(c, 9, 8, 3, 2, accent)
        _rect(c, 5, 9, 2, 3, main)
        _rect(c, 9, 9, 2, 3, main)
        _rect(c, 6, 12, 4, 3, accent)
        _set(c, 6, 2, skin)
        _set(c, 9, 2, skin)
        _diag(c, 12, 5, 14, 3 if frame == 0 else 4, 4)
        _diag(c, 12, 6, 15, 5 if frame == 0 else 6, 4)
        _diag(c, 5, 9, 2, 7, 4)
        _diag(c, 5, 10, 2, 12, 4)
    else:
        main, accent, light, skin = 8, 10, 9, 15
        _rect(c, 5, 0, 6, 3, accent)
        _rect(c, 4, 3, 8, 4, main)
        _rect(c, 5, 4, 2, 1, light)
        _rect(c, 9, 4, 2, 1, light)
        _rect(c, 4, 7, 8, 4, accent)
        _rect(c, 5, 11, 6, 3, main)
        _rect(c, 6, 12, 4, 2, light)
        _set(c, 6, 2, skin)
        _set(c, 9, 2, skin)
        _diag(c, 12, 5, 15, 3 if frame == 0 else 4, accent)
        _diag(c, 12, 7, 15, 9 if frame == 0 else 8, 9)
        _set(c, 13, 2, 10)
        _set(c, 12, 3, 8)
    return _to_data(c)


def _make_enemy(kind, frame):
    c = _canvas(16)
    if kind == 0:
        _rect(c, 6, 1, 4, 3, 7)
        _set(c, 6, 2, 5)
        _set(c, 9, 2, 5)
        _rect(c, 5, 4, 6, 1, 6)
        _rect(c, 4, 5, 8, 4, 6)
        _rect(c, 5, 6, 2, 1, 5)
        _rect(c, 9, 6, 2, 1, 5)
        _vline(c, 6, 8, 5, 6)
        _vline(c, 9, 8, 5, 6)
        _diag(c, 4, 6, 1, 9 if frame == 0 else 8, 5)
        _diag(c, 11, 6, 14, 9 if frame == 0 else 8, 5)
        _vline(c, 7, 9, 4, 7)
        _vline(c, 8, 9, 4, 7)
    elif kind == 1:
        _rect(c, 5, 6, 6, 2, 2)
        _diag(c, 2, 6, 6, 3 if frame == 0 else 4, 2)
        _diag(c, 2, 7, 6, 9 if frame == 0 else 10, 2)
        _diag(c, 13, 6, 9, 3 if frame == 0 else 4, 2)
        _diag(c, 13, 7, 9, 9 if frame == 0 else 10, 2)
        _rect(c, 6, 5, 4, 3, 1)
        _set(c, 6, 6, 14)
        _set(c, 9, 6, 14)
        _rect(c, 7, 8, 2, 4, 2)
    elif kind == 2:
        _circleish(c, 8, 8, 5, 7)
        for yy in range(4, 12):
            _set(c, 8, yy, 12)
        _set(c, 7, 7, 1)
        _set(c, 9, 7, 1)
        _set(c, 8, 9, 6)
        _set(c, 6, 4, 15)
        _set(c, 10, 4, 15)
        _diag(c, 4, 10, 3, 13 if frame == 0 else 12, 15)
        _diag(c, 12, 10, 13, 13 if frame == 0 else 12, 15)
    elif kind == 3:
        _rect(c, 4, 4, 8, 6, 3)
        _rect(c, 5, 2, 6, 3, 11)
        _set(c, 6, 3, 4)
        _set(c, 9, 3, 4)
        _rect(c, 4, 8, 8, 4, 4)
        _rect(c, 3, 10, 2, 3, 4)
        _rect(c, 11, 10, 2, 3, 4)
        _diag(c, 4, 7, 1, 12 if frame == 0 else 11, 11)
        _diag(c, 11, 7, 14, 12 if frame == 0 else 11, 11)
        _set(c, 13, 13, 5)
    elif kind == 4:
        _rect(c, 5, 1, 6, 2, 2)
        _rect(c, 4, 3, 8, 8, 0)
        _rect(c, 5, 4, 6, 5, 2)
        _rect(c, 6, 5, 4, 2, 3)
        _set(c, 6, 5, 14)
        _set(c, 9, 5, 14)
        _vline(c, 12, 5, 6, 10)
        _rect(c, 4, 9, 8, 2, 0)
        _diag(c, 6, 11, 5, 14 if frame == 0 else 13, 2)
        _diag(c, 10, 11, 11, 14 if frame == 0 else 13, 2)
    elif kind == 5:
        _circleish(c, 8, 8, 5, 11)
        _circleish(c, 8, 8, 4, 10)
        _set(c, 7, 7, 15)
        _set(c, 9, 7, 15)
        _set(c, 8, 9, 3)
        _set(c, 8, 5, 15)
        _set(c, 8, 11, 9)
        _set(c, 11, 8, 9)
        _set(c, 5, 8, 9)
    elif kind == 6:
        _rect(c, 5, 1, 6, 2, 0)
        _rect(c, 4, 3, 8, 9, 5)
        _rect(c, 5, 4, 6, 4, 7)
        _set(c, 6, 5, 15)
        _set(c, 9, 5, 15)
        _rect(c, 3, 5, 1, 5, 5)
        _rect(c, 12, 5, 1, 5, 5)
        _diag(c, 4, 11, 2, 14 if frame == 0 else 13, 0)
        _diag(c, 11, 11, 13, 14 if frame == 0 else 13, 0)
        _set(c, 13, 4, 6)
        _set(c, 14, 3, 7)
    else:
        _rect(c, 5, 2, 6, 2, 8)
        _rect(c, 4, 4, 8, 5, 8)
        _rect(c, 5, 5, 2, 2, 9)
        _rect(c, 9, 5, 2, 2, 9)
        _rect(c, 5, 9, 6, 3, 8)
        _diag(c, 4, 6, 1, 3 if frame == 0 else 4, 8)
        _diag(c, 11, 6, 14, 3 if frame == 0 else 4, 8)
        _diag(c, 5, 12, 2, 14 if frame == 0 else 13, 8)
        _diag(c, 10, 12, 13, 14 if frame == 0 else 13, 8)
        _set(c, 8, 13, 4)
        _set(c, 6, 2, 10)
        _set(c, 9, 2, 10)
    return _to_data(c)


def _make_boss():
    c = _canvas(32)
    for yy in range(4, 28):
        span = 9 - abs(16 - yy) // 2
        _rect(c, 16 - span, yy, span * 2, 2, 0)
    _rect(c, 10, 4, 12, 6, 0)
    _rect(c, 12, 6, 8, 5, 5)
    _set(c, 14, 8, 7)
    _set(c, 17, 8, 7)
    _set(c, 15, 10, 0)
    _set(c, 16, 10, 0)
    _set(c, 17, 10, 0)
    _rect(c, 9, 11, 14, 11, 0)
    _diag(c, 10, 13, 6, 25, 0)
    _diag(c, 22, 13, 26, 25, 0)
    _rect(c, 13, 12, 6, 15, 2)
    _rect(c, 15, 13, 2, 12, 5)
    _diag(c, 6, 13, 3, 21, 0)
    _diag(c, 26, 13, 29, 21, 0)
    _diag(c, 7, 13, 2, 18, 0)
    _diag(c, 25, 13, 30, 18, 0)
    _diag(c, 17, 0, 20, 12, 6)
    _diag(c, 18, 1, 22, 9, 7)
    _rect(c, 18, 8, 10, 2, 6)
    _diag(c, 22, 9, 29, 3, 5)
    _diag(c, 23, 9, 30, 2, 5)
    _rect(c, 24, 4, 3, 10, 0)
    _rect(c, 25, 4, 1, 10, 7)
    _diag(c, 23, 9, 27, 14, 6)
    _diag(c, 22, 10, 28, 17, 0)
    _diag(c, 21, 11, 29, 18, 0)
    _rect(c, 14, 26, 4, 3, 6)
    _rect(c, 18, 26, 4, 3, 6)
    _rect(c, 12, 26, 2, 2, 5)
    _rect(c, 22, 26, 2, 2, 5)
    _diag(c, 13, 20, 9, 24, 0)
    _diag(c, 19, 20, 23, 24, 0)
    _rect(c, 13, 22, 2, 3, 2)
    _rect(c, 18, 22, 2, 3, 2)
    return _to_data(c)


def _make_grass(variant):
    c = _canvas(16)
    for y in range(16):
        shade = 3 if y < 8 else 11
        _rect(c, 0, y, 16, 1, shade)
    for x in range(0, 16, 4):
        _diag(c, x, 15, x + 1, 11 + (variant % 2), 3)
    if variant == 0:
        _rect(c, 3, 4, 1, 1, 10)
        _rect(c, 11, 5, 1, 1, 7)
        _rect(c, 7, 9, 2, 1, 6)
    elif variant == 1:
        _diag(c, 2, 12, 4, 10, 10)
        _diag(c, 10, 13, 13, 11, 10)
        _rect(c, 6, 3, 1, 1, 7)
    elif variant == 2:
        _diag(c, 5, 15, 6, 9, 3)
        _diag(c, 11, 15, 12, 8, 3)
        _rect(c, 2, 6, 1, 1, 10)
        _rect(c, 13, 4, 1, 1, 7)
    else:
        _rect(c, 5, 5, 2, 1, 10)
        _rect(c, 9, 9, 1, 1, 7)
        _diag(c, 1, 14, 4, 10, 3)
    return _to_data(c)


def _make_desert(variant):
    c = _canvas(16)
    for y in range(16):
        shade = 10 if y < 8 else 9
        _rect(c, 0, y, 16, 1, shade)
    _diag(c, 0, 12, 15, 9, 10)
    _diag(c, 0, 15, 15, 12, 9)
    if variant == 0:
        _rect(c, 3, 6, 1, 4, 11)
        _rect(c, 2, 7, 3, 1, 11)
    elif variant == 1:
        _rect(c, 11, 5, 1, 5, 11)
        _rect(c, 10, 7, 3, 1, 11)
    elif variant == 2:
        _rect(c, 6, 4, 1, 5, 11)
        _rect(c, 5, 6, 3, 1, 11)
        _set(c, 7, 3, 7)
    else:
        _diag(c, 4, 14, 6, 10, 4)
        _diag(c, 10, 15, 12, 11, 4)
        _rect(c, 13, 8, 1, 2, 11)
    return _to_data(c)


def _make_cave(variant):
    c = _canvas(16)
    for y in range(16):
        shade = 5 if y < 8 else 1
        _rect(c, 0, y, 16, 1, shade)
    _diag(c, 0, 3, 6, 0, 6)
    _diag(c, 9, 2, 15, 0, 6)
    _diag(c, 0, 15, 7, 11, 5)
    _diag(c, 9, 14, 15, 10, 5)
    if variant == 0:
        _rect(c, 12, 4, 1, 4, 12)
        _rect(c, 11, 6, 3, 1, 6)
    elif variant == 1:
        _rect(c, 3, 5, 1, 4, 12)
        _rect(c, 2, 7, 3, 1, 6)
    elif variant == 2:
        _diag(c, 6, 13, 8, 8, 12)
        _diag(c, 7, 13, 10, 9, 7)
    else:
        _rect(c, 7, 3, 2, 2, 12)
        _rect(c, 6, 4, 4, 1, 7)
    return _to_data(c)


def _make_castle(variant):
    c = _canvas(16)
    for y in range(16):
        shade = 2 if y < 8 else 5
        _rect(c, 0, y, 16, 1, shade)
    for x in range(0, 16, 4):
        _rect(c, x, 0, 2, 16, 5)
        _rect(c, x + 1, 0, 1, 16, 2)
    if variant == 0:
        _rect(c, 6, 5, 4, 4, 6)
        _rect(c, 7, 6, 2, 2, 1)
    elif variant == 1:
        _diag(c, 0, 14, 15, 8, 2)
        _diag(c, 0, 15, 15, 9, 5)
    elif variant == 2:
        _rect(c, 3, 4, 2, 2, 10)
        _rect(c, 11, 4, 2, 2, 10)
    else:
        _rect(c, 6, 2, 4, 4, 7)
        _rect(c, 7, 3, 2, 2, 2)
    return _to_data(c)


def _make_heart():
    c = _canvas(16)
    _rect(c, 4, 3, 3, 2, 8)
    _rect(c, 9, 3, 3, 2, 8)
    _rect(c, 3, 5, 10, 4, 8)
    _rect(c, 5, 8, 6, 3, 8)
    _diag(c, 4, 4, 2, 6, 8)
    _diag(c, 11, 4, 13, 6, 8)
    _rect(c, 6, 5, 4, 1, 15)
    _rect(c, 5, 9, 6, 1, 15)
    return _to_data(c)


def _make_dash_icon():
    c = _canvas(16)
    _diag(c, 3, 8, 7, 3, 12)
    _diag(c, 7, 3, 12, 6, 15)
    _diag(c, 12, 6, 8, 12, 12)
    _diag(c, 8, 12, 3, 9, 15)
    _rect(c, 6, 7, 4, 2, 1)
    _rect(c, 7, 6, 2, 4, 13)
    return _to_data(c)


def _make_xp_gem():
    c = _canvas(16)
    _diamond(c, 8, 8, 5, 14)
    _diamond(c, 8, 8, 4, 15)
    _set(c, 8, 4, 7)
    _set(c, 11, 8, 13)
    _set(c, 8, 12, 8)
    _set(c, 5, 8, 12)
    _diag(c, 6, 6, 8, 4, 7)
    _diag(c, 10, 6, 12, 8, 13)
    return _to_data(c)


def _build_sprite_bank():
    bank = {}
    character_slots = [SPR_KNIGHT, SPR_MAGE, SPR_VIKING, SPR_ASSASSIN, SPR_CLERIC, SPR_PALADIN, SPR_RANGER, SPR_PYROMANCER]
    enemy_slots = [SPR_SKELETON, SPR_BAT, SPR_GHOST, SPR_ZOMBIE, SPR_DARK_MAGE, SPR_SLIME, SPR_NECROMANCER, SPR_DEMON]

    for index, slot in enumerate(character_slots):
        bank[slot] = _make_character(index, 0)
        bank[(slot[0], slot[1] + 16)] = _make_character(index, 1)

    for index, slot in enumerate(enemy_slots):
        bank[slot] = _make_enemy(index, 0)
        bank[(slot[0], slot[1] + 16)] = _make_enemy(index, 1)

    bank[SPR_BOSS] = _make_boss()

    biome_builders = [
        (_make_grass, SPR_TILE_GRASS[0]),
        (_make_desert, SPR_TILE_DESERT[0]),
        (_make_cave, SPR_TILE_CAVE[0]),
        (_make_castle, SPR_TILE_CASTLE[0]),
    ]
    for builder, x in biome_builders:
        for variant in range(4):
            bank[(x, 128 + variant * 16)] = builder(variant)

    bank[SPR_HEART] = _make_heart()
    bank[SPR_GEM] = _make_dash_icon()
    bank[SPR_XP_GEM] = _make_xp_gem()
    return bank


SPRITE_BANK = _build_sprite_bank()


def create_sprites():
    image = pyxel.images[0]
    for (x, y), data in SPRITE_BANK.items():
        image.set(x, y, data)
