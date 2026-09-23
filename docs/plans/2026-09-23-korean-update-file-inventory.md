# 2026-09-23 한국 2차 업데이트 이식 대상 목록

상태: **구현 전 읽기 전용 조사 스냅샷**. 이후 콘텐츠를 병합했으며 실제 선택 목록·출처·검증은 [구현 기록](../implementation/2026-09-23-korean-second-wave-port.md)을 따른다. 아래 미구현 표현과 비교 수량은 조사 당시 기준이며 실행 성공 수가 아니다.

[전체 이식 계획](2026-09-23-korean-second-wave-port-plan.md)의 파일별 부록이다. 진행 순서·병합 결정은 전체 계획, 실행 시나리오와 통과 조건은 [검증 계획](2026-09-23-korean-update-validation-plan.md)을 따른다.

## 1. 비교 기준과 수량

| 기준 | 2026-09-23 조사값 |
|---|---|
| 호환판 | `feat/korean-focus-update-20260922@c84fd9faa543a9d2f3aabd8bebe7691984dc6cc3` |
| 조사 시작 작업 트리 | 기존 `AGENTS.md` 수정만 존재. 그 변경을 보존하고 이번 문서들을 추가 |
| 원본 donor | `C:\hoi\hearts_of_korea`, `be5fb40dbd8de33e5adbf65e808bcb0e8c283560`, 작업 트리 깨끗함 |
| 호환판의 기존 선택 입력 | 기본 `887930f6e88c80568d62dab9cfbe1ba8a498a252` + 한국 콘텐츠 `da815305e3ce00186a487b3a378bf8536ff59146` + 역사 AI `118d7b53dfdbc120fcfe4b9d6792e66b2b519be7` |
| 기존 이미지 입력 | `tools/hok_icon_lock.json`의 `698b6eb160efbaa04a4d43846330ba002f5e8cc7` 기반 당시 작업 트리 해시. 최신 커밋 전체를 가져온 구조가 아님 |
| 현재 RT56 관찰값 | Workshop `820260968`, manifest `7475007536894105204`. 실제 구현 직전 다시 확인 |

`git diff 118d7b5..be5fb40`만으로 가져올 목록을 만들면 이미 이식된 첫 60개 이미지가 다시 신규로 잡힌다. 따라서 커밋 간 변경 목록을 읽은 뒤 **현재 호환판의 실제 파일·ID·SHA-256**과 다시 대조했다.

| 항목 | 현재 호환판 | 최신 donor에서 확인한 추가분 | 조사 방법 |
|---|---:|---:|---|
| 한국 중점 | 326개 | 134개, 합계 460개 | `focus` 블록과 ID 비교; 기존 326개 ID 모두 donor에 존재 |
| 이번 확장 국민정신 | 아직 없음 | 10개 신규 파일, 정의 63개 | 신규 `HOK_KOR_*` 국민정신 정의 집계 |
| 이번 확장 기간제 사업 | 아직 없음 | 4개 신규 결정 파일, 사업 18개 | 4+8+2+4개의 `days_remove = 90` 사업 |
| 이번 확장 주 동적 변동치 | 아직 없음 | 1개 신규 파일, 정의 12개 | 독립 최상위 정의 집계; 국민정신 63개와 별도 |
| 첫 확장 HOK 이미지 | 중점 60+국민정신 29 | 기존 89개 전부 donor와 SHA-256 동일 | 동일 상대경로 DDS 전체 해시 비교 |
| 새 HOK 이미지 경로 | 없음 | DDS 232개 | 중점 134+국민정신 63+주 변동치 12+결정/범주 22+공유 광택 사본 1 |
| 새 스프라이트 파일 | 없음 | GFX 16개 | 일반/광택 8쌍 |
| 새 게임 지원 텍스트 | 없음 | 41개 | 국민정신 10+결정 4+범주 4+주 변동치 1+현지화 22 |

**제안하는 실제 이미지 복사량은 231개**다. 232개라는 원본 차이 수량에 포함된 바닐라 광택 사본 1개는 아래 4절의 공유 호스트 참조를 유지한다. 이에 따라 사전 후보는 신규 runtime 파일 288개(텍스트 57+이미지 231)와 기존 중점 파일 병합이다. 최종 참조·충돌 감사에서 필요가 입증되면 목록과 분류를 먼저 갱신한다.

