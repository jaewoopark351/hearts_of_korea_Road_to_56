# ADR-0002: RT56 기준 한국 지도 ID 마이그레이션

## 상태

- 기록일: 2026-09-06
- 결정: 채택
- 정적 구현: 완료
- 런타임 검증: 미실행
- 세이브 정책: 신규 게임 전용

## 맥락

HOK donor는 바닐라 1.19.2 이후에 한국 지역 province `13414–13447` 34개를 추가했다. 현재 RT56도 같은 숫자를 서로 다른 전 세계 province에 사용하며 `13534`까지 확장했다. HOK의 state `1028–1031`, `1082–1085`도 RT56에서 다른 지역에 이미 할당돼 있다.

donor의 `definition.csv`와 `provinces.bmp`를 그대로 사용하면 RT56 state가 참조하는 `13448–13534` 87개 province가 사라지고, 같은 숫자가 서로 다른 지리를 뜻하게 된다. 2026-09-06 14:06 로그의 `Malformed token`과 연쇄 state/map 오류가 이 상태를 보여 준다.

## 결정

RT56 전 세계 지도를 canonical base로 유지하고, HOK와 바닐라의 한국 지역 차이만 합성한다.

### Province

- donor `13414–13447`을 compat `13535–13568`로 1:1 이전한다.
- 각 새 province에는 donor의 RGB·terrain·continent·coastal 속성을 옮긴다.
- RT56의 기존 `1–13534` definition 행과 한국 외 bitmap은 유지한다.
- HOK-vs-바닐라 한국 delta에 해당하는 bitmap 1,889개 픽셀만 RT56 base에 합성한다.
- donor 기준 비해안 province `4126`, `7125`, `7175`, `7204`, `10065`의 coastal 속성을 보존한다.

### State

| donor | compat | 지역 | 할당 근거 |
|---:|---:|---|---|
| 1028 | 918 | 함경 | RT56의 같은 한국 지리 state를 재사용 |
| 1029 | 1144 | 강원 | 현재 RT56에서 비어 있는 ID 할당 |
| 1030 | 920 | 경상 | RT56의 같은 한국 지리 state를 재사용 |
| 1031 | 1145 | 충청 | 현재 RT56에서 비어 있는 ID 할당 |
| 1082 | 919 | 전라 | RT56의 같은 한국 지리 state를 재사용 |
| 1083 | 917 | 황해 | RT56의 같은 한국 지리 state를 재사용 |
| 1084 | 1146 | 제주 | 현재 RT56에서 비어 있는 ID 할당 |
| 1085 | 1147 | 쓰시마 | 현재 RT56에서 비어 있는 ID 할당 |

state `525`, `527`, `528`은 숫자를 유지하되 RT56 base와 새 한국 지형에 맞춰 재구축한다.

### 참조 closure

다음 범위를 함께 이전한다.

- state history, strategic region membership와 victory point/building 항목
- `buildings.txt`, `railways.txt`, `supply_nodes.txt`, `unitstacks.txt`
- country history, OOB, focus, decision, event, on_action과 AI script의 숫자 참조
- 한국 영·한 state localisation

donor에는 별도 adjacency delta 파일이 없으므로 RT56/바닐라 adjacency를 그대로 상속한다. compat descriptor에는 map/state용 `replace_path`를 추가하지 않는다.

## 구현

`tools/build_rt56_map.py`가 donor, RT56과 바닐라 핵심 입력의 SHA-256을 고정하고 합성 산출물을 만든다. `--check`는 다음을 포함해 검사한다.

- 입력 fingerprint 변화
- province ID/RGB 유일성과 bitmap/definition closure
- RT56 전 세계 행과 한국 외 bitmap 보존
- state/province/strategic-region membership closure
- building, railway, supply와 unit-stack 참조
- 모든 building 행의 7필드 구조와 `naval_base_spawn` 좌표/RGB 해석, 복원한 한국 spawn의 sampled province/state/coastal/sea-link closure
- pinned RT56과 비교해 새로 생긴 coastal land province-without-`naval_base_spawn`가 0인지 확인
- 과거 HOK state 파일 제거와 새 파일 집합

`tools/migrate_hok_ids.py`는 map 밖의 HOK-owned 참조를 같은 매핑으로 옮긴다.

`buildings.txt`는 donor-vs-바닐라 2-way 차집합만으로 만들지 않는다. pinned RT56이 바닐라와 동일한 행을 제거했을 수 있으므로, RT56의 실제 행 존재 여부와 합성 bitmap에서 좌표가 소비되는 province를 함께 확인하는 3-way 결정이 필요하다. 2026-09-06 후속 감사에서 이 공백 때문에 HOK 지형에 필요한 vanilla-identical `naval_base_spawn` 7행이 누락된 것을 확인했다. 생성기는 다른 401개 vanilla-identical 한국 건물 행을 되살리지 않고, 감사한 7행만 별도 topology restoration으로 추가한다.

## 결과와 제한

이 결정은 RT56의 다른 지역 ID를 보존하면서 HOK 한국 지형을 제공한다. 대신 숫자 persistent ID가 바뀌므로 기존 HOK 세이브와의 호환을 약속하지 않는다.

후속 생성기는 `map/buildings.txt`를 71,895행에서 71,902행으로 재생성했고, 합성 지도에서 RT56보다 새로 비는 항구 spawn이 없다는 정적 gate를 통과했다. 다만 이 보정 뒤 다음은 아직 증명되지 않았다.

- 엔진의 map database load
- 한국 선택과 지도 진입 후 unpause
- 해안, 항구, adjacency, railway와 supply의 실제 동작
- unit position과 naval placement의 화면상 위치
- 모든 DLC/bookmark에서의 시작 상태

이 런타임 게이트가 통과하기 전에는 시작 크래시 사건을 해결 완료로 닫거나 RT56 지도 호환을 완료했다고 표현하지 않는다.
