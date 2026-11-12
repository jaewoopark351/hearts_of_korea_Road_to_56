# 2026-11-12 한국 신규 첩보원 초상화 이식

2026-11-12(KST). 사용자의 최신 원본 업데이트 반영 요청에 따라 한국 신규 첩보원 남녀 각4명의 전용 그림과 목록·GFX 연결, 관련 유지 문서와 지침을 선택 이식한다. 채택 그림은 donor의 후속 편집을 마친 **검은 중절모·정장·코트와 불투명 회색 배경8종**이다. 현재 문서 상태는 **첩보원 그림 8개·목록 구현 반영 / 범위 검사 통과 / 전체 정적 26 PASS·0 WARNING·기존 16 ERROR / 실제 RT56 모집·UI·저장 미검증**이다.

이 첩보원 계층의 검토·수정·재생성·검증이나 외국 현지 모집·cosmetic tag와의 연결 판단 전에 이 문서, [선택 입력 안내](../upstream/hok-operative-portraits-20261112/README.md), 기존 [과학자·이름 통합 기록](2026-11-12-korean-scientist-update-port.md)을 읽는다. 그림 원본·이전 revision·외부 증거 위치는 [개발 자료 안내](../HOK_DEVELOPMENT_ARTIFACT_ARCHIVE.md)를 따르고, 이름·고정 인물 표시·공유 소비자는 [변경 영향 절차](../HOK_CHANGE_COVERAGE_REVIEW.md)와 [현지화 검토 스킬](../skills/hok-rt56-localisation-review/SKILL.md)을 적용한다.

## 기준과 유지 입력

| 항목 | 이번 작업의 기준과 역할 |
|---|---|
| 호환판 | `C:/hoi/hearts_of_korea_Road_to_56`, `feat/korean-focus-update-20260922@7e29ce80158dfad1635d427f61e5c8b964088adf`, 시작 시 clean. 직전 과학자·이름 선택 이식11출력을 보존하며 확장한다. |
| HOK donor | `C:/hoi/hearts_of_korea`, `feat/korean-focus-expansion-ai@f1282d701bc47e47c119ca31faa6082e9e6ed1e6` 위 미커밋 첩보원 업데이트. 최신 커밋은 직전 과학자·이름 작업을 포함한다. |
| 선택 runtime | 한국 초상화 목록1개·전용 GFX1개·최신 DDS8개, 총10개. source 사본은 원본 SHA와 일치하며 각 사본의 실제 형식을 기록했다. |
| 유지 source 문서 | donor AGENTS·첩보원 계획·자산 manifest·최초 구현/후속 복장·배경 사건 기록2개, 총5개. 초기 투명 그림과 현재 불투명 그림의 출처·실행 이력을 구분한다. |
| 호환판 선조 | `compat_before/portraits/00_portraits_KOR.txt`,1,051바이트·SHA `5E13A8CED8ECEDD70DE77614739C6C2315D98498DE16471ED8BF6363CC2746CC`. 기존 army·navy·scientist 블록을 보존하는 입력이다. |
| source capsule | `docs/upstream/hok-operative-portraits-20261112/`. source10·documents5·선조1개와 현재11출력/과거 잠금·설치 참조16개 지문을 유지한다. |
| 설치 엔진·호스트 | 설치 metadata `Operation Postern v1.19.4.2.2da5 (0bdb)`, Steam build26409260. RT56 Workshop820260968, manifest1963361040482473746. 새 실행 checksum과 구분한다. |
| 외부 작업 경로 | `C:/hoi/test/hok-rt56-operative-update-20261112-01/`. `baseline.json`·`before/`와 새 진단·검증 결과를 보존한다. |
| 역사 입력 | 기존 `C:/hoi/test/hok-rt56-source-cache/sources/`와 과학자/이름 source capsule·잠금은 기존 역할·지문을 유지한다. |

개별 원본/사본·host/schema·고정 인물 참조의 경로·역할·SHA·크기·실제 줄바꿈은 [소스 manifest](../upstream/hok-operative-portraits-20261112/source-manifest.json)에 있다. source manifest SHA는 `43EBCEDBF7506AF5C3AD2F9C13E3469D64C1EA6900E2E18DFEBB98B8DF901CBA`다. source와 documents는 복사 전후 원본과 사본 해시를 대조해 일치했다. runtime 실행은 이 source 보존과 별도 단계로 기록한다.

