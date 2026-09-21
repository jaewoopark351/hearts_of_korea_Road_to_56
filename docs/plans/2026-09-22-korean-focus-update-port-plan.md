# HOK 한국 중점 업데이트의 RT56 이식 계획

작성일: 2026-09-22

상태: **구현 승인 후 코드 반영 완료 / 검증 진행 중**. 최종 구현·실행 결과는 [후속 구현 기록](../implementation/2026-09-22-korean-focus-update-port.md)을 기준으로 한다.

이 문서는 최초 조사 시 작성한 이식 대상, 보존 조건, 도구 보완과 검증 계획이다. 이후 사용자가 구현을 승인하여 별도 구현 기록으로 진행 상황을 관리한다. 아래 조사 당시의 관찰과 계획을 실행 결과로 간주하지 않는다.

## 1. 판단과 적용 원칙

한국 업데이트의 이식 자체는 중간 정도 난이도다. 기존 266개 중점 ID가 유지되고 새 60개가 추가됐으며, 한국 업데이트와 일본 업데이트가 별도 커밋으로 구분된다. 구 donor와 최신 donor, 현재 호환판을 비교해 변경분을 병합할 수 있다. 실제 RT56 동작 검증은 별도로 필요하다.

[ADR-0004](../decisions/0004-hok-korean-content-priority.md)에 따라 최신 HOK에 실제 적용된 한국 중점·보상·AI 변경을 이식 대상으로 삼고 기존 RT56 지도 ID와 만주·대일 강화 보정을 유지한다. 기간 단축과 보상 강화는 원본의 의도적 콘텐츠 업데이트로 기록하고 호환성 수정과 구분한다.

이번 한국 업데이트에 지도 bitmap·state history·GFX·sound 변경은 없다. 이 범위의 이식을 위해 지도나 한국 자산 병합을 다시 설계할 필요는 아직 확인되지 않았다. 새 RT56 스냅샷에 대한 재감사는 별도 선행 작업이다.

## 2. 조사 기준선

| 항목 | 기록 |
|---|---|
| 호환판 조사 시작 | `main@bfbba43c26022f3f64a88c2f1ec6600cb7f0d06f`, 작업 트리 깨끗함 |
| 기존 이식 donor | `887930f6e88c80568d62dab9cfbe1ba8a498a252` |
| 조사한 최신 donor | `81d39fadab9aaf75f3eb86873b39d2bec65c48d4`, 작업 트리 깨끗함 |
| 한국 중점·지원 콘텐츠 | `da815305e3ce00186a487b3a378bf8536ff59146` — 신규 17개 / 기존 수정 2개 |
| 한국 역사 AI | `118d7b53dfdbc120fcfe4b9d6792e66b2b519be7` — 기존 수정 1개 |
| 기존 포트 실행 기준 | 2026-09-06, HOI4 `1.19.2.0.a729`, RT56 manifest `3323396725579032799` |
| 현재 설치 RT56 관찰값 | manifest `7475007536894105204` |
| 현재 읽은 실행 로그 | 2026-09-21, HOI4 `1.19.3.0.c01a (d4e7)`, DLC 36개·활성 HOK 모드 1개 |
| 해당 로그의 물리적 모드 | launcher `hearts of korea.mod` → `C:/hoi/hearts_of_korea`, donor 단독 |
| 후속 지원 대상 | 새 HOI4/RT56 기준선·playset을 재기록한 뒤 확정; 관찰값을 검증된 지원 대상으로 간주하지 않음 |

donor는 `C:/hoi/hearts_of_korea`, 호환판은 `C:/hoi/hearts_of_korea_Road_to_56`이다. donor, Workshop, 바닐라와 사용자 데이터는 읽기 전용이다. 플레이세트 표시 이름, 호환판의 새 실행 체크섬과 최종 localisation 조합은 이번 조사에서 확정하지 않았다.

