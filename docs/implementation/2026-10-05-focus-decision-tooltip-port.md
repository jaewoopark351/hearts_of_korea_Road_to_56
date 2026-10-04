# 2026-10-05 원본 결정 해금 툴팁 이식

사용자의 `C:\hoi\hearts_of_korea` 최신 업데이트 복사 요청에 따라 실제 신규 delta만 선택 이식했다. 원본과 RT56, 사용자 데이터와 launcher는 읽기 전용으로 확인했다. 커밋·푸시·게시·업로드는 수행하지 않았다.

## 변경과 동작 범위

원본 `062a60287e00ac11352c38bca0fca1ae556e7801`은 `AGENTS.md` 6줄과 한국 중점 파일 2줄만 추가한다. 직전 설명 업데이트의 현지화 28개 파일은 기존 동결본과 바이트가 같아 재이식하지 않았다. 조사 초기에 원본은 `272e7a2` 위의 미커밋 변경이었으며, 조사 중 원본 사용자가 이를 커밋한 뒤 새 HEAD와 깨끗한 작업 트리를 재확인했다. 이 작업에서 원본 Git 상태를 변경한 것은 아니다.

`HOK_KOR_cmn_closed_material_cycle`의 `completion_reward` 끝에 원본 주석과 `unlock_decision_tooltip = HOK_KOR_cmn_emergency_material_cycle`을 추가한다. 기존 영구 국민정신 II 지급·I 교체 순서를 보존한다. 결정의 실제 해금은 기존 `has_completed_focus`로 유지하며, 정치력 150·90일·국민정신 II·내전/항복/중복 사용 조건도 그대로다. 개별 결정 해금 안내이며 범주 전체 해금이나 즉시 사용 가능성을 추가하지 않는다.

중점 수·ID·선행 조건·배치·AI·보상 수치·그림·현지화·지도는 변경하지 않는다. 기존 RT56 ID 이전과 ADR-0005 지역 병합을 유지한다. 새 구현·그림을 만들거나 과거 중점 전체에 툴팁 지침을 일괄 적용하지 않았다.

원본의 결정 해금 표시 지침만 호환판 `AGENTS.md`에 동기화했다. 원본 문서 전체나 프로젝트 정체성·과거 개인 이력은 복사하지 않았다. 지침 출처 checkout SHA-256은 `3DB3917841B773F1264EDD310916FD8CB676A963331C500C9C6EEDBE7832FF40`이다.

## 조사 기준선

| 항목 | 관측 |
|---|---|
| 날짜 | 2026-10-05 KST |
| 호환판 branch / HEAD | `feat/korean-focus-update-20260922` / `3b6d11d7dfb0d5dde1f62ddb538dde9ed25608d4` |
| 시작 Git 상태 | `git status --short` 빈 출력 |
| 선택 donor branch / HEAD | `feat/korean-focus-expansion-ai` / `062a60287e00ac11352c38bca0fca1ae556e7801`, 최종 깨끗한 작업 트리 |
| 설치 HOI4 | `1.19.3.0.c01a`, Steam build `25205862`, engine build `Sep 9 2026 09:10:08` |
| 최신 기존 실행 | 2026-10-05 04:24 donor 단독, checksum `(7195)`, DLC 36개; 이번 포트 실행 증거가 아님 |
| RT56 | `820260968`, installed/latest manifest `7475007536894105204`, 업데이트 `2026-09-08 08:14:24 KST` |
| RT56 descriptor SHA-256 | `5B323861ABD63E31CB896277E3EA58BA4BCD9FCEEDA957B50792065E42E03F61` |
| RT56 한국 중점 SHA-256 | `A80FBC767C21902FC56EBBCA35DC3C120700E527B52EA98F3CFDF5221EB0EF90` |
| 현재 active playset | `국뽕한국 test01`, donor 단독 |
| 저장된 target 1 | `Road to 56 한국 test01`: 호환판 → RT56 → RT56 Korean Translation |
| 저장된 target 2 | `HOK RT56 Audit C0 20260922`: RT56 → RT56 Korean Translation → 호환판; 이름과 달리 C1 구성 |
| target donor 여부 | 두 저장된 target 모두 donor 없음, 현재 비활성 |
| OS / 언어 / 사용자 데이터 | Windows 11 x64, Korean; `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV` |

저장 순서는 launcher 기록이며 물리 파일별 유효 우선순위의 실행 증거가 아니다. descriptor·외부 launcher의 호환판 item `3796816200`, root 경로, `1.19.*`, RT56와 Korean Language 의존성을 보존한다. donor item `3793992662`를 복사하지 않는다. RT56의 states/strategicregions replacement와 번역의 localisation replacement를 확인했다. 저장된 target은 선언 의존성 Korean Language `2743487021` 대신 번역 `2769576030`를 사용하며, 최종 localisation 계약은 계속 미확정이다.

도구에 선언된 RT56/vanilla 입력 80개의 해시가 기존 pin과 모두 일치한다. 설치 vanilla `common/national_focus/bulgaria.txt:632`에서 같은 country-scope 보상 문법을 확인했고, RT56 `common/national_focus/korea.txt:1806`에도 해당 툴팁 명령이 있다. 이미 포트의 결정·두 언어 명칭·전용 그림이 존재하므로 새 logical ID나 asset은 추가하지 않는다. 이 소스 검토가 실제 UI 표시의 실행 증거는 아니다.

## 생성기와 출처

