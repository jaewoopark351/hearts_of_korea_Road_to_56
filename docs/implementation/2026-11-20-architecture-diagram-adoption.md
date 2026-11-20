# 2026-11-20 HOK×RT56 구조 문서·다크 도표 체계 도입

상태: **지침·로컬 스킬·16개 구조 문서·32개 Mermaid와 다크 SVG/PNG·오프라인 갤러리 구현 및 문서 표시 확인 완료 / HOI4 실행 검증과 별개**. 사용자의 `AGENTS.md, /docs 읽고 구현해줘` 후속 요청으로 [앞선 도입 계획](../plans/2026-11-20-architecture-diagram-adoption-plan.md)을 실제 적용한다. 계획 작성 당시의 문서화 전용 범위는 역사로 보존한다.

## 범위와 기준

호환판은 `C:/hoi/hearts_of_korea_Road_to_56`, `feat/korean-focus-update-20260922@9a01955785bcdd827c9c85522537a0bfc57ed654` 위 작업 트리다. 시작부터 있던 콘텐츠·구조 계획과 인덱스 변경을 보존한다. 읽기 전용 donor는 `C:/hoi/hearts_of_korea@f180bc8089e2a17f310b1fafa091d3f152063df3`다. 원본의 문서 내부 `0c19f58`+당시 미커밋 표시는 그 작성 시점이며 현재 포트 소스와 혼동하지 않는다.

이 하위 작업은 `AGENTS.md`, 루트 `README.md`, `docs/skills/hok-rt56-architecture-diagrams/SKILL.md`, `docs/architecture/`, 이 기록을 담당한다. 게임 코드·자산·지도·도구·잠금·원장과 주 이식은 동시 콘텐츠 작업의 소유 범위이며 이 문서 작업이 직접 수정하지 않는다. 원본·게임 설치·Workshop·사용자 데이터와 기존 캐시·보관 자료도 수정하지 않는다. 커밋·푸시·게시·업로드는 하지 않는다.

helper·원본 백업·렌더 프로필·초안·검사·화면 증거의 새 위치는 **`C:/hoi/test/hok-rt56-democratic-architecture-20261120-01/architecture/`**다. `AGENTS.before.md`·`README.before.md`는 편집 전 바이트, `author_architecture.py`는 최초 문서 작성 helper다. 후속 편집 정본은 저장소의 Markdown이며 이 초기 helper를 다시 실행해 현재 문서·AGENTS에 중복 삽입하지 않는다. 렌더링은 아래 별도 helper로 재생성한다.

도입한 지침의 읽기 전용 출처는 다음과 같다. 원본 내부 경로를 그대로 활성화하지 않고 로컬 `docs/skills/`와 RT56 소유권에 적응했다.

| donor 상대 경로 | 이번 읽기 SHA-256 |
|---|---|
| `AGENTS.md` | `80D70F1A87F7D63236DE9422F112B5A623630360D1ECA5CA86B673145F930871` |
| `.agents/skills/hok-architecture-diagrams/SKILL.md` | `12A0B169E6B6F2007CB76999EF28A5E1EA106DB838AEC0D4B1663E83C07CDC0F` |
| `docs/architecture/maintenance.md` | `4264582DABA1220B20F53258679EB0AE81D79374B47FEDD7F27EB43CF2AEEE09` |

## 실제 적용과 소유권

| 영역 | 이번 처리 |
|---|---|
| AGENTS | 구조 관계 검토/수정과 문서 도표 작성/미리보기/내보내기의 조건부 필수 읽기2행, 항상 다크·정본/파생물·필요 관계 갱신 규칙 추가. 기존 권한·모드·RT56 보존 규칙 유지 |
| 로컬 스킬 | `docs/skills/hok-rt56-architecture-diagrams/SKILL.md`. 기존 `docs/skills/`+AGENTS 운영을 따르고 ignored `.agents/` 자동 탐색이나 전역 설치를 요구하지 않음. skill-creator 지침 적용 |
| 구조 문서 | 전체·도메인·호출·지도·표시·로드/수명주기·소스/생성·산둥·지휘관 사례 및 State 상세/목차/유지 안내16개 Markdown |
| 도표 | D01–D20·S01–S12의32개 Mermaid. 각 주제 Markdown 한 곳이 정본. 모든 블록에 `theme: dark` 명시 |
| 최종 파생물 | 일반20·State12의 SVG/PNG64개, 전체/State 오프라인 갤러리2개, 전체/State manifest2개. 기본명 호환 사본은 새로 만들지 않음 |
| 현재/예정 상태 | 산둥28출력·64주 소스 통합과 한영 UI·CHI 경계/정보국 슬롯·0% r9/양수 r10 fixture의 범위 내 강제 효과·새 저장 확인을 구분. 구체적 검증 범위·수선 이력·후속 결과·남은 검증은 [최신 콘텐츠 구현 기록](2026-11-20-korean-democratic-support-intelligence-port.md)의 「실제 실행의 현재 기록」 절에 있는 최신 결과·제한을 따름. 설치1.20과 descriptor1.19.* 차이는 별도 |
| 출처 | donor의 도표 질문·분리 원칙·다크 정책을 적응. HOK 원작·donor 기여를 보존하며 기존 donor PNG/SVG를 새 포트 그림으로 복사하지 않음 |

