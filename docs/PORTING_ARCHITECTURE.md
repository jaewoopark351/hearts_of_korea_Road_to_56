# RT56 대상 포팅 아키텍처

## 1. 문서 상태

- 상태: 현재 설계 기준
- 작성일: 2026-09-06
- 적용 대상: C:\hoi\hearts_of_korea_Road_to_56
- 구현 상태: 설계·기준선 수립 단계
- 런타임 호환성: 미완료

이 문서는 어떤 소스를 기준으로 무엇을 보존하고 어떻게 병합할지 정의한다. 파일을 실제로 이식했다거나 게임 검증을 통과했다는 기록이 아니다.

## 2. 목표와 비목표

### 목표

1. 현재 RT56을 필수 호스트로 삼는 별도 HOK 호환 모드를 만든다.
2. HOK의 한국 정체성, 대체역사 설계, 고유 이벤트·중점·결정·인물·자산을 가능한 한 보존한다.
3. RT56의 전 세계 지도, 공유 시스템, 비한국 콘텐츠와 이후 변경을 보존한다.
4. 충돌을 숨기지 않고 파일·논리 ID별로 병합 근거와 출처를 남긴다.
5. 새 Workshop 정체성으로만 배포할 수 있는 구조를 만든다.

### 비목표

- donor HOK와 RT56을 그대로 동시에 켜는 얇은 패치
- donor 전체 파일을 RT56보다 뒤에서 덮어쓰는 방식
- 호환성 작업에 섞인 무관한 리밸런스나 콘텐츠 재설계
- 바닐라, Workshop RT56, HOK donor 또는 사용자 로그의 직접 수정
- 기존 HOK 세이브 호환성의 사전 약속

## 3. 권위와 역할

| 소스 | 권위가 있는 영역 | 권위가 없는 영역 |
|---|---|---|
| 바닐라 1.19.x | 엔진 문법, 스키마, scope, 로더의 기본 동작 | RT56이 바꾼 실제 콘텐츠 값 |
| 현재 RT56 스냅샷 | 호스트의 전 세계 데이터, 공유 시스템, 현재 논리 ID와 병합 기준 | HOK의 디자인 의도 |
| 사용자 제공 HOK donor | HOK 콘텐츠 의도, 상속 ID, 자산과 provenance | RT56 대상 전역 파일, 새 모드 업로드 정체성 |
| 현재 작업 트리 | 검토·이식이 끝난 최종 산출물 | donor에 있다는 이유만으로 복사된 미검토 파일 |
| 런타임 로그와 재현 | 실제 로드·실행 결과 | 로그에 나타나지 않은 동작의 안전성 |

문법 질문은 바닐라를 보고, RT56이 소유하거나 변경한 콘텐츠 질문은 정확한 RT56 스냅샷을 본다. HOK donor는 무엇을 보존할지 알려 주지만, 그 구현 파일이 현재 RT56에 그대로 유효하다는 증거는 아니다.

## 4. 런타임 계층

목표 계층은 다음과 같다.

    Hearts of Iron IV
      └─ The Road to 56
          └─ Hearts of Korea × RT56 compatibility port
              └─ 선택된 localisation 구성

HOK donor 자체는 기본 플레이세트에서 비활성화한다. 호환 포트가 HOK의 필요한 런타임 콘텐츠를 직접 포함하거나, 재배포가 부적절한 부분은 명시적 의존성 또는 대체 방식으로 설계한다.

descriptor의 dependency 선언은 의도를 표현할 뿐 실제 물리적 로드 순서를 증명하지 않는다. launcher playset, launcher .mod 경로와 로드 로그를 함께 확인해야 한다.

## 5. 콘텐츠 소유 원칙

- HOK 고유 한국 콘텐츠: 의도를 보존하되 RT56의 현재 schema와 연결점에 맞게 이식한다.
- RT56 전 세계·공유 콘텐츠: 기본적으로 유지한다.
- 양쪽이 한국을 변경한 경우: 어느 한쪽을 자동 승자로 정하지 않고 기능별 병합 결정을 기록한다.
- 새 접착 코드: 기존 전역 ID와 충돌하지 않는 프로젝트 전용 prefix/namespace를 사용한다.
- HOK 상속 ID: RT56 및 바닐라와 충돌하지 않고 의미가 유지될 때 보존한다.
- 지속 ID를 바꿔야 하는 경우: 참조 closure와 세이브 영향을 기록하고 별도 승인을 받은 마이그레이션으로 처리한다.

## 6. donor 파일 분류

프로덕션 파일은 donor에 존재한다는 이유만으로 유지하지 않는다. 각 파일 또는 논리 정의를 다음 중 하나로 분류한다.

| 분류 | 의미 |
|---|---|
| ADD | RT56과 충돌하지 않는 HOK 고유 정의 |
| USE_RT56 | donor 파일을 싣지 않고 RT56 정의를 사용 |
| THREE_WAY_MERGE | HOK 의도와 현재 RT56 변경을 논리 단위로 병합 |
| OVERRIDE | 근거를 기록하고 RT56 정의를 의도적으로 대체 |
| BINARY_MERGE | RT56 base에서 다시 만들어야 하는 전역/바이너리 산출물 |
| ASSET_COPY | 출처·사용권·참조를 기록한 HOK 자산 |

같은 상대경로 충돌은 하한일 뿐이다. 다른 파일에 같은 event, focus, state, idea, character, sprite 또는 scripted ID가 정의될 수 있으므로 논리 ID 감사도 수행한다.

의도적 whole-file shadowing에는 다음 ledger 정보가 필요하다.

- 상대경로와 논리 ID
- RT56 descriptor 및 원본 파일 해시
- donor 출처와 해시
- 보존할 HOK delta
- whole-file 대체가 불가피한 이유
- RT56 기능 영향
- 정적·런타임 검증 결과

