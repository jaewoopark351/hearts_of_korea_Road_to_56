# 2026-11-08 원본 국토개발·표시·지도 참조 업데이트 이식 계획

작성일: **2026-11-08, Asia/Seoul**. 최초 문서화 당시 상태: **문서화만 승인 / 최신 추가 콘텐츠 미이식 / 당시 게임 정적·런타임 검사 미실행**.

**같은 날 후속:** 사용자가 전체 구현과 별도의 실제 시험용 프로필 임시 변경·게임 실행을 승인했다. [ADR-0007](../decisions/0007-november-content-integration.md)과 [구현·검증 기록](../implementation/2026-11-08-hok-upstream-content-port.md)을 현재 적용 상태로 따른다. 아래 미이식·미실행 문구와 후보 목록은 최초 계획의 이력이며, 후속32출력의 실제 적용·관측을 대신하지 않는다.

사용자가 원본 업데이트 확인 후 요청한 “문서화 작업만”의 결과다. 기존 15주 분할과 그 검증 기록을 보존하고, 그 뒤 원본에 추가된 내용을 기능별로 비교하여 후속 이식 범위와 확인 순서를 제안한다. 이 문서는 게임 파일·이미지·생성기·잠금·활성 캐시·사용자 설정 변경, 검사나 게임 실행, 정리·커밋·게시를 승인하지 않는다.

## 1. 읽을 조건과 기준 자료

| 다음 작업의 조건 | 먼저 읽을 자료와 용도 |
|---|---|
| 이 계획을 구현하거나 범위를 조정할 때 | [프로젝트 지침](../../AGENTS.md). 최신 요청의 운영 모드와 RT56 호스트 보존 규칙을 우선한다. |
| 기존 주 분할·수혜 주·ID를 다룰 때 | [ADR-0006](../decisions/0006-korean-state-split-integration.md), [포트 대응표](../data/HOK_KOREAN_STATE_SPLIT_PORT_MAPPING.json), [분할 구현 기록](../implementation/2026-11-07-korean-state-split-port.md). 기존 47출력과 역사적 실행 범위를 보존한다. |
| 기존 분할 입력을 재현할 때 | [동결 입력 안내](../upstream/hok-state-split-20261107/README.md), [분할 잠금](../../tools/hok_state_split_lock.json). 원본 HEAD만으로 이전 미커밋 입력을 복원하지 않는다. |
| 새 국토개발 사업의 의도·배분·원본 증거를 해석할 때 | 원본의 [CNDP 적용 명세](../../../hearts_of_korea/docs/HOK_KOREAN_CNDP_STATE_DEVELOPMENT_PLAN.md), [사업 배분 JSON](../../../hearts_of_korea/docs/data/HOK_KOREAN_CNDP_STATE_PROJECTS.json), [구현 기록](../../../hearts_of_korea/docs/incidents/2026-11-08-korean-cndp-state-development.md). 계획 아래의 최초 제안과 최종 적용 명세를 구분한다. |
| 표시 수리나 지리 참조 정렬을 설계할 때 | 원본의 [표시 구현 기록](../../../hearts_of_korea/docs/incidents/2026-11-08-localisation-display-implementation.md), [지도 참조 정렬 기록](../../../hearts_of_korea/docs/incidents/2026-11-08-state-reference-alignment.md). 원본 대상·실패·미검증을 포트 결과로 옮기지 않는다. |
| 새 검토 절차를 호환판에 맞추어 정리할 때 | 원본의 [변경 영향 검토 절차](../../../hearts_of_korea/docs/HOK_CHANGE_COVERAGE_REVIEW.md), [현지화 검토 스킬](../../../hearts_of_korea/.agents/skills/hok-localisation-review/SKILL.md), [주 참조 검토 스킬](../../../hearts_of_korea/.agents/skills/hok-state-reference-review/SKILL.md). 7절의 언어·호스트 차이를 적용한다. |
| CNDP 그림을 복사·수정하거나 과거 입력을 재사용할 때 | [호환판 개발 자료 안내](../HOK_DEVELOPMENT_ARTIFACT_ARCHIVE.md), 원본의 [CNDP 그림 출처](../../../hearts_of_korea/docs/HOK_KOREAN_CNDP_ARTWORK.md), [아이콘 manifest](../../../hearts_of_korea/docs/data/HOK_KOREAN_CNDP_ICON_MANIFEST.json). 실제 제작 원본과 런타임 DDS의 역할을 구분한다. |

원본 링크는 `C:\hoi\hearts_of_korea`의 읽기 전용 **현재 파일**이다. 이번에 새 동결 사본을 만들지 않았다. 이후 HEAD가 바뀌면 아래 커밋과 해시를 기준으로 다시 비교한다. 기존 `docs/upstream/hok-state-split-20261107/`의 보관본을 최신 원본으로 덮어쓰지 않는다.

## 2. 이번 읽기 확인의 기준선

