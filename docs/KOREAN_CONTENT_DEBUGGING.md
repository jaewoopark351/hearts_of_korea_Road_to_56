# HOK 한국 콘텐츠 우선 디버깅 플레이북

## 1. 목적과 적용 원칙

이 문서는 RT56 호환 문제를 찾으면서 HOK의 한국 콘텐츠를 제거하거나 RT56 표현으로 조용히 대체하지 않기 위한 실행 절차다. 장기 소유권은 [ADR-0004](decisions/0004-hok-korean-content-priority.md)를 따른다.

핵심 목표는 “오류가 적은 모드”가 아니라 다음 결과다.

- HOK의 한국 gameplay와 시청각 정체성을 가능한 한 그대로 살린다.
- 일반 중국·일본 및 전 세계 gameplay는 현재 RT56을 유지한다.
- 한중·한일 접경에서는 RT56 base에 HOK 한국 연결점만 병합한다.
- 진단 중 일시적으로 제외한 HOK 기능은 원인 판별 뒤 복원하고, 호환되는 형태로 고친다.

이 문서는 게임 실행이나 production 파일 수정을 자동으로 허가하지 않는다. 각 실행·수정은 사용자가 허가한 범위에서만 수행한다.

## 2. 보존 계약을 먼저 작성한다

오류를 고치기 전에 대상 기능별로 다음 표를 채운다. 이 표가 없으면 “파일을 빼니 실행됐다”를 수정 완료로 인정하지 않는다.

| 필드 | 기록 내용 |
|---|---|
| 기능 ID | 예: `KOR-start-history`, `KOR-voice`, `KOR-democratic-focus` |
| HOK 기준 | donor 파일·논리 ID·자산 해시와 원래 관찰 동작 |
| RT56 기준 | 현재 host 파일·ID·연결점과 정상 비한국 동작 |
| 보존 수준 | `EXACT`, `SEMANTIC_EQUIVALENT`, `MIGRATED`, `DEFERRED` |
| 허용한 차이 | 현재 schema, 지도 ID migration 등 불가피하고 검토된 차이 |
| 금지한 손실 | 사라지면 안 되는 focus/event/인물/그림/음성/밸런스 |
| 검증 | 정적 검사, 로그, 화면·청취·gameplay 결과 |

보존 수준의 뜻은 다음과 같다.

- `EXACT`: ID, 값, 동작 또는 asset bytes가 donor와 같다.
- `SEMANTIC_EQUIVALENT`: 현재 엔진 방식은 다르지만 플레이 결과와 의도가 같다.
- `MIGRATED`: 지도 ID나 교리처럼 의도적으로 이전했으며 매핑과 차이가 기록돼 있다.
- `DEFERRED`: 아직 이식 또는 검증하지 못했다. 삭제나 RT56 대체로 숨기지 않는다.

## 3. 콘텐츠 경계

| 영역 | 기본 기준 | 디버깅 중 지켜야 할 것 |
|---|---|---|
| KOR 국가·정치·OOB·인물·focus·idea·decision·event | HOK | 현재 schema로 고치되 HOK 결과와 상속 ID를 보존 |
| HOK 한국 지도 | HOK delta + RT56 전 세계 base | province/state/region/supply 참조를 원자적 묶음으로 검증 |
| KOR 음성·그림·초상화·국기·모델 | HOK payload | registry ID는 중복 없이 단일 병합 정의로 유지 |
| KOR 경로의 `KCH`, `KJP` 등 후속 결과 | HOK | 이름이 CHI/JAP 계열이어도 한국 경로의 산출물이면 보존 |
| 일반 JAP/CHI/PRC/군벌 gameplay | RT56 | donor whole file로 덮지 않음 |
| 한중·한일 상호작용 | RT56 base + HOK 한국 hook | KOR trigger/option/effect/state 참조만 최소 병합 |
| generic·전역 시스템 | RT56/vanilla current schema | 한국 예외는 additive glue 또는 검토된 three-way merge로 추가 |

경계가 애매하면 파일명이 아니라 진입점과 소비자를 추적한다. KOR focus에서 시작해 일본 event option을 거쳐 한국 state를 바꾸는 흐름은 한국 보존 대상이지만, 그 파일에 함께 든 일반 일본 내정은 RT56 대상이다.

## 4. 실행 대조군

모든 런타임 시험은 전체 프로세스를 종료한 뒤 cold start로 실행한다. HOK donor는 `C0`/`C1`에서 활성화하지 않는다.

