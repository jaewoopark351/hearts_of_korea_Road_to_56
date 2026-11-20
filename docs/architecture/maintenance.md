# 구조 문서와 파생물 유지 안내

적용일: **2026-11-20, Asia/Seoul**. [AGENTS](../../AGENTS.md)와 [로컬 스킬](../skills/hok-rt56-architecture-diagrams/SKILL.md)을 적용한다. 현재 관계는 소스·ADR·대응표·최신 구현 기록으로 확인하고 역사 문서의 당시 상태를 자동 갱신하지 않는다.

## 원본·출력과 권한

각 주제 Markdown의 Mermaid 블록 한 곳이 편집 정본이다. 이미지·갤러리·manifest는 같은 정본에서 만든 파생물이다. 도표의 내용에 맞추려고 runtime·지도·보상·기존 저장을 변경하지 않는다. 현재 구현, 원본만 구현/포트 예정, 미확인 상태를 명시하며 소스·렌더링·표시·게임 증거를 별도로 기록한다.

문서 그림 생성이 승인된 작업에서만 렌더링한다. helper·라이브러리·임시 HTML·브라우저 프로필·초안·백업·검사 보고서는 `C:/hoi/test/<task-or-run-id>/`에 둔다. 승인된 최종 SVG/PNG·오프라인 갤러리·유지 manifest만 `docs/architecture/`에 둔다. 입력 capsule·활성 source cache는 시험 출력이 아니다. 렌더러 설치·새 도구 도입은 필요성과 기존 승인 범위를 먼저 확인한다.

<a id="always-dark"></a>

## 항상 다크

모든 Mermaid 블록에 `config: theme: dark`를 명시한다. Markdown 이미지·Mermaid 미리보기·SVG/PNG·확대/다운로드·HTML 갤러리·내보내기도 다크를 유지한다. 배경뿐 아니라 글자·도형·연결선 대비를 함께 확인한다. OS·브라우저의 라이트 모드와 과거 테마 저장값이 이를 해제하지 않게 한다. 게임 아트와 과거 증거 스크린샷을 재색칠하는 규칙이 아니다.

정식 파생물은 `images/Dxx.dark.svg/.png`, `states/images/Sxx.dark.svg/.png`다. donor의 기본명 호환 사본24개는 만들지 않는다. 현재 일반 도표 D01–D26와 State S01–S12를 전체 갤러리 **38개**로 제공하고 State 전용 갤러리도 유지한다. 갤러리는 객체 관계·시퀀스·구조/흐름별 바로 가기를 제공하며 외부 요청·CDN·테마 버튼·저장값 읽기 없이 파일만으로 열린다. 최초32개 도입의 수량·확인 결과는 당시 기록으로 보존한다.

## 어떤 변경이 어느 도표에 영향을 주는가

| 변경 | 대조할 도표·문서 | 근거 |
|---|---|---|
| 소스 역할·소유권·모듈 | D01/D02, overview | ADR-0004·descriptor·실제 소유 정의 |
| source/lock·cache·writer·finalizer·역투영 | D08/D20, source-and-generation | 담당 tools·입력 capsule·구현 기록 |
| scope·캐릭터·초기화 | D03/D04/D14/D18/D19, S03/S11 | 실제 호출부·history·character 역할 |
| 호출·중점 선행·배타·상대 배치 | D05/D06/D07/D15 | 효과·trigger·중점 소스·좌표 명세 |
| Province/State·지리 집합·지도 참조 | D09/D10, S01–S10 | ADR-0002/0006/0007·대응표·실제 부모 |
| 지역 사업 완료·가용/취소·저장 | S10/S11/S12 | CNDP trigger·결정·버전/주 표식 |
| 언어·키·GFX·payload·공급자 | D11/D12/D18 | 로컬 언어 정책·RTK·실제 sprite/texture |
| descriptor·launcher·유효 정의·저장 경로 | D13/D14 | 선언·물리 파일·관측한 구성 |
| 산둥 조건·본토·선택·전력·후속 | D15–D18, S07–S09 | 이번 포트 helper/lock·효과 순서·지리 적응 |
| 전체 runtime 상호작용·callback·저장 | D14/D21 | history·on_actions·기능별 guard·저장 정책 |
| 생성 요청·허용 선조·거부·owner additions | D08/D20/D22 | 실제 writer·finalize/preflight 함수·잠금 |
| 민주 지원·정보국·CNDP의 단계와 예외 | D23/D24/D25, S03/S11/S12 | 비용·타이머·기관 존재·완료/취소·재검사 |
| 언어/키·sprite에서 최종 payload 조회 | D11/D12/D26 | 실제 한/영 provider·GFX registry·파일 |