최신 로그는 이 호환판의 실행 증거가 아니다. [9월 6일 새 게임 크래시](../incidents/2026-09-06-post-port-new-game-crash.md)는 수정 후 재검증이 남은 과거 사건으로 유지한다. 한국 중점 업데이트가 그 크래시를 해결하거나 발생시켰다는 근거는 없다. 문서에 기록된 `17 PASS / 0 WARNING / 0 ERROR`도 과거 기준의 결과이며 이번에 재실행하거나 새 donor/RT56에 승계하지 않았다.

조사한 입력의 SHA-256:

| 입력 | SHA-256 |
|---|---|
| donor `common/national_focus/korea.txt` | `49EC715410B6931E51A6ABB297F7BE17E85D75A1AF72F4A70155E7824A54F903` |
| donor `common/ideas/korea.txt` | `DE22B2B0F7733AE5BC5A1564D9BBA8F47AE439456F893E6238903AC8BE953254` |
| donor `common/ai_strategy_plans/KOR_historical_strategy_plan.txt` | `18C56A24FF5C93A944E58D71BB81AFFADC332601861D980EF243ACF028D2A3E8` |
| 설치 RT56 `descriptor.mod` | `5B323861ABD63E31CB896277E3EA58BA4BCD9FCEEDA957B50792065E42E03F61` |

RT56 descriptor 해시는 기존 기록과 같지만 manifest는 달라졌다. descriptor 하나의 일치로 호스트 전체가 동일하다고 판단하지 않는다. 구현 직전에 관련 입력 전체와 ID 집합을 재확인하고 검토된 스냅샷·파일별 해시를 고정해야 한다.

## 3. 원본 업데이트의 실제 범위와 한계

| 영역 | 실제 적용된 원본 변경 |
|---|---|
| 중점 수 | 기존 266개 + 산업·교육 20 / 군사 25 / 민주·외교 15 = 326개 |
| 기간 | 원본 확장 직전 작업트리 기준 152개 단축. 고정 donor `887930f`·이식 전 호환판 `bfbba43`와 비교하면 선행 변경 2개를 포함해 **154개**가 cost 10→5; 나머지 기간 유지, 신규 60개도 cost 5 |
| 배치 | 최종 326개를 절대 기준 7개·상대 배치 319개로 배치하고 화면 폭을 압축 |
| 연결 콘텐츠 | 신규 국민정신 29개(산업11·군사12·민주6), 결정 10개, 결정 분류 3개, 외교 이벤트 6개, 관계 수정치 1개 |
| 현지화 | 산업·군사·민주·바로가기의 english/korean 4쌍, 8개 신규 파일 |
| 후속 보상 | 37개 중점 완료 보상과 관련 국민정신·결정·관계 수정치 조정 |
| 반복 사업 | 지역 사업 4개는 90일, 공동개발은 180일로 순차 반복; 기존 비용·진행 중 잠금·취소 무보상 유지 |
| 역사 AI | 기본 목록 51개 → 106개, 조건부 지원 계획 3개; 확장 중점 중 53개를 양수 우선순위 대상으로 포함 |

초기 확장 기록의 국민정신 28개는 후속 `HOK_KOR_night_school_spirit` 추가 전 수치다. 지역 사업 180일·1회 제한도 후속 조정 전 상태다. 현재 구현을 옮길 때는 고정한 최신 소스와 후속 적용 기록을 기준으로 한다.

구현 중 실제 Git 기준을 대조하여 기간 집계를 정정했다. 선행 2개는 `KOR_the_vanguard_of_asian_democracy`와 `KOR_stop_moderate_diplomacy`이며 원본의 별도 단축 주석을 보존한다. 최신 원본에 없는 기간 변경을 추가한 것이 아니다.

원본에서 **보병장비 한정 생산량 +10% 및 상위 국민정신으로의 승계는 미적용·응답 대기**다. 생산 비용 약 -9.09% 대안도 적용된 효과가 아니다. 이식 과정에서 이를 새로 구현하거나 이미 존재하는 보상으로 기재하지 않는다.

초기 확장·배치에는 제한된 원본 실행 기록이 있으나 최신 보상·반복 사업 검증 결과는 문서상 미확정이고 역사 AI는 게임 실행 미실시다. 이전 실행 기록은 최신 보상·AI 또는 RT56 동작의 증거가 아니다.

