# 한국 연구·장비의 일본식 명칭: 한영 현지화 수선 계획

작성: 2026-11-10, Asia/Seoul. 최초 단계는 문서화만 수행했다. 이후 별도 구현 승인과 외부 의존성 한 줄의 임시 변경·시험·복구 승인을 받았다. KO05의 동일 경로 병합+RTK 의존성은 관측9문구가 정상이었지만, 좁은17키로 줄인 v5는 KO06의 KLVT-2 전체 이름에서 다시 실패했다. **v6의 영어17키·RTK 동일 경로 한국어1,308키 병합·저장소 RTK 의존성 구현과 선택한 한영 구성의 범위 검증·임시 설정 복구·별도 승인된 외부 영구 동기화를 완료했다.** KO07·EN04에서 각각 수정15/17문구·보존3문구·JAP 대표7표시를 확인했으며1953년형2키는 소스 전용이다. 자체39/0·독립35/0, aggregate28 PASS/기존11 ERROR(exit1)를 구분한다. 언어당 변경17값이며 한국어 비대상1,291키·나머지 원문 바이트와 기존 gameplay를 보존한다. 광범위한 replace_path는 추가하지 않았다. 외부 등록파일을 원본304바이트로 복구한 뒤 별도 영구 승인으로 시험과 같은37바이트 의존성을 반영해 현재341바이트다. 나머지 사용자 metadata는 원본이며 저장82개는 보존됐다. 최종 정적·UI·복구·영구 적용 영수증과 EN03 중단·초기 실패 이력은 [구현 기록](../implementation/2026-11-10-korean-equipment-localisation-repair.md)을 따른다.

**아래 1–8절 전체는 최초 문서화 단계의 역사 기록이다.** 그 안의 ‘현재’, ‘아직 미적용’, ‘미실행’, ‘적용0개’, 추가4키의 ‘미확인’은 그 단계의 판단과 승인 범위를 뜻한다. 이후 구현·실행 결과로 소급해서 바꾸지 않으며 현재 상태로 사용하지 않는다. v1의886/0·후속 파일명/폴더 후보·v4/v5 정적 통과와 UI 실패, EN2 화면 유실·복구 한계는 위 구현 기록에서 구분한다. RTK 없는 한국어 구성은 v6의 보존·지원 확정 범위에서 제외한다. 1953년형2키는 현재 해금 경로를 확인하지 못해 소스 확인으로 한정하며 새 해금을 만들지 않는다.

한국 연구 화면·장비명이 일본식으로 보이는 현상을 조사하거나 이 계획을 구현하기 전에 [현지화 검토 스킬](../skills/hok-rt56-localisation-review/SKILL.md), [변경 영향 절차](../HOK_CHANGE_COVERAGE_REVIEW.md), [언어 계약 ADR-0003](../decisions/0003-localisation-contract.md), [한국 콘텐츠 소유권 ADR-0004](../decisions/0004-hok-korean-content-priority.md)를 읽는다. 생성 입력·영어 계층을 변경하기 전에는 [기존 영어 이식 기록](../implementation/2026-10-20-english-localisation-import.md)도 읽는다.

## 1. 최초 문서화 이력 — 승인 범위와 당시 판단

이 절의 문서 전용 범위와 아래의 미적용 계획은 최초 단계의 이력이다. 후속 사용자의 `AGENTS.md, /docs 읽고 구현해줘`와 실제 UI용 프로필 임시 변경·복구 승인 뒤의 작업은 구현 기록에 별도로 남긴다. 최초 문서 작업을 구현이나 실행 검증으로 소급하지 않는다.

사용자는 모든 현지화가 사라지는 문제가 아니라 **한국의 연구·장비 이름 일부가 일본식으로 나오는 문제**라고 범위를 구체화했다. 이후 **한국어와 영어를 함께 수정해야 한다**고 확인했으며, 현재 요청은 **문서화 작업만**이다. 한영 수정은 후속 구현의 요구사항이며 이번 문서 작업의 실행 승인이 아니다.

이번에는 이 계획, 문서 인덱스와 ADR-0003의 후속 안내만 편집한다. 실제 `.yml`, 기술·장비·history·생성기·잠금·원장·descriptor·플레이세트는 변경하지 않는다. 게임·테스트·validator·진단 helper를 실행하거나 시험 파일을 만들지 않는다. 이전 커밋·푸시 승인은 이미 완료된 산업 업데이트에 한정되며 이번 문서의 Git 작업을 승인하지 않는다.

