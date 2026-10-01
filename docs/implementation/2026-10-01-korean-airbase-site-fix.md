# 2026-10-01 평안·충청 공군기지 중복 배치 수정

## 범위와 상태

사용자는 평안과 충청이 각각 하나의 주인데 공군기지가 두 곳에서 선택된다는 제보를 확인하도록 요청했다. 지정한 플레이세트에서 수정 전 재현을 마친 뒤, `AGENTS.md`와 `docs/`를 읽고 해당 결함을 구현으로 수정하도록 승인했다.

이 작업은 지도 생성기의 공군기지 배치 병합만 보정한다. 평안 `527`과 충청 `1145`에서 HOK 좌표를 유지하고, 함께 남아 있던 RT56 좌표 두 행을 제거한다. 건설 수준, 수용량, 주·province ID, history, 한국 이외 지도와 다른 건물 배치를 변경하지 않는다. `rocket_site_spawn` 중복은 별도 검토 대상이며 이번 수정에 포함하지 않는다.

- 수정 전 파일 중복과 실제 UI 재현: **CONFIRMED**
- 생성기 수정·재생성: **완료**
- 수정 후 대상 정적 검사: **통과**; aggregate는 **20 PASS / 0 WARNING / 1 ERROR**
- 수정 후 cold start 및 동일 UI 재현: **통과**

평안·충청의 공군기지 중복 선택 결함은 수정 후 같은 플레이세트의 새 게임에서 사라졌음을 확인했다. 전체 모드 호환성이나 release readiness를 완료했다는 뜻은 아니며, 정적 aggregate의 기존 교리 검사 오류와 미검증 범위를 아래에 별도로 기록한다.

## 기준선과 입력 출처

| 항목 | 기록 |
|---|---|
| compatibility 시작 Git 상태 | `feat/korean-focus-update-20260922@8a24fbb2f8ccaed50d3bc032053cfd39fe679954`, 시작 시 작업 트리 깨끗함 |
| 작업일 | 2026-10-01, Asia/Seoul |
| 실제 HOI4 버전 | `1.19.3.0.c01a` |
| 수정 전 메뉴 checksum | `d698` |
| 수정 후 메뉴 checksum | `8098` |
| 운영체제·화면 | Windows 11, 1600×900, GUI scale 1.0 |
| 실제 사용자 데이터 | `C:/Users/jaewo/OneDrive/문서/Paradox Interactive/Hearts of Iron IV/` |
| 언어 | 한국어 |
| 사용자가 지정한 플레이세트 | `HOK RT56 Audit C0 20260922` |
| 실제 활성 모드 목록 | The Road to 56 → The Road to 56 Korean Translation → 로컬 compatibility port |
| runtime 구성 분류 | 실제 번역 모드가 포함되므로 검증 분류는 `C1`; 플레이세트 이름의 `C0`와 구분 |
| compatibility 물리 경로 | `C:/hoi/hearts_of_korea_Road_to_56` |
| HOK donor 활성 여부 | 비활성; 실제 게임 의존성으로 사용하지 않음 |
| DLC 설정 | `disabled_dlcs=[]`; 이 값만으로 소유 DLC 전체가 실제 활성화됐다고 판정하지 않음 |
| RT56 Workshop item·manifest | `820260968` / `7475007536894105204` |
| 현재 donor | `C:/hoi/hearts_of_korea`, commit `8609d0b61e4c00e6be6c204dcf31cfa41150664e` |
| 지도 생성기의 고정 HOK base | `887930f6e88c80568d62dab9cfbe1ba8a498a252`의 지도 입력; `.local-artifacts/sources/hok-887930f-korea-118d7b5`에서 소비 |

활성 모드 목록의 순서는 launcher에 기록된 목록이다. 각 모드의 모든 database에서 유효 우선순위가 같다는 증거로 사용하지 않는다. 이번 대상은 실제 로컬 생성 파일과 게임의 공군기지 선택 결과를 함께 확인한다.

지도 생성기가 사용하는 고정 HOK base와 현재 donor HEAD는 별개다. 이번 `map/buildings.txt`는 고정 base와 현재 donor 파일의 SHA-256이 같아 기존 지도 입력을 유지한다. donor 최신 트리 전체를 다시 복사하거나 source pin을 느슨하게 바꾸지 않는다.

