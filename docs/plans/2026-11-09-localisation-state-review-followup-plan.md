# 2026-11-09 현지화·주 참조 검토 후속 수선 계획

작성일: 2026-11-09, Asia/Seoul. 최초 문서 작성 상태: **문서화 완료 / 구현 미착수 / 추가 실행 검증 미실행**. 이 상태는 아래 최초 요청의 역사이며 현재 후속 상태는 다음 절을 따른다.

사용자는 직전 읽기 검토에서 발견한 네 항목의 수정을 준비하되 이번에는 **문서화 작업만** 요청했다. 이 문서는 발견 사실·수리 제안·유지할 계약·후속 확인을 기록한다. 코드·지도·현지화 값·생성기·잠금·원장·런타임 설정의 수정, 테스트·게임 실행·정리·Git 변경·게시를 승인하지 않는다.

## 2026-11-09 후속 승인과 현재 상태

최초 문서 작성 뒤 사용자는 구현과 한정된 실제 실행 검증을 별도로 승인했다. 따라서 아래 원문의 미적용·미실행·산출물 미생성 문장은 최초 문서 전용 작업 당시의 기록이다. 후속 소스·해시·검사·실행·사건을 판단하기 전에는 [구현 기록](../implementation/2026-11-09-review-followup-repairs.md)을 읽는다. 이 계획의 과거 표를 현재 파일의 검증 결과로 사용하지 않는다.

- CIV-01의 두 guarded helper에 표시 metadata6곳, 한영 새 키1쌍을 적용하고 MAP-01의 내륙 부유항 배치1행만 제외했다. 네 출력과 별도 생성·역투영·원장 계약으로 기록하며 기존 핀·고정 입력은 유지한다.
- 최종 aggregate는 **25 PASS / 0 WARNING / 11 기존 ERROR**다. 최초 수선 뒤23/0/13과 원장 hook 보완 과정은 구현 기록에 남긴다. 정적 통과를 실제 표시·효과·저장 입증으로 대신하지 않는다.
- R0/C0 cold smoke의 로그 exact signature는631개로 같고, C0의 기존 duplicate3종 발생 횟수는 각각1회 더 많다. 그 원인은 미확정이며 네 항목의 구체적인 UI·효과·저장 확인은 계속 진행한다. LOC-02/03은 실제 표시를 관측해 수리/유지를 결정할 후보로 남아 있다.
- `fixture-en-01`의 native Save가 기존 날짜12시 `_temp` 시험 저장을 덮어쓴 사건을 보존했다. 새 본문과 receipt를 남긴 뒤 원래 파일의 바이트·mtime을 정확히 복구하고 기존75개 저장 차이0을 확인했다. 별도 독점 시험명으로 stage한 새 BASE만 후속 실행에 사용한다. 이후 차이0을 사건 부재로 해석하지 않는다.
- 독점 시험명 BASE의 선택 raw/receipt/log16검사는 통과했지만 그 본문은 제어 실행 전 기준이며, 두 fixture에서 실제 제어를 실행하지 않았다. fixture-en-01에는 C0 대비 저장/continue rename warning2개의 새 payload가 있다. 사건·한 파일 복구·로그의 새 경고를 실제 효과나 전체 무오류로 대신하지 않는다.
- 이전 UI checkpoint는 **UI_BLOCKED_AWAITING_MANUAL_WINDOW_CLOSE / 복구 대기**였다. `fixture-en-02` PID15380의 활성화가 `failed to activate captured window`로 실패해 맹목 입력을 중단했다. 그 뒤 사용자의 “너가결정해줘”는 수동 닫기 확인이 아니라 판단 위임이었고, root는 소유 게임 종료·복구를 선택했다. OSK 종료는 접근 거부로 실패했으며 게임은 `/F` 없는 native 종료 요청 뒤 PID 부재를 별도로 확인했다. 정상 UI 메뉴 종료는 관측하지 않았다.
- 현재 상태는 **IMPLEMENTATION_APPLIED / RUNTIME_UI_VALIDATION_BLOCKED / USER_PROFILE_RESTORED / OSK_WINDOW_REMAINS**다. `runtime-session/restoration.json`의2026-11-09T09:16:24.245194+00:00 기록으로 원래 metadata18개·기존 저장75개·모드 선택 복구와 시험 `.mod` 부재를 확인했다. 후속 환경/소스 기록도 게임·launcher 부재·시작 환경/manifest 일치·runtime1,476개 중 네 변경만 존재·기존 잠금3개 불변을 확인한다. OSK 유틸리티 창은 남아 있다.
- CIV 실제 한영 표시·지급·guard/clamp·once-only·저장 왕복, LOC-02/03의 실제 노출·과밀 판정은 미검증이다. MAP-01 실행 근거는 R0/C0 지도 진입·시간 진행과 로그 대조에 한정한다. 적용한 civic/지도 수선은 유지하고 미확인 LOC 후보 코드는 바꾸지 않는다. 과거 원본 저장 덮어쓰기·한 파일 복구와 후속 전체 프로필 복구를 구분한다.
- 같은 승인 범위의 재개에 별도 승인을 반복해 요구하지 않는다. 실제 UI 입력 회복·현재 source/host 재확인 뒤 **새 외부 run root의 현재 프로필/저장 백업**으로 시작한다. 복구 뒤의 현재 metadata는 이전 session의 마지막 collection과 다르므로 옛 `session.start()`를 그대로 재실행하지 않고, 기존 baseline·`before/`·preparation manifest도 덮어쓰지 않는다. 명시적 restored-session transition 대안은 아직 구현되지 않았다. native Save 직전 고유 이름과 `_temp` 변형 모두의 충돌 부재·화면 반영을 확인한 후 미완료 검증을 이어간다. 자세한 실제 receipt와 재개 조건은 구현 기록을 따른다.