## 7. 전역 파일 정책

bookmark, generic MIO, medal scripted trigger, on_action, generic advisor, difficulty, intelligence agency, 공용 색상, 일본·중국 공용 콘텐츠 및 전 세계 지도 파일은 stale override 위험이 크다.

- donor 파일 전체를 기본값으로 사용하지 않는다.
- 가능한 경우 프로젝트 전용 추가 파일과 고유 ID를 사용한다.
- 동일 ID를 덮어쓰는 파일은 해당 디렉터리의 loader/merge 규칙을 먼저 확인한다.
- whole-file 파일이 필요하면 현재 RT56 파일을 base로 HOK delta를 다시 적용한다.
- RT56 내용을 산출물에 포함해야 하면 해당 RT56 스냅샷, 해시, 변경 delta 및 notice/licence 상태를 기록한다.

## 8. 지도 아키텍처

### 확인된 충돌

- 바닐라 definition.csv의 현재 최대 province ID: 13413
- HOK donor/current project의 최대 ID: 13447
- 현재 RT56의 최대 ID: 13534
- HOK 추가 범위 13414–13447의 34개 행은 RT56의 같은 ID 34개 행과 모두 다르다.
- 현재 프로젝트가 RT56의 13448–13534를 누락시켜 실제 state 참조 오류를 만들었다.
- HOK state ID 1028–1031과 1082–1085는 RT56이 이미 서로 다른 유럽·카리브 state에 사용한다.

따라서 HOK의 숫자 ID만 보존하는 것은 의미 보존이 아니다. 현재 조합에서는 그 숫자가 이미 RT56의 다른 province 또는 state를 뜻한다.

### 합성 규칙

1. 현재 RT56 전 세계 지도를 canonical base로 사용한다.
2. 가능하면 HOK가 갈라져 나온 역사적 base와 donor를 비교해 HOK의 의도된 한국 지리 delta를 추출한다.
3. 역사적 base가 없으면 HOK와 RT56의 모든 차이를 HOK 고유 변경으로 간주하지 않는다.
4. provinces.bmp와 definition.csv는 현재 RT56 파일에서 합성한다. donor 파일을 그대로 복사하지 않는다.
5. 새 province가 필요하면 작업 직전 RT56 전체 ID/RGB 집합을 다시 조사하고 충돌 없는 새 ID와 RGB를 배정한다. 현재 최대값 다음 번호를 미래에도 안전하다고 하드코딩하지 않는다.
6. RT56 기존 province/state/strategic-region ID를 HOK 편의를 위해 재번호화하지 않는다.
7. 모든 HOK province 참조를 state, strategic region, railway, supply node, building, adjacency, unit position, naval base, victory point, country history, OOB 및 script까지 추적한다.
8. RT56은 history/states와 map/strategicregions를 replace_path한다. 관련 HOK 파일은 바닐라나 donor가 아니라 현재 RT56 정의에서 리베이스한다.
9. 신규 모드에 위 디렉터리의 광범위한 replace_path를 다시 추가하지 않는다.

지도 ID 마이그레이션은 신규 게임 전용 결과가 될 수 있다. 대표적인 변경 전 세이브의 load–advance–save–reload 시험 없이 기존 세이브 호환성을 주장하지 않는다.

## 9. localisation

현재 descriptor는 Korean Language를 선언하지만 실패 플레이세트에는 The Road to 56 Korean Translation이 활성화되어 있었다. 후자는 localisation 전체를 replace_path한다.

최종 구성은 아직 정하지 않았다. 결정 전에는 다음을 분리해서 확인한다.

- HOK 파일의 l_english/l_korean header와 실제 키
- Korean Language가 제공하는 로더 계약
- RT56 Korean Translation의 replace_path와 HOK 문자열 노출 방식
- 두 번역 모드를 함께 쓸 때의 덮어쓰기와 누락
- 영어/한국어 UI에서 HOK 키, 토큰, 아이콘, scripted localisation

일반 YAML formatter를 사용하지 않고 기존 BOM·header·키·토큰을 보존한다.

## 10. 배포 정체성과 provenance

| ID | 의미 | 새 모드에서의 사용 |
|---|---|---|
| 2898629778 | 역사적 HOK 원본 Workshop 항목 | provenance만 |
| 3793992662 | 현재 HOK donor descriptor의 항목 | provenance만 |
| 820260968 | The Road to 56 | 의존성/provenance |
| 미할당 | 이 신규 호환 모드 | 첫 신규 게시에서만 할당 |

새 descriptor는 첫 게시 전 remote_file_id를 갖지 않는다. 위 세 ID를 복사하거나 게시 대상으로 사용하지 않는다. HOK 원작, donor 개정, RT56, localisation, 제3자 자산과 신규 호환 기여분을 구분한다.

## 11. 아키텍처 완료 조건

다음 조건이 모두 충족되어야 “RT56 호환 포트”라고 부를 수 있다.

- 모든 프로덕션 파일에 유지·제거·병합 근거가 있다.
- RT56 exact-path 및 논리 ID 충돌이 ledger로 닫혀 있다.
- 최신 RT56 전 세계 데이터가 의도치 않게 손실되지 않는다.
- HOK 고유 콘텐츠의 보존·변경·제외가 기록돼 있다.
- descriptor와 실제 launcher playset이 일치한다.
- RT56-only 대조군 대비 새 fatal 오류나 심각한 반복 오류가 없다.
- 새 게임에서 한국 로드, 지도 진입, unpause, focus, decision, event, OOB, supply와 핵심 경로를 검증했다.
- 알려진 미검증 DLC·AI·멀티플레이·세이브 경로를 공개했다.
