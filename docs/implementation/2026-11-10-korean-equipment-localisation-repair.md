# 한국 장비명 한영 재정의 구현·검증

작성: 2026-11-10, Asia/Seoul. 현재 상태: **선택 범위 v6 구현·한영UI/수집·임시변경 복구 및 별도 승인된 영구 외부RTK37바이트 동기화 완료**. 자체 QA39/0·독립 QA35/0, aggregate28 PASS·0 WARNING·기존11 ERROR(exit1)이며 KO07·EN04 각각 수정15/17문구·3guard·JAP 대표7표시를 관측했다. 출력은 영어17키 `ADD`·한국어1,308키 `THREE_WAY_MERGE`·descriptor `OVERRIDE`다. EN03 이름 검증0·정상 UI 종료 미관측·원인 미확정과 v1–v5 실패·EN2 화면 유실은 보존한다. 실제 외부 `.mod`는341바이트5D5FAB…이며 그 외 metadata는 원래 상태다. 영구 적용 후 새 게임은 실행하지 않았고 같은 바이트의 KO07·EN04 결과를 기록된 범위로 사용한다.

이 수선의 코드·소스·표시 우선순위를 변경하거나 재생성·검증하기 전에 [범위 계획](../plans/2026-11-10-korean-equipment-localisation-repair-plan.md), [선택 입력 안내](../upstream/hok-equipment-localisation-20261110/README.md), [현지화 스킬](../skills/hok-rt56-localisation-review/SKILL.md), [변경 영향 절차](../HOK_CHANGE_COVERAGE_REVIEW.md)를 읽는다. 언어 의존성은 [ADR-0003](../decisions/0003-localisation-contract.md), 한국/비한국 소유권은 [ADR-0004](../decisions/0004-hok-korean-content-priority.md)를 따른다.

## 승인과 기준

최초 요청은 설명과 문서화였고, 그 단계는 계획의 역사로 유지한다. 이후 사용자가 전체 구현 방향을 인용하며 `AGENTS.md, /docs 읽고 구현해줘`로 한국어·영어 구현을 승인했다. 실제 UI 확인을 위해 사용자 데이터의 별도 쓰기 경계를 설명한 뒤, 사용자는 **프로필·기존 로그·저장 백업, 영어/한국어 모드·언어 임시 변경, 새 게임 실행, 종료 후 복구**를 추가 승인했다. 기존 저장은 로드하거나 덮어쓰지 않는다. 커밋·푸시·업로드는 이번에 승인되지 않았다.

| 항목 | 시작 기준 |
|---|---|
| 작업 소스 | `C:\hoi\hearts_of_korea_Road_to_56`, `feat/korean-focus-update-20260922@2523bf455514c79a3538f0475dc922329afb185d` |
| 기존 변경 | 직전 문서 작업의 README·ADR-0003·새 계획을 보존. 게임/runtime 변경은 없었음 |
| HOK donor | 읽기 전용 `C:\hoi\hearts_of_korea@596b221bb994d93fce552d3ee1ba70fa9b5640f1`, 기존 산업/연구망 미커밋8개 보존 |
| 설치 게임 | Steam build26409260, `Operation Postern v1.19.4.2.2da5 (0bdb)`. 프로세스별 실제 체크섬과 구별 |
| RT56 / 번역 | `820260968` manifest1963361040482473746 / `2769576030` manifest3192804258057474440. 계획 입력8/8 지문 일치, 기존 host pin4,823개 일치 |
| 사용자 데이터 | `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV` |
| 시작 로그·선택 | 최신14:18 로그는 일반 HOK+일반판 영어 번역 `(c191)`·DLC36. 현재 디스크는 영어·포트 선택. 이들을 새 포트 실행 증거로 혼합하지 않음 |
| 외부 작업 | `C:\hoi\test\hok-rt56-equipment-localisation-20261110-01\` — 이하 `<TEST>` |

`baseline.json`, `runtime-before.json`, `maintained-inputs-before.json`, `rt56-files-before.json`, `translation-files-before.json`, `user-profile-hashes-before.json`에 역할별 지문이 있다. 외부 source cache와 과거 source capsule은 유지한다. 새 입력10개는 시험 자료가 아닌 [유지할 선택 입력](../upstream/hok-equipment-localisation-20261110/README.md)이다.

## 적용 내용과 보존

### KO06 실패와 v6 전환 결정 — 적용 전 기록

v5의 독립 정적 검사는36 PASS/0 FAIL(원래33항목에 aggregate 비교3항목 추가), 과거 계층 연동4 PASS/0 FAIL이었다. `static-after-v5-narrow-dependency.txt`의 aggregate는28 PASS/0 WARNING/기존11 ERROR이며, traceback 도구 경로·행번호만 정규화한11오류 본문은 기준선·v4와 동일했다. 이는 소스 결과다.

새 한국어 `ko-06`은 v5의 좁은17키와 저장소·외부 descriptor의 RTK 의존성을 함께 사용했다. `screenshots/06-amphibious2-detail.png`에서 짧은 이름은 KLVT-2지만 상세 제목·해금 안내는 **4식 카츠**였다. 따라서 좁은17키와 의존성만으로 전체 표시가 해결된다는 주장은 DISPROVEN이다. 이 실행은1949년형·남은 전체 범위·일본 대조를 끝내지 않았으며 그 항목을 실패 또는 성공으로 추정하지 않는다.

이 기록에서 다음 v6는 한국어만 v4와 정확히 같은1,308키 동일 경로 병합(82,181바이트, SHA `DF40639AF64C8C307CD6CEBE5327CBFE2228B0B4C79B82D33F83C96450376F8A`)으로 복원하고 v5의397바이트 descriptor·영어1,072바이트는 유지하도록 결정했다. 근거는 이 두 요소를 함께 쓴 KO05의9문구 정상 관측과 KO06의 재실패다. KOR17값만 변경하고 비한국1,291값·기존 주석·나머지 바이트를 보존한다. RTK 없는 한국어 구성은 지원 확인 범위에서 제외한다. RTK 없는 영어 구성은 최종 새 실행으로 확인한다. 이 결정은 아직 v6의15/17 전체 UI 통과를 뜻하지 않는다. 아래는 적용 후의 현재 출력이며 v5 설명은 뒤에 당시 이력으로 남긴다.

### 현재 출력 — v6

[생성기](../../tools/korean_equipment_localisation.py)와 [독립 잠금](../../tools/hok_equipment_localisation_lock.json)의 현재 revision은 `2026-11-10-equipment-localisation-v6-host-merge-dependency`다. 아래3출력을 소유한다. 영어는 고유 경로의17키 `ADD`, 한국어는 실제 RTK provider와 같은 경로의1,308키 `THREE_WAY_MERGE`다. v4 병합을 v5에서 잠시 대체한 뒤 v6에서 정확히 같은 바이트로 복원했다.

| 현재 출력 | 분류·크기·SHA-256 |
|---|---|
| `localisation/english/replace/zz_HOK_KOR_equipment_overrides_l_english.yml` | `ADD`, 1,072바이트, `F1C4044B30BBE48D1702AF4D4757963601C6427AC1CE10FF6D4ACFFE17EAF967` |
| `localisation/korean/replace/r56e_equip_motor_mech_l_korean.yml` | `THREE_WAY_MERGE`, 82,181바이트, `DF40639AF64C8C307CD6CEBE5327CBFE2228B0B4C79B82D33F83C96450376F8A` |
| `descriptor.mod` | `OVERRIDE`, 397바이트·LF, `A3A75B5F463DE4548062E152F464E403F4B14D3371A2CE233F1B7D2E3C203386` |

한영 현지화는 UTF-8 BOM·언어 헤더와 동일한 영어 기여 메모를 가진다. 영어는 v2와 동일한17키·CRLF, 한국어는 v4와 동일한1,308키·원 번역의LF와 마지막 개행 부재를 유지한다. 한국어는17 KOR값만 바꾸며 비한국1,291키·주석·그 밖의 raw 바이트는 RTK 원문과 같다. 한국어 본문은 한국어, 영어 본문은 기존 영국 영어를 따른다. 기존 장비 현지화 쌍의 각286키·바이트와3guard는 바꾸지 않았다. 작업 전 runtime1,476파일 중 **descriptor1개 변경·1,475개 동일**, 새 현지화2개 추가이며 gameplay 파일 해시는 모두 유지된다. 한국어 원문1,291키를 복사하지 않았다는 설명은 좁은 v5 당시만 해당한다.

저장소 descriptor는 기존 `The Road to 56`·`Korean Language` 의존성과 나머지 필드·ID를 보존하고 `The Road to 56 Korean Translation` 및 `#20261110_kpopmodder: Keep compatibility localisation after the active RT56 Korean translation.` 메모를 추가했다. `replace_path`·launcher 전용 `path`·업로드 ID는 추가하지 않았다. 정확한 이전 입력은 이 저장소 commit `2523bf455514c79a3538f0475dc922329afb185d`의 Git blob `4c1fd9af7d752bef207285980fe9854a4f4086bd`다. 원문은 **263바이트·raw LF**, SHA-256 `AA150D6CE82A7779C3D4C3FCDC962A82FA269327F005330B565723CA87BBE247`이며 기존 runtime과 같았다. EN04의 실제 system.log에서 RTK 없는 영어2모드를 확인했다. 저장소397바이트와 시험용 외부341바이트·복구된 원래 외부304바이트는 서로 다른 역할이다.