[독립 lock](../../tools/hok_focus_tooltip_update_lock.json)에 새 원본 commit/blob, 직전 원본 blob, 원본 LF·checkout CRLF 해시, 변경 전후 포트 해시와 정확한 두 추가 줄을 기록한다. 기존 source/artwork/second-wave/policy/localisation/material/prose lock 7개를 변경하지 않는다.

| 바이트 | SHA-256 |
|---|---|
| 새 원본 Git blob `7cc1d3c41f643ef65db5b88d1b7ad7696f109be5` | `377787CD86EC6E51A153215FD596EC3752BC9486B0F92E856F4569C218A93B2A` |
| 새 원본 CRLF checkout | `4D9FAFBA25195A569B2BA4CA0481B1344025CFB009D51E262F571B1EF24F6312` |
| 직전 원본 Git blob `681bb7ad3ded0c5801e909ea3e52177409c38b4f` | `7265ED370C672B49A10B6B177205F178D32073150C68DCCFC07B415AD48B2C8A` |
| 직전 포트 출력 | `6F9F76036B21D22E9716ACE44C124D20BBF2CAF3751AAEE5313C758FC3B8F162` |
| 새 포트 출력 | `4A349FE1631C7A79B178C24C241F00F3E20C20F3B59E061FE1FE6B59DB5F74E1` |

`source_snapshot.py`는 두 immutable blob 사이에 정확히 이 두 줄만 추가됐는지 확인한다. `build_korean_focus_update.py`는 모든 기존 계층을 적용한 후 해금 안내만 덧붙이며, 검토되지 않은 변경 전후 출력은 거부한다. `check_korean_second_wave.py`는 독립 ordered AST로 기존 보상 뒤의 개별 결정 툴팁을 검사한다. 과거 material/prose 보존 gate는 승인된 툴팁을 정확히 역변환한 ancestor와 기존 해시를 비교한다. 기존 assertion이나 source pin을 새 콘텐츠로 덮어쓰지 않는다.

한국 트리는 기존 `OVERRIDE` 분류를 유지한다. 통합 원장에 새 donor 출처·출력 해시와 선택 delta를 기록하며, RT56 base hash와 기존 ancestor 기록을 보존한다. 원장 1,417행·충돌 73개·분류 수량은 그대로다.

## 별도 checkout 바이트 보정

작업 시작 descriptor는 LF였지만 기존 material/prose lock과 원장은 CRLF 바이트를 요구했다. 내용이 현재 HEAD blob과 정확히 같고 CRLF 변환 해시가 두 lock의 `D68DCE620EA3DDDE422F26F2E5155E4D52F35AC4B2EBE1224DC71E07035141CB`와 일치함을 확인한 뒤 바이트만 복원했다. `.gitattributes`에 descriptor CRLF와 새 lock LF를 명시했다. 정체성·의존성·문구를 수정하거나 기존 lock을 약화하지 않았다.

통합 원장 재생성에는 AGENTS·중점 2행 외에 기존 checkout 때문에 낡아 있던 출력 해시 52행 갱신도 포함된다. 52행 모두 output hash만 달라지고, 직전 원장의 해시는 HEAD 내용을 CRLF로 변환한 해시와 일치한다. 현재 52개 파일은 HEAD와 개행 정규화 후 동일하다. 이 작업에서 해당 runtime·README·gitignore 파일은 편집하지 않았다. 한꺼번에 줄바꿈을 정규화하거나 이를 신규 gameplay 변경으로 기록하지 않는다.

## 검증과 한계

- 생성기 관리 output 406개 중 한국 중점 1개만 갱신했다. 실제 runtime 내용 diff는 원본과 같은 2줄이다. descriptor의 별도 개행 복원을 제외하고 새로운 runtime 파일·자산·삭제는 없다.
- 최종 `python tools/validate_port.py`: **20 PASS / 0 WARNING / 1 기존 ERROR**, exit 1. 새 원본 delta·생성기 재현·ordered AST·과거 보존 gate·원장·구조·참조·현지화·ID 검사는 통과했다. 남은 것은 기존 KOR history/doctrine 생성 불일치이며 전체 clean 통과로 보고하지 않는다. 검사 출력은 도구 stdout으로 확인했고 새 test/diagnostic 파일은 만들지 않았다.
- 최종 `git diff --check` exit 0. 실제 내용 diff가 있는 production 경로는 `common/national_focus/korea.txt` 하나다. 통합 원장 SHA-256은 `5E0BD5F54302B405E11EAA8465FB52524716A17AA85433F1D7853F2616AA9DEB`이다.
- 원본 HEAD·깨끗한 작업 트리·선택 checkout 해시와 RT56 manifest를 적용 후 재확인했다.
- 초기 aggregate 실행은 병렬 도구 수정과 겹쳐 새 API 미완성·원장 미갱신 오류를 포함했다. 이를 수정 전 기준선이나 최종 결과로 사용하지 않는다. 후속 검사에서 descriptor의 기존 checkout 불일치를 분리 확인·복원했다.
- HOI4를 실행하거나 playset·설정·로그·세이브를 변경하지 않았다. 실제 보상 툴팁 표시, locked/available/completed UI, 정상 진행, DLC·장기 진행·저장·멀티플레이는 이번 변경에 대해 **UNPROVEN**이다. donor 로그를 포트 검증으로 대신하지 않는다.

기존 KOR history의 MtG 전쟁지지도 `0.1`과 doctrine 생성기의 기대 `0.05` 불일치는 이번 표시 업데이트에서 변경하지 않는다. 정적 결과와 엔진 실행 결과를 구분하며 완전한 호환 검증이나 출시 준비 완료를 주장하지 않는다.