donor 최신 커밋의 과학자 GFX·DDS8개는 직전 source capsule과 같은 해시다. 최종 donor 이름 파일 SHA `32AA863816EE3EACC02AA448E9CCBF0A4FCDB1AF92809CE23BDF2CC5DD096B9F`도 직전 이름 capsule과 같다. 이 커밋을 이유로 기존 이름 제외나 과학자 그림을 중복 적용하지 않는다. [기존 이름 선택 입력](../upstream/hok-scientist-name-exclusions-20261112/README.md)

## 채택 그림과 제작 이력

현재 자산 revision은 `2026-11-12-outfit-and-opaque-background`다. donor는 처음 생성한 가상 한국 첩보원8명의 얼굴을 입력으로 `image_gen.imagegen` 편집을 수행했다. 사용자가 요청한 《도깨비》 저승사자풍 복장을 검은 중절모·정장·코트, 흰 셔츠·검은 넥타이로 해석하고 회색 배경을 그림 전체에 포함했다. 모델명은 도구에 노출되지 않았다. 이번 호환판의 기여는 기존 최신 그림의 정확한 선택 복사와 단일 registry·생성 계층 통합이다. [보관 자산 manifest](../upstream/hok-operative-portraits-20261112/documents/docs/data/HOK_KOREAN_OPERATIVE_PORTRAIT_ASSET_MANIFEST.json)

현재 실제 DDS8개는156×210·uncompressed BGRA32·각131,168바이트·mipmap 헤더0이며 모든 알파값이255다. donor manifest와 각 파일의 해시가 일치하고 현재 외부 native contact sheet8종의 검은 모자·복장·회색 배경을 읽기 전용으로 확인했다. 과학자 DDS의 mipmap 헤더1·투명 그림과 역할별 규격을 따로 유지한다. 첩보원 후보 UI의 흰 칸 문제는 opaque 그림을 공급하는 donor 선택을 따른다. 공용 `naval_leader_selection_entry_bg.dds`와 타국 UI는 기존 host 파일을 유지한다.

| 위치 | 역할 |
|---|---|
| `C:/hoi/test/hok-operative-portraits-20261112-01/art/generated/` | 최초 인물 생성 PNG. 현재 편집의 얼굴·나이·표정 참조 입력과 이전 provenance다. |
| `C:/hoi/test/hok-operative-outfit-background-20261112-01/art/generated/` | 현재 선택 편집 PNG의 외부 보존본. |
| 같은 후속 경로의 `art/prompts.json`·`art/generation-provenance.json` | 정확한 편집 프롬프트·입력/도구 원본/선택 PNG의 경로·해시 대응. |
| 같은 경로의 `art/final-dds/conversion-manifest.json`·`native-contact-sheet.png` | 모자 캔버스 전체를 보존한 bicubic156×210 변환과 현재 작은 크기 검수 자료. |
| donor `source-before/`·`validation/staged-asset-revision-records.json` | 초기 투명 DDS와 현재 불투명 DDS·문서의 이전/현재 대응과 해시. |

위 외부 자료는 donor에서 이미 보존한 원본/변환/검증 이력이다. 이번 호환판의 새 helper·백업·로그·검증 출력은 별도 새 작업 경로에 둔다. 현재 그림은 source capsule의 정확한 DDS로 공급하며 새 그림을 생성하지 않는다.

## 소비자·분기별 처리

