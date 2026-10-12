# 2026-10-12 재벌·시민사회 업데이트 선택 이식

## 요청과 결과

사용자가 C:/hoi/hearts_of_korea의 최신 원본 업데이트를 이 호환판으로 가져오도록 요청했다. 직전 이식 원본 4d8241e 이후의 d4031aaa 변경 중 한국 런타임 31개 파일을 선택 이식했다. 새 파일 29개와 기존 파일 2개를 반영하고, RT56 지도·만주 조건·공용 시스템과 호환판의 기존 독자 수선을 보존했다. 이것은 원본의 의도적인 내정 콘텐츠 확장이며 호스트 drift 수선이나 자체 재설계가 아니다.

플레이 가능한 한국 중점은 460 − 구 협력 노드 1 + 신규 13 = 472개다. 재벌·시민사회 영향력, 비리·기관 장악, 세 산업정책, 결정/mission 13개, 국민정신 20개, 이벤트 11개, 현직 지도자 패널과 그림·현지화가 포함된다. 원본 README/.gitattributes·descriptor·전체 runtime 폴더는 복사하지 않았다. 원본이나 Steam 관리 파일·런처·사용자 설정을 수정하지 않았고, 이번 게임 실행·커밋·푸시·Workshop 업데이트는 수행하지 않았다.

## 작업 기준선

| 항목 | 확인값 |
|---|---|
| 호환판 시작 | feat/korean-focus-update-20260922 @ 71fb843c0b4f6b3521062ffa07d23d5963a0514d, clean |
| 원본 | feat/korean-focus-expansion-ai @ d4031aaa0c1f85bb89b0e6ca21d041beade8bd26, clean |
| 원본 부모/직전 이식 | 4d8241e3cd33ebbceaca9650ab36b9891a22b56d |
| 설치 게임 | Steam build 25205862, 1.19.3.0.c01a; 최신 system.log는 2026-10-12 19:17:20 KST의 donor 단독 checksum 575f |
| DLC·환경 | 최신 donor 로그 active DLC 36개, Windows 사용자 데이터 C:/Users/jaewo/OneDrive/문서/Paradox Interactive/Hearts of Iron IV |
| RT56 | item 820260968, installed/latest manifest 7553774178744855191, 2026-10-09 08:58:55 KST 업데이트 |
| 한국 host focus | A80FBC767C21902FC56EBBCA35DC3C120700E527B52EA98F3CFDF5221EB0EF90; 직전 병합 base와 동일 |
| 호환 descriptor | AA150D6CE82A7779C3D4C3FCDC962A82FA269327F005330B565723CA87BBE247; LF·기존 item 3796816200·RT56/Korean Language·1.19.*; path/replace_path 없음 |
| RT56 descriptor | 5B323861ABD63E31CB896277E3EA58BA4BCD9FCEEDA957B50792065E42E03F61; history/states·map/strategicregions replace_path 유지 |
| 원본 descriptor | 3FBC6868A7D95BACD6B55AF71593A61AF3A7EADA5654D46CC4C828422ECA032A; provenance item 3793992662 |

현재 활성 dlc_load.json은 HOK donor 단독이다. 저장된 호환판 구성은 RT56·RT56 Korean Translation·이 호환판이고 donor를 포함하지 않으며, 외부 호환 .mod의 경로는 이 저장소다. 그 descriptor 해시는 A486F1BD484486BE9BE4668E61C7B7B8DAC292C2E7474EC0258BF6F02C885BF4다. 저장된 순서를 실제 정의 우선순위의 증명으로 사용하지 않는다. 이식 전에 31개 donor working checkout 해시가 새 immutable lock과 전부 일치함을 확인했다. 실제 RT56 playset 실행이나 새로운 모드 checksum은 이번에 수집하지 않았다. Korean Language 선언과 translation 구성의 기존 불일치도 그대로다.

## 동작과 병합 판단

