# 한국 재벌·시민사회 이식 좌표 명세

작성: 2026-10-12 (Asia/Seoul). 상태: **STATIC_SPEC_RUNTIME_UNPROVEN**. 호환판의 직전 460개 소스와 현재 결정적 생성 출력에서 배치·상대 연쇄·진행 선행을 읽어 기록한 유지 관리 명세다. donor의 화면·저장·정상 진행 관측은 호환판 실행 결과로 옮기지 않는다.

## 소스와 수치 입력

| 항목 | 기준 |
|---|---|
| 호환판 직전 소스 | `feat/korean-focus-update-20260922@71fb843c0b4f6b3521062ffa07d23d5963a0514d`의 실제 작업 트리 |
| 직전 checkout SHA-256 | `332DE63A191236AE44C0F5BB87706095002D69C08B5A770DD503D0293323894A` |
| 직전 Git object SHA-256 | `45A09C59FA8BFC609082A3561E6B9B2240574821AEDEDEA8976DEFCA9EC1D8C5` |
| 선택 donor commit | `d4031aaa0c1f85bb89b0e6ca21d041beade8bd26` |
| donor 한국 트리 checkout SHA-256 | `36E90BFDBEFC1980DAD83131745ED00BC4A7A3E33BE11F8504C7234CADBC420A` |
| 호환판 생성 출력 SHA-256 | `7AE9465EE5DA4E3FC59CCAADC36E1F492BC81AEFA715D11992229D383F7AE9D8` |
| 생산 소스 | `common/national_focus/korea.txt` |
| 별도 역사적 ID 등록 | `common/national_focus/HOK_KOR_civic_legacy_focus.txt` |

[기계 명세](data/HOK_KOREAN_CIVIC_LAYOUT_COORDINATES.json)의 `before`는 업데이트 직전 호환판 checkout이고 `after`는 `tools/build_korean_focus_update.py`의 `build_all()`이 메모리에 반환한 최종 출력이다. 직전 Git object와 checkout은 줄바꿈으로 해시가 다르므로 두 값을 구분한다. donor 좌표 문서는 설계 참고이며 수치 입력으로 복사하지 않았다. 문서 작성 뒤 생산 한국 트리와 별도 구 ID 등록 파일의 실제 바이트가 위 생성 입력·해시와 일치함을 확인했다. 이 일치는 엔진이 그 파일을 실제로 로드했다는 증거가 아니다.

[왕정 H1 좌표 명세](HOK_KOREAN_ROYAL_LAYOUT_COORDINATES.md)와 그 JSON은 당시 460개 이력을 그대로 유지한다. 현재 472개 전체의 선언 순서와 상대 연쇄는 이번 JSON에서 제공한다. RT56 지도·주 ID 병합, 기존 왕정 H1 수정과 다른 이전 이식 내용은 최종 생성 소스에 유지된다.

## 트리 수량과 기존 위치 변화

| 소스 해석 항목 | 직전 / 현재 |
|---|---|
| 플레이 가능한 한국 중점 정의 | `460 - 1 + 13 = 472` |
| 절대 기준 / 상대 중점 | `7 / 453` → `7 / 465` |
| 직접 offset 블록 / 소유 중점 | `7 / 5` 유지 |
| 전체 기본 범위 | `x0~211/y0~24` 유지 |
| 살아남은 기존 중점의 기본 위치 | 상선·영국함 2개 이동, 나머지 457개 보존 |
| 살아남은 기존 중점의 상대 선언 순서 | 459개 모두 유지; 제거한 구 노드 뒤의 수치 인덱스는 한 칸 당겨짐 |
| 새 내정 13개 선언 인덱스 | 0부터 세는 `459~471` |
| 지속적 중점 패널 | UI `(200,1700)` 유지 |
| 바로가기 | 8개 목적지와 배율 `0.65` 유지 |

| 기존 ID | 소스 상대값 변화 | 기본 절대 변화 | 민주 진입 완료 HIDE |
|---|---|---|---|
| `KOR_expand_merchant_marine` | `(-2,2)` → `(0,2)` | `(138,11)` → `(140,11)` | `(105,11)` |
| `KOR_british_naval_ship` | `(0,2)` → `(0,2)` | `(138,13)` → `(140,13)` | `(105,13)` |