이 조사에서 새 텍스트 57개는 설치 RT56·바닐라에 같은 상대경로가 없었다. **다른 파일의 같은 논리 ID, 현지화 중복, 이미지 경로 충돌, 유효 로드 우선순위까지 검증한 결과는 아니다.** 모든 아래 분류는 기존 확정 분류를 제외하면 구현 전 감사용 제안이다.

## 2. 정책별 가져올 묶음

중점은 모두 `common/national_focus/korea.txt` 안에 있다. 파일을 통째로 덮어쓰지 않고 다음 묶음의 중점·국민정신·결정·현지화·이미지·AI 가중치·배치를 함께 처리한다. 보상과 조건은 현재 `be5fb40`의 최종 구현을 기준으로 삼고 초기 후보의 임시 보상을 복원하지 않는다.

| 묶음 | 중점 | 국민정신 | 기간제 사업 | 지원 파일의 핵심 접미사 |
|---|---:|---:|---:|---|
| 여운형·박헌영 첫 정책 | 10 | 8 | 4 | `communist_policy`; 그림은 `second_wave` |
| 공산 내정 | 9 | 4 | 4 | `communist_governance` |
| 공산 기술보급·계획 운영 | 9 | 4 | 4 | `communist_development`; 사업은 governance 결정 파일에 포함 |
| 파시즘 F1 군수계약 | 4 | 2 | 2 | `fascist_procurement` |
| 파시즘 F2 참모업무 | 4 | 2 | 0 | `fascist_staff` |
| 파시즘 F3 병역행정 | 4 | 3 | 0 | `fascist_mobilization` |
| 파시즘 F4–F6 점령행정·삼군 조정·재건예산 | 12 | 8 | 0 | `fascist_followup` |
| 입헌 C1–C4 | 14 | 7 | 0 | `constitutional_followup` |
| 전제 A1–A4 | 14 | 7 | 0 | `royal_followup` 파일의 전제 부분 |
| 환제국 H1–H4 | 14 | 8 | 0 | `royal_followup` 파일의 환제국 부분 |
| 만주 M1–M4 | 20 | 0 | 4 | `manchurian_followup`; 국민정신 대신 주 변동치 12개 |
| 공통 산업·군사 G1–G5 | 20 | 10 | 0 | `common_followup` |
| 합계 | **134** | **63** | **18** | 별도 주 변동치 **12** |

첫 7개 행은 공산 28·파시즘 24개이고, 나머지는 잔여 82개다. 현재 원본 정의의 ID 목록과 연결은 [원본 2차 계획](../../../hearts_of_korea/docs/HOK_KOREAN_SECOND_WAVE_PLAN.md), [현재 후보/적용 ID 데이터](../../../hearts_of_korea/docs/data/HOK_KOREAN_SECOND_WAVE_CANDIDATES.json), [현재 좌표 데이터](../../../hearts_of_korea/docs/data/HOK_KOREAN_SECOND_WAVE_COORDINATES.json)를 함께 읽는다. 원본의 실행 결과와 배치 검사는 호환판 검증으로 전용하지 않는다.

## 3. 텍스트 파일별 처리

### 기존 파일

| 경로 | 제안 처리와 소유권 |
|---|---|
| `common/national_focus/korea.txt` | 기존 통합 원장의 **`OVERRIDE` 유지**. 과거 고정 donor·현재 donor·현재 호환판을 비교하는 3자 병합 절차로 134개와 필요한 배치/연결 변경 반영. RT56 같은 경로 및 관련 한국 정의를 다시 감사. 파일 분류와 병합 방법을 혼동하지 않음 |
| `common/ideas/HOK_KOR_democratic_expansion.txt` | 유지. 현재 donor와 차이는 이미 적용된 이미지 연결 주변 기여 주석. 기존 6개 정의를 다시 복사할 기능상 이유 없음 |
| `common/ideas/HOK_KOR_industry_expansion.txt` | 유지. 현재 donor와 주석을 제외한 행 동일; 11개 정의·이미지 연결 유지 |
| `common/ideas/HOK_KOR_military_expansion.txt` | 유지. 현재 donor와 주석을 제외한 행 동일; 12개 정의·이미지 연결 유지 |
| `interface/HOK_KOR_focus_icons.gfx`, `interface/HOK_KOR_spirit_icons.gfx` | 현재 donor와 바이트 동일. 기존 등록을 보존 |
| `interface/HOK_KOR_focus_icons_shine.gfx` | 기존 host fallback 보존. donor의 광택 경로 현지화만 따라잡기 위해 수정하지 않음 |
| `common/ai_strategy_plans/KOR_historical_strategy_plan.txt` | donor와 바이트 동일. 신규 정치 루트를 민주 역사 목록에 임의 삽입하지 않음. 새 중점의 자체 `ai_will_do`와 사업 AI를 모듈별 반영 |
| `common/ai_strategy/KOR.txt` | 현재 포트의 별도 통합 결과 유지. 최신 donor 전체 복사로 기존 host 통합을 되돌리지 않음 |

