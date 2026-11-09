# 2026-11-08 국토개발·표시·참조 업데이트 이식

작성: 2026-11-08, 최종 기록: 2026-11-09, Asia/Seoul. **선택 HOK32개·호스트4개 반영 / 한정된 실제 실행 관측·수집 / 세션 복구·보존 감사 완료**. 검증하지 않은 범위와 기존 정적 오류11개는 아래에 남기며 전체 호환성이나 배포 준비 완료를 뜻하지 않는다.

## 범위와 현재 기준

사용자는 [계획](../plans/2026-11-08-hok-upstream-content-port-plan.md)을 설명받은 뒤 `AGENTS.md, /docs 읽고 구현해줘`로 구현을 승인했다. 실제 검증을 위한 프로필·모드·언어·자동저장·시험용 `.mod` 임시 변경과 게임 실행도 별도로 승인했다. 기존 작업 트리의15주 분할을 보존하며 커밋·푸시·게시·업로드는 하지 않는다.

이 계층의 코드·입력·영토·저장 계약을 수정하기 전에 [ADR-0007](../decisions/0007-november-content-integration.md), [ADR-0006](../decisions/0006-korean-state-split-integration.md), [입력 안내](../upstream/hok-content-update-20261108/README.md), [잠금](../../tools/hok_upstream_content_lock.json)을 읽는다. runtime 검증을 확대할 때는 [계획의 검증 계약](../plans/2026-11-08-hok-upstream-content-port-plan.md#9-후속-검증-계약--전부-미실행-계획)과 [프로젝트 지침](../../AGENTS.md)을 따른다.

| 항목 | 시작 기준 |
|---|---|
| 호환판 | `C:\hoi\hearts_of_korea_Road_to_56`, `feat/korean-focus-update-20260922@3d9355b70152794ed974dcf183323c24206d900a`, 기존 분할·도구·문서의 미커밋 변경 존재 |
| donor | `C:\hoi\hearts_of_korea`, `feat/korean-focus-expansion-ai@596b221bb994d93fce552d3ee1ba70fa9b5640f1`, clean |
| 설치 | Steam build26409260, RT56 설치/상세 manifest7553774178744855191. 실제 프로세스별 엔진 버전·체크섬·DLC·언어는 아래 실행 기록과 구분 |
| 물리 host | `C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968`와 게임 설치. 읽기 전용 |
| 사용자 데이터 | `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV` |
| 시작 모드 선택 | `enabled_mods=[]`, `disabled_dlcs=[]`. 기존 hoi4/launcher 없음, 기존 Steam은 유지. 임시 시험 선택과 구분 |
| 시작 설정 | 한국어·1280×720·GUI1.0·반년 자동저장·binary save. 실제 시험 전 원래 파일을 다시 백업하고 종료 후 복구 |
| 외부 작업 | `C:\hoi\test\hok-rt56-upstream-20261108-01\` — 아래 `<TEST>` |

## 구현과 보존

원본36후보를 기준으로 **기존 경로13개 변경 + 신규19개 = 32출력**을 고정했다. 출력 경로·해시·생성 소유권은 잠금의 `outputs`가 기준이다. 원본의36후보와 출력32개의 집계 차이는 일반 CHI 수선1·MON 제외1·이미 적용된 연구망 한영2개를 유지한 결과다. donor 전역 소스2개는 같은 이름을 복사하지 않고 다른 상대 경로의 전체 호스트 병합2개로 대응한다.

| 모듈 | 실제 적용 내용 | 보존·남은 경계 |
|---|---|---|
| [CNDP 생성](../../tools/upstream_cndp.py) | 기존 결정/한국 중점/KOR history3개와 trigger·GFX·한영 locale·DDS13개 추가 | 새13개와 구형7개 분리, 비용75/150·기간90/180·민공5·주별 완료1회. 기존15주 지도·시작 산업·474중점 보호 필드 유지 |
| [civic 표시](../../tools/upstream_civic_display.py) | 기존7경로의 metadata29·sync8·paired15키·교육 설명1키 | 변수/효과/조건/365일 수명과 L-08 명령 보존. `.3/.13`은 실제 화면 확인 전 원문 유지 |
| [지리 연결](../../tools/upstream_state_references.py) | 한국/일본/결정/사건/KCH5개와 host 병합2개 | 해주·쓰시마·KCH 수도1114·일본/아시아 목록·FRI 수락 guard·SOV/코민테른 함북1152. 일반 CHI/JAP·MON 정책 보존 |
| [최종 생성기](../../tools/upstream_content_update.py) | 이전 포트 입력에 세 모듈을 순차 적용하고 최종 해시 검사 | live donor·가변 production을 기대값으로 삼지 않음. 기존 source pins를 유지한 정확 해시 역투영·소유자별 재생성 |
| [독립 소스 검사](../../tools/check_upstream_content.py) | donor 배분 JSON/명시적 지리 대응/기존 포트·host AST로 조건·보상·보호 필드 비교 | 변환 모듈을 기대값 생성에 호출하지 않음. UI·기간 경과·실제 효과·저장은 정적 통과로 대체하지 않음 |

전체 CNDP 배분표는 계획5절의 실제 port state/province 대응을 유지한다. 특히 동해 province1148을 경남 state1148로 치환하지 않는다. 전역 건설 상한·카테고리 정의는 바꾸지 않았고, 부지 전용3종의 보수적 여력 판정 제한도 보존한다.

KOR 인도차이나 경로의 FRA/FRI 적응과 지연 수락 재검사, Singapore336 조건부 이전·이미 MAL 소유 Penang/Kedah914 유지는 ADR-0007의 명시적 포트 결정이다. 단순 번역 변경이나 모든 상태에서 동작 보존이라고 기술하지 않는다.

## 출처·생성 소유권

`docs/upstream/hok-content-update-20261108/`에 donor36·문서13·기존 포트 입력16+L08 보호1·host2·이전 원장을 별도 역할로 보관했다. `source-manifest.json`과 잠금은 원본/사본·Git blob/raw/checkout·물리 host·기존/최종 출력 해시를 구분한다. 기존47출력의 입력·잠금·활성 캐시는 그대로다.

같은 상대 경로의 SOV host 파일은 SHA-256 `B9D5AC00450D561069C15E664A78DBCFF38D7D43F2F441F3CCE5572586BC82CD`, vanilla state_groups는 `7B920231ED30F856E4BF8503C50115BBD961176E72465DEB2859FAC6EC4757B9`를 기준으로 한국 항목만 변환했다. 원본·host 전체 파일의 기존 기여는 유지한다. 신규 DDS13개는 원본과 바이트 동일이며 기존 그림·색·공유 sprite는 바꾸지 않았다.

이전 generator/checker는 새 최종 바이트의 해시가 정확히 일치할 때만 기존 조상으로 역투영한다. 실제 최종32개는 별도 raw gate와 독립 계약 검사로 확인한다. 기존 전체 gate의 source mismatch를 없애려고 옛 핀을 새 해시로 바꾸지 않았다.

## 이번 정적 확인

| 확인 | 결과와 한계 |
|---|---|
| 수정 전 aggregate | `19 PASS / 0 WARNING / 11 ERROR`. 과거 source drift·descriptor 부채로서 새 변경 전 결과를 `<TEST>/checks/baseline-aggregate.*`에 보존 |
| 새 생성기 | `32`개 고정 출력 재현·실제 디스크 일치, exit0. `<TEST>/checks/content-outputs.*` |
| 독립 소스 검사 | 파서 회귀 수선 후 실제 디스크 **913 PASS / 0 FAIL / 1 runtime UNVERIFIED**. `<TEST>/checks/independent-content-fixed.*`가 현재 결과다. 초기 변이37개는 `validation/independent-upstream-mutation-review.json`, 후속 전역 중복2개는 `validation/independent-global-registry-followup.json`, option 조건키 회귀1개는 `validation/option-trigger-regression-source-review.json`에 각각 보존한다. 서로 다른 시점의 결과이며 UI·효과 통과 수가 아님 |
| 모듈 단위 | CNDP unit10/0, civic 보존62/0, 지리 연결51/0. 초기 helper 실패/정정은 같은 외부 디렉터리에 보존하며 최종 성공으로 지우지 않음 |
| 기존47출력·ID 이전 | `korean_state_split.py --check`, `migrate_hok_ids.py --list` exit0. 후자는 기존 일부 파일의 newline 정규화 제안을 기록하지만 적용하지 않음 |
| 영어 | `source_snapshot.py --english-check` exit0, 기존 영어·연구망 계약 유지. 새 CNDP pair·표시15키는 독립 검사에서 별도 확인 |
| 원장 | `build_integration_manifest.py --check --state-split-only` exit0. 기존 행과 새32개 출처를 고정 입력에서 재현 |
| 지도·무수정 보호 | map/history24개와 L-08 동맹 산업지원 파일의 기존 해시 보존 |
| 수정 후 aggregate | **21 PASS / 0 WARNING / 11 기존 ERROR**. `<TEST>/checks/aggregate-after.*`에 별도 보관하며 신규2gate 통과와 기존11개 오류를 구분한다. 전체 오류 해소나 런타임 완료가 아님 |

## 실제 실행 — 승인 후 진행 상태

### 처음 실행에서 드러난 파서 회귀와 최소 수선

R0 영어 GER1936 대조는 PID2876, 21:45:08 KST에 시작해 실제 UI에서1936.2.11.11까지 진행 후 정상 종료했다. 엔진은 `1.19.4.2.2da5 (7772)`, DLC36개, RT56 단독, province13,535개다. 로그34개·새 저장0개·기존61개 저장의 내용/mtime 차이0을 수집했다. 대조 자체에도 장비/GFX·미정의 trigger·GXC scope 등의 오류가 있으므로 전체 무오류 대조라고 부르지 않는다.

첫 C0는 PID23684, 21:53:27 KST의 영어 KOR/fixture 없는 cold run이다. `41da`, province13,569개로1936.1.1.12 화면까지 진입했으나, 이번에 추가한 `kor_events.62.a`의 **`available` 조건이 불법 effect로 해석되는 새 파서 오류2행**을 재현했다. 당시 소스 해시와 로그는 `<TEST>/session/runs/c0-01/`에 보존했다. R0에 없는 이 두 exact 서명을 이번 회귀로 판정하며 초기51개/912개 정적 성공이 엔진 문법 적법성을 증명하지 못한 한계를 남긴다.

현재 버전의 vanilla `AAT_Generic_Events.txt:307–309`, `AAT_Denmark.txt:2581–2583`의 같은 option 문맥은 `trigger`를 사용한다. 참조 생성기의 새 선택지 조건키 **한 곳만 `available → trigger`**로 바꾸고 효과 직전 `if/limit` 재검사는 유지했다. `events/korea.txt`의 첫 출력 SHA-256 `22884A92F1D3D0D98363D726864C528D70F2C56CFD38AD388FCB4AC7FF1A5C07`과 수선 후 `4A955AEE3AA00759FBBD0A8FC0411342B7E01A7FE6B103C09B80798F3B5BA78E`를 구분한다. 잠금의 원래15주 `previous_sha256`은 유지하고 실패한 첫 출력을 명시적 `accepted_previous_outputs`/`revision_history`로 기록하여 이 한 파일을 검토된 새 출력으로만 이전했다. 실패 바이트·이전 잠금·한키 차이 검토는 `<TEST>/repairs/option-trigger-v1/`에 있다.

독립 검사에도 option 직속 `available`을 거부하는 별도 gate와 해당 회귀 변이를 추가했다. 수선 후 실제 디스크 소스 검사는 **913 PASS / 0 FAIL / 1 runtime UNVERIFIED**다. C0-01을 종료·수집하고 기존 저장61개 변경0을 확인한 뒤 C0-02(PID22192,22:04:14 KST)를 새 프로세스로 시작했다. 사전1,704개 지문 차이0, 엔진 `31a4`·DLC36·실제 모드2개·province13,569개 및 script 로드 단계에서 회귀2서명 부재를 관측했다. 해당 시점의 파싱 관측을 후속 UI·효과·저장 결과로 확대하지 않는다.

### 후속 동작·표시 검증

C0-02는 한국 영어 지도/중점 트리와 CNDP13개 해금 툴팁을 확인하고 실제1936.1.13.06까지 진행한 뒤 정상 종료했다. 로그34개와 기존61개 저장/백업의 SHA 일치를 수집했다. 최종 오류는5,882 records/813 unique이며, 새32경로·선택 심볼 관련 서명과 수선한 `available` 오류는0이다. R0에 없던 GXC 인물/국가 조합2종은 기존 scope 오류 계열과 인접하지만 신규 콘텐츠와의 인과는 미확정이다. 이 결과는 아래 자동 갱신 **전755 manifest**에만 귀속한다. 세부 검토는 `<TEST>/runtime-log-review/c0-02-final-collected-20261108T132651UTC/`에 있다.

실행 직전 원래 설정·선택·저장·로그의 사본은 `<TEST>/session/session-before/`, 세션 기준과 실행 상태는 `<TEST>/session/baseline.json`·`<TEST>/session/active-session.json`, 실행별 PID·체크섬·관측·수집 증거는 `<TEST>/session/runs/<run-id>/`에 둔다. `<TEST>/runtime-session/`은 `session.py`·관측·요약 driver의 위치다. 이전 본문의 증거 인덱스 경로 표기를 정정한 것이며 파일을 이동한 작업은 아니다. 위 R0·C0 기록 이후의 동작·표시 결과와 종료·복구 상태는 실제 증거가 수집된 뒤 별도로 기록한다.

`<TEST>/runtime-preparation/fixture/`와 RUNBOOK은 CNDP full13·취소/재착수·전시 한 province 상실·합성 구형 분기·슬롯 matrix·저장 snapshot의 **준비 자료**다. root가 최종 생산 payload46개 및 trigger 일치를 확인한 뒤만 등록한다. synthetic focus/기술/민공과 native 강제 활성화는 일반 UI 착수·정상 정치 경로·이전 저장 지원으로 기록하지 않는다. 사용자 기존 저장을 덮어쓰지 않는다.

최소 필요한 실제 범위는 정상 UI/비용 경계·90/180일 만료·점유 반환·소유/부분통제 상실 취소·복구 재착수·완료1회·슬롯전용3종·한영 숫자/선택지·새 저장 cold reload다. 기존15주 저장의 미착수/진행/완료, 지연 외교 수락·SOV 정리·실제365일 경과·다른 DLC·장기 AI·멀티플레이는 각각 실제 관측 전 미검증으로 남긴다. RT56의 이전1939 미지원 관측도 별도이며 bookmark를 바꾸거나 날짜를 강제하지 않는다.

## 실행 도중 RT56 자동 갱신과 승인된 새 기준

Steam 로그에서22:20:17 새 RT56 감지,22:20:53 다운로드 시작,22:21:27 완료를 확인했다. manifest가755에서 **1963361040482473746**으로 바뀌었으며 설치 원본에 대한 이 작업의 쓰기나 업데이트 명령이 원인이 아니다. 사용자가 원인을 확인한 뒤 “새 RT 56에 맞춰서 대응하자”라고 명시 승인하여 새 호스트 대응을 계속한다.

같은 선택 수집 범위에서184개 변경·8개 삭제·25개 신규이며, 포트와 겹치는4경로는 북마크·generic MIO·SEA on_action·JAP history다. 전체28,746파일·1,373,729,636바이트 감사 사본과 전후 SHA/경로/크기 검증을 `<TEST>/host-drift/`에 보존했다. 이전4,806 지문은 전체 RT56 목록이 아니므로 미수집 경로를 신규로 판정하지 않는다. 이전 aggregate21/0/11과 별개로, 갱신 직후 재실행한 aggregate는 **15 PASS / 0 WARNING / 17 ERROR**이며 `<TEST>/checks/aggregate-after-option-repair.*`에 보존한다. 새 host drift와 이전 부채를 덮어 통과시키지 않았다.

[ADR-0008](../decisions/0008-november-rt56-host-update.md)과 [새 입력 안내](../upstream/rt56-host-update-20261108/README.md)에 따라 한국32개 뒤에 호스트4개를 별도 합성했다. 이전47/32의 잠금을 보존하고 등록된 해시 쌍/manifest 전환만 허용한다. 한국32·지도24·L-08은 일치하며, 동결755 중간 입력2개를 사용한 이전47출력의 해시 재현도 불일치0이다. 새4출력 preview 독립 검사는5,210 PASS/0 FAIL/1 runtime UNVERIFIED이며 실제 디스크와 실행 검증 결과는 따로 기록한다.

호스트 대응과 검토된 WTT 입력 연결 뒤의 실제 aggregate는 **23 PASS / 0 WARNING / 11 ERROR**, exit1이다. 근거는 `<TEST>/checks/aggregate-new-host-after-wtt-bridge.json`·`.txt`다. 앞의21/0/11과 갱신 직후15/0/17은 각 시점의 기록으로 보존하며, 현재도 남은 source drift·descriptor 등11개 오류를 전체 해소했다고 주장하지 않는다.

이전 세션은 설정·선택·continue/career를 복구했고, 원본 nonlog/nonsave62개와 기존61개 저장, root/career 파일 목록의 차이가0이다. 임시 descriptor가 없고 Steam의 녹색 플레이 버튼을 확인했다. 증거는 `<TEST>/session/restoration.json`, `restoration-full-profile-audit.json`, `restored-ui/`다. 이어 새 manifest 전용 `<TEST>/new-host-session/session/`에 원본157개·기존 저장61개를 포함한4,614,964,282바이트의 별도 백업을 만들었다. 새 driver는 `<TEST>/new-host-session/driver/session.py`이며 구 세션을 수정하지 않는다.

새 호스트의 R0·C0·fixture-01·fixture-02는 종료·수집했다. 다음 기록은 manifest196 전용이며 이전755 실행의 체크섬·오류 서명·단축 통과를 재사용하지 않는다. 실행 원본은 `<TEST>/new-host-session/session/runs/<run-id>/`, 읽기 전용 로그 검토는 `<TEST>/new-host-session/runtime-log-review/`에 보존한다.

새 R0(`r0-01`)는22:40:02 KST, PID21024, 엔진 `1.19.4.2.2da5 (05be)`로 RT56 단독 GER1936을 시작해 실제1936.3.13.05까지 진행하고 정상 종료했다. DLC36개·province13,535개, 로그34개 수집 사본의 크기/SHA 일치와 기존 저장61개 변경0·신규 저장0을 확인했다. 최종 오류는 **669 records / 634 exact unique**로, RT56-only에도 존재하는 그래픽·역할·descriptor·종료 rename 등의 기준이다. 전체 무오류를 뜻하지 않는다. 증거는 `<TEST>/new-host-session/session/runs/r0-01/`과 `<TEST>/new-host-session/runtime-log-review/r0-01-final-collected-20261108T135544UTC/BASELINE_REVIEW.md`다.

새 C0(`c0-01`)는22:53:43 KST, PID21120, `(45ab)`로 RT56+호환 포트2개·DLC36개·province13,569개를 로드했다. fixture·console 없이 원래7일 중점의 실제 UI 착수·완료와1936.1.27.23 도달을 확인했고, 이후 새 시험 BASE를 **인게임 재로드**하여1936.1.1.12/PP1로 복귀했다. 이는 새 프로세스 cold reload 증거가 아니다. 저장 시 `continue`와 새 저장의 rename errno2가 발생해 실제 남은 `_temp`를 사용했으며, 재로드 때 `PRC_luo_ruiqing` advisor 오류18행이 발생했다. 최종 **690 records / 651 exact unique**, 첫 R0에 없는 정확20종은 이 rename2종과 저장 행번호별 PRC18종이다. 당시에는 별도 R0 저장/재로드 대조가 없어 HOK 변경과의 인과가 미확정이었으며, 후속 R0-02 대조는 다음 문단에 구분한다. 새36출력 경로·선택 심볼 관련 오류0, 실제36출력 해시 불일치0이며 로그34개와 원본/백업 저장61개의 크기·SHA가 일치했다. 세부 증거는 `<TEST>/new-host-session/session/runs/c0-01/observations/baseline-save/manifest.json`, 같은 실행의 `screenshots/native-focus-completed-paused.png`·`baseline-reload-observation.png`, `<TEST>/new-host-session/runtime-log-review/c0-01-final-collected-20261108T143050UTC/FINAL_REVIEW.md`다.

후속 `r0-02-reload`는 포트 없이 RT56 단독·영어 GER·DLC36·13,535 province·`(05be)`로 같은 실행에서 저장하고 재로드했다.1936.1.1.12/PP2 유지와 정상 종료를 관측했고, 안정성을 두 번 확인한 Python 사본의12개 파일 hash 및 before→save→reload→최종 byte prefix를 독립 대조했다. 저장 직후 rename2개, 재로드 뒤 random rotation1개와 `PRC_luo_ruiqing` advisor 경고18개, 종료 때 rotation2개를 기록했다. 최종687기록/651고유는 초기664+저장rename2+PRC18+rotation3이다. GER 저장 이름과 near line522799–523904는 KOR 저장과 다르므로 원문 전체가 같다고 하지 않으며, 파일명·near line만 정규화한 경고군이 C0/fixture01/fixture03과 일치한다. **포트 없는 RT56 단독 재현은 CONFIRMED**, 새 HOK 콘텐츠만이 유일한 원인이라는 설명은 **DISPROVEN**이다. 엔진·RT56·저장 writer 중 근본 원인은 미확정이다. 로그34개·원래 저장61개·백업61개·세션 누적 새 저장7개와 사본의 불일치는0이고, 초기 PowerShell sharing/stable 실패 사본은 안정성 근거에서 제외했다. 근거는 `<TEST>/new-host-session/runtime-log-review/r0-02-reload-final-collected-20261108T171048UTC/{FINAL_REVIEW.md,reload-control-and-integrity.json}`이며 최종 프로필 복구 증거는 아니다.

`fixture-01`은23:30:20 KST, PID14180으로 시작한 별도 cold run이다.23:33:59의 초기 관측은 `(5055)`·fixture+RT56+호환 포트3개·DLC36개·province13,569개·1936.1.1.12, **667 records / 630 exact unique**이며 새 R0/production C0에 없는 정확 서명0이다. 그 시점의 fixture prefix 관련 parser/unknown effect/trigger 오류0은 초기 로드 관측일 뿐 수동 helper·17개 버튼·관측 getter 실행 통과가 아니다. 근거는 `<TEST>/new-host-session/runtime-log-review/fixture-01-live-interim-20261108T143359UTC/INITIAL_REVIEW.md`와 같은 디렉터리의 실제 fixture 경로/해시를 기록한 `fixture-attribution.json`이다.

23:47:03에 보존한 `<TEST>/new-host-session/session/runs/fixture-01/observations/native-ui-prefix-01/prefix-manifest.json`은 첫 `native_ui_full` 시도의 안정된167행 prefix를 기록한다. 관측 시작은 `active13=0 / successes=0`이며 첫 일일 tick에서13개의 `NATIVE_DECISION_ENDED`가 기록됐다. root가 보고한 갱신 실패 시도로 분류해 **실제 UI 13개 착수·비용·완료 성공에서 제외**한다. 이 prefix에는 두 번째 시도가 없으며, `ENDED`는 비활성 첫 관측이므로 완료 보상을 뜻하지 않는다. 원래 실패 로그를 유지하고 후속 시도와 분리한다.

### 유효한 두 번째 착수와 활성 저장 후속

fixture-01의 두 번째 시도는 BASE 재로드 뒤 UI201 합성 조건만 준비하고, 실제 공장/결정 갱신을 위해1시간 진행한 후1936.1.1.13에 일시정지했다. 원래 로그169행의 별도 watcher부터13개 **원래 UI 결정의 실제 클릭**과 같은 시각의 활성13·성공0을 확인했다. 정치력2000→950의 합계1050 소비와 프로젝트 가용 민공 getter102→37의65 감소를 전후 snapshot으로 대조했다. 이는 원래 BASE 정치력에서의 차이도, 강제 활성화 `.1`의 비용 가정도 아니다. 보존된 활성 저장은 원래 queue13개(90일12개·180일1개), 정치력950·완료 표식0을 담는다. UI factory 총수나 저장의 construction 보고 counter를 점유 민공으로 동일시하지 않는다. 근거는 `<TEST>/new-host-session/session/runs/fixture-01/observations/active-save/verification-summary.json`·`root-native-ui-attestation.json`과 `<TEST>/new-host-session/runtime-log-review/fixture-01-final-collected-20261108T145714UTC/FINAL_REVIEW.md`다. 앞의 첫 실패16–168행은 그대로 제외한다.

별도 cold process `fixture-02`에서 이 활성 저장을 로드해 실제 UI의 활성13개 타이머를 확인하고 정상 시간 진행으로 원래90/180일 queue의 종료를 관측했다. 첫 일일 비활성 관측은1936.4.1.24/tick91에12개 성공·강원1개 활성,1936.6.30.24/tick181에 활성0·성공13이다. 일일 observer의 첫 비활성 시각을 정확한 만료 순간이나 달력 산술 검증으로 확대하지 않는다. 당시 snapshot의 가용 getter는98, 이후103이며 일자·경제 상태도 바뀌었으므로 시작 때의37과 단순 차감해 개별 점유 반환량으로 확정하지 않는다. 증거는 `<TEST>/new-host-session/session/runs/fixture-02/screenshots/cold-active-all13-timers.png`·`after-native-90-day-completions.png`·`after-native-180day-completion.png`와 같은 실행의 `observations/normal-completion-log/`·`partial-completion-save/`·`completed-save/`다.

후속 독립 원시 검토는 `<TEST>/new-host-session/analysis/native-completion/literal-series-comparison.json`의 **18 PASS / 0 FAIL**, `reward-payload-contract-comparison.json`의 **163 PASS / 0 FAIL**로 선택된 직렬화 필드와 고정 native 보상 계약의 일치를 확인했다. category의 기본 슬롯 lookup 증가11과 extra 슬롯7·석탄5·VP11의 선언 효과량을 해당 저장 필드와 대응했다. 이전 필드가 저장에 없으면 절대값0을 대입한 차분이 아니라 새 직렬화 payload의 일치로 기록하며, 명시된 기존 VP6944의1→2 같은 실제 차분과 구분한다. 고정 시작 history는 `separate-pinned-history-layer.json`의 별도 의미 계층이고, 실제 저장의 누락 값을 대신하지 않는다. 실제 유효 건설 용량·절대 원시 석탄/VP 총량·누락된 점유량은 이 수치로 확정하지 않는다. `normal-progression-log-comparison.json`은 정상 진행 관측과 복사 probe 경계를 별도로 고정하며, fixture-03 전환 후 잘못 복사한47바이트 로그는 fixture-02 근거에서 제외했다.

자연 종료 뒤1936.8.1.16에 실행한 `.98`은 전라북·경상북의 **복사된 완료 보호 두 개를 재호출하는 별도 probe**다. 로그811행의 `COPIED_COMPLETION_GUARD_ONLY_NOT_NATIVE_TIMER` 이후를 자연 종료 구간과 분리하고, 완료 저장과 `observations/completion-guard-save/` 사본을 보존한다. `done-vs-guard-comparison-v2.json`은 **46 PASS / 0 FAIL**이며 같은 일시정지 시각의15주 전체 state block SHA와11개 VP 필드가 동일하고, 정치력1204.612·버전 표식·빈 native queue가 유지됨을 확인했다. 이는 관측한 복사 guard 호출 전후의 선택 보상 중복 부재이며 원래 타이머의 두 번째 만료나13개 전체의 반복 callback 검증은 아니다. 저장된 speed 값을 pause boolean으로 잘못 요구했던 첫 검사 결과도 원래 보고서와 함께 보존한다.

### 별도 V2 준비와 남은 실행 경계

`<TEST>/runtime-preparation-v2/`는 실행 중이던 V1을 수정하지 않고 만든 별도 외부 준비본이다. fixture17파일+launcher1개를18항목 manifest에 고정했고, 기존9 payload 바이트·17버튼 AST를 보존한 뒤 refs10·boundary12를 합쳐39버튼/2범주/채널별86키를 구성했다. 두 TEST ONLY 범주에만 target vanilla 근거의 priority100을 추가했다. 원래 production payload46개·trigger pin을 유지하는 V2 전용 `check_final_production.py`는 **243 PASS / 0 FAIL**, 등록 해시까지 바꾼 메모리 변이8/8 탐지·보존82/0이며 독립 읽기 검토에서도 중요한 blocker가 없었다. 이는 소스/AST 검사이며 신규 버튼·국가 scope 호출·UI 배치 실행 통과가 아니다. 근거는 같은 디렉터리의 `preparation-manifest.json`, `final-production-payload-check.json`, `validation/v2-source-mutation-preservation.json`, `RUNBOOK.md`다.

root는 기존 새 호스트 driver를 `<TEST>/new-host-session/driver/session_v2.py`로 별도 복사해 PREP 경로만 V2로 바꿨다. 같은 부모 세션과 원래 백업을 유지하며, 원본 driver와 V1은 불변이다. 이 한 변경의 원본/사본 SHA는 같은 driver 디렉터리의 `v2-driver-provenance.json`에 있다. V2를 사용한 f03의 확인 범위는 아래 종료 기록으로 구분한다. NoC3 seed는 기존 UI201과 함께 쓰지 않는 별도 합성 경로이고,97/96 예약 idea는 실제102 기준과 갱신 후5/6 getter를 관측하기 전 명목값일 뿐이다.

f03의 negative/partial/legacy/slots 관측을 섞지 않도록 `<TEST>/new-host-session/analysis/scenario-phases/phase_logs.py`와 source contracts를 별도 준비했다. 같은 폴더의 README 절차에 따라 `<TEST>/new-host-session/session/runs/fixture-03/observations/cndp-phases/` 아래 매번 새 UTC 경로에 game/error 전체 prefix·SHA를 보존하고, 모든 `SCENARIO_START`를 경계로 원래 행 번호·시도별 범위를 기록한다. 실제 전체 UI reader는 호출하지 않으며 미시작·현재 prefix·날짜 역행을 분리하고 원시 오류를 특정 phase에 잘못 귀속하지 않는다. source byte 판독18/0은 도구 준비 검증으로서 해당 시나리오의 실제 결과가 아니다.

V2의97 예약 idea 실험은 **SETUP_NOT_AT_TARGET**로 남긴다. `<TEST>/new-host-session/runtime-log-review/fixture-03-live-interim-20261108T160632UTC/boundary-phase-evidence.json`의79–80행은 `hold97=1 / available102 / civ158`,82행은 시간 진행 뒤 `hold97=1 / available103 / civ159 / C3=1 / native0`을 기록한다. 제안했던 가용5에 도달하지 않았다는 관측이며 생산 결함이나 모든 idea modifier의 일반적 무효로 판정하지 않는다. 당시 파일·로그와 엄격한 V2 소스243/0은 변경하거나 완화하지 않았다.

승인된 검증 범위에서 `<TEST>/runtime-preparation-v3/`에 V2 전체 준비 파일61개를 동결하고 별도 최소 역외 민공 시험본을 조립했다. 기존 runtime17·39버튼 AST·46 production payload·61 production pin과 입력 provenance를 보존한 뒤, 새 `HOK_RT56_UPSTREAM_OFFSITE` namespace의 숨김 수동4사건과4버튼만 추가했다. V3는 fixture18+launcher1의19항목 manifest·43버튼·3범주·채널별96키다. 새 seed는 중점/C3/PP/자체 ledger0만 준비하고150 공장이나 idea를 지급하지 않는다. ±1은 이전 UI201/NoC3 seed와 활성20프로젝트를 배제하며 자체 요청 순증0–4 안에서만 허용한다. ledger는 실제 가용량의 원자적 증명이 아니다. 기존 V2 검사 원문을 읽기 전용으로 호출하는243/0을 포함해 V3 소스475/0·변이9/9 탐지·보존122/0을 기록했다. 구체 입력/출력 SHA·등록 후보·한국어 버튼 절차는 같은 V3 디렉터리의 `preparation-manifest.json`, `validation/v3-source-mutation-preservation.json`, `registration-candidate.json`, `RUNBOOK.md`에 있다. 이 준비는 V2·driver·프로필·게임·생산 파일을 수정하지 않았다. V3 준비 당시 실제5·6은 미관측이었으며 이후 V4/f04의 실제 결과는 아래에 별도로 기록한다.

### fixture-03 종료와 확인 범위

**f03는 정상 종료하고 로그34개를 최종 수집했다.** 원래 저장61개와 백업61개·누적 시험 저장6개 및 수집 사본의 불일치는0이다. 시험 저장6개 중 `HOK_RT56_TEST_OLD15_UNSTARTED_20261109.hoi4`는 원래 저장의 동일 바이트 alias이며 새 엔진 생성 저장이나 원본 추가가 아니다. 체크섬 `(1bb3)`/DLC36/RT56+port+V2 fixture3개/13,569 province를 기록했다. 2026-11-09(KST) f03 종료 당시에는 후속 시험이 남아 프로필 복구 전이었으며, 최종 복구 결과는 아래에서 구분한다. 시작 뒤 완료 시험 저장을 cold load한 화면과00:51:20/1936.8.1.16 snapshot에서 `active13=0 / successes=13 / PP1204.612`를 확인했다. 새13개 `available` 복사값과 구형7개 `visible` 복사값은 모두0이다. 이는 해당 완료 저장의 유지 관측이며 모든 기존 저장이나 엔진 UI 필터 전체의 증거가 아니다. 근거는 `<TEST>/new-host-session/runtime-log-review/fixture-03-live-interim-20261108T155207UTC/game.log`와 `<TEST>/new-host-session/session/runs/fixture-03/screenshots/completed-save-cold-loaded.png`·`completed-save-cold-load-observation-02.png`·`completed-cold-snapshot-invoked.png`다.

fresh BASE를 다시 불러온 뒤의 NoC3·PP 경계는 중점/정치력/공장 조건을 합성 준비한 시험이다. NoC3 `.31` 뒤 공장 갱신을 기다린1936.1.1.19에 `C3=0 / available_projects102`에서 원래 국토개발 결정을 막는 기술 조건을 확인했고, `.32`로 C3를 지급한 뒤 활성 조건의 변화를 확인했다. 직후 PP74는 원래75PP 결정이 차단되고 PP75는 활성, 강원 PP149는 차단·PP150은 활성인 실제 UI를 남겼다. copied `available` 값은 PP 비용/active UI 필터를 포함하지 않으므로 PP74에서 복사값1이어도 원래 UI 차단과 모순되지 않는다. 처음 `pp74-paused-setup.png`는 실제 PP75여서74 증거에서 제외하며, `pp74-actual-paused-setup.png`·`native-pp74-blocked.png`와149/150의 별도 실제 setup/tooltip 화면을 사용한다. 로그 기준은 `<TEST>/new-host-session/runtime-log-review/fixture-03-live-interim-20261108T160632UTC/boundary-phase-evidence.json`이다. 초기 공장 갱신 전 가용5는 C3 부재·150공장 반영 전 값이므로 유효한 factory5 경계 통과로 세지 않는다.

이후1936.1.5.04에 일시정지를 유지하고 전라북 원래75PP 결정을 **직접 UI로 착수**했다. 같은 시각 `PP75→0 / 가용 getter103→98 / 해당 native active0→1`과 실제90일 timer 화면을 확인했다. 이 시점에도 `hold97=1`이었고 실제 가용량은103이므로 앞서 실패한 factory5/6 목표와 구분한다. source/화면 근거는 `<TEST>/new-host-session/runtime-log-review/fixture-03-live-interim-20261108T161306UTC/native75-phase-evidence.json` 및 같은 실행의 `screenshots/native75-start-before-pp.png`·`native75-start-pp0-90days.png`다. 해당 f03 사례에서 강원150PP는 활성 화면까지만 관측했고 실제 착수는 후속 f04의 별도 근거로 확인했다.

negative는 별도 BASE 뒤 기존 fixture의 guarded `activate_decision` 경로로 시행했으므로 일반 mouse 착수 증거와 구분한다. 남전라1150이 외국 소유인 상태에서도 대상919의 native 활성화를 관측했다. 이후919 소유/통제 상실과1151 benefit trigger의 `conservative_room=0`에서 두 사업이1936.1.5.24에 종료되고 완료 표식0·성공0을 유지했다. 이 구간의 PP1702.402→1703.603은 인접 일일 증가 수준이며 환급 jump를 관측하지 않았고, 가용 getter84→94를 기록했다.919만 복구하고1150을 외국 소유로 남긴1.7.10의 재시도는 PP1706.005→1631.005와 getter94→89를 동반했다. category base12인920의 착수와 나중1150 포화 설정에서의 착수도 기록했지만90일 완료·포화 보상은 아직 검증하지 않았다. root의 정지 화면1.15.03과 마지막 숫자 checkpoint1.10.24를 구분한다. 근거는 `<TEST>/new-host-session/runtime-log-review/fixture-03-live-interim-20261108T162108UTC/negative-phase-independent-review.json`이며 명목 occupied24를 실제 shared capacity로 취급하지 않는다.

partial도 별도 BASE·fixture lifecycle 시험이다.1149는 소유1을 유지하면서 province13566만 통제0인 vector와 `full=0`이1.3.11부터1.8.09의 명시적 복구 직전까지 여러 checkpoint에 남았다. 즉시 조기 평화로 통제가 돌아왔다는 해석과는 맞지 않지만, 전 기간의 연속 war-status telemetry를 확보한 것은 아니다.1.4.24의 native 종료는 완료0·성공0, 가용 getter97→102와 PP 환급 jump 부재를 기록했다.1.8.09에 fixture `.45`의 white peace와 명시 controller 복구 후 vector가 모두1이 됐고,1.9.08 재시도는 PP1931.8433→1856.8433(-75)·getter103→98·active1을 보였다. 마지막 숫자 observer1.10.24는 완료0이며 root의 day13 정지 화면과 구분한다. **재시도90일 완료는 미검증**이다. 독립 검토와 raw/segment SHA 근거는 `<TEST>/new-host-session/runtime-log-review/fixture-03-partial-capture-20261108T163404UTC/partial-independent-review.json`에 있다. negative/partial 각 보존 구간은 시작 뒤 신규 오류 기록0이지만 전체 실행 무오류나 기존 PRC/rotation 오류 해결을 뜻하지 않는다.

구형 경로는 별도 BASE에서 marker0일 때 구형7개 visible 복사값1·신규13개0으로 전환되고, 구형 강원 착수의 PP2000→1850·가용 getter103→98을 관측했다. marker 복원 뒤에도 getter98과 종료 기록 부재가 제한된 관측 구간에 유지됐다. `ACTIVE_EXPECTED_180DAY`는 무조건 출력하는 기대 표식이므로 정확한 잔여180일·실제 만료·진짜 구형 저장 지원의 증거로 쓰지 않는다. 근거는 `<TEST>/new-host-session/runtime-log-review/fixture-03-legacy-capture-20261108T163736UTC/legacy-independent-review.json`이다. 슬롯 시험의 BASE4/EMPTY20/EMPTY24/EMPTY25/OCCUPIED24/OCCUPIED25라는 명목6설정은 room 복사값1/0/0/0/1/0을 남겼다. factory 종류별 threshold query의20 포화값과 category base는 실제 shared capacity25를 증명하지 않는다. 보상·사업 완료와도 별개이며 근거는 같은 review 루트의 `fixture-03-slots-capture-20261108T164120UTC/slots-independent-review.json`이다.

영어 civic 합성 seed `.202`와 회복 trigger seed `.203/.204` 뒤 원래 사건 `.3/.13`을 열어, 두 사건의 제목·영어 설명은 보이지만 immediate sync의 긴 자동 제거 목록이 acknowledgement를 화면 아래로 밀어내는 **실제 UI overflow**를 확인했다. `air-recovery-before-overflow.png`·`rocket-recovery-before-observation.png` 원시 PNG와 당시 로드한 civic event SHA `CB0916510505C5F77F977712A6671ABA50DD6AE5CC76BEF92FA61B2CE75186F7`은 최종 review의 `recovery-ui-raw/`·`loaded-source/`에 고정했다. rocket 설명이 없다는 첫 축소 판독은 원본 detail 재확인으로 철회했다. air 선택지를 수락하지 않고 최소화한 뒤 rocket을 직접 호출한 합성 경로이므로 정상 계약 만료·회복 선택지 수락 증거가 아니다. 최종 오류는784기록/649고유(초기667+BASE PRC reload108+rotation9)이며 신규36출력/fixture 이름 관련0과 UI 결함을 함께 기록한다. parser 오류가 없다는 사실로 overflow를 통과 처리하지 않는다. 최종 근거는 `<TEST>/new-host-session/runtime-log-review/fixture-03-final-collected-20261108T165108UTC/{FINAL_REVIEW.md,final-integrity-and-ui-review.json}`이다.

이 f03 종료 시점에는 실제 가용5·6, 강원150PP 실제 착수, 재시도90일 완료·포화 보상, 실제 구형 저장·한영 civic 전체·수선 뒤 회복 UI·외교 실제 선택지 등이 미확인이었다. 이후 f04/f05에서 확인한 항목은 아래에 따로 기록한다. 합성 seed와 실제 UI 착수·활성/완료 저장 cold reload·정상 타이머 종료를 정상 중점 진행이나 실제 구형 저장 지원으로 확대하지 않는다. 당시 새 세션은 복구 전이었으며 앞 문단의 이전755 세션 복구 기록과 아래의 manifest196 최종 복구는 서로 다른 시점의 결과다.

### 회복 표시 수선과 별도 V4 준비

확인된 overflow에 대한 수선은 `.3/.13` immediate의 마지막 `HOK_KOR_sync_civic_state = yes` 두 곳만 `hidden_effect`로 감싼다. 비용·수치·조건·효과 순서·선택지·예약·그림은 유지하며 event SHA는 `CB091651…86F7`에서 `E0FC4A82884BB1E3969E649C469E93DAC39130DB2D94BA2AA937292B74B08B78`로 바뀐다. 현재 runtime61경로 중 나머지60은 동일하고, host lock의 preserved32 이전 hash는 지우지 않고 `approved_runtime_revisions`의 정확한 이전/이후 한 쌍으로 연결한다. generator/lock·대장 한 셀의 갱신과 독립 core917/0·host5216/0, 의미 변이4/4 및 별도 독립37/0의 근거는 `<TEST>/repairs/civic-recovery-v2/{source-after.json,apply-checks.json,scope-and-mutation-verification.json,independent-review/review.json}`에 있다. 이 소스 수선은 다음 실행의 회복 UI 통과와 별개다.

회복 수선 뒤 재실행한 aggregate는 **23 PASS / 0 WARNING / 11 ERROR**, exit1이며 `<TEST>/checks/aggregate-after-civic-recovery-v2.json`·`.txt`에 보존했다. 앞선 WTT 연결 뒤23/0/11과 같은 기존11개 오류가 남고, 이번 회복 수선의 신규 오류를 추가하지 않았다. 전체 부채 해소나 실제 UI 통과를 정적 집계로 대신하지 않는다.

별도 `<TEST>/runtime-preparation-v4/`는 V3 준비135파일을 동결하고 **실제 fixture18파일 모두를 바이트 그대로 유지**한다.43버튼/3범주/언어별96키·원래9 payload·17/39버튼·46 production payload 계약은 보존하며 현재61 pin 중 승인된 civic 한 개만 바꾼다. 새 current 검사기는 과거243/475 검사기와 보고서를 변경·재실행하거나 현재 PASS로 부르지 않는다. 자체 current 계약778/0, 등록 hash도 맞춘 메모리 변이14/14 탐지·보존257/0(V3 준비135+V2 준비61+현재 production61)을 기록하고, 두 wrapper를 역변환한 전체 ordered AST와 이전 사건 전체 바이트의 일치를 확인한다. 상세 manifest·차이·초기 newline-reader 불일치 기록·최종 검사는 V4의 `preparation-manifest.json`, `validation/`, `RUNBOOK.md`에 있다.

`<TEST>/new-host-session/driver/session_v4.py`는 V3 driver에서 PREP 경로와 정확한 승인 revision resolver·host preserved-content binding만 바꾼 별도 사본이다. **PREP-only 변경은 아니다.** 같은 SESSION/소유 descriptor/수집·복구 경로를 유지하고 나머지 AST는 동일하다. pure resolver 양성2개·음성9개를 검사했으며 준비 작업에서 driver의 프로필·게임 동작은 실행하지 않았다. 첫 QA의 driver import는 필수 action이 없어 argparse에서 거부됐고, 이후 AST에서 pure 함수2개만 분리해 검사했다(`validation/first-driver-qa-import-refused.txt`). 실제 차이·최종285입력 pin·프로필/게임 동작0은 같은 driver 디렉터리의 `v4-driver-provenance.json` 및 `<TEST>/new-host-session/v4-driver-preparation/`에 있다. `run_session_v4.py check`는 읽기 전용 current778/0을 확인했다. 이 준비는 V1/V2/V3·현재 프로필·게임을 변경하지 않았으며, 이후 실제 실행 결과는 다음 문단에 별도로 기록한다.

### fixture-04 한국어 실행 결과

`fixture-04-ko`는 PID23996, V4 fixture+포트+RT56 Korean Translation+RT56의 선택4개·실제 `(57d3)`·DLC36·13,569 province로 실행해 **정상 종료·로그34개 수집을 완료**했다. 사용자 프로필 원본과 소유 fixture descriptor는 같은 새 호스트 부모 세션의 관리 범위를 유지한다. 새 civic hash `E0FC4A82…08B78`의 한국어 `.3/.13`을 합성 trigger seed로 열어, 제목·본문·수정 뒤의 제한된 자동 효과와 acknowledgement가 한 창 안에 모두 보이는 것을 확인했다. root는 두 실제 acknowledgement를 각각 클릭한 것도 관측했다. 근거는 `<TEST>/new-host-session/session/runs/fixture-04-ko/screenshots/air-recovery-after.png`·`rocket-recovery-after.png`, 같은 실행의 `launch-intent.json`·`source-fingerprints-prelaunch.json`이다. 이는 f03의 CB09 영어 overflow와 다른 새 실행의 한국어 수선 UI 관측이며 정상 계약 만료·영어 수선 UI의 증거가 아니다.

같은 실행의 `civic-influence35-tooltip.png`는 시민사회 지원 조건의 **현재35**를, `institutional-capture-effects-tooltip-observation.png`는 기관 장악망 해체의 제거 효과 **기관 장악 -25 / 조달 비리 -10 / 시민사회 영향력 +5**를 표시한다. 기존 수치·표시 계약과 일치하는 툴팁 관측이며 추가 수선이나 실제60일 완료 효과를 뜻하지 않는다.

별도 fresh BASE의 no150 seed는02:44:45/1936.1.1.12에 focus/C3/PP2000과 own ledger0만 준비했고, 명시적인 갱신 뒤1.1.16 snapshot에서 **실제 가용5·civ8·C3보유·PP2000·native 활성0**을 기록했다. 원래 **전북** 결정 툴팁의 C3는 초록, 가용 민공 `>5`는 빨강이었다.02:49:01의 실제+1 요청1회 뒤 ledger1이 됐지만 직후 getter는 여전히5였고, 다음 갱신 뒤1.2.02 snapshot은 **실제 가용6·civ10·PP2000**을 기록했다. 이때 원래 **강원** 툴팁의 `>5` 조건이 초록이었다. 따라서 동일 강원 버튼을5/6 양쪽에서 확인했다고 확대하지 않는다. `korean-cndp-all13-visible.png`에는 원래13개 한국어 결정 이름과75/150 비용 행도 남겼다.

root가 같은 일시정지1.2.02에 강원을 실제 UI로 눌러 **PP2000→1850·native180일 활성 행**을 확인했다. generic `.99`의 다음1.2.11 관측은 가용 getter1·강원 native active1·state1144 done0이며, 이는 착수 시각보다 **9게임시간 뒤**라6→1을 동일 순간의 차분으로 쓰지 않는다. ledger1은 요청 기록이며 civ8→10의 단독 원인을 그+1로 확정하지 않는다. 첫 지도 조작 오클릭은 실제 요청에서 제외했고 로그에는+1 요청 한 번만 있다. bulk150·강제 native 착수·full13 watcher 초기화 없이 수행한 합성 진입/실제 UI 시험이며180일 만료나 정상 장기 진행을 대신하지 않는다. 독립 근거는 `<TEST>/new-host-session/session/runs/fixture-04-ko/observations/independent-calibration/{INDEPENDENT_REVIEW.md,INDEPENDENT_REVIEW.json}`로, 안정된20로그 파일·16개 prefix·원본 detail PNG3개와 해시 사본을 대조했다. 화면은 같은 실행의 `factory5-native-blocked-tooltip.png`·`factory6-gangwon-native-enabled.png`·`native-gangwon-start-pp1850-180days.png`다. seed 이후 보존 구간 신규 오류0과 과거 f03의97 목표 실패를 구분한다.

후속 구형15주 사례는 원래 저장과 byte-identical인 `HOK_RT56_TEST_OLD15_UNSTARTED_20261109.hoi4` alias를 실제 GUI로 불러와1936.2.5.02/PP43의 지도에 진입했다. 정상 clock으로2.20.05/PP61까지 **15일3시간** 진행한 뒤 새 `KOR_1936_02_20_05zzold15r1_temp.hoi4`를 만들고 **같은 프로세스에서 재로드**해 같은 날짜/PP61 지도에 돌아왔다. 이는 cold 재시작 증거가 아니다. 선택 화면·첫 지도·재로드 지도는 같은 실행의 `screenshots/old15-alias-selection.png`·`old15-loaded-paused-map.png`·`old15-progress-reload-observation.png`다. 원시 사본을 비교한 `observations/old15-real-carry/BOUNDED_SAVE_REVIEW.json`은 새 저장 SHA `F8572378211A0442E28BC4F698579B7A667FA6D7516A5508DFB97F9AA3B25BB4`, 두 저장의 선택15주 KOR 소유, 닫힌 KOR 범위의 신규 marker·구7/신13 project·CNDP focus token 부재를 기록한다. **업데이트 전15주 체계의 CNDP 미착수 저장 한 건**의 제한된 진행/다른 이름 저장/인게임 재로드 결과다. 구형 진행 중·완료 CNDP, 구9주 지도 이전, 모든 세계 상태 동등성이나 전체 기존 저장 지원을 증명하지 않는다.

alias에는 이전 `HOK_RT56_SUITE_verify_base` 진단 decision 흔적이 있어 clean fixture 이력도 아니다. 최초 alias 로드의 invalid decision1개와 후속 parser1개, 합계2개를 보존했고 새 저장에는 해당 원시 token이 없었다. PAL portrait 저장 참조의 missing texture 경고2개도 기록했으며 해당 경로는 포트·현재RT56·고정196 감사 사본에 없다. 그 역사적 누락 원인이나 새 HOK 단독 원인으로 확정하지 않는다. 별도 안정된 재로드 직전 raw 사본이 없으므로 최종 로그 구간과 root의 실제 GUI 관측을 각 근거로 구분한다.

최종 독립 보고서는 `<TEST>/new-host-session/runtime-log-review/fixture-04-ko-final-collected-20261108T180827UTC/FINAL_INTEGRITY_AND_OLD15.json`이다. 로그34개, 원래 저장61개+백업61개, 세션 누적 시험 저장9개와 원본/수집 사본의 불일치는0이다.9개를 모두 f04에서 새로 생성한 것은 아니며 원래 alias도 포함한다. prelaunch와 `post-ko-before-close`의 소스 지문은 각각6,607행으로 key·hash 불일치0이며, 종료 직전 검사는 원래 prelaunch 기록과 별도로 보존한다. 최종 오류716기록/674고유는 초기667+PRC36+이전SUITE2+저장/continue rename4+rotation5+portrait2다. 현재36출력/fixture 관련 오류0과 이전 저장 경고를 구분하며 전체 무오류로 부르지 않는다. f04 검토 당시에는 f05와 최종 복구가 남아 있었고, 그 이후의 결과는 아래 최종 기록에 연결한다.

### fixture-05 선택 refs 결과

`fixture-05-en` PID848의 선택 refs6사례는 root가 매번 fresh BASE를 다시 불러온1936.1.1.12 일시정지 상태에서 실제 진단 UI 버튼을 눌렀다. 독립 PRE/POST 검사는 **REF1 35/0·REF11 20/0·REF13 21/0·REF15 20/0·REF21 19/0·REF22 21/0, 합계136 PASS / 0 FAIL**이다. 이는6사례의 선택 검사항목 수이며 전체 f05 최종 검토가 아니다. 근거 색인은 `<TEST>/new-host-session/session/runs/fixture-05-en/observations/refs-progress-index.json`, 개별 원문·hash·행 범위는 색인이 가리키는 timestamp 디렉터리의 `ref1-independent-review.json` 및 나머지 `ref*-independent-review-v2.json`에 있다. REF11의 첫 판독은 같은 게임 시각에 더해 벽시각까지 같은 초여야 한다고 잘못 요구했으며, 그 원래 실패 보고서는 보존하고 게임 시각 유지·원문 순서·벽시각 단조 증가를 확인한 V2를 선택했다.

REF1은 원래 `KOR_port_fortification` 중점을 강제 완료해 해주917/province13559의 해안요새0→3과 나머지 선택6항구의1→4를 관측했다. REF11은 FRA 종속 FRI의9주 소유/완전통제에서 VIN9주·KOR 종속으로 넘어갔고, REF13의 JAP 종속 FRI와 REF15의 전시 완전통제8/9는 guard0으로 이전하지 않았다. REF21은 ENG 소유/완전통제 Singapore의 MAL 이전·KOR 종속을 관측했다. REF22는 SIA의 완전통제 때문에 **조건부 Singapore 이전만 차단**하고 ENG 소유·SIA 통제를 유지했으며, 무조건 MAL/KOR 정치 효과에 따른 MAL의 KOR 종속은 남았다. REF1을 제외한 수락 효과는 fixture의 복사본 실행이다. **원래 외교 수락 선택지 클릭·1일 뒤 callback·정상 중점 진행·후속 전쟁/장기 저장 결과는 미검증**이다. 뒤의 영어 civic native 선택은 이 외교 refs와 다른 관측 계층으로 기록한다.

### fixture-05 영어 civic native 선택

fresh BASE의 `.202` 합성 C60/V35/I65/P40/PP2000 준비 뒤1936.1.1.12 일시정지를 유지하며 **원래 `.1.a → .11.b → .2.a → .12.b`를 A/B/A/B로 실제 선택**했다. 각 단계의 고유 native 저장4개는 같은 날짜를 유지하고 PP1900→1900→1825→1875, 최종 C60/V40/I70/P70·root stability0.45를 기록한다. 첫 비용 전2000은 고정 seed와 root/UI 근거이고 이후0/−75/+50 차이는 연속 저장의 실제 PP literal 차이다. 독립 원시 검사 **60/0**, 예약 queue 검사 **16/0**, 단계 간 교차 검사 **27/0**은 별도 집계로 유지한다. 근거는 `<TEST>/new-host-session/session/runs/fixture-05-en/observations/en-controlled-series/controlled-series-evidence-index.json`, SHA `C644B37B59E8B251603F1C4197B9885BA0310BA1B920BEEF6C1D94DD49E970F0`와 거기에 연결한 각 단계 raw/queue 보고서·저장·이미지다.

두 경고/두 사고의 선택지8개를 hover하고 실제로 선택한 분기는 위4개뿐이다. 항공 사고의 종이 아래 프레임은 화면에서 잘리지만 두 버튼은 모두 보였으므로 전체4창의 프레임 완전 표시라고 하지 않는다. 첫 `en-air-accident-option-a-tooltip.png`는 너무 일찍 찍혀 효과 tooltip이 없어 제외했고 `en-air-accident-option-a-tooltip-observation.png`를 사용했다. 독립 detail 판독은 같은 실행의 `observations/independent-en-ui-review/independent-en-ui-review.json`에 있다. `.3` 예약의 raw `months=2/days=0/hours=0`과 `.12` 예약의 `months=0/days=27/hours=3`가 직렬화됐지만 시간이 흐른 만료·후속 trigger 성공을 뜻하지 않는다. 사고는 창을 열 때의 원래 immediate 효과까지 포함한 저장 결과이며 각 사고 선택 직전의 별도 저장은 없다. 첫 사건 뒤에는 안정된 저장/화면만 있고 첫4로그 prefix는 두 번째 선택 이후부터다.

이 연속 시험은 회복 중 다른 계약/사고를 여는 합성 flag 진입을 포함한다. 원래3중점 진행,75PP 유료 계약 진입,180일 혜택·무작위 경고/사고 도달·60/365일 lifecycle·미선택 분기의 실제 효과는 검증하지 않았다. 별도 fresh BASE의 회복과 최종 수집/복구는 다음 기록으로 구분한다.

영어 회복은 새 BASE와 `.202` 뒤 원래 `.3`의 전체 창·ACK를 확인하고 실제 선택했으며, 이후 원래 `.13`의 전체 창·ACK도 확인하고 선택했다. 두 회복 사이에 일시적인 진단 행 이동으로 뜻하지 않게 fixture의 `.20` 호출 버튼을 눌러 **숨김 native `.20` → 공개 `.24` 경고와 실제 ACK**가 추가됐다. 해당 화면은 `en-prosecution-warning-unplanned.png`로 보존하며 현재 `en-rocket-recovery-after.png`는 실제 `.13`임을 제목으로 독립 확인했다. **순수한 두 회복만의 독립 사례가 아니다.**

새 `KOR_1936_01_01_12zzencivic_temp.hoi4`는79,458,408바이트/SHA `25893D7A696587577E80EF0CD926EF5E701FF856D67A55DBAF7A279D10878640`이며 같은1.1.12의 C60/V35/I55/P20·PP2000을 기록했다. 회복 선택 raw15/0·선택 queue4/0·추가 맥락9/0은 합산하지 않는다. 선택한 HOK delayed event queue는 비어 있지만 별도 위기 active flag1·pressure idea·active90일 mission은 함께 저장돼 있다. 이를 회복/위기 기간의 자연 경과나90일 취소·만료로 해석하지 않는다. 최종 색인은 `observations/en-recovery-with-warning-save/qualified-recovery-evidence-index.json`, SHA `92BFE04E574DC4CC3852F2F5D9C42BAF1D026197A2E9D1AAE86581463C581A7E`다. 연결된 독립 UI 판독 `observations/independent-en-recovery-review/independent-review.json`은 두 전체 창/ACK 및 닫힌 뒤 지도를 확인하고, 실제 클릭은 root 관측으로 따로 묶었다. f03의 overflow는 수선 뒤 한국어·영어의 이 제한된 실제 UI에서 재현되지 않았다.

### 최종 종료·복구와 보존 감사

root는 PID848을 정상 종료했다. 종료 중 첫 collect는 안전하게 거부됐고 프로세스 종료 뒤 성공한 `session/runs/fixture-05-en/evidence.json`은 **로그34개·세션 누적 시험 저장14개·원래 저장61개 차이0**을 기록한다.14개는 이전 실행과 원본의 별도 alias도 포함하며 f05에서 모두 생성한 것은 아니다. `source-fingerprints-final-before-close.json`의6,607행 불일치도0이다. 독립 종료 대조 `observations/final-independent-closed-audit/closed-run-independent-audit.json`은 **12 PASS / 0 FAIL**, SHA `F2B312B61293D4DF5A8554D641FBE8B5AB64914FB0C458BD8B6D0B1DF55C9C3C`다. 수집 로그/누적 시험 저장의 source·copy·receipt hash를 대조했으며 원본/백업61개 본문 해시는 아래 root 최종 감사에 연결하고 중복 독립 재해시로 주장하지 않는다.

최종 f05 오류 분류는 `observations/final-collected-error-classification.json`의 **812기록/655고유 = 초기667 + BASE PRC advisor126(7회×18) + continue/저장 rename10 + rotation9**다. 선택한 HOK/fixture symbol 관련0이며 전체 무오류는 아니다. R0와 파일명·near line까지 같은 PRC 원문은 아니므로 exact signature 비교의 false와, 별도 RT56 단독 R0-02에서 확인한 같은 경고군의 재현을 구분한다. 조용한 선택 경로나 보존 감사 통과를 전체 오류 해결로 쓰지 않는다.

`<TEST>/new-host-session/session/restoration.json`은2026-11-08T19:07:05 UTC의 **RESTORED_EXACT_SETTINGS_METADATA_CAREER**와 원래 저장 차이0, 원래 선택·설정·metadata/career 복구 및 소유 fixture descriptor 부재를 기록한다. root가 실제 Steam 창에서 HOI4의 녹색 **플레이**를 확인한 별도 UI 근거는 같은 폴더의 `steam-play-after-final-restoration.png`다. 파일 감사만으로 UI 복구를 추정하지 않는다.

최종 읽기 전용 source/profile 감사는 `<TEST>/new-host-session/final-restoration-audits/20261108T191122.511968UTC-24704/audit.json`의 **68 PASS / 0 FAIL, exit0**, SHA `26F9E4473F3BFA4771ED9E242F8A8448959304163BEB090D4662B718FB54368F`다. 원래 nonlog/nonsave62개+백업62개와 원래 저장61개+백업61개의 bytes/mtime/SHA, root/career 이름 목록, 소유 임시 descriptor3개 부재, 최종36출력·지도24·L08·승인된 source6,607행, donor36/docs13와 동결 사본, 전체 현재 RT5628,746파일을 대조했다. manifest1963361040482473746/build26409260은 전후 같고 HOI4/launcher는 없었다. 이는 명시한 파일·프로세스의 보존 결과이며 모든 게임 기능·미수집 사용자 파일·장기 저장 호환성의 증거가 아니다. 시험 저장14개는 보존했고 추가 정리·Git 게시·배포 작업은 수행하지 않았다.

### 현재 확인 범위와 남은 검증

| 범위 | 확인한 내용 | 남은 한계·진행 |
|---|---|---|
| civic·한영 표시 | 수선 뒤 한영 회복2창씩과 ACK, 영어4사건8개 hover/실제 A/B/A/B·raw60/queue16/교차27 각각0실패, 회복 raw15/queue4/맥락9 각각0실패 | 영어 회복 사이에 추가 `.20/.24`가 있어 순수 pair가 아님. 정상 유료 계약·예약 만료·365일 재사용 제한·모든 분기는 미검증 |
| CNDP·저장 |13개 native 정상 타이머/선택 보상·취소/재착수, 실제5/6·75/150PP 착수, 선택한 구형15주 저장의 진행/저장/인게임 재로드 | 재착수90일 완료·포화 보상, 구형 진행/완료 CNDP·구9주 지도 이전·임의 기존 저장 지원은 미검증 |
| 외교 수락 경로 | 고정 source/독립 AST 및 f05 refs6의 선택 PRE/POST136/0. FRI 양성·JAP 종속/부분통제 부정·Singapore 양성/적 통제 부정을 관측 | REF1은 원래 중점 강제 완료, 나머지는 복사 수락 효과. native 외교 선택지 클릭·1일 callback·정상 중점/후속 진행은 미검증 |
| 실행 환경 | 기록한 build26409260/manifest196·DLC36·실제 영어/한국어 playset | 다른 DLC 조합·장기 AI·멀티플레이는 미검증 |

f05 수집·독립 종료 대조와 원래 프로필/기존 저장/소유 descriptor의 복구·최종 보존 감사는 **완료**했다. 위 표의 미검증 동작과 기존11개 정적 부채는 별도 남기며, 이를 이유로 이번 선택 수선의 범위를 확대하지 않는다.

소스 보존 기록도 범위를 나눈다. 최종68개 검사는 선택 donor 원본36/docs13↔동결 capsule과 승인된6,607행을 대조했지만, 활성 `C:\hoi\test\hok-rt56-source-cache\sources\`의3개 캐시 전체를 manifest에 직접 재해시한 것은 아니다.6,607행의 활성 source-cache 경로는0개이고 helper의 메모리 hash cache도 그 외부 캐시가 아니다. 따라서 활성 cache 전체의 이번 직접 재검증은 미수행으로 남긴다. 기존 cache 위치·역할·옛 검증 기록은 유지하며 이번 문서 작업에서 캐시나 감사 도구를 실행·변경하지 않았다.

## 2026-11-09 커밋 전 체크아웃 바이트 보존

사용자가 현재 변경의 커밋·푸시와 영어 커밋 메시지를 승인했다. 스테이징 중 `core.autocrlf=true`가 새 동결 입력의 줄바꿈을 정규화하고, 명시적 속성이 없는 새 LF 출력은 이후 CRLF로 체크아웃할 수 있음을 확인했다. `.gitattributes`에 새 출처 보관본3개의 `-text`, 잠금3개와 관련 CRLF 출력의 명시적 CRLF, 새 주6개와 `state_groups.txt`의 LF 규칙을 추가했다. 보관본은 새 속성으로 다시 스테이징했다. 전역 Git 설정·런타임 원문·잠금 내용·기존 source pins는 바꾸지 않았다.

실제 스테이지345개를 외부 디렉터리에서 `core.autocrlf=true`와 `false`로 각각 체크아웃했다. 각 설정에서 런타임·출처 보관본·잠금·원장의 보호 대상315개를 현재 작업 소스와 SHA-256으로 비교하여 **각315개 일치 / 불일치0개**를 확인했다. 이는 Git 전송 바이트 검사이며 앞선 게임 검증이나 기존11개 오류의 상태를 바꾸지 않는다. `git diff --check`가 지적한 후행 공백·들여쓰기는 이번 커밋 준비에서 정리하지 않았다.

출력은 `C:\hoi\test\hok-rt56-commit-20261109-01\`의 `nul-autocrlf-true/`, `nul-autocrlf-false/`, `checkout-byte-verification.json`이다. 최초 PowerShell 줄 단위 입력은 경로 끝 CR 때문에 모든 경로가 거부됐고, NUL 구분 바이트 입력으로 다시 확인했다. 최초 시도 디렉터리도 외부에 남겼다. 이 자료는 테스트 출력이며 source capsule·활성 캐시·커밋 대상에 포함하지 않는다.

## 외부 자료와 정리

`<TEST>/baseline.json`은 수정 전 런타임1,456경로·선택 host4,806·vanilla134 지문과 backup56개·이전 로그20개를 관리한다. `<TEST>/backups/compat/`는 이전 포트 사본, `preview/`는 신규32 출력 후보, `cndp/`·`civic/`·`references/`·`validation/`은 각 범위의 helper/fixture/검사·과거 실패 자료다. 실행 session 직전 백업은 초기 baseline과 별도로 유지한다. 게임이 생성하는 원본 로그/저장은 실제 user-data에 있고 필요한 증거 사본을 외부에 보존한다.

기존 `tools/__pycache__/`21개·1,088,888바이트와 donor의 검증 PNG4개·815,391바이트는 정리 대기 자료다. 이번 구현은 이 기존 자료의 삭제·이동을 포함하지 않는다. 신규 helper·보고서·fixture·미리보기·backup을 저장소나 활성 source cache에 만들지 않았다. 실행 소유 프로세스 종료·Steam 상태·원래 프로필/기존 저장 복구 결과는 위 최종 기록을 따른다.
