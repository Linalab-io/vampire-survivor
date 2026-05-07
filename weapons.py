import math
import random

import pyxel

from data import *

__all__ = [
    "recalculate_passive_stats",
    "update_gems",
    "check_level_up",
    "generate_level_up_choices",
    "projectile_hits_boss",
    "update_weapons",
    "get_passive_level",
    "get_weapon_stats",
    "check_evolution",
    "check_evolution_ready",
    "fire_whip",
    "fire_magic_wand",
    "fire_axe",
    "fire_knife",
    "fire_holy_water",
    "fire_garlic",
    "fire_cross",
    "fire_fire_wand",
    "fire_targeted_projectile",
    "fire_bloody_tear",
    "fire_holy_wand",
    "fire_death_spiral",
    "fire_thousand_edge",
    "fire_boros_sea",
    "fire_soul_eater",
    "fire_hyperlove",
    "fire_hellfire",
    "create_damage_zone",
    "update_projectiles",
    "update_damage_zones",
    "update_level_up",
    "apply_weapon_upgrade",
    "apply_evolution",
    "apply_passive_upgrade",
]


def _nearby_enemies_for_rect(self, x, y, width, height):
    return self.nearby_enemies(x + width / 2, y + height / 2, max(width, height) / 2 + ENEMY_HITBOX_SIZE)


def _knock_enemy_from_player(self, enemy, distance):
    dx = enemy["x"] - self.player_x
    dy = enemy["y"] - self.player_y
    distance_sq = dx * dx + dy * dy
    dist = math.sqrt(distance_sq) if distance_sq > 0 else 1
    enemy["x"] += dx / dist * distance
    enemy["y"] += dy / dist * distance
    enemy["knockback"] = KNOCKBACK_FRAMES
    self.rebuild_enemy_spatial_hash()


def _damage_enemy_with_weapon(self, enemy, damage, weapon_id):
    self.damage_enemy(enemy, damage)
    if enemy["hp"] <= 0:
        enemy["killed_by_weapon_id"] = weapon_id


