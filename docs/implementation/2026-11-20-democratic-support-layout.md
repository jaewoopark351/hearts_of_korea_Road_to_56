# 2026-11-20 민주인사 지원·정보국의 호환판 배치

상태: **현재 포트 소스 좌표 명세·제한된 정적 모델 확인 / 후속 영어·한국어 초기 UI 일부 관측 / 전체 조건별 실제 배치 미확인**. 이번 전체 이식에서 옮긴 네 지원/후속 중점, 기존 초대 두 중점과 신규 정보국의 배치를 기록한다. 원본의 과거 독립당 배치 화면·1.19 실행·이전 단계 검증 수를 현재 호환판의 결과로 사용하지 않는다. 이후 별도 승인된 실제 실행의 전체 상태는 [전체 이식 기록](2026-11-20-korean-democratic-support-intelligence-port.md)을 따른다.

## 읽을 조건과 입력

해당 중점의 좌표·기준·선행·SHOW/HIDE·직접 offset 또는 새 정보국 배치를 변경하기 전에 이 문서와 [현재 기계 명세](../data/HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_PORT_LAYOUT.json), 프로젝트 배치 규칙, [전체 이식 계획](../plans/2026-11-19-korean-democratic-support-intelligence-port-plan.md)을 읽는다. 기존 11월 1일 압축은 [이전 포트 기록](2026-11-01-korean-democratic-layout-port.md)과 [그 좌표 JSON](../data/HOK_KOREAN_DEMOCRATIC_LAYOUT_COORDINATES.json)에 역사적 입력으로 유지한다. 이를 새 475개 트리 전체의 현행 스냅샷이라고 부르지 않는다.

원본의 [배치 계획](../../../hearts_of_korea/docs/HOK_KOREAN_FOCUS_LAYOUT_PLAN.md), [좌표 기록](../../../hearts_of_korea/docs/HOK_KOREAN_FOCUS_LAYOUT_COORDINATES.md), [압축 사건](../../../hearts_of_korea/docs/incidents/2026-09-21-korean-focus-compact.md), [정치 압축 계획](../../../hearts_of_korea/docs/HOK_KOREAN_POLITICAL_COMPACTION_PLAN.md)과 [적용 사건](../../../hearts_of_korea/docs/incidents/2026-09-22-korean-political-compaction.md)을 먼저 읽고, 최신 [부분 delta 보관본](../upstream/hok-democratic-support-20261120/documents/docs/data/HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_LAYOUT.json)과 실제 포트 소스를 함께 해석했다. 원본 문서의 이전 326/362/474개 좌표, 옛 독립당 정보국 `(120,6)`와 현재 재무장 정보국 `(62,1)`은 서로 다른 단계다.

| 실제 입력 | 위치·SHA-256과 역할 |
|---|---|
| 직전 호환판 | `docs/upstream/hok-democratic-support-20261120/compat_before/common/national_focus/korea.txt`, `EF979199A8A71E28A30ABFEDC5632012095B54D474C886626E778C91E9A19066`. 이번 계층의 동결 이전 checkout이다. |
| 현재 생산 소스 | `common/national_focus/korea.txt`, `265D1E087E00ACEDAA12A4A4BBD3B573DB6919DA08196504874D0B49F3C53F48`. 기존 포트 위에 선택 delta를 합성한 실제 출력이다. |
| 생성 소유자 | `tools/upstream_democratic_support.py`와 `tools/hok_democratic_support_lock.json`. 배치 출력을 손으로 수정하지 않는다. |
| 이전 배치 유지 자료 | `docs/data/HOK_KOREAN_DEMOCRATIC_LAYOUT_COORDINATES.json`. 11월 1일 소스의 기록이며 이번 명세와 분리한다. |
| 현재 부분 명세 | `docs/data/HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_PORT_LAYOUT.json`. 영향 7개와 현재 기준 연쇄·부모/자식·같은 부모의 형제·주변 노드·18개 상태의 위치 및 전체 범위를 기록한다. 전체 트리 스냅샷은 아니다. |
| 외부 helper·확인 | `C:\hoi\test\hok-rt56-democratic-architecture-20261120-01\geography\qa\layout_source.py`, `build_layout_spec.py`, `layout-source-checks.json`. 소스 해석·중간 결과는 이 외부 위치에 두며 저장소에는 유지 명세만 둔다. |

