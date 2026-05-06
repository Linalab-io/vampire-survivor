
import math
import random

import pyxel


SPR_KNIGHT = (0, 0)
SPR_MAGE = (16, 0)
SPR_VIKING = (32, 0)
SPR_ASSASSIN = (48, 0)
SPR_CLERIC = (64, 0)
SPR_PALADIN = (80, 0)
SPR_RANGER = (96, 0)
SPR_PYROMANCER = (112, 0)

SPR_SKELETON = (0, 32)
SPR_BAT = (16, 32)
SPR_GHOST = (32, 32)
SPR_ZOMBIE = (48, 32)
SPR_DARK_MAGE = (64, 32)
SPR_SLIME = (80, 32)
SPR_NECROMANCER = (96, 32)
SPR_DEMON = (112, 32)

SPR_BOSS = (0, 64)

SPR_TILE_GRASS = (0, 128)
SPR_TILE_DESERT = (64, 128)
SPR_TILE_CAVE = (128, 128)
SPR_TILE_CASTLE = (192, 128)

SPR_HEART = (0, 192)
SPR_GEM = (16, 192)
SPR_XP_GEM = (32, 192)

PLAYER_SPEED = 1.5
SPAWN_INTERVAL_FRAMES = 60
MAX_ENEMIES = 50
ENEMY_ACTIVE_RADIUS = 200
ENEMY_DESPAWN_RADIUS = 500
ENEMY_SPAWN_DISTANCE = 112

LEVEL_XP_THRESHOLDS = [0, 5, 12, 22, 35, 52, 73, 100, 133, 173, 220, 275, 338, 410, 492]
while len(LEVEL_XP_THRESHOLDS) <= 99:
    next_xp = int(LEVEL_XP_THRESHOLDS[-1] * 1.18) + 5
    if next_xp <= LEVEL_XP_THRESHOLDS[-1]:
        next_xp = LEVEL_XP_THRESHOLDS[-1] + 1
    LEVEL_XP_THRESHOLDS.append(next_xp)

ENEMY_DATA = [
    # (type_id, name, base_hp, base_speed, spawn_time_seconds, sprite)
    (0, "Skeleton", 3, 0.5, 0, SPR_SKELETON),
    (1, "Bat", 2, 1.5, 30, SPR_BAT),
    (2, "Ghost", 5, 0.8, 120, SPR_GHOST),
    (3, "Zombie", 12, 0.3, 180, SPR_ZOMBIE),
    (4, "Dark Mage", 6, 0.4, 300, SPR_DARK_MAGE),
    (5, "Slime", 4, 0.6, 420, SPR_SLIME),
    (6, "Necromancer", 8, 0.3, 600, SPR_NECROMANCER),
    (7, "Demon", 15, 1.2, 900, SPR_DEMON),
]
ENEMY_BY_TYPE = {enemy[0]: enemy for enemy in ENEMY_DATA}
ENEMY_GEM_VALUES = {0: 1, 1: 1, 2: 2, 3: 3, 4: 3, 5: 2, 6: 4, 7: 5}

WEAPON_DATA = {
    # weapon_id: {"name", "cooldown", "damage", "range", "type"}
    0: {"name": "Whip", "cooldown": 45, "damage": 8, "range": 32, "type": "melee"},
    1: {"name": "Magic Wand", "cooldown": 40, "damage": 6, "range": 120, "type": "projectile"},
    2: {"name": "Axe", "cooldown": 50, "damage": 10, "range": 60, "type": "projectile"},
    3: {"name": "Knife", "cooldown": 15, "damage": 3, "range": 100, "type": "projectile"},
    4: {"name": "Holy Water", "cooldown": 90, "damage": 8, "range": 80, "type": "projectile"},
    5: {"name": "Garlic", "cooldown": 0, "damage": 2, "range": 40, "type": "aura"},
    6: {"name": "Cross", "cooldown": 60, "damage": 7, "range": 80, "type": "projectile"},
    7: {"name": "Fire Wand", "cooldown": 55, "damage": 5, "range": 100, "type": "projectile"},
}

MAX_WEAPON_SLOTS = 6
MAX_PASSIVE_SLOTS = 6
MAX_WEAPON_LEVEL = 8
MAX_PASSIVE_LEVEL = 5

WEAPON_LEVELS = {
    level: {
        "damage_mult": 1.0 + (level - 1) * 0.10,
        "area_mult": 1.0 + (level - 1) * 0.05,
        "cooldown_mult": 1.0,
    }
    for level in range(1, MAX_WEAPON_LEVEL + 1)
}

PASSIVE_EFFECTS = {
    0: {"stat": "max_hp_mult", "per_level": 0.10, "stack": "add"},
    1: {"stat": "weapon_cooldown_mult", "per_level": 0.92, "stack": "mul"},
    2: {"stat": "weapon_area_mult", "per_level": 0.10, "stack": "add"},
    3: {"stat": "projectile_speed_mult", "per_level": 0.10, "stack": "add"},
    4: {"stat": "magnet_mult", "per_level": 0.25, "stack": "add"},
    5: {"stat": "hp_regen", "per_level": 0.5, "stack": "add_flat"},
    6: {"stat": "luck", "per_level": 0.10, "stack": "add_flat"},
    7: {"stat": "weapon_damage_mult", "per_level": 0.10, "stack": "add"},
}

EVOLUTION_REQUIREMENTS = {
    0: {"passive_id": 0, "weapon_level": MAX_WEAPON_LEVEL, "passive_level": MAX_PASSIVE_LEVEL},
    1: {"passive_id": 1, "weapon_level": MAX_WEAPON_LEVEL, "passive_level": MAX_PASSIVE_LEVEL},
    2: {"passive_id": 2, "weapon_level": MAX_WEAPON_LEVEL, "passive_level": MAX_PASSIVE_LEVEL},
    3: {"passive_id": 3, "weapon_level": MAX_WEAPON_LEVEL, "passive_level": MAX_PASSIVE_LEVEL},
    4: {"passive_id": 4, "weapon_level": MAX_WEAPON_LEVEL, "passive_level": MAX_PASSIVE_LEVEL},
    5: {"passive_id": 5, "weapon_level": MAX_WEAPON_LEVEL, "passive_level": MAX_PASSIVE_LEVEL},
    6: {"passive_id": 6, "weapon_level": MAX_WEAPON_LEVEL, "passive_level": MAX_PASSIVE_LEVEL},
    7: {"passive_id": 7, "weapon_level": MAX_WEAPON_LEVEL, "passive_level": MAX_PASSIVE_LEVEL},
}

UPGRADE_POOL = [
    {"type": "weapon", "id": 0, "name": "Whip", "desc": "Melee attack"},
    {"type": "weapon", "id": 1, "name": "Magic Wand", "desc": "Targets nearest enemy"},
    {"type": "weapon", "id": 2, "name": "Axe", "desc": "Arcing throw"},
    {"type": "weapon", "id": 3, "name": "Knife", "desc": "Fast aimed projectile"},
    {"type": "weapon", "id": 4, "name": "Holy Water", "desc": "Lingering splash zone"},
    {"type": "weapon", "id": 5, "name": "Garlic", "desc": "Damaging aura"},
    {"type": "weapon", "id": 6, "name": "Cross", "desc": "Returning boomerang"},
    {"type": "weapon", "id": 7, "name": "Fire Wand", "desc": "Exploding fireball"},
]

