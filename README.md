# Hearts of Korea × The Road to 56 Compatibility

> 상태: **최신 HOK 한국 콘텐츠·MAN 후속 조건 반영 / 보완 fixture 134 PASS·임시 파일 없는 한국 새 게임 부분 검증 / 릴리즈 검증은 별도**
>
> 초기 C1·R0 대조와 C0의 첫 MAN 수선 실패를 보존했다. 후속 MAN 조건을 적용한 기본 fixture는 **118 PASS / 1 FAIL / 7 SKIP**, 부탄의 종속 상태 때문에 실패한 시험 구성을 NEP로 보완한 alternate는 **134 PASS / 0 FAIL / 0 SKIP**다. 두 실행에서 MAN 반복 오류가 관측되지 않았으며 임시 파일을 제거한 한국 새 게임에서도 중점 선택·완료와 한국어 UI를 확인했다. 전체 런타임 검증이나 릴리즈 준비 완료를 뜻하지 않는다. [실행 증거와 한계](docs/audits/2026-09-22-korean-update-runtime.md)

이 저장소는 Hearts of Korea(HOK)의 한국 콘텐츠를 **현재 The Road to 56(RT56)을 호스트로 삼아 다시 이식하는 별도 신규 모드**다. `C:\hoi\hearts_of_korea`는 읽기 전용 donor이며 플레이할 때 함께 켜는 모드가 아니다.

**2026-09-22 이미지 업데이트:** 중점 60개·국민정신 29개의 새 그림과 GFX를 가져오고 AGENTS의 이미지 작업 규칙을 포트에 맞게 반영했다. 그림 연결 외 게임 효과는 보존했다. [이식·검증 기록](docs/implementation/2026-09-22-korean-icon-port.md), [색상 비교](docs/assets/korean-focus-icon-colors/index.html), [소재 크레딧](docs/HOK_KOREAN_FOCUS_ICON_CREDITS.md)을 따른다. 새 이미지의 포트 게임 실행은 아직 하지 않았다.

**2026-09-22 구현:** 한국 runtime 20개 파일에 중점 266→326개 확장, 보상·결정·이벤트·현지화와 역사 AI 기본106개·지원3계획을 반영했다. 기존 지도 ID, 만주15개 주와 대일 강화 처리를 보존하고 RT56 manifest `7475007536894105204`의 변경9개 파일을 재병합했다. [구현·검증 기록](docs/implementation/2026-09-22-korean-focus-update-port.md)과 [이식 계획](docs/plans/2026-09-22-korean-focus-update-port-plan.md)을 구분한다. 기간 단축은 실제 이식 전 호환판 대비154개(확장152개+원본 선행2개)다.

C1에서 발견한 기존 한국 캐릭터 병합 누락에 대한 첫 정의 복원은 C0에서 실패했다. 후속으로 MAN의 한국 고문 조건 두 곳을 `has_character`로 보호한 `is_hired_as_advisor` 검사로 바꿔 생성·정적 검증했고, 기본 C1 시험에서는 기존 반복 오류가 재현되지 않았다. 한국 인물 모집·history·균형과 두 조건 외 MAN 내용은 유지한다.

두 fixture에서 스크립트로 완료한 중점 ID의 합집합은 신규 60개다. 국민정신 상태, 시민교육 세 주의 민간공장 +2, 네 지역 사업의 두 회차 첫 +1·누적 +2와 조기 지급 부재, 평안 취소·무보상·재착수, 관세·면허 협정 수락·세력 탈퇴 정리를 확인했다. 정상 UI의 비용·선행 조건·기간과 모든 보상을 검증한 결과는 아니다. 임시 시험 파일 두 개는 해시 대조 후 제거했으며 실제 AI 계획·협정 거절·자연 만료 등은 남았다.

임시 파일 없는 새 한국 게임은 `1936.04.28.22`까지 진행했다. 기존 중점 둘을 정상 진행하고 원화평가절하의 선택·완료·국민정신 및 한국어 UI를 확인했다. 저장된 중점 진행일수가 적용되어 정확히 35일 걸렸다는 측정은 아니며, 이 실행에서는 수동 저장·재로드를 시험하지 않았다.

## 목표 실행 구성

```text
Hearts of Iron IV 1.19.x
  + The Road to 56
  + 이 HOK–RT56 호환 포트
  + 선택한 localisation 구성
```

