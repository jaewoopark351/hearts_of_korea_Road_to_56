# 2026-10-10 왕정 선행 조건·환제국 물자 배치 업데이트 이식

## 요청과 결과

사용자의 원본 업데이트 이식 요청에 따라 직전 원본 af6fccf 이후 commit 4d8241e의 왕정 변경을 선택 이식했다. 한국 중점 15개 블록과 연락망 국민정신 2개 블록이 바뀐다. H1 자식 3개는 코드 변경 없이 기준점 이동을 상속하여 물자 가지 4개의 좌표가 이동한다. 이번 변경은 원본의 의도적인 진입·선행·보상 유지 정책 변경이며 파서 또는 RT56 버전 수선으로 설명하지 않는다.

생성기 관리 output 406개 중 common/national_focus/korea.txt와 common/ideas/HOK_KOR_royal_followup.txt 두 개만 바뀌고 나머지 404개는 바이트 그대로다. RT56 지역 대응, 기존 보상·기간·AI·그림·현지화·결정·ID와 나머지 중점 배치를 보존했다. 새 커밋·푸시·Workshop 업로드와 게임 실행은 이 요청에서 수행하지 않았다.

## 작업 기준선

| 항목 | 확인값 |
|---|---|
| 호환판 | feat/korean-focus-update-20260922 @ ecd265795982f29cddaa7610acf0427a66f0db6c |
| 시작 상태 | Git status의 descriptor.mod 수정 표시만 존재; working bytes와 raw HEAD bytes는 동일, 실제 diff 없음. 그대로 보존 |
| 원본 | feat/korean-focus-expansion-ai @ 4d8241e3cd33ebbceaca9650ab36b9891a22b56d, clean |
| 원본 부모 | af6fccf2248311c01565c796555ed334ec685015 |
| 읽기 전용 조사 | 2026-10-10 23:23:59–23:25:51 KST |
| 설치 게임 | Steam build 25205862, revision c01a3d507f10bd8c713e88234de69ca110618138 |
| 최신 로그 | 23:10:40 시작 donor 단독 실행, HOI4 1.19.3.0.c01a (0dab), system.log:273/274/312 |
| OS / 언어 / GUI | Windows 11 x64, l_korean, GUI scale 1.000000 |
| DLC | 최신 donor 로그 active 36개, dlc_load.json disabled DLC 없음 |
| RT56 | item 820260968, installed/latest manifest 7553774178744855191, 2026-10-09 08:58:55 KST 업데이트 |
| 한국 host base | A80FBC767C21902FC56EBBCA35DC3C120700E527B52EA98F3CFDF5221EB0EF90, 이전 한국 병합 base와 동일 |

실제 사용자 데이터는 C:/Users/jaewo/OneDrive/문서/Paradox Interactive/Hearts of Iron IV다. 현재 active playset 국뽕한국 test01은 donor 단독이다. 저장된 호환판 playset은 RT56·RT56 Korean Translation·이 호환판을 로드하고 donor는 포함하지 않는다. 외부 launcher descriptor의 물리 경로는 이 저장소를 가리키며 변경하지 않았다. 기록된 배열 순서를 실제 정의의 우선순위 증명으로 사용하지 않는다. 저장소 descriptor는 호환판 item 3796816200, RT56와 Korean Language 의존성, 1.19.*, replace_path 없음이다. 이 의존성 선언과 실제 translation 설정의 기존 불일치는 이번에 해결하지 않았다.

현재 donor 로그와 donor 문서의 초기 SHOW/HIDE 관측·68/0 정적 결과는 원본 실행의 증거다. 이 호환판의 새로운 실행 또는 형성 전 연락망 정신 유지 결과로 재사용하지 않는다.

## 선택한 동작 변경

| 묶음 | 대상 | 적용 |
|---|---|---|
| A2 | am_petition_calendar, am_granary_ledgers, am_relief_dispatches | 성리학 질서 완료 검사 제거 |
| A3 | am_regimental_returns, am_nco_examinations, am_reserve_cadre, am_mobilization_review | 성리학 질서 완료 검사 제거; regimental_returns의 군제개혁 검사도 제거 |
| A4 | am_technical_memorials, am_civil_service_practicum, am_merit_registers | 성리학 질서 완료 검사 제거; technical_memorials의 비변사 검사도 제거 |
| H2 | hw_dispatch_codes, hw_courier_relays, hw_signal_logs, hw_relay_exercises | 환제국 형성 완료 검사만 제거 |
| H1 | hw_provincial_inventory 및 상대 자식 3개 | 실제 선행·위치 기준을 KOR_empire_of_hwan으로 바꾸고 상대 x25→6, y1 유지 |
| 연락망 정신 | hw_courier_service_1/2 | 환제국 미형성 cancel 제거; 새로운 정부·독립·영토 cancel을 추가하지 않음 |