| ID | 플레이세트·선택 국가 | 판별 목적 |
|---|---|---|
| `V0` | vanilla | 엔진·DLC 자체 기준선 |
| `R0` | RT56 | host 자체 오류와 정상 동작 |
| `R1` | RT56 + 선택 localisation | 번역 계층이 추가한 차이 |
| `C0-NONKOR` | RT56 + compat, 비한국 국가 | compat의 전역 map/shared/on_action 영향 |
| `C0-KOR` | RT56 + compat, KOR | 한국 초기화와 콘텐츠 영향 |
| `C1-NONKOR` | RT56 + localisation + compat, 비한국 국가 | 목표 구성의 전역·번역 영향 |
| `C1-KOR` | RT56 + localisation + compat, KOR | 실제 목표 한국 구성 |
| `C1-JAP/CHI` | 최종 구성, JAP와 대표 중국 국가 | RT56 중국·일본 보존 회귀 검사 |
| `H0` | donor HOK + donor가 요구한 원래 의존성 | 선택적 보존 기준 캡처 전용; target 호환 구성 아님 |

`H0`는 현재 버전에서 성공한다고 가정하지 않는다. 실행 가능할 때 HOK의 화면, 음성, 수치와 이벤트 흐름을 기록하는 참고 대조군일 뿐이다.

## 5. 실행 게이트

각 실행은 아래 게이트를 순서대로 통과시키고, 처음 실패한 지점에서 증거를 보존한다.

| Gate | 관찰 |
|---|---|
| `G0 Discovery` | launcher 표시명, 실제 물리 경로, dependency, 활성 모드와 RT56 snapshot |
| `G1 Database` | main menu 도달, province/definition/state/ID 등록과 최초 parser 오류 |
| `G2 New game` | 국가 선택 후 1936 새 게임 생성과 crash 여부 |
| `G3 Paused map` | 한국 정부·지도·OOB·UI가 일시정지 상태에서 표시 |
| `G4 +1 day` | unpause 후 24시간, 즉시 event/on_action/crash/error spam 없음 |
| `G5 +7/+30 days` | 주간·월간 초기화, AI, mission, decision와 이벤트 반복성 |
| `G6 Feature` | focus, decision, event, 전쟁·평화, 음성, 자산, supply 등 목표 시나리오 |

메인 메뉴나 `G1` 통과만으로 지도와 gameplay를 정상이라고 판정하지 않는다.

## 6. 오류 귀속 규칙

| 관찰 | 우선 귀속 | 다음 행동 |
|---|---|---|
| `R0`에도 같은 오류·빈도로 존재 | RT56/엔진 baseline | compat에서 무작정 수정하지 말고 한국을 막는지 확인 |
| `C0`에서만, KOR와 비한국 모두 실패 | compat 초기화 영역 | map/shared뿐 아니라 모든 국가와 함께 초기화되는 KOR history/OOB도 임시 slice로 격리 |
| KOR만 실패 | 플레이어 선택 이후 한국 경로 | KOR UI/controller와 선택 후 효과부터 보되 history/OOB 정적 오류가 없다는 증거로 쓰지 않음 |
| `C0`는 통과하고 `C1`만 실패 | localisation/load contract | `replace_path`, locale header, dependency와 실제 우선순위 조사 |
| JAP/CHI만 RT56 대조와 달라짐 | 동아시아 병합 회귀 | HOK whole-file shadow 또는 과도한 hook 검사 |
| 기능을 끄면 통과하고 다시 켜면 재현 | 인과 후보 | 그 묶음 안에서 최소 재현; 기능 제거를 최종 수정으로 삼지 않음 |
| 로그 오류는 없지만 HOK 표현이 다름 | 보존 회귀 | payload와 registry 소비 경로를 별도로 추적 |

판정에는 `CONFIRMED`, `STRONGLY_SUPPORTED`, `UNPROVEN`, `DISPROVEN`을 사용한다. 네이티브 crash stack이 파일을 가리키지 않으면 직전 로그 한 줄만으로 직접 원인을 확정하지 않는다.

## 7. 현재 새 게임 크래시의 격리 순서

현재 사건은 [포팅 후 새 게임 접근 위반](incidents/2026-09-06-post-port-new-game-crash.md)이다. 21:28 비한국 국가와 21:30 KOR의 `C0`는 번역 모드 없이도 같은 `C0000005` stack으로 실패했다. 두 실행에서 폐기 수송기 기술 오류가 사라졌으므로 그 오류는 직접 원인이 아니며, 국가 선택과 localisation도 이 재현의 필요조건이 아니다.

