# 2026-09-06 1차 포팅 구현 배치

> 상태: **정적 구현 및 정적 검증 완료 / HOI4 런타임 미검증**
>
> 이 문서는 호환 완료 선언이 아니다. 최신 런타임 증거는 구현 전인 2026-09-06 14:06 실행뿐이며, 구현 후 게임 실행은 없었다.
>
> 후속 상태: 한국 음성·기본 항공기 소유권과 KOR 기술 보정은 [한국 우선 자산·KOR 기술 보정](2026-09-06-korea-first-assets-and-kor-tech.md)에 기록한다. 아래 수치와 자산 결정은 1차 배치 당시 스냅샷이다.
>
> 후속 정정: 이 배치의 buildings 정적 closure는 해안 좌표 coverage를 검사하지 않았다. 발견된 항구 spawn 7행 누락과 새 회귀 gate는 [한국 해안 항구 배치 closure 보정](2026-09-06-map-building-closure-fix.md)에 기록한다. 아래 당시 `15 PASS`는 소급 변경하지 않는다.

## 1. 범위

이번 배치는 기존 HOK 폴더를 RT56과 함께 켜는 방식이 아니라, 현재 RT56을 호스트로 삼고 HOK의 의도된 한국 콘텐츠만 이 저장소에 이식하는 독립 호환 포트를 구현했다.

허용되고 수행한 범위:

- HOK donor, RT56 Workshop snapshot, 설치된 HOI4 파일과 기존 로그의 읽기 전용 조사
- RT56 기반 한국 지도 합성 및 province/state 참조 이전
- 공용 파일, 동아시아 공유 파일, 한국 국가 데이터의 감사된 병합
- HOK/RT56 중복 자산의 소유권 정리
- 현재 HOI4 1.19 교리 체계로 국가 history의 낡은 교리 선언 이전
- 누락 localisation과 도달 가능한 이벤트·그림 참조의 정적 폐쇄
- 1,014개 donor production/root 파일의 전수 분류 원장 생성
- 재현 가능한 생성·정리·검증 도구 추가와 정적 검증

수행하지 않은 범위:

- HOI4 또는 Nudger 실행
- launcher playset, 외부 `.mod`, 로그, 저장 파일, Workshop 또는 게임 설치 폴더 수정
- 런타임 로드, 새 게임, unpause, UI localisation, DLC, 세이브, AI 또는 멀티플레이 검증
- Git commit, push, tag, 배포 또는 Workshop 업로드

## 2. 기준선

| 항목 | 고정한 상태 |
|---|---|
| 호환 저장소 | `main@70aaba43a98fd429378ec1a67d4398f16330e101` 위의 미커밋 구현 변경 집합 |
| HOK donor | `C:\hoi\hearts_of_korea`, `main@887930f6e88c80568d62dab9cfbe1ba8a498a252`, 읽기 전용 |
| HOK donor 정체성 | descriptor의 revision item `3793992662`; 역사적 item `2898629778`과 구분 |
| RT56 | Workshop item `820260968`, manifest `3323396725579032799` |
| RT56 descriptor | SHA-256 `5B323861ABD63E31CB896277E3EA58BA4BCD9FCEEDA957B50792065E42E03F61` |
| 대상 엔진 증거 | HOI4 `1.19.2.0.a729`, Steam build ID `23969257` |
| 최신 로그 | 2026-09-06 14:06 실행; `setup.log`의 마지막 기록은 14:06:19 |

저장소의 `descriptor.mod`는 개발판 `0.1.0-dev`, `supported_version="1.19.*"`, 필수 dependency `The Road to 56`만 선언한다. `path`, `replace_path`, `remote_file_id`는 없다. `supported_version`은 호환 증명이 아니라 대상 선언일 뿐이다.

외부 launcher 파일 `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV\mod\hearts_of_korea_Road_to_56.mod`는 여전히 과거 이름·버전과 `Korean Language`만 선언한다. 따라서 launcher가 현재 저장소 descriptor와 같은 구성 및 물리 경로를 실제로 로드한다는 증거가 없으며, 이 파일이 재생성 또는 별도 승인된 갱신을 거치기 전에는 C0/C1 런타임 검증을 유효하다고 볼 수 없다.

## 3. 근거와 원인 분류

### CONFIRMED — 지도 기반 불일치