- 산업·사회협약은 독립당 또는 자유당 단독집권 이후의 민주 가지로 진입하며 150PP와 패널·첫 결정 범주를 제공한다. 신규 13개 중점의 cost5, 보상, AI, 정치·내전·항복 조건을 원본 그대로 가져왔다.
- 네 country 변수는 최초 60/35/20/40으로 초기화되고 0–100으로 제한된다. 명시적인 KOR startup/monthly scope가 초기화·구 완료 이력 등록·tier 동기화를 수행한다. 패널 조작을 해금하기 전에도 초기 영향력 tier 정신이 적용되는 것이 원본의 의도다.
- 재벌 협력·시민 개혁·공공 소유 정책은 서로 배타적이다. 지원/견제의 GUI와 결정은 각각 50PP를 한 번만 차감하고 공통 90일 대기를 사용한다. 조달 계약·사고·감사·회복과 검찰 장악 위기 흐름, 비용·기한·flag·event 예약 순서를 유지했다.
- KOR_cooperation_with_the_jaebeol의 플레이 가능한 노드만 제거했다. 별도의 unavailable/AI0/빈 보상 shared_focus에 같은 ID를 한 번 등록하고 once helper가 구 완료 또는 새 산업협력 이력을 처리한다. 이것은 참조 유지이며 호환판 기존 저장 지원을 증명하지 않는다.
- 기존 삼성·현대·선경 주문의 visible/available OR 6개에 새 산업협력 완료와 협력 이력 flag를 추가했다. 기존 100PP·90일·보상·재사용 규칙과 길들이기 대안은 보존했다.
- 원본의 merchant navy x−2→0 이동과 상대 British 후속의 이동을 함께 반영했다. 기존 457개 중점의 기본 좌표는 그대로이고, 새 13개는 x132–139/y6–12에 놓인다. 완성 후 민주 HIDE 이동은 기준점에서 −35x를 한 번 상속한다. [472개 좌표 기록](../HOK_KOREAN_CIVIC_LAYOUT_COORDINATES.md)과 [JSON](../data/HOK_KOREAN_CIVIC_LAYOUT_COORDINATES.json)은 역사적 왕정 명세와 분리했다.
- inlay는 (1050,1400), 500×670이며 지속적 중점 패널·8개 바로가기를 보존했다. 고정 UI의 정적 bounds와 실제 엔진의 연결선·카메라·클릭 영역 검증은 구분한다.

신규 HOK_KOR_civic/HOK_KOR_CIVIC 관련 ID·namespace는 현재 RT56·vanilla와 두 localisation 모드에 충돌이 없었다. 변경 경로 중 기존 korea.txt만 RT56과 exact-path 충돌하며 기존 HOK 우선 OVERRIDE 정책을 유지했다. 기존 한국 지리 병합을 다시 donor whole file로 덮어쓰지 않았다. vanilla on_monthly_GER(00_on_actions.txt:5920), on_monthly_NOR(09_aat_on_actions.txt:717), Japan focus inlay, nationalfocusview.gui의 focus_tree_scripted_window_container(:188–191)가 동일 context 스키마 근거다. RT56의 on_monthly_KOR나 global nationalfocusview.gui override는 없었다. 이러한 소스 근거가 실행 증명은 아니다.

## 생성 소유권·출처·자산

[독립 civic lock](../../tools/hok_civic_update_lock.json)은 원본/부모 Git blob·raw/checkout SHA·size, 이전/새 호환 출력 SHA, 전체 원본 diff 목록과 6개 focus hunk·3개 decision hunk를 고정한다. 기존 historical lock 10개의 바이트는 그대로다. source_snapshot.py는 원본 diff가 이 31개 런타임·23개 문서/소재·제외한 root 2개로만 구성되는지, 각 frozen source와 immutable Git object가 같은지 검사한다.

build_korean_focus_update.py의 마지막 계층에서 기존 royal까지의 출력에 정확한 hunk만 적용한다. 기존 KOR_decision.txt의 map-ID/Manchuria 이전 출력도 historical snapshot과 기존 migrator로 먼저 재현한 뒤 civic 변경을 적용한다. 관리 출력은 406→436개이며 이전 출력 405개를 바이트 그대로 보존했다. migrate_hok_ids와 역사적 확장/2차 검사기는 실제 변경된 두 파일만 exact hash 기반으로 역산하므로 새 내용을 없애거나 과거 pins를 느슨하게 만들지 않는다.

