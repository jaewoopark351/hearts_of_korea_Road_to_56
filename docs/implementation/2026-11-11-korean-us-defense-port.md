# 2026-11-11 한미 방위비·주둔 협상 선택 이식

상태: **18출력 구현 반영 / 독립119·생성8·통합35 정적 확인 통과 / 전체24 PASS·0 WARNING·기존16 ERROR / 이번 호환판 실행 미검증**. 이 계층을 수정·재생성·검증하기 전 [선택 입력 안내](../upstream/hok-us-defense-update-20261111/README.md), [잠금](../../tools/hok_us_defense_update_lock.json), [원본 사양 사본](../upstream/hok-us-defense-update-20261111/documents/docs/HOK_KOREAN_US_DEFENSE_COST_SHARING_SPEC.md)을 읽는다. 표시·지역 판단에는 [현지화 스킬](../skills/hok-rt56-localisation-review/SKILL.md), [주 참조 스킬](../skills/hok-rt56-state-reference-review/SKILL.md), [변경 영향 절차](../HOK_CHANGE_COVERAGE_REVIEW.md)를 적용한다. 그림 입력 재사용 전에는 [개발 자료 안내](../HOK_DEVELOPMENT_ARTIFACT_ARCHIVE.md)를 읽는다.

## 요청·기준과 범위

업데이트된 `C:\hoi\hearts_of_korea`에서 한국의 한미 방위비·미국 선택·주둔 후속 모듈만 현재 RT56 통합 위에 선택한다. 기존 핵분열 보너스와 지역 산업 업데이트는 이미 반영돼 있으므로 중복 적용하지 않는다. donor README의 일반 안내 문구는 제외한다. 게임/launcher 실행·사용자 설정 변경, 기존 자료 정리, Git commit/push·게시·업로드는 포함하지 않는다.