| 계획의 후보 | 실제 처리 |
|---|---|
| 상충13키 | **변경 적용.** 기존 HOK의 K-511·KHT-1/2·KAPC-1·KLVT-1/2·KMRL-27 전체/짧은 이름을 그대로 재사용 |
| 추가형4키 | **표시명 추가.** `KOR_mechanized_equipment_x[_short]`는 KAPC-1 1949년형, `_x_2[_short]`는1953년형. 영어 전체 이름은 `KAPC-1 (1949/1953) Infantry Armoured Vehicle`, 짧은 이름은 `KAPC-1 (1949/1953)` |
| 유지3키 | **기존 원문 유지.** K-311 전체/짧은 이름과 K-511 짧은 이름은 새 파일에 불필요하게 복제하지 않고 보존 검사를 연결 |
| 기술·성능·비한국 | **선택 구성의 소스 보존.** 연구 해금·시간·장비 수치·AI·기존 variant/history는 변경하지 않음. 한국어 병합의 JAP·타국·generic 등 비대상1,291키는 기존 RTK 원문과 같음. RTK 없는 한국어 구성은 추가 번역 영향 때문에 제외하며 실제 표시와 선택 구성은 새 UI에서 별도 확인 |

새 네 값은 호환판이 작성한 표시명이다. 기존 HOK `mechanized_equipment_3`의 KAPC-1과 RT56 `mechanized.txt`의 부모 계통 `3→x→x_2`, 연도1949/1953에 근거한다. 원본 HOK 값이나 실제 역사 기종이라고 주장하지 않는다. `_x`의1949년 기술 해금은 확인했고 `_x_2`의 명시적 현재 기술 해금은 찾지 못했으므로 이름만 공급하며 정상 연구 접근을 새로 만들지 않는다. 별도 KOR 설명을 요구하는 consumer 근거가 없어 `_desc`는 추가하지 않았다.

## 재현·검사·원장 연결

- 기존 source/영어 lock을 덮지 않고, 새 capsule의 정확한 원문과 명시된 새4값으로 출력한다. 실제 원문·선택 host·설치/latest manifest·게임 버전 drift는 거부한다.
- `validate_port.py`의 raw gate가 정확한3출력·영어17키·한국어1,308키 중17값 delta와1,291비대상 raw 바이트·보존 원문·정확한3의존성 descriptor를 확인한다. 기존 중복 검사에서는 **등록13키와 해당 언어의 기존 korea_equipment/새 출력 두 정확한 경로·동일 값·정확한 실제 바이트**만 허용한다. 다른 키·제3파일·언어·변조는 기존처럼 실패한다. 폐기한 루트 한국어 경로의 locale 예외는 제거했다. 이는 소스 검사 예외이지 실제 UI 우선권의 증명이 아니다.
- `source_snapshot.py --english-check`는 새 영어 파일1개와 정확한 생성 바이트를 명시적으로 확인한다. 과거 영어 키 총량과 역사 핀·내용 검사는 그대로다.
- `build_integration_manifest.py`의 full/scoped 경로는 영어 `ADD`/`SHIPPED`·한국어 `THREE_WAY_MERGE`/`GENERATED`2행을 마지막에 붙이고, 기존 descriptor 행의 `output_sha256`·추가 `reason`만 명시적으로 투영한다. **다른1,540개 원본 raw 행과 descriptor의 나머지 필드**를 보존하며 최종1,543행이다. 새 파일의 가짜 donor Git blob을 만들지 않고 기존 포트/RTK 입력·해시·신규 명칭 작성·생성기/잠금을 reason에 기록한다.
- `review_followup.historical_bytes`는 기존 계층의 검사보다 먼저 descriptor만 정확한397바이트 새 입력에서263바이트 옛 입력으로 역투영한다. 정확한 옛 입력은 그대로이며, 그 밖의 입력은 역투영으로 승인하지 않는다. 현지화2개는 작업 전 없던 추가 파일이다. 과거 lock·pruning 정책은 바꾸지 않는다. `.gitattributes`는 동결 입력의 `-text`, 영어 현지화CRLF·한국어 병합LF·실제 descriptor LF를 보존한다.

## 실제 정적 결과와 수선 이력

| 관측 | 결과·근거 |
|---|---|
| 작업 전 aggregate | **27 PASS / 0 WARNING / 11 ERROR**, exit1. `<TEST>/static-before.txt`, receipt와 `pristine-tools-export.json`. 사전31도구를 외부로 내보내 `__file__`/하위 실행 경로만 조정했으며 runtime1,476 전후 차이0 |
| 최초 기준선 시도 | 도구 export 전환 과정에서 root 요청으로 소유 validator만 중단. 이 시도는 별도 보존하며 완료 결과나 새 실패로 계산하지 않음 |
| 최초 적용 | 새 생성기로2출력 기록. 초기 원장 단계는 선행 AGENTS 해시 갱신 전의 바이트를 받아 엄격한 이전 해시에서 거부됐고 원장은 쓰지 않음 |
| 원장 순서 수선 | `<TEST>/ledger-predecessor-analysis.json`에서 차이는 AGENTS 출력 해시 한 셀뿐이며 기존 `build_documentation_csv` 뒤에는 정확히 이전B570 원장이 됨을 확인. 새 append를 그 뒤에 연결해 원장 갱신. 기존 lock이나 해시 gate를 완화하지 않음 |
| 독립 QA 최초 | `<TEST>/qa/independent-preview-qa-initial.json`. 캐시된 `build_outputs` 뒤 원본 변조 시 duplicate helper가 True를 반환한 실제2실패와, 적용 후에도 preview가 runtime 무변경을 기대한 가정1실패를 보존 |
| duplicate helper 수선 | 매 호출에 실제 원문과 동결 원문 바이트를 비교하도록 보완. production을 변조하지 않은 메모리 기반 거부 검사로 재확인 |
| 독립 QA 최종 | **886 PASS / 0 FAIL**, `<TEST>/qa/independent-runtime-qa.json`. 새 이름·한영 버전/토큰/BOM/CRLF·13상충·3guard·286원문·기존 입력/잠금·host·정확2추가·후속 계통과 변조 거부 확인. 실제 엔진/화면/저장 검사가 아님 |
| 새 raw gate | `korean_equipment_localisation.py --check` 통과. 실제2출력이 생성 바이트와 일치 |
| 기존 영어 gate | `source_snapshot.py --english-check` 통과, `<TEST>/english-after.txt`. 역사 총량·한국어 보존 계약 유지 |
| 작업 후 aggregate | **28 PASS / 0 WARNING / 11 기존 ERROR**, exit1, `<TEST>/static-after.txt`. `aggregate-comparison.json`에서 traceback 도구 경로·행번호만 정규화한 오류 본문11개가 사전과 같음을 확인 |
| 원장 보존·멱등성 | `<TEST>/ledger-preservation.json`: 이전1,541행의 전체 바이트 prefix 동일, 새2행만 append, 현재 원장 재적용 동일. 최종1,543행 |

이 표의 `static-after.txt`와886/0은 첫 파일명 후보의 결과다. 실제 UI와 후속 검사는 아래에 별도로 기록한다. 이전 산업 업데이트나 과거 C1의 성공을 이번17키의 실행 통과로 사용하지 않는다.

## 첫 파일명 실패와 후속 파일명 후보

영어 `en-01`은 `replace/HOK_KOR_equipment_overrides_l_english.yml`을 추가한 상태에서 새 KOR 게임을 시작했다. 연구 카드에는 Type98 So-Da·Type1 Ho-Ki·Ho-Ha·Type5 Tarenso·Toyota Su-Ki·Type4 Ka-Tsu가 남았고 상세 제목도 일본식 이름이었다. `<TEST>/runtime-session/en-01/{ui-observations.json,screenshots/}`에 실패 관측을 보존한다. 따라서 이 구성에서 **새 replace 파일만 만들면 해결된다는 가정은 DISPROVEN**이다. K-511 짧은 이름은 원래 충돌이 없는 보존 키여서 그것 하나가 보이는 것은 성공 근거가 아니었다.

다음 후보는 두 파일명에만 `zz_`를 붙였다. 17키/언어의 값·순서·주석·BOM·줄 끝은 그대로이며, 영어1,072바이트 SHA-256 `F1C4044B30BBE48D1702AF4D4757963601C6427AC1CE10FF6D4ACFFE17EAF967`, 한국어1,057바이트 `0BF14E0FEF7CEA851156D5B3AF59CE505EAD0DFFF800E89CC2CFA03B0376CE4A`다. descriptor·dependencies·replace_path는 바꾸지 않았다. 잠금 v2는 실패한 v1의 모듈·잠금·출력 해시를 기록하고, 생성기의 폐기 처리는 정확한 자체 구파일2개에만 적용한다. 이전 원장1,541행의 바이트 해시 `B570CDFF9F5375151230FBCEA7AFD73B64AD835959DB1A6FB5DB440034B2CD39`는 그대로며 최종2행의 이름만 바꿨다. 원장 v1 `45C253…`에서 v2 `7C507D…`로의 자체2행 변경을 정확한 이전 해시로 제한했다.

