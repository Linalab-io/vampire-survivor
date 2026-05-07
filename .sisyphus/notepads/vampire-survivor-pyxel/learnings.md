# Learnings

## 2026-05-06: Project Setup
- Pyxel game: 160x120 screen, 30fps, 16-color palette
- Single main.py file with App class pattern
- Art quality: VS original level (dark fantasy pixel art at 16x16)
- No external files, all sprites created in code via pyxel.images[].set()
- MCP tools for QA: validate_script, run_and_capture, play_and_capture, inspect_state
- Verified `inspect_state` reports the App instance after frame updates, so `timer_frames` is 31 at requested frame 30 because `update()` increments once per frame.

## 2026-05-06: Sprite Bank Definition
- Pyxel MCP `image.set(x, y, data)` for this harness expects `list[str]` row data, not one multiline string.
- Loading sprite data in `__init__` after `pyxel.init()` and before `pyxel.run()` works cleanly with the existing state machine unchanged.
- `inspect_sprite` confirmed the main references are readable: Knight at (0,0), Skeleton at (0,32), Grass tile at (0,128).

## Task 4: Title Screen
- Used `pyxel.rectb` for drawing border decorations.
- Used `pyxel.frame_count % 30 < 15` for blinking text animation.
- Verified text centering using `_draw_centered_text` helper.
- Verified state transition from `TITLE` to `CHAR_SELECT` using `play_and_capture` with simulated `KEY_RETURN` input.

## Task 5: HUD Rendering
- Added `player_xp` and `player_xp_next` to `App.__init__`.
- Created `draw_hud` method to render HP bar, XP bar, Level text, and Timer.
- Called `draw_hud` from `draw_playing`, `draw_boss`, `draw_level_up`, and `draw_paused`.
- Used `pyxel.rect` for bars and `pyxel.text` for text.
- Timer calculation: `timer_frames // 30` gives total seconds, which is then formatted as MM:SS.

## Task 6: Player Movement and Camera
- Added `PLAYER_SPEED = 1.5` and persistent `facing_x`/`facing_y` fields for movement direction tracking.
- `update_playing()` uses Arrow keys and WASD, with diagonal axes normalized by `0.707` before applying speed.
- `draw_playing()` keeps the player sprite screen-centered at `(72, 52)` for a 16x16 sprite around `(80, 60)` and uses `colkey=0` transparency.
- Pyxel MCP `inspect_state` cannot simulate menu/movement input; input-sensitive state evidence was saved separately to `.sisyphus/evidence/task-6-state-sim.json`.

## Task 7: Infinite Scrolling Deterministic Tiles
- Added `_tile_hash(wx, wy)` and `tile_type(wx, wy)` so tile variants are stable for the same world tile coordinates.
- `draw_ground()` uses camera offset from `player_x/player_y`, selects biome from `timer_frames`, and renders only a 12x9 visible tile window.
- Pyxel validation warns about tile `blt()` without `colkey`; this is intentional because ground tiles fill the full 16x16 tile area.

## Task 8: Dash Ability
- Added `dash_invincible` alongside the existing `dash_cooldown` state and updated both counters only during `PLAYING`.
- Dash uses the last facing vector, normalizes it before applying the 40px teleport, and falls back to right when the facing vector is still zero.
- HUD dash feedback reuses `SPR_GEM` at `(16, 192)` with a cyan cooldown bar that shrinks as `dash_cooldown` counts down.

## Task 9: Biome Transition Blend
- Added `get_current_biome()` to return `(primary_biome, secondary_biome, blend_ratio)` so rendering and future spawn weighting can share the same time-based biome logic.
- Implemented 30-second transition zones before the 5:00, 10:00, and 20:00 boundaries by switching tiles deterministically with `_tile_hash(tx, ty)` instead of frame-random blending.
- Exposed `self.biome` so state inspection can report the active primary biome during QA.
- Pyxel validation still warns about `blt()` calls without `colkey`; that warning is expected for ground tiles because they intentionally fill the full 16x16 tile area.

