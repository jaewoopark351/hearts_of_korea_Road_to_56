# 한국 장비명 한영 수선의 선택 입력

이 폴더는 유지할 생성 입력·출처 사본이다. 시험 helper·프리뷰·검사 보고서나 게임 출력의 보관소가 아니다. 이 입력의 수정·재사용·재생성 전에 [구현 기록](../../implementation/2026-11-10-korean-equipment-localisation-repair.md), [범위 계획](../../plans/2026-11-10-korean-equipment-localisation-repair-plan.md), [현지화 검토 스킬](../../skills/hok-rt56-localisation-review/SKILL.md)을 읽는다.

이 문서의 `<TEST>`는 외부 작업 경로 `C:\hoi\test\hok-rt56-equipment-localisation-20261110-01\`을 뜻한다.

현재는 **선택 범위 v6 구현·한영UI/수집·임시변경 복구와 별도 승인된 영구 외부RTK37바이트 동기화 완료** 상태다. 자체 QA39/0·독립 QA35/0, aggregate28 PASS/0 WARNING/기존11 ERROR(exit1)이며 출력은 영어17키 `ADD`·한국어1,308키 `THREE_WAY_MERGE`·저장소 descriptor `OVERRIDE`다. KO07·EN04 각각 수정15/17문구·3guard·JAP 대표7표시를 관측했다. EN03은 이름 검증0·정상 UI 종료 미관측·원인 미확정으로 유지한다. 원래304바이트 복구 뒤 영구 적용한 현재 외부 `.mod`는341바이트5D5FAB…이고 그 외 metadata는 원래 상태다. 아래10개 동결 입력과 manifest는 v1부터 변경하지 않았다.

| 위치 | 역할 |
|---|---|
| `C:\hoi\hearts_of_korea_Road_to_56` | 실제 호환판 작업 소스. 선택 기준 `2523bf455514c79a3538f0475dc922329afb185d`와 기존 문서 변경을 보존 |
| `compat_before/` | 기존 한국어·영어 장비 현지화 2개. 기존 HOK 명칭13키와 유지3키의 정확한 입력이며 실제 두 파일은 수정하지 않음 |
| `donor/` | 읽기 전용 HOK donor 한국어 장비 파일1개. 현재 포트 한국어와 동일한 원문·기여의 근거 |
| `host/rt56/` | RT56 영어 장비명·기술·기계화 장비 정의와 descriptor4개. 상충 명칭과 1949/1953년 후속 계통의 읽기 전용 비교 사본 |
| `host/translation/` | RT56 한국어 번역의 장비명과 descriptor2개. 상충 명칭과 로드 선언의 읽기 전용 비교 사본 |
| `ledger_before.csv` | 1,541행의 이전 통합 원장 원문. 이 입력 자체는 변경하지 않음. v5 이후 별도 출력에서 descriptor 행의 두 셀만 투영하고 현지화2행을 추가 |
| [source-manifest.json](source-manifest.json) | 위10개 입력의 원본/사본·provider·경로·크기·SHA-256과 선택한 HOK/포트 commit 역할 |
| [잠금](../../../tools/hok_equipment_localisation_lock.json) | manifest·실제 host 지문·설치/latest manifest·기존 언어별 원문·새 이름4개·최종3출력 해시·과거 revision·descriptor Git 객체 입력과 원장 투영/이전 해시 |
| `C:\hoi\test\hok-rt56-equipment-localisation-20261110-01\` | 실제 이번 baseline·프리뷰·백업·시험 helper·검사 결과의 외부 위치. 생성 입력이나 배포 파일로 참조하지 않음 |

[생성기](../../../tools/korean_equipment_localisation.py)는 13개 원래 HOK 키와 4개 호환판 작성 이름을 사용해 언어당17값을 재정의한다. 새 네 이름은 기존 KAPC-1의 후속으로 RT56 장비 정의의 1949/1953년만 붙인 표시명이다. 실제 역사 기종이나 원본 donor 작성값이라고 주장하지 않는다. `_x_2` 두 키는 한영 모두 소스 확인만 했으며 새 연구·해금·성능이나 실제 UI 접근을 추가하지 않는다. 유지3키와 각286키인 기존 한영 파일은 바이트 그대로다.

현재 생성기가 소유하는 출력은 다음3개다. 현지화는 BOM·언어별 헤더와 같은 기여 메모를 가지며, 영어17키·CRLF는 v2와 같고 한국어1,308키·LF/EOF는 v4와 같다. v5에서 잠시 대체했던 전체 한국어 병합을 v6에서 정확한 바이트로 복원했다. 원문17 KOR값만 변경하며 비한국1,291키·기존 주석·나머지 raw 바이트는 RTK 원문과 같다.

| 현재 경로 | 분류·크기·SHA-256 |
|---|---|
| `localisation/english/replace/zz_HOK_KOR_equipment_overrides_l_english.yml` | `ADD`, 1,072바이트, `F1C4044B30BBE48D1702AF4D4757963601C6427AC1CE10FF6D4ACFFE17EAF967` |
| `localisation/korean/replace/r56e_equip_motor_mech_l_korean.yml` | `THREE_WAY_MERGE`, 82,181바이트, `DF40639AF64C8C307CD6CEBE5327CBFE2228B0B4C79B82D33F83C96450376F8A` |
| `descriptor.mod` | `OVERRIDE`, 397바이트·LF, `A3A75B5F463DE4548062E152F464E403F4B14D3371A2CE233F1B7D2E3C203386` |

descriptor의 별도 불변 입력은 이 저장소 commit `2523bf455514c79a3538f0475dc922329afb185d`의 Git blob `4c1fd9af7d752bef207285980fe9854a4f4086bd`다. 263바이트·raw LF·SHA `AA150D6CE82A7779C3D4C3FCDC962A82FA269327F005330B565723CA87BBE247`를 잠금의 `descriptor_input`에 고정했으며 원래10개 입력을 다시 쓰거나 manifest에 소급 추가하지 않았다. 기존 RT56·Korean Language 의존성과 나머지 필드를 보존하고 `The Road to 56 Korean Translation` 및 필수 기여 메모만 추가한다. `review_followup`의 과거 검사 연결은 정확한 새 descriptor를 정확한 옛 입력으로 역투영하며 임의 descriptor 변경을 허용하지 않는다.

처음의 `HOK_KOR_…` 파일명은 영어 `en-01` 연구창에서 일본식 이름을 이기지 못했다. 같은17키·바이트의 `zz_` v2는 영어 `en-02`에서15/17수정 문자열과3guard를 관측했지만, 한국어 `ko-01`의 KLVT-2 전체 이름과1949년형 전체/짧은 이름은 실패했다. 루트 `replace/` v3도 `ko-02`에서 같은3문구에 실패했다. v4는 실제 RTK와 같은 경로에1,308키를 병합해17값만 바꾸고1,291비대상 키·나머지 바이트를 보존했으나 `ko-03`에서 실패했고 선택 배열만 뒤집은 `ko-04`도 실패했다. 이 전체 병합은 **v5에서 좁은17키로 대체했다가 KO06 실패 뒤 v6에서 복원**했다.

외부 descriptor에 RTK 의존성37바이트 한 줄만 추가하고 v4를 유지한 `ko-05`는 한국어9문구 정상·불일치0을 확인했다. 이는 그 대조의 충분성을 보여주며 엔진 정렬의 일반 법칙을 증명하지 않는다. 이 근거로 v5는 두 언어 모두 좁은17키로 복귀하고 저장소 의존성을 명시했지만 `ko-06`에서 KLVT-2 전체 제목·해금 안내가4식 카츠로 다시 실패했다. KO06의1949년형·전체15/17·JAP는 미완료이며 이를 실패나 성공으로 추정하지 않는다. 그 뒤 v6는 같은 전체 한국어 병합과 정확한 의존성을 함께 유지한다. 파일명·폴더만으로 모든 모드 조합의 우선권을 보장하지 않는다. EN2 화면7개가 KO 화면으로 덮인 사건과 남아 있는7개 원본 PNG의 구분도 구현 기록에 남긴다. 과거 관측이나 `ko-05`의9문구 통과는 최종 v6 UI 증거가 아니다.

잠금의 `revision_history`와 `superseded_outputs`는 v1–v5의 경로·해시를 보존한다. 현재 폐기 대상은 접두사 없는 구한영2개·v3 루트 한국어·좁은 v5 한국어의 정확한 자체 구경로4개뿐이며 해시·크기가 다르거나 별도 편집이 있으면 거부한다. 네 경로는 모두 부재이고 현재 전체 병합 경로는 활성 출력이다. 과거 버전별 모듈·잠금·출력·원장과 helper v1–v6는 외부 시험 경로에 보존하며 세부 매핑은 구현 기록을 따른다.

- `localisation/english/replace/HOK_KOR_equipment_overrides_l_english.yml`
- `localisation/korean/replace/HOK_KOR_equipment_overrides_l_korean.yml`
- `localisation/replace/zz_HOK_KOR_equipment_overrides_l_korean.yml`
- `localisation/korean/replace/zz_HOK_KOR_equipment_overrides_l_korean.yml` — 정확한1,057바이트·0BF14E…만 폐기 허용

동결 원장 SHA `B570CDFF9F5375151230FBCEA7AFD73B64AD835959DB1A6FB5DB440034B2CD39`는 변경하지 않았다. v5부터 descriptor 행(CSV 물리69행)의 `output_sha256`·추가 `reason`만 투영하며 **다른1,540개 raw 행과 descriptor의 다른 필드**는 보존한다. 현재 v6의1,543행·942,562바이트 원장 SHA는 `78FDB9007133CA6E9E29A2AC1CDF7E3AA887F0D743C4875A344D3BCC613F531D`다. v5 원장8B5C…에서 한국어 마지막 행만 `THREE_WAY_MERGE`/`GENERATED`로 바꿨고 투영1,541행 base49A3…와 영어 `ADD` 행은 같다. 현재 원장이 옛1,541행 전체 prefix와 같다고 하지는 않는다. 정확한 동결/투영 base와 등록한 v1–v5 전체 원장 해시에서만 전환하며 다른 행·필드·임의 tail은 거부한다. 기존 원본과의13키 중복도 두 정확한 경로·실제 원문/출력 바이트·동일 값을 확인한 정적 예외뿐이다. 폐기된 루트 한국어 경로의 v3 locale 예외는 제거했다.

선택해 검증한 UI 구성은 한국어 **RT56+RT56 Korean Translation+호환판**, 영어 **RT56+호환판**이다. RTK 없는 한국어에는1,291개 번역을 새로 공급할 수 있어 그 구성의 보존·지원 확인은 제외한다. EN04의 실제 system.log에서 RTK 없는 영어2모드를 확인했지만 이를 최종 Workshop 의존성 계약의 확정과 구분한다. 기존 runtime1,476파일 중 descriptor1개만 변경하고1,475개는 그대로이며 현지화2개를 추가했다. gameplay·기존 장비 원문은 편집하지 않았으며 선택한 RTK 구성의 비대상1,291문구·raw 바이트는 RTK 원문 그대로 복사한다. 그 복사가 없었다는 설명은 v5 당시만 해당한다. RTK 비현지화 충돌의 소스 검토와 실제 GUI 확인 한계도 구현 기록에 남긴다.

실제 launcher의 외부 `.mod` 수정은 사용자가 별도 승인한 임시 대조였다. 원본304바이트와 정확히37바이트 추가한341바이트 후보만 예외로 허용했다. 이는397바이트 저장소 출력과 다른 파일이며 EN04 종료·수집 뒤 원본304바이트/mtime과 기본 프로필 복구를 각각 완료했다. 이후 사용자의 별도 `영구 반영해줘` 승인으로 같은37바이트 영구 적용을 완료했다. 임시 복구와 뒤의 영구 적용은 별개 사건으로 보존한다. v5 독립 QA는 최초33/0에서 aggregate 비교3개를 추가한36/0이며 두 시점의 해시를 구현 기록에 따로 남겼다. v5 aggregate28 PASS/0 WARNING/기존11 ERROR의 본문은 기준선·v4와 같았고 KO06의99사본·기존82저장 차이0·새 저장0·로그669/631은 별도 수집 기록이다. collection SHA는 `9818BB0DBC6E52A6BE58305A853241111A8B2081F4BB39D6A7B9F8CF25BA9201`이며 로그 본문·빈도는KO05와 같았다. 이 정적 결과·조용한 로그가 KO06 UI 실패를 덮지 않는다.

v6 자체 QA39/0은 외부 `v6-host-merge-dependency/candidate-apply-report.json`, 독립35/0은 `qa/independent-runtime-qa-v6-host-merge-dependency.json`에 있다. 완료 aggregate 원문 `static-after-v6-host-merge-dependency.txt`의 SHA는 `BA94BEC172CFB7CAAF307401E90E58A03E1A71F70F66AA764FCB81D8A8AD94B4`다. 별도 `aggregate-comparison-v6-host-merge-dependency.json`에서 보호 source61파일 변경0과 기준선·v4·v5 대비 같은11오류 본문을 확인했다. traceback 도구 경로·행번호만 정규화했으며 원래35/0 QA 보고서는 그대로다. aggregate의28 PASS/0 WARNING/기존11 ERROR·exit1을 전체 성공으로 표현하지 않는다.

KO07의 새 캡처00–13·14PNG와 `runtime-session/ko-07/final-visual-coverage.json`은 수정15/17문구·3guard 기대 문자열과 불일치0·JAP 대표7표시 보존을 확인했다. 최종 시각 보고서 SHA는 `EC37495AE6C024A74D7F4BC1D0DB5D72DF072A44F3378FB97F718D39530AA912`이며 초기00–12 한국어 보고서와PNG도 보존했다. KLVT-2 전체 제목·해금 안내와1949년형 전체/짧은 이름은 정상이며 생산 선택기12는 현재 해금된K-311 guard만 확인했다. 1953년형2키는 계속 소스 전용이고 잠긴 수정 장비의 실제 생산·연구 완료·save compatibility 증거가 아니다.

KO07 collection SHA `DBEDA0241C63028B99A7B7C0FF096D5F12167F340D6F1C678EEC1ED94DA1D44E`는 정상 종료 후99사본·보관3출력 무결·기존82저장 차이0·새 저장0을 기록한다. 독립 `runtime-session/ko-07/independent-final-log-review.json`의 SHA는 `8C5D69140203415E57FAE04FF46500582A155E254C2E481B8A24EAB133D9F20C`다. 실제 `(cf8c)`·36 DLC·RT56/RTK/호환판3모드를 확인했으며 error.log671기록/631고유 본문에서 KO06·과거 R0 대비 새 정확 본문0·장비 현지화 관련 검색0건이었다. KO06 대비 기존 random.log rename 오류의 반복만2회 증가(2→4)했으며 고유 새 오류와 구분한다. 수집 당시에는 승인된37바이트 의존성 예외가 남았고 뒤의 EN04 종료 후 별도로 복구했다.

EN03 준비 영수증 SHA `FB7A5F1E3059157C93AB713997DE2C8A23038355C2F0078186D99F1614515A41`는 `l_english`·선택 `[RT56,호환판]`과 같은3출력 핀을 기록한다. cold launch 뒤 환영 창을 관측했지만 다음 클릭의 `unknown screenshotId`로 결과를 확정하지 못했고, 새 소총 상세·톱니바퀴 클릭 뒤 전차 상세의 예상 밖 흐름에서 조작을 멈췄다. 사용자가 `맡길게`로 검증·복구를 다시 인계한 뒤 확인한 시점에는 창·프로세스가 없었다. 최신 crash 폴더는11월6일자였고 새 폴더는 찾지 못했지만 사용자 조작·충돌·종료 원인을 단정하지 않는다. 보관 캡처는00뿐이며 **INTERRUPTED·이름 검증0·정상 UI 종료 미관측**으로 기록한다.

EN03은 `normal_ui_exit_observed=false`로 수집했다. raw collection SHA `3F217EFA526768DB820A3DFDCD920E2E03C2601B7902D430CE2CDD1AD446D6AB`, 독립 중단/로그 검토SHA `325F235B8D7C10A39D926929D02FD1263226C520D7BA926C5D2720A1EBB678F9`는99사본·3출력 핀·기존82저장 차이0·새 저장0과669/631로그를 기록한다. 후속 EN04의 성공은 EN03 이름 검증0·정상 종료 미관측을 바꾸지 않는다. 별도 `runtime-session/en04-continuation/`에 이전 helper 사본·새 후보·activation-link를 보존해 같은 동결 v6 소스에서 EN04를 진행했다.

EN04 최종 `runtime-session/en-04/final-visual-coverage.json` SHA `2469AB543B22687ED96013FCCA56824C4C8FCED720388E633D71DE0657060104`는 새14PNG에서 수정15/17문구·3guard 불일치0·JAP 대표7표시 보존을 확인한다. 초기13PNG 보고서7590C2…도 유지했다. 생산 선택기는K-311 guard만 확인했고1953두키는 양 언어 소스 전용이다. raw collection SHA `49ACFE4B02E0C107CEC6E766445F92E1C7FF91A94E91D18E06B1D0344E5A7CBB`는 정상UI종료·프로세스 부재·99사본·3출력 무결·기존82저장 차이0·새 저장0을 기록한다. 독립 최종 로그 검토SHA `7245798E330B2A5384D84D8FDC3CF90F297C6DE850963434AD19491A04F7E242`에서 실제 `(cf8c)`·36 DLC·RT56+호환판2모드·RTK비활성,671/631로그·KO07본문/빈도동일·R0대비 새 본문0을 확인했다. EN04 사본은 `runs/en-04/loaded-source/` 아래 저장소 상대3경로이며 별도manifest는 없다.

외부 descriptor 복구 `runs/en-04/descriptor-restoration.json` SHA `A41B38D75E8E3335F572B663985CDC7EB5A42F55AAE6E0B3F3671CAFAA59266B`는 원래304바이트·A486F1…·mtime을 복원했다. raw49ACFE…를 변경하지 않고 파생상태1D08F8…를 만든 뒤 `runtime-session/restoration.json` SHA `E0D4D449BE6AB3DF2EC951658BAF79B869BAA548EA5F152CD7395AAFECAED342`에서6metadata·기존저장 차이0·프로세스 부재를 확인했다. 원본 로그는 USER에 남기고 시험 전/후 사본은 외부에 보존한다.

**현재 실제 launcher 항목의 영구37바이트 RTK 동기화도 완료했다.** 외부 helper `<TEST>/apply_permanent_equipment_dependency.py`와 `runtime-session/permanent-descriptor-sync/approval.json` SHA `FA74765332722E0A24CE5DA70FADEA5C04EF6A83C1AE9879E2CD7A570E75BAB8`, `receipt.json` SHA `D0E130B0ADF78816A9C53C602316DB268D3B8D4E90213827E66C9569BFDAC648`가 별도 승인·범위 적용을 기록한다. 2026-11-10 21:19 KST에 원래304바이트A486F1…·mtime을 `runtime-session/permanent-descriptor-sync/before.mod`로 보존한 뒤, 실제 USER의 `mod/hearts_of_korea_Road_to_56.mod`를 시험과 같은 **341바이트·SHA `5D5FAB7036D3512BA01EEA4E40C912735A7145A3B7D232E2A7741D1EA7612733`·mtime `1794313142351069400`**으로 바꿨다. 저장소397바이트를 통째로 외부에 복사하지 않았다.

감사한65metadata 중 이 `.mod` 한 경로만 의도적으로 달라졌고 다른metadata는 원래 상태다. 프로세스 부재·저장 쓰기0이며 적용 후 새 게임을 실행하지 않았다. UI 근거는 동일 후보 바이트의 KO07·EN04에 한정한다. 원래304바이트로 돌아간 임시 복구E0D4…와 뒤의 영구341바이트 적용D0E130…는 모두 유지한다. 최종 Workshop 의존성·전체 번역 재배포 계약은 여전히 미확정이다. 범위 UI·복구·영구 적용 완료를 모든 장비/저장/gameplay 검증 완료로 확대하지 않는다. v6 코드·출력·잠금·원장은 계속 동결한다.

최종 독립 감사는 외부 `runtime-session/permanent-descriptor-sync/independent-final-review.json` SHA `96078366F12CAB19986CBD364F4F061FB54393BAC58B65D1A43DD1D3A0881B65`다. 실제341바이트·정확한37바이트 역투영·나머지64metadata 보존과 현재3출력/잠금/원장5핀을 확인했다. 영구 적용 전 원본304바이트·65metadata 원상복구 감사244D0A…는 별도로 보존했다. 원래 언어·선택 배열 복구와 시험 구성의 차이, 저장 보존 증거의 범위는 구현 기록을 따른다.

기존 HOK·영어 번역·RT56·RT56 한국어 번역의 저작과 기여를 유지한다. 이 capsule은 개발 출처이며 신규 이름 작성과 기존 명칭 재사용을 구분한다. release staging에 이 폴더 전체를 넣지 않는다. 공개 고지·재배포 조건 검토를 대체하는 포괄 허가가 아니다. 외부 source cache와 과거 입력/잠금은 변경하지 않는다.