기준 포트 커밋은 `9a01955785bcdd827c9c85522537a0bfc57ed654`, 원본 HEAD는 `f180bc8089e2a17f310b1fafa091d3f152063df3`, 콘텐츠 커밋은 `f2356e2a2c6db9048e18a4dde41454865f10742a`다. 현재 설치 metadata는1.20이고 지원 선언은1.19.*이다. 이번 계산은 엔진 실행·로드 체크섬·지원 버전 판정이 아니다.

## 현재 좌표·진행 관계

좌표는 focus grid 단위다. `relative_position_id`의 **해석된 기본 위치**에 소스 상대값을 더하며, 기준의 소스 상대값을 절대좌표로 오해하지 않는다. 진행 선행은 위치 기준과 따로 기록한다. 아래 일곱 중점은 각각 표의 기준 중점을 실제 진행 선행으로도 쓰지만 그 사실을 다른 중점의 일반 규칙으로 확대하지 않는다.

| 중점 | 현재 상대 기준 | 소스 상대값 | 직전 기본 위치 → 현재 기본 위치 | HIDE 민주 완료 위치 |
|---|---|---|---|---|
| 중국 초대 `KOR_invite_china` | 아시아 연합 수립 `(119,15)` | `(-2,2)` | `(117,17) → (117,17)` | `(82,17)` |
| 중국 민주인사 지원 `KOR_support_for_democracy_in_china` | 아시아 민주주의 선봉 `(116,6)` | `(-6,1)` | `(113,17) → (110,7)` | `(75,7)` |
| 중국 독재자 축출 `KOR_overthrow_the_chinese_dictators` | 중국 민주인사 지원 `(110,7)` | `(0,2)` | `(113,19) → (110,9)` | `(75,9)` |
| 일본 초대 `KOR_invite_japan` | 아시아 연합 수립 `(119,15)` | `(2,2)` | `(121,17) → (121,17)` | `(86,17)` |
| 일본 민주인사 지원 `KOR_support_for_democracy_in_japan` | 아시아 민주주의 선봉 `(116,6)` | `(-3,1)` | `(123,17) → (113,7)` | `(78,7)` |
| 민슈 잇키 `KOR_minshu_ikki` | 일본 민주인사 지원 `(113,7)` | `(0,2)` | `(123,19) → (113,9)` | `(78,9)` |
| 비밀 정보국 확장 `HOK_KOR_expand_secret_intelligence_service` | 재무장 시작 `(54,0)` | `(8,1)` | 신규 → `(62,1)` | `(62,1)` |

지원 중점의 진행을 선봉으로 앞당긴 원본의 변경과 초대/지원 배타 제거를 그대로 선택 이식한 결과다. 초대 두 개의 위치는 움직이지 않는다. 중국 축출은 코드의70일 변경이 포함된 별도 기능 delta이며 배치 문서가 보상·비용·가용성을 추가 변경하지 않는다.

정보국은 공통 군사 절대 기준의 자손이다. 정치 노선의 offset이 이 연쇄에 없고 자체 offset도 없으므로 모든 계산 상태에서 `(62,1)`이다. `allow_branch`는 La Resistance만 요구한다. 이전 독립당 단독집권 선행이나 민주 HIDE guard를 되살리지 않았다. 같은 재무장 부모를 쓰는 해군 `(55,1)`·공군 `(69,1)`과 정보국은 독립된 자식이다. 주변 수리 `(61,2)`, 군도 훈련 `(60,3)`, 호송 학교 `(62,3)`, 공군기지 확장 `(65,2)`도 현재 위치로 명세에 포함했다.