특히 원본의 두 채널 한국어·일반판 외부 번역 구성은 포트의 실제 영어/한국어·RTK·RT56 구성으로 다시 썼다. 한국 State/Province 이관과15주 대응은 로컬 ADR·대응표를 정본으로 삼는다. source cache·capsule→생성기/lock·최종화→runtime/원장은 개발 과정이며 HOI4가 Python을 실행하는 것으로 그리지 않는다. `historical_bytes`와 실제 최종 바이트 검사도 분리한다. 기존 포팅 문서의9월6일 crash·검사 상태는 새 현황으로 복제하거나 소급 변경하지 않는다.

## 재생성 도구와 산출물

기존 외부 환경 `C:/hoi/test/state-diagrams-render-20261119/venv/Scripts/python.exe`의 Playwright를 사용하고, `C:/hoi/test/shandong-dominion-20261119/mermaid-12.3.0.min.js`를 읽기 전용으로 재사용했다. 새 렌더러·네트워크 라이브러리를 설치하지 않았다. 실행 helper는 새 외부 경로의 `render_architecture.py`이며 임시 프로필은 `render-profile/`, 초안은 `output/`이다. 실제 Chrome·Mermaid·Playwright 버전, 글꼴·테마·source/output 지문은 [전체 manifest](../architecture/images/manifest.json)에 기록한다.

```powershell
& 'C:\hoi\test\state-diagrams-render-20261119\venv\Scripts\python.exe' -B 'C:\hoi\test\hok-rt56-democratic-architecture-20261120-01\architecture\render_architecture.py'
```

helper는32개 Markdown 블록을 읽고 관련 다크 파생물만 만든다. 같은 Mermaid 해시의 기존 이미지는 그대로 유지할 수 있다. 모든 필요한 출력 생성이 끝난 뒤 명시한 SVG/PNG·갤러리·manifest만 `docs/architecture/`에 복사한다. 게임 runtime·캐시·기존 사용자 프로필을 쓰지 않는다. 원본 작성 helper와 렌더 helper의 역할을 구분한다.

## 확인 결과와 한계

초기 `author_architecture.py`의 목차 f-string 닫기 오타는 Python 구문 검사 단계에서 실패했고 저장소 쓰기 전에 수정했다. 첫 렌더는 D18의 점선 라벨 `PREV.PREV` 인용 누락으로 D17 다음에 중단됐다. 이때 저장소 이미지 배포 전이었다. 정본 라벨을 인용한 뒤32개 전체가 렌더됐고64개 이미지와 갤러리/manifest4개를 반영했다. 앞선 실패를 최종 성공으로 덮어 쓰지 않는다.

skill-creator의 `quick_validate.py`는 시스템 Python과 기존 Playwright 환경 모두 `ModuleNotFoundError: yaml`로 검사를 시작하지 못했다. 스킬 검증 통과로 기록하지 않으며 PyYAML을 설치하지 않았다. 이름·frontmatter의 `name`/`description`·범위·조건부 상대 링크는 직접 읽어 검토한다. 새 스킬에 실행 helper나 추가 의존성을 포함하지 않았다.

32개 PNG를 각각 열어 한글·도형·연결선·잘림과 다크 대비를 확인했다. source 설명에서 `mutually_exclusive` 선을 물리적 “가로선”이라고 한 문구는 실제 자동 배치가 세로일 수도 있어 “화살촉 없는 연결선”으로 바로잡았다. 이것은 중점 코드를 바꾸거나 실제 HOI4 레이아웃을 확인한 결과가 아니다. 로컬 갤러리·링크·manifest의 최종 확인은 아래 후속 결과로 기록한다.

첫 갤러리 QA는 기본 임시 브라우저 프로필의 위치를 새 외부 TASK로 명시하지 못한 경로 설정 누락이 있었다. 그 실행은 종료했으며 실제 기본 임시 경로를 별도로 수집하지 않았다. 후속 helper에는 `TEMP/TMP`, 영구 격리 `qa-profile/`, 다운로드 위치를 모두 이 외부 작업 폴더로 고정했다. 최초 실행의 경로 한계를 최종 명시 경로와 혼동하지 않는다. 사용자 Chrome 프로필이나 HOI4 설정을 선택·조작한 것은 아니다.