- donor `definition.csv`는 province `13447`에서 끝나지만 RT56은 `13534`까지 사용한다.
- donor 지도를 그대로 로드하면 RT56 state가 참조하는 `13448-13534` 87개 province가 정의되지 않는다.
- donor가 추가한 `13414-13447` 34개 province ID는 현재 RT56에서 서로 다른 전 세계 province가 이미 모두 사용한다.
- donor state `1028-1031`, `1082-1085`도 RT56이 서로 다른 지역에 사용한다.
- 구현 전 14:06 로그의 `Malformed token` 및 후속 state/map 오류는 이 불일치와 일치한다.

### CONFIRMED — 낡은 whole-file shadow와 중복 소유권

donor 복사본의 bookmark, generic MIO, 훈장 trigger, 공용 on_action, 중국 공유 중점, 일본 이벤트/history, 난이도·정보기관·advisor·색상 파일이 현재 RT56/vanilla 정의를 가리거나 중복시켰다. 음성 ID, 한국 항공기 entity/attachment와 일부 shared asset도 양쪽이 동시에 소유하고 있었다.

### CONFIRMED — 1.19 교리 schema 불일치

`KOR`, `KCH`, `KJP`, `RKY`, `TWN` 국가 history의 `set_technology` 안에 현재 체계에서 교리 기술로 쓰지 않는 과거 ID가 남아 있었다. 현재 vanilla와 RT56 정의 및 vanilla 독일 history의 전환 예를 기준으로 교리 루트와 1939 진척을 별도 명령으로 이전했다.

### CONFIRMED — 도달 가능한 PHI cosmetic localisation 누락

`common/decisions/KOR_decision.txt`가 `PHI_free` cosmetic tag를 실제로 설정하지만, `PHI_free_democratic`, `_DEF`, `_ADJ`가 없었다. 영어와 한국어에 각각 세 키를 추가했다.

### UNPROVEN — 구현 후 엔진 결과

위 원인은 소스와 구현 전 로그로 확인했지만, 수정된 포트를 엔진이 발견·파싱·등록하고 의도한 동작을 실행하는지는 아직 확인하지 않았다. 특히 RT56 단독에서도 발생할 수 있는 항공기 graphic DB 오류는 대조 실행 전까지 이 포트의 회귀로 분류할 수 없다.

## 4. 변경 사항

### 4.1 지도와 persistent ID

`tools/build_rt56_map.py`가 고정한 RT56 지도 위에 검토한 HOK 한국 delta를 합성한다.

- province `13414-13447`을 `13535-13568`로 1:1 이전
- RT56 `definition.csv`의 기존 `0-13534` 행 보존 후 새 34행 추가
- vanilla 대비 HOK 한국 지형 차이 1,889 pixel을 RT56 `provinces.bmp`에 합성
- province `4126`, `7125`, `7175`, `7204`, `10065`의 HOK coastal 속성 반영
- 7개 전역 지도 파일과 11개 state 파일, 총 18개 `BINARY_MERGE` 산출물 생성
- buildings, victory points, railways, supply nodes, strategic region, unit stacks와 스크립트/OOB 참조를 같은 매핑으로 폐쇄
- donor에는 별도 adjacency delta 파일이 없으므로 RT56/vanilla adjacency를 상속

State 매핑은 다음과 같다.

| donor | compat | 지역 |
|---:|---:|---|
| 1028 | 918 | 함경 |
| 1029 | 1144 | 강원 |
| 1030 | 920 | 경상 |
| 1031 | 1145 | 충청 |
| 1082 | 919 | 전라 |
| 1083 | 917 | 황해 |
| 1084 | 1146 | 제주 |
| 1085 | 1147 | 쓰시마 |

`525`, `527`, `528`은 ID를 유지하되 RT56 기반으로 한국 분할과 쓰시마 분리를 재구축했다. 이 숫자 이전은 기존 HOK 세이브 및 해당 숫자를 직접 참조하는 제3자 submod와 호환되지 않을 수 있으므로, 현재 포트 정책은 **새 게임 전용**이다. 상세 결정은 [ADR-0002](../decisions/0002-map-id-migration.md)를 따른다.

### 4.2 공용 database와 동아시아 공유 콘텐츠

