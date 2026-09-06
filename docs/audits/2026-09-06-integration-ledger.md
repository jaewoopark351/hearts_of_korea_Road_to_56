# 2026-09-06 통합 원장 요약

> 상태: donor 1,014개 전수 분류 및 정적 산출물 확인 완료 / 런타임 충돌 감사 미완료

이 문서는 HOK donor production/root 파일을 새 RT56 호환 포트에서 누가 소유하고 어떻게 처리했는지 요약한다. 행별 근거는 [production 파일 분류 CSV](2026-09-06-production-file-classification.csv)가 정본이며, 이 요약만으로 게임 호환을 증명하지 않는다.

## 1. 원장 범위와 재현 조건

- donor root: `C:\hoi\hearts_of_korea`
- donor Git: `main@887930f6e88c80568d62dab9cfbe1ba8a498a252`
- 제외한 donor 영역: `.git/`, `docs/`
- 분류한 production/root 파일: 1,014개
- RT56 root: `C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968`
- RT56 Workshop item/manifest: `820260968` / `3323396725579032799`
- RT56 descriptor SHA-256: `5B323861ABD63E31CB896277E3EA58BA4BCD9FCEEDA957B50792065E42E03F61`
- exact-relative-path RT56 충돌: 73개
- 생성기: `tools/build_integration_manifest.py`

생성기는 donor 파일 수가 1,014개가 아니거나 exact-path 충돌 수가 73개가 아니면 실패한다. 또한 73개 충돌 모두에 명시 규칙을 요구하므로, 충돌 파일이 binary/text 기본 규칙으로 조용히 분류될 수 없다. 각 CSV 행은 `source_path`, 통합 분류, 상태, exact-path 충돌 여부, 산출 경로, 이유, donor SHA-256과 output/host SHA-256을 기록한다.

## 2. 분류 집계

| 분류 | 수 | 의미 |
|---|---:|---|
| `ADD` | 119 | RT56과 같은 경로가 없는 HOK 고유 text/metadata를 호환 모드에 유지 |
| `ASSET_COPY` | 776 | 출처를 유지해야 하는 HOK 고유 binary asset 또는 의도적인 HOK 한국 자산 |
| `BINARY_MERGE` | 18 | RT56 전역 지도 기반에 검토한 HOK 한국 delta를 합성 |
| `OVERRIDE` | 7 | 호환 모드가 명시적으로 소유하는 한국 정의 또는 프로젝트 metadata |
| `THREE_WAY_MERGE` | 31 | current host base와 HOK donor 의도를 정의/ID 단위로 병합 |
| `USE_RT56` | 63 | donor 파일을 싣지 않고 RT56/vanilla 소유를 유지하거나 범위 밖 콘텐츠를 제외 |
| **합계** | **1,014** | 모든 donor production/root 파일에 정확히 한 분류 적용 |

산출 상태는 분류 의도와 별도로 다음처럼 집계된다.

| 상태 | 수 | 의미 |
|---|---:|---|
| `SHIPPED` | 902 | 같은 경로 또는 명시한 포트 경로에 포함 |
| `GENERATED` | 49 | `BINARY_MERGE` 또는 `THREE_WAY_MERGE` 산출물로 포함 |
| `OMITTED_HOST_OWNED` | 7 | 호환 모드에서는 제외하고 실제 RT56 파일의 hash를 원장에 기록 |
| `OMITTED_OUT_OF_SCOPE` | 56 | RT56 파일이 따로 없더라도 한국 전용 포트 범위에서 제외 |
| **합계** | **1,014** | donor 행 전체 |

## 3. 73개 exact-path 충돌 처리

