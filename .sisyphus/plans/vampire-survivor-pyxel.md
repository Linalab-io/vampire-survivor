# Vampire Survivors Pyxel Clone — Phased Work Plan

## TL;DR

> **Quick Summary**: Pyxel 엔진으로 Vampire Survivors 클론 게임을 8개 페이즈에 걸쳐 구축합니다. Vertical slice(1캐릭터, 1무기, 2적) → 시스템 확장 → 콘텐츠 충원 → 폴리시 순서로 진행합니다.
> 
> **Deliverables**:
> - 완전한 VS 클론 Pyxel 게임 (`main.py` + 리소스 파일)
> - 6-8종 무기 / 6-8종 적 / 6-8종 캐릭터 / 4-6종 바이옴
> - 타이틀 → 캐릭터 선택 → 난이도 선택 → 게임 → 게임오버 전체 흐름
> - 무기 진화 시스템, 30분 보스전, 대시 능력
> - SFX (공격/킬/레벨업)
> 
> **Estimated Effort**: XL (40-60 tasks)
> **Parallel Execution**: YES - 8 Phases
> **Critical Path**: Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → Phase 7 → Phase 8 → Final Verification

---

## Context

### Original Request
뱀파이어 서바이버 라이크 장르의 게임을 Pyxel로 만들기. VS 오리지널 기획에서 적당히 가져와서 충실한 클론 우선 완성.

### Interview Summary
**Key Discussions**:
- 30라운드 소크라테스식 인터뷰 완료, 모호성 0.90 → 0.02
- 장르 특성으로 정해진 것은 재질문하지 않음
- 무기/적 세부 디자인은 VS 원작에서 차용 (내가 결정)
- 세션 기록만 유지 (파일 저장 없음)
- VS 클론 우선, 독자적 요소는 나중에

**Research Findings**:
- Pyxel: 160×120 화면, 16색 팔레트, 3개 이미지 뱅크(256×256), 4 오디오 채널
- 16×16 스프라이트로 6-8종 구분 → 실루엣/팔레트 discipline 필요
- 50적 화면 제한 + Python 성능 → 공간 분할 또는 거리 기반 필터링 필수
- MCP 도구로 자동 QA 가능: `validate_script`, `play_and_capture`, `inspect_state`, `capture_frames`, `render_audio`

### Metis Review
**Identified Gaps** (addressed):
- MVP vs Full completion 기준 불명확 → Phase별 vertical slice 후 확장으로 해결
- 승리 조건 불명확 → 보스 처치 시 승리로 명확화
- 무기/패시브/진화 조합 미고정 → Phase 6에서 명세화
- 무한 맵 구현 방식 → deterministic tile function으로 결정 (영속 저장 아님)
- 아트 품질 기준 → **VS 원작 수준의 픽셀아트 품질** (단순 플레이스홀더가 아닌, Vampire Survivors 원작의 다크 판타지 비주얼 퀄리티를 16×16/16색으로 재현)
- 30분 QA 현실성 → debug time scale / injectable timer 필요
- Edge case 다수 → guardrails에 명시

---

## Work Objectives

### Core Objective
Pyxel 엔진으로 Vampire Survivors의 핵심 게임플레이 루프를 충실하게 재현한 클론 게임을 완성한다.

### Concrete Deliverables
- `main.py`: 메인 게임 파일 (Pyxel convention에 따른 App 클래스 구조)
- `resources/`: Pyxel 리소스 파일 (.pyxres 또는 코드 내 생성)
- 6-8종 무기 (근접/원거리/특수 혼합)
- 6-8종 적 (패턴 다양성: 돌진, 원거리, 분열, 소환 등)
- 6-8종 캐릭터 (시작 무기만 다름)
- 4-6종 바이옴 타일
- 타이틀/선택/게임오버 UI
- SFX 3종 (공격/킬/레벨업)

### Definition of Done
- [ ] `python -m py_compile main.py` → PASS
- [ ] Pyxel MCP `validate_script main.py` → no errors
- [ ] `run_and_capture`로 타이틀 화면 캡처 가능
- [ ] `play_and_capture`로 타이틀→캐릭터선택→난이도선택→게임 시작 전환 성공
- [ ] `inspect_state`로 게임 내 상태 검증 (state, hp, level, enemy_count, timer)
- [ ] 30분 생존 → 보스 등장 → 보스 처치 시 승리 화면
- [ ] 게임오버 화면에 통계 표시 (시간, 레벨, 킬, 무기)

### Must Have
- 8방향 이동 (Arrow + WASD)
- 무기 자동 공격
- XP 젬 + 자석 수집
- 레벨업 시 3개 선택지 (게임 일시정지)
- 무기 진화 (무기 + 패시브 아이템 = 진화 무기)
- 대시 능력 (Space/X, 쿨다운)
- 30분 타이머 + 보스전
- 3 난이도 (Easy/Normal/Hard)
- 최대 50적 화면 제한
- HUD: HP바 + XP바 + 타이머
- 게임오버 통계 화면

### Must NOT Have (Guardrails)
- ❌ Unity 의존성
- ❌ 영속 세이브 파일
- ❌ BGM (SFX만)
- ❌ 온라인/멀티플레이어
- ❌ 메타 프로그레션/언록
- ❌ 하이레스 에셋
- ❌ 물리 엔진
- ❌ 컨트롤러 지원 (향후 요청 시)
- ❌ VS 클론 베이스라인 이전의 독자적 메커니즘
- ❌ 무한 chunk 영속 저장 (메모리에 카메라 주변만 유지)
- ❌ 과도한 추상화 (단순한 data-driven table 사용)
- ❌ AI slop: 과도한 주석, 불필요한 유틸리티 추상화, 제네릭 네이밍

---

## Game Design Specification

### Weapons (8 types from VS originals)

| # | Name | Type | Behavior | Evolution | Passive Required |
|---|------|------|----------|-----------|-------------------|
| 1 | **Whip** | Melee | Player 주변 좌우 휘두름 | Bloody Tear | Hollow Heart |
| 2 | **Magic Wand** | Ranged | 가장 가까운 적에게 투사체 발사 | Holy Wand | Empty Tome |
| 3 | **Axe** | Thrown | 위로 부메랑처럼 던짐 | Death Spiral | Candelabrador |
| 4 | **Knife** | Ranged | facing direction으로 빠른 투사체 | Thousand Edge | Bracer |
| 5 | **Holy Water** | Area | 바닥에 던져서 데미지 존 생성 | Boros Sea | Attractorb |
| 6 | **Garlic** | Aura | 주변 적에게 지속 데미지 + 넉백 | Soul Eater | Pummarola |
| 7 | **Cross/Boomerang** | Thrown | 부메랑 궤적으로 돌아옴 | Hyperlove | Clover |
| 8 | **Fire Wand** | Ranged | 랜덤 적에게 화염 투사체 | Hellfire | Spinach |

### Passive Items (8 types, paired with weapons for evolution)

| # | Name | Effect | Paired Weapon |
|---|------|--------|---------------|
| 1 | Hollow Heart | Max HP +10% | → Whip evolution |
| 2 | Empty Tome | Cooldown -8% | → Magic Wand evolution |
| 3 | Candelabrador | Area +10% | → Axe evolution |
| 4 | Bracer | Projectile Speed +10% | → Knife evolution |
| 5 | Attractorb | Magnet Range +25% | → Holy Water evolution |
| 6 | Pummarola | HP Recovery/sec | → Garlic evolution |
| 7 | Clover | Luck +10% | → Cross evolution |
| 8 | Spinach | Damage +10% | → Fire Wand evolution |

### Enemies (8 types, dark fantasy theme)

| # | Name | Behavior | HP | Speed | Appears |
|---|------|----------|-----|-------|---------|
| 1 | **Skeleton** | Walk toward player | Low | Slow | 0:00 |
| 2 | **Bat** | Fast, erratic movement | Low | Fast | 0:30 |
| 3 | **Ghost** | Phase through others, medium speed | Medium | Medium | 2:00 |
| 4 | **Zombie** | Slow, high HP, tanks | High | Very Slow | 3:00 |
| 5 | **Dark Mage** | Ranged, shoots projectiles at player | Medium | Slow | 5:00 |
| 6 | **Slime** | Splits into 2 smaller slimes on death | Low | Medium | 7:00 |
| 7 | **Necromancer** | Summons 2 skeletons periodically | Medium | Slow | 10:00 |
| 8 | **Demon** | Fast, high damage, dashes at player | High | Fast | 15:00 |

### Characters (8, one per starting weapon)

| # | Name | Starting Weapon | Color Theme |
|---|------|-----------------|-------------|
| 1 | **Knight** | Whip | Silver/Blue |
| 2 | **Mage** | Magic Wand | Purple/Gold |
| 3 | **Viking** | Axe | Brown/Red |
| 4 | **Assassin** | Knife | Dark Gray/Black |
| 5 | **Cleric** | Holy Water | White/Gold |
| 6 | **Paladin** | Garlic | White/Silver |
| 7 | **Ranger** | Cross | Green/Brown |
| 8 | **Pyromancer** | Fire Wand | Red/Orange |

### Biomes (4 types, time-based transition)

| # | Name | Tile Colors | Transition Time |
|---|------|------------|-----------------|
| 1 | **Grassland** | Green tones | 0:00 - 5:00 |
| 2 | **Desert** | Sandy/yellow | 5:00 - 10:00 |
| 3 | **Cave** | Dark gray/blue | 10:00 - 20:00 |
| 4 | **Castle** | Dark purple/stone | 20:00 - 30:00 |

### Difficulty Scaling

| Setting | Enemy HP Mult | Enemy Speed Mult | Spawn Rate | XP Required |
|---------|--------------|-----------------|------------|-------------|
| Easy | ×0.7 | ×0.8 | ×0.7 | ×0.8 |
| Normal | ×1.0 | ×1.0 | ×1.0 | ×1.0 |
| Hard | ×1.5 | ×1.3 | ×1.5 | ×1.2 |

### Boss (appears at 30:00)

- **Death**: Large sprite (32×32, overlaid from 2 sprites)
- HP: 500 × difficulty multiplier
- Attacks: Slow homing projectiles + minion summon every 10 sec
- Minions: Skeletons (count: difficulty × 3)
- Victory condition: Boss HP ≤ 0 → Victory screen
- Boss counts toward 50 enemy cap (boss + minions ≤ 50)

---

## Verification Strategy

> **ZERO HUMAN INTERVENTION** - ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: NO (Pyxel game — visual QA via MCP)
- **Automated tests**: NONE (unit tests not applicable; MCP visual/state QA instead)
- **Framework**: Pyxel MCP tools
- **Primary QA**: Agent-executed via Pyxel MCP tools

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Visual QA**: `run_and_capture`, `capture_frames`, `play_and_capture` → 스크린샷
- **State QA**: `inspect_state` → 내부 상태 JSON 검증
- **Layout QA**: `inspect_layout`, `inspect_palette` → UI/색 검증
- **Audio QA**: `render_audio` → SFX 파형 검증
- **Code QA**: `validate_script`, `python -m py_compile` → 문법 검증

### Inspectable State Variables (MUST be exposed on App instance)
```python
# App class attributes for QA inspection:
self.state  # "TITLE" | "CHAR_SELECT" | "DIFF_SELECT" | "PLAYING" | "LEVEL_UP" | "PAUSED" | "BOSS" | "GAME_OVER" | "VICTORY"
self.timer_frames  # frames elapsed (timer_frames / (30*60) = minutes)
self.player_hp  # current HP
self.player_max_hp  # max HP
self.player_level  # current level
self.player_x, self.player_y  # world position
self.enemy_count  # enemies on screen
self.gem_count  # XP gems on screen
self.weapon_inventory  # list of weapon IDs
self.passive_inventory  # list of passive IDs
self.boss_active  # bool
self.boss_hp  # boss current HP
self.kills  # total kills
self.dash_cooldown  # frames remaining
self.selected_character  # character index
self.difficulty  # 0=Easy, 1=Normal, 2=Hard
self.high_score  # session high score
self.enemy_list  # list of active enemies (for count verification)
self.projectile_list  # list of active projectiles
self.gem_list  # list of active gems
```

---

## Execution Strategy

### Phase Overview

