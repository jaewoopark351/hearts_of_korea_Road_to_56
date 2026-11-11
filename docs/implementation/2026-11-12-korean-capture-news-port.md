# 2026-11-12 중국 도시 함락 뉴스 조건 이식

상태는 **단일 출력 구현 반영·독립181항목과3,840논리 사례 통과 / 전체25 PASS·0 WARNING·기존16 ERROR / 호환판 실제 실행 미검증**이다. 이 계층의 수정·재생성·검증 전 선택 입력 안내와 잠금, 주 참조 스킬 및 변경 영향 절차를 읽는다. [선택 입력 안내](../upstream/hok-capture-news-update-20261112/README.md), [잠금](../../tools/hok_capture_news_update_lock.json), [주 참조 스킬](../skills/hok-rt56-state-reference-review/SKILL.md), [변경 영향 절차](../HOK_CHANGE_COVERAGE_REVIEW.md)

## 요청과 관측 기준

사용자의 원본 업데이트 확인 요청 뒤 이어진 “우리도 수정하자”에 따라 원본 `cdc022e`의 베이핑·난징·충칭 함락 뉴스 조건을 현재 RT56 호환판에 반영했다. 사건 파일은 기존 HOK 전용 `ADD` 출력이며, 지리 참조를 RT56에 맞춘 선택 병합으로 처리했다.