위 접미 중점과 정신은 모두 HOK_KOR_ 접두사를 유지한다. A2/A3/A4의 original_tag KOR·neutrality·내전 없음은 그대로다. A1 네 중점의 성리학·비변사 검사도 그대로다. H2는 original_tag·내전 없음·독립·RT56 병합 영토 보유/완전 통제 조건을 유지한다. 원본의 8주 조건으로 덮어쓰지 않고 기존 RT56 전체 지역 15주 대응을 보존한다. H1의 환제국 형성·독립·영토 조건은 유지한다.

표시되는 기존 prerequisite와 군사 내부 AND 합류, 35일(cost5), 보상·AI factor2, cancel_if_invalid/continue_if_invalid/available_if_capitulated는 H1 부모 교체 외에 그대로다. 완료 검사 완화로 A 정책과 H2를 더 일찍 진행할 수 있지만 표시된 연결과 상태 조건은 계속 적용된다. H1은 기존 왕의 귀환 선행 대신 실제 환제국 형성을 선행으로 요구하여 형성 이후에 진입한다. 왕정 묶음 자체의 각 35일과 4중점 모듈 140일 분량은 바뀌지 않는다. 전체 정책 도달 시점은 선택 순서·형성/영토 확보에 따라 달라지므로 정상 플레이로 검증해야 한다.

연락망 I은 initiative +10%, army speed +5%; II는 +15%, +10%를 유지한다. I→II 교체와 직접 II 취득 보상도 유지한다. 이 두 정신을 형성 전 유지시키는 것이 원본의 명시적인 변경이다. 다른 환제국 정신 6개의 형성 취소는 그대로다.

H1 기본 좌표는 (211,5) → (210,6)/(212,6) → (211,7)에서 (184,11) → (183,12)/(185,12) → (184,13)으로 이동한다. 환제국 기준 (178,10)에 상대 (6,1)을 적용했다. 왕정 완료 HIDE는 기존 기준 연쇄의 −101x를 한 번 상속하여 (83,11) → (82,12)/(84,12) → (83,13)이다. SHOW와 초기 HIDE는 기본 좌표를 쓴다. 다른 456개 위치·7개 직접 offset·지속적 중점 패널·바로가기는 그대로다. 세부 기계 명세와 주변 가지·연결·실제 화면 검수 한계는 [호환판 좌표 기록](../HOK_KOREAN_ROYAL_LAYOUT_COORDINATES.md)에 구분했다.

## 출처와 생성 소유권

새 [royal lock](../../tools/hok_royal_update_lock.json)은 source 4d8241e와 부모 af6fccf의 두 immutable Git blob, CRLF checkout, 이전/새 호환판 출력 해시, 정의별 원본/포트 편집 범위를 고정한다. H2 원본과 포트는 영토 조건 길이가 다르므로 두 span을 구분하고 제거한 완료 검사 외의 포트 문구를 보존한다. Git 원본 전체 차이가 해당 span들로만 재현되는지 검사한다. 기존 소스 lock 9개의 바이트와 각 계층을 그대로 보존하며 새 계층을 tooltip→선행조건 다음에 적용했다.

변경된 원본 docs 7개는 [바이트 보존 사본](../upstream/hok-royal-update-20261010/README.md)으로 별도 기록한다. source_snapshot.py가 Git blob과 사본의 SHA/크기/경로를 다시 검사한다. 그림·root README·원본 전체 runtime·이전 소스 pins를 갱신하지 않았다. 생성 파일을 손으로 수정하지 않고 build_korean_focus_update.py로 재생성했다. 원장도 build_integration_manifest.py로 재생성하여 두 기존 행의 ADD/OVERRIDE 분류와 historical host base를 유지했다.

| 경로 | 원본 Git object SHA-256 | 원본 checkout SHA-256 | 이전 포트 → 새 포트 SHA-256 |
|---|---|---|---|
| common/national_focus/korea.txt | E254896264A5FDF628B92FFEDC48007215259C70F97B9DB80761B69ECD65B3C5 | 572C035B21A79D89F7E8FA55AEE353F12B4230816CBFD491FF0667EFC09AC007 | EB78279B778326F1EC6B08932533CE2FDEEA618C6872610A0A7746E0FDE50AD4 → 332DE63A191236AE44C0F5BB87706095002D69C08B5A770DD503D0293323894A |
| common/ideas/HOK_KOR_royal_followup.txt | 899EFE1BF2ABCB983D9D9E29A411172B7A991EDD02B20D7B53D913E593EF2A79 | 409BB42B63602F01B15800EF7BD92BB0C85D7EDC56FC5E4A4A26DA2A9625D5FA | 985B07C6D64F3039AE398B83764DB9312B328D23285AC23967CE0F5FBD62E2F0 → 409BB42B63602F01B15800EF7BD92BB0C85D7EDC56FC5E4A4A26DA2A9625D5FA |