```
Phase 1: FOUNDATION — 프로젝트 뼈대 + 상태머신 + 기본 렌더링
  ├── Task 1: 프로젝트 초기화 + Pyxel 앱 스켈레톤 [quick]
  ├── Task 2: 게임 상태머신 + 화면 전환 [quick]
  ├── Task 3: 스프라이트/타일 데이터 정의 (코드 내) [quick]
  ├── Task 4: 타이틀 화면 [visual-engineering]
  └── Task 5: 기본 HUD 렌더링 [visual-engineering]

Phase 2: PLAYER + WORLD — 플레이어 이동/카메라/무한 맵
  ├── Task 6: 플레이어 이동 + 8방향 + 카메라 [deep]
  ├── Task 7: 무한 스크롤 맵 (deterministic tile) [deep]
  ├── Task 8: 대시 능력 [quick]
  └── Task 9: 바이옴 전환 시스템 [quick]

Phase 3: COMBAT CORE — 첫 무기 + 적 + 데미지 루프
  ├── Task 10: 적 스폰 시스템 + 캡 관리 [deep]
  ├── Task 11: 첫 적: Skeleton AI (플레이어 추적) [quick]
  ├── Task 12: 첫 무기: Whip (근접 범위 공격) [deep]
  ├── Task 13: 데미지/히트박스 시스템 [deep]
  └── Task 14: XP 젬 드롭 + 자석 수집 [quick]

Phase 4: PROGRESSION — 레벨업 + 업그레이드 선택
  ├── Task 15: XP/레벨 시스템 + threshold 테이블 [quick]
  ├── Task 16: 레벨업 화면 (3 선택지) [visual-engineering]
  ├── Task 17: 업그레이드 효과 적용 (무기/패시브) [deep]
  └── Task 18: 패시브 아이템 시스템 [quick]

Phase 5: EXPANSION — 추가 무기/적/캐릭터
  ├── Task 19: Magic Wand + Axe + Knife [deep]
  ├── Task 20: Holy Water + Garlic + Cross + Fire Wand [deep]
  ├── Task 21: Bat + Ghost + Zombie [quick]
  ├── Task 22: Dark Mage + Slime + Necromancer + Demon [deep]
  ├── Task 23: 캐릭터 선택 화면 (8캐릭터) [visual-engineering]
  └── Task 24: 난이도 선택 화면 (3단계) [visual-engineering]

Phase 6: EVOLUTION + BOSS — 무기 진화 + 30분 보스전
  ├── Task 25: 무기 진화 시스템 (무기+패시브=진화) [deep]
  ├── Task 26: 진화 무기 8종 구현 [deep]
  ├── Task 27: 30분 타이머 + 보스 spawn [deep]
  ├── Task 28: 보스 AI (Death) + 미니언 소환 [deep]
  └── Task 29: 승리/게임오버 화면 [visual-engineering]

Phase 7: AUDIO + POLISH — SFX + 난이도 스케일링 + 밸런스
  ├── Task 30: SFX 3종 (공격/킬/레벨업) [quick]
  ├── Task 31: 난이도 스케일링 적용 [quick]
  ├── Task 32: 일시정지 + 컨트롤 표시 [quick]
  ├── Task 33: 게임오버 통계 화면 [visual-engineering]
  └── Task 34: 밸런스 튜닝 + 타임 스케일 디버그 [deep]

Phase 8: INTEGRATION TEST — 전체 흐름 검증
  ├── Task 35: 전체 게임 플로우 통합 테스트 [deep]
  └── Task 36: 최종 리소스 정리 + README.md 생성 [writing]

Phase FINAL: VERIFICATION (after ALL tasks)
  ├── Task F1: Plan compliance audit [oracle]
  ├── Task F2: Code quality review [unspecified-high]
  ├── Task F3: Real manual QA via MCP [unspecified-high]
  └── Task F4: Scope fidelity check [deep]
```

### Dependency Matrix

| Task | Depends On | Blocks | Wave |
|------|-----------|--------|------|
| 1 | - | 2,3,4,5 | 1 |
| 2 | 1 | 6,15,16 | 1 |
| 3 | 1 | 6,7,10,11,12 | 1 |
| 4 | 1,2,3 | 23,24 | 1 |
| 5 | 1,2,3 | 16,33 | 1 |
| 6 | 2,3 | 8,10,13 | 2 |
| 7 | 3,6 | 9 | 2 |
| 8 | 6 | - | 2 |
| 9 | 7 | 34 | 2 |
| 10 | 3,6 | 11,14 | 3 |
| 11 | 3,10 | 21,22 | 3 |
| 12 | 3,6 | 13,19 | 3 |
| 13 | 6,12 | 14 | 3 |
| 14 | 10,13 | 15 | 3 |
| 15 | 14 | 16,17 | 4 |
| 16 | 5,15 | 23 | 4 |
| 17 | 15 | 18,25 | 4 |
| 18 | 17 | 25 | 4 |
| 19 | 12,17 | 25,26 | 5 |
| 20 | 12,17 | 25,26 | 5 |
| 21 | 11 | 22,35 | 5 |
| 22 | 11,21 | 27,35 | 5 |
| 23 | 4,16 | 35 | 5 |
| 24 | 4,23 | 35 | 5 |
| 25 | 17,18 | 26,35 | 6 |
| 26 | 19,20,25 | 35 | 6 |
| 27 | 22,25 | 28,35 | 6 |
| 28 | 22,27 | 29,35 | 6 |
| 29 | 27,28 | 33,35 | 6 |
| 30 | - | 35 | 7 |
| 31 | 10,15 | 35 | 7 |
| 32 | 2 | 35 | 7 |
| 33 | 5,29 | 35 | 7 |
| 34 | 9,31 | 35 | 7 |
| 35 | ALL above | 36 | 8 |
| 36 | 35 | F1-F4 | 8 |
| F1 | 36 | - | FINAL |
| F2 | 36 | - | FINAL |
| F3 | 36 | - | FINAL |
| F4 | 36 | - | FINAL |

### Agent Dispatch Summary

- **Phase 1** (5 tasks): T1-T3 → `quick`, T4-T5 → `visual-engineering`
- **Phase 2** (4 tasks): T6-T7 → `deep`, T8-T9 → `quick`
- **Phase 3** (5 tasks): T10, T12, T13 → `deep`, T11, T14 → `quick`
- **Phase 4** (4 tasks): T15, T17 → `deep`, T16 → `visual-engineering`, T18 → `quick`
- **Phase 5** (6 tasks): T19-T20 → `deep`, T21 → `quick`, T22 → `deep`, T23-T24 → `visual-engineering`
- **Phase 6** (5 tasks): T25-T29 → `deep` (except T29 → `visual-engineering`)
- **Phase 7** (5 tasks): T30-T32 → `quick`, T33 → `visual-engineering`, T34 → `deep`
- **Phase 8** (2 tasks): T35 → `deep`, T36 → `writing`
- **FINAL** (4 tasks): F1 → `oracle`, F2 → `unspecified-high`, F3 → `unspecified-high`, F4 → `deep`

---

## TODOs

> Implementation tasks are detailed below. Each task has QA scenarios using Pyxel MCP tools.

---

### Phase 1: FOUNDATION — 프로젝트 뼈대 + 상태머신 + 기본 렌더링

- [x] 1. 프로젝트 초기화 + Pyxel 앱 스켈레톤

  **What to do**:
  - `main.py` 생성: Pyxel convention에 따른 `App` 클래스 (`__init__`, `update`, `draw`)
  - `pyxel.init(160, 120, title="Vampire Survivors", fps=30)`
  - 기본 game state 변수 초기화 (위 "Inspectable State Variables" 참고)
  - `pyxel.run(self.update, self.draw)` 구조
  - ESC 키 → `pyxel.quit()` 바인딩
  - 디버그용 time scale 변수 `self.debug_time_scale = 1` 추가

  **Must NOT do**:
  - 게임 로직 구현 금지 (스켈레톤만)
  - 외부 파일 로드 금지 (코드 내 리소스만)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`pyxel`]
    - `pyxel`: Pyxel convention, validate_script, run_and_capture 필요

  **Parallelization**: Can start immediately. Blocks: 2,3,4,5. Wave 1.

  **References**:
  - Pyxel 공식 퀵스타트: `pyxel.init()`, `pyxel.run(update, draw)` 패턴
  - Inspectable State Variables: 위 "Verification Strategy" 섹션의 변수 목록 전체

  **Acceptance Criteria**:
  - [ ] `python -m py_compile main.py` → PASS
  - [ ] `validate_script main.py` → no errors
  - [ ] `run_and_capture main.py frames=60` → 검은 화면 또는 cls 화면 캡처
  - [ ] `inspect_state main.py frames=30` → `state`, `player_hp`, `timer_frames` 속성 존재

  **QA Scenarios**:

  ```
  Scenario: App initializes correctly
    Tool: Bash + Pyxel MCP (validate_script, run_and_capture, inspect_state)
    Preconditions: main.py exists
    Steps:
      1. Run `python -m py_compile main.py` → exit code 0
      2. `validate_script main.py` → no errors
      3. `run_and_capture main.py frames=60` → screenshot captured
      4. `inspect_state main.py frames=30 attributes="state,player_hp,timer_frames"` → JSON with state="TITLE", player_hp>0, timer_frames=0
    Expected Result: All 4 checks pass
    Evidence: .sisyphus/evidence/task-1-init.png, .sisyphus/evidence/task-1-state.json

  Scenario: ESC quits the app
    Tool: Pyxel MCP (play_and_capture)
    Preconditions: main.py runs
    Steps:
      1. `play_and_capture main.py inputs='[{"frame":30,"keys":["KEY_ESCAPE"]}]' frames="60"` → app exits cleanly
    Expected Result: Process exits with code 0, no hang
    Evidence: .sisyphus/evidence/task-1-esc-exit.txt
  ```

  **Commit**: YES - `feat(init): Pyxel app skeleton with state variables`

---

- [x] 2. 게임 상태머신 + 화면 전환

  **What to do**:
  - 상태 상수 정의: `"TITLE"`, `"CHAR_SELECT"`, `"DIFF_SELECT"`, `"PLAYING"`, `"LEVEL_UP"`, `"PAUSED"`, `"BOSS"`, `"GAME_OVER"`, `"VICTORY"`
  - `update()`에서 `self.state` 기반 분기: `update_title()`, `update_playing()` 등
  - `draw()`에서도 동일 분기: `draw_title()`, `draw_playing()` 등
  - 상태 전환 로직: TITLE→CHAR_SELECT (Enter), CHAR_SELECT→DIFF_SELECT (Enter), DIFF_SELECT→PLAYING (Enter)
  - PAUSED 전환: PLAYING 중 ESC → PAUSED, PAUSED 중 ESC → PLAYING
  - 각 상태의 `update_*`와 `draw_*` 메서드 stub 생성

  **Must NOT do**:
  - 실제 게임 로직 구현 금지 (상태 전환만)
  - 텍스트/스프라이트 디자인 금지 (placeholder만)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 1. Blocks: 6,15,16. Wave 1.

  **References**:
  - Task 1의 App 클래스 구조
  - 상태 전환 다이어그램: TITLE → CHAR_SELECT → DIFF_SELECT → PLAYING ⇄ PAUSED / LEVEL_UP / BOSS → GAME_OVER / VICTORY

  **Acceptance Criteria**:
  - [ ] `validate_script main.py` → no errors
  - [ ] `inspect_state main.py frames=30` → state == "TITLE"
  - [ ] `play_and_capture`로 Enter 3회 → state == "PLAYING"
  - [ ] `play_and_capture`로 ESC → state == "PAUSED"

  **QA Scenarios**:

  ```
  Scenario: State transitions from TITLE to PLAYING
    Tool: Pyxel MCP (play_and_capture, inspect_state)
    Preconditions: main.py with state machine
    Steps:
      1. `play_and_capture main.py inputs='[{"frame":10,"keys":["KEY_RETURN"]},{"frame":30,"keys":["KEY_RETURN"]},{"frame":50,"keys":["KEY_RETURN"]}]' frames="1,30,50,70"`
      2. `inspect_state main.py frames="70" attributes="state"` → state == "PLAYING"
    Expected Result: 3 screenshots showing state transitions, final state is "PLAYING"
    Evidence: .sisyphus/evidence/task-2-state-flow.png

  Scenario: PAUSED state stops game updates
    Tool: Pyxel MCP (play_and_capture, inspect_state)
    Preconditions: In PLAYING state
    Steps:
      1. `play_and_capture main.py inputs='[{"frame":10,"keys":["KEY_RETURN"]},{"frame":30,"keys":["KEY_RETURN"]},{"frame":50,"keys":["KEY_RETURN"]},{"frame":90,"keys":["KEY_ESCAPE"]}]' frames="80,100"`
      2. `inspect_state main.py frames="80,100" attributes="state,timer_frames"` → timer_frames should NOT increase between frame 80 and 100 when paused
    Expected Result: timer_frames is same at frame 80 and 100 (paused at frame 90)
    Evidence: .sisyphus/evidence/task-2-pause-state.json
  ```

  **Commit**: YES (groups with Task 1) - `feat(core): state machine and screen transitions`

---