## 4. 반영할 runtime 파일 20개

두 한국 커밋의 신규 17개와 기존 수정 3개다. 기존 원장 분류는 유지하고 신규 파일은 `ADD` 후보로 제시한다. 조사 시 신규 17개에 현재 RT56/호환판의 동일 경로 파일은 없었지만 다른 경로의 논리 ID 충돌과 참조 감사는 구현 전에 완료해야 한다.

| 상대경로 | 구분·분류 | 처리 |
|---|---|---|
| `common/national_focus/korea.txt` | 기존 / `OVERRIDE` | 326개 트리·기간·배치·보상 + 지도 ID·만주 보정 |
| `common/ideas/korea.txt` | 기존 / `OVERRIDE` | 한국 국민정신 변경 |
| `common/ai_strategy_plans/KOR_historical_strategy_plan.txt` | 기존 / `ADD` | 기본 목록과 조건부 지원 계획 3개 |
| `common/decisions/HOK_KOR_democratic_expansion.txt` | 신규 / `ADD` 후보 | 원조·협정·공동개발, scope·반복·취소 |
| `common/decisions/HOK_KOR_industry_expansion.txt` | 신규 / `ADD` 후보 | 지역 ID·비용·부지·반복·취소 |
| `common/decisions/categories/HOK_KOR_democratic_expansion.txt` | 신규 / `ADD` 후보 | 민주 결정 분류 |
| `common/decisions/categories/HOK_KOR_industry_expansion.txt` | 신규 / `ADD` 후보 | 산업 결정 분류 |
| `common/ideas/HOK_KOR_democratic_expansion.txt` | 신규 / `ADD` 후보 | 협정 등 국민정신 부여·해제 |
| `common/ideas/HOK_KOR_industry_expansion.txt` | 신규 / `ADD` 후보 | 단계 교체·생산 방식 선택 |
| `common/ideas/HOK_KOR_military_expansion.txt` | 신규 / `ADD` 후보 | 육해공군 보정 |
| `common/modifiers/HOK_KOR_democratic_expansion.txt` | 신규 / `ADD` 후보 | 쌍방 면허생산 관계 보정 |
| `events/HOK_KOR_democratic_expansion.txt` | 신규 / `ADD` 후보 | 수락·거절·통보와 수신국 |
| `localisation/english/HOK_KOR_democratic_expansion_l_english.yml` | 신규 / `ADD` 후보 | 민주·외교 문자열 |
| `localisation/english/HOK_KOR_expansion_navigation_l_english.yml` | 신규 / `ADD` 후보 | 바로가기 문자열 |
| `localisation/english/HOK_KOR_industry_expansion_l_english.yml` | 신규 / `ADD` 후보 | 산업 문자열 |
| `localisation/english/HOK_KOR_military_expansion_l_english.yml` | 신규 / `ADD` 후보 | 군사 문자열 |
| `localisation/korean/HOK_KOR_democratic_expansion_l_korean.yml` | 신규 / `ADD` 후보 | 민주·외교 문자열 |
| `localisation/korean/HOK_KOR_expansion_navigation_l_korean.yml` | 신규 / `ADD` 후보 | 바로가기 문자열 |
| `localisation/korean/HOK_KOR_industry_expansion_l_korean.yml` | 신규 / `ADD` 후보 | 산업 문자열 |
| `localisation/korean/HOK_KOR_military_expansion_l_korean.yml` | 신규 / `ADD` 후보 | 군사 문자열 |

이는 donor 콘텐츠 반영 범위다. 생성기·검증기·분류 원장·구현 기록 수정은 별도다. 참조 감사에서 추가 의존 파일이 확인되면 소유권과 근거를 기록해 범위를 갱신한다.

## 5. 보존할 호환 동작과 제외 범위

### 지도와 지역 효과

[ADR-0002](../decisions/0002-map-id-migration.md)의 기존 매핑을 유지한다. 신규 지역 사업의 표시·착수·완료·취소·지도 강조도 같은 대상 지역으로 변환한다.

