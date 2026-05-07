
import math
import random

import pyxel


SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
FPS = 30

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
BOSS_SPAWN_FRAMES = 30 * 60 * FPS
BOSS_WARNING_FRAMES = 2 * FPS

DASH_COOLDOWN_FRAMES = 60
HP_REGEN_INTERVAL_FRAMES = 180
SFX_COOLDOWN_FRAMES = 10
WHIP_ATTACK_FRAMES = 10
BOSS_ATTACK_INTERVAL = 120
BOSS_SUMMON_INTERVAL = 600
GARLIC_TICK_INTERVAL = 30
DARK_MAGE_ATTACK_INTERVAL = 90
SLIME_WANDER_INTERVAL = 120
NECROMANCER_SUMMON_INTERVAL = 180
DEMON_DASH_INTERVAL = 120
DEMON_DASH_DURATION = 15
SOUL_EATER_TICK_INTERVAL = 20

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

EVOLVED_WEAPON_DATA = {
    8: {"name": "Bloody Tear", "base": 0, "cooldown": 40, "damage": 12, "range": 40, "type": "melee", "effect": "lifesteal"},
    9: {"name": "Holy Wand", "base": 1, "cooldown": 35, "damage": 9, "range": 150, "type": "projectile", "effect": "pierce"},
    10: {"name": "Death Spiral", "base": 2, "cooldown": 45, "damage": 14, "range": 80, "type": "projectile", "effect": "pierce"},
    11: {"name": "Thousand Edge", "base": 3, "cooldown": 12, "damage": 5, "range": 120, "type": "projectile", "effect": "multi"},
    12: {"name": "Boros Sea", "base": 4, "cooldown": 75, "damage": 12, "range": 100, "type": "projectile", "effect": "big_zone"},
    13: {"name": "Soul Eater", "base": 5, "cooldown": 0, "damage": 4, "range": 55, "type": "aura", "effect": "heal"},
    14: {"name": "Hyperlove", "base": 6, "cooldown": 50, "damage": 10, "range": 100, "type": "projectile", "effect": "multi_return"},
    15: {"name": "Hellfire", "base": 7, "cooldown": 45, "damage": 9, "range": 120, "type": "projectile", "effect": "pierce_burn"},
}