## 최종 문서 확인

| 확인 단계 | 실제 결과·외부 자료 | 한계 |
|---|---|---|
| 소스·파생물 | `render-log.json`, `published-files.json`.32개 정본에서 SVG/PNG64개를 생성하고 갤러리/manifest4개를 반영. 최종32개는 같은 Mermaid 해시라 이미지 바이트를 유지하면서 문서·관련 소스 지문만 갱신 | 게임 등록·실행이 아님 |
| 이미지 시각 확인 |32개 PNG를 각각 직접 열어 한글·도형·연결선·다크 대비 확인. SVG32개의 텍스트 bbox가 viewBox 밖으로 나간 사례0 | VS Code 자체 미리보기나 HOI4 UI를 조작한 것이 아님 |
| 오프라인 갤러리 | `architecture-qa.json`: 전체32개/State12개 ×1440/420px의4구성. 라이트 환경과 저장된 light값을 넣고 reload해도 다크 유지, 이미지 모두 로드·깨짐0·가로 넘침0·외부 요청0·페이지 오류0. script/테마 버튼0 | 격리한 문서 브라우저의 실제 파일 표시 |
| 지문·연결 | 같은 최종 보고서의 상대 링크376개·64출력 해시/크기·원본 Markdown 지문에서 오류0. 최초 병행 작업 중 main 구현 기록 링크5개 부재는 `architecture-qa-before-main-record.json`에 보존하고 파일 작성 후 최종0으로 확인 | 링크/지문 일치가 게임 효과 의미를 입증하지 않음 |
| 스킬 | 이름·name/description frontmatter·권한/범위·발견 경로·상대 링크 수동 확인. bundled quick validator는 위 PyYAML import 실패로 미수행 | 자동 스킬 검사 통과를 주장하지 않음 |
| 변경 범위 | 최초 AGENTS7줄·루트README2줄 추가, 새 로컬 스킬과 도입 기록, architecture84파일(문서16·PNG32·SVG32·HTML2·JSON2). 관련 `git diff --check` 통과. 후속으로 AGENTS의 외부 descriptor 불일치 단정을 아래 현재 상태 재확인 규칙으로 정리 | 동일 작업의 다른 콘텐츠 변경은 main 기록에서 별도 감사 |

실제 확인 화면은 `gallery-all-1440.png`, `gallery-all-420.png`, `gallery-states-1440.png`, `gallery-states-420.png`다. 브라우저 스크롤 직후 한 초기 캡처가 표시 완료 전 배경만 담겨, 후속 helper에 두 animation frame 대기와 heading/scroll 위치 확인을 추가했다. 최종 캡처의 실제 제목·그림을 다시 열어 확인했으며 이 조정은 갤러리 파일이나 게임 코드를 변경하지 않는다. 초기 작성/렌더/스킬/링크 실패는 `initial-failures.json`에 따로 색인한다.

동시 콘텐츠 작업의 영어 의미 계층·preflight가 정확한 역투영으로 보완된 뒤에도 D08/D20의 입력·최종화·현재 raw 검사·과거 계약 관계는 같다. 따라서 다이어그램을 불필요하게 재생성하지 않고 최종 관련 소스 지문과 유지 이유를 기록했다. 산둥은 소스 통합과 범위 내 UI·강제 효과·새 저장 확인을 구분하며, 원본63주 대신 포트64주/반복64와 Gyarong1075를 설명한다. 이번 제한된 검증의 각 사례 결과·수선 이력·검증 한계와 이후 추가 확인은 [최신 콘텐츠 구현 기록](2026-11-20-korean-democratic-support-intelligence-port.md)의 「실제 실행의 현재 기록」 절에 있는 최신 결과·제한을 따른다. 정상 중점 진행 전체·장기 캠페인·기존 저장 호환·MP·DLC 조합 검증의 완료를 뜻하지 않는다.

렌더링 성공·문서 표시와 게임 등록·가용 조건·정상 진행·효과·새 저장·기존 저장은 별개다. 원본의 피감독국·영토·웡원하오 실행은 당시 원본 소스와 구성에 한정한다. 이번 자치령·CHI50%/70일·인간 일본과 RT56/1.20 전체 호환성을 구조도만으로 보장하지 않는다.

기존 `tools/__pycache__/`21파일·1,088,888바이트는 시작 기록의 정리 미결이며 이 하위 작업에서 이동·삭제하지 않는다. 새 Python helper는 외부 위치와 `-B`를 사용해 저장소에 새 bytecode를 만들지 않는다.

## 후속 descriptor 지침 정정