| 원본 state | 호환판 state | 신규 콘텐츠 사용처 |
|---:|---:|---|
| 1029 | 1144 | 강원 지역 개발 사업 |
| 1030 | 920 | 경상 조선소 사업 |
| 1031 | 1145 | 충청 개발 사업, 실업·시민교육 공장 지급 |
| 1082 | 919 | 실업·시민교육 공장 지급 |

교육 중점의 경기 525는 유지한다. 최종 대상 525·919·1145의 소유·완전통제·부지를 착수와 완료 양쪽에서 확인하고 각 주 슬롯 2·민간공장 2 지급 정책을 보존한다. 다른 지역 대체·과거 완료 보상 소급은 하지 않는다. 표 밖의 상속 state/province 참조도 사용 문맥 전체를 검토한다.

### 만주와 대일 강화

- 기존 8개 주 `716, 745, 328, 717, 714, 761, 715, 610`과 RT56 분할주 `941–947`의 총 15개 주 처리를 유지한다.
- `KOR_multiethnic_embrace`, `KOR_korean_dream`, `KOR_teaching_korean_to_manchurians`의 분리주의 완화·제거를 분할주까지 유지한다.
- 만주 승전·만슐루스·국뽕 초기화와 대일 강화의 통제·이전·코어·주둔군 처리 범위를 보존한다.
- `MAN`의 일본 종속 관계가 먼저 사라져도 대일 강화 결정이 유지되고, 잔존 `MAN`과의 전쟁을 조건부로 끝내며, 일본 종속국으로 남은 경우에만 합병하는 기존 보정을 유지한다.

관련 중점 ID와 기존 변환 도구의 `610` 처리 기준은 최신 donor에도 남아 있다. 이는 병합 위치가 유지된다는 근거이며 기존 도구를 새 소스에서 실행해 성공했다는 뜻은 아니다. [기존 이식 도구](../../tools/migrate_hok_ids.py)와 [만주 회귀 검사](../../tools/validate_port.py)를 기준으로 보존 여부를 확인한다.

### 일반 일본 콘텐츠와 AI

원본의 일본 민주 루트·일본 중점 전체·대만 수정은 이번 20개 파일에 포함하지 않는다. 일반 일본·중국은 RT56 소유라는 결정을 유지한다.

특히 donor `common/ai_strategy/KOR.txt`의 별도 변경은 `HOK_JAP_strengthen_civilian_government`를 참조한다. 이를 최신 donor 동기화에 포함하면 일본 루트 의존이 추가된다. 현재 호환판의 지도 ID가 변환된 KOR 전략과 `common/ai_strategy/r56_KOR.txt`의 RT56 김구·대중국 전략을 보존하고 역사 중점 계획 업데이트와 구분한다.

## 6. 생성·감사 도구의 후속 보완

| 도구 | 확인한 제약 | 필요한 후속 작업 |
|---|---|---|
| [migrate_hok_ids.py](../../tools/migrate_hok_ids.py) | `source_targets()`가 호환판에 없는 파일을 건너뜀 | 신규 17개를 명시적 목록으로 가져오고 변환·재현하는 소유 절차를 정함 |
| 같은 도구의 만주 보정 | 특정 중점 ID·블록을 기준으로 후처리 | 최신 source에 15개 주 보정을 적용하고 중복 적용·누락 검사 |
| [build_integration_manifest.py](../../tools/build_integration_manifest.py) | donor 전체 열거, 파일 1,014개·동일 경로 충돌 73개 고정 | 구 기준 + 한국 변경 목록의 출처를 고정하거나 최신 전체 donor를 재분류해 일본 제외를 기록하는 구조를 결정 |
| [validate_port.py](../../tools/validate_port.py) | `HOK_EVENT_FILES`와 문자열 정규식이 기존 이벤트·namespace만 검사 | 새 이벤트 파일과 `HOK_KOR_democratic_expansion` namespace를 함께 검사하고 결정·국민정신·현지화 참조 포함 |
| 원본 해시 검사 | 고정한 donor/RT56/vanilla 입력 변경 시 실패 | 검토된 새 기준선의 정확한 해시 기록. assertion 제거·자동 수용·오류 우회 금지 |