| 분류 | 경로/범위 | 처리 |
|---|---|---|
| OVERRIDE | common/national_focus/korea.txt | 기존 RT56 base·지역 병합 유지 + 원본의 6개 hunk |
| ADD의 선택 갱신 | common/decisions/KOR_decision.txt | 이전 migrated 출력 + 3개 hunk, 기업 주문 OR만 변경 |
| ADD | 신규 text 21개 | 결정·범주·효과·trigger·ideas·event·inlay·shared-focus·GFX/GUI·현지화 6개 |
| ASSET_COPY | 신규 DDS 8개 | vanilla 유래 UI/사건 6개와 작은 결정 그림 2개, 바이트·포맷 유지 |

29개 추가 경로에 RT56 exact-path 충돌은 없다. 통합 원장은 1,446행·기존 충돌73개이며 ADD220/ASSET_COPY1105/BINARY_MERGE18/OVERRIDE9/THREE_WAY_MERGE31/USE_RT5663다. 생성 CSV SHA-256은 FFEA39379FC30BD800E9308B9035A74D69C1A24FC12362D5523F68B00451D98A다.

| 변경 출력 | SHA-256 |
|---|---|
| korea.txt | 7AE9465EE5DA4E3FC59CCAADC36E1F492BC81AEFA715D11992229D383F7AE9D8 |
| KOR_decision.txt | F0B90524C98B7CD3D45D977462C5EDCA7D1BA5FB3BCFD7B9C0E05BFA64F6673C |

[보존 원본 문서·소재](../upstream/hok-civic-update-20261012/README.md)에 설계·의도적 개정·원본 실행 이력·그림 출처를 함께 남겼다. 원본 실행 성공을 이 호환판의 결과로 재사용하지 않는다. 기존 한국 초상·회사 로고·정책 그림과 Ultimate HOI4 GFX/Paradox 귀속을 유지한다. 새 이미지 생성·다운로드·recolor는 하지 않았다. 51×40 category와 32×32 파란 support/suppress 그림, paired localisation BOM/header/동일 contributor note를 보존했다.

광택 26개는 기존 호환판 정책에 따라 HOK_KOR/shine_overlay.dds 대신 vanilla gfx/interface/goals/shine_overlay.dds provider를 참조한다. HOK-owned base/mask는 로컬에 남는다. 두 overlay SHA는 BB416649358C73D34AACD46BAD61BC44211FAC8111627B56E25F385AD98F4448로 같았다. UI effectFile의 .lua 이름은 target vanilla registry의 기존 키이며 실제 .shader 파일까지 확인한다. 검사의 초기 물리 .lua 파일 가정은 source 근거(goals_shine.gfx:8, core.gfx:46)에 맞춰 수정했고 gameplay나 shader를 복사·수정하지 않았다. 기존 source credits는 새로운 사용 허가나 일반 재배포 허가의 주장으로 바꾸지 않았다.

## 검증과 한계

Python 3.12.14는 C:/Users/jaewo/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe이며 -B로 실행했다. 새 테스트 파일·로그 사본·fixture·pycache를 저장소에 만들지 않고 메모리/표준 출력으로 확인했다.

