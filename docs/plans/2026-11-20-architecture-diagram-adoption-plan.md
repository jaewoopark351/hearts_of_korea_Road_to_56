# HOK RT56 구조 문서와 다이어그램 체계 도입 계획

작성일: **2026-11-20, Asia/Seoul**. 최초 문서화 당시 상태: **도입 방안 문서화만 승인 · 새 지침과 스킬 미적용 · 구조도와 갤러리 미작성**.

2026-11-20 후속 구현: 사용자의 전체 구현 승인으로 AGENTS 조건부 지침·로컬 스킬·호환판 구조 문서와 다크 그림/갤러리를 도입했다. 실제 적용·렌더링·표시 확인과 남은 범위는 [도입 기록](../implementation/2026-11-20-architecture-diagram-adoption.md)을 따른다. 아래 예정 경로·미작성/미실행 표는 최초 계획의 역사 기록이다.

원본의 AGENTS.md·다이어그램 SKILL.md·구조 문서·다크 이미지 갤러리를 참고해 호환판의 문서 체계를 설계한다. 공통 작성·갱신 방식은 따르되, 내용은 현재 RT56 통합 구조와 호환판의 지도 ID·언어·생성 소유권을 기준으로 작성한다. [민주인사 지원·산둥 정부 이식 계획](2026-11-19-korean-democratic-support-intelligence-port-plan.md)과 연결되는 별도 문서 작업이다.

사용자의 “이것도 문서화 작업만 진행해줘” 요청에 따라 도입 범위·예정 경로·갱신 절차를 기록한다. 이번에는 이 계획, 문서 인덱스, 기존 콘텐츠 이식 계획의 연결 안내만 편집한다. AGENTS.md·SKILL.md를 실제로 수정하거나 새 Mermaid·PNG·SVG·HTML·manifest를 만들지 않는다. 게임 코드·자산·생성기·잠금·원장·설정 변경, 도구 설치·렌더링·검사·게임 실행·정리·Git 변경·게시도 포함하지 않는다.

## 1. 기준과 먼저 읽을 자료

| 항목 | 기준과 역할 |
|---|---|
| 호환판 | `C:\hoi\hearts_of_korea_Road_to_56`, `feat/korean-focus-update-20260922@9a01955785bcdd827c9c85522537a0bfc57ed654` |
| 시작 시 기존 변경 | `docs/README.md` 수정과 미추적 콘텐츠 이식 계획1개가 존재한다. 앞선 승인된 문서 작업이며 보존한다. clean checkout으로 기술하지 않는다. |
| 원본 | `C:\hoi\hearts_of_korea`, `f180bc8089e2a17f310b1fafa091d3f152063df3`, 이번 조회 시 작업 트리 clean. 읽기 전용 출처다. |
| 원본 구조 문서의 내부 기준 | 최초 도표는 `0c19f58` 위 당시 미커밋 소스를 기준으로 작성됐다. 이후 `f180bc8`에 보존된 문서의 실제 내용과 과거 작성·렌더 이력을 구분한다. |
| 호환판의 기존 구조 안내 | `docs/PORTING_ARCHITECTURE.md`는 보존 원칙과 2026-09-06 상태를 함께 담고 있다. 새 현황은 최신 구현 기록·실제 소스에서 작성하고 과거 crash·검사 결과를 현재 결과로 복제하지 않는다. |
| 현재 도입 상태 | 호환판에는 새 `docs/architecture/` 묶음과 해당 전용 스킬이 아직 없다. 아래 경로와 구성은 예정안이다. |

