# 2026-10-31 한국 기능 연동·민간 핵 연구 선택 이식

## 범위와 고정 출처

업데이트된 `C:/hoi/hearts_of_korea`의 한국 콘텐츠를 RT56 호환판에 선택 이식한다. 대상은 함장 훈장·문구, 소양강댐 수문, MIO 전문화, 연구망, 나가사키 급습, 네 세력 템플릿, 기존 결정 해금 안내와 민간 핵 연구 중점 두 개다. 의도적인 신규 보상·기능은 호환성 복구와 구분하며, 전체 donor 트리나 공용 RT56 시스템을 복사하지 않는다.

- 호환판 시작: `feat/korean-focus-update-20260922@e871bd1246152c2d32f67c43181441ff31a706e7`, 작업 트리 깨끗함.
- donor 출처: `feat/korean-focus-expansion-ai@07de265c1e992abb6584bdfcdf140320188c07f9`; 부모 `860efe7a3513148dc6964b7e0e3dfafd19addfb7`. 최초 인벤토리에서는 부모 위의 staged 변경이었으나, 작업 중 donor의 새 커밋을 확인하여 최종 출처를 이 커밋으로 고정했다. donor에 대한 Git 작업은 이 이식에서 수행하지 않았다.
- RT56: Workshop `820260968`, manifest `7553774178744855191`. 2026-10-20 이식에 사용한 호스트 manifest와 같으며, 이번에도 관련 물리 파일의 해시를 별도로 확인한다.
- 이전 source lock과 역사적 보관본은 유지한다. [이번 잠금](../../tools/hok_feature_update_lock.json)과 [별도 보관본](../upstream/hok-feature-integration-20261031/)에 런타임 텍스트 30개·자산 28개·문서와 원본 기록 51개의 출처·출력·변환을 기록하고, 기존 `tools/source_snapshot.py`와 `tools/build_korean_focus_update.py`의 선택 이식 흐름에 연결한다. 별도 RT56 22파일과 vanilla 19파일, 현재 Workshop manifest도 고정해 대조한다.
- 원본, Steam Workshop·게임 설치, launcher, 사용자 데이터·로그·저장은 읽기 전용으로 취급했다. 커밋·푸시·게시·업로드는 이번 요청에 포함하지 않는다.

## 설치와 실제 실행 구성

| 항목 | 이번에 확인한 기준 |
|---|---|
| 설치 HOI4 | `Operation Postern 1.19.4.1.99a5`, Steam build `26282552` |
| 기존 실제 실행 체크섬 | `f584`; donor 실행이며 호환판 체크섬이 아님 |
| 활성 구성 | `mod/hearts of korea.mod` → `mod/Hearts of Korea English Translation Anime Modder's Edition.mod`; donor HOK와 일반판 영어 번역이며 호환판·RT56 대상 실행이 아님 |
| 활성 playset | `한국test01`; launcher SQLite와 `dlc_load.json`의 위 donor 구성을 구분해 확인 |
| 비활성 대상 playset | `Road to 56 한국 테스트`: enabled 위치 0 호환판(현재 root) → 1 RT56 Korean Translation `2769576030` → 2 RT56 `820260968`; donor 없음 |
| DLC | `disabled_dlcs=[]`; 실제 보유·인식 DLC와 각 기능의 작동 검증을 대신하지 않음 |
| OS·사용자 데이터 | Windows 11, `C:/Users/jaewo/OneDrive/문서/Paradox Interactive/Hearts of Iron IV` |
| 물리 원본·번역 | `C:/hoi/hearts_of_korea`; `C:/hoi/Hearts of Korea English Translation Anime Modder's Edition`, 번역 item `3823285419` |
| 언어·화면 | `l_korean`, GUI 배율 `1.0`, 기존 system 정보 `1280×720`; 이번 호환판 UI 관측이 아님 |
| 호환판 launcher | 이 호환판 root를 가리키며 기존 item `3796816200` 유지; 새 게시·원본 item 재사용 없음 |
| 언어·선언 | 기존 영어/한국어 계층과 RT56 + Korean Language 의존성 유지; 최종 대상 언어 조합은 별도 실행 대조 필요 |