| 항목 | 확인값·한계 |
|---|---|
| 호환판 소스 | `C:\hoi\hearts_of_korea_Road_to_56`, `feat/korean-focus-update-20260922@3d9355b70152794ed974dcf183323c24206d900a` |
| 호환판 작업 트리 | 이전 15주 분할의 런타임·생성기·문서 수정과 미추적 파일이 존재한다. 이번 문서 변경의 이전 작업이며 그대로 보존한다. clean 또는 HEAD만의 트리로 기술하지 않는다. |
| 원본 소스 | `C:\hoi\hearts_of_korea`, `feat/korean-focus-expansion-ai@596b221bb994d93fce552d3ee1ba70fa9b5640f1`, 작업 트리 clean |
| 원본 새 런타임 커밋 | `1e5c907`, 2026-11-08 20:49:03 KST. 88파일, +6,845/-775. 이미 이식한 분할 변경도 함께 포함하므로 전부 새 미이식량이 아니다. |
| 원본 새 지침 커밋 | `596b221`, 2026-11-08 20:49:12 KST. 5파일, +248/-1. 게임 런타임 변경은 없다. |
| 이전 선택 입력 | donor `0d73d49726abbfa435c73f1bf8cc24d4a5af014b` 위 미커밋 분할 입력 42개. 분할 잠금과 보관본으로 특정하며 0d73d49 checkout 자체와 구분한다. |
| 설치 메타데이터 재조회 | `appmanifest_394360.acf`의 Steam build `26409260`, `appworkshop_394360.acf`의 RT56 설치/상세 manifest 모두 `7553774178744855191` |
| 게임·실행 기준 | 이전 분할 기록의 HOI4 `1.19.4.2.2da5`, DLC 36개와 실행별 체크섬은 역사적 관측이다. 이번에는 게임을 실행하거나 현재 playset·DLC·언어·유효 우선순위를 새로 입증하지 않았다. |
| 의존성·정체성 | 실제 호환 descriptor는 RT56와 Korean Language, `1.19.*`, 기존 호환판 ID `3796816200`을 선언한다. donor ID `3793992662`, 역사적 HOK `2898629778`, RT56 `820260968`과 구분하며 어느 항목도 이번에 변경·업로드하지 않는다. |
| 언어 미결 | 이전 실제 시험의 RT56 Korean Translation과 선언된 Korean Language 차이는 남아 있다. 원본 일반판의 활성 번역을 포트의 의존성으로 추가하지 않는다. |

선택 파일의 SHA-256을 읽기 조회했다. 이는 전체 소스 불변·등록·게임 동작 검증이 아니다.

| 원본 상대 경로 또는 기록 | SHA-256 |
|---|---|
| `common/decisions/KOR_decision.txt` | `9A22D108DC50533BFF5E9DED621B4DB826A1D29709F9996CFC629A3E6E7EC9E4` |
| `common/national_focus/korea.txt` | `1E465973FC220C227F91DCEF7DAE1E30D99E811C462F00198CEA30CCF0CB5365` |
| `common/national_focus/japan.txt` | `1A9E1135F0123E752D206A82420F716227402DD49EB0E8BF369931FA57423DAE` |
| `common/national_focus/china_shared_TSR.txt` | `158B5BFCCF20AAA779FCD787E960C677B4E01FE14680EAAE8D26AEF570DC2222` |
| `events/korea.txt` | `ABE66AF64D6FB0BF15FB18FCBB7BCBAC50306EB6B60E79D77B486401CA398206` |
| 원본 `AGENTS.md` | `A9AE0C8A006D352CDCD0B32EEDB5DECA352E5C937D8C8587EDC9062A794E8103` |
| 원본 `descriptor.mod` | `3FBC6868A7D95BACD6B55AF71593A61AF3A7EADA5654D46CC4C828422ECA032A` |
| 호환판 `tools/hok_state_split_lock.json` | `521D8A8CA637AEAEDF014E094317A2B8F25EF7E5B1B175053C221EEF9E0FE8A9` |

## 3. 파일 차이 재고와 집계 규칙

기존 동결 donor 42입력과 최신 원본을 SHA-256으로 읽기 대조한 결과 **37개 동일·5개 변경**이다. 동결 범위 밖에서 `0d73d49..596b221`에 변경된 런타임은 **31경로**다. 합계 **36경로는 추가 검토 후보**이며 최종 이식 수나 출력 수가 아니다. 여기에는 이미 별도 적용한 연구망 표시 2개와 기존 제외 정책의 몽골 모듈 1개가 포함된다. 한국 주 정의와 `map/buildings.txt` 등 기존 분할 지도 입력은 동결본과 같다.

### 3.1. 기존 동결 입력 중 추가 변경된 5개