| 후속 작업 조건 | 먼저 읽을 자료와 용도 |
|---|---|
| 도입 범위를 정하거나 지침을 실제로 수정할 때 | [AGENTS.md](../../AGENTS.md), [변경 영향 검토 절차](../HOK_CHANGE_COVERAGE_REVIEW.md). 요청 모드·보존 경계·문서 역할과 `docs/skills/`의 기존 운영 방식을 따른다. |
| 원본 지침·도표 구성을 적응할 때 | 원본 [다이어그램 SKILL.md](../../../hearts_of_korea/.agents/skills/hok-architecture-diagrams/SKILL.md), [구조 문서 목차](../../../hearts_of_korea/docs/architecture/README.md), [유지·갱신 안내](../../../hearts_of_korea/docs/architecture/maintenance.md). 현재 항상 다크 정책과 앞선 라이트·테마 전환 이력을 구분한다. |
| 한국·RT56 소유권이나 생성 구조를 그릴 때 | [ADR-0004](../decisions/0004-hok-korean-content-priority.md), [기존 포팅 아키텍처](../PORTING_ARCHITECTURE.md), [최신 지휘관 계층의 소유권](../implementation/2026-11-14-korean-commander-unlock-port.md). 오래된 상태를 최신으로 취급하지 않으며 실제 담당 생성기·입력·최종화 경로를 확인한다. |
| 지도·주 관계나 ID 대응을 그릴 때 | [주 참조 스킬](../skills/hok-rt56-state-reference-review/SKILL.md), [ADR-0002](../decisions/0002-map-id-migration.md), [ADR-0006](../decisions/0006-korean-state-split-integration.md), [분할 대응표](../data/HOK_KOREAN_STATE_SPLIT_PORT_MAPPING.json), [ADR-0007](../decisions/0007-november-content-integration.md). donor 지리와 포트 지리를 구분한다. |
| 현지화·이미지·이름의 표시 경로를 그릴 때 | [현지화 스킬](../skills/hok-rt56-localisation-review/SKILL.md), [ADR-0003](../decisions/0003-localisation-contract.md), [영어 이식 기록](../implementation/2026-10-20-english-localisation-import.md). 실제 영어·한국어, RTK 덮어쓰기와 관측한 구성을 구분한다. |
| 문서 그림을 생성하거나 과거 자료·렌더링 입력을 재사용할 때 | [개발 자료 안내](../HOK_DEVELOPMENT_ARTIFACT_ARCHIVE.md), 원본 [State 도표 목차](../../../hearts_of_korea/docs/architecture/states/README.md), [이미지 manifest](../../../hearts_of_korea/docs/architecture/states/images/manifest.json). 최종 문서 그림과 외부 helper·중간물·과거 증거의 역할을 구분한다. |

원본 링크는 현재 donor 파일을 가리킨다. 이번에 동결 사본이나 새 manifest를 만들지 않았다. 후속 도입에서 출처를 보관할 때에는 원본 커밋·checkout 줄 끝·아래 선택 SHA-256을 구분한다. 전체 소스의 무결성이나 그림 전체를 새로 검증한 기록은 아니다.

| 원본 상대 경로 | 이번 읽기 조회 SHA-256 |
|---|---|
| `AGENTS.md` | `80D70F1A87F7D63236DE9422F112B5A623630360D1ECA5CA86B673145F930871` |
| `.agents/skills/hok-architecture-diagrams/SKILL.md` | `12A0B169E6B6F2007CB76999EF28A5E1EA106DB838AEC0D4B1663E83C07CDC0F` |
| `docs/architecture/README.md` | `1D0AD47245E6CCB63FDFABB62199E351B08B5CE43B685E26C65FE0B7ABB04AD0` |
| `docs/architecture/maintenance.md` | `4264582DABA1220B20F53258679EB0AE81D79374B47FEDD7F27EB43CF2AEEE09` |
| `docs/architecture/states/images/manifest.json` | `BE1825D8F1E96F072732B5007797BA834C9326A299E5CEEC41563C736A3BECE2` |

## 2. AGENTS.md와 전용 스킬에 반영할 내용

다음은 **후속 도입안**이다. 현재 AGENTS의 규칙이 추가·변경된 것으로 해석하지 않는다.

AGENTS.md에는 공통 의무와 조건부 읽기 링크를 간결하게 둔다. 구조 검토 또는 파일 간 호출·scope·초기화·지도/표시 참조를 변경할 때 구조 목차와 유지 안내를 읽도록 연결한다. 문서 도표 작성·미리보기·렌더링·내보내기에는 전용 스킬을 연결한다. 관계가 바뀐 도표를 갱신하고 관계가 같으면 유지 이유를 남기는 원칙, 모든 문서 도표의 항상 다크 정책을 공통 규칙으로 제안한다. 상세 목록·명세·출처·검증 이력은 `docs/`에서 관리한다.