## Task 10: Enemy Spawning and Cap Management
- Added `ENEMY_DATA` with spawn unlock times and kept runtime enemies as lean dictionaries containing only type, position, hp, speed, facing, anim_frame, and ai_state.
- `update_spawning()` uses a 60-frame adjustable interval, a 50-enemy cap, and a 112px radial spawn distance from the player so new enemies start outside the 160x120 camera view.
- `update_enemies()` only runs chase movement inside 200px, idles farther enemies, and filters out hp <= 0 or distance > 500px before syncing `enemy_count`.
- Pyxel MCP validation still reports the known ground-tile `blt()` without `colkey`; enemy and player sprites use `colkey=0`.

## Task 11: Skeleton Contact Damage
- Added `player_invincible` to the core player state and decremented it during `update_playing()` alongside dash timers.
- Added 12px enemy contact damage in `update_enemies()` with a 60-frame invincibility window and `GAME_OVER` transition when HP reaches 0.
- Blink rendering for the player uses `pyxel.frame_count % 2` while invincible; normal sprite drawing resumes after the timer ends.
- `python -m py_compile main.py` and `lsp_diagnostics` both passed after the change.

## Task 14: XP Gems and Magnet Collection
- Enemy death handling should split hp <= 0 before despawn filtering so dead enemies can drop XP gems and increment kills in the same frame.
- Gem updates work cleanly with a simple distance check: despawn beyond 500px, pull toward the player within 30px, collect within 8px, then sync gem_count from gem_list.
- A small 4x4 blit from SPR_XP_GEM at (32, 192) is enough for the on-screen pickup marker without adding new art paths.

## Task 15: XP / Level Thresholds
- Use a module-level `LEVEL_XP_THRESHOLDS` table and initialize `player_xp_next` from the current level index instead of a hardcoded value.
- `check_level_up()` should preserve XP overflow, bump `player_max_hp` by 2, and switch to `LEVEL_UP` while storing `prev_state` for later return flow.
- Calling the level-up check after gems and weapons keeps XP collection responsive without touching combat or spawn logic.
- Implemented level up screen with 3 choices using random.sample.
- Used pyxel.line with step 2 to create a semi-transparent dark overlay effect.

## Task 17: Weapon and Passive Upgrade Effects
- Keep base stats separate from derived passive stats; `base_player_max_hp` lets Hollow Heart and flat Max HP choices recalculate cleanly.
- Weapon levels are tracked in `weapon_levels`; Whip runtime stats should come from `get_weapon_stats()` so damage, area, and cooldown modifiers stack in one path.
- Passive inventory remains `{"id", "level"}` dicts, with `recalculate_passive_stats()` applying immediate bonuses and capping passives at 5 levels.

## Task 18: Passive Item System
- `recalculate_passive_stats()` already drives derived passive values; `hp_regen` is accumulated from Pummarola levels and `magnet_range` still comes from `30 * magnet_mult`.
- HP regeneration is frame-based in `update_playing()`: a dedicated `hp_regen_timer` ticks to 180 frames, then heals `ceil(self.hp_regen)` and clamps at `player_max_hp`.
- `get_passive_level()` already returns the equipped level for a passive ID, so evolution gating can reuse passive inventory entries directly.

## Task 25: Weapon Evolution System
- Evolved weapon IDs 8-15 live alongside base weapon data, and `get_weapon_stats()` selects from evolved data before applying existing level/passive multipliers.
- Level-up evolution choices are represented as `type: "evolution"` and replace one normal choice when `check_evolution()` finds a max-level base weapon plus required max-level passive.
- `apply_evolution()` swaps the base ID in `weapon_inventory`, transfers the same weapon level and current cooldown, and clears the base weapon state.

## Task 27: 30-Minute Boss Spawn
- Use module constants for the 30-minute frame threshold and 2-second warning so debug_time_scale can jump timer_frames without changing the warning duration.
- Keep boss as its own dict instead of adding it to enemy_list; clear regular enemies at spawn and run BOSS state through the shared active gameplay update with regular spawning disabled.
- Existing weapon damage paths need explicit boss hooks because most weapons iterate enemy_list directly; projectile, zone, whip, garlic, Soul Eater, and targeted projectile paths now account for boss_active.

## Task 28: Death Boss AI and Minions
- Boss AI remains isolated in the self.boss dict; boss projectiles use enemy_projectile_list with type "boss_homing" and per-frame steering in update_enemy_projectiles().
- Boss minion summons should account for the separate boss entity by reserving one slot from MAX_ENEMIES, keeping boss plus active minions at 50 or fewer.
- A fake pyxel module plus importlib can exercise App boss logic without opening a Pyxel window, while MCP run_and_capture still provides runnable-surface smoke QA.