## 1. 적용 조건과 기준 자료

이 네 항목을 구현·재생성·검증하기 전에는 [AGENTS.md](../../AGENTS.md), [변경 영향 검토 절차](../HOK_CHANGE_COVERAGE_REVIEW.md)와 아래 관련 지침을 읽는다.

| 작업 조건 | 먼저 읽을 자료 |
|---|---|
| 수치·조건·효과 표시 또는 툴팁 과밀 수리 | [호환판 현지화 스킬](../skills/hok-rt56-localisation-review/SKILL.md), [언어 계약 ADR-0003](../decisions/0003-localisation-contract.md), [영어 이식·주석 계층](../implementation/2026-10-20-english-localisation-import.md) |
| civic 공용 효과·호출부 또는 그 생성 계층 변경 | [civic 이식 기록](../implementation/2026-10-12-korean-civic-update-port.md), [11월 콘텐츠 ADR-0007](../decisions/0007-november-content-integration.md), [최신 구현·실행의 확인 범위](../implementation/2026-11-08-hok-upstream-content-port.md) |
| 소양강 결정·표식 표시 변경 | [feature 이식 기록](../implementation/2026-10-31-korean-feature-integration-port.md), [feature 잠금](../../tools/hok_feature_update_lock.json) |
| 부유항의 주·프로빈스·배치 참조 또는 지도 생성 계층 변경 | [주 참조 스킬](../skills/hok-rt56-state-reference-review/SKILL.md), [ID 이관 ADR-0002](../decisions/0002-map-id-migration.md), [분할 ADR-0006](../decisions/0006-korean-state-split-integration.md), [분할 대응표](../data/HOK_KOREAN_STATE_SPLIT_PORT_MAPPING.json), [분할 구현 기록](../implementation/2026-11-07-korean-state-split-port.md), [분할 입력·출처 안내](../upstream/hok-state-split-20261107/README.md) |
| 현재 출력의 보호·역투영·새 후속 계층 연결 | [RT56 호스트 ADR-0008](../decisions/0008-november-rt56-host-update.md), [11월 출력 잠금](../../tools/hok_upstream_content_lock.json), [호스트 잠금](../../tools/rt56_host_update_lock.json) |

원본·설치·Workshop·활성 cache는 읽기 전용 비교 입력이다. 관련 HOK 정의의 기존 ADD/OVERRIDE 등 원장 분류와 RT56 소유권을 유지하고, 실제 구현에서는 선택한 새 delta와 출력 소유자를 별도 기록한다.

### 조사 기준선