`<TEST>/filename-candidate-v2/`는 v1 보존 사본·적용 영수증·61/0 좁은 검사를 담는다. `<TEST>/qa/independent-runtime-qa-v2-zz.json`의 독립 검사는 **903 PASS / 0 FAIL**이다. 기존1,476 runtime 파일·장비286키·3guard 보존, 같은 payload·옛 파일 부재·원장 prefix와 최종2행·엄격한 영어/중복 gate·변조 거부를 확인했다. 최종 aggregate는 `<TEST>/static-after-v2-zz.txt`에서 **28 PASS / 0 WARNING / 11 기존 ERROR**, exit1이다. `aggregate-comparison-v2-zz.json`은 사전과 v1 양쪽의 오류 본문11개가 같음을 확인한다. 도구 traceback 경로·행번호만 정규화했고 검사 중8개 보호 파일은 바뀌지 않았다. 정적 결과 자체는 엔진 우선권을 증명하지 않는다.

### 한국어 폴더 후보 v3

v2의 한국어 실패 뒤 한국어 출력만 `localisation/replace/zz_HOK_KOR_equipment_overrides_l_korean.yml`로 옮겼다. 영어 경로와 한영17키의 바이트는 동일하다. 과거 v2는 `<TEST>/folder-candidate-v3/before/`에 보존한다. 생성기는 정확한 자체 구경로3개만 등록 해시가 같을 때 폐기하며, 현재 원장과 정확한 v1/v2 원장 해시에서만 이 작업의2행을 재작성한다. 기존1,541행 prefix·영어 추가 행은 그대로이고 한국어 행의 경로만 바뀐다.

기존 validator는 첫 폴더 이름으로 locale을 판단하므로 루트 `replace/`를 `l_replace`로 오인했다. 등록된 한국어 **단일 경로와 정확한 생성 바이트**에만 locale 경로 예외를 연결했다. 임의의 루트 파일·잘못된 헤더·값·추가 키·다른 중복 경로는 계속 거부한다. `<TEST>/folder-candidate-v3/candidate-narrow-checks.json`은50/0, `<TEST>/qa/independent-runtime-qa-v3-ko-rootreplace.json`은77/0이다. 두 payload·기존 runtime1,476개·장비 원문286키와3guard·원장 prefix·새2출력 범위·거부 검사를 확인했다. 폴더 우선순위의 일반 법칙은 소스에서 확정하지 못했으며 실제 효과는 아래 새 실행에 한정한다.

## 실제 UI 실행·복구

### v3 실패 뒤 동일 경로 병합 결정 — v4에서 도입, v5에서 대체, v6에서 복원

`ko-02`의 cold restart에서도 루트 `replace/` 후보는 같은3문구에 실패했다. 연구 카드·상세는 시간 진행이나 연구 시작 없이 확인했고 정상 UI 종료 후99파일을 수집했다. 기존 저장82개 차이0·새 저장0이며 collection SHA는 `467F774300084296D562B2F610EF1E8FBA33E7702A964475000DD8E6180D744F`다. `<TEST>/runtime-session/ko-02/screenshots/00–04`와 `ko-02/loaded-source/`에 실패 화면과 실제 v3 입력을 보존한다. v3 aggregate는28 PASS/0 WARNING/동일한 기존11 ERROR, 좁은 독립 검사는77/0이었다. 정적 통과로 UI 실패를 덮지 않는다.

이 단계에서는 계획5.3의 조건부 통합 결정을 적용했다. **선택한 한국어 구성은 RT56+RT56 Korean Translation+호환판**이며 영어는 RT56+호환판이었다. 한국어만 실제 번역 provider와 같은 경로 `localisation/korean/replace/r56e_equip_motor_mech_l_korean.yml`에서 동결 RTK 파일을 병합했다. 이 파일은1,308고유 키 중 대상KOR17개와 비한국1,291개다. KOR17값만 기존 HOK13값·호환판 작성4값으로 치환하고 비한국1,291값·기존 주석·나머지 바이트를 보존했다. 새 기여 메모의 추가를 별도로 기록하고 영어의 좁은17키 출력은 유지했다. 이후 **v5에서 전체 병합을 좁은17키로 대체했다가 KO06 실패 뒤 v6에서 정확한 v4 바이트를 복원**했다. v6에는 당시와 달리 정확한 RTK 의존성도 함께 유지한다.

v4 방식은 RTK가 꺼진 한국어 구성에도1,291개 RTK 문구를 새로 공급할 수 있어 그 구성은 당시 지원·회귀 확인 범위에서 **제외**했다. 당시에는 전역 RTK 의존성 추가를 채택하지 않고 descriptor·replace_path를 유지했으며, 번역 파일 전체 누락을 막기 위해 대상17키만 남긴 동명 파일은 만들지 않았다. 좁은 v5에는1,291키 복사 자체가 없었지만, **같은 전체 병합을 복원한 현재 v6에서도 RTK 없는 한국어 구성은 보존·지원 확인 범위에서 제외**한다. 이는 RTK 없는 영어의 별도 새 실행이나 최종 Workshop 의존성 계약과 구분한다.

병합 입력은 기존 capsule의 RTK 원문 SHA `322541C886E096ECDC4C6F9EEA9DCE36EDA29911010EEE3B7B4AB482C0072974`를 그대로 사용했다. 원문·과거 잠금·v1/v2/v3 이력과 v4 revision·구출력 폐기·원장 경로를 보존한다. RTK 원 번역자의 저작·기여와 원문 주석을 유지했다. 설치된 번역에서 별도 LICENSE/CREDITS/README를 찾지 못했다는 것은 포괄 재배포 허가를 뜻하지 않는다. 현재 v6의 전체 병합을 공개 패키지·Workshop에 넣으려면 해당 번역 원문·명칭·기여의 고지와 배포 조건을 별도로 확인해야 한다. 이번 작업은 로컬 구현·시험이며 외부 게시를 하지 않는다.

승인된 확인은 영어 `RT56+호환판`, 한국어 `RT56+RT56 Korean Translation+호환판`의 새 게임에서 연구/해금 장비/생산·설계 이름을 보는 것이다. 기존 저장은 선택하거나 덮어쓰지 않는다. 새 게임은 이름 확인에 필요한 일시정지 상태를 유지한다. 일본 등 비한국 표시도 대조하며, 기존 저장 variant의 자동 개명·성능/해금 변경을 주장하지 않는다.

v4의 좁은 검사는55/0, 독립 검사는 `<TEST>/qa/independent-runtime-qa-v4-ko-exactpath.json`의162/0이다. 원 번역의17개 값 span을 되돌리고 정확한 새 메모만 제거하면 원문 바이트와 같음을 확인했다. aggregate는 `static-after-v4-exact-path.txt`에서28 PASS/0 WARNING/기존11 ERROR이며 사전·v1/v2/v3와 오류 본문이 같다. 그러나 `ko-03` 실제 차량 트리에서는 98식 소다·1식 호키/호하·5식 다연장·토요타 스키·4식 카츠 등 일본 이름이 다시 선택됐다. `<TEST>/runtime-session/ko-03/screenshots/01-kor-vehicle-tree-failed.png`에 보존한다. 동일 경로 파일의 실제 우선권도 이 선택 구성에서 성립하지 않았으며 성공으로 채택하지 않는다.

`ko-04`는 runtime v4·언어·DLC·같은 모드 집합을 유지하고 `dlc_load.json`의 선택 배열만 기존 `[호환판, RTK, RT56]`에서 `[RT56, RTK, 호환판]`으로 뒤집었다. 실행 후 세 번 읽은 배열은 준비 바이트와 같았고, `Active Mod` 목록은 두 실행 모두 RT56·RTK·호환판이었다. 그러나 새 KOR 차량 트리에는 같은 일본 이름이 남았다. `<TEST>/runtime-session/ko-04/screenshots/01-kor-vehicle-tree.png`와 `runs/ko-04/`에 준비·선택·수집 근거를 보존한다. 따라서 **배열 반전만으로 v4가 해결된다는 가설은 DISPROVEN**이며 일반 엔진 정렬 규칙은 확정하지 않는다.

후속 물리 파일 추적에서는 세 활성 모드의 모든 파일과 헤더를 확인했다. 해당 키를 공급하는 추가 `localisation_synced`나 다른 언어 헤더는 찾지 못했고, 한국어 병합 경로는 RTK와 정확히 같다. RTK의 실제 외부 descriptor는 `replace_path="localisation"` 및 RT56 의존성을 선언하지만 호환판의 외부 descriptor에는 RTK 의존성이 없었다. **v4 파일·선택 배열을 유지하고 실제 launcher descriptor에 RTK 의존성 한 줄만 임시 추가**하는 대조를 준비했다. 외부 `.mod`의 별도 읽기 전용 경계에 대해 후보와 복구 계약을 먼저 제시했고 사용자가 추가37바이트 한 줄의 임시 수정·시험·원상복구를 명시적으로 승인했다. 후보·diff·원본304바이트와 해시·정확 복구 조건은 `<TEST>/runtime-session/descriptor-dependency-trial/`에 둔다.

