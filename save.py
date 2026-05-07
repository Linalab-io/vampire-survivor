# save.py - Persistent save data management
import json
from pathlib import Path
from copy import deepcopy

SAVE_PATH = Path(__file__).with_name("save.json")

DEFAULT_SAVE = {
    "coins": 0,
    "total_coins_earned": 0,
    "upgrades": {
        "max_hp": 0,
        "speed": 0,
        "xp_bonus": 0,
        "weapon_level": 0,
        "coin_bonus": 0,
    },
    "unlocked_characters": [0, 1, 2],
    "unlocked_weapons": [0, 1, 2, 3, 4, 5, 6, 7],
    "achievements": [],
    "arcade_high_score": 0,
    "daily_results": {},
    "settings": {
        "sfx_volume": "High",
        "bgm_volume": "Medium",
        "default_difficulty": "Normal",
    },
    "stats": {
        "total_play_time_frames": 0,
        "total_kills": 0,
        "max_level": 1,
        "max_survival_frames": 0,
        "boss_kills": 0,
        "max_weapons_equipped": 0,
        "evolutions_done": 0,
        "hard_clears": 0,
        "total_coins_earned": 0,
        "upgrades_bought": 0,
        "max_upgrade_level": 0,
    },
    "run_history": [],
}


def _merge_save(defaults, loaded):
    merged = deepcopy(defaults)
    if not isinstance(loaded, dict):
        return merged
    for key, value in loaded.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge_save(merged[key], value)
        elif key in merged:
            merged[key] = value
    return merged


def load_save(path=SAVE_PATH):
    save_path = Path(path)
    try:
        loaded = json.loads(save_path.read_text())
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return deepcopy(DEFAULT_SAVE)
    return _merge_save(DEFAULT_SAVE, loaded)


def save_save(data, path=SAVE_PATH):
    save_path = Path(path)
    merged = _merge_save(DEFAULT_SAVE, data)
    temp_path = save_path.with_suffix(save_path.suffix + ".tmp")
    temp_path.write_text(json.dumps(merged, indent=2) + "\n")
    temp_path.replace(save_path)
    return merged


def reset_save(path=SAVE_PATH):
    save_path = Path(path)
    try:
        save_path.unlink()
    except FileNotFoundError:
        pass
