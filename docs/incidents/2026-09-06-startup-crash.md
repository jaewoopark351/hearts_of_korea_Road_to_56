# 2026-09-06 HOI4 1.19.2 시작 크래시 조사

> 역사적 사건 기록: 아래 판정은 1차 구현 전 14:06 실행에 대한 것이다. 지도와 공용 파일의 정적 수정은 이후 구현됐지만 재실행은 아직 없으므로, 이 사건이 런타임에서 해결됐다고 닫지 않는다. 후속 상태는 [1차 구현 기록](../implementation/2026-09-06-first-port-batch.md)과 [정적 검증 기록](../validation/2026-09-06-static-validation.md)을 참조한다.
>
> 후속 기록: 이후 17:14와 19:20 실행은 13,569 province와 history를 로드해 이 사건의 조기 지도 장애를 넘어섰지만, singleplayer launch 직후 별도의 접근 위반이 재현됐다. 현재 사건은 [포팅 후 새 게임 접근 위반](2026-09-06-post-port-new-game-crash.md)에서 추적한다. 이 문서의 당시 음성 인코딩 가설도 최신 무오류 로드 증거로 대체됐다.

## 문서 상태

- 조사 유형: Review / read-only diagnostics
- 조사 일자: 2026-09-06 (Asia/Seoul)
- 대상 실행: `hoi4_20260906_140619`
- 판정: 실제 시작 크래시 확인
- 최우선 확인 사항: HOK 지도 데이터와 현재 Road to 56 지도 데이터의 버전 불일치
- 프로덕션 수정: 없음
- 게임 재실행 및 대조군 시험: 수행하지 않음

이 문서는 한 번의 실행에서 수집된 로그, 크래시 메타데이터, 활성 모드 설정 및 실제 로컬 소스를 교차 검토한 기록이다. 크래시를 고쳤다는 기록이 아니며, 아래의 수정 및 검증 계획도 별도의 구현·실행 허가 없이는 작업 허가로 간주하지 않는다.

## 1. 조사 범위와 경로 별칭

허가된 범위는 로그 확인과 이 진단 문서 작성이다. 게임, Steam Workshop 원본, 사용자 설정, 세이브 및 프로덕션 모드 파일은 수정하지 않았다.

개인 식별 경로는 다음 별칭으로 기록한다.

- `<HOI4_USER_DATA>`: Windows OneDrive 문서 아래 `Paradox Interactive/Hearts of Iron IV`
- `<COMPAT_ROOT>`: `C:/hoi/hearts_of_korea_Road_to_56`
- `<RT56_ROOT>`: `C:/Program Files (x86)/Steam/steamapps/workshop/content/394360/820260968`
- `<VANILLA_ROOT>`: `C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV`

## 2. 실행 기준선

### 게임

- 게임: Hearts of Iron IV
- 버전: `Operation Postern v1.19.2.0.a729`
- 엔진 커밋: `a729d47bd1c55457e6886b6eeb2fcdef4ac05057`
- 빌드 시각: `2026-06-29 15:17:03 +0200`
- 빌드 유형: Release / Live
- 운영체제: Windows 11 x86_64, 시스템 언어 `ko`
- 렌더러: DirectX 11

### 활성 모드

`<HOI4_USER_DATA>/dlc_load.json`과 크래시 메타데이터에 기록된 활성 모드는 다음 세 개다.

1. `mod/hearts_of_korea_Road_to_56.mod`
   - 실제 경로: `<COMPAT_ROOT>`
   - 선언 호환 버전: `1.19.*`
2. `mod/ugc_820260968.mod`
   - 이름: The Road to 56
   - 실제 경로: `<RT56_ROOT>`
   - `replace_path = "history/states"`
   - `replace_path = "map/strategicregions"`
3. `mod/ugc_2769576030.mod`
   - 이름: The Road to 56 Korean Translation
   - `replace_path = "localisation"`

`disabled_dlcs`는 빈 목록이다. 이는 설치·보유한 모든 DLC의 상세 목록을 증명하지 않고, 사용자 설정에서 명시적으로 비활성화한 DLC가 없다는 의미로만 사용한다.

HOK descriptor가 요구하는 `Korean Language`는 이 플레이셋에 없다. 대신 `The Road to 56 Korean Translation`이 활성화되어 있다. 이것이 의도적인 대체인지와 HOK localisation 계약을 충족하는지는 `UNPROVEN`이다.