`ko-05`는 그 한 줄만 달랐다. 새 KOR 연구창에서 KHT-1/2·KAPC-1·두돈반 KMRL-27·KLVT-1/2 카드, KLVT-2 전체 제목, 1949년형 KAPC-1 전체/짧은 이름이 기대값으로 바뀌었다. `<TEST>/runtime-session/ko-05/screenshots/00–04`에 직접 저장했다. 이 대조에서 의존성 추가가 해당 v4 표시를 바꾸기에 충분했다는 것은 **CONFIRMED**다. 내부 VFS 정렬의 일반 법칙이나 1,308키 병합의 필요성을 증명한 것은 아니다. `Active Mod` 열거는 추가 전후 같았으며 로그 목록만으로 우선순위를 추론하지 않는다.

`ko-05`는 정상 종료 후99개 수집 사본을 확인했고 기존 저장82개 차이0·새 저장0이었다. collection SHA는 `08A33042D3B7618D809E6A3723C85AE6813CB4A54E4290F7DC52C354F4B866AB`다. 관측9문구 통과를 한영17키 전체나 최종 v5 UI의 통과로 확대하지 않는다.

### 후속 최소 계층 선택 — v5 구현 전 결정

구현 전의 전체 병합은 한국어 장비명17값을 고치기 위해 비한국1,291값까지 복사하는 방식이었다. 의존성 대조가 성공했으므로 **한국어도 같은17키의 고유 `zz_` 파일로 복귀하고 저장소 descriptor에 실제 RTK 이름을 의존성으로 추가**하는 좁은 후보를 선택했다. 기존 RT56·Korean Language 선언과 다른 필드·ID를 보존하고 전역 `replace_path`를 추가하지 않는 결정이다. 원본10입력과 v1–v4 이력을 유지하며 v4 전체 파일은 정확한 자체 해시가 같을 때만 폐기하도록 정했다. 새 후보의 UI 성공은 별도 cold restart에서 다시 확인한다.

descriptor 변경은 기존 원장의1행에도 영향을 준다. 동결1,541행 입력은 덮지 않고 descriptor 행의 출력 해시·추가 사유만 명시적으로 투영하며 다른1,540행과 그 행의 나머지 필드는 보존한다. 생성기·과거 역투영·현재 descriptor gate는 정확한 새/옛 바이트와 등록 해시로 이 변환을 제한한다. 임의 descriptor나 원장 변경을 허용하지 않는다. 이 후보에서는 양 언어 모두17키 `ADD`이며1,291개 타국 번역을 새로 공급하지 않는다.

RTK의 비현지화 파일도 추적했다. 런타임 interface5파일은 compat와 동일 경로 충돌이 없고, RT56과 겹치는4GUI의 차이는 번역 문구·글꼴이다. 나머지 한국어 글꼴 등록도 언어별 fontfile 참조1곳 차이이며 gameplay 정의는 없다. 같은 구성의 글꼴·장비 툴팁·관련 오류 로그를 확인하되 모든 외국 GUI가 실제 검증됐다고 하지 않는다. RTK가 없는 영어 실행도 새 descriptor로 다시 확인해, 선택한 두 구성에서의 동작과 최종 Workshop 의존성 계약을 구분한다. 사용자 외부 `.mod`의 변경은 계속 임시이며 시험 종료 후 원래 바이트와mtime으로 복구한다.

### v5 당시 구현·정적 통과와 KO06 UI 실패

위 결정대로 당시에는 한영 각17키 `ADD`와 descriptor `OVERRIDE`를 적용했다. 영어 파일은 계속 같고 한국어는 v2의1,057바이트와 같았다. v4 전체 병합 파일은 SHA `DF40639AF64C8C307CD6CEBE5327CBFE2228B0B4C79B82D33F83C96450376F8A`·82,181바이트가 정확할 때만 폐기했다. 당시 폐기 대상4개는 v1의 접두사 없는 두 파일·v3 루트 파일·v4 동명 전체 파일이었고 임의 파일이나 별도 편집은 거부했다. 당시 한국어 `zz_` 경로는 v2에서 재사용한 활성 출력이었다. 현재 v6에서는 그 좁은 경로를 폐기하고 v4 병합을 복원했다.

`<TEST>/v5-narrow-dependency/before/`와 `before-records.json`에 변경 전 v4 모듈·잠금·관련 도구·descriptor·속성·원장·출력11파일을 보존했다. 원래10개 capsule 입력, `source-manifest.json`과 모든 과거 lock/source pin은 바꾸지 않았다. descriptor 입력은 `descriptor-input.json`에 Git 객체·raw LF·263바이트·해시를 기록한다. 준비 중의 CRLF 가정은 실제 입력과 맞지 않아 적용 전에 거부됐으며 `preparation-history.json`에 정정 이력을 남겼다. 이 시도를 production 변경이나 통과 결과로 세지 않는다.

동결 `ledger_before.csv`의1,541행·SHA `B570CDFF9F5375151230FBCEA7AFD73B64AD835959DB1A6FB5DB440034B2CD39`는 그대로다. v5 원장은 그중 `descriptor.mod` 행(CSV 물리69행)의 **`output_sha256`·추가 `reason` 두 셀만 투영**했다. 나머지1,540개 raw 행과 descriptor의 다른 모든 셀은 byte-exact다. 투영된1,541행 base SHA는 `49A3EB2B8294C43E58BA8D8A68CD7DF1B572683064E68C6D4F6D9A0F24ECE341`, 당시 한영 `ADD`2행을 붙인1,543행의 SHA는 `8B5C7E14A5180610D0042CD16B5FE00068D438B5A4A37FFCD5063D78A4F4D3F2`다. 영어 추가 행도 v4와 같았다. v5 이후의 원장 전체가 옛1,541행 prefix와 동일하다는 주장은 하지 않는다. 당시에는 정확한 동결/투영 base와 등록된 v1–v4 전체 원장 해시에서만 전환하고 다른 행·필드·임의 tail을 거부했다. v6에서 승인한 v5 전체 해시를 추가했다.

`descriptor_historical_bytes(relative, data)`는 정확한 새397바이트를 옛263바이트로, 정확한 옛 입력을 그대로 처리한다. `review_followup.historical_bytes`를 통한 실제 선행 연결도 확인했다. raw gate는 현재3출력과 정확한 새 descriptor를 요구한다. 적용 전 preflight만 descriptor의 정확한 새/옛 바이트를 허용하며, 누락 descriptor·변조·중복 의존성·다른 ID·추가 `replace_path`를 임의로 승인하지 않는다.

| v5 관측 | 결과·외부 근거 |
|---|---|
| 적용·raw gate | `candidate-apply-report.json`: 새 한국어와 descriptor 기록, 정확한 v4 전체 파일 폐기. `korean_equipment_localisation.py --check`에서3등록 출력 일치 |
| 독립 좁은 QA | 최초 **33 PASS / 0 FAIL**에 후속 aggregate 비교3개를 추가한 **36 PASS / 0 FAIL**, `<TEST>/qa/independent-runtime-qa-v5-narrow-dependency.json`. 한영17키·286원문·3guard·원래10입력·기존 pin·descriptor만 기존 runtime 변경·1,475파일 보존·원장 두 셀과 다른1,540행·엄격한 역투영/변조 거부 확인. 두 시점의 해시는 아래 별도 기록 |
| 과거 계층 연동 | **4 PASS / 0 FAIL**, `<TEST>/v5-narrow-dependency/historical-integration-checks.json`. 정확한3의존성 gate와 review/split 경로에서 새 descriptor→옛AA150D… 및 옛 입력 유지 확인 |
| aggregate | **28 PASS / 0 WARNING / 11 기존 ERROR**, exit1. `<TEST>/static-after-v5-narrow-dependency.txt`·`static-after-v5-narrow-dependency-receipt.json`. 완료 로그SHA `9A14FE2F96F55981DFE9EC7FA57AE16E1B0FC4A647F59C0A18C99D039AA470BC`. traceback 도구 경로·행번호만 정규화한11오류 본문은 기준선·v4와 동일 |
| UI·수집 | `ko-06`의 KLVT-2 전체 제목·해금 안내 **실패**. 정상 종료 후99수집 사본 확인, 기존 저장82개 차이0·새 저장0. collection SHA `9818BB0DBC6E52A6BE58305A853241111A8B2081F4BB39D6A7B9F8CF25BA9201`. 전체15/17·1949년형·JAP·영어 재검증을 완료한 실행이 아님 |

v5의 초기33/0 보고서 SHA `4A79EAC272635DAC9B60A7C35ED25AEF9D9D08ABD98A0A1E3C99109A4B4C5466`는 `runtime-session/runs/ko-06/preflight-validation-links.json`과 `runtime-session/v5-helper-activation-and-preflight.json`에 보존됐다. 같은 보고서 경로에 기존33검사를 유지한 채 aggregate 비교3개를 덧붙인36/0의 SHA는 `6ACA71F9740C04304C823741C066850D2BEC0A7296C6375B9F7DD961180F5493`다. 별도33/0 보고서 원본 사본을 새로 만들었다고 주장하지 않으며, 해시가 다른 두 시점을 하나의 불변 영수증으로 취급하지 않는다.