| 항목 | 확인한 사실과 한계 |
|---|---|
| 호환판 | `C:\hoi\hearts_of_korea_Road_to_56`, `feat/korean-focus-update-20260922@f8fdd821cf80dd291b02a59b55e8d85fe558a9b3` |
| 시작 작업 트리 | 앞선 지침 도입의 `AGENTS.md`·`docs/README.md` 수정과 공통 절차·스킬2개 신규 문서, 총5개를 보존. 이번 계획의 수리 코드가 아님 |
| HOK donor | `C:\hoi\hearts_of_korea`, HEAD `596b221bb994d93fce552d3ee1ba70fa9b5640f1`, 확인 시 작업 트리 깨끗함 |
| 설치 HOI4 | `launcher-settings.json`의 `Operation Postern v1.19.4.2.2da5 (0bdb)`. 이번에 실행한 게임의 checksum이 아님 |
| RT56 | `appworkshop_394360.acf`의 설치/최신 manifest `1963361040482473746`, `timeupdated=1794141719`. ADR-0008의 새 호스트와 같음 |
| 현재 실행 구성의 한계 | 직전 읽기 검토에서 `dlc_load.json`은 일반 HOK donor와 일반판 영어 번역을 선택했고, 언어 설정은 `l_korean`, `disabled_dlcs=[]`였음. 이번에 설정을 바꾸거나 호환판을 실행하지 않음. 전체 DLC 실제 로드·launcher 유효 우선순위는 새 실행에서 확인해야 함 |
| 과거 실행 근거 | 최신 11월 구현 기록의 한정된 한영 civic UI·선택 효과·저장 관측과 aggregate `23 PASS / 0 WARNING / 11 기존 ERROR`를 유지. 이번 네 항목의 새 검증 결과로 재사용하지 않음 |

아래 줄 번호는 이 기준선의 읽기 위치다. 구현 시에는 현재 파일과 해시를 다시 확인한다. 검색 결과 수·고유 기능 수·UI 후보 수를 검사 통과 수로 합산하지 않는다.

## 2. 항목별 대장

| ID | 기능·사용처 | 소스에서 확인한 사실 | 판정·처리 | 아직 확인하지 않은 것 |
|---|---|---|---|---|
| CIV-01A | 재벌과의 산업협력 → 공용 협력 보정 | [중점](../../common/national_focus/korea.txt) 14705행 → [공용 효과](../../common/scripted_effects/HOK_KOR_civic_effects.txt) 219–228행. 재벌 영향력+10·조달 비리+5·기관 장악+5의 명목 변경에 표시 metadata/별도 수치 안내가 없음 | 명시적 metadata/수치 안내 부재는 **CONFIRMED**. 기존 같은 명령의 표시 누락·수선 기록에 비춰 중점 UI 누락은 **STRONGLY_SUPPORTED**. 최소 수리 제안, 미적용 | 현재 실제 중점 툴팁, 이미 등록된 상태와 수치 경계의 표시 |
| CIV-01B | 재벌 길들이기 → 공용 길들이기 보정 | 중점7753행 → 같은 공용 효과232–241행. 재벌 영향력-10·시민사회 영향력+5·조달 비리-5도 같은 형태 | CIV-01A와 같은 판정. 호출부·정치 분기는 별도 확인, 수리 제안 미적용 | 해당 중점의 한영 UI와 once-only 분기 |
| MAP-01 | 황해북도 부유항 배치 | [buildings](../../map/buildings.txt) 71421행의 `1153;floating_harbor;4725.00;9.50;1289.00;-4.47;10065`. [definition](../../map/definition.csv) 10066행에서10065는 `land;false` | 비해안 참조는 **CONFIRMED**, 실제 표시·동작 영향은 **UNPROVEN**. 지도 참조 최소 수리 제안, 미적용 | 부유항 행의 현행 엔진 의미·필요성, 삭제/유지 비교와 실제 지도 표시 |
| LOC-02 | 소양강 개방·정상화 결정의 가용/취소 조건 | [결정](../../common/decisions/HOK_KOR_soyang_water_gates.txt) 12–13·53–56행의 내부 global flag4종에 이름 정의와 조건용 wrapper가 없음. 취소37·77–78행도 관련됨 | 정의/wrapper 부재는 **CONFIRMED**, 원시 ID의 실제 노출은 **UNPROVEN**. UI 관측 후 수리 여부 결정 | 가용·차단·취소 화면에서 이미 설명되는 정보와 실제 노출 항목 |
| LOC-03 | civic 공용 sync의 다른 중점·결정 소비자 | [공용 효과](../../common/scripted_effects/HOK_KOR_civic_effects.txt) 82·187·201·214·227·240행 및 [civic 결정](../../common/decisions/HOK_KOR_civic_decisions.txt) 73·100·128·158·182·206·245행에서 직접 호출. 많은 파생 국민정신 교체를 포함 | 호출 구조는 **CONFIRMED**, 이 화면들의 실제 과밀/잘림은 **UNPROVEN**. 재현된 호출부만 수리하는 제안 | 각 소비 화면의 한영 펼친 목록, 주요 효과와 파생 정리의 구분 |