- **CONFIRMED:** RT56 자체 영어와 RT56 한국어 번역이 한국 전용 `KOR_` 장비 키에 일본식 이름을 정의한다. 호환판은 같은 키에 다른 HOK 이름을 정의한다.
- **STRONGLY_SUPPORTED:** 이 상충 정의는 사용자가 설명한 차량·기계화·수륙양용 장비의 일본식 명칭을 설명하는 구체적인 원인 후보다. host 쪽은 `replace/`, 호환판 장비 파일은 일반 언어 폴더에 있다는 배치 차이도 있다.
- **UNPROVEN:** 사용자가 본 개별 화면의 최종 선택 키·물리 파일·설계명과, 후속 override 방식의 실제 승자. 실패 화면이나 그 상태를 이번에 직접 재현하지 않았다.
- 전차·공군·해군 전체가 같은 원인이라고 확대하지 않는다. 이름 수선은 장비 성능·연구 효과·전역 기술·지도 수선과 별개다.

## 2. 최초 문서화 이력 — 기준 소스와 위치

| 항목 | 이번 문서화 기준과 역할 |
|---|---|
| 호환판 | `C:\hoi\hearts_of_korea_Road_to_56`, `feat/korean-focus-update-20260922@2523bf455514c79a3538f0475dc922329afb185d`. 문서 편집 시작 시 작업 트리 깨끗함 |
| 읽기 전용 HOK donor | `C:\hoi\hearts_of_korea`, HEAD `596b221bb994d93fce552d3ee1ba70fa9b5640f1`. 산업·연구망의 기존 미커밋 8파일이 있으며 이번 대상 장비 파일의 변경은 아님 |
| 읽기 전용 RT56 | `C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968`. 설치 manifest `1963361040482473746`을 다시 읽음. 전역 파일 전체 해시 재검사나 새 실행 결과가 아님 |
| 읽기 전용 RT56 한국어 번역 | 같은 Workshop content 루트의 `2769576030`. 한국어 일본식 장비명 정의의 공급자 |
| 설치 HOI4 | `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\launcher-settings.json`의 `Operation Postern v1.19.4.2.2da5 (0bdb)`. 이번 실행 체크섬이 아님 |
| 사용자 데이터 | `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV`. 원본 로그·설정·저장 위치이며 쓰기 대상 아님 |
| 기존 생성 입력·영어 출처 | `tools/hok_source_lock.json`, `tools/hok_english_translation_lock.json`, `docs/upstream/hok-english-20261020/`. 과거 핀·보관 바이트를 유지 |

다음은 이번에 읽은 물리 입력의 SHA-256이다. 별도의 source capsule이나 시험 사본을 만들지 않았다. 원본·현재 출력·후속 생성 입력의 역할을 섞지 않는다.

| 루트·상대 경로 | SHA-256 |
|---|---|
| 호환판 `localisation/korean/korea_equipment_l_korean.yml` | `AE477E1CDF7E70CADABB794AEAF97D27C98C105FCF1691980991E24B3CCFA021` |
| 호환판 `localisation/english/korea_equipment_l_english.yml` | `A16E9093B1019657EA9FDB6BD8E1475FEFD0271801242D9371061518F1A9B062` |
| donor `localisation/korean/korea_equipment_l_korean.yml` | `AE477E1CDF7E70CADABB794AEAF97D27C98C105FCF1691980991E24B3CCFA021` |
| RT56 `localisation/english/replace/r56e_equip_motor_mech_l_english.yml` | `329F1A7AD9FEB8EF88155A52B4361A9103081EDE3A28D81E013C134E9DF5D0A5` |
| RT56 번역 `localisation/korean/replace/r56e_equip_motor_mech_l_korean.yml` | `322541C886E096ECDC4C6F9EEA9DCE36EDA29911010EEE3B7B4AB482C0072974` |
| RT56 `common/technologies/r56_vechicles.txt` | `65E523637AE9A305135BAEFF67443EBA20A372ECCC202D50CA87B2E626D19B98` |
| 호환판 `history/countries/KOR - Korea.txt` | `E6D2488E2A894AF9C3FA478815669175FAEA537B1A5BE7D09C61FCF1578C7068` |
| RT56 번역 `descriptor.mod` | `A0508F4A91AF911917AD3A84BF829CB38ED1557DD8F9643A010F1AEE36F48D6C` |

