# 한반도 미사일 기지 배치 수정

함경 `918`의 RT56 미사일 위치 두 행을 제외하고 누락된 HoK 원래 위치 한 행을 복원했다. 충청 `1145`는 기존 HoK 위치를 유지하고 RT56 위치 한 행만 제외했다. **구현과 해당 배치의 정적 검증은 완료했으며, 실제 기지의 단일 표시·선택과 건설·발사 검증은 미완료다.**

## 승인 범위와 기준선

2026-10-11 사용자가 [수정 계획](../plans/2026-10-11-korean-rocket-site-fix-plan.md)을 제시하고 `AGENTS.md, /docs 읽고 구현해줘`라고 요청했다. 앞선 문서화 요청과 구분되는 구현 승인이다. 변경은 두 주의 `rocket_site_spawn` 배치, 소유 생성기·검사, 통합 원장과 기록으로 제한했다. 기지 수준·건설비·시간·기술·DLC 조건·장비·생산·발사 효과를 변경하지 않았다. Git commit, push와 Workshop 게시도 수행하지 않았다.

| 항목 | 구현 시작 시 기준선 |
|---|---|
| 호환판 | `C:/hoi/hearts_of_korea_Road_to_56`; `feat/korean-focus-update-20260922@9b63b53bae89c6c2f6635447f5838c9ac54a2c1b` |
| 시작 작업 트리 | 기존 문서 인덱스 수정과 미사일 계획 문서만 있었으며 보존함 |
| 현재 HoK donor | `C:/hoi/hearts_of_korea`; clean `4d8241e3cd33ebbceaca9650ab36b9891a22b56d` |
| 생성기의 고정 HoK 입력 | `.local-artifacts/sources/hok-887930f-korea-118d7b5`; map base `887930f6e88c80568d62dab9cfbe1ba8a498a252` |
| RT56 | Workshop `820260968`; manifest `7553774178744855191`; `timeupdated=1791503935` (2026-10-09 08:58:55 KST) |
| 수정 전 실제 실행 | 01:23:45 시작; HOI4 `1.19.3.0.c01a (f040)`, DLC 36개, 한국어, Windows 11, 1600×900, GUI scale 1 |
| 기록된 활성 모드 | RT56 → RT56 Korean Translation `2769576030` → 로컬 호환판; donor 없음 |
| 사용자 데이터 | `C:/Users/jaewo/OneDrive/문서/Paradox Interactive/Hearts of Iron IV` |
| 로컬 launcher 연결 | `mod/hearts_of_korea_Road_to_56.mod`의 `path`가 위 호환판 root를 가리킴 |

실제 목록은 `dlc_load.json`과 `system.log`에서 확인했다. 특정 정의의 효과적 우선순위를 목록 순서만으로 확정하지 않았다. 저장소 descriptor는 RT56과 Korean Language를 선언하지만 이번 실행은 RT56 Korean Translation을 사용한다. 기존 localisation 계약 차이는 해결하지 않았다. launcher 플레이세트 이름은 확인하지 못했으며 해당 실행은 번역 모드를 포함한 C1 구성이다.

## 원인과 선택 규칙

`CONFIRMED`: 수정 전 함경과 충청의 배치 파일에는 미사일 위치가 각각 두 행 있었다. 함경의 HoK 행은 vanilla와 동일하여 기존 donor-versus-vanilla 차집합에서 빠졌다. 따라서 RT56 위치 중 하나를 고르는 것으로는 HoK 우선 결정을 적용할 수 없었다. 충청의 HoK 행은 이미 출력에 있었다.

