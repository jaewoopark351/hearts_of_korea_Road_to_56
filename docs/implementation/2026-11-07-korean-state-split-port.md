# 2026-11-07 한국 15주 분할과 연결 콘텐츠 이식

상태: **이번 47출력 이식의 구현·범위 검증·환경 복구 완료**(2026-11-08 KST). 최종 suite는 **190 PASS / 0 MISMATCH / 10 UNVERIFIED**이며 아래 미검증·기존 정적 오류·출시 제약을 포함한다. 모든 게임플레이나 출시 준비 완료를 뜻하지 않는다. 사용자가 [전체 이식 계획](../plans/2026-11-07-korean-state-split-port-plan.md)의 구현을 승인한 뒤 적용한 기록이다. 원본의 실행 결과와 RT56 단독 결과는 이 포트의 실행 결과로 사용하지 않는다. 아래 실행 절에서 대조·45출력 C0·후속 47출력을 구별한다.

## 기준선과 먼저 읽을 기록

| 다음 작업 조건 | 필요한 기록 |
|---|---|
| 분할 구현을 수정하거나 회귀를 판단할 때 | [ADR-0006](../decisions/0006-korean-state-split-integration.md)의 ID·영토 집합·보상·호스트 소유권 결정과 [포트 대응표](../data/HOK_KOREAN_STATE_SPLIT_PORT_MAPPING.json) |
| 동결 입력·출력 해시를 검증하거나 생성기를 재실행할 때 | [입력 보관본 안내](../upstream/hok-state-split-20261107/README.md)와 [분할 잠금](../../tools/hok_state_split_lock.json). HEAD만으로 미커밋 원본 입력을 복원하지 않음 |
| 기존 지도 이전·만주 통합과 결합할 때 | [ADR-0002](../decisions/0002-map-id-migration.md), [ADR-0005](../decisions/0005-korean-second-wave-regional-integration.md). 분할 밖의 ID·영토 조건은 유지 |
| 기존 캐시나 과거 자료의 경로를 해석할 때 | [개발 자료 안내](../HOK_DEVELOPMENT_ARTIFACT_ARCHIVE.md). 세 활성 source cache와 이번 시험 디렉터리를 구별 |
| 새 실행을 시작하거나 검증 범위를 확대할 때 | [이식 계획의 검증 계약](../plans/2026-11-07-korean-state-split-port-plan.md#9-검증-계약--모두-향후-계획)과 [프로젝트 지침](../../AGENTS.md). 실제 설정·모드 선택을 백업하고 시험 후 복구 |

| 항목 | 이번 구현의 기준 |
|---|---|
| 호환판 | `C:\hoi\hearts_of_korea_Road_to_56`, `feat/korean-focus-update-20260922@3d9355b70152794ed974dcf183323c24206d900a`. 앞선 계획·문서 인덱스 변경을 보존 |
| donor | 읽기 전용 `C:\hoi\hearts_of_korea`, `feat/korean-focus-expansion-ai@0d73d49726abbfa435c73f1bf8cc24d4a5af014b` 위의 미커밋 6도 분할. 선택 입력 42개를 동결 |
| 엔진·호스트 | 설치 HOI4 `Operation Postern v1.19.4.2.2da5`, Steam build `26409260`; RT56 `820260968`, manifest `7553774178744855191`. 메타데이터 체크섬은 새 실행의 체크섬이 아님 |
| 정체성 | 호환판 Workshop ID `3796816200`과 기존 RT56/Korean Language 선언 유지. donor `3793992662`·역사적 HOK `2898629778`·RT56 `820260968`은 업로드 대상이 아님 |
| 원본 및 호스트 보호 | donor·Steam Workshop·게임 설치는 읽기 전용. 이번 입력 복사본·개발 소스와 외부 시험 자료를 별도로 유지 |
| 실행 구성 | 이전 기록의 `Road to 56 한국 테스트`, RT56 한국어 번역과 선언된 Korean Language의 차이를 현재 실행 증거로 갈음하지 않음. 새 실행의 물리 경로·DLC·언어·유효 구성을 아래 별도 기록 |

## 적용 범위와 수치

현재 생성 계층은 **런타임 47개 경로**다. donor 변경 42개와 포트 추가 변경 5개로, `events/WTT_PRC.txt`, `events/r56_japan.txt`, 기존 쓰시마 이름 키 수선, 기존 연구망 한영 툴팁 파일 2개가 추가 변경이다. 원본 파일 수와 포트 출력 수는 같은 집계가 아니다. 일반 C0는 연구망 문구 보완 전 **초기 45출력**으로 실행했다. 45출력의 해시·정적 검사·실행 관측을 47출력의 최종 통과로 확대하지 않는다.

그중 **신규 런타임 경로 9개**는 한국 주 6개, 한영 주 이름 파일 2개, `common/national_focus/japan.txt`다. 일본 중점은 현재 RT56 파일을 기반으로 한국 연결만 병합한 새 override이며 donor 일본 중점 전체를 복사하지 않았다. 나머지 **38개는 기존 호환판 경로**의 변경이다. 연구망 한영 파일은 새 경로가 아니며 표시 참조만 보완했다. 전체 경로·출처·해시는 분할 잠금의 `outputs`에 있다.

| 옛 donor → 기존 포트 | 기존 ID가 맡는 후속 도 | 신설 donor → 포트 |
|---|---|---|
| `1030 → 920` | 경상북도 `920` | 경상남도 `1086 → 1148` |
| `1031 → 1145` | 충청남도 `1145` | 충청북도 `1087 → 1149` |
| `1082 → 919` | 전라북도 `919` | 전라남도 `1088 → 1150` |
| `527 → 527` | 평안남도 `527` | 평안북도 `1089 → 1151` |
| `1028 → 918` | 함경남도 `918` | 함경북도 `1090 → 1152` |
| `1083 → 917` | 황해남도 `917` | 황해북도 `1091 → 1153` |

설치 RT56의 주 ID와 대조해 신설 `1148–1153`을 정했다. donor의 `1086–1091`은 RT56 외국 주와 충돌하므로 그대로 쓰지 않는다. 기존 province 이전 `13414–13447 → 13535–13568`은 유지한다. 새 province·색·비트맵·해안선은 만들지 않는다. 쓰시마·나가사키는 한국 9→15 집계에 포함하지 않는다.

한국 인구 `25,899,038`, 시작 민공·군공·조선소 `9·4·1`, 부모별 원자원·승점·고정 공장 총량을 보존했다. 기본 카테고리 슬롯 합은 `33 → 57`, 시작 기반시설 레벨 합은 `14 → 23`이다. 부모 카테고리와 기반시설을 양쪽에 유지하는 의도된 변화이며 게임플레이 완전 동일을 뜻하지 않는다. 공유 슬롯 25·유형별 20 등 전역 제한과 시작 공장 증설은 변경하지 않았다. 소스 산술과 엔진 getter·기술 적용 후 가용량을 구별한다.

12개 후속 주는 `HOK_KOR_STATE_<donor ID>` 논리 키를 사용한다. 숫자 접미사를 실제 포트 ID로 일괄 변환하지 않는다. 한글 지명과 실제 영어 North/South 지명을 새 한영 파일에 연결했으며 기존 전역 `STATE_*` 별칭은 보존했다. 별도 확인된 쓰시마 `1147`의 `name="STATE_1088"`만 이미 존재하는 `STATE_1147`로 맞췄다. 전남 신설 키와 혼동하지 않는 좁은 표시 참조 수선이며 새 저장 마이그레이션이 아니다.

후속 47출력은 기존 `HOK_KOR_research_network_l_english.yml`·`_l_korean.yml`의 해군·핵 연구망 설명에서 우선 주 이름 참조만 명확히 했다. 해군 `$STATE_920$ → $HOK_KOR_STATE_1086$`는 실제 우선 주인 경남 `1148`, 핵 `$STATE_918$ → $HOK_KOR_STATE_1028$`는 함남 `918`을 표시한다. 기존 4키·조건·시설 수·fallback·과학자 보상을 유지한 표시 보완이며 donor 변경에 포함된 새 게임플레이가 아니다. 영어 출력 SHA-256은 `19A3F7547811E2945C5B69A563B67F627FB0ECFA6973D7C4106950DF07098C06`, 한국어는 `722645B04632E29C7ED1A4A8C6A3225573E9ED9ACD68B08D112F1C4849D79DCE`다.

## 한국 콘텐츠와 공유 연결

- 474개 중점 ID·선언 순서와 배치·선행·상호 배타·비용·AI·아이콘을 보존했다. 23개 중점의 지역 조건과 보상 대상만 변환했다. 대구 수도 중점은 기존 프로빈스와 경북을 유지한다.
- 옛 도 전체의 소유·통제 조건은 양쪽 AND, 주 후보 집합은 OR, 어느 한쪽 상실로 취소하는 조건은 실패의 OR다. 슬롯·해안·기지 수용량은 실제 보상 대상에서만 검사한다.
- 포항 강철 +25와 반복 +9는 경북, 부산·남동임해 산업은 경남, 운산 민공은 평북, 함경 강철 +15는 함북·텅스텐 +5는 함남에 연결했다. 도별 슬롯·기반시설·신도시 인구 이동·예비군의 기존 총량을 복제하지 않고 배분했다.
- 지역 투자와 포항 사업은 양쪽 영토를 검사한다. 포항의 PP25·민공9·90일·반복/취소 규칙과 산업 투자의 PP150·민공 미점유·90일 규칙을 유지했다. 영어 산업 투자 설명 세 키에는 실제 수혜 도와 양쪽 영토 상실 규칙만 반영했다.
- 한국 전체 15·북부 6·남부 9·제주 제외 14를 구별한다. 함경남도·황해남도는 북부다. SEA 내전의 북부+경기 7주와 다른 남부 8주를 유지했다. 한국 `kor_events.2`는 양쪽 경상과 제주를 제외한 한국 12주, `kor_events.3`은 경기와 제주를 제외한 13주이며 기존 만주 목록도 보존했다.
- 일본의 기존 경기·평안 판정은 경기·평남·평북으로 확장했다. 소련 국경분쟁은 함북으로 옮기면서 선택·표시·병력·attacker·flag·event target·확전·철회·후속 이벤트·정리를 함께 이전했다. 1939 일본 이력은 15주에 적용하되 host의 compliance/resistance 설정을 유지했다.
- 중국 전쟁목표 generator는 평남+평북으로 넓히고 평남 CONTROLLER 선정·중복 방지 proxy는 보존했다. 후속 주의 controller가 다른 경우를 새로운 다중 상대 외교 설계로 확장하지 않았다.
- 두 국뽕 옵션, 한국 AI buffer, KOR core 회복, 강화 AI와 공군 BBA/legacy를 함께 이전했다. 업적은 전북 한 주의 기존 기반시설 조건과 ID를 유지한다. 일반 국뽕 공군 OOB 두 개는 이번 donor diff에 없지만 기존 경기·평남 배치의 유효성을 감사했다.
- 전라 CAS는 전남, 중견국 경상 기지는 경남으로 옮겼다. 연구망의 해군 우선지는 경남으로, 핵 우선 함남과 분야별 단일 배치·fallback은 유지했다. 소양강의 경기·강원·서울·춘천 범위는 확대하지 않았다.

공유 연결 13개는 [공유 변환 모듈](../../tools/korean_state_split_shared.py)의 명시적 allowlist만 대상으로 한다. 일본·중국·공용 시스템의 일반 내용은 현재 RT56/vanilla 기반으로 남긴다. 과거 전체 생성기의 지문 실패를 없애려고 기존 핀을 변경하지 않았다.

## 지도·생성기·입력 소유권

[분할 생성기](../../tools/korean_state_split.py)는 12개 후속 주 출력, 건물 배치, 한국 콘텐츠 16개, 새 현지화 2개, 공유 연결 13개, 쓰시마 키 수선과 기존 연구망 현지화 2개를 한 최종 계층으로 재현한다. 한국 콘텐츠와 공유 변환은 별도 모듈이 담당한다. 기존 focus/map/ID/shared/East Asia 생성기는 정확한 이전 출력 또는 검토한 현재 호스트 중간 출력만 최종 계층에 넘길 수 있다. 과거 검사는 잠금으로 확인된 최종 바이트만 이전 호환판 바이트로 투영하고, 기존 핀·AST·변형 거부 조건을 유지한다. 최종 분할 자체는 실제 출력 바이트를 읽는 별도 gate로 검사한다.

`outputs[*].host_base_sha256`는 `host_provider`가 지목하는 **설치 RT56/vanilla 물리 파일**의 해시다. `host_intermediate_sha256`는 그 파일에 기존 HOK 호환 연결을 적용한 **메모리 중간 출력**이며 물리 호스트 해시가 아니다. 최종 `sha256`와 이전 작업 트리 `previous_sha256`도 각각 별도다. `current_inputs`는 1,193개 물리 입력을 고정하고, `compat_inputs`는 45출력 당시 46개에서 연구망 이전 파일 2개를 더해 **48개**다. 그 수량은 출력 47개와 다르다.

각 자식의 RT56 `state_victory_points` hook은 실제 자식 VP만 담는다. 주 파일 줄바꿈은 기존 부모 형식을 따르며 줄바꿈 정렬 전후의 정규화 내용이 같음을 별도 확인했다. 지도 비트맵·province 정의·철도·보급·unitstack 등 분할 외 지도 바이트는 유지한다. 건물 배치는 기존 호환판 한국 행을 새 부모에 연결하고 비한국 행은 현 RT56에서 보존한다. 기존 항구 spawn 복원과 기지 위치 규칙을 유지하며, 새 표시 앵커를 실제 공장 지급으로 해석하지 않는다.

추가 표시 앵커 중 donor 함북 산업 표시의 X `4834.00`은 보존한 RT56 지도에서 외국 province `944`/state `942`를 가리켰다. 같은 의도된 한국 province `6944` 안의 X `4836.50`으로 `2.5`픽셀 이동했다. 원본 입력은 그대로 보존하고 포트 출력의 이 한 좌표 적응을 `map_adaptations`에 기록했다. 이는 실제 화면 위치 확인을 대신하지 않는다.

### 추가 필드 감사에서 발견한 생성기 결함

초기 7,170개 소스 검사가 통과한 뒤의 별도 읽기 감사에서 건물 표시 행의 검사 공백을 찾았다. 새 표시 앵커를 찾는 전후 비교가 부모 ID만 바뀐 기존 209행까지 신규 행으로 볼 수 있었고, 범용 숫자 재출력이 ID가 아닌 소수 필드의 표기까지 정규화할 수 있었다. 따라서 초기 통과를 모든 건물 필드 보존의 증거로 삼지 않는다.

후속 수선은 행의 부모를 제외한 나머지 payload의 multiset으로 기존 행과 **실제 신규 172행**을 구별한다. 그중 경북의 기존 선호 공군/로켓 위치와 중복되는 신규 후보 2개를 제외해 170개를 선택했다. 기존 한국 배치 546행은 ID 필드 밖의 바이트를 보존했다. 건물 행은 state인 첫 필드와 sea-link인 일곱째 필드만 명시적으로 이전하며 좌표·회전·높이·소수 자릿수는 그대로 보존한다. 한국 콘텐츠의 숫자 변환도 매핑 대상이 아닌 토큰은 원래 문자열을 반환하고 소수 내부를 ID로 해석하지 않도록 제한했으며 실제 콘텐츠 16개의 출력은 이 방어 수선으로 바뀌지 않았다.

기존 RT56 경상 공군/로켓 위치가 모두 경북에 있어 경남 `1148`에 필요한 두 표시 위치는 donor의 기존 행에서 별도로 복원했다. `1086;air_base;4810.00;11.45;1239.00;4.32;0`과 `1086;rocket_site_spawn;4817.00;9.90;1237.00;4.79;0`의 부모만 `1148`로 이전한다. 원본의 정확한 한 행 존재·실제 경남 육지 소속·주별 기지 유일성을 검사하는 두 행 한정 예외다. 이 두 행을 근거로 원본의 재부모화 209행이나 다른 과거 제외 배치를 일괄 복원하지 않는다. 새 건물 수 지급도 아니다.

수선 전후 출력의 필드 비교는 `peer-final-anchor-and-content-review.json`, 최종 독립 검사는 `validation/independent-production-final-result.json`에 구별해 남겼다. 최종 7,180개 검사에는 실제 source 신규 172행의 비ID 필드와 제외/적응 사유가 포함된다. `validation/negative-input-checks-final.json`의 회전/부호 필드·province·인구·자원 변형 사본 4개는 모두 예상대로 거부됐다. 초기 7,170/0을 이 확장 검사나 엔진 통과와 동일시하지 않는다. 건물 수선과 최종 소스/필드 확인은 첫 엔진 대조 실행 전에 수행했다.

## 실제 수행한 정적 확인

| 확인 | 이번 결과와 한계 |
|---|---|
| 적용 전 전체 검사 | 외부 `static-before.txt`: **17 PASS / 0 WARNING / 11 ERROR**. 과거 vanilla/RT56 지문, descriptor 보존 핀 등의 기존 부채. 분할 결과가 아님 |
| 초기 45출력 최종 전체 검사 | 외부 `static-final.txt`: **19 PASS / 0 WARNING / 11 ERROR**. 신규 범위 gate 2개가 추가됐고 오류 항목 11개는 적용 전과 동일. 과거 핀·descriptor 부채는 미해결. 후속 47출력의 재검사와 구별 |
| 최종 47출력 전체 검사 | 외부 `static-final-47.txt`: **19 PASS / 0 WARNING / 11 ERROR**. English translation import와 state-split provenance 모두 PASS이며 적용 전과 같은 기존 11개 오류 항목 유지. 후속 연구망 표시 참조를 포함한 실제 47출력의 결과 |
| 기존 오류의 독립 대조 | 외부 `final-static-error-classification.md`: 초기/최종의 11개 gate명·exit·경로·캡처된 오류 본문·표시된 hash가 동일. `source_snapshot` traceback 줄 번호만 `1405 → 1423`. subprocess tail만 대조했으므로 전체 drift 목록의 동일이나 출력되지 않은 launcher/descriptor 실제 hash의 동일은 입증하지 않음. 새로운 실패 gate 0이지만 기존 11개 부채는 미해결 |
| 초기 독립 지도·소스 검사 | `validation/independent-production-result.json`: **7,170 PASS / 0 FAIL**. 실물 출력의 주·province·총량·VP/건물·유효 참조 등 한정된 소스 계약. 이후 발견한 건물 소수 필드/신규 앵커 분류까지 완전하게 검증했다는 뜻은 아니며 엔진 검증도 아님 |
| 초기 45출력 최종 독립 지도·필드 검사 | `validation/independent-production-final-result.json`: **7,180 PASS / 0 FAIL**. 신규 172개 표시 행의 원문 필드와 기존 배치/호스트 보존까지 확장. `negative-input-checks-final.json`의 외부 변형 4개 전부 거부. 실제 건물 화면·엔진 평가의 증거는 아님 |
| 공유 의미 검사 | `shared-semantic-checks.json`: **42 PASS / 0 FAIL**. 영토 집합·중국 proxy·일본 이력/건설/분쟁 등 한정된 소스/조건 검사 |
| 한국 콘텐츠 재생·역변환 | `content-probe.json`: 16개 모두 동결 입력 재생과 실제 출력 일치, 역변환의 이전 바이트 복원 |
| 중점 보호 필드 | `content_focus_semantics.json`: 474개 ID/순서 유지, 변경 23개. `available`·`completion_reward` 밖의 순서 있는 필드 동일, 대구 수도 중점 유지 |
| 이전 기능 회귀 | `historical-first-wave*.txt`, `historical-civic.txt`, `historical-shipbuilding.txt`: 중점/아이콘/참조, 22개 변형 거부, 시민사회 31출력, 조선 9출력 통과 |
| 언어·ID 이전 | `historical-english.txt`: 기존 번역 수량과 추가 12개 HOK 주 이름 별도 통과. `historical-migrate-list.txt`: 18파일 목록, 실제 기록 변경 0. 기존 5개 newline 정렬 후보는 변경하지 않음 |
| 역사적 실패 유지 | `historical-second-wave.txt`의 descriptor 보존 핀, `historical-feature.txt`·`historical-layout.txt`의 과거 `launcher-settings.json` 지문 실패. 기존 핀을 느슨하게 하지 않음 |
| 통합 원장 범위 | 현재 47개 출력의 출처·분류를 잠금과 연결. 연구망 두 기존 경로를 추가한 현재 CSV SHA-256은 `A36C138B7CD70371928DC33CBE978B04707E5AAF05058C957733FB2E0CDC408B`. 관련 없는 원장 행과 독립된 host 물리/중간 해시를 구별 |
| 실행 중 선택 소스 재지문 | 외부 `independent-final-source-fingerprints.json`: live donor 42/42, RT56 1,166/1,166·vanilla 27/27(총 1,193), 동결 donor before 34/34·after 42/42·compat 48/48 일치. 실제 출력 47/47과 CSV 대상 47행·위 SHA-256 일치. 설치 및 details RT56 manifest 모두 처음의 `7553774178744855191`, Steam build `26409260`, Git HEAD와 잠금도 유지. 불일치 0. 미선택 설치 파일 전체의 불변 또는 엔진 동작을 주장하지 않음 |
| 실행 종료·복구 후 선택 소스 재지문 | 외부 `post-runtime-source-fingerprints.json`: 2026-11-08 01:47 KST 감사에서 위 live donor42·물리 RT561,166/vanilla27·동결 compat48/before34/after42·런타임47·원장 대상47의 일치와 drift0 확인. Steam build `26409260`, RT56 manifest `7553774178744855191` 유지. 정상 suite 종료·복구 뒤이며 지도 보호 도구만의 후속 수정 전 관측. 이후 core/변형 검사를 대신하지 않음 |
| 지도 보호 수선 뒤 사후 core·원장 확인 | 외부 `post-runtime-core47-check.txt` exit0: 결정적47출력·한국15주·충돌 없는6신규ID·입력 계층 보존 PASS. `post-runtime-ledger-check.txt` exit0: CSV 위 `A36C…408B` 해시 유지·관련 없는 역사적 행 byte 보존. 전체 aggregate를 다시 통과시킨 결과는 아님 |
| buildings-only 최종 동반 파일 보호 | 외부 `validation/buildings-only-final-guard/results.json`: **5/0**. 완전한 최종 지도에서 건물만 쓰는 양성1개·신설 주 누락/변형/부모 구버전의 쓰기 전 거부3개·전체 지도에서 신규6주 유지 양성1개. 실제 build_all/finalize/validator/guard/writer를 사용해 외부 파일 변화를 확인. 과거 source 합성 부분만 검증된 동결 중간 입력으로 격리했으므로 전체 legacy CLI 재생이나 과거 source-pin 통과로 확대하지 않음. 실제47출력·tools JSON 핀은 전후 동일 |
| 공유 파일 공백 검사 한계 | 외부 `shared-whitespace-comparison.md`: `git diff --check -- events/SEA_Japan.txt events/r56_japan.txt`는 exit 2, 공백 진단 56건. SEA의 space-before-tab 14건과 r56의 줄끝 공백 42건은 모두 원래 host/동결 템플릿의 들여쓰기·접미사를 새 행에 보존/복제한 결과. 새 문자열 값이나 gameplay/syntax 결함을 확인한 것이 아니지만 공백 검사를 클린 PASS로 기록하지 않음. 별도 formatting 정리는 하지 않았음 |

중간 `static-after.txt`의 18 PASS / 13 ERROR 중 2개는 영토 검사기가 새 중첩 AND를 인식하지 못한 오탐이었다. 검사 대상은 AND 하위로만 엄격하게 재귀하도록 수정했고 OR/NOT를 통해 실제 영토 조건을 완화하지 않았다. 최종에는 이 두 오탐이 없어졌고 신규 분할 gate 두 개를 통과해 19/0/11이 됐다. 나머지 기존 오류 11개를 핀 수정이나 검사 생략으로 없애지 않았다.

검사 항목은 서로 겹치는 사실을 확인하므로 위 수치를 합산한 독립 기능 수로 발표하지 않는다. 정적 통과만으로 실행·UI·저장·DLC·멀티플레이 통과를 주장하지 않는다.

## 증거·소스의 위치와 남은 정리

동결 입력은 `docs/upstream/hok-state-split-20261107/`의 유지 관리용 출처 사본이다. `runtime/`는 donor 변경 42개, `before/`는 존재하는 donor HEAD 이전 입력, `compat_before/`는 포트 이전 입력, `documents/`는 원본 설계·배분·원본 검증 기록이다. 이들은 시험 산출물이 아니다. 원본은 donor/설치본/이전 호환판이며 이 보관본은 재현을 위한 사본이다. 자세한 해시·역할은 [입력 안내](../upstream/hok-state-split-20261107/README.md)를 따른다.

이번 모든 helper·백업·보고서·프리뷰·로그 사본·실행 준비 자료는 **`C:\hoi\test\hok-rt56-state-split-20261107-01\`**에 둔다. `backups/compat/`는 초기 비교 사본, `preview/`·`shared-preview/`는 적용 전 후보, `validation/`은 독립 검사와 외부 시험 fixture, `profile/`은 승인된 실제 프로필 시험의 백업/관측 경로다. fixture 준비는 게임 실행 성공이 아니다. 게임이 생성하는 로그·저장 원본은 실제 user-data에 남기며 증거 사본과 구별한다.

기존 `tools/__pycache__/` 21개·1,088,888바이트(약 1.04 MiB)는 정리 대기 캐시이며 이번 범위에서 이동·삭제하지 않았다. 기존 활성 입력 `C:\hoi\test\hok-rt56-source-cache\sources\` 세 트리는 유지했다. 캐시나 donor의 과거 시험 결과를 이번 포트의 실행 증거로 합치지 않는다.

## 실제 실행 결과

**R0·초기 45출력 C0·47출력 C0-02·한국어 C1·국뽕 두 옵션과 final v5 suite를 종료·수집하고 범위 평가를 마쳤다.** 실제 프로필의 임시 모드 선택·설정 변경을 별도로 승인받아 사전 백업 후 실행하고 원래 설정을 복구했다. 날짜를 생략한 시각은 2026-11-07 KST이며 자정 뒤 관측은 2026-11-08 KST로 구별한다. 외부 `runtime-evidence-index.json`은 실행·관측·증거 사본의 위치 인덱스이며, 최종 suite의 개별 결과·해시·복구와 미검증 범위는 `validation/runtime-evaluations/suite-final-validation-summary.json`에 연결했다.

| 실행 | 실제 구성·시각 | 확인한 결과와 한계 |
|---|---|---|
| R0 | PID `27604`, `22:30:34` 시작. RT56 단독, 영어, DLC 36개, HOI4 `1.19.4.2.2da5` | 13,535 province 로드. 실제 UI의 1936년 1월 1일 12시에서 1월 3일 17시까지 진행한 뒤 정상 UI로 종료했다. `profile/runs/r0/evidence.json`과 해당 `logs/`에 수집했다. 새 저장 0개, 원래 저장 43개 변경 없음. 이 결과는 host 대조이며 분할 포트 통과가 아님 |
| C0 — 초기 45출력 | PID `24272`, `22:40:00` 시작·약 `22:55` 정상 종료. 호환판+RT56, 영어. donor·fixture 없음 | 13,569 province와 한국 1936 지도 진입을 확인했다. 실제 UI에서 1월 23일 08시까지 진행하고 새 저장 사본을 수집했다. `profile/runs/c0/evidence.json`과 `logs/`, `post-game/`에 보존했고 원래 저장 43개는 변경되지 않았다. 아래 관측과 미검증 범위를 구별 |
| C0-02 — 후속 47출력 | PID `27332`, `22:59:16` 시작. 영어, 호환판+RT56만 활성 | 메뉴에서 `KOR_1936_01_23_08x_temp.hoi4`를 선택해 Load → Start로 진입했다. 1월 23일 08시 상태와 후속 이벤트 복원을 확인한 뒤 1월 27일 02시까지 진행했다. 이어 실제 새 게임 시나리오 화면에서 1936 카드만 있고 1939 카드가 없음을 확인했다. `profile/runs/c0-02/evidence.json`에 수집 완료, 원래 저장 43개 차이 0 |
| C1 — 최종 47출력 | PID `26900`, `23:10:56` cold launch. 한국어, 호환판+RT56+RT56 한국어 번역 | 한국 1936 지도와 한글 경남·포항제철 UI를 관측하고 1월 28일 21시까지 진행했다. 정상 Exit Game 후 PID 종료를 확인하고 `profile/runs/c1/evidence.json`에 수집 완료. 원래 저장 43개 차이 0. 수집된 새 저장 사본 1개는 이전 C0 저장의 재수집이며 C1에서 새 저장하지 않음 |
| 일반 국뽕 gook | PID `15440`, `23:22:02` 시작. 영어 1936, 실제 production 국뽕 옵션과 외부 진단 관측 | `validation/runtime-evaluations/gook-evaluation.json`: **30 PASS / 0 FAIL / 누락 증거 0**. production on_startup 뒤 1월 1일 13시·daily tick 7·daily tick 30의 세 관측에서 한국 15주 물리 민공·군공·조선소 합 `17·9·3`을 확인했다. 국가 전체 캐시/만주 포함 수치나 모든 UI·장기 AI 검증과 구별 |
| 중견국 middle | 영어 1936, 실제 production 중견국 옵션과 외부 진단 관측 | `validation/runtime-evaluations/middle-evaluation.json`: **30 PASS / 0 FAIL**. 초기·daily tick 7·daily tick 30의 한국 15주 물리 시설 합 `17·10·3`. 최종 UI 2월 3일 04시에서 종료·수집했고 원래 저장 43개 차이 0. 다른 옵션이나 suite 전체의 판정으로 확대하지 않음 |
| Final v5 suite | PID `29168`, **2026-11-07 23:56:41 KST** cold launch. DEFAULT KOR 1936, 영어, fixture+호환판+RT56 | 11월 8일 KST에 다섯 BASE 재로드·보상·양쪽 부분 상실·슬롯·반복2회·활성 저장 인게임 재로드의 아래 범위를 확인했다. 최종 v2는 **190 PASS / 0 MISMATCH / 10 UNVERIFIED**. 8월 28일 06시 저장 뒤 정상 종료·수집했고 원래 환경도 복구했다. 같은 프로세스의 분기이며 여러 cold launch로 계산하지 않음 |

현재 RT56의 `common/bookmarks/blitzkrieg.txt:3–4`는 1939 시나리오를 **지원하지 않는다고 명시**하며 파일 수정·삭제도 금지한다. 이 파일의 날짜는 `1939.8.14.12`, 이번 읽기 SHA-256은 `325D97BF530947CE6E07713CE5548DB07FD13DDBB90515661570424BBB3CDBD1`이다. C0-02의 실제 **Single Player → New Game → The Scenario** 화면도 **1 January 1936 카드 하나만 표시하며 1939 카드는 없었다.** 소스와 UI가 일치하는 구체적인 host 미지원으로 기록한다. 임의 bookmark/시작일·CLI 변경 없이 이 경로의 1939 실행 검증을 진행하지 않았다. 15개 한국 주의 1939 이력 보존은 정적 데이터 보존이며 지원되는 1939 시나리오를 입증하지 않는다.

R0의 독립 수집 로그/물리 소스 확인은 `validation/runtime-evaluations/r0-evaluation-complete.json`에서 **14 PASS / 0 FAIL**이다. C0·C0-02의 각 수집 평가도 **14/0**이며 로드·물리 입력 gate만 판정한다. R0 원시 오류는 2,081줄·정규화 고유 760개, C0는 9,634줄이다. `c0-r0-error-fingerprint-review.json`의 한정 대조에서는 새 정확 fingerprint 93개 중 알려진 GXC/중국 인물 scope 계열 밖의 항목은 `continue_game`과 새 저장의 rename 실패 2개였다. R0는 GER/1월 3일 17시, C0는 KOR/1월 23일 08시여서 개수 증가나 새 나라 태그만으로 포트 원인이라고 판정하지 않는다. rename 실패가 남긴 실제 `_temp` 파일의 생성과 후속 cold reload는 위 별도 경로로 확인했다. 오류 0·모든 host 동작 통과·장기 AI 귀속 완료를 주장하지 않는다.

최종 `suite-r0-c0-error-fingerprint-review-v2.json`의 suite 로그는 **비어 있지 않은 156,424줄·정규화 fingerprint 896개**다. R0+C0에 정확히 존재하던 것은 852개, 새 exact fingerprint 44개는 새 파일명의 기존 rename 계열16개·GXC/CHI 인물 scope 계열의 새 사례3개·변경47경로 밖의 공유 경고25개다. 25개는 PRC 저장 재로드의 고문 template18개, WTT 군벌 역할3개, 인도네시아 시장2개, 스페인 역할2개로 분류했으나 원인·포트 귀속은 미확정이다. 새44개 전체를 기존 오류라고 부르지 않는다. PRC 고문 경고의 한국 밖 인물 보존 영향은 동일 조건의 host 재로드 대조 없이 미검증이다. rename `errno2` 계열은 사전 원본 로그26건에도 있었지만 OS/OneDrive 등의 원인을 확정하지 않는다. 이전 v1 보고서는 보존했다.

이 대조의 **4 PASS / 0 FAIL**은 변경47경로·fixture·선택한 주/보상 심벌의 새 fingerprint, 기록된 map/state/fatal signature, dynamic-token warning을 찾지 못했다는 한정 관측이다. 클린 로그·모든 world 저장 호환·장기 AI 검증으로 확대하지 않는다. 전체 새 항목과 분류 근거는 위 외부 보고서에 유지한다.

C0에서 직접 본 내용은 다음과 같다.

- 지도에 **North Gyeongsang / South Gyeongsang** 이름과 KOR 소유가 표시됐다. 경남 공군기지는 UI에 `1/10`으로 표시됐고 시설 표시도 보였다. 이 관측은 해당 화면의 실제 표시이며 모든 새 주의 건물 배치가 맞다는 포괄 판정은 아니다.
- 한국 중점 UI를 열고 **The Future of the Republic**의 정상 진행을 관측했다. 1월 9일 08시 중점 세부 화면에는 7일이 표시됐고, 1월 11일 13시 활성 진행 UI, 1월 16일 07시 관측에서는 완료 알림과 후속 이벤트가 보였다. 정확한 완료 시각은 관측하지 않았으므로 “1월 16일 정각 완료”나 임의의 착수 시각으로 기록하지 않는다. 강제 완료 fixture 실행과 구별한다.
- 현재 GUI 배율의 높이 1504px 화면에서 기존 긴 영문 초기 이벤트 하단이 화면 밖으로 넘쳤다. 해당 본문/창 배치는 이번 주 분할에서 추가한 내용이 아니며 별도 UI 개선은 요청 범위 밖이라 변경하지 않았다.
- `KOR_1936_01_23_08x_temp.hoi4`를 새로 저장했다. 엔진이 실제 남긴 `_temp` 접미사를 그대로 보존했으며 사본은 `profile/runs/c0/post-game/save games/`에 있다. 크기 **81,591,622바이트**, 저장 헤더는 `Operation Postern 1.19.4.2.2da5 (3e60)`이다. 최초 C0 수집 때는 파일 생성만 확인했고, 이후 별도 C0-02 프로세스에서 **cold reload와 추가 시간 진행을 실제 확인**했다.

이번 cold reload는 **새 분할 지도에서 45출력으로 만든 새 저장 → 표시 참조를 보완한 47출력의 새 프로세스**라는 구체적 경로다. 변경 전 9주 저장의 호환이나 마이그레이션을 입증하지 않는다. 아래 suite의 진행 중 decision 저장 재로드는 같은 프로세스에서 수행한 별도 경로다.

C1 한국어 화면에서는 경상남도 패널에 인구 `2.31M`, 기반시설 `2/5`, 공군 `1/10`, 슬롯 `5/25`와 공장 표시가 보였다. 1월 20일 09시까지의 진행 중 한국어 중점 계통도 → 산업·교육 → 포항제철 상세에서 **경상북도·경상남도의 대한민국 지배 조건이 둘 다 체크**됐다. 경북 강철 +25와 포항 제철소 확장 결정 잠금 해제가 보상으로 표시됐지만, 중공업 개발 선행 조건은 미완료 빨간색으로 남아 실제 진행을 차단했다. 이 C1에서는 강제 완료나 보상 발동을 하지 않았으므로 실제 강철 지급·결정 착수의 증거로 사용하지 않는다. 이후 1월 28일 21시 메뉴 일시정지까지 진행한 뒤 정상 종료·수집했다.

### Final v5 suite의 범위 확인 — 2026-11-08 KST

최종 `validation/runtime-evaluations/suite-final-mixed-evaluation-v2.json`은 **190 PASS / 0 MISMATCH / 10 UNVERIFIED**다. 미검증 10개는 BASE 재로드 뒤 다섯 분기의 `REPEATED_STARTUP` marker 5개와 fresh Verify 재클릭 5개다. 이들을 PASS로 계산하지 않는다. 최초 v1은 BASE 저장 전의 Verify 클릭을 재로드 뒤 클릭으로 잘못 세었으므로 v2가 대체한다. 실제 UI BASE 재로드 다섯 번과 선택한 raw 초기화·후속 보상/취소/슬롯/반복/활성 저장 재로드의 별도 증거는 유지된다. 아래 개별 검사와 수치가 겹치므로 합산하지 않는다.

`validation/runtime-evaluations/`의 ledger-009~011은 half-new, ledger-013은 slots, ledger-016은 반복 활성 저장의 실제 재로드, ledger-017은 수집된 반복 결과와 증거 결합이다. 최신 `suite-ledger-018-final-evaluated-restored.json`은 최종 평가·복구를 연결하며 초기 ledger의 오래된 미확인 문구도 현재 범위로 정리했다. 과거본은 유지한다.

- **BASE:** 실제 저장의 한국 15주 합은 민공·군공·조선소 `9·4·1`, 기반시설 합 `23`, 공군기지 합 `6`이다. `suite-base-structural-check.json`의 literal 범위 검사는 **14/0**이다. BASE를 실제 UI로 불러와 다시 저장한 비교에서 15주 블록은 byte-identical, 선택한 KOR 중점·정치력·대상 decision queue·비진단 flag/variable도 동일했다. 그러나 원래 BASE 대비 **전체 KOR에는 미분류 literal 차이 27개가 남아 있다.** 생산/수출/사용 캐시·일부 함대/GUI 관련 항목 등이 포함되지만 전부 무해한 refresh라고 확정하지 않는다.
- **다섯 재로드 기준:** 최초 두 실제 UI reload는 `suite-reloaded-kor-equivalence-01.json` **5/0**, 후속 half-new·slots·repeat의 사전 비교는 각각 **10/0**이다. 다섯 postload KOR raw는 모두 SHA-256 `E5EE2598D5EF966EB4D45A09DC672D3254906C184DEF2802F5B9A3CD0EE2BC77`로 같았다. 이는 postload 결과 사이의 동일성이지, 원래 BASE와 전체 나라/세계가 같거나 원래 BASE 대비 27개 차이의 원인을 규명한 것이 아니다.
- **강제 보상:** 실제 중점 완료 4개 뒤의 `suite-rewards-literal-payout-review.json`은 한정된 **11/0**이다. 저장에 새로 기록된 자원 **추가량**은 `920 강철25`, `1152 강철15`, `918 텅스텐5`다. 특히 함북 `1152`는 시작 강철15가 따로 있으므로 저장 payload15를 최종 기초 자원 총량15로 해석하지 않는다. 실제 민공은 경남 `1148: 1→4`, 평북 `1151: 1→2`, 추가 공유 슬롯은 각각 `3·1`, 부산 province `4056`의 해군기지는 `5→9`로 기록됐다. 정상 선행·기간을 밟은 보상 시험이 아니라 강제 완료의 실제 효과 확인이다. 15주 raw에는 진단 변수·경과 상태 등을 포함한 literal 차이 567개가 있어 이 보고서가 모든 필드나 전체 나라를 설명한 것은 아니다.
- **기존 ID 쪽 상실 half-retained:** 사전 비교 **9/0**, 실제 active queue **7/0**, 결과 literal 범위 **9/0**을 각각 기록했다. 실제 90일 포항 decision queue가 존재한 뒤 경북 `920`만 KOR→JAP로 바뀌고 경남 `1148`은 유지됐으며, 결과 저장에서 queue는 사라지고 기존 포항 중점의 강철 추가량25만 남아 추가9는 없었다. 한국 15주의 물리 공장 레벨은 그대로였다. day30 관측은 게임 날짜 **3월 6일 24시**, 실제 결과 저장은 **4월 18일 22시**로 구별한다. 최종 mixed v2는 실제 착수 PP25 차감, 취소 경계의 국가 민공 getter38 고정·프로젝트 가용15→24(+9), 두 경계 PP476.201 동일을 확인했다. source `cancel_effect={}`와 관측 경계에서 별도 환급이 보이지 않은 사실을 기록하며 경과 PP 증가를 환급으로 해석하지 않는다. raw parser의 점유 필드 부재를 점유0으로 해석하지 않는다. 이 분기의 active/result 저장 자체는 cold reload하지 않았다.
- **신규 ID 쪽 상실 half-new:** `suite-half-new-pre-comparison.json` **10/0**, `suite-half-new-active-check.json` **7/0**, `suite-half-new-literal-payout-review.json` **9/0**이다. actual active 저장에 90일 queue·PP475·경북 강철 추가량25·한국 15주 KOR 소유가 기록됐다. 이후 결과 저장 **3월 14일 04시**에는 경남 `1148`만 JAP로 바뀌고 경북 `920`은 KOR를 유지했으며 queue는 사라지고 추가량25는 그대로여서 추가9가 없었다. 별도 `validation/runtime-live-observations/suite-half-new-interim-01/review.json`의 **7/0**은 PP500→475, 약1.875일 뒤 조기 종료, 국가 민공 getter38 고정 상태에서 프로젝트 가용15→24(+9), 취소 경계 PP476.201 동일 및 day7/day30을 기록했다. 당시 prefix 길이·SHA만 남긴 중간 관측은 종료 후 아래 3/0 대조로 최종 수집 로그와 연결했다.
- **슬롯 합성 검증:** `suite-slots-pre-comparison.json` **10/0**, `suite-slots-literal-review.json` **7/0**이다. 실제 **2월 11일 10시** 결과 저장은 충북 `1149`만 바뀌고 다른 한국 14주 raw는 동일했다. `1149`는 군공20·민공5·조선소0, `extra_shared_slots=51`(강제50+1)이었다. live 중간 검사는 **7/0**, PHASE 6개·EXPECTATION 5개·DONE을 확인했고 종료 후 아래 prefix 대조로 연결했다. 여섯 단계가 모두 2월 5일 03시여서 `hours=1`의 실제 한 시간 경과를 주장하지 않는다. `instantbuild`·`include_locked=yes` 합성 경로이며 일반 건설 UI를 검증하지 않았다. 마지막 군공21 시도에는 공유 슬롯25도 이미 차 있어 유형 상한만의 강제 효과를 분리하지 못했고, 내륙 조선소 시도에는 해안 조건도 섞였다.
- **반복의 활성 저장·인게임 재로드:** `suite-repeat-pre-comparison.json` **10/0**으로 다섯 분기의 기준을 대조했고, `suite-repeat-active-check.json` **8/0**은 실제 **2월 12일 24시** 저장의 남은 queue83일·PP483.407·day8/start_day1·starts1/ends0·경북 강철 추가량25를 확인했다. 그 파일을 실제 인게임 Load한 직후 같은 시각에 `...02_12_24a_temp.hoi4`로 다시 저장한 `suite-repeat-active-reload-review.json`은 **14/0**이다. 한국 15주 raw와 대상 queue·PP·강철·카운터·flag·완료 중점이 유지됐다. 전체 KOR raw의 25개 차이는 미분류로 남기며 전체 나라 동일을 주장하지 않는다. 같은 프로세스의 인게임 재로드이며 별도 cold launch나 변경 전 저장 호환이 아니다. 재로드 직후 민공9 점유 getter의 직접 판정도 별도다.
- **반복 2회 완료:** `suite-repeat-literal-payout-review.json`은 **16/0**이다. 한국 15주 resource 필드 변화는 경북 `920`의 강철 추가량 **25→34→43**, 회당 +9뿐이었다. 활성/첫 완료 뒤 중간/최종 저장의 starts·ends는 각각 `1/0 → 2/1 → 2/2`이며 최종 queue는 없었다. START 관측은 **2월 6일 02시·5월 7일 01시**, END는 **5월 6일 24시·8월 4일 24시**, 각 타이머의 관측 경과는 **90 daily tick**이다. 날짜 문자열과 tick을 따로 기록하며 달력 연산으로 타이머를 추정하지 않는다. **6월 6일 12시** 중간 저장은 두 번째 queue59일을 포함하고, day200은 **8월 23일 24시**, 최종 저장은 **8월 28일 06시**였다. 생산 getter 증가14.04를 원자원 +9의 증거로 삼지 않고 짝지은 저장의 추가 payload 차이를 사용했다. 실제 decision 효과를 강제 활성한 시험이며 일반 선행 조건·플레이어 UI 착수의 통과는 아니다.

`suite-interim-prefix-bindings.json` **3/0**은 rewards·half-new·slots 중간 관측의 prefix 길이/해시를 최종 수집 `game.log`와 연결했다. `suite-production47-bindings-final.json` **75/0**은 실제 suite의 생산 출력47개·fixture26개·manifest를 결합했다. 이 일치는 forced 효과를 정상 UI 시험으로 바꾸거나 누락된 다른 증거를 보충하지 않는다.

인게임 BASE reload 직후에는 진단용 freshVerify 표시가 보이지 않다가 시간 진행 뒤 다시 나타났다. 원인은 미확정이다. `REPEATED_STARTUP` marker가 없으므로 이 UI 현상만으로 startup callback 재실행을 입증하지 않는다. 실제 UI reload와 raw 상태 비교는 별도 증거로 유지한다.

47출력의 정적·언어 재검사는 위 19/0/11로 완료했다. 일반 국뽕 fixture 준비 중 외부 profile helper의 `Path + str` 결합 오류를 먼저 수선한 뒤 실제 gook을 실행했다. 실패한 준비 시도에서는 게임이 시작되지 않았으며 이를 게임 런타임·저장 코드 결함으로 분류하지 않는다. 실행 뒤 지도 보호 도구만의 후속 수선과 5사례는 위 정적 표에 구별했다.

### 실행 종료와 원래 환경 복구 — 2026-11-08 KST

`profile/runs/suite/evidence.json`의 최종 수집은 누적 새 저장 사본 17개를 포함하고, 기존 저장 43개의 차이는 없었다. 누적 수량에는 앞선 실행 저장도 포함되므로 suite 한 실행만의 신규 저장 수로 해석하지 않는다. 실제 게임이 생성한 시험 저장 17개는 user-data에 그대로 보존했으며, 프로필 복구 때 삭제하지 않았다. 최종 게임 메뉴 시각은 8월 28일 06시였다.

`profile/restoration-result.json`은 로그를 제외한 **원래 프로필 20개·기존 저장 43개, 총 63개**의 복구/보존 확인과 차이 0, 새 optional 잔여 0, 임시 fixture descriptor 제거를 기록했다. 사전 백업 97개에는 로그도 있어 복원 대상 97개로 부르지 않는다. 별도 읽기 감사 `validation/final-original-profile-save-check.json`은 **108 PASS / 0 FAIL**로 위 원본과 저장의 내용·mtime 및 HOI4/launcher 프로세스 부재를 확인했다. 원래 모드 선택으로 복구했으며 `profile/final-ui-restoration-observation.json`에는 01:47 KST 기존 Steam 창의 실제 녹색 **플레이** 버튼 관측을 기록했다. 기존에 열려 있던 Steam은 유지했다.

최종 런타임 47출력·선택 donor/host/schema의 사후 재지문은 위 drift0이며, 지도 보호 도구 수선 뒤 core47·원장 검사도 exit0이다. 복구·지문·도구 확인을 미검증 항목의 통과로 확대하지 않는다. 1939는 위 host 미지원으로 기록한다.

원본은 핵심 1936·옵션·보상·취소·반복·슬롯 검증을 기록했으나 실제1939·UI·새 저장 재로드는 원본에서도 미검증이다. 분할 포트는 위에 각각 적은 UI·새 저장 cold reload·국뽕 옵션·강제 보상·양쪽 부분 상실·슬롯 합성 경로·반복 2회·진행 중 저장의 인게임 재로드 범위만 확인했다. 기존 저장 마이그레이션, 다른 DLC 조합, 장기 AI 경고의 귀속, 멀티플레이와 외부 호환 모드는 검증 없이 지원을 주장하지 않는다. 영어와 RT56 한국어 번역 구성의 개별 관측을 최종 배포 언어 의존성 계약의 확정으로 확대하지 않으며, 선언된 Korean Language와 실제 시험의 RT56 한국어 번역 차이는 출시 전 별도 결정이 필요하다.

새만금의 기존 충청 지정, 비해안 항구 요새 `13419 → 13540`, 일본 요새 `1003` 범위, 비해안 `10065` floating-harbor 앵커는 별도 결함이다. 이번 부모 정렬을 그 수선 완료로 기록하지 않는다. 커밋·푸시·태그·패키징·업로드는 수행하지 않았다.
