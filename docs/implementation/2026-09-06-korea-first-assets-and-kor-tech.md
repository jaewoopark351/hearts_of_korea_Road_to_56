# 2026-09-06 한국 우선 자산·KOR 기술 보정

> 상태: **정적 구현 완료 / aggregate pruning 오류 1건 / HOI4 런타임 미실행**

## 1. 목적

이 배치는 오류를 줄이기 위해 HOK 한국 콘텐츠를 제거한 1차 자산 결정을 되돌리고, 현재 RT56과 충돌하지 않는 형태로 HOK 음성·기본 항공기 표현을 복원한다. 동시에 19:20 로그에서 명시된 KOR 시작 기술 오류를 최소 수정한다.

일반 JAP/CHI/PRC 콘텐츠, RT56 세계 지도, donor/Workshop/vanilla/user-data는 변경하지 않았다.

## 2. 고정 source

| source | 기준 |
|---|---|
| compatibility worktree | `main@70aaba43a98fd429378ec1a67d4398f16330e101` 위 미커밋 변경 |
| HOK donor | `C:\hoi\hearts_of_korea`, revision item `3793992662`, 읽기 전용 |
| RT56 | Workshop item `820260968`, manifest `3323396725579032799`, 읽기 전용 |
| HOI4 | 19:20 로그의 `1.19.2.0.a729 (18bf)`; 설치 폴더 읽기 전용 |

생성기는 사용한 donor/RT56 text와 binary를 SHA-256으로 고정한다. source drift가 있으면 새 기준선 검토 없이 통과하지 않는다.

## 3. KOR 시작 기술

`history/countries/KOR - Korea.txt`의 두 할당을 다른 기술로 치환하지 않고 제거했다.

- `bba_early_transport_plane`
- `early_transport_plane`

현재 RT56은 두 기술 정의를 활성 등록하지 않고 `transport_plane_equipment_1`을 `active = yes`로 제공한다. KOR OOB와 다른 HOK script에도 두 ID의 소비자가 없으므로, 이 수정은 HOK의 관찰 가능한 1933 수송기 해금 상태를 유지하는 `SEMANTIC_EQUIVALENT` migration으로 분류한다.

`tools/migrate_doctrines.py`가 donor KOR history에서 교리 migration과 이 정리를 함께 재생성한다. 생성기는 다음을 확인한다.

- 두 폐기 tech가 RT56의 활성 top-level 기술 ID가 아님
- `transport_plane_equipment_1`이 RT56에서 전역 활성 상태임
- 산출 KOR `set_technology`에 두 ID가 남지 않음
- 기존 1차 doctrine 산출물의 정확한 hash만 후속 migration 입력으로 허용

19:20 로그의 관련 5개 기록이 실제로 사라지는지와 수송기 생산 UI는 아직 런타임 미검증이다. 이 수정과 `C0000005`의 인과도 `UNPROVEN`이다.

## 4. HOK 한국 음성

HOK donor WAV 18개는 변환·재압축하지 않고 byte-identical하게 유지한다. 파일 형식은 모두 IEEE float WAV, 44.1 kHz, mono, 32-bit다.

donor `sound/voice_korea.asset`을 별도로 싣지 않는다. 대신 compat의 `sound/r56_vo_Korean.asset` 하나가 같은 RT56 가상경로를 shadow하도록 생성했다.

- RT56에서 유지: 현재 `Voices` category와 compressor
- HOK에서 유지: sound 정의, idle 반복 가중, neutral/positive/retreat/move 목록, `max_audible=1.3`, `volume=1.0`
- 포함: `kor_Positive_005.wav`
- 제외: RT56 전용 payload `kor_Idle_006.wav`, `kor_Neutral_005.wav`

생성기는 5개 `KOR_infantry_*` soundeffect가 산출물에서 각각 한 번만 정의되고, 참조 WAV 집합이 donor 18개와 정확히 일치하는지 검사한다. 실제 VFS에서 host 파일 하나만 유효한지, 음성 오류 0건인지와 선택·이동·전투·후퇴 상황의 가청 결과는 새 cold start가 필요하다.

호환용 음성·mesh·entity ID의 중복 검사는 compat와 RT56뿐 아니라 설치된 바닐라, `Korean Language`, `The Road to 56 Korean Translation`의 관련 GFX/sound 파일도 읽기 전용으로 훑는다. 이 검사는 물리 정의의 충돌 부재만 증명하며 실제 launcher 순서나 VFS 우선순위는 증명하지 않는다.

## 5. HOK 기본 항공기 자산

HOK 경·중·대형 항공기 mesh와 diffuse/normal/specular를 donor bytes로 관리한다. 복원한 diffuse의 계약은 다음과 같다.