### 소스 상태

`<COMPAT_ROOT>`에는 `.git` 디렉터리가 없어 브랜치와 커밋을 기록할 수 없다. 이 조사 중 commit, push 또는 다른 Git 변경은 수행하지 않았다.

## 3. 증거 목록

| 증거 | SHA-256 |
|---|---|
| `<HOI4_USER_DATA>/logs/error.log` | `3122B5F4064B1B510C8BB8E9B0AF7AAA0A959A20EE3F1CA249505BBF17A0F20C` |
| `<HOI4_USER_DATA>/logs/setup.log` | `2B59FDC41BF38A9CDD4671E8B63561AD142C7F000D73EF4B7F455AAA467CA653` |
| `<HOI4_USER_DATA>/logs/system.log` | `D47AEA547380AC6B7E7879A9BA62A929AF4C74A6670FFEF33A305979411FC498` |
| `<HOI4_USER_DATA>/logs/game.log` | `59FFAF4D6538D22496375875F591B04C54D4412C4D3DA59CDE10454793D16775` |
| `<HOI4_USER_DATA>/crashes/hoi4_20260906_140619/exception.txt` | `FFA7958193C3E8EFB57E5A7E379EE3C9523EFA1FD55D6B6C827E52E5068D6868` |
| `<HOI4_USER_DATA>/dlc_load.json` | `A5D8A4E360D03F39935ABFD765260AEC39455F821C565C7592D4E2D3A01AD1BD` |

크래시 폴더에 보존된 `error.log`, `system.log`, `dlc_load.json`은 조사 당시 현재 파일과 각각 같은 SHA-256이었다. 따라서 이 문서의 로그와 `hoi4_20260906_140619` 크래시는 같은 실행에서 나온 것으로 확인된다.

## 4. 관찰된 크래시

`CONFIRMED`

- 발생 시각: `2026-09-06 14:06:19 +0900`
- 예외: `C0000005 (EXCEPTION_ACCESS_VIOLATION)`
- 주소: `0x00007FF6958F3322`
- 첫 스택 표기: `hoi4.exe PHYSFS_swapULE64 (+18853090)`
- `DataChecksum`과 `AppChecksum`: 모두 공란
- `IsOldSave`: `false`
- `HasMods`: `true`

스택은 심볼이 제거되었거나 잘못 매핑되어 있어 `PHYSFS_swapULE64` 표기만으로 실제 내부 함수나 원인 파일을 특정할 수 없다.

`STRONGLY_SUPPORTED`

- `game.log`에는 `4469 defines loaded` 한 줄만 기록됐다.
- `setup.log`는 14:06:11부터 14:06:19까지 데이터베이스 등록을 기록한다.
- 모든 런타임 로그가 `[no_game_date]` 상태다.
- 체크섬이 계산되지 않았다.

따라서 체크섬 계산과 국가·세이브 진입 전에 초기 데이터베이스 로딩 중 크래시한 것으로 강하게 뒷받침된다. `setup.log`의 마지막 성공 항목은 `common/ai_strategy_plans/r56_warlord_plan.txt`이지만, 이는 마지막으로 기록된 성공 항목일 뿐 해당 파일이 원인이라는 증거는 아니다.

`error.log`는 938개 물리 행과 877개 타임스탬프 항목으로 구성되며, 시간 범위는 14:06:04~14:06:17이다.

## 5. 발견 사항

### 5.1 CONFIRMED — HOK와 현재 RT56의 지도 definition 불일치

가장 위험한 구조 오류다.

- `error.log:187-273`에는 state 파싱 오류가 49개 항목으로 기록된다.
- `Malformed token`으로 보고된 프로빈스 ID는 중복 없이 정확히 87개다.
- ID 범위는 빈틈없이 `13448`부터 `13534`까지다.
- `<COMPAT_ROOT>/map/definition.csv:13448`의 마지막 프로빈스 ID는 `13447`이다.
- 현재 `<RT56_ROOT>/map/definition.csv:13449-13535`는 `13448`부터 `13534`까지 추가로 정의한다.

대표 오류:

- `history/states/1061-Tacna.txt:29` — `13485`
- `history/states/1131 - Limbang.txt:39` — `13533`, `13534`
- `history/states/667-West Nusa Tenggara.txt:47` — `13504`~`13511`

