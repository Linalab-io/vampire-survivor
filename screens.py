import random

import pyxel

from data import *
from data import _tile_hash
from sprites import *

__all__ = [
    "draw_fade_overlay",
    "draw_title",
    "draw_shop",
    "draw_stats",
    "draw_achievements",
    "draw_arcade",
    "draw_daily_challenge",
    "draw_run_history",
    "draw_settings",
    "draw_achievement_popup",
    "draw_char_select",
    "draw_diff_select",
    "draw_playing",
    "draw_debug_overlay",
    "draw_boss_entity",
    "draw_enemies",
    "draw_projectiles",
    "draw_enemy_projectiles",
    "draw_ground",
    "get_current_biome",
    "draw_level_up",
    "draw_paused",
    "draw_boss",
    "draw_boss_hp_bar",
    "draw_game_over",
    "draw_victory",
    "draw_hud",
    "_draw_centered_text",
]

def draw_fade_overlay(self):
    if self.fade_alpha <= 0:
        return
    if self.fade_alpha >= 15:
        pyxel.rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0)
        return
    for y in range(0, SCREEN_HEIGHT, 2):
        for x in range(0, SCREEN_WIDTH, 2):
            if ((x // 2) + (y // 2) * 3) % 16 < self.fade_alpha:
                pyxel.rect(x, y, 2, 2, 0)

def draw_title(self):
    pyxel.rectb(4, 4, 152, 112, 2)
    pyxel.rectb(6, 6, 148, 108, 8)

    self._draw_centered_text("VAMPIRE SURVIVORS", 40, 8)
    self._draw_centered_text("Pyxel Edition", 52, 5)

    if pyxel.frame_count % 30 < 15:
        self._draw_centered_text("PRESS ENTER TO START", 62, 7)
    self._draw_centered_text("S/RIGHT: SHOP  A: ACH  D: STATS", 78, 6)
    self._draw_centered_text("3: ARCADE  4: DAILY", 90, 10)
    self._draw_centered_text("5: HISTORY  6: SETTINGS", 102, 6)

def draw_arcade(self):
    pyxel.rectb(4, 4, 152, 112, 9)
    pyxel.rectb(6, 6, 148, 108, 10)
    self._draw_centered_text("ARCADE MODE", 12, 10)
    self._draw_centered_text("Pure skill challenge", 28, 7)
    pyxel.text(18, 44, "Knight / Normal", 7)
    pyxel.text(18, 54, "All weapons available", 6)
    pyxel.text(18, 64, "No shop bonuses or coins", 6)
    pyxel.text(18, 78, f"High Score: {self.save_data.get('arcade_high_score', 0)}", 10)
    self._draw_centered_text("ENTER: Start  ESC: Back", 106, 7)

def draw_daily_challenge(self):
    if self.daily_seed is None or self.daily_config is None:
        self.daily_seed = get_daily_seed()
        self.daily_config = get_daily_config(self.daily_seed)
    config = self.daily_config
    date_key = str(self.daily_seed)
    result = self.save_data.get("daily_results", {}).get(date_key)
    pyxel.rectb(4, 4, 152, 112, 12)
    pyxel.rectb(6, 6, 148, 108, 5)
    self._draw_centered_text("DAILY CHALLENGE", 10, 12)
    pyxel.text(16, 26, f"Seed: {date_key}", 7)
    pyxel.text(16, 38, f"Character: {CHARACTER_DATA[config['character']]['name']}", 10)
    pyxel.text(16, 50, f"Difficulty: {DIFFICULTY_DATA[config['difficulty']]['name']}", 10)
    pyxel.text(16, 62, f"Biome Start: {BIOME_DATA[config['biome_start']]['name']}", 10)
    if result:
        pyxel.text(16, 78, f"Best: {result.get('score', 0)} pts", 6)
        pyxel.text(16, 88, f"Time: {_format_frames_ms(result.get('time', 0))}", 6)
    else:
        pyxel.text(16, 82, "No local result today", 6)
    self._draw_centered_text("ENTER: Start  ESC: Back", 106, 7)

def draw_run_history(self):
    pyxel.rectb(4, 4, 152, 112, 13)
    self._draw_centered_text("RUN HISTORY", 8, 13)
    history = list(reversed(self.save_data.get("run_history", [])))
    if not history:
        self._draw_centered_text("No runs recorded", 54, 5)
        self._draw_centered_text("ESC: Back", 110, 7)
        return
    start = min(getattr(self, "run_history_scroll", 0), max(0, len(history) - 4))
    rows = history[start:start + 4]
    for row, record in enumerate(rows):
        y = 22 + row * 20
        character = CHARACTER_DATA[record.get("character", 0)]["name"]
        difficulty = DIFFICULTY_DATA[record.get("difficulty", 1)]["name"]
        result = "Victory" if record.get("result") == "victory" else "Defeat"
        mode = record.get("mode", "normal").upper()[:6]
        pyxel.rectb(8, y - 2, 144, 18, 10 if row == 0 and start == 0 else 5)
        pyxel.text(11, y, f"{mode} {character[:7]} {difficulty[:4]} {result}", 7)
        pyxel.text(11, y + 8, f"{_format_frames_ms(record.get('time_frames', 0))} Lv{record.get('level', 1)} K{record.get('kills', 0)} C+{record.get('coins_earned', 0)}", 6)
    if len(history) > 4:
        self._draw_centered_text(f"UP/DOWN {start + 1}-{start + len(rows)}/{len(history)}", 101, 6)
    self._draw_centered_text("ESC: Back", 110, 7)

def draw_settings(self):
    pyxel.rectb(4, 4, 152, 112, 11)
    self._draw_centered_text("SETTINGS", 10, 11)
    sfx_index = self._setting_volume_index(self.config["volume"]["sfx"])
    bgm_index = self._setting_volume_index(self.config["volume"]["bgm"])
    rows = [
        ("SFX Volume", SETTINGS_VOLUME_LABELS[sfx_index]),
        ("BGM Volume", SETTINGS_VOLUME_LABELS[bgm_index]),
        ("Default Difficulty", self.config.get("default_difficulty", "Normal")),
    ]
    for index, (label, value) in enumerate(rows):
        y = 36 + index * 18
        selected = index == self.settings_cursor
        pyxel.rect(10, y - 3, 140, 13, 1 if selected else 0)
        pyxel.rectb(10, y - 3, 140, 13, 10 if selected else 5)
        pyxel.text(16, y, label, 7 if selected else 6)
        pyxel.text(98, y, f"< {value} >", 10 if selected else 7)
    self._draw_centered_text("UP/DOWN Select  LEFT/RIGHT Change", 96, 6)
    self._draw_centered_text("ESC: Back", 108, 7)

def draw_shop(self):
    pyxel.rectb(4, 4, 152, 112, 10)
    self._draw_centered_text("SHOP", 8, 10)
    pyxel.text(10, 18, f"COINS: {self.save_data['coins']}", 10)

    upgrades = self.save_data["upgrades"]
    start_y = 28
    row_h = 15
    for index, upgrade in enumerate(SHOP_UPGRADES):
        y = start_y + index * row_h
        selected = index == self.shop_cursor
        current_level = upgrades.get(upgrade["id"], 0)
        max_level = upgrade["max_level"]
        border_color = 10 if selected else 5
        text_color = 7 if selected else 6
        pyxel.rectb(8, y, 144, 13, border_color)
        pyxel.text(12, y + 2, upgrade["name"][:10], text_color)
        for level in range(max_level):
            color = 10 if level < current_level else 1
            pyxel.rect(56 + level * 5, y + 3, 3, 3, color)
        if current_level >= max_level:
            pyxel.text(96, y + 2, "MAX", 10)
        else:
            cost = upgrade["costs"][current_level]
            color = 10 if self.save_data["coins"] >= cost else 5
            pyxel.text(96, y + 2, f"BUY {cost}", color)
        pyxel.text(12, y + 8, upgrade["desc"][:32], 13)

    self._draw_centered_text("ENTER: Buy | ESC: Back", 108, 7)

def _format_frames_hms(frames):
    total_seconds = frames // FPS
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def _format_frames_ms(frames):
    total_seconds = frames // FPS
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def draw_stats(self):
    pyxel.rectb(4, 4, 152, 112, 12)
    self._draw_centered_text("STATISTICS", 8, 12)
    stats = self.save_data["stats"]
    rows = [
        ("Total Play Time", _format_frames_hms(stats.get("total_play_time_frames", 0))),
        ("Total Kills", str(stats.get("total_kills", 0))),
        ("Highest Level", str(stats.get("max_level", 1))),
        ("Longest Survival", _format_frames_ms(stats.get("max_survival_frames", 0))),
        ("Boss Defeats", str(stats.get("boss_kills", 0))),
        ("Total Coins Earned", str(max(stats.get("total_coins_earned", 0), self.save_data.get("total_coins_earned", 0)))),
        ("Total Runs", str(len(self.save_data.get("run_history", [])))),
    ]
    for index, (label, value) in enumerate(rows):
        y = 24 + index * 11
        pyxel.text(12, y, f"{label}:", 7)
        pyxel.text(102, y, value, 10)
    self._draw_centered_text("ESC: Back", 110, 7)

def draw_achievements(self):
    pyxel.rectb(4, 4, 152, 112, 10)
    self._draw_centered_text("ACHIEVEMENTS", 6, 10)
    unlocked = set(self.save_data.get("achievements", []))
    total = len(ACHIEVEMENT_DEFS)
    pyxel.text(10, 16, f"{len(unlocked)}/{total} Unlocked", 7)
    page = min(getattr(self, "achieve_page", 0), max(0, (total - 1) // 5))
    start = page * 5
    end = min(start + 5, total)
    for row, achievement in enumerate(ACHIEVEMENT_DEFS[start:end]):
        y = 27 + row * 16
        is_unlocked = achievement["id"] in unlocked
        color = 7 if is_unlocked else 5
        mark = "OK" if is_unlocked else "--"
        name = achievement["name"].strip() if is_unlocked else "???"
        pyxel.text(10, y, mark, 10 if is_unlocked else 5)
        pyxel.text(24, y, name[:22], color)
        pyxel.text(24, y + 7, achievement["desc"][:32], 6 if is_unlocked else 5)
    if total > 5:
        self._draw_centered_text(f"UP/DOWN Page {page + 1}/{max(1, (total + 4) // 5)}", 101, 6)
    self._draw_centered_text("ESC: Back", 110, 7)

def draw_achievement_popup(self):
    popup = getattr(self, "achievement_popup", None)
    if popup is None:
        return
    pyxel.rect(12, 94, 136, 18, 0)
    pyxel.rectb(12, 94, 136, 18, 10)
    self._draw_centered_text("ACHIEVEMENT UNLOCKED!", 98, 10)
    self._draw_centered_text(popup["name"][:28], 106, 7)

def draw_char_select(self):
    self._draw_centered_text("SELECT CHARACTER", 4, 7)
    unlocked_characters = set(self.save_data["unlocked_characters"])
    new_character_unlocks = {unlock_id for unlock_type, unlock_id in getattr(self, "new_unlocks", []) if unlock_type == "character"}

    cards_per_row = 4
    card_w, card_h = 36, 22
    gap_x, gap_y = 4, 4
    start_x, start_y = 4, 20

    for i, char in enumerate(CHARACTER_DATA):
        col = i % cards_per_row
        row = i // cards_per_row
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)

        locked = i not in unlocked_characters
        pyxel.rect(x, y, card_w, card_h, char["color"])
        if i == self.char_cursor:
            pyxel.rectb(x - 1, y - 1, card_w + 2, card_h + 2, 10)

        pyxel.text(x + 2, y + 2, char["name"], 0)
        weapon_name = WEAPON_DATA[char["weapon"]]["name"][:6]
        pyxel.text(x + 2, y + 12, weapon_name, 7)
        if i in new_character_unlocks and not locked:
            pyxel.text(x + card_w - 18, y + 2, "NEW!", 10)
        if locked:
            for stripe_y in range(y, y + card_h, 4):
                pyxel.rect(x, stripe_y, card_w, 2, 0)
            lock_x = x + card_w // 2 - 4
            lock_y = y + 5
            pyxel.rectb(lock_x + 1, lock_y, 6, 5, 7)
            pyxel.rect(lock_x, lock_y + 5, 8, 6, 7)
            pyxel.rect(lock_x + 3, lock_y + 7, 2, 2, 0)
            condition = CHARACTER_UNLOCK_CONDITIONS.get(i, {})
            pyxel.text(x + 2, y + 15, condition.get("desc", "Locked")[:8], 6)

def draw_diff_select(self):
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
    shake_x = random.randint(-self.shake_intensity, self.shake_intensity) if self.shake_frames > 0 else 0
    shake_y = random.randint(-self.shake_intensity, self.shake_intensity) if self.shake_frames > 0 else 0
    self.draw_ground(shake_x, shake_y)
    cam_x = self.player_x - 80
    cam_y = self.player_y - 60
    character_sprite_x = self.selected_character * 16
    player_color = CHARACTER_DATA[self.selected_character]["color"]
    frame_y = 0
    if pyxel.frame_count % 30 >= 15:
        frame_y += 16
    self.draw_enemies(cam_x, cam_y, shake_x, shake_y)
    self.draw_boss_entity(cam_x, cam_y, shake_x, shake_y)
    self.draw_projectiles(cam_x, cam_y, shake_x, shake_y)
    self.draw_enemy_projectiles(cam_x, cam_y, shake_x, shake_y)
    for gem in self.gem_list:
        screen_x = int(gem["x"] - cam_x - 2 + shake_x)
        screen_y = int(gem["y"] - cam_y - 2 + shake_y)
        pyxel.blt(screen_x, screen_y, 0, SPR_XP_GEM[0], SPR_XP_GEM[1], 4, 4, colkey=0)
    if self.whip_attack_timer > 0:
        whip_weapon_id = 8 if 8 in self.weapon_inventory else 0
        whip_range = int(self.get_weapon_stats(whip_weapon_id)["range"])
        whip_x = 80 if self.whip_attack_side > 0 else 80 - whip_range
        whip_color = 2 if whip_weapon_id == 8 else 8
        pyxel.rect(whip_x + shake_x, 52 + shake_y, whip_range, 16, whip_color)
    if self.player_invincible <= 0 or pyxel.frame_count % 2 == 0:
        pyxel.blt(80 - 8 + shake_x, 60 - 8 + shake_y, 0, character_sprite_x, frame_y, 16, 16, colkey=0)
        pyxel.rect(76 + shake_x, 56 + shake_y, 8, 7, player_color)
        if self.player_flash > 0:
            pyxel.rect(76 + shake_x, 56 + shake_y, 8, 8, 8)
    for particle in self.particles:
        px = particle["x"] - cam_x + shake_x
        py = particle["y"] - cam_y + shake_y
        if 0 <= px < SCREEN_WIDTH and 0 <= py < SCREEN_HEIGHT:
            pyxel.rect(int(px), int(py), particle["size"], particle["size"], particle["color"])
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

def draw_boss_entity(self, cam_x, cam_y, shake_x=0, shake_y=0):
    if not self.boss_active or self.boss is None:
        return
    screen_x = int(self.boss["x"] - cam_x - 16 + shake_x)
    screen_y = int(self.boss["y"] - cam_y - 16 + shake_y)
    if self.boss.get("flash_timer", 0) > 0:
        pyxel.rect(screen_x, screen_y, 16, 16, 7)
        pyxel.rect(screen_x + 16, screen_y, 16, 16, 10)
        pyxel.rect(screen_x, screen_y + 16, 16, 16, 10)
        pyxel.rect(screen_x + 16, screen_y + 16, 16, 16, 7)
    else:
        pyxel.blt(screen_x, screen_y, 0, SPR_BOSS[0], SPR_BOSS[1], 32, 32, colkey=0)

def draw_enemies(self, cam_x, cam_y, shake_x=0, shake_y=0):
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
        screen_x = int(enemy["x"] - cam_x - 8 + shake_x)
        screen_y = int(enemy["y"] - cam_y - 8 + shake_y)
        if enemy.get("flash_frames", 0) > 0:
            pyxel.rect(screen_x, screen_y, 16, 16, 7)
        else:
            pyxel.blt(screen_x, screen_y, 0, sprite_x, sprite_y, 16, 16, colkey=0)

def draw_projectiles(self, cam_x, cam_y, shake_x=0, shake_y=0):
    aura_weapon_id = 13 if 13 in self.weapon_inventory else 5 if 5 in self.weapon_inventory else None
    if aura_weapon_id is not None:
        garlic_range = int(self.get_weapon_stats(aura_weapon_id)["range"])
        aura_color = 11 if aura_weapon_id == 13 else 10
        pyxel.circb(int(self.player_x - cam_x + shake_x), int(self.player_y - cam_y + shake_y), garlic_range, aura_color)

    for zone in self.damage_zone_list:
        if zone["timer"] % 6 < 3:
            screen_x = int(zone["x"] - cam_x + shake_x)
            screen_y = int(zone["y"] - cam_y + shake_y)
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
        screen_x = int(projectile["x"] - cam_x - width / 2 + shake_x)
        screen_y = int(projectile["y"] - cam_y - height / 2 + shake_y)
        pyxel.rect(screen_x, screen_y, width, height, color)

def draw_enemy_projectiles(self, cam_x, cam_y, shake_x=0, shake_y=0):
    for projectile in self.enemy_projectile_list:
        screen_x = int(projectile["x"] - cam_x - 2 + shake_x)
        screen_y = int(projectile["y"] - cam_y - 2 + shake_y)
        pyxel.rect(screen_x, screen_y, 4, 4, 2)

def draw_ground(self, shake_x=0, shake_y=0):
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
            screen_x = tx * tile_w - int(cam_x) + shake_x
            screen_y = ty * tile_h - int(cam_y) + shake_y
            tile_hash = _tile_hash(tx, ty)
            active_biome = biome
            if secondary_biome != biome and tile_hash < blend_ratio * 0x100000000:
                active_biome = secondary_biome
            sprite_x = biome_tiles[active_biome][0]
            sprite_y = biome_tiles[active_biome][1] + variant * 16
            pyxel.blt(screen_x, screen_y, 0, sprite_x, sprite_y, 16, 16)

def get_current_biome(self):
    elapsed_seconds = self.timer_frames / FPS
    transition_seconds = BIOME_TRANSITION_SECONDS
    boundaries = [biome["boundary"] for biome in BIOME_DATA if biome["boundary"] is not None]

    biome_offset = getattr(self, "biome_start", 0)
    for biome, boundary in enumerate(boundaries):
        transition_start = boundary - transition_seconds
        if elapsed_seconds < transition_start:
            active = (biome + biome_offset) % len(BIOME_DATA)
            return active, active, 0.0
        if elapsed_seconds < boundary:
            blend_ratio = (elapsed_seconds - transition_start) / transition_seconds
            return (biome + biome_offset) % len(BIOME_DATA), (biome + 1 + biome_offset) % len(BIOME_DATA), blend_ratio

    active = (3 + biome_offset) % len(BIOME_DATA)
    return active, active, 0.0

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
    self._draw_centered_text("ESC:Resume | Arrows:Move | X:Dash", 110, 7)

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
    pyxel.rectb(4, 4, 152, 112, 8)
    pyxel.rectb(6, 6, 148, 108, 2)

    title = "ARCADE OVER" if getattr(self, "arcade_mode", False) else "DAILY OVER" if getattr(self, "daily_mode", False) else "GAME OVER"
    self._draw_centered_text(title, 10, 8)

    total_sec = self.timer_frames // FPS
    mins = total_sec // 60
    secs = total_sec % 60

    pyxel.text(15, 22, f"Time: {mins:02d}:{secs:02d}", 7)
    pyxel.text(85, 22, f"Level: Lv.{self.player_level}", 7)
    pyxel.text(15, 32, f"Kills: {self.kills}", 7)
    pyxel.text(85, 32, f"Score: {getattr(self, 'final_score', 0)}", 7)

    if getattr(self, "is_new_high_score", False) and pyxel.frame_count % 16 < 8:
        pyxel.text(15, 42, "NEW RECORD!", 10)
    else:
        high_score = self.save_data.get("arcade_high_score", 0) if getattr(self, "arcade_mode", False) else self.high_score
        pyxel.text(15, 42, f"High Score: {high_score}", 6)

    coin_label = "Coins: --" if getattr(self, "arcade_mode", False) else f"Coins: +{getattr(self, 'coins_earned', 0)}"
    pyxel.text(15, 50, coin_label, 10)
    pyxel.text(85, 50, f"Total: {self.save_data['coins']}", 10)

    pyxel.text(15, 60, "Weapons:", 7)
    weapon_names = []
    for w_id in self.weapon_inventory:
        if w_id < 8:
            weapon_names.append(WEAPON_DATA[w_id]["name"])
        else:
            weapon_names.append(EVOLVED_WEAPON_DATA[w_id]["name"])

    for i, name in enumerate(weapon_names[:6]):
        col = i % 3
        row = i // 3
        pyxel.text(15 + col * 50, 68 + row * 8, name[:10], 6)

    pyxel.text(15, 84, "Passives:", 7)
    passive_names = []
    for p in self.passive_inventory:
        passive_names.append(PASSIVE_POOL[p["id"]]["name"])

    for i, name in enumerate(passive_names[:6]):
        col = i % 3
        row = i // 3
        pyxel.text(15 + col * 50, 92 + row * 8, name[:10], 12)

    if pyxel.frame_count % 30 < 15:
        self._draw_centered_text("PRESS ENTER TO RETURN TO TITLE", 112, 7)

def draw_victory(self):
    pyxel.rectb(4, 4, 152, 112, 10)
    pyxel.rectb(6, 6, 148, 108, 7)

    title = "ARCADE CLEAR" if getattr(self, "arcade_mode", False) else "DAILY CLEAR" if getattr(self, "daily_mode", False) else "VICTORY!"
    self._draw_centered_text(title, 10, 10)

    total_sec = self.timer_frames // FPS
    mins = total_sec // 60
    secs = total_sec % 60

    pyxel.text(15, 22, f"Time: {mins:02d}:{secs:02d}", 7)
    pyxel.text(85, 22, f"Level: Lv.{self.player_level}", 7)
    pyxel.text(15, 32, f"Kills: {self.kills}", 7)
    pyxel.text(85, 32, f"Score: {getattr(self, 'final_score', 0)}", 10)

    if getattr(self, "is_new_high_score", False) and pyxel.frame_count % 16 < 8:
        pyxel.text(15, 42, "NEW RECORD!", 10)
    else:
        high_score = self.save_data.get("arcade_high_score", 0) if getattr(self, "arcade_mode", False) else self.high_score
        pyxel.text(15, 42, f"High Score: {high_score}", 10)

    coin_label = "Coins: --" if getattr(self, "arcade_mode", False) else f"Coins: +{getattr(self, 'coins_earned', 0)}"
    pyxel.text(15, 50, coin_label, 10)
    pyxel.text(85, 50, f"Total: {self.save_data['coins']}", 10)

    pyxel.text(15, 60, "Weapons:", 7)
    weapon_names = []
    for w_id in self.weapon_inventory:
        if w_id < 8:
            weapon_names.append(WEAPON_DATA[w_id]["name"])
        else:
            weapon_names.append(EVOLVED_WEAPON_DATA[w_id]["name"])

    for i, name in enumerate(weapon_names[:6]):
        col = i % 3
        row = i // 3
        pyxel.text(15 + col * 50, 68 + row * 8, name[:10], 6)

    pyxel.text(15, 84, "Passives:", 7)
    passive_names = []
    for p in self.passive_inventory:
        passive_names.append(PASSIVE_POOL[p["id"]]["name"])

    for i, name in enumerate(passive_names[:6]):
        col = i % 3
        row = i // 3
        pyxel.text(15 + col * 50, 92 + row * 8, name[:10], 12)

    if pyxel.frame_count % 30 < 15:
        self._draw_centered_text("PRESS ENTER TO RETURN TO TITLE", 112, 7)

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
    total_sec = self.timer_frames // FPS
    mins = total_sec // 60
    secs = total_sec % 60
    pyxel.text(128, 2, f"{mins:02d}:{secs:02d}", 7)
    wx = 2
    for weapon_id in self.weapon_inventory[:6]:
        pyxel.rect(wx, 114, 4, 4, self.get_weapon_display_color(weapon_id))
        pyxel.text(wx + 6, 114, f"Lv.{self.weapon_levels.get(weapon_id, 1)}", 7)
        wx += 22

def _draw_centered_text(self, text, y, color):
    pyxel.text((pyxel.width - len(text) * 4) // 2, y, text, color)
