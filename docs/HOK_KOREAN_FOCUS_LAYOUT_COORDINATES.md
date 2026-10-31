# 한국 중점 현행 배치 좌표와 이식 이력

## 2026-11-01 민주주의 내부 간격 압축

상태: **STATIC_SPEC_RUNTIME_UNPROVEN**. 현행 배치는 donor `07de265` 위의 미커밋 민주 압축 delta를 호환판 `656d9b425a66d95f55d8c86f1b976b2e094cc4d8` 이후에 선택 이식한 것이다. [이번 구현 기록](implementation/2026-11-01-korean-democratic-layout-port.md)과 [신규 전후 좌표 JSON](data/HOK_KOREAN_DEMOCRATIC_LAYOUT_COORDINATES.json)을 따른다. 기존 아래의 10월 31일 민간 핵 가지 기록과 그 JSON은 당시 소스의 이력으로 보존하며 현행 전체 배치의 해시로 사용하지 않는다.

474개 ID·선언 순서·절대 기준 7개·상대 467개·직접 offset 7개와 모든 게임플레이·RT56 지도 참조를 유지한다. 민주 기준 `(127,2)` 아래 95개 중 직접 배치 32개(37개 x/y 값)를 수정하여 86개 기본 위치가 바뀌고 비민주 379개 위치는 유지한다. 민주 기본 범위는 `x108~158/y2~24→x113~151/y2~24`, 중심 가로 폭은 50→38칸(24% 감소)이다. 대통령과 서방/미국 선택의 간격은 각각 18→10칸·16→10칸이다. 전체 기본 범위는 `x0~211/y0~24`를 유지한다.

HIDE 민주 완료의 기존 `−35x`는 자기·조상 연쇄에서 한 번 적용되며 완료 민주 범위는 `x78~116/y2~24`다. SHOW 및 초기 HIDE에는 이 완료 offset이 적용되지 않는다. 산업·사회협약과 그 13개 시민사회 묶음은 내부 모양을 유지한 채 `−1x` 이동한다. 고정 산업·핵 연구·다른 정치·만주 배치, 지속적 중점 패널 `(200,1700)`, 8개 바로가기와 시민사회 inlay `(1050,1400)`은 유지한다.

신규 JSON은 실제 호환판 직전 Git object `3D06E88B4DF242E81E4FD15FC32D7D84FD9E3F6073AA23F180D89651D8193117`과 최종 checkout `DE7959986349B07C014C866B08E03DC2BF0AE81BE80E6AF29D92CF03F572B5B1`을 순서 있게 해석한 위치·전체 기준 연쇄·선행/배타 그룹·offset 원문과 제한된 SHOW/HIDE 모델이다. 474개 x/y 외 ordered gameplay와 고정 UI·기준/offset 보존을 확인했다. Git object와 checkout 해시는 줄바꿈을 포함한 입력 표현을 구분한다.

실제 provider GUI의 `(96,130)` grid·`165×128` 항목·`147×20` textbox와 배경 DDS `183×84`로 계산한 사각형은 네 모델에서 전후 겹침 0개다. 세 orthogonal 선 가설에는 **새 비관련 배경 캔버스 접촉 후보 3개**가 있고 새 textbox 접촉은 없다. 공직감찰→결산/만주 선제타격, 아시아 초대→지원/중국 초대, 전쟁 준비→군 예산/극단주의 금지의 후보와 공유 선행 관계를 [구현 기록](implementation/2026-11-01-korean-democratic-layout-port.md)에 분리했다. 실제 선 routing·표시 간섭은 **UNPROVEN**이며 이 가정만으로 원본 배치를 재설계하지 않았다.

donor의 실제 HIDE/SHOW 관측·보존 검사 수·메타데이터를 포트 runtime 결과로 복사하지 않는다. 실제 이름판·아이콘·선·클릭·광택·조건 전환과 저장·AI·DLC·성능·멀티플레이는 **UNPROVEN**이다.

## 2026-10-31 민간 핵 가지 이식 당시 기록

작성: 2026-10-31 (Asia/Seoul). 상태: **STATIC_SPEC_RUNTIME_UNPROVEN**. 이 문서는 호환판의 기존 배치 기록 위에 이번 민간 핵 중점 두 개의 선택 이식을 기록하는 유지 관리 명세다. donor의 좌표 문서나 실제 화면 결과를 호환판 검증으로 복사하지 않는다.

## 기존 명세와 이번 입력

기존 472개 전체의 배치·상대 연쇄·SHOW/HIDE·시민사회 패널은 [시민사회 좌표 명세](HOK_KOREAN_CIVIC_LAYOUT_COORDINATES.md)와 [그 JSON](data/HOK_KOREAN_CIVIC_LAYOUT_COORDINATES.json)에 당시 소스로 보존한다. [왕정 H1 명세](HOK_KOREAN_ROYAL_LAYOUT_COORDINATES.md)와 역사적 `docs/upstream/` 문서는 해당 변경 당시의 기록이며 이번에 고쳐 쓰지 않는다.