- [x] 3. 스프라이트/타일 데이터 정의 (코드 내)

  **What to do**:
  - `pyxel.image(0)` 에 16×16 스프라이트 데이터를 코드로 직접 그리기 (`pyxel.images[0].set()` 또는 `pix` 문자열)
  - 이미지 뱅크 레이아웃 계획:
    - Bank 0 (0,0)-(255,255): Characters (8×16px per row = 16 sprites per row)
      - Row 0-1: Player sprites (8 characters × 2 frames = 16 slots → row 0-1)
      - Row 2-3: Enemy sprites (8 types × 2 frames = 16 slots → row 2-3)
      - Row 4: Boss sprite (32×32 = 2×2 grid)
      - Row 5-7: Weapon/effect sprites
    - Bank 0 continued: Tiles (16×16 each)
      - Row 8-11: Biome tiles (4 biomes × 4 variants = 16 tiles)
      - Row 12-15: UI elements (HP bar, XP bar, icons)
  - **VS 원작 수준 픽셀아트**: Vampire Survivors의 다크 판타지 비주얼을 16×16/16색으로 충실하게 재현
    - 캐릭터: 개별 직업 특성이 드러나는 장비/색상 디테일 (기사의 갑옷, 마법사의 로브, 도적의 후드 등)
    - 적: 각종 다크 판타지 크리처의 핵심 실루엣 + 색상 디테일 (해골 뼈다귀, 박쥐 날개, 좀비 상처 등)
    - 타일: 바이옴별 독특한 텍스처 (잔디 풀, 사막 모래, 동굴 석순, 늪 수초 등)
  - 스프라이트당 최소 3회 이상 반복 개선 (`inspect_sprite` → 수정 → 재검증)
  - 스프라이트 인덱스 상수 정의 (`SPR_PLAYER_KNIGHT = 0`, `SPR_ENEMY_SKELETON = 16` 등)

  **Must NOT do**:
  - 복잡한 픽셀아트 **권장** — VS 원작 수준의 시각 품질이 목표
  - 외부 이미지 파일 로드 금지 (pyxel 코드 내 생성만)
  - 대충 그린 플레이스홀더 금지 — 각 스프라이트는 inspect_sprite로 품질 검증 통과해야 함

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 1. Blocks: 6,7,10,11,12. Wave 1.

  **References**:
  - Characters 테이블: 8캐릭터, 색상 테마 (위 "Game Design Specification")
  - Enemies 테이블: 8종 (위 "Game Design Specification")
  - Biomes 테이블: 4종 (위 "Game Design Specification")
  - Pyxel `pyxel.images[0].set(x, y, data)` API

  **Acceptance Criteria**:
  - [ ] `validate_script main.py` → no errors
  - [ ] `inspect_bank main.py bank=0` → 스프라이트 데이터 보임
  - [ ] `inspect_sprite main.py x=0 y=0 w=16 h=16` → 플레이어 스프라이트 존재 + **VS 원작 수준 디테일** (장비/색상 식별 가능)
  - [ ] `inspect_sprite main.py x=0 y=32 w=16 h=16` → 적 스프라이트 존재 + **VS 원작 수준 디테일** (특징적 실루엣)

  **QA Scenarios**:

  ```
  Scenario: Sprite bank contains expected sprites
    Tool: Pyxel MCP (inspect_bank, inspect_sprite)
    Preconditions: main.py with sprite data
    Steps:
      1. `inspect_bank main.py bank=0` → image bank screenshot
      2. `inspect_sprite main.py x=0 y=0 w=16 h=16` → player sprite has non-zero pixels
      3. `inspect_sprite main.py x=0 y=32 w=16 h=16` → enemy sprite has non-zero pixels
      4. `inspect_sprite main.py x=0 y=128 w=16 h=16` → tile sprite exists
    Expected Result: Bank shows organized sprite layout with distinct colored sprites
    Evidence: .sisyphus/evidence/task-3-sprite-bank.png

  Scenario: Sprite palette uses distinct colors per character
    Tool: Pyxel MCP (inspect_palette)
    Preconditions: Sprites loaded
    Steps:
      1. `inspect_palette main.py frame=5` → color distribution report
    Expected Result: Multiple distinct colors used (at least 6 different palette indices)
    Evidence: .sisyphus/evidence/task-3-palette-report.txt
  ```

  **Commit**: YES (groups with 1-2) - `feat(assets): placeholder sprites, tiles, and layout constants`

---

- [x] 4. 타이틀 화면

  **What to do**:
  - `draw_title()`: 게임 타이틀 텍스트 "VAMPIRE SURVIVORS" (pyxel.text 중앙 배치)
  - 부제 "Pyxel Edition"
  - "PRESS ENTER TO START" 깜빡임 텍스트 (30프레임 주기)
  - 배경: 다크 판타지 톤 (검은 배경 + 보라/빨간 장식)
  - `update_title()`: Enter 키 → `state = "CHAR_SELECT"`

  **Must NOT do**:
  - 복잡한 애니메이션 금지 (텍스트+깜빡임만)
  - BGM 금지

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 1,2,3. Blocks: 23,24. Wave 1.

  **References**:
  - Pyxel `pyxel.text(x, y, text, color)` API
  - 화면 크기: 160×120, 텍스트 중앙 배치 기준
  - 색상: Pyxel 기본 팔레트 인덱스 사용 (0=black, 1=dark purple, 8=red 등)

  **Acceptance Criteria**:
  - [ ] `run_and_capture main.py frames=30` → 타이틀 화면 캡처
  - [ ] `inspect_layout main.py frame=30` → 텍스트 중앙 정렬 확인
  - [ ] `play_and_capture` Enter → state transitions to CHAR_SELECT

  **QA Scenarios**:

  ```
  Scenario: Title screen displays correctly
    Tool: Pyxel MCP (run_and_capture, inspect_layout)
    Preconditions: main.py starts
    Steps:
      1. `run_and_capture main.py frames=30` → screenshot
      2. `inspect_layout main.py frame=30` → layout analysis
    Expected Result: Title text centered, "PRESS ENTER" visible, dark background
    Evidence: .sisyphus/evidence/task-4-title.png, .sisyphus/evidence/task-4-layout.txt

  Scenario: Title blinking text
    Tool: Pyxel MCP (capture_frames)
    Preconditions: Title screen
    Steps:
      1. `capture_frames main.py frames="1,15,30,45,60"` → 5 screenshots
    Expected Result: "PRESS ENTER" text alternates visibility across frames
    Evidence: .sisyphus/evidence/task-4-blink.png
  ```

  **Commit**: YES - `feat(ui): title screen with dark fantasy theme`

---

- [x] 5. 기본 HUD 렌더링

  **What to do**:
  - `draw_hud()`: 화면 상단 고정 HUD
  - HP 바: 왼쪽 상단, 빨간색 막대 (player_hp / player_max_hp 비율)
  - XP 바: HP 바 아래, 파란색 막대 (현재 XP / 다음 레벨 XP 비율)
  - 타이머: 우측 상단, "MM:SS" 형식 (timer_frames / 1800 = 분, %60 = 초)
  - HUD는 화면 좌표에 고정 (월드 좌표 아님)
  - 레벨 표시: XP 바 옆에 "Lv.X"

  **Must NOT do**:
  - 복잡한 HUD 디자인 금지 (기본 막대+텍스트만)
  - 숫자/텍스트 이외의 장식 금지

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 1,2,3. Blocks: 16,33. Wave 1.

  **References**:
  - Pyxel `pyxel.rect(x, y, w, h, color)` for bars
  - Pyxel `pyxel.text(x, y, text, color)` for labels
  - 화면: 160×120, HUD는 상단 10-12픽셀 사용

  **Acceptance Criteria**:
  - [ ] `run_and_capture` PLAYING 상태 → HUD 보임 (HP바, XP바, 타이머)
  - [ ] `inspect_state` + `capture_frames` → HP/XP 감소 시 바 길이 변화
  - [ ] 타이머가 frame에 따라 증가

  **QA Scenarios**:

  ```
  Scenario: HUD displays HP, XP, timer during PLAYING state
    Tool: Pyxel MCP (play_and_capture, inspect_state, inspect_layout)
    Preconditions: In PLAYING state (need to reach via state transitions)
    Steps:
      1. `play_and_capture main.py inputs='[{"frame":10,"keys":["KEY_RETURN"]},{"frame":30,"keys":["KEY_RETURN"]},{"frame":50,"keys":["KEY_RETURN"]}]' frames="70"`
      2. `inspect_state main.py frames="70" attributes="state,player_hp,timer_frames"` → state=="PLAYING"
      3. Screenshot should show HP bar (red), XP bar (blue), timer (top right)
    Expected Result: All 3 HUD elements visible in screenshot
    Evidence: .sisyphus/evidence/task-5-hud.png

  Scenario: Timer increments over time
    Tool: Pyxel MCP (inspect_state)
    Preconditions: In PLAYING state
    Steps:
      1. `inspect_state main.py frames="70,100,130" attributes="timer_frames"` → values should increase: 70→100→130 approximately
    Expected Result: timer_frames strictly increasing
    Evidence: .sisyphus/evidence/task-5-timer.json
  ```

  **Commit**: YES - `feat(ui): basic HUD with HP bar, XP bar, timer`

---

### Phase 2: PLAYER + WORLD — 플레이어 이동/카메라/무한 맵

- [x] 6. 플레이어 이동 + 8방향 + 카메라

  **What to do**:
  - `update_playing()`: Arrow keys + WASD로 8방향 이동
  - 플레이어 위치: `self.player_x`, `self.player_y` (월드 좌표)
  - 이동 속도: `PLAYER_SPEED = 1.5` pixels/frame
  - 대각선 이동 시 속도 정규화 (√2로 나눔)
  - 카메라: 항상 플레이어를 화면 중앙에 배치
  - 화면 좌표 = 월드 좌표 - 카메라 오프셋
  - 플레이어 스프라이트: 화면 중앙 (80, 60)에 항상 고정
  - facing direction 추적: 마지막 이동 방향 기록

  **Must NOT do**:
  - 화면 밖 제한 금지 (무한 월드)
  - 충돌 처리 아직 구현 금지

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 2,3. Blocks: 8,10,13. Wave 2.

  **References**:
  - `pyxel.btn(pyxel.KEY_UP)`, `pyxel.btn(pyxel.KEY_W)` 등
  - 대각선 정규화: `dx, dy = dx * 0.707, dy * 0.707` (1/√2 ≈ 0.707)
  - 카메라 오프셋: `cam_x = player_x - 80`, `cam_y = player_y - 60`
  - 스프라이트 참조: Task 3의 SPR_PLAYER_* 상수

  **Acceptance Criteria**:
  - [ ] `play_and_capture`로 Arrow/WASD 이동 → 플레이어 월드 좌표 변화
  - [ ] `inspect_state`로 player_x, player_y 증가/감소 확인
  - [ ] 대각선 이동 시 속도가 수평/수직과 동일

  **QA Scenarios**:

  ```
  Scenario: Player moves with arrow keys
    Tool: Pyxel MCP (play_and_capture, inspect_state)
    Preconditions: In PLAYING state
    Steps:
      1. `play_and_capture main.py inputs='[{"frame":10,"keys":["KEY_RETURN"]},{"frame":30,"keys":["KEY_RETURN"]},{"frame":50,"keys":["KEY_RETURN"]},{"frame":60,"keys":["KEY_RIGHT"]},{"frame":90,"keys":[]}]' frames="55,90"`
      2. `inspect_state main.py frames="55,90" attributes="player_x,player_y"` → player_x should increase from frame 55 to 90
    Expected Result: player_x increased by ~45 pixels (1.5 * 30 frames), player_y unchanged
    Evidence: .sisyphus/evidence/task-6-move-right.json

  Scenario: Diagonal movement speed normalized
    Tool: Pyxel MCP (play_and_capture, inspect_state)
    Preconditions: In PLAYING state
    Steps:
      1. Move right only for 30 frames → record distance
      2. Move right+down for 30 frames → record distance
      3. Total distance should be approximately equal
    Expected Result: Both movements cover similar distance
    Evidence: .sisyphus/evidence/task-6-diagonal.json
  ```

  **Commit**: YES - `feat(player): 8-direction movement with camera system`

---

- [x] 7. 무한 스크롤 맵 (deterministic tile)

  **What to do**:
  - Deterministic tile function: `tile_type(wx, wy)` → 월드 좌표 기반 바이옴/타일 결정
  - 시드 기반 의사난수로 일관된 맵 생성: 같은 좌표 → 항상 같은 타일
  - 카메라 주변 타일만 렌더링: 화면에 보이는 160/16 × 120/16 = 10×8 = 80타일 + 여유분
  - chunk 기반 캐시: 8×8 타일 단위로 메모리에 유지, 벗어나면 폐기
  - 바이옴 결정: 시간 기반 (0-5분=grassland, 5-10분=desert, 10-20분=cave, 20-30분=castle)
  - `draw_ground()`: 카메라 오프셋 기반으로 타일 렌더링
  - 바이옴 내 변형: 4종 타일 패턴으로 시각적 다양성

  **Must NOT do**:
  - 영속 저장 금지 (메모리만)
  - 전체 맵 생성 금지 (카메라 주변만)
  - 타일맵 충돌 금지 (통과 가능)

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 3,6. Blocks: 9. Wave 2.

  **References**:
  - Deterministic pseudo-random: `hash((wx, wy)) % N` 패턴
  - Biomes 테이블 (위 "Game Design Specification")
  - Tile sprites: Task 3의 SPR_TILE_* 상수
  - Pyxel `pyxel.blt(x, y, img, u, v, w, h)` for tile rendering

  **Acceptance Criteria**:
  - [ ] `play_and_capture`로 이동 시 바닥 타일 스크롤
  - [ ] 같은 위치로 돌아오면 같은 타일 배치
  - [ ] 시간 경과에 따라 바이옴 색상 변화

  **QA Scenarios**:

  ```
  Scenario: Infinite map scrolls with player movement
    Tool: Pyxel MCP (play_and_capture, capture_frames)
    Preconditions: In PLAYING state with tile rendering
    Steps:
      1. `play_and_capture main.py inputs='[...] (navigate to PLAYING, then move right)' frames="70,100,130"`
      2. Screenshots should show different tile positions (scrolling)
    Expected Result: Ground tiles shift left as player moves right
    Evidence: .sisyphus/evidence/task-7-scroll.png

  Scenario: Deterministic tiles - same position same result
    Tool: Pyxel MCP (inspect_state, compare_frames)
    Preconditions: In PLAYING state
    Steps:
      1. Move right 30 frames, capture state (player_x)
      2. Move left back 30 frames
      3. `compare_frames` at original position → should match initial tile layout
    Expected Result: Same tile pattern when returning to same coordinates
    Evidence: .sisyphus/evidence/task-7-deterministic.png
  ```

  **Commit**: YES - `feat(world): infinite scroll procedural map with biomes`

