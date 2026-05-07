import datetime
import json
import math
from copy import deepcopy
from pathlib import Path

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
FPS = 30
PYXEL_VOLUME_MAX = 7

PLAYER_START_HP = 100
PLAYER_START_MAGNET_RANGE = 30
PLAYER_INVINCIBLE_FRAMES = 60
PLAYER_HIT_RADIUS = 12
PLAYER_HITBOX_HALF_SIZE = 6
PLAYER_HITBOX_SIZE = 12
PLAYER_CONTACT_DAMAGE = 1

PARTICLE_LIMIT = 30
PARTICLE_SPEED_MIN = 0.4
PARTICLE_SPEED_MAX = 1.5

SPATIAL_HASH_CELL_SIZE = 32
ENEMY_HITBOX_HALF_SIZE = 6
ENEMY_HITBOX_SIZE = 12
BOSS_HITBOX_HALF_SIZE = 16
BOSS_HITBOX_SIZE = 32

DASH_DISTANCE = 40
DASH_INVINCIBLE_FRAMES = 10

KNOCKBACK_DISTANCE = 15
EVOLVED_KNOCKBACK_DISTANCE = 18
KNOCKBACK_FRAMES = 5

GEM_COLLECT_RANGE = 8
GEM_DESPAWN_RADIUS = 500
GEM_MAGNET_SPEED = 2

PROJECTILE_SPEED_WAND = 3
PROJECTILE_SPEED_AXE_X = 0.8
PROJECTILE_SPEED_AXE_Y = -3
PROJECTILE_SPEED_KNIFE = 4
PROJECTILE_SPEED_HOLY_WATER = 1.8
PROJECTILE_HOLY_WATER_ARC = 2.0
PROJECTILE_SPEED_CROSS = 2.5
PROJECTILE_SPEED_FIRE_WAND = 3
PROJECTILE_SPEED_HOLY_WAND = 4
PROJECTILE_SPEED_DEATH_SPIRAL = 2.5
PROJECTILE_SPEED_THOUSAND_EDGE = 4.8
PROJECTILE_SPEED_HYPERLOVE = 3
PROJECTILE_SPEED_HELLFIRE = 3.2
PROJECTILE_HYPERLOVE_SIDE_SPEED = 0.6
PROJECTILE_AXE_LIFETIME = 60
PROJECTILE_AXE_GRAVITY = 0.15
PROJECTILE_HOLY_WATER_GRAVITY = 0.12
RETURNING_PROJECTILE_EXTRA_FRAMES = 10
RETURNING_PROJECTILE_PLAYER_RADIUS_SQ = 64
FIRE_WAND_EXPLOSION_DAMAGE = 4
FIRE_WAND_EXPLOSION_RADIUS = 24
HELLFIRE_EXPLOSION_RADIUS = 32
BOROS_SEA_MAX_DISTANCE = 48
BOROS_SEA_ZONE_SIZE = 40
BOROS_SEA_ZONE_TIMER = 45
BOROS_SEA_TICK_INTERVAL = 8
DAMAGE_ZONE_SIZE = 24
DAMAGE_ZONE_TIMER = 30
DAMAGE_ZONE_TICK_INTERVAL = 10
PROJECTILE_HITBOXES = {
    "axe": (16, 16),
    "death_spiral": (16, 16),
    "knife": (8, 4),
    "thousand_edge": (8, 4),
    "holy_water": (6, 6),
    "cross": (6, 6),
    "hyperlove": (8, 8),
    "fire_wand": (5, 5),
    "hellfire": (5, 5),
}
DEFAULT_PROJECTILE_HITBOX = (4, 4)
LEVEL_UP_CHOICE_COUNT = 3
STAT_MAX_HP_BONUS = 10
LEVEL_UP_HP_BONUS = 2
LEVEL_UP_PARTICLE_COUNT = 10
LEVEL_UP_PARTICLE_COLOR = 10
LEVEL_UP_PARTICLE_LIFE = 20
LEVEL_UP_PARTICLE_SIZE = 2
LEVEL_UP_PARTICLE_RADIUS = 12
GEM_COLLECT_PARTICLE_COUNT = 2
GEM_COLLECT_PARTICLE_COLOR = 12
GEM_COLLECT_PARTICLE_LIFE = 8
BIOME_TRANSITION_SECONDS = 30
FADE_MAX_ALPHA = 15
FADE_SPEED = 2
PLAYER_FLASH_FRAMES = 3
ENEMY_FLASH_FRAMES = 2
HIT_SHAKE_FRAMES = 3
HIT_SHAKE_INTENSITY = 2

