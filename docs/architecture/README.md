# HOK×RT56 구조 문서와 다크 다이어그램

기준: **2026-11-20, Asia/Seoul**. 현재 미커밋 포트 소스를 읽고 전체 도표를 상세화한 문서다. **D01–D26 + S01–S12, 총38개**의 Mermaid 정본과 다크 파생물·갤러리를 제공한다. 최초32개 도입은 [도입 기록](../implementation/2026-11-20-architecture-diagram-adoption.md), 이번 보강·실제 문서 확인은 [상세화 기록](../implementation/2026-11-20-architecture-detail-expansion.md)을 따른다. 게임 UI·효과·저장은 [콘텐츠 구현 기록](../implementation/2026-11-20-korean-democratic-support-intelligence-port.md)의 당시 소스·조건에 한정한다.

[전체 오프라인 다크 갤러리](images/index.html) · [State 갤러리](states/images/index.html) · [이미지 manifest](images/manifest.json) · [유지·갱신 안내](maintenance.md) · [문서 인덱스](../README.md)

## 어떤 문서를 먼저 읽는가

| 다룰 관계 | 문서 |
|---|---|
| 네 소스·한국/세계 소유권 | [전체 구성](overview.md) |
| 생성기·잠금·최종화·역투영 | [개발 생성 과정](source-and-generation.md) |
| 국가·주·인물·scope | [도메인](domain-model.md) |
| 호출·조건·중점 선행/배치 | [콘텐츠 연결](content-flow.md) |
| 지도·ID·한국15주 | [지도](map-data.md), [State 상세](states/README.md) |
| 실제 영어·한국어·RTK·sprite/payload | [표시](presentation-assets.md) |
| 물리 경로·등록·history·저장 | [로드와 수명주기](load-and-lifecycle.md) |
| 현재 지휘관 계층의 구 저장 guard | [구현 사례](commander-unlock.md) |
| 이번 산둥·민주 지원 이식 | [산둥 사례](shandong-government.md) |

## 객체 관계와 시퀀스를 바로 찾기

