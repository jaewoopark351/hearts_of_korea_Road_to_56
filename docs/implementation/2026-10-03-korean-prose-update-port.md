# 2026-10-03 한국 국민정신·디시전 설명 업데이트 이식

상태: 설명 124개/채널·28개 파일 선택 이식 및 정적 검사 완료. Aggregate **20 PASS / 0 WARNING / 1 기존 ERROR**. 이번 작업의 호환판 실행 검증은 미실행이다.

사용자의 “원본 모드 업데이트 되었어, 베껴올 수 있겠어?” 요청에 따라 최신 HOK의 실제 변경을 확인하고 한국 설명 업데이트를 선택 이식한다. 신규 콘텐츠 설계·보상 변경·원본 전체 복사·커밋·게시 작업으로 확대하지 않는다.

## 선택 변경과 보존 범위

원본 HEAD 이후 미커밋 설명 변경은 현지화 28개 파일, 14쌍이다. 채널당 국민정신 88개, 디시전 28개, 연결 범주 8개의 `_desc` 본문을 수정해 총 124개 설명·248개 값을 반영한다. 파시즘·공산주의 문체 후속 수정도 실제 선택 원본에 포함된다. 현재 두 채널은 `l_english`와 `l_korean` 헤더 아래 같은 한국어 본문을 제공한다. 별도 영어 번역을 작성하지 않는다.

원료 순환체계 I·II 강화, 긴급 지원 결정·정신·그림은 이전 [원료 순환체계 이식](2026-10-03-korean-material-cycle-port.md)에 이미 들어 있으므로 다시 변경하지 않는다. 이번 변화는 명칭·키·버전·키 순서·중점 설명·이벤트 설명·`_tt`·게임 효과·AI·지도·그림을 보존한다. 다음 여섯 설명은 최신 원본에서도 그대로 유지된다.

- `HOK_KOR_cmn_material_cycle_1_desc`, `HOK_KOR_cmn_material_cycle_2_desc`
- `HOK_KOR_cmn_emergency_material_cycle_boost_desc`, `HOK_KOR_cmn_emergency_material_cycle_desc`
- `HOK_KOR_rapid_repairs_spirit_desc`, `HOK_KOR_air_maintenance_spirit_desc`

면허협정 참가 정신의 정부·지도국 상실 조건은 게임 정의의 OR에 맞춰 “또는”으로 설명한다. 디시전 배경과 실행 목적을 보강하고 필요한 비용·기간·재사용·취소 안내를 보존한다. 실제 효과의 오류를 고쳤다는 뜻은 아니다.

만주 설명에는 [ADR-0005](../decisions/0005-korean-second-wave-regional-integration.md)의 기존 지역 suffix 24개/채널과 기여자 주석을 재적용한다. 원본 문안을 그대로 덮어써 RT56의 분할 주 안내를 잃는 방식은 채택하지 않는다. 지역 사업의 효과·대상·해금 자체는 변경하지 않는다.

## 현재 기준선

| 항목 | 이번 읽기 전용 관측 |
|---|---|
| 조사 날짜 | 2026-10-03 KST; 전체 production 해시 캡처 23:02:50 |
| 호환판 branch / HEAD | `feat/korean-focus-update-20260922` / `84f354f007c814f279947dfa7f0ad19eaaae0eba` |
| 작업 시작 상태 | 최초 `git status --short` 빈 출력. 후속 캡처의 untracked upstream 사본은 이번 작업이 만든 입력 사본 |
| donor branch / HEAD | `feat/korean-focus-expansion-ai` / `43dbb38ac2553942e898e6093a2a46f0430995fc` |
| 실제 선택 원본 | HEAD 위의 미커밋 locale 28개, prose 계획·구현 기록 2개. HEAD 자체에 최신 문안이 있다는 뜻은 아님 |
| 설치 HOI4 | `Operation Postern v1.19.3.0.c01a (5632)` / raw `1.19.3.0`, Steam build `25205862` |
| RT56 | `820260968`, installed/latest manifest `7475007536894105204`, timeupdated `1788822864` |
| RT56 descriptor SHA-256 | `5B323861ABD63E31CB896277E3EA58BA4BCD9FCEEDA957B50792065E42E03F61` |
| 현재 active playset | `한국test01`, donor만 활성. `dlc_load.json`도 `mod/hearts of korea.mod`만 기록 |
| 기존 donor 실행 로그 | 22:26의 `1.19.3.0.c01a (4e60)`, DLC 36개·mod 1개. 이번 포트 실행 결과가 아님 |
| 저장된 호환 playset | 비활성 `Road to 56 한국 테스트`: 위치 0 호환판, 1 RT56 Korean Translation `2769576030`, 2 RT56 |
| 호환 playset donor 여부 | 저장된 활성 mod 목록에 donor 없음 |
| OS / 언어 / 화면 | Windows 11 x64, `l_korean`, 1280×720, GUI 1.0 |
| 실제 사용자 데이터 | `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV` |

