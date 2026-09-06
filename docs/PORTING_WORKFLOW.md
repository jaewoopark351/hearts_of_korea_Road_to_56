# RT56 포팅·검증 워크플로

## 1. 목적

이 절차는 HOK donor 복제본을 RT56 기반의 검증 가능한 신규 포트로 전환하는 작업 순서와 게이트를 정의한다. 빠르게 로그 줄 수를 줄이는 것이 아니라, RT56의 현재 동작을 보존하면서 HOK의 의도된 차이를 재구성하는 것이 목표다.

## 2. 작업 전 고정할 것

각 구현 묶음을 시작하기 전에 다음을 기록한다.

- HOI4 버전, build/checksum 및 Steam build ID
- 활성 DLC와 비활성 DLC를 구분할 수 있는 실제 자료
- launcher playset, 모드 표시명, launcher .mod 경로, 실제 물리 경로와 순서
- 현재 compat 작업 트리의 Git 상태 또는 “Git 없음”
- HOK donor commit/hash와 descriptor
- RT56 descriptor, 디렉터리 수정 시각 및 대상 파일 SHA-256
- localisation 모드와 언어 설정
- 기준 로그의 실행 ID, 시각과 SHA-256

RT56 Workshop 폴더가 작업 도중 바뀌면 해당 묶음의 비교를 중단하고 새 기준선을 만든다.

## 3. 권장 대조군

| ID | 플레이세트 | 용도 |
|---|---|---|
| V0 | 바닐라 | 엔진/DLC 자체 오류 기준 |
| R0 | RT56 | 호스트의 기준 오류와 동작 |
| R1 | RT56 + 선택 localisation | 번역 계층의 영향 |
| C0 | RT56 + compat port | 포트 자체의 영향 |
| C1 | RT56 + 선택 localisation + compat port | 목표 사용자 구성 |

HOK donor는 C0/C1에서 활성화하지 않는다. 모드 순서 표시는 실제 로드 우선순위의 증거가 아니므로 launcher 파일과 로그로 확인한다.

게임 실행은 별도 허가가 있을 때만 한다. 실행이 허가되지 않은 단계에서는 정적 결론을 런타임 완료로 표현하지 않는다.

## 4. 단계와 게이트

### Phase 0 — 기준선과 재현

1. 네 source root와 로그 경로가 실제로 존재하는지 확인한다.
2. descriptor 및 launcher .mod를 읽고 ID, dependency, replace_path, path를 기록한다.
3. 최신 실패 로그가 어느 실행·플레이세트에서 나왔는지 연결한다.
4. 허가된 경우 R0/R1과 C0/C1을 깨끗한 프로세스 재시작으로 재현한다.

게이트: 실제 물리 경로, RT56 snapshot과 실패 조건을 설명할 수 있어야 한다.

### Phase 1 — 전체 파일과 논리 ID 인벤토리

1. current tree와 donor, RT56, 바닐라의 상대경로 manifest와 해시를 만든다.
2. 각 current production 파일을 ADD, USE_RT56, THREE_WAY_MERGE, OVERRIDE, BINARY_MERGE, ASSET_COPY 중 하나로 분류한다.
3. event, focus, decision, state, province, character, idea, sprite, scripted trigger/effect 등 논리 ID 충돌을 별도로 찾는다.
4. 출처·재배포 상태가 불명확한 파일을 표시한다.

게이트: “donor에 있었기 때문” 외에 각 파일을 선적할 이유가 있어야 한다. 미분류 파일은 release package에 넣지 않는다.

### Phase 2 — descriptor와 런타임 계약

1. 현재 RT56 표시명과 정확히 맞는 필수 dependency를 설계한다.
2. donor HOK는 런타임 dependency로 두지 않는다.
3. Korean Language와 RT56 Korean Translation 중 어떤 구성을 지원할지 localisation 감사 후 결정한다.
4. 새 compat descriptor에 과거 remote_file_id나 RT56 remote_file_id가 없는지 확인한다.
5. 새 replace_path를 기본적으로 추가하지 않는다.

게이트: descriptor, launcher playset 및 문서의 dependency 계약이 서로 일치해야 한다.

### Phase 3 — 지도 리베이스

지도는 현재 시작 크래시의 선행 blocker이므로 다른 콘텐츠의 런타임 판정보다 먼저 닫는다.

1. 현재 RT56 definition.csv와 provinces.bmp를 base로 고정한다.
2. HOK의 의도된 한국 지리 delta와 모든 참조 closure를 작성한다.
3. 충돌하는 HOK province/state ID의 새 할당안을 만든다.
4. ID·RGB 전역 유일성, bitmap 색상 집합, definition 행, state/region membership를 함께 검증한다.
5. buildings, railways, supply nodes, unit stacks/positions, adjacencies, naval bases, victory points, history와 OOB를 새 ID에 맞춰 추적한다.
6. RT56의 비한국 province/state/region이 보존되는지 전 세계 집합 비교를 한다.