후속 구현 직전에 이 지문과 버전·실제 로드 구성을 다시 확인한다. source drift가 있으면 이번 행 번호·값을 최신 입력의 증거로 재사용하지 않는다.

## 3. 최초 문서화 이력 — 확인된 상충 정의와 사용처

host 영어 파일의 939–955행과 번역 한국어 파일의 707–722행·1301행에 같은 `KOR_` 키의 일본식 명칭이 있다. 호환판 한영 장비 파일의 121–136행·171–172행에는 대응 HOK 이름이 있다.

| 장비 키·계열 | RT56 영어 / RT56 한국어 번역 | HOK 영어 / HOK 한국어 |
|---|---|---|
| `KOR_motorized_equipment_1` | Type 94 / 94식 | Kia K-511 2½-Ton Truck / 기아 K-511 두돈반 |
| `KOR_mechanized_equipment_1` | Type 98 … So-Da / 98식 장갑병차 소다 | KHT-1 Half-Track / KHT-1 반궤도 |
| `KOR_mechanized_equipment_2` | Type 1 … Ho-Ki / 1식 장갑병차 호키 | KHT-2 Half-Track / KHT-2 반궤도 |
| `KOR_mechanized_equipment_3` | Type 1 … Ho-Ha / 1식 장갑병차 호하 | KAPC-1 Infantry Armoured Vehicle / KAPC-1 보병장갑차 |
| `KOR_amphibious_mechanized_equipment_1` | Toyota 4x4 Su-Ki / 토요타 4x4 스키 | KLVT-1 / KLVT-1 |
| `KOR_amphibious_mechanized_equipment_2` | Type 4 Ka-Tsu / 4식 카츠 | KLVT-2 / KLVT-2 |
| `KOR_motorized_rocket_equipment_1` | Type 5 Shi-Sei 150mm Tarenso / 5식 시제 150mm 다연장 | 기존 HOK의 KMRL-27 탑재 트럭 명칭. 한영 원문·짧은 이름을 각각 유지 기준으로 사용 |

이는 `JAP_` 키로의 fallback을 가정해야만 설명되는 상황이 아니다. **한국 자신의 `KOR_` 키가 일본식 이름을 직접 갖는다.** 한국어 번역을 끄는 것만으로 host 영어의 상충 정의까지 없어지지는 않는다.

연구 제목과 해금 장비 이름은 별도 사용처다. 예를 들어 RT56 번역 `research_l_korean.yml:313`의 `motorised_infantry`는 `차량화보병`이다. RT56 `common/technologies/r56_vechicles.txt`의 연결은 다음과 같다.

| 기술·소스 행 | 해금 장비 | 문서화 판단 |
|---|---|---|
| `motorised_infantry`, 73–76행 | `motorized_equipment_1` | 한국 장비명의 상충 키로 연결됨 |
| `mechanised_infantry`, 474–477행 | `mechanized_equipment_1` | 같은 연결 확인 |
| `mechanised_infantry2`, 670–673행 | `mechanized_equipment_2` | 같은 연결 확인 |
| `mechanised_infantry3`, 711–714행 | `mechanized_equipment_3` | 같은 연결 확인 |
| 수륙양용 기술 블록, 560–563행 | `amphibious_mechanized_equipment_1` | 같은 연결 확인 |
| `mechanised_infantry_a`, 761–765행 | `mechanized_equipment_x` | RT56 추가형의 해금 확인. HOK 대응 이름은 미결 |

일본식으로 보이는 것이 기술 제목인지, 해금 장비의 전체/짧은 이름인지, 생산·설계창의 저장된 이름인지 먼저 식별한다. 같은 화면에 여러 종류의 이름이 함께 나타날 수 있다. 위 연결은 소스 근거이며 실제 UI가 어느 키를 최종 선택했는지의 관측은 아니다.

## 4. 최초 문서화 이력 — 변경 영향 대장·좁은 후보20키

아래 수는 언어당 고유 논리 키의 합집합이다. 한영 파일 수나 실제 화면 수, 오류 발생 횟수가 아니다. `1/2/3` 등은 각 키를 나열한 표기이며 실제 키를 슬래시 포함 문자열로 만들지 않는다.

