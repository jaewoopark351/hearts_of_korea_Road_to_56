# 2026-09-23 한국 2차 확장 이식 구현

<!-- [2026-09-23]_kpopmodder: 후속 실제 게임 검증 결과와 범위 제한을 연결한다. -->
상태: **콘텐츠·이미지·생성기 병합 완료. 정적 20 PASS / 0 WARNING / 1 기존 ERROR. 후속 실제 게임 검사 9개 시나리오에서 909 PASS / 0 FAIL / 0 SKIP.** 강제 완료·효과 검사 기준이며, 정상 중점 진행·화면 표시·저장 재로드는 미검증입니다. 자세한 범위와 남은 오류는 [실행 검증 기록](../audits/2026-09-23-second-wave-runtime.md)에 정리했습니다. 아래 기준선 표는 구현 착수 당시의 관측값입니다.

## 범위와 기준선

사용자가 [계획](../plans/2026-09-23-korean-second-wave-port-plan.md)을 인용하고 `AGENTS.md`, `/docs`를 읽어 구현하도록 요청했다. 현재 RT56 호환판 위에 원본의 한국 확장만 이식했다. 원본·Workshop·게임 설치본은 수정하지 않았고 커밋·푸시·업로드도 하지 않았다. 앞선 AGENTS 및 계획 문서 변경은 보존했다.

| 항목 | 고정값·관측 |
|---|---|
| 호환판 | `feat/korean-focus-update-20260922`, `c84fd9faa543a9d2f3aabd8bebe7691984dc6cc3` + 미커밋 작업 |
| 선택 donor | `be5fb40dbd8de33e5adbf65e808bcb0e8c283560`, `feat/korean-focus-expansion-ai`; 작업 시작 당시 clean |
| donor 중점 입력 SHA-256 | `1CEDAF78903DB31D15E3837E20069B71BCA8FC674212B1D033F0D721B2B6735C` |
| 이전 호환판 중점 SHA-256 | `D33DC929878F3CBB2750164086D9B0120C2DAC2ED45B994C5384A720E8D15C22` |
| 최종 호환판 중점 SHA-256 | `6F9F76036B21D22E9716ACE44C124D20BBF2CAF3751AAEE5313C758FC3B8F162` |
| RT56 | Workshop `820260968`, manifest `7475007536894105204`, timeupdated `1788822864` |
| RT56 descriptor SHA-256 | `5B323861ABD63E31CB896277E3EA58BA4BCD9FCEEDA957B50792065E42E03F61` |
| 관측한 최근 게임 | 9월 23일 14:29:53 `system.log`, HOI4 `1.19.3.0.c01a (c5c7)`, Windows 11 x64, `l_korean` |
| 최근 게임의 구성 | donor 포함 Workshop 13개. RT56/호환판 없는 사용자 혼합 구성으로, 이번 이식의 실행 증거가 아님 |
| DLC·번역 | `disabled_dlcs=[]`만 관측, 이번 시험의 활성 DLC는 미확인. descriptor의 Korean Language와 별도 RT56 번역 계약은 미확정 |

이전 전역 donor lock와 89개 그림의 lock는 그대로 두고 [새 lock](../../tools/hok_second_wave_lock.json)에 선택 입력을 별도로 고정했다. Git commit/blob, Git 객체 SHA-256, 실제 checkout SHA-256·크기·개행 형태를 각각 기록한다. 최신 원본 전체를 기존 전역 생성기의 기준으로 바꾸지 않았다.

## 반영한 내용

