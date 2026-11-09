# 2026-11-09 재벌 영어 표현과 번역 지침

재벌 영어 표현이나 그 생성 계층을 수정·재생성할 때 이 기록과 [현지화 스킬](../skills/hok-rt56-localisation-review/SKILL.md#영어-의미-번역과-논조), [변경 영향 절차](../HOK_CHANGE_COVERAGE_REVIEW.md)를 읽는다. 사용자 승인 범위는 재벌의 영어 표현과 AGENTS/현지화 스킬의 예방 지침이다. 다른 번역 후보, 한국어, 게임플레이, 지도, 저장 ID, GUI 배치, 의존성과 사용자 설정은 변경하지 않는다. 커밋·푸시·게시·업로드는 승인되지 않았다.

## 기준과 의미 선택

- 호환판: `feat/korean-focus-update-20260922@95d801fddf8f98fe3641860c2cffa976fb91f5b5`, 시작 작업 트리 깨끗함.
- 설치 게임: `Operation Postern v1.19.4.2.2da5 (0bdb)`, RT56 설치/latest manifest `1963361040482473746`. 이번 작업의 새 실행 체크섬이나 런타임 검증 결과가 아니다.
- 읽기 전용 HOK donor HEAD: `596b221bb994d93fce552d3ee1ba70fa9b5640f1`. 이번 번역 입력은 donor가 아니라 아래 동결된 현재 호환판 영어다.
- OS·실제 사용자 디렉터리, 기존 언어·모드/DLC 설정과 지문은 외부 `baseline.json`에 기록한다. 게임을 실행하거나 플레이세트·설정을 변경하지 않는다.
- 사본·검사·중간 출력의 외부 경로: `C:/hoi/test/hok-rt56-chaebol-english-20261109-01/`. 작업 시작 시 저장소 `.local-artifacts`는 없었다. 기존 외부 source cache와 보관소는 이동·수정하지 않는다.

사용자는 재벌을 비판적인 경제 권력집단으로 표현하도록 요청했다. 영어 사전에 `chaebol`이 존재하거나 바닐라 일본이 `Zaibatsu`를 사용한다는 사실은 이 문맥의 번역 선택을 확정하지 않는다. 세력·행위자는 `corporate oligarchs`, 영향력은 `Oligarchic Influence`, 기업집단·국유화 대상은 `conglomerates`로 구분한다. 좁은 영향력 창 제목에는 `Oligarchs`를 사용한다. 독점·담합·범죄라는 새 사실을 추가하거나 모든 문장을 같은 비난 강도로 재작성하지 않는다. 원문의 착취·정경유착·탐욕 서술과 기업 투자·공급망 설명을 유지한다.

`Chaebol`의 낯선 음역과 의도한 정치적 의미 사이의 불일치가 이번 수선 대상이다. 내부 `chaebol`/`jaebeol` ID와 `$...$`·`[?... ]`·scripted localisation 참조는 표시 단어가 아니므로 유지한다. 숫자 증감의 중립 색상·변수 수치·비용·기한도 유지한다.

## 변경 범위와 연결 경로

각 키의 변경 전후 영어·선행/최종 해시·대응 한국어 지문은 [잠금](../../tools/hok_english_terminology_lock.json)에 있다. 아래의 키 수는 직접 바뀐 표시값이며 치환을 통해 함께 바뀌는 사용처 수와 다르다.

| 영어 파일 | 변경 값 | 표시·호출 경로와 처리 |
|---|---:|---|
| `HOK_KOR_civic_focus_l_english.yml` | 3 | 한국 중점의 산업협력·공공 소유 이름/설명. 행위자와 소유권 변경 대상 기업을 구분해 수정 |
| `HOK_KOR_civic_state_l_english.yml` | 19 | 국민정신의 확립·간섭·지배 단계, 정책·결정·조달 설명, 영향력 이름. `common/scripted_effects/HOK_KOR_civic_effects.txt`의 단계 선택과 `common/decisions/HOK_KOR_civic_decisions.txt`의 지원/견제 양 경로가 소비. 변수 이름을 치환하는 비교·증감 툴팁의 토큰 자체는 의도적 유지 |
| `HOK_KOR_civic_ui_l_english.yml` | 6 | `interface/HOK_KOR_civic_influence.gui`의 제목·설명·지원/견제 툴팁과 정책 표식 이름. 동적 단계 선택은 `common/scripted_localisation/HOK_KOR_civic_influence_scripted_loc.txt`; 원시 ID와 치환 유지 |
| `HOK_KOR_fascist_procurement_l_english.yml` | 1 | 한국 조달 중점 설명의 기존 재벌별 주문. 회사별 주문으로 의미를 명시 |
| `korea_event_l_english.yml` | 2 | `events/korea.txt`의 도입 및 선거 사건 설명. 초기 경제권력의 등장과 친재벌 정책을 수정 |
| `korea_focus_l_english.yml` | 8 | 노조 선동·자산 몰수·반동분자·협력·군정의 재벌 통제 중점. 각 정치 경로의 어조를 유지 |
| `korea_ideas_l_english.yml` | 2 | 대공황 설명의 파산한 사업체와 국유화된 기업집단. 사람을 국유화한 것으로 번역하지 않음 |
| `replace/korea_decisions_l_english.yml` | 2 | `common/decisions/KOR_decision.txt`의 재벌 범주. 협력/통제 중점에 따른 대체 해금 경로와 삼성·현대·선경 주문이 소비. 범주 설명은 권력자들이 기업집단을 지배하는 문장으로 수정 |
| 합계 | 43 | 영어 8파일; 키·파일·로드 순서와 기존 `ADD` 분류 유지 |

한국어 대응 8파일과 그 밖의 한국어 채널은 의도적 유지다. 다른 번역 후보인 어용 지식인·히키아게샤·무궁화·향약·곡명은 이번 승인 범위에서 제외한다. RT56의 일반 외국 플레이와 공용 표현도 제외한다. 외부 번역 모드의 유효 덮어쓰기와 실제 UI는 이번 작업에서 미확인이다. 본체의 중복 정의·활성 값·동적 참조와 별도로 취급한다.

## 생성·출처와 지침

[새 생성 계층](../../tools/english_terminology.py)은 [동결된 현재 호환판 입력 8파일](../upstream/hok-english-terminology-20261109/README.md)에 명시적인 키별 영어 변경만 적용한다. 입력 capsule은 유지할 생성 입력이고 외부 작업 전 사본은 테스트 자료다. 두 역할을 혼동하지 않는다. 이전 영어/주석 번역·지도 분할·11월 콘텐츠·RT56 host·검토 후속 수선의 잠금과 보관 바이트는 변경하지 않는다.

기존 최종화의 뒤에 새 영어 계층을 연결하고 역사 검사는 정확히 입증한 새 최종 바이트만 이전 상태로 역투영한다. 미등록 입력과 독립적인 수정은 자동 승인하거나 덮어쓰지 않는다. 생성된 영어 파일에는 수동 기여 주석을 추가하지 않고 소유 생성기에 기여 이유를 남긴다. 한국어·paired 주석을 바꾸기 위한 불필요한 변경도 하지 않는다.

통합 원장은 기존 저작·번역·HOK/RT56 출처 열을 유지하면서 영어 8행의 최종 해시와 후속 근거를 갱신한다. `AGENTS.md`의 해시 변경은 문서 전용 생성 경로로 별도 반영한다. 실제 테스트 기록은 저장소나 입력 capsule 안에 두지 않는다.

`AGENTS.md`에는 새 코드 이식·영어 표시 변경 시 읽을 조건과 스킬 링크를 추가했다. 스킬은 일반 개념의 의미 번역, 고유명칭 구분, 원문의 비판/중립/찬양과 정치적 관점 보존, 근거 없는 독점·담합 의미 추가 방지, 관련 이름·설명·툴팁·동적 경로 확인을 규정한다. 이 규칙은 관련 없는 상속 문구의 전수 재번역을 승인하지 않는다.

## 확인 상태

필수 소스 확인은 43개 값의 문맥·영어 잔존 음역, 전체 키·보호 토큰·숫자·BOM/줄바꿈 보존, 한국어와 다른 runtime 파일 보존, 이전 source pins 보존, 결정적 재현·기존 gate 및 지침 구문 확인이다. 실제 UI·효과·저장·장기 AI·DLC·멀티플레이는 별도 미실행이며 이번 문구 변경의 소스 확인으로 대체했다고 주장하지 않는다.

수선 전 aggregate는 **25 PASS / 0 WARNING / 11 ERROR**였다. 지침 문서 두 파일만 먼저 수정된 뒤 검사했으며 영어/runtime 및 생성기 변경 전 결과다. 기존 host/vanilla source drift·descriptor·전체 원장 충돌 등 11개 오류는 외부 `static-before.txt`에 보존한다.

최초 수선 후 aggregate(`static-after.txt`)는 **25 PASS / 0 WARNING / 12 ERROR**였다. 새 오류는 Korea-only pruning의 `korea_event_l_english.yml` 비교 한 건이다. 이 생성기의 별도 출력 경로가 과거 영어 계층에서 끝나는 것을 확인하고 같은 말단 최종화와 정확한 기존 바이트 preflight를 연결했다. 정책·제거 목록이나 과거 입력은 바꾸지 않았다. 보완 후 정리 생성기 16출력 전부가 현재 파일과 일치했다(`pruning-terminology-contract.json`). 최초 실패를 후속 성공으로 덮어쓰지 않는다.

최종 문맥 대조에서 자산 국유화 중점의 동사는 원문과 기존 영어의 `Nationalise`를 유지했다. 잠금의 최종 값은 `Nationalise the Oligarchs' Assets`다. 개발 중간의 `Seize` 후보는 외부 draft 사본에만 보존하며 유지 입력·과거 소스 핀으로 채택하지 않는다.

| 실제 수행한 확인 | 결과·근거 |
|---|---|
| 새 영어 계층 | `--apply` 8출력 생성, 최종 `--check` 일치; 43개 값·기존 키/토큰/숫자 유지 |
| 기존 영어 검사 | `source_snapshot.py --english-check` 통과. 과거 영어 이식과 새 콘텐츠의 원래 언어·키·치환 계약 유지 |
| 기존 후속 수선 | raw 검사와 결정적 출력 `--check` 통과. 새 영어가 기존 civic 수치 수선을 지우지 않음 |
| 11월 콘텐츠·분할 | 32출력 및 47출력의 기존 `--check` 각각 통과 |
| 원장 | scoped 및 문서 전용 검사 통과. 기존 1,541행 중 영어 8행의 해시/근거와 AGENTS 1행의 출력 해시만 변경; 출처·분류·다른 셀 유지 |
| 독립 QA | 최종 재실행 9개 검사 그룹 통과: 기준 runtime 1,479파일 중 영어 8파일·43값만 변경, 한국어 46파일과 기존 입력/잠금/보관본/캐시 2,176파일 해시 유지. 실제 영어 45파일의 2,868개 값을 검사해 표시 단어 `Chaebol` 없음; 내부 키·치환·역사 주석은 의도적 유지 |
| 역투영·재생성 보호 | 대소문자/구분자 별칭 48건, 이전/최종 바이트·중첩 finalizer·멱등성, 미등록 바이트·토큰 변조·다른 값의 drift 거부 확인. 실제 runtime을 변조하지 않은 메모리 기반 검사 |
| 지침 | frontmatter가 기존과 같고 이름/설명·새 절·조건부 링크가 유효함을 확인; AGENTS CRLF와 스킬 LF 유지. 제공된 `quick_validate.py`는 설치 Python 3.14/3.12에 PyYAML이 없어 실행 차단됐으며 의존성은 설치하지 않음. 수동 확인 결과를 이 자동 검사 통과로 표기하지 않음 |

외부 상세 근거는 `baseline.json`, `terminology-final.txt`, `new-content-check.txt`, `followup-check.txt`, `ledger-check.txt`, `documentation-ledger-check.json`, `qa/independent-qa.json`과 해당 helper다. 독립 QA의 최초 한국어 예상 개수 45는 실제 기준선 46으로 정정한 검사 가정이며 파일 누락·추가가 아니었다. 과거 결과와 정정 이력은 JSON의 `verification_history`에 구분한다. 실제 UI·효과·저장 검증과 커밋/푸시는 수행하지 않았다.

최종 aggregate는 **26 PASS / 0 WARNING / 11 기존 ERROR**, exit1이다(`static-final.txt`). 오류 11개의 실제 메시지가 사전 결과와 모두 같음을 `aggregate-comparison.json`에서 확인했다. 새 영어 gate가 추가로 통과했고 최초 pruning 회귀는 해소됐으나 기존 source/descriptor/전체 원장 부채를 고친 것으로 해석하지 않는다.

새 유지 입력은 `.gitattributes`의 해당 capsule `-text`와 새 잠금/생성기 LF 규칙으로 보존한다. Git 객체를 쓰지 않는 `hash-object`의 서로 다른 `core.autocrlf` 해석 16건에서 8개 입력 바이트가 그대로 보존됨을 확인했다. 이 검사는 Git 설정 변경·스테이징·커밋이 아니다. 최종 `final-environment-preservation.json`은 사용자 설정 지문, donor HEAD/status, 호환판 branch/HEAD, RT56 acf/descriptor와 게임 버전 파일의 보존도 확인한다. `git diff --check` 통과; 배포·게시·게임 실행은 수행하지 않았다.

## 2026-11-09 정책 선택 문장 한 곳 교정

이후 사용자는 영국 영어 검토에서 지적한 문장 한 곳만 교정하도록 승인했다. 같은 branch/HEAD의 위 미커밋 변경을 보존하고 `HOK_KOR_policy_cooperation`의 영어만 `Industrial cooperation policy with corporate oligarchs selected`에서 **`Industrial cooperation with the corporate oligarchs has been selected.`**로 바꿨다. 다른 설명 문장과 기존 42개 번역값은 의도적 유지다.

이 키는 `common/scripted_effects/HOK_KOR_civic_effects.txt:186`에서 설정하는 정책 표식을 설명하며 `common/scripted_triggers/HOK_KOR_civic_triggers.txt:3`과 한국 중점의 정책 조건이 소비한다. ‘정책이 선택된 상태’라는 의미를 유지한다. 표식·조건·효과·한국어·공용/동적 참조는 바꾸지 않는다. 실제 활성 번역 덮어쓰기와 UI는 이번에도 미확인이다.

현재 입력 잠금의 해당 `after` 값과 UI 출력 해시/크기를 갱신하고, 선행 잠금 해시·출력 해시·문장과 변경 이유는 `revision_history`에 보존했다. 변경 전 전체 잠금과 실제 출력 사본은 새 외부 경로 `C:/hoi/test/hok-rt56-chaebol-ui-proofread-20261109-01/`의 `lock-before.json`과 `ui-before.yml`이다. 이 사본은 검증 근거이며 기존 유지 입력 capsule을 대체하지 않는다. 이전 43개 번역 검사의 결과는 그 당시 문구에 귀속한다.

기존 생성기로 선행 바이트와 당시 최종 출력 전체가 맞는지 먼저 확인한 뒤 새 명시 값으로 재생성했다. 새 UI 출력 SHA-256은 `D5830053C32F869D00D75D3689198DD6F206960D01F71CCE4A3E006A250477B1`이다. 원장도 소유 생성기로 갱신했으며 직전 원장과의 차이는 이 UI 행의 `output_sha256` 한 셀뿐이다.

`scope-verification.json`에서 이번 시작 runtime 1,479파일 중 해당 영어 파일 한 곳·한 값만 바뀌고, 다른 42개 번역값과 한국어를 포함한 다른 runtime, 유지 입력/잠금/보관본/캐시 2,185파일이 보존됨을 확인했다. BOM·줄 끝·다른 바이트와 중첩 finalizer의 재생성도 일치했다. 영어 전체 검사·새 영어 계층 검사·scoped 원장 검사와 `git diff --check`는 통과했다. 이 후속의 aggregate는 **26 PASS / 0 WARNING / 11 기존 ERROR**, exit1이다. 새 외부 `static-after.txt`와 `aggregate-comparison.json`에서 직전 11개 오류 메시지가 그대로이며 추가 오류가 없음을 확인했다. 게임 실행·커밋·푸시는 수행하지 않았다.