- RT56이 전 세계 지도, 공용 시스템과 비한국 콘텐츠를 소유한다.
- 이 포트는 검토된 HOK 한국 콘텐츠와 필요한 접착 코드만 제공한다.
- HOK donor는 런타임 의존성이 아니다.
- 현재 `descriptor.mod`는 `The Road to 56`과 `Korean Language`를 의존성으로 선언한다. 19:20 실행은 대신 `The Road to 56 Korean Translation`을 사용했지만, 21:28/21:30에는 번역 계층을 모두 빼도 같은 crash가 재현됐다. 최종 localisation 계약 자체는 여전히 미결정이다.
- broad `replace_path`와 launcher 전용 `path`는 넣지 않았다. `remote_file_id=3796816200`은 이미 별도로 배정된 이 호환판 항목 ID이며 donor·RT56 ID를 재사용하지 않는다.
- localisation의 최종 권장 조합은 런타임 대조군 시험 전까지 미결정이다.

## 이번 구현

- RT56 `definition.csv`와 `provinces.bmp`를 기준으로 HOK 한국 지형 delta를 합성했다.
- 충돌하던 HOK province `13414–13447`을 새 범위 `13535–13568`로 이전했다.
- 충돌하던 HOK state를 `917–920`, `1144–1147`로 이전하고 모든 추적 가능한 참조를 갱신했다.
- donor-vs-vanilla 차집합만 사용하던 지도 생성기에서 RT56이 제거한 vanilla-identical HOK 항구 spawn 7개가 누락되는 결함을 고쳤다. 합성 후 새로 비던 province `1054`, `7121`, `11912`, `12060`, `13546`, `13556`, `13564`만 복원하고, RT56 기준보다 새 coastal-without-spawn이 없음을 생성 시 검사한다.
- 한국의 네 만주 획득 경로에서 구 8개 주와 RT56 분할주 `941–947`의 통제 조건, 이전, 한국 코어, 분리주의와 경로별 기존 중국계 코어·주둔군 처리를 같은 15개 주 집합으로 맞췄다. 전쟁 점령 뒤 휴전 결정은 RT56 전쟁 처리로 `MAN`의 일본 종속 관계가 먼저 사라져도 계속 표시되고, 살아 있는 `MAN`과의 별도 전쟁도 조건부로 끝내며, 분할주 지명은 RT56 정의를 그대로 사용한다.
- bookmark, MIO, 훈장 trigger, generic advisor, 일본·중국 이벤트/결정/history/OOB 등은 현재 RT56 또는 바닐라를 기준으로 필요한 한국 delta만 다시 적용했다.
- 낡은 difficulty, MTG on_action과 비한국 FIN/MON/SIB 도전 모듈은 포트에서 제외했다. ADR-0004에 따라 한국 음성·DDS payload는 HOK 것을 우선하고, `.asset`·`.gfx` 논리 registry는 중복 없이 병합한다.
- KOR 인물, AI 전략, MIO, 편제명과 함명을 HOK/RT56 양쪽 정의에서 병합했다.
- 1차 포팅에서 HOK event namespace, 호출되지 않는 이벤트, 비한국 cosmetic, 일본 전용 고아 GFX·음악·trait와 영·한 localisation 참조를 정리했다. 이후 `Minshu_ikki.ogg`가 일시적으로 다시 나타났던 보류 이력은 날짜가 붙은 검증 문서에 보존하며, 첫 MAN 수선 시점의 pruning gate는 통과했다.
- KOR history의 `bba_early_transport_plane`·`early_transport_plane` 할당은 대체 기술을 주지 않고 제거했다. RT56은 해당 1933 수송기 장비를 전 국가에 이미 활성화한다.
- HOK WAV 18개와 기본 항공기 mesh/texture를 donor bytes 그대로 관리한다. 음성은 RT56 category/compressor와 HOK 재생 목록·volume을 합친 `sound/r56_vo_Korean.asset` 하나만 등록하고, HOK 항공기 mesh/entity는 `hok_rt56_` 고유 ID로 소비한다.
- 기존 donor 1,014개에 한국 업데이트20개를 선택 적용한 입력1,031개와 새 한국 이미지·GFX92개를 합쳐 1,123개를 분류했다: `ADD 139`, `USE_RT56 63`, `THREE_WAY_MERGE 31`, `OVERRIDE 9`, `BINARY_MERGE 18`, `ASSET_COPY 863`. 고정 Git 입력과 미커밋 artwork의 출처·해시를 원장에서 구분한다.

### 지도 ID 마이그레이션

| donor state | compat state | 지역 |
|---:|---:|---|
| 1028 | 918 | 함경 |
| 1029 | 1144 | 강원 |
| 1030 | 920 | 경상 |
| 1031 | 1145 | 충청 |
| 1082 | 919 | 전라 |
| 1083 | 917 | 황해 |
| 1084 | 1146 | 제주 |
| 1085 | 1147 | 쓰시마 |

이 마이그레이션 때문에 현재 목표는 **신규 게임 전용**이다. 대표적인 기존 세이브의 load–advance–save–reload 시험 없이 기존 HOK 세이브 호환성을 주장하지 않는다.

