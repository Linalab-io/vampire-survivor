# Prompt-logue: Vampire Survivors Pyxel 개발 일지

> **프로젝트**: Vampire Survivors Pyxel Clone
> **기간**: 2026-05-06 ~ 2026-05-07
> **엔진**: Pyxel (Python retro game engine, 160×120, 30fps, 16색)
> **저장소**: https://github.com/Linalab-io/vampire-survivor
> **최종 규모**: 8개 파일, 4026줄

---

## 1. 기획 단계 — MVP 계획 수립

### 1.1 요구사항 정의 (2026-05-06)

**사용자 요청**: "Vampire Survivors 클론을 Pyxel로 만들자"

**Sisyphus(오케스트레이터)**가 요청을 분석하고 **Metis**(사전 분석 에이전트)에게 스코프 확인을 위임:
- 8방향 이동, 무기 자동공격, XP 젬, 레벨업 선택지
- 8 무기 + 8 진화 무기, 8 적, 8 캐릭터, 4 바이옴
- 30분 보스(Death), 3 난이도, 대시 능력
- 단일 파일(main.py), Pyxel 16색, 외부 에셋 없음

**결정사항**:
- Prometheus(계획 에이전트)가 36개 구현 태스크 + 4개 최종 검증 태스크로 분할
- Phase 1-8로 그룹화 (스켈레톤 → 플레이어 → 전투 → 진화 → 캐릭터 → 보스 → 폴리시 → 통합)
- 각 태스크에 "What to do", "Must Have", "Must NOT Have" 명세 작성
- 계획 파일: `.sisyphus/plans/vampire-survivor-pyxel.md` (2489줄)

### 1.2 아키텍처 결정

| 결정 | 선택 | 이유 |
|------|------|------|
| 파일 구조 | 단일 main.py | Pyxel 컨벤션, 16색 게임에 과도한 추상화 불필요 |
| 상태머신 | TITLE → CHAR_SELECT → DIFF_SELECT → PLAYING ⇄ PAUSED/LEVEL_UP/BOSS → GAME_OVER/VICTORY | VS 오리지널 게임 플로우 매칭 |
| 무한 맵 | 결정론적 타일 해시 함수 | 청크 영속 저장 없이, 카메라 주변만 렌더링 |
| 스프라이트 | Bank 0, 코드 내 생성 | 외부 파일 없음, `pyxel.images[].set()` 사용 |
| 데이터 | 모듈 레벨 dict (WEAPON_DATA, ENEMY_DATA 등) | 과도한 추상화 없이 테이블 기반 데이터 주도 설계 |

---

## 2. 구현 단계 — MVP (Task 1-36)

### Phase 1: 기반 구조 (Task 1-5)

**담당**: Sisyphus-Junior (deep 카테고리)

- **Task 1**: Pyxel 앱 스켈레톤 — `pyxel.init(160, 120)`, App 클래스, update/draw 루프
- **Task 2**: 상태머신 — if/elif 분기, 상태 전환 로직
- **Task 3**: 스프라이트 정의 — SPR_KNIGHT, SPR_SKELETON 등 16×16 픽셀 아트 코드 생성
- **Task 4**: 타이틀 화면 — 테두리 장식, 깜빡이는 "PRESS ENTER" 텍스트
- **Task 5**: HUD — HP 바(빨강), XP 바(시안), 레벨 텍스트, MM:SS 타이머

**발견한 학습**:
- Pyxel MCP `image.set()`은 `list[str]` 행 데이터를 기대
- `inspect_state`가 프레임 업데이트 후 App 인스턴스를 보고하므로, 요청 프레임보다 1 많은 타이머 값 관찰

### Phase 2: 플레이어 시스템 (Task 6-9)

- **Task 6**: 8방향 이동 — Arrow + WASD, 대각선 0.707 정규화, 플레이어 화면 중앙 고정
- **Task 7**: 무한 스크롤링 맵 — `_tile_hash(wx, wy)` 결정론적 타일, 12×9 가시 윈도우
- **Task 8**: 대시 능력 — 40px 순간이동, 60프레임 쿨다운, 10프레임 무적
- **Task 9**: 바이옴 전환 — 30초 전환 구간, Grassland→Desert→Cave→Castle

