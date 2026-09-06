# 2026-09-06 포팅 후 새 게임 접근 위반

## 문서 상태

- 상태: **Open — 항구 배치 원인 후보 정적 수정, cold test 대기**
- 최초 확인된 동일 계열 실행: 2026-09-06 17:14
- 최신 재현: 2026-09-06 21:30
- 이전 사건: [14:06 시작 크래시 조사](2026-09-06-startup-crash.md)
- 디버깅 절차: [HOK 한국 콘텐츠 우선 디버깅 플레이북](../KOREAN_CONTENT_DEBUGGING.md)

이 사건은 1차 포팅 전 14:06 데이터베이스 로드 크래시와 구분한다. 최신 21:28 비한국 국가와 21:30 KOR 실행은 번역 모드 없이 지도 등록과 history 실행을 통과해 싱글플레이 시작 요청까지 도달했지만, 지도 화면에 진입하기 전에 같은 네이티브 접근 위반으로 종료됐다.

## 1. 조사 범위

이 기록은 다음 자료를 읽기 전용으로 조사한 결과다.

- `<HOI4_LOGS>/error.log`
- `<HOI4_LOGS>/game.log`
- `<HOI4_LOGS>/setup.log`
- `<HOI4_LOGS>/system.log`
- `<HOI4_USER_DATA>/crashes/hoi4_20260906_192054/`
- `<HOI4_USER_DATA>/crashes/hoi4_20260906_212823/`
- `<HOI4_USER_DATA>/crashes/hoi4_20260906_213040/`
- 현재 compat, HOK donor, RT56과 vanilla의 관련 정의

최초 조사는 읽기 전용으로 수행했다. 후속 구현에서는 compatibility 저장소의 생성기와 생성 산출물·문서만 수정했으며, donor, RT56 Workshop, vanilla, 사용자 로그·crash dump와 launcher 설정은 수정하지 않았다.

## 2. 실행 기준선

| 항목 | 값 |
|---|---|
| HOI4 | Operation Postern `1.19.2.0.a729 (18bf)` |
| build time | 2026-06-29 14:16:56 |
| commit | `a729d47bd1c55457e6886b6eeb2fcdef4ac05057` |
| DataChecksum | `1b8bfef72bfa60a3735bc6782b2ca33b` |
| 새 세이브 | `IsOldSave: false` |
| DLC | active 36 |
| RT56 Workshop manifest | `3323396725579032799` |
| compat Git 기준 | `main@70aaba43a98fd429378ec1a67d4398f16330e101` 위 미커밋 포팅 작업 |

21:28/21:30 crash bundle의 `dlc_load.json`과 `meta.yml`이 기록한 활성 모드는 다음 두 개다.

1. The Road to 56
2. 하츠 오브 코리아 × Road to 56 호환 포트 [개발판]

실제 compat와 launcher descriptor는 `The Road to 56` 및 `Korean Language`를 dependency로 선언하지만, 최신 C0 재현은 localisation 모드를 모두 비활성화했다. 이 구성에서도 같은 crash가 발생했으므로 localisation은 이번 재현의 필요조건이 아니다. 다만 공식 localisation dependency 계약은 별도 C1 검증 전까지 미결정이다. 19:20 실행이 `Korean Language` 대신 `The Road to 56 Korean Translation`을 사용했다는 과거 불일치도 보존한다.

### 증거 hash

| 파일 | SHA-256 |
|---|---|
| `21:28/error.log` | `D309A3F130B48BEC586304F62D59FB60EA2688755131D3F06CD5065A0E7DF05B` |
| `21:28/exception.txt` | `5E95619E3820045EC8ABC66897A299B3848113E684F29148DD21953C5262A053` |
| `21:30/error.log` | `E1D522814E148EFE6FB910D4B550E907D8F98247D59D1D814A6C9EDE5BDC27EA` |
| `21:30/setup.log` | `D72495B2EE4C6DD830D1CEE8B92D260CD57F5D4466BCFE25ADE8CAE776C4C121` |
| `21:30/system.log` | `593DD580828C44EFC047BB6ED88835F72E4AA6F0E8A6A67C4CC6869D1399CB6D` |
| `21:30/game.log` | `53494A3DB3CF4177D2C7F527B4EF60AA0018C9F7C4224C1F9EDFA4AD72C6A5A7` |
| `21:30/exception.txt` | `EDDACCA9CD23EA0C26F693D853878BE7FF9CF6644E56048F8021EC76F11E2AC1` |

