# 2026-11-20 프로젝트 전체 구조도 상세화

상태: **기존32개 전체 상세화·신규6개 추가·다크 파생물 및 갤러리 갱신 완료**. 현재 정본은38개(객체 관계3·시퀀스8·구조/흐름27)다. 아래 문서 확인과 소스 보존 결과에 한정하며 게임 실행 검증은 하지 않았다. 앞선 [최초 도입](2026-11-20-architecture-diagram-adoption.md)의 32개 그림 생성·표시 확인과 이번 상세화는 다른 작업이다.

## 요청과 범위

사용자의 “overview도 … 좀 더 자세하게 코드 작성해서, 다이어그램 … 전체적으로” 요청에 따라 기존 전체 구성·객체 관계·호출·지도·표시·로드·개발 생성·State 도표를 실제 소스와 대조해 보강한다. Markdown의 Mermaid 코드가 편집 정본이며 다크 PNG/SVG·오프라인 갤러리·manifest는 그 파생물이다.

이번 권한은 문서·도표에 한정한다. 게임 코드·자산·설정·생성기·lock·원장·source cache를 변경하거나 게임·게임플레이 validator를 실행하지 않는다. 커밋·푸시·정리·패키지·게시·업로드도 하지 않는다. 문서 렌더링과 링크·지문·갤러리 확인만 수행한다.

## 작업 기준과 자료 위치

| 역할 | 위치·기준 |
|---|---|
| 작업 소스 | `C:/hoi/hearts_of_korea_Road_to_56`, `feat/korean-focus-update-20260922@9a01955785bcdd827c9c85522537a0bfc57ed654` 위 기존 미커밋 작업 보존 |
| HOK 원본 참고 | 읽기 전용 `C:/hoi/hearts_of_korea/docs/architecture/`. 원본 문서 안의 작성 당시 `0c19f58`와 선택 donor revision·현재 포트 소스를 구분 |
| RT56 host | 읽기 전용 Workshop `820260968`. 이번 ACF 읽기에서 installed/latest manifest 모두 `1963361040482473746` |
| 설치 metadata | 읽기 전용 `launcher-settings.json`: `Operation Postern v1.20.0.0.8873 (0c4f)` / `rawVersion=1.20.0.0`. 실행한 게임 버전 관측은 아님 |
| source cache | `C:/hoi/test/hok-rt56-source-cache/sources/` — 감사된 생성 입력, 이번 작업 공간과 구분·보존 |
| 새 외부 작업 | `C:/hoi/test/hok-rt56-architecture-detail-20261120-01/` — 이번 helper·백업·문서 렌더·확인 보고서 |
| 이전 그림·문서 백업 | 새 외부 작업의 `before-architecture/`, 파일별 시작 지문 `before.json`, Git 읽기 상태 `git-before.json` |
| 최종 유지 문서 | [전체 구조 목차](../architecture/README.md), [State 목차](../architecture/states/README.md), 각 주제 Markdown |
| 최종 유지 파생물 | `docs/architecture/images/`, `docs/architecture/states/images/`의 명시한 PNG/SVG·갤러리·manifest |

이전 도입의 helper·검증은 `C:/hoi/test/hok-rt56-democratic-architecture-20261120-01/architecture/`에 남겨 두었다. 기존 helper를 그 위치에서 수정·재실행해 현재 문서를 다시 덮지 않는다. 새 helper는 이번 외부 작업에 사본을 만들고 현재 도면 목록에 맞춰 사용한다. 기존 렌더 환경·Mermaid bundle은 읽기 전용으로 재사용하며 새 설치는 하지 않는다.

## 범위별 보강과 처리 대장

