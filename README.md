# Hearts of Korea × The Road to 56 Compatibility

> 상태: **개발 초기 / 호환성 미완료**
> 2026-09-06 기준, HOI4 1.19.2 시작 크래시와 RT56 지도 충돌이 확인되었다. 현재 이름이나 `supported_version` 선언은 호환 완료를 뜻하지 않는다.

이 저장소는 Hearts of Korea(HOK)의 의도와 고유 콘텐츠를 **The Road to 56(RT56)을 런타임 기반으로 삼아 다시 이식하는 별도 신규 모드**다. HOK 원본 계보, 사용자 제공 HOK 기준 스냅샷, RT56 및 바닐라 중 어느 것도 이 저장소 자체의 업로드 정체성이 아니다.

## 통합 모델

```text
HOI4 1.19.x
  + The Road to 56                    # 호스트 데이터와 전 세계 기준
  + 이 HOK–RT56 호환 포트             # 검토된 HOK 차이만 제공
  + localisation 구성                 # 별도 결정 후 고정
```

- 사용자 제공 HOK 폴더는 콘텐츠 의도·자산·출처를 확인하는 **읽기 전용 donor**다. 기본 플레이세트에서 이 신규 포트와 함께 활성화하지 않는다.
- RT56은 공유 시스템, 전 세계 지도, 비한국 콘텐츠의 **호스트 기준**이다.
- 바닐라는 엔진 문법·스키마·동작을 판단하는 기준이다.
- 충돌 파일은 donor 전체를 복사하지 않고, 현재 RT56 파일에 필요한 HOK 차이만 다시 적용한다.

## 기준 경로

| 별칭 | 경로 | 역할 |
|---|---|---|
| `<COMPAT_ROOT>` | `C:\hoi\hearts_of_korea_Road_to_56` | 유일한 기본 쓰기 대상, 신규 모드 소스 |
| `<HOK_DONOR>` | `C:\hoi\hearts_of_korea` | 읽기 전용 HOK donor/provenance |
| `<RT56_SOURCE>` | `C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968` | 읽기 전용 RT56 Workshop 스냅샷 |
| `<VANILLA_SOURCE>` | `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV` | 읽기 전용 HOI4 기준 |
| `<HOI4_LOGS>` | `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV\logs` | 읽기 전용 런타임 증거 |

Steam은 RT56 소스를 자동 갱신할 수 있다. 비교·구현·검증을 시작할 때마다 RT56 descriptor와 핵심 파일의 시각·해시를 새 기준선에 고정한다.

## 현재 확인된 상태

- 문서 개편 전 프로덕션 트리의 비교 가능한 1,014개 파일 중 `descriptor.mod`를 제외한 파일은 `<HOK_DONOR>`와 동일했다. 즉 현재 트리는 아직 RT56 포트라기보다 donor 복제본에 가깝다.
- 현재 프로젝트와 RT56 사이에 같은 상대경로 파일이 73개 있다. 전역 지도, state, 전략 지역, bookmark, 공용 MIO, medal trigger, on_action, 일본·중국 콘텐츠 등이 포함된다.
- HOK donor의 추가 province ID `13414–13447` 34개는 RT56의 같은 ID 34개와 전부 다른 정의다. ID 보존만으로 합칠 수 없으며 명시적인 지도 ID 마이그레이션이 필요하다.
- 현재 프로젝트의 `map/definition.csv`는 `13447`에서 끝나지만 RT56은 `13534`까지 사용한다. 실제 로그에는 RT56 state가 참조한 `13448–13534` 87개 province의 누락이 기록됐다.
- 현재 `descriptor.mod`는 `Korean Language`만 의존성으로 선언하고 RT56을 선언하지 않는다. 2026-09-06 실패 플레이세트에는 대신 `The Road to 56 Korean Translation`이 활성화되어 있었다. 최종 localisation 계약은 아직 미결정이다.

자세한 증거와 등급은 [2026-09-06 시작 크래시 조사](docs/incidents/2026-09-06-startup-crash.md)를 참조한다.

## 작업 원칙

1. 목표는 `RT56 + 검토된 HOK delta`이며 `HOK 전체 복사본 + RT56`이 아니다.
2. HOK 고유 한국 콘텐츠와 정체성은 보존하고, RT56의 전 세계 데이터와 공유 시스템은 보존한다.
3. 한국 관련 양쪽 변경이 충돌하면 자동 우선순위를 두지 않고 결정 기록을 남긴다.
4. 같은 경로뿐 아니라 event, focus, state, character, idea 등 같은 논리 ID의 충돌도 검사한다.
5. 전역 단일 파일이 필요하면 현재 RT56을 base로 합성한다. donor의 `definition.csv`나 `provinces.bmp`를 그대로 싣지 않는다.
6. 호환성 수정, 원본 버그 수정, 리밸런스, 신규 콘텐츠는 별도 작업으로 관리한다.
7. 신규 게임 검증이 끝나기 전에는 기존 HOK 세이브 호환성을 주장하지 않는다.
8. 게임 실행, launcher 설정 변경, Git 작업, 외부 게시·업로드는 각각 별도 명시 요청이 있을 때만 한다.

## 문서

- [문서 인덱스](docs/README.md)
- [포팅 아키텍처](docs/PORTING_ARCHITECTURE.md)
- [포팅·검증 워크플로](docs/PORTING_WORKFLOW.md)
- [2026-09-06 프로젝트 기준선](docs/baselines/2026-09-06-project-baseline.md)
- [2026-09-06 exact-path 충돌 인벤토리](docs/audits/2026-09-06-exact-path-collision-inventory.md)
- [ADR-0001: 런타임 의존성과 로드 구성](docs/decisions/0001-runtime-dependencies-and-load-order.md)
- [2026-09-06 시작 크래시 조사](docs/incidents/2026-09-06-startup-crash.md)

## 출처와 배포 정체성

- `2898629778`: 역사적 HOK 원본 Workshop 항목 — provenance 전용
- `3793992662`: 사용자 제공 HOK donor descriptor의 항목 — provenance 전용
- `820260968`: The Road to 56 — 런타임 의존성/provenance 전용
- 이 신규 호환 모드: 첫 신규 게시 전까지 Workshop ID 미할당

새 모드는 위 세 ID 어느 것도 상속하거나 업로드 대상으로 사용하지 않는다. HOK 원작자, donor 개정 기여자, RT56 팀, localisation 및 제3자 기여자를 구분해 크레딧하며, 근거 없이 HOK 또는 RT56의 “공식” 버전으로 표현하지 않는다.
