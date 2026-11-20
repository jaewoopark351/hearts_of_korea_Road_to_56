# 2026-11-19 산둥군벌 영토 기본 편입 구현·검증 기록

작성: **2026-11-19 (Asia/Seoul)**. 상태: **구현·핵심 엔진·실제 중점 UI·새 저장 왕복 확인**. 아래 소스·합성 효과·실제 UI·저장·복원의 검증 범위를 구분하며, 이전 산둥 정부 구현의 실행 결과를 이번 통과로 재사용하지 않는다.

## 요청·기준과 자료 위치

사용자는 [후속 설계 18절](../HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_PLAN.md#18-shandong-warlord-integration-design)의 전체 흐름을 인용하고 원본·원작·로그 경로와 함께 `AGENTS.md, /docs 읽고 구현해줘`라고 요청했다. 앞선 문서화·설명 전용 단계와 이번 계속개발 구현 승인을 구분한다. 커밋·푸시·Workshop 업로드는 승인 범위에 포함하지 않는다.

| 구분 | 현재 기준·역할 |
|---|---|
| 작업 소스 | `C:\hoi\hearts_of_korea`; 브랜치 `feat/korean-focus-expansion-ai`, HEAD `0c19f58fa7a9ff898196dcdbe46edfd0ad5fdbbc`의 기존 미커밋 작업 |
| 설치 원본 | `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV`; 설치 메타데이터 `Operation Postern v1.19.5.0.7c6c (c184)`, 읽기 전용 구문·주 정의 출처 |
| 원작 Workshop | `C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\2898629778`; 읽기 전용 역사 출처이며 업로드 대상 아님 |
| 사용자 데이터 | `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV`; 게임이 생성하는 실제 로그·저장 원본 |
| 이번 외부 TASK | `C:\hoi\test\hok-shandong-full-integration-20261119-01\`; 모든 helper·백업·probe·검사 출력·로그/저장/화면 증거 사본 |
| 이전 외부 TASK | `C:\hoi\test\hok-shandong-democratic-government-20261119-01\`; 전면 편입 전 소스·실행 증거. 이전 결과·스크립트 출처이며 이번 실행 결과가 아님 |
| 활성 모드 출처 | launcher 개발 pointer는 저장소를 직접 로드. 시작 선택은 HOK → 외부 English Translation이며 `disabled_dlcs`는 빈 배열. 실제 실행의 구성·DLC 조회·체크섬은 실행별 기록을 따름 |
| 외부 번역 | `C:\hoi\Hearts of Korea English Translation Anime Modder's Edition`; 활성 덮어쓰기 비교용, 이번 수정 대상 아님 |

`TASK/source-baseline.json`에 편집 전 runtime **1,595파일** 해시·Git 상태를, `TASK/baseline-source/`에 runtime 8파일과 관련 문서·지리 목록·descriptor를 합한 **13파일**을 보존했다. `TASK/runtime/launcher-source.json`은 실제 launcher pointer와 설치 메타데이터를 기록한다. `TASK/runtime/baseline/`에는 profile 11파일·현재 로그의 증거 사본과 기존 저장 **157개·11,441,308,865바이트**의 SHA-256 목록이 있다. 이전 작업 시작의 124개와 그 작업에서 생성한 33개는 이번 시작 시점에는 모두 보존해야 할 기존 저장이다.

시작 전 HOI4·launcher·crash reporter 프로세스는 없었다. 다만 root가 Steam 창을 직접 활성화해 확인한 화면은 이미 HOI4의 **실행 중·파란 정지** 표시였다. 이 시작 전 표시를 이번 시험 프로세스가 만든 상태로 단정하지 않으며 `TASK/ui/00-steam-before-task.png`와 `ui/observations.json`에 기록했다. 종료 시 실제 게임 프로세스·설정·기존 저장과 Steam 표시를 각각 확인한다.

이 기능의 지역·소유/통제 조건을 변경할 때는 [변경 영향 검토 절차](../HOK_CHANGE_COVERAGE_REVIEW.md), [주 참조 검토 스킬](../../.agents/skills/hok-state-reference-review/SKILL.md), [지리·출처 목록](../data/HOK_KOREAN_CHINESE_GOVERNMENT_STATE_GROUPS.json)을 먼저 읽는다. 효과·조건 안내를 바꿀 때는 [현지화 검토 스킬](../../.agents/skills/hok-localisation-review/SKILL.md)과 [두 채널 계약](2026-09-01-localisation-contract.md)을, 로그를 판정할 때는 [로그 검토 스킬](../../.agents/skills/hok-log-review/SKILL.md)을 먼저 읽는다.

## 확정한 구현 계약

1. 기존 597·743의 적격 기본 거점을 먼저 선택하고, **기존 중국 본토 63주 집합·완전 통제·소유국/통제국 적격 조건을 통과하는 SND 실제 소유 주 전부**를 추가 기본 선택한다. SND 핵심주만 가진 다른 나라 영토를 일괄 이전하지 않는다.
2. SND의 적격 본토 정복지·고립지도 기본 편입에 포함한다. 만주·섬/조차지 등 기존 지리 집합 밖 영토, 한국 소유 또는 통제, 일본 및 직접·2단계 일본 종속 관계의 보호는 우선한다. 따라서 SND가 보호 대상 주를 남기면 국가 소멸을 보장하지 않는다.
3. 다른 중국 국가는 새 기본 영토와 육지로 연결되는 후보 중 원소유국별 `적격 주 수 × min(0.90, 민주주의 지지도)` 예산으로 추가 선택한다. 기존 597·743은 해당 원소유국의 예산에서 차감한다. 고립 SND 기본 영토가 있으면 그곳도 추가 확장의 출발점이 되는 의도적 범위 변경이다.
4. SND 부재 시 기존 597·743 출범 경로를 유지한다. 두 곳 중 어느 곳도 원소유국을 병력 이관까지 생존시킬 안전한 첫 거점이 아니면 기존처럼 출범을 차단한다. 1038 단독 출범 fallback이나 보호 우회는 추가하지 않는다. MtG·기존 KCH 부재·가용 상실 취소 조건도 그대로다.
5. 선택을 마친 뒤 KCH 생성·안전한 첫 거점·필요한 기존 공군기지 확보 또는 기존 최소 1단계 보충·참여국 전력 이관·나머지 영토 이전 순서를 보존한다. 원국의 마지막 주는 전력 이관 뒤 넘긴다. 실제 참여국의 양수 p를 육해공·비축/연료에 공통 적용하고 p=0이면 이관 명령을 생략한다. **참여한 SND의 남은 소유 주가 하나 이상이고 전부 선택됨·현재도 이전 가능함을 재확인한 경우에만**, 비례 귀순 뒤 잔여 장비·수송선·연료를 0으로 만들어 소멸의 추가 승계를 막는다. 다른 국가와 보호·제외 주가 남은 SND는 이 처리를 하지 않는다. 지휘관은 귀순 대상에서 제외하며 소멸 뒤 생존을 보장하지 않는다.
6. 한국 피감독국·세력·본토 63주 핵심주·기존 전쟁명분·CHI 한정 후속 인정과 효과 종료 시 임시 상태 정리를 유지한다. 지도·시작 이력·중점 ID/35일/AI/좌표·다른 이념 경로는 변경하지 않는다. 자동 전쟁·공동 참전·기완료 저장 소급 지급도 추가하지 않는다.

## 변경 범위와 후보 처리

| 기능·파일 | 처리 | 근거·보존과 확인 단계 |
|---|---|---|
| [출범 효과](../../common/scripted_effects/HOK_KOR_chinese_government_effects.txt)의 SND 기본 선택·소멸 보정 | 수정 | 기본 선택 9줄과 비례 귀순 뒤 소멸 예정 SND의 잔여 자산 처리 24줄 추가. 지역/보호 필터·가용 조건·나머지 기존 효과 순서 재사용 |
| [공용 주 트리거](../../common/scripted_triggers/HOK_KOR_chinese_government_state_triggers.txt) | 의도적 유지 | 시작 baseline 바이트와 같음. 본토 63주·한국/일본 보호·완전 통제·안전 첫 거점 조건 유지 |
| [중점 호출부](../../common/national_focus/korea.txt)의 `KOR_overthrow_the_chinese_dictators` | 의도적 유지 | baseline 바이트와 같음. helper 호출·35일·가용/취소·AI·좌표·인정 결정 해금·16태그 전쟁명분 유지 |
| 본체 `korea_focus_l_korean.yml`·`korea_focus_l_english.yml` | 수정 | 기존 효과 `_tt`와 헤더 뒤 동일 기여 주석 갱신. 서술 `_desc`·키·기존 다른 내용 보존 |
| 본체 `HOK_KOR_chinese_government_l_korean.yml`·`_l_english.yml` | 수정 | 실제 고유 효과 키의 기본 SND 영토·타국 지지도·전력 비율 안내 갱신. 가용 3키와 paired 본문/BOM/줄끝 유지 |
| 외부 번역의 동명 기존 중점 `_tt`·`_desc` | 제외 — 별도 저장소 미수정 | 오래된 영어 본문이 남음. 고유 효과 파일은 외부 번역에 없으며 실제 한국어 UI에서 이번 기본 편입·폐기 안내를 확인함. 영어 채널 전체 갱신·영어 UI 검증으로 과장하지 않음 |
| [인정 결정](../../common/decisions/KOR_decision.txt)의 `KOR_New_China_Government`·공용 63주 핵심주 | 의도적 유지 | CHI 한정 합병·조건·비용·완료 이력 유지. 다른 군벌 일괄 합병 아님 |
| SND 시작 이력·상속 사건/on_action | 제외 — 직접 변경 없음 / 상호작용 검토 | SND를 시작 시 없애지 않음. 국가 소멸 뒤 잔여 자산·후속 존재/부재 접점은 범위를 제한해 검토·실행 구분 |
| 지리 목록·계획·이 기록·README | 수정 — 유지 기록 | 기존 지리 집합은 유지하고 1038의 기본 편입 역할·이전/현재 계약·외부 증거 위치와 실제 검증 상태를 갱신 |

## 소스 확인

`TASK/source-review/implementation-minimal-delta.json`은 최초 선택 후보에 9줄만 추가됐고 trigger·중점이 baseline과 바이트 일치함을 확인한 이전 단계 보고서다. 이때 출범 효과 SHA-256은 `7cedd40d9585d4231fedb4d2ea372f92a28bdec2c164d9dc7b0790e6d88f2167`이었다. 장비·연료 처리를 18줄 더한 중간 r2 효과는 `49b5c27b6ec7783c7edf7d3929eef0ce9aa3fdaec8b6af0d3a98c91ee78bdbe1`이며 `source-review/implementation-final-delta.json`이 당시 총 27줄을 확인한다. 이후 수송선만의 잔여 처리 6줄을 기존 guard 안에 추가한 **최종 r3 효과 SHA-256은 `b9318ca802c0b4f266d7cb140761ba34e132d4cfa70384deb08e1a032a2de052`**이고, `source-review/implementation-final-r3-delta.json`이 baseline 대비 정확한 두 삽입·총 33줄·순서·보존·임시 변수 API를 확인한다.

기존 candidate 필터를 통과한 미선택 주만 재사용 helper로 선택하므로 중복 차감이 없으며, SND 예산이 음수가 되어도 SND 미선택 적격 주가 남지 않고 효과 끝에서 snapshot 국가의 변수를 정리한다. 새 잔여 자산 처리는 `every_country`의 참여 SND 한정·현재 소유 주 존재·모든 남은 주의 선택 및 이전 가능 조건을 검사한 뒤 수행한다. 소스 확인은 등록·UI·효과 실행·저장 검증을 대신하지 않는다.

현지화 최초 정적 확인은 `source-review/localisation-review.json`의 60/60이고, 장비·연료 폐기의 r2는 `source-review/localisation-review-final-r2.json`의 69/69다. 수송선까지 명시한 최종 paired 4파일은 `source-review/localisation-review-final-r3.json`의 **69/69**다. 이 검사 수들을 합산하지 않는다. 각 보고서는 `_desc`·가용 3키·키 집합·BOM/개행과 다른 본문 보존, 고유 효과의 실제 중점 호출 및 외부 번역 경로를 구분한다. 최초 문서·runtime 1,595파일 범위 확인도 `documentation/source-and-links.json`의 해당 SHA·시점 결과이며 이후 최종 소스 결과로 바꾸어 기록하지 않는다.

최초 정적 보고는 CRLF를 잘못 가정해 newline 항목을 실패로 표시했다. `source-review/implementation-minimal-delta-first-newline-check.json`에 보존하고 baseline과 변경본이 모두 LF임을 대조하여 교정했다. 실제 파일을 다시 포맷한 것이 아니며 LF 159→168의 정확한 9줄 증가다.

## 실행 검증과 남은 항목

### 최초 선택 소스와 소멸 통제에서 확인한 추가 승계

최초 효과 해시 `7cedd40d…f2167`의 production `zero` 실행은 지지도 0%에서도 기본 597·1038·743 세 주, SND 소멸, 한국 피감독국 지위·보호·임시 자료 정리를 확인했다. 그러나 전력 이관 명령을 생략해도 비축 장비·연료가 새 정부에 생겨 자산 0 기대는 실패했다. 복사한 zero 진단에 잘못 남은 「군대를 받아야 한다」 기대 1건은 별도의 fixture 오류로 구분하며 최종 0% 사례에서는 교정한다. 이 실행을 최종 통과로 표시하지 않는다.

독립 `elimination0-r2`는 새 정부의 거점·비행장과 살아 있는 SND를 먼저 준비하고 귀순 명령 없이 마지막 1038을 이전했다. SND의 비축 소총 1,000,002·육군 장착 소총 14,252에서 KCH 비축이 **0→1,003,565**로 늘었으며 육해공 수량은 추가되지 않았다. 이는 `1,000,002 + 14,252 × 0.25`와 일치한다. 설치 원본 `common/defines/00_defines.lua` 650–653행은 `ANNEX_STOCKPILES_RATIO = 1.0`, `ANNEX_FIELD_EQUIPMENT_RATIO = 0.25`, `ANNEX_FUEL_RATIO = 0.25`, `ANNEX_CONVOYS_RATIO = 0.15`를 정의한다. 이 소스와 같은 실행의 전후 getter는 국가 소멸에 따른 추가 자산 승계를 강하게 지지하며, 전역 define을 바꾸어 해결하지 않는다.

첫 `elimination0`에는 실제 getter와 별개로 staging assertion의 getter를 일반 trigger처럼 쓴 진단 구문 오류 2건이 있었다. 이를 교정한 `elimination0-r2`에서도 비축·연료 추가 승계 기대의 3 FAIL이 재현됐다. 첫 raw 오류와 교정 후 재현을 별도로 보존한다. 하이픈이 있는 사례명의 저장 검색 glob 오류와 수집 요약의 UTF-8 stdout을 기본 cp949로 읽어 경로가 깨진 문제도 helper/보고서 층에서 교정했다. 이미 생성한 원본 저장·캡처를 삭제하지 않고 잘못된 요약을 superseded로 보존한다.

독립 `clear0`에서는 귀순 명령을 생략한 뒤, 마지막 주를 넘기기 전에 SND에 정식 country 효과 `set_equipment_fraction = 0`·`set_fuel = 0`을 적용했다. 측정한 비축 소총은 **1,000,002→0**, 육군 장착 소총은 **14,252→0**, 연료는 **28.878k→0**이었고 사단·함정·배치 항공기 개수는 이 시점에 그대로였다. 마지막 주 이전 뒤에는 KCH의 검사한 각군·비축·장착·연료가 전부 0이었다. **10 native PASS / 0 FAIL**은 이 독립 통제 범위이며 production 보정이나 모든 장비 종류의 포괄 검증을 대신하지 않는다. 부분 귀순분 보존과 수송선은 후속 통제로 구분한다.

`set_equipment_fraction`·연료 효과·바닐라 실례는 `TASK/source-review/residual-stockpile-primary-source.json`과 후속 대안 조사에 기록했다. archetype 47개를 정적으로 순회해 비축을 지우는 대안은 외부 `source-review/candidate-stockpile-drain-47.txt`에만 준비했으며, 이 글 작성 시 production에 넣거나 그 대안의 엔진 검증을 수행하지 않았다.

독립 `clear20`의 **9 native PASS / 0 FAIL**과 실제 저장 getter는 귀순 직후 KCH의 **18개 사단·9척·27기·소총 비축 200,000·육군 장착 소총 2,964·연료 5.77507k**가 SND 잔여 처리 직후와 마지막 주 이전 뒤까지 각각 동일함을 확인했다. 남은 SND의 소총 비축·장착·연료는 0이 되었으며 소멸 뒤 각군이 사라졌다. 다만 이 합성 통제에서는 최초 597 이전 뒤 SND가 항구를 잃은 조건에서 p=20% 명령에도 9척 전부가 이관됐다. 항구 상실과 함정 배분의 인과는 독립적으로 입증하지 않았다. 비율 입력·실제 단위별 배분·항구 상실 조건을 구분하며 **함정 수가 정확히 지지도 비례라는 통과로 사용하지 않는다**. 수송선과 최종 production 결과는 후속 실행으로 구분한다.

### 수송선 예외와 최종 r3 보정

r2 소스에서 실행한 `clear70-convoys`의 공식 `num_equipment@convoy` getter는 SND **140→42(귀순 후)→42(장비/연료 처리 후)→0(소멸 후)**, KCH **0→98→98→140**이었다. p=70% 귀순은 98척으로 정상이나 소멸 때 잔여 42척이 추가됐다. 설치 define의 `ANNEX_CONVOYS_RATIO = 0.15`와 이 실제 42척 전부의 승계는 별개 사실이며 내부 적용 경로를 단정하지 않는다. 같은 진단의 `num_convoys`는 공식 동적 getter가 아니었고 모두 0으로 기록돼, 이를 함께 요구한 staging 기대의 FAIL은 별도 진단 오류로 남겼다. 최종 production 진단에서는 이 미입증 getter를 제거한다.

이후 `clear70-convoy-drain`은 장비·연료 처리 뒤 잔여 `num_equipment@convoy`를 임시 변수로 읽고 음수로 바꿔 `add_equipment_to_stockpile = { type = convoy_1 amount = var:... }`로 제거했다. **11 native PASS / 0 FAIL** 및 실제 저장에서 SND **140→42→0→0**, KCH **0→98→98→98**을 확인했다. 다른 측정 자산인 KCH **64개 사단·9척·93기·소총 비축 700,000·장착 소총 9,676·연료 20.21407k**도 귀순 직후부터 마지막 주 이전 뒤까지 동일했다. 임시 값 `HOK_SFI_convoy_drain`은 이 저장에 대소문자를 무시한 이름 검색으로도 없었다. 증거는 `runtime/clear70-convoy-drain-metrics.json`·`runtime/clear70-convoy-temp-readback.json`·실행별 source manifest다.

정식 근거는 설치본 `common/decisions/NOR.txt` 23–29행의 음수 `convoy_1` 제거, 36–46행의 `num_equipment@convoy` 사용과 `common/units/equipment/convoys.txt`의 현재 단일 구체 모델이다. `source-review/convoy-remainder-primary-source.json`에 원문·행·해시를 기록했다. 생산국을 제한하지 않고 남은 수송선 전체를 제거하되, 기존 SND 소멸 guard 안에서만 실행한다. 이 독립 통제의 코드는 r2 소스를 로드한 외부 probe이며, 승격한 r3 production의 5개 사례·UI·저장 왕복은 아래에서 따로 기록한다.

### 최종 r3 production 사례

`runtime/final-production-freeze.json`의 8개 runtime 원문과 hash를 고정하고 각 시작 전에 일치를 확인한다. 그중 이번 실제 delta는 효과 1파일·현지화 4파일이다. `runtime/final-source-copy/`는 최종 8파일 원문 사본이며, 이전 27줄 r2의 동결 목록은 superseded 사본으로 보존했다. 각 실행의 348파일 start/capture manifest는 더 넓은 텍스트 소스 범위이며 전체 바이너리 검증이나 두 샘플 사이의 일시 변경 부재를 입증하지 않는다.

| 사례 | 확인 상태 | 범위·남은 판독 |
|---|---|---|
| `zero-final` | **611 native PASS occurrences / 0 FAIL**, start/capture source 동일 | 실제 D04 소유는 597·743·1038만. SND 소멸·피감독국·63주 핵심주·각군/비축/장착/수송선 0·보호·정리 확인 |
| `low-final` | **613 native PASS occurrences / 0 FAIL**, start/capture source 동일 | 실제 D04 소유 5주(597·598·607·743·1038), 21개 사단·4척·26기·소총 비축 200,000·장착 3,092·수송선 28 |
| `high-final` | **610 native PASS occurrences / 0 FAIL**, start/capture source 동일 | 실제 D04 소유 44주, 170개 사단·6척·92기·소총 비축 700,246·장착 22,404·수송선 101. 다른 donor·엔진 단위 배분과 구분하며 모든 자산의 정확한 p 비례를 주장하지 않음 |
| `partial-protection` | **20 native PASS / 0 FAIL**, start/capture source 동일 | 한국 1084·일본 1001 부분 province 통제 유지, SND 1038·일본 통제 599·MAN 1034·일본 종속 HBC 1032 보존. 고립 SND 325 편입·만주 610 제외와, 보호 주가 남은 SND의 0% 백만 소총 비축·부대 불변 확인 |
| `no-ncns` | **603 native PASS occurrences / 0 FAIL**, start/capture source 동일 | 실제 NCNS 비활성·SND 부재. 두 거점을 한국이 소유할 때 출범 gate 차단·helper 무효·소유 보존, CHI 소유로 복원한 뒤 형성 가능·기존 두 거점·0% 검사 자산 0·새 비행장 없음의 순차 관측 |

611·613 등의 수는 같은 정리·핵심주 조건을 여러 곳에서 평가한 **발생 횟수**이며 고유 기능 수나 서로 합산한 통과 수로 사용하지 않는다. native fixture는 출범 helper와 실제 중점 보상을 강제로 실행한 합성 조건이므로 정상 중점 시간 진행을 대신하지 않는다.

같은 최종 r3·동일 초기 자산을 준비한 0%→20%→70%의 관측은 **3→5→44주**, 육군 **0→21→170개 사단**, 함정 **0→4→6척**, 배치 항공기 **0→26→92기**다. 서로 다른 fresh 실행의 지정 결과이며 같은 난수 seed·모든 단위의 정확한 비율·다른 소멸 donor의 자산 처리까지 입증하지 않는다. 이번 잔여 처리는 SND에만 적용하며 다른 donor의 기존 처리는 유지한다. 이전 소스의 7→42주·26→185기 결과를 이번 값으로 재사용하지 않는다.

지정 실제 저장 getter는 `runtime/zero-final-metrics.json`·`runtime/low-final-metrics.json`·`runtime/high-final-metrics.json`에 기록한다. `runtime/final-temporary-state-readback.json`은 최종 텍스트 저장에서 새 수송선 임시 값까지 포함한 생산 scratch 11개 이름의 부재를 대소문자 무시 검색으로 확인한 범위다. 이것은 일반 저장 재로드나 바이너리·기존 캠페인 호환성 검증을 대신하지 않는다.

`zero-final`의 초기 효과 직후 평화 검사는 통과했지만, 뒤 `-ai_testing` 실행의 **1936.1.2.02**에는 한국의 신강 대상 선전포고 로그가 있었다. 강제 보상 직후와 뒤 AI 활동을 구분한다. 이번 production delta에는 전쟁 선언·참전 명령이 없고 기존 전쟁명분 loop·AI 설정은 baseline과 같으며, 이 로그를 새 강제 선전포고 효과가 추가됐다는 증거로 바꾸지 않는다. 실제 플레이어 UI의 정상 진행은 `-ai_testing` 없이 별도로 확인한다.

지휘관의 경우 `source-review/snd-commander-final-save-readback.json`이 설치본 SND 시작 이력의 두 기존 군 지휘관 `CHI_sun_tongxuan`(5358:type73)·`SND_han_fuju`(5380:type73)를 최종 `zero-final`·`high-final` 및 실제 UI 첫/재로드 후 텍스트 저장 4개에서 추적했다. 모두 global historical의 `country="SND"`와 SND의 unit-leader 등록을 유지하고, 실제 명부가 존재하는 D04/KCH의 지휘관 등록에는 두 ID가 없었다. 이 4개 관측에서는 기존 SND 지휘관의 자동 KCH 합류가 없음을 확인했다. 소멸한 SND의 역사 기록 잔존을 지휘관의 생존·사망·UI 선택 가능성으로 바꾸어 해석하지 않으며, 이후 새로 모집한 모든 인물이나 장기 상속 경로를 검증한 것도 아니다.

### 실제 중점 UI와 정상 시간 진행

최종 r3의 `ui-ready`는 선행 중점·한국 민주정/세력·정치력과 SND 20%·다른 중국 donor 0%만 외부에서 준비했다. 「중국 독재자 축출」은 미완료였고 출범 helper도 실행하지 않았다. 시간 가속 define·`-ai_testing` 없이 플레이어가 실제 중점을 시작하고 일반 시간을 진행했다. 전체 정치 경로의 자연 진행을 시험한 것은 아니다.

`ui/observations.json`과 `01-focus-tooltip.png`~`07-supervised-state.png`에 다음 관측을 기록했다.

- 1936.1.1.12의 실제 한국어 중점 안내에서 녹색 가용 조건·35일 표기, SND 적격 본토 전부·타국 지지도 규칙·각군/비축 비율 및 소멸 SND의 장비·수송선·연료 폐기를 확인했다.
- 실제 시작 버튼으로 중점이 활성화됐고 1936.1.14.16의 진행 막대 증가와 1936.2.4.1의 완료 팝업을 확인했다. 중점 자동완료·직접 보상 명령은 사용하지 않았다. 초기 축적 진행과 팝업 중 시간 진행이 있으므로 정확히 35일 경과했다고 계산하지 않는다.
- 완료 팝업을 닫고 1936.2.11.18에 일시정지했다. 산둥 자유 공화국 외교창의 민주정부·산둥 지도 표시, 한국 국기와 **피감독국** 관계 툴팁을 확인했다. 화면만으로 63주 핵심주나 자산 수량 전부를 입증하지 않는다. 표시된 `HOK_SFI_UI_DIAGNOSTIC_FACTION`은 외부 준비용 세력명이다.
- 원래 예정한 `HOK_SFI_UI_20261119_01` 대신 실제 UI 기본 이름 `KOR_1936_02_11_18`을 사용했다. 입력 필드에 사용자 지정 문자열이 반영되지 않아 기본 이름과 `_temp` 파일이 모두 없음을 먼저 확인하고 Local Save를 눌렀다. 생성 원본은 실제 사용자 저장 폴더의 `KOR_1936_02_11_18_temp.hoi4`(72,764,131바이트)이며 `08-after-ui-save.png`와 별도 수집 기록으로 구분한다. 정상 메뉴의 게임 종료→OK 뒤 게임 창이 사라짐을 확인했다. `_temp` 생성과 완전한 재로드 성공 여부는 별개로 검증한다.

### 새 프로세스에서 실제 저장 왕복

첫 UI 저장의 SHA-256은 `d536ab6766b71326664988ad7961046576ec7bc1e2a917af1f469a15ea71d352`이며 `runtime/ui-first-save-contract.json`·`runtime/ui-first-save-native.json`·`runtime/ui-first-save-context.json`에 텍스트 판독을 보존했다. D04의 597·743·1038 소유, 공용 목록과 정확히 일치한 본토 63주 핵심주, 민주정부·피감독 관계·축출 중점 완료와 생산 scratch 11개 이름 부재를 확인했다. 저장 시점의 군대는 2개 사단·함정 0·배치 항공기 0이었다. 관계의 시작 기록은 완료 팝업과 같은 **1936.2.4.1**이다. 저장 헤더의 실행 checksum `22b5`는 설치 메타데이터의 `c184`와 구분한다.

첫 게임을 정상 종료하고 설정을 복원한 뒤, **새 PID 5892**에서 원래 HOK+외부 English Translation 두 모드만으로 실행했다. 진단 probe·`-ai_testing`은 없었으며, 두 번째 저장 판독을 위해 텍스트 저장 설정만 임시 유지했다. 1936.1.1.12의 일반 초기 게임에서 실제 메뉴→Local Load로 `KOR_1936_02_11_18_temp`를 선택하고 불러오기를 눌렀다. `ui/09-fresh-original-playset.png`~`12-reloaded-supervised-government.png`와 관측 목록에 초기 상태·선택 파일명·실제 로딩·복원된 1936.2.11.18의 민주정부/한국 피감독국 표시를 남겼다.

재로드 뒤 일반 시간을 **1936.2.15.1**까지 진행하고 다시 일시정지했다. `13-reloaded-time-advanced.png`·`14-new-resave-name.png`에 진행 및 새 이름을 기록하고, 존재하지 않음을 확인한 `KOR_1936_02_15_01`로 Local Save했다. 새 원본은 사용자 저장 폴더의 `KOR_1936_02_15_01_temp.hoi4`(72,644,858바이트)다. 두 번째 게임도 정상 메뉴의 게임 종료→OK로 종료했다. 이 결과는 첫 `_temp` 저장의 실제 재로드·짧은 진행·별도 재저장을 확인한 것이며, OneDrive 저장 경로의 정상 이름 rename 오류가 해결됐다는 뜻은 아니다. 두 번째 저장 판독·최종 설정/원본/프로세스 복원은 아래 결과를 따른다.

두 번째 저장 SHA-256은 `e32ba8ef5c96e26256cc67bbaebadc2aa8b221cf13e1d9e0f3fdb9ac0ee915b3`이다. `runtime/ui-after-reload-save-contract.json`은 재로드 후 **79게임시간** 진행한 1936.2.15.1에도 민주정부·피감독 관계·3주 소유·정확한 63주 핵심주·축출 중점 완료·생산 scratch 11개 이름 부재와 관계 시작일 1936.2.4.1이 유지됨을 확인한다. 두 번째 저장의 실행 checksum `f685`는 원래 두 모드 구성의 값이고 첫 진단 준비 저장의 `22b5`와 구분한다. 두 저장·실행별 동결 소스의 종합 대조는 `runtime/ui-roundtrip-comparison.json`, 원본과 외부 증거 사본의 경로·바이트·해시는 `runtime/ui-saves/`의 수집 manifest를 따른다. 런타임 전체 색인은 `runtime/RUNTIME_CLOSEOUT.md`다.

### 최종 보존·복원과 완료 범위

`runtime/final-save-preservation.json`은 기존 저장 **157개·11,441,308,865바이트 전부의 SHA-256 일치**, profile **11/11**의 시작 바이트 복원, 원래 없던 보조 파일의 부재, 임시 probe pointer의 부재와 게임 프로세스 목록 `[]`를 확인한다. 복원은 두 번째 정상 종료 뒤 **2026-11-19 07:53:12 UTC**에 수행했다. `continue_game.temp`도 이번 시작 원본으로 복원했으며 이전 작업에서의 복원 예외와 혼동하지 않는다. 게임이 생성한 신규 저장 14개(합성/native 12개·실제 UI 2개)는 실제 사용자 폴더에 원본을 두고 외부 TASK에 증거를 복사했다. 기존 원본이나 신규 게임 원본을 정리 목적으로 삭제·이동하지 않았다.

`runtime/final-source-preservation.json`은 시작 runtime 1,595파일 중 효과 1개·현지화 4개만 변경됐고 다른 1,590개는 동일함을 확인한다. 최종 동결 8파일은 현재 소스·증거 사본과 각각 일치한다. 작업 시작부터 있던 Git 변경을 보존했으며 커밋·푸시·외부 게시를 수행하지 않았다.

`runtime/final-log-review.json`은 원래 두 모드·진단 없는 마지막 실행과 보존한 시작 로그를 제한적으로 대조했다. 변경한 출범 helper·효과·현지화 경로·임시 수송선 변수·event target의 오류 일치와 변경 중점 키의 충돌 일치는 없었다. 전체 모드의 무오류를 뜻하지 않는다. 시작 로그에도 있던 descriptor 경고·OneDrive rename 오류가 남으며, 마지막 로그의 `map/buildings.txt:66858` 인자 오류와 함장/부대 훈장 현지화 충돌은 이번 r3 전 최초 독립 통제에도 있었다. 이 지도/현지화 파일들은 시작 runtime 대조에서 바뀌지 않았다. 바닐라 단독 통제 없이 오류를 바닐라 탓이나 HOK 무관으로 확정하지 않았고 이번 출범 수정에 섞어 수리하지 않았다.

게임의 실제 종료와 별도로 Steam의 시작 전부터 남아 있던 실행 중 표시를 확인했다. Steam의 정지→확인 뒤에도 중지 중에 머물러, 다른 게임 실행·다운로드 표시가 없는 상태에서 Steam 메뉴의 **정상 종료** 후 다시 실행했다. 라이브러리에서 HOI4의 **녹색 플레이 버튼**과 실행 중 표기 부재를 직접 확인했다. `ui/15-steam-stopping.png`·`ui/16-steam-play-restored.png`·관측 목록에 이를 기록했다. 다른 앱을 강제 종료하거나 개인정보 수집 질문을 조작하지 않았다.

최종 r3의 대표 production 5개 사례는 각각 기능 FAIL 0이며 source 안정성을 확인했고 실제 UI·중점 진행·새 저장 재로드/추가 진행/재저장과 위 보존·복원도 확인했다. native source·실제 저장·UI·정상 진행·복원 범위를 한 통과 수로 합산하지 않는다. 요청한 변경과 그 핵심 검증은 완료했으며 아래 장기·기존 캠페인 등의 미검증 한계는 남는다.

문서·범위 검토 보고서 TASK/documentation/source-and-links-final-post-ui.json은 58/58 소스·기록 대조 및 상대 링크/anchor 259개를 확인한 별도 층이다. 지휘관·로그 문단까지 포함한 마지막 문서 스냅샷은 TASK/documentation/source-and-links-closeout.json에 기록한다. 앞선 source-and-links-final-r3.json과 최초 보고서는 그 당시 소스·문서의 스냅샷으로 보존한다. 이 문서 검토 수를 native 검사나 실제 UI 통과 수로 합산하지 않는다.

이전 [출범 구현 기록](2026-11-19-shandong-democratic-government.md)의 6개 native·실제 UI·저장 결과는 전면 편입 전 소스의 이력이다. 이번 시험의 통과 수나 새 설명의 UI 확인으로 합산하지 않는다. 기존 캠페인·1939 bookmark·장기 AI·모든 DLC·멀티플레이는 이번 변경에 맞춘 실행 범위와 구분하며 미실행 상태에서 호환을 주장하지 않는다.

기존 `docs/assets/korean-fascist-mobilization-validation-20260923/`의 시험 PNG 4개·총 815,391바이트는 별도 정리 미결이다. 이번 작업의 신규 시험 자료는 외부 TASK에만 생성하며 기존 PNG·기존 저장 원본을 이동·삭제하지 않는다.