| 항목 | 이번 기준 |
|---|---|
| 호환판 시작 | `feat/korean-focus-update-20260922@180ffad37821835be3338e66e27c755982a16468`, 작업 트리 깨끗함 |
| 원본 | 읽기 전용 `C:\hoi\hearts_of_korea`, `feat/korean-focus-expansion-ai@cdc022eee15fbf7404d4cb30cf2d0102d29e550c`, 작업 트리 깨끗함 |
| 원본 변경 전 | `424e4d962803b5cc7a3667a7df4604fbd128733a`의 뉴스 파일 Git blob |
| 설치 엔진 | `Operation Postern v1.19.4.2.2da5 (0bdb)`, 설치 메타데이터 기준 |
| RT56 | 읽기 전용 Workshop `820260968`, 설치·최신 manifest `1963361040482473746` |
| 현재 사용자 구성 | Windows 11 Home, `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV`, `l_korean`, disabled DLC 없음. `dlc_load.json`은 원본 HOK·국뽕팩·anime 구성이며 playset 이름은 이번에 조회하지 않음 |
| 기존 로그 | 원본 구성의 `1.19.4.2.2da5 (85ea)`·활성 DLC36 기록. 이번 RT56 실행 결과는 미검증 |
| 외부 작업 경로 | `C:\hoi\test\hok-rt56-capture-news-20261112-01\` |

원본 산업·핵분열·한미 방위 협상은 앞선 이식 기록을 확인했다. 최신 원본의 한미 helper와 유지 입력 간 차이는 보병 행 들여쓰기 두 곳이며, 이번 실질적인 추가 대상은 세 뉴스 trigger다. 원본의 지역 정렬 실행 기록은 동결 문서의 출처 이력으로 보존한다. [원본 정렬 기록 사본](../upstream/hok-capture-news-update-20261112/documents/docs/HOK_STATE_REFERENCE_ALIGNMENT_PLAN.md)

## 변경 영향 대장

| 기능·사용처 | 처리와 최종 의도 | 근거와 확인 범위 |
|---|---|---|
| 베이핑 `newsk.22` | **수정**. 한국이 도시 province9843을 통제하고, 부모 주608 소유국이 CHI이면 대CHI 전쟁, HBC이면 대HBC 전쟁을 검사 | 실제 RT56608의 도시·초기 HBC 소유를 확인. 주 전체 통제 조건을 도시 기준으로 변경 |
| 난징 `newsk.23` | **수정**. 한국의 도시11913 통제, 주1114의 CHI 소유, 대CHI 전쟁을 검사 | 기존 포트613은 상하이. donor1035는 RT56 Finnmark/NOR이므로 이 trigger 안에서1114로 대응 |
| 충칭 `newsk.24` | **수정**. 한국의 도시6999 통제, 주1116의 CHI/대CHI 또는 SIC/대SIC 짝을 검사 | 기존 포트605에는 충칭 도시가 없음. donor1037은 RT56 Hame/FIN이므로 이 trigger 안에서1116으로 대응 |
| 사건 ID·호출·범위 | **의도적 유지**. 각 사건의 자체 trigger 평가, `major=yes`, 2일 MTTH, `immediate`와 선택지 | 관련 포트·설치 RT56 common/events·vanilla events 검색에서 별도 직접 호출·중복 정의를 발견하지 못함 |
| 일회 표식 | **의도적 유지**. `fall_of_beijing_kor`, `fall_of_nanjing_kor`, `fall_of_chongqing_kor`의 기존 검사와 설정 | 관련 검색에서 각 뉴스의 trigger와 immediate에만 사용. 이미 발생한 사건의 표식은 재발을 차단하는 기존 소스 계약 |
| 한영 문구·그림 | **의도적 유지**. 각 사건의 제목·본문·선택지·사진 참조 | 기존 한영 `korea_event_l_*`의354–368행과 그림 registry를 확인. 세 trigger 밖의 원문 바이트 보존 |
| 신징과 다른 뉴스 | **의도적 유지**. 기존 trigger·표식·효과 | 세 수정 영역의 역변환으로 기존 파일 전체 바이트가 복원되는지 검사 |
| `newsk.27`, `newsj.1–4` | **제외**. 기존 비한국 콘텐츠 제거 계약 | 과거 pruning을 거친 포트 입력 위에서 적용하며 제거된 사건의 재도입을 거부 |
| 전역 지도·한국 분할·타국 시스템·앞선 이식 | **제외**. 이번 코드 참조 수정 범위 밖 | production 파일 전체 목록·해시를 수정 전과 대조 |
| 실제 RT56 발화·수신 UI·저장 | **미확인**. 도시만 점령한 경우와 차단·대안 경로의 실제 엔진 동작 | 소스 논리와 donor 실행 이력을 현재 호환판 실행 증거로 합산하지 않음 |

현행 RT56의 주5개 원문과 부모 province를 동결했다. 설치 vanilla의 `controls_province` 문서는 COUNTRY scope를 명시하며, `common/national_focus/soviet.txt`의 ROOT 사용례도 지문으로 기록했다. 관련 위치·SHA-256·크기와 원본/사본 역할은 source manifest를 따른다. [소스 manifest](../upstream/hok-capture-news-update-20261112/source-manifest.json)

## 생성 소유권과 원장

`tools/upstream_capture_news.py`가 단일 후속 계층을 소유한다. 동결 donor 전후에서 세 trigger와 인접 기여 주석만 바뀌었음을 확인한 뒤, 기존 pruning 출력의 세 영역을 교체하고 난징·충칭의 부모 주만 대응한다. 기존 파일의 BOM·혼합 줄바꿈과 다른 영역은 바이트로 보존한다. 최종 출력은14,032바이트이며 SHA-256은 `4C3331C7AB9DC0782DD90210780CF7710787325ED7418DEE0FD3748C0398A5F7`이다. [생성기](../../tools/upstream_capture_news.py)

`review_followup`의 최종화·역투영·사전 검사에 연결하고 pruning CLI도 보호 파일의 미등록 수정을 먼저 검사한다. 과거 검사는 정확히 입증된 최종 바이트에서만 직전 출력으로 역투영한다. 전체 validator에는 원시 최종 출력을 검사하는 새 gate를 추가했다. `.gitattributes`는 새 source capsule을 byte-exact 입력으로 보존한다.

전체·부분 원장 생성 경로는 기존 한미 방위 계층 뒤에 새 원장 처리를 연결했다. 이번 실제 원장 갱신은 새 생성기의 `ledger_bytes`로 기존1,559행에 적용했다. 바뀐 값은 뉴스 파일 한 행의 `output_sha256`과 `reason`이며 다른 원시 행·기존 분류와 provenance를 보존했다. 기존 전체 원장 재생성의 오류는 아래 정적 결과에 남긴다.

## 검증과 남은 항목

| 단계 | 이번 결과 |
|---|---|
| 수정 전 전체 정적 | `static-before.txt`, exit1, **24 PASS / 0 WARNING / 16 ERROR** |
| 독립 생성기 검사 | `agent-generator/generator-qa.json`, **20 PASS / 0 FAIL**. 세 literal trigger의 전체 바이트 재구성, 역투영·멱등성·미등록 수정/경로/별칭 거부와 원장 보존 |
| 독립 소스·논리 검사 | `independent-qa/source-logic-report.json`, **68 PASS / 0 FAIL**, 별도 조건 모델 **3,840사례 / 불일치0**. 도시 미점령·소유국/전쟁 불일치·이미 발생·도시만 점령을 포함 |
| 생성기 계약·기존 소유 경로 | `independent-qa/generator-contract-report.json`의 **92 PASS / 0 FAIL**, `owner-integration-report.json`의 **21 PASS / 0 FAIL**. 이전 계층의 역투영·최종화·사전 검사와 pruning16출력 일치를 확인. 부분 원장 전체 재생성은 기존 descriptor 오류로 차단 |
| 수정 후 전체 정적 | `static-after.txt`, exit1, **25 PASS / 0 WARNING / 같은 기존16 ERROR**. `aggregate-comparison.json`에서 오류 이름·마지막 진단 일치, 새 통과 gate1개와 신규 오류0을 확인 |
| 파일·소스 보존 | `independent-qa/runtime-after-comparison.json`에서 **1,497→1,497경로, 추가·삭제0, 뉴스1파일 변경**. `preservation-after.json`에서 기존 잠금·donor 입력·기존 pycache의 변경0. 사용자 모드 선택 파일의 동시 변경은 아래 별도 관측으로 기록 |
| 실제 로드·UI·발화·저장 | 미실행. CHI3도시와 HBC/SIC 대안, 도시 미점령·소유국/전쟁 불일치·기발생 차단 및 저장 재로드의 현재 포트 관측이 남음 |

전체 정적16오류는 수정 전부터 있던 descriptor 계약, MIO·지도·건물·공유 override·교리·layout의 과거 source pin 차이와 그 연쇄 gate, 원장의 `.gitignore` 충돌 분류 등을 포함한다. 이번 작업에서 과거 source pins를 현재 설치본에 맞춰 갱신하지 않았다.

기존 저장소 `tools/__pycache__/`의21파일·1,088,888바이트는 정리 미결이다. 이번 helper·보고서·백업·미리보기와 Python cache 목적지는 모두 외부 작업 경로로 설정했다. 유지 source capsule의 입력 사본은 재현에 필요한 프로젝트 출처 자료다. Git branch/HEAD 변경, commit·push·외부 게시·업로드와 게임/launcher 실행은 수행하지 않았다.

부분 원장의 전체 재생성 시도는 `equipment ledger runtime mismatch: descriptor.mod`에서 멈췄다. 직접 단일 행을 생성한 실제 원장과 반복 적용은 별도 계약 검사로 확인했으며, 전체 원장 재생성 성공으로 기록하지 않는다. 수정 후 전체 검사에서도 기존 `.gitignore` 충돌 오류가 확인됐다.

독립 helper의 최초 후보 검사는 균일 CRLF 가정으로1실패를 기록했다. 실제 기준 파일은904CRLF·24bareLF이며 최종 출력은923CRLF·24bareLF다. helper를 기존 혼합 줄바꿈 계약에 맞춘 뒤68항목을 통과했고, 최초 보고서는 외부 `independent-qa/source-logic-preview.initial-line-ending-assumption.json`에 보존했다. 기본 `git diff --check`의 byte-exact 뉴스 CR 표시도 확인했으며 CR-at-EOL을 인식하는 공백 검사에서 통과했다.

검증 중 사용자 `dlc_load.json`이2026-11-12 02:27:49 KST에161→117바이트로 바뀌고, 선택 배열에서 국뽕팩이 빠져 원본 HOK·anime 구성이 된 것을 관측했다. 별도 HOI4 프로세스PID13564도 관측했다. 원인 행위자는 확인하지 않았으며, 이 작업의 도구는 해당 파일에 쓰거나 게임 프로세스를 실행·제어하지 않았다. `preservation-after-first-config-drift.json`은 최초 차이를, `user-configuration-drift.json`은 원래/관측 해시·선택·시각·프로세스를 보존한다. 최종 `preservation-after.json`의 전체 파일 보존 `pass=false`와 프로젝트 소스 보존 `source_preservation_pass=true`를 구분한다. 기존 잠금·donor 입력·pycache·그 외 감시한 사용자 파일은 같은 바이트였다. 이 관측은 호환판 실행 검증에 포함하지 않았다.