`runtime-session/ko-06/independent-v5-failure-collection-review.json`은 raw99사본과 실제 v5 소스·36 DLC·한국어3모드·자연 종료를 검토했다. error.log는669기록/631고유 본문이며 KO05와 정확한 오류 본문·빈도가 같고 장비 현지화 관련 검색0건이다. 조용한 로그와36/0 정적 결과는 확인된 `4식 카츠` 오표시를 상쇄하지 않는다. 당시에는 승인된 외부 descriptor 차이만 수집 시점에 남아 최종 복구가 대기였으며, 뒤의 EN04 종료 후 별도 영수증으로 복구했다.

### v6 적용·정적 검증과 한영 실행·복구

`<TEST>/v6-host-merge-dependency/before/`와 `before-records.json`에 전환 직전 v5 모듈·잠금·관련 도구·descriptor·속성·원장·한영 출력11파일을 보존했다. v5 revision·출력·모듈/잠금 해시·KO06 collection과 원장8B5C…를 잠금의 추가 이력으로 유지한다. 원래10개 capsule 입력·manifest·과거 source pin은 그대로이며 descriptor A3A75…와 역투영·263바이트 Git 입력, 영어F1C404…도 변경하지 않았다.

한국어는 정확한 v4 병합 DF4063…/82,181바이트로 복원했다. 자체 구파일은 아래4경로만 등록된 해시·크기가 같을 때 폐기하며 모두 부재다. 현재 병합 경로는 폐기 대상이 아니다.

- `localisation/english/replace/HOK_KOR_equipment_overrides_l_english.yml`
- `localisation/korean/replace/HOK_KOR_equipment_overrides_l_korean.yml`
- `localisation/replace/zz_HOK_KOR_equipment_overrides_l_korean.yml`
- `localisation/korean/replace/zz_HOK_KOR_equipment_overrides_l_korean.yml` — 좁은 v5 한국어, 1,057바이트·0BF14E…

현재 원장은 **1,543행·942,562바이트**, SHA `78FDB9007133CA6E9E29A2AC1CDF7E3AA887F0D743C4875A344D3BCC613F531D`다. v5 원장에서는 한국어 마지막 행만 `THREE_WAY_MERGE`/`GENERATED`와 RTK 원문 해시·17/1,291 보존·v6 의존성 근거로 바꿨다. 투영1,541행 base49A3…와 영어 추가 행은 v5와 byte-exact다. 따라서 원래1,541행 중 **다른1,540개 raw 행·descriptor의 승인 두 셀 외 모든 필드**의 보존은 유지된다. 정확한 v5 전체 원장 해시를 전환 allowlist에 추가했으며 임의 변경은 허용하지 않는다.

| v6 관측 | 결과·외부 근거 |
|---|---|
| 적용·raw gate | `<TEST>/v6-host-merge-dependency/apply-stdout.txt`, `raw-check.txt`. 한국어 병합 기록·좁은 한국어 폐기 후3등록 출력 일치 |
| 자체 좁은 QA | **39 PASS / 0 FAIL**, `<TEST>/v6-host-merge-dependency/candidate-apply-report.json`. v4 exact bytes·17/1,291 보호·원문·중복/변조 거부·descriptor 역투영·원장 범위·물리 줄 끝과 최초 runtime1,476중 descriptor1개 변경/1,475동일 확인 |
| 독립 좁은 QA | **35 PASS / 0 FAIL**, `<TEST>/qa/independent-runtime-qa-v6-host-merge-dependency.json`, SHA `73D9F25FCAD563AD4086A7E2BED70C51EB48F200B6F92FDB7AF6C2CE8EC6606E`. 원본10입력·과거 lock·1,475runtime·한국어17/1,291 raw 보존·동일EN/descriptor·원장 범위·엄격한 변조 거부를 독립 확인. 엔진·aggregate 실행은 하지 않은 소스 검토 |
| aggregate | **28 PASS / 0 WARNING / 11 기존 ERROR**, validator exit1. `<TEST>/static-after-v6-host-merge-dependency.txt`, SHA `BA94BEC172CFB7CAAF307401E90E58A03E1A71F70F66AA764FCB81D8A8AD94B4`. 완료 receipt의 보호 source61파일 전후 변경0 |
| aggregate 독립 비교 | `<TEST>/aggregate-comparison-v6-host-merge-dependency.json`, SHA `8F5871B18E68D0831343359977F14841D22A2B04A7D6E5EC9CA0441B0B6C134A`. Python traceback 도구 경로·행번호만 정규화한11오류 본문·순서·빈도가 기준선·v4·v5와 동일, 새 오류/경고 본문0. 원래35/0 QA JSON은 변경하지 않은 별도 추가 기록이며 aggregate 전체 성공을 뜻하지 않음 |
| KO07 최종 시각 검토 | `runtime-session/ko-07/final-visual-coverage.json`, SHA `EC37495AE6C024A74D7F4BC1D0DB5D72DF072A44F3378FB97F718D39530AA912`. 새 캡처00–13의14PNG에서 **수정15/17문구·3guard 기대 문자열 확인, 불일치0·JAP 대표7표시 보존**. 06의 KLVT-2 전체 제목·해금 안내와10/11의1949년형 전체/짧은 이름 정상. 12의 생산 선택기는 현재 해금된K-311 guard만 확인. 초기00–12 한국어 보고서4BE8…도 변경 없이 보존 |
| KO07 종료·수집 | `runtime-session/runs/ko-07/collection.json`, SHA `DBEDA0241C63028B99A7B7C0FF096D5F12167F340D6F1C678EEC1ED94DA1D44E`. 정상 UI 종료 후 프로세스 부재,99수집 사본의 크기/해시 차이0·보관3출력 핀 일치·기존82저장 차이0·새 저장0·새 metadata0. 외부 `.mod`는 정확히 승인한37바이트 의존성 예외만 차이 |
| KO07 독립 로그 검토 | `runtime-session/ko-07/independent-final-log-review.json`, SHA `8C5D69140203415E57FAE04FF46500582A155E254C2E481B8A24EAB133D9F20C`. 실제 `(cf8c)`·36 DLC·RT56/RTK/호환판3모드, error.log671기록/631고유 본문. R0·KO06 대비 새 정확 본문0, 장비 현지화 관련 검색0건. KO06 대비 기존 random.log rename 본문 반복만2회 증가(2→4) |
| EN03 중단·수집 | **INTERRUPTED·이름 검증0·정상 UI 종료 미관측**. 수집SHA `3F217EFA526768DB820A3DFDCD920E2E03C2601B7902D430CE2CDD1AD446D6AB`, 독립 중단/로그 검토SHA `325F235B8D7C10A39D926929D02FD1263226C520D7BA926C5D2720A1EBB678F9`. normal flag=false·프로세스 부재·99사본/3출력 무결·기존82저장 차이0·새 저장0. 조용한 로그로 정상 종료나 UI 통과를 추정하지 않음 |
| EN04 최종 시각 검토 | `runtime-session/en-04/final-visual-coverage.json`, SHA `2469AB543B22687ED96013FCCA56824C4C8FCED720388E633D71DE0657060104`. 새00–13의14PNG에서 **수정15/17문구·3guard 불일치0·JAP 대표7표시 보존**. 초기00–12 보고서7590C2…와13PNG도 그대로 보존. 생산 선택기는 현재K-311 guard만 확인 |
| EN04 종료·수집·로그 | raw collection SHA `49ACFE4B02E0C107CEC6E766445F92E1C7FF91A94E91D18E06B1D0344E5A7CBB`, normal flag=true·프로세스 부재·99사본/3출력 무결·기존82저장 차이0·새 저장0. 독립 최종 로그 검토SHA `7245798E330B2A5384D84D8FDC3CF90F297C6DE850963434AD19491A04F7E242`: 실제 `(cf8c)`·36 DLC·RT56+호환판2모드, RTK 비활성. 로그671/631·KO07와본문/빈도동일·R0대비 새 본문0 |
| 외부 descriptor·프로필 복구 | descriptor 복구SHA `A41B38D75E8E3335F572B663985CDC7EB5A42F55AAE6E0B3F3671CAFAA59266B`, 원래304바이트A486F1…/mtime복원. 별도 파생 상태SHA `1D08F85E8DD70A19AFAEE088A714C77EB589BBF9EB6A887C87B2F4366F546908`를 검토한 뒤 `runtime-session/restoration.json` SHA `E0D4D449BE6AB3DF2EC951658BAF79B869BAA548EA5F152CD7395AAFECAED342`에서 metadata·기존 저장 차이0·프로세스 부재 확인. raw 수집은 수정하지 않음 |
| 별도 영구 RTK 동기화 | `runtime-session/permanent-descriptor-sync/receipt.json` SHA `D0E130B0ADF78816A9C53C602316DB268D3B8D4E90213827E66C9569BFDAC648`. 사용자의 `영구 반영해줘` 승인 뒤 원래304바이트에서 시험과 동일한341바이트5D5FAB…로 정확히37바이트 추가. 감사한65metadata 중 해당외부 `.mod`만 의도적으로 변경·다른 항목 원래 상태·프로세스 부재. 소스3출력/잠금/원장 변경과 새 게임 실행 없음 |