이는 현재 RT56의 state 세트가 새 프로빈스를 참조하지만, 실제 결합 데이터에서는 HOK의 이전 `definition.csv`가 사용되어 해당 프로빈스가 등록되지 않은 상태임을 직접 보여준다. 관련 49개 state의 province 구성과 후속 지도 데이터는 신뢰할 수 없다.

크래시와의 관계:

- 지도 데이터 불일치 자체: `CONFIRMED`
- 이것이 네이티브 접근 위반의 직접 원인이라는 주장: `UNPROVEN`
- 현재 확인된 오류 중 시작 크래시와 가장 직접적으로 연결될 수 있는 최우선 후보라는 판단: `STRONGLY_SUPPORTED`

`definition.csv`에 누락 행만 추가해서는 안 된다. HOK와 현재 RT56의 `provinces.bmp` 해시도 서로 다르므로, 새 ID의 색상 정의뿐 아니라 실제 픽셀 지형과 다음 데이터를 함께 병합·검증해야 한다.

- state 소속
- strategic region 소속
- adjacency 및 coastal/land/sea 분류
- buildings와 unit positions
- supply nodes와 railways
- victory points
- HOK의 한국 지역 커스텀 지형과 안정 ID

### 5.2 CONFIRMED — HOK의 구형 동일경로 파일이 현재 RT56 정의를 가림

지도 이외에도 같은 형태의 exact-path 충돌이 여러 곳에서 확인된다.

#### MIO 공통 정의

- HOK와 RT56이 모두 `common/military_industrial_organization/organizations/00_generic_organization.txt`를 제공한다.
- HOK 파일에는 `generic_train_organization_r56_NSB`와 최신 anti-vehicle land-mine trait가 없다.
- 현재 RT56 파일은 `generic_mio_trait_anti_vehicle_land_mines`를 7412행에, `generic_train_organization_r56_NSB`를 8646행에 정의한다.
- 로그 결과:
  - train MIO include 누락 37건
  - override trait 누락 3건
  - relative trait 누락 1건
  - 후속 `generic_train_organization_r56_NSB` event target 누락 2건
  - 관련 항목 합계 43건

#### 훈장 scripted trigger

- HOK와 RT56이 모두 `common/scripted_triggers/unit_medals_scripted_triggers.txt`를 제공한다.
- HOK 파일에는 다음 trigger가 없다.
  - `should_have_belgian_medals_trigger`
  - `should_have_peruvian_medals_trigger`
  - `should_have_afghan_medals_trigger`
- 현재 RT56 파일에는 각각 80, 89, 92행에 정의되어 있다.
- 18개 호출 지점이 `Invalid trigger`와 `Unknown trigger-type`으로 각각 출력되어 총 36개 로그 항목이 발생했다.

#### 1936 bookmark

- HOK가 현재 RT56과 같은 경로의 `common/bookmarks/the_gathering_storm.txt` 전체를 제공한다.
- 로그에 기록된 행 번호는 HOK 파일의 참조 위치와 일치한다.
- 존재하지 않는 focus 참조 37개와 idea 참조 7개, 총 44개 참조가 검출됐다.
- 고유하게 잘못된 ID는 40개다.

이 파일은 한국 bookmark 항목만 추가하는 작은 델타가 아니라 다른 국가의 오래된 focus 및 idea 목록까지 유지하여 현재 RT56 bookmark를 가리고 있다.

#### 중국 공용 중점과 CAMCO MIO

- `<COMPAT_ROOT>/common/national_focus/china_shared_TSR.txt:3627` 및 3684에 CAMCO MIO 참조가 활성 상태다.
- 현재 RT56의 대응 참조와 MIO 정의는 주석 처리되어 있다.
- 결과적으로 `CHI_camco_fighter_organization` 4건과 `CHI_camco_bomber_organization` 2건이 존재하지 않는 MIO로 기록된다.

#### HOK 항공기 graphic DB

- `<COMPAT_ROOT>/gfx/interface/equipmentdesigner/graphic_db/00_hok_plane_icons.txt:151`이 `supersonic_fighter_equipment_1`을 활성 참조한다.
- 현재 RT56에서는 이 구형 타입이 주석 처리되어 있다.
- 로그에는 `Unknown equipment type: supersonic_fighter_equipment_1`이 10회 기록된다.

### 5.3 STRONGLY_SUPPORTED — RT56 plane graphic DB의 1.19.2 호환 문제