| 영역·도면 | 처리 | 상세화 계약 |
|---|---|---|
| 전체 구성 D01/D02 | 수정 | 출처의 권위·고정 입력·writer·runtime 공급자를 구분하고 실제 기능군과 입구 파일을 연결 |
| 객체·scope D03/D04 | 수정 | 국가·주·인물·idea·event·중점·결정·조건·효과·표시를 나누고 실제 호출별 scope 경로를 설명 |
| 콘텐츠 D05–D07 | 수정 | 진입·공유 코드·직접 효과·선행·배타·상대 배치·AI와 표시의 다른 관계를 분리 |
| 개발 생성 D08/D20 | 수정 | output owner·후속 finalizer·preflight·현재 raw/역사 view·원장을 구분 |
| 지도 D09/D10 | 수정 | ID 종류·Province 소속·네트워크·한국 delta·주 분할·콘텐츠 지역 정렬을 구분 |
| 표시 D11/D12 | 수정 | 실제 한/영·번역 공급 후보·명시/암시/동적 키·sprite/registry/payload 경로를 설명 |
| 로드 D13/D14 | 수정 | 물리 path·파일/논리 ID 등록·새 게임 이력·DLC OOB·저장 복원·후크·guard를 구분 |
| 산둥 D15–D18·지휘관 D19 | 수정 | 현재 공용 조건·예외·생성국/인물·실제 순서·legacy guard를 상세화 |
| State S01–S12 | 수정 | 데이터·초기화·실행 상태, 한국15주 전체 대응, 명령별 scope·조건·이전·소비자·저장·건설 제약을 설명 |
| 전체 실행·생성 D21/D22 | 수정 | 새 시퀀스 추가. 엔진 비공개 호출 순서·모든 writer의 동일 CLI 실행을 뜻하지 않음 |
| 지원·정보국·CNDP D23–D25 | 수정 | 새 시퀀스 추가. 비용·기간·중복 차단·대체·취소·재검사·완료 표식을 소스 기준으로 구분 |
| 표시 해결 D26 | 수정 | 새 시퀀스 추가. 유효 provider·키·sprite 참조와 실제 UI 관측을 구분 |
| 기존 도면 ID·anchor·HOK 저작·RT56 세계 소유권 | 의도적 유지 | 기존 링크·출처·호환판 정체성과 지리 ID/키 계약 유지 |
| 모든 ID의 전수 호출 그래프·전 세계 개별 주 지도 | 제외 | 전체 구조와 각 분야의 구체적 대표 경로를 제공한다. 모든 runtime 정의·모든 지리 관계의 전수 감사로 주장하지 않음 |
| 실제 DB 중복 처리·외부 번역 우선순위·옛 저장·DLC/MP·장기 AI | 미확인 | 이번에 실행하지 않음. 관련 과거 구현 기록의 소스·구성·범위만 유효 |

원본에서 질문·도표 구분을 참고하되 포트와 다른 donor 번호·값·번역 정책·개발 경로·검증 결과는 그대로 복사하지 않는다. [주 검토 스킬](../skills/hok-rt56-state-reference-review/SKILL.md), [현지화 스킬](../skills/hok-rt56-localisation-review/SKILL.md), [변경 영향 절차](../HOK_CHANGE_COVERAGE_REVIEW.md)와 각 도표의 근거·처리 표를 함께 따른다.

## 실제 문서 확인 기록

외부 작업 폴더의 `render_architecture.py`가 각 Markdown의 명시 anchor에서 Mermaid를 추출한다. 도면 ID의 기대 집합은 D01–D26/S01–S12다. 정본 해시가 같은 그림은 유지하고 달라진 그림만 새로 렌더하며, 전체 성공 뒤 명시한 PNG/SVG·갤러리·manifest만 복사한다. 이 helper는 문서 파생물 생성용이며 게임 생성기를 import·실행하지 않는다.

```powershell
& 'C:\hoi\test\state-diagrams-render-20261119\venv\Scripts\python.exe' -B 'C:\hoi\test\hok-rt56-architecture-detail-20261120-01\render_architecture.py'
```

Mermaid **12.3.0**, 실제 환경의 Playwright **1.65.2**, Chromium **158.0.8127.37**, Malgun Gothic을 사용했다. 기존 환경·로컬 bundle을 재사용했고 라이브러리를 설치하지 않았다. 문서/이미지·helper·bundle 해시와 도구 설정은 [전체 manifest](../architecture/images/manifest.json), State 부분집합은 [State manifest](../architecture/states/images/manifest.json)가 정본이다.