KO07 한국어 관측은 RT56+RTK+호환판,36 DLC, 화면과 system.log의 `1.19.4.2.2da5 (cf8c)`, `12:00, 1 January 1936` 일시정지 상태에 귀속한다. 초기 한국어 시각 보고서 SHA `4BE8C6B81CA6F1E4D3F5724894F08E419871E73996CDDAE258D86B8EC49E5774`에 일본 대조PNG13을 더한 별도 최종 시각 보고서를 만들었고 초기13PNG는 같았다. 후속 독립 로그 검토도 최종14PNG·시각 보고서와 수집 사본을 변경하지 않았다. 1953년형 `_x_2` 두 문구는 계속 소스 전용이다. exact lookup key는 소비 소스와 연결한 것이며 엔진 key telemetry는 아니다. 연구 시작·시간 진행·잠긴 장비의 실제 생산/설계·save compatibility 검증으로 확대하지 않는다.

KO07의 독립 검토는 기존82저장을 다시6GB 재해시한 별도 시험이 아니라 raw 수집기의 차이0·새 저장0 기록과99보관 사본을 확인한 것이다. R0는 같은 게임/RT56 manifest의 과거 영어 GER 실행이며 새 한국어/일본 대조와 구분한다. KOR와JAP 초기화·메뉴 복귀에 따른 기존 오류의 반복 수와 새 고유 오류를 분리한다. 새 오류 본문이 없다는 것은 기존 오류 전체가 해결됐다는 뜻이 아니다.

### EN03 검증 중단과 재인계 — 중단 이력 유지

EN03에서는 첫 신선한 화면에 환영 창이 보였다. 다음 클릭 호출은 `unknown screenshotId`를 반환해 그 동작의 결과를 확정하지 못했다. 이어 새로 읽은 화면은 소총 상세였고, `(482,283)` 톱니바퀴 위치 클릭 뒤 새 화면은 전차 상세였다. 예상한 화면 흐름과 달라 조작을 중단하고 사용자에게 현재 조작 여부를 물었다. 이 화면 변화 자체로 사용자 입력이나 충돌을 원인으로 판단하지 않는다. 장비17값·3guard·JAP 대조는 이 실행에서 검증하지 못했으며 보관한 캡처는 `runtime-session/en-03/screenshots/00-main-menu-version.png`뿐이다.

사용자는 `맡길게`로 검증·복구를 계속 인계했다. 그 뒤 첫 신선한 화면 요청은 foreground PID 접근에 실패했고, 창 목록에HOI4가 없었으며 프로세스 조회에서도 부재였다. 정상 UI 메뉴 종료는 담당자가 관측하지 않았다. 관측한 최신 crash 폴더는11월6일자였고 새 폴더는 찾지 못했지만, 이것만으로 충돌 여부나 종료 원인을 확정하지 않는다. EN03은 **INTERRUPTED·정상 UI 종료 미관측·이름 검증0**으로 유지하며 성공한 영어 시험이나 확인된 장비명 실패로 분류하지 않는다.

후속 수집은 `normal_ui_exit_observed=false`를 유지했다. raw 영수증3F217E…는99사본·기존82저장 차이0·새 저장0·새metadata0·정확한 외부37바이트 예외만 차이를 기록한다. `runtime-session/en-03/independent-interruption-log-review.json`은 실제 `(cf8c)`·36 DLC·RT56+호환판2모드와 보관3출력 핀을 확인했다. 로그669기록/631고유 본문·KO07/R0 대비 새 본문0이지만 정상 종료나 장비명 통과의 증거로 바꾸지 않는다. EN04는 별도 run·파일로 검증했으며 뒤의 성공으로 EN03을 재분류하지 않는다.

### EN04 새 영어 검증과 종료·복구

EN04 준비SHA는 `DEF7FCCC6814729E018894AAD5169A208EB5F11F09C128B939976C4CC20A34F2`다. `runtime-session/en04-continuation/`의 `session-active-v6-before.py`·`trial-active-v6-before.py`에 이전 helper를 보존하고, 별도 `session-candidate.py`·`trial-candidate.py`와 `activation-link.json`으로 EN04 계속 시험을 연결했다. `runs/en-04/reviewed-continuation-link.json`은 검토한 EN03 raw3F217E…와 유지한 승인 외부 descriptor5D5FAB…를 가리킨다. 기존82저장·원본 백업·source/descriptor·최종 복구 guard를 유지했으며 저장소 소스는 변경하지 않았다.

초기 KOR 시각 보고서 `en-04/independent-kor-visual-coverage.json` SHA `7590C2B1DF351A870AA320F185962F2AC8167C73BADB6203846E3A412F26F821`에 일본 대조PNG13을 추가한 별도 최종 시각 보고서2469AB…를 작성했다. 첫13PNG는 같다. 한국어KO07과 영어EN04 각각 **수정15/17문구·3guard·JAP 대표7표시**를 관측했으며 불일치0이다. EN04 캡처05의 일부 상세 제목이 가려져도 Enables 툴팁의 전체 장비명은 확인됐다. 생산 선택기는K-311 guard만 확인했고 연구·시간 진행·잠긴 수정 장비의 실제 생산·설계·저장은 시험하지 않았다. 1953년형2키는 두 언어 모두 소스 전용이다. 신선한 EN04만 영어 최종 증거로 사용하며 EN03·유실된EN2 PNG를 재사용하지 않았다.

정상 UI 메뉴 종료를 관측한 뒤 raw collection49ACFE…와 독립 `en-04/independent-final-log-review.json`을 별도로 작성했다. 실제 system.log는 `(cf8c)`·36 DLC·**RT56와호환판2모드**를 기록하며 RTK는 활성 모드가 아니었다. error.log671기록/631고유 본문은 KO07과 정확한 본문·빈도가 같고 장비 현지화 관련 검색0건·R0대비 새 본문0이다. EN04 소스 사본은 `runs/en-04/loaded-source/`에 저장소 상대 경로3파일로 보존했고 각 핀과 일치한다. KO07과 달리 이 폴더에는 별도 `manifest.json`이 없으므로 존재한다고 기록하지 않는다. 99수집 사본과14PNG의 크기/해시는 독립 검토에서 같았으며, 기존82저장 차이0·새 저장0은 raw 수집기의 결과다.

이후 `runs/en-04/descriptor-restoration.json`은 실제 외부 `.mod`를 원래304바이트·SHA `A486F1BD484486BE9BE4668E61C7B7B8DAC292C2E7474EC0258BF6F02C885BF4`·mtime `1794288120184596200`으로 복원했음을 기록한다. raw49ACFE…는 그대로 두고 `post-descriptor-restoration-state.json`의 별도 파생 상태1D08F8…를 검토한 뒤 기본 프로필을 복구했다. `runtime-session/restoration.json`은 `RESTORED_EXACT_METADATA_AND_EXISTING_SAVES_PRESERVED`, metadata차이0·기존저장차이0·프로세스 부재를 기록한다. 설정·언어/모드 선택·career profile 등6항목을 원상복구했으며 새 게임 원본 로그는 USER에 남기고 시험 전/후 사본은 외부에 유지했다.

### 임시 복구 뒤 별도 승인된 영구 RTK 동기화 — 완료

사용자는 임시 복구 완료 뒤 `영구 반영해줘`로 **외부 descriptor의 정확한37바이트 RTK 동기화**를 별도로 승인했다. `runtime-session/permanent-descriptor-sync/approval.json`의 SHA는 `FA74765332722E0A24CE5DA70FADEA5C04EF6A83C1AE9879E2CD7A570E75BAB8`다. 담당자는 `<TEST>/apply_permanent_equipment_dependency.py`로 원본·경로·기존 의존성·정확한 후보 바이트를 확인한 뒤 2026-11-10 21:19 KST에 적용했다. 이 스크립트는 외부 작업 helper이며 저장소 생성 입력이나 배포 파일이 아니다.

영수증 `runtime-session/permanent-descriptor-sync/receipt.json`은 **`PERMANENT_TESTED_RTK_DEPENDENCY_APPLIED`**다. 실제 대상은 `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV\mod\hearts_of_korea_Road_to_56.mod`이며, 변경 전304바이트A486F1…·원래mtime `1794288120184596200`의 사본을 같은 폴더의 `before.mod`에 보존했다. 변경 후는 **341바이트·SHA `5D5FAB7036D3512BA01EEA4E40C912735A7145A3B7D232E2A7741D1EA7612733`·mtime `1794313142351069400`**이다. 저장소397바이트를 통째로 복사한 것이 아니라 시험에 쓴 외부 descriptor와 정확히 같은37바이트 간선만 추가했다.

감사한65metadata 중 차이는 `mod/hearts_of_korea_Road_to_56.mod` 한 경로뿐이고 다른 metadata는 원래 상태다. 프로세스는 없었으며 게임 실행·저장 읽기/로드/쓰기 없이 적용했다. 저장82개의 보존은 앞선 실제 복구 영수증에 귀속한다. 영구 적용 뒤 새 cold run은 하지 않았으므로 별도 새 UI 통과를 주장하지 않는다. 적용 바이트는 이미 KO07·EN04에서 관측한 시험 후보와 동일하다. 임시304바이트 복구E0D4…와 그 뒤 영구341바이트 적용D0E130…는 둘 다 보존하며 앞선 사건을 취소하거나 덮어쓰지 않는다.