새 스킬의 예정 위치는 `docs/skills/hok-rt56-architecture-diagrams/SKILL.md`, 이름은 `hok-rt56-architecture-diagrams`다. 설명에는 HOK×RT56 구조도·문서 이미지·갤러리·내보내기에 적용하는 조건을 적는다. 기존 `.gitignore`의 `/.agents/` 제외와 [로컬 지침 운영 원칙](../HOK_CHANGE_COVERAGE_REVIEW.md)에 맞춰 AGENTS의 필수 읽기로 연결하며, 자동 탐색·전역 설치를 전제하지 않는다.

스킬에는 범위, 선행 문서, 항상 다크, Mermaid 원본과 파생물, 갱신 절차, 외부 중간물 위치, 확인 상태의 구분을 담는다. 기존 현지화·주 참조 스킬과 연결하고 ID 대응표·실행 수치·특정 기능의 조건을 중복 고정하지 않는다. 실제 스킬을 작성할 때는 당시 사용 가능한 skill-creator 지침을 적용한다. 이 계획 단계에서는 스킬 파일이나 검사기를 생성·실행하지 않는다.

원본 HOK의 새 지침은 출처로 보관할 수 있지만 호환판의 정체성·RT56 소유권·언어·생성 소유권 규칙은 로컬 지침을 따른다. 게임 아트와 기존 증거 스크린샷의 색을 바꾸는 규칙으로 확대하지 않는다.

## 3. 구조 문서의 예정 구성

아래 표의 경로는 **생성 예정**이며 이번에 작성한 파일이 아니다. 도표 수는 필요한 관계에 따라 정하고 원본의 파일 수나 도면 수를 복제 목표로 삼지 않는다.

| 예정 경로 | 설명할 관계와 근거 |
|---|---|
| `docs/architecture/README.md` | 질문별 진입 목차, 도면 ID·범례·갱신 조건, 전체 문서 읽기 경로 |
| `docs/architecture/maintenance.md` | 코드/문서 변경에서 관련 도표를 찾는 표, 작성 양식, 원본/파생물 정책, 확인·갱신 이력 |
| `docs/architecture/overview.md` | HOK donor·RT56·바닐라·호환판의 역할과 한국/세계/공유 소유권 |
| `docs/architecture/source-and-generation.md` | 고정 입력·capsule·외부 source cache → 담당 생성기/lock·최종화 → runtime 출력·통합 원장. 개발 작업의 생성 과정 |
| `docs/architecture/domain-model.md` | Country·State·인물·중점·결정의 정의·참조·소속·scope 개념 |
| `docs/architecture/content-flow.md` | 호출·조건·보상·재호출과 중점 선행/배타/상대 배치의 구분, 결정 해금·AI 연결 |
| `docs/architecture/map-data.md` | province 정체성과 State/전략 지역 소속, 철도·보급·건물 위치, 한국 이관과 RT56 세계 지도 |
| `docs/architecture/presentation-assets.md` | 한국어·실제 영어·RTK 표시 후보, 키→문자열과 sprite→texture/mask/overlay·초상화 연결 |
| `docs/architecture/load-and-lifecycle.md` | descriptor 선언·launcher 물리 경로·실제 로드 증거, 정의 등록·새 게임 history·효과 실행·저장 복원 |
| `docs/architecture/implemented-feature.md` | 현재 구현된 시민사회·CNDP·주 분할·지휘관 계층 등에서 적절한 사례를 선정해 여러 관점으로 설명. 최종 파일명은 선정 사례를 명확히 표현 |
| `docs/architecture/shandong-government.md` | 원본 구현과 포트 이식 예정의 호출·영토 선택·전력 이전·지도자·후속 인정. 실제 포트 적용 전에는 설계안으로 표시 |
| `docs/architecture/states/README.md` | State 상세 주제와 이미지 목록·갤러리 진입 |
| `docs/architecture/states/definition-and-scope.md` | 주 정의·history·런타임 데이터·Country/State scope |
| `docs/architecture/states/geography-and-splits.md` | donor→포트 ID 대응, 한국 15주, province 부모·전략 지역·영향 추적 |
| `docs/architecture/states/ownership-and-transfer.md` | 소유·통제·완전 통제·core/claim, 이전 적격·첫 거점·동적 생성국의 처리 순서 |
| `docs/architecture/states/change-impact.md` | 소비자·국가/주 표식·저장 경계·건설 공간과 유형별 상한 |
| `docs/architecture/states/images/` | 승인된 범위의 최종 다크 SVG/PNG·오프라인 `index.html`·`manifest.json` |