상선 추가 징발 `KOR_expand_merchant_marine`의 기준은 `KOR_join_the_allie`이고 상대 x만 `-2→0`이다. 영국 구축함 구매 `KOR_british_naval_ship`의 기준은 상선 추가 징발이며 상대 `(0,2)`를 유지해 부모 이동을 상속한다. 새 내정 가지와의 간격을 위한 donor 배치 변경이며 두 기존 중점의 보상·기간·진행 선행을 바꾸지 않는다.

## 새 민주 내정 가지와 실제 진입

구 `KOR_cooperation_with_the_jaebeol` 노드의 자리와 민주 선행을 **산업·사회협약**이 이어받는다. `relative_position_id = KOR_democracy_advance_forward`, 상대 `(6,4)`, 기본 `(133,6)`이다. 실제 선행은 하나의 `prerequisite` 블록에 있는 `KOR_liberal_party_sole_power` **OR** `KOR_independent_party_in_power`다. 두 단독집권을 동시에 요구하거나 공통 산업화 중점을 추가로 요구하지 않는다. 위치 기준과 진행 선행은 별도 필드다.

새 게임의 정상 진입은 민주주의 → 자유당 또는 독립당 단독집권 → 산업·사회협약 → 세 산업정책 중 하나다. 협약은 명목 35일이며 150PP와 세력 관리 범주를 해금한다. 협약 완료 자체를 기업 협력 정책 완료로 취급하지 않는다. 재벌 산업협력을 완료해야 기존 삼성·현대·선경 주문의 새 정책 경로를 열고 협력 상태의 일회성 조정을 적용한다. 기존 길들이기, 구 협력 완료와 등록 이력의 주문 경로도 유지한다.

세 정책은 상호 배타적이다. 기업 연구·설비 후속은 재벌 산업협력에, 시민 인력·인사·정착 후속은 시민 개혁에, 공공 계약 후속은 공공 소유에 연결된다. 시민 개혁의 정착은 국민개병제와 공적 책임 중점의 별도 singleton 선행 그룹 두 개를 유지하므로 둘 다 요구한다. 조달 검수체계는 세 정책을 한 선행 블록에 두어 어느 하나 완료로 접근한다. 후속의 정책 flag·내전·항복·취소 조건은 생산 소스의 조건이며 이 좌표 계산이 실제 진행을 증명하지 않는다.

| 선언 인덱스 | 이름 / ID | 상대 기준 | 소스 상대값 | 기본 · SHOW · 초기 HIDE | 민주 진입 완료 HIDE |
|---|---|---|---|---|---|
| 459 | 산업·사회협약 / `HOK_KOR_civic_industrial_compact` | `KOR_democracy_advance_forward` | `(6,4)` | `(133,6)` | `(98,6)` |
| 460 | 재벌과의 산업협력 / `HOK_KOR_civic_chaebol_cooperation` | `HOK_KOR_civic_industrial_compact` | `(0,1)` | `(133,7)` | `(98,7)` |
| 461 | 재벌의 공공 소유 전환 / `HOK_KOR_civic_nationalization` | `HOK_KOR_civic_industrial_compact` | `(2,1)` | `(135,7)` | `(100,7)` |
| 462 | 독점 해체와 시민 개혁 / `HOK_KOR_civic_break_monopolies` | `HOK_KOR_civic_industrial_compact` | `(4,1)` | `(137,7)` | `(102,7)` |
| 463 | 선경 원료·설비 투자 / `HOK_KOR_civic_sunkyong_investment` | `HOK_KOR_civic_chaebol_cooperation` | `(-1,1)` | `(132,8)` | `(97,8)` |
| 464 | 삼성전자 기술투자 / `HOK_KOR_civic_samsung_electronics` | `HOK_KOR_civic_chaebol_cooperation` | `(1,1)` | `(134,8)` | `(99,8)` |
| 465 | 금성 대량생산 설비 / `HOK_KOR_civic_goldstar_mass_production` | `HOK_KOR_civic_chaebol_cooperation` | `(0,2)` | `(133,9)` | `(98,9)` |
| 466 | 노동·생산 협약 / `HOK_KOR_civic_labor_compact` | `HOK_KOR_civic_break_monopolies` | `(0,2)` | `(137,9)` | `(102,9)` |
| 467 | 국민개병제 정비 / `HOK_KOR_civic_mass_conscription` | `HOK_KOR_civic_labor_compact` | `(-1,1)` | `(136,10)` | `(101,10)` |
| 468 | 공적 책임과 공정 인사 / `HOK_KOR_civic_public_accountability` | `HOK_KOR_civic_labor_compact` | `(1,1)` | `(138,10)` | `(103,10)` |
| 469 | 시민 개혁의 정착 / `HOK_KOR_civic_social_settlement` | `HOK_KOR_civic_labor_compact` | `(0,3)` | `(137,12)` | `(102,12)` |
| 470 | 공공 계약과 기술 승계 / `HOK_KOR_civic_public_procurement` | `HOK_KOR_civic_nationalization` | `(0,2)` | `(135,9)` | `(100,9)` |
| 471 | 조달 검수체계 / `HOK_KOR_civic_procurement_inspections` | `HOK_KOR_civic_industrial_compact` | `(6,2)` | `(139,8)` | `(104,8)` |

