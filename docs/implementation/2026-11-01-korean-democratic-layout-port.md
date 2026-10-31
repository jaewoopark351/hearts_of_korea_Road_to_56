# 2026-11-01 한국 민주주의 중점 내부 배치 선택 이식

## 범위와 출처

업데이트된 HOK donor의 민주주의 내부 간격 압축을 호환판에 선택 이식한다. 이는 큰 내부 공백과 긴 연결을 줄이는 의도적인 UI 배치 개선이며 게임플레이·지도 호환성 수리나 신규 콘텐츠 추가가 아니다. 474개 중점의 ID·선언 순서·선행 AND/OR·배타·보상·기간·조건·AI, 기존 RT56 지도 매핑·기능 연동·영국 영어·자산을 유지한다.

- 호환판 시작: `feat/korean-focus-update-20260922@656d9b425a66d95f55d8c86f1b976b2e094cc4d8`, 작업 트리 깨끗함.
- donor: `feat/korean-focus-expansion-ai@07de265c1e992abb6584bdfcdf140320188c07f9` 위의 **미커밋** 배치·문서 변경. donor Git commit만으로 이번 변경을 재현할 수 없으므로 선택한 물리 파일을 별도로 해시 고정한다.
- donor 직전 중점 SHA-256: `3CC9F676203E18F53B7B6A896ADBD9E03796B861D492326E48056EC5E3A122CA`.
- donor 새 중점 SHA-256: `6562D4ACFD05F791026502A9AEACE3668D3C89869DF4279F75C2F1016763F163`.
- 호환판 직전 checkout SHA-256: `FDD4296796566676BD1B298FB3587AA7F4486D4F436116102B58E57842E6C753`.
- RT56: Workshop `820260968`, manifest `7553774178744855191`. 기존 source lock과 역사적 보관본은 유지하고 이번 배치만 별도 가역 계층으로 연결한다.

[이번 잠금](../../tools/hok_democratic_layout_lock.json)과 [별도 보관본](../upstream/hok-democratic-layout-20261101/)은 중점 소스 한 개·출처 문서 여섯 개와 직전/통합 출력을 고정한다. 기존 통합 원장의 한국 트리 소유권 분류 `OVERRIDE`는 유지하고, 이번 계층에서는 donor delta와 기존 호환판 출력을 `THREE_WAY_MERGE`로 결합한다. 기존 feature 계층을 정확히 복원하는 역적용을 연결하며 과거 source 핀을 새 donor 트리로 바꾸지 않는다.

donor `descriptor.mod`의 기존 사용자 수정과 donor 프로젝트 README는 이 호환판의 descriptor·정체성·업로드 설정으로 복사하지 않는다. 원본·Workshop·게임 설치·사용자 데이터·설정·로그·저장은 읽기 전용으로 다뤘으며 커밋·푸시·게시·업로드는 이번 요청에 포함하지 않는다.

## 현재 설치와 구성

| 항목 | 읽기 전용 인벤토리 |
|---|---|
| HOI4 | `Operation Postern 1.19.4.1.99a5`, Steam build `26282552`; 기존 로그 checksum `f584`는 donor 실행 |
| 활성 playset | `한국test01`: donor `C:/hoi/hearts_of_korea` → 일반판 English Translation Anime Modder's Edition `3823285419` |
| 비활성 대상 playset | `Road to 56 한국 테스트`: enabled 위치 0 현재 호환판 → 1 RT56 Korean Translation `2769576030` → 2 RT56 `820260968`; donor 없음 |
| 언어·DLC | `l_korean`, GUI 배율 `1.000000`, `disabled_dlcs=[]`; 실제 보유/인식 DLC별 동작을 검증한 목록이 아님 |
| 사용자 데이터 | Windows, `C:/Users/jaewo/OneDrive/문서/Paradox Interactive/Hearts of Iron IV` |
| 호환판 정체성·의존 | 기존 item `3796816200`, RT56 + Korean Language 선언 유지 |

외부 `C:/hoi/test/hok-rt56-democratic-layout-20261101/baseline-context.json`에 물리 경로·선택 목록·launcher descriptor 해시를 보존했다. 목록 순서는 엔진의 유효 우선순위 증거가 아니다. 대상의 RT56 Korean Translation은 선언된 Korean Language와 다른 모드이고 `replace_path="localisation"`을 사용하므로 최종 언어 계약은 별도 실행 대조가 필요하다. 이번에는 게임을 실행하거나 playset·설정을 변경하지 않았다. 현재 donor 구성이나 과거 donor 화면을 호환판 실행 결과로 쓰지 않는다.

