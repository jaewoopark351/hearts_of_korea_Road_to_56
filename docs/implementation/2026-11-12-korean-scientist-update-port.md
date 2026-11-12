# 2026-11-12 한국 신규 과학자 초상화와 이름 후보 이식

2026-11-12(KST). 원본 업데이트 검토 후 사용자가 승인한 한국 신규 과학자 초상화8개와 이름 후보 제외, 관련 유지관리 기록과 조건부 지침을 호환판에 선택 반영한다. 초기 `Geunhye`1개 제외를 구현하던 중 donor의 후속 이름20개 제외를 확인해 같은 기능의 최신 입력으로 채택했다. 최종 로마자 이름 풀은 **남성56·여성11·성14개, 총81개**다. 현재 문서 상태는 **11개 출력 구현 반영·범위 검사 통과 / 전체 정적 26 PASS·0 WARNING·기존 16 ERROR / 실제 RT56 실행 미검증**이다. 아래 소스 근거와 donor 실행 이력을 이번 호환판 결과와 구분한다.

이 계층의 이름·그림·연결·소스 잠금을 수정하거나 재생성·검증하기 전에 이 문서와 [초기 선택 입력 안내](../upstream/hok-scientist-update-20261112/README.md), [추가 이름 제외 입력](../upstream/hok-scientist-name-exclusions-20261112/README.md), [변경 영향 절차](../HOK_CHANGE_COVERAGE_REVIEW.md), [현지화 검토 스킬](../skills/hok-rt56-localisation-review/SKILL.md)을 읽는다. 이미지 원본이나 과거 경로를 찾을 때는 [개발 자료 안내](../HOK_DEVELOPMENT_ARTIFACT_ARCHIVE.md)를 함께 따른다.

## 기준 소스와 위치

| 항목 | 이번 작업의 기준과 역할 |
|---|---|
| 호환판 | `C:/hoi/hearts_of_korea_Road_to_56`, `feat/korean-focus-update-20260922@51ac53cbe8c25eeb203b6f6914ce53b0a5cc2c58`. 구현 시작 시 clean. 기존 도시 함락 뉴스·한미 방위·핵분열·산업 이식 위에 적용한다. |
| HOK donor | `C:/hoi/hearts_of_korea`, `feat/korean-focus-expansion-ai@cdc022eee15fbf7404d4cb30cf2d0102d29e550c` 위 미커밋 작업. source11개와 유지 문서6개를 정확한 사본으로 보존했다. 전체 donor dirty 목록은 manifest에 기록한다. |
| 설치 엔진 | 설치 metadata `Operation Postern v1.19.4.2.2da5 (0bdb)`, Steam build26409260. 설치 값은 새 호환판 실행의 checksum을 뜻하지 않는다. |
| RT56 | Workshop820260968, manifest1963361040482473746. 공용 이름·초상화 registry와 descriptor를 읽기 전용으로 지문 기록했다. |
| 바닐라 schema | `portraits/998_scientist_portraits.txt`, `interface/_scientists_portraits.gfx`, 이름 목록·launcher metadata를 읽기 전용 참조로 고정했다. 국가별 scientist와 남녀 sprite 목록의 근거다. |
| 새 외부 작업 경로 | `C:/hoi/test/hok-rt56-scientist-update-20261112-01/`. `baseline.json`과 `before/`는 구현 전 호환판·donor·활성 cache 보존 기준이며 새 시험·진단 출력도 이 경로를 사용한다. |
| 유지 source capsule | `docs/upstream/hok-scientist-update-20261112/`. `source/`는 선택 donor runtime의 정확한 사본, `documents/`는 donor 유지 문서의 정확한 사본이다. |
| 후속 이름 capsule | `docs/upstream/hok-scientist-name-exclusions-20261112/`. 추가 제외 후 이름 원본1개와 유지 문서2개의 정확한 사본을 새로 보존한다. 초기 capsule과 baseline은 유지한다. |
| 역사적 활성 cache | `C:/hoi/test/hok-rt56-source-cache/sources/`. 이번 선택 delta와 별도 입력이며 기존 source pins와 바이트를 보존한다. |