## 3. 실행 진행과 크래시

19:20과 최신 21:28/21:30 `game.log` 계열은 다음 단계까지 기록했다.

- `19:20:10`: 4,469 defines 로드
- `19:20:25`: **13,569 provinces 로드**
- `19:20:33-34`: 1936.1.1.12까지 history 실행
- 21:28과 21:30: 1936 새 게임 `Launching SINGLEPLAYER-game`

그 직후 crash bundle이 생성됐다.

- 예외: `C0000005 (EXCEPTION_ACCESS_VIOLATION)`
- 최신 주소: `0x00007FF7B393E510` — ASLR 때문에 절대 주소는 달라질 수 있음
- 기록 시각: `2026-09-06 21:28:24`, `21:30:41 +0900`
- stack: 두 실행의 14개 frame offset이 전부 동일하며 첫 frame은 `PHYSFS_swapULE64 (+11427536)`

21:28 비한국 국가와 21:30 KOR는 같은 DataChecksum, 정규화 오류군과 stack으로 실패했다. 17:14와 19:20 실행도 같은 offset stack 계열이다. 현재 실패가 우연한 단발성 종료가 아니라 국가 선택 및 번역 계층과 무관하게 같은 계열로 재현된다는 점은 `CONFIRMED`다. 다만 stack 자체에는 원인 파일명이 없다.

## 4. 14:06 사건 대비 진행

| 항목 | 14:06 구현 전 | 19:20–21:30 포팅 후 | 판정 |
|---|---:|---:|---|
| `error.log` 물리 행 | 938 | 678 | 참고값; 줄 수 자체는 완료 기준 아님 |
| 구조화 오류 기록 | 877 | 675 | 같은 주의 적용 |
| `Malformed token` | 다수 | 0 | 이전 province 누락 오류 해소 |
| 미등록 province 13448–13534 | 87 | 0 | RT56 province 집합 보존 |
| 로드된 province | history 이전 crash | 13,569 | compat definition이 실제 적용된 강한 증거 |
| state/region/railway/supply/adjacency 진단 | 연쇄 오류 | 0 | 초기 지도 등록 문제 해소 |
| 한국 음성 duplicate/load failure | 각각 18 등 | 0 | 단일 registry + HOK WAV payload 구조 정상 로드 |
| 도달 단계 | database load 중 | singleplayer launch | 이전 조기 crash는 넘어감 |

이 결과는 지도 topology, 해안, adjacency, railway와 supply가 gameplay에서 정상이라는 증명은 아니다. crash 때문에 paused map과 unpause를 아직 통과하지 못했다.

## 5. 확인된 남은 오류

### 5.1 CONFIRMED source defect / DISPROVEN crash cause — KOR 시작 history의 유효하지 않은 기술

`error.log:673-677`은 다음을 기록한다.

- `bba_early_transport_plane`: invalid database object, 두 번
- `early_transport_plane`: invalid database object, 두 번
- `history/countries/KOR - Korea.txt:132`: `set_technology: Invalid tech`, 한 번

19:20 실행 당시 compat의 해당 `set_technology` 블록은 DLC 분기에서 두 ID를 사용했다. 현재 RT56의 `common/technologies/bba_air_techs.txt`와 `air_techs.txt`는 이 ID의 기술 정의를 활성 등록하지 않고 “모두 사용 가능” 취지로 처리한다. 따라서 당시 KOR history가 현재 RT56 데이터베이스에 없는 기술을 설정했다는 호환 결함은 `CONFIRMED`다.

후속 구현에서 두 할당을 임의의 대체 기술 없이 제거했다. pinned RT56 source에서 `transport_plane_equipment_1`이 `active = yes`이고 두 폐기 기술 ID의 활성 정의가 없음을 생성기가 검사한다. 21:28/21:30 C0에서 관련 로그 5건은 실제로 0건이 됐지만 동일 crash가 계속됐다. 따라서 source 호환 결함의 수정은 확인됐고, 이 결함이 현재 접근 위반의 직접 원인이라는 가설은 `DISPROVEN`이다. 수송기 생산 UI 자체는 paused map에 도달하지 못해 미검증이다.

### 5.2 CONFIRMED — 한국 음성 로드 오류 없음

19:20 및 21:28/21:30 `error.log`에는 다음이 없다.

- `kor_*` 또는 `.wav` load failure
- duplicate sound ID
- duplicate KOR soundeffect
- category overwrite