`tools/build_shared_overrides.py`는 공용 전체 파일을 donor 상태로 유지하지 않고 다음 원칙을 적용한다.

- 색상, cosmetic 색상, 이름 pool, 정보기관은 `zz_hok_rt56_*` additive 파일로 HOK 레코드만 분리
- generic MIO, 훈장 trigger, bookmark, 특수 프로젝트 scripted effect, KOR 결정, generic advisor는 현재 RT56 또는 vanilla 기반에 필요한 KOR delta만 병합
- 낡은 donor 난이도 전체 파일은 싣지 않고 RT56이 소유

`tools/build_east_asia_overrides.py`는 일본·중국 공유 파일과 평화회담 AI를 현재 RT56/vanilla 기반으로 재생성한다.

- `WTT_Japan`, `SEA_Japan`, `ElectionEvents`, `WTT_PRC`, `r56_japan`
- 일본 결정, HOK 일본 관련 추가 결정, 일본 scripted trigger
- `china_shared_TSR`, `14_sea_on_actions`
- 일본 country history와 1936 일반/NSB/legacy naval OOB
- SOV/USA peace AI의 전체 한국 state 집합

독립한 1936년 한국을 유지하기 위해 일본 지상 부대의 donor 배치를 센다이·고베·쓰시마 쪽으로 재배치했으며, RT56의 다른 세계 콘텐츠는 해당 파일의 host base에서 유지했다.

### 4.3 한국 콘텐츠의 논리 병합

- HOK의 Syngman Rhee 정의와 현재 RT56의 Yi Un, Kim Il-sung, Pak Hon-yong 정의를 `common/characters/KOR.txt`에 병합
- RT56의 Yi Kang을 HOK `KOR_constitutional_monarchy` 흐름에 연결
- RT56 KOR AI 전략을 HOK의 `KOR_Gu_Kim`과 중립/민주 정부 조건에 맞춘 `common/ai_strategy/r56_KOR.txt`로 이식
- Hanjin MIO에 HOK의 일반 항공 설계와 RT56의 KOR/NKR 소유·state 525 조건을 병합
- HOK 사단명/함명과 RT56 `KOR_MOT_01` 및 함종 그룹을 함께 유지하고 참조 대소문자를 정리
- HOK 한국 focus, idea와 1936 국가 history는 의도적인 HOK 소유 영역으로 유지하되, 숫자 ID와 1.19 교리 참조를 이전

### 4.4 이벤트, ID, localisation

`tools/migrate_hok_ids.py`가 19개 HOK-owned 파일의 state/province 참조와 검토한 후속 수정을 재현한다.

- 이벤트 namespace와 ID 호출의 `KOR_events`/`kor_events` 대소문자를 `kor_events`로 통일
- 호출되지 않고 localisation·그림이 없던 `kor_events.44` 제거
- 빈 그림을 사용하던 `kor_events.51`, `.55`에 유효한 vanilla report-event 그림 연결
- 과거 Workshop ID를 포함한 achievement 그룹을 `hok_rt56_achievements`로 이전
- 도달 가능한 `PHI_free_democratic`, `_DEF`, `_ADJ`를 영어·한국어에 각각 추가

정적 localisation 결과는 36개 파일, 3,614개 key이며 BOM, locale header와 저장소 내부 중복 검사를 통과했다. 제거한 MON 모듈이 기본 몽골 국명을 덮어쓰던 8개 키도 양 locale에서 제거해 RT56 소유권으로 돌렸고, runtime 참조가 없는 일본 공화국 cosmetic 9개, RAJ cosmetic 1개와 미등록 일본 음악 1개도 양 locale에서 제거했다. 다만 `Korean Language`와 `The Road to 56 Korean Translation` 중 어떤 조합을 공식 지원할지는 [ADR-0003](../decisions/0003-localisation-contract.md)의 런타임 매트릭스를 통과하기 전까지 보류한다.

### 4.5 교리 이전

`tools/migrate_doctrines.py`는 고정한 donor country history와 현재 vanilla/RT56 교리 정의를 함께 검사한 뒤 다음을 생성한다.