| 경로 | 새 검토 내용 | 후속 통합 분류 제안 |
|---|---|---|
| `common/decisions/KOR_decision.txt` | CNDP13, 옛7개 분기, 쓰시마・KCH 코어・해방 지역 목록 | 기존 한국 출력에 선택 병합. 원본 전체 복사 금지 |
| `common/national_focus/korea.txt` | CNDP 해금・해주 요새・인도차이나 통제・일본 보호령 조건 | 기존 `OVERRIDE`의 HOK delta 갱신 |
| `common/national_focus/japan.txt` | 일본 트리의 중국・태평양 섬・한반도 요새 수선 | `THREE_WAY_MERGE` 또는 `USE_RT56` 판단 대기 |
| `common/national_focus/china_shared_TSR.txt` | 인도차이나 우회 조건에 donor state1017 추가(V-03) | `THREE_WAY_MERGE` 또는 `USE_RT56` 판단 대기 |
| `events/korea.txt` | 외교 영토 이전·지역 범위 | 기존 RT56 지역 병합을 보존하는 선택 병합 |

### 3.2. 동결 범위 밖의 31개

아래 18개 텍스트 경로와 DDS13개를 각각 센다. `ADD`·`ASSET_COPY` 등은 향후 충돌·출처 검토를 거쳐 확정할 후보이며 이번에 통합 원장을 바꾸지 않았다.

```text
common/decisions/HOK_KOR_civic_decisions.txt
common/on_actions/mongppong_on_actions.txt
common/script_constants/zzzz_HOK_KOR_state_reference_constants.txt
common/scripted_effects/00_HOK_KOR_state_reference_effects.txt
common/scripted_triggers/HOK_KOR_civic_triggers.txt
common/scripted_triggers/HOK_KOR_cndp_triggers.txt
events/HOK_KOR_civic_events.txt
history/countries/KCH - Korean China.txt
history/countries/KOR - Korea.txt
interface/HOK_KOR_cndp_icons.gfx
localisation/english/HOK_KOR_civic_state_l_english.yml
localisation/english/HOK_KOR_cndp_state_development_l_english.yml
localisation/english/HOK_KOR_democratic_expansion_l_english.yml
localisation/english/HOK_KOR_research_network_l_english.yml
localisation/korean/HOK_KOR_civic_state_l_korean.yml
localisation/korean/HOK_KOR_cndp_state_development_l_korean.yml
localisation/korean/HOK_KOR_democratic_expansion_l_korean.yml
localisation/korean/HOK_KOR_research_network_l_korean.yml
```

DDS 경로 접두사는 `gfx/interface/decisions/HOK_KOR/cndp/`이며, 다음 파일 13개다.

```text
cndp_chungcheongbuk.dds
cndp_chungcheongnam.dds
cndp_gangwon.dds
cndp_gyeongsangbuk.dds
cndp_gyeongsangnam.dds
cndp_hamgyeongbuk.dds
cndp_hamgyeongnam.dds
cndp_hwanghaebuk.dds
cndp_hwanghaenam.dds
cndp_jeollabuk.dds
cndp_jeollanam.dds
cndp_pyeonganbuk.dds
cndp_pyeongannam.dds
```

신규 지침 5경로는 별도 집계한다: `AGENTS.md`, `README.md`, `docs/HOK_CHANGE_COVERAGE_REVIEW.md`, `.agents/skills/hok-localisation-review/SKILL.md`, `.agents/skills/hok-state-reference-review/SKILL.md`. 이번에는 이 파일들을 호환판에 복사하거나 지침을 동기화하지 않았다.

## 4. 기능별 처리 대장 — 제안과 현재 상태

`수정 제안`은 미적용이며 구현 승인을 뜻하지 않는다. `미확인`은 정상·불필요 판정으로 대체하지 않는다.

