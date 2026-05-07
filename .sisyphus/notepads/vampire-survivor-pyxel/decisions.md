# Decisions

## 2026-05-06: Architecture
- Single main.py file (Pyxel convention)
- State machine: TITLE → CHAR_SELECT → DIFF_SELECT → PLAYING ⇄ PAUSED/LEVEL_UP/BOSS → GAME_OVER/VICTORY
- Infinite map: deterministic tile function (no persistent chunk storage)
- Sprite bank layout: Bank 0 for all sprites/tiles
- Inspectable state variables on App instance for QA