중점 파일에서 유지할 포트 차이는 [주 번호 이전](../decisions/0002-map-id-migration.md), [기존 한국 업데이트 이식](../implementation/2026-09-22-korean-focus-update-port.md), [독립당 부분 동원 보상](../implementation/2026-09-22-independent-party-reward.md)을 기준으로 삼는다. 기존 326개 ID, 국민정신 및 연구/정치력 등 부수 보상, 필요한 만주 분할주 `941–947` 처리, `KOR_independent_party_in_power`의 `partial_economic_mobilisation` 보상을 보존한다. donor에도 같은 보상이 있으면 다시 주입하여 두 번 실행시키지 않도록 병합한다.

### 새 국민정신 파일 10개 — `ADD` 제안

모두 `common/ideas/` 아래이며 수량은 정의 수다. 정책별 하위/상위 교체, 취소 조건, 상대국에 부여되는 정신의 소유 범위를 함께 가져온다.

| 파일 | 정의 수 |
|---|---:|
| `HOK_KOR_communist_policy.txt` | 8 |
| `HOK_KOR_communist_governance.txt` | 4 |
| `HOK_KOR_communist_development.txt` | 4 |
| `HOK_KOR_fascist_procurement.txt` | 2 |
| `HOK_KOR_fascist_staff.txt` | 2 |
| `HOK_KOR_fascist_mobilization.txt` | 3 |
| `HOK_KOR_fascist_followup.txt` | 8 |
| `HOK_KOR_constitutional_followup.txt` | 7 |
| `HOK_KOR_royal_followup.txt` | 15 |
| `HOK_KOR_common_followup.txt` | 10 |

### 새 결정·범주·주 변동치 9개

| 경로 | 수량/핵심 | 제안 분류 |
|---|---|---|
| `common/decisions/HOK_KOR_communist_policy.txt` | 사업 4개; 선택, 비용, 공통 활성/대기 플래그 | `ADD` |
| `common/decisions/HOK_KOR_communist_governance.txt` | 내정 4+기술보급 4, 합계 8개 | `ADD` |
| `common/decisions/HOK_KOR_fascist_procurement.txt` | 군수 사업 2개 | `ADD` |
| `common/decisions/HOK_KOR_manchurian_followup.txt` | 지역 사업 4개; 보상·취소·제거·재착수·주 강조 참조 | `ADD` 경로. 대상 지역 변환은 별도 의미 검토 |
| `common/decisions/categories/HOK_KOR_communist_policy.txt` | 범주·소형 아이콘 | `ADD` |
| `common/decisions/categories/HOK_KOR_communist_governance.txt` | 범주·소형 아이콘 | `ADD` |
| `common/decisions/categories/HOK_KOR_fascist_procurement.txt` | 범주·소형 아이콘 | `ADD` |
| `common/decisions/categories/HOK_KOR_manchurian_followup.txt` | 범주·소형 아이콘 | `ADD` |
| `common/dynamic_modifiers/HOK_KOR_manchurian_followup.txt` | 지역 서비스 4계열 × I/II/기간제 =12; 국가 정신 아님 | `ADD`, scope/제거 조건 감사 필요 |

`ADD`는 무수정 복사를 보장하는 말이 아니다. 신규 ID의 참조가 RT56의 다른 지리를 가리키면 해당 논리의 원본 의도·현재 host·포트 동작을 비교하고 `THREE_WAY_MERGE` 여부를 통합 원장에 명시한다. 기존 주 매핑은 `1028→918`, `1029→1144`, `1030→920`, `1031→1145`, `1082→919`, `1083→917`, `1084→1146`, `1085→1147`이다.