게이트:

- RT56의 기존 전 세계 ID/RGB/지리 데이터가 의도 없이 사라지지 않는다.
- 모든 HOK 신규·이동 province가 정확히 한 state와 한 strategic region에 속한다.
- 참조되지 않는 ID와 정의되지 않은 ID가 없다.
- 허가된 런타임 시험에서 map load, 한국 선택, unpause, supply/railway/adjacency가 통과한다.

### Phase 4 — 전역·공유 파일 제거 또는 병합

우선순위가 높은 감사 대상:

1. bookmark와 시작 국가 설정
2. generic MIO 및 KOR MIO
3. medal scripted triggers
4. on_actions
5. generic advisors, difficulty, intelligence agencies
6. country colors/cosmetic
7. 일본·중국 공용 focus, decision, event와 history
8. frontend 및 공용 GFX

각 파일은 현재 RT56을 base로 논리 정의 단위에서 병합한다. stale donor whole-file로 RT56 추가 기능을 제거하지 않는다.

게이트: R0 대비 사라진 RT56 정의, duplicate ID, 새 parser/scope 오류가 없어야 한다.

### Phase 5 — HOK 고유 콘텐츠 이식

권장 순서:

1. 국가·state·history·OOB 기반
2. character와 leader/advisor 연결
3. idea와 modifier
4. focus tree
5. decision/mission
6. event와 on_action 연결
7. 장비·MIO·기술 연결
8. GFX, 모델, 음향과 UI
9. localisation
10. AI와 밸런스

각 묶음에서 entry scope, 모든 참조 ID, DLC gate와 RT56 연결점을 추적한다. restoration과 의도적 리밸런스는 같은 변경에 섞지 않는다.

게이트: 긍정 경로 하나와 중요한 차단/부정 경로 하나를 검증하고 R0 대비 회귀를 기록한다.

### Phase 6 — 통합 검증

정적 검사:

- brace, quote, block placement
- duplicate 및 missing logical ID
- descriptor/dependency/replace_path
- localisation BOM/header/key/token
- 맵 ID/RGB와 참조 closure
- 예상치 못한 whole-file/encoding/line-ending 변경

런타임 검사:

- launcher가 정확한 compat copy를 로드
- main menu와 새 게임
- 한국 지도·정부·법·idea·research·resource
- focus 연결, bypass/cancel/mutual exclusion/reward
- decision visibility/availability/cost/remove
- event scope/options/repeat chain
- OOB, 장비, character와 portrait
- supply, railway, adjacency와 unpause
- R0/R1 대비 로그 delta
- 필요 시 AI, save round trip, multiplayer sync

게이트: 성공한 항목과 미실행 항목을 구분해 기록한다. 메인 메뉴 진입만으로 통과시키지 않는다.

### Phase 7 — release 준비

1. source commit 또는 불변 snapshot을 기록한다.
2. allowlist 기반 staging을 만든다.
3. 로그, 덤프, 세이브, launcher 개인 설정, AGENTS.md, 캐시와 자격 증명을 제외한다.
4. dependency, target version, changelog, known limitations와 실제 검증 상태를 작성한다.
5. 파일별 provenance와 필요한 notice/credit을 확인한다.
6. 첫 게시가 새 Workshop 항목이고 다른 세 ID를 대상으로 하지 않는지 확인한다.

외부 게시·업로드는 그 구체적인 행동을 사용자가 별도로 요청했을 때만 수행한다.

## 5. 변경 묶음 기록 양식

각 구현 묶음은 최소한 다음을 보고한다.

- 범위와 비범위
- source fingerprints
- 원래 실패 또는 보존할 동작
- 파일/논리 ID별 분류
- 확인된 원인과 남은 가설
- 변경 파일과 HOK delta
- RT56 동작 영향
- 정적 검사
- 실행한 플레이세트와 런타임 결과
- 미검증 DLC, bookmark, AI, save, multiplayer 경로
- Git 및 외부 행동 상태

## 6. 즉시 중지 조건

- RT56 snapshot이 비교 중 바뀜
- donor HOK가 목표 플레이세트에 함께 로드됨
- 광범위한 replace_path가 RT56 데이터를 숨김
- 설명되지 않은 same-path 또는 logical-ID 충돌
- 최신 RT56 전역 지도를 보존할 병합 방법이 없음
- map persistent ID 변경에 필요한 migration 결정이 없음
- 출처·재배포 권한이 불명확함
- launcher가 다른 물리적 mod copy를 로드함
- 여러 원인이 같은 정도로 가능하고 구분 시험이 없음

중지 시 추측으로 파일을 지우지 말고, 확인된 증거와 다음 구분 시험을 문서화한다.