CONFIG_PATH = Path(__file__).with_name("config.json")
SETTINGS_VOLUME_VALUES = [0.25, 0.5, 0.8]
SETTINGS_VOLUME_LABELS = ["Low", "Medium", "High"]
SETTINGS_DIFFICULTY_LABELS = ["Easy", "Normal", "Hard"]

DEFAULT_CONFIG = {
    "key_bindings": {
        "up": "UP",
        "down": "DOWN",
        "left": "LEFT",
        "right": "RIGHT",
        "dash": "SPACE",
        "pause": "ESC",
        "confirm": "ENTER",
    },
    "volume": {
        "sfx": 0.8,
        "bgm": 0.5,
    },
    "default_difficulty": "Normal",
}


def get_daily_seed():
    """Return deterministic seed based on today's date."""
    today = datetime.date.today()
    return today.year * 10000 + today.month * 100 + today.day


def get_daily_config(seed):
    """Return deterministic game config from seed."""
    import random as _r
    rng = _r.Random(seed)
    return {
        "character": rng.randint(0, 7),
        "difficulty": rng.randint(0, 2),
        "biome_start": rng.randint(0, 3),
    }

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
COIN_BASE_PER_RUN = 5
COIN_PER_MINUTE = 2
COIN_PER_KILL = 1
COIN_PER_LEVEL = 3
COIN_VICTORY_BONUS = 20
COIN_HARD_MODE_MULT = 1.5

SHOP_UPGRADES = [
    {
        "id": "max_hp",
        "name": "Vitality",
        "desc": "Start HP +10%",
        "max_level": 3,
        "costs": [50, 100, 200],
        "effect_per_level": 0.10,
    },
    {
        "id": "speed",
        "name": "Swiftness",
        "desc": "Move Speed +5%",
        "max_level": 3,
        "costs": [60, 120, 240],
        "effect_per_level": 0.05,
    },
    {
        "id": "xp_bonus",
        "name": "Wisdom",
        "desc": "XP Gain +10%",
        "max_level": 3,
        "costs": [80, 160, 320],
        "effect_per_level": 0.10,
    },
    {
        "id": "weapon_level",
        "name": "Mastery",
        "desc": "Start Weapon +1 Lv",
        "max_level": 2,
        "costs": [150, 300],
        "effect_per_level": 1,
    },
    {
        "id": "coin_bonus",
        "name": "Greed",
        "desc": "Coin Gain +15%",
        "max_level": 3,
        "costs": [100, 200, 400],
        "effect_per_level": 0.15,
    },
]

ACHIEVEMENT_DEFS = [
    {"id": "first_blood", "name": "First Blood", "desc": "Defeat first enemy", "check": "total_kills", "threshold": 1},
    {"id": "hunter", "name": "Hunter", "desc": "Defeat 100 enemies", "check": "total_kills", "threshold": 100},
    {"id": "exterminator", "name": "Exterminator", "desc": "Defeat 1000 enemies", "check": "total_kills", "threshold": 1000},
    {"id": "survivor_5", "name": "Survivor", "desc": "Survive 5 minutes", "check": "max_survival_sec", "threshold": 300},
    {"id": "survivor_10", "name": "Veteran", "desc": "Survive 10 minutes", "check": "max_survival_sec", "threshold": 600},
    {"id": "survivor_20", "name": "Legend", "desc": "Survive 20 minutes", "check": "max_survival_sec", "threshold": 1200},
    {"id": "boss_slayer", "name": "Death Slayer", "desc": "Defeat the Death boss", "check": "boss_kills", "threshold": 1},
    {"id": "first_evolution", "name": "Evolution", "desc": "Evolve a weapon", "check": "evolutions_done", "threshold": 1},
    {"id": "level_10", "name": " Experienced", "desc": "Reach level 10", "check": "max_level", "threshold": 10},
    {"id": "level_30", "name": "Master", "desc": "Reach level 30", "check": "max_level", "threshold": 30},
    {"id": "full_arsenal", "name": "Full Arsenal", "desc": "Equip 6 weapons at once", "check": "max_weapons", "threshold": 6},
    {"id": "hard_clear", "name": "Hard Mode Hero", "desc": "Clear Hard mode", "check": "hard_clears", "threshold": 1},
    {"id": "rich", "name": "Wealthy", "desc": "Earn 500 coins total", "check": "total_coins_earned", "threshold": 500},
    {"id": "shopper", "name": "Shopper", "desc": "Buy first upgrade", "check": "upgrades_bought", "threshold": 1},
    {"id": "maxed", "name": "Maxed Out", "desc": "Max any upgrade", "check": "max_upgrade_level", "threshold": 1},
]

