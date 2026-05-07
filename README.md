# Vampire Survivors — Pyxel Edition

A Vampire Survivors-like survival game built with the Pyxel retro game engine. Survive waves of enemies, collect XP gems, level up, and evolve your weapons to defeat the ultimate boss.

## Features
- **8 Playable Characters**: Each with a unique starting weapon and color scheme.
- **8 Base Weapons**: Auto-attacking weapons with different behaviors (melee, projectile, aura).
- **8 Evolved Weapons**: Powerful upgrades achieved by combining max-level weapons with specific passive items.
- **8 Enemy Types**: Unique AI behaviors and stats, scaling in difficulty over time.
- **4 Biomes**: Dynamic environment transitions (Grassland, Desert, Cave, Castle) based on survival time.
- **Evolution System**: Strategic item combinations for massive power spikes.
- **30-Minute Challenge**: Survive until the 30:00 mark to face the final boss, Death.
- **3 Difficulty Levels**: Easy, Normal, and Hard modes to suit your skill level.
- **Dash Ability**: Quick movement with invincibility frames and a short cooldown.
- **Retro Aesthetics**: 160x120 resolution, 16-color palette, and chiptune SFX.

## Installation
Ensure you have Python installed, then install Pyxel:
```bash
pip install pyxel
```

## How to Run
Run the game using Python:
```bash
python main.py
```

## Controls
- **Arrow Keys / WASD**: Move character
- **Space / X**: Dash (includes brief invincibility)
- **ESC**: Pause / Resume game
- **Enter**: Select / Confirm in menus
- **F1-F4 (Debug)**:
  - **F1**: Increase game speed (2x)
  - **F2**: Decrease game speed (0.5x)
  - **F3**: Reset game speed
  - **F4**: Toggle debug overlay

## How to Play
1. **Survive**: Move around to avoid enemies and let your weapons auto-attack.
2. **Level Up**: Collect XP gems dropped by defeated enemies to fill your XP bar.
3. **Choose Upgrades**: Each level-up allows you to pick a new weapon, passive item, or upgrade an existing one.
4. **Evolve**: Maximize a weapon's level and possess the required passive item to unlock its evolved form during level-up.
5. **Defeat Death**: Survive for 30 minutes to spawn the final boss. Defeat it to win!

## Weapon Evolutions
| Base Weapon | Passive Item | Evolved Weapon |
| :--- | :--- | :--- |
| Whip | Hollow Heart | Bloody Tear |
| Magic Wand | Empty Tome | Holy Wand |
| Axe | Candelabrador | Death Spiral |
| Knife | Bracer | Thousand Edge |
| Holy Water | Attractorb | Boros Sea |
| Garlic | Pummarola | Soul Eater |
| Cross | Clover | Hyperlove |
| Fire Wand | Spinach | Hellfire |

## Technical Notes
- **Engine**: Pyxel (Python)
- **Resolution**: 160x120
- **Frame Rate**: 30 FPS
- **Assets**: All sprites and sounds are generated programmatically within `main.py`.
- **Codebase**: Single-file implementation (~2600 lines).

## Credits
- **Game Design**: Inspired by *Vampire Survivors* by poncle.
- **Engine**: Built with [Pyxel](https://github.com/kitao/pyxel).
- **Project**: Unity Indie School Project.