| 후보·수 | 기대 의미와 사용 경로 | 처리 | 현재 근거·남은 항목 |
|---|---|---|---|
| `KOR_motorized_equipment_1` — 1키 | K-511 트럭. 차량화 연구의 해금 장비·장비 이름 | **수정 제안** | 양 채널 상충 정의 확인. 실제 화면 승자와 공급 파일 확인 대기 |
| `KOR_mechanized_equipment_1`, `_2`, `_3`와 각각의 `_short` — 6키 | KHT-1·KHT-2·KAPC-1. 기계화 연구/생산의 전체·짧은 이름 | **수정 제안** | 양 채널 상충 정의 확인. 긴 이름만 수정해 짧은 이름을 남기지 않음 |
| `KOR_amphibious_mechanized_equipment_1`, `_2`와 각각의 `_short` — 4키 | KLVT-1·KLVT-2 | **수정 제안** | 양 채널 상충 정의 확인. 해당 기술·장비 표시를 연결해 확인 |
| `KOR_motorized_rocket_equipment_1`, `_short` — 2키 | 기존 HOK KMRL-27 탑재형과 짧은 이름 | **수정 제안** | 영어 939–940행, 한국어 707·1301행. 분산된 짧은 이름도 포함 |
| `KOR_mechanized_equipment_x`, `_short`, `KOR_mechanized_equipment_x_2`, `_short` — 4키 | RT56 추가 기계화형의 한국 명칭 | **미확인** | host에는 일본식 값, HOK에는 대응값 없음. `_x` 해금은 확인. `_x_2`는 장비 정의가 있으나 현재 기술 소비 경로·실제 표시를 확인하지 못함. 이름을 임의 확정하지 않음 |
| `KOR_motorized_equipment_0`, `_short`, `KOR_motorized_equipment_1_short` — 3키 | K-311·K-511의 기존 HOK 명칭 | **의도적 유지** | 조사한 host의 동일 키 상충 정의는 없음. 한영 이름 묶음의 회귀 확인 대상으로 유지 |

합계는 **상충 정의 13키의 수선 제안 + 미확인 4키 + 의도적 유지 3키 = 20키**다. 이번에 실제 적용된 수정은 0개다. 이 정확한 ID들의 별도 `_desc`는 확인한 파일에서 찾지 못했지만, 이를 필수 누락으로 계산하거나 빈 설명을 추가하지 않는다. 설명이 실제로 요청되는 화면과 generic 설명 공급자를 확인한 뒤 필요한 것만 다룬다.

별도로 다음 경로는 보존 또는 확대 조사 대상으로 구분한다.

| 경로·영역 | 처리와 이유 |
|---|---|
| generic 기술 이름·설명, 기술 효과와 해금·장비 성능 | **제외·보존.** 한국 장비 이름 수선 때문에 전역 `motorised_infantry` 등을 바꾸지 않음 |
| `JAP_` 및 다른 국가 키·RT56 세계 번역 | **제외·보존.** 원본 파일이 남아 있어도 잘못된 override로 비한국 표시가 달라질 수 있으므로 후속 보존 확인 필요 |
| NSB 전차 설계기 | **미확인.** `NSB_armor.txt:165–171/551–558`은 chassis ID를 해금. 기존 `KOR_light_tank_equipment_*`만 수정해 설계기 chassis 표시까지 해결됐다고 하지 않음 |
| BBA 항공기 | **미확인.** `plane_airframes.txt:196/214`와 `x_plane_airframes.txt:39–43`의 `derived_variant_name` 등 별도 경로. 일부 초기 HOK 파생형 이름 부재만으로 일본식 표시를 확정하지 않음 |
| 해군·기존 설계명 | **미확인·현행 보존.** `history/countries/KOR - Korea.txt:274–370`의 Type II-K·Donghae·Incheon·Yi Sabu, 394–406행의 KA-30·KP-33 같은 명시 이름은 기본 현지화 키와 별도. 저장된 variant·노획/면허 장비까지 자동 개명하지 않음 |
| 한국 공군·해군의 일반 장비 현지화 | **현재 수선 범위에서 제외.** 조사한 동일 KOR 항공장비 키의 일본식 host 정의를 확인하지 못함. 구체적인 실패 항목을 확보하면 다시 추적 |

## 5. 최초 문서화 이력 — 당시 미적용인 한영 후속 구현 원칙