| `map/buildings.txt` 입력/수정 전 출력 | SHA-256 |
|---|---|
| RT56 host | `807C419FEB4CB107BFE73EBFE82FEA01B895977751F01D604A3C8ACE1FB3B42E` |
| 고정 HOK 지도 입력 | `DA7A22BC7F3996FC89496BEE248B530FA7039917564AD50B09F6B05A7F574A53` |
| 현재 HOK donor | `DA7A22BC7F3996FC89496BEE248B530FA7039917564AD50B09F6B05A7F574A53` |
| target vanilla 참조 | `4A336B6245026FCC693ED2BE7AE316A164135585AEC945EA190E32B8E65F4094` |
| compatibility 수정 전 | `D59C5981AAF8409E12E4FC85D048573270402AAC18E88854F8ED233E7583E2FA` |

관련 선행 결정은 [ADR-0002 지도 ID 마이그레이션](../decisions/0002-map-id-migration.md), [ADR-0004 한국 콘텐츠 우선](../decisions/0004-hok-korean-content-priority.md), [9월 6일 항구 배치 closure 보정](2026-09-06-map-building-closure-fix.md), [9월 22일 source 재기준선](../audits/2026-09-22-source-rebaseline.md)이다. 그 문서의 과거 실행 상태를 이번 실행 결과로 대체하지 않는다.

## 수정 전 증거와 원인

`CONFIRMED`: 수정 전 compatibility `map/buildings.txt`에 동일 주의 `air_base`가 서로 다른 좌표로 두 행씩 존재했다.

| 주 | 수정 전 출력 행 | 출처·행 내용 |
|---|---:|---|
| 평안 `527` | 56132 | RT56 유지 행: `527;air_base;4784.00;14.15;1336.00;2.38;0` |
| 평안 `527` | 71876 | HOK 추가 행: `527;air_base;4770.21;10.70;1308.47;2.17;0` |
| 충청 `1145` | 58685 | RT56 `919` 배치를 한국 지형에 따라 재분류: `1145;air_base;4787.00;9.62;1254.00;1.47;0` |
| 충청 `1145` | 71878 | HOK donor `1031`을 ADR-0002의 `1145`로 이전: `1145;air_base;4782.00;9.68;1257.00;2.43;0` |

RT56 원본의 충청 관련 행은 58685행 `919;air_base;4787.00;9.62;1254.00;1.47;0`이며, 기존 생성기의 좌표 샘플·state 재분류가 compatibility에서 이를 `1145`로 옮겼다. RT56 원본의 다른 지역 state `1031` 공군기지 행은 별개 정의이며 제거 대상이 아니다.

HOK donor의 평안·충청 행은 각각 66677, 66679행이다. vanilla의 `527`, `1031` 배치는 위 HOK 변경 좌표와 다르다. 이는 HOK 한국 지형에서 새로 선택한 두 좌표라는 근거이며, vanilla 전체 배치를 복원해야 한다는 뜻은 아니다.

`CONFIRMED`: 사용자가 지정한 플레이세트에서 두 주의 UI 증상을 직접 확인했다. 평안의 두 아이콘을 각각 클릭했을 때 같은 비행단과 `60/200`이 표시됐다. 충청에서는 기지 한 단계만 건설하고 비행단을 이동했으며, 두 아이콘에서 같은 비행단과 `60/200`이 표시됐다. 따라서 이 재현에서는 기지 수준 두 개가 별도로 생긴 것이 아니라, 한 주의 같은 기지 상태가 두 위치에서 선택됐다.

- [평안 수정 전 선택 화면](</C:/Users/jaewo/.codex/visualizations/2026/10/01/01a0f635-d03a-7820-8c19-75cf0e8b9324/hoi4-airbase-audit/pyongan-south-selected.png>)
- [충청 수정 전 비행단 이동 후 선택 화면](</C:/Users/jaewo/.codex/visualizations/2026/10/01/01a0f635-d03a-7820-8c19-75cf0e8b9324/hoi4-airbase-audit/chungcheong-southeast-selected-occupied.png>)

원인 분류는 **map building placement 병합 결함**이다. 기존 생성기는 RT56 행을 유지·재분류한 다음 HOK-vs-vanilla 추가 행을 붙였다. 기존 중복 검사는 전체 행의 동일성만 확인하므로, 주와 건물 종류가 같아도 좌표가 다른 두 행은 모두 통과했다. 보존된 RT56 배치와 HOK 배치가 같은 effective state의 공군기지 선택 지점으로 함께 등록된 것이 이번 최소 수정의 대상이다.