| 종류 | 결과 |
|---|---|
| 중점 | 326 → **460**. 신규 134개: 공산 28, 파시즘 24, 입헌 14, 전제 14, 환제국 14, 만주 20, 공통 20 |
| 연계 콘텐츠 | 국민정신 63개, 90일 사업 18개, 결정 분류 4개, 주 동적 효과 12개 |
| 지원 텍스트 | 41개: ideas 10, decisions 4, categories 4, dynamic modifiers 1, 한영 현지화 22 |
| 신규 시각 자산 | HOK DDS **231개**, GFX 등록 파일 **16개**, sprite 정의 365개 |
| 기존 그림 | DDS 89개와 기존 GFX 3개 바이트 유지 |
| 런타임 파일 | 신규 **288개** + 기존 `common/national_focus/korea.txt` 병합. 기존 생성기 관리 112개를 포함하여 최종 관리 출력 400개 |
| 출처 문서 | 원본 명세·이미지 manifest·크레딧 37개를 [고정 문서 사본](../upstream/hok-second-wave-be5fb40/README.md)에 바이트 그대로 보존 |
| 통합 원장 | 1,123 → **1,411행**, 과거 exact-path RT56 충돌 73개 유지. 새 파일은 `ADD`/`ASSET_COPY`, 한국 중점은 기존 `OVERRIDE` 안의 검토된 병합 |

원본 수치·정치 경로·선행 조건·보상·AI 조건·사업 비용·90일 기간을 보존했다. 한 게임에서 배타 경로를 포함한 460개 전부를 완료한다는 뜻은 아니다. 기존 민주 역사 AI 계획은 donor와 동일하여 변경하지 않았다.

기존 326개 중점에서 허용한 변경은 다음 7개의 배치 필드뿐이다. 각각 최신 고정 donor의 값과 대조하며 그 밖의 보상·조건 변경은 검사기가 거부한다.

- `KOR_support_gaema_plateau`, `KOR_build_soyanggang_dam`: 상대 기준·x·y.
- `KOR_future_of_the_republic`, `KOR_democracy_advance_forward`, `KOR_empowering_the_nrsc`, `KOR_urihwangsilsaranghoe`: offset·x.
- `KOR_long_live_the_dictatorship_of_the_proletariat`: offset.

기존 한국 주·province 번호 변환, 15주 만주 통합, 대일 강화, MAN 인물 조건 보호와 독립당의 부분 동원 보상을 유지했다. 최신 원본에 있는 부분 동원 보상을 다시 주입하지 않는다. 국민정신 3개 기존 파일의 donor 차이는 주석뿐이므로 현재 출력도 유지했다. 지도·국가 history·JAP/CHI 전역 파일·descriptor·Workshop 신원은 이번 구현에서 바꾸지 않았다.

## 지역과 이미지 병합

[ADR-0005](../decisions/0005-korean-second-wave-regional-integration.md)는 같은 주 번호가 다른 영역을 뜻하는 문제를 실제 province 및 지도 중첩으로 확인하고 대응을 고정한다. **RT56 행정 경계에 맞춘 근사 대응**이며 원본 경계를 완전히 복원한 것은 아니다.

- 만주 M1/M2/M4: `328·941` 모두. M3: `328·941·714·944·945·717·942·943` 모두.
- 착수·유지·중단·재착수·효과 제거·지도 강조·한영 설명에 같은 집합을 사용한다. 주별 효과 수치는 원본 그대로다.
- 환제국은 원본의 거점 8개 대안 중 하나를 요구하며, 각 대안 안에서는 대응 주 전부를 요구한다. 분할주 하나만으로 통과시키지 않는다. 거점 상실을 기존 환제국 국민정신 제거 조건으로 확대하지 않는다.
- 신규 HOK DDS는 원본과 해시가 같다. 크기·alpha·frame·format을 바꾸지 않았고, 결정에는 원본의 소형 전용 그림을 연결했다.
- 새 shine registry의 overlay 경로만 `gfx/interface/goals/shine_overlay.dds`로 바꿨다. donor가 복사해 둔 overlay 1개는 가져오지 않는다. vanilla 공급 파일의 SHA-256은 `BB416649358C73D34AACD46BAD61BC44211FAC8111627B56E25F385AD98F4448`이다. HOK payload·mask는 로컬이며 공유 광택은 host 참조다.

## 검증과 재현

Python은 이 환경의 `C:\Users\jaewo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`를 사용했다. 아래 `python`은 이 실행 파일을 뜻한다.

```text
python tools/source_snapshot.py --import-second-wave --export-second-wave-docs
python tools/build_korean_focus_update.py
python tools/build_integration_manifest.py --apply
python tools/validate_port.py
python tools/check_korean_focus_update.py --self-test
python tools/check_korean_second_wave.py --self-test
python tools/korean_second_wave_geography.py --check
```