PASSIVE_POOL = [
    {"type": "passive", "id": 0, "name": "Hollow Heart", "desc": "Max HP +10%"},
    {"type": "passive", "id": 1, "name": "Empty Tome", "desc": "Cooldown -8%"},
    {"type": "passive", "id": 2, "name": "Candelabrador", "desc": "Area +10%"},
    {"type": "passive", "id": 3, "name": "Bracer", "desc": "Proj Speed +10%"},
    {"type": "passive", "id": 4, "name": "Attractorb", "desc": "Magnet +25%"},
    {"type": "passive", "id": 5, "name": "Pummarola", "desc": "HP Regen"},
    {"type": "passive", "id": 6, "name": "Clover", "desc": "Luck +10%"},
    {"type": "passive", "id": 7, "name": "Spinach", "desc": "Damage +10%"},
]

CHARACTER_DATA = [
    {"name": "Knight",   "weapon": 0, "color": 9},   # Whip - orange
    {"name": "Mage",     "weapon": 1, "color": 12},  # Magic Wand - blue
    {"name": "Warrior",  "weapon": 2, "color": 4},   # Axe - brown/red
    {"name": "Rogue",    "weapon": 3, "color": 13},  # Knife - green
    {"name": "Cleric",   "weapon": 4, "color": 14},  # Holy Water - teal
    {"name": "Paladin",  "weapon": 5, "color": 7},   # Garlic - white
    {"name": "Priest",   "weapon": 6, "color": 10},  # Cross - yellow
    {"name": "Pyro",     "weapon": 7, "color": 8},   # Fire Wand - red
]

DIFFICULTY_DATA = [
    {"name": "Easy",   "hp_mult": 0.7,  "speed_mult": 0.8,  "spawn_mult": 1.3, "xp_mult": 0.8,  "desc": "Relaxed"},
    {"name": "Normal", "hp_mult": 1.0,  "speed_mult": 1.0,  "spawn_mult": 1.0, "xp_mult": 1.0,  "desc": "Balanced"},
    {"name": "Hard",   "hp_mult": 1.5,  "speed_mult": 1.3,  "spawn_mult": 0.7, "xp_mult": 1.3,  "desc": "Intense"},
]


def rect_overlap(ax, ay, aw, ah, bx, by, bw, bh):
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


def _tile_hash(wx, wy):
    """Deterministic hash for tile selection. Same coords = same result."""
    h = wx * 374761393 + wy * 668265263
    h = (h ^ (h >> 13)) * 1274126177
    return (h ^ (h >> 16)) & 0xFFFFFFFF


def tile_type(wx, wy):
    return _tile_hash(wx, wy) % 4


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


