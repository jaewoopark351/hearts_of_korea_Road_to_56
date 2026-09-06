# 2026-09-06 exact-path 충돌 인벤토리

> 역사적 pre-port 인벤토리: 아래 73개 수치는 구현 전 exact-path 교집합이다. 현재 파일별 결정과 해시는 [1,014개 분류 CSV](2026-09-06-production-file-classification.csv), 병합 결과 요약은 [통합 ledger](2026-09-06-integration-ledger.md)를 참조한다.

## 상태

- 유형: 읽기 전용 정적 inventory
- 비교: COMPAT_ROOT 대 RT56_SOURCE
- 기록일: 2026-09-06
- 결과: 같은 상대경로 73개, byte-identical 0개
- 논리 ID 감사: 미완료
- 병합 분류: 미완료

이 목록은 파일 경로가 겹친다는 사실만 기록한다. 어느 파일을 보존·삭제·대체할지 결정하지 않으며, RT56 또는 HOK 쪽이 자동으로 옳다는 뜻도 아니다. 다른 파일명으로 같은 논리 ID를 정의하는 충돌은 이 목록에 포함되지 않는다.

## 집계

| 최상위 경로 | 수 |
|---|---:|
| common | 19 |
| descriptor.mod | 1 |
| events | 3 |
| gfx | 15 |
| history | 8 |
| interface | 1 |
| map | 7 |
| README.md | 1 |
| sound | 17 |
| thumbnail.png | 1 |
| **합계** | **73** |

## 전체 목록

### common (19)

- common/bookmarks/the_gathering_storm.txt
- common/characters/KOR.txt
- common/countries/colors.txt
- common/countries/cosmetic.txt
- common/decisions/JAP.txt
- common/difficulty_settings/00_difficulty.txt
- common/ideas/korea.txt
- common/intelligence_agencies/00_intelligence_agencies.txt
- common/military_industrial_organization/organizations/00_generic_organization.txt
- common/military_industrial_organization/organizations/KOR_organization.txt
- common/names/00_names.txt
- common/national_focus/china_shared_TSR.txt
- common/national_focus/korea.txt
- common/on_actions/04_mtg_on_actions.txt
- common/on_actions/14_sea_on_actions.txt
- common/scripted_triggers/unit_medals_scripted_triggers.txt
- common/units/names_divisions/KOR_names_divisions.txt
- common/units/names_divisions/MON_names_divisions.txt
- common/units/names_ships/KOR_ship_names.txt

### events (3)

- events/ElectionEvents.txt
- events/SEA_Japan.txt
- events/WTT_Japan.txt

### history (8)

- history/countries/JAP - Japan.txt
- history/countries/KOR - Korea.txt
- history/countries/MON - Mongolia.txt
- history/general/generic_advisors.txt
- history/states/525-South Korea.txt
- history/states/527-North Korea.txt
- history/states/528-Nagasaki.txt
- history/units/JAP_1936_naval.txt

### map (7)

- map/buildings.txt
- map/definition.csv
- map/provinces.bmp
- map/railways.txt
- map/strategicregions/186-Korea.txt
- map/supply_nodes.txt
- map/unitstacks.txt

### gfx (15)

- gfx/flags/KOR_communism.tga
- gfx/flags/KOR_democratic.tga
- gfx/flags/KOR_fascism.tga
- gfx/flags/KOR_neutrality.tga
- gfx/flags/medium/KOR_communism.tga
- gfx/flags/medium/KOR_fascism.tga
- gfx/flags/medium/KOR_neutrality.tga
- gfx/flags/small/KOR_communism.tga
- gfx/flags/small/KOR_fascism.tga
- gfx/flags/small/KOR_neutrality.tga
- gfx/loadingscreens/load_10.dds
- gfx/loadingscreens/load_11.dds
- gfx/models/units/planes/KOR_plane_heavy_diffuse.dds
- gfx/models/units/planes/KOR_plane_light_diffuse.dds
- gfx/models/units/planes/KOR_plane_medium_diffuse.dds

### sound (17)

- sound/kor/kor_Idle_001.wav
- sound/kor/kor_Idle_002.wav
- sound/kor/kor_Idle_003.wav
- sound/kor/kor_Idle_004.wav
- sound/kor/kor_Idle_005.wav
- sound/kor/kor_Neutral_001.wav
- sound/kor/kor_Neutral_002.wav
- sound/kor/kor_Neutral_003.wav
- sound/kor/kor_Neutral_004.wav
- sound/kor/kor_Positive_001.wav
- sound/kor/kor_Positive_002.wav
- sound/kor/kor_Positive_003.wav
- sound/kor/kor_Positive_004.wav
- sound/kor/kor_Retreat_001.wav
- sound/kor/kor_Retreat_002.wav
- sound/kor/kor_Retreat_003.wav
- sound/kor/kor_Retreat_004.wav

### interface와 root metadata (4)

- interface/frontendmainviewbg.gfx
- descriptor.mod
- README.md
- thumbnail.png

## 우선 감사 대상

다음은 RT56 전역/공유 동작이나 시작 로드를 크게 바꿀 수 있어 먼저 분류한다.

1. map의 7개 파일과 history의 state 3개
2. bookmark
3. generic MIO와 KOR MIO
4. medal scripted triggers와 on_actions
5. difficulty, intelligence agency, generic advisor, colors/cosmetic
6. 일본·중국 공용 focus/decision/event/history
7. KOR character, idea, focus와 OOB 연결
8. frontend와 공용 loading screen

KOR 이름이 있는 파일도 자동으로 안전하지 않다. RT56이 같은 KOR 논리 ID를 정의하거나 다른 시스템에서 참조할 수 있으므로 정의와 호출자를 함께 검사한다.

## 후속 ledger 필드

각 항목에 다음을 추가해야 분류가 완료된다.

- integration class: ADD / USE_RT56 / THREE_WAY_MERGE / OVERRIDE / BINARY_MERGE / ASSET_COPY
- 충돌 logical ID
- compat/donor/RT56 SHA-256
- RT56 Workshop manifest와 파일 수정 시각
- 보존할 HOK delta
- RT56에서 보존할 동작
- 재배포 및 attribution 상태
- 정적 검사
- 대조군/실험군 런타임 결과

완성된 ledger 없이 파일이 release package에 남아 있다는 사실 자체를 채택 결정으로 보지 않는다.
