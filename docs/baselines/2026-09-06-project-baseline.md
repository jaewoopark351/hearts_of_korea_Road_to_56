# 2026-09-06 프로젝트 기준선

> 역사적 스냅샷: 이 문서는 1차 구현 전 상태와 14:06 실패 실행을 보존한다. 현재 구현 결과는 [1차 구현 기록](../implementation/2026-09-06-first-port-batch.md), 현재 정적 결과는 [검증 기록](../validation/2026-09-06-static-validation.md)을 참조한다.

## 1. 상태

- 조사 시각 기준: 2026-09-06 (Asia/Seoul)
- 작업 유형: 읽기 전용 source/log inventory와 문서화
- 프로덕션 구현 변경: 없음
- 게임 실행: 없음
- Git 변경: 없음
- 현재 compat root: Git 저장소 아님

이 문서는 특정 시점의 로컬 파일과 2026-09-06 실패 실행을 연결한다. RT56 Workshop 폴더는 Steam이 갱신할 수 있으므로 이후 작업은 새 fingerprint를 기록해야 한다.

## 2. 경로와 역할

| 별칭 | 경로 | 접근/역할 |
|---|---|---|
| COMPAT_ROOT | C:\hoi\hearts_of_korea_Road_to_56 | 이 신규 모드의 쓰기 대상 |
| HOK_DONOR | C:\hoi\hearts_of_korea | 읽기 전용 donor와 provenance |
| RT56_SOURCE | C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968 | 읽기 전용 호스트 snapshot |
| VANILLA_SOURCE | C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV | 읽기 전용 엔진 기준 |
| HOI4_LOGS | C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV\logs | 읽기 전용 런타임 증거 |

## 3. 게임·실행 기준선

2026-09-06 14:06:19 +09 실패 실행에서 확인:

- HOI4: Operation Postern 1.19.2.0.a729
- engine revision: a729d47bd1c55457e6886b6eeb2fcdef4ac05057
- Steam app build ID: 23969257
- 운영체제: Windows 11 x64
- 예외: C0000005 ACCESS_VIOLATION
- disabled_dlcs: 빈 배열. 보유/활성 DLC 전체가 확인됐다는 뜻은 아니다.

활성 목록의 기록 순서:

1. mod/hearts_of_korea_Road_to_56.mod
2. mod/ugc_820260968.mod — The Road to 56
3. mod/ugc_2769576030.mod — The Road to 56 Korean Translation

The Road to 56 Korean Translation(Workshop `2769576030`)은 1.19.*를 선언하고 localisation을 replace_path하며 RT56을 의존성으로 둔다. compat descriptor가 요구하는 Korean Language(Workshop `2743487021`, 설치 descriptor 기준 supported 1.17.*)는 설치되어 있었지만 이 실행에는 활성화되지 않았다.

실행의 상세 로그 해시와 오류 순서는 [시작 크래시 조사](../incidents/2026-09-06-startup-crash.md)에 있다.

## 4. descriptor fingerprint

| 대상 | 핵심 선언 | SHA-256 |
|---|---|---|
| compat | version 1.0.0; supported 1.19.*; dependency Korean Language; remote ID 없음 | 8F3C37B919E729E681B4FFC9A0A0F5DECACC5AF58B479E80FC5349862073E71E |
| HOK donor | version 1.0.0; supported 1.19.*; dependency Korean Language; remote 3793992662 | 3FBC6868A7D95BACD6B55AF71593A61AF3A7EADA5654D46CC4C828422ECA032A |
| RT56 | version/supported 1.19.*; replace_path history/states, map/strategicregions; remote 820260968 | 5B323861ABD63E31CB896277E3EA58BA4BCD9FCEEDA957B50792065E42E03F61 |

compat descriptor의 표시명은 RT56 호환을 주장하지만 RT56 dependency가 없다. 이는 문서 작성 시점의 미해결 구성 결함이며, 이번 문서 작업에서는 descriptor를 수정하지 않았다.

RT56 snapshot 참고값:

- Workshop manifest: `3323396725579032799`
- Workshop metadata timeupdated: `2026-08-07 23:34:24Z`
- RT56 README label: `Road to 56 Beta Build / 1956_Operation_Crimson [1.19.* Compatibility]`

descriptor에는 더 구체적인 semantic version이 없으므로 위 label을 정식 버전처럼 확대 해석하지 않는다. 실제 고정 기준은 Workshop ID/manifest와 대상 파일 해시다.

## 5. 소스 계보와 파일 상태

CONFIRMED:

- HOK_DONOR는 Git main의 commit 887930f이며 조사 당시 working tree가 깨끗했다.
- donor descriptor의 이름은 1.19 호환 개정판임을 나타내고 remote_file_id는 3793992662다.
- 따라서 HOK_DONOR를 역사적 Workshop 2898629778의 손대지 않은 원본이라고 부를 수 없다. 이 프로젝트에서는 “사용자 제공 HOK donor snapshot”으로 기록한다.
- COMPAT_ROOT에는 .git 디렉터리가 없다.
- 문서 개편 전 COMPAT_ROOT에는 총 1,015개 파일이 있었고, 그중 1,014개가 production/root 파일, 하나가 2026-09-06 incident 문서였다.
- HOK_DONOR에는 1,014개 production/root 파일과 14개 과거 문서가 있었다.
- 양쪽의 비교 가능한 production/root 파일 1,014개 중 descriptor만 달랐고 나머지 1,013개는 byte-identical이었다.