현재 순서는 다음과 같다.

1. RT56 snapshot, HOI4 build, DLC, active mods, 작업 트리와 현재 로그 hash를 고정한다.
2. 확인된 `map/buildings.txt` 생성 결함을 먼저 수정·검증한다. 기존 2-way donor-vs-바닐라 delta가 RT56에서 제거된 vanilla-identical HOK 항구 spawn 7행을 누락했다.
3. 생성기 `--check`와 aggregate validator에서 다음을 확인한다.
   - 7행이 정확히 한 번만 복원되고 총 building 행이 71,902개다.
   - 각 spawn 좌표가 예상 한국 coastal province와 effective state를 가리킨다.
   - 마지막 연결 province가 유효한 sea province다.
   - 합성 결과에 pinned RT56 기준보다 새로 생긴 coastal-without-`naval_base_spawn`가 없다.
4. 새 산출물로 `C0-NONKOR`와 `C0-KOR`를 각각 cold start해 `G2`, `G3`, `G4`까지 비교한다. 우선 순서는 GER/KOR 새 게임 → paused map → +1 day다.
5. 둘 다 계속 같은 stack으로 실패할 때만 다음 전역 초기화 묶음으로 이동한다.
   - frontend/UI override
   - shared database와 전역 on_action
   - entity와 equipment graphic DB
   - 한국 지도 합성의 나머지 closure
   - 임시 비배포 KOR history/OOB slice: OOB 호출 억제 뒤 NSB 육군, BBA 공군, MTG 해군 순 재활성화
6. KOR만 실패하면 플레이어 선택 이후 경로를 우선하되 다음 vertical slice 순서로 좁힌다.
   - country history, 시작 기술·정치·법과 OOB
   - state history, unit position, railway와 supply
   - character, leader와 portrait 연결
   - idea, MIO, equipment
   - focus
   - decision과 mission
   - event와 KOR 관련 on_action
   - model, GFX, sound와 UI
   - AI
7. 새 `C0`가 통과한 뒤 `C1`을 추가해 RT56 Korean Translation의 `replace_path="localisation"` 영향을 별도로 분리한다.
8. 원인 수정 후 제외했던 HOK 묶음을 모두 복원하고 동일 재현을 다시 통과시킨다.

지도는 `definition.csv`, `provinces.bmp`, state, strategic region, adjacency, buildings, railways, supply nodes, unit positions와 history/OOB 참조가 함께 맞아야 한다. 특히 `naval_base_spawn`은 마지막 필드가 해안 province가 아니라 연결된 sea province이므로, `x`와 `z`를 내림한 좌표로 `provinces.bmp`를 샘플해 항구가 소비하는 coastal province를 판정한다. 모든 building 타입에 좌표-state 일치를 강제하지 말고 spawn 행과 이번 복원 행에 필요한 범위로 gate를 제한한다. 이 중 한 파일만 빼는 실험으로 지도 원인을 판정하지 않는다.

## 8. Sound 디버깅

### 19:20 실행 증거

- compat의 `sound/kor` 18개 WAV는 donor와 byte-identical하다.
- compat에는 donor `sound/voice_korea.asset`이 없다.
- 당시에는 RT56 `r56_vo_Korean.asset`이 KOR sound/soundeffect ID를 단일 등록했다.
- 2026-09-06 19:20 로그에서 duplicate sound ID, WAV load failure와 `kor_*` 오류는 0건이다.
- 따라서 당시 방식은 HOK WAV payload 우선에는 성공한 것으로 강하게 지지된다. 실제 청취와 모든 sample 사용은 증명하지 않았다.

### 현재 정적 구현과 확인할 것

현재 compat `sound/r56_vo_Korean.asset`은 RT56 category/compressor와 HOK sound/soundeffect 목록·가중·`volume=1.0`을 병합한다. HOK 18개 WAV와 `Positive_005`를 모두 사용하고 RT56 전용 물리 payload `kor_Idle_006.wav`·`kor_Neutral_005.wav`는 참조하지 않는다. donor `sound/voice_korea.asset`은 계속 미선적이다. 이 구조는 정적 생성·중복 검사를 통과했고 21:28/21:30 C0 로그에도 한국 음성 duplicate/load 오류가 없었다. 다만 crash가 paused map 전에 발생해 실제 단일-owner 소비와 가청 결과는 미검증이다.