- build_korean_focus_update.py: exit0, 정확히 31개 출력 작성·이전405개 동일.
- build_integration_manifest.py --apply: exit0, 위 1,446개 분류·해시 재생성.
- check_korean_second_wave.py --civic-check: exit0. 31개 source/전체 ordered AST·405개 보존·472 playable/구 ID 등록·초기화/clamp/tier·scope·비용/공통 대기·정책·legacy·localisation·그림/UI closure 통과.
- --civic-self-test: exit0, 현재 positive fixture 통과·의도적 회귀 26개 거부. --royal-self-test: exit0, 정확한 civic 역산 뒤 기존 왕정/선행조건 회귀57개 거부.
- check_korean_focus_update.py --check와 migrate_hok_ids.py --list: exit0. 이전 확장/AI/그림 계약 유지, 이식된 KOR_decision은 already-migrated이며 쓰기 없음. 별도 AI의 would-normalize는 실행하지 않았다.
- 독립 최종 검토에서 migrator의 civic 판별 범위를 정확한 final SHA로 좁혔다. 메모리 main(--list) fixture6개: 현재 civic/기존 migrated 보존, pinned original/legacy migration/canonical LF 허용, 독립 수정 거부 모두 통과. 기존 정상 이전 입력을 막지 않으며 production writes는 없다.
- 구 협력 ID의 잔여 참조도 전수 검색했다. AI plan/strategy·달성 선행·강제 완료 참조는 없고, shared 등록·기업 주문 OR·legacy helper OR만 남는다. 기존 historical AI의 독립당 진입은 유지되며 새 13개 모듈의 실제 선택 시점은 미검증이다.
- 최종 전체 검사(이전 도구 판별 수선 포함)는 135.779초, exit1·18/0/5로 위 기존 오류만 재확인했다. 종료 시 donor HEAD/31개 live checkout SHA·RT56 manifest/descriptor/한국 focus SHA·호환판 HEAD/descriptor와 기존 lock10개가 시작과 같았다. Git 변경99개 중 runtime은 정확히31개다.
- Python tools15개 memory AST 구문 확인 및 git diff --check 통과. Git의 도구 LF→CRLF checkout 안내는 actual file 오류나 변환 수행이 아니다.
- python -B tools/validate_port.py: exit1, **18 PASS / 0 WARNING / 5 ERROR**. 한국 생성·civic·기존 확장·ID 이전·원장·200개 구조·72개 locale/5,450개 key·logical ID·만주 closure 등 통과. 기존 map/shared/East Asia/doctrine source drift 네 gate와 descriptor preservation pin 하나만 실패했다. 초기 aggregate의 새 shader 검사 false failure는 검사기에서 보정하고 전체 검사를 다시 실행했다.

작업 전 2026-10-11 기록은 17 PASS/0 WARNING/5 기존 ERROR였다. 이번 pre-implementation aggregate 시도는 제한 시간/출력 수집 문제로 완료 결과를 얻지 못했으므로 새 측정 기준선으로 주장하지 않는다. 기존 소스 pins와 source drift 기록을 보존했고 변경 diff에서 runtime31개 외의 게임 파일 변경이 없음을 확인했다.

최신 RT56의 기존 7개 입력 drift(railways, generic MIO, bookmark, generic advisors, JAP decisions/history, GER history)를 해결하거나 historical pins를 새 해시로 바꾸지 않았다. 기존 descriptor actual LF SHA와 material/prose preservation CRLF pin D68DCE620EA3DDDE422F26F2E5155E4D52F35AC4B2EBE1224DC71E07035141CB의 불일치도 그대로다. 이식 범위 검사 성공을 전체 RT56 기준선 재병합 완료로 표현하지 않는다.

cold start와 실제 RT56 초기/완료 SHOW/HIDE 화면·패널/지도자/클릭·정상 민주 진입과 35일 완료·월간 상태 전이·사고/복구/정변·AI·장기 진행·DLC off·save·멀티플레이는 이번에 검증하지 않았다. map-ID 이전 때문에 신규 게임 전용이라는 기존 지원 범위를 유지하며, 구 shared ID 보존만으로 기존 저장 호환을 주장하지 않는다. 외부 업로드는 별도 요청 범위다.

## 2026-10-12 커밋 준비

사용자가 전체 변경의 커밋·푸시와 영어 commit subject/body를 명시적으로 승인했다. 준비 시 core.autocrlf=true에서 새 civic snapshot/lock과 LF 출력의 checkout 바이트가 달라지는 조건을 확인하여 .gitattributes에 원본 snapshot -text, 독립 lock LF, 23개 생성 text의 실제 LF/CRLF 규칙을 추가했다. 게임 출력·보상·source pins는 변경하지 않았다. 이전 구현 종료 기록의 변경99개에 attributes1개가 추가되어 커밋 대상은100개이며 runtime31개는 그대로다.

스테이징된 54개 immutable snapshot과 독립 lock1개의 blob, 생성 runtime31개의 checkout filter 결과 등86개 바이트 검사는 모두 고정 SHA와 일치했다. staged diff --check는 새로 추가한 원본 보존 사본의 기존 trailing whitespace와 원본과 동일한 effects/events의 EOF 빈 줄 때문에 exit2다. 실제 이식 부분의 기존 diff --check 통과와 구분하며, immutable source를 정규화하거나 소스 해시를 바꾸어 숨기지 않았다.