개별 원본·사본·설치 참조의 경로·SHA-256·크기와 복사 역할은 [초기 소스 manifest](../upstream/hok-scientist-update-20261112/source-manifest.json)와 [후속 이름 manifest](../upstream/hok-scientist-name-exclusions-20261112/source-manifest.json)에 있다. 현재 플레이세트·언어·DLC 배열의 수집 결과와 실제 적용 여부는 아래 검증 절에서 구분해 기록한다. donor 문서의 HOK+애니 실행 조건을 호환판의 현재 플레이세트로 추정하지 않는다.

초기 source는 남성71·여성16·성14개, 이름 원본 SHA `08C6CAD04DED79DFD18DD49AE32E8D68570D77FF78DB0BEE3E1DED17D6745C8D`를 동결했다. 작업 중 donor의 이름·manifest·사건 기록3개가 동시 변경됐고, 후속 기록이 사용자 요청과 추가 제외20개를 설명한다. 해당3개만 새 capsule로 보존해 최종56/11/14개와 이름 SHA `32AA863816EE3EACC02AA448E9CCBF0A4FCDB1AF92809CE23BDF2CC5DD096B9F`를 선택했다. 초기4,733바이트·SHA `F06C9DE9A35C43A86BA7B76AD447A7E511060A035B2F396C659F8459A320F781` 출력은 v1 중간 결과로 남긴다. 처음 baseline 대비 donor 전체 바이트 보존을 주장하지 않으며 이 동시 원본 변경과 호환판 작업의 변경을 구분한다.

## 채택한 최종 동작과 영향 범위

| 기능·소비자 | 처리·기대 동작 | 근거와 남은 확인 |
|---|---|---|
| KOR 신규 남녀 이름 | **수정**. 초기 `Geunhye`와 후속 남성15·여성5항목을 제외하고 남은 로마자 철자·순서·인용·성별 목록과 성14개를 유지한다. 최종 남성56·여성11·성14개다. | 최신 donor 이름 SHA `32AA863816EE3EACC02AA448E9CCBF0A4FCDB1AF92809CE23BDF2CC5DD096B9F`. 전체 이름 출력의 선택 delta와 보존 범위를 정적으로 확인한다. |
| 같은 KOR 이름 풀을 쓰는 다른 생성 인물 | **의도적 공통 적용**. 신규 과학자를 포함한 이 풀의 소비자에게 같은 후보 제외가 적용된다. | 기존 엔진 이름·성 조합 순서를 유지한다. 이미 생성된 인물과 기존 저장의 이름은 이관 대상에서 제외한다. |
| 이름·성의 독립 조합 | **의도적 공통 적용**. 제외한 이름 토큰은 남은 모든 성과의 조합에서 빠진다. | 알려진 정치인과 같은 성의 조합만 차단하는 새 필터를 추가하지 않는다. 모든 현대 정치인과의 중복 제거를 입증한 전수 조사로 해석하지 않는다. |
| 한국 신규 과학자 남녀 초상화 | **수정**. 기존 KOR 정의에 남성4·여성4 scientist sprite 목록을 추가하고 전용 DDS8개를 연결한다. | donor 한국 초상화 목록·GFX·자산 manifest를 함께 동결했다. 실제 RT56 모집·표시·성별 선택은 확인 대기다. |
| 한국 고정 과학자4명 | **의도적 유지**. 황부길·조경연·도상록·김용관의 character ID·개별 sprite·현지화·시작 모집을 유지한다. | 신규 무작위 풀과 고정 character 소비 경로를 구분해 소스/회귀 확인한다. |
| 기존 KOR 육군·해군 목록 | **의도적 유지**. 기존 목록에 scientist만 추가한다. | 기존 파일의 다른 블록·스프라이트 바이트 보존을 확인한다. |
| KJP·KCH·RKY·TWN 이름과 RT56 타국/공용 풀 | **의도적 유지**. 기존 HOK 선택 출력과 host 정의를 보존한다. | donor `common/names/00_names.txt` 전체를 runtime에 복사하지 않는다. 공유 이름 토큰의 전역 현지화도 추가하지 않는다. |
| 한글 직접 이름과 부분 키 방식 | **제외**. 현재 donor의 로마자 복원과 사용자 지정 제외를 채택한다. | donor 문서 중간의 한글102개·여성17개와 초기101개는 이전 단계의 이력이다. 부분 키 방식의 원시 키 노출은 donor 시험에서 반증됐다. |
| 초상화 능력·특성·비용·선택 가중치와 다른 gameplay | **제외**. 이번 표시·후보 변경 밖의 동작을 유지한다. | 대상 밖 runtime 파일의 전후 보존을 최종 확인한다. |
| 애니 서브모드·cosmetic tag·기존 저장·모든 언어와 DLC | **미확인**. 현재 호환판 구성의 실제 유효 정의와 동작은 별도 관측이 필요하다. | donor의 일부 표본과 저장 결과로 호환판의 지원 범위를 확대하지 않는다. |