19:20 실행 당시 compat `sound/kor`의 WAV 18개는 HOK donor와 byte-identical하고, donor `voice_korea.asset`은 compat에 없었다. RT56 `r56_vo_Korean.asset`이 ID를 등록하며 compat의 동일 가상경로 HOK WAV를 소비하는 구조였다. 이 실행은 HOK payload의 오류 없는 로드를 강하게 지지하지만 실제 가청 출력은 기록하지 않는다.

후속 구현은 compat의 동일 상대경로 `sound/r56_vo_Korean.asset`을 생성해 RT56 category/compressor와 HOK의 전체 재생 목록·가중·volume을 병합했다. `Positive_005`를 포함한 HOK WAV 18개를 모두 사용하고 RT56 전용 두 payload는 참조하지 않는다. 새 registry도 21:28/21:30 로그에서 duplicate/load error 0건이지만 실제 청취는 crash 때문에 미검증이다.

오디오 관련 유일한 메시지는 HOK 음악 `Sinarirang`이 44.1 kHz여야 최적이라는 경고 1건이다. 실제 파일은 48 kHz이며 이 경고는 현재 crash의 직접 증거가 아니다.

### 5.3 CONFIRMED defect / STRONGLY_SUPPORTED crash cause — 한국 해안 항구 spawn 7행 누락

`tools/build_rt56_map.py`의 기존 buildings 병합은 donor 행의 state 뒤 내용이 바닐라와 같으면 RT56에 실제로 존재하는지 확인하지 않고 제외했다. pinned source에서는 이 조건에 해당하지만 RT56에서 제거된 한국 대상 건물 행이 401개이므로 전부 복원할 수는 없다. 합성 bitmap을 좌표로 감사한 결과, 그중 정확히 7개의 `naval_base_spawn`만 HOK 해안 복원 때문에 다시 필요하다.

| effective state | spawn이 필요한 province |
|---:|---:|
| 920 | 1054, 7121, 11912, 12060, 13556 |
| 919 | 13546 |
| 1145 | 13564 |

정적 비교 결과는 다음과 같다.

- pinned RT56: coastal land 2,544개, spawn 미커버 `490`, `1201`, `10715`
- 수정 전 compat: coastal land 2,554개, 위 3개와 한국 7개가 미커버
- donor 후보 7행을 메모리 적용한 뒤 및 현재 생성 산출물: RT56의 기존 3개만 미커버
- 각 후보는 donor에 1회, state를 제외한 같은 행은 바닐라에 1회 존재하고 RT56에는 없음
- 각 좌표는 예상 coastal land province/state를 샘플하며 마지막 필드는 유효한 sea province `2708`, `2781` 또는 `7932`

생성기는 이제 감사한 7행만 별도 topology restoration으로 추가해 `map/buildings.txt`를 71,902행으로 만들고, pinned RT56보다 새로 생긴 coastal-without-spawn이 있으면 실패한다. 출력 SHA-256은 `7BEA83AEC433FBF43A45E31C19C9860F1F907B2AA35959862501E16C42FD7780`이다.

이 생성 결함 자체는 `CONFIRMED`다. crash 인과는 아직 `STRONGLY_SUPPORTED`다. 최신 stack의 14개 offset이 2026-09-01 17:23/18:03 실행과 전부 같고, 당시 로그는 `mapbuildings.cpp:634` 오류 직후 `map.cpp:1679`에서 “coastal but has no port … likely crash”를 명시했다. 그러나 최신 실행은 debug map 경고를 남기지 않았고 수정 산출물로 cold test하지 않았으므로, 사건을 닫거나 직접 원인을 `CONFIRMED`로 올리지 않는다.

상세 변경과 정적 결과는 [한국 해안 항구 배치 closure 보정](../implementation/2026-09-06-map-building-closure-fix.md)에 기록한다.

### 5.4 STRONGLY_SUPPORTED — RT56 plane GFX baseline 오류군

675개 구조화 기록 중 660개가 GFX/entity/equipment graphics 계열이다.

- `Invalid Scope`: 510건
  - RT56 `00_plane_icons.txt`: 494
  - RT56 `01_bba_plane_icons.txt`: 16
- duplicate entity: 60
- equipment graphic DB의 entity 누락: 37
- attachment entity 누락: 20
- missing GFX: 14
- unknown `supersonic_fighter_equipment_1`: 9
- missing animation: 7
- missing parent clone: 2