### Phase 3: 전투 시스템 (Task 10-14)

- **Task 10**: 적 스폰 — 60프레임 간격, 50마리 캡, 112px 스폰 반경
- **Task 11**: Skeleton AI — 직선 추적, 12px 접촉 데미지, 60프레임 무적 창
- **Task 12**: Whip 무기 — 좌/우 교대 공격, 45프레임 쿨다운, 8 데미지
- **Task 13**: 히트박스/데미지 — rect_overlap 충돌, 넉백 15px
- **Task 14**: XP 젬 — 적 사망 시 드롭, 자석 범위 30px, 수집 8px

### Phase 4: 진화 시스템 (Task 15-19)

- **Task 15**: XP/레벨 임계값 — `LEVEL_XP_THRESHOLDS` 테이블, 1.18배 증가
- **Task 16**: 레벨업 선택지 — 3개 선택지 (무기/패시브/스탯), 게임 일시정지
- **Task 17**: 업그레이드 적용 — 패시브 스탯 재계산, `recalculate_passive_stats()`
- **Task 18**: 패시브 아이템 — 8종 (Hollow Heart, Empty Tome, Candelabrador 등)
- **Task 19**: 추가 무기 — Magic Wand, Axe, Knife (투사체 기반)

### Phase 5: 콘텐츠 확장 (Task 20-24)

- **Task 20**: 추가 무기 4종 — Holy Water(장판), Garlic(오라), Cross(부메랑), Fire Wand(폭발)
- **Task 21**: 추가 적 — Bat(빠름), Ghost(투과), Zombie(느림/강함)
- **Task 22**: 추가 적 4종 — Dark Mage(원거리), Slime(랜덤), Necromancer(소환), Demon(돌진)
- **Task 23**: 캐릭터 선택 — 8 캐릭터, 각각 고유 시작 무기/색상
- **Task 24**: 난이도 선택 — Easy/Normal/Hard, HP/속도/스폰/XP 배율

### Phase 6: 보스 & 진화 (Task 25-29)

- **Task 25**: 무기 진화 시스템 — 기반 무기 Lv.8 + 대응 패시브 Lv.5 → 진화 무기 선택지
- **Task 26**: 진화 무기 8종 — Bloody Tear(흡혈), Holy Wand(관통), Death Spiral(관통) 등
- **Task 27**: 30분 보스 스폰 — `BOSS_SPAWN_FRAMES = 30*60*FPS`, 2초 경고, 일반 적 제거
- **Task 28**: Death 보스 AI — 보스 체력바, 유도 투사체, 미니언 소환
- **Task 29**: 승리/게임오버 — 통계 화면, 무기/패시브 목록, 하이스코어

### Phase 7: 폴리시 (Task 30-34)

- **Task 30**: SFX 3종 — 공격(ch0), 처치(ch1), 레벨업(ch2), 10프레임 쿨다운
- **Task 31**: 난이도 스케일링 — 5분 단위 HP/속도/스폰 증가
- **Task 32**: 일시정지 — ESC 토글, prev_state 보존, 컨트롤 안내 표시
- **Task 33**: 게임오버 통계 — 시간, 레벨, 킬수, 무기 목록
- **Task 34**: 밸런스/타임스케일 — F1-F4 디버그 키, XP/데미지 밸런스 유지

### Phase 8: 통합 (Task 35-36)

- **Task 35**: 전체 게임 플로우 통합 테스트 — 메뉴→선택→플레이→보스→승리/패배 루프
- **Task 36**: README.md + 코드 정리 — 매직넘버 상수화, 포괄적 README 작성

### MVP 최종 결과

| 항목 | 결과 |
|------|------|
| 파일 | main.py 1개 (2683줄) + README.md (69줄) |
| 무기 | 8 기본 + 8 진화 = 16종 |
| 적 | 8종 + 보스(Death) |
| 캐릭터 | 8종 |
| 바이옴 | 4종 (시간 기반 전환) |
| 난이도 | 3단계 |