| 원하는 그림 | 편집 정본 |
|---|---|
| 프로젝트 객체·콘텐츠 관계 | [D03](domain-model.md#d03-domain-relations) |
| State 정의·초기화·실행 데이터 / 국가·주·프로빈스 관계 | [S01](states/definition-and-scope.md#s01-state-concept), [S07](states/ownership-and-transfer.md#s07-country-state-relations) |
| 프로젝트 전체 실행·저장 | [D21](load-and-lifecycle.md#d21-project-runtime-sequence) |
| 개발 생성·후속 계층·거부·원장 | [D22](source-and-generation.md#d22-development-sequence) |
| 산둥 전체 출범 / 주별 이전과 자산 순서 | [D16](shandong-government.md#d16-formation-order), [S09](states/ownership-and-transfer.md#s09-selection-and-transfer) |
| 반복 민주 지원 / 정보국 / CNDP 주별 사업 | [D23](content-flow.md#d23-support-cycle), [D24](content-flow.md#d24-intelligence-sequence), [D25](content-flow.md#d25-cndp-sequence) |
| 문자열·그림 조회 | [D26](presentation-assets.md#d26-presentation-sequence) |

클래스 모양은 실제 소스의 개념 관계이며 C++ 구현 복원이 아니다. 시퀀스는 역할·효과의 순서를 보여 주며 엔진 내부의 모든 DB 로드 순서나 게임 실행 성공을 보장하지 않는다. 전체 개요 → 주제별 상세 → 실제 사례·소스 순서로 읽는다.

도표·문서 그림·갤러리를 작성·수정·미리보기·내보내기 전에 [로컬 다이어그램 스킬](../skills/hok-rt56-architecture-diagrams/SKILL.md)과 [유지 안내](maintenance.md)를 읽는다. 지리/표시 작업에는 기존 [주 참조](../skills/hok-rt56-state-reference-review/SKILL.md)·[현지화](../skills/hok-rt56-localisation-review/SKILL.md) 스킬과 [변경 영향 절차](../HOK_CHANGE_COVERAGE_REVIEW.md)를 함께 적용한다. 이 링크는 새 작업 권한을 부여하지 않는다.

## 도표 목차

모든 이미지·Mermaid 원본·확대/다운로드·갤러리는 **항상 다크**다. Markdown의 Mermaid 블록이 유일한 편집 원본이고 PNG/SVG는 파생물이다. 실선·점선은 각 그림의 범례를 따르며 서로 다른 문서의 선 모양만으로 같은 의미를 추론하지 않는다.

| 설명·편집 원본 | 다크 이미지 |
|---|---|
| [D01 · 네 소스와 하나의 작업 결과](overview.md#d01-source-ownership) | [PNG](images/D01.dark.png) · [SVG](images/D01.dark.svg) |
| [D02 · 게임 콘텐츠 모듈과 공용 접점](overview.md#d02-content-modules) | [PNG](images/D02.dark.png) · [SVG](images/D02.dark.svg) |
| [D03 · 국가·주·인물·조건·효과·표시의 관계](domain-model.md#d03-domain-relations) | [PNG](images/D03.dark.png) · [SVG](images/D03.dark.svg) |
| [D04 · 실제 호출부에서 PREV를 결정하는 세 경로](domain-model.md#d04-scope-context) | [PNG](images/D04.dark.png) · [SVG](images/D04.dark.svg) |
| [D05 · 진입점에서 조건·효과·데이터까지](content-flow.md#d05-call-and-reference) | [PNG](images/D05.dark.png) · [SVG](images/D05.dark.svg) |
| [D06 · 직접 선행·상호 배타·별도 가용 조건](content-flow.md#d06-focus-prerequisite) | [PNG](images/D06.dark.png) · [SVG](images/D06.dark.svg) |
| [D07 · 실제 relative_position_id와 로컬 좌표](content-flow.md#d07-focus-placement) | [PNG](images/D07.dark.png) · [SVG](images/D07.dark.svg) |
| [D08 · 입력에서 runtime과 원장까지](source-and-generation.md#d08-generation-pipeline) | [PNG](images/D08.dark.png) · [SVG](images/D08.dark.svg) |
| [D09 · 좌표·Province·State·전략 지역과 토폴로지](map-data.md#d09-map-databases) | [PNG](images/D09.dark.png) · [SVG](images/D09.dark.svg) |
| [D10 · 지도 이관·주 분할·콘텐츠 지역 정렬의 구분](map-data.md#d10-map-migration) | [PNG](images/D10.dark.png) · [SVG](images/D10.dark.svg) |
| [D11 · 소비자·언어·덮어쓰기 후보에서 문자열 치환까지](presentation-assets.md#d11-localisation-resolution) | [PNG](images/D11.dark.png) · [SVG](images/D11.dark.svg) |
| [D12 · 콘텐츠·sprite·shader·모델·음성 registry와 payload](presentation-assets.md#d12-sprite-payload) | [PNG](images/D12.dark.png) · [SVG](images/D12.dark.svg) |
| [D13 · 목표 구성과 읽기 전용 출처](load-and-lifecycle.md#d13-physical-sources) | [PNG](images/D13.dark.png) · [SVG](images/D13.dark.svg) |
| [D14 · 등록·새 게임·저장 복원의 구분](load-and-lifecycle.md#d14-runtime-lifecycle) | [PNG](images/D14.dark.png) · [SVG](images/D14.dark.svg) |
| [D15 · 중점·공유 조건·공용 핵심주·후속 인정](shandong-government.md#d15-call-and-shared-guards) | [PNG](images/D15.dark.png) · [SVG](images/D15.dark.svg) |
| [D16 · 한국·원국·생성국의 실제 처리 순서](shandong-government.md#d16-formation-order) | [PNG](images/D16.dark.png) · [SVG](images/D16.dark.svg) |
| [D17 · 기본 영토·연결 확장·항공기·SND 잔여 분기](shandong-government.md#d17-territory-and-remainders) | [PNG](images/D17.dark.png) · [SVG](images/D17.dark.svg) |
| [D18 · 전용 웡원하오의 정의·초기 모집·이동·승격·표시](shandong-government.md#d18-character-lifecycle) | [PNG](images/D18.dark.png) · [SVG](images/D18.dark.svg) |
| [D19 · 모집된 인물의 역할·중점 해금·기존 저장 분기](commander-unlock.md#d19-commander-save-guard) | [PNG](images/D19.dark.png) · [SVG](images/D19.dark.svg) |
| [D20 · 최종 바이트 검사와 과거 계약의 역투영](source-and-generation.md#d20-raw-and-historical) | [PNG](images/D20.dark.png) · [SVG](images/D20.dark.svg) |
| [D21 · 프로젝트 전체 실행 경계와 저장의 시퀀스](load-and-lifecycle.md#d21-project-runtime-sequence) | [PNG](images/D21.dark.png) · [SVG](images/D21.dark.svg) |
| [D22 · 개발 생성·거부·문서 갱신의 시퀀스](source-and-generation.md#d22-development-sequence) | [PNG](images/D22.dark.png) · [SVG](images/D22.dark.svg) |
| [D23 · 반복 민주 지원의 구매·중복 차단·만료](content-flow.md#d23-support-cycle) | [PNG](images/D23.dark.png) · [SVG](images/D23.dark.svg) |
| [D24 · 정보국 중점과 기존 기관 재사용](content-flow.md#d24-intelligence-sequence) | [PNG](images/D24.dark.png) · [SVG](images/D24.dark.svg) |
| [D25 · CNDP 전북 사업의 착수·취소·종료 재검사](content-flow.md#d25-cndp-sequence) | [PNG](images/D25.dark.png) · [SVG](images/D25.dark.svg) |
| [D26 · 표시 요청에서 최종 문자열·그림까지의 시퀀스](presentation-assets.md#d26-presentation-sequence) | [PNG](images/D26.dark.png) · [SVG](images/D26.dark.svg) |
| [S01 · 주 데이터와 국가·프로빈스 관계](states/definition-and-scope.md#s01-state-concept) | [PNG](states/images/S01.dark.png) · [SVG](states/images/S01.dark.svg) |
| [S02 · 황해남917의 실제 중첩과 토큰](states/definition-and-scope.md#s02-state-file-tree) | [PNG](states/images/S02.dark.png) · [SVG](states/images/S02.dark.svg) |
| [S03 · Country 조건과 State 조건의 분리](states/definition-and-scope.md#s03-country-state-scope) | [PNG](states/images/S03.dark.png) · [SVG](states/images/S03.dark.svg) |
| [S04 · 서로 다른 지리 집합과 네트워크](states/geography-and-splits.md#s04-province-state-region) | [PNG](states/images/S04.dark.png) · [SVG](states/images/S04.dark.svg) |
| [S05 · 한국9→15주 전체 분할과 포트ID 대응](states/geography-and-splits.md#s05-korean-split-map) | [PNG](states/images/S05.dark.png) · [SVG](states/images/S05.dark.svg) |
| [S06 · 지역이 바뀔 때 따라갈 소비자](states/geography-and-splits.md#s06-reference-closure) | [PNG](states/images/S06.dark.png) · [SVG](states/images/S06.dark.svg) |
| [S07 · 국가와 주의 서로 다른 관계](states/ownership-and-transfer.md#s07-country-state-relations) | [PNG](states/images/S07.dark.png) · [SVG](states/images/S07.dark.svg) |
| [S08 · 이전 적격과 안전한 첫 거점](states/ownership-and-transfer.md#s08-transfer-eligibility) | [PNG](states/images/S08.dark.png) · [SVG](states/images/S08.dark.svg) |
| [S09 · 선택 표식과 실제 영토 이전](states/ownership-and-transfer.md#s09-selection-and-transfer) | [PNG](states/images/S09.dark.png) · [SVG](states/images/S09.dark.svg) |
| [S10 · 주 데이터의 영향 범위](states/change-impact.md#s10-state-consumers) | [PNG](states/images/S10.dark.png) · [SVG](states/images/S10.dark.svg) |
| [S11 · 국가 버전 표식과 주별 완료 표식](states/change-impact.md#s11-project-version-and-save) | [PNG](states/images/S11.dark.png) · [SVG](states/images/S11.dark.svg) |
| [S12 · 기본 공간·추가 슬롯·공유/유형별 상한](states/change-impact.md#s12-building-space) | [PNG](states/images/S12.dark.png) · [SVG](states/images/S12.dark.svg) |

기준 소스·생략 범위·갱신 조건을 각 페이지와 [유지 표](maintenance.md)에 둔다. 원본 도면의 질문·ID 체계를 적응했고 D08/D20의 포트 생성 구조와 D19의 지휘관 사례는 로컬 내용이다. 원본의 실행·도표 제작 실적을 이번 포트의 결과로 합산하지 않는다.