권장 출처 모델은 구 donor 기준에 이번 한국 변경 목록을 명시적으로 겹쳐 적용하는 방식이다. 실제 도구 설계는 구현 전에 확정하고 파일마다 원본 커밋·해시와 호환 변환을 추적한다. 현재 donor HEAD에는 일본 변경도 있으므로 파일 수만 `1014 → 1031`로 바꾸는 방식은 충분하지 않다. 생성 CSV를 손으로 고치지 않는다.

## 7. 후속 구현 순서

1. **기준선 재확정:** 최신 HOI4/RT56·관련 해시·DLC·언어·실제 모드 경로를 기록하고 source drift와 기존 지도 ID 할당의 충돌 여부를 검토한다.
2. **기존 실행 상태 분리:** 실행 작업 시 로그를 먼저 보존하고 신규 중점 적용 전 포트의 실행 가능 여부와 기존 크래시를 구분한다. 호스트 갱신 대응은 별도 변경 묶음으로 처리한다.
3. **변경 목록 고정:** 구 donor → 두 한국 커밋 → 현재 호환판을 비교하고 20개 파일의 참조·논리 ID·namespace를 감사한다.
4. **지원 콘텐츠·중점 병합:** 신규 파일 유입 절차와 함께 326개 중점·기간·배치·보상을 반영하고 지도 ID·만주·대일 강화 보정을 유지한다.
5. **역사 AI 반영:** 기본106개와 방어전·만주 승전 후 연합 창설·창설 후 협력 계획3개를 반영한다. 다른 이념 계획과 RT56 전략은 보존한다.
6. **도구·원장 갱신:** source pin·분류 근거와 신규 파일 생성·검사 범위를 재현 가능하게 갱신한다.
7. **정적·실행 검증:** 아래 행렬에 따라 실제 실행한 범위와 미실행 범위를 각각 기록한다.

이 순서는 후속 작업 계획이다. 현재 문서화에서 구현 단계는 실행하지 않았다.

## 8. 예정 검증과 완료 조건

후속 runtime·도구 구현 후 `python tools\validate_port.py`를 실행한다. 현재 문서만 수정하는 작업에서는 실행하지 않는다. 정적 통과를 엔진 동작의 증거로 대체하지 않는다.

| 검증 영역 | 확인할 결과와 중요한 차단 경로 |
|---|---|
| 재현·참조 | 새 source pin에서 생성 재현, 파일별 분류, 관련 ID의 donor/compat/RT56/vanilla 충돌 및 focus·idea·event·decision·category·modifier 참조 해소 |
| 중점 보존 | 기존266 + 신규60, 확장152개와 선행2개 기간 단축, 나머지 기간 보존, 326개 선행·배타·분기·배치 및 의도한 보상 변경 |
| 보상 | 37개 완료 보상, 국민정신 교체·누적, 연구 대상/횟수/배율, 원조 재고 차감, 관계 보정의 부여·제거 |
| 지도 참조 | 기존 매핑 전체와 새 지역 사업의 표시·보상·취소 대상 일치, 원본 state ID가 잘못 남지 않음 |
| 통제된 실행 | donor 없는 R0(RT56 단독)와 C0(RT56+포트), 비한국/KOR 새 게임·지도 진입·시간 진행·관련 오류 비교. 기존 크래시와 신규 오류 분리 |
| UI·현지화 | 신규 가지·바로가기·긴 이름·숨김 분기, BOM·header·키·토큰과 실제 보상 설명. 선택할 번역 구성의 R1/C1에서 실제 표시와 덮어쓰기 비교 |
| 사업·공장 | 정상 완료·동일 대상 재착수·취소 후 재착수, 비용·회당 보상1회·진행 중 중복 방지. 소유/통제 상실·부지 부족의 차단/취소와 무보상. 교육 세 주 조건·총 민간공장6개 지급 |
| 외교·협정 | 수락/거절·수신국·통보, 쌍방 관계 보정, 세력·정부·지도권 변화 및 전쟁·기간 만료, 공동개발 반복과 과거 플래그·카운터의 영향 |
| 군사·DLC | 실제 AAT/BBA/MTG 등 보유/미보유 분기·대체 보상, RT56 기술·교리·장비 참조와 연구 보너스 소비, 의용군 조건, 기존 KOR history/OOB 및 폐기 기술 제거 유지 |
| 만주·강화 | 15개 주 중 일부 미통제인 차단 경로, 완전통제·승전·만슐루스·국뽕 경로, MAN 소멸/독립/종속 유지별 휴전·합병 |
| AI | 기본106개·지원3개·양수 우선대상 고유118개/신규53개 대응, 역사 기본/명시 민주/다른 규칙, 정부지원365일·선행·연구조건, 방어전과 연합 창설/지도권 상실의 실제 선택·지원 전환 |
| 진행·호스트 보존 | +1/+7/+30일과 필요한 장기 AI 관찰, 일반 JAP/CHI의 RT56 콘텐츠 보존, 중복 이벤트·반복 보상·로그 증가 확인 |
| 세이브·추가 경로 | 새 게임 저장·재로드와 기존 세이브 호환 구분. 신규 게임 전용 정책 유지; 1939·미검증 DLC·멀티플레이는 실제 시험 없이 완료로 표기하지 않음 |