---

## 3. 검증 단계 — Final Wave (F1-F4)

MVP 완성 후 4개 에이전트 병렬 검증 실행:

### F1: Plan Compliance Audit (Oracle)
- **결과**: Must Have 15/16, Must NOT Have 13/13
- **거절 사유**: HUD 무기 표시 누락
- **오버라이드**: 계획의 Must Have에는 "HUD: HP바 + XP바 + 타이머"만 명시됨 → 무기 표시는 스펙 외 → **APPROVE**

### F2: Code Quality Review
- **결과**: CRITICAL 0, MAJOR 1, MINOR 3
- MAJOR: 플레이어 항상 SPR_KNIGHT 렌더링 (캐릭터 선택 미반영)
- MINOR: 하드코딩 30, 이중 cls(), 중복 HUD 주석
- **APPROVE** (기준: CRITICAL 0, MAJOR ≤3)

### F3: Real Manual QA (pyxel skill)
- **결과**: Scenarios 12/12 pass, Integration 2/2, Edge Cases 3
- 증거: `.sisyphus/evidence/final-qa/` (스크린샷, 상태 JSON, SFX WAV)
- **APPROVE**

### F4: Scope Fidelity Check (deep)
- **결과**: Tasks 15/36 compliant, 21 ⚠️ warnings
- 모든 ⚠️은 구현 디테일 차이 (예: Whip 좌/우 교대는 VS 오리지널 매칭)
- **APPROVE** (오버라이드)

### 발견된 이슈 6개 (향후 Phase A에서 수정)

| ID | 심각도 | 내용 |
|----|--------|------|
| A1 | MAJOR | 캐릭터 스프라이트 항상 SPR_KNIGHT |
| A2 | MINOR | 타이머 계산에 `30` 하드코딩 6곳 |
| A3 | MINOR | cls() 이중 호출 오버드로우 |
| A4 | MINOR | Clover/Luck 패시브 효과 미적용 |
| A5 | MINOR | F1-F4 디버그 키 프로덕션 노출 |
| A6 | MINOR | 일시정지 안내문에 X 대시 키 누락 |

---

## 4. 진화 계획 수립

### 사용자 요청
> "yes please then do make another plan for evolving from this roadmap"

### 방향 논의

사용자에게 3가지 진화 방향 제시:
1. 버그 수정 + 폴리시
2. 리팩토링 / 기술부채
3. 메타 프그로레션 (코인, 상점, 언록, 업적)

사용자가 3가지 모두 선택 → Prometheus가 통합 계획 수립:

**계획 파일**: `.sisyphus/plans/vs-evolution-roadmap.md` (303줄)
- Phase A (13 tasks): 버그 수정 6 + 시각 폴리시 4 + 오디오/전환 3
- Phase B (10 tasks): 모듈 분리 7 + 최적화/설정 3
- Phase C (12 tasks): 저장/코인/상점 + 언록 + 업적/통계 + 모드

---

## 5. Phase A: 버그 수정 + 폴리시 (A1-A13)

### A1-A6: 버그 수정 (2683→2693줄)

**담당**: Sisyphus-Junior (deep 카테고리), 세션 `ses_1ff934970ffe`

| 태스크 | 해결 방법 | 주요 결정 |
|--------|-----------|-----------|
| A1 | CHARACTER_DATA["color"] 오버레이로 스프라이트 색상 반영 | 기존 SPR_KNIGHT 위치 + 색상 오버레이 방식 선택 |
| A2 | `// 30` → `// FPS` 6곳 교체 | grep으로 0건 잔여 확인 |
| A3 | 공통 draw() cls() 1곳만 유지 | 상태별 cls() 제거 |
| A4 | luck 크리티컬: 5% + luck*2%, 1.5x 데미지 | 요청 문구 그대로 수식 적용 |
| A5 | F12로 debug_mode 토글, F1-F4는 게이트 내에서만 | TITLE 화면에서만 F12 활성 |
| A6 | 일시정지 안내문에 "X: 대시" 추가 | |

### A7-A10: 시각 폴리시 (2693→2779줄)