CHARACTER_UNLOCK_CONDITIONS = {
    3: {"type": "total_kills", "threshold": 100, "desc": "100 total kills"},
    4: {"type": "survival_frames", "threshold": 10 * 60 * FPS, "desc": "Survive 10 min"},
    5: {"type": "boss_damage_percent", "threshold": 50, "desc": "Boss damage 50%"},
    6: {"type": "clear_normal", "threshold": 1, "desc": "Clear Normal"},
    7: {"type": "clear_hard", "threshold": 1, "desc": "Clear Hard"},
}

WEAPON_UNLOCK_CONDITIONS = {
    8: {"type": "weapon_kills", "weapon_id": 0, "threshold": 50, "desc": "50 kills with Whip"},
    9: {"type": "weapon_kills", "weapon_id": 1, "threshold": 50, "desc": "50 kills with Wand"},
    10: {"type": "weapon_kills", "weapon_id": 2, "threshold": 50, "desc": "50 kills with Axe"},
    11: {"type": "weapon_kills", "weapon_id": 3, "threshold": 50, "desc": "50 kills with Knife"},
    12: {"type": "weapon_kills", "weapon_id": 4, "threshold": 50, "desc": "50 kills with Holy Water"},
    13: {"type": "weapon_kills", "weapon_id": 5, "threshold": 50, "desc": "50 kills with Garlic"},
    14: {"type": "weapon_kills", "weapon_id": 6, "threshold": 50, "desc": "50 kills with Cross"},
    15: {"type": "weapon_kills", "weapon_id": 7, "threshold": 50, "desc": "50 kills with Fire Wand"},
}

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

PASSIVE_ITEM_DATA = PASSIVE_POOL
BIOME_DATA = [
    {"name": "Grassland", "boundary": 300},
    {"name": "Desert", "boundary": 600},
    {"name": "Cave", "boundary": 1200},
    {"name": "Castle", "boundary": None},
]

def rect_overlap(ax, ay, aw, ah, bx, by, bw, bh):
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


class SpatialHash:
    def __init__(self, cell_size=SPATIAL_HASH_CELL_SIZE):
        self.cell_size = cell_size
        self.cells = {}

    def clear(self):
        self.cells.clear()

    def _cell_coords(self, x, y):
        return int(math.floor(x / self.cell_size)), int(math.floor(y / self.cell_size))

    def insert(self, entity, index=0):
        cell = self._cell_coords(entity["x"], entity["y"])
        entity["_spatial_index"] = index
        self.cells.setdefault(cell, []).append(entity)

    def build(self, entities):
        self.clear()
        for index, entity in enumerate(entities):
            self.insert(entity, index)

    def query(self, x, y, radius):
        min_cx, min_cy = self._cell_coords(x - radius, y - radius)
        max_cx, max_cy = self._cell_coords(x + radius, y + radius)
        nearby = []
        seen = set()
        for cy in range(min_cy, max_cy + 1):
            for cx in range(min_cx, max_cx + 1):
                for entity in self.cells.get((cx, cy), ()):
                    entity_id = id(entity)
                    if entity_id in seen:
                        continue
                    seen.add(entity_id)
                    nearby.append(entity)
        nearby.sort(key=lambda entity: entity.get("_spatial_index", 0))
        return nearby


def _merge_config(defaults, loaded):
    merged = deepcopy(defaults)
    if not isinstance(loaded, dict):
        return merged
    for key, value in loaded.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key].update(value)
        elif key in merged:
            merged[key] = value
    return merged


def load_config(path=CONFIG_PATH):
    config_path = Path(path)
    try:
        loaded = json.loads(config_path.read_text())
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return deepcopy(DEFAULT_CONFIG)
    return _merge_config(DEFAULT_CONFIG, loaded)


def save_config(config, path=CONFIG_PATH):
    config_path = Path(path)
    merged = _merge_config(DEFAULT_CONFIG, config)
    config_path.write_text(json.dumps(merged, indent=2) + "\n")
    return merged


def _tile_hash(wx, wy):
    """Deterministic hash for tile selection. Same coords = same result."""
    h = wx * 374761393 + wy * 668265263
    h = (h ^ (h >> 13)) * 1274126177
    return (h ^ (h >> 16)) & 0xFFFFFFFF


def tile_type(wx, wy):
    return _tile_hash(wx, wy) % 4