LOC-03의 기존 회복 사건 overflow와 그 후속 수선은 [11월 구현 기록](../implementation/2026-11-08-hok-upstream-content-port.md)의 142·148행 및 현재 확인 범위 표를 따른다. 그 기록을 남은 모든 중점·결정 화면의 overflow 증거로 확대하지 않는다.

## 3. CIV-01: 공개 수치 안내의 최소 수리안

기본 방향은 기존 두 helper의 guarded `add_to_variable` 6곳에 명시적인 표시 metadata 또는 같은 조건에서만 나오는 수치 안내를 연결하는 것이다. 이미 등록된 상태에서도 무조건 보상을 약속하는 중점 설명·툴팁을 추가하지 않는다.

- 변수4개의 ID·값·0–100 clamp, KOR tag guard, 초기화, once-only 등록 flag, 호출 순서와 실제 국민정신 결과를 보존한다. 중점 ID·기간·선행·AI·해금도 변경하지 않는다.
- 현재 양 채널의 `HOK_KOR_civic_influence_change_tt`, `HOK_KOR_procurement_corruption_change_tt`, `HOK_KOR_institutional_capture_change_tt`는 재사용 가능성을 확인한다. `HOK_KOR_chaebol_influence_change_tt`는 현재 정의돼 있지 않으므로 필요하면 명시적 새 한영 키를 후속 계층에 추가한다. 재벌 영향력의 증감을 일률적으로 좋음/나쁨으로 색칠하지 않는다.
- 효과의 명목 증감과 clamp 후 실제 차이를 구분한다. 표시 수리를 위해 증감값이나 경계 처리를 바꾸지 않는다. 한영 이름·부호·수량·색상·치환 토큰과 조건부 표시를 대조한다.
- `HOK_KOR_legacy_nationalization_adjustment`의 재벌-20·시민+10·기관 장악-5는 공용 효과245–253행, 등록271행과 startup/monthly의 별도 실행 경로다. 이를 직접 중점 보상으로 옮기거나 기존 저장의 등록 시점·일회성을 바꾸지 않는다. 이번 직접 중점2개와 구분해 의도적 유지한다.

현재 `HOK_KOR_civic_effects.txt`는 10월 civic ADD이며 [한국 builder](../../tools/build_korean_focus_update.py) 401–431행과 [civic 잠금](../../tools/hok_civic_update_lock.json), `source_snapshot.read_civic_source()` / `apply_civic_update()`가 원본을 재현한다. 이 파일은 현재 [11월 표시 모듈](../../tools/upstream_civic_display.py)의 `_CODE`/`civic_paths()` 소유 목록에 없다. 따라서 현재 출력만 고치거나 과거 civic 사본/핀을 덮어쓰는 방식은 채택하지 않는다.

구현이 승인되면 현재 최종 바이트를 선행 입력으로 고정한 좁은 후속 표시 변환을 설계한다. 기존 표시 계층의 명시적 확장 또는 새 후속 계층 중 생성 소유권과 정확한 역투영을 유지하는 방식을 선택하고, 바뀐 경로·키·이전/이후 해시·분류를 기록한다.

## 4. MAP-01: 비해안 부유항의 최소 수리안

[황해북도1153](../../history/states/1153-Hwanghaebuk.txt)의 네 프로빈스 `7070·10065·11915·13560`은 현재 합성 지도에서 모두 `land;false`다. 따라서 **1153 안의 다른 번호로 바꾸는 안은 유효한 해안 수리가 아니다.**