## 병합 결정과 구현

`map/buildings.txt`의 기존 분류 **`BINARY_MERGE / GENERATED`**를 유지한다. RT56을 전체 지도 base로 삼고 HOK 한국 지형에서 의도한 배치만 적용하는 결정이다. HOK 우선 범위는 ADR-0004의 한국 presentation·지도이고, 한국 밖 RT56 행은 보존한다.

| effective state | 남길 HOK 행 | 제거할 RT56 base 행 |
|---:|---|---|
| 527 | `527;air_base;4770.21;10.70;1308.47;2.17;0` | `527;air_base;4784.00;14.15;1336.00;2.38;0` |
| 1145 | `1145;air_base;4782.00;9.68;1257.00;2.43;0` | 원본 `919;air_base;4787.00;9.62;1254.00;1.47;0`, 기존 재분류 뒤 `1145` |

`tools/build_rt56_map.py`에 `KOREAN_AIR_BASE_SITE_OVERRIDES` 두 항목을 추가했다. 정확한 두 host 원본 행과 HOK replacement 행이 source에서 각 한 번, 재분류된 host 행과 이전된 HOK 행이 병합 목록에서 각 한 번 존재하는지 검사한다. 두 배치의 bitmap 샘플이 모두 예상 effective state의 land province에 있는지 검증한 뒤 host 행만 제거한다. 예상 source 행·migration·좌표 소속이 달라지면 중단하며, 임의로 다른 공군기지 행을 골라 제거하지 않는다. 유지할 HOK 행은 기존 추가 행에서 소비하며 두 번 삽입하지 않는다.

또한 `validate_korean_air_base_sites()`가 `BUILDING_TARGET_STATES`의 모든 한국 대상 주(`525`, `527`, `917–920`, `1144–1147`)에 정확히 한 개의 `air_base` 배치가 있는지 검사한다. 0개와 2개 이상 모두 실패한다. HOK 지리 대상에서 제외된 `528`과 한국 이외 RT56 주에는 이 단일 배치 규칙을 확대하지 않는다. 공장·벙커·항구처럼 여러 배치가 가능한 다른 건물은 이 규칙의 대상이 아니다.

기존 150행 재분류, HOK 추가 21행, 해안 항구 복원 7행, state site 복원 3행을 유지하고, 검토한 host 행 2개만 제외했다. 최종 행 수는 `71863 + 21 + 7 + 3 - 2 = 71892`다. 생성기가 관리하는 다른 지도 산출물 17개는 모두 바이트가 같다.

생성 산출물은 직접 편집하지 않았다. 생성기를 수정한 뒤 `--apply`로 `map/buildings.txt`를 재생성했다. 최종 SHA-256은 `839486E33E51AB800BB8930A11AB5F7A9F6C779FE8F9CADB1E54E5D147733841`이다. 수정 전 바이트에서 검토한 host 행 두 개만 뺀 결과와 바이트 단위로 같아 나머지 행의 내용·순서·줄바꿈이 보존됐음을 확인했다.

`tools/build_integration_manifest.py`의 기존 지도 병합 설명에 이 결정을 추가하고, [생성 분류 원장](../audits/2026-09-06-production-file-classification.csv)을 재생성했다. 1,411행을 유지하며 `map/buildings.txt`의 출력 hash와 이유만 갱신했다. 원장 최종 SHA-256은 `CBFBE965429C644730A8CAB0F12288A88E4C31EC5186B4F32CCB918B8B98EA22`다. donor/RT56/vanilla source hash와 기존 source lock은 유지했다.

이 선택의 대안으로 HOK 좌표를 버리고 RT56 좌표만 남기는 방법도 있으나, 두 좌표는 HOK 한국 지형을 위한 placement delta이고 한국 표현을 HOK 우선으로 보존하는 ADR-0004와 맞지 않아 채택하지 않는다. 모든 한국 건물 배치를 일반 중복 제거하는 방식은 host 내용 손실 위험과 관련 없는 건물의 의미를 바꾸므로 채택하지 않는다.

## 검증 기록