1. active registry 전체에서 `KOR_infantry_*`와 `kor_*` 논리 ID가 한 번만 등록되는지 확인한다.
2. `Idle 1–5`, `Neutral 1–4`, `Positive 1–5`, `Retreat 1–4` HOK 파일 hash를 donor와 비교한다.
3. KOR 부대를 선택해 idle을 여러 차례, 이동 명령, 전투 중 선택, 후퇴 명령을 실제 청취한다.
4. HOK `Positive_005`가 실제 재생 후보인지, RT56 전용 물리 payload `kor_Idle_006.wav`·`kor_Neutral_005.wav`가 섞이지 않는지 기록한다. HOK의 `kor_Idle_006` 논리 sound ID는 `kor_Idle_003.wav`를 가리키므로 둘을 혼동하지 않는다.
5. HOK의 `volume=1.0`, `max_audible=1.3`, 재생 목록과 반복 가중이 실제로 적용되는지 확인한다.
6. 새 single-owner merge에서 duplicate/load error 0건을 다시 확인한다.

donor `voice_korea.asset`을 그대로 복구하면 과거의 sound와 soundeffect 중복이 재발하므로 사용하지 않는다.

### 음악 OGG의 별도 소유권 판정

음성 payload 보존 규칙을 모든 음악 OGG에 자동 적용하지 않는다. 음악은 최소한 `.asset`의 sound ID, `music_station`의 song 등록·chance, 실제 KOR/JAP 조건을 함께 추적해야 한다. 파일이 donor에 남아 있거나 focus와 이름이 같다는 사실만으로 런타임 소비를 추정하지 않는다.

현재 `Minshu_ikki.ogg`는 donor `hok_music.asset`에는 정의되지만 `b3ec30e`에서 `hok_songs.txt`의 등록 블록이 삭제됐다. 삭제 전 조건은 `JAP_proclaim_the_republic` 완료뿐이었고, 현재 `KOR_minshu_ikki` focus는 일본 내전을 시작하지만 song을 재생하거나 그 JAP focus를 완료하지 않는다. 따라서 현재 donor 기준으로는 한국 플레이 소비자가 없는 과거 HOK 일본 경로의 고아 payload다.

- donor 현재 동작을 보존하려면 OGG를 다시 제외한다.
- KOR focus 완료 뒤 곡을 재생 대상으로 복원하려면 asset·localisation·station 조건을 함께 설계해야 하며, 이는 호환 복원이 아니라 명시적으로 승인할 새 동작이다.
- 사용자가 복구했을 가능성이 있는 현재 파일은 선택 전까지 자동 삭제하지 않는다.

## 9. DDS·GFX 디버깅

한국 시각 자산은 다음 순서로 확인한다.

1. 소비자를 먼저 적는다: focus, idea, decision, event, character, flag, equipment 또는 mesh/material.
2. 해당 소비자가 참조하는 sprite/entity/material ID와 최종 texture 경로를 추적한다.
3. HOK와 RT56의 동일 경로 파일에 대해 hash, width/height, DDS codec, alpha, mipmap, frame 수를 비교한다.
4. payload만 바꿔도 되는 경우 HOK `.dds`/`.tga`를 같은 가상경로의 `ASSET_COPY`로 둔다.
5. registry 의미도 다르면 RT56의 현행 `.gfx`/`.asset`을 base로 HOK delta를 한 번만 등록한다.
6. 로그의 missing GFX/entity/attachment뿐 아니라 실제 화면을 확인한다.

실제 표시 점검표:

- KOR 국기와 cosmetic flag의 세 크기
- 지도자·장군·제독·advisor portrait
- focus, idea, decision과 event picture
- 연구·장비 아이콘
- 육군·항공기·함정 3D 모델의 diffuse/normal/specular
- 투명도, 색 번짐, 보라색 누락 texture, 잘못된 국가 자산과 animation/attachment

KOR plane diffuse 3개는 형식·material 계약 감사 뒤 HOK `ASSET_COPY`로 복원했다. heavy는 256×128, light/medium은 256×256이며 모두 비압축 32-bit BGRA, alpha 포함, mip 1이다. HOK mesh가 해당 diffuse/normal/specular 이름을 내장하므로, 기본 mesh/entity를 `hok_rt56_` 고유 ID로 등록하고 HOK KOR graphic DB를 새 entity에 연결했다. 실제 UV 정렬, 크기와 렌더링은 런타임에서 확인한다.