launcher 목록의 순서는 기록된 구성이지 유효한 엔진 우선순위의 증거가 아니다. 위 대상 playset은 비활성이며 실제 실행 관측이 아니다. 대상의 RT56 Korean Translation `2769576030`은 descriptor에 선언된 Korean Language와 다른 모드이고 `replace_path="localisation"`을 사용하므로, 이번 정적 이식으로 최종 언어 계약이 해결되었다고 판단하지 않는다. 읽기 전용 launcher 인벤토리는 외부 `launcher-inventory.json`에 보존한다.

현재 활성 donor 실행을 호환판의 C0/C1 결과로 사용하지 않는다. 이번에는 게임 실행이나 사용자 실행 설정 변경을 승인받지 않았으므로 수행하지 않았다. 대상 검증은 donor를 제외하고 RT56와 이 호환판의 실제 파일을 로드하는 별도 전체 재시작이 필요하다.

## 선택한 병합과 동작

| 대상 | 통합 분류·선택 | 유지하는 내용 |
|---|---|---|
| 한국 중점 트리 | 기존 `OVERRIDE`에 선택 delta 적용 | 기존 472개 ID·배치·선행·기간·AI·보상, RT56 지도 참조 및 기존 포트 수정 유지. 신규 민간 핵 중점 두 개로 474개 |
| 한국 MIO 조직 | 기존 `THREE_WAY_MERGE`에 `add_trait` 15개 병합 | 공용 RT56 트리와 기존 접근 조건 유지. 특히 한진항공의 KOR/NKR 소유권 및 경기 통제 조건을 donor의 단순 `tag=KOR`로 되돌리지 않음 |
| 소양강 모듈 | HOK 전용 정의 `ADD`, 카테고리 아이콘·중점 안내 선택 병합 | 기존 카테고리와 이름 ID, 다른 원인의 공유 침수 수정치 보존 |
| 연구망·습격·세력 | HOK 전용 정의 `ADD`, 중점·사건 호출만 선택 병합 | 기존 보상·인물 ID·외교 사건과 창설국·이름 유지; 공용 시스템 미교체 |
| 훈장 | 기존 HOK 정의에 해군 효과·통합 경험치 추가 | 훈장 네 ID·육군 효과·그림·기본 비용 30 유지. 공통 경험치 100과 기존 일회 효과가 중복 지급되지 않게 donor의 변경 단위 유지 |
| 영문·한국어·그림 | 신규 HOK locale·sprite `ADD`, 선택 payload `ASSET_COPY` | 기존 번역과 키·BOM·헤더·기여자·자산 출처 보존; 기존 RT56 공용 그림 체계 미교체 |
| 한국·KCH/KJP/RKY 역사 교리 | `USE_RT56`에 맞춘 기존 포트 전환 보존 | `tools/migrate_doctrines.py`가 이미 적용한 현행 교리 구조를 유지. donor 역사 파일 전체를 덮거나 교리를 재지급하지 않음 |

소양강은 donor의 강원 주 `1029→1144`, 춘천 프로빈스 `13418→13539`를 기존 ADR-0002에 따라 변환한다. 경기 `525`와 서울 `7125`는 유지한다. 결정의 강조, 실제 댐 조회, 조건, 침수 적용·정리와 일일 dispatcher를 포함한 참조 전체에 같은 매핑을 사용한다. 연구망의 우선 배치도 해군 `1030→920`, 항공 `1029→1144`, 핵 `1028→918`을 적용하며 육군 `525`는 유지한다. 이는 기존 승인된 ID 이전의 참조 closure이며 새 지도·주·프로빈스 변경이 아니다.