개발 생성 과정과 게임 수명주기를 각각 그린다. 게임이 Python 생성기를 실행하는 것처럼 연결하지 않는다. 생성 구조의 첫 근거는 [source_snapshot.py](../../tools/source_snapshot.py), [한국 분할 계층](../../tools/korean_state_split.py), [후속 수선 계층](../../tools/review_followup.py), [지휘관 최종 계층](../../tools/upstream_commanders.py)다. 실제 입력 공급자·최종화·역투영·preflight의 관계를 소스에서 확인한 뒤 화살표를 정한다.

기존 포팅 아키텍처와 ADR은 결정·출처를 맡고, 새 구조도는 현재 소스와 해당 근거로 찾아가는 연결을 맡는다. 전체 중점·키·수치 목록과 검증 보고서를 그림마다 복제하지 않는다.

## 4. 원본 도표에서 호환판으로 바꿔야 할 내용

| 후보 | 처리 | 호환판의 기대 내용과 근거 |
|---|---|---|
| 원본 AGENTS의 도표 필수 읽기·항상 다크 | **수정 제안** | 호환판 스킬·구조 문서의 상대 링크로 연결. 기존 요청 모드와 권한 경계 유지 |
| 원본 스킬의 원본/파생물·갱신 방식 | **수정 제안** | 로컬 `docs/skills/` 구조와 RT56 문서 역할에 적응 |
| 문서별 Mermaid 한 곳을 편집 원본으로 관리 | **의도적 유지 제안** | SVG/PNG·갤러리는 같은 원본에서 생성하며 별도 내용 원본으로 관리하지 않음 |
| 원본 D 도표의 기능·관계 구성 | **수정 제안** | 전체 구성·도메인·호출·수명주기·표시의 관점을 따르고 실제 포트 정의·호출자·파일로 다시 작성 |
| State S01–S12의 질문·분류 | **의도적 유지 제안** | 정의/scope·지리/분할·이전·저장/슬롯의 분류를 활용. 유지할 도면 ID·anchor와 도입 출처를 기록 |
| donor 한국 주 번호와 중국 본토 목록 | **수정 제안** | ADR-0002/0006/0007과 현행 포트 지리를 사용. 원본 S05의1030/1086 등을 포트920/1148 등의 대응으로 설명 |
| 원본의 두 locale 채널 한국어 본문 설명 | **수정 제안** | 포트 한국어와 실제 영어를 구분하고 RTK·replace/·동일 키의 표시 후보와 실제 관측을 분리 |
| 원본 HOK+외부 영어 번역 실행 도표 | **수정 제안** | RT56+호환판+선택 언어 구성과 물리 경로를 설명. donor는 읽기 전용 출처, 현재 설정 목록과 입증된 실행을 별도 표시 |
| 생성·입력 소유권 도표 | **추가 제안** | 기존 lock·capsule·외부 캐시·생성 출력·역투영·원장을 연결. 어떤 파일을 어느 소유자를 통해 바꾸는지 설명 |
| 산둥 사례를 현재 구현으로 표시 | **미확인 / 이식 예정** | 원본 구현과 포트 계획을 명시. 포트 구현 완료 뒤 해당 소스·검증 상태에 맞춰 갱신 |
| 원본의 과거 렌더·UI·효과·저장 결과 | **제외** | 출처 링크와 당시 조건을 유지하며 포트의 새 확인 결과로 집계하지 않음 |
| 기존 코드·지도·보상·생성 구조의 재설계 | **제외** | 도표는 확인한 관계를 설명. 문서에 맞추기 위한 runtime 수리나 구조 변경은 별도 범위 |