독립 원상복구 감사 `runtime-session/final-restoration-and-source-review.json` SHA `244D0A918755C45DC876451B274A6B14484E366A39F5F6AD41780F1B32034F03`는 영구 적용 전65metadata의 크기·SHA·mtime 차이0과 원래 외부304바이트를 확인했다. 이후 별도 `runtime-session/permanent-descriptor-sync/independent-final-review.json` SHA `96078366F12CAB19986CBD364F4F061FB54393BAC58B65D1A43DD1D3A0881B65`는 실제341바이트가 시험 후보·영수증과 같고37바이트 한 줄을 제거하면 원본이 정확히 복원됨을 확인했다. 나머지64metadata 차이0·원본 백업의 크기/해시/mtime·현재3출력/잠금/원장5핀 일치와 앞선 복구 증거의 보존도 확인했다. 이는 작은 파일의 독립 읽기 감사이며 새 게임 실행이나 저장82개의 추가6GB 재해시는 아니다.

언어 설정과 선택 배열은 승인한 임시 시험 후 원래대로 복구했다. 원래 언어는 영어, 원래 선택 배열은 `[호환판, RTK, RT56]`이며 최종 UI 실행은 영어 `[RT56, 호환판]`, 한국어 `[RT56, RTK, 호환판]`이었다. 별도 영구 적용은 외부 `.mod` 한 줄만 바꿨으며 원래 선택 배열을 새 검증 구성으로 재분류하지 않는다. 최종 `git diff --check`는 통과했고 기존 `review_followup.py` 줄 끝 변환 안내만 남았다. 커밋·푸시·업로드는 하지 않았다.

기존 외부 격리 시도는 `-userdir`와 복제 설치에서도 실제 사용자 설정·로그에 접근한 기록이 있고, 기존 V4 driver 역시 실제 USER를 사용하는 구조다. 이를 안전한 격리라고 가정해 재시도하지 않았다. 별도 승인 뒤 이번 전용 `<TEST>/runtime-session/`에 신선한 원본 백업과 실행별 증거·복구 기록을 둔다. 과거 driver나 archive를 덮지 않는다.

실행별 버전·체크섬·DLC·실제 모드·물리 포트·언어·관측 키·화면·로그는 해당 run에 귀속한다. 정상 이름 하나만 보고 전체 우선권을 통과 처리하지 않으며, 로그가 조용한 것과 실제 이름이 보이는 것은 별도다. 초기/최종 source와 기존 저장·프로필 보존을 확인하고, 종료·수집·복구 전 작업을 완료로 닫지 않는다.

이번 신선한 백업은 `<TEST>/runtime-session/before/`, 인덱스는 `runtime-session/baseline.json`이다. 181파일·기존 저장82개·6,203,941,587바이트를 크기·SHA-256·mtime으로 확인했다. `session.py`는 백업·승인된 언어/모드 준비·종료 후 수집·복구만 담당한다. 게임 조작은 computer-use 스킬의 실제 창 관측을 통해 수행하며 기존 저장을 로드하거나 덮어쓰지 않았다. helper의 source guard는 각 후보의 정확한 출력·잠금·원문에 결합한다. v5 당시의 각17키·3guard·원래286키·구경로4개 부재·정확한397바이트 저장소 descriptor 연결과 초기 독립33/0·연동4/0 영수증은 `v5-helper-activation-and-preflight.json`에 보존한다. v6 helper는1,308키 병합·17값 delta·1,291raw 보존과 같은 descriptor를 별도로 결합하며 준비나 활성화를 실제 UI 통과로 간주하지 않는다.

| 외부 helper 이력 (`<TEST>/runtime-session/` 아래) | 보존 역할 |
|---|---|
| `session-v1-before-zz-binding.py` | 첫 `HOK_` 파일명 v1 |
| `session-v2-before-root-ko-binding.py` | 언어별 `zz_` v2 |
| `session-v3-before-exact-path-ko-binding.py`, `session-v3-first-reader-crlf-refused.py` | 루트 한국어 v3와 최초 CRLF reader 거부. `v3-binding-first-prepare-refused.json` 및 정정 provenance도 보존 |
| `session-v4-before-ko04-array-hypothesis.py`, `session-v4-before-v5-minimal17-continuation.py` | v4 전체 병합, 배열 대조와 v5 전 원본 |
| `session-v5-continuation-candidate.py`, `session-v5-before-v6-full-ko-continuation.py` | 당시17키/descriptor v5에 결합한 helper와 v6 전 보존본. KO06 실패 결과와 분리하지 않음 |
| `session-v6-continuation-candidate.py`, 작업용 `session.py` | v6 전체 한국어 병합과 동일 descriptor에 결합하는 helper. 실제 실행 결과는 별도 run 영수증에 귀속 |
| `descriptor-dependency-trial/`의 `trial-v1-before-v5-continuation.py`, `trial-v5-continuation-candidate.py`, `trial-v5-before-v6-continuation.py`, `trial-v6-continuation-candidate.py`, 작업용 `trial.py` | 별도 승인한 외부 descriptor 대조 wrapper와 v5/v6 계속 시험. 원래 save/profile/source/복구 guard는 유지 |
| `en04-continuation/`의 `session-active-v6-before.py`, `trial-active-v6-before.py`, `session-candidate.py`, `trial-candidate.py`, `activation-link.json` | EN03 중단 수집을 유지한 별도 EN04 계속 시험. 출력 소스·기존 저장·원본 백업·최종 복구 guard는 그대로 |

외부 trial은 저장소 descriptor와 별개다. `descriptor-dependency-trial/original-compat.mod`는 launcher의 `path`를 포함한 **304바이트**, SHA `A486F1BD484486BE9BE4668E61C7B7B8DAC292C2E7474EC0258BF6F02C885BF4`이며, 승인 후보는 RTK 의존성 한 줄 **37바이트만 추가한341바이트**, SHA `5D5FAB7036D3512BA01EEA4E40C912735A7145A3B7D232E2A7741D1EA7612733`다. 이 정확한 원본/승인 후보만 예외로 등록했고 descriptor 일반 변경을 허용하지 않았다. EN04 종료·raw 수집 뒤 원래304바이트/mtime과 기본 프로필 복구를 각각 완료했다. 이후 별도 승인된 영구37바이트 적용도 실제D0E130… 영수증으로 완료했다. 현재 실제 외부 항목은341바이트5D5FAB…이며 다른 metadata는 원래 상태다. 임시 복구 기록을 영구 적용 이력과 합치거나 덮어쓰지 않는다.