## 배치 delta와 보존

donor diff는 32개 중점의 직접 x/y 대입 37개와 기여 주석 32개다. `common/national_focus/korea.txt`의 기존 `OVERRIDE`에 이 배치 hunk만 적용한다. 기준 ID·정의 순서·7개 offset·진행 조건을 바꾸지 않고 이동한 기준의 상대 자손이 따라가게 한다.

| 항목 | 직전 → 적용 |
|---|---|
| 전체 중점·절대 기준·상대 중점 | 474 · 7 · 467 유지 |
| 민주 기준 사슬 | 95개 유지; 직접 배치 32개, 해석된 기본 위치 이동 86개 |
| 비민주 위치 | 379개 유지 |
| 민주 기본 범위 | `x108~158/y2~24` → `x113~151/y2~24` |
| 민주 중심 간 가로 폭 | 50 → 38칸, 24% 감소 |
| 대통령 선택 간격 | 18 → 10칸 |
| 서방·미국 선택 간격 | 16 → 10칸 |
| 전체 기본 범위 | `x0~211/y0~24` 유지 |
| 민주 진입 기준·HIDE offset | `(127,2)`, 완료 때 `(-35,0)` 단일 상속 유지 |
| 민주 완료 HIDE 계산 범위 | `x73~123/y2~24` → `x78~116/y2~24` |

산업·사회협약과 시민사회 13개 묶음은 내부 모양을 유지한 채 `−1x` 이동한다. 세계 속의 대한민국은 `(148,6)→(145,5)`로 옮기지만 부모와의 상대 가로 차이는 `12→14`이므로 모든 개별 연결이 짧아진다고 표현하지 않는다. 서방 기존 상선·영국 구축함의 `(140,11)/(140,13)`은 유지하고 의용군·미국 계열·아시아 초대/지원·공동통상 후속을 함께 압축한다.

기준점·배치 기준과 진행 선행은 별개다. 정부 지원 강화의 두 선행 AND, 시민사회 진입의 두 단독집권 OR, 대한의용군단의 서방/미국 OR를 그대로 유지한다. HIDE에서 민주 진입 완료 후 위치를 갱신하는 기존 `mark_focus_tree_layout_dirty`도 유지하며 자손에 추가 offset이나 콜백을 넣지 않는다. 신규 시설·과학자·급습·세력·훈장, 핵 35일+245일 보상 경로와 모든 RT56 주/프로빈스 매핑도 이 배치 작업에서 바꾸지 않는다.

## 좌표 명세와 제한된 기하 계산

[현재 배치 진입 문서](../HOK_KOREAN_FOCUS_LAYOUT_COORDINATES.md)와 [신규 기계 명세](../data/HOK_KOREAN_DEMOCRATIC_LAYOUT_COORDINATES.json)는 실제 호환판의 직전 Git 소스와 최종 생성 출력으로 작성했다. donor 좌표 JSON의 runtime 검증 상태는 이식하지 않았다. 기존 [10월 31일 핵 가지 좌표 JSON](../data/HOK_KOREAN_FEATURE_INTEGRATION_LAYOUT_COORDINATES.json), 시민사회·왕정 명세와 `docs/upstream/` 역사 자료는 해당 시점의 증거로 보존했다.

| 해석 입력 | SHA-256 |
|---|---|
| 직전 호환판 Git object | `3D06E88B4DF242E81E4FD15FC32D7D84FD9E3F6073AA23F180D89651D8193117` |
| 최종 생산 checkout | `DE7959986349B07C014C866B08E03DC2BF0AE81BE80E6AF29D92CF03F572B5B1` |

Git object와 checkout은 줄바꿈 표현이 다르므로 해시를 같은 입력으로 취급하지 않는다. 독립 해석은 474개 ID·순서·모든 x/y 외의 순서 있는 중점 정의, 고정 UI·바로가기와 7개 offset 보존을 확인했다. 직접 수정 32개·숫자 대입 37개·기본 위치 이동 86개, 민주 사슬 95개와 비민주 379개 위치 보존을 재계산했다. SHOW 초기·민주 완료 및 HIDE 초기의 모델 표시 수는 474개, HIDE 민주 완료는 271개로 전후 동일하다. 이 수치는 선언된 Boolean/기준 연쇄 모델이며 실제 엔진의 표시 수 관측이 아니다.