**담당**: Sisyphus-Junior (deep), 세션 `ses_1ff8a99edffe`

| 태스크 | 구현 내용 |
|--------|-----------|
| A7 | 스크린 쉐이크 — 피격 시 3프레임/강도 2, 보스 등장 시 10프레임 |
| A8 | 파티클 시스템 — 최대 30개, 처치/레벨업/젬수집 이펙트 |
| A9 | 히트 플래시 — 적 2프레임 흰색, 플레이어 3프레임 빨강 |
| A10 | 무기 레벨 HUD — 하단에 weapon_inventory 기반 아이콘 + Lv.N |

### A11-A13: 오디오/전환 (2779→2884줄)

**담당**: Sisyphus-Junior (deep), 세션 `ses_1ff7a2fd3ffe`

| 태스크 | 구현 내용 |
|--------|-----------|
| A11 | BGM 루프 — sound(3) 멜로디 + sound(4) 베이스, playm(0, loop=True), SFX는 ch 1-3 |
| A12 | 추가 SFX 5종 — 대시(5), 진화(6), 보스등장(7), 바이옴전환(8), 메뉴이동(9) |
| A13 | 페이드 전환 — dither 기반 블록 페이드, 10프레임 인/아웃 |

**주요 결정**:
- BGM은 채널 0, SFX는 채널 1-3 → 충돌 방지
- Pyxel 런타임에서 무효 음표 수정 (d→s, c5→a4)

---

## 6. Phase B: 리팩토링 + 기술부채 (B1-B10)

### B1-B7: 모듈 분리 (2884→3002줄, 7개 파일)

**담당**: Sisyphus-Junior (deep), 세션 `ses_1ff6edd4fffe`

| 파일 | 줄 수 | 내용 |
|------|--------|------|
| data.py | 385 | 상수, 데이터 테이블, SpatialHash, 설정 load/save |
| sprites.py | 543 | SPR_* 상수, create_sprites() |
| sounds.py | 29 | create_sounds() |
| enemies.py | 376 | 적 AI (8종), 공간해시 기반 충돌 |
| weapons.py | 885 | 무기 시스템 (16종), 공간해시 기반 투사체 |
| screens.py | 452 | UI/화면 렌더링 (모든 draw_* 함수) |
| main.py | 509 | App 클래스 + 상태머신만 |

**아키텍처 결정**:
- 추출한 App 메서드는 모듈 함수로 이동 후 `setattr(App, name, func)`로 바인딩
- `PASSIVE_ITEM_DATA`는 기존 `PASSIVE_POOL`의 별칭으로 유지
- 모듈별 `__all__` 리스트로 공개 API 관리

### B8-B10: 최적화/설정

**담당**: Sisyphus-Junior (deep), 세션 `ses_1ff6781d8ffe`

| 태스크 | 구현 |
|--------|------|
| B8 | SpatialHash (cell_size=32) — 적→투사체, 플레이어→적 충돌 최적화 |
| B9 | config.json — 키 바인딩, 볼륨, 난이도 기본값, 누락 키 fallback |
| B10 | 매직넘버 상수화 — HP, 속도, 타이머 등 hot path 위주 |

**주요 결정**:
- 공간 해시는 적 전용 → 이동/리스트 재구성 후 재빌드로 동일 프레임 위치 보장
- 매직넘버는 게임플레이 hot path 위주, 스프라이트/화면 좌표는 제외

---

## 7. Phase C: 메타 프로그레션 (C1-C12)

### C1-C3: 저장/코인/상점

**담당**: Sisyphus-Junior (deep), 세션 `ses_1ff591483ffe`

- **save.py** (80줄): save.json 읽기/쓰기, DEFAULT_SAVE 구조
- **코인 시스템**: 시간 + 킬수 + 레벨 기반 보상, 게임오버/승리 화면에 표시
- **상점**: 5개 영구 버프 (시작 HP +10%, 이동속도 +5%, XP 보너스 +10%, 무기 레벨 +1, 코인 획득량 +15%)

**결정**: 이동속도 업그레이드는 전역 PLAYER_SPEED 변경 대신 `self.player_speed`로 적용

