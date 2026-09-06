# ADR-0004: HOK 한국 콘텐츠 우선 보존

## 상태

- 결정: **Accepted**
- 결정일: 2026-09-06
- 결정 근거: 사용자 지시 — HOK의 한국 부분은 최대한 보존하고, 중국·일본 자체 콘텐츠는 RT56을 사용한다.
- 적용 범위: 이후의 포팅, 디버깅, 자산 선택, 검증과 release 판단

이 ADR은 1차 구현 기록의 당시 상태를 지우지 않는다. 현재 통합 원장과 생성 CSV는 이 결정을 반영하며, 1차 기록에서 한국 공용 음성과 KOR 항공기 diffuse texture를 RT56 소유로 정한 결정은 이 ADR이 대체한다.

## 맥락

이 포트의 목적은 오류 수를 줄이기 위해 HOK 콘텐츠를 제거하는 것이 아니라, 현재 RT56 세계 위에서 HOK의 한국 플레이 경험을 되살리는 것이다. 중국·일본의 일반 콘텐츠까지 오래된 donor 파일로 덮으면 RT56 기능을 잃지만, 반대로 충돌한다는 이유만으로 한국 음성·그림·이벤트·중점 등을 RT56 것으로 바꾸면 HOK의 정체성을 잃는다.

따라서 소유권은 파일명이나 국가 태그 하나만으로 정하지 않고, **그 정의가 최종적으로 어떤 플레이 경험을 제공하는지**를 기준으로 정한다.

## 결정

### 1. 최종 한국 동작과 표현은 HOK 우선이다

다음은 기본적으로 HOK 보존 영역이다.

- KOR 시작 history, 정치, 법, 연구, OOB와 시작 장비
- HOK의 한국 focus, idea, decision, mission, event와 on_action 흐름
- 한국 character, leader, advisor, trait, AI plan, MIO와 이름 목록
- HOK가 설계한 한반도 state/province 구성, 지명, 자원, 건물, 승점, 철도와 보급
- 한국 국기, 초상화, 중점·결정·idea·event 그림, 모델, texture, 음성, 음악과 UI 표현
- KOR 경로가 생성하거나 직접 소비하는 HOK 전용 후속 태그와 결과. 예를 들어 `KCH`와 `KJP`는 이름에 중국·일본이 들어가더라도 한국 경로의 산출물이라면 한국 보존 영역으로 본다.
- 한국 콘텐츠가 참조하는 localisation key와 scripted localisation

“HOK 우선”은 donor의 오래된 파일 전체를 그대로 적재한다는 뜻이 아니다. 현재 HOI4 문법과 RT56 연결점에 맞게 고치더라도, 관찰 가능한 한국의 설계·ID·밸런스·시청각 결과를 가능한 한 유지한다는 뜻이다.

### 2. 중국·일본 자체 플레이와 전역 시스템은 RT56 우선이다

다음은 기본적으로 RT56 기준을 사용한다.

- 일반 JAP, CHI, PRC와 군벌의 focus, decision, event, history, OOB, AI와 시청각 자산
- RT56 전 세계 지도와 한반도 밖 state/province
- generic database, 공용 on_action, bookmark, 공용 MIO, 훈장 trigger, 난이도와 정보기관
- RT56이 현재 버전에 맞게 확장한 공용·동아시아 시스템

HOK의 중국·일본 whole file을 다시 적재해 RT56 정의를 가리지 않는다.

### 3. 한국과 중국·일본의 접경은 최소 병합한다

중국·일본 파일 안에 한국 독립, 영토, 외교, 전쟁, 이벤트 후속 또는 KOR 경로 진입점이 있으면 그 연결점까지 버리지 않는다.

1. 현재 RT56 파일 또는 additive 파일을 base로 삼는다.
2. HOK 한국 경로에 필요한 trigger, option, effect, event 호출과 state 참조만 이식한다.
3. HOK 상속 ID를 충돌 없이 보존하고, 새 접착 ID가 필요하면 `hok_rt56_` 계열의 확인된 빈 namespace를 사용한다.
4. 정상 JAP/CHI 플레이가 RT56과 같게 남는지와 KOR 경로가 HOK 의도대로 작동하는지를 둘 다 검사한다.

파일의 대부분이 일본·중국 코드여도 한국 흐름에 필요한 한 블록은 `THREE_WAY_MERGE` 대상이다. 반대로 KOR이 한 번 언급된다는 이유만으로 파일 전체를 HOK 소유로 만들지는 않는다.

### 4. binary payload와 논리 registry의 소유권을 분리한다

음성·DDS 같은 자산은 두 층으로 본다.

| 층 | 예 | 기본 정책 |
|---|---|---|
| payload/presentation | `.wav`, `.dds`, `.tga`, mesh texture | 한국을 표현하는 payload는 HOK 우선 |
| registry/behavior | `.asset`, `.gfx`, entity, sprite, soundeffect | 현재 RT56/HOI4 schema를 base로 단일 effective definition을 유지하고 HOK 의미를 병합 |

동일 논리 ID를 서로 다른 두 파일에서 중복 등록하지 않는다. 같은 상대경로 payload를 HOK 파일로 제공할 수는 있지만, 실제 우선순위와 소비자가 그 경로를 사용하는지는 런타임에서 확인한다.