---

- [x] 8. 대시 능력

  **What to do**:
  - 대시 입력: Space 또는 X 키
  - 대시 거리: 40 pixels (순간 이동)
  - 대시 방향: 마지막 이동 방향 (facing direction)
  - 대시 쿨다운: 60프레임 (2초)
  - 대시 중 무적: 10프레임간 무적 상태 (`self.dash_invincible` 카운터)
  - `self.dash_cooldown`: 쿨다운 남은 프레임
  - HUD에 대시 쿨다운 표시 (작은 아이콘 또는 바)

  **Must NOT do**:
  - 대시 중 장애물 충돌 금지 (관통)
  - 연속 대시 금지 (쿨다운 필수)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 6. Wave 2.

  **References**:
  - `pyxel.btnp(pyxel.KEY_SPACE)`, `pyxel.btnp(pyxel.KEY_X)`
  - Player movement from Task 6 (facing direction)
  - Dash specs: 40px distance, 60f cooldown, 10f invincibility

  **Acceptance Criteria**:
  - [ ] `play_and_capture` Space/X → 플레이어 위치 급변
  - [ ] `inspect_state` dash_cooldown 감소 확인
  - [ ] 쿨다운 중 대시 불가

  **QA Scenarios**:

  ```
  Scenario: Dash moves player in facing direction
    Tool: Pyxel MCP (play_and_capture, inspect_state)
    Preconditions: In PLAYING state, facing right
    Steps:
      1. Move right briefly to set facing direction
      2. Press Space → `inspect_state frames="N,N+1"` → player_x increases by ~40
    Expected Result: Player position jumps ~40 pixels in facing direction
    Evidence: .sisyphus/evidence/task-8-dash.json

  Scenario: Dash cooldown prevents rapid reuse
    Tool: Pyxel MCP (play_and_capture, inspect_state)
    Preconditions: In PLAYING state
    Steps:
      1. Press Space (dash) at frame 60
      2. Press Space again at frame 70
      3. `inspect_state` → dash_cooldown > 0, position doesn't change on second press
    Expected Result: Only one dash per 60-frame cooldown
    Evidence: .sisyphus/evidence/task-8-cooldown.json
  ```

  **Commit**: YES - `feat(player): dash ability with cooldown`

---

- [x] 9. 바이옴 전환 시스템

  **What to do**:
  - 시간 기반 바이옴 결정 로직 구현:
    - 0:00-5:00 → Grassland (녹색 톤)
    - 5:00-10:00 → Desert (모래색 톤)
    - 10:00-20:00 → Cave (어두운 회색/파랑 톤)
    - 20:00-30:00 → Castle (어두운 보라/석재 톤)
  - 바이옴 전환 시 부드러운 경계 (혼합 구간 30초)
  - 각 바이옴의 타일 팔레트/변형 적용
  - 바이옴에 따라 적 스폰 가중치 변화 (선택적)

  **Must NOT do**:
  - 바이옴 간 물리적 경계 금지 (부드러운 전환)
  - 바이옴별 고유 적 금지 (공통 적 사용)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 7. Blocks: 34. Wave 2.

  **References**:
  - Biomes 테이블 (위 "Game Design Specification")
  - Tile sprites from Task 3
  - Timer: `timer_frames / 1800` = minutes

  **Acceptance Criteria**:
  - [ ] `inspect_state` timer_frames > 5*1800 → 바이옴 desert
  - [ ] `run_and_capture` 다른 시간대 → 다른 색상 타일

  **QA Scenarios**:

  ```
  Scenario: Biome transitions based on game time
    Tool: Pyxel MCP (inspect_state, run_and_capture)
    Preconditions: debug_time_scale available for faster testing
    Steps:
      1. Set debug_time_scale high or inject timer_frames to simulate 5+ minutes
      2. `inspect_state main.py frames="X" attributes="timer_frames"` → > 9000
      3. `run_and_capture` → tile colors changed from green to sandy
    Expected Result: Visual biome change corresponding to timer threshold
    Evidence: .sisyphus/evidence/task-9-biome-transition.png
  ```

  **Commit**: YES (groups with 6-8) - `feat(world): biome transition system`

---

### Phase 3: COMBAT CORE — 첫 무기 + 적 + 데미지 루프

- [x] 10. 적 스폰 시스템 + 캡 관리

  **What to do**:
  - `self.enemy_list = []`: 적 오브젝트 풀 (리스트)
  - 적 딕셔너리 구조: `{type, x, y, hp, speed, facing, anim_frame, ai_state}`
  - 스폰 로직: 플레이어 주변 화면 밖 (스크린 가장자리 + 32px)에서 랜덤 위치
  - 스폰 간격: 기본 60프레임, 난이도/시간에 따라 감소
  - 캡 관리: `len(enemy_list) >= 50` → 스폰 중단
  - 적 제거: HP ≤ 0 또는 플레이어와 거리 > 500px → 리스트에서 제거
  - 시간 기반 적 타입 해금: Skeleton(0:00), Bat(0:30), Ghost(2:00) 등
  - 거리 기반 필터링: 매 프레임 전수 충돌 대신 플레이어 반경 200px 내 적만 처리

  **Must NOT do**:
  - 50 초과 스폰 금지
  - 화면 내 스폰 금지 (항상 가장자리 밖)
  - 객체 생성/삭제 최적화 아직 필요 없음 (Python list 충분)

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 3,6. Blocks: 11,14. Wave 3.

  **References**:
  - Enemies 테이블 (위 "Game Design Specification") - spawn times
  - Difficulty Scaling 테이블 - spawn rate multiplier
  - Player position: `self.player_x, self.player_y`
  - Screen: 160×120, spawn zone = screen edge + 32px offset

  **Acceptance Criteria**:
  - [ ] `inspect_state` enemy_count ≤ 50 항상
  - [ ] 시간 경과에 따라 enemy_count 증가
  - [ ] 적이 플레이어 주변에 스폰됨

  **QA Scenarios**:

  ```
  Scenario: Enemies spawn around player over time
    Tool: Pyxel MCP (play_and_capture, inspect_state)
    Steps:
      1. Start game, wait 3 seconds (90 frames)
      2. `inspect_state main.py frames="150" attributes="enemy_count"` → > 0
      3. `run_and_capture main.py frames=150` → enemies visible on screen
    Expected Result: enemy_count > 0, enemies visible around player
    Evidence: .sisyphus/evidence/task-10-spawn.png

  Scenario: Enemy cap enforced at 50
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Run with debug fast-forward (high spawn rate)
      2. `inspect_state` at various frames → enemy_count never exceeds 50
    Expected Result: enemy_count <= 50 at all times
    Evidence: .sisyphus/evidence/task-10-cap.json
  ```

  **Commit**: YES - `feat(enemies): spawn system with 50 cap and distance filtering`

---

- [x] 11. 첫 적: Skeleton AI (플레이어 추적)

  **What to do**:
  - Skeleton 적 타입 구현: HP=3, Speed=0.5, Behavior=walk toward player
  - AI: 매 프레임 플레이어 방향으로 이동 (`atan2`로 각도 계산)
  - 충돌: 플레이어와 12px 이내 → 데미지 1 (60프레임 쿨다운)
  - 스프라이트: 16×16, 해골 실루엣, 기본 색상
  - 애니메이션: 2프레임 걷기 (15프레임 토글)
  - 사망 시: XP 젬 드롭 (Task 14에서 구현, 여기서는 플레이스홀더)

  **Must NOT do**:
  - 복잡한 AI 금지 (직선 추적만)
  - 다른 적 타입 구현 금지

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 3,10. Blocks: 21,22. Wave 3.

  **References**:
  - Enemies 테이블: Skeleton stats
  - `math.atan2(player_y - enemy_y, player_x - enemy_x)` for direction
  - Sprite: Task 3 SPR_ENEMY_SKELETON

  **Acceptance Criteria**:
  - [ ] Skeleton이 플레이어를 향해 이동
  - [ ] 플레이어 충돌 시 HP 감소
  - [ ] HP 0에서 사라짐

  **QA Scenarios**:

  ```
  Scenario: Skeleton moves toward player
    Tool: Pyxel MCP (play_and_capture, inspect_state)
    Steps:
      1. Start game, wait for skeleton to spawn
      2. `inspect_state main.py frames="120,150" attributes="enemy_list"` → skeleton positions closer to player at frame 150
    Expected Result: Skeleton distance to player decreases over time
    Evidence: .sisyphus/evidence/task-11-skeleton-ai.json

  Scenario: Skeleton damages player on contact
    Tool: Pyxel MCP (play_and_capture, inspect_state)
    Steps:
      1. Start game, stand still, let skeleton reach player
      2. `inspect_state` player_hp decreases by 1 after collision
    Expected Result: player_hp drops when skeleton touches player
    Evidence: .sisyphus/evidence/task-11-damage.json
  ```

  **Commit**: YES - `feat(enemies): Skeleton enemy with chase AI`

---

- [x] 12. 첫 무기: Whip (근접 범위 공격)

  **What to do**:
  - Whip 무기 구현: 자동 공격, 쿨다운 45프레임
  - 공격 범위: 플레이어 좌/우 32px 영역 (16×32 히트박스)
  - 공격 방향: 마지막 facing direction (좌/우 번갈아)
  - 데미지: 8 per hit
  - 시각 효과: 10프레임 동안 whip 스트라이크 스프라이트 표시
  - `self.weapon_inventory = [0]`: 시작 무기 (whip = 0)
  - 무기 쿨다운 타이머: 각 무기별 개별 타이머

  **Must NOT do**:
  - 수동 조준 금지 (자동 공격)
  - 다른 무기 구현 금지

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 3,6. Blocks: 13,19. Wave 3.

  **References**:
  - Weapons 테이블: Whip stats
  - Player facing direction from Task 6
  - Sprite: Task 3 SPR_WEAPON_WHIP

  **Acceptance Criteria**:
  - [ ] Whip이 자동으로 공격 (쿨다운마다)
  - [ ] 범위 내 적에게 데미지
  - [ ] 공격 시 시각 효과

  **QA Scenarios**:

  ```
  Scenario: Whip auto-attacks nearby enemies
    Tool: Pyxel MCP (play_and_capture, inspect_state)
    Steps:
      1. Start game with Knight (whip), spawn skeleton nearby
      2. Wait for whip cooldown → skeleton HP decreases by 8
      3. `inspect_state` enemy_list → skeleton hp drops
    Expected Result: Skeleton takes 8 damage every ~45 frames
    Evidence: .sisyphus/evidence/task-12-whip.json

  Scenario: Whip visual effect shows on attack
    Tool: Pyxel MCP (capture_frames)
    Steps:
      1. Start game, have enemy near player
      2. `capture_frames` during attack → whip sprite visible
    Expected Result: Whip strike sprite visible for ~10 frames during attack
    Evidence: .sisyphus/evidence/task-12-whip-visual.png
  ```

  **Commit**: YES - `feat(weapons): Whip auto-attack with area damage`

---

- [x] 13. 데미지/히트박스 시스템

  **What to do**:
  - 범용 충돌 검사 함수: `rect_overlap(ax, ay, aw, ah, bx, by, bw, bh)`
  - 히트박스: 스프라이트(16×16)보다 작은 충돌 박스 (12×12, 중앙 정렬)
  - 적→플레이어 데미지: 접촉 시 1 데미지, 60프레임 무적 시간
  - 무기→적 데미지: 각 무기의 데미지 값 적용
  - 넉백: 적이 피격 시 5프레임 뒤로 밀림 (3px/frame)
  - 플레이어 무적: 피격 후 60프레임 깜빡임 (홀수 프레임에만 스프라이트 표시)
  - 데미지 넘버: 선택적 (나중에)

  **Must NOT do**:
  - 복잡한 물리 엔진 금지 (단순 넉백만)
  - 크리티컬 히트 등 금지 (기본 데미지만)

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 6,12. Blocks: 14. Wave 3.

  **References**:
  - Player position, enemy positions from Task 10-11
  - Weapon damage from Task 12
  - Hitbox size: 12×12 centered in 16×16 sprite → offset (2,2)

  **Acceptance Criteria**:
  - [ ] 적 피격 시 HP 감소 + 넉백
  - [ ] 플레이어 피격 시 HP 감소 + 무적 시간
  - [ ] HP 0에서 적 제거 / 게임오버

  **QA Scenarios**:

  ```
  Scenario: Enemy takes damage and gets knocked back
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Have whip attack hit skeleton
      2. `inspect_state` enemy HP decreased, position shifted away from player
    Expected Result: enemy hp -8, position pushed back ~15px
    Evidence: .sisyphus/evidence/task-13-knockback.json

  Scenario: Player invincibility after hit
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Let skeleton touch player → hp drops by 1
      2. Immediate second contact within 60 frames → hp unchanged
    Expected Result: Only 1 damage per 60-frame window
    Evidence: .sisyphus/evidence/task-13-invuln.json
  ```

  **Commit**: YES - `feat(combat): damage/hitbox system with knockback and invincibility`