추가 남성 제외15개는 `Gun`, `Woong`, `Yoon-Gi`, `Yoongi`, `Jaeyoung`, `Jinho`, `Jiwon`, `Jungho`, `Junghoon`, `Minseok`, `Minsoo`, `Sanghoon`, `Sungho`, `Sunghoon`, `Sungmin`이고 여성5개는 `Bora`, `Ji-young`, `Kyung-hee`, `Jiyoung`, `Kyunghee`다. 선정 근거는 동결 donor가 기록한 확인된 실명 중복과 사용자 요청에 한정한다. [최신 donor 이름 기록](../upstream/hok-scientist-name-exclusions-20261112/documents/docs/incidents/2026-11-12-korean-random-name-localisation.md)

분류는 기존 이름 출력의 `THREE_WAY_MERGE`, 한국 초상화 목록의 기존 분류를 유지하며 신규 GFX는 `ADD`, DDS8개는 `ASSET_COPY`로 연결한다. 최종11출력은 기존2개와 신규9개다. 개별 분류·최종 출력 SHA·원장 반영은 아래 최종 확인에 기록한다.

## 이미지 출처와 기존 donor 관측

초상화는 donor가2026-11-12 `image_gen.imagegen`으로 생성한 가상 한국 과학자 남녀 각4명이다. 원본 manifest에는 프롬프트·입력 이미지 없음·투명 배경·모델명 `not_exposed`, 선택 생성 PNG와 crop/변환 및 DDS 해시가 있다. 이번 호환판은 해당 DDS를 바이트 그대로 재사용한다. 생성 원작과 호환판의 선택 복사·registry 통합 기여를 구분한다. [보관 자산 manifest](../upstream/hok-scientist-update-20261112/documents/docs/data/HOK_KOREAN_SCIENTIST_PORTRAIT_ASSET_MANIFEST.json)

선택 PNG는 기존 `C:/hoi/test/hok-scientist-portraits-20261112-01/art/generated/`, 프롬프트는 같은 `art/prompts.json`, 생성 대응은 `art/generation-provenance.json`, 변환 기록은 `art/final-dds/conversion-manifest.json`에 유지된다. 이는 기존 donor 원본 보존 역할이다. 이번 호환판의 진단·백업 경로는 별도 새 작업 경로를 사용한다. [경로 대응과 사본 역할](../upstream/hok-scientist-update-20261112/source-manifest.json)