특히 원본 만주 M1/M2/M4는 `328`, M3는 `328/714/717`을 대상으로 한다. 환제국 운영의 적격 거점 조건은 기존 만주 8개 주를 사용한다. 기존 광역 만주 처리에 쓰는 `941–947`을 모든 신규 지역 보상에 일괄 추가하면 수혜 지역과 균형이 달라진다. **같은 숫자의 지리 의미, RT56에서 갈라진 실제 지역, 정책의 대상 범위를 먼저 대조한 뒤** 착수·완료·취소·제거·AI·지도 강조의 동일한 집합을 확정한다. 이 작업은 기존 지도 파일이나 새 주 ID를 추가하는 작업으로 확대하지 않는다.

### 현지화 22개 — `ADD` 제안

다음 11개 접미사 각각에 대해 `localisation/english/HOK_KOR_<접미사>_l_english.yml`과 `localisation/korean/HOK_KOR_<접미사>_l_korean.yml`을 한 쌍으로 가져온다.

`communist_policy`, `communist_governance`, `communist_development`, `fascist_procurement`, `fascist_staff`, `fascist_mobilization`, `fascist_followup`, `constitutional_followup`, `royal_followup`, `manchurian_followup`, `common_followup`.

중점 이름·설명뿐 아니라 국민정신, 선택/대기/재착수, 동적 변동치, 결정 조건과 비용 설명도 함께 대상이다. UTF-8 BOM·언어 헤더·키·색/치환 토큰을 보존한다. English 경로라고 영문 번역을 새로 만들거나 기존 한국어 본문을 교체하지 않는다. 번역 모드의 `replace_path="localisation"` 문제는 최종 언어 계약 검증에 남기며 이 목록만으로 해결됐다고 하지 않는다.

## 4. 이미지·스프라이트·출처

### 복사 후보 231개 — `ASSET_COPY` 제안

표의 폴더는 `gfx/interface/<goals|ideas|decisions>/HOK_KOR/` 아래다. `ideas/remaining_followup`의 44개에는 국민정신 32개와 주 변동치 12개가 함께 있다.

| 모듈 폴더 | goals | ideas | decisions | 적용 매니페스트 접미사 |
|---|---:|---:|---:|---|
| `second_wave` | 10 | 8 | 0 | `SECOND_WAVE` |
| `communist_policy` | 0 | 0 | 5 | `SMALL_DECISION` |
| `communist_governance` | 9 | 4 | 5 | `COMMUNIST_GOVERNANCE`, `SMALL_DECISION` |
| `communist_development` | 9 | 4 | 4 | `COMMUNIST_DEVELOPMENT` |
| `fascist_procurement` | 4 | 2 | 3 | `FASCIST_PROCUREMENT` |
| `fascist_staff` | 4 | 2 | 0 | `FASCIST_STAFF` |
| `fascist_mobilization` | 4 | 3 | 0 | `FASCIST_MOBILIZATION` |
| `fascist_followup` | 12 | 8 | 0 | `FASCIST_FOLLOWUP` |
| `remaining_followup` | 82 | 44 | 5 | `REMAINING_FOLLOWUP` |
| 합계 | **134** | **75** | **22** | **231** |

파일 목록·ID·스프라이트·이미지 해시·출처·팔레트는 donor의 `docs/data/HOK_KOREAN_<접미사>_ICON_MANIFEST.json`으로 특정한다. 소형 결정 자료는 초기 큰 텍스처를 사용한 sprite 설명보다 **현재 runtime GFX의 경로와 small-decision manifest**를 우선 대조한다. 기록 간 차이는 삭제하지 않고 최종 적용 연결을 포트 manifest에 별도로 남긴다.

원본에 기록된 크기는 중점 100×88, 국민정신/주 변동치 60×68, 결정 행 32×32, 범주 51×40이다. 형식·알파·프레임과 exact casing을 유지하고 재압축·재생성·기존 89개 재색칠을 하지 않는 복사를 제안한다. 원본의 크기 적합성 검사는 RT56 GUI 실측을 대신하지 않는다.

### 스프라이트 16개 — `ADD` 제안, 광택 경로만 결정적 변환

`interface/HOK_KOR_<모듈>_icons.gfx`와 `interface/HOK_KOR_<모듈>_icons_shine.gfx`의 8쌍이다.

`second_wave`, `communist_governance`, `communist_development`, `fascist_procurement`, `fascist_staff`, `fascist_mobilization`, `fascist_followup`, `remaining_followup`.