## Task 29: Victory and Game Over Screens
- `self.high_score` should be updated when entering `GAME_OVER` or `VICTORY` state.
- `reset_game()` should reset all game state variables to their initial values.
- `draw_game_over` and `draw_victory` should display the score, high score, and weapon list.
- `getattr(self, "score_calculated", False)` is a safe way to check if the score has been calculated without throwing an `AttributeError` if it hasn't been initialized yet.

## Task 30: SFX 3종
- `pyxel.sound(0).set()`, `pyxel.sound(1).set()`, `pyxel.sound(2).set()` were added after `pyxel.init()` in `__init__`.
- A shared `self.sfx_cooldowns` map plus `play_sfx(sound_id)` keeps each effect from replaying more than once per 10 frames.
- Attack, kill, and level-up hooks are wired into the main combat and progression paths, including projectile hits and `update_enemies()` death handling.

## Task 31: Difficulty Scaling
- Added `get_time_scaling()` so elapsed time drives HP, speed, and spawn scaling from the shared 30 FPS timer.
- `update_spawning()` now stacks time scaling on top of difficulty multipliers for enemy HP/speed and reduces the spawn interval over time.
- `summon_boss_minions()` reuses the same time scaling so boss-summoned skeletons stay consistent with regular spawns.

## Task 32: Pause and Controls Display
- `update_playing()` now stores `self.prev_state = self.state` before switching to `PAUSED`, so resume returns to the exact state that was active when pause started.
- `update_paused()` stays input-minimal and only reacts to ESC, which keeps pause from advancing timer, enemies, weapons, XP, or dash logic.
- `draw_paused()` reuses `draw_playing()`, adds the same line-based dark overlay used by level-up, and keeps HUD visible while showing centered pause text plus bottom controls help.
- Enhanced draw_game_over and draw_victory to display passive items using PASSIVE_POOL.
- Improved layout to fit Time, Level, Kills, Score, High Score, Weapons, and Passives on the 160x120 screen.
- Added blinking 'NEW RECORD!' text for high scores in both game over and victory screens.

## Task 34: Balance Tuning and Time Scale Debug
- `debug_time_scale` is driven through a shared `update_debug_controls()` helper so PLAYING and BOSS states use identical F1/F2/F3/F4 behavior.
- `draw_playing()` now owns the debug overlay; `draw_boss()` reuses it through `draw_playing()` before drawing the boss HP bar.
- Existing XP thresholds, weapon damage, and enemy HP looked reasonable for the current early-game curve, so no balance constants were changed.

## Task 35: Full Game Flow Integration
- Full-flow smoke testing should cover menu transitions, level-up resume via `prev_state`, pause/resume from both PLAYING and BOSS, boss warning/fight/victory, game-over return, and post-reset state cleanliness.
- `reset_game()` must reset round-derived base stats before assigning current HP/max HP, and should also clear menu cursors, biome, SFX cooldowns, debug flags, score flags, boss warning/entity state, and `prev_state`.
- Boss integration needs explicit boss damage hooks for every weapon family; base Garlic aura required the same boss hook that Soul Eater already had.
- Any regular enemy summon path that can run during BOSS must reserve one slot for the separate boss entity so boss plus minions never exceeds `MAX_ENEMIES`.

## Task 36: 최종 리소스 정리 + README.md 생성
- Extracting magic numbers (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, etc.) to module-level constants improves readability and makes it easier to adjust game-wide settings.
- A comprehensive README.md is essential for single-file projects to explain the scope, mechanics, and controls that might not be obvious from the code alone.
- Using `python3 -m py_compile main.py` is a quick way to verify that minor cleanup didn't introduce syntax errors in a large file.
- Documenting weapon evolution pairs in the README helps players understand the strategic depth of the game.

## Final QA - 2026-05-07
- Pyxel MCP screenshots can be saved directly by invoking `python -m pyxel_mcp.harness` and `python -m pyxel_mcp.input_harness`; this avoids inline-only image results.
- State-only QA for menu-gated gameplay can use evidence-local patched copies of `main.py` that preserve source behavior while starting in specific states; never modify `main.py` for QA setup.
- Final QA approved: core scenarios 12/12, integration 2/2, edge cases 3 tested; evidence stored under `.sisyphus/evidence/final-qa/`.