결론: 현재 compat production tree는 아직 RT56용으로 선별된 delta가 아니라 HOK donor snapshot의 복제본이다.

## 6. exact-relative-path 충돌

COMPAT_ROOT와 RT56_SOURCE의 같은 상대경로는 총 73개였고 byte-identical 파일은 없었다.

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

고위험 충돌 예:

- common/bookmarks/the_gathering_storm.txt
- common/military_industrial_organization/organizations/00_generic_organization.txt
- common/scripted_triggers/unit_medals_scripted_triggers.txt
- common/on_actions/04_mtg_on_actions.txt
- common/on_actions/14_sea_on_actions.txt
- common/national_focus/china_shared_TSR.txt
- common/national_focus/korea.txt
- common/characters/KOR.txt
- events/ElectionEvents.txt
- events/SEA_Japan.txt
- events/WTT_Japan.txt
- history/states/525-South Korea.txt
- history/states/527-North Korea.txt
- history/states/528-Nagasaki.txt
- map/definition.csv
- map/provinces.bmp
- map/buildings.txt
- map/railways.txt
- map/supply_nodes.txt
- map/unitstacks.txt
- map/strategicregions/186-Korea.txt

73은 exact-path 하한이다. 다른 파일명으로 같은 논리 ID를 정의하는 충돌은 아직 전체 감사하지 않았다.

전체 상대경로 목록은 [exact-path 충돌 인벤토리](../audits/2026-09-06-exact-path-collision-inventory.md)에 있다.

## 7. 지도 데이터

### definition.csv

| 대상 | 행/ID 수 | ID 범위 | SHA-256 |
|---|---:|---|---|
| 바닐라 | 13,414 | 0–13413 | 86846BE71198D6772C651638AA22E3656133198DE9B7C49C6234ED48CF33D87B |
| HOK donor | 13,448 | 0–13447 | 0DD53CE40928593FA59C4661863EA4257BDC1E3EC8FDA6D3F790C319A2F8F228 |
| compat | 13,448 | 0–13447 | 0DD53CE40928593FA59C4661863EA4257BDC1E3EC8FDA6D3F790C319A2F8F228 |
| RT56 | 13,535 | 0–13534 | 005BB6052AEDBAA85FFE4607B21398A33055624A78C2F822F116AE895B58393E |

CONFIRMED:

- HOK와 RT56의 공통 ID 13,448개 중 definition 행이 다른 ID는 654개다.
- HOK가 바닐라 뒤에 추가한 13414–13447의 34개는 RT56의 같은 ID 34개와 전부 다른 행이다.
- RT56에만 13448–13534의 87개 ID가 있다.
- HOK는 바닐라 기존 행 중 4126, 7125, 7175, 7204, 10065의 coastal 값을 true에서 false로 바꿨다. 이 변경의 현재 RT56 적용 필요성은 별도 검토 대상이다.
- 세 provinces.bmp는 모두 5632×2048이지만 SHA-256이 서로 다르다.

### state와 strategic region

CONFIRMED:

- HOK/compat state ID 1028–1031과 1082–1085는 RT56이 이미 서로 다른 유럽·카리브 지역에 사용한다.
- HOK는 같은 8개 ID를 함경, 강원, 경상, 충청·전라, 전라, 황해, 제주, 쓰시마 계열 state에 사용한다.
- HOK/compat의 525, 527, 528과 RT56의 같은 state는 각각 South Korea, North Korea, Nagasaki 계열이지만 province membership가 다르다.
- strategic region 186은 양쪽 모두 Korea 계열이지만 HOK 쪽은 위 충돌 province들을 포함한다.

따라서 province뿐 아니라 최소 8개 HOK state ID도 명시적인 재할당과 참조 migration이 필요하다. 정확한 새 ID는 최신 RT56 snapshot을 다시 확인하고 별도 구현 결정으로 배정한다.

## 8. 현재 판정

- CONFIRMED: 시작 크래시가 발생했다.
- CONFIRMED: 현재 compat 전역 지도는 RT56 state가 요구하는 87개 province를 정의하지 않는다.
- CONFIRMED: HOK의 한국 추가 province/state ID가 RT56의 다른 전 세계 엔티티와 충돌한다.
- CONFIRMED: 현재 production tree는 RT56 delta가 아니라 donor 복제본이다.
- STRONGLY_SUPPORTED: map base mismatch가 시작 크래시의 최우선 선행 원인이다.
- UNPROVEN: map mismatch만 고치면 모든 시작 오류가 사라진다.
- UNPROVEN: Korean Language 또는 RT56 Korean Translation 중 어느 구성이 최종 계약에 적합한가.
- UNPROVEN: 기존 HOK 세이브를 새 RT56 포트에서 유지할 수 있는가.

## 9. 다음 게이트

구현 전 다음 산출물이 필요하다.

1. 1,014개 production/root 파일의 분류 manifest
2. exact-path 73개 및 logical-ID 충돌 ledger
3. 현재 RT56을 base로 한 한국 지도 ID/RGB/state migration 설계
4. localisation dependency 결정
5. descriptor 수정 범위 승인
6. RT56-only와 목표 플레이세트의 깨끗한 대조 실행 허가