클래스 모양은 개념 관계를 표현한다. 실제 엔진의 C++ 클래스·상속을 복원했다고 설명하지 않는다. 호출·참조·평가 조건·초기화·표시를 라벨과 범례로 구분하고, 중점 선행과 `relative_position_id` 배치는 별개로 그린다. 도표의 상자 위치도 실제 HOI4 좌표나 UI 검증을 뜻하지 않는다.

## 5. 그림·갤러리·출처 관리 계획

모든 Mermaid 원본에 `config`의 `theme: dark`를 명시한다. Markdown 미리보기·최종 PNG/SVG·갤러리·확대/다운로드 링크·내보내기도 같은 다크 표시를 사용한다. OS·뷰어의 라이트 설정이나 과거 저장된 테마가 이를 해제하지 않도록 한다. 배경뿐 아니라 도형·문자·연결선도 함께 읽을 수 있어야 한다.

State의 예정 정식 파일은 `Sxx.dark.svg`·`Sxx.dark.png`다. 원본의 기본 파일명 다크 사본은 기존 링크의 호환을 위한 것이다. 우리 쪽은 실제 이전 링크를 유지해야 할 경우에만 호환 사본을 두고 그 목적과 정식 파일의 관계를 기록한다. 신규 링크는 정식 다크 파일을 사용한다. 일반 구조도도 승인된 이미지 제공 범위를 정해 같은 방식으로 연결한다.