새 13개 기본 범위는 `x132~139/y6~12`, 민주 완료 HIDE 계산 범위는 `x97~104/y6~12`다. 모든 새 중점은 기존 민주 기준으로 끝나는 전체 `anchor_chain`을 JSON에 기록한다. 민주 offset 소유자는 각 연쇄에서 한 번이며 자식에게 직접 offset을 추가하지 않는다. 시민 정착의 배치 기준은 노동·생산협약이며 진행 선행 둘과 구분한다.

## 구 협력 ID와 저장 이력

직전 선언 인덱스 122의 플레이 가능한 `KOR_cooperation_with_the_jaebeol`은 한국 트리에서 제거한다. 별도 `shared_focus` 정의는 같은 ID를 전역 등록하되 트리에 import하지 않고 `available = { always = no }`, AI factor 0, 빈 완료 보상을 사용한다. 이 ID는 현재 472개 플레이 가능한 정의 수에 포함하지 않는다.

구 ID 등록은 저장된 `has_completed_focus` 조회의 연결을 유지하려는 소스 계약이다. 구 이력을 새 협약·정책 완료로 강제 전환하거나 협약의 150PP를 재지급하지 않는다. 초기·월간 등록과 회사 주문에서 구 ID를 읽는 연결이 함께 이식되지만 호환판의 기존 저장 로드·월간 비중복·재저장 검증은 아직 **UNPROVEN**이다. donor의 제한된 구 저장 사례를 일반 포트 저장 호환으로 확대하지 않는다.

## SHOW/HIDE와 고정 영향력 패널

중점 x/y는 격자 단위다. `기본 위치 = 부모의 해석된 기본 위치 + 소스 상대값`이며 조건부 위치는 자기·조상에서 만나는 활성 offset만 더한다. JSON의 472개 노드는 자기 ID부터 절대 기준까지의 전체 연쇄, 전후 선언 인덱스, 선행·배타 그룹, 직접·상속 offset ID를 기록한다. 7개 offset 원문도 별도 보존한다.

조건부 모델은 SHOW와 HIDE 각각의 초기 및 공산·민주·파시·왕정 진입 완료, 총 10개다. 각 완료 모델은 해당 진입 중점만 참이고 나머지 세 경로 진입 완료는 거짓이다. 현재 SHOW의 모든 모델은 offset이 비활성이고 초기 HIDE도 기본 위치다. 민주 완료 HIDE는 공통 공화국 기준의 `-35x`와 별도 민주 기준의 `-35x` 조건을 활성화한다. 새 내정 가지는 민주 기준에 직접 연결되므로 민주 이동을 한 번만 받는다. JSON 항목의 `committed_hide`는 이 **민주 진입 완료 HIDE** 조건을 뜻하며 정책 완료나 Git commit 상태를 뜻하지 않는다.