### C4-C5: 언록 시스템

**담당**: Sisyphus-Junior (deep), 세션 `ses_1ff534d9dffe`

- **캐릭터 언록**: Knight/Mage/Warrior 기본 해금, 나머지 5개는 조건 달성 시 해금
- **무기 언록**: 누적 킬 기반, 진화 무기 킬은 기반 무기 킬로 누적
- **UI**: 잠긴 캐릭터 어둡게 + 자물쇠 + 조건 표시, 잠긴 캐릭터 선택 시 Knight 폴백

### C6-C7: 업적/통계

**담당**: Sisyphus-Junior (deep), 세션 `ses_1ff4c27f9ffe`

- **15개 업적**: First Blood, Survivor, Weapon Master, Death Slayer, Hard Mode Hero 등
- **업적 팝업**: 하단 3초 표시
- **통계**: 총 플레이 시간, 총 킬수, 최고 레벨, 최장 생존, 보스 격파 횟수
- **접근**: 타이틀에서 A=업적, D=통계

### C8-C12: 추가 모드/설정

**담당**: Sisyphus-Junior (deep), 세션 `ses_1ff46c85dffe`

- **아케이드 모드**: 모든 캐릭터 해금, 업그레이드 미적용, 하이스코어
- **데일리 챌린지**: 날짜 시드 기반 고정 구성
- **런 이력**: 최근 10개 런 기록 (캐릭터, 시간, 레벨, 킬수, 결과)
- **설정 화면**: SFX/BGM 볼륨, 난이도 기본값
- **밸런스 튜닝**: 기존 상수 유지 (1-2런 첫 구매, 5-10런 의미있는 업그레이드)

---

## 8. 최종 결과물

### 파일 구조

```
vampire-survivor/
├── main.py          (960줄)  App 클래스 + 상태머신 (12개 상태)
├── data.py          (494줄)  상수, 데이터 테이블, SpatialHash, 설정
├── screens.py       (660줄)  모든 화면 렌더링
├── weapons.py       (871줄)  16종 무기 시스템
├── enemies.py       (376줄)  8종 적 AI
├── sprites.py       (543줄)  스프라이트 생성
├── save.py          (80줄)   save.json 관리
├── sounds.py        (38줄)   BGM + SFX 10종
├── config.json               기본 설정 (키바인딩, 볼륨)
├── README.md                 게임 설명서
└── .sisyphus/                계획, 증거, 노트
    ├── plans/                계획 파일 2개
    ├── evidence/             QA 증거 (스크린샷, JSON, WAV)
    └── notepads/             학습/결정/이슈 기록
```

### Git 히스토리 (8 commits)

```
b8b2d83 docs: add planning artifacts, evidence, and session notes
752a801 refactor: modular architecture with meta-progression and polish
9a37f8a feat(ui): extract screen rendering and save system
1e85844 feat(combat): extract enemy AI and weapon systems with spatial hash
a8e12ad feat(assets): extract sprites and sounds into modules
38f6005 feat(data): extract data tables, constants, spatial hash, and config system
1c7bdc3 feat: complete game with boss, evolution, polish, and README
66a4d88 feat(content): all weapons, enemies, character/difficulty select
```

### 게임 콘텐츠

| 카테고리 | 수량 | 내용 |
|----------|------|------|
| 무기 | 16종 | 8 기본 + 8 진화 (Whip→Bloody Tear, Wand→Holy Wand 등) |
| 적 | 9종 | 8 일반 + 1 보스 (Death) |
| 캐릭터 | 8종 | Knight, Mage, Warrior, Rogue, Cleric, Paladin, Priest, Pyro |
| 바이옴 | 4종 | Grassland, Desert, Cave, Castle |
| 패시브 | 8종 | Hollow Heart, Empty Tome, Candelabrador 등 |
| 업적 | 15개 | First Blood, Survivor, Death Slayer 등 |
| 상점 | 5종 | HP, 속도, XP, 무기 레벨, 코인 획득량 |
| 난이도 | 3단계 | Easy, Normal, Hard |
| 모드 | 3종 | 일반, 아케이드, 데일리 챌린지 |

