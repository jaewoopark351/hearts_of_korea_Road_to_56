# 2026-09-06 한국 해안 항구 배치 closure 보정

## 상태

- 생성기 및 생성 산출물: **수정 완료**
- 대상 정적 gate: **통과**
- aggregate static gate: **15 PASS / 0 WARNING / 1 ERROR**
- HOI4 런타임: **수정 후 미실행**
- 사건 판정: 생성 결함은 `CONFIRMED`, 접근 위반의 직접 원인은 cold test 전까지 `STRONGLY_SUPPORTED`

이 작업은 HOK 한국 해안 지형을 유지하면서 RT56 전 세계 buildings를 보존하는 `BINARY_MERGE` 보정이다. 기술, OOB, 음성, DDS, GFX와 gameplay 수치는 변경하지 않았다.

## 기준선

| 항목 | 값 |
|---|---|
| compat Git 기준 | `main@70aaba43a98fd429378ec1a67d4398f16330e101` 위 기존 미커밋 포팅 작업 |
| HOI4 | `1.19.2.0.a729 (18bf)` |
| RT56 Workshop manifest | `3323396725579032799` |
| RT56 `map/buildings.txt` | `5622673138F7269FA433E80CA19B49F5C48B52E7AA386568F4E6C3E96B0F99BB` |
| RT56 `map/definition.csv` | `005BB6052AEDBAA85FFE4607B21398A33055624A78C2F822F116AE895B58393E` |
| RT56 `map/provinces.bmp` | `B41B67B844407C70EB393E6979DCB8EE718BA76596ECEB2A9CCD38171156580F` |
| HOK donor `map/buildings.txt` | `DA7A22BC7F3996FC89496BEE248B530FA7039917564AD50B09F6B05A7F574A53` |
| vanilla `map/buildings.txt` | `4A336B6245026FCC693ED2BE7AE316A164135585AEC945EA190E32B8E65F4094` |

외부 source, launcher, 로그와 crash bundle은 읽기 전용으로 사용했다.

## 확인된 결함

기존 `tools/build_rt56_map.py`는 donor building 행에서 state 뒤 내용이 바닐라와 같으면 그 행을 HOK delta가 아니라고 보고 무조건 제외했다. 그러나 pinned RT56은 바닐라와 같은 일부 행을 자체적으로 제거했다. 그 결과 RT56 기준 지형에서는 필요 없지만 HOK 한국 해안을 복원하면 다시 필요한 `naval_base_spawn` 7행도 함께 탈락했다.

일반적인 `donor == vanilla && RT56에 없음` 규칙으로 복원하면 안 된다. 이 조건에 맞는 HOK 대상-state 건물은 401행이고, `naval_base_spawn`만으로 좁혀도 29행이다. 모두 추가하면 RT56이 의도적으로 바꾼 공장·보급·벙커·항구 배치를 되살리는 회귀가 된다.

좌표의 `x`, `z`를 내림하고 해당 source의 `provinces.bmp` RGB를 definition ID로 역매핑해 조사한 결과는 다음과 같다.

| 지도 | coastal land | spawn 미커버 province |
|---|---:|---|
| pinned RT56 | 2,544 | `490`, `1201`, `10715` |
| 수정 전 compat | 2,554 | RT56 3개 + `1054`, `7121`, `11912`, `12060`, `13546`, `13556`, `13564` |
| 수정 후 compat | 2,554 | `490`, `1201`, `10715` |

`naval_base_spawn`의 7번째 필드는 해안 province가 아니라 연결된 sea province다. 따라서 항구 coverage는 마지막 ID가 아니라 bitmap 좌표 샘플로 계산한다. BMP에 별도 y-flip을 적용하지 않고 기존 생성기와 같은 저장 행 좌표를 사용한다.

## 복원한 7행