| 실행 | 실제 구성·결과 | 외부 증거 위치 (`<TEST>/runtime-session/` 아래) |
|---|---|---|
| `en-01` | `l_english`, RT56+호환판, 36 DLC, `1.19.4.2.2da5 (cf8c)`. 첫 `HOK_` 파일명 실패. 정상 UI 종료 후 자연 종료·수집. 기존 저장82개 차이0·새 저장0 | `en-01/ui-observations.json`, `en-01/screenshots/`; `runs/en-01/{prepared,collection}.json`. collection SHA `98080B726771B3E2A1626AF743655D8CE9FB06DD768530D533655C008C3E8146` |
| `en-02` | 같은 영어 구성과36 DLC·버전/체크섬에서 `zz_`2개로 cold restart. KOR 연구 카드·상세·해금 이름 **수정15/17개와 보존3개 기대 문구 확인**, 관측 불일치0. 생산 선택기는 현재 해금된 K-311 보존 이름만 확인. 이어 새 JAP 게임의 대표 차량7개가 일본 이름으로 유지됨 | `en-02/independent-visual-coverage.json`; `runs/en-02/{prepared,collection}.json`. 당시 PNG00–13 중 현재 영어 원본은 `en-02/screenshots/07–13`만 유지되며00–06 소실은 아래 사고 기록 참조. collection SHA `D690F27FF741EC6A3E03159707C8B5754E3AB2D594801C1DCA321018405D8185` |
| `ko-01` | `l_korean`, RT56+RT56 Korean Translation+호환판, 36 DLC, 같은 `(cf8c)`. v2 한국어 **실패**: KLVT-2 전체·1949년형 전체/짧은 이름3문구가 일본식 이름. 연구·시간 진행·저장 없이 정상 UI 종료 후 자연 종료·수집. 기존 저장82개 차이0·새 저장0 | `ko-01/screenshots/`, `ko-01/misdirected-capture-recovery/`, `ko-01/loaded-source/`; `runs/ko-01/{prepared,collection}.json`. collection SHA `A367B87D75700D2B6DCE43AABFC157433A5FD5961613BA617E3F9FE328589483` |
| `ko-02` | 같은 한국어 구성·36 DLC·`(cf8c)`. v3 루트 폴더도 같은3문구 **실패**. 정상 UI 종료·수집, 저장82개 차이0·새 저장0 | `ko-02/screenshots/00–04`, `ko-02/independent-final-log-review.json`, `runs/ko-02/{prepared,collection}.json`. collection SHA `467F774300084296D562B2F610EF1E8FBA33E7702A964475000DD8E6180D744F` |
| `ko-03` | 같은 구성. v4 동일 경로 병합 후 차량 트리의 일본식6표시가 남아 **실패**. 정상 UI 종료·수집, 저장82개 차이0·새 저장0 | `ko-03/screenshots/00–01`, `ko-03/independent-final-log-review.json`, `runs/ko-03/{prepared,collection}.json`. collection SHA `7B19FA18403D09F24922E911F4F9862CF19343B35074C0188D98A3860966AE2C` |
| `ko-04` | v4·언어·DLC·같은 모드 집합을 고정하고 선택 배열만 반전. 같은 일본식6표시가 남아 **실패**. 정상 UI 종료·수집, 저장82개 차이0·새 저장0 | `ko-04/screenshots/00–01`, `ko-04/independent-final-log-review.json`, `runs/ko-04/{prepared,collection}.json`. collection SHA `C3B04C7025751BA621A3C0B8FE28179796EF891DA3FAB801986157210B555F43` |
| `ko-05` | v4·반전 배열·언어·DLC 고정, 외부 descriptor에 RTK 의존성37바이트만 추가. **관측9문구 정상·불일치0**. 정상 UI 종료·수집, 저장82개 차이0·새 저장0. 전체15/17·JAP UI 검증은 아님 | `ko-05/screenshots/00–04`, `ko-05/independent-final-log-and-visual-review.json`, `runs/ko-05/{prepared,collection}.json`. collection SHA `08A33042D3B7618D809E6A3723C85AE6813CB4A54E4290F7DC52C354F4B866AB` |
| `ko-06` | v5 좁은17키·RTK 의존성. **KLVT-2 전체 제목·해금 안내가4식 카츠로 실패**. 1949년형·전체15/17·JAP 대조는 미완료. 정상 UI 종료·99사본 수집, 저장82개 차이0·새 저장0. 로그669기록/631고유 본문은KO05와 동일 | `ko-06/independent-v5-failure-collection-review.json`, `runs/ko-06/{prepared,collection}.json`. collection SHA `9818BB0DBC6E52A6BE58305A853241111A8B2081F4BB39D6A7B9F8CF25BA9201` |
| `ko-07` | v6 한국어 전체 병합+정확한RTK 의존성. **수정15/17문구·3guard 불일치0·JAP 대표7표시 보존**. KLVT-2 전체/해금 및1949년형 전체/짧은 이름 정상. 생산 선택기는K-311 guard만 확인. 정상 종료 후99수집 사본·3출력 무결, 기존82저장 차이0·새 저장0. 로그671/631·KO06/R0 대비 새 본문0. 당시 미완료였던 최종 프로필 복구는 EN04 뒤 별도 완료 | `ko-07/final-visual-coverage.json`, `ko-07/independent-final-log-review.json`, `ko-07/screenshots/00–13`; collection SHA `DBEDA0241C63028B99A7B7C0FF096D5F12167F340D6F1C678EEC1ED94DA1D44E` |
| `en-03` | 같은 v6 소스·RTK 없는 영어RT56+호환판2모드로 cold launch했으나 **INTERRUPTED·이름 검증0·정상 UI 종료 미관측**. 재관측 시 창·프로세스 부재, 원인 미확정. normal flag=false로99사본/3출력 무결·기존82저장 차이0·새 저장0 수집. 후속EN04 성공으로 재분류하지 않음 | collection SHA `3F217EFA526768DB820A3DFDCD920E2E03C2601B7902D430CE2CDD1AD446D6AB`, `en-03/independent-interruption-log-review.json` SHA `325F235B8D7C10A39D926929D02FD1263226C520D7BA926C5D2720A1EBB678F9`; 보관 캡처00뿐 |
| `en-04` | 같은 동결v6·실제영어RT56+호환판2모드·RTK비활성. **수정15/17문구·3guard 불일치0·JAP 대표7표시 보존**. 생산K-311 guard만 확인,1953두키소스전용. 정상 UI 종료·프로세스 부재·99사본/3출력 무결·기존82저장 차이0·새 저장0. 로그671/631·KO07본문/빈도동일 | `en-04/final-visual-coverage.json` SHA2469AB…·`en-04/independent-final-log-review.json` SHA724579…; raw collection SHA `49ACFE4B02E0C107CEC6E766445F92E1C7FF91A94E91D18E06B1D0344E5A7CBB`. 이후 descriptor·프로필 복구는 별도 영수증으로 완료 |

EN2는 연구를 시작하거나 시간을 진행하지 않고 KOR와 JAP 모두 `12:00, 1 January 1936` 일시정지 상태에서 확인했다. 연구/생산 선택기를 여는 일시적 UI 상태는 저장하지 않았다. 화면은 기대 문자열을 직접 관측한 것이고, 정확한 lookup key는 소비 소스와 연결한 것이다. KLVT처럼 전체/짧은 문자열이 같으면 화면만으로 어느 키를 읽었는지 구분할 수 없다. 1953년형 `_x_2`의2키는 소스 검사만 통과했으며 해금이나 실제 UI를 새로 만들지 않았다. 미래 장비의 정상 연구 완료 후 생산·설계 이름, 기존 저장의 variant 자동 개명·재로드·장기 진행은 이 시험의 통과 항목이 아니다.

EN2 최종 로그 독립 검토는 `en-02/independent-final-log-review.json`이다. 수집99파일의 크기·SHA를 확인했고, system.log는 RT56와 호환판2모드·DLC36을 기록했다. error.log671기록/631고유 본문에서 이 장비 키·새 파일명·현지화 구문 관련 검색0건, 같은 RT56의 보존된 R0와 비교한 새로운 정확 오류 본문0종이다. JAP 초기화·메뉴 복귀로 일부 기존 오류의 반복 횟수는 달랐다. 로그 결과는 UI 성공·실제 연구 완료·전체 오류 해소를 대신하지 않는다.

## 남은 범위·Git·기존 산출물

한국어 `ko-01`의 같은 `zz_` 후보는 전체 통과하지 못했다. KHT-1/2·KAPC-1·K-511·로켓 트럭과 KLVT-1 상세는 HOK 이름이지만, KLVT-2의 짧은 표시는 맞아도 상세 제목·해금 안내는 `4식 카츠`였다. 1949년형 카드·상세도 `1식 호하 개`/`1식 장갑병차 호하 개`였다. 신규17키 중 이 세 기대 문자열이 남아 있어 `zz_`만으로 한국어 전체 해결을 주장하지 않는다. 보존 트럭 `기아 K-311 한돈반`은 포트와 donor 원문이 일치하며, 잘못 기록된 기대어 `닷지`로 변경하지 않는다. 별도 KOR 기술 별칭이나 하드코딩된 해당 설계명은 소스에서 찾지 못했다. 이후 루트 `replace/` v3, 동일 경로 병합 v4, 배열 반전도 실패했다. `ko-05`는 동일 v4 소스에서 정확한 외부 RTK 의존성 한 줄의 충분성을9문구로 확인했지만 좁은 v5는 `ko-06`에서 다시 실패했다. 현재 v6는 같은 전체 병합과 의존성을 함께 유지하며, 모든 모드 조합의 동작은 이 역사만으로 확정하지 않는다.

화면 저장 helper의 경로 캡처 실수로 EN2 PNG00–06의7개가 KO 화면으로 덮였다. 이 실수는 `<TEST>/runtime-session/evidence-incidents/en02-ko01-screenshot-overwrite.json`에 기록했고 현재 KO 바이트를 `ko-01/misdirected-capture-recovery/`에 별도 보존했다. EN2 PNG07–13의7개는 사전 검토 해시와 같지만, 사라진7개는 작업 폴더에서 복구하지 못했다. EN2의 당시 직접 관측·사전 독립 검토와 현재 보존 PNG를 구분하며, 현재00–06을 영어 화면 증거로 사용하지 않는다. 후속 화면은 명시적 run 경로에 직접 기록한다.

KO07·EN04에서 각각 수정15/17문구·3guard·JAP 대표7표시 관측과 종료·수집·독립 로그 검토를 완료했다. EN03은 이름 검증0·정상 UI 종료 미관측·원인 미확정으로 별도 보존한다. 임시 descriptor·기본 프로필 복구E0D4… 뒤 별도 승인된 영구37바이트 동기화D0E130…도 완료했다. 현재 사용자metadata 중 의도적 차이는 외부341바이트 `.mod` 하나뿐이며 새 게임을 추가 실행하지 않았다. v6 aggregate는28 PASS/0 WARNING/기존11 ERROR·exit1이고, 보호 source61파일 변경0·기준선/v4/v5와 같은11오류 본문이다. 기존 오류를 수선하거나 aggregate 전체를 성공 처리하지 않는다. RTK 없는 한국어는 지원·보존 확인 범위에서 제외한다. 최종 Workshop 의존성·번역 재배포 계약도 미확정이다. 1953년형2키는 한영 모두 소스 확인만 해당하며 잠긴 수정 장비의 실제 생산·설계·기존 저장 variant 자동 개명·장기 진행은 검증하지 않았다. 전차·공군·해군의 다른 표시 문제를 이번 차량17키 확인으로 해결됐다고 하지 않는다.

기존 저장소 `tools/__pycache__/` 21파일·1,088,888바이트는 정리 미결이며 이동·삭제하지 않는다. `.local-artifacts`는 없다. 이번 새 테스트·백업·프리뷰는 외부 `<TEST>`에만 둔다. 원본 HOK·RT56·번역·게임 설치·외부 source cache는 수정하지 않는다. 커밋·푸시·Workshop 업로드는 수행하지 않는다.