## 정적 검사 상태

9월22일 첫 MAN 정의 복원 시점과 후속 MAN 조건 생성 뒤의 aggregate 검사는 각각 **`20 PASS / 0 WARNING / 0 ERROR`**였다. 후속 결과는 fixture 설치 전 `static-validation-man-guard.txt`에 보존했다. 한국 중점 의미 검사 `--check`도 통과했고 `--self-test`는 13개 회귀 변형을 모두 거부했다. 이 수치는 각 실행 당시 스냅샷이며 9월6일의 `15 PASS`, 후속 `17 PASS`와 구분한다. 최신 정적 결과와 임시 파일 제거 후 상태는 [이번 구현 기록](docs/implementation/2026-09-22-korean-focus-update-port.md)과 [실행 감사](docs/audits/2026-09-22-korean-update-runtime.md)를 따른다.

```powershell
python tools\source_snapshot.py --import-icons
python tools\validate_port.py
python tools\check_korean_focus_update.py --check
python tools\check_korean_focus_update.py --self-test
```

검사는 고정 소스·지도·공용 파일·동아시아 파일·한국 자산·삭제 목록·ID 이식·한국 업데이트·1,123개 분류표의 재현성, Paradox Script 괄호/따옴표, descriptor 계약, 폐기 ID, localisation BOM/header/key, event asset/loc, 핵심 논리 ID 중복, 만주15개 주 처리와 신규 중점·지역사업·외교·AI 계약을 확인한다. 최초 소스 준비는 donor의 고정 Git 객체와 별도 해시로 고정한 artwork를 읽어 저장소 내부 `.local-artifacts/sources/`에만 쓴다. 원본 또는 기존 캐시가 기록된 해시와 다르면 덮어쓰지 않고 중단한다.

ADR-0004의 자산 정책과 만주 획득 경로 보정은 도구·원장·회귀 검사에 반영됐다. 이미지 이식 후 정적 결과는 **19 PASS / 0 WARNING / 1 ERROR**다. 기존 사용자 변경인 KOR 시작 전쟁 지지도 `0.1`이 doctrine 생성기의 `0.05`와 달라 한 검사가 실패하며, 이번 이미지 이식에서는 그 게임플레이 변경을 보존했다. 이미지·기존 보상 보존 검사는 통과했다. 과거 정적 20 PASS와 `Minshu_ikki.ogg` 보류 상태는 당시 기록과 구분한다.

이 검사는 HOI4 엔진 파싱, launcher 발견/로드 순서, 새 게임, unpause, DLC 경로, 실제 UI localisation, AI, 세이브와 멀티플레이를 증명하지 않는다.

## 기존 산출물 기준과 현재 제한

| 항목 | 기준 |
|---|---|
| 문서화 시작 시점 | `main@bfbba43c26022f3f64a88c2f1ec6600cb7f0d06f`, 작업 트리 깨끗함 |
| 기존 이식 HOK donor | `887930f6e88c80568d62dab9cfbe1ba8a498a252`, 읽기 전용 |
| 기존 RT56 Workshop manifest | `3323396725579032799` |
| RT56 descriptor SHA-256 | `5B323861ABD63E31CB896277E3EA58BA4BCD9FCEEDA957B50792065E42E03F61` |
| HOI4 로그 기준 | 2026-09-06 21:30 실행, 1.19.2.0.a729 (18bf), DataChecksum `1b8bfef72bfa60a3735bc6782b2ca33b` |

2026-09-06의 HOK donor와 번역 모드 없는 RT56+호환판 실행에서는 21:28 비한국 국가와 21:30 KOR 모두 같은 새 게임 접근 위반을 재현했다. KOR 폐기 기술 오류와 한국 음성 중복·로드 오류는 0건이었으므로 번역과 폐기 기술은 그 crash의 필요조건이 아니었다. 이후 C1은 당시 실패 지점을 넘어 한국 지도 진입·시간 진행까지 확인했지만 엔진과 호스트도 달라 항구 배치 수정 하나의 인과를 확정하지 않는다.

