import math
import random

import pyxel

from data import *

__all__ = [
    "start_boss_fight",
    "update_boss_entity",
    "fire_boss_projectiles",
    "summon_boss_minions",
    "update_enemy_projectiles",
    "update_spawning",
    "update_enemies",
]

def start_boss_fight(self):
    diff = DIFFICULTY_DATA[self.difficulty]
    boss_hp = int(500 * diff["hp_mult"])
    self.enemy_list.clear()
    self.enemy_count = 0
    self.boss = {
        "x": self.player_x,
        "y": self.player_y - PLAYER_INVINCIBLE_FRAMES,
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
    self.shake_frames = 10
    self.shake_intensity = 4
    self.play_sfx(7)
    self.set_state("BOSS")

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
        self.damage_player(5)
        self.player_invincible = PLAYER_INVINCIBLE_FRAMES
        if self.player_hp <= 0:
            self.start_fade_to("GAME_OVER")

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
            "flash_frames": 0,
        })
    self.enemy_count = len(self.enemy_list)

def defeat_boss(self):
    self.boss_hp = 0
    self.boss_active = False
    self.enemy_projectile_list.clear()
    self.start_fade_to("VICTORY")

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
            if rect_overlap(projectile["x"] - 2, projectile["y"] - 2, 4, 4, self.player_x - PLAYER_HITBOX_HALF_SIZE, self.player_y - PLAYER_HITBOX_HALF_SIZE, PLAYER_HITBOX_SIZE, PLAYER_HITBOX_SIZE):
                self.damage_player(projectile["damage"])
                self.player_invincible = PLAYER_INVINCIBLE_FRAMES
                if self.player_hp <= 0:
                    self.start_fade_to("GAME_OVER")
                continue

        if projectile["lifetime"] > 0:
            kept_projectiles.append(projectile)

    self.enemy_projectile_list = kept_projectiles

def update_spawning(self):
    self.spawn_timer -= 1
    if self.spawn_timer > 0:
        self.enemy_count = len(self.enemy_list)
        return

    elapsed_seconds = self.timer_frames / FPS
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
        "flash_frames": 0,
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
        enemy["flash_frames"] = max(0, enemy.get("flash_frames", 0) - 1)
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
                        "flash_frames": 0,
                    })
                    added_enemies += 1
            self.spawn_particles(enemy["x"], enemy["y"], 5, self.get_enemy_color(enemy), 10)
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
                                "flash_frames": 0,
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

        kept_enemies.append(enemy)

    self.enemy_list = kept_enemies
    self.rebuild_enemy_spatial_hash()
    if self.dash_invincible <= 0 and self.player_invincible <= 0:
        for enemy in self.nearby_enemies(self.player_x, self.player_y, PLAYER_HIT_RADIUS):
            dx = self.player_x - enemy["x"]
            dy = self.player_y - enemy["y"]
            if dx * dx + dy * dy <= PLAYER_HIT_RADIUS * PLAYER_HIT_RADIUS:
                damage = 3 if enemy["type"] == 7 and enemy.get("dash_active") else PLAYER_CONTACT_DAMAGE
                self.damage_player(damage)
                self.player_invincible = PLAYER_INVINCIBLE_FRAMES
                if self.player_hp <= 0:
                    self.start_fade_to("GAME_OVER")
                break
    self.enemy_count = len(self.enemy_list)
