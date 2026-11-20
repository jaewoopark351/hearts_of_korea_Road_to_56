# State 상세 구조도 S01–S12

기준: **2026-11-20, Asia/Seoul**. 현재 미커밋 소스에서 S01–S12 전체를 상세화했다. State는 지리 주이며 상태 머신을 뜻하지 않는다. 개념 UML은 엔진의 실제 C++ 클래스 복원이 아니다. 코드·지도·게임 설정은 변경하지 않았다. 실제 문서 파생물 확인은 [후속 상세화 기록](../../implementation/2026-11-20-architecture-detail-expansion.md)을 따른다.

[State 다크 갤러리](images/index.html) · [전체 구조 목차](../README.md) · [유지 안내](../maintenance.md) · [State 이미지 manifest](images/manifest.json)

| 질문 | 먼저 읽을 문서 |
|---|---|
| 주 필드·ID·scope | [정의](definition-and-scope.md) |
| Province 부모·전략 지역·분할 | [지리](geography-and-splits.md) |
| 소유·완전 통제·core·이전 | [영토 관계](ownership-and-transfer.md) |
| 소비자·버전/완료 표식·저장·슬롯 | [변경 영향](change-impact.md) |

| 설명·Mermaid 정본 | 이미지 |
|---|---|
| [S01 · 주 데이터와 국가·프로빈스 관계](definition-and-scope.md#s01-state-concept) | [PNG](images/S01.dark.png) · [SVG](images/S01.dark.svg) |
| [S02 · 황해남917의 실제 중첩과 토큰](definition-and-scope.md#s02-state-file-tree) | [PNG](images/S02.dark.png) · [SVG](images/S02.dark.svg) |
| [S03 · Country 조건과 State 조건의 분리](definition-and-scope.md#s03-country-state-scope) | [PNG](images/S03.dark.png) · [SVG](images/S03.dark.svg) |
| [S04 · 서로 다른 지리 집합과 네트워크](geography-and-splits.md#s04-province-state-region) | [PNG](images/S04.dark.png) · [SVG](images/S04.dark.svg) |
| [S05 · 한국9→15주 전체 분할과 포트ID 대응](geography-and-splits.md#s05-korean-split-map) | [PNG](images/S05.dark.png) · [SVG](images/S05.dark.svg) |
| [S06 · 지역이 바뀔 때 따라갈 소비자](geography-and-splits.md#s06-reference-closure) | [PNG](images/S06.dark.png) · [SVG](images/S06.dark.svg) |
| [S07 · 국가와 주의 서로 다른 관계](ownership-and-transfer.md#s07-country-state-relations) | [PNG](images/S07.dark.png) · [SVG](images/S07.dark.svg) |
| [S08 · 이전 적격과 안전한 첫 거점](ownership-and-transfer.md#s08-transfer-eligibility) | [PNG](images/S08.dark.png) · [SVG](images/S08.dark.svg) |
| [S09 · 선택 표식과 실제 영토 이전](ownership-and-transfer.md#s09-selection-and-transfer) | [PNG](images/S09.dark.png) · [SVG](images/S09.dark.svg) |
| [S10 · 주 데이터의 영향 범위](change-impact.md#s10-state-consumers) | [PNG](images/S10.dark.png) · [SVG](images/S10.dark.svg) |
| [S11 · 국가 버전 표식과 주별 완료 표식](change-impact.md#s11-project-version-and-save) | [PNG](images/S11.dark.png) · [SVG](images/S11.dark.svg) |
| [S12 · 기본 공간·추가 슬롯·공유/유형별 상한](change-impact.md#s12-building-space) | [PNG](images/S12.dark.png) · [SVG](images/S12.dark.svg) |

지리·지역 대상을 검토하거나 바꾸기 전에 [주 참조 스킬](../../skills/hok-rt56-state-reference-review/SKILL.md), [변경 영향 절차](../../HOK_CHANGE_COVERAGE_REVIEW.md), [ADR-0002](../../decisions/0002-map-id-migration.md)·[0006](../../decisions/0006-korean-state-split-integration.md)·[0007](../../decisions/0007-november-content-integration.md)을 읽는다. 실제 한국15주와 전체 대응은 [대응표](../../data/HOK_KOREAN_STATE_SPLIT_PORT_MAPPING.json)를 정본으로 한다.

원본 S01–S12의 질문·분류·ID를 적응했으며 내부 내용과 소스 링크는 포트 기준으로 다시 썼다. 새 PNG/SVG는 현재 Mermaid에서 생성한다. donor의 기존 라이트/다크 파일·기본명 호환 사본을 복사한 그림이 아니다. 파생물의 실제 생성·표시 확인은 [로컬 도입 기록](../../implementation/2026-11-20-architecture-diagram-adoption.md)에 분리한다.

이번에는 일부 분할 예시에 머물렀던 그림을 한국15주 전체 관계로 확장하고, 실제 State 항목·자료형 구분·여러 scope 전환·이전 거부/일반/거점 분기·S09 시퀀스·소비자·저장·건설 조회를 상세화했다. 개별 수치/프로빈스 전체 대장은 JSON 대응표에 유지한다. RT56 전 세계 모든 주의 전수 그래프·지리 정합성 감사 또는 모든 조건의 실제 게임 실행 결과를 의미하지 않는다.