---

- [x] 14. XP 젬 드롭 + 자석 수집

  **What to do**:
  - `self.gem_list = []`: XP 젬 리스트
  - 적 사망 시 젬 드롭: 적 위치에 1개 젬 생성
  - 젬 딕셔너리: `{x, y, value}` (value = 적 종류에 따라 1-5)
  - 자석 범위: 기본 30px, 패시브 아이템으로 증가 가능
  - 자석 로직: 매 프레임 범위 내 젬을 플레이어 쪽으로 이동 (speed 2px/frame)
  - 수집: 플레이어와 8px 이내 → XP 증가 + 젬 제거
  - 젬 시각: 작은 4×4 반짝이는 스프라이트, 색상 = 파란색
  - `self.player_xp`: 현재 XP 값

  **Must NOT do**:
  - 복잡한 젬 물리 금지 (단순 직선 이동)
  - 화면 밖 젬 제거 금지 (거리 > 500px까지만 유지)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 10,13. Blocks: 15. Wave 3.

  **References**:
  - Magnet range: base 30px, Attractorb passive +25%
  - Gem visual: 4×4 blue sparkle sprite
  - Player XP for level-up calculation in Task 15

  **Acceptance Criteria**:
  - [ ] 적 사망 시 젬 드롭
  - [ ] 자석 범위 내 젬이 플레이어 쪽 이동
  - [ ] 수집 시 XP 증가

  **QA Scenarios**:

  ```
  Scenario: Enemies drop XP gems on death
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Kill a skeleton with whip
      2. `inspect_state` gem_count increases by 1, gem_list has new entry near skeleton position
    Expected Result: gem_count > 0 after kill
    Evidence: .sisyphus/evidence/task-14-gem-drop.json

  Scenario: Magnet pulls gems toward player
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Have gem within 30px of player
      2. `inspect_state frames="N,N+30"` → gem position moves toward player
      3. Eventually player_xp increases
    Expected Result: Gem position converges on player, XP increases on pickup
    Evidence: .sisyphus/evidence/task-14-magnet.json
  ```

  **Commit**: YES (groups with 10-13) - `feat(xp): gem drop and magnet collection`

---

### Phase 4: PROGRESSION — 레벨업 + 업그레이드 선택

- [x] 15. XP/레벨 시스템 + threshold 테이블

  **What to do**:
  - `self.player_level = 1`: 시작 레벨
  - `self.player_xp = 0`: 현재 XP
  - XP threshold 테이블: `level_thresholds = [0, 5, 12, 22, 35, 52, 73, 100, 133, 173, ...]`
  - 레벨업 체크: `player_xp >= level_thresholds[level]` → `state = "LEVEL_UP"`
  - 레벨업 시: `player_level += 1`, XP 차감 (초과분 보존)
  - 최대 레벨: 99 (threshold 이후는 레벨업 없음)
  - 최대 HP 증가: 레벨당 +2 (선택적)

  **Must NOT do**:
  - 레벨업 선택지 구현 금지 (다음 태스크)
  - 스탯 증가 금지 (업그레이드에서만)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 14. Blocks: 16,17. Wave 4.

  **References**:
  - `self.player_xp` from Task 14 gem collection
  - XP threshold: exponential growth pattern
  - Level-up triggers state transition to "LEVEL_UP"

  **Acceptance Criteria**:
  - [ ] XP 충족 시 레벨업 + state 전환
  - [ ] 레벨업 시 timer/enemy 정지

  **QA Scenarios**:

  ```
  Scenario: Level up triggers at XP threshold
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Collect enough gems to reach threshold
      2. `inspect_state` → state == "LEVEL_UP", player_level increased
    Expected Result: state transitions to LEVEL_UP when XP threshold met
    Evidence: .sisyphus/evidence/task-15-levelup.json

  Scenario: Level up pauses game
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Trigger level up
      2. Check timer_frames before and after → timer stopped
    Expected Result: timer_frames unchanged during LEVEL_UP state
    Evidence: .sisyphus/evidence/task-15-pause.json
  ```

  **Commit**: YES - `feat(progression): XP and level-up threshold system`

---

- [x] 16. 레벨업 화면 (3 선택지)

  **What to do**:
  - `draw_level_up()`: 화면 중앙에 3개 선택지 카드 표시
  - 선택지 생성 로직:
    - 미보유 무기 중 랜덤 1-2개
    - 미보유 패시브 중 랜덤 1-2개
    - 보유 무기/패시브 레벨업
    - 총 3개 선택지 (중복 없음)
  - 네비게이션: ↑↓ 또는 W/S로 선택, Enter로 확정
  - 시각: 선택된 항목 하이라이트 (노란 테두리)
  - 항목 정보: 이름 + 효과 설명 (짧은 텍스트)
  - `update_level_up()`: 게임 로직 정지, 선택지만 동작

  **Must NOT do**:
  - 3개 미만 선택지 금지 (항상 3개)
  - 레벨업 중 게임 진행 금지

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 5,15. Blocks: 23. Wave 4.

  **References**:
  - HUD from Task 5 (overlay on game screen)
  - Weapons table (names and effects) from Game Design Specification
  - Passive Items table from Game Design Specification

  **Acceptance Criteria**:
  - [ ] 레벨업 시 3개 선택지 표시
  - [ ] ↑↓ 네비게이션 + Enter 선택
  - [ ] 선택 후 PLAYING 복귀

  **QA Scenarios**:

  ```
  Scenario: Level up shows 3 choices
    Tool: Pyxel MCP (play_and_capture, inspect_state)
    Steps:
      1. Trigger level up by collecting XP
      2. `run_and_capture` → 3 choice cards visible
      3. `inspect_state` → state == "LEVEL_UP"
    Expected Result: 3 distinct choice items displayed on screen
    Evidence: .sisyphus/evidence/task-16-choices.png

  Scenario: Select upgrade and resume
    Tool: Pyxel MCP (play_and_capture, inspect_state)
    Steps:
      1. In LEVEL_UP state
      2. Press ↓ to highlight second option
      3. Press Enter to select
      4. `inspect_state` → state == "PLAYING", weapon/passive inventory updated
    Expected Result: State returns to PLAYING, selected item added to inventory
    Evidence: .sisyphus/evidence/task-16-select.json
  ```

  **Commit**: YES - `feat(progression): level-up screen with 3 choices`

---

- [x] 17. 업그레이드 효과 적용 (무기/패시브)

  **What to do**:
  - 업그레이드 적용 시스템:
    - 새 무기 획득 → `weapon_inventory.append(weapon_id)`
    - 기존 무기 레벨업 → 데미지 +10%, 범위 +5% 등
    - 새 패시브 획득 → `passive_inventory.append(passive_id)`
    - 패시브 레벨업 → 효과 증가
  - 무기 레벨별 데이터 테이블: `weapon_levels[weapon_id][level] = {damage, area, cooldown}`
  - 패시브 효과 적용: 최종 스탯에 패시브 보너스 곱/합
  - 최대 무기/패시브 슬롯: 각각 6개
  - 진화 조건 체크: 무기+패시브 모두 최대 레벨 + 특정 패시브 보유

  **Must NOT do**:
  - 진화 자체는 구현 금지 (Phase 6)
  - 6개 초과 슬롯 금지

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 15. Blocks: 18,25. Wave 4.

  **References**:
  - Weapons table: base stats for each weapon
  - Passive Items table: effects and multipliers
  - `weapon_inventory`, `passive_inventory` lists

  **Acceptance Criteria**:
  - [ ] 무기 획득 시 인벤토리에 추가 + 자동 공격
  - [ ] 패시브 획득 시 스탯 반영
  - [ ] 레벨업 시 수치 증가

  **QA Scenarios**:

  ```
  Scenario: New weapon added to inventory after level-up
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Level up, select a new weapon
      2. `inspect_state` → weapon_inventory contains new weapon ID
    Expected Result: weapon_inventory length increased by 1
    Evidence: .sisyphus/evidence/task-17-weapon-add.json

  Scenario: Passive bonus applied to stats
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Level up, select Hollow Heart (+10% max HP)
      2. `inspect_state` → player_max_hp increased by 10%
    Expected Result: Max HP increased proportionally
    Evidence: .sisyphus/evidence/task-17-passive.json
  ```

  **Commit**: YES - `feat(progression): upgrade effects for weapons and passives`

---

- [x] 18. 패시브 아이템 시스템

  **What to do**:
  - 8종 패시브 아이템 데이터 테이블:
    - Hollow Heart: max_hp += 10%
    - Empty Tome: weapon_cooldown -= 8%
    - Candelabrador: weapon_area += 10%
    - Bracer: projectile_speed += 10%
    - Attractorb: magnet_range += 25%
    - Pummarola: hp_regen += 0.5/sec
    - Clover: luck += 10% (critical chance or better drops)
    - Spinach: weapon_damage += 10%
  - HP 리젠: `pummarola` 보유 시 매 180프레임마다 HP +1
  - 자석 범위: 기본 30 + Attractorb 레벨 × 7.5
  - 패시브 최대 레벨: 5
  - `passive_inventory`에 `{id, level}` 저장

  **Must NOT do**:
  - 패시브 없이 게임 진행 불가 금지 (선택적)
  - 복잡한 시너지 금지 (단순 수치 보너스만)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 17. Blocks: 25. Wave 4.

  **References**:
  - Passive Items table from Game Design Specification
  - Stats: max_hp, magnet_range, weapon_damage, etc.

  **Acceptance Criteria**:
  - [ ] 각 패시브 효과가 스탯에 반영
  - [ ] HP 리젠 작동
  - [ ] 자석 범위 증가

  **QA Scenarios**:

  ```
  Scenario: Pummarola provides HP regeneration
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Get Pummarola passive
      2. Take damage, wait 180 frames
      3. `inspect_state` → player_hp increased by 1
    Expected Result: HP regenerates by 1 per 6 seconds with Pummarola
    Evidence: .sisyphus/evidence/task-18-regen.json

  Scenario: Attractorb increases magnet range
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Get Attractorb passive
      2. Check magnet range → increased from base 30
    Expected Result: Magnet range = 30 + 7.5 per Attractorb level
    Evidence: .sisyphus/evidence/task-18-magnet.json
  ```

  **Commit**: YES (groups with 15-17) - `feat(progression): passive item system with stat bonuses`

---

### Phase 5: EXPANSION — 추가 무기/적/캐릭터

- [x] 19. Magic Wand + Axe + Knife

  **What to do**:
  - **Magic Wand** (ID=1): 가장 가까운 적에게 투사체 발사, 쿨다운 40f, 데미지 6
    - 투사체: 4×4 스프라이트, 속도 3px/frame, 사거리 120px
    - 타겟팅: `min(enemies, key=lambda e: dist(player, e))`
  - **Axe** (ID=2): 위쪽으로 부메랑 투사체, 쿨다운 50f, 데미지 10
    - 궤적: 위로 올라갔다가 아래로 내려옴 (포물선)
    - 히트박스: 16×16 (던지는 무기)
  - **Knife** (ID=3): facing direction으로 빠른 투사체, 쿨다운 15f, 데미지 3
    - 투사체: 8×4 스프라이트, 속도 4px/frame, 사거일 100px
    - 방향: 마지막 이동 방향 (상/하/좌/우/대각선)
  - `self.projectile_list = []`: 투사체 풀
  - 투사체 딕셔너리: `{type, x, y, dx, dy, damage, lifetime, speed}`
  - 투사체 수명: 사거리/속도 = 프레임 수

  **Must NOT do**:
  - 투사체 충돌 최적화 금지 (아직 단순 순회)
  - 관통/폭발 금지 (기본 투사체만)

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 12,17. Blocks: 25,26. Wave 5.

  **References**:
  - Weapons table: Magic Wand, Axe, Knife stats
  - Projectile system: position, velocity, lifetime
  - Enemy positions from Task 10
  - Player facing direction from Task 6

  **Acceptance Criteria**:
  - [ ] 각 무기가 고유 패턴으로 공격
  - [ ] 투사체가 적에게 데미지
  - [ ] 쿨다운 적용

  **QA Scenarios**:

  ```
  Scenario: Magic Wand targets nearest enemy
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Have Magic Wand, spawn 2 enemies at different distances
      2. Wait for attack → projectile moves toward closer enemy
    Expected Result: Projectile direction points at nearest enemy
    Evidence: .sisyphus/evidence/task-19-wand-target.json

  Scenario: Knife shoots in facing direction
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Face right, have Knife weapon
      2. Wait for attack → projectile moves right
    Expected Result: Knife projectile travels in player's facing direction
    Evidence: .sisyphus/evidence/task-19-knife-dir.json
  ```

  **Commit**: YES - `feat(weapons): Magic Wand, Axe, Knife with projectiles`