donor의 HOK+애니 구성에서는 정상 모집한 남녀 표본과 고정4명 공존을 관측했다. 날짜 진행 후 만든 임시 저장의 같은 프로세스 UI 재로드에서는 남녀 표본이 유지됐다. 최초 즉시 저장의 남성 미표시와 저장 rename 오류는 미해결이며 전체8개·두 번째 저장의 cold reload·과거 저장·cosmetic tag는 미검증이다. 이름의 최종 로마자 복원·`Geunhye` 제외와 후속20개 제외 후 실행도 미실시다. 이 기록은 이번 RT56 호환판 실행의 증거로 사용하지 않는다. [donor 초상화 기록](../upstream/hok-scientist-update-20261112/documents/docs/incidents/2026-11-12-korean-scientist-portraits.md), [donor 최종 이름 기록](../upstream/hok-scientist-name-exclusions-20261112/documents/docs/incidents/2026-11-12-korean-random-name-localisation.md)

## 생성 소유권과 지침 반영

[소유 모듈](../../tools/upstream_scientists.py)과 [선택 잠금](../../tools/hok_scientist_update_lock.json)은 동결 donor 입력·초기/후속 source manifest와 호환판 이전 출력을 검증한 뒤11출력을 재현한다. `build_outputs()`가 이름21토큰 제외·KOR scientist 목록·전용 GFX·DDS를 생성한다. `finalize_one()`·`historical_bytes()`·`preflight_outputs()`는 기존 `review_followup`의 생성·역투영·사전 보호 경로에 연결한다. 실제 말단 바이트와 일치할 때만 역사 검사용 직전 출력으로 역투영하며 기존 이름 출력의 생성 소유권과 source pins를 보존한다.

`ledger_bytes()`는 기존 도시 함락 뉴스 뒤에 연결해 변경2행의 최종 해시/이유와 신규9행의 분류·출처를 관리한다. 전체 validator의 새 원시 `--check` gate는 역사 역투영된 중간 출력과 별개로 실제 최종11출력을 검사한다. `compat_before/`는 이전 출력의 정확한 선조 사본이고 source manifest와 선택 잠금은 각각 donor/참조 지문과 생성 계약을 소유한다. 원장은 1,559행에서 1,568행이 됐다. 기존 이름·초상화 두 행의 출력 해시와 이유, AGENTS 문서 해시 한 칸을 갱신하고 GFX 한 행과 DDS 여덟 행을 추가했다. 다른 원시 행과 기존 출처 필드는 보존했다. 최종 이름 출력은 4,682바이트이며 SHA-256은 `67A034FD66369E8EB6A4B02DE173C174F33E1C50A1EAE7335B05930FD8185F5B`다. 첫 단계와 최종 단계 모두 소유 `ledger_bytes()`와 기존 문서 해시 생성 함수를 사용했고, 최초 기준 원장에서의 재생과 반복 적용 결과가 같다.

donor AGENTS의 신규 과학자 조건부 읽기1행을 호환판의 로컬 통합 기록 링크로 적응했다. donor의 원문 계획과 AGENTS는 정확한 출처 사본으로 보존하고, 활성 읽기는 이 문서의 RT56 소유권·생성 소유권·최종 이름 상태·검증 구분을 따른다. donor AGENTS SHA는 `BD9232F4C2616669108988847E9F3AC0D8F76FFDCCB4A7E4361902926DDC5EF0`다. 이 지침 적응으로 donor의 전체 runtime·언어 계약·애니 설정을 가져오지 않는다.

## 이번 호환판 확인과 남은 항목