| 기능·분기 | 현재 확인 | 처리 상태와 다음 판단 |
|---|---|---|
| 한국 15주 지도·기존 분할47출력 | 기존 분할 입력을 유지하며 신규 province·색·경계 변경이 없다 | **의도적 유지**. 새 원본 커밋을 이유로 지도 분할을 다시 구현하지 않음 |
| 새 CNDP13와 구형7 | 포트에는 새 표식·트리거·사업·전용 GFX가 없음 | **수정 제안**. 5절의 일관된 모듈로 이식, 신규 경로 `ADD`와 DDS `ASSET_COPY` 후보 |
| 시민사회 L-03~07 숫자·표식 표시 | 포트는 metadata·해당 새 문구 이전 상태 | **수정 제안**. 기존 civic 생성 계층에 표시 delta만 적용 |
| CNDP L-01~02 내부 조건 표시 | 새 사업 자체가 포트에 없음 | **수정 제안**. 새 사업 이식과 함께 최종 표시 수리를 적용 |
| L-08 동맹 산업지원 누적 | 원본 실제 화면에서 정상 비표시로 판정, 생산 명령 무수정 | **의도적 유지**. 새 번역·횟수 제한·wrapper를 만들 근거로 사용하지 않음 |
| 공개 시민 사건 `.1/.2/.11/.12` | 원본은 sync8곳을 같은 위치의 `hidden_effect`로 감쌈 | **수정 제안**. 선택지 접근과 공개 숫자 안내를 보존 |
| 회복 사건 `.3/.13` | 원본에도 공개 immediate의 sync가 남음. 긴 목록 위험은 `STRONGLY_SUPPORTED`, 실제 선택 차단은 `UNPROVEN` | **미확인**. 별도 UI 재현 후보이며 원본의 수리8곳에 포함하지 않음 |
| 해군·핵 연구망 현지화2개 | 포트에 경남 `$HOK_KOR_STATE_1086$`, 함남 `$HOK_KOR_STATE_1028$` 표시를 이미 적용 | **의도적 유지**. 새 이식 성과로 중복 집계하지 않고 한영 표현·실제 수혜주 확인 |
| 해주 해안요새 | 포트 `korea.txt:5637–5638`은 강원1144/province13540에 해안요새3 지급. `definition.csv:13541`은 coastal=false | **수정 제안**. 해주 province13559/황해남917로 대상만 교정. 실제 지급 실패·수선 성공은 이번 미검증 |
| 쓰시마·한국 연결·KCH·해방/외교 목록 | 원본의 지역 의도는 확인했으나 외국 ID는 RT56와 다름 | **미확인**. 6절의 기능·분기별 지리 대응을 확정한 뒤 선택 병합 |
| `comintern_starting_border`, `SOV_start_civil_war` | 전역 호스트 정의와 결합하는 신규 원본 파일 | **미확인**. 현 RT56 유효 정의와 엔진의 합성 규칙 확인 후 한국 국경 연결만 검토 |
| 중국·일본 일반 요새·우회 수선 | 원본 지도 기반의 일반 콘텐츠 변경이며 RT56 결함으로 입증하지 않음 | **미확인**. RT56 현재 대상이 맞으면 `USE_RT56`, 필요한 HOK 연결만 병합 |
| `mongppong_on_actions.txt` | 기존 통합 원장의 정책은 `USE_RT56`, 한국 전용 포트에서 MON 도전 모듈 제외 | **제외 유지 제안**. 원본 보급8개 수선을 이유로 몽골 모듈을 새로 활성화하지 않음 |
| 새 검토 문서·스킬 | 호환판에 새 파일·조건부 링크가 없음 | **문서 동기화 후보**. 7절의 차이를 반영한 별도 문서 작업으로 취급 |

## 5. CNDP13 이식 시 보존할 계약

### 5.1. 주·보상 대응

경기·제주는 추가하지 않는다. 아래는 원본 최종 배분을 기존 포트 ID로 대응한 **설계표**이며 실제 지급 관측이 아니다. 카테고리는 목표보다 낮을 때만 올리고 상위 등급을 낮추거나 차액을 추가 지급하지 않는다. 승점 열의 각 province에는 +1을 지급한다. 빈 칸은 해당 보상 없음이다.

| 지역·ID 접미사 | donor state → port state | 목표 카테고리 | 명시적 추가 슬롯 | 석탄 | 포트 승점 province | 부지 여력 검사 |
|---|---|---|---:|---:|---|---|
| 전북 `jeollabuk` | 1082 → 919 | large_town | 0 | 1 | 13550 | 없음 |
| 전남 `jeollanam` | 1088 → 1150 | — | 1 | 0 | 10110 | 없음 |
| 경북 `gyeongsangbuk` | 1030 → 920 | city | 0 | 0 | 7121 | 없음 |
| 경남 `gyeongsangnam` | 1086 → 1148 | — | 1 | 0 | 12060, 13556 | 없음 |
| 충남 `chungcheongnam` | 1031 → 1145 | large_town | 0 | 0 | 7204 | 없음 |
| 충북 `chungcheongbuk` | 1087 → 1149 | — | 1 | 0 | 13567 | 없음 |
| 황남 `hwanghaenam` | 1083 → 917 | large_town | 0 | 0 | — | 필요 |
| 황북 `hwanghaebuk` | 1091 → 1153 | — | 1 | 0 | 11915 | 없음 |
| 평남 `pyeongannam` | 527 → 527 | large_city | 0 | 1 | 9790 | 없음 |
| 평북 `pyeonganbuk` | 1089 → 1151 | — | 1 | 0 | — | 필요 |
| 함남 `hamgyeongnam` | 1028 → 918 | town | 0 | 0 | — | 필요 |
| 함북 `hamgyeongbuk` | 1090 → 1152 | — | 1 | 0 | 6944 | 없음 |
| 강원 `gangwon` | 1029 → 1144 | town | 1 | 3 | 1148 | 없음 |

**강원 동해의 province1148은 경남 state1148과 다른 ID 종류다.** 숫자가 같아도 state 치환을 적용하지 않는다. province 이전은 기존 명시적 `13414–13447 → 13535–13568` 대응만 사용하고, 각 승점의 실제 부모 주를 따로 대조한다. `HOK_KOR_STATE_<donor ID>` 표시 키의 숫자도 실제 state 번호로 일괄 변환하지 않는다.