| 기능·ID·호출부 | 처리·기대 동작 | 근거와 남은 확인 |
|---|---|---|
| `KOR.operative.female`·`KOR.operative.male` | **수정**. 한국을 초상화 기준으로 삼는 신규 첩보원에게 성별별4개 sprite를 연결한다. | 국가별 operative 목록은 설치 La Resistance의 RAJ schema를 참조한다. 정상 RT56 모집 UI의 실제 선택은 미검증이다. |
| `GFX_HOK_KOR_operative_{female,male}_01`~`04` | **추가**. 전용 GFX8개와 실제 최신 DDS8개를 연결한다. | 실제 상대 경로·대소문자·파일 형식·고유 정의를 최종 소스 검사에서 확인한다. |
| 기존 KOR army·navy·scientist | **의도적 유지**. 기존 블록 뒤에 operative만 추가한다. |1,051바이트 선조와 원상 역투영해 다른 부분의 보존을 확인한다. |
| 기존 이름·과학자 runtime10개 | **의도적 유지**. 최종 로마자56/11/14항목, 과학자 GFX·DDS8개를 유지한다. | 직전 잠금의 실제11출력 중 한국 목록만 확장하고 나머지10개는 기존 해시를 보존한다. |
| 윤봉길·이봉창 | **의도적 유지**. La Resistance gate·명시 GFX·국적·특성·모집 설정·기존 초상화를 보존한다. | 호환판 history·고정 GFX·DDS2개를 별도 지문 참조로 기록했다. 신규 무작위 풀의 소비자로 대체하지 않는다. |
| RT56 외국 현지 모집8개 생성 지점 | **의도적 유지**. `nationalities = { FROM.OWNER }`와 `portrait_tag_override = FROM.OWNER`를 따른다. | 외국 초상화 기준을 한국으로 강제하지 않는다. 현재 RT56 결정 원본을 지문 기록했다. 실제 정상 현지 모집은 미검증이다. |
| 아시아 공용 풀·일반 타국·공용 후보 UI | **의도적 유지**. 한국 소유 목록·새 sprite·새 경로만 추가한다. | host portrait registry와 vanilla DLC GFX/UI를 읽기 전용으로 참조한다. |
| 이름·호출부호·능력·성별 확률·비용·슬롯 | **제외**. 이번 신규 초상화 연결 밖의 규칙은 기존 값을 유지한다. | 새 이름 제외나 생성 효과·게임 수치 변경을 추가하지 않는다. |
|13개 Korean cosmetic tag | **미확인**. 기본 KOR 목록의 선택·상속과 자연 경로를 구분한다. | donor 초기 강제 생성 결과는 해당 donor 입력과 시험 조건의 이력이다. 현재 RT56 자연 경로·실제 선택은 별도 확인이 필요하다. |
| 애니 서브모드·기존 저장·DLC 없음·멀티플레이 | **미확인**. 실제 물리 파일·저장 방식·지원 조건을 확인한 범위만 주장한다. | 신규 경로는 donor 애니의 `gfx/leaders/KOR` 교체 경로 밖이지만 현재 RT56 구성의 실제 선택을 대신하지 않는다. |

donor가 수집한 cosmetic 후보는 `KOR_Balhae`, `KOR_CHI`, `KOR_Goguryeo`, `KOR_Hwan`, `KOR_Hwan_neutrality`, `KOR_JAP`, `KOR_PRC`, `KOR_PRK_communism`, `KOR_SOV_communism`, `KOR_democratic`, `KOR_greater_Hwan_neutrality`, `KOR_neutrality`, `KOR_reichskommissariat_fascism`의13개다. 이 후보 명단과 강제 생성 관측을 현재 호환판의 자연 정치 경로 검증으로 바꾸지 않는다.

## 생성 소유권과 분류

기존 [소유 모듈](../../tools/upstream_scientists.py)과 [선택 잠금](../../tools/hok_scientist_update_lock.json)의 v3 확장으로 관리한다. top-level 과학자 source·이름 제외 capsule·역사 source pins를 유지하고 `operative_update`에 새 source manifest·선조와 현재 그림 계약을 연결한다. 기존11출력의 한국 목록1개를 확장하고 신규 GFX1개·DDS8개를 더해 최종 소유 출력은20개다.

한국 초상화 목록의 기존 `ADD` 분류를 유지하고 GFX는 `ADD`, DDS8개는 원본과 같은 `ASSET_COPY`로 기록한다. 기존 이름 출력의 `THREE_WAY_MERGE`와 과학자 분류·출처는 보존한다. 생성·역투영·사전 보호·원장은 같은 소유 API를 통해 최종 그림/목록과 역사 검사 경로를 연결한다. 정확한 최종 바이트일 때만 이전 registry로 역투영하며 원본·역사 cache를 덮어쓰지 않는다.

통합 목록은 1,505바이트이며 SHA-256은 `9825E25CD274449311AB43CE75DA29B15EA4DA98455164D5C8E0DE3B36F29181`이다. 원장은 1,568→1,577행으로 기존 초상화 행의 출력 해시·이유, AGENTS 문서 해시 한 칸과 새 GFX·DDS 아홉 행만 변경했다. 기존 이름 행과 과학자 출처·다른 원시 행은 보존했다. 소유 `ledger_bytes()`와 기존 문서 해시 생성 함수를 통해 반영했으며 반복 적용과 최초 선조 원장 재생 결과가 일치한다.