HOK가 같은 경로를 제공하지 않는 RT56 graphic DB에서도 현 버전 오류가 발생한다.

- `Invalid Scope`: 510건
  - `gfx/interface/equipmentdesigner/graphic_db/00_plane_icons.txt`: 494건
  - `gfx/interface/equipmentdesigner/graphic_db/01_bba_plane_icons.txt`: 16건
- 반복을 제거하면 고유 문제 구문은 21개다.
- 엔진은 국가 scope를 사용하는 조건에 대해 모두 `provided: None`이라고 보고한다.
- 별도로 `00_plane_icons.txt`의 `SPA`, `SPB`, `SPC` 루트 블록을 유효한 country tag로 처리하지 못하는 다중 파싱 오류가 1건 있다.

이 파일들은 HOK가 제공하지 않으므로 RT56와 HOI4 1.19.2 사이의 독립적인 호환 문제로 강하게 뒷받침된다. 다만 RT56 단독 대조 실행을 하지 않았으므로, 이 오류들이 단독으로 시작 크래시를 일으키는지는 `UNPROVEN`이다.

### 5.4 그래픽 및 엔티티 오류

지도와 별개로 다음 오류가 기록된다.

- duplicate entity: 63건, 고유 ID 52개
- attachment 대상 누락: 20건, 고유 ID 6개
- equipment graphic DB의 entity 누락: 37건, 고유 ID 4개
- GFX 누락: 14건, 고유 ID 2개
- parent clone 누락: 2건
- animation 누락: 7건

대표 cascade는 `<RT56_ROOT>/gfx/entities/units_planes.asset:5655`의 `AST_CAS_equipment_entity` parent clone 실패와 그 ID를 사용하는 후속 equipment graphic DB 오류다. 이 그룹에는 RT56와 최신 vanilla/DLC asset 간 불일치 및 HOK 중복 정의가 함께 섞여 있어 파일별 분리 검증이 필요하다.

`common/country_leader/taog_traits.txt:487`의 `mio_cat_eq_only_artillery` enum 오류 1건도 있다. 현재 증거는 RT56의 script enum과 HOI4 1.19.2의 equipment-group 정의가 맞지 않는 별도 dependency 호환 문제를 가리키지만, 대조 실행이 없어 `STRONGLY_SUPPORTED`로 제한한다.

### 5.5 CONFIRMED — 한국 음성 ID 충돌

RT56의 `sound/r56_vo_Korean.asset`과 HOK의 `sound/voice_korea.asset`이 같은 한국 음성 ID를 함께 정의한다.

- sound ID 중복: 18건
- 동일 sound file 로드 실패: 18건
- soundeffect 중복: 5건
- category overwrite: 5건
- `Sinarirang` 44.1 kHz 권고: 1건

HOK의 WAV 파일 18개는 실제로 존재하므로 단순 경로 누락은 아니다. HOK 파일은 32-bit float PCM, 현재 RT56 대응 파일은 16-bit PCM이어서 HOK WAV 인코딩이 로드 실패 원인이라는 해석은 `STRONGLY_SUPPORTED`다.

### 5.6 현재 플레이셋과 무관한 descriptor 경고

`error.log:1-6`의 다음 항목은 현재 활성 플레이셋에 없는 Workshop descriptor를 런처가 검색하면서 발생한 것이다.

- 잘못된 `supported_version`: `ugc_1287402890`, `ugc_1862018480`, `ugc_2038610068`, `ugc_2144271749`
- 예상하지 않은 `thumbnail` token: `ugc_2751312808`, `ugc_3316202525`

이 항목들은 시간상 가장 먼저 나오지만 현재 시작 크래시의 선행 원인은 아니다.

## 6. 원인 판정과 경쟁 가설