변경한 파일·ID·관계에서 시작해 관련 호출자·대체 분기를 읽는다. 질문·기준 소스·도표ID/anchor·범례·생략한 조건·확인 상태를 남긴다. 바뀐 관계를 정본에서 고친 뒤 해당 파생물·링크·manifest를 갱신한다. 관계가 같으면 유지 이유를 기록하고 그림 전체를 불필요하게 재생성하지 않는다. 도면 ID를 재배열하지 말고 새 도면은 추가한다.

## 재생성과 실제 기록

최초 helper·확인은 [도입 기록](../implementation/2026-11-20-architecture-diagram-adoption.md), 현재38개 상세화·재생성·보존 확인은 [후속 상세화 기록](../implementation/2026-11-20-architecture-detail-expansion.md), 현재 source/output 지문·도구는 [이미지 manifest](images/manifest.json)에 둔다. helper가 없어지면 manifest의 Mermaid 블록 해시·도구/글꼴/테마·생성 기준으로 새 외부 환경을 마련한다. 과거 helper의 donor 경로·예전 baseline·출력 경로를 현재 포트에 그대로 실행하지 않는다.

manifest는 source revision/미커밋 포함 여부, 원본 Markdown/anchor·블록 해시, 출력 해시·크기, 도구·글꼴·테마·생성 시점, source evidence 지문을 구분한다. 렌더 성공과 실제 한글·잘림·연결선 확인, 로컬 갤러리의 라이트 환경/좁은 폭 확인도 별도 보고한다. 문서 렌더의 통과를 HOI4의 등록·UI·효과·저장 통과로 바꾸지 않는다.

## 도표와 근거를 함께 읽기

| 표현 | 담는 정보 | 담지 않는 보증 |
|---|---|---|
| `classDiagram` | 정의·참조·초기화 데이터·실행 상태의 개념 관계 | 실제 C++ 클래스·상속·메모리 구조 |
| `sequenceDiagram` | 참여자·호출·조건 분기·상태 변경·정리의 순서 | 전 엔진 내부 호출 순서·모든 경로의 실행 성공 |
| `flowchart` | 출처·모듈·조건·후보·거부·소비자 관계 | 화살표만으로 결정되는 파일 로드 순서 |

각 그림에 질문·관계 범례·실제 경로·처리 대장·생략/미확인 범위를 둔다. 대표 호출부가 실제 그 경로를 쓰는지 대조하고, 폴더 묶음에 있는 모든 함수가 서로 호출된다고 그리지 않는다. State/Province/표시 키, Country/State/Character scope, 소유/통제/core, 개발 owner/게임 owner를 구분한다. 전체 그림은 코드 탐색 입구이며 모든 runtime ID의 전수 호출 그래프는 아니다.

## 원본 도입 출처

읽기 전용 HOK `f180bc8089e2a17f310b1fafa091d3f152063df3`의 `docs/architecture/`, `AGENTS.md`, `.agents/skills/hok-architecture-diagrams/SKILL.md`를 참고했다. 원본의 도표 질문·분리 원칙과 항상 다크 운영을 적응했고 포트 소스·언어·지도·생성 구조는 새로 작성했다. HOK 원작과 donor의 기여를 보존하며 원본 도표·출처를 신규 게임플레이 저작으로 표시하지 않는다. 원본 실행·이미지 제공 결과는 포트 증거가 아니다.

[목차](README.md) · [State](states/README.md) · [도입 계획](../plans/2026-11-20-architecture-diagram-adoption-plan.md)