수문 개방·정상화는 각각 정치력 25와 14일이 필요하다. 침수는 서울·춘천 두 타일의 전용 `HOK_KOR_soyang_flooded`로 한정하며, 건물 피해는 경기·강원의 기존 기반시설·민간공장·군수공장에 적용한다. 미존재 건물 보호 조건과 멱등 정리, 전쟁·소유·정확한 타일 통제·댐·한국 존속 조건을 보존한다. 공유 `flooded`를 제거하지 않으며 AI factor는 0이다.

MIO 특성은 기존 중점 13개를 통해 15개 조직의 구매 조건을 연다. AAT 조건의 툴팁은 무료 특성 지급이 아니며, 기존 부모·성장·특성 포인트 구매를 유지한다. 연구망 네 효과는 Götterdämmerung 조건에서 분야 시설의 중복을 막고 적합한 보유·통제 core 주를 선택한다. 기존 과학자에게 해당 분야 수준 +1을 일회 지급하며 다른 시설·분야나 기존 중점 보상을 제거하지 않는다.

RT56의 실제 generic MIO 파일 SHA-256 `02A80CAB1C40E5F8F4065F14A8D151795F896F134170D9ED16008D2DFDFB8AC0`과 최종 호환판 조직 파일 `5D6A7630565416E4777A6225900FA95E9C8703008D51AAD3F9549F76F8188300`에서 15개 parent/anchor 연쇄와 새 상대 위치를 독립 계산했다. 15개 모두 해석되며 각 조직 안의 기존 노드와 같은 중심을 쓰는 새 노드는 0개다. 새 위치는 donor 명세의 수치와 같았다. 외부 `C:/hoi/test/hok-rt56-feature-port-20261031/mio-host-coordinate-calculation.json`에 근거를 보존한다. 이 계산은 중심 중복만 검사하며 아이콘·이름판 외곽, 선 routing, 실제 특성 구매나 수치 적용의 증거가 아니다. RT56 공용 트리는 vanilla와 다르므로 donor의 vanilla 트리 검증을 호스트 검증으로 대신하지 않았다.

해병 급습은 Thunder at Our Gates 조건에서 해병대 창설 후 공개한다. 적 일본의 나가사키 프로빈스 `9950` 군항만 표적으로 삼으며, 해병 3개 대대·수송선 40·지휘력 40·120일 준비·1회성 조건과 원래 성공·손실·AI 구조를 보존한다. 네 세력 템플릿은 아시아 해방전선·아시아 연합·자유국가기구·동맹국의 기존 창설 지점만 사용한다. 일반 RT56 세력·창설국의 기존 세력을 일괄 교체하거나 이전 저장의 세력을 자동 이전하지 않는다.

민간 핵 가지는 서울대학교 확장 → 핵분열 연쇄반응 실험 → 민간 원자로 투자다. 첫 중점은 35일, 핵 혁신 `1.00`과 핵 기술 선행 연구 불이익 2년 감소 1회를 준다. 둘째는 `cost=35`의 기본 245일이며 핵 연구와 Götterdämmerung을 요구하고 `commercial_nuclear_reactor_tech`를 지급한다. 기술 기보유 bypass·조건 상실 취소를 보존한다. 5일 감산은 최종 donor 소스에서 제거되었으므로 이식하지 않는다. 기본 합계는 280일이며 일반 핵 기술·프로젝트 완료·시설·과학자·완성 건물을 자동 지급하지 않는다. [별도 배치 명세](../HOK_KOREAN_FOCUS_LAYOUT_COORDINATES.md)를 따른다.

## 자산과 출처 경계

신규 핵 중점 그림은 donor가 기록한 AI 생성 원본과 DDS를 선택 재사용하며 이번 이식에서는 새 그림을 생성하거나 색상을 바꾸지 않는다. MIO·수문·세력·습격의 선택 vanilla 자산은 Paradox Interactive 출처·원본/최종 해시·같은 게임 모드 안에서의 재사용 기록을 유지한다. HOK 원작·donor 개발·포트 통합·RT56/vanilla 기여를 구분하고 새 저작권이나 라이선스를 주장하지 않는다.