| 처리 | 수 | 설명 |
|---|---:|---|
| `ASSET_COPY / SHIPPED` | 31 | HOK 한국 국기, 음성 WAV, 항공기 diffuse와 thumbnail을 명시적으로 선택 |
| `BINARY_MERGE / GENERATED` | 10 | 7개 전역 지도 파일과 같은 경로 state 525/527/528 재생성 |
| `OVERRIDE / SHIPPED` | 6 | HOK 한국 idea/focus/history, branding 및 프로젝트 metadata의 명시 소유 |
| `THREE_WAY_MERGE / GENERATED` | 19 | 공용·KOR·동아시아 파일을 host base와 병합 |
| `USE_RT56 / OMITTED_HOST_OWNED` | 7 | 난이도, on_action, OOB, loading screen과 비한국 MON history/name을 RT56에 위임 |
| **합계** | **73** | default 규칙 미사용 |

Exact-path 73개는 물리 파일명 충돌만 센 값이다. 서로 다른 파일에서 같은 event, focus, idea, character, MIO, GFX 또는 localisation key를 선언하는 논리 충돌은 별도 정적 ID 검사와 builder assertion으로 다뤘으며, 런타임 등록 순서 검증은 아직 남아 있다.

## 4. 핵심 소유권 결정

| 영역 | 소유자/기준 | 통합 결정 |
|---|---|---|
| 전 세계 지도 | RT56 | RT56 definition/bitmap/world references 보존, 한국 delta만 합성 |
| 한국 province/state 설계 | compat에서 이식한 HOK delta | province `13535-13568`, state `917-920`, `1144-1147` 매핑 사용 |
| broad state/strategic-region replace | RT56 | compat descriptor에는 `replace_path`를 추가하지 않음 |
| 공용 난이도와 MTG on_action | RT56 | 낡은 donor whole file을 싣지 않음 |
| generic MIO, 훈장 trigger, bookmark, generic advisor | RT56/vanilla base + HOK delta | current base에 필요한 KOR 레코드·조건만 병합 |
| 중국/일본 공유 이벤트·결정·on_action | RT56 base + HOK delta | current 동아시아 콘텐츠를 보존하며 한국 state/독립 흐름만 병합 |
| 일본 OOB와 SOV/USA peace AI | current vanilla base + HOK Korea delta | RT56 파일이 없는 현재 schema base에 한국 관련 변경만 적용 |
| KOR focus, idea, 1936 history | HOK | 충돌 없는 HOK 논리 ID를 유지하고 map/doctrine만 현재 체계로 이전 |
| KOR character, AI, MIO, division/ship names | HOK + RT56 | 양쪽 한국 정의를 ID별로 병합 |
| 한국 음성 | HOK payload + 단일 merged registry | WAV 18개는 donor bytes, RT56 category/compressor에 HOK 재생 목록·volume 병합 |
| 한국 항공기 자산 | HOK payload + 호환 고유 registry ID | HOK 기본/고유 mesh·texture 유지, 충돌하는 기본 mesh/entity는 `hok_rt56_` ID로 소비 |
| HOK 한국 국기와 branding | HOK | provenance-bearing 시각 자산으로 의도적 override/copy |
| FIN/MON/SIB 도전 모듈 | 범위 밖 | 한국 전용 포트에서 규칙·script·localisation·고아 그림까지 제외 |
| localisation dependency | Pending Runtime | compat 자체 `l_english`/`l_korean`은 유지하되 외부 번역 모드 계약은 미확정 |
| runtime dependency | RT56 + 현재 선언된 Korean Language | donor 비활성; 최종 localisation 조합은 Pending Runtime |

## 5. Generated 산출물 49개

### 5.1 `BINARY_MERGE` 18개

`tools/build_rt56_map.py`가 다음을 생성한다.

- 전역 map 7개: `definition.csv`, `provinces.bmp`, `buildings.txt`, `railways.txt`, `supply_nodes.txt`, `unitstacks.txt`, `strategicregions/186-Korea.txt`
- state 11개: `525`, `527`, `528`, `917`, `918`, `919`, `920`, `1144`, `1145`, `1146`, `1147`

기존 donor state `1028-1031`, `1082-1085`는 새 산출 경로로 대응되며 호환 모드에서 과거 파일명/ID를 싣지 않는다.