## 관련 지침의 출처와 적응

현재 donor AGENTS SHA는 `F80ACF2E2F32D68DA006D8DE44D2A2A8154340AFEBBA1D734B9A7711193E2F5D`다. donor commit `f1282d701bc47e47c119ca31faa6082e9e6ed1e6`에 포함된 역사적 이름 지침7줄과 그 위 미커밋 첩보원 조건부 읽기1행을 구분해 출처 기록으로 보존한다. [정확한 donor 지침 사본](../upstream/hok-operative-portraits-20261112/documents/AGENTS.md)

호환판의 조건부 읽기는 이 로컬 통합 기록을 가리킨다. 역사적 이름 지침은 HOK 소유의2차대전 콘텐츠와 승인된 변경 범위에 적용하도록 적응한다. 확인한 현대 정치인 실명·원어·로마자·철자/하이픈 변형과 이름·성의 조합을 검토하고, 특정 조합만 거를 수 없으면 해당 이름 구성요소를 제외하며 공유 소비자를 기록한다. 검증된 중복과 흔한 이름에 대한 추정을 구분하고 근거·출처·제외 이유를 남기는 유지 문서에는 이름을 기록할 수 있다. 적용 대상은 [기존 로컬 이름 기록](2026-11-12-korean-scientist-update-port.md)과 [후속 선택 입력](../upstream/hok-scientist-name-exclusions-20261112/README.md)을 따른다. 이 지침으로 현재 RT56 전 세계 이름 목록을 전수 수정하는 범위를 추가하지 않는다.

## donor 관측과 이번 호환판 확인

donor 최초 그림의 실행에서는 정상 남녀 모집·채용, 게임 생성 임시 저장의 전체 재시작 재로드와 애니 조합의 저장 인물 일부 표시를 기록했다. 별도 강제 생성 진단에서는 KOR와13개 cosmetic tag의 남녀28명·외국 기준4명을 비교했다. 최초 일반 저장 이름 변경은 errno2로 실패했다. [최초 donor 구현 기록](../upstream/hok-operative-portraits-20261112/documents/docs/incidents/2026-11-12-korean-operative-portraits.md)

현재 검은 복장·불투명 배경 revision은 donor 본체의 기존 저장된 남녀와 후보 화면8종, 새 일반 후보1개를 확인한 기록이다. 이번 그림 revision에서 새 저장은 시도하지 않았고 애니 조합·자연 정치 경로·외국 현지 모집 결정·장기 진행·멀티플레이는 미검증이다. 이전 진단 저장을 불러올 때 추가된 함대 경고64종의 원인 귀속도 미확정이다. [현재 donor 복장·배경 기록](../upstream/hok-operative-portraits-20261112/documents/docs/incidents/2026-11-12-korean-operative-outfit-background.md)

| 확인 단계 | 이번 호환판의 현재 기록 |
|---|---|
| source·문서·선조 보존 |10runtime·5문서·선조1개 정확한 사본과 해시 일치. 기존11출력·잠금 및 host/schema/fixed 참조16개 지문을 기록했다. |
| DDS와 native 그림 | 실제8개 DDS의 해시·헤더·알파를 읽고 현재 donor 자산 manifest와 대조했다. 기존 외부 native contact sheet8종을 육안 확인했다. |
| 생성·연결·회귀·원장 | 독립 소스 QA 72 PASS·0 FAIL, 외부 전환 계약 46 PASS·0 FAIL, 기존 생성 경로 검사 33 PASS·0 FAIL. 최초 CLI는 10파일을 반영했고 이후 `--check`·`--apply`·`--check`는 0 written이다. runtime 1,506→1,515파일이며 기존 목록 1개와 신규 GFX 1개·DDS 8개가 대상이다. |
| 전체 정적 결과·기존 실패 | 사전·사후 모두 26 PASS·0 WARNING·16 ERROR, exit 1이다. 기존 오류 16개의 이름과 상세 문장이 같고 신규 오류는 0개다. 원래 원시 gate를 확장해 첩보원도 같은 생성 경로에서 검사하며 기존 gate를 제거하지 않았다. |
| 현재 플레이세트·DLC·유효 파일 | 읽기 전용 metadata는 `한국test01`, 원본 HOK→일반판 영어 번역, `l_korean`, `disabled_dlcs=[]`다. 사용자 데이터는 `C:/Users/jaewo/OneDrive/문서/Paradox Interactive/Hearts of Iron IV/`이며 호환판 launcher는 이 작업 소스를 가리킨다. 실제 호환판 모집을 실행한 결과로 사용하지 않는다. |
| 실제 RT56 모집·고정/타국 회귀·cosmetic·애니 UI | 미검증. donor 기록과 이번 source 검사를 실제 실행의 근거로 합산하지 않는다. |
| 실제 채용·진행·저장·cold reload·과거 저장 | 미검증. donor의 임시 저장 결과와 현재 호환판 결과를 구분한다. |
| 대상 밖 파일·donor·cache 보존 | 기존 다른 잠금 27개·이전 capsule 785파일·donor 1,859파일·활성 cache 1,490파일·기존 runtime 1,505파일이 같다. 기존 이름 56/11/14와 과학자 GFX·DDS는 같은 바이트다. host/사용자 설정 14파일·설치 참조 16파일·선택 donor 입력/문서 15파일과 RT56 manifest도 유지됐다. HEAD `7e29ce8` 위 미커밋 작업 트리이며 Git 기록 변경·푸시·업로드는 수행하지 않았다. |

