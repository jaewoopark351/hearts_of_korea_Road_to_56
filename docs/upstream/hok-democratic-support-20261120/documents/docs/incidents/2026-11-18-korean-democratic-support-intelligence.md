# 한국 민주인사 지원과 비밀 정보국 확장 구현 기록

> 2026-11-19 중국 대상 확장 후속: 지원·축출을 정식 16태그의 공통 판정으로 연결했다. 현재 구현·검증 상태는 [계획 14절](../HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_PLAN.md#14-2026-11-19-최신-중국-군벌-대상-누락-검토미구현-확장안)을 따른다. 아래 기존 중국 7태그의 실행 결과는 당시 소스의 이력이며 신규 군벌·쿠물·동적 국가 제외의 실행 검증으로 재사용하지 않는다.

> 2026-11-19 추가 후속: 「중국 독재자 축출」·「민슈 잇키」에서 한국의 세력 맹주 가용 조건만 제거했다. [현행 명세 12절](../HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_PLAN.md#12-2026-11-19-두-봉기-중점의-한국-세력-맹주-조건-제거)의 소스 비교와 미검증 범위를 따른다. 아래 맹주 상태의 기존 실행 결과를 새 비맹주·무세력 분기의 성공 증거로 사용하지 않는다.

> 2026-11-19 후속 변경: 정보국의 선행·위치 기준을 「재무장 시작」으로 옮겼다. 현재 (62,1) 고정 배치·LaR 전용 표시 조건·AI 순서·소스 비교 27확인/미해결 0은 [현행 명세 11절](../HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_PLAN.md#11-2026-11-19-재무장-시작-선행으로-이관)을 따른다. 아래 독립당 선행의 B8·762d·c212 결과는 이전 단계 이력이며 이번 선행 변경의 게임·UI 검증은 실시하지 않았다. 전후 사본과 검토는 `C:\hoi\test\hok-intelligence-rearm-parent-20261119-01\`에 있다.

작성: 2026-11-18, 최종 갱신: 2026-11-19 (Asia/Seoul). 상태: **구현 반영 / 정적·핵심 엔진 확인 / 실제 UI·기존 저장 재로드·작전 실측 미검증**.

사용자는 [기능 계획](../HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_PLAN.md)의 전체 구조를 인용하고 `AGENTS.md, /docs 읽고 구현해줘`라고 요청했다. 앞선 문서화 전용 작업과 이번 구현 승인을 구분한다. 중점 연결·반복 지원 결정·일본 봉기 비율·신규 정보국 중점·국민정신·시각 자산·한국어 두 채널의 변경이며 호환성 복구·원본 전체 교체·배포 작업이 아니다.

## 기준과 외부 증거

| 구분 | 이번 기준 |
|---|---|
| 작업 소스 | `C:\hoi\hearts_of_korea` |
| 시작 Git | `feat/korean-focus-expansion-ai`, HEAD `0c19f58fa7a9ff898196dcdbe46edfd0ad5fdbbc` |
| 시작 시 기존 변경 | README·2차 확장 계획과 새 기능 계획의 문서 3개. 보존한 뒤 구현 기록을 이어 씀 |
| 설치 원본 | `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV`; 읽기 전용 |
| 설치 메타데이터 | `Operation Postern v1.19.5.0.7c6c (c184)`; probe 실행 체크섬과 별개 |
| 원작 구버전 | `C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\2898629778`; 역사 출처, 수정·업로드 대상 아님 |
| 실제 사용자 데이터 | `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV` |
| 외부 작업·증거 TASK | `C:\hoi\test\hok-democratic-support-intelligence-20261118-01\` |
| 원래 선택 | HOK 저장소 → 영어 번역 Anime Modder's Edition. 언어 `l_korean`, 비활성 DLC 목록은 빈 배열 |
| 진단 구성 | Korean Language `2743487021` → HOK 저장소 → TASK의 해당 외부 probe. 실제 실행은 DLC 37개를 기록 |
| 프로세스 착수 상태 | 기존 HOI4·launcher 없음. 기존 Steam PID 13492는 유지 |

원래 `settings.txt`·`dlc_load.json`, launcher descriptor, 시작 로그, 기존 저장 해시 목록과 관련 수정 전 소스는 `TASK/baseline/`에 있다. 진단 overlay·helper·미리보기·로그 사본·저장 증거는 모두 TASK 아래에 둔다. 실제 게임이 생성한 원본 로그·저장은 실제 사용자 데이터에 남으며 복사본의 역할을 구분한다. descriptor·업로드 ID·의존성·base game·Workshop 파일은 변경하지 않았다.

## 적용 내용

| 파일 | 실제 변경 |
|---|---|
| [한국 중점](../../common/national_focus/korea.txt) | 중국·일본 지원 선행을 선봉으로 교체, 초대 ↔ 지원 양쪽 배타 4곳 제거, 직접 280일 지급을 결정 해금으로 이동. 민슈 잇키는 아래 helper 호출. 독립당 단독집권 아래 35일 정보국 중점 1개 추가 |
| [지원 결정](../../common/decisions/HOK_KOR_democratic_support.txt)·[범주](../../common/decisions/categories/HOK_KOR_democratic_support.txt) | 각각 정치력 25·180일·추가 대기 0·반복. 중국 기존 7태그 전체와 JAP 지원, 기존 정신이 남으면 차단 |
| [일본 봉기 helper](../../common/scripted_effects/HOK_KOR_democratic_intelligence_effects.txt) | JAP scope의 직전 민주 지지율을 0.10–0.90으로 제한, `size`·육해공 비율 모두 명시적 `var:`로 사용. 기존 세력 편입·참전 순서 유지 |
| [정보국 국민정신](../../common/ideas/HOK_KOR_democratic_intelligence.txt) | 별도 한국 전용 영구 정신, 요원 2·고정 정보망 25/계수 25%·작전 속도 35%·비용/위험 −35%·결과 25%·피탐지 계수 −35%·일곱 효율 각 75% |
| [역사 AI 순서](../../common/ai_strategy_plans/KOR_historical_strategy_plan.txt) | 독립당 단독집권 직후 새 정보국 중점 1개를 추가. 기존 순서·가중치·다른 계획 유지 |
| [기존 Korean 중점 현지화](../../localisation/korean/korea_focus_l_korean.yml)·[paired English 채널](../../localisation/english/korea_focus_l_english.yml) | 기존 ID 유지, 정확히 5키의 설명/봉기 안내 수정. 아시아 연합 창설 이전에도 맞도록 설명 정리 |
| 신규 현지화 두 쌍 | `HOK_KOR_democratic_support_l_*`와 `HOK_KOR_democratic_intelligence_l_*`: 지원 운영·조건·효과, 새 중점과 정신 이름/설명. 두 본문은 계약대로 같은 한국어, BOM 보존 |
| 신규 GFX·DDS | 바닐라 영국 원본과 기존 시민 소형 자산을 내부 사본 6개·전용 sprite로 연결. 이미지 생성·재색칠·리샘플링 없음 |

지원은 시작한 뒤 수혜국의 정권·외교관계 변경에도 잔여 기간을 유지하고 취소·환불하지 않는다. 중국은 현존하는 지정 태그가 하나도 없으면 비용을 지불할 수 없으며, 현존 대상 중 하나라도 기존 지원이 남으면 묶음 전체를 차단한다. 기존 280일 잔여 기간을 덮어쓰지 않고 기완료 중점 저장에도 새 결정이 표시되는 소스 조건이다. 실제 변경 전 저장의 재로드는 별도 검증 대상이다.

공유 정신의 정의·태국 280일·VIN/MAL/PHI/INS 720일 호출, 중국 독재자 축출의 KCH 생성·영토·전쟁명분·후속 결정은 유지했다. 신규 지지도 비율의 하한 10%·상한 90%, 육해공 동일 비례, 신규 정보국 35일은 이번 구현에서 선택한 운영값이다. 비축 물자는 `size`의 기본 적용을 따르고 고정 주 목록·코어·지도 변경은 추가하지 않았다.

이미지의 원본 경로·원저작·허용 근거·해시·실제 치수·내부 sprite/마스크/광택 사슬은 [자산 출처](../HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_ASSET_CREDITS.md)와 [매니페스트](../data/HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_ASSET_MANIFEST.json)를 따른다. 눈 문양과 MI6 그림은 사용자 선정 원형의 그대로 복사이며 continuation 팀의 신규 원화로 표시하지 않는다. 새 결정 행은 32×32, 범주는 51×40이다.

배치는 중국 지원 `(110,7)` → 축출 `(110,9)`, 일본 지원 `(113,7)` → 봉기 `(113,9)`, 정보국 `(120,6)`이다. 민주 완료 HIDE에서는 기존 조상의 −35x를 한 번 상속한다. 전체 475개·절대 기준 7개·상대 468개·offset 7개이며 기존 전체 범위 x0–211/y0–24를 유지한다. [이번 변경 좌표](../data/HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_LAYOUT.json)는 변경된 5노드의 부분 명세이고, 과거 474개 JSON을 현재 전체 snapshot으로 바꿔 읽지 않는다.

새 정보국 중점은 La Résistance 보유와 기존 민주 분기의 `allow_branch` 조건을 함께 요구한다. HIDE에서 왕정·공산·파시 경로를 완료하면 해당 분기와 같이 숨기며, SHOW에서는 DLC 조건만 남는다. 11월 19일의 최종 가시성 가드는 보상·기간·좌표를 바꾸지 않았다. 최종 `korea.txt` SHA-256은 `b8b427df8e8a73820156a6abcff6632b60c89e2fb68c317b96f24ef2e694584d`다. 가드 전 소스 `e30428b406f210ccef8b5d5e7db436a1103b832a65cc427d191451b713ef7aef`에서의 AI 진행 증거와 구분한다. 파일 SHA-256과 아래 게임 체크섬은 서로 다른 값이다.

## 정적 검토와 범위

- `TASK/validation/source-checks.json`: 최종 가드 이후 재검토 **75 PASS / 0 FAIL**. 기존 중점 정의 보존·선행·배타·해금·지원 비용/기간/대상·보상 15값·비율·역사 AI 순서와 paired 현지화의 소스 검토다.
- `focus-source-independent-review.json`·`focus-namespace-independent-review.json`: **38개 독립 확인 / 실패 0개**. 기존 474개에서 정확히 5개만 변경되고 1개 추가됨, 상대 기준 존재·선언 순서·무순환·이동 및 신규 노드의 좁은 사각형 모델 충돌 0, 기존 offset 상속, 본체 두 채널의 정확히 5키 수정과 BOM/CRLF를 확인했다.
- 자산 하위 검토: 6개 DDS 원본/사본 바이트·해시, 포맷/알파/치수·6개 sprite·내부 텍스처/마스크/광택 경로와 작은 크기 미리보기를 확인했다. 이 결과는 게임 UI 검수가 아니다.
- `postguard-source-review.json`: **60 PASS / 0 FAIL**. DLC·SHOW/HIDE·다른 이념 완료 조합과 가드 이외 변경 부재를 독립 확인했다. 가드와 해당 주석만 이전 형태로 되돌리면 위 가드 전 SHA-256이 재현된다.

각 검토는 범위가 겹치므로 합산하지 않는다. Git의 LF 본문과 작업 트리 CRLF를 바이트 비교한 최초 48/1, 명시적 `var:` 반영을 놓친 중간 검사 오탐은 `source-check-history.json`·superseded 보고서에 남아 있다. 실제 공유 정신 파일의 변경으로 바꿔 설명하지 않는다.

활성 영어 번역 저장소의 기존 5키는 이전 영어 본문을 제공한다. 현재 시험 언어는 `l_korean`이며 이 별도 번역 저장소는 수정하지 않았다. 영어 UI에서는 새 지지도 설명과 서술이 가려지는 한계가 남아 있으므로 영어 표시 완료로 보고하지 않는다.

## 엔진 진단 기록

probe의 준비용 강제 중점 완료·지지도 설정·효과 호출과 정상 진행을 구분한다. 네이티브 scripted-test의 `TEST_FAIL_...` 이름은 **그 시점 저장을 생성하려고 의도한 capture 이름**이며 production 기능 실패 횟수가 아니다. 기능 판정은 `HOK_DSI_20261118 PASS/FAIL` 관측과 실제 저장 필드로 따로 판단한다.

| 실행 | 조건·현재 확인 | 한계 |
|---|---|---|
| `support` PID 5532 | 최초 probe에서 정치력 25 소비 두 건·수혜 8태그·정보기관/정신 지급 로그 확인 | 실행 인자 `-ai_testing` 누락으로 native capture 없음. 복합 `NOT` 감사식 4건이 잘못 작성돼 실패했으며 이 감사 오류를 production 차단 결함으로 귀속하지 않음. 본체 수정 없이 fixture 교정 |
| `support-clean-v2` PID 16580 | 체크섬 `00d5`·DLC 37개. 초기 **20 PASS / 0 FAIL**, 8개국 지원 각각 1개·잔여 179일, 실제 결정별 정치력 25 소비 확인 | 7월 만료 감사 4 FAIL을 보존. 결정 횟수가 1→2, 지원 잔여 177/178일로 바뀌어 자동 재지원이 강하게 뒷받침됨. 만료만 분리한 증거는 다음 통제 실행 |
| `support-expiry-controlled` PID 16468 | 체크섬 `776a`, **40 PASS / 0 FAIL**. 초기→만료→재구매 3단계에서 8개국 정신 개수 1→0→1, 결정 실행 횟수 1→1→2, 재구매 때 각각 정치력 25 소비 | 외부 사본의 AI factor만 1→0, 나머지 결정 바이트 동일; 본체 AI는 1 유지. 약 183일 후 만료 확인으로 정확한 180일 경계 시각·UI 클릭을 입증하지 않음 |
| `uprising-low` PID 3376 / `uprising-high` PID 19968 | 체크섬 `a098`/`25f8`. 지지도 20%/70%를 합성 준비하고 helper 직접 호출. 아래 저장 비교 **13개 확인 / 실패 0개** | 별도 새 게임·난수 시드. 자연 지지도 축적·전체 정상 중점 진행과 10%/90% 경계는 미검증 |
| 최초 `focus-ai` PID 18576 | 새 중점을 선택하지 않고 민주주의 강화 중점으로 진행. 역사 AI 목록에 신규 중점이 빠진 통합 문제를 발견해 독립당 직후 추가 | 최초 미완료 실행과 늦은 fixture 플래그 조건을 보존. `focus-ai-v2` 외부 AI 대체안은 준비만 했고 실행하지 않음 |
| `focus-ai-production` PID 14000 | 가드 전 소스, 체크섬 `c212`. 부모 4개만 합성 완료, 외부 AI 계획 없이 본체 역사 AI가 목표 선택→진행→완료. **4 PASS / 0 FAIL**, 저장/fixture 확인 9개 모두 참 | 목표를 강제 완료하지 않음. 1월 2일 progress 2·미완료·정신 없음 → 2월 5일 완료·정신·기관 존재. 명목 35일이며 정확한 840시간 실측·전체 정치 경로 정상 진행·UI 증거는 아님 |
| 최종 `production` PID 24356 | 최종 가드 소스로 전체 재시작. 원래 HOK→영어 번역 2모드·`l_korean`·DLC 37개·체크섬 `762d`. 1936.1.1.12 일시정지 상태에서 `RestoreDeviceObjects` 완료 | probe 없는 로드 확인. 원래 전체 오류가 사라졌다는 의미는 아님; 아래 9행 잔존 |

통제 지원 저장은 `1936.1.2.1 → 1936.7.3.1 → 1936.7.5.1`이며 타이머는 179일→없음→179일이다. 초기 해금은 자동 지원을 주지 않았고, 기존 지원을 주입한 조건 및 신규 지원 중 재실행이 차단됐다. 보고서는 `TASK/validation/support-expiry-controlled-summary.json`과 각 단계 JSON에 있다. 기존 변경 전 저장을 직접 재로드한 증거로 확대하지 않는다.

봉기 전 일본은 26주·60개 사단이었다. 민주 일본의 실제 저장 비교는 다음과 같다.

| 합성 민주 지지도 | 소유 주 | 사단 | 함선 레코드 | 배치 항공기 |
|---|---:|---:|---:|---:|
| 20% | 4 | 12 | 83 | 141 |
| 70% | 12 | 42 | 118 | 543 |

두 실행 모두 민주주의 D04(`original_tag=JAP`, `KJP_democratic`)가 생겼고 KOR와 같은 세력에 들어갔으며, KOR의 대일 참전 사유 `asked_to_join`을 저장에서 확인했다. 육군 사단은 각각 60의 20%·70%와 일치한다. 면적·인구·공장·함선 전투력·해공군 정확 비율·비축 물자 배분은 입증하지 않았다. `TASK/validation/uprising-low-high-comparison.json`과 두 context 파일에 관측·분류를 남겼다.

초기 지원 실행에서 정보망 25·계수 0.25·작전 속도 0.35·아군 피탐지 −0.35·7개 임무 0.75의 국가 보정값을 관측했다. 기관 기본 슬롯 1과 국민정신 +2로 총 3이며, 국민정신 보상이 +3이라는 뜻은 아니다. 정상 시간 진행 정보국 완료와 다음 「민주주의는 우리의 힘」 선택은 `TASK/validation/focus-ai-production-summary.json`에 기록했다. 최종 가드 소스의 로드와 가드 전 AI 완료 증거를 합쳐 최종 UI까지 검증했다고 쓰지 않는다.

원래 support의 `modifier@operation_cost/risk/outcome` 감사 조회는 동적 토큰 동기화 경고 6행을 만들었다. clean-v2에서는 이 세 감사 getter만 제외했다. production의 보정 키를 삭제하거나 전역 동기화 설정을 바꾸지 않았다. 실제 작전 소요일수·비용·위험·결과의 변화는 국가 보정값 조회와 별도 검증 대상이다.

장기 지원 실행의 4월 5일·6월 21일 `Invalid SlotId 0/1 for operation instance`는 국가 식별 정보가 없어 원인이 미해결이다. 최종 production 시작 오류 9행은 다른 등록 모드 descriptor 경고 7행, localisation collision 1행, 변경하지 않은 `map/buildings.txt:66858`의 인자 개수 오류 1행이다. 이번 신규 정의의 파싱·등록 오류는 발견하지 않았지만 전체 무오류나 이 경고들의 확정 귀속을 주장하지 않는다. 최종 로드 로그는 `TASK/runs/production/capture-20261118T150605Z/logs/`와 종료 후 `capture-20261118T150609Z/logs/`에 있다.

native capture에서 OneDrive 사용자 데이터의 최종 rename이 `errno 2`로 실패하여 `_temp.hoi4`가 남았다. 확보한 입력은 완전한 `HOI4txt`로 읽기 파싱했고 외부 증거 사본과 원본 해시도 대조했다. 최종 이름의 정상 저장이나 재로드가 성공했다는 뜻으로 바꾸지 않는다. 게임 생성 `continue_game.temp`도 시험 저장 경로로 바뀌었다. 이 임시 재개 색인은 사전 백업이 없어 복원하지 않았으므로 사용자 데이터 전체를 원상 복구했다고 주장하지 않는다.

## UI와 정리 상태

Computer Use `@oai/sky`의 native pipe가 연결되지 않아 목록 조회 재시도·세션 재초기화 뒤에도 실패했고, Unified Computer Use inventory도 같은 native pipe 오류를 반환했다. 자체 Windows UI 입력 도구를 만들지 않았다. 실제 중점·결정·국민정신 화면, 클릭 영역·광택·줄바꿈·SHOW/HIDE·정상 플레이어 클릭은 미검수다.

최종 실행의 소유 PID 24356 종료를 확인했다. UI 연결 불가로 소유 프로세스를 강제 종료했으며 정상 GUI 종료로 표현하지 않는다. 최종 CIM 조회에서 HOI4·dowser·Paradox Launcher·GameOverlayUI·crash_reporter는 없고 기존 Steam PID 13492는 유지했다. Steam의 실제 「플레이」 버튼 표시는 관측하지 못했다. 처음 PID 5532의 강제 종료 직후 1초 조회는 아직 종료 중이었고 다음 조회에서 프로세스 부재를 확인했다. 이 두 시점은 `support-first-run-eventual-process-observation.json` 등에서 구분한다.

`TASK/restoration.json`에서 `dlc_load.json`의 SHA-256 `6c07dda995f2f0c69b877ab56e7ec7386682dc3d64bd42593664357c89478d17`, `settings.txt`의 `de97534fed2150477ee0b9144888b0794fc70379fe0a780c1e1c523f5b4f3088`이 각 사전 원본과 일치한다. 임시 launcher 모드 포인터도 제거했다. `TASK/final-process-profile-observation.json`은 종료 뒤 두 설정의 실제 현재 해시·프로세스 부재·기존 Steam 유지·UI 미관측을 다시 기록한다. `TASK/final-inventory.json`은 이번 작업 runtime 파일 20개·문서 9개의 위치/해시와 기존 저장 99개 전부의 내용 불변을 기록한다. 이 목록은 배포 allowlist가 아니다. 실행별 프로세스·종료 기록은 `TASK/runs/<case>/process*.json`에 남아 있다.

남은 확인은 실제 SHOW/HIDE·아이콘·줄바꿈·결정 클릭, 변경 전 저장 재로드와 280일 잔여 타이머, 자연 지지도 축적 후 정상 봉기, 10%/90% 경계, 실제 작전 시간/비용/위험/결과, DLC 없는 실행·멀티플레이와 장기 저장 동작이다. 새 정보국의 DLC 가드와 수치 정의만으로 이 검증을 대신하지 않는다.

기존 `docs/assets/korean-fascist-mobilization-validation-20260923/` 시험 PNG 4개(합계 약 0.82 MiB)는 정리 미결이며 이번 구현 범위에 포함하지 않아 그대로 두었다. 새 테스트·진단 파일은 저장소에 만들지 않았다. 커밋·푸시·업로드는 하지 않는다.