donor 명세·manifest의 과거 버전·`runtime_pending` 등 상태는 그 출처의 작성 시점 기록이다. 이를 호환판 결과로 바꾸거나 역사 문서를 재작성하지 않는다. 현재 생산 출력의 출처·해시와 호환판 검증은 이 문서 및 이번 잠금에서 따로 관리한다.

donor의 영어 함장 fallback 파일에는 한국어 본문인 공용 키 13개가 있으므로 그대로 이식하지 않는다. 원래 영어의 공용 함장 UI 키는 호스트·게임의 해당 계층을 사용하고, 이번 HOK 전용 신규 영어는 기존 포트의 영국 영어 기준에 맞춰 연결한다. 네 역사 교리 파일과 이 fallback의 제외 사유를 이번 잠금에 남긴다.

## 정적 검증과 기존 오류

검증·임시 도구·보고서는 `C:/hoi/test/`의 이번 전용 경로에 두고 저장소에는 재현에 필요한 감사된 generator 입력과 유지 관리 문서만 남긴다. 범위 검사는 기존 레이어의 정확한 보존과 역적용, 추가 정의·조건·효과·DLC gate·ID 이전·locale·sprite·payload 연결을 분리한다. 순서 있는 구문 검사는 등록·실제 scope·런타임 호출을 증명하지 않는다.

2026-10-20 기록의 전체 validator는 20 PASS / 0 WARNING / 5 ERROR였다. 당시 소스 drift 네 개와 material-cycle 보존 목록의 `descriptor.mod` 바이트 핀 한 개는 그 시점의 이력이다. 이번에는 immutable `e871bd1`의 기존 도구로 실제 업데이트 전 소스를 다시 검사해 **18 PASS / 0 WARNING / 7 ERROR**를 확인했다. 현재 설치 1.19.4 소스 기준의 map 전체·Korean buildings·공용 override·동아시아·교리 drift 다섯 개, 기존 descriptor 핀 한 개, 통합 원장의 기존 README 출력 해시 불일치 한 개다. README 차이는 원장의 옛 `7AA670…`와 실제 checkout `6221D3…`로 분리해 외부 기록에 보존했다.

새 기능의 출처·출력과 README를 포함해 통합 원장을 재생성했다. 이전의 지도·공용 시스템·교리 소스 핀과 descriptor 보존 검사는 바꾸지 않았다. 호스트 전체를 재고정하거나 이전 검사를 느슨하게 하여 기존 오류를 숨기지 않았으며, 새 범위의 정적 결과와 전체 잔여 오류를 구분한다.

| 실제 정적 검사 | 결과·경계 |
|---|---|
| 이번 source snapshot | 런타임 텍스트 30개·자산 28개·출처 기록 51개 통과 |
| 생성 출력·역적용 | 최종 런타임 출력 58개 고정·기존 수정 파일 다섯 개의 정확한 ancestor 복원 통과 |
| 신규 기능 의미 검사 | 474개 트리, 핵 35/245일·보상, MIO 15개·기존 RT56 접근 보존, 연구망 주 매핑, 수문·습격·세력·훈장·그림 연결 통과 |
| 기존 expansion·civic·shipbuilding 검사 | 이번 계층을 역적용한 뒤 각 기존 계약 통과; 이전 source pin·descriptor 검사를 삭제하지 않음 |
| 통합 원장 재생성 | 1,505행, 같은 호스트 상대경로 충돌 73개 유지; 기존 1,452행 중 해당 수정 5개는 사유·출력 해시만 갱신, README는 출력 해시만 갱신, 신규 53행 추가 |
| 독립 최종 소스 감사 | 기존 수정 파일 5개·추가 53개로 58개 출력 확인, 자산 28개 원본과 바이트 일치·locale BOM 보존·무관한 tracked runtime 변경 없음 |
| 독립 배치 계산 | 기존 472개 배치·선행·배타·기본 위치 보존, 신규 두 개·전체 474개; MIO 추가 15개 해석·기존 중심과 중복 0개 |
| 전체 구조·현지화 | UTF-8 script 216파일 brace 검사, locale 85파일·5,627키의 BOM·헤더·키 유일성 및 논리 ID 검사 통과 |
| 전체 aggregate validator | **20 PASS / 0 WARNING / 6 ERROR**; 신규 feature·출처·생성·영어·기존 expansion/civic/shipbuilding·원장 gate 통과, 새 실패 없음 |