class App:
    def __init__(self):
        self.state = "TITLE"
        self.timer_frames = 0
        self.base_player_max_hp = 100
        self.player_hp = 100
        self.player_max_hp = self.base_player_max_hp
        self.player_level = 1
        self.player_xp = 0
        self.player_xp_next = LEVEL_XP_THRESHOLDS[self.player_level]
        self.player_x = 0.0
        self.player_y = 0.0
        self.facing_x = 1.0
        self.facing_y = 0.0
        self.prev_state = self.state
        self.enemy_count = 0
        self.gem_count = 0
        self.weapon_inventory = [0]
        self.weapon_levels = {0: 1}
        self.weapon_cooldowns = {0: 0}
        self.whip_attack_timer = 0
        self.whip_attack_side = 1
        self.whip_next_attack_side = 1
        self.passive_inventory = []
        self.weapon_cooldown_mult = 1.0
        self.weapon_area_mult = 1.0
        self.projectile_speed_mult = 1.0
        self.magnet_range = 30
        self.hp_regen = 0.0
        self.hp_regen_timer = 0
        self.luck = 0.0
        self.weapon_damage_mult = 1.0
        self.evolution_ready = []
        self.level_up_choices = []
        self.level_up_cursor = 0
        self.boss_active = False
        self.boss_hp = 0
        self.kills = 0
        self.dash_cooldown = 0
        self.dash_invincible = 0
        self.player_invincible = 0
        self.selected_character = 0
        self.difficulty = 1
        self.char_cursor = 0
        self.diff_cursor = 1
        self.high_score = 0
        self.biome = 0
        self.enemy_list = []
        self.spawn_timer = SPAWN_INTERVAL_FRAMES
        self.spawn_interval = SPAWN_INTERVAL_FRAMES
        self.projectile_list = []
        self.enemy_projectile_list = []
        self.damage_zone_list = []
        self.garlic_tick_timer = 0
        self.gem_list = []
        self.debug_time_scale = 1

        pyxel.init(160, 120, title="Vampire Survivors", fps=30)
        self._load_sprite_bank()
        pyxel.run(self.update, self.draw)

    def _load_sprite_bank(self):
        image = pyxel.images[0]
        for (x, y), data in SPRITE_BANK.items():
            image.set(x, y, data)

    def update(self):
        if self.state == "TITLE":
            self.update_title()
        elif self.state == "CHAR_SELECT":
            self.update_char_select()
        elif self.state == "DIFF_SELECT":
            self.update_diff_select()
        elif self.state == "PLAYING":
            self.update_playing()
        elif self.state == "LEVEL_UP":
            self.update_level_up()
        elif self.state == "PAUSED":
            self.update_paused()
        elif self.state == "BOSS":
            self.update_boss()
        elif self.state == "GAME_OVER":
            self.update_game_over()
        elif self.state == "VICTORY":
            self.update_victory()

    def draw(self):
        pyxel.cls(0)
        if self.state == "TITLE":
            self.draw_title()
        elif self.state == "CHAR_SELECT":
            self.draw_char_select()
        elif self.state == "DIFF_SELECT":
            self.draw_diff_select()
        elif self.state == "PLAYING":
            self.draw_playing()
        elif self.state == "LEVEL_UP":
            self.draw_level_up()
        elif self.state == "PAUSED":
            self.draw_paused()
        elif self.state == "BOSS":
            self.draw_boss()
        elif self.state == "GAME_OVER":
            self.draw_game_over()
        elif self.state == "VICTORY":
            self.draw_victory()

    def update_title(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_RETURN2):
            self.state = "CHAR_SELECT"

    def update_char_select(self):
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A):
            self.char_cursor = (self.char_cursor - 1) % 8
        elif pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D):
            self.char_cursor = (self.char_cursor + 1) % 8
        elif pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            self.char_cursor = (self.char_cursor - 4) % 8
        elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
            self.char_cursor = (self.char_cursor + 4) % 8
        elif pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_RETURN2):
            self.selected_character = self.char_cursor
            self.state = "DIFF_SELECT"

    def update_diff_select(self):
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A):
            self.diff_cursor = (self.diff_cursor - 1) % 3
        elif pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D):
            self.diff_cursor = (self.diff_cursor + 1) % 3
        elif pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_RETURN2):
            self.difficulty = self.diff_cursor
            self._apply_selections()
            self.state = "PLAYING"

    def _apply_selections(self):
        char_data = CHARACTER_DATA[self.selected_character]
        self.weapon_inventory = [char_data["weapon"]]
        self.weapon_levels = {char_data["weapon"]: 1}
        self.weapon_cooldowns = {char_data["weapon"]: 0}
        self.difficulty = self.diff_cursor
        
        diff = DIFFICULTY_DATA[self.difficulty]
        self.spawn_interval = int(SPAWN_INTERVAL_FRAMES * diff["spawn_mult"])
        self.spawn_timer = self.spawn_interval
        self.player_xp_next = int(LEVEL_XP_THRESHOLDS[self.player_level] * diff["xp_mult"])

    def update_playing(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.state = "PAUSED"
        self.timer_frames += 1
        self.dash_cooldown = max(0, self.dash_cooldown - 1)
        self.dash_invincible = max(0, self.dash_invincible - 1)
        self.player_invincible = max(0, self.player_invincible - 1)
        if self.hp_regen > 0:
            self.hp_regen_timer += 1
            if self.hp_regen_timer >= 180:
                self.hp_regen_timer -= 180
                self.player_hp = min(self.player_max_hp, self.player_hp + math.ceil(self.hp_regen))

        dx = 0
        dy = 0
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            dx += 1
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            dx -= 1
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            dy += 1
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            dy -= 1
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707

        self.player_x += dx * PLAYER_SPEED
        self.player_y += dy * PLAYER_SPEED
        if dx != 0 or dy != 0:
            self.facing_x = dx
            self.facing_y = dy

        if self.dash_cooldown == 0 and (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_X)):
            length = math.sqrt(self.facing_x * self.facing_x + self.facing_y * self.facing_y)
            if length == 0:
                dash_x = 1.0
                dash_y = 0.0
            else:
                dash_x = self.facing_x / length
                dash_y = self.facing_y / length
            self.player_x += dash_x * 40
            self.player_y += dash_y * 40
            self.dash_cooldown = 60
            self.dash_invincible = 10

        self.update_spawning()
        self.update_enemies()
        self.update_enemy_projectiles()
        self.update_weapons()
        self.update_projectiles()
        self.update_damage_zones()
        self.update_gems()
        self.check_level_up()

    def update_weapons(self):
        for weapon_id in self.weapon_inventory:
            cooldown = self.weapon_cooldowns.get(weapon_id, 0)
            if cooldown > 0:
                cooldown -= 1
                self.weapon_cooldowns[weapon_id] = cooldown
            if cooldown <= 0:
                if weapon_id == 0:
                    self.fire_whip()
                elif weapon_id == 1:
                    self.fire_magic_wand()
                elif weapon_id == 2:
                    self.fire_axe()
                elif weapon_id == 3:
                    self.fire_knife()
                elif weapon_id == 4:
                    self.fire_holy_water()
                elif weapon_id == 5:
                    self.fire_garlic()
                elif weapon_id == 6:
                    self.fire_cross()
                elif weapon_id == 7:
                    self.fire_fire_wand()

    def get_passive_level(self, passive_id):
        for passive in self.passive_inventory:
            if passive["id"] == passive_id:
                return passive["level"]
        return 0

    def get_weapon_stats(self, weapon_id):
        weapon = WEAPON_DATA[weapon_id]
        level = self.weapon_levels.get(weapon_id, 1)
        level_data = WEAPON_LEVELS[level]
        return {
            "cooldown": max(1, int(weapon["cooldown"] * level_data["cooldown_mult"] * self.weapon_cooldown_mult)),
            "damage": weapon["damage"] * level_data["damage_mult"] * self.weapon_damage_mult,
            "range": weapon["range"] * level_data["area_mult"] * self.weapon_area_mult,
        }

    def recalculate_passive_stats(self):
        old_max_hp = self.player_max_hp
        max_hp_mult = 1.0
        weapon_cooldown_mult = 1.0
        weapon_area_mult = 1.0
        projectile_speed_mult = 1.0
        magnet_mult = 1.0
        hp_regen = 0.0
        luck = 0.0
        weapon_damage_mult = 1.0

        for passive in self.passive_inventory:
            effect = PASSIVE_EFFECTS[passive["id"]]
            level = passive["level"]
            if effect["stack"] == "mul":
                weapon_cooldown_mult *= effect["per_level"] ** level
            elif effect["stat"] == "max_hp_mult":
                max_hp_mult += effect["per_level"] * level
            elif effect["stat"] == "weapon_area_mult":
                weapon_area_mult += effect["per_level"] * level
            elif effect["stat"] == "projectile_speed_mult":
                projectile_speed_mult += effect["per_level"] * level
            elif effect["stat"] == "magnet_mult":
                magnet_mult += effect["per_level"] * level
            elif effect["stat"] == "hp_regen":
                hp_regen += effect["per_level"] * level
            elif effect["stat"] == "luck":
                luck += effect["per_level"] * level
            elif effect["stat"] == "weapon_damage_mult":
                weapon_damage_mult += effect["per_level"] * level

        self.player_max_hp = int(self.base_player_max_hp * max_hp_mult)
        if self.player_max_hp > old_max_hp:
            self.player_hp += self.player_max_hp - old_max_hp
        self.player_hp = min(self.player_hp, self.player_max_hp)
        self.weapon_cooldown_mult = weapon_cooldown_mult
        self.weapon_area_mult = weapon_area_mult
        self.projectile_speed_mult = projectile_speed_mult
        self.magnet_range = 30 * magnet_mult
        self.hp_regen = hp_regen
        self.luck = luck
        self.weapon_damage_mult = weapon_damage_mult
        self.check_evolution_ready()

    def check_evolution_ready(self):
        ready = []
        for weapon_id, requirement in EVOLUTION_REQUIREMENTS.items():
            weapon_level = self.weapon_levels.get(weapon_id, 0)
            passive_level = self.get_passive_level(requirement["passive_id"])
            if weapon_level >= requirement["weapon_level"] and passive_level >= requirement["passive_level"]:
                ready.append(weapon_id)
        self.evolution_ready = ready

    def update_gems(self):
        magnet_range = self.magnet_range
        collect_range = 8
        despawn_range_sq = 500 * 500
        kept_gems = []

        for gem in self.gem_list:
            dx = self.player_x - gem["x"]
            dy = self.player_y - gem["y"]
            dist_sq = dx * dx + dy * dy

            if dist_sq > despawn_range_sq:
                continue

            dist = math.sqrt(dist_sq) if dist_sq > 0 else 0
            if dist <= collect_range:
                self.player_xp += gem["value"]
                continue

            if dist <= magnet_range and dist > 0:
                gem["x"] += dx / dist * 2
                gem["y"] += dy / dist * 2

            kept_gems.append(gem)

        self.gem_list = kept_gems
        self.gem_count = len(self.gem_list)

    def check_level_up(self):
        if self.player_level >= 99:
            return
        if self.player_xp < self.player_xp_next:
            return

        self.player_xp -= self.player_xp_next
        self.player_level += 1
        diff = DIFFICULTY_DATA[self.difficulty]
        base_next_xp = LEVEL_XP_THRESHOLDS[self.player_level] if self.player_level < len(LEVEL_XP_THRESHOLDS) else 99999
        self.player_xp_next = int(base_next_xp * diff["xp_mult"])
        self.base_player_max_hp += 2
        self.recalculate_passive_stats()
        self.prev_state = self.state
        self.generate_level_up_choices()
        self.state = "LEVEL_UP"

    def generate_level_up_choices(self):
        candidates = []
        owned_passive_ids = [passive["id"] for passive in self.passive_inventory]
        for p in PASSIVE_POOL:
            passive_level = self.get_passive_level(p["id"])
            if passive_level > 0 and passive_level < MAX_PASSIVE_LEVEL:
                candidates.append(p)
            elif passive_level == 0 and len(self.passive_inventory) < MAX_PASSIVE_SLOTS:
                candidates.append(p)

        for weapon_upgrade in UPGRADE_POOL:
            weapon_id = weapon_upgrade["id"]
            if weapon_id in self.weapon_inventory and self.weapon_levels.get(weapon_id, 1) < MAX_WEAPON_LEVEL:
                candidates.append(weapon_upgrade)
            elif weapon_id not in self.weapon_inventory and len(self.weapon_inventory) < MAX_WEAPON_SLOTS:
                candidates.append(weapon_upgrade)
             
        self.level_up_choices = []
        if len(candidates) >= 3:
            self.level_up_choices = random.sample(candidates, 3)
        else:
            self.level_up_choices = list(candidates)
            while len(self.level_up_choices) < 3:
                self.level_up_choices.append({"type": "stat", "name": "Max HP", "desc": "Max HP +10"})
                
        self.level_up_cursor = 0

    def fire_whip(self):
        weapon = self.get_weapon_stats(0)
        self.weapon_cooldowns[0] = weapon["cooldown"]
        self.whip_attack_side = self.whip_next_attack_side
        self.whip_next_attack_side *= -1
        self.whip_attack_timer = 10

        attack_range = weapon["range"]
        if self.whip_attack_side > 0:
            min_x = self.player_x
            max_x = self.player_x + attack_range
        else:
            min_x = self.player_x - attack_range
            max_x = self.player_x
        min_y = self.player_y - 16
        max_y = self.player_y + 16

        for enemy in self.enemy_list:
            enemy_hitbox_x = enemy["x"] - 6
            enemy_hitbox_y = enemy["y"] - 6
            if rect_overlap(
                min_x,
                min_y,
                max_x - min_x,
                max_y - min_y,
                enemy_hitbox_x,
                enemy_hitbox_y,
                12,
                12,
            ):
                enemy["hp"] -= weapon["damage"]
                dx = enemy["x"] - self.player_x
                dy = enemy["y"] - self.player_y
                distance_sq = dx * dx + dy * dy
                dist = math.sqrt(distance_sq) if distance_sq > 0 else 1
                enemy["x"] += dx / dist * 15
                enemy["y"] += dy / dist * 15
                enemy["knockback"] = 5

    def fire_magic_wand(self):
        weapon_id = 1
        weapon = self.get_weapon_stats(weapon_id)
        self.weapon_cooldowns[weapon_id] = weapon["cooldown"]
        if not self.enemy_list:
            return

        target = min(
            self.enemy_list,
            key=lambda enemy: (enemy["x"] - self.player_x) * (enemy["x"] - self.player_x)
            + (enemy["y"] - self.player_y) * (enemy["y"] - self.player_y),
        )
        dx = target["x"] - self.player_x
        dy = target["y"] - self.player_y
        distance = math.sqrt(dx * dx + dy * dy)
        if distance == 0:
            dx = 1.0
            dy = 0.0
            distance = 1.0

        speed = 3 * self.projectile_speed_mult
        self.projectile_list.append({
            "type": "wand",
            "x": self.player_x,
            "y": self.player_y,
            "dx": dx / distance * speed,
            "dy": dy / distance * speed,
            "damage": weapon["damage"],
            "lifetime": max(1, int(weapon["range"] / speed)),
            "weapon_id": weapon_id,
            "gravity": 0,
        })

    def fire_axe(self):
        weapon_id = 2
        weapon = self.get_weapon_stats(weapon_id)
        self.weapon_cooldowns[weapon_id] = weapon["cooldown"]
        self.projectile_list.append({
            "type": "axe",
            "x": self.player_x,
            "y": self.player_y,
            "dx": self.facing_x * 0.8 * self.projectile_speed_mult,
            "dy": -3 * self.projectile_speed_mult,
            "damage": weapon["damage"],
            "lifetime": 60,
            "weapon_id": weapon_id,
            "gravity": 0.15,
        })

    def fire_knife(self):
        weapon_id = 3
        weapon = self.get_weapon_stats(weapon_id)
        self.weapon_cooldowns[weapon_id] = weapon["cooldown"]
        length = math.sqrt(self.facing_x * self.facing_x + self.facing_y * self.facing_y)
        if length == 0:
            dx = 1.0
            dy = 0.0
        else:
            dx = self.facing_x / length
            dy = self.facing_y / length

        speed = 4 * self.projectile_speed_mult
        self.projectile_list.append({
            "type": "knife",
            "x": self.player_x,
            "y": self.player_y,
            "dx": dx * speed,
            "dy": dy * speed,
            "damage": weapon["damage"],
            "lifetime": max(1, int(weapon["range"] / speed)),
            "weapon_id": weapon_id,
            "gravity": 0,
        })

    def fire_holy_water(self):
        weapon_id = 4
        weapon = self.get_weapon_stats(weapon_id)
        self.weapon_cooldowns[weapon_id] = weapon["cooldown"]
        length = math.sqrt(self.facing_x * self.facing_x + self.facing_y * self.facing_y)
        if length == 0:
            dx = 1.0
            dy = 0.0
        else:
            dx = self.facing_x / length
            dy = self.facing_y / length

        speed = 1.8 * self.projectile_speed_mult
        self.projectile_list.append({
            "type": "holy_water",
            "x": self.player_x,
            "y": self.player_y,
            "dx": dx * speed,
            "dy": dy * speed - 2.0 * self.projectile_speed_mult,
            "damage": weapon["damage"],
            "lifetime": max(1, int(weapon["range"] / speed)),
            "weapon_id": weapon_id,
            "gravity": 0.12,
        })

    def fire_garlic(self):
        weapon_id = 5
        weapon = self.get_weapon_stats(weapon_id)
        self.garlic_tick_timer += 1
        if self.garlic_tick_timer < 30:
            return
        self.garlic_tick_timer -= 30

        range_sq = weapon["range"] * weapon["range"]
        for enemy in self.enemy_list:
            if enemy["hp"] <= 0:
                continue
            dx = enemy["x"] - self.player_x
            dy = enemy["y"] - self.player_y
            distance_sq = dx * dx + dy * dy
            if distance_sq <= range_sq:
                enemy["hp"] -= weapon["damage"]

    def fire_cross(self):
        weapon_id = 6
        weapon = self.get_weapon_stats(weapon_id)
        self.weapon_cooldowns[weapon_id] = weapon["cooldown"]
        length = math.sqrt(self.facing_x * self.facing_x + self.facing_y * self.facing_y)
        if length == 0:
            dx = 1.0
            dy = 0.0
        else:
            dx = self.facing_x / length
            dy = self.facing_y / length

        speed = 2.5 * self.projectile_speed_mult
        self.projectile_list.append({
            "type": "cross",
            "x": self.player_x,
            "y": self.player_y,
            "dx": dx * speed,
            "dy": dy * speed,
            "damage": weapon["damage"],
            "lifetime": max(1, int(weapon["range"] * 2 / speed) + 10),
            "weapon_id": weapon_id,
            "gravity": 0,
            "start_x": self.player_x,
            "start_y": self.player_y,
            "traveled": 0.0,
            "max_range": weapon["range"],
            "returning": False,
            "hit_enemy_ids": [],
        })

    def fire_fire_wand(self):
        weapon_id = 7
        weapon = self.get_weapon_stats(weapon_id)
        self.weapon_cooldowns[weapon_id] = weapon["cooldown"]
        if not self.enemy_list:
            return

        target = min(
            self.enemy_list,
            key=lambda enemy: (enemy["x"] - self.player_x) * (enemy["x"] - self.player_x)
            + (enemy["y"] - self.player_y) * (enemy["y"] - self.player_y),
        )
        dx = target["x"] - self.player_x
        dy = target["y"] - self.player_y
        distance = math.sqrt(dx * dx + dy * dy)
        if distance == 0:
            dx = 1.0
            dy = 0.0
            distance = 1.0

        speed = 3 * self.projectile_speed_mult
        self.projectile_list.append({
            "type": "fire_wand",
            "x": self.player_x,
            "y": self.player_y,
            "dx": dx / distance * speed,
            "dy": dy / distance * speed,
            "damage": weapon["damage"],
            "lifetime": max(1, int(weapon["range"] / speed)),
            "weapon_id": weapon_id,
            "gravity": 0,
            "explosion_damage": 4 * WEAPON_LEVELS[self.weapon_levels.get(weapon_id, 1)]["damage_mult"] * self.weapon_damage_mult,
        })

    def create_damage_zone(self, x, y, damage, weapon_id):
        self.damage_zone_list.append({
            "x": x - 12,
            "y": y - 12,
            "width": 24,
            "height": 24,
            "damage": damage,
            "timer": 30,
            "tick_interval": 10,
            "weapon_id": weapon_id,
        })

    def update_projectiles(self):
        kept_projectiles = []
        for projectile in self.projectile_list:
            projectile["dy"] += projectile["gravity"]
            projectile["x"] += projectile["dx"]
            projectile["y"] += projectile["dy"]
            projectile["lifetime"] -= 1

            if projectile["type"] == "cross":
                step_distance = math.sqrt(projectile["dx"] * projectile["dx"] + projectile["dy"] * projectile["dy"])
                projectile["traveled"] += step_distance
                if not projectile["returning"] and projectile["traveled"] >= projectile["max_range"]:
                    projectile["dx"] *= -1
                    projectile["dy"] *= -1
                    projectile["returning"] = True
                    projectile["hit_enemy_ids"] = []

            if projectile["type"] == "axe":
                width = 16
                height = 16
            elif projectile["type"] == "knife":
                width = 8
                height = 4
            elif projectile["type"] == "holy_water":
                width = 6
                height = 6
            elif projectile["type"] == "cross":
                width = 6
                height = 6
            elif projectile["type"] == "fire_wand":
                width = 5
                height = 5
            else:
                width = 4
                height = 4
            projectile_x = projectile["x"] - width / 2
            projectile_y = projectile["y"] - height / 2
            hit_enemy = False

            for enemy in self.enemy_list:
                if enemy["hp"] <= 0:
                    continue
                if projectile["type"] == "cross" and id(enemy) in projectile["hit_enemy_ids"]:
                    continue
                if rect_overlap(projectile_x, projectile_y, width, height, enemy["x"] - 6, enemy["y"] - 6, 12, 12):
                    if projectile["type"] == "holy_water":
                        self.create_damage_zone(projectile["x"], projectile["y"], projectile["damage"], projectile["weapon_id"])
                        hit_enemy = True
                        break
                    if projectile["type"] == "fire_wand":
                        enemy["hp"] -= projectile["damage"]
                        dx = enemy["x"] - self.player_x
                        dy = enemy["y"] - self.player_y
                        distance_sq = dx * dx + dy * dy
                        dist = math.sqrt(distance_sq) if distance_sq > 0 else 1
                        enemy["x"] += dx / dist * 15
                        enemy["y"] += dy / dist * 15
                        enemy["knockback"] = 5
                        explosion_range_sq = 24 * 24
                        for splash_enemy in self.enemy_list:
                            if splash_enemy["hp"] <= 0:
                                continue
                            splash_dx = splash_enemy["x"] - projectile["x"]
                            splash_dy = splash_enemy["y"] - projectile["y"]
                            if splash_dx * splash_dx + splash_dy * splash_dy <= explosion_range_sq:
                                splash_enemy["hp"] -= projectile["explosion_damage"]
                        hit_enemy = True
                        break

                    enemy["hp"] -= projectile["damage"]
                    dx = enemy["x"] - self.player_x
                    dy = enemy["y"] - self.player_y
                    distance_sq = dx * dx + dy * dy
                    dist = math.sqrt(distance_sq) if distance_sq > 0 else 1
                    enemy["x"] += dx / dist * 15
                    enemy["y"] += dy / dist * 15
                    enemy["knockback"] = 5
                    if projectile["type"] == "cross":
                        projectile["hit_enemy_ids"].append(id(enemy))
                    else:
                        hit_enemy = True
                        break

            if projectile["type"] == "holy_water" and not hit_enemy and projectile["lifetime"] <= 0:
                self.create_damage_zone(projectile["x"], projectile["y"], projectile["damage"], projectile["weapon_id"])
            elif projectile["type"] == "cross" and projectile["returning"]:
                dx = projectile["x"] - self.player_x
                dy = projectile["y"] - self.player_y
                if projectile["lifetime"] > 0 and dx * dx + dy * dy > 64:
                    kept_projectiles.append(projectile)
            elif not hit_enemy and projectile["lifetime"] > 0:
                kept_projectiles.append(projectile)

        self.projectile_list = kept_projectiles

    def update_enemy_projectiles(self):
        kept_projectiles = []
        for projectile in self.enemy_projectile_list:
            projectile["x"] += projectile["dx"]
            projectile["y"] += projectile["dy"]
            projectile["lifetime"] -= 1

            if self.dash_invincible <= 0 and self.player_invincible <= 0:
                if rect_overlap(projectile["x"] - 2, projectile["y"] - 2, 4, 4, self.player_x - 6, self.player_y - 6, 12, 12):
                    self.player_hp -= projectile["damage"]
                    self.player_invincible = 60
                    if self.player_hp <= 0:
                        self.state = "GAME_OVER"
                    continue

            if projectile["lifetime"] > 0:
                kept_projectiles.append(projectile)

        self.enemy_projectile_list = kept_projectiles

    def update_damage_zones(self):
        kept_zones = []
        for zone in self.damage_zone_list:
            if zone["timer"] % zone["tick_interval"] == 0:
                for enemy in self.enemy_list:
                    if enemy["hp"] <= 0:
                        continue
                    if rect_overlap(zone["x"], zone["y"], zone["width"], zone["height"], enemy["x"] - 6, enemy["y"] - 6, 12, 12):
                        enemy["hp"] -= zone["damage"]
            zone["timer"] -= 1
            if zone["timer"] > 0:
                kept_zones.append(zone)

        self.damage_zone_list = kept_zones

    def update_spawning(self):
        self.spawn_timer -= 1
        if self.spawn_timer > 0:
            self.enemy_count = len(self.enemy_list)
            return

        self.spawn_timer = self.spawn_interval
        if len(self.enemy_list) >= MAX_ENEMIES:
            self.enemy_count = len(self.enemy_list)
            return

        elapsed_seconds = self.timer_frames / 30
        available_enemies = [enemy for enemy in ENEMY_DATA if elapsed_seconds >= enemy[4]]
        type_id, _, base_hp, base_speed, _, _ = random.choice(available_enemies)
        angle = random.random() * math.tau
        diff = DIFFICULTY_DATA[self.difficulty]
        enemy = {
            "type": type_id,
            "x": self.player_x + math.cos(angle) * ENEMY_SPAWN_DISTANCE,
            "y": self.player_y + math.sin(angle) * ENEMY_SPAWN_DISTANCE,
            "hp": int(base_hp * diff["hp_mult"]),
            "speed": base_speed * diff["speed_mult"],
            "facing": 1,
            "anim_frame": 0,
            "ai_state": "chase",
            "knockback": 0,
        }
        if type_id == 1:
            enemy["zigzag_timer"] = 0
            enemy["zigzag_dx"] = 0.0
            enemy["zigzag_dy"] = 0.0
        elif type_id == 4:
            enemy["attack_timer"] = 0
        elif type_id == 5:
            enemy["wander_timer"] = 0
            enemy["wander_angle"] = random.uniform(0, math.tau)
        elif type_id == 6:
            enemy["summon_timer"] = 90
        elif type_id == 7:
            enemy["dash_timer"] = 0
            enemy["dash_active"] = False
            enemy["dash_frames"] = 0
        self.enemy_list.append(enemy)
        self.enemy_count = len(self.enemy_list)

    def update_enemies(self):
        active_radius_sq = ENEMY_ACTIVE_RADIUS * ENEMY_ACTIVE_RADIUS
        despawn_radius_sq = ENEMY_DESPAWN_RADIUS * ENEMY_DESPAWN_RADIUS
        kept_enemies = []
        added_enemies = 0

        for enemy in self.enemy_list:
            dx = self.player_x - enemy["x"]
            dy = self.player_y - enemy["y"]
            distance_sq = dx * dx + dy * dy
            if enemy["hp"] <= 0:
                if enemy["type"] == 5:
                    for i in range(2):
                        if len(self.enemy_list) + added_enemies >= MAX_ENEMIES:
                            break
                        kept_enemies.append({
                            "type": 8,
                            "x": enemy["x"] + i * 10 - 5,
                            "y": enemy["y"] + i * 10 - 5,
                            "hp": 1,
                            "speed": 0.8,
                            "facing": 1,
                            "anim_frame": 0,
                            "ai_state": "chase",
                            "knockback": 0,
                        })
                        added_enemies += 1
                gem_value = ENEMY_GEM_VALUES.get(enemy["type"], 1)
                self.gem_list.append({"x": enemy["x"], "y": enemy["y"], "value": gem_value})
                self.kills += 1
                continue
            if distance_sq > despawn_radius_sq:
                continue

            if enemy.get("knockback", 0) > 0 and enemy["type"] not in (2, 3):
                enemy["knockback"] -= 1
                kept_enemies.append(enemy)
                continue
            if enemy["type"] in (2, 3):
                enemy["knockback"] = 0

            if distance_sq <= active_radius_sq:
                distance = math.sqrt(distance_sq)
                if distance > 0:
                    enemy_type = enemy["type"]
                    base_dx = dx / distance
                    base_dy = dy / distance
                    if enemy_type == 1:
                        enemy["zigzag_timer"] = enemy.get("zigzag_timer", 0) + 1
                        if enemy["zigzag_timer"] % 10 == 0:
                            angle_offset = random.uniform(-0.8, 0.8)
                            cos_a = math.cos(angle_offset)
                            sin_a = math.sin(angle_offset)
                            enemy["zigzag_dx"] = base_dx * cos_a - base_dy * sin_a
                            enemy["zigzag_dy"] = base_dx * sin_a + base_dy * cos_a
                        move_dx = enemy.get("zigzag_dx") or base_dx
                        move_dy = enemy.get("zigzag_dy") or base_dy
                        enemy["x"] += move_dx * enemy["speed"]
                        enemy["y"] += move_dy * enemy["speed"]
                    elif enemy_type == 2:
                        enemy["x"] += base_dx * enemy["speed"]
                        enemy["y"] += base_dy * enemy["speed"]
                    elif enemy_type == 3:
                        enemy["x"] += base_dx * enemy["speed"]
                        enemy["y"] += base_dy * enemy["speed"]
                    elif enemy_type == 4:
                        if distance > 80:
                            enemy["x"] += base_dx * enemy["speed"]
                            enemy["y"] += base_dy * enemy["speed"]
                            enemy["attack_timer"] = 0
                        else:
                            enemy["attack_timer"] = enemy.get("attack_timer", 0) + 1
                            if enemy["attack_timer"] >= 90:
                                enemy["attack_timer"] = 0
                                self.enemy_projectile_list.append({
                                    "type": "enemy",
                                    "x": enemy["x"],
                                    "y": enemy["y"],
                                    "dx": base_dx * 2,
                                    "dy": base_dy * 2,
                                    "damage": 2,
                                    "lifetime": 120,
                                })
                    elif enemy_type == 5:
                        enemy["wander_timer"] = enemy.get("wander_timer", 0) + 1
                        if enemy["wander_timer"] >= 120:
                            enemy["wander_timer"] = 0
                            enemy["wander_angle"] = random.uniform(0, math.tau)
                        wander_angle = enemy.get("wander_angle", 0.0)
                        enemy["x"] += math.cos(wander_angle) * enemy["speed"]
                        enemy["y"] += math.sin(wander_angle) * enemy["speed"]
                    elif enemy_type == 6:
                        enemy["x"] += base_dx * enemy["speed"]
                        enemy["y"] += base_dy * enemy["speed"]
                        enemy["summon_timer"] = enemy.get("summon_timer", 90) + 1
                        if enemy["summon_timer"] >= 180:
                            enemy["summon_timer"] = 0
                            total_enemies = len(self.enemy_list) + added_enemies
                            to_summon = min(2, MAX_ENEMIES - total_enemies)
                            for _ in range(to_summon):
                                angle = random.uniform(0, math.tau)
                                summon_distance = random.uniform(60, 80)
                                kept_enemies.append({
                                    "type": 0,
                                    "x": enemy["x"] + math.cos(angle) * summon_distance,
                                    "y": enemy["y"] + math.sin(angle) * summon_distance,
                                    "hp": 3,
                                    "speed": 0.5,
                                    "facing": 1,
                                    "anim_frame": 0,
                                    "ai_state": "chase",
                                    "knockback": 0,
                                })
                                added_enemies += 1
                    elif enemy_type == 7:
                        if enemy.get("dash_active"):
                            enemy["x"] += base_dx * 8
                            enemy["y"] += base_dy * 8
                            enemy["dash_frames"] = enemy.get("dash_frames", 0) - 1
                            if enemy["dash_frames"] <= 0:
                                enemy["dash_active"] = False
                                enemy["dash_timer"] = 0
                        else:
                            enemy["x"] += base_dx * enemy["speed"]
                            enemy["y"] += base_dy * enemy["speed"]
                            enemy["dash_timer"] = enemy.get("dash_timer", 0) + 1
                            if enemy["dash_timer"] >= 120:
                                enemy["dash_active"] = True
                                enemy["dash_frames"] = 15
                    else:
                        enemy["x"] += base_dx * enemy["speed"]
                        enemy["y"] += base_dy * enemy["speed"]
                    enemy["facing"] = 1 if dx >= 0 else -1
                enemy["anim_frame"] = 1 if pyxel.frame_count % 30 >= 15 else 0
                enemy["ai_state"] = "chase"
            else:
                enemy["ai_state"] = "idle"

            if distance_sq <= 144 and self.dash_invincible <= 0 and self.player_invincible <= 0:
                damage = 3 if enemy["type"] == 7 and enemy.get("dash_active") else 1
                self.player_hp -= damage
                self.player_invincible = 60
                if self.player_hp <= 0:
                    self.state = "GAME_OVER"

            kept_enemies.append(enemy)

        self.enemy_list = kept_enemies
        self.enemy_count = len(self.enemy_list)

    def update_level_up(self):
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            self.level_up_cursor = (self.level_up_cursor - 1) % 3
        elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
            self.level_up_cursor = (self.level_up_cursor + 1) % 3
        elif pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_RETURN2):
            choice = self.level_up_choices[self.level_up_cursor]
            if choice["type"] == "passive":
                self.apply_passive_upgrade(choice["id"])
            elif choice["type"] == "weapon":
                self.apply_weapon_upgrade(choice["id"])
            elif choice["type"] == "stat":
                self.base_player_max_hp += 10
                self.recalculate_passive_stats()
            self.state = self.prev_state

    def apply_weapon_upgrade(self, weapon_id):
        if weapon_id in self.weapon_inventory:
            current_level = self.weapon_levels.get(weapon_id, 1)
            self.weapon_levels[weapon_id] = min(MAX_WEAPON_LEVEL, current_level + 1)
        elif len(self.weapon_inventory) < MAX_WEAPON_SLOTS:
            self.weapon_inventory.append(weapon_id)
            self.weapon_levels[weapon_id] = 1
            self.weapon_cooldowns[weapon_id] = 0
        self.check_evolution_ready()

    def apply_passive_upgrade(self, passive_id):
        for passive in self.passive_inventory:
            if passive["id"] == passive_id:
                passive["level"] = min(MAX_PASSIVE_LEVEL, passive["level"] + 1)
                self.recalculate_passive_stats()
                return

        if len(self.passive_inventory) < MAX_PASSIVE_SLOTS:
            self.passive_inventory.append({"id": passive_id, "level": 1})
            self.recalculate_passive_stats()

    def update_paused(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.state = "PLAYING"

    def update_boss(self):
        pass

    def update_game_over(self):
        pass

    def update_victory(self):
        pass

    def draw_title(self):
        pyxel.cls(0)
        
        pyxel.rectb(4, 4, 152, 112, 2)
        pyxel.rectb(6, 6, 148, 108, 8)
        
        self._draw_centered_text("VAMPIRE SURVIVORS", 40, 8)
        self._draw_centered_text("Pyxel Edition", 52, 5)
        
        if pyxel.frame_count % 30 < 15:
            self._draw_centered_text("PRESS ENTER TO START", 80, 7)

    def draw_char_select(self):
        pyxel.cls(0)
        self._draw_centered_text("SELECT CHARACTER", 4, 7)
        
        cards_per_row = 4
        card_w, card_h = 36, 22
        gap_x, gap_y = 4, 4
        start_x, start_y = 4, 20
        
        for i, char in enumerate(CHARACTER_DATA):
            col = i % cards_per_row
            row = i // cards_per_row
            x = start_x + col * (card_w + gap_x)
            y = start_y + row * (card_h + gap_y)
            
            pyxel.rect(x, y, card_w, card_h, char["color"])
            if i == self.char_cursor:
                pyxel.rectb(x - 1, y - 1, card_w + 2, card_h + 2, 10)
                
            pyxel.text(x + 2, y + 2, char["name"], 0)
            weapon_name = WEAPON_DATA[char["weapon"]]["name"][:6]
            pyxel.text(x + 2, y + 12, weapon_name, 7)

    def draw_diff_select(self):
        pyxel.cls(0)
        self._draw_centered_text("SELECT DIFFICULTY", 10, 7)
        
        cards_per_row = 3
        card_w, card_h = 46, 40
        gap_x = 4
        start_x = 6
        start_y = 30
        
        for i, diff in enumerate(DIFFICULTY_DATA):
            x = start_x + i * (card_w + gap_x)
            y = start_y
            
            pyxel.rect(x, y, card_w, card_h, 5)
            if i == self.diff_cursor:
                pyxel.rectb(x - 1, y - 1, card_w + 2, card_h + 2, 10)
                
            pyxel.text(x + 2, y + 4, diff["name"], 7)
            pyxel.text(x + 2, y + 14, diff["desc"], 6)
            pyxel.text(x + 2, y + 24, f"HP:{int(diff['hp_mult']*100)}%", 13)
            pyxel.text(x + 2, y + 32, f"SPD:{int(diff['speed_mult']*100)}%", 11)

    def draw_playing(self):
        pyxel.cls(0)
        self.draw_ground()
        cam_x = self.player_x - 80
        cam_y = self.player_y - 60
        frame_y = SPR_KNIGHT[1]
        if pyxel.frame_count % 30 >= 15:
            frame_y += 16
        self.draw_enemies(cam_x, cam_y)
        self.draw_projectiles(cam_x, cam_y)
        self.draw_enemy_projectiles(cam_x, cam_y)
        for gem in self.gem_list:
            screen_x = int(gem["x"] - cam_x - 2)
            screen_y = int(gem["y"] - cam_y - 2)
            pyxel.blt(screen_x, screen_y, 0, SPR_XP_GEM[0], SPR_XP_GEM[1], 4, 4, colkey=0)
        if self.whip_attack_timer > 0:
            whip_range = int(self.get_weapon_stats(0)["range"])
            whip_x = 80 if self.whip_attack_side > 0 else 80 - whip_range
            pyxel.rect(whip_x, 52, whip_range, 16, 8)
            self.whip_attack_timer -= 1
        if self.player_invincible <= 0 or pyxel.frame_count % 2 == 0:
            pyxel.blt(80 - 8, 60 - 8, 0, SPR_KNIGHT[0], frame_y, 16, 16, colkey=0)
        self.draw_hud()

    def draw_enemies(self, cam_x, cam_y):
        for enemy in self.enemy_list:
            if enemy["type"] == 2 and pyxel.frame_count % 6 >= 3:
                continue
            if enemy["type"] == 8:
                sprite_x, sprite_y = SPR_SLIME
            else:
                enemy_data = ENEMY_BY_TYPE[enemy["type"]]
                sprite_x, sprite_y = enemy_data[5]
            if enemy["anim_frame"] == 1:
                sprite_y += 16
            screen_x = int(enemy["x"] - cam_x - 8)
            screen_y = int(enemy["y"] - cam_y - 8)
            pyxel.blt(screen_x, screen_y, 0, sprite_x, sprite_y, 16, 16, colkey=0)

    def draw_projectiles(self, cam_x, cam_y):
        if 5 in self.weapon_inventory:
            garlic_range = int(self.get_weapon_stats(5)["range"])
            pyxel.circb(int(self.player_x - cam_x), int(self.player_y - cam_y), garlic_range, 10)

        for zone in self.damage_zone_list:
            if zone["timer"] % 6 < 3:
                screen_x = int(zone["x"] - cam_x)
                screen_y = int(zone["y"] - cam_y)
                pyxel.rect(screen_x, screen_y, zone["width"], zone["height"], 14)

        for projectile in self.projectile_list:
            if projectile["type"] == "wand":
                width = 4
                height = 4
                color = 12
            elif projectile["type"] == "axe":
                width = 8
                height = 8
                color = 4
            elif projectile["type"] == "holy_water":
                width = 6
                height = 6
                color = 14
            elif projectile["type"] == "cross":
                width = 6
                height = 6
                color = 10
            elif projectile["type"] == "fire_wand":
                width = 5
                height = 5
                color = 8
            else:
                width = 8
                height = 4
                color = 13
            screen_x = int(projectile["x"] - cam_x - width / 2)
            screen_y = int(projectile["y"] - cam_y - height / 2)
            pyxel.rect(screen_x, screen_y, width, height, color)

    def draw_enemy_projectiles(self, cam_x, cam_y):
        for projectile in self.enemy_projectile_list:
            screen_x = int(projectile["x"] - cam_x - 2)
            screen_y = int(projectile["y"] - cam_y - 2)
            pyxel.rect(screen_x, screen_y, 4, 4, 2)

    def draw_ground(self):
        cam_x = self.player_x - 80
        cam_y = self.player_y - 60
        biome, secondary_biome, blend_ratio = self.get_current_biome()
        self.biome = biome
        biome_tiles = [SPR_TILE_GRASS, SPR_TILE_DESERT, SPR_TILE_CAVE, SPR_TILE_CASTLE]
        tile_w, tile_h = 16, 16
        start_tx = int(cam_x // tile_w) - 1
        start_ty = int(cam_y // tile_h) - 1
        end_tx = start_tx + 12
        end_ty = start_ty + 9
        for ty in range(start_ty, end_ty):
            for tx in range(start_tx, end_tx):
                variant = tile_type(tx, ty)
                screen_x = tx * tile_w - int(cam_x)
                screen_y = ty * tile_h - int(cam_y)
                tile_hash = _tile_hash(tx, ty)
                active_biome = biome
                if secondary_biome != biome and tile_hash < blend_ratio * 0x100000000:
                    active_biome = secondary_biome
                sprite_x = biome_tiles[active_biome][0]
                sprite_y = biome_tiles[active_biome][1] + variant * 16
                pyxel.blt(screen_x, screen_y, 0, sprite_x, sprite_y, 16, 16)

    def get_current_biome(self):
        elapsed_seconds = self.timer_frames / 30
        transition_seconds = 30
        boundaries = [300, 600, 1200]

        for biome, boundary in enumerate(boundaries):
            transition_start = boundary - transition_seconds
            if elapsed_seconds < transition_start:
                return biome, biome, 0.0
            if elapsed_seconds < boundary:
                blend_ratio = (elapsed_seconds - transition_start) / transition_seconds
                return biome, biome + 1, blend_ratio

        return 3, 3, 0.0

    def draw_level_up(self):
        self.draw_playing()
        for y in range(0, 120, 2):
            pyxel.line(0, y, 160, y, 0)
            
        self._draw_centered_text("LEVEL UP!", 10, 10)
        
        card_w = 140
        card_h = 28
        start_x = (160 - card_w) // 2
        start_y = 25
        
        for i, choice in enumerate(self.level_up_choices):
            y = start_y + i * (card_h + 4)
            border_color = 10 if i == self.level_up_cursor else 5
            pyxel.rect(start_x, y, card_w, card_h, 0)
            pyxel.rectb(start_x, y, card_w, card_h, border_color)
            
            pyxel.text(start_x + 5, y + 5, choice["name"], 7)
            pyxel.text(start_x + 5, y + 15, choice["desc"], 13)

    def draw_paused(self):
        pyxel.cls(1)
        pyxel.text(64, 56, "PAUSED", 7)
        self.draw_hud()

    def draw_boss(self):
        pyxel.cls(0)
        pyxel.text(64, 56, "BOSS", 7)
        self.draw_hud()

    def draw_game_over(self):
        pyxel.cls(0)
        pyxel.text(52, 56, "GAME OVER", 7)

    def draw_victory(self):
        pyxel.cls(0)
        pyxel.text(60, 56, "VICTORY", 7)

    def draw_hud(self):
        # HP bar background (dark red)
        pyxel.rect(2, 2, 50, 4, 0)  # bg
        # HP bar fill (red, width proportional to hp/max_hp)
        hp_w = int(50 * self.player_hp / self.player_max_hp) if self.player_max_hp > 0 else 0
        pyxel.rect(2, 2, hp_w, 4, 8)
        # XP bar background
        pyxel.rect(2, 8, 50, 3, 0)
        # XP bar fill (blue/cyan)
        xp_w = int(50 * self.player_xp / self.player_xp_next) if self.player_xp_next > 0 else 0
        pyxel.rect(2, 8, min(xp_w, 50), 3, 12)
        # Level text
        pyxel.text(54, 7, f"Lv.{self.player_level}", 7)
        pyxel.blt(2, 13, 0, SPR_GEM[0], SPR_GEM[1], 16, 16, colkey=0)
        pyxel.rect(20, 18, 40, 4, 1)
        cooldown_w = int(40 * self.dash_cooldown / 60)
        pyxel.rect(20, 18, cooldown_w, 4, 12)
        # Timer MM:SS (top right)
        total_sec = self.timer_frames // 30
        mins = total_sec // 60
        secs = total_sec % 60
        pyxel.text(128, 2, f"{mins:02d}:{secs:02d}", 7)

    def _draw_centered_text(self, text, y, color):
        pyxel.text((pyxel.width - len(text) * 4) // 2, y, text, color)


App()