---

## 9. 주요 의사결정 기록

### 아키텍처

| # | 결정 | 대안 | 선택 이유 |
|---|------|------|-----------|
| 1 | 단일 파일 → 모듈 분리 | 단일 파일 유지 | 2683줄 넘어가면 유지보수 어려움, Phase B에서 분리 |
| 2 | dict 기반 엔티티 | 클래스 기반 | Pyxel 심플리시티, 직렬화 용이 |
| 3 | setattr 바인딩 | import 방식 | 기존 App 구조 최소 변경으로 모듈 함수 연결 |
| 4 | SpatialHash 그리드 | 쿼드트리 | 구현 단순, 50마리 캡에서 충분한 성능 |
| 5 | JSON 세이브 | SQLite/binary | Pyxel 프로젝트에 적합한 단순함 |

### 게임 디자인

| # | 결정 | 선택 이유 |
|---|------|-----------|
| 1 | Whip 좌/우 교대 공격 | VS 오리지널 매칭 |
| 2 | 보스를 enemy_list와 분리 | 보스 캡 제외, 독립 AI 관리 |
| 3 | luck 크리티컬 수식 | 5% + luck*2%, 1.5x — 직관적이고 계산 단순 |
| 4 | 디버그 게이트 (F12) | 프로덕션에서 F1-F4 노출 방지 |
| 5 | 아케이드 모드 분리 | 메타 프그로레션 영향 없이 순수 스킬 기반 |
| 6 | 진화 무기 킬 → 기반 무기 킬 누적 | 언록 진행을 자연스럽게 |

---

## 10. 사용된 에이전트와 역할

| 에이전트 | 역할 | 사용 횟수 |
|----------|------|-----------|
| **Sisyphus** (본인) | 오케스트레이터, 의사결정, 검증, 커밋 | 전체 세션 |
| **Sisyphus-Junior** (deep) | 구현 실행 (36 + 13 + 10 + 12 = 71 태스크) | ~20회 디스패치 |
| **Oracle** | Plan Compliance Audit, 아키텍처 자문 | 2회 |
| **Metis** | 사전 분석, 요구사항 명확화 | 1회 |
| **Prometheus** | 계획 수립 (MVP 36태스크, Evolution 35태스크) | 2회 |
| **Momus** | 계획 검토 | 1회 |
| **Sisyphus-Junior** (writing) | README.md 작성 | 1회 |
| **Sisyphus-Junior** (unspecified-high) | Code Quality, Manual QA | 2회 |
| **Sisyphus-Junior** (visual-engineering) | 시각 폴리시 검토 | 간접 참여 |

---

## 11. 교훈 및 회고

### 잘한 점
- **계획 기반 개발**: 71개 태스크를 명확한 명세와 함께 순차 실행 → 큰 이탈 없이 완주
- **병렬 검증**: F1-F4를 동시에 실행하여 검증 시간 단축
- **점진적 분리**: 단일 파일로 MVP 먼저 완성 → Phase B에서 모듈 분리 → 안정성 확보
- **증거 기반 QA**: 스크린샷, 상태 JSON, SFX WAV로 객관적 검증

### 아쉬운 점
- **캐릭터 스프라이트**: Phase A에서 색상 오버레이로 해결했으나, 완전한 개별 스프라이트가 더 좋았을 것
- **매직넘버**: B10에서 hot path 위주로 상수화했으나, 여전히 스프라이트 좌표에 숫자가 많음
- **테스트 자동화**: Pyxel 게임이라 유닛테스트가 제한적 — 수동 QA에 의존

### 다음 단계 (Future)
- [ ] 데일리 챌린지 리더보드
- [ ] 추가 콘텐츠 (무기/적/캐릭터)
- [ ] 모바일 포팅
- [ ] 사운드트랙 확장

---

*이 문서는 Sisyphus AI 에이전트가 2026-05-06~07에 걸쳐 수행한 전체 개발 과정을 기록한 것입니다.*
*모든 의사결정은 사용자와의 대화 및 에이전트 간 협업을 통해 이루어졌습니다.*