| 가설 | 판정 | 구분할 관찰 |
|---|---|---|
| HOK의 구형 지도 스냅샷과 현재 RT56 state 세트의 혼합이 시작 크래시를 유발했다 | `STRONGLY_SUPPORTED` | RT56 단독 대조군이 로드되고, 지도 병합 후 동일 플레이셋이 체크섬 및 메인 메뉴를 통과하는지 확인 |
| 동일경로의 구형 HOK 공통 파일들이 MIO·훈장·bookmark·중국 중점 오류를 만든다 | 오류 발생은 `CONFIRMED`, 네이티브 크래시 인과는 `UNPROVEN` | 각 파일을 현재 RT56 기준으로 재기반화한 뒤 해당 오류군이 사라지는지 비교 |
| RT56 1.19.2 자체의 graphic/enum 오류만으로 크래시한다 | `UNPROVEN` | HOK를 제외한 RT56 + RT56 Korean Translation 대조 실행 |
| 마지막 setup 항목인 `r56_warlord_plan.txt`가 원인이다 | `UNPROVEN`; 직접 증거 없음 | 직전·직후 로더 증거 또는 최소 재현 필요 |
| GPU, 마이크 미감지 또는 표시된 드라이버 버전 `0.0.0.0`이 원인이다 | 현재 증거로 지지되지 않음 | vanilla 및 RT56 대조 실행과 실제 드라이버 상태 비교 필요 |

네이티브 스택이 원인 파일을 특정하지 못하므로, 어떤 단일 오류도 `ACCESS_VIOLATION`의 직접 원인이라고 `CONFIRMED`로 올리지 않는다.

## 7. 권장 수정 및 검증 순서 — 미실행

1. 다음 실행 전에 현재 로그와 크래시 폴더를 실행 ID별로 보존한다. 복사 위치와 보존 작업은 별도 승인을 받는다.
2. `RT56 + RT56 Korean Translation`만 활성화한 대조군을 전체 프로세스 재시작으로 실행한다.
3. 현재 RT56 map을 기준으로 HOK의 한국 지역 변경만 재적용하는 지도 병합 계획을 만든다.
4. `definition.csv`와 `provinces.bmp`뿐 아니라 state, strategic region, adjacency, buildings, unit positions, supply 및 railway를 함께 감사한다.
5. HOK의 동일경로 전체 파일을 현재 RT56 버전으로 재기반화하고, 가능한 경우 HOK 전용 델타만 남긴다.
   - `00_generic_organization.txt`
   - `unit_medals_scripted_triggers.txt`
   - `the_gathering_storm.txt`
   - `china_shared_TSR.txt`
6. HOK 고유 항공기 graphic 참조와 RT56 한국 음성 ID 중복을 별도 GFX/audio 작업으로 분리한다.
7. 각 수정 후 최초 오류군부터 다시 확인하고, 오류가 줄었다는 사실만으로 완료 처리하지 않는다.
8. 최종적으로 메인 메뉴, 새 게임, 한국 국가 상태, focus, decisions, OOB, map, supply, unpause를 확인한다.
9. save 및 multiplayer 호환성을 주장하려면 별도의 save round-trip과 checksum/OOS 검증을 수행한다.

지도 작업은 고위험 작업이다. `definition.csv` 행 추가, 프로빈스 ID 일괄 치환, RT56 전체 map 폴더 복사 또는 broad `replace_path` 추가를 임시 처방으로 사용하지 않는다.

## 8. 실제 수행한 검증

- 로그와 크래시 폴더의 시각 및 SHA-256 대응 확인
- 실제 게임 버전과 크래시 예외 확인
- 활성 모드 목록과 launcher `.mod`의 실제 경로 확인
- HOK와 RT56 `definition.csv`의 프로빈스 ID 범위 비교
- 87개 malformed province ID가 `13448`~`13534`의 완전한 연속 범위임을 확인
- 오류가 가리킨 HOK/RT56 동일경로 파일과 정의 존재 여부 비교
- `setup.log`에서 HOK와 RT56 데이터베이스 항목이 모두 발견·등록된 흔적 확인
- 비활성 descriptor 경고와 활성 플레이셋 오류 분리

## 9. 미검증 범위와 남은 위험

- RT56 단독 대조 실행
- HOK 포함 재현 실행
- 수정 후 로그 비교
- 정확한 DLC 보유·활성 조합
- launcher가 계산한 최종 mod checksum
- 메인 메뉴 및 한국 새 게임 진입
- 모든 affected state의 지도 표시와 supply/railway
- focus, decision, event 및 AI 런타임 동작
- 기존 save 호환성
- multiplayer checksum 및 OOS
- HOK localisation과 `Korean Language` 의존 계약

## 10. 변경 상태

이 사건 문서만 새로 작성했다. 게임 데이터, HOK 프로덕션 파일, Steam Workshop 파일, 로그, 세이브 및 launcher 설정은 변경하지 않았다. 게임 실행, commit, push 및 배포도 수행하지 않았다.
