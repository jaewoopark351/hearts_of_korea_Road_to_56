# ADR-0001: 런타임 의존성과 로드 구성

## 상태

- 기록일: 2026-09-06
- RT56 호스트 결정: 채택
- HOK donor 비활성 원칙: 채택
- localisation 구성: 미결정
- 저장소 descriptor 반영: 완료
- launcher `.mod` 반영: 미실행

> 2026-09-06 19:20 후속 상태: 저장소와 launcher descriptor는 현재 모두 `The Road to 56`과 `Korean Language`를 선언하고 표시명·버전·물리 경로도 일치한다. 그러나 실제 플레이세트는 `Korean Language` 대신 `The Road to 56 Korean Translation`을 활성화했다. RT56 필수 host 및 donor 비활성 결정은 유지하지만, 아래의 “RT56만 dependency”와 launcher 미반영 설명은 1차 구현 당시 기록이다. localisation 계약은 ADR-0003에서 계속 Pending Runtime이다.

## 맥락

사용자는 HOK를 RT56과 함께 동작시키는 “새로운 모드”를 만들고자 한다. 구현 전 작업 트리는 HOK donor의 production 파일 복제본이었고 RT56과 같은 상대경로 파일 73개, 전 세계 지도와 persistent ID 충돌이 확인됐다. 1차 구현은 이 충돌을 파일별로 분류하고 RT56 base에서 재구성했다.

구현 전 compat descriptor와 현재 외부 launcher `.mod`는 Korean Language(Workshop `2743487021`)만 dependency로 선언하고 The Road to 56을 선언하지 않았다. 반면 2026-09-06 실패 실행에는 RT56과 RT56 Korean Translation(Workshop `2769576030`)이 활성화되었고 Korean Language는 설치되어 있었지만 활성화되지 않았다.

## 결정

### 1. RT56은 필수 호스트다

목표 모드는 RT56 없이 standalone으로 동작하는 HOK 복원판이 아니라, 현재 RT56 위에 HOK 콘텐츠를 이식하는 별도 포트다. 따라서 release descriptor와 설명은 정확한 RT56 dependency를 표현해야 한다.

저장소 `descriptor.mod`는 표시명 `The Road to 56`을 유일한 dependency로 선언하도록 반영했다. HOK donor와 localisation 모드는 필수 dependency로 선언하지 않았다.

### 2. HOK donor는 런타임 dependency가 아니다

C:\hoi\hearts_of_korea는 콘텐츠 의도와 provenance를 제공하는 읽기 전용 donor다. 목표 플레이세트에서 donor와 compat port를 동시에 활성화하지 않는다.

현재 donor 전역 파일이 RT56 데이터를 덮어쓰므로 “HOK + RT56 + 얇은 patch” 3모드 구조는 기본안으로 채택하지 않는다. 나중에 이를 선택하려면 별도의 아키텍처 변경과 완전한 재검증이 필요하다.

### 3. compat port는 의도한 delta만 제공한다

호환 포트는 RT56 뒤의 유효 계층에서 HOK의 검토된 정의만 제공해야 한다. dependency 선언만 신뢰하지 않고 launcher .mod, 실제 물리 경로와 로그로 로드를 확인한다.

새로운 broad replace_path는 기본적으로 사용하지 않는다. 특히 RT56의 history/states와 map/strategicregions replace_path를 compat에 복사하지 않는다.

### 4. 새 업로드 정체성을 사용한다

- 2898629778: 역사적 HOK 원본, provenance 전용
- 3793992662: HOK donor descriptor의 revision, provenance 전용
- 820260968: RT56 dependency, provenance 전용
- compat port: 첫 신규 게시 전까지 ID 미할당

compat descriptor에는 첫 게시 전 remote_file_id를 넣지 않고, 위 ID를 복사하거나 업로드 대상으로 사용하지 않는다.

## 미결정: localisation

다음 두 구성을 비교해야 한다.

1. RT56 + Korean Language + compat
2. RT56 + RT56 Korean Translation + compat

필요하다면 두 구성을 별도 지원 대상으로 둘 수 있지만, 하나의 playset에서 두 번역 모드를 함께 켜는 것을 기본값으로 가정하지 않는다.

결정 기준:

- HOK l_english/l_korean 파일이 실제로 로드되는가
- RT56 Korean Translation의 replace_path=localisation이 HOK 키를 숨기는가
- Korean Language가 HOK의 기존 header/키 계약에 실제로 필요한가
- 영어·한국어 UI에서 누락·중복·잘못된 fallback이 없는가
- 배포 dependency와 사용자 설치 절차가 명확한가

후속 ADR이 localisation 결론, 지원 조합과 descriptor 값을 고정한다.

## 결과

장점:

- RT56의 세계 데이터와 공유 기능을 호스트가 계속 소유한다.
- HOK 고유 delta와 신규 포트 기여분의 provenance가 분명해진다.
- donor의 stale global file로 인한 무관한 회귀를 줄인다.

비용:

- 현재 donor 복제본을 파일별로 분류하고 상당수 전역 파일을 RT56에서 다시 병합해야 한다.
- 지도 province/state ID 충돌 때문에 신규 게임 중심의 명시적 migration이 필요하다.
- RT56 업데이트마다 override/merge ledger를 재검증해야 한다.

## 검증

최소 비교 조합은 RT56-only, RT56+선택 localisation, RT56+compat 및 RT56+선택 localisation+compat다. HOK donor는 목표 조합에서 비활성화한다.

이 ADR 자체와 저장소 descriptor의 정적 검사는 launcher나 런타임 통과를 증명하지 않는다.

저장소 descriptor의 정적 계약은 검사했다. 그러나 사용자 데이터의 `mod/hearts_of_korea_Road_to_56.mod`는 여전히 `version="1.0.0"`, 과거 표시명, Korean Language-only dependency를 가지며 저장소 path를 가리킨다. launcher가 이 외부 메타데이터를 사용하므로 C0/C1 실행 전에 재가져오기 또는 명시적 갱신과 물리 경로 확인이 필요하다. 해당 외부 파일은 이 구현에서 수정하지 않았다.

따라서 이 ADR의 dependency 설계와 저장소 반영은 완료됐지만 실제 launcher 계약과 런타임 통과는 아직 증명되지 않았다.