- KOR: `superior_firepower`, `new_convoy_raiding`, `new_battlefield_support` grand doctrine 설정
- KCH/KJP/RKY/TWN: `new_mobile_warfare`, `new_convoy_raiding`, `new_battlefield_support` grand doctrine 설정
- 네 분리 태그의 1939 진척: `set_sub_doctrine`와 `add_mastery`로 mobile infantry, mission type tactics, mobile recon/assault, fighter tactical flexibility, dive bomber 진척 이전
- 과거 교리 ID가 `set_technology` 안에 남지 않는지 검사

이는 현재 데이터 정의와 vanilla 전환 예에 맞춘 정적 migration이며, 실제 시작 보너스와 AI 체감이 donor 의도와 동등한지는 런타임에서 별도로 검증해야 한다.

### 4.6 GFX, 음성과 범위 정리

- 한국 음성의 단일 소유자를 RT56으로 정하고 donor `voice_korea.asset`과 중복 WAV 18개를 호환 모드에서 제외
- RT56과 겹치는 한국 공용 항공기 texture/entity/attachment를 제외하고 HOK 고유 초음속기·모함·헬리콥터 자산만 유지
- 삭제된 `supersonic_fighter_equipment_1` 참조를 현재 HOK 고유 `jet_fighter_equipment_x`로 이전
- 한국 포트 범위를 벗어난 FIN/MON/SIB 도전 모듈, 연결된 규칙·on_action·localisation·그림을 제거
- 호출되지 않는 일본 전용 `newsj.1-4` 이벤트와 고아 그림을 제거
- runtime 참조가 없는 일본 공화국 cosmetic localisation 9개와 flag 9개를 제거
- 제거된 일본 경로에만 속한 focus 그림 10개, idea 그림 2개, event 그림 2개, 결정 그림 1개와 연결되지 않은 일본 portrait 16개·trait 2개를 제거
- 소비자가 없는 HOK 대일무역 focus 그림 1개와 한일회담 event 그림 1개를 제거
- 연결되지 않은 RAJ cosmetic flag 1개와 song 등록이 없는 `Minshu_ikki` 음악·localisation을 제거
- 남아 있는 Ragnarok 흐름의 누락된 `hokRagnarok.7` 영어·한국어 문자열을 추가

### 4.7 descriptor와 전체 분류

저장소 descriptor는 RT56만 필수 dependency로 선언하며 HOK donor를 dependency로 요구하지 않는다. broad `replace_path`나 어떤 source Workshop ID도 승계하지 않는다.

donor의 production/root 파일 1,014개는 다음과 같이 전부 분류했다.

| 분류 | 수 |
|---|---:|
| `ADD` | 119 |
| `ASSET_COPY` | 755 |
| `BINARY_MERGE` | 18 |
| `OVERRIDE` | 7 |
| `THREE_WAY_MERGE` | 30 |
| `USE_RT56` | 85 |
| **합계** | **1,014** |

세부 출처·산출 경로·분류 이유·donor/output SHA-256은 [1,014행 production 파일 분류 CSV](../audits/2026-09-06-production-file-classification.csv)에 있으며, 집계와 소유권 해설은 [통합 원장 요약](../audits/2026-09-06-integration-ledger.md)에 있다. 현재 RT56과 같은 상대 경로인 73개는 모두 명시 규칙으로 분류했으며, default `ADD`/`ASSET_COPY`에 맡기지 않았다.

## 5. 생성·검증 도구

| 도구 | 역할 |
|---|---|
| `tools/build_rt56_map.py` | 고정한 RT56 지도 위에 HOK 한국 delta와 전체 참조 closure 합성 |
| `tools/build_shared_overrides.py` | 공용 database의 RT56/vanilla rebase 및 additive HOK 레코드 생성 |
| `tools/build_east_asia_overrides.py` | 동아시아 이벤트·결정·history·OOB·평화 AI의 host 기반 병합 |
| `tools/migrate_hok_ids.py` | HOK-owned numeric 참조, 이벤트/achievement ID와 PHI localisation 이전 |
| `tools/migrate_doctrines.py` | 5개 country history의 1.19 교리 이전 |
| `tools/prune_rt56_owned_files.py` | RT56 소유 파일 27개가 호환 모드에 남지 않는지 적용·검사 |
| `tools/prune_non_korean_content.py` | 범위 외 모듈과 그 고아 참조·자산 제거 |
| `tools/build_integration_manifest.py` | donor 1,014개와 exact-path 충돌 73개의 전수 분류 CSV 재현 |
| `tools/validate_port.py` | 위 도구와 구조·descriptor·ID·localisation closure의 aggregate 정적 gate |