| 항목 | 이번 관측·입력 |
|---|---|
| 호환판 시작 | `feat/korean-focus-update-20260922@39e8e7e5bc3dbdcf52d8c8acc04a92c97cd0b2f5`, 작업 트리 깨끗함 |
| 원본 | 읽기 전용 `C:\hoi\hearts_of_korea`, HEAD `e2009b635d79c80a67fed0370d5fe36a823b656f` 위 미커밋 모듈. HEAD만으로 새 내용을 복원할 수 없음 |
| 영어 입력 | 읽기 전용 `C:\hoi\Hearts of Korea English Translation Anime Modder's Edition`, HEAD `11ec9e2096af906a086f5c076949f2da1a1c790d` 위 검토된 미추적 파일의 정확한 바이트를 동결 |
| 게임·host | 설치 `Operation Postern v1.19.4.2.2da5 (0bdb)`, Steam build26409260; RT56 manifest `1963361040482473746`. 기존 host 입력4,823경로의 크기·SHA 대조 missing0/changed0 |
| 현재 사용자 구성 | Windows11, `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV`; `한국test01`의 donor→일반판 영어 번역, `l_korean`, disabled DLC 없음. 현재 donor 로그 checksum `a3bb`·활성 DLC36은 포트 결과가 아님 |
| 외부 시험·진단 위치 | `C:\hoi\test\hok-rt56-us-defense-update-20261111-01\`; 아래 유지 source capsule·기존 활성 source cache와 역할을 구별 |

runtime 대상은 **18출력: 기존2개 병합·신규16개**다. `common/national_focus/korea.txt`와 `events/korea.txt`는 `THREE_WAY_MERGE`; 새 사건6개·국민정신4개·scripted effect5개·trigger1개, GFX2개·한영 현지화 각36키는 해당 신규 파일의 `ADD`; DDS8개는 원본과 정확한 `ASSET_COPY`다. 한국 노선의 USA 수신 사건·정신만 추가하며 일반 미국 트리·RT56 전역 시스템을 교체하지 않는다.

## 변경 영향 대장

| 기능·호출부·분기 | 처리·의도 | 확인 한계·남은 항목 |
|---|---|---|
| 조약 `KOR_rok_us_mutual_defense_treaty`→`kor_events.45`→한국 helper | **수정**: 미국 체결 때 한국 소비재 공장 계수 +5%, 미국 −5%; 중점 완료 자체는 지급하지 않음 | 기존 체결/거부 AI10/0과 한국 통보·상호 보장/통행권 경로 보존. 이번 실제 지급 미검증 |
| `KOR_usfk`→`HOK_KOR_us_defense.1` | **수정**: 완료 즉시 사단 대신 미국 응답 대기. 협정 수락은 기본 정신을 제거하고 한국 **최종 +35%**, 미국 **최종 −15%**로 교체 | 각각 +30/−10만큼의 변화이며 +5/+35 중첩이나 국가 전체 최종 소비재 비율·공장 이전을 뜻하지 않음. 미국 AI10/0/0 |
| 자치령·거절 | **의도적 유지한 원본 선택 사양**: 자치령은 기존 ±5% 유지·미국 dominion·사단3개·승인; 거절은 조약 유지·신규 사단/강화/세계 뉴스 없음 | 자치령은 합병이 아니며 한국 통보의 수락은 확인1개. 실제 선택·뉴스·자치령 상태는 미검증 |
| effect5개·국가 표식·사단 지급 helper | **수정**: 한국 scope를 명시하고 요청·결과·배치 일회 guard 사용. 사단3개 생성 뒤 state iterator 안에서 한국 지급 flag 기록 | 기존9보병·지원3·경험0.3·한국 소유 보존. 중복 호출·후보 없음·실제 생성 위치와 저장 지속성 미검증 |
| `prioritize = { 835 }`와 배치 fallback | **의도적 유지**: 현재 RT56 `835-Haraghe.txt`는 Hararghe이며 한국 지명이 아님. 적격 한국 소유·통제 주가 선택 범위이고835가 후보가 아니면 무작위 fallback | 지도/ID나 우선값을 임의 변경하지 않음. `KOR = { has_full_control_of_state = PREV }`로 USA 수신 사건의 ROOT 혼동 방지. 실제 후보 선택 미검증 |
| KATUSA·기존 소문자 통보 | **의도적 유지**: 새 요청은 승인 필요, 요청 표식 없는 legacy 경로는 기존 진입 허용. 포트의 `kor_events.46/47` 소문자 호출 유지 | donor의 대문자 호출을 재도입하지 않음. legacy 허용은 기존 저장 일반 호환 보장이 아니며 실제 수신·연구협력 미검증 |
| 응답 전 조건 무효·처음부터 USA 부재 | **수정**: 양국 존재·한국 독립·양국 내전 없음·상호 전쟁 없음·배치 후보를 재검사. 무효는 거부 helper로 resolved·배치 무산 통보, 승인/사단/강화/뉴스 없음. 최초 USA 부재도 같은 종료 경로 | helper가 기존 조약/정신을 직접 제거하지 않으며 정신 자체의 상대 소멸/전쟁 취소는 별도. 실제 지연 상황 미검증 |
| 한영36키·사진4·아이콘4·GFX2 | **수정**: 한국어와 동결된 실제 영국 영어를 연결, 기존 이름/조건을 덮지 않는 모듈 전용 표시·상대 texture 경로 | 영어 donor 채널의 한국어 본문 대신 번역 입력 사용. 활성 번역·폰트·각 선택/뉴스 UI 미검증 |
| 기존 핵분열·산업·지도·그 외 중점/사건·descriptor | **제외**: 이전 승인 통합과 source pins 유지 | 원본 전체 복사·공유 자산 교체·추가 보상 조정 없음 |
| USA가 사건 대기 중 소멸 | **미확인**: 초기 부재 종료와 선택 처리 때 재검사는 있으나 수신 국가가 사라져 선택 자체가 실행되지 않는 경우의 종료는 입증하지 못함 | 자동 재요청·정리 on_action을 새로 만들지 않음. pending 표식·KATUSA 차단·정신 취소·국가 재생성의 별도 관측 필요 |

## 출처·생성 소유권과 검증

[source-manifest](../upstream/hok-us-defense-update-20261111/source-manifest.json)는 원본18파일·donor Git 선조2개·이전 포트2개·문서4개/선택 PNG6개·번역1개·host/schema 입력의 역할·SHA·크기를 구별한다. manifest SHA `BF51203AA4E88EDF6E61C547D3FE46CD25C566BD1DE481CBC170AFA8C606F29C`는 새 잠금에 고정한다. 원본과 사본의 구체 경로는 선택 입력 안내를 따른다. 기존 cache나 capsule을 이동/덮어쓰지 않는다.

생성 소유권은 [새 생성기](../../tools/upstream_us_defense.py)에 뒀다. 검토된 donor 전후 delta를 기존 포트2개에 적용하고 신규16개를 고정 입력에서 생성했으며, 기존 핵분열 최종화 뒤 terminal hook으로 연결했다. `--apply`로18개를 기록했고 재검사는0 written으로 통과했다. 정확히 입증된 최종 바이트만 이전 포트로 역투영해 과거 계약을 검사하고 미등록 수정은 거부한다. 과거 잠금·해시를 현재 출력에 맞춰 바꾸거나 runtime 파일을 손으로 수정하지 않았다.

한국 생성기의 allowlist와 focus 소유 추가 경로에 신규16개를 연결하고, state-split CLI가 정확한 직전 출력에서 진행할 수 있게 했다. 전체/부분 원장에는 기존 fission 계층 뒤에 새 원장을 연결했다. 기존 전체 원장 경로는 수정 전부터 descriptor·소스 지문 등에서 차단돼 있어, 이번에는 같은 새 `ledger_bytes` 함수로 기존1,543행을 입력받아 두 행의 최종 해시·사유만 변경하고16행을 추가했다. 최종1,559행이며 기존 다른 행/셀·원시 바이트는 보존했다. 전체 생성기의 성공을 주장하지 않는다.

자산의 형식/해시·원본 선택은 [보관된 크레딧](../upstream/hok-us-defense-update-20261111/documents/docs/HOK_KOREAN_US_DEFENSE_ASSET_CREDITS.md)과 [자산 manifest](../upstream/hok-us-defense-update-20261111/documents/docs/data/HOK_KOREAN_US_DEFENSE_ASSET_MANIFEST.json)에 보존한다. AI 생성 가상 사진/아이콘과 HOK/Paradox 국기 참조의 권리를 구별하며 새 공개 라이선스를 주장하지 않는다. raw 국기 TGA/PNG는 donor·설치본의 읽기 전용 참조로 남기고 새 capsule에 복사하지 않는다. donor의 과거 화면/효과 기록을 호환판 결과로 합산하지 않는다.

| 증거 단계 | 필수 확인과 현재 상태 |
|---|---|
| 소스·정적 | 18출력·제한된2병합·이전 핀 보존,6사건/4정신/5effect/1trigger·scope/일회 guard, 한영36키/토큰/BOM·자산8개/GFX·충돌·원장·생성/역투영 확인. **독립119·생성8·통합35 통과; 전체24/0/기존16** |
| 로드·UI | 대상 RT56 구성의 실제 한영 조약/세 선택·통보·뉴스·아이콘·KATUSA 조건 확인. **이번 미실행** |
| 실제 효과·정상 진행 | 조약 수락/거절·세 주둔 선택·조건 무효·USA 부재·fallback·중복 지급·AI를 구별. 강제 진단과 정상 중점 진행은 별도. **이번 미실행** |
| 저장 | 요청/해결/승인/배치 flag·정신·사단·자치령과 pending의 새 저장 왕복. 변경 전 legacy 저장·국가 소멸/재생성·장기 AI/멀티플레이는 별도. **미검증** |

### 실제 정적 결과와 보존

아래 파일은 모두 위 외부 작업 경로에 있다. 소스/파일 확인을 엔진의 효과 실행으로 해석하지 않는다.

| 확인 | 결과·근거 |
|---|---|
| 수정 전 전체 검사 | `static-before.txt`, exit1: **23 PASS / 0 WARNING / 16 ERROR** |
| 독립 동작·표시·자산 소스 대조 | `preview-qa.json`, 적용 후 `runtime-qa.json`: 각각 **119 PASS / 0 FAIL**. 별도 ordered parser로474중점·보호 필드·3선택·가드·편제·상속835·36문구·DDS8/GFX 확인. runtime은 디스크 파일을 뜻함 |
| 새 생성기 경계 | `generator-preview-check.json`: **8 PASS / 0 FAIL**. 독립18 preview 바이트·이전/최종·신규16·미등록 수정/경로 이탈 거부 |
| 이전 계층 연결·보존 | `integration-qa.json`: **35 PASS / 0 FAIL**. 역사 역투영·최종화·Path/문자열 키·소유별 추가·원장 멱등성·해시/사유 외 보존. 실행파일1,478→1,494개, 기존2변경·신규16·삭제0 |
| 원본·host 재확인 | 위 통합 확인에서 donor18·문서/PNG10·영어 입력1·RT56 기록4,823개 지문 보존 |
| 최초 적용 후 전체 검사 | `static-after-first.txt`, exit1: **23 PASS / 0 WARNING / 17 ERROR**. 신규 영어 파일의 과거 파일 목록 연결 누락1건을 발견 |
| 영어 목록 연결 수선 | [source_snapshot.py](../../tools/source_snapshot.py)의 허용 목록에 새1파일만 추가하고 한영36키·토큰·정확한 바이트를 확인. 역사적37파일/2,747키 등 이전 계층 계약은 변경하지 않음. `--english-check` 통과 |
| 최종 전체 검사 | `static-after.txt`, exit1: **24 PASS / 0 WARNING / 같은 기존16 ERROR**. `aggregate-comparison.json`에서 수정 전과 오류 이름·마지막 진단 동일, 신규0 확인 |

최초 독립 preview에서 기존 사건 파일의 BOM 누락을 발견해 입력 예상값을 수정한 뒤 적용했다. 생성기는 처음부터 기존 BOM을 보존했고 `preview-events-first-without-bom.txt`는 잘못된 최초 예상값의 외부 기록이다. 독립 helper의 sibling `else` 해석 실패는 `qa-last-failure.json`에 보존했으며, 통합 helper의 단계별 입력·Windows 경로 표기 기대값도 바로잡은 뒤 최종 수치를 수집했다. 이런 helper 실패를 게임 결함이나 성공 검증으로 합산하지 않는다.

기존16오류는 descriptor 잠금 불일치와 연쇄 gate, 과거 map·건물·공유 override·교리·MIO·layout source pin 차이 및 원장의 `.gitignore` 충돌 분류 등을 포함한다. 이번 모듈 때문에 새로 생긴 오류로 취급하거나 과거 핀을 갱신해 숨기지 않았다. 실제 RT56 UI·효과·정상 진행·저장·AI·멀티플레이 검증은 남아 있어 완료 주장을 **구현 반영·범위 정적 확인**으로 한정한다.

별도 승인된 커밋 준비에서 새 trigger와 GFX2개의 원본 LF가 Git 속성의 CRLF와 다름을 발견해 해당3개만 `eol=lf`로 맞췄다. 실행 파일·소스 핀은 변경하지 않았다. Git 필터를 적용한 staged checkout18개의 SHA-256과 출력 잠금이 모두 일치했고, staged 출처 입력33개와 manifest도 고정 해시에 일치했다. 원본 보존 capsule과 donor-identical effect의 기존 혼합 들여쓰기는 원본 바이트로 보존했으며, 이 두 범주를 제외한 편집 파일의 staged 공백 검사를 통과했다.

기존 `tools/__pycache__/` 21파일·1,088,888바이트는 정리 미결로 보존한다. 새 helper·보고서·미리보기·백업은 외부 작업 경로만 사용한다. donor·Workshop·설치본·사용자 데이터는 변경하지 않으며 commit·push·게시·업로드는 수행하지 않는다.