RT56 건물 정의는 `rocket_site`의 `spawn_point = rocket_site_spawn`을 사용하고, 위치 정의는 `type = state`와 `max = 1`이다. 건물 `state_max = 3`은 수준 상한이며 위치 수와 구분했다. 상세 수정 전 근거·행 번호는 [계획의 위치 조사](../plans/2026-10-11-korean-rocket-site-fix-plan.md#현재-위치와-증거-수준)에 보존했다.

| 처리 | 원본 행 | 최종 주 / 샘플링한 육지 프로빈스 |
|---|---|---|
| 제외 | `527;rocket_site_spawn;4784.00;12.82;1312.00;5.72;0` (RT56) | `918 / 10083` |
| 제외 | `918;rocket_site_spawn;4827.00;9.65;1341.00;1.39;0` (RT56) | `918 / 959` |
| 제외 | `919;rocket_site_spawn;4788.00;9.70;1254.00;2.71;0` (RT56) | `1145 / 7175` |
| 복원 | `1028;rocket_site_spawn;4816.00;9.70;1333.00;1.13;0` (HoK) | `918 / 6922` |
| 유지 | `1031;rocket_site_spawn;4785.00;9.68;1255.00;3.78;0` (HoK) | `1145 / 13563` |

`tools/build_rt56_map.py`는 위 RT56 source 세 행과 HoK source 두 행을 정확히 지정한다. source 유일성, 기존 주 이전, 예상 프로빈스·육지·소속 주, 병합 후 행의 유일성이 달라지면 중단한다. 복원 allowlist에 함경 한 행만 추가했다. 출력의 다른 `1028`·`1031`은 RT56이 소유하는 한반도 밖 주이므로 ID로 넓게 삭제하지 않는다.

본토 `525, 527, 917, 918, 919, 920, 1144, 1145`의 미사일 위치를 각각 정확히 한 행으로 검사하며, 각 좌표가 해당 주의 육지에 있는지도 확인한다. 제주 `1146`·쓰시마 `1147`와 한반도 밖에는 새 중복 정리 정책을 확장하지 않았다. 기존 한국 대상 10개 주의 공군기지 단일 배치, 항구 spawn coverage와 전체 위치 coverage 검사를 유지했다.

## RT56 철도 차이와 제한 생성 모드

RT56 `map/railways.txt`는 작업 전부터 과거 pin과 달랐다. 전체 지도 재기준선과 미사일 위치 수정을 분리했다.

| 파일 | SHA-256 |
|---|---|
| RT56 철도 과거 input pin | `0CFEF6244DF5A04A8EBE0C1027C27287C375F31CBDA94F265FC549DF6CC61547` |
| 현재 RT56 철도 | `52E60257F9490A27E7AC6EFD07BDD34FD46B0FBE82D2BA55A5558F25C1A7392D` |
| 보존한 호환판 철도 | `D424E72B580B35C836B0881D6D6C18744B5C747C1652BD25D3E555D65FFED89E` |

차이는 한반도 밖 Java의 두 경로다. 현재 원본 411행은 `1 9 12249 7421 13499 4434 7642 13523 10135 10491 4608`이며, 과거 경로의 `13524`가 `10135`로 바뀌었다. 412행은 `1 3 13522 13524 10491`이며, 마지막 `13523`가 `10491`로 바뀌었다. 이 두 변경만 메모리에서 되돌리면 과거 pin의 바이트 해시와 정확히 일치한다. 이번에 Java 경로를 이식하거나 host 철도 pin을 갱신하지 않았다.

새 `--buildings-only` 모드는 사용하지 않는 현재 RT56 철도 입력만 읽기·검증 대상에서 제외한다. 다른 고정 입력은 모두 검사하고, 기존 호환판 철도는 위 고정 해시와 일치해야 한다. definition·bitmap·주·보급망 등 동반 산출물 17개를 재구성·검증한 뒤 현재 파일과 바이트가 모두 같아야 `map/buildings.txt` 한 파일만 생성한다. 입력 검증은 생성 전후에 실행한다. 기본 전체 생성 모드는 기존 철도 pin을 그대로 검사하므로 현재 drift를 계속 실패로 보고한다.

## 산출물과 출처

생성기는 아래 한 파일을 다시 만들었고 통합 원장은 소유 스크립트로 갱신했다. 게임 runtime 변경은 `map/buildings.txt` 하나뿐이다.

| 항목 | 결과 |
|---|---|
| 수정 후 지도 생성기 SHA-256 | `0034DFED55FC6908DE810EDF82A37FEDB66A30725D7DD43F4C706BF2C263C76C` |
| 수정 전 배치 SHA-256 | `839486E33E51AB800BB8930A11AB5F7A9F6C779FE8F9CADB1E54E5D147733841` |
| 수정 후 배치 SHA-256 | `C74C4CDE00969EEA98AE4F42CD60727BB6D6BD2411FDFC159EEF32E8AC999F79` |
| 배치 행 수 | 71,892 → 71,890 |
| 전체 미사일 위치 행 수 | 1,149 → 1,147 |
| 두 주 밖 미사일 위치 | 1,145행, 바이트·순서 동일; LF 및 마지막 LF를 포함한 목록 해시 `8984948F7A02E97F5A66533C9127A4D3178755233439F32DBE3B140F59617226` |
| 다른 지도 산출물 | 17개 전부 바이트 동일 |
| 원장 | 1,417행; 분류 `BINARY_MERGE / GENERATED` 유지; 새 출력 해시·선택 근거·이 기록 연결 |
| 원장 SHA-256 | `D0AA993918D9B05843F552A179F29B0C55CB138C04C9AF08921C995816B11A9C` |

HoK 현재 donor 및 고정 `buildings.txt` 입력은 `DA7A22BC7F3996FC89496BEE248B530FA7039917564AD50B09F6B05A7F574A53`, RT56은 `807C419FEB4CB107BFE73EBFE82FEA01B895977751F01D604A3C8ACE1FB3B42E`, vanilla는 `4A336B6245026FCC693ED2BE7AE316A164135585AEC945EA190E32B8E65F4094`다. donor 최신 전체 트리 복사나 source snapshot 갱신은 하지 않았다. RT56 manifest와 buildings·definition·bitmap·railways는 02:02:50 KST 독립 재확인에서도 동일했다.

수정 파일은 지도 생성기, `map/buildings.txt`, 통합 원장 생성기와 CSV, `tools/validate_port.py`, `tools/check_korean_second_wave.py` 및 관련 문서다. 역사적 원료 순환·설명 업데이트의 lock JSON은 그대로 보존했다. 기존 배치 pin 검사는 허용된 네 행 변경만 역변환한 전체 바이트가 원래 `839486…` 해시와 일치해야 통과하도록 추가했다. 관련 없는 행·순서·개행 변경을 허용하지 않는다.

## 정적 검증

시험 파일·기준선·로그 사본은 `C:/hoi/test/2026-10-11-rocket-site-fix/`에 보관했다. 저장소나 donor·Workshop·game·사용자 데이터에 시험 파일을 생성하지 않았다.

| 검사 | 실제 결과 |
|---|---|
| `build_rt56_map.py --apply --buildings-only` 및 `--check --buildings-only` | 통과; 동일한 새 SHA-256으로 재현 |
| 통합 manifest `--apply` 및 aggregate의 `--check` | 통과; 1,417행 |
| 외부 `placement-regression.py` | **34 PASS / 0 FAIL**: 정확한 바이트 변경, 17개 산출물 보존, 본토 8개 주별 누락·중복, 다른 주·바다 좌표, source 누락·중복·변경, 예상 프로빈스·migration 변화, 철도·동반 산출물 변화 거부 |
| 독립 역사적 배치 검사 | 원래 배치와 새 배치 역변환 통과; 의도적 변형 12개 거부 |
| 원료 순환·설명 보존 검사 격리 | 각각 통과. live descriptor 불일치를 구분하기 위해 역사적 descriptor fixture만 메모리에 넣었으며 실제 파일은 변경하지 않음 |
| `git diff --check` | 통과 |
| aggregate 수정 전 | **16 PASS / 0 WARNING / 5 ERROR**, exit 1 |
| aggregate 수정 후 | **17 PASS / 0 WARNING / 5 ERROR**, exit 1; 새 미사일 배치 gate 통과 |

전체 검증의 기존 다섯 오류는 full map 철도 input drift, shared overrides input drift, East Asia overrides input drift, doctrine migration의 GER history drift, second-wave 계약의 `descriptor.mod` 바이트 pin 불일치다. 이번 작업에서 오류를 숨기거나 무관한 원본 변경을 섞어 고치지 않았다. scoped 통과를 aggregate 전체 통과로 표현하지 않는다.

## 실행 관찰과 남은 검증

수정 전 01:28:19 KOR 새 게임은 1936.01.01.12 일시정지까지 들어갔다. `~` 계열 콘솔 입력이 반영되지 않아 `ic`·`roic` 활성화와 미사일 기지 건설은 수행하지 못했다. 사용자 제보가 함경·충청을 가리키는지와 이중 표시·선택의 직접 재현은 여전히 `UNPROVEN`이다.

수정 후 기존 게임 창이 없는 상태에서 새 프로세스를 실행했다. 02:05:52 시작, `system.log:273`의 **HOI4 Operation Postern v1.19.3.0.c01a (f1b6)**, DLC 36개, 동일한 활성 모드 3개를 확인했다. `game.log`는 02:06:16에 13,569 provinces 로딩, 02:06:28–29에 1936 history 실행을 기록한다. 일반 클릭·키 입력은 국가 선택 화면에서 반영되지 않았지만, 마우스를 조금 오래 누르는 방식으로 회복했다. 한국 선택 후 **02:15:08 KOR 단일플레이 새 게임 실행**, 1936.01.01.12 일시정지 지도와 RT56 환영 창 해제를 실제 UI에서 확인했다. 이 기록은 새 게임 진입 증거이며 미사일 기지 표시 검증과 구분한다.

진입 후 `grave`와 `Shift_L+grave`를 다시 시도했지만 콘솔이 열리지 않았다. 화상 키보드도 시도했으나 콘솔이 확인되지 않았고 닫기 버튼·표준 닫기 단축키 입력도 반영되지 않았다. 임시 화상 키보드가 남아 있다. `ic`·`roic`는 켜지 않았으며 기지 건설, 단일 아이콘·선택, 수준 증가, 발사 동작은 확인하지 않았다. 기존 저장 게임을 읽거나 덮어쓰지 않았고 launcher·번역·게임 설정을 변경하지 않았다.

시작 직후 보존한 `postpatch-logs/`의 error.log는 launcher descriptor 오류 6행만 있었으나 이후 로그가 더 기록됐다. 최종 `postpatch-kor-logs/`는 비어 있지 않은 error.log 667행을 보존한다. 수정 전 669행과 시간 부분만 제거하고 행별 횟수를 비교했을 때 **신규·증가 행은 0개**였다. 수정 전 random.log rename 실패 2행만 이번 실행에서 없었다. 공용 GFX·항공기 DB 등의 기존 오류는 남아 있으며 전체 로그가 깨끗하다고 판정하지 않는다. `rocket_site`, rocket spawn, missile position, building position 및 buildings.txt 오류 검색은 0행이다. 로그에 해당 오류가 없다는 사실로 표시·선택 정상 여부를 확정하지 않는다.

증거는 `prepatch-logs/`, 초기 `postpatch-logs/`, KOR 진입 후 `postpatch-kor-logs/`, `runtime-status.txt`에 구분했다. 남은 완료 조건은 입력 가능한 실행에서 수정 전 제보 대상과 두 좌표를 확인하고, 수정 후 완전 재시작한 새 게임의 함경·충청에서 HoK 한 위치 표시·선택과 실제 건설·발사를 비교하는 것이다. normal progression, RT56-only 대조, 장기 진행, 저장 호환성, 다른 DLC·bookmark와 multiplayer는 이번에 검증하지 않았다. 기존 지도 migration의 신규 게임 정책을 유지한다.
