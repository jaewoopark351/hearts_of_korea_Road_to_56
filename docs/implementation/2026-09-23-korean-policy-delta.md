# 2026-09-23 원본 정책 변경 17파일 이식

상태: **요청한 원본 변경 반영 완료. 정적 검증 20 PASS / 0 WARNING / 1 기존 ERROR. 이번 변경의 게임 실행 검증은 하지 않았다.**

## 범위와 기준선

사용자가 스크린샷으로 지정한 원본 변경 17개를 현재 호환판에 반영하도록 요청했다. 원본 작업 트리에는 정확히 같은 17개 경로가 있었다(수정 15개, 새 문서 2개). 한국 정책의 의도적 비용·보상 변경이며 호환성 복구나 전체 원본 재이식이 아니다.

| 항목 | 확인한 기준 |
|---|---|
| 호환판 착수 상태 | `feat/korean-focus-update-20260922@f108e847159670d88238009c8e28de3828cd7fae`, clean |
| 원본 | `be5fb40dbd8de33e5adbf65e808bcb0e8c283560` + 지정된 미커밋 17파일 |
| 엔진 | HOI4 `1.19.3.0.c01a`, 2026-09-09 빌드; Steam build ID `25205862` |
| 실행 파일 SHA-256 | `7DC947BE34970DA1E1C787BCDDBE7F62B610FF258AEBF8F06AA8B348F3A031D5` |
| RT56 | Workshop `820260968`, manifest `7475007536894105204`, timeupdated `1788822864`; 작업 전후 동일 |
| RT56 descriptor SHA-256 | `5B323861ABD63E31CB896277E3EA58BA4BCD9FCEEDA957B50792065E42E03F61` |
| 호환판 descriptor | RT56 + Korean Language 의존성, 기존 호환판 ID `3796816200`; `replace_path`·launcher `path` 없음; 변경 없음 |
| 운영체제·언어 | Windows 11 x64 `10.0.26200.0`, `l_korean` |
| 실제 사용자 데이터 | `C:/Users/jaewo/OneDrive/문서/Paradox Interactive/Hearts of Iron IV` |
| 현재 선택 구성 | `dlc_load.json`에는 원본 HOK만 활성화. 최신 로그도 원본 모드 1개·DLC 36개를 기록하며 호환판 검증 근거가 아님 |
| 호환판 launcher 경로 | `mod/hearts_of_korea_Road_to_56.mod` → 이 저장소, RT56 + Korean Language 의존성. 현재 원본 전용 구성을 변경하지 않음 |

직전 [실행 감사](../audits/2026-09-23-second-wave-runtime.md)는 같은 엔진/RT56에서 원본을 끈 C0/C1 검증과 강제 효과 909 PASS를 기록한다. 그 결과는 이번 비용·보상 변경의 실행 증거로 전용하지 않는다. 현재 모드 목록의 순서를 유효 로드 우선순위로 주장하지 않으며, 새 target run은 수행하지 않았다. 번역 의존성 최종 계약도 이번 범위에서 변경하지 않았다.

## 반영 내용

런타임은 결정 3파일, 국민정신 1파일, 한영 현지화 6파일이다. [잠금 파일](../../tools/hok_policy_update_lock.json)에 전체 경로·이전 출력 해시·원본 해시가 있고, [원본 문서 사본](../upstream/hok-policy-update-20260923/README.md)에 관련 명세·지침·사건 기록 7개가 있다.

| 변경 대상 | 최종 동작 |
|---|---|
| 평안·강원·충청·경상 지역 산업 사업 4개 | 정치력 150, 민간공장 5개 점유 및 가용 공장 수 조건 제거; 90일 유지 |
| `HOK_KOR_finance_allied_industry` | 정치력 75 → 150, 민간공장 2개 점유 및 수량 조건 제거; 180일 유지 |
| `HOK_KOR_yeo_rural_credit_project` | 정치력 75 → 150, 민간공장 2개 점유·착수 및 AI 공장 수 조건 제거; 건설 속도 +10% 유지 |
| `HOK_KOR_pak_current_output_project` | 정치력 75 → 150, 민간공장 2개 점유·착수 및 AI 공장 수 조건 제거; 군수공장 생산량 +10% 유지 |
| `HOK_KOR_accountable_administration_idea` | 일일 정치력 고정 수치 0.25 → 1.0 |
| `HOK_KOR_public_accounts_idea` | 일일 정치력 고정 수치 0.25 → 1.0, 기존 안정도 +2% 유지 |

`CONFIRMED`: 원본 diff와 현재 출력에서 위 변경이 일치한다. 정치력은 비율이 아닌 일일 고정 수치다. 결정 보상·기간·재사용·대기시간·소유/통제/슬롯·항복/내전 조건, 공산 사업의 정치력 AI 조건 및 기존 AI 가중치는 유지한다. 다른 사업의 비용 정책으로 확대하지 않았다.