민주 구역의95개 상대 연쇄는 유지하고 기존 기본 위치는 네 개만 바뀐다. 구역 범위는 `x113..151/y2..24 → x110..151/y2..24`이며, 전체 트리 범위는 **x0..211/y0..24**로 같다. 기존470개 기본 위치와474개 기존 ID의 상대 선언 순서를 유지한다. 정보국 삽입 뒤의 선언 인덱스 이동은 ID 이전이 아니다.

## 기준·조건부 이동·표시 모델

현재 트리는 **475개, 절대 기준7개, 상대468개, 직접 offset7개**다. 모든 상대 기준이 먼저 선언되고, 자기 참조·순환·누락 없이 절대 기준으로 끝나는지 직전/현재 모두 계산했다. 직접 offset7개의 순서 있는 정의와 조건은 이전 포트와 같다. 신규 중점이나 네 자손에 정치 이동을 복제하지 않는다.

SHOW 또는 초기 HIDE에는 민주 완료 이동이 적용되지 않는다. HIDE에서 `KOR_democracy_advance_forward`를 **완료한 뒤** 해당 민주 기준과 자손의 x에−35가 한 번 반영된다. 분기 진행 중이라는 사정만으로 완료 offset을 미리 적용하지 않는다. 공산·파시·왕정 완료의 기존 숨김 조건과 각각의 기준 이동도 실제 소스에서 해석했다.

18개 상태는 SHOW/HIDE 각각 초기·공화국만 완료·민주 분기 진행 중·민주 완료·공산 완료·파시 완료·왕정 완료의14개와, SHOW/HIDE 각각 초기/민주 완료의 LaR 없는4개다. 진행 중 상태의 완료 집합은 공화국만 완료한 상태와 같고 별도 완료 표식을 가정하지 않는다.

| 대표 모델 상태 | 지원/후속 네 개 | 초대 두 개 | 정보국 |
|---|---|---|---|
| SHOW 모든 정치 단계 | 기본 위치 | 기본 위치 | `(62,1)`·LaR가 있을 때 표시 |
| HIDE 초기·공화국만 완료·민주 진행 중 | 기본 위치 | 기본 위치 | `(62,1)`·LaR가 있을 때 표시 |
| HIDE 민주 완료 | x−35 단일 상속 | x−35 단일 상속 | `(62,1)`·정치 이동 없음 |
| HIDE 공산·파시·왕정 완료 | 민주 기준의 조건 때문에 모델상 숨김 | 같은 모델상 숨김 | `(62,1)`·LaR가 있을 때 유지 |
| LaR 없는 초기/민주 완료 | 기존 정치 배치 유지 | 기존 정치 배치 유지 | 자체 DLC 조건 때문에 모델상 숨김 |

모델상 표시는 자신과 상대 기준 조상의 `allow_branch`를 평가하는 **명시적인 정적 가정**이다. `relative_position_id` 자체가 엔진의 숨김 수명주기를 보장한다고 주장하지 않는다. 가용성·우회·실제 선택·하위 가지 발견 규칙·실행 순서는 시뮬레이션하지 않았다. 숨겨진 기준의 자손을 실제 엔진에서 접근할 수 있는지는 화면 검증이 남는다.

모델의 HIDE 민주 완료는 LaR 있을 때272개, 없을 때271개이며 중심 범위는 x0..116/y0..24다. 이 수치를 실제 UI의 표시 개수나 스크롤 한계 관측으로 사용하지 않는다. 각 상태의 전체 정의 범위·모델상 표시 범위와 주변 노드 위치는 JSON에 별도 필드로 남긴다.

## 제한된 기하·보존 확인