GUI·sprite·texture의 동일 상대경로를 호환판→RT56→vanilla 순서로 조사했고, 선택 GUI·배경 registry의 호환판/RT56 override와 RT56의 같은 GUI/배경 sprite ID는 발견하지 못했다. 선택 provider는 설치 vanilla의 `interface/nationalfocusview.gui`이며 SHA-256은 `247B096A53AEE65E139FFF1BF0049C9FBD7A3AFA40916882304749FEFAAAED96`다. 이는 소스 모델의 provider 선택이며 엔진 우선순위를 관측한 결과가 아니다.

실제 GUI의 grid `(96,130)`, 항목 `165×128`, 이름 textbox `(15,58)/147×20`, 배경 sprite 위치 `(5,40)`, link 시작 `(80,64)`·끝 `(80,0)`·간격 `(16,16)`을 읽었다. `GFX_technology_unavailable_item_bg`의 DDS는 **183×84**이며 alpha가 있는 픽셀의 전체 bounds도 같은 캔버스다. donor의 보수적 164×50 이름판 모델은 별도 가정이므로 두 결과를 같은 기하 검사로 취급하지 않는다. 새 JSON은 실제 payload 캔버스·항목·textbox 각각을 구분한다.

| 제한된 모델 결과 | SHOW 초기/완료·HIDE 초기 | HIDE 민주 완료 |
|---|---|---|
| 항목·배경 캔버스·textbox 사각형 겹침 | 전후 모두 0개 | 전후 모두 0개 |
| 세 선 가설의 비관련 캔버스/textbox 접촉 후보 | 75→74개; 새 3개·해소 4개 | 48→47개; 새 3개·해소 4개 |
| 다른 선행 부모와의 공유 관계 접촉 후보 | 139→144개; 새 5개 | 88→93개; 새 5개 |
| 새 후보 중 textbox 접촉 | 0개 | 0개 |

후보 수는 세 꺾임·두 영역 모델의 서로 다른 조합 수이며 실제 결함 개수나 게임 시험 수가 아니다. 새 비관련 후보 세 개는 모두 배경 캔버스 사각형에서만 생겼다.

1. 공직 감찰 정비 → 국회 결산위원회 선의 자식 가까운 꺾임과 만주 선제타격 배경.
2. 아시아 독립국가 초대 → 아시아 독립 지원 선의 부모 가까운 꺾임과 중국 초대 배경.
3. 다음 전쟁의 준비 → 군 예산안 증액 선의 부모 가까운 꺾임과 극단주의 금지 배경.

이 후보의 실제 엔진 선 경로와 표시 간섭은 **UNPROVEN**이다. 소스 모델 결과만으로 donor의 의도된 배치를 다시 바꾸지 않았으며, RT56 실제 UI에서 해당 세 지점과 기존·공유 후보를 함께 확인해야 한다. 전체 ID·좌표·선행/배타·조건부 투영과 후보 ID/영역/꺾임은 신규 JSON에, 도구와 요약은 외부 `documentation-coordinate-review.py`·`documentation-coordinate-summary.json`에 기록했다.

사각형과 여러 orthogonal 선 가설은 엔진 렌더러가 아니다. 상위 항목의 크기가 glow·아이콘·광택 외곽 전체를 감싼다는 보장, 실제 폰트 줄바꿈·GUI 배율·카메라·선 routing·배타 표식·클릭 영역 판정은 이 계산에서 하지 않는다. 공유 OR/AND 합류에 대한 선 접촉 후보와 관계없는 접촉을 구분하고 새 후보가 없다는 사실도 모든 상태의 UI 무겹침으로 일반화하지 않는다.

## 정적 검증과 기존 오류

직전 2026-10-31 전체 검사는 **20 PASS / 0 WARNING / 6 ERROR**였다. map synthesis·Korean building placements·shared overrides·East Asia overrides·doctrine migration의 기존 소스 drift 다섯 개와 second-wave material-cycle의 `descriptor.mod` 보존 해시 한 개다. 이번 배치 이식에서 해당 소스 핀을 재설정하거나 검사를 완화하지 않았다. 이번 범위 검사와 전체 결과를 별도로 기록한다.