def projectile_hits_boss(self, projectile, projectile_x, projectile_y, width, height):
    if not self.boss_active or self.boss is None or self.boss["hp"] <= 0:
        return False
    if projectile["type"] in ("cross", "hyperlove", "holy_wand", "death_spiral", "hellfire") and id(self.boss) in projectile["hit_enemy_ids"]:
        return False
    if not rect_overlap(projectile_x, projectile_y, width, height, self.boss["x"] - BOSS_HITBOX_HALF_SIZE, self.boss["y"] - BOSS_HITBOX_HALF_SIZE, BOSS_HITBOX_SIZE, BOSS_HITBOX_SIZE):
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
    self.magnet_range = PLAYER_START_MAGNET_RANGE * magnet_mult
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

    for enemy in _nearby_enemies_for_rect(self, min_x, min_y, max_x - min_x, max_y - min_y):
        enemy_hitbox_x = enemy["x"] - ENEMY_HITBOX_HALF_SIZE
        enemy_hitbox_y = enemy["y"] - ENEMY_HITBOX_HALF_SIZE
        if rect_overlap(
            min_x,
            min_y,
            max_x - min_x,
            max_y - min_y,
            enemy_hitbox_x,
            enemy_hitbox_y,
            ENEMY_HITBOX_SIZE,
            ENEMY_HITBOX_SIZE,
        ):
            _damage_enemy_with_weapon(self, enemy, weapon["damage"], 0)
            if enemy["hp"] <= 0:
                self.play_sfx(1)
            _knock_enemy_from_player(self, enemy, KNOCKBACK_DISTANCE)
    if self.boss_active and self.boss is not None:
        if rect_overlap(min_x, min_y, max_x - min_x, max_y - min_y, self.boss["x"] - BOSS_HITBOX_HALF_SIZE, self.boss["y"] - BOSS_HITBOX_HALF_SIZE, BOSS_HITBOX_SIZE, BOSS_HITBOX_SIZE):
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

    speed = PROJECTILE_SPEED_WAND * self.projectile_speed_mult
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
        "dx": self.facing_x * PROJECTILE_SPEED_AXE_X * self.projectile_speed_mult,
        "dy": PROJECTILE_SPEED_AXE_Y * self.projectile_speed_mult,
        "damage": weapon["damage"],
        "lifetime": PROJECTILE_AXE_LIFETIME,
        "weapon_id": weapon_id,
        "gravity": PROJECTILE_AXE_GRAVITY,
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

    speed = PROJECTILE_SPEED_KNIFE * self.projectile_speed_mult
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

    speed = PROJECTILE_SPEED_HOLY_WATER * self.projectile_speed_mult
    self.projectile_list.append({
        "type": "holy_water",
        "x": self.player_x,
        "y": self.player_y,
        "dx": dx * speed,
        "dy": dy * speed - PROJECTILE_HOLY_WATER_ARC * self.projectile_speed_mult,
        "damage": weapon["damage"],
        "lifetime": max(1, int(weapon["range"] / speed)),
        "weapon_id": weapon_id,
        "gravity": PROJECTILE_HOLY_WATER_GRAVITY,
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
    for enemy in self.nearby_enemies(self.player_x, self.player_y, weapon["range"] + ENEMY_HITBOX_HALF_SIZE):
        if enemy["hp"] <= 0:
            continue
        dx = enemy["x"] - self.player_x
        dy = enemy["y"] - self.player_y
        distance_sq = dx * dx + dy * dy
        if distance_sq <= range_sq:
            _damage_enemy_with_weapon(self, enemy, weapon["damage"], weapon_id)
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

    speed = PROJECTILE_SPEED_CROSS * self.projectile_speed_mult
    self.projectile_list.append({
        "type": "cross",
        "x": self.player_x,
        "y": self.player_y,
        "dx": dx * speed,
        "dy": dy * speed,
        "damage": weapon["damage"],
        "lifetime": max(1, int(weapon["range"] * 2 / speed) + RETURNING_PROJECTILE_EXTRA_FRAMES),
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
    self.fire_targeted_projectile(7, "fire_wand", PROJECTILE_SPEED_FIRE_WAND)

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
        projectile["explosion_damage"] = FIRE_WAND_EXPLOSION_DAMAGE * WEAPON_LEVELS[self.weapon_levels.get(weapon_id, 1)]["damage_mult"] * self.weapon_damage_mult
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

    for enemy in _nearby_enemies_for_rect(self, min_x, min_y, max_x - min_x, max_y - min_y):
        enemy_hitbox_x = enemy["x"] - ENEMY_HITBOX_HALF_SIZE
        enemy_hitbox_y = enemy["y"] - ENEMY_HITBOX_HALF_SIZE
        if rect_overlap(min_x, min_y, max_x - min_x, max_y - min_y, enemy_hitbox_x, enemy_hitbox_y, ENEMY_HITBOX_SIZE, ENEMY_HITBOX_SIZE):
            _damage_enemy_with_weapon(self, enemy, weapon["damage"], weapon_id)
            if enemy["hp"] <= 0:
                self.play_sfx(1)
            hit_count += 1
            _knock_enemy_from_player(self, enemy, EVOLVED_KNOCKBACK_DISTANCE)
    if hit_count > 0:
        self.player_hp = min(self.player_max_hp, self.player_hp + hit_count)
    if self.boss_active and self.boss is not None:
        if rect_overlap(min_x, min_y, max_x - min_x, max_y - min_y, self.boss["x"] - BOSS_HITBOX_HALF_SIZE, self.boss["y"] - BOSS_HITBOX_HALF_SIZE, BOSS_HITBOX_SIZE, BOSS_HITBOX_SIZE):
            self.damage_boss(weapon["damage"])
            self.player_hp = min(self.player_max_hp, self.player_hp + 1)

def fire_holy_wand(self):
    self.fire_targeted_projectile(9, "holy_wand", PROJECTILE_SPEED_HOLY_WAND)

def fire_death_spiral(self):
    weapon_id = 10
    weapon = self.get_weapon_stats(weapon_id)
    self.weapon_cooldowns[weapon_id] = weapon["cooldown"]
    self.play_sfx(0)
    speed = PROJECTILE_SPEED_DEATH_SPIRAL * self.projectile_speed_mult
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
    speed = PROJECTILE_SPEED_THOUSAND_EDGE * self.projectile_speed_mult
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
    distance = min(weapon["range"], BOROS_SEA_MAX_DISTANCE)
    self.create_damage_zone(
        self.player_x + math.cos(angle) * distance,
        self.player_y + math.sin(angle) * distance,
        weapon["damage"],
        weapon_id,
        size=BOROS_SEA_ZONE_SIZE,
        timer=BOROS_SEA_ZONE_TIMER,
        tick_interval=BOROS_SEA_TICK_INTERVAL,
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
    for enemy in self.nearby_enemies(self.player_x, self.player_y, weapon["range"] + ENEMY_HITBOX_HALF_SIZE):
        if enemy["hp"] <= 0:
            continue
        dx = enemy["x"] - self.player_x
        dy = enemy["y"] - self.player_y
        if dx * dx + dy * dy <= range_sq:
            _damage_enemy_with_weapon(self, enemy, weapon["damage"], weapon_id)
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
    speed = PROJECTILE_SPEED_HYPERLOVE * self.projectile_speed_mult
    for side in (-1, 1):
        self.projectile_list.append({
            "type": "hyperlove",
            "x": self.player_x,
            "y": self.player_y,
            "dx": dx * speed + -dy * side * PROJECTILE_HYPERLOVE_SIDE_SPEED,
            "dy": dy * speed + dx * side * PROJECTILE_HYPERLOVE_SIDE_SPEED,
            "damage": weapon["damage"],
            "lifetime": max(1, int(weapon["range"] * 2 / speed) + RETURNING_PROJECTILE_EXTRA_FRAMES),
            "weapon_id": weapon_id,
            "gravity": 0,
            "traveled": 0.0,
            "max_range": weapon["range"],
            "returning": False,
            "hit_enemy_ids": [],
        })

def fire_hellfire(self):
    self.fire_targeted_projectile(15, "hellfire", PROJECTILE_SPEED_HELLFIRE)

def create_damage_zone(self, x, y, damage, weapon_id, size=DAMAGE_ZONE_SIZE, timer=DAMAGE_ZONE_TIMER, tick_interval=DAMAGE_ZONE_TICK_INTERVAL):
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

        width, height = PROJECTILE_HITBOXES.get(projectile["type"], DEFAULT_PROJECTILE_HITBOX)
        projectile_x = projectile["x"] - width / 2
        projectile_y = projectile["y"] - height / 2
        hit_enemy = False

        for enemy in _nearby_enemies_for_rect(self, projectile_x, projectile_y, width, height):
            if enemy["hp"] <= 0:
                continue
            if projectile["type"] in ("cross", "hyperlove", "holy_wand", "death_spiral", "hellfire") and id(enemy) in projectile["hit_enemy_ids"]:
                continue
            if rect_overlap(projectile_x, projectile_y, width, height, enemy["x"] - ENEMY_HITBOX_HALF_SIZE, enemy["y"] - ENEMY_HITBOX_HALF_SIZE, ENEMY_HITBOX_SIZE, ENEMY_HITBOX_SIZE):
                if projectile["type"] == "holy_water":
                    self.create_damage_zone(projectile["x"], projectile["y"], projectile["damage"], projectile["weapon_id"])
                    hit_enemy = True
                    break
                if projectile["type"] in ("fire_wand", "hellfire"):
                    _damage_enemy_with_weapon(self, enemy, projectile["damage"], projectile["weapon_id"])
                    if enemy["hp"] <= 0:
                        self.play_sfx(1)
                    _knock_enemy_from_player(self, enemy, KNOCKBACK_DISTANCE)
                    explosion_range_sq = (HELLFIRE_EXPLOSION_RADIUS if projectile["type"] == "hellfire" else FIRE_WAND_EXPLOSION_RADIUS) ** 2
                    for splash_enemy in self.nearby_enemies(projectile["x"], projectile["y"], math.sqrt(explosion_range_sq) + ENEMY_HITBOX_HALF_SIZE):
                        if splash_enemy["hp"] <= 0:
                            continue
                        splash_dx = splash_enemy["x"] - projectile["x"]
                        splash_dy = splash_enemy["y"] - projectile["y"]
                        if splash_dx * splash_dx + splash_dy * splash_dy <= explosion_range_sq:
                            _damage_enemy_with_weapon(self, splash_enemy, projectile["explosion_damage"], projectile["weapon_id"])
                            if splash_enemy["hp"] <= 0:
                                self.play_sfx(1)
                    if projectile["type"] == "hellfire":
                        projectile["hit_enemy_ids"].append(id(enemy))
                    else:
                        hit_enemy = True
                        break
                    continue

                _damage_enemy_with_weapon(self, enemy, projectile["damage"], projectile["weapon_id"])
                if enemy["hp"] <= 0:
                    self.play_sfx(1)
                _knock_enemy_from_player(self, enemy, KNOCKBACK_DISTANCE)
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
            if projectile["lifetime"] > 0 and dx * dx + dy * dy > RETURNING_PROJECTILE_PLAYER_RADIUS_SQ:
                kept_projectiles.append(projectile)
        elif not hit_enemy and projectile["lifetime"] > 0:
            kept_projectiles.append(projectile)

    self.projectile_list = kept_projectiles


def update_damage_zones(self):
    kept_zones = []
    for zone in self.damage_zone_list:
        if zone["timer"] % zone["tick_interval"] == 0:
            for enemy in _nearby_enemies_for_rect(self, zone["x"], zone["y"], zone["width"], zone["height"]):
                if enemy["hp"] <= 0:
                    continue
                if rect_overlap(zone["x"], zone["y"], zone["width"], zone["height"], enemy["x"] - ENEMY_HITBOX_HALF_SIZE, enemy["y"] - ENEMY_HITBOX_HALF_SIZE, ENEMY_HITBOX_SIZE, ENEMY_HITBOX_SIZE):
                    _damage_enemy_with_weapon(self, enemy, zone["damage"], zone["weapon_id"])
                    if enemy["hp"] <= 0:
                        self.play_sfx(1)
            if self.boss_active and self.boss is not None:
                if rect_overlap(zone["x"], zone["y"], zone["width"], zone["height"], self.boss["x"] - BOSS_HITBOX_HALF_SIZE, self.boss["y"] - BOSS_HITBOX_HALF_SIZE, BOSS_HITBOX_SIZE, BOSS_HITBOX_SIZE):
                    self.damage_boss(zone["damage"])
        zone["timer"] -= 1
        if zone["timer"] > 0:
            kept_zones.append(zone)

    self.damage_zone_list = kept_zones

def update_level_up(self):
    if self.btnp_action("up", pyxel.KEY_W):
        self.level_up_cursor = (self.level_up_cursor - 1) % LEVEL_UP_CHOICE_COUNT
    elif self.btnp_action("down", pyxel.KEY_S):
        self.level_up_cursor = (self.level_up_cursor + 1) % LEVEL_UP_CHOICE_COUNT
    elif self.btnp_action("confirm", pyxel.KEY_RETURN2):
        choice = self.level_up_choices[self.level_up_cursor]
        if choice["type"] == "passive":
            self.apply_passive_upgrade(choice["id"])
        elif choice["type"] == "weapon":
            self.apply_weapon_upgrade(choice["id"])
        elif choice["type"] == "evolution":
            self.apply_evolution(choice["base_id"], choice["evolved_id"])
        elif choice["type"] == "stat":
            self.base_player_max_hp += STAT_MAX_HP_BONUS
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
    self.evolution_done = True
    if not getattr(self, "arcade_mode", False):
        stats = self.save_data["stats"]
        stats["evolutions_done"] = stats.get("evolutions_done", 0) + 1
        self.check_achievements()
    self.check_evolution_ready()
    self.play_sfx(6)

def apply_passive_upgrade(self, passive_id):
    for passive in self.passive_inventory:
        if passive["id"] == passive_id:
            passive["level"] = min(MAX_PASSIVE_LEVEL, passive["level"] + 1)
            self.recalculate_passive_stats()
            return

    if len(self.passive_inventory) < MAX_PASSIVE_SLOTS:
        self.passive_inventory.append({"id": passive_id, "level": 1})
        self.recalculate_passive_stats()


def update_gems(self):
    magnet_range = self.magnet_range
    collect_range = GEM_COLLECT_RANGE
    despawn_range_sq = GEM_DESPAWN_RADIUS * GEM_DESPAWN_RADIUS
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
            self.spawn_particles(gem["x"], gem["y"], GEM_COLLECT_PARTICLE_COUNT, GEM_COLLECT_PARTICLE_COLOR, GEM_COLLECT_PARTICLE_LIFE)
            continue

        if dist <= magnet_range and dist > 0:
            gem["x"] += dx / dist * GEM_MAGNET_SPEED
            gem["y"] += dy / dist * GEM_MAGNET_SPEED

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
    self.base_player_max_hp += LEVEL_UP_HP_BONUS
    self.recalculate_passive_stats()
    self.spawn_particles(self.player_x, self.player_y, LEVEL_UP_PARTICLE_COUNT, LEVEL_UP_PARTICLE_COLOR, LEVEL_UP_PARTICLE_LIFE, size=LEVEL_UP_PARTICLE_SIZE, radius=LEVEL_UP_PARTICLE_RADIUS)
    self.prev_state = self.state
    self.generate_level_up_choices()
    self.play_sfx(2)
    self.state = "LEVEL_UP"

def generate_level_up_choices(self):
    candidates = []
    available_evolutions = self.check_evolution()
    unlocked_weapons = set(WEAPON_DATA) if getattr(self, "arcade_mode", False) else set(self.save_data["unlocked_weapons"])
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
        if weapon_id not in self.weapon_inventory and weapon_id not in unlocked_weapons:
            continue
        if weapon_id in self.weapon_inventory and self.weapon_levels.get(weapon_id, 1) < MAX_WEAPON_LEVEL:
            candidates.append(weapon_upgrade)
        elif weapon_id not in self.weapon_inventory and len(self.weapon_inventory) < MAX_WEAPON_SLOTS:
            candidates.append(weapon_upgrade)

    self.level_up_choices = []
    if len(candidates) >= LEVEL_UP_CHOICE_COUNT:
        self.level_up_choices = random.sample(candidates, LEVEL_UP_CHOICE_COUNT)
    else:
        self.level_up_choices = list(candidates)
        while len(self.level_up_choices) < LEVEL_UP_CHOICE_COUNT:
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