이번 완료 범위는 최신 그림과 모집 목록의 소스 이식, 관련 지침 적응과 위 정적 확인이다. 실제 RT56의 정상 모집·채용, 고정 인물·외국 현지 모집·cosmetic tag·애니 조합의 표시와 저장·재로드는 미검증이다. donor의 과거 관측과 현재 호환판의 소스 결과를 구분한다.


## 증거 위치와 검사 이력

외부 작업 기준은 `C:/hoi/test/hok-rt56-operative-update-20261112-01/`다. `baseline.json`과 `before/`는 구현 전 소스·도구의 지문과 선조 사본이다. `independent-qa.json`, `recruitment-owner-contract-qa.json`, `owner-integration-checks.json`은 각각 최종 72·46·33개 확인을 기록한다. `static-before.json`·`static-before.txt`, `static-after.json`·`static-after.txt`, `aggregate-comparison.json`은 사전/사후 전체 검사와 같은 오류 16개를 기록한다. `ledger-update.json`과 후보 CSV는 두 기존 행의 세 필드 변경·신규 아홉 행·멱등성을 보존한다. `environment-before.json`·`environment-after.json`과 `preservation-after.json`은 환경과 파일 보존을 기록한다.

기존 생성 경로 검사에서는 실제 `generated_additive_file()`→한국 분할 finalizer→최종 초상화 소유자와 inherited preflight를 거쳤다. 이름·초상화의 원본/직전/최종 상태를 검증했고, 현재 통합 목록을 역사 검사용 최초 목록으로 역투영하며 미등록 바이트는 숨기지 않는다. 반복 CLI 적용은 20출력을 같은 바이트로 유지한다.

읽기 전용 Git clean-filter와 유효 EOL 재현 검사에서 runtime·capsule 37경로를 확인했다. 새 첩보원 GFX는 실제 CRLF 35개·1,351바이트이므로 `text eol=crlf`, 기존 과학자 GFX는 LF이므로 기존 `text eol=lf`를 따른다. source capsule은 `-text`로 보존한다. native 그림의 기존 contact sheet 관측은 `visual-review.json`에 있으며 실제 게임 UI 관측을 뜻하지 않는다.

최초 Git helper는 새 binary DDS에 명시적 `-text`가 있어야 한다고 잘못 가정해 멈췄다. 실제 Git binary 감지와 clean-filter 결과를 확인하고 helper만 수정했다. 최초 기록과 helper는 `independent-qa.initial-git-binary-assumption.json`·`.py`에 보존했다. 최종 72개 검사는 실제 필터 결과와 원본 바이트를 기준으로 통과했다.

기존 전체 오류는 descriptor 계약, 과거 host/source pin 차이와 지도·건물·공용 override·교리·layout 등의 연쇄 gate, 원장 `.gitignore` 충돌 분류를 포함한다. 과거 핀을 완화하지 않았으며 전체 통과·호환판 실행 완료로 보고하지 않는다. 기존 `tools/__pycache__/` 21파일·1,088,888바이트는 같고 외부 정리 대기다. 새 helper·fixture·보고서·백업·진단 출력은 외부 작업 경로에 둔다. 저장소의 source capsule·선조는 결정적 생성의 유지 입력이다.