기존 포트가 기록한 grid `(96,130)`을 이번에도 **정적 기하 가정**으로 사용한다. 현재 설치 `interface/nationalfocusview.gui`는 SHA-256 `247B096A53AEE65E139FFF1BF0049C9FBD7A3AFA40916882304749FEFAAAED96`로 기존 기록과 같으며, 소스에서 item165×128·이름 영역147×20의 위치를 다시 읽었다. 기존 배경 모델183×84도 같은 명세를 사용한다. 실제 엔진 간격을 새로 실측한 결과가 아니다.

18개 모델에서 중복 중심과 새 item/title-background/name-textbox 사각형 접촉은 없다. 이 사각형은 그림 symbol·글자 glyph·외곽 효과·완료 shine의 전체 범위를 포함하지 않는다. 실제 아이콘 무겹침·연결선 무간섭·클릭 가능·광택 표시의 통과로 확대하지 않는다. 기존 11월 1일 기록의 직각 선 가설 후보도 새 그림/후속 연결을 실제로 확인한 결과가 아니므로, 이번에는 실제 연결선 routing을 검증했다고 하지 않는다.

지속적 중점 패널 `(200,1700)`, 시민사회 inlay `(1050,1400)`,8개 바로가기의 목적지·배율0.65와 나머지 non-focus 필드는 이전 포트와 순서 있는 AST가 같다. 이 수치와 focus grid를 같은 단위로 비교하지 않는다. 패널·스크롤·바로가기의 실제 접근은 별도 UI 항목이다.

외부 `layout-source-checks.json`은 **2011 PASS / 0 FAIL**이다. 직전474개/현재475개 정의의 기준 선행 선언과 연쇄를 각각 확인한 항목, 보존 항목과18개 모델의 중심·사각형·정보국 이동/DLC 조건을 합한 소스 검사 수다. 게임 실행·중점 정상 완료·UI 관측 수가 아니다. 별도 독립 이식 검토 `independent-port-review.json`의265/0은28출력·순서 있는 변경 범위·현지화·정의 유일성·mutation 거부를 다루며, 두 검사 수를 합쳐 런타임 성공 수로 보고하지 않는다.

초기 배치 담당 작업은 새 좌표 명세와 이 문서만 추가했다. 런타임 좌표·지도·게임 설치·원본·Workshop·사용자 설정·저장을 변경하거나 게임을 실행하지 않았다. 이후 root의 별도 승인된 실제 관측은 다음 절에 출처를 구분해 기록한다. 이 문서 갱신 역시 UI·활성 프로필·생산 좌표·저장을 변경하지 않으며 Git·게시 작업을 하지 않는다. 현재 소스가 달라지면 위 해시·계산을 다시 수행하고 과거 결과를 고쳐 덮지 않는다.

## 별도 승인 후 제한된 실제 UI·효과 관측

TASK는 `C:\hoi\test\hok-rt56-democratic-architecture-20261120-01`이다. `runtime/ui-observations.json`·`ui-observations-followup.json`은 **root가 Computer Use로 실제 관측하고 전달한 기록**이며 이 문서 작성자가 화면을 직접 조작·관측한 증거가 아니다. 화면 사본은 `runtime/ui/`, 실제 적용 소스·프로필 지문은 `runtime/runs/c0-en/`·`c1-ko/`의 `applied.json`에 있다. 프로필의 창1280×720·GUI배율1.0은 **설정 요청값**이며 실제 캡처 크기로 표현하지 않는다. 보관된 C0/C1 이미지 파일13개의 읽기 전용 메타데이터는 각각2564×1504다. 실제 캡처 치수를 설정값으로 대체하지 않는다. 중점 화면에서 확대·축소를 조작한 관측이며 source grid의 픽셀 실측도 아니다. C0는RT56+호환판의 영어, C1은RTK를 더한 한국어다. 해당 cold run은 실제1.20.0.0.8873 체크섬 `a044`로 보고됐으며 설치 metadata·다른 fixture 체크섬과 혼동하지 않는다.