1. 한국어·영어를 한 쌍으로 다룬다. 기존 HOK의 한국어 값과 영국 영어 값을 각각 유지 기준으로 사용하고, 영어 파일에 한국어 본문을 복사하지 않는다. 키·대상·숫자·치환 의미는 대응시키되 번역 본문의 동일 바이트를 요구하지 않는다.
2. 승인된 HOK 장비명과 상충하는 `KOR_` 키만 좁게 재정의한다. 후보 위치는 호환판의 `localisation/korean/replace/`와 `localisation/english/replace/`이다. 예시 파일명 `HOK_KOR_equipment_overrides_l_korean.yml`과 영어 대응은 **제안 경로이며 현재 생성되지 않았다**.
3. host에도 `replace/` 정의가 있으므로 파일을 옮기거나 복제하는 것만으로 최종 우선권을 보장하지 않는다. 실제 선택 경로를 확인해 필요한 최소 전략을 결정한다. 동일 경로의 host 병합이 필요하다는 증거가 나오면 비한국 전체 값 보존·새 source pin·귀속/재배포 조건을 검토한 별도 통합 결정을 먼저 기록한다.
4. 기존 한영 장비 파일은 생성 출력이다. `tools/hok_source_lock.json:4952/5042`의 기본 핀과 `tools/hok_english_translation_lock.json:438–450/616`의 영어 출력·한국어 보존 계약을 직접 새 값으로 덮지 않는다. `tools/source_snapshot.py`의 영어 계층, `tools/build_korean_focus_update.py:435–440`, `tools/build_integration_manifest.py:925` 이후의 출처 처리를 함께 추적한다.
5. 후속 구현에서는 선택 원본·현재 포트의 보관 바이트, 한영 확정값, 생성·최종화·필요한 정확 역투영, 개별 출력의 통합 분류와 원장을 재현 가능하게 연결한다. 새 말단 계층이나 다른 방식의 선택은 구현 시 검토 사항이며 이번 문서가 새 도구/잠금을 만든 것은 아니다. 과거 핀을 면제하거나 출력만 수동 수정하지 않는다.
6. RT56 추가형 4키는 한국 이름·실제 사용처를 결정한 뒤 해당 범위에 포함한다. HOK 원본에 없는 이름을 이번 문서가 승인한 것처럼 사용하지 않는다. 안정 ID·성능·연구 시간·해금·AI·저장된 설계명은 별도 승인 없이 변경하지 않는다.

## 6. 최초 문서화 이력 — `dependencies`, 두 종류의 replace, `zz_` 판단