저장된 순서는 런처 기록이며 파일별 유효 precedence의 실행 증거가 아니다. 사용자의 donor 세션·설정·저장을 변경하거나 HOI4를 실행하지 않았다.

호환 descriptor는 `0.1.0-dev`, `supported_version="1.19.*"`, RT56와 Korean Language 의존성, 기존 호환 item `3796816200`을 유지한다. repository에 `path`·`replace_path`가 없으며 외부 launcher `.mod`는 이 작업 root를 가리킨다. donor는 `3793992662`와 `C:/hoi/hearts_of_korea`를 사용한다. RT56의 states/strategicregions replacement와 번역 모드의 localisation replacement를 확인했으며 변경하지 않는다. 설치 Korean Language `2743487021`은 `1.17.*`를 선언하고 저장된 호환 playset에 없다. 선언 의존성과 실제 번역 구성의 차이는 기존 [localisation 계약](../decisions/0003-localisation-contract.md)의 미확정 사항이다.

## 출처와 통합 방식

선택 파일은 두 언어의 `common_followup`, `communist_development`, `communist_governance`, `communist_policy`, `constitutional_followup`, `democratic_expansion`, `fascist_followup`, `fascist_mobilization`, `fascist_procurement`, `fascist_staff`, `industry_expansion`, `manchurian_followup`, `military_expansion`, `royal_followup`이다.

[고정 사본](../upstream/hok-prose-update-20261003/README.md)과 [독립 lock](../../tools/hok_prose_update_lock.json)에 source 바이트·크기·SHA-256, immutable donor base blob, 수정 설명 키, 직전 port 출력 해시를 기록한다. 기존 source/artwork/second-wave/policy/localisation/material lock 여섯 개를 최신 donor로 다시 고정하지 않는다. 원본의 28개 checkout은 BOM·CRLF를 보존하며 runtime에 생성기를 통해 반영한다. 만주 두 파일은 기존 지리 안내를 포함하는 검토된 출력이다.

각 파일은 기존 `ADD` 정의 위의 reviewed prose overlay다. RT56·vanilla에서 해당 exact path 및 locale key 충돌은 발견하지 않았다. 선택 원본의 716개 key/채널은 설치 RT56 Korean Translation·Korean Language 현지화에서도 충돌이 없었다. RT56 번역 layer와의 기존 최종 로드 계약은 별도의 실행 확인 대상으로 유지한다. [통합 원장](../audits/2026-09-06-production-file-classification.csv)은 직전 출처와 새 동결 원본·최종 output 해시를 구분하며, 미커밋 문안을 donor 커밋으로 표기하지 않는다.

전체 source inventory를 비교해 확인한 의미 차이 36개 중 이번 업데이트는 locale 28개뿐이다. 나머지 8개는 과거부터 있던 AI·일본 연결·아이콘 매핑·history·광택 차이이며 이번 범위에 합치지 않는다. donor 일본 민주 분기 8개와 donor-local `shine_overlay.dds`도 기존 RT56 ownership·공유 광택 정책에 따라 이식하지 않는다. 원본의 root README·AGENTS 전체를 덮어쓰지 않으며 문안에 적용된 author 지침은 선택 prose 문서에 보존한다.

## 검증 기록

작업 전 `python tools/validate_port.py`를 실제 실행했다. 결과는 **19 PASS / 0 WARNING / 2 기존 ERROR**다. 하나는 KOR history의 MtG 전쟁지지도 0.1과 doctrine 생성기 기대 0.05의 기존 불일치다. 다른 하나는 선행 `84f354f`의 AGENTS 변경 이후 통합 원장이 갱신되지 않은 상태다. 기존 AGENTS 원장 hash는 직전 commit의 CRLF checkout과 같으며, 재생성한 hash는 현재 HEAD의 CRLF checkout과 같다. 이번 작업은 AGENTS를 편집하지 않았다. 최신 설명을 반영하기 전의 결과이며 과거 20 PASS 기록으로 대체하지 않는다.