이번 [기계 명세](data/HOK_KOREAN_FEATURE_INTEGRATION_LAYOUT_COORDINATES.json)는 `e871bd1246152c2d32f67c43181441ff31a706e7`의 실제 호환판 Git 소스와 이번 최종 생산 출력 `common/national_focus/korea.txt`를 독립 해석한다. donor 고정 출처는 `07de265c1e992abb6584bdfcdf140320188c07f9`, 부모는 `860efe7a3513148dc6964b7e0e3dfafd19addfb7`다. 파일 해시, 472→474개의 ID·선언 인덱스·배치·진행 선행·offset 및 전체 기준 연쇄를 기록한다. 체크섬·UI·정상 진행 결과를 뜻하지 않는다.

| 입력 | SHA-256 |
|---|---|
| 직전 호환판 Git object | `A30390A980BD842BDE447BCDE8570C60E1FB85AC55AD30A74A637C0066D7B023` |
| 최종 생산 checkout | `FDD4296796566676BD1B298FB3587AA7F4486D4F436116102B58E57842E6C753` |

이 해시는 각각 원래 Git object와 실제 최종 checkout 바이트다. 줄바꿈 표현이 다른 입력의 해시를 동일한 것으로 취급하지 않는다. 외부 `C:/hoi/test/hok-rt56-feature-port-20261031/documentation-layout-calculation.py`가 기존 순서 보존 parser로 두 실제 소스를 읽어 이 기계 명세를 만들었다. 기존 472개 배치 필드·진행 선행·배타·기본 위치와 고정 패널·바로가기의 보존을 확인했으며, gameplay validator나 게임을 실행한 결과로 표현하지 않는다.

## 두 새 중점과 주변 위치

| 중점 | 상대 기준 | 소스 상대값 | 해석한 기본 위치 | 실제 진행 선행 |
|---|---|---|---|---|
| 원화 평가 절하 `KOR_devalue_the_won` | 절대 기준 | `(15,0)` | `(15,0)` | 기존 조건 유지 |
| 경공업 수출 지원 `KOR_support_light_industry_export` | 원화 평가 절하 | `(0,1)` | `(15,1)` | 원화 평가 절하 |
| 서울대학교 확장 `KOR_seoul_national_university_expansion` | 경공업 수출 지원 | `(-1,1)` | `(14,2)` | 기존 선행 유지 |
| 핵분열 연쇄반응 실험 `HOK_KOR_fission_chain_reaction_experiments` | 서울대학교 확장 | `(0,1)` | **`(14,3)`** | 서울대학교 확장 |
| 민간 원자로 투자 `HOK_KOR_civilian_nuclear_investment` | 핵분열 연쇄반응 실험 | `(0,1)` | **`(14,4)`** | 핵분열 실험 + 핵 연구·Götterdämmerung 가용 조건 |
| 세계수준 석학 유치 `KOR_attract_worldclass_scholars` | 서울대학교 확장 | `(2,1)` | `(16,3)` | 기존 선행·공장 조건 유지 |

중점 x/y는 픽셀이 아닌 격자 단위다. 기본 위치는 기준의 해석된 위치와 상대값을 합해 계산하며, `relative_position_id`는 진행의 `prerequisite`와 별개다. 신규 두 중점의 기준 연쇄는 고정 산업 기준으로 끝나며 자신이나 조상의 직접 정치 offset이 없다. 따라서 소스 모델의 SHOW/HIDE 정치 선택에 따라 이동할 offset이 없다. 실제 엔진의 표시·선·전환·스크롤은 별도 확인한다.

기존 472개 배치 필드·진행 선행·배타·7개 offset·기준 7개·지속적 중점 패널 `(200,1700)`·8개 바로가기·고정 시민사회 inlay `(1050,1400)`은 유지한다. 두 새 정의는 서울대학교 확장 뒤에 삽입하므로 이전 선언 인덱스 15 이상은 두 칸 증가한다. 인덱스 변화는 ID 이전이 아니며 기존 중점 위치를 바꾸지 않는다. 트리는 474개, 절대 기준 7개·상대 467개이며 전체 기본 범위 `x0~211/y0~24`를 유지한다.

## 보상·기간과 검증 경계

첫 중점은 35일에 핵 혁신 `1.00`과 핵 기술 선행 연구 불이익 2년 감소 1회를 준다. 둘째는 `cost=35`의 기본 245일이며 민간 원자로 기술을 지급한다. 최종 소스에는 5일 감산이 없고 두 중점의 기본 합계는 280일이다. 기존 국방·무궁화·연구망 경로의 위치·선행·보상을 바꾸지 않는다. 기술 기보유 bypass·조건 상실 취소 및 DLC 조건은 생산 스크립트에서 확인하며 배치 계산으로 실행 성공을 판정하지 않는다.

중심 좌표·부모 연쇄·수치 범위는 정적 근거다. 이름판 폭·연결선 routing·아이콘 외곽·클릭 영역·잠김/활성/완료·shine·한국어/영어 표시와 실제 GUI 배율·확대·스크롤은 RT56 대상 새 게임에서 확인해야 한다. 현재 UI·정상 진행·DLC·AI·저장·멀티플레이 결과는 **UNPROVEN**이다. donor의 이전 240일 소스 실행은 최종 245일 소스나 이 호환판의 실행 증거가 아니다.

통합 범위와 검증 상태는 [이번 구현 기록](implementation/2026-10-31-korean-feature-integration-port.md)을 따른다.