## 10. 한중·한일 접경 시나리오

한국을 살리면서 RT56 중국·일본을 보존하려면 최소 다음을 양쪽에서 시험한다.

- KOR 시작 시 독립, 영토·core·claim과 일본 주둔군 처리
- HOK KOR focus/event가 JAP·CHI·PRC 또는 군벌을 대상으로 하는 외교·전쟁·평화 효과
- 쓰시마 및 한반도 인접 state의 소유권·보급·해군기지 변화
- KOR 경로가 만드는 `KCH`, `KJP` 등의 국가 history, localisation, OOB와 후속 event
- 정상 JAP 시작에서 RT56 focus, decision, event, OOB와 AI가 보존되는지
- 대표 중국 국가 시작에서 RT56 shared focus, MIO, event와 warlord 흐름이 보존되는지

한국 경로가 통과해도 JAP/CHI 회귀가 있으면 병합은 완료가 아니다. 반대도 마찬가지다.

## 11. 실행 기록 양식

```text
Run ID / 시각:
목표 가설:
HOI4 version / checksum:
RT56 manifest / 대상 파일 hash:
compat branch / commit / working-tree 식별:
DLC / 언어:
활성 모드와 실제 물리 경로:
선택 국가 / 재현 단계:
통과한 마지막 gate:
최초 신규 오류:
R0/R1 대비 로그 delta:
crash 폴더 / exception 주소:
HOK 보존 관찰(화면·수치·음성):
JAP/CHI 회귀 관찰:
판정과 다음 구분 실험:
미검증 범위:
```

원본 로그·dump·세이브를 저장소에 자동 복사하거나 commit하지 않는다. 실행 ID, 시각, 원본 경로와 hash를 문서에 기록하고, 별도 fixture가 필요하면 개인정보를 제거한 뒤 명시적 범위로 만든다.

## 12. 현재 도구 상태

- `tools/build_korean_assets.py`가 HOK WAV·기본 항공기 payload와 병합 registry를 pinned source에서 재현한다.
- RT56-owned pruning은 HOK WAV 18개와 KOR diffuse 3개를 더 이상 삭제하지 않으며 donor `sound/voice_korea.asset`만 중복 방지 대상으로 유지한다.
- manifest builder는 위 payload를 `ASSET_COPY`, 음성 registry를 `THREE_WAY_MERGE`로 분류하고 donor byte 동일성을 검사한다. 생성 CSV를 직접 수정하지 않는다.
- aggregate validator의 한국 자산·기술 검사는 통과했다. 전체 검증은 donor 현행 song 목록에 등록되지 않은 일본 민주화 테마 `Minshu_ikki.ogg`의 Korea-only pruning 오류 1건 때문에 아직 clean이 아니다. 같은 이름의 KOR focus에는 음악 재생 효과가 없어 최종 자산 소유권을 별도로 결정해야 한다.
- HOK 음성이나 모델은 새 게임 crash 이분 탐색을 위해 영구 삭제하지 않는다. 격리가 필요하면 임시 진단 slice로만 제외하고 결과 뒤 복원한다.

## 13. 완료 기준

- 최소 3회 cold start에서 현재 접근 위반이 재현되지 않는다.
- `R0`/`R1` 대비 compat가 추가한 새 fatal 또는 심각한 반복 오류가 없다.
- `C0-KOR`와 최종 `C1-KOR`에서 새 게임, paused map, 1일·7일·30일 진행이 성공한다.
- KOR history, 정부, 법, OOB, 인물, idea, MIO, focus, decision, event와 장비가 보존 계약을 통과한다.
- 한국 지도, 해안, adjacency, 철도, 보급, 건물과 unit 위치를 실제 지도에서 확인한다.
- HOK 음성을 선택·이동·전투·후퇴 상황에서 실제 청취한다.
- HOK 초상화·국기·아이콘·event picture·3D 모델을 실제 화면에서 확인한다.
- 정상 JAP/CHI 시작과 핵심 RT56 경로가 대조군과 일치한다.
- 모든 한국 donor 기능이 `EXACT`, `SEMANTIC_EQUIVALENT`, `MIGRATED`, `DEFERRED` 중 하나로 기록된다.
- 진단 중 제외한 HOK 기능이 최종 산출물에 복원됐으며, 미보존 항목은 이유와 사용자 결정을 갖는다.
- 기존 HOK 세이브는 별도의 load–advance–save–reload 검증 전까지 호환을 주장하지 않는다.