EVOLUTION_MAP = {0: 8, 1: 9, 2: 10, 3: 11, 4: 12, 5: 13, 6: 14, 7: 15}

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
    {"type": "weapon", "id": 8, "name": "Bloody Tear", "desc": "Evolved whip with lifesteal"},
    {"type": "weapon", "id": 9, "name": "Holy Wand", "desc": "Evolved wand with piercing"},
    {"type": "weapon", "id": 10, "name": "Death Spiral", "desc": "Evolved axe with piercing"},
    {"type": "weapon", "id": 11, "name": "Thousand Edge", "desc": "Evolved knife barrage"},
    {"type": "weapon", "id": 12, "name": "Boros Sea", "desc": "Evolved holy water zone"},
    {"type": "weapon", "id": 13, "name": "Soul Eater", "desc": "Evolved garlic aura"},
    {"type": "weapon", "id": 14, "name": "Hyperlove", "desc": "Evolved returning cross"},
    {"type": "weapon", "id": 15, "name": "Hellfire", "desc": "Evolved piercing fireball"},
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
        self.boss = None
        self.boss_hp = 0
        self.boss_max_hp = 0
        self.boss_warning_timer = 0
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
        self.debug_overlay = False
        self.score_calculated = False
        self.is_new_high_score = False
        self.final_score = 0

        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Vampire Survivors", fps=FPS)
        self.sfx_cooldowns = {0: 0, 1: 0, 2: 0}
        pyxel.sound(0).set("g4 c4", "pp", "77", "n", 2)  # type: ignore[attr-defined]
        pyxel.sound(1).set("c3 e3", "ss", "77", "n", 2)  # type: ignore[attr-defined]
        pyxel.sound(2).set("c3 e3 g3", "ppp", "777", "nnn", 3)  # type: ignore[attr-defined]
        self._load_sprite_bank()
        self.state = "PLAYING"
        self._apply_selections()
        self.spawn_timer = 9999
        self.enemy_list = [{"type": 0, "x": 20.0, "y": 0.0, "hp": 1, "speed": 0.0, "facing": 1, "anim_frame": 0, "ai_state": "chase", "knockback": 0}]
        self.enemy_count = 1
        pyxel.run(self.update, self.draw)

    def _load_sprite_bank(self):
        image = pyxel.images[0]
        for (x, y), data in SPRITE_BANK.items():
            image.set(x, y, data)

    def _tick_sfx_cooldowns(self):
        for sound_id in self.sfx_cooldowns:
            self.sfx_cooldowns[sound_id] = max(0, self.sfx_cooldowns[sound_id] - 1)

    def play_sfx(self, sound_id):
        if self.sfx_cooldowns.get(sound_id, 0) > 0:
            return
        pyxel.play(sound_id % 4, sound_id)
        self.sfx_cooldowns[sound_id] = SFX_COOLDOWN_FRAMES

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

    def get_time_scaling(self):
        minutes = self.timer_frames / (30 * 60)
        intervals = int(minutes // 5)
        hp_scale = 1.0 + intervals * 0.10
        speed_scale = 1.0 + intervals * 0.10
        spawn_scale = max(0.3, 1.0 - intervals * 0.10)
        return hp_scale, speed_scale, spawn_scale

    def update_debug_controls(self):
        if pyxel.btnp(pyxel.KEY_F1):
            self.debug_time_scale = min(100, self.debug_time_scale * 2)
        elif pyxel.btnp(pyxel.KEY_F2):
            self.debug_time_scale = max(1, self.debug_time_scale // 2)
        elif pyxel.btnp(pyxel.KEY_F3):
            self.debug_time_scale = 1
        elif pyxel.btnp(pyxel.KEY_F4):
            self.debug_overlay = not self.debug_overlay

    def update_playing(self):
        self._tick_sfx_cooldowns()
        self.update_debug_controls()
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.prev_state = self.state
            self.state = "PAUSED"
            return

        self.timer_frames += self.debug_time_scale
        self.biome = self.get_current_biome()[0]
        if self.boss_warning_timer > 0:
            self.boss_warning_timer -= 1
            if self.boss_warning_timer <= 0:
                self.start_boss_fight()
            return
        if self.timer_frames >= BOSS_SPAWN_FRAMES and not self.boss_active:
            self.boss_warning_timer = BOSS_WARNING_FRAMES
            return

        self.update_active_game(allow_spawning=True)

    def update_active_game(self, allow_spawning):
        self.dash_cooldown = max(0, self.dash_cooldown - 1)
        self.dash_invincible = max(0, self.dash_invincible - 1)
        self.player_invincible = max(0, self.player_invincible - 1)
        if self.whip_attack_timer > 0:
            self.whip_attack_timer -= 1
        if self.hp_regen > 0:
            self.hp_regen_timer += 1
            if self.hp_regen_timer >= HP_REGEN_INTERVAL_FRAMES:
                self.hp_regen_timer -= HP_REGEN_INTERVAL_FRAMES
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
            self.dash_cooldown = DASH_COOLDOWN_FRAMES
            self.dash_invincible = 10

        if allow_spawning:
            self.update_spawning()
        self.update_enemies()
        self.update_boss_entity()
        self.update_enemy_projectiles()
        self.update_weapons()
        self.update_projectiles()
        self.update_damage_zones()
        self.update_gems()
        self.check_level_up()

    def start_boss_fight(self):
        diff = DIFFICULTY_DATA[self.difficulty]
        boss_hp = int(500 * diff["hp_mult"])
        self.enemy_list.clear()
        self.enemy_count = 0
        self.boss = {
            "x": self.player_x,
            "y": self.player_y - 60,
            "hp": boss_hp,
            "max_hp": boss_hp,
            "speed": 0.5 * diff["speed_mult"],
            "facing": 1,
            "attack_timer": 0,
            "summon_timer": 0,
            "flash_timer": 0,
        }
        self.boss_hp = boss_hp
        self.boss_max_hp = boss_hp
        self.boss_active = True
        self.state = "BOSS"

    def update_boss_entity(self):
        if not self.boss_active or self.boss is None:
            return
        if self.boss["hp"] <= 0:
            self.defeat_boss()
            return

        dx = self.player_x - self.boss["x"]
        dy = self.player_y - self.boss["y"]
        distance = math.sqrt(dx * dx + dy * dy)
        if distance > 0:
            self.boss["x"] += dx / distance * self.boss["speed"]
            self.boss["y"] += dy / distance * self.boss["speed"]
            self.boss["facing"] = 1 if dx >= 0 else -1

        self.boss["attack_timer"] += 1
        if self.boss["attack_timer"] >= BOSS_ATTACK_INTERVAL:
            self.boss["attack_timer"] = 0
            self.fire_boss_projectiles(dx, dy, distance)

        self.boss["summon_timer"] += 1
        if self.boss["summon_timer"] >= BOSS_SUMMON_INTERVAL:
            self.boss["summon_timer"] = 0
            self.summon_boss_minions()

        self.boss["flash_timer"] = max(0, self.boss["flash_timer"] - 1)
        self.boss_hp = max(0, int(self.boss["hp"]))
        self.boss_max_hp = int(self.boss["max_hp"])
        if distance <= 22 and self.dash_invincible <= 0 and self.player_invincible <= 0:
            self.player_hp -= 5
            self.player_invincible = 60
            if self.player_hp <= 0:
                self.state = "GAME_OVER"

    def fire_boss_projectiles(self, dx, dy, distance):
        if self.boss is None:
            return
        if distance == 0:
            dx = 1.0
            dy = 0.0
            distance = 1.0

        base_dx = dx / distance
        base_dy = dy / distance
        speed = 1.5
        for angle in (-0.22, 0, 0.22):
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            shot_dx = base_dx * cos_a - base_dy * sin_a
            shot_dy = base_dx * sin_a + base_dy * cos_a
            self.enemy_projectile_list.append({
                "type": "boss_homing",
                "x": self.boss["x"],
                "y": self.boss["y"],
                "dx": shot_dx * speed,
                "dy": shot_dy * speed,
                "speed": speed,
                "homing": 0.02,
                "damage": 2,
                "lifetime": 300,
            })

    def summon_boss_minions(self):
        if self.boss is None:
            return
        summon_counts = [2, 3, 4]
        desired_count = summon_counts[self.difficulty]
        room = MAX_ENEMIES - 1 - len(self.enemy_list)
        summon_count = min(desired_count, room)
        if summon_count <= 0:
            return

        diff = DIFFICULTY_DATA[self.difficulty]
        time_hp_scale, time_speed_scale, _ = self.get_time_scaling()
        _, _, base_hp, base_speed, _, _ = ENEMY_BY_TYPE[0]
        for index in range(summon_count):
            angle = math.tau * index / summon_count + random.uniform(-0.35, 0.35)
            distance = random.uniform(24, 32)
            self.enemy_list.append({
                "type": 0,
                "x": self.boss["x"] + math.cos(angle) * distance,
                "y": self.boss["y"] + math.sin(angle) * distance,
                "hp": int(base_hp * diff["hp_mult"] * time_hp_scale),
                "speed": base_speed * diff["speed_mult"] * time_speed_scale,
                "facing": 1,
                "anim_frame": 0,
                "ai_state": "chase",
                "knockback": 0,
            })
        self.enemy_count = len(self.enemy_list)

    def defeat_boss(self):
        self.boss_hp = 0
        self.boss_active = False
        self.enemy_projectile_list.clear()
        self.state = "VICTORY"

    def damage_boss(self, damage):
        if not self.boss_active or self.boss is None or self.boss["hp"] <= 0:
            return
        self.boss["hp"] = max(0, self.boss["hp"] - damage)
        self.boss["flash_timer"] = 10
        self.boss_hp = max(0, int(self.boss["hp"]))
        if self.boss["hp"] <= 0:
            self.defeat_boss()

    def projectile_hits_boss(self, projectile, projectile_x, projectile_y, width, height):
        if not self.boss_active or self.boss is None or self.boss["hp"] <= 0:
            return False
        if projectile["type"] in ("cross", "hyperlove", "holy_wand", "death_spiral", "hellfire") and id(self.boss) in projectile["hit_enemy_ids"]:
            return False
        if not rect_overlap(projectile_x, projectile_y, width, height, self.boss["x"] - 16, self.boss["y"] - 16, 32, 32):
            return False

        if projectile["type"] == "holy_water":
            self.create_damage_zone(projectile["x"], projectile["y"], projectile["damage"], projectile["weapon_id"])
            return True
        self.damage_boss(projectile["damage"])
        if projectile["type"] in ("cross", "hyperlove", "holy_wand", "death_spiral", "hellfire"):
            projectile["hit_enemy_ids"].append(id(self.boss))
            return False
        return True

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
                elif weapon_id == 8:
                    self.fire_bloody_tear()
                elif weapon_id == 9:
                    self.fire_holy_wand()
                elif weapon_id == 10:
                    self.fire_death_spiral()
                elif weapon_id == 11:
                    self.fire_thousand_edge()
                elif weapon_id == 12:
                    self.fire_boros_sea()
                elif weapon_id == 13:
                    self.fire_soul_eater()
                elif weapon_id == 14:
                    self.fire_hyperlove()
                elif weapon_id == 15:
                    self.fire_hellfire()

    def get_passive_level(self, passive_id):
        for passive in self.passive_inventory:
            if passive["id"] == passive_id:
                return passive["level"]
        return 0

    def get_weapon_stats(self, weapon_id):
        weapon = EVOLVED_WEAPON_DATA[weapon_id] if weapon_id in EVOLVED_WEAPON_DATA else WEAPON_DATA[weapon_id]
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

    def check_evolution(self):
        evolutions = []
        for weapon_id in self.weapon_inventory:
            if weapon_id not in EVOLUTION_REQUIREMENTS:
                continue
            requirement = EVOLUTION_REQUIREMENTS[weapon_id]
            weapon_level = self.weapon_levels.get(weapon_id, 0)
            passive_level = self.get_passive_level(requirement["passive_id"])
            if weapon_level >= requirement["weapon_level"] and passive_level >= requirement["passive_level"]:
                evolutions.append((weapon_id, EVOLUTION_MAP[weapon_id]))
        return evolutions

    def check_evolution_ready(self):
        self.evolution_ready = [base_weapon_id for base_weapon_id, _ in self.check_evolution()]

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
        self.play_sfx(2)
        self.state = "LEVEL_UP"

    def generate_level_up_choices(self):
        candidates = []
        available_evolutions = self.check_evolution()
        for passive_upgrade in PASSIVE_POOL:
            passive_level = self.get_passive_level(passive_upgrade["id"])
            if passive_level > 0 and passive_level < MAX_PASSIVE_LEVEL:
                candidates.append(passive_upgrade)
            elif passive_level == 0 and len(self.passive_inventory) < MAX_PASSIVE_SLOTS:
                candidates.append(passive_upgrade)

        for weapon_upgrade in UPGRADE_POOL:
            weapon_id = weapon_upgrade["id"]
            if weapon_id in EVOLVED_WEAPON_DATA and weapon_id not in self.weapon_inventory:
                continue
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

        if available_evolutions:
            base_weapon_id, evolved_weapon_id = random.choice(available_evolutions)
            base_name = WEAPON_DATA[base_weapon_id]["name"]
            evolved_name = EVOLVED_WEAPON_DATA[evolved_weapon_id]["name"]
            evolution_choice = {
                "type": "evolution",
                "base_id": base_weapon_id,
                "evolved_id": evolved_weapon_id,
                "name": f"EVOLVE: {base_name} -> {evolved_name}",
                "desc": "Replace weapon with evolved form",
            }
            if self.level_up_choices:
                self.level_up_choices[0] = evolution_choice
            else:
                self.level_up_choices = [evolution_choice]
                
        self.level_up_cursor = 0

    def fire_whip(self):
        weapon = self.get_weapon_stats(0)
        self.weapon_cooldowns[0] = weapon["cooldown"]
        self.play_sfx(0)
        self.whip_attack_side = self.whip_next_attack_side
        self.whip_next_attack_side *= -1
        self.whip_attack_timer = WHIP_ATTACK_FRAMES

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
                if enemy["hp"] <= 0:
                    self.play_sfx(1)
                dx = enemy["x"] - self.player_x
                dy = enemy["y"] - self.player_y
                distance_sq = dx * dx + dy * dy
                dist = math.sqrt(distance_sq) if distance_sq > 0 else 1
                enemy["x"] += dx / dist * 15
                enemy["y"] += dy / dist * 15
                enemy["knockback"] = 5
        if self.boss_active and self.boss is not None:
            if rect_overlap(min_x, min_y, max_x - min_x, max_y - min_y, self.boss["x"] - 16, self.boss["y"] - 16, 32, 32):
                self.damage_boss(weapon["damage"])

    def fire_magic_wand(self):
        weapon_id = 1
        weapon = self.get_weapon_stats(weapon_id)
        self.weapon_cooldowns[weapon_id] = weapon["cooldown"]
        targets = list(self.enemy_list)
        if self.boss_active and self.boss is not None and self.boss["hp"] > 0:
            targets.append(self.boss)
        if not targets:
            return

        self.play_sfx(0)

        target = min(
            targets,
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
        self.play_sfx(0)
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
        self.play_sfx(0)
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
        self.play_sfx(0)
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
        if self.garlic_tick_timer < GARLIC_TICK_INTERVAL:
            return
        self.garlic_tick_timer -= GARLIC_TICK_INTERVAL

        self.play_sfx(0)
        range_sq = weapon["range"] * weapon["range"]
        for enemy in self.enemy_list:
            if enemy["hp"] <= 0:
                continue
            dx = enemy["x"] - self.player_x
            dy = enemy["y"] - self.player_y
            distance_sq = dx * dx + dy * dy
            if distance_sq <= range_sq:
                enemy["hp"] -= weapon["damage"]
                if enemy["hp"] <= 0:
                    self.play_sfx(1)
        if self.boss_active and self.boss is not None:
            dx = self.boss["x"] - self.player_x
            dy = self.boss["y"] - self.player_y
            if dx * dx + dy * dy <= range_sq:
                self.damage_boss(weapon["damage"])

    def fire_cross(self):
        weapon_id = 6
        weapon = self.get_weapon_stats(weapon_id)
        self.weapon_cooldowns[weapon_id] = weapon["cooldown"]
        self.play_sfx(0)
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
        self.fire_targeted_projectile(7, "fire_wand", 3)

    def fire_targeted_projectile(self, weapon_id, projectile_type, speed):
        weapon = self.get_weapon_stats(weapon_id)
        self.weapon_cooldowns[weapon_id] = weapon["cooldown"]
        targets = list(self.enemy_list)
        if self.boss_active and self.boss is not None and self.boss["hp"] > 0:
            targets.append(self.boss)
        if not targets:
            return

        self.play_sfx(0)

        target = min(
            targets,
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

        projectile_speed = speed * self.projectile_speed_mult
        projectile = {
            "type": projectile_type,
            "x": self.player_x,
            "y": self.player_y,
            "dx": dx / distance * projectile_speed,
            "dy": dy / distance * projectile_speed,
            "damage": weapon["damage"],
            "lifetime": max(1, int(weapon["range"] / projectile_speed)),
            "weapon_id": weapon_id,
            "gravity": 0,
        }
        if projectile_type in ("fire_wand", "hellfire"):
            projectile["explosion_damage"] = 4 * WEAPON_LEVELS[self.weapon_levels.get(weapon_id, 1)]["damage_mult"] * self.weapon_damage_mult
        if projectile_type in ("holy_wand", "hellfire"):
            projectile["hit_enemy_ids"] = []
        self.projectile_list.append(projectile)

    def fire_bloody_tear(self):
        weapon_id = 8
        weapon = self.get_weapon_stats(weapon_id)
        self.weapon_cooldowns[weapon_id] = weapon["cooldown"]
        self.play_sfx(0)
        self.whip_attack_side = self.whip_next_attack_side
        self.whip_next_attack_side *= -1
        self.whip_attack_timer = WHIP_ATTACK_FRAMES

        attack_range = weapon["range"]
        if self.whip_attack_side > 0:
            min_x = self.player_x
            max_x = self.player_x + attack_range
        else:
            min_x = self.player_x - attack_range
            max_x = self.player_x
        min_y = self.player_y - 20
        max_y = self.player_y + 20
        hit_count = 0

        for enemy in self.enemy_list:
            enemy_hitbox_x = enemy["x"] - 6
            enemy_hitbox_y = enemy["y"] - 6
            if rect_overlap(min_x, min_y, max_x - min_x, max_y - min_y, enemy_hitbox_x, enemy_hitbox_y, 12, 12):
                enemy["hp"] -= weapon["damage"]
                if enemy["hp"] <= 0:
                    self.play_sfx(1)
                hit_count += 1
                dx = enemy["x"] - self.player_x
                dy = enemy["y"] - self.player_y
                distance_sq = dx * dx + dy * dy
                dist = math.sqrt(distance_sq) if distance_sq > 0 else 1
                enemy["x"] += dx / dist * 18
                enemy["y"] += dy / dist * 18
                enemy["knockback"] = 5
        if hit_count > 0:
            self.player_hp = min(self.player_max_hp, self.player_hp + hit_count)
        if self.boss_active and self.boss is not None:
            if rect_overlap(min_x, min_y, max_x - min_x, max_y - min_y, self.boss["x"] - 16, self.boss["y"] - 16, 32, 32):
                self.damage_boss(weapon["damage"])
                self.player_hp = min(self.player_max_hp, self.player_hp + 1)

    def fire_holy_wand(self):
        self.fire_targeted_projectile(9, "holy_wand", 4)

    def fire_death_spiral(self):
        weapon_id = 10
        weapon = self.get_weapon_stats(weapon_id)
        self.weapon_cooldowns[weapon_id] = weapon["cooldown"]
        self.play_sfx(0)
        speed = 2.5 * self.projectile_speed_mult
        for angle in (0, math.pi / 2, math.pi, math.pi * 1.5):
            self.projectile_list.append({
                "type": "death_spiral",
                "x": self.player_x,
                "y": self.player_y,
                "dx": math.cos(angle) * speed,
                "dy": math.sin(angle) * speed,
                "damage": weapon["damage"],
                "lifetime": max(1, int(weapon["range"] / speed)),
                "weapon_id": weapon_id,
                "gravity": 0,
                "hit_enemy_ids": [],
            })

    def fire_thousand_edge(self):
        weapon_id = 11
        weapon = self.get_weapon_stats(weapon_id)
        self.weapon_cooldowns[weapon_id] = weapon["cooldown"]
        self.play_sfx(0)
        length = math.sqrt(self.facing_x * self.facing_x + self.facing_y * self.facing_y)
        base_dx, base_dy = (1.0, 0.0) if length == 0 else (self.facing_x / length, self.facing_y / length)
        speed = 4.8 * self.projectile_speed_mult
        for spread in (-0.16, 0, 0.16):
            cos_a = math.cos(spread)
            sin_a = math.sin(spread)
            dx = base_dx * cos_a - base_dy * sin_a
            dy = base_dx * sin_a + base_dy * cos_a
            self.projectile_list.append({
                "type": "thousand_edge",
                "x": self.player_x,
                "y": self.player_y,
                "dx": dx * speed,
                "dy": dy * speed,
                "damage": weapon["damage"],
                "lifetime": max(1, int(weapon["range"] / speed)),
                "weapon_id": weapon_id,
                "gravity": 0,
            })

    def fire_boros_sea(self):
        weapon_id = 12
        weapon = self.get_weapon_stats(weapon_id)
        self.weapon_cooldowns[weapon_id] = weapon["cooldown"]
        self.play_sfx(0)
        angle = random.random() * math.tau
        distance = min(weapon["range"], 48)
        self.create_damage_zone(
            self.player_x + math.cos(angle) * distance,
            self.player_y + math.sin(angle) * distance,
            weapon["damage"],
            weapon_id,
            size=40,
            timer=45,
            tick_interval=8,
        )

    def fire_soul_eater(self):
        weapon_id = 13
        weapon = self.get_weapon_stats(weapon_id)
        self.garlic_tick_timer += 1
        if self.garlic_tick_timer < SOUL_EATER_TICK_INTERVAL:
            return
        self.garlic_tick_timer -= SOUL_EATER_TICK_INTERVAL

        self.play_sfx(0)
        range_sq = weapon["range"] * weapon["range"]
        hit_count = 0
        for enemy in self.enemy_list:
            if enemy["hp"] <= 0:
                continue
            dx = enemy["x"] - self.player_x
            dy = enemy["y"] - self.player_y
            if dx * dx + dy * dy <= range_sq:
                enemy["hp"] -= weapon["damage"]
                if enemy["hp"] <= 0:
                    self.play_sfx(1)
                hit_count += 1
        if self.boss_active and self.boss is not None:
            dx = self.boss["x"] - self.player_x
            dy = self.boss["y"] - self.player_y
            if dx * dx + dy * dy <= range_sq:
                self.damage_boss(weapon["damage"])
                hit_count += 1
        if hit_count > 0:
            self.player_hp = min(self.player_max_hp, self.player_hp + 1)

    def fire_hyperlove(self):
        weapon_id = 14
        weapon = self.get_weapon_stats(weapon_id)
        self.weapon_cooldowns[weapon_id] = weapon["cooldown"]
        self.play_sfx(0)
        length = math.sqrt(self.facing_x * self.facing_x + self.facing_y * self.facing_y)
        dx, dy = (1.0, 0.0) if length == 0 else (self.facing_x / length, self.facing_y / length)
        speed = 3 * self.projectile_speed_mult
        for side in (-1, 1):
            self.projectile_list.append({
                "type": "hyperlove",
                "x": self.player_x,
                "y": self.player_y,
                "dx": dx * speed + -dy * side * 0.6,
                "dy": dy * speed + dx * side * 0.6,
                "damage": weapon["damage"],
                "lifetime": max(1, int(weapon["range"] * 2 / speed) + 10),
                "weapon_id": weapon_id,
                "gravity": 0,
                "traveled": 0.0,
                "max_range": weapon["range"],
                "returning": False,
                "hit_enemy_ids": [],
            })

    def fire_hellfire(self):
        self.fire_targeted_projectile(15, "hellfire", 3.2)

    def create_damage_zone(self, x, y, damage, weapon_id, size=24, timer=30, tick_interval=10):
        self.damage_zone_list.append({
            "x": x - size / 2,
            "y": y - size / 2,
            "width": size,
            "height": size,
            "damage": damage,
            "timer": timer,
            "tick_interval": tick_interval,
            "weapon_id": weapon_id,
        })

    def update_projectiles(self):
        kept_projectiles = []
        for projectile in self.projectile_list:
            projectile["dy"] += projectile["gravity"]
            projectile["x"] += projectile["dx"]
            projectile["y"] += projectile["dy"]
            projectile["lifetime"] -= 1

            if projectile["type"] in ("cross", "hyperlove"):
                step_distance = math.sqrt(projectile["dx"] * projectile["dx"] + projectile["dy"] * projectile["dy"])
                projectile["traveled"] += step_distance
                if not projectile["returning"] and projectile["traveled"] >= projectile["max_range"]:
                    projectile["dx"] *= -1
                    projectile["dy"] *= -1
                    projectile["returning"] = True
                    projectile["hit_enemy_ids"] = []

            if projectile["type"] in ("axe", "death_spiral"):
                width = 16
                height = 16
            elif projectile["type"] in ("knife", "thousand_edge"):
                width = 8
                height = 4
            elif projectile["type"] == "holy_water":
                width = 6
                height = 6
            elif projectile["type"] == "cross":
                width = 6
                height = 6
            elif projectile["type"] == "hyperlove":
                width = 8
                height = 8
            elif projectile["type"] in ("fire_wand", "hellfire"):
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
                if projectile["type"] in ("cross", "hyperlove", "holy_wand", "death_spiral", "hellfire") and id(enemy) in projectile["hit_enemy_ids"]:
                    continue
                if rect_overlap(projectile_x, projectile_y, width, height, enemy["x"] - 6, enemy["y"] - 6, 12, 12):
                    if projectile["type"] == "holy_water":
                        self.create_damage_zone(projectile["x"], projectile["y"], projectile["damage"], projectile["weapon_id"])
                        hit_enemy = True
                        break
                    if projectile["type"] in ("fire_wand", "hellfire"):
                        enemy["hp"] -= projectile["damage"]
                        if enemy["hp"] <= 0:
                            self.play_sfx(1)
                        dx = enemy["x"] - self.player_x
                        dy = enemy["y"] - self.player_y
                        distance_sq = dx * dx + dy * dy
                        dist = math.sqrt(distance_sq) if distance_sq > 0 else 1
                        enemy["x"] += dx / dist * 15
                        enemy["y"] += dy / dist * 15
                        enemy["knockback"] = 5
                        explosion_range_sq = (32 if projectile["type"] == "hellfire" else 24) ** 2
                        for splash_enemy in self.enemy_list:
                            if splash_enemy["hp"] <= 0:
                                continue
                            splash_dx = splash_enemy["x"] - projectile["x"]
                            splash_dy = splash_enemy["y"] - projectile["y"]
                            if splash_dx * splash_dx + splash_dy * splash_dy <= explosion_range_sq:
                                splash_enemy["hp"] -= projectile["explosion_damage"]
                                if splash_enemy["hp"] <= 0:
                                    self.play_sfx(1)
                        if projectile["type"] == "hellfire":
                            projectile["hit_enemy_ids"].append(id(enemy))
                        else:
                            hit_enemy = True
                            break
                        continue

                    enemy["hp"] -= projectile["damage"]
                    if enemy["hp"] <= 0:
                        self.play_sfx(1)
                    dx = enemy["x"] - self.player_x
                    dy = enemy["y"] - self.player_y
                    distance_sq = dx * dx + dy * dy
                    dist = math.sqrt(distance_sq) if distance_sq > 0 else 1
                    enemy["x"] += dx / dist * 15
                    enemy["y"] += dy / dist * 15
                    enemy["knockback"] = 5
                    if projectile["type"] in ("cross", "hyperlove", "holy_wand", "death_spiral"):
                        projectile["hit_enemy_ids"].append(id(enemy))
                    else:
                        hit_enemy = True
                        break

            if not hit_enemy:
                hit_enemy = self.projectile_hits_boss(projectile, projectile_x, projectile_y, width, height)

            if projectile["type"] == "holy_water" and not hit_enemy and projectile["lifetime"] <= 0:
                self.create_damage_zone(projectile["x"], projectile["y"], projectile["damage"], projectile["weapon_id"])
            elif projectile["type"] in ("cross", "hyperlove") and projectile["returning"]:
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
            if projectile.get("type") == "boss_homing":
                dx = self.player_x - projectile["x"]
                dy = self.player_y - projectile["y"]
                distance = math.sqrt(dx * dx + dy * dy)
                if distance > 0:
                    projectile["dx"] += dx / distance * projectile["homing"]
                    projectile["dy"] += dy / distance * projectile["homing"]
                    speed = projectile["speed"]
                    current_speed = math.sqrt(projectile["dx"] * projectile["dx"] + projectile["dy"] * projectile["dy"])
                    if current_speed > 0:
                        projectile["dx"] = projectile["dx"] / current_speed * speed
                        projectile["dy"] = projectile["dy"] / current_speed * speed

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
                        if enemy["hp"] <= 0:
                            self.play_sfx(1)
                if self.boss_active and self.boss is not None:
                    if rect_overlap(zone["x"], zone["y"], zone["width"], zone["height"], self.boss["x"] - 16, self.boss["y"] - 16, 32, 32):
                        self.damage_boss(zone["damage"])
            zone["timer"] -= 1
            if zone["timer"] > 0:
                kept_zones.append(zone)

        self.damage_zone_list = kept_zones

    def update_spawning(self):
        self.spawn_timer -= 1
        if self.spawn_timer > 0:
            self.enemy_count = len(self.enemy_list)
            return

        elapsed_seconds = self.timer_frames / 30
        available_enemies = [enemy for enemy in ENEMY_DATA if elapsed_seconds >= enemy[4]]
        type_id, _, base_hp, base_speed, _, _ = random.choice(available_enemies)
        angle = random.random() * math.tau
        diff = DIFFICULTY_DATA[self.difficulty]
        time_hp_scale, time_speed_scale, time_spawn_scale = self.get_time_scaling()
        self.spawn_interval = max(10, int(SPAWN_INTERVAL_FRAMES * diff["spawn_mult"] * time_spawn_scale))

        if len(self.enemy_list) >= MAX_ENEMIES:
            self.spawn_timer = self.spawn_interval
            self.enemy_count = len(self.enemy_list)
            return
        self.spawn_timer = self.spawn_interval
        enemy = {
            "type": type_id,
            "x": self.player_x + math.cos(angle) * ENEMY_SPAWN_DISTANCE,
            "y": self.player_y + math.sin(angle) * ENEMY_SPAWN_DISTANCE,
            "hp": int(base_hp * diff["hp_mult"] * time_hp_scale),
            "speed": base_speed * diff["speed_mult"] * time_speed_scale,
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
                self.play_sfx(1)
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
                            if enemy["attack_timer"] >= DARK_MAGE_ATTACK_INTERVAL:
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
                        if enemy["wander_timer"] >= SLIME_WANDER_INTERVAL:
                            enemy["wander_timer"] = 0
                            enemy["wander_angle"] = random.uniform(0, math.tau)
                        wander_angle = enemy.get("wander_angle", 0.0)
                        enemy["x"] += math.cos(wander_angle) * enemy["speed"]
                        enemy["y"] += math.sin(wander_angle) * enemy["speed"]
                    elif enemy_type == 6:
                        enemy["x"] += base_dx * enemy["speed"]
                        enemy["y"] += base_dy * enemy["speed"]
                        enemy["summon_timer"] = enemy.get("summon_timer", 90) + 1
                        if enemy["summon_timer"] >= NECROMANCER_SUMMON_INTERVAL:
                            enemy["summon_timer"] = 0
                            total_enemies = len(self.enemy_list) + added_enemies + (1 if self.boss_active else 0)
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
                            if enemy["dash_timer"] >= DEMON_DASH_INTERVAL:
                                enemy["dash_active"] = True
                                enemy["dash_frames"] = DEMON_DASH_DURATION
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
            elif choice["type"] == "evolution":
                self.apply_evolution(choice["base_id"], choice["evolved_id"])
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

    def apply_evolution(self, base_weapon_id, evolved_weapon_id):
        if (base_weapon_id, evolved_weapon_id) not in self.check_evolution():
            return
        level = self.weapon_levels.get(base_weapon_id, 1)
        cooldown = self.weapon_cooldowns.get(base_weapon_id, 0)
        self.weapon_inventory = [evolved_weapon_id if weapon_id == base_weapon_id else weapon_id for weapon_id in self.weapon_inventory]
        self.weapon_levels.pop(base_weapon_id, None)
        self.weapon_cooldowns.pop(base_weapon_id, None)
        self.weapon_levels[evolved_weapon_id] = level
        self.weapon_cooldowns[evolved_weapon_id] = cooldown
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
            self.state = self.prev_state

    def update_boss(self):
        self._tick_sfx_cooldowns()
        self.update_debug_controls()
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.prev_state = "BOSS"
            self.state = "PAUSED"
            return

        self.timer_frames += self.debug_time_scale
        self.biome = self.get_current_biome()[0]
        self.update_active_game(allow_spawning=False)

    def calculate_score(self):
        diff_mult = self.difficulty + 1
        self.final_score = self.kills * self.player_level * diff_mult
        if self.final_score > self.high_score and self.final_score > 0:
            self.high_score = self.final_score
            self.is_new_high_score = True
        else:
            self.is_new_high_score = False

    def reset_game(self):
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
        self.prev_state = "TITLE"
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
        self.boss = None
        self.boss_hp = 0
        self.boss_max_hp = 0
        self.boss_warning_timer = 0
        self.kills = 0
        self.dash_cooldown = 0
        self.dash_invincible = 0
        self.player_invincible = 0
        self.selected_character = 0
        self.difficulty = 1
        self.char_cursor = 0
        self.diff_cursor = 1
        self.biome = 0
        self.enemy_list = []
        self.spawn_timer = SPAWN_INTERVAL_FRAMES
        self.spawn_interval = SPAWN_INTERVAL_FRAMES
        self.projectile_list = []
        self.enemy_projectile_list = []
        self.damage_zone_list = []
        self.garlic_tick_timer = 0
        self.gem_list = []
        self.sfx_cooldowns = {0: 0, 1: 0, 2: 0}
        self.debug_time_scale = 1
        self.debug_overlay = False
        self.score_calculated = False
        self.is_new_high_score = False
        self.final_score = 0

    def update_game_over(self):
        if not getattr(self, "score_calculated", False):
            self.calculate_score()
            self.score_calculated = True
            
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.reset_game()
            self.state = "TITLE"

    def update_victory(self):
        if not getattr(self, "score_calculated", False):
            self.calculate_score()
            self.score_calculated = True
            
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.reset_game()
            self.state = "TITLE"

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
        self.draw_boss_entity(cam_x, cam_y)
        self.draw_projectiles(cam_x, cam_y)
        self.draw_enemy_projectiles(cam_x, cam_y)
        for gem in self.gem_list:
            screen_x = int(gem["x"] - cam_x - 2)
            screen_y = int(gem["y"] - cam_y - 2)
            pyxel.blt(screen_x, screen_y, 0, SPR_XP_GEM[0], SPR_XP_GEM[1], 4, 4, colkey=0)
        if self.whip_attack_timer > 0:
            whip_weapon_id = 8 if 8 in self.weapon_inventory else 0
            whip_range = int(self.get_weapon_stats(whip_weapon_id)["range"])
            whip_x = 80 if self.whip_attack_side > 0 else 80 - whip_range
            whip_color = 2 if whip_weapon_id == 8 else 8
            pyxel.rect(whip_x, 52, whip_range, 16, whip_color)
        if self.player_invincible <= 0 or pyxel.frame_count % 2 == 0:
            pyxel.blt(80 - 8, 60 - 8, 0, SPR_KNIGHT[0], frame_y, 16, 16, colkey=0)
        self.draw_hud()
        self.draw_debug_overlay()
        if self.boss_warning_timer > 0 and pyxel.frame_count % 20 < 14:
            self._draw_centered_text("DEATH APPROACHES", 42, 8)

    def draw_debug_overlay(self):
        if not self.debug_overlay:
            return
        pyxel.text(2, 28, f"FPS:{pyxel.frame_count}", 7)
        pyxel.text(2, 34, f"ENM:{self.enemy_count}", 7)
        pyxel.text(2, 40, f"GEM:{self.gem_count}", 7)
        pyxel.text(2, 46, f"TMR:{self.timer_frames}", 7)
        pyxel.text(2, 52, f"TSC:{self.debug_time_scale}x", 7)

    def draw_boss_entity(self, cam_x, cam_y):
        if not self.boss_active or self.boss is None:
            return
        screen_x = int(self.boss["x"] - cam_x - 16)
        screen_y = int(self.boss["y"] - cam_y - 16)
        if self.boss.get("flash_timer", 0) > 0:
            pyxel.rect(screen_x, screen_y, 16, 16, 7)
            pyxel.rect(screen_x + 16, screen_y, 16, 16, 10)
            pyxel.rect(screen_x, screen_y + 16, 16, 16, 10)
            pyxel.rect(screen_x + 16, screen_y + 16, 16, 16, 7)
        else:
            pyxel.blt(screen_x, screen_y, 0, SPR_BOSS[0], SPR_BOSS[1], 32, 32, colkey=0)

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
        aura_weapon_id = 13 if 13 in self.weapon_inventory else 5 if 5 in self.weapon_inventory else None
        if aura_weapon_id is not None:
            garlic_range = int(self.get_weapon_stats(aura_weapon_id)["range"])
            aura_color = 11 if aura_weapon_id == 13 else 10
            pyxel.circb(int(self.player_x - cam_x), int(self.player_y - cam_y), garlic_range, aura_color)

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
            elif projectile["type"] == "death_spiral":
                width = 10
                height = 10
                color = 5
            elif projectile["type"] == "holy_water":
                width = 6
                height = 6
                color = 14
            elif projectile["type"] == "cross":
                width = 6
                height = 6
                color = 10
            elif projectile["type"] == "hyperlove":
                width = 8
                height = 8
                color = 9
            elif projectile["type"] == "holy_wand":
                width = 5
                height = 5
                color = 7
            elif projectile["type"] == "hellfire":
                width = 7
                height = 7
                color = 9
            elif projectile["type"] == "fire_wand":
                width = 5
                height = 5
                color = 8
            elif projectile["type"] == "thousand_edge":
                width = 8
                height = 4
                color = 11
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
        self.draw_playing()
        for y in range(0, 120, 2):
            pyxel.line(0, y, 160, y, 0)
        self.draw_hud()
        if self.prev_state == "BOSS":
            self.draw_boss_hp_bar()
        self._draw_centered_text("PAUSED", 46, 7)
        self._draw_centered_text("Arrows/WASD:Move  Space:Dash  ESC:Pause", 110, 7)

    def draw_boss(self):
        self.draw_playing()
        self.draw_boss_hp_bar()

    def draw_boss_hp_bar(self):
        if not self.boss_active or self.boss_max_hp <= 0:
            return
        bar_x = 20
        bar_y = 110
        bar_w = 120
        hp_w = int(bar_w * self.boss_hp / self.boss_max_hp)
        pyxel.rect(bar_x, bar_y, bar_w, 6, 0)
        pyxel.rect(bar_x, bar_y, max(0, hp_w), 6, 2)
        pyxel.rectb(bar_x - 1, bar_y - 1, bar_w + 2, 8, 7)
        self._draw_centered_text("DEATH", 101, 7)

    def draw_game_over(self):
        pyxel.cls(0)
        pyxel.rectb(4, 4, 152, 112, 8)
        pyxel.rectb(6, 6, 148, 108, 2)
        
        self._draw_centered_text("GAME OVER", 10, 8)
        
        total_sec = self.timer_frames // 30
        mins = total_sec // 60
        secs = total_sec % 60
        
        pyxel.text(15, 22, f"Time: {mins:02d}:{secs:02d}", 7)
        pyxel.text(85, 22, f"Level: Lv.{self.player_level}", 7)
        pyxel.text(15, 32, f"Kills: {self.kills}", 7)
        pyxel.text(85, 32, f"Score: {getattr(self, 'final_score', 0)}", 7)
        
        if getattr(self, "is_new_high_score", False) and pyxel.frame_count % 16 < 8:
            pyxel.text(15, 42, "NEW RECORD!", 10)
        else:
            pyxel.text(15, 42, f"High Score: {self.high_score}", 6)
            
        pyxel.text(15, 54, "Weapons:", 7)
        weapon_names = []
        for w_id in self.weapon_inventory:
            if w_id < 8:
                weapon_names.append(WEAPON_DATA[w_id]["name"])
            else:
                weapon_names.append(EVOLVED_WEAPON_DATA[w_id]["name"])
        
        for i, name in enumerate(weapon_names[:6]):
            col = i % 3
            row = i // 3
            pyxel.text(15 + col * 50, 62 + row * 8, name[:10], 6)
            
        pyxel.text(15, 78, "Passives:", 7)
        passive_names = []
        for p in self.passive_inventory:
            passive_names.append(PASSIVE_POOL[p["id"]]["name"])
            
        for i, name in enumerate(passive_names[:6]):
            col = i % 3
            row = i // 3
            pyxel.text(15 + col * 50, 86 + row * 8, name[:10], 12)
            
        if pyxel.frame_count % 30 < 15:
            self._draw_centered_text("PRESS ENTER TO RETURN TO TITLE", 108, 7)

    def draw_victory(self):
        pyxel.cls(0)
        pyxel.rectb(4, 4, 152, 112, 10)
        pyxel.rectb(6, 6, 148, 108, 7)
        
        self._draw_centered_text("VICTORY!", 10, 10)
        
        total_sec = self.timer_frames // 30
        mins = total_sec // 60
        secs = total_sec % 60
        
        pyxel.text(15, 22, f"Time: {mins:02d}:{secs:02d}", 7)
        pyxel.text(85, 22, f"Level: Lv.{self.player_level}", 7)
        pyxel.text(15, 32, f"Kills: {self.kills}", 7)
        pyxel.text(85, 32, f"Score: {getattr(self, 'final_score', 0)}", 10)
        
        if getattr(self, "is_new_high_score", False) and pyxel.frame_count % 16 < 8:
            pyxel.text(15, 42, "NEW RECORD!", 10)
        else:
            pyxel.text(15, 42, f"High Score: {self.high_score}", 10)
            
        pyxel.text(15, 54, "Weapons:", 7)
        weapon_names = []
        for w_id in self.weapon_inventory:
            if w_id < 8:
                weapon_names.append(WEAPON_DATA[w_id]["name"])
            else:
                weapon_names.append(EVOLVED_WEAPON_DATA[w_id]["name"])
        
        for i, name in enumerate(weapon_names[:6]):
            col = i % 3
            row = i // 3
            pyxel.text(15 + col * 50, 62 + row * 8, name[:10], 6)
            
        pyxel.text(15, 78, "Passives:", 7)
        passive_names = []
        for p in self.passive_inventory:
            passive_names.append(PASSIVE_POOL[p["id"]]["name"])
            
        for i, name in enumerate(passive_names[:6]):
            col = i % 3
            row = i // 3
            pyxel.text(15 + col * 50, 86 + row * 8, name[:10], 12)
            
        if pyxel.frame_count % 30 < 15:
            self._draw_centered_text("PRESS ENTER TO RETURN TO TITLE", 108, 7)

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
        cooldown_w = int(40 * self.dash_cooldown / DASH_COOLDOWN_FRAMES)
        pyxel.rect(20, 18, cooldown_w, 4, 12)
        # Timer MM:SS (top right)
        total_sec = self.timer_frames // 30
        mins = total_sec // 60
        secs = total_sec % 60
        pyxel.text(128, 2, f"{mins:02d}:{secs:02d}", 7)

    def _draw_centered_text(self, text, y, color):
        pyxel.text((pyxel.width - len(text) * 4) // 2, y, text, color)


App()