일반 registry의 `GFX_HOK_KOR_*` 및 `GFX_idea_HOK_KOR_*`는 현지 HOK 이미지에 연결한다. 신규 광택 registry가 참조하는 donor 로컬 `gfx/interface/goals/HOK_KOR/shine_overlay.dds`는 **`gfx/interface/goals/shine_overlay.dds`의 기존 바닐라 fallback으로 변환**하는 안이다. 기존 첫 60개 광택 registry는 현재 bytes를 유지한다. 공유 광택의 실제 provider는 바닐라 설치본이며 RT56 파일이 제공한다고 잘못 기록하지 않는다.

donor 로컬 사본과 설치 바닐라 원본의 SHA-256은 모두 `BB416649358C73D34AACD46BAD61BC44211FAC8111627B56E25F385AD98F4448`이다. 이는 같은 이미지라는 근거이며 새 재배포 허가의 근거는 아니다. 해당 1개는 복사 `ASSET_COPY`에서 제외하고 **공유 호스트 의존 유지**로 기록한다. 6종 통합 분류의 `USE_RT56` 범주를 사용할 때에도 provider를 `VANILLA`로 명시해야 한다. 그 외 HOK-owned 텍스처·마스크는 모두 포트 runtime 디렉터리에 존재해야 한다. 공유 참조가 남으므로 이미지 연결 전체가 자급적이라고 표현하지 않는다.

### 보존할 출처 문서

선택한 8모듈의 `HOK_KOREAN_*_ICON_CREDITS.md`, 위 9개 manifest, [소형 결정 수정 기록](../../../hearts_of_korea/docs/incidents/2026-09-22-korean-decision-icon-size.md), [잔여 확장 출처](../../../hearts_of_korea/docs/HOK_KOREAN_REMAINING_FOLLOWUP_ICON_CREDITS.md), 기존 `UPSTREAM_CREDITS.txt`가 근거다. 구현 때 필요한 문서를 포트에 보존하고 donor 내부 상대 링크와 `.local-artifacts` 참조를 실제 포트 보존 위치/원본 provenance로 명확히 나눈다. donor 로컬 절대경로를 runtime 경로로 사용하지 않는다.

출처 문서는 선택한 Globvs / Ultimate HOI4 GFX 고정 소재와 해당 CREDITS를 사용 근거로 기록한다. 이를 다른 모드 전체·별도 MIT/CC 허가로 확대하지 않는다. 잔여 확장의 HOK 왕관·태극 소재와 개별 원저자 미상 기록, 원본 기여자와 kpopmodder의 합성·선택·색상 작업을 구별하여 보존한다. 이번 문서 작업은 새 허가를 취득하거나 외부 자료를 다운로드한 작업이 아니다.

## 5. 가져오지 않을 것과 도구의 경계

| 대상 | 처리 |
|---|---|
| donor `history/countries/KOR - Korea.txt` | 중점/이미지 이식에서 제외. `118d7b5..be5fb40`의 MtG 시작 전쟁지지도 `0.05→0.1`은 별도 시작 균형 변경이며 포트의 폐기 수송기 기술 수선을 되돌릴 이유가 없음 |
| donor map·history/states·전역 공유 시스템 | 기존 RT56 병합 결과 유지. 숫자 참조 이전 때문에 폴더를 다시 복사하지 않음 |
| 일반 JAP/CHI·대만 업데이트, 별도 donor 일본 AI 연결 | 신규 한국 정책의 필수 참조로 입증되지 않은 내용은 제외; 기존 [한국 우선/host 보존 결정](../decisions/0004-hok-korean-content-priority.md) 유지 |
| descriptor·launcher·Workshop ID·언어 의존성 변경 | 이식 파일 복사에 포함하지 않음. 별도 검증과 명시적 결정 대상 |
| donor의 임시 진단·로그·세이브·렌더러·전체 `.local-artifacts` | runtime 및 릴리즈에 복사하지 않음. 필요한 출처 증거만 선별 보존 |
| 기존 한국 WAV·모델·MIO·MAN 수선·음성 registry | 현재 포트 소유와 병합 결과 유지; 새 이미지 목록에 묶어 donor판으로 되돌리지 않음 |
| 기존/새 `on_action`, 이벤트, scripted effect/trigger 파일 | 이번 고정 donor 차이에서 새 한국 정책을 위한 신규 경로가 확인되지 않음. 별도 필요가 입증되기 전에는 추가하지 않음 |
| 보병장비 한정 생산량 +10%의 미결 설계, 보상 재강화, 추가 중점 | 기존 미결·후속 개발로 분리. 이번 134개 이식에 임의로 해결하거나 수량을 늘리지 않음 |

