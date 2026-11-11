# 2026-11-12 중국 도시 함락 뉴스 선택 입력

이 계층의 입력·출력·생성기·검사를 다루기 전에 이 안내, [잠금](../../../tools/hok_capture_news_update_lock.json), [생성기](../../../tools/upstream_capture_news.py), [소스 manifest](source-manifest.json)를 읽는다. 지역 판단에는 [로컬 주 참조 스킬](../../skills/hok-rt56-state-reference-review/SKILL.md)과 [변경 영향 절차](../../HOK_CHANGE_COVERAGE_REVIEW.md)를 적용한다. 실제 적용과 전체 검사 결과는 [포트 구현 기록](../../implementation/2026-11-12-korean-capture-news-port.md)을 따른다.

## 원본·사본·역할

원본 HOK는 읽기 전용 `C:\hoi\hearts_of_korea`, `feat/korean-focus-expansion-ai@cdc022eee15fbf7404d4cb30cf2d0102d29e550c`다. 이번 변경 전 조상은 `424e4d962803b5cc7a3667a7df4604fbd128733a`이며, 호환판 시작은 `feat/korean-focus-update-20260922@180ffad37821835be3338e66e27c755982a16468`다. 두 작업 트리는 시작 시 깨끗했다.

| 유지 사본 | 원본과 보존 역할 |
|---|---|
| `before/events/NewsEvents_KOR.txt` | donor 조상 커밋의 Git blob `e51b56a0e92c33df1f3646129e154d4743c55d70`. Git blob의 정규화된 줄바꿈을 그대로 보존한 역사 입력이며 과거 물리 checkout 바이트로 표시하지 않는다. |
| `runtime/events/NewsEvents_KOR.txt` | donor 최신 커밋의 실제 깨끗한 checkout 바이트. donor blob `33e644953d16ae7f0903b3548091f370b11f7887`과 원본 경로를 manifest에서 구별한다. 이 사본은 직접 배포하는 호환판 출력이 아니다. |
| `compat_before/events/NewsEvents_KOR.txt` | 위 호환판 시작 시점의 실제 생성 출력. SHA-256 `10E07D6B7469C9853EAAAE77837A1EDFC4DC95B8BBF9EFDCF37CD7186983DB64`, 13,495바이트. 기존 비한국 뉴스 제거를 이미 포함한다. |
| `documents/docs/HOK_STATE_REFERENCE_ALIGNMENT_PLAN.md` | donor 최신 기준의 의도·적용·과거 실행 기록. 원본은 `C:\hoi\hearts_of_korea\docs\HOK_STATE_REFERENCE_ALIGNMENT_PLAN.md`이며 donor 실행을 RT56 포트 실행으로 합산하지 않는다. |
| `host/rt56/history/states/` | `C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968`의 실제 대상 주5개를 동결한 읽기 전용 입력. 608·1114·1116은 도시 부모 주이며 1035·1037은 donor 번호가 현행 host의 다른 지역이라는 근거다. |
| `host/vanilla/launcher-settings.json` | 설치 원본의 엔진 버전 메타데이터 사본. 게임 실행 증거나 사용자 설정 사본이 아니다. |