| 사례·증거 | 관측 범위 | 확대하지 않는 범위 |
|---|---|---|
| C0 영어 정보국 | `ui/c0-en-intelligence-layout.png`·`ui/c0-en-intelligence-tooltip.png`: 재무장 가지의 새 눈 그림,35일·재무장 시작 선행·기관 생성/요원+2·영어 효과 툴팁 | 정상 완료·완료shine·다른 조건별 배치의 통과가 아니다. |
| C0 영어 지원/산둥 | `ui/c0-en-support-layout.png`·`ui/c0-en-support-unlock-tooltip.png`·`ui/c0-en-shandong-tooltip.png`: 두 지원 가지가 구분되어 겹치지 않는 초기 화면, 지원35일·결정 해금과 산둥70일·CHI50%·TfV·거점/이전 안내 | 모든 제목·연결선·배타선·숨긴 기준·스크롤 경계의 검증으로 확대하지 않는다. |
| C1 한국어 | `ui/c1-ko-intelligence-*.png`·`ui/c1-ko-support-*.png`·`ui/c1-ko-shandong-tooltip.png`: 같은 선택 중점의 그림·한국어 조건/보상·해금 표시. 각 실제 파일은 UI 관측JSON에 열거 | 초기 전쟁 지지도15%라 재무장 시작의20% 초과 조건에 막힌 화면도 별도 보존했다. 이 실행의 정상35일·70일 완료를 주장하지 않는다. |
| CHI 경계 강제 효과 | `ui/chi-boundary-agency-three-slots.png`와 `geography/qa/native-chi-effects-02.json`: 실제 기관 UI0/3, 새 저장의 기존 기관슬롯1→3/증가2와 정보국 정신 | 기관이 없을 때 생성하는 분기·정상 정보국 완료·배치 offset/shine의 증거가 아니다. |
| 산둥 출범·인정 강제 효과 | zero r9·positive r10·protection r12b의 별도 native 보고서에서 동적 정부·지역·전력·보호·기지/인정을 확인했다. root는zero r9의 자치령·웡 외교 화면도 관측 | 이는 중점 배치18개 모델·정상 진행·한국어/영어 모든 완료 화면의 검증이 아니다. 자세한 지역 경계는 [지리 기록](2026-11-20-chinese-government-state-mapping.md)의 실제 확인 절을 따른다. |

보관 이미지13개의 경로·SHA·실제 픽셀 치수와 프로필 요청값의 구분은 TASK의 `geography/qa/layout-ui-capture-metadata-01.json`에 남겼다. 이미지 메타데이터를 읽었으며 화면 관측을 새로 수행하거나 그림을 수정한 것은 아니다.

기계 명세의 상태 `STATIC_CURRENT_PORT_SPEC_RUNTIME_UI_UNVERIFIED`와18개 scenario는 **초기 작성 시점의 정적 명세**로 보존한다. 위 일부 초기 UI 관측을 이유로 그18개 모델을 모두 실제 검증으로 승격하거나 source 계산·hash·모델 좌표를 바꾸지 않는다. source2011/0, UI 관측, 강제 effect·저장, 정상 진행의 결과 수를 합치지 않는다. root가 실제 종료를 관측한 사례와 positive r10의 backend `CloseMainWindow` 종료도 전체 이식 기록에서 구분한다.

## 남은 실제 확인

위 실제 초기 화면 관측 밖의 SHOW/HIDE 전환, 정상 민주 완료 전후·다른 이념 완료·LaR 없는 배치를 확인해야 한다. 지원/초대의 제거된 배타선 전체, 중국70일 정상 진행·도중 취소, 정보국 정상 완료·shine, 주변 해군/공군 가지·한영 긴 이름판·연결선·숨겨진 기준·패널·바로가기·스크롤의 나머지 조합은 관측 대상으로 남긴다. 정상 진행과 강제 완료 진단, 새 저장 재로드와 변경 전 저장의 호환은 각각 구분한다.