- `dependencies`는 모드 간 관계, descriptor의 `replace_path`는 경로별 파일 구성, 언어 폴더의 `replace/`는 현지화 재정의 배치다. 어느 한 설정을 다른 단계의 모든 우선순위와 동일시하지 않는다.
- 현재 호환판은 `The Road to 56`과 `Korean Language`를 선언하고, 실제 검토된 한국어 실행은 `The Road to 56 Korean Translation`을 사용했다. 최종 언어 계약은 [ADR-0003](../decisions/0003-localisation-contract.md)의 미결정 사항이다. 이번 장비명 충돌은 host 영어에도 있으므로 그 자체로 dependencies 변경이나 RT56 번역의 필수 의존성화를 확정하지 않는다.
- RT56 번역의 `replace_path="localisation"` 선언은 존재하지만 이것만으로 HOK 파일 전체가 사라졌다고 하지 않는다. [과거 fixture-04-ko 기록](../implementation/2026-11-08-hok-upstream-content-port.md#fixture-04-한국어-실행-결과)에는 같은 manifest196에서 번역 활성 상태로 HOK 전용 한국어 결정13개와 회복 사건이 표시된 근거가 있다. [한국어 C1 기록](../implementation/2026-11-07-korean-state-split-port.md)도 선택한 HOK 표시의 공존을 기록한다. 이는 해당 실행·키의 공존이지 모든 키의 우선권 증거가 아니다.
- `zz_`·`zzz_`는 우리 대상 빌드에서 동일 키의 승리를 보장한다고 입증되지 않았다. 파일명 정렬, 런처 화면 번호, 선택 배열 또는 `Active Mod`의 열거 순서만으로 현지화의 승자를 확정하지 않는다. `replace/`끼리의 동일 키 충돌도 실제 확인이 필요하다.
- 기본 방향은 본체의 자체 한영 HOK 문구와 선택한 RT56 한국어 번역의 공존이다. 광범위한 `replace_path="localisation"`을 우리 호환판에 추가·확대하거나 RT56/번역 원본을 수정하는 계획은 채택하지 않는다. 일부 화면 문제만으로 전체 번역 복사나 모든 HOK locale을 중복하는 별도 bridge를 확정하지 않는다.

## 7. 최초 문서화 이력 — 당시 미실행인 후속 검증 계약

구현·필요한 실행이 승인된 다음에 수행할 항목이다. 새 시험·진단 helper, 출력·백업·로그/화면 사본은 시작 전에 정한 `C:\hoi\test\<task-or-run-id>\`에 두며 이번 문서 작업에서는 그 폴더나 자료를 생성하지 않는다.

| 확인 단계 | 필요한 확인과 완료 기준 |
|---|---|
| 기준 고정 | 버전·RT56/번역 지문, 실제 물리 포트·선택 모드·DLC·언어·기존 저장/새 게임을 같은 실행 기준으로 기록. 현재 설정을 이전 로그의 설정으로 간주하지 않음 |
| 소스·재현 | 20키의 수선/유지/미확인을 각각 정리. 한영 키·전체/짧은 이름·실제 필요한 설명·BOM/헤더/줄 끝·토큰·의미와 consumer 연결 확인. 기존 생성 계약·pins·다른 runtime 보존 및 필요한 정적 gate를 실행하고 기존 오류와 새 오류를 구분 |
| 영어 UI | RT56 단독 대조와 RT56+호환판에서 같은 KOR 기술/장비 항목 비교. 일반판 영어 번역이나 한국어 전역 번역을 불필요하게 섞지 않은 구성에서 HOK 영어 이름 확인 |
| 한국어 UI | 같은 소스·언어·화면에서 RT56+호환판과 RT56+선택 한국어 번역+호환판을 비교. 한 번에 언어와 모드 여부를 모두 바꾸어 원인을 단정하지 않음 |
| 화면별 이름 | 기술 제목/설명, 해금 장비의 전체·짧은 이름, 생산·설계창·재고/부대 툴팁 중 실제 관련 소비자를 각각 관측. 하나의 정상 이름으로 다른 키까지 통과 처리하지 않음 |
| 소비자·출처 분리 | 실제 요청 키가 KOR용인지 generic/JAP/노획·면허·명시 variant 이름인지 구분. 원시 ID·영어 fallback·일본식 번역·항목 부재를 같은 증상으로 합치지 않음 |
| 비한국 보존 | 원본 RT56·번역 파일의 무수정과 함께 변경 키 allowlist 밖의 정의를 보존. 일본과 관련 타국의 연구/장비 표시를 대표 화면에서 확인. 파일 무수정만으로 유효 로드·문구 보존을 주장하지 않음 |
| 저장·한계 | 새 설계와 기존 저장의 설계명을 구분. 기존에 저장된 사용자/명시 variant 이름 자동 변경이나 기존 저장 호환을 이번 locale 수선으로 보장하지 않음. 로드·UI·게임 효과·저장 증거를 따로 기록 |

해당 검증이 끝나기 전 완료 표현은 **수선 계획 문서화**, 후속 코드 적용 뒤에는 **구현 반영 / UI 검증 대기**로 한정한다. 이전 산업 업데이트의 정적219/0·aggregate27/0/11과 과거 C1의 일부 정상 표시를 이 수선의 검사 결과로 가져오지 않는다.

## 8. 최초 문서화 이력 — 실제 확인과 정리 미결

실제 수행한 것은 프로젝트 지침·유지 기록·현지화·기술·history·descriptor 원문과 선택 파일의 SHA-256을 읽고, 이 문서의 키·경로·상태 구분 및 문서 링크를 검토하는 일이다. 실행 재현, UI 확인, 게임 테스트·validator·생성기·진단 스크립트는 새로 수행하지 않았다. 따라서 원인 후보와 후속 동작은 위 한계 안에서만 기록한다.

기존 `tools/__pycache__/`는 **21파일·1,088,888바이트**이며 정리 미결이다. `.local-artifacts`는 없다. 이번 작업에서는 이동·삭제·새 시험 자료 생성이나 외부 cache/archive 위치 변경을 하지 않았다. 문서 외 runtime·잠금·원장·설정·Git index/branch/HEAD는 변경하지 않는다. 커밋·푸시·배포는 하지 않는다.