대량 scope 오류의 source는 RT56 파일이고 14:06에도 비슷한 수로 존재했다. 그러나 `R0` 대조 실행이 없으므로 “호환 포트와 무관한 RT56-only 오류”라는 최종 판정은 아직 `STRONGLY_SUPPORTED`다.

### 5.5 기타

- RT56 `taog_traits.txt:487`: `mio_cat_eq_only_artillery` enum 오류 1건
- 빈 faction template 오류 1건
- RT56 `frontendmainview.gui:380`: `subscription_size` UI element 누락 1건
- 비활성 Workshop descriptor의 `supported_version`/`thumbnail` 경고 6건

frontend 파일은 compat가 제공하지 않고 RT56 파일에서 `subscription_size`가 주석 처리돼 있다. 별도 host/UI 문제로 보이지만 현재 crash의 직접 원인이라는 증거는 없다.

## 6. 경쟁 가설과 구분 실험

| 가설 | 현재 판정 | 구분할 실행 |
|---|---|---|
| 수정 전 KOR invalid tech가 crash의 직접 원인 | `DISPROVEN` | 21:28/21:30에서 오류 0건인데 crash 지속 |
| 합성 지도에서 누락된 한국 항구 spawn 7행이 crash의 직접 원인 | `STRONGLY_SUPPORTED`; defect는 수정됨 | 수정 산출물로 GER/KOR cold start 후 paused map 진입 확인 |
| compat의 다른 전역 map/shared/on_action이 모든 국가 새 게임을 crash시킴 | `UNPROVEN` | 항구 보정 뒤에도 실패할 경우 `R0` 대 `C0-NONKOR` |
| KOR 선택 이후 경로만 crash시킴 | `DISPROVEN` | 비한국 국가에서도 동일 stack 재현 |
| KOR history/OOB/character의 전역 초기화가 crash시킴 | 정적 감사상 지지 약함, 완전 배제는 안 됨 | 항구 보정 뒤에도 실패할 때만 임시 KOR history/OOB 진단 slice 사용 |
| RT56 또는 1.19.2가 compat 없이도 같은 crash를 냄 | `UNPROVEN` | `R0` 및 `R1` cold start |
| RT56 Korean Translation이 이번 crash 재현에 필요 | `DISPROVEN` | 번역 없는 C0에서도 동일 재현; C1 계약은 별도 검증 |
| 복구한 HOK 음성이 crash를 일으킴 | 현재 로그로 지지되지 않음 | 음성 오류 0건이며 우선 제거하지 않음; 필요 시 독립 audio 재현만 수행 |

## 7. 다음 진단 순서

1. 수정된 지도 생성기 `--check`, 1,014-file manifest와 aggregate gate를 통과시킨다.
2. `C0-NONKOR` GER를 cold start해 새 게임 → paused map → +1 day까지 확인한다.
3. 같은 산출물로 `C0-KOR`를 cold start하고 같은 gate 및 한국 항구·해군기지·보급을 확인한다.
4. 두 실행의 관련 기술 오류, 한국 sound duplicate/load 오류, 새 map/port 오류와 crash stack을 비교한다.
5. 같은 stack이 계속되면 `R0` 로그 기준선을 보존한 뒤 global/shared 및 KOR 전역 초기화 slice로 돌아간다. OOB는 NSB 육군 → BBA 공군 → MTG 해군 순으로 되살리고 history는 정치·idea·technology/doctrine, character, variant 묶음으로 이분한다.
6. `C0`가 성공한 뒤 `C1`에서 localisation 계층을 추가한다.
7. 한국이 통과한 뒤 JAP/CHI 시작으로 RT56 동아시아 회귀가 없는지 확인한다.

구체적인 gate, 실행 기록 양식, sound/DDS 검증과 완료 조건은 [디버깅 플레이북](../KOREAN_CONTENT_DEBUGGING.md)을 사용한다.

## 8. 변경 상태

이 문서의 최초 조사는 기존 로그와 source를 읽기 전용으로 수행했다. 후속 구현은 compatibility 저장소에서 KOR 폐기 기술 참조, 한국 자산 registry, 지도 생성기와 생성된 `map/buildings.txt`를 수정했다. donor, RT56 Workshop, vanilla, 사용자 로그·crash dump·launcher 파일은 계속 읽기 전용으로 유지했다. 항구 보정 후 게임 실행, commit, push와 배포는 수행하지 않았다.