이 행의 계보는 vanilla/현 RT56의 부모527 → 기존 포트917 → 분할 donor1091 → 현재 포트1153이다. 현 RT56/vanilla의10065는 해안이지만, [지도 생성기](../../tools/build_rt56_map.py)의 `COASTAL_FALSE_PROVINCES`와 합성 정의가 승인된 HOK 지도에 맞춰 비해안으로 만든다. 현재 RT56 원본의 해안 속성만 보고 포트 정의를 되돌리지 않는다.

- 우선 검토할 안은 현재 내륙 주에서 성립하지 않는 **해당 부유항 행 한 개만 제외**하는 것이다. 이는 아직 확정·적용한 수리가 아니다. 엔진의 같은 건물 행 의미, HOK의 배치 의도와 실제 지도를 대조해 판단한다.
- 인접 해안 주로 이전하는 대안은 의도한 대상과 실제 합성 기하를 입증한 경우에만 검토한다. 임의의 해안 번호·기존 항구·새 좌표를 이 문서에서 정하지 않는다.
- 주/프로빈스 ID, 소속·해안선·RGB·definition, 인구·자원·시작 건물·승점·철도·보급·기존 해군기지 spawn을 보존한다. 이 한 행의 수리를 지도 재분할이나 건물 보상 변경으로 확대하지 않는다.

현재 [기본 지도 생성기](../../tools/build_rt56_map.py)는 부유항의 연결 프로빈스로 부모를 정하고, [분할 생성기](../../tools/korean_state_split.py) 196–197행도 연결 프로빈스의 현행 부모를 따라 재부모화한다. 이 흐름은10065의 새 부모1153을 얻지만 그 프로빈스의 해안 적격성은 별도로 보장하지 않는다.

또한 [11월 잠금](../../tools/hok_upstream_content_lock.json)의 `preserved_map_hashes`와 [호스트 잠금](../../tools/rt56_host_update_lock.json)의 같은 보호 목록은 현재 `map/buildings.txt` 해시를 고정한다. 호스트의 현재 `approved_runtime_revision` 경로는 콘텐츠 보존 예외이며 지도 전체 mismatch 면제가 아니다. **분할 출력/해시만 바꾸면 후속 지도 보호 계약과 충돌한다.**

후속 구현에서는 원래 지도 핀·동결 입력은 유지하고, 정확한 이전/새 지도 해시와 허용한 한 행 delta만 인정하는 등록된 최종 지도 수리·역투영 경로를 설계한다. 기본 생성·분할·후속 보호 gate에서 같은 좁은 수리가 재현되는지 확인한다. HOK 영향 부유항의 연결 ID·부모·육지/해안 속성과 합성 bitmap/배치의 대응도 별도로 확인한다. 기존 naval-base spawn 누락 검사는 이 부유항 적격성 검사를 대신하지 않는다. 분할 대응표의 과거 미해결 기록은 보존하고 후속 결정을 덧붙인다. 이전 핀의 일괄 재고정이나 보호 검사 생략은 수리안에 포함하지 않는다.

## 5. LOC-02: 소양강 내부 조건의 표시 관측과 수리안

대상은 `HOK_KOR_soyang_managed_water`, `HOK_KOR_soyang_flooding_active`, `HOK_KOR_soyang_opening`, `HOK_KOR_soyang_draining`의 실제 가용·취소 표시다. 이름 정의가 없다는 사실만으로 네 표식에 모두 번역을 추가하지 않는다.

실제 화면에서 다음을 분류한 뒤 선택한다.

| 관측 | 후속 처리안 |
|---|---|
| 플레이어에게 필요한 상태가 원시 ID로 보임 | 긍정 상태명 또는 명확한 조건 wrapper로 뜻을 제공한다. NOT에 부정 이름을 겹치지 않는다. |
| 이미 결정 설명/다른 안내로 설명된 내부 조건이 중복 노출됨 | 필요한 공개 조건을 남기며 내부 구현의 중복 표시만 정리한다. |
| 엔진에서 표시되지 않는 정상 내부 처리 | 비표시·내부 용도 근거를 남기고 수정하지 않는다. |

global scope·네 저장 ID·flag 수명·멱등 cleanup, 개방/배수 각14일·정치력25·피해·안전 조건·AI0은 유지한다. visible/available/cancel의 실제 조건을 삭제하거나 완화하지 않는다. 다른 원인의 침수 효과도 보존한다.