| 구분 | 상태·결과 |
|---|---|
| 수정 전 실제 UI 재현 | 위 평안·충청 두 선택 지점, 같은 비행단/수용량 확인 |
| source fingerprint 시작 확인 | 위 세 source `map/buildings.txt` 해시 일치; 고정 HOK와 현재 donor 바이트 일치 |
| 생성기 `--check`/재생성 재현 | PASS; 생성 전 baseline, 생성 후 및 runtime 종료 후 검사 통과. 최종 18개 산출물이 생성기와 일치하고 입력 fingerprint assertion도 모두 유지 |
| 정확한 출력 diff | PASS; 수정 전 바이트에서 지정한 RT56 재분류 행 2개만 제거한 결과와 일치, 다른 지도 산출물 17개 변화 없음 |
| 한국 대상 주당 단일 `air_base` gate | PASS; 대상 10개 주 각각 한 행 |
| 독립 인메모리 회귀 검사 | PASS; 8개 검사 통과. 중복/누락 air site gate 실패, 비한국 주·rocket site 비대상, 한국 10개 주 한 행, HOK 두 좌표 유지 및 정확한 두 행 제거를 확인; 디스크 입력·runtime 출력 변조 없음 |
| 기존 map closure·host 보존 gate | PASS; map generator의 기존 gate 유지 |
| 통합 manifest 재생성·검사 | PASS; 1,411행 유지 |
| `python tools/validate_port.py` | **20 PASS / 0 WARNING / 1 ERROR**; 공군기지/map 관련 gate 통과, 아래 교리 검사 오류 별도 |
| `git diff --check` | PASS, exit code 0 |
| 수정 후 full-process restart | PASS; 16:32 KST 새 HOI4 프로세스, 같은 활성 모드 3개, 메뉴 `1.19.3.0.c01a (8098)` |
| 평안 단일 아이콘·실제 선택 | PASS; HOK 위치의 한 아이콘, 2개 비행단 `60/200`, level 1; 제거한 옛 RT56 위치 클릭은 기지가 아닌 공역 선택 |
| 충청 한 단계 정상 건설·단일 아이콘 | PASS; 1월 1일 일반 건설 UI에서 1단계만 예약, 3월 28일 22:00 완료 후 한 아이콘에서 `0/200`, level 1 |
| 충청 비행단 이동 후 실제 선택 | PASS; 경기의 전투기 비행단 2개(각 30기)를 일반 UI로 이동, 1936-03-29 16:00 paused 상태에서 한 기지 클릭 시 level 1·`60/200`·두 비행단 확인 |
| 새 게임·unpause·정상 진행 | PASS; `game.log` 16:34:23 KST SINGLEPLAYER launch, 16:34:27 RestoreDeviceObjects, 16:34:30 지도 진입; 1936 KOR 1월 1일에서 3월 29일까지 진행 |
| 수정 후 관련 로그 확인 | 대상 검색에서 `air_base`, `airbase`, `airport`, 건물 중복 관련 결과 0건; 전체 로그 무오류를 의미하지 않음 |
| 수정 후 RT56 manifest·source fingerprint 재확인 | PASS; 검증 종료 시 manifest `7475007536894105204`와 HOK/RT56/vanilla buildings 입력 hash 불변 |

정적 aggregate의 1 ERROR는 `tools/migrate_doctrines.py --check`의 교리 migration 재현 검사이며 공군기지/map gate와 구분한다. 독립 대조 결과, 예상 산출물과 현행 `history/countries/KOR - Korea.txt:52`의 차이는 MtG 분기 `set_war_support = 0.05` 기대값과 커밋된 `0.1#20260922_kpopmodder` 한 곳이다. 현행 파일 SHA-256은 `243FC1FBDE8DB75B82CCFEBD6BB01CA7001DABCD944CA8534E7324413705BE30`으로 [9월 23일 runtime 감사](../audits/2026-09-23-second-wave-runtime.md)와 [9월 26일 현지화 이식](2026-09-26-localisation-sync.md)의 baseline과 같다. 이번 작업에서 이 파일, 교리 생성기와 `source_snapshot.py`를 변경하지 않았다. 별도 balance·생성 소유권 문제이며 해당 수치나 gate를 공군기지 수정에 끼워 바꾸지 않았다.

수정 후 UI 증거:

- [cold start 메뉴·checksum](</C:/Users/jaewo/.codex/visualizations/2026/10/01/01a0f635-d03a-7820-8c19-75cf0e8b9324/hoi4-airbase-audit/postpatch-main-menu.png>)
- [평안 단일 기지 선택·60/200](</C:/Users/jaewo/.codex/visualizations/2026/10/01/01a0f635-d03a-7820-8c19-75cf0e8b9324/hoi4-airbase-audit/postpatch-pyongan-single-selected.png>)
- [평안 옛 RT56 기지 위치 클릭·공역 선택](</C:/Users/jaewo/.codex/visualizations/2026/10/01/01a0f635-d03a-7820-8c19-75cf0e8b9324/hoi4-airbase-audit/postpatch-pyongan-old-site-air-region.png>)
- [충청 일반 UI 건설·1단계 예약](</C:/Users/jaewo/.codex/visualizations/2026/10/01/01a0f635-d03a-7820-8c19-75cf0e8b9324/hoi4-airbase-audit/postpatch-chungcheong-one-level-queue.png>)
- [충청 정상 건설 완료·단일 기지 0/200](</C:/Users/jaewo/.codex/visualizations/2026/10/01/01a0f635-d03a-7820-8c19-75cf0e8b9324/hoi4-airbase-audit/postpatch-chungcheong-single-empty.png>)
- [충청 비행단 도착·단일 기지 60/200](</C:/Users/jaewo/.codex/visualizations/2026/10/01/01a0f635-d03a-7820-8c19-75cf0e8b9324/hoi4-airbase-audit/postpatch-chungcheong-single-occupied.png>)

공군기지 건설·비행단 이동은 정상 UI로 실행했다. 강제 효과나 console reload를 적용한 결과로 대체하지 않았다. 수정 후 로그와 실제 활성 목록은 같은 evidence directory의 `postpatch-run-logs/`, `postpatch-dlc_load.json`에 복사해 분리 보존했다. 대상 검색 결과와 실제 두 주의 선택 결과를 확인했으며, 전체 `error.log`가 깨끗하다는 주장은 하지 않는다. 검증 종료 후 게임은 1936-03-29 16:00, 충청 기지 선택 화면에서 일시정지해 뒀다.

## 동작 영향·남은 검증·Git 상태

수정 후 평안·충청은 각각 한 공군기지 아이콘·클릭 지점을 제공한다. 평안과 충청 모두 level 1에서 수용량 200, 비행단 두 개의 60기가 정상 표시됨을 확인했다. 기지 레벨, 항공기 수용량, 건설비, 건설 기간, 비행단 ID·편제, 시작 OOB·history, 연구와 보상은 변경하지 않았다. 새 state/province ID를 만들거나 이전하지 않았다.

기존 ADR-0002의 지도 migration 세이브 정책을 이번 위치 보정으로 완화하지 않는다. 수정 전 세이브의 호환, 장기 진행, 모든 bookmark, DLC 조합, 추가 모드, AI와 multiplayer는 이번 대상 UI 검증만으로 증명되지 않는다. 새 R0/R1 control 실행도 이번 batch에서 하지 않았으므로 RT56 전체 비교 완료를 주장하지 않는다. 이번 두 공군기지 문제와 별도로 발견될 수 있는 rocket site 배치 문제 역시 해결했다고 기록하지 않는다.

최종 변경은 아래 다섯 파일이다.

- `tools/build_rt56_map.py`: 검토한 RT56 좌표 두 행 제거와 한국 주당 한 공군기지 배치 검사.
- `map/buildings.txt`: 생성기가 지정한 두 행만 제거.
- `tools/build_integration_manifest.py`: 기존 지도 병합 분류의 설명에 이번 결정 기록.
- `docs/audits/2026-09-06-production-file-classification.csv`: 해당 출력 hash와 설명 재생성.
- `docs/implementation/2026-10-01-korean-airbase-site-fix.md`: 이 구현·검증 기록.

원본 donor, RT56 Workshop, 게임 설치, 사용자 데이터, 로그·세이브·launcher 설정을 직접 편집하지 않았다. 게임 실행에 따라 새로 생긴 runtime 로그는 읽기 전용 증거로 복사했다. 네 기존 파일의 수정과 이 신규 문서 한 개를 작업 트리에 남겼으며 commit, push, tag, Workshop update/publication은 하지 않았다.