생성기는 허용 목록과 이전 출력 해시를 검사하고 독립적으로 수정된 파일 덮어쓰기를 거부한다. 기존 source lock를 바꾸거나 donor를 수정하지 않는다. 주석을 제외한 순서 보존 AST 비교는 생성기 출력 자체가 아니라 고정 donor에서 기대값을 만든다. 신규 지역 변환은 별도의 AST 알고리즘으로 재구성해 텍스트 변환 구현과 대조한다.

| 검사 | 결과 |
|---|---|
| 작업 전 aggregate | **18 PASS / 0 WARNING / 2 ERROR**: 기존 doctrine 생성 불일치 및 갱신 전 원장 불일치 |
| 최종 콘텐츠 aggregate | **20 PASS / 0 WARNING / 1 ERROR**: 아래 기존 doctrine 문제만 남음 |
| 기존 중점 계약·변형 시험 | PASS; 의도적으로 만든 회귀 13개 탐지 |
| 신규 중점 계약·변형 시험 | PASS; 의도적으로 만든 회귀 14개 탐지 |
| 새 경로·논리 ID 충돌 | compat/RT56/vanilla/두 번역 모드와 대조, 신규 288 경로 및 134 focus·63 idea·18 decision·4 category·12 dynamic·365 sprite·언어별 479 key의 외부 충돌 0 |
| 지역 근거 | 28개 지리 입력 해시, 원본 override 부재, 대응표 재계산과 부분 소유/통제 실패 조건 PASS |
| 재현·그림·현지화 | 생성 출력 400개 일치, 231 DDS 원본 해시, 경로 대소문자·연결·공급자, 66개 현지화 파일·5,050 key PASS |
| RT56 보존 | 기존 map·공용 override·pruning·15주 만주·MAN·대일 처리 gate PASS |

`CONFIRMED`: `history/countries/KOR - Korea.txt`는 작업 전부터 MtG 분기 `set_war_support = 0.1`이고 `migrate_doctrines.py`의 기대 출력은 `0.05`다. 이 파일과 생성기를 이번에 변경하거나 검사를 약화하지 않았다. 따라서 전체 정적 검사가 깨끗하게 통과했다고 보고하지 않는다. 실행물은 별도 사용자 변경을 보존한 상태다.

마지막 변경 목록에서도 기존 런타임 파일 중 변경된 것은 한국 중점 파일 하나이며 신규 런타임 파일은 288개다. KOR history의 SHA-256 `243FC1FBDE8DB75B82CCFEBD6BB01CA7001DABCD944CA8534E7324413705BE30`을 유지했다. CRLF를 보존한 `git diff --check`는 exit 0이고, 사용자 모드 목록도 백업과 바이트 동일하다.

감사 원본은 `.local-artifacts/second-wave-port-20260923/`와 `.local-artifacts/second-wave/pre-import-collision-audit.json`에 있다. 사용자 로그·저장·개인 경로가 포함될 수 있는 실행 증거는 배포 대상으로 삼지 않는다.

## 후속 실행 검증과 남은 범위

구현 직후에는 게임을 실행하지 않았으나, 이후 사용자의 실제 실행 요청에 따라 HOI4 `1.19.3.0.c01a`의 RT56 대조 게임과 호환판 한국 새 게임을 실행했다. 실행별 통과·중단·진단 결과와 설정 복원은 [9월 23일 실행 감사](../audits/2026-09-23-second-wave-runtime.md)에 기록한다. 원본의 실행 PASS나 9월 22일 기존 326개 중점 실행 결과를 이번 460개 포트의 통과 증거로 사용하지 않는다.

후속 검사는 임시 이벤트에서 실제 중점 완료·결정 활성화를 호출하고 효과 및 기간 경과를 로그로 관측한다. 정상 중점 선택·35일 진행·조건부 화면 배치·실제 DDS 표시·AI·수동 저장/재로드·다른 DLC 및 번역 조합은 별도 검증이 필요하다. 기존 저장 호환·멀티플레이·전체 오류 0건·배포 준비 완료는 주장하지 않는다.