| 확인 단계 | 실제 결과 | 외부 기록·한계 |
|---|---|---|
| 기존 도면 전체 상세화 | 기존32개의 Mermaid가 모두 변경됐고 신규6개를 추가. 기존32개의 ID·anchor·문서 위치 변경0 | `final-doc-audit.json`, 시작 `before-architecture/`와 현재 정본 대조. 코드가 길다는 이유만으로 완전성을 판정하지 않음 |
| 소스·정본·파생물 지문 | 현재38개 정본·PNG/SVG76개, 근거 파일92개, State subset의 해시/크기 불일치0 | `final-doc-audit.json`. 근거 파일은 현재 소스 설명에 연결한 실제 로컬 파일 |
| 문서 렌더링 |38개 모두 생성. 최종 파생물·갤러리·manifest80파일 반영 | `render-attempt-01.log`~`render-attempt-04-gallery.log`, `render-log.json`, `published-files.json`. 게임 runtime은 쓰지 않음 |
| 배치 확인·수선 | 가로로 긴10개를 세로/그룹 배치로 조정. D12의 중첩돼 보이는 자산 그룹은 노드 간 invisible 배치로 수정 | `layout-trials.json`, `layout-adjustments.json`, `D12-layout-candidate.*`. `~~~`는 호출·선행 관계를 추가하지 않음 |
| 수동 이미지 확인 | contact sheet5개에서38개 전체 배치 확인. 마지막 D12/D21/S12의 유지 PNG는 크게 열어 한글·관계·다크 대비 확인 | `visual-review.json`. contact-02의 D12는 수정 전 이력이며 최종 D12는 별도 확인. 모든 작은 라벨을 원래 배율로 하나씩 판독한 것은 아님 |
| SVG·갤러리 |38개 SVG에서 글자 bbox가 viewBox 밖으로 나간 사례0. 전체38/State12 ×1440/420px에서 이미지 누락·가로 넘침·깨진 파일 링크·외부 페이지 요청·page error0 | `architecture-qa.json`, `qa-attempt-final.log`, `gallery-*.png`. 라이트 환경·저장된 light값에서도 다크 유지. VS Code 미리보기·HOI4 UI 확인은 아님 |
| 문서 링크 | 해당 정본·이번 기록의 상대 파일/anchor 연결 오류0 | `architecture-qa.json`에 실제 수량 기록. PNG/SVG·Mermaid 정본 링크와 각 소스 링크 구분 |
| 변경 범위·보존 | 시작 대비 기존85파일 변경·13파일 추가·삭제0, 모두 허용 문서 범위. 문서 범위 밖2,636파일의 크기/SHA-256 동일, HEAD 동일 | `preservation-final.json`. game code·asset·tool·lock·원장·AGENTS를 바꾸지 않음. 외부 원본 전체의 새 전수 해시 감사라고 주장하지 않음 |

읽기 교차검토에서 D01의 RT56→HOK 전용 cache 화살표, D02의 모델/음성→GUI 혼동을 바로잡았다. 산둥 첫 이전 설명도 실제 source에 맞춰 **597은 bootstrap 재검사, 대안743은 그 else에서 별도 재검사 없음**으로 수정했다. 코드에 새 재검사를 추가한 것이 아니다.

최초 전체 렌더는 문법 오류 없이38개를 생성했다. 이후 렌더는 새 배치/갤러리 수정에 따른 것으로, 두번째10개·세번째D12만 재생성하고 마지막에는 그림38개를 유지했다. 최초 gallery의 유형별 navigation 상위 flex 묶음도 독립 section으로 조정해 큰 화면과 좁은 화면에서 구분해 읽도록 했다. 기존 환경에서 Pillow가 없어 contact sheet는 설치 없이 기존 Playwright로 만들었다. 이전 도입의 renderer 실패·게임 자동 진단 실패는 이번 실행으로 덮지 않는다.

## 남은 의미·실행 확인

- RT56 `developed_rural` 범주는 슬롯3으로 정의돼 있으나 현재 CNDP의 낮은 범주 목록에 없다. [S12](../architecture/states/change-impact.md#s12-building-space)에 소스 사실과 의도/실행 미확인을 기록했으며 사업 조건을 임의 확대하지 않았다.
- 전체 그림은 실제 모듈·ID·참조·예외를 따라가는 상세 탐색도다. 모든 함수·국가·주·동적 태그·외부 모드 조합을 전개한 전수 호출 그래프는 아니다.
- 현재 유효 DB 우선권, 모든 표시/외부 번역, 정상 진행·장기 AI·DLC·멀티플레이·기존 저장 등은 이번에 실행하지 않았다. 과거 실행은 각 구현 기록에 명시한 소스·조건·관측만 유효하다.

## 알려진 보존·제한

시작 인벤토리는 Git 데이터 제외 2,721파일을 기록했다. 기존 `tools/__pycache__/`는 앞선 작업에서 보고한 정리 미결 자료이며 이번에 이동·삭제하지 않는다. `.local-artifacts`·source cache·옛 helper도 정리하지 않는다. 최종 문서 외 helper·프로필·초안·스크린샷·QA 보고서는 외부 작업 폴더에 둔다.

도표의 클래스 모양은 소스 개념 관계이며 엔진 C++ 구현·상속·메모리 구조 복원이 아니다. 시퀀스는 역할·소스 효과 순서를 설명하며 실제 실행·UI·저장 증거를 대신하지 않는다. 이번 문서 상세화는 앞선 콘텐츠 이식의 기존 정적 오류·게임 호환성 제한을 해결했다는 뜻이 아니다.