남북12개는 각 **75PP·민공5 점유·90일**, 강원은 **150PP·민공5·180일**이다. 합계 **1,050PP·6,300민공일**, 초기 카테고리 증가분11·명시적 추가 슬롯7·석탄5·승점11, 직접 공장0을 보존한다. 독립 병행과 기술·반올림·상한 때문에 과거7개와 모든 시점의 밸런스가 같다는 뜻은 아니다. 시작 공장·인구·자원·주 경계는 새 사업 구현으로 변경하지 않는다.

### 5.2. 착수·취소·완료·상한

- 대상은 `tag = KOR`이며, 표시에는 체계 표식・`KOR_comprehensive_national_development_plan` 완료・해당 주 미완료를 요구한다. 개별 조건의 실제 배치와 공유 영토 트리거의 역할을 구분하여 보존한다.
- 건설III와 가용 민공 `>5`는 **착수 조건**이다. 진행 중 가용 민공이 줄었다는 이유만으로 취소 조건을 새로 추가하지 않는다.
- 체계 표식·비항복·해당 주 자국 소유·완전통제·미완료는 착수/취소/완료 직전에 같은 의미로 검사한다. 다른 쪽 도의 영토를 새 독립 사업에 요구하지 않는다.
- `fire_only_once = no`와 주별 영구 `HOK_KOR_cndp_developed_v1`로 완료1회와 취소 후 재착수를 구분한다. 취소 시 보상·PP환불 없이 민공 점유를 해제한다.
- 황남·평북·함남의 부지 전용3종은 확장 여력도 검사하고 진행 중 여력 상실 시 취소한다. 민공/군공 각각0~19의 잠금 포함·제외40쌍 비교는 **정확한 공유25 getter가 아니다**. 저점유20~24칸 주를 보수적으로 차단할 수 있는 원본 제한을 기록한다.
- 명시적 추가 슬롯7은 원래대로 가산하고 자원·승점 사업은 상한에서 부분 편익을 허용한다. RT56의 공유/종류별 상한·카테고리·modifiers를 구현 전에 대조하며 원본25/20을 맞추려고 호스트 상한을 바꾸지 않는다. 의미가 다르면 차이를 문서화하여 통합 판단을 먼저 한다.

### 5.3. 새 게임과 저장

`HOK_KOR_cndp_state_projects_v1`은 한국 country history의 **새 게임 초기화**에서만 부여한다. 표식이 있는 게임에는 신규 `HOK_KOR_cndp_develop_<region>`13개, 없는 저장에는 구형7개 ID·비용·기간·보상·완료 이력을 유지한다. 중점 `KOR_comprehensive_national_development_plan`은 이 분기에 맞춰 개별 결정13/7개의 해금 안내만 구분한다.

저장 로드 때 표식을 소급 부여하거나 옛 완료를 추정하여13개로 변환하지 않는다. 기존 타이머 재시작·차액 환불·소급 보상을 추가하지 않는다. 구형7개 보호 기준은 **분할 후 현재 포트의 블록**이며 과거9주 donor 파일을 복원하는 것이 아니다. 이 계약은 9→15주 지도 저장 마이그레이션과 별개다. 기존15주 포트 저장의 미착수/진행/완료 사례를 확인하기 전에는 이전 저장 호환을 주장하지 않는다.

### 5.4. 그림

원본13개는 새로 작성한 도형·지리 윤곽 기반 32×32, 각4,224바이트의 알파 포함 BGRA32 DDS와 전용 GFX다. 우선 제안은 선택 DDS를 바이트 보존하여 로컬 `gfx/interface/decisions/HOK_KOR/cndp/`에 복사하고 `GFX_HOK_KOR_decision_cndp_<region>` 연결을 유지하는 것이다. 실제 포트 소속·윤곽 의도가 같은지 확인하고 새 생성·색 변경·공유 RT56 sprite 교체를 기본 작업에 넣지 않는다. 기존 원작·지도 계통 출처와 새 도안의 kpopmodder 기여를 구분한다.

