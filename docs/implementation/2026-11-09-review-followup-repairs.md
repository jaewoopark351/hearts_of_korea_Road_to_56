# 2026-11-09 검토 후속: civic 수치 표시와 내륙 부유항 수선

기록일: 2026-11-09, Asia/Seoul. 상태: **IMPLEMENTATION_APPLIED / RUNTIME_UI_VALIDATION_BLOCKED / USER_PROFILE_RESTORED / OSK_WINDOW_REMAINS**.

현재 상태: **civic 수치·지도 수선은 적용됐고 정적 결과는25/0/11 기존 부채다. 실제 CIV/LOC UI·효과·저장 검증은 입력 차단으로 미완료다.** 사용자가 “너가결정해줘”라고 판단을 위임한 뒤 root는 소유 게임 종료와 사용자 환경 복구를 선택했다. 게임 프로세스 종료를 확인해 수집했고 원래 설정/metadata18개·기존 저장75개·선택을 복구했으며 시험 `.mod`도 제거했다. OSK 창은 접근 거부로 남아 있다. 기존 저장 덮어쓰기 사건과 그 뒤의 정확한 복구를 구분하며, 정상 UI 메뉴 종료를 관측했다고 기록하지 않는다.

이 기록은 구현·정적 확인, 제한된 cold smoke, 미완료 UI 검증과 실제 종료/복구를 구분한다. 네 런타임 출력에 수선이 적용됐지만 CIV-01의 실제 표시·지급·저장, MAP-01의 특정 앵커 표시/운용, LOC-02/03의 실제 표시 판정은 아직 완료로 기록하지 않는다. 이후 재개 결과도 해당 실행·소스에 한정해 추가해야 한다.

## 범위와 먼저 읽을 자료

직전 요청의 문서 전용 상태는 [수선 계획](../plans/2026-11-09-localisation-state-review-followup-plan.md)에 보존한다. 이후 사용자는 네 검토 항목의 구현을 승인했고, 실행 검증에 필요한 사용자 설정·모드 선택·언어·자동저장·launcher metadata의 임시 변경과 원상 복구, 시험용 `.mod` 한 개의 생성/제거, 게임 실행, 새 로그·시험 저장의 보존도 명시적으로 승인했다. 이 승인으로 donor·Workshop·게임 설치의 수정이나 Git 커밋·푸시·게시를 수행하는 것은 아니다.

| 작업 조건 | 먼저 읽을 자료 |
|---|---|
| 이 수선의 범위·검증 상태를 판단하거나 후속 변경을 준비함 | [AGENTS.md](../../AGENTS.md), [계획](../plans/2026-11-09-localisation-state-review-followup-plan.md), [변경 영향 절차](../HOK_CHANGE_COVERAGE_REVIEW.md) |
| 수치·flag·sync의 표시 변경이나 한영 안내를 다룸 | [현지화 검토 스킬](../skills/hok-rt56-localisation-review/SKILL.md), [ADR-0003](../decisions/0003-localisation-contract.md), [영어 생성 계층](2026-10-20-english-localisation-import.md) |
| 부유항·주/프로빈스 소속 또는 지도 생성기를 다룸 | [주 참조 스킬](../skills/hok-rt56-state-reference-review/SKILL.md), [ADR-0002](../decisions/0002-map-id-migration.md), [ADR-0006](../decisions/0006-korean-state-split-integration.md), [분할 대응표](../data/HOK_KOREAN_STATE_SPLIT_PORT_MAPPING.json) |
| 현재 수선의 재현·역투영·원본 바이트를 다룸 | [새 source capsule](../upstream/hok-review-followup-20261109/README.md), [후속 잠금](../../tools/hok_review_followup_lock.json), [11월 콘텐츠 기록](2026-11-08-hok-upstream-content-port.md), [호스트 ADR-0008](../decisions/0008-november-rt56-host-update.md) |

## 기준선과 보존 대상