| 확인 단계 | 현재 기록 |
|---|---|
| 선택 입력·문서 사본 | source11·documents6개를 복사 직후 원본 SHA-256과 대조해 일치. 설치 참조10개의 읽기 전용 지문을 manifest에 기록. |
| 후속 이름 입력·문서 사본 | 추가 제외 후 이름1·유지 문서2개를 별도 capsule에 복사. 복사 전후 원본과 사본 SHA가 일치했고 초기 manifest SHA도 유지됐다. |
| 대상 runtime 생성·연결·보존 | 1,497→1,506파일. 기존 이름·초상화 목록 2개 수정과 GFX 1개·DDS 8개 추가다. 초상화 DDS는 원본과 같은 바이트이며 156×210·BGRA32·mipmap 1·각 131,168바이트다. 남녀 목록과 sprite 8개의 연결, 기존 육군 9개·해군 4개와 고정 과학자 4명의 연결을 소스로 확인했다. |
| 표적·회귀·전체 정적 검사 | 독립 소스 QA 72 PASS·0 FAIL, 외부 전환 계약 36 PASS·0 FAIL, 기존 생성 경로 검사 19 PASS·0 FAIL. 새 CLI의 반복 `--check`·`--apply`는 0 written이다. 전체 정적은 25 PASS·0 WARNING·16 ERROR에서 26 PASS·0 WARNING·같은 16 ERROR가 됐다. 오류 이름과 상세 문장이 같고 신규 오류는 0개다. |
| 플레이세트·언어·DLC·실제 유효 정의 | 읽기 전용 metadata는 `한국 anime 테스트`, HOK→애니, `l_korean`, `disabled_dlcs=[]`다. 실제 사용자 경로는 `C:/Users/jaewo/OneDrive/문서/Paradox Interactive/Hearts of Iron IV/`다. 호환판 외부 descriptor는 이 작업 소스를 가리키며 저장소와 같은 RT56·Korean Language·RT56 한국어 번역 의존성을 가진다. 현재 선택 구성은 호환판 실행 결과가 아니며 이번 작업에서 게임을 실행하지 않았다. |
| 실제 RT56 모집·고정 인물·타국 회귀 UI | 미검증. 소스/정적 검사와 별도 결과가 필요하다. |
| 실제 효과·일반 진행·저장·cold reload | 미검증. donor의 임시 저장 표본과 이번 호환판 결과를 구분한다. |
| 대상 밖 파일·source cache·donor 보존 | 기존 잠금 27개·이전 capsule 759파일·활성 cache 1,490파일·고정 콘텐츠 1,191파일과 host/사용자 설정 14파일의 지문이 일치했다. 초기 donor 1,846파일 중 이름·이름 manifest·이름 기록 3개의 동시 변경만 관측됐고 최신 사본과 현재 donor가 같다. 호환판 HEAD `51ac53c`는 유지되며 구현은 미커밋 작업 트리다. |

이 기록의 완료 범위는 소스 이식과 위 정적 검증이다. 실제 RT56의 정상 과학자 모집, 남녀 초상화 선택, 고정 인물 공존, cosmetic tag 상속과 저장·재로드는 미검증이다. 이름 후보 수 감소는 의도한 변경이며 구체적인 엔진 선택 확률도 실행으로 확인하지 않았다. Git 커밋·푸시·게시·업로드는 수행하지 않았다.


## 검사 증거와 초기 시도의 처리

증거 경로는 `C:/hoi/test/hok-rt56-scientist-update-20261112-01/`다. `independent-qa.json`, `scientist-module-contract-qa.json`, `owner-integration-checks.json`은 각각 최종 72·36·19개 검사의 범위와 결과를 기록한다. `static-before.json`·`static-before.txt`와 `static-after.json`·`static-after.txt`, `aggregate-comparison.json`은 승인된 작업 전/최종 전체 검사와 오류 대조다. `ledger-update.json`, `ledger-followup-update.json`과 후보 CSV는 1차 원장 반영과 후속 이름 한 행의 두 필드 변경, 반복 적용 및 최초 원장 재생을 기록한다. `environment-before.json`·`environment-after.json`, `preservation-after.json`은 환경과 파일 지문을 구분해 보존한다.

처음 전체 검사는 검사 실행과 새 계층 등록이 겹쳐 임시 import 오류 세 개가 생겼다. 그 22 PASS·19 ERROR 결과는 `static-before-initial-concurrency.json`과 `static-before-initial.*`에 보존하고 최종 기준에서 제외했다. 기존 세 도구와 AGENTS의 바이트를 복원·대조한 뒤 재실행한 25 PASS·16 ERROR를 기준선으로 채택했다. 추가 이름 제외 전 중간 결과 26 PASS·16 ERROR는 `static-after-v1.*`와 `aggregate-comparison-v1.json`에 남겼으며 최종 이름 풀의 결과로 사용하지 않는다.