2026-09-22 조사에서 donor는 `81d39fa`, 설치 RT56 manifest는 `7475007536894105204`로 확인됐다. 9월 21일 HOI4 `1.19.3.0.c01a` 로그는 donor 단독 실행이며 호환판 검증 증거가 아니다. [이식 계획의 기준선](docs/plans/2026-09-22-korean-focus-update-port-plan.md#2-조사-기준선)에 구 기준과 관찰값을 구분했다.

현재 [C1·R0·C0 실행 기록](docs/audits/2026-09-22-korean-update-runtime.md)은 HOI4 `1.19.3.0.c01a`와 DLC 36개 기준이며 실행별 체크섬을 구분한다. 저장 최종 이름 변경 오류와 PRC advisor 재로드 오류는 R0에서도 재현되어 포트 없이 발생함을 확인했다. fixture에서도 엔진 임시 자동저장과 rename 실패가 있었고 전체 오류 0건은 아니다. NEP 시험은 assertion 종료 뒤 1937년까지 진행됐으나 프로세스 종료 원인은 미확인이며 장기 안정성 검증으로 집계하지 않는다. 실제 AI·만주 경로·DLC 분기 등은 남아 있고 임시 저장 재로드를 정상 저장 완료나 기존 세이브 호환성으로 설명하지 않는다.

## 기준 경로

| 별칭 | 경로 | 역할 |
|---|---|---|
| `<COMPAT_ROOT>` | `C:\hoi\hearts_of_korea_Road_to_56` | 유일한 구현 쓰기 대상 |
| `<HOK_DONOR>` | `C:\hoi\hearts_of_korea` | 읽기 전용 HOK donor/provenance |
| `<RT56_SOURCE>` | `C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968` | 읽기 전용 RT56 host snapshot |
| `<VANILLA_SOURCE>` | `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV` | 읽기 전용 HOI4 문법·스키마 기준 |
| `<HOI4_LOGS>` | `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV\logs` | 읽기 전용 런타임 증거 |

Steam 갱신으로 고정한 RT56 입력 파일의 해시가 바뀌면 pinned source 검사에서 중단된다. manifest 변경과 관련 파일 해시를 함께 확인하고 새 기준선에서 병합을 다시 검토한다.

## 문서

- [문서 인덱스](docs/README.md)
- [2026-09-22 한국 중점 업데이트 이식 계획](docs/plans/2026-09-22-korean-focus-update-port-plan.md)
- [2026-09-22 한국 중점 업데이트 구현](docs/implementation/2026-09-22-korean-focus-update-port.md)
- [2026-09-22 한국 업데이트 런타임 증거](docs/audits/2026-09-22-korean-update-runtime.md)
- [포팅 아키텍처](docs/PORTING_ARCHITECTURE.md)
- [포팅·검증 워크플로](docs/PORTING_WORKFLOW.md)
- [HOK 한국 콘텐츠 우선 디버깅](docs/KOREAN_CONTENT_DEBUGGING.md)
- [ADR-0004: HOK 한국 콘텐츠 우선 보존](docs/decisions/0004-hok-korean-content-priority.md)
- [포팅 후 새 게임 접근 위반](docs/incidents/2026-09-06-post-port-new-game-crash.md)
- [한국 우선 자산·KOR 기술 구현](docs/implementation/2026-09-06-korea-first-assets-and-kor-tech.md)
- [한국 해안 항구 배치 closure 보정](docs/implementation/2026-09-06-map-building-closure-fix.md)
- [1차 구현 기록](docs/implementation/2026-09-06-first-port-batch.md)
- [통합 ledger](docs/audits/2026-09-06-integration-ledger.md)
- [1,123개 파일 분류 CSV](docs/audits/2026-09-06-production-file-classification.csv)
- [정적 검증 기록](docs/validation/2026-09-06-static-validation.md)
- [한국 우선 후속 정적 검증](docs/validation/2026-09-06-korea-first-static-validation.md)
- [시작 크래시 조사](docs/incidents/2026-09-06-startup-crash.md)

## 출처와 배포 정체성

- `2898629778`: 역사적 HOK 원본 Workshop 항목 — provenance 전용
- `3793992662`: 사용자 제공 HOK donor revision — provenance 전용
- `820260968`: The Road to 56 — 런타임 의존성과 provenance
- `3796816200`: 현재 descriptor에 기록된 이 호환판 ID — 후속 게시·갱신 전 대상 재확인

새 모드는 기존 ID를 상속하거나 업로드 대상으로 사용하지 않는다. HOK 원작자, donor 개정 기여자, RT56 팀, localisation 및 제3자 기여자를 구분해 크레딧하고, 근거 없이 HOK 또는 RT56의 “공식” 버전으로 표현하지 않는다.

원작 HOK는 [oixxta의 Hearts of Korea](https://steamcommunity.com/workshop/filedetails/?id=2898629778)다. 사용자가 밝힌 계승 경위는 원작자의 업데이트 중단에 따라 유지보수를 이어가며, 원작자가 돌아오면 협의할 예정이라는 것이다. 이는 현재 작업의 경위이며 원작자의 명시적 승인이나 저작권 이전을 뜻하지 않는다. 이번 작업에서는 커밋·푸시·Workshop 게시를 수행하지 않는다.