지도·공용·동아시아·교리 builder는 사용한 donor/RT56/vanilla 입력의 SHA-256을 고정한다. 나머지 migration/pruning/manifest 도구는 대상 집합과 산출 상태를 검사한다. Workshop 또는 설치 파일의 고정 입력이 달라지면 관련 builder는 조용히 새 결과를 만들지 않고 source drift로 실패하도록 했다.

## 6. 동작 영향

보존하려는 동작:

- RT56의 전 세계 지도, 공용 시스템과 비한국 콘텐츠
- HOK의 한국 국가 정체성, focus, idea, 인물, 결정, 이벤트, 고유 자산과 한국 지역 설계
- 기존 HOK 논리 ID는 RT56과 충돌하지 않는 한 유지

의도적으로 달라진 동작 또는 소유권:

- 충돌한 HOK province/state numeric ID는 ADR-0002 매핑으로 변경
- 1936 일본 OOB의 한국 주둔 부대는 독립 한국을 위해 일본 본토/쓰시마로 이동
- 공용 한국 음성은 RT56이 소유
- FIN/MON/SIB 선택 도전 콘텐츠와 호출되지 않는 일본 news 이벤트는 한국 전용 포트에서 제외
- 과거 교리 기술은 현재 grand/sub-doctrine 모델로 이전

따라서 기존 HOK 세이브 호환, 제3자 submod의 숫자 참조 호환, 과거 checksum 동일성은 주장하지 않는다.

## 7. 정적 검증

2026-09-06 현재 `python tools\validate_port.py` 결과:

- `15 PASS / 0 WARNING / 0 ERROR`
- 지도 합성, 공용 override, 동아시아 override, RT56-owned pruning, 한국 범위 pruning 재현성 통과
- HOK ID 및 교리 migration, 1,014행 integration manifest 재현성 통과
- UTF-8 Paradox Script 132개 brace/quote 구조 통과
- descriptor가 RT56-only dependency이고 `path`/`replace_path`/`remote_file_id`가 없음
- 폐기한 ID와 모듈의 활성 token 없음
- localisation 36개, 3,614개 key의 BOM/header/중복 검사 통과
- HOK 이벤트의 영어·한국어 localisation과 picture 참조 폐쇄 통과
- state/event/focus/tree/character/MIO/achievement 논리 ID 검사 통과
- 필수 KOR 병합 assertion 통과

이 결과는 텍스트·바이너리 산출물이 고정 입력에서 재현되고, 구현한 정적 invariant를 만족한다는 뜻이다. 엔진 parser, database 등록, 실제 scope 평가와 UI 렌더링을 증명하지 않는다.

## 8. 남은 위험과 다음 gate

가장 먼저 해결해야 할 blocker는 외부 launcher `.mod`와 저장소 descriptor의 불일치다. 그 다음 사용자에게 별도 런타임 실행 권한이 있는 범위에서 다음을 새 프로세스로 검증해야 한다.

1. RT56 단독 대조군과 로그 기준선
2. RT56 + 선택 localisation 대조군
3. RT56 + compat, HOK donor 비활성 상태의 C0
4. 최종 localisation 조합의 C1-KL 또는 C1-RTK
5. 한국 선택, 새 게임 진입, 지도 표시와 unpause
6. 정부·법·idea·focus·결정·이벤트·OOB·장비·인물·초상화
7. 한국 state의 인접성, 해안, 철도, 보급, unit 위치
8. 로그 증가량과 RT56-only 대비 신규 fatal/반복 오류
9. 필요한 DLC 분기, AI 경로, save round trip과 멀티플레이 checksum

최신 로그는 여전히 구현 전 14:06 실행이므로, 현재 `error.log`의 감소나 크래시 해소를 이번 구현의 결과라고 주장할 수 없다.

## 9. Git 상태

- 기준 commit: `70aaba43a98fd429378ec1a67d4398f16330e101`
- 상태: 1차 포팅 구현이 미커밋 working-tree 변경으로 존재
- 기존 사용자 변경을 reset, checkout 또는 clean하지 않음
- commit, push, tag, merge, rebase, 배포와 외부 업로드 없음