최종 문서 그림과 오프라인 갤러리는 유지 문서의 파생물이다. 저장소에는 승인된 최종 파일을 두고, 렌더러·라이브러리·임시 HTML·프로필·초안·백업·검사 보고서는 먼저 정한 `C:\hoi\test\<task-or-run-id>\`에 둔다. 기존 외부 source cache나 게임 이미지 폴더를 문서 렌더링 작업 공간으로 사용하지 않는다. 이번에는 그 작업 경로·도구 환경이나 파일을 만들지 않는다.

미래 manifest에는 도면 ID·제목·원본 Markdown/anchor·Mermaid 해시·최종 SVG/PNG 해시·바이트 크기·도구/글꼴/테마 설정·생성 시점과 source revision을 기록한다. 이전 이미지를 유지했다면 그 사유·대응 원본을 구분한다. donor manifest의 과거 `sourceHead`·미커밋 표시·외부 helper 경로를 포트의 새 생성 기록으로 복사하지 않는다.

## 6. 갱신 조건과 순서

| 바뀌는 관계 | 우선 확인할 문서·도표 |
|---|---|
| 모듈·경로·소유권 | 전체 구성·source/generation·목차 |
| 중점 선행·배타·상대 배치·보상 호출·결정 해금 | 콘텐츠 연결, 실제 좌표 명세, 해당 기능 사례 |
| shared effect/trigger·사건·on_action·scope·처리 시점 | 콘텐츠 연결·도메인·수명주기와 관련 호출자/대체 분기 |
| 국가/주 history·인물 모집/이동/승격 | 도메인·수명주기·표시와 해당 기능의 순서도 |
| state/province·영토·코어·수도·보급·사업 표식 | 지도·State 상세·기능 사례. 지도 파일이 그대로여도 콘텐츠 대상 변경을 추적 |
| 언어·키·GFX·texture/mask·초상화 | 표시 자산·공유 소비자·실제 선택 언어 구성 |
| source/lock·캐시·writer·최종화/역투영 | 생성 과정·입력/출력 소유권과 관련 구현 기록 |
| descriptor·launcher·로드/저장 경로 | 로드와 수명주기. 선언·선택·관측된 유효 정의를 구분 |

후속 작업에서는 변경한 파일·ID·관계에서 시작해 해당 도표를 찾고 실제 소스·명세와 대조한다. 바뀐 관계와 관련 설명을 수정한 뒤 해당 원본에서 그림·링크·갤러리·manifest를 갱신한다. 원본 관계가 같으면 그림을 유지한 이유를 기록한다. 보상 숫자나 문구 변경만으로 모든 도표를 다시 만들거나 날짜를 일괄 갱신하지 않는다.

도표별로 질문·기준 소스·현재/예정 상태·안정 ID/anchor·범례·생략한 분기·근거 파일·갱신 조건·확인 상태를 둔다. 출처 도면 번호를 유지하는 경우에도 포트에 실제 적용된 범위와 수정 내용을 명시한다. 새 도면은 기존 번호를 재배열하지 않고 추가한다.

## 7. 확인 단계와 도입 완료 기준

| 단계 | 완료로 기록할 수 있는 내용 | 이번 상태 |
|---|---|---|
| 도입 계획 | 지침/스킬·문서/그림 구성·포트 적응·갱신·확인 범위의 문서화 | 이 계획에 기록 |
| 지침·스킬 적용 | AGENTS의 유효한 조건부 링크와 작성된 로컬 스킬, 상대 경로·역할·권한 일치 | 미적용 |
| 구조 설명 | 최신 소스·담당 생성기·참조·scope와 대응한 Mermaid, 현재 구현/설계/미확인의 명확한 구분 | 미작성 |
| 렌더링 | 승인한 원본에서 실제 다크 SVG/PNG·갤러리·manifest 생성 | 미실행 |
| 표시 확인 | 한글·연결선·잘림·가독성, 라이트 환경에서도 다크 유지, 이미지/링크 일치·갤러리 로컬 표시 확인 | 미실행 |
| 게임 UI·효과·저장 | 해당 게임 버전·RT56·언어·DLC·소스에서 실제 관측한 범위 | 이번 문서 체계 도입의 통과 기준과 별개. 새 실행 없음 |

원본의 Mermaid 문서·유지 정책과 대표 이미지 S01·S05·S09는 앞선 설명 단계에서 직접 읽고 보았다. 갤러리 HTML·manifest도 읽었지만, 우리 쪽 렌더링·갤러리 실행이나 원본 전체 이미지의 신규 시각 검증을 수행한 것은 아니다. 이번에는 관련 문서·선택 출처 지문·문서 간 연결을 읽어 대조했다.

후속 도입 완료는 지침/스킬과 구조 문서만 작성한 단계, 실제 그림을 제공한 단계, 표시까지 확인한 단계를 구분해 보고한다. 그림이 만들어졌다는 사실을 게임 호환성·정상 로드·효과·기존 저장의 검증으로 바꾸지 않는다. 원본의 과거 실행은 그 소스와 구성에 한정하며 포트의 현황은 최신 로컬 구현 기록으로 연결한다.

## 8. 이번 편집 범위와 후속 작업

이번 문서 작업은 이 계획을 추가하고 [문서 인덱스](../README.md)와 [기존 콘텐츠 이식 계획](2026-11-19-korean-democratic-support-intelligence-port-plan.md)에 조건부 읽기와 후속 연결을 추가한다. 기존 두 문서의 앞선 변경을 보존한다. 콘텐츠 이식 계획의 당시 “이 계획과 인덱스만 변경” 기록은 앞선 작업의 범위로 유지하며 이번 세 문서 편집과 구분한다.

실제 도입이 승인되면 최신 소스를 다시 확인하고 AGENTS의 간결한 규칙·로컬 스킬과 목차/유지 안내를 연결한 뒤, 현재 구현 사례와 생성/지도/표시 구조를 작성한다. 산둥은 이식 전 설계로 연결한다. 최종 문서 이미지·갤러리 제공 범위와 도구 환경을 정하고 외부 작업 위치에서 생성·표시를 확인한 다음 승인된 최종 문서 파생물만 반영한다. 실제 적용·렌더링 결과는 별도 도입 기록으로 남긴다.

새 helper·검사기·미리보기·백업·진단 파일은 만들지 않았다. 앞선 검토에서 확인한 `tools/__pycache__/`21파일·1,088,888바이트는 정리 미결로 유지하며 이번에 이동·삭제하거나 재측정하지 않는다. 원본·Workshop·설치 게임·사용자 데이터·기존 외부 자료·source cache는 수정하지 않았고 커밋·푸시·게시·업로드는 수행하지 않는다.