첫 독립 QA의 65 PASS·4 FAIL은 `independent-qa.initial.json`에 보존했다. 세 항목은 동시 donor 변경을 검출했고 한 항목은 기존 공용 생성기가 함께 제공하는 두 출력을 helper가 누락한 가정이었다. `donor-source-drift-observed.json`은 변경된 세 원본과 남성 15개·여성 5개 추가 삭제를 기록한다. 새 capsule로 입력을 고정하고 helper를 수정한 최종 결과가 72 PASS·0 FAIL이다. 별도 생성 경로 helper의 같은 단일 출력 가정은 `owner-integration-initial-failure.json`에 기록했다. 최초 단계의 29개 전환 계약과 v1 도구·잠금은 `before-name-followup/`에 보존했고 최종 36개 계약은 v2와 추가 이름 제외를 검사한다.

전체 검사의 기존 16개 오류에는 descriptor 계약, 오래된 host/source pin의 지도·건물·공유 override·교리·layout 연쇄 차이와 원장의 `.gitignore` 충돌 분류가 있다. 기존 전체 원장 재생도 descriptor 계약에서 막히며 이번 선택 계층의 재생 통과와 구분한다. 이 작업에서 과거 소스 핀을 완화하거나 해당 오류를 수선하지 않았다.

기존 저장소 `tools/__pycache__/`의 21파일·1,088,888바이트는 지문이 같으며 외부 정리가 남아 있다. 새 helper·시험 fixture·보고서·백업과 중간 결과는 위 외부 작업 경로에 둔다. 저장소의 두 source capsule과 `compat_before/`는 재현 생성기에 필요한 유지 입력이다.


## 후속 Git 요청과 체크아웃 속성 보정

2026-11-12 후속 요청으로 사용자가 이 변경의 커밋·푸시와 영어 커밋 메시지를 승인했다. 작업 전 로컬 HEAD와 원격 기능 브랜치는 모두 `51ac53cbe8c25eeb203b6f6914ce53b0a5cc2c58`였다. 포함 범위는 기존 수정 9개와 신규 38개, 총 47파일이다.

스테이징 뒤 실제 Git 체크아웃 바이트를 대조하여 신규 GFX의 속성 오류를 확인했다. `interface/HOK_KOR_scientist_portraits.gfx` 원문은 LF 35개·CR 0개·1,316바이트인데 CRLF 속성이 지정돼 있었다. `.gitattributes`의 해당 행을 `text eol=lf`로 교정했다. GFX·DDS·이름·초상화 runtime과 동결 입력·잠금의 바이트는 보존했고 새 CLI의 11출력 검사가 통과했다. 독립 검사에서 runtime 11개와 capsule 26개, 총 37개의 체크아웃 바이트·크기가 작업 파일과 일치했고 runtime 11개는 잠금 해시와도 일치했다.

전체 47개 중 46개는 체크아웃 바이트가 동일했다. 해시로 잠그지 않은 기존 Python 도구 `tools/review_followup.py` 한 개는 저장소의 기본 줄바꿈 변환만 적용되며 LF로 비교한 본문은 같다. CR을 줄 끝으로 인식한 작성 파일의 staged 공백 검사는 통과했다. 동결 donor 사본의 기존 들여쓰기·공백은 출처 해시를 보존한다.

후속 작업의 외부 기록은 `C:/hoi/test/hok-rt56-scientist-commit-20261112-01/`에 둔다. `pre-commit-inventory.json`은 최초 47개 파일과 앞선 검증 지문의 일치를, `staged-byte-review.initial.json`은 발견 당시 체크아웃 차이를, `staged-verification.json`은 교정 뒤 최종 포함·바이트·공백 검사를 기록한다. 영어 메시지 원문은 `commit-message.txt`, 실제 커밋·푸시 결과는 `commit-receipt.json`과 Git 이력을 따른다.