| 검사 | 실제 결과 |
|---|---|
| 생성기 적용 | 관리 output 406개 중 locale 28개만 갱신 |
| `check_korean_second_wave.py --check` | PASS. 채널당 124개 설명, key/version/order, 여섯 보호 설명·기여자 주석·ADR-0005·기존 보상과 scope 계약 확인 |
| 기존 회귀 `--self-test` | PASS. 의도적 회귀 35개 거부; production 수정 없음 |
| 전체 production 보존 | 기준선 1,352개 중 locale 28개만 hash 변화, 다른 1,324개 동일; 추가·삭제 0 |
| 독립 출력 검토 | 26개는 frozen donor 바이트와 동일, 만주 한 쌍만 기존 지역 suffix·주석 유지; runtime 값 변화 정확히 248개 |
| descriptor·기존 lock | descriptor와 여섯 historical lock 해시 동일 |
| source 재확인 | 선택한 원본 30개 모두 동결 해시와 동일; RT56 installed/latest manifest·descriptor 동일 |
| diff whitespace | `git diff --check` exit 0 |
| `python tools/validate_port.py` 최종 | **20 PASS / 0 WARNING / 1 기존 ERROR**, exit 1. 통합 원장 갱신 누락은 해소했고 기존 KOR history/doctrine 생성 불일치는 보존 |

테스트·진단 기록은 `C:\hoi\test\20261003-upstream-prose-port\`에 저장한다. 새 lock SHA-256은 `FA480E4921F3D97CB7B2380A9A17D6D2A0E3C847D23EE0943A18C4FB001D3809`다. 원장 1,417개·기존 exact-path 충돌 73개와 분류 수량을 유지한다 (`ADD` 199, `ASSET_COPY` 1,097, `BINARY_MERGE` 18, `OVERRIDE` 9, `THREE_WAY_MERGE` 31, `USE_RT56` 63). 이번 원장 diff는 locale 28행과 위 기존 AGENTS 출처 갱신 1행이다. 최종 원장 SHA-256은 `3AFC58EE95C46421C913CB9B5B22B673E5276EA0B46355DA69855BF37505D771`이다.

기존 KOR history는 MtG 분기에 `set_war_support = 0.1`을 유지하고 생성기는 0.05를 기대한다. 이 설명 이식으로 gameplay를 바꾸거나 assertion을 약화하지 않았으므로 aggregate 전체가 clean 통과했다고 보고하지 않는다. 구조 185개 UTF-8 파일, locale 66개 파일·5,062 key, logical-ID·기존 지도/한국 콘텐츠·출처 gate는 이번 최종 검사에서 통과했다.

이번 문안의 실제 툴팁 길이·줄바꿈·정부/결정 상태별 UI·번역 layer의 유효 로드·cold-run은 **UNPROVEN**이다. donor의 기존 정적 검사·실행 로그를 호환판의 결과로 사용하지 않는다. 게임 동작·저장·DLC·AI·멀티플레이의 새 검증을 주장하지 않는다. 변경은 이 호환판 working tree에 기록했으며 커밋·푸시·게시·업로드는 수행하지 않았다.


커밋 준비 과정에서 새 `hok_prose_update_lock.json`의 checkout CRLF를 선언된 `.gitattributes`의 LF로 맞췄다. JSON 내용·선택 원본·production 출력·여섯 historical lock는 변경하지 않았다. 위 잠금 hash는 Git index와 working tree가 동일한 LF 바이트의 hash이며, 커밋 전 source snapshot을 다시 확인했다.

커밋 전 staged plain whitespace 검사는 byte-exact upstream 사본의 CRLF를 행 끝 공백으로 표시했다. CRLF를 정상 개행으로 처리한 전체 검사에는 원본 군사 현지화 한 쌍의 EOF 빈 행 2개만 남았다. source 해시 보존을 위해 사본을 정리하지 않았으며 upstream 사본을 제외한 staged runtime·tools·문서는 plain 검사에 통과했다.
