# 2026-11-11 핵분열 실험 연구 보너스 선택 이식

상태: **보상 두 줄 구현 반영·범위 정적25 PASS / 전체23 PASS·0 WARNING·기존16 ERROR / 실제 실행 검증 대기**. 이 계층을 수정·재생성·검증하기 전 [선택 입력 안내](../upstream/hok-fission-update-20261111/README.md), [새 잠금](../../tools/hok_fission_update_lock.json), [기존 산업 계층 기록](2026-11-10-korean-industry-update-port.md)을 읽는다. 표시 경로 판단에는 [현지화 검토 스킬](../skills/hok-rt56-localisation-review/SKILL.md)과 [변경 영향 절차](../HOK_CHANGE_COVERAGE_REVIEW.md)를 적용한다.

## 범위와 기준

업데이트된 HOK 원본을 호환판에 반영하라는 요청에 따라, 이미 이식된 지역 산업 업데이트 위에 핵분열 실험 보상 두 줄만 선택한다. 원본 전체 복사·지도·자산·의존성 변경, 게임 실행·사용자 설정 변경, Git commit/push·업로드는 수행 범위가 아니다.

| 항목 | 이번 관측·출처 |
|---|---|
| 호환판 시작 | `feat/korean-focus-update-20260922@6931151ff3009127bf35564cd39eb9b2df88f508`, 작업 트리 깨끗함 |
| 읽기 전용 donor | `C:\hoi\hearts_of_korea`, HEAD `1c2e5423c08677228fa89c0181535bc30fc5764d`; 해당 지역 산업 커밋 내용은 이미 11월10일에 이식됨. 새 미커밋 차이는 중점1파일과 문서2파일 |
| 설치 게임 | `Operation Postern v1.19.4.2.2da5 (0bdb)`, Steam build `26409260`; 새 호환판 실행 결과가 아님 |
| RT56 | live manifest `1963361040482473746`, 현재 host/industry 잠금과 일치. 관련 파일 SHA-256은 새 잠금에 고정 |
| 현재 사용자 구성 | Windows 11; `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV`; `한국test01`에서 donor → 일반판 영어 번역, `l_korean`, `disabled_dlcs=[]` |
| 기존 로그 | 11월11일 donor 실행은 checksum `2787`, 활성 DLC36개. RT56·호환판 시험이나 새 보상의 지급·소모 증거로 사용하지 않음 |
| 새 시험·진단 위치 | `C:\hoi\test\hok-rt56-fission-update-20261111-01\`; source capsule과 기존 활성 source cache는 시험 출력과 구별 |

## 변경 영향 대장

| 기능·사용처 | 처리·기대 의미 | 소스 근거·확인 한계 |
|---|---|---|
| `HOK_KOR_fission_chain_reaction_experiments`의 `add_tech_bonus` | **수정 적용**: 기여 주석과 `bonus = 1.5` 두 줄 추가, 핵 기술 연구 보너스150% | 원본 전후 SHA와 정확한 추가 문자열을 새 잠금에 고정. 기존 `THREE_WAY_MERGE` 분류 유지. 생성기 적용·정확한 바이트 대조 통과 |
| 같은 블록의 `name`, `ahead_reduction = 2`, `uses = 1`, `category = nuclear`·핵 혁신 `1.00` | **의도적 유지**: 선행 연구 불이익2년 감소와 연구 보너스를 같은1회 혜택으로 제공 | 2년은 혜택 유효기간이 아님. 자동 핵 기술 지급·영구 연구속도·사용 횟수 추가가 아님 |
| 474개 중점 ID·선행·기간·조건·배치·AI·둘째 민간 원자로·기존 연구망/무궁화 경로 | **의도적 유지**: 첫 중점의 해당 보상 외 기존 내용 보존 | 적용 뒤 두 줄 외 전체 바이트·ID/선언 순서 보존과 이전 생성기의 최종화·역투영 확인. 과거 donor 실행은 새 보상 검증이 아님 |
| 한영 보상 이름·엔진 `EFFECT_ADD_TECH_BONUS` 표시 | **의도적 유지**: 기존 이름 키와 상속된 수치 효과 안내 사용, 현지화 파일 추가/수정 없음 | 현행 vanilla의 핵 연구 보너스·선행 감소 병용 예와 양 locale 효과 문구, RT56 대응 예를 새 잠금에 고정. 실제 한영 UI는 미확인 |
| 주/프로빈스·그림·공유 자산·이미 이식된 지역 산업 업데이트 | **제외**: 새 원본 차이에 해당하지 않음 | 기존 ID 이관·산업 보상·결정·문구·관련 잠금과 capsule 보존 |
| 새 UI·정상 완료·연구 혜택 소모·AI·저장 | **미확인** | 이미 완료한 중점의 소급 지급·기존 보너스 변환 코드를 추가하지 않음. 실제 적용/소모, 새 저장 왕복과 이전 저장 호환은 별도 검증 필요 |

## 재현·출처와 검증 기록

[기존 생성기](../../tools/upstream_industry_update.py)를 확장해 통합했다. 기존 산업 잠금·입력·역사적 `build_outputs`는 보존하고, 새 잠금과 `current_outputs`로 최종 바이트를 구별한다. 정확히 입증된 최종 출력만 산업 출력으로 역투영한 뒤 기존 역사 검사를 이어가며 미등록 수정은 허용하지 않는다. `--apply`로 실행 파일1개를 기록했고 이후 `--check`는 0 written으로 통과했다. runtime 파일을 손으로 고치거나 현재 출력을 기대값으로 삼지 않았다.

전체/부분 원장 생성 경로에서는 기존 장비 원장의 정확한 이전 바이트 검사를 끝낸 다음 `fission_ledger_bytes`를 적용한다. 현재 전체/부분 경로는 수정 전부터 존재한 descriptor 불일치에서 차단되므로 이번에는 같은 함수로 기존 원장의 대상1행만 갱신했다. 원장1,543행 중 이 행의 최종 해시·추가 사유 외 셀과 다른 행의 원시 바이트는 그대로다. 전체 원장 재생성 성공을 주장하지 않는다.

원본 runtime 입력은 donor HEAD의 불변 Git blob `af90f80d2228961e869eca7615aed6bce579d80c`을 CRLF checkout 바이트로 복원하고 잠금의 두 줄을 정확한 위치에 추가해 재현한다. donor runtime 전체 사본은 새 capsule에 만들지 않는다. 문서2개는 읽기 전용 원본에서 복사한 출처 증거이며, 그 문서의 과거 실행 수치를 이번 포트 검증으로 합산하지 않는다. 입력·출력 해시와 host/schema 공급자는 새 잠금이 관리한다.

| 수행한 확인 | 실제 결과·외부 증거 |
|---|---|
| 수정 전 전체 검사 | `static-before.txt`: **23 PASS / 0 WARNING / 16 ERROR**. 과거11오류 기록을 현재 결과로 재사용하지 않음 |
| 독립 범위 확인 | `scoped-verification.json`: **25 PASS / 0 FAIL**. 정확한 두 줄·474 ID/순서·재생성/역투영/멱등성·미등록 수정 거부·원장 한 행 보존 확인 |
| 파일·호스트 보존 | 감사한 실행파일1,478개 중 한국 중점1개만 변경. 현지화·지도·descriptor 보존. RT56 기록 입력4,823개 차이0, live donor 해시 일치 |
| 적용 후 전체 검사 | `static-after.txt`: **23 PASS / 0 WARNING / 같은16 ERROR**. `aggregate-comparison.json`에서 오류 이름·마지막 진단 동일 및 신규0 확인 |
| diff·기존 시험 자료 | `git diff --check` 통과. 기존 pycache21개·1,088,888바이트 유지, `.local-artifacts` 없음 |

기존16오류는 descriptor 잠금 불일치 및 연쇄 gate, 과거 host/vanilla map·MIO·doctrine·layout source pin 불일치와 원장 `.gitignore` 충돌 분류 등을 포함한다. 이번 원본 보상 변경의 원인으로 취급하거나 과거 핀을 갱신해 숨기지 않았다. 최초 원장 생성에서 CSV 헤더 중복을 발견해 `DictReader.fieldnames`를 먼저 읽도록 수정하고 보존한 원장 기준선에서 다시 생성했다. 최초 사본은 `ledger-first-generated.csv`, 수정 전 원본은 `ledger.before.csv`로 외부 폴더에 구별해 남겼다. 초기 helper 구문·집계 실패는 최종25개 성공에 합산하지 않았다.

변경 전 포트 중점 SHA-256은 `488C4B4A95ABC02EB63DDC07D727D623B07D614043100EEE42C73907DF30AA52`, 변경 후는 `E283260E2BBA048C4D5E800DFB42D79F2E73963A11E8428C38158FF272180C0B`다. `korea.before.txt`는 외부 증거 사본이고 현재 작업 소스는 계속 저장소의 중점 파일이다. 실제 UI·정상 연구 적용/소모·저장 검증은 미실행이며 이식 완료 주장은 **구현 반영·범위 정적 확인**으로 한정한다.

기존 정리 미결 산출물 `tools/__pycache__/` 21파일·1,088,888바이트는 이번 작업에서 이동·삭제하지 않는다. 새 시험 산출물은 위 외부 작업 폴더에만 둔다. donor·Workshop·설치 게임·사용자 데이터와 기존 source cache는 읽기 전용으로 보존하며 commit·push·게시·업로드는 수행하지 않는다.