후속 buildings 감사에서 donor-vs-바닐라 차집합만으로는 RT56에서 제거된 vanilla-identical 항구 배치를 보존할 수 없음을 확인했다. 현재 생성기는 합성 HOK 해안에 필요한 `naval_base_spawn` 7행만 별도 복원하고, pinned RT56보다 새 coastal-without-spawn이 생기지 않는지 좌표 기반으로 검사한다. 상세 근거와 출력 hash는 [한국 해안 항구 배치 closure 보정](../implementation/2026-09-06-map-building-closure-fix.md)에 기록한다.

### 5.2 `THREE_WAY_MERGE` 31개

생성·병합 경로는 다음 묶음이다.

- 공용 10개: bookmark, 색상, cosmetic, 이름, 정보기관, generic MIO, 훈장 trigger, 특수 프로젝트 effect, KOR 결정, generic advisor
- 동아시아 donor 대응 13개: 일본 trigger/결정/history, 세 이벤트 파일, 중국 공유 중점, SEA on_action, 일본 OOB 3개, SOV/USA peace AI
- KOR 및 자산 8개: KOR character, Hanjin MIO, KOR division/ship names, HOK plane asset/entity/graphic DB, 단일 한국 음성 registry

`tools/build_korean_assets.py`는 donor `sound/voice_korea.asset` 행에서 `sound/r56_vo_Korean.asset`을 생성하고, HOK WAV 18개와 기본 항공기 mesh/texture를 donor bytes로 관리한다. 항공 mesh/entity와 HOK graphic DB도 충돌 없는 `hok_rt56_` ID로 함께 생성한다.

`tools/build_east_asia_overrides.py`는 위 donor 대응 행 외에도 host 보존을 위해 `events/WTT_PRC.txt`, `events/r56_japan.txt`를 출력하고, HOK 일본 전용 추가 결정은 `common/decisions/HOK_RT56_JAP.txt`로 분리한다. 이 세 파일은 donor 1,014행의 일대일 source row가 아니라 병합 구현에 필요한 host/additive 지원 산출물이다.

## 6. `USE_RT56` 63개 상세 원칙

### `OMITTED_HOST_OWNED` 7개

- `common/difficulty_settings/00_difficulty.txt`
- `common/on_actions/04_mtg_on_actions.txt`
- donor의 낡은 `history/units/JAP_1936_naval.txt`
- RT56 shared loading screen 2개
- RT56의 MON country history와 division names 2개

### `OMITTED_OUT_OF_SCOPE` 56개

- FIN AI/on_action 도전 모듈
- MON character/history/on_action/division names와 결정 그림
- SIB 도전 on_action
- 호출되지 않는 일본 news 그림 4개
- 제거된 FIN `newsk.27`의 고아 그림 1개
- runtime 참조가 없는 일본 공화국 cosmetic flag 9개
- 제거된 일본 경로에만 쓰이던 focus 10개, idea 2개, event 그림 2개와 결정 그림 1개
- 소비자가 없는 HOK 대일무역 focus 그림 1개와 한일회담 event 그림 1개
- 연결 정의가 없는 일본 portrait asset 16개
- 연결되지 않은 RAJ cosmetic flag 1개와 현행 song 목록에 등록되지 않은 일본 민주화 테마 음악 1개

`Minshu_ikki`는 donor `hok_music.asset`에는 정의되지만 현행 `hok_songs.txt`에는 등록되지 않는다. donor commit `b3ec30e`가 제거한 song 조건은 `JAP_proclaim_the_republic` 완료뿐이었고, 같은 이름의 `KOR_minshu_ikki` focus에도 음악 재생 효과가 없다. 따라서 현재 원장은 삭제된 HOK JAP 경로의 고아 곡으로 보고 계속 범위 밖으로 둔다. 다만 물리 OGG가 20:13:59에 작업 트리에 다시 나타나 Korea-only pruning 검사 1건을 실패시킨다. 동시 사용자 변경과 새 HOK 보존 원칙 사이의 선택이 필요해 자동 삭제하지 않았다.