| 실제 검사 | 결과 |
|---|---|
| 선택 snapshot·생성·역적용 | 중점 소스 1개·문서 6개 고정, 기존 feature ancestor 복원 통과; 런타임 변경은 `korea.txt` 한 개 |
| 민주 배치 전용 계약 | 474 ID/순서·32개 블록/37개 값·95/86/379·7개 기준/offset·SHOW/HIDE 조건 모델 통과 |
| 기존 feature·civic·shipbuilding·expansion | 다섯 범위 검사 중 나머지 네 계약 통과; 이전 계층과 게임플레이 보존 |
| 독립 범위 감사 | x/y 외 ordered AST 동일, 무관한 runtime 수정 없음 |
| 통합 원장 | 1,505행·같은 상대경로 충돌 73개와 기존 분류 유지; 역사 열 변화는 한국 트리의 reason/출력 해시와 README 출력 해시뿐 |
| 전체 구조·현지화 | script 216파일과 locale 85파일·5,627키 유지; 구조·BOM/헤더·키·논리 ID 검사 통과 |
| 전체 aggregate validator | **21 PASS / 0 WARNING / 6 ERROR**; 신규 민주 gate 통과, 기존 여섯 실패 유지, 새 실패 없음 |

결과는 외부 `democratic-layout-check.txt`, `feature-check.txt`, `civic-check.txt`, `shipbuilding-check.txt`, `expansion-check.txt`, `independent-layout-audit.json`, `ledger-audit.json`, `final-validation.txt`에 둔다. 생성·정적·보존·기하 계산과 엔진 실행 결과는 구분한다.

최종 여섯 실패는 위의 기존 소스 drift 다섯 gate와 descriptor 보존 해시 gate다. 전체 포트가 정적 통과하거나 새 게임 실행 가능하다는 판정은 아니다. 새 배치 계층·기존 네 콘텐츠 계약·구조·현지화·통합 원장의 통과와 이 잔여 실패를 함께 기록한다. 최종 donor 물리 중점은 고정한 `6562D4AC…63F163`과 같았으며, 최종 호환판 runtime 변경은 해시 `DE795998…572B5B1`의 한국 중점 파일 하나다.

## donor 관측과 호환판의 미검증 범위

donor 출처 기록에는 소스 보존 29/0·좌표 대조 25/0, HOK-only `1.19.4.1.99a5`/인식 DLC 36개의 기준 `1395`, HIDE probe `f02c`, 진단 없는 SHOW `7572`가 있다. HIDE에서는 부모만 합성 준비한 뒤 민주 진입의 실제 선택·정상 완료와 같은 프로세스 체크포인트 재로드, 별도로 준비한 이승만/협력 및 김구/공공 소유의 해당 화면을 관측했다. SHOW에서는 부모·민주 진입을 정상 선택·진행하고 같은 카메라·트리 배율 0.65의 상단 위치 유지를 관측했다.

이 자료는 donor의 제한된 증거다. 정확한 35칸 픽셀 측정·재시작 후 기존 저장 재로드·모든 95개 이름판/클릭/광택·모든 정책과 다른 정치 전환·장기 AI·멀티플레이를 증명하지 않는다. `SLOW INTERFACE`는 표시됐지만 비교 성능을 측정하지 않았다. HIDE 오류 행은 기준 47→54→59, SHOW는 47→54→54→56으로 frontend·rename 경고가 남으므로 전체 새 오류 0으로 옮겨 적지 않는다.

이번 호환판의 **실제 RT56 UI·SHOW/HIDE 정상 전환·정상 진행·저장·DLC·AI·성능·멀티플레이는 UNPROVEN**이다. 별도 대상 실행에서는 donor를 제외한 물리 구성과 언어·DLC·GUI/트리 배율을 고정하고 대표 대통령·시민사회·중앙 AND·하단 아시아·서방/미국 연결, 패널·바로가기와 스크롤 접근을 확인해야 한다. 소스 보존과 배치만으로 기존 저장의 일반 호환을 약속하지 않는다.

현재 결과는 작업 트리에 남기며 커밋·푸시·Workshop 변경은 수행하지 않는다.