| donor state | compat state | sampled province | sea link | 좌표 `x,z` |
|---:|---:|---:|---:|---|
| 1030 | 920 | 7121 | 7932 | `4825,1251` |
| 1030 | 920 | 13556 | 7932 | `4826,1245` |
| 1030 | 920 | 12060 | 7932 | `4816,1233` |
| 1030 | 920 | 1054 | 2708 | `4804,1226` |
| 1031 | 1145 | 13564 | 2781 | `4778,1263` |
| 1082 | 919 | 13546 | 2781 | `4779,1238` |
| 1030 | 920 | 11912 | 7932 | `4825,1266` |

각 행은 HOK donor에 정확히 1회 존재한다. state 뒤 내용은 바닐라에 정확히 1회 존재하고 pinned RT56에는 없다. 7개 sampled province는 모두 `land;true`이며 sea link는 정의된 `sea` province다.

## 구현

`tools/build_rt56_map.py`에 다음을 추가했다.

- 7행의 ordered allowlist와 예상 sampled province
- building 좌표의 7필드·범위·RGB→province 해석 helper
- allowlist source가 donor/vanilla/RT56 pinned 전제와 일치하는지 검사
- state/province ID 이식 뒤 sampled province, effective state, coastal 속성과 sea link 검사
- 전체 `naval_base_spawn` coverage를 pinned RT56과 비교하는 회귀 gate
- 합성 결과가 RT56보다 새 coastal-without-spawn을 만들거나 RT56 baseline을 예상 밖으로 덮으면 build 실패

기존 HOK-only 21행은 그대로 유지하고 topology restoration 7행을 별도 추가했다. 생성된 `map/buildings.txt`는 71,895행에서 71,902행으로 바뀌었고 최종 SHA-256은 `7BEA83AEC433FBF43A45E31C19C9860F1F907B2AA35959862501E16C42FD7780`이다. 다른 지도 생성 산출물은 모두 byte-identical하게 유지됐다.

생성 산출물 hash가 바뀌었으므로 `tools/build_integration_manifest.py --apply`로 1,014행 분류 원장의 `map/buildings.txt` 출력 hash도 재생성했다. 분류는 계속 `BINARY_MERGE / GENERATED`다.

## 정적 검증

실행한 명령:

```powershell
python -B tools\build_rt56_map.py --check
python -B tools\build_rt56_map.py --apply
python -B tools\build_rt56_map.py --check
python -B tools\build_integration_manifest.py --apply
python -B tools\build_integration_manifest.py --check
python -B tools\validate_port.py
```

결과:

- map generator 재현: PASS
- 다른 map output 변화: 0개
- 7개 topology restoration 중복: 0개
- 최종 새 coastal-without-spawn: 0개
- integration manifest 재현: PASS, 1,014행·exact-path collision 73개 유지
- aggregate: `15 PASS / 0 WARNING / 1 ERROR`

남은 1개 오류는 기존 `music/Minshu_ikki.ogg`가 donor 현행 song 목록에 등록되지 않아 Korea-only pruning 정책과 충돌하는 별도 사용자 변경이다. 이번 지도 보정과 무관하며 임의로 삭제하지 않았다.

## 런타임 판정과 다음 gate

21:28 비한국 국가와 21:30 KOR 실행은 번역 모드 없이 RT56+compat만 활성화한 상태에서 같은 `C0000005` 14-frame offset stack으로 실패했다. 그 stack은 2026-09-01에 `mapbuildings.cpp:634` 및 `map.cpp:1679`의 coastal-without-port likely-crash 경고 직후 발생한 stack과 같다. 이 때문에 항구 결함의 crash 인과는 강하게 지지되지만, 최신 실행은 이 보정 전 산출물이다.

다음 순서로 별도 cold start가 필요하다.

1. RT56 + compat, 비한국 국가(GER): 새 게임 → paused map → +1 day
2. 같은 구성, KOR: 새 게임 → paused map → +1 day
3. 한국 항구·해군기지·보급 및 새 map/port 오류 확인
4. 두 실행에서 같은 stack이 사라졌는지 비교

두 실행을 통과하기 전에는 사건을 Close하거나 HOI4 런타임 호환을 완료했다고 표현하지 않는다.