english 경로에도 한국어 본문을 쓰는 기존 HOK 계약을 유지하며 새 영문 번역 제공으로 표현하지 않는다. 최종 언어 의존성 선택은 [ADR-0003](../decisions/0003-localisation-contract.md)의 별도 미결 과제다.

완료 보고에는 source commit·입력 해시·playset, 반영/제외 파일, 원본 보상 변화, 보존한 호환 동작, 정적 결과, 실제 실행 결과와 남은 미검증 항목을 남긴다. 기존 크래시가 runtime 진행을 막으면 코드 이식 상태와 플레이 가능 여부를 분리한다. 커밋·푸시·게시도 실제 수행 여부만 기록한다.

## 9. 문서화 결과와 참고 자료

이번에는 Git 이력·파일·해시·기존 로그를 읽고 이 계획과 README 안내를 작성했다. runtime 파일·도구·생성 CSV·descriptor·외부 원본은 수정하지 않았다. 생성기·정적 검증기·HOI4 실행과 커밋·푸시·업로드도 하지 않았다.

조사한 donor 문서는 위 `81d39fa` 시점의 다음 파일이다. 내부의 오래된 미커밋 상태·검증 수치는 당시 기록으로 해석한다.

- `<HOK_DONOR>/docs/incidents/2026-09-21-korean-focus-expansion.md` — 초기 확장·기간 단축·지원 콘텐츠와 제한된 실행 기록
- `<HOK_DONOR>/docs/incidents/2026-09-21-korean-focus-compact.md` — 최종 배치 압축과 화면 검증 범위
- `<HOK_DONOR>/docs/HOK_KOREAN_FOCUS_REBALANCE_PLAN.md` 10절 — 보상37개·반복 사업 적용, 미적용 생산량 보너스와 검증 한계
- `<HOK_DONOR>/docs/HOK_KOREAN_HISTORICAL_AI_PLAN.md` — 기본106개·지원3계획과 실게임 미검증
- `<HOK_DONOR>/docs/HOK_KOREAN_FOCUS_FIRST_60_SPEC.md` — 신규60개 이름·선행·보상 명세

호환판의 [아키텍처](../PORTING_ARCHITECTURE.md), [작업 절차](../PORTING_WORKFLOW.md), [한국 콘텐츠 보존](../decisions/0004-hok-korean-content-priority.md), [통합 원장](../audits/2026-09-06-integration-ledger.md)을 함께 참조한다. 기존 원장의 분류 수와 검증 결과를 최신 donor 전체 감사 완료로 해석하지 않는다.