---

- [x] 20. Holy Water + Garlic + Cross + Fire Wand

  **What to do**:
  - **Holy Water** (ID=4): 바닥에 데미지 존 생성, 쿨다운 90f, 데미지 3/tick (15f 간격)
    - 던지는 방향: 가장 가까운 적 방향
    - 데미지 존: 20×20 영역, 지속시간 120프레임
    - 시각: 파란 물 웅덩이 스프라이트
  - **Garlic** (ID=5): 오라 공격, 쿨다운 30f, 데미지 2 + 넉백
    - 범위: 반경 40px 원형
    - 시각: 반투명 흰색 원 (pyxelcirc)
  - **Cross/Boomerang** (ID=6): 부메랑 궤적, 쿨다운 60f, 데미지 8
    - 궤적: 전진 → 정지 → 되돌아옴
    - 관통: 적을 통과하며 데미지
  - **Fire Wand** (ID=7): 랜덤 적에게 화염 투사체, 쿨다운 45f, 데미지 7
    - 타겟팅: 랜덤 적 (Clover가 luck 증가 → 더 가까운 적 우선?)
    - 화염 투사체: 주황색, 관통 안함

  **Must NOT do**:
  - 복잡한 파티클 시스템 금지
  - 사운드 이펙트 아직 금지 (Phase 7)

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 12,17. Blocks: 25,26. Wave 5. (Parallel with Task 19)

  **References**:
  - Weapons table: Holy Water, Garlic, Cross, Fire Wand stats
  - Projectile system from Task 19
  - Area effect: damage zones, auras

  **Acceptance Criteria**:
  - [ ] 각 무기 고유 패턴 구현
  - [ ] 오라/영역 데미지 작동
  - [ ] 부메랑 궤적 정상

  **QA Scenarios**:

  ```
  Scenario: Garlic damages all enemies in aura range
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Have Garlic weapon, surround player with 3 enemies within 40px
      2. Wait for attack tick → all 3 take 2 damage
    Expected Result: All enemies within range take damage
    Evidence: .sisyphus/evidence/task-20-garlic.json

  Scenario: Cross returns to player like boomerang
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Throw Cross → projectile moves forward, stops, returns
      2. Track projectile_list position over frames
    Expected Result: Projectile position goes out then comes back
    Evidence: .sisyphus/evidence/task-20-cross.json
  ```

  **Commit**: YES - `feat(weapons): Holy Water, Garlic, Cross, Fire Wand`

---

- [x] 21. Bat + Ghost + Zombie

  **What to do**:
  - **Bat** (ID=1): 빠른 속도(1.5), 낮은 HP(2), 에러틱 이동
    - AI: 플레이어 방향 + 랜덤 오프셋 (zigzag)
    - 스프라이트: 작은 박쥐 실루엣, 보라색
    - 등장: 0:30부터
  - **Ghost** (ID=2): 중간 속도(0.8), 중간 HP(5), 투과 이동
    - AI: 직선 이동, 다른 적 통과
    - 스프라이트: 반투명 형태, 연한 파랑
    - 등장: 2:00부터
  - **Zombie** (ID=3): 느린 속도(0.3), 높은 HP(12), 탱커
    - AI: 느리지만 꾸준히 추적
    - 스프라이트: 녹색 큰 형태
    - 등장: 3:00부터, 높은 XP 젬 드롭

  **Must NOT do**:
  - 복잡한 AI 금지 (기본 추적 + 특성만)
  - 적 간 상호작용 금지

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 11. Blocks: 22,35. Wave 5.

  **References**:
  - Enemies table: Bat, Ghost, Zombie stats
  - Skeleton AI pattern from Task 11 as base
  - Sprite constants from Task 3

  **Acceptance Criteria**:
  - [ ] 각 적 고유 AI/속도/HP
  - [ ] 시간 기반 해금 작동
  - [ ] 스프라이트 VS 원작 수준 품질 (inspect_sprite로 픽셀 디테일 확인)

  **QA Scenarios**:

  ```
  Scenario: Bat has erratic movement
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Spawn bat, track position over 60 frames
      2. Position should not be straight line (zigzag pattern)
    Expected Result: Bat path has random deviations
    Evidence: .sisyphus/evidence/task-21-bat-ai.json

  Scenario: Zombie has high HP
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Spawn zombie, hit with whip (8 damage)
      2. HP = 12 - 8 = 4 (still alive, unlike skeleton)
    Expected Result: Zombie survives whip hit
    Evidence: .sisyphus/evidence/task-21-zombie-hp.json
  ```

  **Commit**: YES - `feat(enemies): Bat, Ghost, Zombie with unique AI`

---

- [x] 22. Dark Mage + Slime + Necromancer + Demon

  **What to do**:
  - **Dark Mage** (ID=4): 원거리, 투사체 발사
    - AI: 플레이어에게 접근하다가 80px 이내에서 정지, 90f마다 투사체 발사
    - 투사체: 4×4 보라색, 속도 2, 데미지 2
    - HP: 6, Speed: 0.4, 등장: 5:00
  - **Slime** (ID=5): 분열, 사망 시 2개 작은 슬라임 생성
    - AI: 무작위 이동 (랜덤 방향 전환 120f마다)
    - 분열: 죽을 때 2개의 Small Slime (HP=1, Speed=0.8) 생성
    - HP: 4, Speed: 0.6, 등장: 7:00
    - Small Slime: HP=1, 죽어도 분열 안함
  - **Necromancer** (ID=6): 소환, 주기적으로 Skeleton 생성
    - AI: 느리게 이동 + 180f마다 화면 밖에서 Skeleton 2마리 소환
    - 소환은 enemy cap 체크 (50-현재수 < 2면 1마리만)
    - HP: 8, Speed: 0.3, 등장: 10:00
  - **Demon** (ID=7): 돌진, 빠르고 강함
    - AI: 플레이어 방향으로 이동, 120f마다 대시 (8px/frame, 15f)
    - 대시 데미지: 3 (일반 접촉 1)
    - HP: 15, Speed: 1.2, 등장: 15:00

  **Must NOT do**:
  - 소환 시 enemy cap 무시 금지
  - 분열 시 cap 초과 금지

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 11,21. Blocks: 27,35. Wave 5.

  **References**:
  - Enemies table: Dark Mage, Slime, Necromancer, Demon stats
  - Enemy cap system from Task 10
  - Projectile system from Task 19

  **Acceptance Criteria**:
  - [ ] Dark Mage 원거리 공격
  - [ ] Slime 분열
  - [ ] Necromancer 소환 (cap 준수)
  - [ ] Demon 대시 공격

  **QA Scenarios**:

  ```
  Scenario: Slime splits on death
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Kill a Slime → enemy_count increases by 1 (2 small - 1 dead = +1)
      2. Check enemy_list for small slimes near death position
    Expected Result: 2 small slimes spawned at slime's death position
    Evidence: .sisyphus/evidence/task-22-split.json

  Scenario: Necromancer respects enemy cap
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Fill enemy_list to 49 enemies
      2. Necromancer attempts summon → only 1 skeleton created (cap 50)
    Expected Result: enemy_count reaches 50 but never exceeds
    Evidence: .sisyphus/evidence/task-22-cap.json

  Scenario: Demon dashes at player
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Spawn Demon, track position over 120 frames
      2. Demon position should show burst of speed (dash)
    Expected Result: Demon periodically accelerates toward player
    Evidence: .sisyphus/evidence/task-22-dash.json
  ```

  **Commit**: YES - `feat(enemies): Dark Mage, Slime, Necromancer, Demon`

---

- [x] 23. 캐릭터 선택 화면 (8캐릭터)

  **What to do**:
  - `draw_char_select()`: 8 캐릭터 카드 표시 (2행 × 4열)
  - 각 카드: 캐릭터 스프라이트 + 이름 + 시작 무기명
  - ←→↑↓ 네비게이션, Enter 선택
  - 선택 시 `self.selected_character = index`
  - 선택된 카드: 노란 테두리 하이라이트
  - 캐릭터별 고유 색상 테마 적용 (카드 배경)
  - Characters 테이블의 8종 구현

  **Must NOT do**:
  - 스탯 차이 금지 (시작 무기만 다름)
  - 잠금 캐릭터 금지 (전부 선택 가능)

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 4,16. Blocks: 35. Wave 5.

  **References**:
  - Characters table: 8 characters with names, weapons, color themes
  - Sprite constants from Task 3
  - State transition: CHAR_SELECT → DIFF_SELECT on Enter

  **Acceptance Criteria**:
  - [ ] 8 캐릭터 표시
  - [ ] 네비게이션 + 선택 작동
  - [ ] 선택한 캐릭터의 시작 무기로 게임 시작

  **QA Scenarios**:

  ```
  Scenario: Character selection screen shows 8 characters
    Tool: Pyxel MCP (play_and_capture)
    Steps:
      1. From title, press Enter → CHAR_SELECT
      2. Screenshot → 8 character cards visible
    Expected Result: 8 distinct character cards with sprites and names
    Evidence: .sisyphus/evidence/task-23-charsel.png

  Scenario: Selected character determines starting weapon
    Tool: Pyxel MCP (play_and_capture, inspect_state)
    Steps:
      1. Select Mage (character 2, starts with Magic Wand)
      2. Enter difficulty, start game
      3. `inspect_state` → weapon_inventory contains Magic Wand ID
    Expected Result: weapon_inventory starts with character's associated weapon
    Evidence: .sisyphus/evidence/task-23-starting-weapon.json
  ```

  **Commit**: YES - `feat(ui): character selection screen with 8 characters`

---

- [x] 24. 난이도 선택 화면 (3단계)

  **What to do**:
  - `draw_diff_select()`: 3 난이도 카드 표시 (1행 × 3열)
  - Easy / Normal / Hard
  - 각 카드: 난이도명 + 간단 설명 (적 HP, 속도, 스폰율)
  - ←→ 네비게이션, Enter 선택
  - 선택 시 `self.difficulty = 0/1/2`
  - Normal이 기본 선택 (커서 시작 위치)
  - Difficulty Scaling 테이블의 수치 적용

  **Must NOT do**:
  - 난이도 잠금 금지 (전부 선택 가능)
  - 복잡한 난이도 설명 금지 (간단 텍스트만)

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 4,23. Blocks: 35. Wave 5.

  **References**:
  - Difficulty Scaling table from Game Design Specification
  - State transition: DIFF_SELECT → PLAYING on Enter
  - `self.difficulty` affects: enemy_hp_mult, enemy_speed_mult, spawn_rate_mult, xp_required_mult

  **Acceptance Criteria**:
  - [ ] 3 난이도 표시
  - [ ] 선택에 따라 게임 난이도 적용

  **QA Scenarios**:

  ```
  Scenario: Difficulty selection affects enemy HP
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Select Hard difficulty
      2. Start game, spawn skeleton
      3. Skeleton HP = base 3 × 1.5 = 4 (rounded) or 5
    Expected Result: Enemies have more HP on Hard vs Normal
    Evidence: .sisyphus/evidence/task-24-hard-hp.json
  ```

  **Commit**: YES (groups with 23) - `feat(ui): difficulty selection screen`

---

### Phase 6: EVOLUTION + BOSS — 무기 진화 + 30분 보스전

- [x] 25. 무기 진화 시스템 (무기+패시브=진화)

  **What to do**:
  - 진화 조건 체크: 무기 최대 레벨(8) + 특정 패시브 보유
  - 진화 테이블 (Weapons 테이블의 Evolution 컬럼):
    - Whip + Hollow Heart → Bloody Tear
    - Magic Wand + Empty Tome → Holy Wand
    - Axe + Candelabrador → Death Spiral
    - Knife + Bracer → Thousand Edge
    - Holy Water + Attractorb → Boros Sea
    - Garlic + Pummarola → Soul Eater
    - Cross + Clover → Hyperlove
    - Fire Wand + Spinach → Hellfire
  - 진화 발동: 보스 처치 시 또는 다음 레벨업 시 자동 진화 (선택지 대신)
  - 진화 시 기존 무기 → 진화 무기로 교체 (레벨 유지)
  - 진화 무기는 더 강한 버전 (범위↑, 데미지↑, 관통 등)

  **Must NOT do**:
  - 진화 없이 게임 완료 가능하게 금지 (핵심 기능)
  - 수동 진화 금지 (자동)

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 17,18. Blocks: 26,35. Wave 6.

  **References**:
  - Weapons table: evolution pairs
  - Passive Items table: paired weapons
  - `weapon_inventory`, `passive_inventory`

  **Acceptance Criteria**:
  - [ ] 조건 충족 시 진화 발동
  - [ ] 진화 무기로 교체
  - [ ] 진화 무기가 더 강함

  **QA Scenarios**:

  ```
  Scenario: Weapon evolves when conditions met
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Get Whip to max level, have Hollow Heart
      2. Trigger evolution condition
      3. `inspect_state` → weapon_inventory has Bloody Tear instead of Whip
    Expected Result: Whip replaced with Bloody Tear
    Evidence: .sisyphus/evidence/task-25-evolve.json
  ```

  **Commit**: YES - `feat(weapons): evolution system`