### 5. 한국 음성의 목표 상태

호환 포트에는 donor `sound/voice_korea.asset`을 싣지 않는다. 대신 RT56과 같은 가상경로인 `sound/r56_vo_Korean.asset`을 생성해 RT56의 현행 category/compressor와 HOK의 sound 정의, idle 가중 반복, combat/move 재생 목록, `max_audible=1.3`, `volume=1.0`을 병합한다. 이 registry는 HOK WAV 18개 전부를 참조하며 `kor_Positive_005.wav`를 포함하고, RT56 전용 `kor_Idle_006.wav`와 `kor_Neutral_005.wav` payload는 참조하지 않는다.

`tools/build_korean_assets.py`는 두 source asset과 WAV를 hash로 고정하고, 각 soundeffect ID가 산출물에서 한 번만 정의되는지 검사한다. 19:20 무오류 로그는 이 병합 전 중간 상태의 증거이므로 새 registry의 실제 단일-owner VFS 동작, duplicate/load failure 0건과 실제 청취는 다음 cold start에서 확인해야 한다.

### 6. 한국 DDS와 기타 시각 자산의 목표 상태

한국 focus/idea/decision/event/portrait/flag/unit model이 사용하는 `.dds`와 `.tga`는 HOK 자산을 기본 선택으로 한다. 동일 상대경로라면 HOK payload override를 우선 검토하고, sprite/entity/material 정의는 현재 schema에 맞춰 중복 없이 병합한다.

동일 경로라는 이유만으로 바로 교체하지는 않는다. 다음을 먼저 확인한다.

- width/height, DDS codec, alpha, mipmap과 frame 수
- `.gfx`, `.asset`, mesh/material이 기대하는 정확한 경로와 이름 대소문자
- HOK 자산이 실제 KOR 소비자에 연결되는지
- 교체 후 누락·보라색 texture·왜곡·잘못된 국가 그림이 없는지

`KOR_plane_heavy_diffuse.dds`, `KOR_plane_light_diffuse.dds`, `KOR_plane_medium_diffuse.dds`는 감사 후 HOK `ASSET_COPY`로 복원했다. 모두 비압축 32-bit BGRA, alpha 포함, mip 1이며 heavy는 양쪽 모두 256×128, HOK light/medium은 256×256으로 RT56의 256×128과 다르다. diffuse만 RT56 일본계 mesh에 씌우지 않도록 HOK 기본 mesh/entity를 `hok_rt56_` 고유 ID로 복원하고 HOK KOR graphic DB만 새 entity를 소비하게 했다. 중형 entity에는 RT56 공중보급 state를 병합했다. UV·크기·렌더링 결과는 아직 런타임 미검증이다.

## 디버깅 원칙

- 오류가 사라졌다는 이유만으로 HOK 한국 기능을 제거하지 않는다.
- 격리 시험에서 기능을 잠시 제외하더라도 이는 원인 판별용일 뿐 최종 소유권 결정이 아니다.
- HOK 기준 동작과 현재 포트 동작을 나란히 기록하고, 차이가 호환 수정인지 콘텐츠 손실인지 구분한다.
- RT56-only에서도 발생하는 오류는 host baseline으로 분리하되, 그것이 한국 콘텐츠를 막는 경우에만 좁은 compatibility shim을 검토한다.
- 세부 실행 절차와 판정표는 [한국 콘텐츠 우선 디버깅 플레이북](../KOREAN_CONTENT_DEBUGGING.md)을 따른다.

## 구현 상태

- `tools/build_korean_assets.py`가 HOK WAV 18개, 기본 항공기 mesh/texture, 고유 registry ID와 소비자, 단일 병합 음성 registry를 재현한다.
- `tools/prune_rt56_owned_files.py`는 위 WAV와 diffuse 3개를 삭제하지 않고 donor `sound/voice_korea.asset`만 중복 방지를 위해 제외한다.
- 생성 manifest는 WAV·diffuse를 `ASSET_COPY`, donor 음성 registry를 `THREE_WAY_MERGE`로 기록하며 모든 `ASSET_COPY`가 donor bytes와 같은지 강제한다.
- aggregate validator의 한국 자산·폐기 기술 gate는 통과했다. 전체 run은 동시 복구된 일본 민주화 테마 `music/Minshu_ikki.ogg` 때문에 Korea-only pruning 오류 1건이 남아 있다. donor의 현행 song 목록은 이 곡을 등록하지 않고 같은 이름의 KOR focus도 음악을 재생하지 않으므로, 사용자 변경과 HOK 보존 의도를 임의로 판단하지 않고 파일 처리를 보류했다.

## 결과

- HOK 한국 콘텐츠의 보존이 충돌 해결보다 하위 목표로 밀리지 않는다.
- RT56의 중국·일본 및 전역 기능은 donor whole-file shadow로부터 보호된다.
- 음성처럼 payload는 HOK, registry는 단일 병합 정의로 분리할 수 있다.
- 콘텐츠를 제외하는 수정은 한국 보존 계약과 대조군 결과를 제시하지 않으면 완료로 인정하지 않는다.
- 기존 HOK 세이브 호환성은 별도 migration과 검증 전까지 주장하지 않는다.