다른 세 완료 HIDE는 기존 offset 원문의 조건을 그대로 계산한다. `all_defined_node_bounds`는 숨겨질 수 있는 정의까지 포함한 수치 범위이며 실제 표시 가지의 범위나 엔진 스크롤 한계가 아니다. `allow_branch`의 실제 숨김·갱신 시점과 전환 중 표시를 이 모델에서 실행하지 않았다.

영향력 inlay는 UI `(1050,1400)`, 크기 `500×670`이다. `HOK_KOR_civic_influence_inlay_window` → `HOK_KOR_civic_influence_window` 연결을 사용한다. 이는 중점 격자와 별도 고정 UI 설정이므로 민주 군집의 `-35x` 이동을 상속하지 않는다. KOR의 내정 초기화 flag가 표시를 제어하고 협약의 `HOK_KOR_civic_panel_unlocked` flag가 버튼·관리 범주 해금을 제어한다. 패널 표시와 관리 가능 상태를 구분한다.

현재 vanilla `interface/nationalfocusview.gui`의 `focus_tree_scripted_window_container`와 focus spacing `(96,130)`, 설치본의 focus-inlay 예제를 확인했다. RT56에 같은 `nationalfocusview.gui` 경로의 override는 발견하지 않았다. 이는 등록·배치에 사용할 소스 counterpart이며 포트에서 실제 패널이 표시되고 눌린다는 증거가 아니다. 합성고무 이름판·산업 하단·만주 내정 줄·지속적 중점 패널과의 외곽·이름판·연결선·클릭 영역은 실제 RT56 UI에서 확인한다.

## 정적 근거와 남은 실행 검증

순서 있는 소스 해석에서 현재 고유 ID 472개, 절대 기준 7개, 앞선 선언을 가리키는 상대 노드 465개를 계산했다. 연쇄 누락·순환·후행 기준 참조 없이 좌표를 계산했고, 살아남은 기존 노드의 순서·7개 offset 원문·지속적 중점 패널·8개 바로가기를 직전 소스와 대조했다. 이 수치는 문서의 소스 재구성 근거이며 파서·엔진·화면 검증 횟수가 아니다. 별도 게임 실행이나 gameplay validator는 이 문서 작성에서 수행하지 않았다.

포트에서 전체 재시작한 새 게임의 초기 SHOW/HIDE, 민주 선택 전후와 단독집권 이후, 세 정책 선택과 배타 가지 표시를 확인해야 한다. 13개 아이콘·한국어 제목판·선행 합류·배타선·상선·영국함 연결, 패널 전 영역·단추·하단 문구·지속적 중점과의 접근을 실제 해상도·GUI 배율·확대 단계·스크롤과 함께 기록한다. 중심 좌표가 다르다는 사실만으로 무겹침을 판정하지 않는다.

자유당·독립당 정상 OR 진입, 두 선행을 요구하는 시민 정착의 한쪽만 완료한 차단과 양쪽 완료 착수, 후속 정책 gate·취소, 기존 주문·월간 상태·구 ID 저장, AI·DLC·영문/한글 언어 의존성·멀티플레이는 실제 수행한 범위만 판정한다. 강제 효과 진단은 정상 진행과 별도다. 현재 호환판 UI·진행·저장 결과는 **UNPROVEN**이며 donor 명세의 결과를 포트 통과로 가져오지 않는다.

설계 참고: [donor 현행 내정 명세](../../hearts_of_korea/docs/HOK_KOREAN_CHAEBOL_CIVIL_SOCIETY_SPEC.md), [donor 주문·진입·배치 개정](../../hearts_of_korea/docs/HOK_KOREAN_CHAEBOL_CIVIL_SOCIETY_REVISION_PLAN.md), [donor 좌표 이력](../../hearts_of_korea/docs/HOK_KOREAN_FOCUS_LAYOUT_COORDINATES.md). 각 문서의 과거 473개·고정 산업 진입·y1300 기록은 이력이며 현재 포트의 472개·민주 진입·y1400 입력과 구분한다.