외부 근거 루트는 `C:\hoi\test\hok-rt56-review-followup-20261109-01\`이며 아래 `<TEST>/`는 이 경로다. 실제 helper·검사 출력·로그/저장 사본·화면·프로필 백업은 이 외부 위치에 둔다. 저장소에는 유지할 수선 코드·문서·고정 재현 입력만 둔다.

| 항목 | 이번 기준과 한계 |
|---|---|
| 호환판 | `feat/korean-focus-update-20260922@f8fdd821cf80dd291b02a59b55e8d85fe558a9b3` |
| 기존 변경 | 이번 구현 전에 있던 지침 문서6개를 보존: `AGENTS.md`, `docs/README.md`, 공통 검토 절차, 검토 스킬2개, 후속 수선 계획. `baseline.json` 수집 시점에는 병렬 작성 중이던 새 변환 모듈2개도 untracked로 나타나며, 이를 이전부터 있던 gameplay 변경으로 계산하지 않는다. |
| HOK donor | `596b221bb994d93fce552d3ee1ba70fa9b5640f1`, 확인 시 깨끗함. 읽기 전용 입력으로 유지. |
| 설치 HOI4 | `Operation Postern v1.19.4.2.2da5 (0bdb)`, Steam build `26409260`. 설치 버전과 개별 modded checksum은 별개다. |
| RT56 | 설치/최신 manifest `1963361040482473746`. descriptor·관련 map·Nanjing·Chatham·SOV source 지문은 `<TEST>/baseline.json`에 보존. |
| 시작 사용자 구성 | 일반 HOK donor와 일반판 영어 번역 선택, 한국어·`disabled_dlcs=[]`. 그 구성을 포트의 C0/C1 실행 증거로 쓰지 않는다. |
| 게임 사용자 경로 | `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV` |
| 실행 전 백업 | `<TEST>/runtime-session/baseline.json`과 `before/`: 파일127개, metadata18개, 기존 저장75개, 총 `5,797,162,033`바이트의 백업·동일성 확인. 백업 성공은 최종 복구 성공과 다르다. |
| 기존 정적 부채 | 작업 전 aggregate **23 PASS / 0 WARNING / 11 ERROR**. 근거 `<TEST>/aggregate-before.txt`. 기존 source/descriptor 부채의 핀을 이번 수선을 통과시키려고 갱신하지 않는다. |

본 작업은 donor/RT56/vanilla 원본, 이전 source capsule·lock, 외부 활성 cache의 기존 바이트를 변경하지 않는다. source cache `C:\hoi\test\hok-rt56-source-cache\sources\`는 시험 출력과 구분한다.

## 항목별 처리와 확인 단계

| ID·사용처 | 처리 | 소스로 확인한 변화·보존 | 실행·저장 상태 |
|---|---|---|---|
| CIV-01A: 재벌과의 산업협력 → 협력 helper | **수정 적용** | guarded 변수3곳에 metadata. 재벌+10·비리+5·기관 장악+5, KOR/once-only·초기화·clamp·효과 순서 보존 | 한영 중점 툴팁·등록 전/후·수치 경계·실제 일회 지급·저장은 진행 전/미확인 |
| CIV-01B: 재벌 길들이기 → 길들이기 helper | **수정 적용** | guarded 변수3곳에 metadata. 재벌-10·시민+5·비리-5 및 기존 등록 flag·호출 순서 보존 | 다른 정치 분기의 별도 확인 필요. CIV-01A의 결과로 대신하지 않음 |
| MAP-01: 황해북도1153 부유항 | **수정 적용** | 비해안10065에 연결된 특정 배치1행만 제외. definition·경계·ID·주 소속·자원·시작 건물·승점·철도·보급·naval-base spawn과 다른23 map 파일 보존 | R0/C0 지도 진입·시간 진행·로그 대조만 확인. 특정 부유항 근접 표시·운용·저장은 미검증 |
| LOC-02: 소양강4 global flag의 가용/취소 표시 | **미확인 / 코드 유지** | 정의/wrapper 부재는 확인했으나 실제 raw 노출은 미관측. 이름을 일괄 추가하지 않음 | 개방 준비·침수·배수·안전 조건 상실의 한영 표시 관측 후 결정 |
| LOC-03: 다른 civic sync 소비 화면 | **미확인 / 코드 유지** | 다른 중점·결정에서 직접 호출되는 구조는 확인. 공용 helper 전체를 숨기지 않음 | 소비자별 과밀·주요 보상/파생 정리·선택지 접근성을 관측한 뒤 필요한 곳만 판단 |

관련 항목의 유지·제외도 구분한다. 국유화 legacy 보정은 startup/monthly 등록 경로이며 직접 중점 효과로 옮기지 않았다. 세 helper의 등록 flag와 기존 저장 의미를 보존하고 CIV-01의 직접 중점2개에 섞지 않는다. `HOK_KOR_asian_projects_started`는 기존 L-08 내부 기록의 비표시·무수정 결정을 유지한다. 기존 회복 사건 `.3/.13`의 좁은 sync 숨김 수선과 그 한정된 과거 한영 UI 증거도 변경하지 않았다. 동적 정상 참조나 선택적 `_desc` 부재는 새 결함으로 계산하지 않는다.

## 네 런타임 출력의 실제 delta

| 출력 | 기존 분류 | 적용한 변화 | 이전 → 이후 SHA-256 |
|---|---|---|---|
| `common/scripted_effects/HOK_KOR_civic_effects.txt` | ADD | 두 helper의 `add_to_variable`6곳에 `tooltip` metadata·기여 주석2개 | `A114ABEEA79AC284CDEF5D62E0D88DDB232EF5B43BEDA94E4E991923742151DB` → `91F8B01BD60230433F94020F36E445FCF60F384DF400DF72D742BFDB0BB6FEC8` |
| `localisation/english/HOK_KOR_civic_state_l_english.yml` | ADD | 새 키1개·헤더 바로 뒤 영문 기여 주석1개 | `4FFA106AF26D078432DEA853C4B341BE33D3A5E547D63B47A1024274FC1C9EE1` → `C905815621AB3DAC5E48F7372314DC80B2634201A0634D48CDAC46EA11C55779` |
| `localisation/korean/HOK_KOR_civic_state_l_korean.yml` | ADD | 대응 키1개·같은 기여 주석1개 | `546845E0B1F2F997DCDC4EF22EDAE77F6C3024C1A4898B1187DE251346EFC8F7` → `E711FAAD10B71C1A74EF4AB0C201C4306596FD5BECB7DB2565C85925C0448829` |
| `map/buildings.txt` | THREE_WAY_MERGE | 아래 부유항 행1개만 제외, 55바이트 감소 | `0CB4A2ABA190F42D31F732159C77A48732C41B7CFAD5F7E94816242E2D62835D` → `FC70C7C85B9FD8CD9567477C648A80E8F29454EB88D270DE6D189EDB3124BEFA` |

제외한 행은 `1153;floating_harbor;4725.00;9.50;1289.00;-4.47;10065`다. 황해북도 네 province `7070·10065·11915·13560`이 현재 합성 definition에서 모두 내륙이라는 근거에 따라 부적격 표시 앵커 한 개만 제거했다. 인접 주/항구로 임의 이전하거나 현 RT56 원본의 해안 속성으로 포트 definition을 되돌리지 않았다. 실제 엔진 표시·동작의 개선은 별도 관측 대상이다.

새 `HOK_KOR_chaebol_influence_change_tt`는 두 채널 모두 `$HOK_KOR_chaebol_influence$: $RIGHT|=0$`를 사용한다. 기존 언어별 변수 이름을 치환하고 재벌 영향력 증감을 일률적으로 좋음/나쁨 색으로 표시하지 않는 형식이다. 시민·비리·기관 장악의 기존 표시 키를 재사용했다. 명목 증감과 0–100 clamp 뒤 실제 값 차이는 구분하며, 새 형식의 실제 엔진 부호·중립 표시를 아직 PASS로 선언하지 않는다.

## 생성·역투영·원장 통합

- [순수 civic 변환](../../tools/review_followup_content.py)과 [순수 지도 변환](../../tools/review_followup_map.py)은 호출자가 전달한 바이트에만 작용한다. 기록된 helper/행이 없거나 중복·변형된 경우 거부하며 live donor·현재 runtime을 기대값 생성에 사용하지 않는다.
- [최종 후속 생성기](../../tools/review_followup.py)는 [잠금](../../tools/hok_review_followup_lock.json)의 네 경로와 [capsule](../upstream/hok-review-followup-20261109/README.md)의 정확한 선행 바이트에서 결과를 만든다. 이전/새 해시·크기, base Git blob과 Git 원문/checkout 바이트의 역할을 구분한다.
- 기존 최종화 뒤에 **분할 → 11월 콘텐츠 → 새 RT56 host → 이번 수선**을 연결했다. 역사적 검사는 이번 수선을 먼저 정확히 입증·역투영한 뒤 기존 역순 체인을 따른다. 미등록 바이트는 정상 ancestor로 투영하지 않으며 기존 gate가 실패하도록 남긴다.
- [독립 raw 검사](../../tools/check_review_followup.py)는 생성/변환 모듈을 import하지 않고 여섯 metadata·주석, 한영 새 키, 지도 한 행 제거만 허용했는지 확인한다. 별도 현재 지리 확인과 원래 byte 복원도 수행한다. 과거 gate의 projection 통과가 새 출력 자체의 근거를 대신하지 않도록 aggregate에 raw 검사와 결정적 재현 gate를 추가했다.
- 구 builder의 중첩 최종화, Windows 대소문자 별칭, preflight와 이미 최종 상태인 원장의 현재 출력 drift 검사를 통합했다. 구 finalizer에 새 출력이 다시 들어가도 등록 ancestor를 확인한 뒤 같은 terminal 출력으로 돌아가며, 알 수 없는 hash나 중복 물리 경로는 허용하지 않는다.
- [원장 builder](../../tools/build_integration_manifest.py)는 기존 HOK·donor·RT56·번역 귀속을 보존한다. 이번 네 행의 `output_sha256`과 설명의 후속 수선 근거만 바꾸며 다른 행의 원문 바이트를 유지한다. full/scoped 원장 생성에도 같은 말단 변환을 연결했다. 원장 갱신은 기존 source hash를 새 출력값으로 덮어쓰는 작업이 아니다.

## 정적·회귀 확인과 최초 실패

각 검사 단위는 서로 더하지 않는다. 표의 성공은 소스·정적 계약에 한정하며 실제 UI·지급·저장·장기 진행을 입증하지 않는다.

| 확인 | 실제 결과·근거 |
|---|---|
| civic 순수 변환 | **31 PASS / 0 FAIL**. 전체 ordered AST에서 표시 metadata만 제외하면 이전과 같고 기존 locale 값·guard·국유화 바이트를 보존. `<TEST>/content/regression-results.json` |
| civic 최초 시도 | mutation fixture가 파일 전체의 첫 `-10`을 바꿔 무관한 helper를 변형한 뒤 거부를 기대해 실패했다. 대상 길들이기 helper 안으로 fixture를 좁힌 후 위 결과를 얻었다. `<TEST>/content/first-regression-attempt.txt`를 유지하며 생산 결함과 구분. |
| 지도 순수 변환 | **28 PASS / 0 FAIL**, 비대상 map23개 보존·대상 한 행 제외. `<TEST>/map/source-only-map-result.json` |
| 지도 최초 시도 | **25 PASS / 2 FAIL**. 중복 동일 행·동일 주 추가 부유항 후보의 거부 부족을 남겼고, 검사를 무시하지 않고 변환의 입력 유일성 조건을 보강했다. 최초 결과/스크립트는 `source-only-map-result-first.json`·`verify_map_delta-first.py`로 보존. |
| 최종 계층 통합 회귀 | **70 PASS / 0 FAIL**. 기존 잠금3개 byte 보존·네 capsule/rawproof·중첩 finalizer·미등록 hash/대소문자 별칭·원장 네 hash/reason만 변경·메모리 주입 runtime drift 거부. `<TEST>/integration/integration-results-20261109T082158820732Z.json`과 stdout. 저장소 파일을 변조하는 실험이 아님. |
| 11월 결정적 출력 | 기존32출력 보존. `<TEST>/content-integration-after.txt` |
| 독립 11월 내용 | **917 PASS / 0 FAIL / 1 runtime UNVERIFIED**. `<TEST>/content-contracts-after.txt` |
| 기존 분할 생성 | 47출력·15주·6개 이전 ID 및 역사적 계층 보존. `<TEST>/split-after.txt` |
| 독립 새 host | **5,216 PASS / 0 FAIL / 1 runtime UNVERIFIED**. `<TEST>/host-contracts-after.txt` |
| 영어 생성·계약 | 해당 gate 통과. `<TEST>/english-after.txt`. 실제 한영 UI 결과와 구분. |
| 전체 aggregate 최초 수선 뒤 | **23 PASS / 0 WARNING / 13 ERROR**. `<TEST>/aggregate-after-initial.txt`. 기존11개 외에 scoped 원장의 `update_state_split_rows()`가 새 buildings 출력을 기존 분할 hash와 직접 비교해 발생한 두 실패를 식별. |
| 원장 후속 hook 수선 | `update_state_split_rows()`에도 새 exact review 역투영을 연결했다. 자원/분할 scoped 원장의 byte 보존은 `<TEST>/prospecting-after-corrected.txt`·`split-ledger-after.txt`에 기록. 최초 기록 때 최종 aggregate는 진행 중이었으며, 후속 마감 결과는 아래 절에서 구분. |

기존11개 부채와 일시적으로 새로 생긴 통합 실패를 구분하며 최초 결과를 지우지 않는다. 아래 후속 결과와 source-only 한계를 함께 읽는다.

### 후속 aggregate 마감

`aggregate-after-hook-fix.txt`의 완료 결과는 **25 PASS / 0 WARNING / 11 ERROR**, exit1이다. 새 raw 계약·결정적 출력 gate2개가 통과해 작업 전23개에서25개가 됐다. 최초 수선 뒤 발생한 `map/buildings.txt` 원장 역투영 누락의 자원/분할 gate2개도 통과했다.

| 시점 | PASS / WARNING / ERROR | 구분 |
|---|---|---|
| 작업 전 | 23 / 0 / 11 | `aggregate-before.txt` |
| 최초 적용 뒤 | 23 / 0 / 13 | `aggregate-after-initial.txt`. 기존11개와 scoped 원장 신규 실패2개를 함께 보존. |
| hook 보완 뒤 완료 | 25 / 0 / 11 | `aggregate-after-hook-fix.txt`. 새 표시/지도 raw gate2개 통과, scoped 원장 실패2개 해소. |

완료본의 `ERROR`11줄은 작업 전11줄과 문구까지 같다. 남은 것은 feature generic MIO source drift3개 gate, vanilla `map/buildings.txt` 핀2개 gate, shared advisor source1개, East Asia USA peace source1개, 제거된 doctrine source1개, descriptor 보존1개, democratic layout의 `launcher-settings.json` 핀1개, full manifest의 미분류 `.gitignore` exact-path 충돌1개다. 이는 gate 수이며 고유 root cause11개라는 뜻은 아니다. 이 수선이 남긴 새 aggregate 실패는 없지만 기존 부채를 해결하거나 전체 static PASS를 달성한 결과도 아니다.

## 단계별 실행 기록과 후속 종료/복구

실제 사용자 환경을 조작한 실행과 외부 mock session-safety 시험은 다르다. `<TEST>/runtime-preparation/session-safety/`의 거부·rollback 시나리오를 실제 게임 실행 성공으로 계산하지 않는다. 실제 실행/백업/복구의 정본은 `<TEST>/runtime-session/`이다.

| 실행 | 관측한 사실 | 아직 입증하지 않은 것 |
|---|---|---|
| R0 `r0-01` | RT56 단독 영어 GER cold run, PID21308. root가 지도와 `1936.1.2.23` 진행을 보고 정상 종료했다. `runtime-session/runs/r0-01/process.json`, `observations/r0-ger-paused-map.png`, `r0-ger-progressed-paused.png`, `collection.json`에 실행·화면·수집을 분리해 보존. 수집52파일, 새 저장 없음, 원래 저장 차이0. | 포트 수선의 효과·영어 civic 표시·C0/C1·모든 RT56 상태의 정상이나 오류0을 뜻하지 않음. 이 기록에서 로그 원인을 새로 귀속하지 않음. |
| C0 최초 상태 | 최초 기록 시 RT56+호환판 cold run은 진행 중이었다. 뒤의 수집 결과는 아래에 별도 추가. | 당시 지도/unpause·한영 CIV 표시·실제 지급·저장·후보2종 판정은 미확정이었다. |

### R0/C0 cold run 수집 후속

R0 `r0-01`의 독립 수집 로그 검토는 `<TEST>/runtime-log-review/r0-01/FINAL_REVIEW.md`·`baseline-review.json`에 있다. 로그는 HOI4 `1.19.4.2.2da5 (05be)`, DLC36개와 RT56만을 기록하며 설치 버전의 `(0bdb)`와 구분한다. `error.log`는 **666기록 / 631 exact message signature**, 그중 startup **664 / 630**이며 나머지2기록은 `1936.01.02.23` 종료 시점의 같은 `random.log` rename payload다. 오류가 있는 대조군을 무오류로 부르거나 이 숫자만으로 포트 원인을 귀속하지 않는다.

C0 `c0-01`은 영어 RT56+호환판, KOR cold run **PID6840**이며 fixture는 없고 donor/일반판 영어 서브모드는 선택하지 않았다. `process.json`·`launch-intent.json`이 실제 구성·환경·시작을 기록한다. `observations/c0-kor-paused-map.png`와 `c0-kor-progressed-paused.png`에는 KOR 지도 진입 및 시간 진행 뒤 다시 정지한 화면이 있다. 후자의 상단은 `24:00, 1 Jan, 1936`, 일시정지 tooltip의 player 값은 `23:00, 1 Jan, 1936`이므로 두 값을 같은 시각으로 단정하지 않는다. 이 전체 지도 화면은 특정 부유항 앵커의 근접 표시나 CIV 수치·LOC 후보 툴팁을 관측한 증거가 아니다.

C0의 `collection.json`은 `2026-11-09T08:44:53.594230+00:00` 수집, **52파일·새 저장0·원래 저장 차이0**을 기록한다. R0도 각각52파일·새 저장0·원래 저장 차이0이다. 수집 성공과 시간 진행을 저장/재로드·정상 중점 완료·부유항의 모든 기능 또는 전체 세션 복구로 확대하지 않는다. C0 수집 당시 이후 표시/효과 fixture와 최종 복구는 **진행/대기**였으며 뒤의 시점별 결과와 구분한다.

C0의 대조 검토는 `<TEST>/runtime-log-review/c0-01/FINAL_REVIEW.md`와 `comparison-review.json`에 확정했다. C0 로그는 `1.19.4.2.2da5 (19e3)`, DLC36개, RT56+호환판, province13,569개를 기록한다. R0는 `(05be)`·RT56 단독·province13,535개이며 두 실행의 DLC 이름 목록은 같다.

| 실행 | Startup 기록 | 전체 error 기록 | Exact payload signature |
|---|---:|---:|---:|
| R0-01 | 664 | 666 | 631 |
| C0-01 | 667 | 669 | 631 |

**새 exact signature0·제거된 signature0**이다. 기존 `JAP_light_armor_entity`·`JAP_medium_armor_entity`·`JAP_heavy_armor_entity` duplicate message가 C0에서 각각1회 더 발생하며 나머지 발생 횟수는 같다. 이 증가의 직접 원인은 미확정이다. 두 실행 모두 종료 시 `random.log` rename2기록이 있고 C0의 기록 날짜는 `1936.01.01.24`다. small-river graphics payload2개도 서로 같다. C0 `game.log`의 마지막 날짜 `1936.01.01.12`와 root의 화면 시간 진행은 별도 근거다.

네 검토 항목을 겨냥한 오류 검색은0건이지만, 이는 수집한 parser/log smoke 범위에 한정한다. CIV 수치·clamp·once-only, 부유항 앵커 표시, 소양강 raw flag와 sync 과밀은 각각의 화면·실제 효과 확인이 필요하다. 수집52파일 지문 불일치0, 두 실행 입력 로그40개 재읽기 불변과 검토 시 네 수선 출력 지문의 lock 일치도 확인했으나, 이 사후 확인을 모든 파일의 prelaunch binding 증명으로 확대하지 않는다.

### fixture-en-01: 기존 시험 저장 덮어쓰기 사건

영어 fixture cold run **PID8668**은 `1936.1.1.12` 일시정지 지도까지 도달했다. 이 시점에는 fixture의 설정/검증 제어를 실행하지 않았으므로 CIV 실제 효과나 LOC 후보의 UI를 통과시킨 실행이 아니다.

저장 창에서 focus와 재시도 뒤에도 Sky의 `type_text`/키 입력이 반영되지 않았다. root는 `KOR_1936_01_01_12.hoi4`가 없다는 것은 확인했지만, baseline에 이미 있던 실제 임시 저장명 **`KOR_1936_01_01_12_temp.hoi4`**를 놓쳤다. 그 상태의 native Save가 기존 시험 저장을 덮어썼다. 이 실패는 입력 도구의 무응답과 별개로 실제 저장 대상의 중복 확인을 빠뜨린 결과다.

| 단계 | 바이트 | SHA-256 |
|---|---:|---|
| 세션 전 기존 저장·검증된 백업 | 45,571,274 | `E1AAADA62CC1293896E499F55F317785D70F626A177BC07485ECD8385C7C23B7` |
| 덮어쓴 새 fixture 본문 | 79,535,319 | `EFE5DA16DABBC4EADE14752779C1193325823636950DE305441A496871F04692` |

독립 파서는 원래 저장의 차이를 감지해 **본문 파싱 전에 중단**했다. 이 중단을 실제 효과 검사 실패나 완료로 바꾸지 않는다. 사건 초기 대응 당시 root는 사용자에게 알리고 게임의 정상 종료를 요청했으며, 새 본문·사건 receipt 보존 뒤 검증된 백업을 복구하는 한정 helper를 준비했다. 그 시점에는 복구 완료를 주장하지 않았고, 실제 복구 결과는 다음 후속 기록과 구분한다.

이후 기본 날짜12시 저장을 다시 시도하지 않는다. 다음 시험에서는 실제 native 저장 대상과 `_temp` 변형까지 원래 저장 목록에 대해 대조하고, 충돌 없는 명시적 시험 이름이 화면에 반영됐음을 확인한 뒤 저장해야 한다. 새 본문은 원래 파일을 재차 덮지 않는 외부 증거로 보존한다. 후속 복구의 차이0은 복구 결과로 별도 기록하며, 이번 실제 덮어쓰기·최초 차이·차단된 파싱·사용자 통지를 없던 일로 취급하지 않는다.

### 해당 저장 한 개의 검증된 복구·별도 시험 사본 수집

`<TEST>/runtime-session/recovery/fixture-en-01-save-collision-01/`의 `before-recovery.json`은 최초 차이와 새 본문 보존의 사건 receipt다. 같은 폴더의 `after-recovery.json`은 **2026-11-09T08:59:01.467720+00:00**, 상태 **RECOVERED_EXACT_ORIGINAL_WITH_HISTORICAL_COLLISION_PRESERVED**를 기록한다. 원래 `KOR_1936_01_01_12_temp.hoi4`의 **45,571,274바이트·SHA `E1AAADA62CC1293896E499F55F317785D70F626A177BC07485ECD8385C7C23B7`·mtime_ns `1792497343971212300`**를 복구했고, 기존 저장75개 차이는 빈 목록이며 baseline 바이트도 그대로다. 사용자는 이 복구 결과도 전달받았다.

덮어쓴 새 엔진 본문은 `overwritten-new-engine-body.hoi4`로 외부 보존했다. **79,535,319바이트·SHA `EFE5DA16DABBC4EADE14752779C1193325823636950DE305441A496871F04692`**다. root가 명시적으로 선택한 별도 시험 이름 **`HOK_REVIEW_20261109_01_EN_BASE.hoi4`**와 `_temp` 변형이 현재/원래 저장 목록 모두에 없음을 확인한 후, 이 보존 본문을 해당 새 이름에 한정해 stage했다. 이는 새 이름으로 native Save가 성공했다는 증거가 아니며, `staged-owned-test-save.json`의 **2026-11-09T09:00:00.135972+00:00** 영수증에 사전 충돌 확인·원본/사본 관계·해시를 기록한다.

이어 `fixture-en-01/collection.json`은 **2026-11-09T09:00:38.367915+00:00**, 수집53파일·새 저장1개(`save games/HOK_REVIEW_20261109_01_EN_BASE.hoi4`)·기존 저장 차이0을 기록한다. 같은 파일의 `historical_integrity_incidents`는 before/after recovery receipt를 함께 연결하므로, 이 차이0은 사건이 없었다는 기록이 아니다. 이 실행에서는 fixture 제어를 한 번도 실행하지 않았으며 staged BASE를 후속 별도 프로세스에서 검증할 준비만 했다. 당시 root는 다음 `fixture-en-02`를 시작하는 단계였다.

이 결과는 **충돌한 저장 한 개의 복구**와 보존 본문의 독점 시험명 배치·수집에 한정한다. 그 시점의 설정·metadata·선택·소유 `.mod`를 포함한 전체 세션 복구는 대기 중이었으며 뒤의 실제 복구 receipt와 구분한다.

### 새 BASE의 제한된 raw 검토

외부 `<TEST>/runtime-log-review/fixture-en-01/FINAL_REVIEW.md`·`baseline-save-and-log-review.json`과 `<TEST>/save-analysis/EN_BASE-raw-review.json`은 보존·수집한 새 시험 본문만 읽었다. 원래 저장의 본문은 파싱하지 않았다. 선택 검사는 **16 PASS / 0 FAIL**이며 actual effect 이후의 게임플레이 검사나 UI 완료가 아니다.

새 본문은 KOR·`1936.1.1.12`·speed0, 버전 checksum `(a475)`이며 안정된 읽기의 KOR 한정 구간287,126바이트에서 **재벌60·시민35·비리20·기관 장악40**, civic 초기화 flag1, 협력/길들이기 등록 flag 부재를 확인했다. 선택된 HOK 정신은 `chaebol_interfering`·`civic_established`, PP는1.186이다. focus progress1은 있으나 완료 중점 literal은 없으며 그 값에서 진행 기간이나 중점 완료를 추론하지 않는다. fixture 실행 marker도 없어 실제 제어를 실행하지 않았다는 root 기록과 일치한다.

fixture-en-01 로그는 **671기록 / 633 exact payload signature**, startup은 **667 / 630**으로 C0와 같다. 추가 signature2개는 `continue_game.temp`에서 `continue_game.json`으로의 rename과 기본 save의 `_temp`에서 최종 이름으로의 rename 경고(`errno2`)이며, 나머지 발생 횟수는 C0와 같다. 이 경고를 저장 덮어쓰기의 직접 엔진 원인으로 단정하지 않는다. 선택 civic/부유항 parser 오류와 fixture 실행 marker는 없었다. 수집53파일의 해시/크기 불일치0과 비교 입력 로그40개 재읽기 불변은 자료 보존 결과로 구분한다.

### fixture-en-02: 실제 UI 차단과 사용자 수동 닫기 대기

`fixture-en-02/process.json`은 영어 fixture+호환판+RT56의 cold run **PID15380**, 시작 `2026-11-09T09:01:35.159317+00:00`을 기록한다. root는 `1936.1.1.12` 일시정지의 welcome 화면을 보았지만 이 실행에서도 **fixture 제어·저장·불러오기를 실행하지 않았다.** 앞의 staged BASE가 이 프로세스에서 성공적으로 불러와졌다고 기록하지 않는다.

무시되는 게임 키 입력을 조사하기 위해 root는 기존 OSK를 Sky로 열었다. 관측된 OSK 식별자는 PID8512·hwnd2427570이다. 클릭·최소화·Alt-F4 시도는 효과가 없었고, 별도 비UI 종료 경로는 `Get-Process.Path`가 예상과 다르거나 빈 값인 identity guard에서 **`Stop-Process` 전에 예외**로 중단했다. 따라서 그 경로에서 실제로 종료한 프로세스는 없다. Node kernel을 초기화한 뒤 새 Sky 선택과 닫기 재시도도 실패했다.

게임 창 활성화는 정확히 **`failed to activate captured window`**를 반환했고 fresh 목록·선택·명시적 활성화 재시도도 같은 상태였다. Computer Use의 복구 절차에 따라 추가 맹목 입력을 멈췄다. 사용자에게 OSK를 수동으로 닫도록 비동기 요청했으나 이 checkpoint에는 응답이 없으며, 소유 게임이 살아 있는 상태라 정상 종료·수집·복구를 진행하지 못했다. 이것은 게임 수선의 정상 여부 판정과 다른 UI 제어 blocker다.

실제 checkpoint는 `<TEST>/runtime-session/ui-blocked-status-20261109T0915Z.json`에 있다. 파일명의0915는 식별자이며 측정 시각은 본문의 **2026-11-09T09:12:34.803224+00:00**다. 상태는 **UI_BLOCKED_AWAITING_MANUAL_WINDOW_CLOSE**, 소유 게임15380 실행 중, 기존75개 저장의 현재 차이0, 세션 시작 환경 일치, 소유 시험 `.mod` 존재, 최종 프로필 복구 **PENDING_GAME_NORMAL_EXIT_AND_COLLECTION**이다. 최종 aggregate 이후 코드 변경은 없고 두 fixture 모두 제어를 실행하지 않았다는 항목도 기록한다.

따라서 CIV-01의 실제 한영 표시·지급·일회성·저장, LOC-02/03의 노출/과밀 판정은 계속 미확인이다. 구현한 civic·지도 수선은 유지하고 LOC-02/03 코드는 그대로다. OSK 닫기 응답 후 게임 제어 회복·정상 종료·로그/새 저장 수집·전체 설정/metadata와 `.mod` 복구를 완료한 별도 근거가 필요하다. 현재 상태를 작업 완료나 전체 환경 원상 복구로 보고하지 않는다.

위 차단 checkpoint 당시 프로필 복구는 **RESTORATION_PENDING**이었다. 이후 사용자의 판단 위임으로 수행한 종료·수집·실제 복구 결과는 다음과 같으며, 당시 차단 기록을 덮지 않는다.

### 판단 위임 뒤 소유 게임 종료·수집·사용자 환경 복구

사용자의 “너가결정해줘”는 OSK를 수동으로 닫았다는 확인이 아니라 다음 조치의 판단 위임이었다. root는 추가 검증을 억지로 진행하지 않고 소유 시험 게임을 종료하고 사용자 환경을 복구하기로 결정했다. OSK8512의 이름·창 식별자를 확인한 종료 시도는 **Access is denied**로 실패했으며 OSK를 종료하지 못했다.

이어 root는 소유 게임 **PID15380**의 실행 경로와 command line을 확인한 뒤 native **`taskkill.exe /PID 15380`를 `/F` 없이** 사용했다. `runtime-session/runs/fixture-en-02/shutdown-attempt.json`은 **2026-11-09T09:15:08.5101442Z**, 종료 요청과 **`normal_ui_exit_observed=false`**를 기록한다. 명령의 성공은 우선 종료 신호 전달 결과이며, root가 이후 해당 PID의 부재를 별도로 확인했다. 이를 정상 UI 메뉴 종료로 부르지 않는다.

`fixture-en-02/collection.json`은 **2026-11-09T09:16:04.323234+00:00**, 수집53파일·기존 저장 차이0을 기록한다. baseline 대비 새 저장1개는 이전 recovery에서 stage한 **같은 EN_BASE 사본의 누적 보존**이며 이 두 번째 실행에서 native Save나 불러오기를 수행한 결과가 아니다.

독립 검토 `<TEST>/runtime-log-review/fixture-en-02/FINAL_REVIEW.md`·`shutdown-and-log-review.json`에 따르면 이 실행은 `(a475)`·DLC36개·province13,569개이며 `game.log`의 마지막 날짜는 `1936.1.1.12`다. fixture 실행 marker는 없고 root도 실제 제어/저장/불러오기를 실행하지 않았다고 기록했다. 오류는 **669기록 / 631 exact payload signature**, startup **667 / 630**으로 C0의 모든 payload 발생 횟수와 같다. fixture-en-01의 저장/continue rename 두 signature만 사라졌고 새 signature는 없다. 종료 시 `random.log` rename2기록은 남는다. 수집53파일 해시/크기 불일치0, 비교 입력 로그60개 재읽기 불변, 수선 출력4개와 고정 ancestor4개 지문 일치를 확인했다. 이 검토는 full source cache 재검증이나 모든 과거 로드 바이트의 소급 입증은 아니다.

최종 `<TEST>/runtime-session/restoration.json`은 **2026-11-09T09:16:24.245194+00:00**, 상태 **RESTORED**다. 원래 metadata18개를 기록된 바이트·mtime 기준으로 복구해 전부 true, 기존 저장75개 차이 빈 목록, 소유 시험 descriptor 부재, 알 수 없는 새 metadata 빈 목록을 확인했다. 모드 선택은 원래 **일반 HOK donor + 일반판 영어 번역**, `disabled_dlcs=[]`로 돌아갔고 새 고유 EN_BASE 시험 사본은 보존했다. 이는 충돌했던 원래 저장을 복구한 사건 경위를 지우는 “처음부터 불변” 판정이 아니다.

추가 `<TEST>/final-environment-20261109.json`은 **2026-11-09T09:18:09.160465+00:00**에 시작 환경 일치·원래 preparation manifest 불변·게임/launcher 프로세스 빈 목록·소유 descriptor 부재를 확인한다. `<TEST>/runtime-scope-final-20261109.json`은 runtime1,476파일에서 **정확히 네 경로만 변경·추가/제거0·최종 해시 등록값 일치**, 기존 분할/11월 콘텐츠/host 잠금3개 바이트 불변을 기록한다. 최종 aggregate25/0/11 이후 runtime 코드 변경은 없다.

게임·프로필 복구는 완료했지만 **OSK8512 유틸리티 창은 남아 있다.** 접근 거부를 우회해 다른 프로세스를 종료하지 않았으며, 사용자에게 남은 OSK 창은 X로 닫을 수 있음을 알릴 상태다. 이 잔여 창과 미완료 gameplay/UI 검증을 완료 처리하지 않는다.

### 재개 전제

기존 구현·한정 실행 승인은 범위 안에서 유지되며 같은 승인을 반복해 요청할 필요는 없다. 재개 시에는 다음 구체적인 조건을 먼저 충족한다.

- OSK/창 활성화 문제를 해소하고 실제 캡처 대상과 입력 반응을 확인한 뒤 UI 검증을 진행한다. 실패한 창에 맹목 입력을 반복하지 않는다.
- 원래 프로필·75개 저장과 현재 소스/RT56 지문을 다시 읽어 기록하고, donor/일반판 영어 모드를 제외한 승인된 포트 시험 구성을 별도 백업/복구 계약으로 설정한다. 새 RT56/HOI4 드리프트는 별도 평가한다.
- **새 외부 run root에 현재 프로필을 새로 백업해 재개**한다. 기존 `session.start()`는 마지막 collection의 변경된 metadata와 현재 값을 비교하지만, 실제 복구는 그 값을 최초 baseline으로 되돌렸으므로 이전 start를 맹목 재실행하지 않는다. 대안인 명시적 restored-session transition은 별도 검토·구현되지 않았다. 기존 run의 `baseline.json`·`before/`·preparation manifest를 새 값으로 덮어쓰지 않는다.
- native Save 직전에 **최종 이름과 `_temp` 변형 둘 다** 현재 파일/원래 저장 목록에 없는지 확인한다. 입력한 고유 이름이 실제 창에 반영됐는지도 확인하며, 기본 날짜12시 이름을 재사용하지 않는다.
- 검증한 고유 EN_BASE를 실제로 불러왔다면 로드 후 소스·날짜·상태를 따로 입증한다. CIV 두 정치 분기·guard/clamp·한영 표시·지급·저장 왕복, LOC-02/03 후보 판정을 수행하고 정상 중점 진행과 강제 진단을 구분한다.

현재 결론은 **두 소스 수선 적용·정적 계약 확인·R0/C0 한정 smoke·사용자 프로필 복구 완료**, **실제 수치 UI/효과/저장과 LOC 후보는 차단으로 미검증·OSK 창 잔존**이다. 네 항목 전체 완료·전체 무오류·기존 저장 호환성은 주장하지 않는다.

## 남은 확인과 산출물 경계

- CIV-01A/B는 서로 다른 정치 경로에서 한영 표시·등록 전/후·수치 경계와 실제 변수/국민정신·일회성·필요 저장을 확인한다. 강제 helper 호출과 정상 중점 완료를 구분한다.
- MAP-01은 동일 RT56 대조와 포트의 실제 지도/부유항/인접 항구·unpause·관련 오류를 비교한다. 단일 표시 앵커 제거를 기존 저장의 지도 변환이나 gameplay 동일성 보장으로 설명하지 않는다.
- LOC-02/03은 먼저 실제 화면으로 수정·유지·제외·미확인을 결정한다. 관측 전 예상만으로 표식 이름이나 광범위한 sync wrapper를 추가하지 않는다.
- 새 저장 왕복과 변경 전 저장 호환, 합성 seed/강제 효과와 정상 진행, UI와 실제 지급, 다른 DLC·장기 AI·멀티플레이를 구분한다. 기존9주 저장 변환은 이번 수선에 포함하지 않는다.
- 외부 근거 루트와 source capsule은 역할이 다르다. 유지할 `docs/upstream/hok-review-followup-20261109/before/` 네 파일은 source 입력이며 테스트 폐기물이 아니다.
- 기존 `tools/__pycache__/`의21파일·`1,088,888`바이트는 정리 미결 자료로 보존한다. 이번 실행 도구는 새 cache를 저장소에 만들지 않도록 했으며 기존 자료를 이동·삭제하지 않았다. 실제 파일 목록·생성 시점까지 재분류한 기록으로 확대하지 않는다.

이 checkpoint까지 커밋·푸시·게시·업로드는 수행하지 않았다. 이후 재개 결과는 위 미검증·OSK 잔존과 저장 사건을 보존한 상태에서 추가한다.
