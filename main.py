# pyright: reportAttributeAccessIssue=false
import math
import random
import time

import pyxel

from data import *
from sprites import create_sprites
from sounds import create_sounds
from save import load_save, save_save
import enemies
import weapons
import screens


KEY_NAME_TO_PYXEL = {
    "UP": pyxel.KEY_UP,
    "DOWN": pyxel.KEY_DOWN,
    "LEFT": pyxel.KEY_LEFT,
    "RIGHT": pyxel.KEY_RIGHT,
    "SPACE": pyxel.KEY_SPACE,
    "ESC": pyxel.KEY_ESCAPE,
    "ENTER": pyxel.KEY_RETURN,
    "RETURN": pyxel.KEY_RETURN,
    "A": pyxel.KEY_A,
    "D": pyxel.KEY_D,
    "S": pyxel.KEY_S,
    "W": pyxel.KEY_W,
    "X": pyxel.KEY_X,
    "3": pyxel.KEY_3,
    "4": pyxel.KEY_4,
    "5": pyxel.KEY_5,
    "6": pyxel.KEY_6,
}


def _clamp_unit(value):
    return max(0.0, min(1.0, float(value)))


class App:
    def __init__(self):
        self.config = load_config()
        self.save_data = load_save()
        self.key_bindings = self.config["key_bindings"]
        self.sfx_volume = _clamp_unit(self.config["volume"]["sfx"])
        self.state = "TITLE"
        self.timer_frames = 0
        self.base_player_max_hp = PLAYER_START_HP
        self.player_speed = PLAYER_SPEED
        self.player_hp = PLAYER_START_HP
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
        self.magnet_range = PLAYER_START_MAGNET_RANGE
        self.hp_regen = 0.0
        self.hp_regen_timer = 0
        self.luck = 0.0
        self.weapon_damage_mult = 1.0
        self.evolution_ready = []
        self.evolution_done = False
        self.boss_defeated_this_run = False
        self.level_up_choices = []
        self.level_up_cursor = 0
        self.shop_cursor = 0
        self.stats_page = 0
        self.achieve_page = 0
        self.run_history_scroll = 0
        self.settings_cursor = 0
        self.achievement_popup = None
        self.boss_active = False
        self.boss = None
        self.boss_hp = 0
        self.boss_max_hp = 0
        self.boss_damage_dealt = 0
        self.boss_warning_timer = 0
        self.kills = 0
        self.weapon_kill_counts = {}
        self.dash_cooldown = 0
        self.dash_invincible = 0
        self.player_invincible = 0
        self.player_flash = 0
        self.shake_frames = 0
        self.shake_intensity = 0
        self.particles = []
        self.selected_character = 0
        self.difficulty = self.get_default_difficulty_index()
        self.char_cursor = 0
        self.diff_cursor = self.difficulty
        self.high_score = 0
        self.biome = 0
        self.biome_start = 0
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
        self.debug_mode = False
        self.score_calculated = False
        self.is_new_high_score = False
        self.new_unlocks = []
        self.final_score = 0
        self.coins_earned = 0
        self.arcade_mode = False
        self.daily_mode = False
        self.daily_seed = None
        self.daily_config = None
        self.biome_start = 0
        self.enemy_spatial_hash = SpatialHash(SPATIAL_HASH_CELL_SIZE)
        self.bgm_volume = int(round(_clamp_unit(self.config["volume"]["bgm"]) * PYXEL_VOLUME_MAX))
        self.bgm_playing = False
        self.fade_alpha = 0
        self.fade_direction = 0
        self.fade_target_state = None
        self.fade_speed = FADE_SPEED

        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Vampire Survivors", fps=FPS)
        self.sfx_cooldowns = {sound_id: 0 for sound_id in (0, 1, 2, 5, 6, 7, 8, 9)}
        create_sounds(self.bgm_volume, self.sfx_volume)
        create_sprites()
        pyxel.run(self.update, self.draw)
    def get_default_difficulty_index(self):
        difficulty_name = self.config.get("default_difficulty", DEFAULT_CONFIG["default_difficulty"])
        for index, difficulty in enumerate(DIFFICULTY_DATA):
            if difficulty["name"] == difficulty_name:
                return index
        return 1
    def get_key(self, action):
        key_name = self.key_bindings.get(action, DEFAULT_CONFIG["key_bindings"].get(action, ""))
        return KEY_NAME_TO_PYXEL.get(str(key_name).upper())
    def btn_action(self, action, *fallback_keys):
        key = self.get_key(action)
        return (key is not None and pyxel.btn(key)) or any(pyxel.btn(key) for key in fallback_keys)
    def btnp_action(self, action, *fallback_keys):
        key = self.get_key(action)
        return (key is not None and pyxel.btnp(key)) or any(pyxel.btnp(key) for key in fallback_keys)
    def rebuild_enemy_spatial_hash(self):
        self.enemy_spatial_hash.build(self.enemy_list)
    def nearby_enemies(self, x, y, radius):
        return self.enemy_spatial_hash.query(x, y, radius)
    def start_bgm(self):
        if not self.bgm_playing:
            pyxel.playm(0, loop=True)
            self.bgm_playing = True
    def stop_bgm(self):
        if self.bgm_playing:
            pyxel.stop(0)
            self.bgm_playing = False
    def set_state(self, state):
        self.state = state
        if state in ("PLAYING", "BOSS"):
            self.start_bgm()
        elif state in ("TITLE", "SHOP", "STATS", "ACHIEVEMENTS", "ARCADE", "DAILY", "RUN_HISTORY", "SETTINGS", "GAME_OVER", "VICTORY"):
            self.stop_bgm()
    def start_fade_to(self, target_state):
        if self.fade_direction != 0:
            return
        self.fade_direction = 1
        self.fade_alpha = 0
        self.fade_target_state = target_state
    def update_fade(self):
        if self.fade_direction == 0:
            return False
        self.fade_alpha += self.fade_direction * self.fade_speed
        if self.fade_alpha >= FADE_MAX_ALPHA:
            self.fade_alpha = FADE_MAX_ALPHA
            self.fade_direction = -1
            if self.fade_target_state is not None:
                self.set_state(self.fade_target_state)
                self.fade_target_state = None
        elif self.fade_alpha <= 0:
            self.fade_alpha = 0
            self.fade_direction = 0
        return True
    def _tick_sfx_cooldowns(self):
        for sound_id in self.sfx_cooldowns:
            self.sfx_cooldowns[sound_id] = max(0, self.sfx_cooldowns[sound_id] - 1)
    def play_sfx(self, sound_id):
        if self.sfx_volume <= 0 or self.sfx_cooldowns.get(sound_id, 0) > 0:
            return
        pyxel.play(1 + sound_id % 3, sound_id)
        self.sfx_cooldowns[sound_id] = SFX_COOLDOWN_FRAMES
    def update_achievement_popup(self):
        popup = self.achievement_popup
        if popup is None:
            return
        popup["timer"] -= 1
        if popup["timer"] <= 0:
            self.achievement_popup = None

    def update_stats(self):
        if self.btnp_action("pause"):
            self.start_fade_to("TITLE")

    def update_achievements(self):
        max_page = max(0, (len(ACHIEVEMENT_DEFS) - 1) // 5)
        if self.btnp_action("up", pyxel.KEY_W):
            self.achieve_page = max(0, self.achieve_page - 1)
            self.play_sfx(9)
        elif self.btnp_action("down", pyxel.KEY_S):
            self.achieve_page = min(max_page, self.achieve_page + 1)
            self.play_sfx(9)
        elif self.btnp_action("pause"):
            self.start_fade_to("TITLE")

    def update_live_stats(self):
        stats = self.save_data["stats"]
        stats["max_weapons_equipped"] = max(stats.get("max_weapons_equipped", 0), len(self.weapon_inventory))

    def _achievement_value(self, achievement):
        stats = self.save_data["stats"]
        check = achievement["check"]
        if check == "total_kills":
            return stats.get("total_kills", 0) + self.kills
        if check == "max_survival_sec":
            return max(stats.get("max_survival_frames", 0), self.timer_frames) // FPS
        if check == "max_level":
            return max(stats.get("max_level", 1), self.player_level)
        if check == "max_weapons":
            return max(stats.get("max_weapons_equipped", 0), len(self.weapon_inventory))
        if check == "total_coins_earned":
            return max(stats.get("total_coins_earned", 0), self.save_data.get("total_coins_earned", 0))
        return stats.get(check, 0)

    def check_achievements(self):
        achievements = self.save_data.setdefault("achievements", [])
        unlocked = set(achievements)
        for achievement in ACHIEVEMENT_DEFS:
            if achievement["id"] in unlocked:
                continue
            if self._achievement_value(achievement) >= achievement["threshold"]:
                achievements.append(achievement["id"])
                unlocked.add(achievement["id"])
                self.achievement_popup = {"name": achievement["name"].strip(), "timer": 3 * FPS}

    def spawn_particles(self, x, y, count, color, life, size=1, radius=0):
        for _ in range(count):
            if len(self.particles) >= PARTICLE_LIMIT:
                self.particles.pop(0)
            angle = random.random() * math.tau
            spawn_radius = random.uniform(0, radius)
            speed = random.uniform(PARTICLE_SPEED_MIN, PARTICLE_SPEED_MAX)
            self.particles.append({
                "x": x + math.cos(angle) * spawn_radius,
                "y": y + math.sin(angle) * spawn_radius,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": life,
                "max_life": life,
                "color": color,
                "size": size,
            })
    def update_visual_effects(self):
        if self.shake_frames > 0:
            self.shake_frames -= 1
        else:
            self.shake_intensity = 0

        self.player_flash = max(0, self.player_flash - 1)
        for particle in self.particles:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["life"] -= 1
        self.particles = [particle for particle in self.particles if particle["life"] > 0]
    def get_enemy_color(self, enemy):
        if enemy.get("type") == 8:
            return 11
        return (8, 13, 7, 4, 12, 11, 5, 8)[enemy.get("type", 0)]
    def damage_enemy(self, enemy, damage):
        enemy["hp"] -= self.apply_luck_critical(damage)
        enemy["flash_frames"] = ENEMY_FLASH_FRAMES
    def record_weapon_kill(self, weapon_id):
        if weapon_id not in WEAPON_DATA and weapon_id not in EVOLVED_WEAPON_DATA:
            return
        base_weapon_id = EVOLVED_WEAPON_DATA.get(weapon_id, {}).get("base", weapon_id)
        self.weapon_kill_counts[base_weapon_id] = self.weapon_kill_counts.get(base_weapon_id, 0) + 1
    def record_pending_weapon_kills(self):
        for enemy in self.enemy_list:
            if enemy["hp"] <= 0 and not enemy.get("weapon_kill_recorded"):
                self.record_weapon_kill(enemy.get("killed_by_weapon_id", -1))
                enemy["weapon_kill_recorded"] = True
    def damage_player(self, damage):
        self.player_hp -= damage
        self.player_flash = PLAYER_FLASH_FRAMES
        self.shake_frames = HIT_SHAKE_FRAMES
        self.shake_intensity = HIT_SHAKE_INTENSITY
    def get_weapon_display_color(self, weapon_id):
        weapon_colors = (8, 12, 4, 13, 14, 7, 10, 9, 2, 7, 5, 11, 14, 11, 9, 8)
        return weapon_colors[weapon_id] if 0 <= weapon_id < len(weapon_colors) else 7
    def update(self):
        self.update_visual_effects()
        self.update_achievement_popup()
        if self.update_fade():
            return
        if self.state == "TITLE":
            self.update_title()
        elif self.state == "CHAR_SELECT":
            self.update_char_select()
        elif self.state == "SHOP":
            self.update_shop()
        elif self.state == "STATS":
            self.update_stats()
        elif self.state == "ACHIEVEMENTS":
            self.update_achievements()
        elif self.state == "ARCADE":
            self.update_arcade()
        elif self.state == "DAILY":
            self.update_daily()
        elif self.state == "RUN_HISTORY":
            self.update_run_history()
        elif self.state == "SETTINGS":
            self.update_settings()
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
        elif self.state == "SHOP":
            self.draw_shop()
        elif self.state == "STATS":
            self.draw_stats()
        elif self.state == "ACHIEVEMENTS":
            self.draw_achievements()
        elif self.state == "ARCADE":
            self.draw_arcade()
        elif self.state == "DAILY":
            self.draw_daily_challenge()
        elif self.state == "RUN_HISTORY":
            self.draw_run_history()
        elif self.state == "SETTINGS":
            self.draw_settings()
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
        self.draw_fade_overlay()
        self.draw_achievement_popup()
    def update_title(self):
        if self.btnp_action("pause"):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_F12):
            self.debug_mode = not self.debug_mode

        if pyxel.btnp(pyxel.KEY_A):
            self.start_fade_to("ACHIEVEMENTS")
        elif pyxel.btnp(pyxel.KEY_D):
            self.start_fade_to("STATS")
        elif pyxel.btnp(pyxel.KEY_3):
            self.start_fade_to("ARCADE")
        elif pyxel.btnp(pyxel.KEY_4):
            self.daily_seed = get_daily_seed()
            self.daily_config = get_daily_config(self.daily_seed)
            self.start_fade_to("DAILY")
        elif pyxel.btnp(pyxel.KEY_5):
            self.run_history_scroll = 0
            self.start_fade_to("RUN_HISTORY")
        elif pyxel.btnp(pyxel.KEY_6):
            self.start_fade_to("SETTINGS")
        elif self.btnp_action("right") or pyxel.btnp(pyxel.KEY_S):
            self.start_fade_to("SHOP")
        elif self.btnp_action("confirm", pyxel.KEY_RETURN2):
            self.arcade_mode = False
            self.daily_mode = False
            self.start_fade_to("CHAR_SELECT")
    def _start_fixed_run(self, character, difficulty, arcade=False, daily=False, biome_start=0):
        daily_seed = self.daily_seed
        daily_config = self.daily_config
        self.reset_game()
        self.arcade_mode = arcade
        self.daily_mode = daily
        self.daily_seed = daily_seed if daily else None
        self.daily_config = daily_config if daily else None
        self.selected_character = character
        self.char_cursor = character
        self.difficulty = difficulty
        self.diff_cursor = difficulty
        self.biome_start = biome_start
        self._apply_selections()
        self.start_fade_to("PLAYING")

    def update_arcade(self):
        if self.btnp_action("pause"):
            self.start_fade_to("TITLE")
        elif self.btnp_action("confirm", pyxel.KEY_RETURN2):
            self._start_fixed_run(0, 1, arcade=True)

    def update_daily(self):
        if self.daily_seed is None or self.daily_config is None:
            self.daily_seed = get_daily_seed()
            self.daily_config = get_daily_config(self.daily_seed)
        if self.btnp_action("pause"):
            self.start_fade_to("TITLE")
        elif self.btnp_action("confirm", pyxel.KEY_RETURN2):
            config = self.daily_config
            self._start_fixed_run(config["character"], config["difficulty"], daily=True, biome_start=config["biome_start"])

    def update_run_history(self):
        history_len = len(self.save_data.get("run_history", []))
        max_scroll = max(0, history_len - 4)
        if self.btnp_action("up", pyxel.KEY_W):
            self.run_history_scroll = max(0, self.run_history_scroll - 1)
            self.play_sfx(9)
        elif self.btnp_action("down", pyxel.KEY_S):
            self.run_history_scroll = min(max_scroll, self.run_history_scroll + 1)
            self.play_sfx(9)
        elif self.btnp_action("pause"):
            self.start_fade_to("TITLE")

    def _setting_volume_index(self, value):
        return min(range(len(SETTINGS_VOLUME_VALUES)), key=lambda index: abs(SETTINGS_VOLUME_VALUES[index] - float(value)))

    def _sync_settings_save(self):
        self.save_data["settings"] = {
            "sfx_volume": SETTINGS_VOLUME_LABELS[self._setting_volume_index(self.config["volume"]["sfx"])],
            "bgm_volume": SETTINGS_VOLUME_LABELS[self._setting_volume_index(self.config["volume"]["bgm"])],
            "default_difficulty": self.config.get("default_difficulty", "Normal"),
        }

    def _change_setting(self, direction):
        if self.settings_cursor == 0:
            index = (self._setting_volume_index(self.config["volume"]["sfx"]) + direction) % len(SETTINGS_VOLUME_VALUES)
            self.config["volume"]["sfx"] = SETTINGS_VOLUME_VALUES[index]
            self.sfx_volume = _clamp_unit(self.config["volume"]["sfx"])
        elif self.settings_cursor == 1:
            index = (self._setting_volume_index(self.config["volume"]["bgm"]) + direction) % len(SETTINGS_VOLUME_VALUES)
            self.config["volume"]["bgm"] = SETTINGS_VOLUME_VALUES[index]
            self.bgm_volume = int(round(_clamp_unit(self.config["volume"]["bgm"]) * PYXEL_VOLUME_MAX))
            create_sounds(self.bgm_volume, self.sfx_volume)
        else:
            current = self.config.get("default_difficulty", "Normal")
            index = (SETTINGS_DIFFICULTY_LABELS.index(current) + direction) % len(SETTINGS_DIFFICULTY_LABELS) if current in SETTINGS_DIFFICULTY_LABELS else 1
            self.config["default_difficulty"] = SETTINGS_DIFFICULTY_LABELS[index]
            if not self.arcade_mode and not self.daily_mode:
                self.difficulty = self.get_default_difficulty_index()
                self.diff_cursor = self.difficulty
        self.config = save_config(self.config)
        self._sync_settings_save()
        self.save_data = save_save(self.save_data)
        self.play_sfx(9)

    def update_settings(self):
        if self.btnp_action("up", pyxel.KEY_W):
            self.settings_cursor = (self.settings_cursor - 1) % 3
            self.play_sfx(9)
        elif self.btnp_action("down", pyxel.KEY_S):
            self.settings_cursor = (self.settings_cursor + 1) % 3
            self.play_sfx(9)
        elif self.btnp_action("left", pyxel.KEY_A):
            self._change_setting(-1)
        elif self.btnp_action("right", pyxel.KEY_D):
            self._change_setting(1)
        elif self.btnp_action("pause"):
            self.start_fade_to("TITLE")

    def update_char_select(self):
        moved = False
        unlocked_characters = set(self.save_data["unlocked_characters"])
        if self.btnp_action("left", pyxel.KEY_A):
            self.char_cursor = self.next_unlocked_character(-1, unlocked_characters)
            moved = True
        elif self.btnp_action("right", pyxel.KEY_D):
            self.char_cursor = self.next_unlocked_character(1, unlocked_characters)
            moved = True
        elif self.btnp_action("up", pyxel.KEY_W):
            self.char_cursor = self.next_unlocked_character(-4, unlocked_characters)
            moved = True
        elif self.btnp_action("down", pyxel.KEY_S):
            self.char_cursor = self.next_unlocked_character(4, unlocked_characters)
            moved = True
        elif self.btnp_action("confirm", pyxel.KEY_RETURN2):
            if self.char_cursor in unlocked_characters:
                self.selected_character = self.char_cursor
                self.start_fade_to("DIFF_SELECT")
        if moved:
            self.play_sfx(9)
    def next_unlocked_character(self, step, unlocked_characters=None):
        unlocked_characters = unlocked_characters or set(self.save_data["unlocked_characters"])
        cursor = self.char_cursor
        for _ in range(len(CHARACTER_DATA)):
            cursor = (cursor + step) % len(CHARACTER_DATA)
            if cursor in unlocked_characters:
                return cursor
        return 0
    def update_diff_select(self):
        moved = False
        if self.btnp_action("left", pyxel.KEY_A):
            self.diff_cursor = (self.diff_cursor - 1) % 3
            moved = True
        elif self.btnp_action("right", pyxel.KEY_D):
            self.diff_cursor = (self.diff_cursor + 1) % 3
            moved = True
        elif self.btnp_action("confirm", pyxel.KEY_RETURN2):
            self.difficulty = self.diff_cursor
            self._apply_selections()
            self.start_fade_to("PLAYING")
        if moved:
            self.play_sfx(9)
    def update_shop(self):
        moved = False
        if self.btnp_action("up", pyxel.KEY_W):
            self.shop_cursor = (self.shop_cursor - 1) % len(SHOP_UPGRADES)
            moved = True
        elif self.btnp_action("down", pyxel.KEY_S):
            self.shop_cursor = (self.shop_cursor + 1) % len(SHOP_UPGRADES)
            moved = True
        elif self.btnp_action("pause"):
            self.start_fade_to("TITLE")
        elif self.btnp_action("confirm", pyxel.KEY_RETURN2):
            upgrade = SHOP_UPGRADES[self.shop_cursor]
            upgrade_id = upgrade["id"]
            current_level = self.save_data["upgrades"].get(upgrade_id, 0)
            if current_level < upgrade["max_level"]:
                cost = upgrade["costs"][current_level]
                if self.save_data["coins"] >= cost:
                    self.save_data["coins"] -= cost
                    new_level = current_level + 1
                    self.save_data["upgrades"][upgrade_id] = new_level
                    stats = self.save_data["stats"]
                    stats["upgrades_bought"] = stats.get("upgrades_bought", 0) + 1
                    if new_level >= upgrade["max_level"]:
                        stats["max_upgrade_level"] = max(stats.get("max_upgrade_level", 0), 1)
                    self.check_achievements()
                    self.save_data = save_save(self.save_data)
                    self.play_sfx(6)
        if moved:
            self.play_sfx(9)
    def _apply_selections(self):
        if not (self.arcade_mode or self.daily_mode) and self.selected_character not in self.save_data["unlocked_characters"]:
            self.selected_character = 0
        char_data = CHARACTER_DATA[self.selected_character]
        self.weapon_inventory = [char_data["weapon"]]
        upgrades = {} if self.arcade_mode else self.save_data["upgrades"]
        starting_weapon_level = 1 + upgrades.get("weapon_level", 0)
        self.weapon_levels = {char_data["weapon"]: starting_weapon_level}
        self.weapon_cooldowns = {char_data["weapon"]: 0}
        if not (self.arcade_mode or self.daily_mode):
            self.difficulty = self.diff_cursor

        max_hp_level = upgrades.get("max_hp", 0)
        speed_level = upgrades.get("speed", 0)
        xp_bonus_level = upgrades.get("xp_bonus", 0)
        self.base_player_max_hp = int(PLAYER_START_HP * (1 + max_hp_level * 0.10))
        self.player_max_hp = self.base_player_max_hp
        self.player_hp = self.player_max_hp
        self.player_speed = PLAYER_SPEED * (1 + speed_level * 0.05)

        diff = DIFFICULTY_DATA[self.difficulty]
        self.spawn_interval = int(SPAWN_INTERVAL_FRAMES * diff["spawn_mult"])
        self.spawn_timer = self.spawn_interval
        self.player_xp_next = int(LEVEL_XP_THRESHOLDS[self.player_level] * diff["xp_mult"] * (1 / (1 + xp_bonus_level * 0.10)))
    def get_time_scaling(self):
        minutes = self.timer_frames / (FPS * 60)
        intervals = int(minutes // 5)
        hp_scale = 1.0 + intervals * 0.10
        speed_scale = 1.0 + intervals * 0.10
        spawn_scale = max(0.3, 1.0 - intervals * 0.10)
        return hp_scale, speed_scale, spawn_scale
    def update_debug_controls(self):
        if not self.debug_mode:
            return
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
        if self.btnp_action("pause"):
            self.prev_state = self.state
            self.state = "PAUSED"
            return

        self.timer_frames += self.debug_time_scale
        current_biome = self.get_current_biome()[0]
        if current_biome != self.biome:
            self.play_sfx(8)
        self.biome = current_biome
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
        if self.btn_action("right", pyxel.KEY_D):
            dx += 1
        if self.btn_action("left", pyxel.KEY_A):
            dx -= 1
        if self.btn_action("down", pyxel.KEY_S):
            dy += 1
        if self.btn_action("up", pyxel.KEY_W):
            dy -= 1
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707

        self.player_x += dx * self.player_speed
        self.player_y += dy * self.player_speed
        if dx != 0 or dy != 0:
            self.facing_x = dx
            self.facing_y = dy

        if self.dash_cooldown == 0 and self.btnp_action("dash", pyxel.KEY_X):
            length = math.sqrt(self.facing_x * self.facing_x + self.facing_y * self.facing_y)
            if length == 0:
                dash_x = 1.0
                dash_y = 0.0
            else:
                dash_x = self.facing_x / length
                dash_y = self.facing_y / length
            self.player_x += dash_x * DASH_DISTANCE
            self.player_y += dash_y * DASH_DISTANCE
            self.dash_cooldown = DASH_COOLDOWN_FRAMES
            self.dash_invincible = DASH_INVINCIBLE_FRAMES
            self.play_sfx(5)

        if allow_spawning:
            self.update_spawning()
        self.record_pending_weapon_kills()
        self.update_enemies()
        self.rebuild_enemy_spatial_hash()
        self.update_boss_entity()
        self.update_enemy_projectiles()
        self.update_weapons()
        self.update_projectiles()
        self.update_damage_zones()
        self.update_gems()
        if not self.arcade_mode:
            self.update_live_stats()
            self.check_achievements()
        self.check_level_up()
    def defeat_boss(self):
        self.boss_hp = 0
        self.boss_active = False
        self.boss_defeated_this_run = True
        self.enemy_projectile_list.clear()
        self.start_fade_to("VICTORY")
    def apply_luck_critical(self, damage):
        crit_chance = 0.05 + self.luck * 0.02
        if random.random() < crit_chance:
            return damage * 1.5
        return damage
    def damage_boss(self, damage):
        if not self.boss_active or self.boss is None or self.boss["hp"] <= 0:
            return
        damage = self.apply_luck_critical(damage)
        old_hp = self.boss["hp"]
        self.boss["hp"] = max(0, self.boss["hp"] - damage)
        self.boss_damage_dealt += old_hp - self.boss["hp"]
        self.boss["flash_timer"] = 10
        self.boss_hp = max(0, int(self.boss["hp"]))
        if self.boss["hp"] <= 0:
            self.defeat_boss()
    def update_paused(self):
        if self.btnp_action("pause"):
            self.state = self.prev_state
    def update_boss(self):
        self._tick_sfx_cooldowns()
        self.update_debug_controls()
        if self.btnp_action("pause"):
            self.prev_state = "BOSS"
            self.state = "PAUSED"
            return

        self.timer_frames += self.debug_time_scale
        current_biome = self.get_current_biome()[0]
        if current_biome != self.biome:
            self.play_sfx(8)
        self.biome = current_biome
        self.update_active_game(allow_spawning=False)
    def calculate_score(self):
        diff_mult = self.difficulty + 1
        self.final_score = self.kills * self.player_level * diff_mult
        high_score_key = "arcade_high_score" if self.arcade_mode else "high_score"
        stored_high_score = self.save_data.get(high_score_key, 0) if self.arcade_mode else self.high_score
        if self.final_score > stored_high_score and self.final_score > 0:
            if self.arcade_mode:
                self.save_data["arcade_high_score"] = self.final_score
            else:
                self.high_score = self.final_score
            self.is_new_high_score = True
        else:
            self.is_new_high_score = False

        victory = self.state == "VICTORY"
        coins = 0
        if not self.arcade_mode:
            minutes = self.timer_frames // (FPS * 60)
            coins = (
                COIN_BASE_PER_RUN
                + (minutes * COIN_PER_MINUTE)
                + (self.kills // 10 * COIN_PER_KILL)
                + (self.player_level * COIN_PER_LEVEL)
            )
            if victory:
                coins += COIN_VICTORY_BONUS
            if self.difficulty == 2:
                coins = int(coins * COIN_HARD_MODE_MULT)
            coin_bonus_level = self.save_data["upgrades"].get("coin_bonus", 0)
            coins = int(coins * (1 + coin_bonus_level * 0.15))
        self.coins_earned = coins

        if not self.arcade_mode:
            self.save_data["coins"] += coins
            self.save_data["total_coins_earned"] += coins
            stats = self.save_data["stats"]
            stats["total_kills"] += self.kills
            stats["max_level"] = max(stats.get("max_level", 1), self.player_level)
            stats["max_survival_frames"] = max(stats.get("max_survival_frames", 0), self.timer_frames)
            stats["total_play_time_frames"] = stats.get("total_play_time_frames", 0) + self.timer_frames
            stats["total_coins_earned"] = stats.get("total_coins_earned", 0) + coins
            stats["max_weapons_equipped"] = max(stats.get("max_weapons_equipped", 0), len(self.weapon_inventory))
            if victory or self.boss_defeated_this_run:
                stats["boss_kills"] = stats.get("boss_kills", 0) + 1
            if victory and self.difficulty == 2:
                stats["hard_clears"] = stats.get("hard_clears", 0) + 1
            for weapon_id, kill_count in self.weapon_kill_counts.items():
                stat_key = f"weapon_kills_{weapon_id}"
                stats[stat_key] = stats.get(stat_key, 0) + kill_count
            self.check_unlocks()
            self.check_achievements()

        if self.daily_mode and self.daily_seed is not None:
            date_key = str(self.daily_seed)
            result = {
                "score": self.final_score,
                "character": self.selected_character,
                "difficulty": self.difficulty,
                "time": self.timer_frames,
                "result": "victory" if victory else "defeat",
            }
            daily_results = self.save_data.setdefault("daily_results", {})
            if self.final_score >= daily_results.get(date_key, {}).get("score", -1):
                daily_results[date_key] = result

        run_record = {
            "mode": "arcade" if self.arcade_mode else "daily" if self.daily_mode else "normal",
            "character": self.selected_character,
            "difficulty": self.difficulty,
            "time_frames": self.timer_frames,
            "level": self.player_level,
            "kills": self.kills,
            "weapons": list(self.weapon_inventory),
            "result": "victory" if victory else "defeat",
            "coins_earned": self.coins_earned,
            "timestamp": int(time.time()),
        }
        self.save_data.setdefault("run_history", []).append(run_record)
        if len(self.save_data["run_history"]) > 10:
            self.save_data["run_history"] = self.save_data["run_history"][-10:]
        self.save_data = save_save(self.save_data)
    def check_unlocks(self):
        self.new_unlocks = []
        stats = self.save_data["stats"]
        unlocked_characters = self.save_data["unlocked_characters"]

        for char_id, condition in CHARACTER_UNLOCK_CONDITIONS.items():
            if char_id in unlocked_characters:
                continue
            condition_type = condition["type"]
            threshold = condition["threshold"]
            unlocked = False
            if condition_type == "total_kills" and stats["total_kills"] >= threshold:
                unlocked = True
            elif condition_type == "survival_frames" and stats["max_survival_frames"] >= threshold:
                unlocked = True
            elif condition_type == "boss_damage_percent" and self.boss_max_hp > 0:
                unlocked = self.boss_damage_dealt >= self.boss_max_hp * threshold / 100
            elif condition_type == "clear_normal" and self.state == "VICTORY" and self.difficulty == 1:
                unlocked = True
            elif condition_type == "clear_hard" and self.state == "VICTORY" and self.difficulty == 2:
                unlocked = True
            if unlocked:
                unlocked_characters.append(char_id)
                self.new_unlocks.append(("character", char_id))

        unlocked_weapons = self.save_data["unlocked_weapons"]
        for weapon_id, condition in WEAPON_UNLOCK_CONDITIONS.items():
            if weapon_id in unlocked_weapons or condition["type"] != "weapon_kills":
                continue
            kill_count = stats.get(f"weapon_kills_{condition['weapon_id']}", 0)
            if kill_count >= condition["threshold"]:
                unlocked_weapons.append(weapon_id)
                self.new_unlocks.append(("weapon", weapon_id))
    def reset_game(self):
        self.timer_frames = 0
        self.base_player_max_hp = PLAYER_START_HP
        self.player_speed = PLAYER_SPEED
        self.player_hp = PLAYER_START_HP
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
        self.magnet_range = PLAYER_START_MAGNET_RANGE
        self.hp_regen = 0.0
        self.hp_regen_timer = 0
        self.luck = 0.0
        self.weapon_damage_mult = 1.0
        self.evolution_ready = []
        self.evolution_done = False
        self.boss_defeated_this_run = False
        self.level_up_choices = []
        self.level_up_cursor = 0
        self.boss_active = False
        self.boss = None
        self.boss_hp = 0
        self.boss_max_hp = 0
        self.boss_damage_dealt = 0
        self.boss_warning_timer = 0
        self.kills = 0
        self.weapon_kill_counts = {}
        self.dash_cooldown = 0
        self.dash_invincible = 0
        self.player_invincible = 0
        self.player_flash = 0
        self.shake_frames = 0
        self.shake_intensity = 0
        self.particles = []
        self.selected_character = 0
        self.difficulty = self.get_default_difficulty_index()
        self.char_cursor = 0
        self.diff_cursor = self.difficulty
        self.biome = 0
        self.biome_start = 0
        self.enemy_list = []
        self.spawn_timer = SPAWN_INTERVAL_FRAMES
        self.spawn_interval = SPAWN_INTERVAL_FRAMES
        self.projectile_list = []
        self.enemy_projectile_list = []
        self.damage_zone_list = []
        self.garlic_tick_timer = 0
        self.gem_list = []
        self.enemy_spatial_hash.clear()
        self.sfx_cooldowns = {sound_id: 0 for sound_id in (0, 1, 2, 5, 6, 7, 8, 9)}
        self.debug_time_scale = 1
        self.debug_overlay = False
        self.debug_mode = False
        self.score_calculated = False
        self.is_new_high_score = False
        self.achievement_popup = None
        self.final_score = 0
        self.coins_earned = 0
        self.arcade_mode = False
        self.daily_mode = False
        self.daily_seed = None
        self.daily_config = None
    def update_game_over(self):
        if not getattr(self, "score_calculated", False):
            self.calculate_score()
            self.score_calculated = True
            
        if self.btnp_action("confirm", pyxel.KEY_RETURN2):
            self.reset_game()
            self.start_fade_to("TITLE")
    def update_victory(self):
        if not getattr(self, "score_calculated", False):
            self.calculate_score()
            self.score_calculated = True
            
        if self.btnp_action("confirm", pyxel.KEY_RETURN2):
            self.reset_game()
            self.start_fade_to("TITLE")


for _module in (enemies, weapons, screens):
    for _name in getattr(_module, "__all__", (name for name in dir(_module) if not name.startswith("_"))):
        _func = getattr(_module, _name)
        if callable(_func):
            setattr(App, _name, _func)


App()