파일만 삭제한 것이 아니라 관련 game rule, event, sprite, 일본 trait 2개와 localisation 참조도 함께 제거했으며, aggregate validator는 폐기 token이 활성 script에 남지 않는지 검사한다.

## 7. 분류 원장 밖의 교차 파일 수정

CSV는 donor 파일 한 행이 호환 산출물에서 어떤 운명을 갖는지 설명한다. 다음 작업은 해당 행의 output hash에는 반영되지만 분류 이름만으로는 의미가 충분히 드러나지 않으므로 별도로 기록한다.

- `tools/migrate_hok_ids.py`: 숫자 state/province 참조, `kor_events` casing, achievement 그룹, event picture, PHI cosmetic localisation
- `tools/migrate_doctrines.py`: KOR/KCH/KJP/RKY/TWN history의 현재 grand/sub-doctrine migration과 KOR 폐기 수송기 기술 할당 제거
- `tools/build_korean_assets.py`: HOK WAV·기본 항공기 payload, 단일 음성 registry와 고유 mesh/entity 소비 경로 생성
- `tools/prune_non_korean_content.py`: 범위 외 정의와 orphan 참조의 폐쇄
- KOR character/AI/MIO/name의 수동 검토 three-way merge

특히 `PHI_free`는 KOR 결정에서 도달 가능하므로 영어와 한국어에 `PHI_free_democratic`, `_DEF`, `_ADJ`를 각각 추가했다. 반대로 제거한 MON 모듈의 기본 몽골 국명 override 8개, runtime 참조가 없는 일본 공화국 cosmetic 9개, RAJ cosmetic 1개와 미등록 일본 음악 1개는 양 locale에서 삭제했다. 정적 localisation 집계는 이 수정 후 36개 파일, 3,614개 key다.

## 8. 검증 결과와 한계

`python tools\validate_port.py`의 후속 결과는 `15 PASS / 0 WARNING / 1 ERROR`다. 한국 자산, manifest, source pin, 지도 closure, script 구조, descriptor 정책, 폐기 token, localisation, event picture와 주요 논리 ID 검사는 통과했다. 유일한 오류는 위 `music/Minshu_ikki.ogg`의 Korea-only pruning 위반이다.

최신 로그는 2026-09-06 21:30 C0 실행이며, 번역 없이도 21:28 비한국 국가와 21:30 KOR가 같은 접근 위반 stack으로 실패했다. 이 실행들은 한국 자산·기술 보정 뒤지만 항구 배치 closure 보정 전 산출물이다. 다음은 원장 또는 정적 validator가 증명하지 않는다.

- 외부 launcher `.mod`가 현재 descriptor와 일치하는지
- 실제 load order와 물리 파일 discovery
- HOI4 parser/database 등록과 scope 평가
- 한국 새 게임, 지도 진입과 unpause
- localisation mod의 `replace_path` 아래 실제 UI 문자열
- DLC 분기, AI, save, multiplayer checksum
- RT56 단독 대비 신규 fatal·반복 오류가 없는지

외부 launcher `.mod`와 저장소 descriptor는 현재 모두 RT56과 `Korean Language`를 선언하지만, 19:20 실제 플레이세트는 대신 RT56 Korean Translation을 사용했다. 이를 해결하고 donor를 비활성화한 playset에서 런타임 대조군을 확보하기 전에는 이 원장을 “RT56 호환 완료”의 근거로 사용해서는 안 된다.

## 9. Git 및 외부 상태

- 원장과 구현은 `main@70aaba43a98fd429378ec1a67d4398f16330e101` 위의 미커밋 변경 집합이다.
- donor, RT56, vanilla, 로그, launcher 파일은 수정하지 않았다.
- 게임 실행, 로그 갱신, commit, push, tag, 배포와 Workshop 작업은 수행하지 않았다.