| 자산 | HOK 크기 | 형식 |
|---|---:|---|
| heavy diffuse | 256×128 | 비압축 32-bit BGRA, alpha, mip 1 |
| light diffuse | 256×256 | 비압축 32-bit BGRA, alpha, mip 1 |
| medium diffuse | 256×256 | 비압축 32-bit BGRA, alpha, mip 1 |

HOK mesh 안에는 같은 HOK diffuse/normal/specular 파일명이 내장돼 있다. RT56의 일본계 KOR mesh에 diffuse만 씌우지 않고 HOK mesh/entity를 다음 고유 ID로 복원했다.

| 종류 | compatibility ID |
|---|---|
| light mesh | `hok_rt56_KOR_plane_light_mesh` |
| medium mesh | `hok_rt56_KOR_plane_medium_mesh` |
| heavy mesh | `hok_rt56_KOR_plane_heavy_mesh` |
| light entity | `hok_rt56_KOR_light_plane_entity` |
| medium entity | `hok_rt56_KOR_medium_plane_entity` |
| heavy entity | `hok_rt56_KOR_heavy_plane_entity` |

RT56의 기존 `KOR_*` mesh/entity ID는 건드리거나 다시 등록하지 않았다. HOK `00_hok_plane_icons.txt`의 KOR 소비자만 새 entity를 사용하며, medium entity에는 현행 RT56의 `supply` state를 병합했다. HOK scale과 locator는 유지했다.

실제 UV 정렬, 모델 크기, animation/attachment, 보라색 texture와 공중보급 표현은 런타임 화면에서 검증해야 한다.

## 6. 도구·원장 변경

- `tools/build_korean_assets.py`: pinned source에서 음성·항공기 산출물 재생성/검사
- `tools/prune_rt56_owned_files.py`: HOK WAV 18개와 KOR diffuse 3개를 삭제 목록에서 제거; donor 음성 registry는 계속 제외
- `tools/build_integration_manifest.py`: 위 21개 payload를 `ASSET_COPY`, donor 음성 registry를 `THREE_WAY_MERGE`로 분류; 모든 `ASSET_COPY`의 donor byte 동일성 강제
- `tools/migrate_doctrines.py`: KOR 폐기 수송기 기술 migration과 RT56 계약 검사
- `tools/validate_port.py`: 한국 자산 generator, 폐기 기술과 필수 registry/consumer assertion 추가

현재 1,014행 집계는 다음과 같다.

| 분류 | 수 |
|---|---:|
| `ADD` | 119 |
| `ASSET_COPY` | 776 |
| `BINARY_MERGE` | 18 |
| `OVERRIDE` | 7 |
| `THREE_WAY_MERGE` | 31 |
| `USE_RT56` | 63 |

## 7. 정적 결과와 남은 오류

한국 자산 builder, doctrine migration, RT56-owned pruning과 manifest 재생성은 모두 통과했다. aggregate `python tools\validate_port.py`는 `15 PASS / 0 WARNING / 1 ERROR`다.

유일한 오류는 구현 도중 20:13:59에 다시 나타난 `music/Minshu_ikki.ogg`다. donor asset에는 일본 민주화 테마로 정의돼 있지만 현행 `hok_songs.txt`에는 등록되지 않았고, 같은 이름의 `KOR_minshu_ikki` focus에도 음악 재생 효과는 없다. 기존 Korea-only pruning 정책과 충돌하지만 동시 사용자 변경과 HOK 보존 의도를 임의로 판단하지 않기 위해 자동 삭제하지 않았다. 한국 음성·항공기나 KOR 기술 gate의 실패는 아니다.

세부 출력은 [후속 정적 검증 기록](../validation/2026-09-06-korea-first-static-validation.md)에 있다.

## 8. 다음 런타임 게이트

1. `R0`: RT56 단독 cold start
2. `R1`: RT56 + 실제 선택 localisation
3. `C0-NONKOR`: 번역 없이 RT56 + compat, 기본 game rule
4. `C0-KOR`: 같은 구성에서 KOR
5. 기술 오류 5건, sound duplicate/load, GFX entity/texture 오류 비교
6. paused map, 1일·7일·30일 진행
7. HOK 음성 청취와 기본 항공기 모델·도색 확인

비한국 국가를 선택해도 KOR history/OOB는 전체 초기화에 포함될 수 있다. 두 `C0`가 모두 실패하면 국가 선택만으로 KOR 초기화를 배제하지 않고 임시 비배포 diagnostic slice로 OOB/history 묶음을 이분한다. 진단 중 제외한 HOK 기능은 원인 판별 뒤 반드시 복원한다.

게임 실행, 로그·launcher 수정, commit, push와 배포는 수행하지 않았다.