AGENTS의 descriptor 공통 규칙에는 외부 `.mod`가 아직 불일치한다는 이전 단정이 남아 있었다. [11월10일 외부 descriptor 기록](2026-11-10-korean-equipment-localisation-repair.md)의 별도 승인된 동기화 이력과 구분하도록, descriptor·릴리즈 작업 전에 해당 기록을 읽고 현재 머신의 저장소/외부 descriptor·playset·물리 경로를 함께 재확인하는 조건부 규칙으로 바꿨다. 외부 파일을 수정하거나 패키지 준비를 승인한 것이 아니다. 원장의 AGENTS 출력 지문은 문서 전용 경로로 갱신한다.

## 후속 일본 비맹주 초대 수선의 문서 범위

실제 `japan-50`에서 한국이 비맹주일 때 반군의 세력 가입이 실패한 기록을 보존하고, 소스의 초대 actor를 좁게 수선했다. 수선 기록 시점은 독립 소스 검토·생성 소유 검사 후 새 `japan-50-r16` 재검증 대기이며, 이후 결과는 [전체 콘텐츠 구현 기록](2026-11-20-korean-democratic-support-intelligence-port.md)의 실행 절을 정본으로 삼는다. 초기 실패를 새 소스의 통과로 덮거나 이 문서 갱신을 게임 실행으로 세지 않는다.

바뀐 관계의 설명은 [산둥 문서의 일본 helper 문단](../architecture/shandong-government.md)에만 추가했다. 가입한 비맹주 KOR의 실제 `faction_leader`가 `PREV.PREV`의 민주 반군을 초대하고 KOR는 기존 `PREV` 반군과의 참전을 유지한다. 맹주·무세력 경로,10–90% 비율·ID·보상/기간·중국 helper를 바꾸지 않는다. 원본 입력·capsule의 일본 helper `F2A255FB9AB4194B9E24AB908B0CD8F20BE6C1CE973AE0A4F4FF83D86D72D1F6`·851바이트는 보존하고, 최종 호환판 helper는 `8684B6498B3866B102676E1B995BBCAFE306984B708B7720777FB5472C2C8A5C`·1,118바이트의 별도 `source_adaptation`으로 기록했다. HOK 저작·donor 출처와 호환판 원인 수선을 분리한다.

기존32개 Mermaid에는 일본의 세력 초대 actor 경로가 없다. D03/D04의 도메인/CNDP scope 예시, D05의 일반 호출, D08/D20의28출력 소유·등록된 선조/최종화·역투영 관계는 같다. D15–D18·S07–S09는 중국 출범/인물/영토 흐름이며 일본 helper 수선으로 바꾸지 않는다. 일본 수선의 초기 기록 시점에는 중국 비맹주도 별도 미검증이었다. 후속 `chinese-nonleader-r18`에서 ENG 맹주·독립 KOR 비맹주의 기존 전체 helper 경로가 추가 수선 없이 같은 세력·KOR 자치령을 만드는 것을 실제 확인했으며, 내부 자동가입 단계의 원인을 확정한 것은 아니다. 따라서 **32 Mermaid와 SVG/PNG64개를 같은 바이트로 유지하고 새 도표·렌더링을 만들지 않았다**. 갤러리 두 개도 같은 제목·상대 링크·이미지를 표시하므로 유지한다.

양쪽 manifest는 `sourceEvidence`의 실제 생성 소유자 `tools/upstream_democratic_support.py`·잠금 `tools/hok_democratic_support_lock.json` 지문을 갱신하고 일본 helper의 직접 지문을 추가했다. 전체 manifest의 D15–D18은 변경된 Markdown 전체 지문만 갱신하며 Mermaid·SVG·PNG 지문은 유지한다. State manifest의12개 Markdown 관계도 그대로다. 원래 렌더 시각·도구·시각 QA 결과를 새 렌더로 바꾸지 않고, 별도 `sourceEvidenceRefresh`로 이번 메타데이터 갱신을 구분한다.

읽기 전용 영향·편집 전 보존 원장은 외부 `geography/qa/japanese-faction-architecture-impact-01.json`, 반영 후 바이트·지문 대조는 `geography/qa/japanese-faction-architecture-preservation-01.json`에 둔다. 위치는 위 공통 TASK 루트 아래다. helper·보고서만 외부에 쓰며 생산 코드·활성 프로필·게임 UI·저장 원본을 수정하거나 추가 실행·렌더러/라이브러리 설치를 하지 않았다. 소스 설명·지문 일치는 실제 일본 비맹주 재검증이나 중국 비맹주 검증을 대신하지 않는다.

[구조 목차](../architecture/README.md) · [전체 갤러리](../architecture/images/index.html) · [유지 안내](../architecture/maintenance.md)