구현을 시작하면 기존 `tools/build_korean_focus_update.py`, `source_snapshot.py`, `hok_source_lock.json`, `hok_icon_lock.json`을 중심으로 입력 고정·출력 소유권을 확장한다. 기존 snapshot을 무효화하거나 최신 donor 전체로 바꾸지 않고 선택한 경로와 새 provenance를 추가한다. 신규 DDS는 원본 bytes, registry는 기록된 광택 변환, 중점/지역 참조는 기록된 병합이 재현되어야 한다.

`build_integration_manifest.py`, pruning 규칙, `check_korean_focus_update.py`, `validate_port.py`에는 새 경로·ID·expected count·별도 host provider를 반영해야 한다. 다만 현재 pin 불일치를 우회하거나 검사를 약화시키는 변경은 허용하지 않는다. **이번 문서화에서 이러한 도구나 검사를 수정·실행하지 않았다.**

## 6. 주요 입력 해시

아래는 2026-09-23 실제 읽은 파일 bytes의 SHA-256이다. 구현 때 모든 채택 경로에 commit/blob/checkout/input/output hash를 기록하는 manifest를 확장해야 하며, 이 짧은 표를 전체 lock의 대체물로 쓰지 않는다.

| 입력 | SHA-256 |
|---|---|
| donor `common/national_focus/korea.txt` | `1CEDAF78903DB31D15E3837E20069B71BCA8FC674212B1D033F0D721B2B6735C` |
| 현재 포트 `common/national_focus/korea.txt` | `D33DC929878F3CBB2750164086D9B0120C2DAC2ED45B994C5384A720E8D15C22` |
| donor `common/decisions/HOK_KOR_manchurian_followup.txt` | `5B9E162E175E9FC1EB5D1B1A29AD12911AF73DF340D01F82CD9D5D3F52974E1D` |
| donor `common/dynamic_modifiers/HOK_KOR_manchurian_followup.txt` | `650FB00A2AD75FE0CB485DF4A9CC9C2A46C5342E32DC623F832BFD2B8EF41A7E` |
| donor `docs/data/HOK_KOREAN_SECOND_WAVE_CANDIDATES.json` | `6F5D16FB7226E4CC108CDFE43A9D6EA8D847DEB01C6F550B72FC580C551D119E` |
| donor `docs/data/HOK_KOREAN_REMAINING_FOLLOWUP_ICON_MANIFEST.json` | `B4BC596D93CAA69AC3DBBD0BE07776546F972ED31D573544D75467F2E68844DC` |
| donor `docs/data/HOK_KOREAN_SMALL_DECISION_ICON_MANIFEST.json` | `9771D81EC0D9D578B91592DF4401D15D0C3D08D7052ED9BEC85FCB0532DAD20C` |
| 현재 포트 `tools/hok_source_lock.json` | `436B730E92D58A33FBBBB913E064C3A0D6A904D069F61D8CDBE38DCCB28FC94B` |
| 현재 포트 `tools/hok_icon_lock.json` | `DBB2A37CAE0DB55171C393CDFDA3F24E9B09B65CEF224E81593310A9620C59A3` |
| 현재 포트 `tools/build_korean_focus_update.py` | `D0C917EA456330F2EBC0C2C1B0F2E2697AAD9ADA4A869BCBCF746DB3E32B1C5E` |
| RT56 `descriptor.mod` | `5B323861ABD63E31CB896277E3EA58BA4BCD9FCEEDA957B50792065E42E03F61` |

확인된 것은 선택 대상의 존재·개수·현재 경로·일부 동일성이다(`CONFIRMED`). 논리 ID 전수 충돌 해소, 엔진 scope, 실제 배치·아이콘 표시·정상 진행·AI·저장 호환성은 이번 목록 작성으로 입증되지 않았다(`UNPROVEN`). 현재 사용자 playset의 별도 donor 혼합 실행 역시 이 포트의 target/control 실행 증거로 사용하지 않는다.