선택한 왕정 정신 파일은 RT56/vanilla에 없고, 15개 왕정 정신 ID와 am/hw 중점 ID28개는 RT56/vanilla common 및 두 언어 모드에 충돌이 없었다. 한국 focus의 exact path 충돌은 기존 OVERRIDE 정책을 유지한다. 설치 vanilla japan focus:316–324와 RT56 korea focus:78–85에서 prerequisite/relative_position_id 분리를 확인했다. vanilla ideas/japan:1425–1448와 RT56 ideas/r56_japan:554–571은 country spirit의 allowed/allowed_civil_war 및 cancel 없는 동일 context 예제다. 이는 스키마 근거이며 실제 정신 지속 증명은 아니다.

## 검증 결과와 남는 범위

- python -B tools/build_korean_focus_update.py: exit0, 406개 관리 output 중 두 파일 생성·나머지 404개 바이트 동일.
- python -B tools/build_integration_manifest.py --apply: exit0, 원장1,417개·충돌73개. ADD199/ASSET_COPY1097/BINARY_MERGE18/OVERRIDE9/THREE_WAY_MERGE31/USE_RT5663. 최종 SHA-256 68B59579D9A032F2A131B1D9B7CD7343B9E9EC1B6D8BAE5B55B2B634E6B87E2B. 두 runtime 출처 행 외에 descriptor 행은 실제 보존된 LF working bytes의 SHA를 기록하며 descriptor 파일을 수정한 것이 아니다.
- python -B tools/check_korean_second_wave.py --royal-self-test: exit0, 현재 positive fixture 통과·의도적 회귀 **57개 거부**(직전 선행조건16 + 왕정41). immutable source와 전체 ordered AST, 14중점의 완료 검사16개 제거, 15변경 블록·460개 ID/순서, 보상/정치/RT56 전체 지역/AND 보존, 물자 네 좌표·단일 조건부 상속, 연락망 두 정신 취소/수치 및 maintained JSON을 검사한다. production writes와 외부 테스트 파일 없이 메모리/표준 출력만 사용했다.
- tools/check_korean_second_wave.py --check: exit1, 기존 material/prose 보존 gate의 **material-cycle update changed preserved runtime: descriptor.mod**에서 차단. 과거 descriptor pin은 CRLF D68DCE620EA3DDDE422F26F2E5155E4D52F35AC4B2EBE1224DC71E07035141CB를 요구하지만 시작부터 존재한 actual LF는 AA150D6CE82A7779C3D4C3FCDC962A82FA269327F005330B565723CA87BBE247다. HEAD object와 working bytes가 실제로 같은 점을 함께 확인했다. scoped 옵션은 이 관련 없는 과거 assertion을 변경하지 않으면서 새 왕정 계약만 독립 검사한다. 전체 self-test의 모든 과거 사례 통과를 주장하지 않는다.
- python -B tools/validate_port.py: exit1, **16 PASS / 0 WARNING / 5 ERROR**. 한국 생성기·expansion·원장 재현·스크립트 구조·descriptor 의미·현지화·logical ID·만주 closure 등16gate 통과. 기존 host source drift 네 gate(map/shared/East Asia/doctrine)와 위 descriptor 바이트 보존 gate 하나는 실패했다. 이번 변경 subsystem의 scoped 성공과 aggregate 실패를 구분한다.
- Python 구문 확인 및 git diff --check 통과. 시작/종료(23:36:11 KST) 원본 HEAD/두 runtime 해시·RT56 manifest/descriptor/한국focus·vanilla 스키마 파일·호환판 HEAD/descriptor bytes 동일. Steam timetouched 메타데이터만 변동하고 선택 source 내용은 변하지 않았다.


현재 RT56 manifest에서 과거 고정 입력의 drift가 이미 존재한다. 직접 선언한 56개 source pins 중 49개 일치, vanilla17/17 일치, RT5632/39 일치다. 기존 JAP decisions/history·map railways·generic MIO·1936 bookmark·generic advisors·GER history 7개와 별도 ledger intelligence agency drift는 이번 source 변경 전부터 있다. historical source pins를 최신 hash로 바꾸어 검사 실패를 숨기지 않았다. 상세 기존 해시는 [직전 선행조건 이식 기록](2026-10-10-korean-focus-prerequisite-port.md)에 있다.

전체 RT56 기준선 재병합은 별도 미완료 작업이다. 기존 KOR history war_support 0.1과 생성 기대 0.05의 불일치도 이번 왕정 범위 밖이며 현재 GER drift가 해당 검사에 먼저 걸릴 수 있다. descriptor의 actual bytes가 HEAD와 같아도 옛 material/prose preservation pin이 CRLF SHA를 요구하는 별도 실패가 있을 수 있다. descriptor bytes와 기존 assertions는 그대로 보존했다.

호환판의 cold start, 초기/완료 후 SHOW/HIDE 화면, 아이콘·명판·연결선·패널·바로가기, 형성 전 H2 정상 착수·35일 완료와 정신 I/II 지속/교체, A 갈래 차단조건과 병렬 진행, H1 형성 전 차단/형성 후 영토 진입, AI·저장·DLC·멀티플레이는 이번에 검증하지 않았다. 현재 구현·정적 계약의 성공을 전체 호환성 또는 런타임 완성으로 표현하지 않는다.