---

- [x] 26. 진화 무기 8종 구현

  **What to do**:
  - 각 진화 무기의 강화된 버전 구현:
    - **Bloody Tear**: Whip + 더 넓은 범위, HP 흡혹 (데미지의 10% 회복)
    - **Holy Wand**: Magic Wand + 관통, 더 빠른 속도
    - **Death Spiral**: Axe + 더 큰 범위, 관통
    - **Thousand Edge**: Knife + 다중 발사 (3방향)
    - **Boros Sea**: Holy Water + 더 큰 데미지 존, 지속시간 증가
    - **Soul Eater**: Garlic + 더 넓은 오라, 추가 HP 회복
    - **Hyperlove**: Cross + 더 빠른 부메랑, 다중 발사
    - **Hellfire**: Fire Wand + 관통 화염, 데미지 증가
  - 각 진화 무기는 기존 패턴 기반 + 강화 수치 적용
  - 시각: 기존 스프라이트 + 진화 특유의 화려한 색상/이펙트 변화 (빨간색 톤, 글로우 효과 등, VS 원작 수준)

  **Must NOT do**:
  - 완전히 새로운 패턴 금지 (기존 기반 강화만)
  - 진화 무기 전용 스프라이트 시트 **권장** (VS 원작처럼 진화 무기는 시각적으로 확연히 다름)

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 19,20,25. Blocks: 35. Wave 6.

  **References**:
  - Base weapon implementations from Tasks 12, 19, 20
  - Evolution weapon specs above

  **Acceptance Criteria**:
  - [ ] 8종 진화 무기 모두 구현
  - [ ] 기존 무기보다 강함
  - [ ] 각 고유 강화 효과 적용

  **QA Scenarios**:

  ```
  Scenario: Evolved weapon is stronger than base
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Compare Whip damage (8) vs Bloody Tear damage (>8, with lifesteal)
      2. Kill enemy with Bloody Tear → player_hp increases slightly
    Expected Result: Bloody Tear does more damage and heals player
    Evidence: .sisyphus/evidence/task-26-evolved.json
  ```

  **Commit**: YES - `feat(weapons): 8 evolved weapons with enhanced effects`

---

- [x] 27. 30분 타이머 + 보스 spawn

  **What to do**:
  - 30분 타이머: `timer_frames >= 30 * 60 * 30 = 54000` → 보스 spawn
  - 보스 spawn 시:
    - 모든 일반 적 제거 (enemy_list clear)
    - `self.boss_active = True`
    - `self.state = "BOSS"` (또는 PLAYING + boss_active 플래그)
    - 게임 일시정지 2초 + "DEATH APPROACHES" 텍스트 표시
    - 보스 엔티티 생성 (HP=500×difficulty)
  - 보스: Death (32×32 스프라이트, 2×2 그리드)
  - 보스 속도: 0.5, 느리지만 강력
  - 디버그: `debug_time_scale`로 빠른 테스트 가능

  **Must NOT do**:
  - 30분 전 보스 spawn 금지
  - 보스 중 일반 스폰 금지 (보스+미니언만)

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 22,25. Blocks: 28,35. Wave 6.

  **References**:
  - Timer: `self.timer_frames`
  - Boss specs from Game Design Specification
  - Sprite: Task 3 SPR_BOSS (32×32)

  **Acceptance Criteria**:
  - [ ] 30분에 보스 spawn
  - [ ] 일반 적 제거 + 보스 등장
  - [ ] "DEATH APPROACHES" 텍스트 표시

  **QA Scenarios**:

  ```
  Scenario: Boss spawns at 30-minute mark
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Use debug_time_scale to fast-forward to 30:00
      2. `inspect_state` → boss_active == True, boss_hp > 0, enemy_count drops then boss appears
    Expected Result: boss_active transitions from False to True at 30:00
    Evidence: .sisyphus/evidence/task-27-boss-spawn.json

  Scenario: All regular enemies cleared before boss
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Have 50 enemies on screen
      2. Timer hits 30:00 → enemy_count drops to 0, then boss appears (count=1)
    Expected Result: enemy_count = 0 before boss spawns
    Evidence: .sisyphus/evidence/task-27-clear.json
  ```

  **Commit**: YES - `feat(boss): 30-minute timer and Death boss spawn`

---

- [x] 28. 보스 AI (Death) + 미니언 소환

  **What to do**:
  - **Death Boss AI**:
    - 기본 이동: 플레이어 방향으로 0.5 speed
    - 투사체 공격: 120f마다 플레이어 방향으로 느린 유도 투사체 3개
    - 유도 투사체: 속도 1.5, 300f 수명, 플레이어 방향으로 살짝 커브
    - 접촉 데미지: 5 (매우 강함)
  - **미니언 소환**:
    - 600f마다 Skeleton 소환 (Easy: 2, Normal: 3, Hard: 4)
    - 소환은 enemy cap 체크 (boss + minions ≤ 50)
    - 소환 위치: 보스 주변 32px
  - 보스 피격 시 깜빡임 효과
  - 보스 HP 바: 화면 하단 중앙에 긴 바 표시
  - 보스 처치: HP ≤ 0 → `state = "VICTORY"`

  **Must NOT do**:
  - 보스 패턴 과도하게 복잡 금지 (이동+투사체+소환만)
  - 2페이즈 등 금지 (단일 페이즈)

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 22,27. Blocks: 29,35. Wave 6.

  **References**:
  - Boss specs from Game Design Specification
  - Skeleton from Task 11 (minion)
  - Projectile system from Task 19

  **Acceptance Criteria**:
  - [ ] 보스 이동 + 투사체 공격
  - [ ] 미니언 소환 (cap 준수)
  - [ ] 보스 처치 시 VICTORY

  **QA Scenarios**:

  ```
  Scenario: Boss fires homing projectiles
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Boss active, wait 120 frames
      2. `inspect_state` → projectile_list contains boss projectiles moving toward player
    Expected Result: Boss projectiles appear every 120 frames
    Evidence: .sisyphus/evidence/task-28-boss-proj.json

  Scenario: Boss defeat triggers victory
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Reduce boss HP to 0 (debug or sustained damage)
      2. `inspect_state` → state == "VICTORY"
    Expected Result: Game transitions to VICTORY state on boss death
    Evidence: .sisyphus/evidence/task-28-victory.json
  ```

  **Commit**: YES - `feat(boss): Death AI with projectiles and minion summon`

---

- [x] 29. 승리/게임오버 화면

  **What to do**:
  - **VICTORY 화면** (`draw_victory()`):
    - "VICTORY!" 대형 텍스트
    - 보스 처치 시간 표시
    - 통계: 플레이 시간, 레벨, 킬 수, 획득 무기 목록
    - "PRESS ENTER TO RETURN TO TITLE"
    - 배경: 금색/흰색 승리 톤
  - **GAME_OVER 화면** (`draw_game_over()`):
    - "GAME OVER" 텍스트
    - 사망 시간 표시
    - 통계: 플레이 시간, 레벨, 킬 수, 획득 무기 목록
    - 세션 최고 기록 갱신 시 "NEW HIGH SCORE!" 표시
    - "PRESS ENTER TO RETURN TO TITLE"
    - 배경: 빨간색/검은색 패배 톤
  - `self.high_score`: 세션 내 최고 점수 ( kills × level × difficulty_multiplier )
  - `update_victory()` / `update_game_over()`: Enter → `state = "TITLE"`

  **Must NOT do**:
  - 파일 저장 금지 (세션만)
  - 복잡한 통계 금지 (시간/레벨/킬/무기만)

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 27,28. Blocks: 33,35. Wave 6.

  **References**:
  - State transitions: VICTORY/GAME_OVER → TITLE on Enter
  - Stats: `self.kills`, `self.player_level`, `self.timer_frames`, `self.weapon_inventory`

  **Acceptance Criteria**:
  - [ ] 승리/게임오버 각각 다른 화면
  - [ ] 통계 표시 (시간, 레벨, 킬, 무기)
  - [ ] Enter → 타이틀 복귀

  **QA Scenarios**:

  ```
  Scenario: Victory screen shows after boss defeat
    Tool: Pyxel MCP (inspect_state, run_and_capture)
    Steps:
      1. Defeat boss → state == "VICTORY"
      2. `run_and_capture` → "VICTORY!" text, stats displayed
    Expected Result: Victory screen with kill count, level, time, weapons
    Evidence: .sisyphus/evidence/task-29-victory.png

  Scenario: Game over screen shows on death
    Tool: Pyxel MCP (inspect_state, run_and_capture)
    Steps:
      1. Player HP reaches 0 → state == "GAME_OVER"
      2. `run_and_capture` → "GAME OVER" text, stats displayed
    Expected Result: Game over screen with death stats
    Evidence: .sisyphus/evidence/task-29-gameover.png
  ```

  **Commit**: YES - `feat(ui): victory and game over screens with stats`

---

### Phase 7: AUDIO + POLISH — SFX + 난이도 스케일링 + 밸런스

- [x] 30. SFX 3종 (공격/킬/레벨업)

  **What to do**:
  - Pyxel 사운드 슬롯에 SFX 생성:
    - SFX 0: **Attack** (짧은 타격음, 0.1초, 높은 톤 → 낮은 톤)
    - SFX 1: **Kill** (팝 소리, 0.15초, 상승 톤)
    - SFX 2: **Level Up** (징글, 0.3초, 상승 음계 3음)
  - `pyxel.sound(N).set(notes, tones, volumes, effects, speed)` 사용
  - 재생: `pyxel.play(CH_NEEDED, sound_id)`
  - 오디오 채널 관리: 4채널 중 채널 0=attack, 채널 1=kill, 채널 2=levelup
  - 동시 재생 제한: 같은 SFX는 10프레임 간격으로만 재생 (소리 겹침 방지)

  **Must NOT do**:
  - BGM 금지 (SFX만)
  - 외부 사운드 파일 금지 (코드 내 생성만)
  - 4채널 초과 금지

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`pyxel`]

  **Parallelization**: No dependencies. Wave 7.

  **References**:
  - Pyxel `pyxel.sound(N).set()` API
  - Pyxel `pyxel.play(channel, sound_id)` API
  - 4 audio channels: ch0=attack, ch1=kill, ch2=levelup, ch3=reserved

  **Acceptance Criteria**:
  - [ ] `render_audio main.py sound_index=0` → attack SFX 파형 존재
  - [ ] `render_audio main.py sound_index=1` → kill SFX 파형 존재
  - [ ] `render_audio main.py sound_index=2` → levelup SFX 파형 존재

  **QA Scenarios**:

  ```
  Scenario: Attack SFX plays on weapon use
    Tool: Pyxel MCP (render_audio, inspect_state)
    Steps:
      1. `render_audio main.py sound_index=0` → waveform data present
      2. Play game, attack → sound channel 0 active
    Expected Result: Distinct attack waveform in render output
    Evidence: .sisyphus/evidence/task-30-attack-sfx.json

  Scenario: All 3 SFX are distinct
    Tool: Pyxel MCP (render_audio)
    Steps:
      1. Render SFX 0, 1, 2 separately → compare waveforms
      2. Each should have different note patterns
    Expected Result: 3 distinct sound patterns
    Evidence: .sisyphus/evidence/task-30-all-sfx.json
  ```

  **Commit**: YES - `feat(audio): attack, kill, level-up SFX`

---

- [x] 31. 난이도 스케일링 적용

  **What to do**:
  - Difficulty Scaling 테이블 수치 적용:
    - `self.difficulty` → `enemy_hp_mult`, `enemy_speed_mult`, `spawn_rate_mult`, `xp_required_mult`
  - 적 HP: `base_hp × difficulty_hp_mult`
  - 적 속도: `base_speed × difficulty_speed_mult`
  - 스폰 간격: `base_interval / difficulty_spawn_mult` (높을수록 빈번)
  - XP 요구량: `base_threshold × difficulty_xp_mult`
  - 시간 기반 추가 스케일링: 매 5분마다 적 HP/속도 +10% 추가
  - 스폰 가속화: 매 5분마다 스폰 간격 -10%

  **Must NOT do**:
  - 플레이어 능력치 변화 금지 (적/시스템만)
  - Hard에서 불가능한 난이도 금지

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 10,15. Blocks: 35. Wave 7.

  **References**:
  - Difficulty Scaling table from Game Design Specification
  - `self.difficulty` from Task 24

  **Acceptance Criteria**:
  - [ ] Easy/Normal/Hard에서 적 HP/속도/스폰율 다름
  - [ ] 시간 경과에 따라 난이도 추가 증가

  **QA Scenarios**:

  ```
  Scenario: Hard enemies have more HP than Normal
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Play on Normal, spawn skeleton → HP = 3
      2. Play on Hard, spawn skeleton → HP = 3 × 1.5 = 4 or 5
    Expected Result: Hard skeleton HP > Normal skeleton HP
    Evidence: .sisyphus/evidence/task-31-hard-hp.json
  ```

  **Commit**: YES - `feat(balance): difficulty scaling with time-based progression`