소양강 결정과 한영 문구는 [feature 잠금](../../tools/hok_feature_update_lock.json), `source_snapshot.feature_addition()`과 한국 builder의 feature 계층이 소유한다. `docs/upstream/hok-feature-integration-20261031/`의 `runtime`/`integrated`는 고정 입력이며 새 수정본의 저장 장소가 아니다. 관측 후 필요한 출력 경로만 후속 표시 계층에 등록한다.

## 6. LOC-03: 공용 sync의 호출부별 표시 수리안

먼저 대장의 직접 소비자6곳과 결정7곳을 실제 화면·상태별로 분류한다. 공통 초기화가 다른 호출 안에 중첩될 수 있으므로 검색된13개 위치를 고유 결함13개 또는 최종 조사 범위라고 단정하지 않는다. 관련 역호출자·분기를 확인하고 동등 경로를 묶을 때 근거를 남긴다.

`HOK_KOR_sync_civic_state`는 clamp와 실제 국민정신 교체를 수행한다. 공용 helper 전체를 일괄 숨기는 안은 채택하지 않는다. 과밀이 관측된 소비자에서 파생 정리의 표시를 좁게 감싸는 안을 우선 검토하되, 공개 수치와 실제 정책/기본 국민정신 보상은 명시적으로 남긴다. clamp·idea 추가/제거·flag·호출 횟수·순서·scope는 보존한다.

공용 효과는 CIV-01의 이전 civic 계층, civic 결정은 그 위의 11월 표시 계층도 관련된다. 현재 생성 최종화는 **분할 → 11월 콘텐츠 → 새 RT56 host**, 역사적 역투영은 역순이다. 새 표시 수리는 이 소유권과 호스트의 정확한 등록 해시 계약에 연결한다. 기존 회복 사건 수선과 그 증거를 덮어쓰지 않는다.

## 7. 후속 구현·검증 순서

아래는 **별도 구현·진단/실행 범위가 승인된 뒤** 수행할 계획이며 이번 작업의 실행 결과가 아니다.

1. 현재 branch/HEAD·기존 변경, 설치 HOI4·RT56 manifest/관련 해시·실제 모드 물리 경로·언어·DLC를 다시 기록한다. 다른 RT56 snapshot이면 그 차이를 별도로 평가한다. 이전 결과와 핀을 새 값으로 덮지 않는다.
2. CIV-01과 지도 한 행은 별도 수리 단위로 준비한다. LOC-02/03은 먼저 승인된 화면 관측으로 수정·유지·제외·미확인을 결정한다. 화면을 보지 못하면 후보 상태를 유지한다.
3. 원래 바이트·관련 호출/분기·소유 계층을 고정하고 현재 출력에 대한 좁은 수정·역투영 계약을 명시한다. 생성 출력 수동 편집 대신 승인된 생성 경로를 연결한다. 독립 기대값과 보호 범위를 먼저 정한다.
4. 관련 경로를 재생성하고 이전/새 출력·한영 키/토큰/BOM·의도 delta·비대상 경로 보존을 확인한다. 과거 ancestor/protected-map hash를 단순 완화하지 않는다. 기존11개 전체 정적 부채와 새 실패를 구분한다.
5. 필요한 실제 UI·효과·저장 확인을 아래 표대로 수행한다. 호환판 영어 구성에는 일반판 영어 서브모드와 donor를 넣지 않으며, 한국어 번역 조합·현재 선언 dependency와 실제 로드 차이를 기록한다. 사용자의 기존 설정을 바꾸는 조치는 그때의 승인 범위와 백업/복구 조건을 따른다.

| 항목 | 소스·재현 확인 | 승인된 실행에서 필요한 확인 |
|---|---|---|
| CIV-01A/B | guarded 명령6곳·각 호출자·한영 키·부호/색상·clamp·once-only·순서 보존 | 한영 중점의 등록 전/후 툴팁, 필요한 수치 경계, 실제 변수/국민정신과 일회 지급·저장 재로드. 두 정치 분기를 구분 |
| MAP-01 |10065/1153의 현재 지리, 한 행 delta, 비대상 map 행·필드·ID 집합 보존, 생성/역투영/호스트 보호 일치 | RT56 대조와 포트의 새 게임 지도 진입·주변 해안/항구/부유항 표시·배치, unpause·관련 오류 차이. 표시 앵커 수리를 게임플레이·기존 저장 호환 보장으로 확대하지 않음 |
| LOC-02 | 표시 경로·긍정/부정·네 flag ID·global scope·비용/기간·cleanup 보존 | 한영 개방 준비/침수/배수/안전 조건 상실의 가용·차단·취소 표시와 실제 비용·상태·정리. 정상 진행과 강제 상태를 구분 |
| LOC-03 | 호출부별 공개 효과/파생 정리 구분·실행 순서/idea 결과 보존 | 해당 중점·결정의 한영 펼친 목록과 접근성·잘림, 실제 변수·국민정신·필요한 저장 값/타이머 비교 |