각 사본의 크기·SHA-256·원본 절대 경로·커밋·역할은 manifest에 있다. 원본 파일을 이동하거나 기존 cache를 대체하지 않았다. `C:\hoi\test\hok-rt56-source-cache\sources\`의 과거 활성 입력과 모든 기존 잠금은 그대로 유지한다. 새 capsule은 별개의 선택 변경 입력이다.

## 선택 변경과 RT56 대응

설치 기준은 `Operation Postern v1.19.4.2.2da5 (0bdb)`와 RT56 Workshop item820260968 manifest `1963361040482473746`이다. 생성기는 실제 대상 주5개·게임 버전 메타데이터·manifest를 다시 확인한다. 설치 원본 `documentation/triggers_documentation.md`의 `controls_province` 국가 trigger 설명과 `common/national_focus/soviet.txt`의 국가 scope 사용례도 원본 경로·크기·SHA로 고정한다. 두 schema 원본은 복사하거나 변경하지 않는다.

| 사건·분기 | 선택한 동작 | 처리 |
|---|---|---|
| 베이핑 `newsk.22` | KOR의 도시9843 통제. 부모 주608의 CHI 소유·대CHI 전쟁 또는 HBC 소유·대HBC 전쟁 | **수정**: donor의 도시 기준·소유국/전쟁 짝을 그대로 반영. 현행 host608은 베이징이다. |
| 난징 `newsk.23` | KOR의 도시11913 통제, 부모 주1114의 CHI 소유·대CHI 전쟁 | **수정**: donor1035를 이 trigger 안에서만 RT56 난징1114로 대응. host1035는 Finnmark/NOR다. |
| 충칭 `newsk.24` | KOR의 도시6999 통제. 부모 주1116의 CHI 소유·대CHI 전쟁 또는 SIC 소유·대SIC 전쟁 | **수정**: donor1037을 이 trigger 안에서만 RT56 충칭1116으로 대응. host1037은 Hame/FIN이다. |
| 사건 ID·기여 주석·일회 표식·2일 MTTH·major·선택지·문구·그림 | donor의 세 인접 기여 주석을 보존하고 기존 호환판의 다른 바이트를 유지 | **의도적 유지**. 기존 영어 번역이나 그림을 donor 전체 파일로 교체하지 않는다. |
| 신징 `newsk.18`와 다른 뉴스 | 기존 동작 | **의도적 유지**. 미발생 수정 대상이 아니다. |
| `newsk.27`, `newsj.1–4`, 기존 전역 지도·타국 시스템 | 기존 제거/소유 계약 | **제외**. 새로운 trigger3개 때문에 삭제한 비한국 모듈을 복구하지 않는다. |
| 실제 RT56 사건 등록·자동 발화·부분 도시 통제·차단·수신 UI·저장 | 이 소스 계층이 입증하지 않는 엔진 결과 | **미확인**. donor 실행 기록은 원본 구성에만 적용한다. |

## 재현 소유권과 증거

역사적 `tools/prune_non_korean_content.py`가 만든 단일 ADD 출력 위에 `tools/upstream_capture_news.py`가 제한된 후속 계층으로 적용된다. 생성기는 donor 전후의 LF 비교에서 세 trigger와 인접 기여 주석만 변경됐음을 먼저 입증하고, 호환판의 정확한 직전 trigger3개를 교체한다. 그 안의 난징·충칭 부모 주만 위 표에 맞춘다. 다른 줄바꿈·BOM·선택지·내용은 호환판 바이트로 보존한다.

최종 단일 출력은 **14,032바이트**, SHA-256 **`4C3331C7AB9DC0782DD90210780CF7710787325ED7418DEE0FD3748C0398A5F7`**다. `historical_bytes`는 정확히 입증한 최종 출력만 직전 바이트로 역투영하며, `finalize_one`은 정확한 직전/최종 출력만 받는다. `preflight_outputs`는 보호 파일의 미등록 수정·중복 별칭을 거부한다. 원장 처리는 기존 ADD 분류를 유지하며 해당 행의 출력 해시·이유만 변경하고 다른 원시 행을 보존한다. 과거 입력·출력 잠금을 현재 바이트에 맞춰 고치지 않는다.

새 helper·미리보기·보고서는 **`C:\hoi\test\hok-rt56-capture-news-20261112-01\agent-generator\`**에 있다. `check_generator.py`, `expected-news-events.txt`, `ledger-preview.csv`, `generator-qa.json`은 유지 source capsule과 다른 외부 검증 산출물이다. generator API 검사20개가 통과했다. 독립 literal3블록 전체 바이트 재구성, 역투영·멱등성·미등록 수정 거부, 원장 한 행의 두 필드만 변경 및 다른 원시 행 보존을 확인했다. Python은 `PYTHONDONTWRITEBYTECODE=1`과 `-B`로 실행해 저장소 cache를 만들지 않았다.

이 안내의 generator 증거는 실제 게임/UI/효과/저장 검증이 아니다. 전체 생성 계층 연결·적용·aggregate 결과와 기존 저장소 시험 산출물 미결 상태는 위 포트 구현 기록에 별도로 남긴다. 이 작업은 donor·Workshop·설치본·사용자 데이터·기존 cache를 변경하거나 Git commit/push·게시·업로드하지 않는다.