---

- [x] 32. 일시정지 + 컨트롤 표시

  **What to do**:
  - `draw_paused()`: "PAUSED" 텍스트 + 반투명 오버레이
  - PAUSED 중: timer/enemy/weapon/xp 모두 정지
  - ESC: PLAYING ⇄ PAUSED 토글
  - 컨트롤 표시: PAUSED 화면 하단에 간단한 컨트롤 안내
    - "Arrow/WASD: Move | Space/X: Dash | ESC: Pause"
  - Level-up 중 ESC 금지 (순서 보장: LEVEL_UP 해제 후 PAUSE 가능)

  **Must NOT do**:
  - 일시정지 중 조작 금지 (ESC만)
  - 설정 메뉴 금지

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 2. Blocks: 35. Wave 7.

  **References**:
  - State machine from Task 2
  - Controls: Arrow/WASD, Space/X, ESC

  **Acceptance Criteria**:
  - [ ] ESC 토글로 PAUSE/RESUME
  - [ ] PAUSE 중 게임 정지
  - [ ] 컨트롤 안내 표시

  **QA Scenarios**:

  ```
  Scenario: Pause stops all game updates
    Tool: Pyxel MCP (play_and_capture, inspect_state)
    Steps:
      1. In PLAYING state, press ESC at frame 80
      2. `inspect_state frames="80,100" attributes="state,timer_frames,enemy_count"` → timer_frames same at both frames
    Expected Result: timer_frames unchanged during pause
    Evidence: .sisyphus/evidence/task-32-pause.json
  ```

  **Commit**: YES - `feat(ui): pause screen with control hints`

---

- [x] 33. 게임오버 통계 화면 강화

  **What to do**:
  - `draw_game_over()` 상세 통계:
    - 생존 시간: "MM:SS" 형식
    - 도달 레벨: "Lv.XX"
    - 총 킬 수: "XXX Kills"
    - 획득 무기 목록: 무기 이름 나열
    - 획득 패시브 목록: 패시브 이름 나열
    - 세션 최고 기록: "HIGH SCORE: XXXX"
    - 기록 갱신 시 "NEW RECORD!" 깜빡임
  - 점수 계산: `kills × level × difficulty_multiplier`
  - 스크롤 가능 (무기/패시브 많을 때): ↑↓로 스크롤

  **Must NOT do**:
  - 파일 저장 금지
  - 온라인 랭킹 금지

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 5,29. Blocks: 35. Wave 7.

  **References**:
  - Game over screen from Task 29
  - HUD from Task 5
  - Stats: `self.kills`, `self.player_level`, `self.timer_frames`, `self.weapon_inventory`, `self.passive_inventory`

  **Acceptance Criteria**:
  - [ ] 모든 통계 표시
  - [ ] 세션 최고 기록 추적
  - [ ] 기록 갱신 시 표시

  **QA Scenarios**:

  ```
  Scenario: Game over shows complete stats
    Tool: Pyxel MCP (run_and_capture)
    Steps:
      1. Die → game over screen
      2. Screenshot → time, level, kills, weapons all visible
    Expected Result: All stat categories displayed
    Evidence: .sisyphus/evidence/task-33-stats.png
  ```

  **Commit**: YES - `feat(ui): detailed game over statistics screen`

---

- [x] 34. 밸런스 튜닝 + 타임 스케일 디버그

  **What to do**:
  - `self.debug_time_scale = 1`: 개발/테스트용 타임 스케일
  - 타임 스케일: `timer_frames += debug_time_scale` (1=정상, 10=10배속)
  - 디버그 키: F1 → time_scale × 2, F2 → time_scale / 2, F3 → time_scale = 1
  - 밸런스 조정:
    - XP threshold 곡선 조정 (너무 느리거나 빠르면)
    - 적 HP/데미지 밸런스
    - 무기 데미지 밸런스
    - 스폰 속도 밸런스
  - 디버그 오버레이: F4 → FPS, enemy_count, gem_count, timer 표시

  **Must NOT do**:
  - 프로덕션에 디버그 키 포함 금지 (개발 모드만)
  - 핵/치트 금지 (테스트용 타임 스케일만)

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 9,31. Blocks: 35. Wave 7.

  **References**:
  - All weapon stats, enemy stats, XP thresholds from Game Design Specification
  - `debug_time_scale` from Task 1

  **Acceptance Criteria**:
  - [ ] 타임 스케일 변경 가능
  - [ ] 10배속으로 30분 시뮬레이션 가능
  - [ ] 밸런스 수치 조정 완료

  **QA Scenarios**:

  ```
  Scenario: Debug time scale speeds up game
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Set debug_time_scale = 10
      2. `inspect_state frames="30"` → timer_frames should be ~300 (30 × 10)
    Expected Result: Timer advances 10x faster
    Evidence: .sisyphus/evidence/task-34-timescale.json
  ```

  **Commit**: YES - `feat(debug): time scale and balance tuning`

---

### Phase 8: INTEGRATION TEST — 전체 흐름 검증

- [x] 35. 전체 게임 플로우 통합 테스트

  **What to do**:
  - 전체 게임 플로우 엔드투엔드 테스트:
    1. Title → Character Select → Difficulty Select → Playing
    2. 이동, 적 처치, XP 수집, 레벨업
    3. 무기 획득/업그레이드
    4. 무기 진화 (조건 충족 시)
    5. 바이옴 전환
    6. 30분 보스전
    7. 승리/게임오버
    8. 타이틀 복귀
  - 버그 수정: 통합 중 발견된 모든 이슈
  - 프레임 드랍 확인: 50적 + 다중 무기 + 젬 상태에서 30fps 유지
  - 엣지 케이스 검증:
    - 레벨업과 보스 스폰 동시 발생 → 레벨업 우선
    - 대시 중 충돌 → 무적 적용
    - enemy cap 보스 포함 → 정상 유지

  **Must NOT do**:
  - 새 기능 추가 금지 (버그 수정만)
  - 큰 리팩토링 금지

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on ALL above tasks (1-34). Blocks: 36. Wave 8.

  **References**:
  - All tasks from Phase 1-7
  - Full game state machine from Task 2
  - All QA scenarios from previous tasks

  **Acceptance Criteria**:
  - [ ] 전체 플로우 타이틀→승리/게임오버→타이틀 무결함
  - [ ] 30fps 유지 (50적 상태)
  - [ ] 모든 엣지 케이스 정상 처리

  **QA Scenarios**:

  ```
  Scenario: Full game flow from title to victory
    Tool: Pyxel MCP (play_and_capture, inspect_state)
    Steps:
      1. Start → select character → select difficulty → play
      2. Kill enemies, level up, get weapons
      3. Fast-forward to 30:00 (debug time scale)
      4. Defeat boss → victory screen
      5. Return to title
    Expected Result: Complete flow without crashes or soft-locks
    Evidence: .sisyphus/evidence/task-35-full-flow.png

  Scenario: Performance under load (50 enemies + weapons)
    Tool: Pyxel MCP (inspect_state)
    Steps:
      1. Spawn 50 enemies with multiple weapons active
      2. Verify frame timing consistent (no significant slowdown)
    Expected Result: Game runs smoothly with max enemies
    Evidence: .sisyphus/evidence/task-35-perf.json
  ```

  **Commit**: YES - `fix(integration): full game flow integration and bug fixes`

---

- [x] 36. 최종 리소스 정리 + README.md 생성

  **What to do**:
  - 코드 정리: 불필요한 주석 제거, 매직넘버 상수화
  - 스프라이트 품질 검토: `inspect_sprite`로 각 스프라이트 확인 — **VS 원작 수준 품질 기준**:
    - 각 스프라이트 16×16 내에서 최소한의 핵심 디테일 포함 (눈, 무기, 장식 등)
    - 16색 팔레트 내에서 명암/하이라이트 활용
    - VS 원작의 다크 판타지 분위기 유지
    - 플레이스홀더 수준 스프라이트는 모두 교체
  - `README.md` 생성:
    - 게임 소개
    - 설치/실행 방법 (`pip install pyxel`, `python main.py`)
    - 조작법 (Arrow/WASD, Space/X, ESC)
    - 게임 방법 (VS 클론 설명)
    - 크레딧 (팀원 목록)
    - 로드맵/페이즈 구조 요약

  **Must NOT do**:
  - 기능 변경 금지 (정리만)
  - 과도한 리팩토링 금지

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: [`pyxel`]

  **Parallelization**: Depends on 35. Blocks: F1-F4. Wave 8.

  **References**:
  - All tasks for credits
  - Team member list from user input
  - Game design specification for README content

  **Acceptance Criteria**:
  - [ ] README.md 존재
  - [ ] 실행 방법 명확
  - [ ] 코드에 매직넘버 최소화

  **QA Scenarios**:

  ```
  Scenario: README contains installation and run instructions
    Tool: Bash (read file)
    Steps:
      1. Read README.md → contains "pip install pyxel" and "python main.py"
    Expected Result: Clear instructions for setup and play
    Evidence: .sisyphus/evidence/task-36-readme.md

  Scenario: Game runs from clean state following README
    Tool: Bash
    Steps:
      1. `pip install pyxel` (if not installed)
      2. `python main.py` → Pyxel window opens
    Expected Result: Game launches successfully
    Evidence: .sisyphus/evidence/task-36-launch.txt
  ```

  **Commit**: YES - `docs: README with installation, controls, and roadmap`

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

> 4 review agents run in PARALLEL. ALL must APPROVE.
> Present consolidated results to user and get explicit "okay" before completing.

- [x] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (validate_script, run_and_capture, inspect_state). For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in .sisyphus/evidence/. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [x] F2. **Code Quality Review** — `unspecified-high`
  Run `python -m py_compile main.py` + `validate_script`. Review all files for: performance issues (O(n²) collision without spatial partition), hardcoded magic numbers, dead code, excessive comments, inconsistent naming. Check Pyxel-specific anti-patterns: frame-dependent timing, missing cls(), overdraw.
  Output: `Compile [PASS/FAIL] | Validate [PASS/FAIL] | Files [N clean/N issues] | VERDICT`

- [x] F3. **Real Manual QA** — `unspecified-high` (+ `pyxel` skill)
  Start from clean state. Execute EVERY QA scenario from EVERY task — follow exact steps, capture evidence via MCP tools. Test cross-phase integration (full game loop from title to victory/game over). Test edge cases: 50 enemy cap, pause during level-up, dash during boss. Save to `.sisyphus/evidence/final-qa/`.
  Output: `Scenarios [N/N pass] | Integration [N/N] | Edge Cases [N tested] | VERDICT`

- [x] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual file content. Verify 1:1 — everything in spec was built (no missing), nothing beyond spec was built (no creep). Check "Must NOT Have" compliance. Flag unaccounted code.
  Output: `Tasks [N/N compliant] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Commit Strategy

- **After Phase 1**: `feat(core): project skeleton, state machine, title screen, HUD`
- **After Phase 2**: `feat(player): 8-dir movement, infinite map, dash, biomes`
- **After Phase 3**: `feat(combat): first enemy, whip weapon, damage, XP gems`
- **After Phase 4**: `feat(progression): level-up, upgrades, passive items`
- **After Phase 5**: `feat(content): all weapons, enemies, character/difficulty select`
- **After Phase 6**: `feat(evo-boss): weapon evolution, 30min boss, victory/defeat`
- **After Phase 7**: `feat(polish): SFX, difficulty scaling, pause, stats, balance`
- **After Phase 8**: `feat(integration): full flow test, README, final cleanup`

---

## Success Criteria

### Verification Commands
```bash
python -m py_compile main.py                    # Expected: no output (PASS)
python main.py                                   # Expected: Pyxel window opens with title screen
pyxel MCP validate_script main.py               # Expected: no errors
pyxel MCP inspect_state main.py frames="180"    # Expected: state=="PLAYING", enemy_count<=50
pyxel MCP render_audio main.py sound_index=0    # Expected: waveform data present (attack SFX)
```

### Final Checklist
- [ ] All "Must Have" present
- [ ] All "Must NOT Have" absent
- [ ] Full game loop: Title → Select → Play → Boss → Victory/GameOver
- [ ] 8 weapons functional with auto-attack
- [ ] 8 enemies with distinct AI patterns
- [ ] 8 characters selectable
- [ ] 4 biomes transition correctly
- [ ] Weapon evolution works (weapon + passive → evolved weapon)
- [ ] Boss appears at 30:00 with minions
- [ ] SFX plays for attack, kill, level-up
- [ ] Dash works with cooldown
- [ ] Enemy cap (50) enforced
- [ ] 3 difficulty levels scale correctly
- [ ] Game over shows stats (time, level, kills, weapons)