제작 원본·레시피는 원본 기록의 `C:\hoi\test\hok-korean-cndp-state-development-20261108-01\artwork\sources\`, 원본 PNG는 `artwork\renders\originals\`, 아이콘/소재 해시 원장은 원본 `docs/data/HOK_KOREAN_CNDP_ICON_MANIFEST.json`이다. 이는 donor의 별도 자료 위치이며 호환판 활성 source cache와 다르다. 이번에는 해당 외부 자료의 내용·해시를 재검증하거나 복사하지 않았다.

## 6. 지도 참조 수선의 병합 경계

원본 정렬 기록의 R/V/D 번호는 **원본 기능 식별자**로만 쓴다. 포트 적용·결함·통과 번호가 아니다.

| 원본 작업 | 포트에서 필요한 판단 |
|---|---|
| R-02 쓰시마 | donor1085 → port1147, province10011을 현재 상태·표시 키·기존 결정 비용과 대조. 이미 수선한 state 이름 키와 결정의 잘못된 영토 참조를 구분 |
| R-03 일본 보호령·낙일, R-04 중국 인정, R-05 KCH 수도 | donor13주·중국 추가15주를 숫자로 복사하지 않고 RT56 실제 지역·일본/중국 경로의 코어·이전 목록을 재구성. donor 난징1035는 RT56 Finnmark이므로 직접 이식 불가. 현재 포트 수도613의 적합성도 실제 난징 province11913 부모로 판정 |
| R-06 해주 항구 | donor13438 → port13559, state917. 현 포트13540은 coastal=false, 새 대상13559는 coastal=true이며 `history/states/917-Hwanghae.txt:6`에 소속. 해안요새3과 나머지6항구·중점 보호 필드는 유지 |
| R-07 일본 한반도 요새 | 평양·해주의 실제 부모와 소유/통제 검사를 구분. 현재 RT56 일본 트리의 동작을 기준으로 HOK 지리 연결만 병합 |
| R-08 몽골 보급 | 기존 MON 모듈 제외 유지가 기본 제안. 다른 공유 코드에서 같은 수선이 필요한지는 별도 후보로 조사 |
| R-09A~F 해방, R-10 인도차이나 외교, H-01 해협식민지 | visible/available·controller·일반/내전·종속국·수락 사건의 대상 집합을 같은 의도 지역으로 대응. transfer와 core는 별도 효과로 검토. RT56 분할·태그·영토 보존과 기존 포트 지역 ADR을 우선 |
| V-01 중국 요새, V-02 태평양 섬 요새, V-03 인도차이나 우회 | 현 RT56 파일의 올바른 대상이면 유지. 원본 일반 수선을 포트 결함으로 단정하지 않고 실제 HOK 영향과 고정 보상·명령 순서 검토 후 결정 |
| D-01~04 지역 설명·주 이름 | 연구망 한영2개와 기존12개 논리 지명은 포트에 이미 적응됨. 교육·투자 설명은 실제 수혜주·양쪽 영토 조건과 영어 문구를 대조하여 필요한 값만 갱신 |
| 코민테른 접경·소련 내전 정리 | donor 함북1090은 포트1152. RT561090은 다른 외국 주이므로 그대로 사용 불가. 전역 상수와 `SOV_start_civil_war`의 현재 유효 정의·누적/대체 규칙·호출부를 확인하고 한국 국경 관련 차이만 선택 |

외국 지역은 현재 국가의 core만으로 무제한 확장하지 않는다. 지리 이름·province 부모·기존 HOK 의도·RT56 현재 목록을 함께 근거로 삼는다. 영토 범위를 넓히면 이전받는 기존 산업·인력도 달라질 수 있으므로 고정 보상이 같다는 이유로 밸런스 동일을 주장하지 않는다. 지도·시작 산업 수정을 참조 정렬에 포함하지 않는다.

## 7. 표시·검토 지침의 포트 적응

원본 표시 수리는 고유 키 L-01~07의7개, 시민 숫자 metadata29곳, 현지화15키, sync wrapper8곳을 각각 다른 단위로 기록한다. L-03~06은 원문 ID 노출이 아니라 자동 숫자 조건·효과가 누락되던 현상이며, L-07과 CNDP 내부 표식 노출과 구분한다. L-08은 정상 비표시이므로 무수정이다.

포트 영어 채널은 사람이 읽는 본문·주석을 **영어**로 작성하는 기존 계약을 유지한다. 원본의 `_l_english`에도 한국어를 유지하고 일반판 영문 번역으로 덮는 정책은 가져오지 않는다. 영어·한국어 paired 키·토큰·BOM·숫자 부호·색상·NOT/OR 의미와 실제 활성 번역의 동명 파일 덮어쓰기를 함께 확인한다. 원본의 공통 안내 최종 축약은 의미를 영어로 옮기며 이전 스크린샷을 새 문구의 UI 증거로 사용하지 않는다.

새 검토 스킬은 영향 기능·ID·공유 호출자·대체 분기·활성 번역·상속 코드를 대장으로 추적하는 절차를 참고할 수 있다. 후속 지침 동기화 시 donor 전용 경로와 지도 정책을 ADR-0006·포트 대응표·RT56 우선 규칙으로 바꾸고, 원본 현지화 스킬57행의 언어 계약을 그대로 복사하지 않는다. 로그를 실제로 검토할 때만 관련 원본 로그 스킬을 추가로 읽는다. 이번 문서는 스킬 설치나 `AGENTS.md` 변경이 아니다.

## 8. 생성 소유권과 제안 작업 순서

기존 한국 builder의 civic→영문→후속 feature/prospecting→분할 최종 계층, [분할 콘텐츠 모듈](../../tools/korean_state_split_content.py), [공유 모듈](../../tools/korean_state_split_shared.py), [동아시아 builder](../../tools/build_east_asia_overrides.py)의 소유권을 보존한다. 새 내용을 최종 생성 파일에 손으로 덧붙이면 재생성과 잠금이 불일치한다. 이전 입력 핀을 새 원본 해시로 조용히 바꾸거나 실패하는 비교를 완화하지 않는다.

아래는 **향후 구현이 승인된 경우**의 순서다.

1. 현재 branch/HEAD/기존 변경과 실제 HOI4·RT56·언어 구성을 재확인한다. 36후보의 커밋/checkout 해시·기존 출력·host/schema 대응을 기록하고 검토한 새 입력만 별도 동결한다. 옛 cache·lock·보관본은 보존한다.
2. 기존47출력의 재현·보호 범위를 먼저 정하고 신규 delta의 생성 소유자를 명시한다. 별도 새 잠금/선택 병합 계층을 설계하며 기존 잠금과 소스 핀 변경을 구분한다. 원장 분류·해시 갱신은 이때 실제 출력에 맞춰 수행한다.
3. 해주 등 입증된 한국 참조 수선을 별도 최소 단위로 구현한다. CNDP 신설·표시 수리·한국 밖 호스트 판단과 서로 다른 diff/기록으로 남긴다.
4. CNDP13을 country history·기존/신규 결정·트리거·중점 해금·한영 현지화·DDS/GFX까지 한 모듈로 통합한다. 기존7개와474개 중점 보호 필드·15주 지도를 보존한다.
5. 시민사회 metadata·공개 사건8곳 표시 수리를 적용하고 `.3/.13`은 재현 결과로 별도 판단한다. 변수·조건·효과·호출 순서는 유지한다.
6. 한국 외 지역/공용 시스템은 기능별 RT56 병합 결정을 확정한다. `USE_RT56`·의도적 유지·제외와 실제 수정 대상을 모두 남기며 전체 donor 파일 교체로 마감하지 않는다.
7. 변경에 맞는 정적 확인·aggregate·실제 동작/표시·저장 검증을 수행하고 결과를 별도 구현 기록에 남긴다. 필수 미확인 항목이 남으면 구현/검증 상태를 제한하여 보고한다. 커밋·게시 여부는 별도 요청을 따른다.

## 9. 후속 검증 계약 — 전부 미실행 계획

| 층·기능 | 필요한 확인과 중요한 경계 |
|---|---|
| 소스·재현 | 36후보 처리 대장, 신규13개 ID·13개 sprite·13개 DDS 연결, 구형7개 보호, 전체13주 목표/보상 부모, 중점474개 보호 필드, BOM·영어/한국어·scope·전역 ID 충돌과 generator 재현. 실제 원장 분류/파일 수는 구현 후 확정 |
| RT56 보존 | 현재 host 물리 파일/manifest 재지문, 중국·일본 비한국 내용과 소련 공유 효과·접경 목록 보존. 기존 aggregate11개 ERROR를 새 회귀와 구분하고 조용히 면제/삭제하지 않음 |
| 실제 구성 | R0 RT56-only, C0 영어 호환판, 필요한 R1/C1 한국어 구성을 분리해 cold launch. donor·원본 일반판 번역이 포트 구성에 없는지 확인. effective precedence·DLC·체크섬을 관측 |
| CNDP UI·착수 | 신규13개와 구형7개 분리·개별 해금·강조·아이콘, 가용 민공5/6, PP74/75·강원149/150, 건설III·주 소유/완전통제·항복·완료 경계. 일반 UI 착수와 강제 활성화는 별도 결과 |
| CNDP 기간·편익 | 실제90/180일·정치력·점유/반환·독립 병행·단일 완료, 카테고리 상승/상위 유지·명시적 슬롯7·석탄5·승점11을 실제 주/저장에서 확인. 숫자 원장과 엔진 관측을 구분 |
| CNDP 차단·취소 | 한쪽 도만 보유, 전쟁 중 한 province 통제 상실·소유 상실·항복, 부지 전용3종의 진행 중 여력 상실, 취소 무환불·재착수·재완료 차단. 공유/유형 상한과 저점유20~24칸 보수 차단을 별도 관측 |
| 시민사회 표시·효과 | 양 언어의 수치·현재값·부호·색·OR/NOT, 공개 `.1/.2/.3/.11/.12/.13` 선택지 접근과 sync 목록. 실제 선택 효과·기존 국민정신·비용·변수/표식 수명을 별도 비교 |
| 참조 정렬 | 해주 실제 해안요새3·나머지6항구, 한국/외국 소유·부분 통제, 종속국·내전·수락/거절·fallback별 영토와 core, SOV 경계분쟁 양 방향 정리. 적용하기로 정한 기능만 검증하며 제외 이유도 남김 |
| 저장 | 새 저장 cold reload와 대표 기존15주 포트 저장의 미착수/진행/완료 경로를 분리. flag 값·날짜·활성 타이머·365일 직렬화와 실제 기간 경과를 구분. 9주 저장 자동이전은 이번 제안에 없음 |
| 한계·복구 | RT56의 이전1939 미지원 관측은 현재 host 재확인 전 유지. 다른 DLC·장기 AI·외부 호환 모드·멀티플레이는 주장 범위에 맞춰 별도 평가. 시험 후 소유 프로세스 종료·원래 설정/모드·기존 저장 보존·Steam 상태를 확인 |

반복 소스 검사 항목 수, 고유 기능 수, 실제 실행·화면 수를 더하지 않는다. 단일 대표 사례를 묶을 때 구조상 동등성 근거와 미실행 대상을 기록한다. 새로운 필수 항목의 미검증을 이전 suite의 PASS로 대체하지 않는다.

## 10. 역사적 증거와 자료 위치

| 자료 | 기록의 역할과 재사용 한계 |
|---|---|
| 포트 분할 구현 기록 | 이전47출력의 aggregate19 PASS/0 WARNING/기존11 ERROR, suite190 PASS/0 MISMATCH/10 UNVERIFIED. 이번 CNDP/표시/추가 참조의 검증이 아님 |
| donor CNDP 구현 기록 | 실제 생산 정의13개 강제 활성화 뒤90/180일 만료·성공 표식·비용/점유/반환, 전시 부분 통제 상실 취소·복구 재착수 관측. 일반 UI 전체13개 착수·raw슬롯/VP 직접 관측·재착수 완료·기존 저장 전체 검증으로 확대하지 않음 |
| donor 표시 구현 기록 | L-01~07 수리와 일부 양 언어 화면. 저장 비교 부재쌍55/0·양성 패치쌍55/1·선택A 후25/1의 원래 결과를 보존. 재로드 생산선 speed 차이는 원형 통제에서도 동일했지만 정확한 엔진 원인과 선택 후 추가 차이 귀속은 미확정 |
| donor 최종 공통 안내 | 표시 수리 화면 확인 후 문구를 축약함. 축약 후 새 화면 확인은 기록되지 않았으며 이전 화면을 최종 문구의 증거로 쓰지 않음 |
| 이전 포트 동결 입력 | `docs/upstream/hok-state-split-20261107/`와 분할 잠금은 관리용 source 사본/해시. 시험 산출물이나 새 runtime load 경로가 아님 |
| 기존 포트 시험 증거 | `C:\hoi\test\hok-rt56-state-split-20261107-01\`. 이전 helper·backup·fixture·로그·저장 사본이며 이번에 재실행·이동하지 않음 |
| donor 후속 증거 | `C:\hoi\test\hok-korean-cndp-state-development-20261108-01\`, `hok-state-reference-alignment-20261108-01\`, `hok-localisation-display-20261108-01\`, `hok-cndp-common-copy-20261108-01\`와 별도 영문 번역 증거 경로는 각 원본 문서가 관리. 이번에 외부 증거 전체를 재검증하지 않음 |
| 호환판 활성 source cache | `C:\hoi\test\hok-rt56-source-cache\sources\`의 감사된 세 입력. 일반 정리 대상이나 새 출력 경로가 아님. 과거 archive 대응은 개발 자료 안내를 따름 |
| 후속 새 시험 위치 제안 | `C:\hoi\test\hok-rt56-upstream-20261108-01\`. **이번에는 만들지 않았으며**, 실제 실행 시 충돌 없는 새 run-id를 확정하고 helper의 출력·로그·backup·fixture를 모두 그 아래로 구성 |

정리 대기 자료는 호환판 `tools/__pycache__/` **21파일·1,088,888바이트**, 원본 `docs/assets/korean-fascist-mobilization-validation-20260923/`의 시험 PNG **4파일·815,391바이트**다. 호환판 `.local-artifacts`는 이번 읽기 확인에서 없다. 새 시험 파일을 저장소에 만들지 않았으며 위 기존 자료도 이동·삭제하지 않았다.

## 11. 이번 문서화의 완료 범위

이번 실제 작업은 Git 이력·작업 트리·선택 파일 해시·설치 메타데이터·관련 소스/문서의 읽기 비교, 이 계획 작성과 [문서 인덱스](../README.md) 연결이다. 새 계획의 상대 링크21곳은 대상 부재0이고, UTF-8 재독에서 대체 문자0을 확인했다. 독립 읽기 검토에서 지적한 한국/일본/중국 파일별 변경 귀속을 바로잡고 CNDP 대상・표시 조건을 보완했다. 읽기 소스 재고·문서 링크·문서 diff 확인을 게임 정적 검사 통과로 부르지 않는다. 새 source snapshot·잠금·도구·진단 파일은 만들지 않았고 게임 코드·이미지·캐시·설정·기존 시험 자료는 그대로 유지했다. 검사기·게임 실행과 커밋·푸시·게시·업로드는 수행하지 않았다.