새 저장 왕복과 변경 전 저장 호환, 표시와 실제 지급, 강제 진단과 정상 진행은 각각 기록한다. 새 게임 정책을 바꾸거나 기존9주 저장 변환·장기 AI·다른 DLC·멀티플레이 지원을 이번 수리의 자동 범위에 넣지 않는다.

## 8. 산출물·완료 기준과 이번 작업 결과

향후 승인된 시험·진단의 제안 근거 루트는 `C:\hoi\test\hok-rt56-review-followup-20261109-01\`이다. **이번에는 생성하지 않았다.** 실제 시작 때 기존 자료와 충돌하면 새 run ID를 정한다. helper·backup·로그/저장 사본·UI 증거·임시 preview·검사 출력은 그 외부 전용 위치에 둔다. `C:\hoi\test\hok-rt56-source-cache\sources\`는 고정 입력 cache이며 새 시험 출력을 넣지 않는다.

기존 `tools/__pycache__/`의21파일·1,088,888바이트는 직전 읽기 검토에서 확인한 정리 미결 자료다. 이번에는 이동·삭제하지 않으며 이 수선 계획이 정리 승인을 겸하지 않는다.

후속 수리 완료는 실제 변경 경로·키·대상·원장 분류·생성 소유권·원본/출력 해시와 비대상 보존, 각 필수 확인의 실제 결과가 갖춰졌을 때만 항목별로 판정한다. 후보가 정상 비표시/정상 목록으로 확인되면 유지 근거와 관측 범위를 남긴다. 필요한 UI·효과·저장 항목이 남으면 **구현 반영 / 검증 대기**로 제한하고, 지도 대상이 미해결이면 **수리안 판단 대기**로 남긴다.

이번 작업에서는 이 계획을 작성하고 문서 인덱스에 연결했다. 문서·소스의 읽기 대조, 관련 경로·생성 소유권·상대 링크와 변경 파일 목록만 확인했다. 구현·테스트·validator·스킬 검사·게임 실행은 하지 않았고 runtime·원본/host·source cache·lock·기존 검증 기록은 변경하지 않았다. 앞선 지침 도입5개 변경을 보존했으며 커밋·푸시·게시도 하지 않았다.

### 문서화 시 확인한 현재 출력 SHA-256

다음은 소스 기준선 식별용이며 검증 통과 결과가 아니다.

| 파일 | SHA-256 |
|---|---|
| `common/scripted_effects/HOK_KOR_civic_effects.txt` | `A114ABEEA79AC284CDEF5D62E0D88DDB232EF5B43BEDA94E4E991923742151DB` |
| `common/decisions/HOK_KOR_civic_decisions.txt` | `E5D46F0E03B33F91DB325A18F7EC8C15B79C5FBFC99544532B388843A58A61DA` |
| `common/decisions/HOK_KOR_soyang_water_gates.txt` | `603985506552D53D875C46137CE2B6CAFE1BDE73AD73ADCE633C095D34BCB953` |
| `common/national_focus/korea.txt` | `6D98EBB26EDA579D0A00ABCEA97D15E78164335A5C1D9FE65B0F894F9D6A53AC` |
| `map/buildings.txt` | `0CB4A2ABA190F42D31F732159C77A48732C41B7CFAD5F7E94816242E2D62835D` |
| `map/definition.csv` | `0B47E8CFC81D571BC1864280A213C9488AF17148B6D0F7581162BB7EEC6331D4` |
| `history/states/1153-Hwanghaebuk.txt` | `D477A60E4245BEF92E6C3A27D2D0CFD5B4460B007B56C5ECEBB8745F335A7561` |