모든 대상은 기존 HOK 논리 ID를 유지하는 `ADD` 분류다(호스트에 없는 한국 전용 정의라는 뜻이며 이번에 새 파일을 추가했다는 뜻은 아니다). 열 개 경로에 RT56/vanilla 동일 경로 파일이 없고, 변경된 결정 7개·국민정신 2개의 ID도 두 공급자의 해당 데이터베이스에서 충돌하지 않는다. `political_power_gain`의 국가 국민정신 사용은 설치 vanilla `common/ideas/GER.txt:61`, `japan.txt:172` 및 RT56 `GER.txt:6236`, `SOV.txt:2055`에서 확인했다.

산업 결정은 기존 생성기의 주 변환 `1029→1144`, `1031→1145`, `1030→920`을 적용하며 평안 `527`은 유지한다. 지도·중점·이미지·공유 RT56 정의·descriptor·국가 history는 변경하지 않았다. 민주 국민정신의 기존 포트 그림 기여 주석 6개도 보존했다.

## 재현과 출처 보존

기존 `hok_source_lock.json`, `hok_icon_lock.json`, `hok_second_wave_lock.json`과 당시 원본 문서들은 그대로 유지한다. 새 잠금은 기준 커밋의 Git blob과 검토한 줄 변경을 보관하며 정확한 BOM·혼합 개행까지 재구성하고 SHA-256으로 확인한다. 이후 원본의 미커밋 작업이 변하더라도 이번 승인 범위가 조용히 바뀌지 않는다. Git 객체는 기존과 같이 읽기 전용 원본 저장소에서 읽는다.

`source_snapshot.py`의 문서 export, `build_korean_focus_update.py`의 마지막 10파일 정책 계층, 기존 검사기 두 개, 통합 원장 생성기를 갱신했다. 통합 원장은 1,411행을 유지하고 이번 미커밋 출처를 과거 donor 커밋의 완성본으로 잘못 표기하지 않는다. 생산 파일은 생성기를 통해서만 썼으며 이전 출력 해시가 다른 사용자 변경은 덮어쓰지 않는다.

## 검증 결과와 한계

아래 `python`은 `C:/Users/jaewo/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`다.

```text
python tools/source_snapshot.py --export-policy-docs
python tools/build_korean_focus_update.py
python tools/build_integration_manifest.py --apply
python tools/check_korean_focus_update.py --self-test
python tools/check_korean_second_wave.py --self-test
python tools/validate_port.py
git diff --check
```

| 검사 | 결과 |
|---|---|
| 원본 고정 | 17파일 원본/재구성 SHA-256 일치, 기존 잠금 3개 불변, 원본 작업 상태 불변 |
| 재생성 | 기존 400개 관리 출력과 원장 일치; 런타임 변경은 지정한 10파일뿐 |
| 기존 확장 회귀 검사 | 22개 의도적 변형 탐지 PASS |
| 2차 확장 회귀 검사 | 24개 의도적 변형 탐지 PASS |
| 이번 핵심 조건 | 공장 점유·착수·AI 수량 조건 재도입, 잘못된 정치력 비용, 낮은 단계/상위 단계 정치력 회귀 및 상위 안정도 소실 탐지 |
| 전체 정적 검사 | 20 PASS / 0 WARNING / 1 기존 ERROR |
| 현지화 | 66파일/5,050키 BOM·header·중복 검사 PASS, 변경 쌍의 기여 주석 및 원본 개행 보존 |
| RT56 보존 | 지도·공유 override·pruning·지역/만주 병합 gate PASS, manifest 및 descriptor 지문 유지 |
| diff 검사 | `git diff --check` PASS |

기존 ERROR는 `history/countries/KOR - Korea.txt`의 MtG 분기 `set_war_support = 0.1`과 `migrate_doctrines.py` 기대값 `0.05`의 불일치다. [직전 구현 기록](2026-09-23-korean-second-wave-port.md)에도 남아 있던 문제이며 해당 파일은 이번 HEAD와 내용이 동일하고 SHA-256 `243FC1FBDE8DB75B82CCFEBD6BB01CA7001DABCD944CA8534E7324413705BE30`을 유지한다. 이번 범위 밖의 값을 고치거나 검사를 약화하지 않았다.

`UNPROVEN`: 변경된 결정을 실제 선택했을 때 정치력 차감·공장 점유 해제·UI 설명·기간 완료/취소가 의도대로 동작하는지, 국민정신의 실제 일일 정치력 및 정상 업그레이드 동작. 정상 진행·AI 실행·기존 진행 중 사업의 저장 호환·다른 DLC/번역·멀티플레이도 미검증이다. 이전 실행 결과와 정적 검사를 이번 엔진 검증으로 표현하지 않는다.

원본·Workshop·게임·사용자 설정은 수정하지 않았다. 커밋·푸시·게시·업로드 없이 이 호환판 작업 트리에 변경을 남겼다.