외부 `feature-check.txt`, `expansion-check.txt`, `civic-check.txt`, `shipbuilding-check.txt`, `generation.txt`, `manifest-generation.txt`와 `final-validation.txt`는 `C:/hoi/test/hok-rt56-feature-port-20261031/`에 둔다. 이 표는 소스·정적 계산의 통과이며 엔진·UI·정상 진행 결과가 아니다.

최종 여섯 오류는 map synthesis, Korean building placements, shared overrides, East Asia overrides, doctrine migration의 기존 소스 해시 drift 다섯 개와 second-wave material-cycle의 `descriptor.mod` 보존 해시 한 개다. 시작 시점 일곱 번째였던 stale README 원장 해시는 이번 출처·출력을 정상 반영하면서 해소했다. 원장의 기존 행 변화는 외부 `ledger-audit.json`, 런타임 수정 범위·자산·인코딩은 `output-audit.json`에 별도로 보존한다. 이 결과는 이번 이식 범위의 정적 검증 통과이며 전체 포트의 정적 통과나 새 게임 실행 가능 판정이 아니다.

마지막 donor 확인은 작업 트리 깨끗한 `07de265c1e992abb6584bdfcdf140320188c07f9`다. 소스·출력·병합 범위를 확인했으며 donor의 검증 결과를 포트 실행 결과로 바꾸지 않았다.

## 실행 증거와 남은 검증

호환판의 이번 게임 실행·UI·정상 진행·저장 결과는 **UNPROVEN**이다. donor의 검사 수나 HOK-only 실행을 포트 통과로 합산하지 않는다.

- donor MIO는 합성 준비 상태에서 15개 특성의 실제 구매·비용·저장과 프로세스 재시작 후 유지가 관측됐다. 정상 중점·성장 순서, 장비·생산 실제 수치, AI·DLC 미보유·임의 옛 저장·멀티플레이는 별도다.
- donor 수문은 보호 조건 전 소스에서 일반 14일 개방·정상화를, 보호 조건 후 소스에서 강제 효과 회귀를 확인했다. 최종 조건의 일반 반복과 정확한 대상 타일 상실·종전·항복·병합·댐 상실 정리, 중도 취소·재로드는 별도다.
- donor 핵 가지의 이전 5일 감산 소스에는 정상 240번째 일일 진행·기술 지급·건설 대기열·재로드 관측이 있다. 최종 245일 무감산과 후속 2년 연구 혜택은 정적 대조만 수행했으므로 이식 후 정상 기간·표시·소비를 검증해야 한다.
- 함장 훈장·보상, 연구망의 배치·중복 방지·과학자 일회 성장, 실제 급습의 생성·비용·준비·결과, 세력 목표·가입/추방/지도권과 기존 외교 흐름도 대상 RT56 실행에서 확인해야 한다.
- 새 중점의 잠김·사용 가능·활성·완료·shine와 이름판·연결선·SHOW/HIDE, 실제 언어 구성, DLC 분기·AI·장기 진행·기존/신규 저장·멀티플레이는 실행한 범위만 판정한다. 신규 보상의 자동 소급이나 임의 기존 저장 호환을 약속하지 않는다.

현재 작업은 작업 트리 변경으로 남긴다. 커밋·푸시·Workshop 게시·업로드는 수행하지 않는다.
