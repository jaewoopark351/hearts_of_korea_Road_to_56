# 2026-09-22 한국 업데이트 런타임 증거

상태: **초기 대조·첫 수선 실패와 기본 fixture 118 PASS·1 FAIL·7 SKIP 보존 / NEP alternate 134 PASS·0 FAIL·0 SKIP / 임시 파일 없는 한국 UI 진행 확인 / 최종 정적 20 PASS**. clean 실행 후반 로그는 다른 프로세스가 덮어써 전체 오류 집계가 불가능하다. fixture의 통과를 전체 플레이·릴리즈 검증으로 확대하지 않는다. 구현 범위는 [구현 기록](../implementation/2026-09-22-korean-focus-update-port.md), 입력 변경은 [기준선 감사](2026-09-22-source-rebaseline.md)를 따른다.

## 기준선과 증거 보존

| 항목 | C1 관측값 |
|---|---|
| 실행 | 사용자가 2026-09-22 00:48:55 KST에 시작한 `hoi4.exe`, PID `46824` |
| 엔진 | `Operation Postern v1.19.3.0.c01a (940d)`, build `2026-09-09 09:10:08` (`system.log:273`) |
| 호환판 | `main@bfbba43c26022f3f64a88c2f1ec6600cb7f0d06f` + 한국 업데이트와 호스트 재기준화의 미커밋 변경; MAN 참조 수선 전 |
| 고정 donor | base `887930f6e88c80568d62dab9cfbe1ba8a498a252`, 한국 콘텐츠 `da815305e3ce00186a487b3a378bf8536ff59146`, 역사 AI `118d7b53dfdbc120fcfe4b9d6792e66b2b519be7` |
| RT56 | item `820260968`, manifest `7475007536894105204`; C1 조사에서도 manifest 동일 |
| 활성 구성 | RT56 + RT56 Korean Translation `2769576030` + 로컬 호환판 `3796816200`; donor와 Korean Language `2743487021`은 활성 목록에 없음 |
| 실제 경로 | 호환판 `C:/hoi/hearts_of_korea_Road_to_56`; RT56와 번역은 Steam `workshop/content/394360/820260968`, `2769576030` |
| DLC·언어 | 활성 DLC 36개, 비활성 DLC 목록 `[]`; La Resistance·No Compromise, No Surrender·No Step Back·By Blood Alone 포함. 전체 이름은 `system.log:276–311`; 설정 `language="l_korean"` |
| 사용자 데이터 | `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV` |

보존 위치는 `.local-artifacts/runtime/2026-09-22/C1-initial/`이다. `logs/system.log`, `game.log`, `error.log`, `setup.log`, `dlc_load.json`, 실제 launcher descriptor 3개와 `snapshot-index.json`을 저장했다. 여기서 `initial`은 첫 C1 프로세스를 뜻하며 **00:57:16 임시 저장 재로드 오류까지** 포함한다. 네 로그 모두 복사 전후 크기와 수정 시각이 같았다. 로그 인용의 줄 번호는 이 보존본 기준이다. 스크린샷을 독립 판독한 기록이 아니라 실행 담당자의 UI 관측을 전달받은 부분은 아래에서 구분한다.

`dlc_load.json` 배열은 호환판 → RT56 → 번역이고, 엔진의 활성 모드 이름은 RT56 → 번역 → 호환판이다(`system.log:312–314`). 이 목록 순서를 전체 데이터베이스의 유효 덮어쓰기 순서로 단정하지 않는다. 호환판 descriptor는 여전히 `Korean Language`를 요구하지만 이 실행은 RT56 Korean Translation을 사용했다. 번역의 `replace_path="localisation"`을 포함한 최종 의존성 계약은 해결되지 않았다.

| 보존 파일 | SHA-256 |
|---|---|
| `logs/system.log` | `3377CBCF3B1E93B23003DA7049EB6108DAF3ABAFCE29238CC4790AE5384A5338` |
| `logs/game.log` | `FE42E7BFC57842B70A769B2B3978B5AD5B764CB12206A4EE0C79C49297A6505E` |
| `logs/error.log` | `3A0654E3EB5E2AEB7333EA2EC4503DC10C6E91292325BC19BAE581FE834CF799` |
| `logs/setup.log` | `36B7B3B19374F25E0B9D852AB6BFB525B44EC8237C92C86E3771C6B0681DCB34` |

## 확인된 로드와 진행

- **CONFIRMED — 로그:** `game.log:2`의 00:49:19에 province 13,569개 로드, `:4–5`에서 history 실행, `:8`에서 1936 singleplayer 시작, `:12`의 00:49:52에 `End RestoreDeviceObjects`까지 진행했다. `:15`에는 `1936.01.02.05`의 게임 효과 실행이 기록됐다.
- **CONFIRMED — 로더 기록:** 신규 국민정신 29개(`setup.log:1184–1186`), 결정 분류 3개(`:1537–1538`), 결정 10개(`:1674–1675`), 이벤트 6개(`:2306`), 관계 수정치(`:568`) 및 한국 역사 AI 파일(`:2145`)이 로드됐다. AI 행의 `#304`는 전체 누적값이므로 한국 계획 개수로 해석하지 않는다. 파일 등록은 모든 효과·조건의 실제 실행 증거가 아니다.
- **실행 담당자의 UI 관측:** KOR 선택·일시정지 지도 진입 후 +1일과 +7일을 지나 `1936.01.16 07`에 일시정지했다. `공화국의 미래` 중점 완료와 이벤트 표시를 확인했다. 이어 새 임시 세이브를 같은 프로세스에서 다시 불러와 같은 날짜·한국 정치 화면이 유지된 것을 확인했다. 중점 326개 전체, 신규 보상 전체 또는 역사 AI 계획을 검증한 것은 아니다.
- **오류 검색의 한계:** 보존 `error.log`는 물리 1,127행·시각이 붙은 레코드 1,110개다. 신규 `HOK_KOR`, 한국 focus/history/AI 경로, 폐기 수송기 키 및 과거 map/port/한국 sound 오류 패턴은 검색 0건이었다. 다른 호스트·그래픽·파서 오류는 남아 있어 전체 오류 0건이라는 뜻이 아니다.
- 조사 시 PID 46824가 살아 있었고 crash 디렉터리에는 하위 폴더가 없었다. 이 C1은 9월 6일의 새 게임 시작 직후 실패 지점을 넘어 진행했지만, 이전 실행과 엔진·호스트가 달라 **과거 크래시 원인을 특정 수선 하나로 확정할 수 없다**.

## 분리해서 다룰 오류

| 분류 | 증거와 판정 | 다음 판별 |
|---|---|---|
| 기존 한국 registry 통합 누락 | **CONFIRMED:** `error.log:699`부터 `MAN.txt:559,584`의 `has_idea = kim_chang_ryong` 오류 408건(559에서 15건, 584에서 393건). RT56 `common/characters/KOR.txt:539–588`의 캐릭터가 `:552`에 해당 idea token을 정의하지만 포트의 동일 경로 파일은 그 블록을 포함하지 않는다. | R0에서는 0건. **첫 수선 실패:** host 블록 정의만 복원하고 모집하지 않은 C0에서도 같은 오류가 반복됐다. 정의 복원만으로 idea 참조가 유효해진다는 가설은 이 실행에서 **DISPROVEN**이다. |
| 저장·로그 이름 변경 실패 | **CONFIRMED:** `error.log:1107–1109`의 `errno 2`: `continue_game.temp → continue_game.json`, `KOR_1936_01_16_07_temp.hoi4 → KOR_1936_01_16_07.hoi4`, `random.log → random_1.log`. 새 `_temp.hoi4`는 51,390,883 bytes로 존재하고 UI 재로드는 진행됐다. 정상 이름으로 저장 완료한 결과는 아니다. | **CONFIRMED:** R0에서도 세 종류 모두 재현되어 포트가 없어도 발생한다. OneDrive·경로·환경의 구체적 원인은 **UNPROVEN**이며 기존 세이브를 수정하거나 이름을 바꾸지 않는다. |
| PRC advisor 재로드 오류 | **CONFIRMED:** `error.log:1110–1127`, `PRC_luo_ruiqing`에 advisor 정의가 없다는 오류 18건. 포트에는 해당 토큰이나 `common/characters/PRC.txt`, `history/general/china_shared_advisors.txt`가 없다. | **CONFIRMED:** R0 재로드에서도 18건 재현. 한국 업데이트가 없어도 발생하는 host 실행 문제다. NCNS 캐릭터 분기와 공용 advisor 생성의 원인 연결은 **STRONGLY_SUPPORTED**로 유지한다. |

MAN 누락의 포트 파일은 현재와 `bfbba43`의 Git blob이 모두 `4265ac6670e75098c5d05cb2287ec3bc9e3fad4d`다. 이번 한국 업데이트가 이 정의를 삭제한 것은 아니다. 다만 구 RT56 KOR/MAN 원본 전체를 확보하지 않았으므로 9월 6일에도 같은 런타임 오류가 있었다고 소급 확정하지 않는다. 현 RT56 KOR SHA-256은 `979185140DA5A9CA57AC8399A47DA5EBFA9157C9FD2F2AACBD51E7E4E8C078CA`, MAN은 `CFE4943CF980417F047F90E920B1171E1ABBBF1647AEF1E7DC58AE37B7F53BF0`다.

PRC의 현 RT56 `common/characters/PRC.txt:470`은 NCNS 활성 instance(`:473`)에 commander만 두고, advisor는 NCNS 비활성+La Resistance instance(`:494–525`)에 둔다. 반면 `history/general/china_shared_advisors.txt:81–108`은 NCNS 분기 없이 동일 `token_base`로 advisor를 생성한다. 이 연결은 원인 가설의 근거이며 실제 저장 로더 내부 동작을 입증하지 않는다.

## R0: RT56-only 대조

별도 launcher playset `HOK RT56 Audit R0 20260922`에서 실행했다는 담당자의 UI 관측과 실제 `dlc_load.json`의 `mod/ugc_820260968.mod` 한 개가 일치한다. 프로세스 PID `33360`의 시작 시각은 01:05:24 KST이며 첫 defines 기록은 01:05:28이다. 활성 DLC 36개와 `l_korean` 설정은 C1과 같고, 번역 모드·호환판·donor는 비활성이다. `system.log:273`은 같은 엔진 빌드에 체크섬 `c8ff`, `:275,312`는 활성 모드 1개 RT56을 기록한다. RT56 manifest, KOR/MAN source SHA-256 및 donor HEAD `81d39fadab9aaf75f3eb86873b39d2bec65c48d4`를 다시 읽었으며 앞선 조사와 같았다.

`game.log:2`는 01:05:46에 host province 13,535개, `:8`은 01:07:03 singleplayer 시작, `:12`는 01:07:11 `End RestoreDeviceObjects`를 기록한다. 실행 담당자는 GER·보통 난이도·역사 AI를 선택하고 `1936.01.18 05`까지 진행한 뒤 일시정지했다고 보고했다. 없는 이름임을 확인한 후 생성한 `GER_1936_01_18_05_temp.hoi4`는 50,704,429 bytes다. 같은 프로세스에서 이를 다시 불러와 동일 날짜·일시정지 지도와 정치력 41이 유지된 것을 UI로 확인했다. 이 역시 정상 이름 저장이나 cold reload 통과를 뜻하지 않는다.

보존 위치는 `.local-artifacts/runtime/2026-09-22/R0/`이다. `logs/`의 네 로그와 `snapshot-index.json`을 추가했다. 이 디렉터리에 있던 사전 준비용 설정은 보존하고, **실제 로드 구성은 `observed/dlc_load.json`과 `observed/mod/ugc_820260968.mod`**에 따로 복사했다. 네 로그 모두 복사 중 크기·수정 시각이 같았다.

| R0 보존 파일 | SHA-256 |
|---|---|
| `logs/system.log` | `DB00705964203CE5E7A92BE054FA0B10D98414821D9D5DEB1279E6806BE761E2` |
| `logs/game.log` | `016A6DED3379DACCE9867A27E05FC5BF3937D0A0D1591AE3F5C7B5250A2A8F31` |
| `logs/error.log` | `50734271B53F125FF1F43C3E0EC8AF7880504CCE220AFC7F08274C99BAA3962A` |
| `logs/setup.log` | `3D60D6563048DFECFCE2EDC10CE08C401C8011EE7C7EE92E0A18ABC7F16B6B23` |

R0 보존 오류는 물리 760행·시각 레코드 743개다. `kim_chang_ryong` 오류는 0건, 재로드의 `PRC_luo_ruiqing` 오류는 18건(`error.log:741–758`)이다. 이름 변경 실패는 세이브·continue 각 1건(`:738–739`), random 로그 3건(`:740,759–760`)으로 총 5건이다. 같은 환경에서 포트를 비활성화해도 PRC와 파일 이름 변경 문제가 재현되므로 이 둘을 한국 콘텐츠 수선으로 처리하지 않는다.

시작 단계만 비교하려고 C1은 첫 MAN 오류 직전 698행, R0는 첫 저장 오류 직전 737행으로 범위를 고정했다. 시각·게임 날짜를 제거한 시각 레코드의 고유 문자열은 **공통 647종**, R0에만 38종, C1에만 1종이다. R0에만 있는 38종은 `l_korean` 상태에서 번역 모드 없이 발생한 현지화 키 오류이며, C1에만 있는 1종은 `Sinarirang` 44.1kHz 음악 권고다. 초기의 나머지 다수 그래픽·파서 오류는 이 RT56-only 대조에서도 관측됐다. 이 비교는 다중 행 메시지 전체·반복 횟수·플레이 중 모든 오류의 동등성을 증명하지 않는다.

## C0-GER-first: 첫 MAN 수선의 실패

R0 playset을 복제하고 호환판만 추가한 구성이다. 실제 `dlc_load.json`은 `mod/ugc_820260968.mod`, `mod/hearts_of_korea_Road_to_56.mod` 두 개와 `disabled_dlcs: []`이며 번역·donor는 없다. PID `31036`은 01:16:43 KST 시작, `system.log:273`은 동일 엔진 빌드·체크섬 `30e5`, 활성 DLC 36개·모드 2개를 기록한다. `game.log:2`에서 province 13,569개와 history 완료를 확인했다.

이 실행에는 `common/characters/zz_hok_rt56_kor_host_references.txt`가 포함됐다(SHA-256 `40ED38039B49E32CC20A9789D9B9D0EFB443414DEF925647362C5E8EC8DE2AEF`). 첫 수선은 RT56 `KOR_kim_chang_ryong` 캐릭터 블록을 그대로 정의하되 한국에 모집하지 않는 방식이다. **메뉴 초기 오류가 0건이었던 것과 달리, 시간 진행 후 기존 MAN의 `has_idea` 오류가 계속 발생했다. 따라서 수선 성공으로 판정하지 않는다.** 현재 파일과 첫 수선의 정적 통과 여부는 엔진 실패를 대체하지 않는다.

초기 C0 741행과 R0 초기 737행의 시각·게임 날짜를 제외한 고유 레코드를 비교하면 R0의 685종이 모두 C0에 있고, C0에만 `Sinarirang` 음악 권고 1종이 더 있다. 초기 메뉴 확인만으로 반복 평가 시점의 오류 부재를 증명할 수 없음을 이번 실행이 보여준다.

실행 담당자의 마지막 UI 관측은 GER `1936.01.28 24`이다. 이후 일시정지 클릭은 **실행되지 않았으며**, 사용자가 ESC로 컴퓨터 조작을 중단했다. 감사자는 추가 UI 조작·일시정지·프로세스 종료를 하지 않았다. 보존 시점에도 PID 31036은 살아 있었고, 오류 로그의 게임 날짜는 이미 `1936.03.03.20`까지 진행했다. 로그 날짜를 마지막으로 확인한 일시정지 UI 날짜로 표현하지 않는다.

`.local-artifacts/runtime/2026-09-22/C0-GER-first/`에 주요 로그 4개·실제 `dlc_load.json`·descriptor 2개·해시 인덱스를 보존했다. `error.log`는 실행 중 증가하여 `StableDuringCopy=false`였다. 무한히 따라 읽지 않고 **복사 시작 시점 길이 423,289 bytes까지만** 보존했으므로 종료 로그가 아닌 유한한 실행 중 증거다. 다른 세 로그는 복사 중 크기·수정 시각이 같았다.

보존 오류는 물리 2,419행·시각 레코드 2,402개이며 `kim_chang_ryong`은 **1,678건**(MAN 559에서 60건, 584에서 1,618건)이다. 마지막 행은 01:21:55의 `1936.03.03.20` 오류다. PRC·파일 이름 변경 오류는 이 보존본에서 0건이지만 C0 저장·재로드를 하지 않았으므로 이 두 문제가 해결됐다는 의미는 아니다.

| C0-GER-first 보존 파일 | SHA-256 |
|---|---|
| `logs/system.log` | `40D044F3ABFA1D080738F4FA130DDA5F72C6DA82DE3C6A18D9A04EAA8E363354` |
| `logs/game.log` | `A8FA5F8513AA73CC15D4C07C58826E3EB6DE2442FEA4FD8C08EF9D42E4DD2EBE` |
| `logs/error.log` | `54D93AF0142DFF68F8A3FBF4AE96C753165F6E2A3A5D13563BFAB39A8C37642B` |
| `logs/setup.log` | `1E54DBC1CEB28AD01F1B7027CB9FFFE8490EF0E58A9ED7939FBE24C1FA951307` |

향후 대체 조건 검토에서도 `has_active_advisor`를 추측해 도입하지 않는다. 현재 vanilla/RT56 텍스트와 설치된 trigger 문서에서 그 이름의 정의·용례를 찾지 못했다. 설치 `documentation/triggers_documentation.md:5645`의 `is_hired_as_advisor`, `:6106`의 `is_political_advisor`는 **character scope**의 문서화된 trigger다. 미모집 캐릭터의 유효한 scope 진입과 기존 MAN의 한국 고용 여부 조건 보존을 별도로 입증한 후 검토해야 하며, 이번 감사에서 대체 코드를 작성하거나 실행하지 않았다.

## 재개 승인 전: 후속 MAN 후보와 임시 한국 검증 준비

이 절은 PC 재개 승인 전 준비 시점의 기록이다. 이후 생성·실행 결과는 다음 절에 추가한다.

첫 수선 실패 후 `tools/build_shared_overrides.py`에 두 번째 후보를 준비했다. RT56 MAN 전체를 고정 해시로 읽고 `MAN_kim_chang_ryong`의 한국 조건 두 곳만 바꾼다. `has_character = KOR_kim_chang_ryong`인 경우에만 character scope에 들어가 `is_hired_as_advisor = yes`를 부정한다. 한국이 인물을 보유하지 않거나 고용하지 않았으면 기존 MAN 조건을 허용하고, 고용했다면 차단하려는 변경이다. HOK에 인물을 새로 모집하거나 MAN의 다른 보상·역할을 바꾸지 않는다.

현재 설치 vanilla `common/national_focus/norway.txt:372–378`의 `if`/`has_character`/`is_hired_as_advisor` 조합, `common/characters/ENG.txt:15–59`의 advisor 조건부 trigger, `common/characters/DEN.txt:1694`의 부정된 character 고용 검사를 문법 근거로 확인했다. 생성기는 두 조건을 원복했을 때 RT56 원문과 같음을 검사한다. 메모리에서 후보를 생성해 입력 해시와 괄호 검사를 통과했으며 후보는 34,143 bytes, SHA-256 `461D54C88101CBAD78D98706D4ADA5F9F255A63F1AD977D983D9E2654BD83603`이다. **production `common/characters/MAN.txt`는 아직 생성하지 않았고 이 후보의 aggregate 검사·엔진 검증은 미실행이다.** 첫 수선 시점의 `20 PASS`를 이 후보의 통과 기록으로 사용하지 않는다.

사용자는 donor에서 썼던 임시 테스트 코드의 작성·실행·제거 방식을 요청했다. donor의 `docs/incidents/2026-09-21-korean-focus-expansion.md`와 `.local-artifacts/incidents/2026-09-21-korean-focus-expansion/RUNTIME/`에 보존된 one-shot `on_startup`/hidden-event fixture를 확인했다. 그 초기 확장 검증의 `104 PASS`는 이번 호환판이나 이후 보상 변경의 검증 결과가 아니다. 호환판용 후보는 `.local-artifacts/runtime/2026-09-22/harness/`에서 준비하며, 별도 새 한국 게임과 현재 지도 ID를 사용한다. 테스트 중 강제 중점 완료는 정상 선행 조건·35일 진행의 증거와 구분한다.

임시 후보는 두 모드로 생성했고 `harness/static-review.json`에 정적 결과를 기록했다. 두 모드 각각 중점 58개, 합집합은 신규 60개이며 기본 모드는 hidden event 7개·약 185일, 대안 모드는 3개·약 3일이다. 20개 한국 production 입력의 해시 불변, 후보 파일 해시·괄호·구문 구조와 중복 없는 이벤트 ID를 확인했다. 게임이 읽을 `common/on_actions/zz_hok_rt56_test_runtime.txt`, `events/zz_hok_rt56_test_runtime.txt`는 아직 배치하지 않았다. 실행·삭제 절차는 `harness/README.md`, 후보 파일과 제거 시 대조할 해시는 `harness/manifest.json`에 남겼다. 생성 도구 실행과 후보 정적 통과를 엔진 검증으로 집계하지 않는다.

PC 제어 재연결은 자동 승인 심사에서 거부됐다. 이유는 앞선 물리 ESC 중단 상태가 유지된다는 것이며, 이후 우회 조작·프로세스 종료 없이 저장소 안의 준비 작업만 진행했다. 실행 파일 배치와 게임 재시작은 PC 제어 재개 승인을 받은 뒤 수행할 단계다.

## C1-KOR-harness-default: MAN 후속 조건과 한국 기본 fixture

앞선 ESC 중단과 UI 재연결 거부 이후 사용자 재개 승인을 받았고, 게임 종료 확인 뒤 MAN 후속 조건을 생성했다. `common/characters/MAN.txt`는 고정 RT56 원본의 두 KOR 조건만 `if / has_character / NOT / KOR_kim_chang_ryong / is_hired_as_advisor`로 바꾼다. 한국 인물을 모집하지 않으며 나머지 MAN 내용과 별도 KOR 정의는 그대로다. fixture 설치 전 aggregate는 `20 PASS / 0 WARNING / 0 ERROR`였고 `.local-artifacts/audits/2026-09-22/static-validation-man-guard.txt`에 보존했다.

임시 `common/on_actions/zz_hok_rt56_test_runtime.txt`와 `events/zz_hok_rt56_test_runtime.txt`를 사용하는 폐기용 새 한국 게임을 실행했다. 실제 활성 구성은 RT56+RT56 Korean Translation+호환판의 C1이며, playset 이름에 C0가 남아 있어도 실제 세 모드 구성으로 분류한다. `system.log:273,312–314`는 엔진 `1.19.3.0.c01a (2d4b)`와 이 구성을 기록한다. fixture가 중점을 스크립트로 완료하고 결정을 활성화하므로 정상 UI의 선택 가능 여부·정치력 비용·35일 중점 진행을 검증한 시험은 아니다.

증거는 `.local-artifacts/runtime/2026-09-22/C1-KOR-harness-default/`의 `result-summary.json`, `snapshot-index.json`, 네 로그와 실제 로드 구성·설치 해시에 보존했다. 네 로그는 모두 복사 중 크기·수정 시각이 같았다. 기본 fixture의 집계는 **118 PASS / 1 FAIL / 7 SKIP**이며 `game.log:154–155`의 최종 표시는 `RESULT_FAIL`과 실행 종료다. 실행 종료를 자동 통과로 해석하지 않는다.

| 확인 범위 | 기본 fixture 결과와 한계 |
|---|---|
| 중점·국민정신 | 58개 scripted focus 완료, 최종 국민정신 17개 존재, 이전·미선택 국민정신 10개 부재, 반대 선택 중점 2개 부재 PASS (`game.log:17–107`). 연구·경험치·modifier 수치를 모두 검증한 것은 아님 |
| 시민교육 보상 | state 525·919·1145 각각 민간공장 +2 PASS (`:104–106`) |
| 지역 사업 반복 | 평안·강원·충청·경상 네 사업에서 두 번씩 활성화. 각 회차 예정 89일 검사 시 계속 활성·조기 공장 지급 없음 PASS (`:129–132,144–147`). 예정 92일 완료 검사에서 첫 회차 공장 +1, 두 번째 누적 +2 PASS (`:134–140,149–152`) |
| fixture 실패 1건 | `fixture_government_and_faction` FAIL (`:16`). RT56 `history/countries/BHU - Bhutan.txt:28–33`의 BHU는 영국 `autonomy_protectorate`이며 미종속국만 세력에 넣는 fixture 조건을 충족하지 못함. 이 시험 준비 실패를 production 보상 결함으로 분류하지 않음 |
| 생략 7건 | 취소 준비·미착수, 면허협정 수락 미관측, BHU 세력 미가입, 관세·면허협정 탈퇴 정리 미관측, 면허 관계 정리 부적격. 취소·협정의 통과 증거로 집계하지 않음 |

MAN 참조·임시 fixture·신규 `HOK_KOR` 오류 검색은 각각 **0건**이다. 실행 담당자의 마지막 UI 관측은 `1936.08.13.02` 일시정지이며, 로그도 1월 1일 시작부터 그 종료 시점까지 보존됐다. 따라서 **이 C1 구성과 진행 범위에서 MAN의 반복 오류가 재현되지 않았음은 CONFIRMED**다. 한국 인물을 고용하는 별도 분기와 모든 DLC·국가·장기 실행까지 보장하지 않는다.

전체 `error.log`는 물리 710행·시각 레코드 693개로 오류 0건이 아니다. `:703–704`에는 7월 1일 엔진 자동저장 시 `continue_game.temp`와 `autosave_temp.hoi4` 이름 변경 실패가 있고, `:709–710`에는 종료 시 random 로그 이름 변경 실패가 있다. 실행 중 7월 임시 자동저장이 생성됐으므로 수동 저장을 하지 않았다는 사실을 세이브 파일 생성 0건으로 표현하지 않는다. 이 임시 저장은 정상 저장·재로드 통과 증거가 아니다.

| 기본 fixture 보존 로그 | SHA-256 |
|---|---|
| `logs/game.log` | `9FB03F3B7364023B3A8EE1A74D73548F463065E3ECC393BD25629C907FFA7280` |
| `logs/error.log` | `0051ABDCE7713471618201991F893030BFD393C6F71FF596AC757312FD4E6B9A` |

게임 종료 후 `.local-artifacts/runtime/2026-09-22/harness/cleanup-default.json`에 두 임시 파일의 설치 해시 일치·제거와 production 입력 해시 불변을 기록했다. 기본 fixture는 제거됐고, 깨끗한 재실행을 요구하는 `clean_restart_pending` 기록을 남겼다. 이어 독립국 NEP를 대상으로 fixture를 보완한 alternate 실행을 진행했으며 결과는 아래에 분리한다.

## C1-KOR-harness-nepal-alternate: 보완 시험 134 PASS

`.local-artifacts/runtime/2026-09-22/C1-KOR-harness-nepal-alternate/`의 결과는 **134 PASS / 0 FAIL / 0 SKIP**다. RT56+RT56 Korean Translation+호환판, DLC 36개, 엔진 `1.19.3.0.c01a (fb72)` 구성이다. NEP의 존재·독립·무소속 AI 조건과 한국 세력 가입을 먼저 확인한 뒤 실행했다(`game.log:17–19`). `:165–166`은 `1936.07.04.11`의 `RESULT_PASS`와 `END`를 기록한다. 기본 fixture의 실패 기록을 이 결과로 덮어쓰지 않는다.

- 반대 선택 중점 `HOK_KOR_flexible_production_lines`, `HOK_KOR_foreign_aircraft_designs`를 포함한 58개 완료와 해당 국민정신 상태를 확인했다. 기본·대안 fixture의 완료 ID 합집합은 신규 60개이며 정상 UI·선행·35일 진행 검증과 구분한다.
- state 527을 하루 동안 넘겨 평안 사업의 취소, 완료 flag 부재, 공장 무지급을 확인한 뒤 주 복구·재착수에 성공했다(`:116–123`). 다른 세 사업은 계속 활성 상태였다.
- 관세·면허 협정의 수락을 관측했고(`:127–128`), KOR→NEP와 NEP→KOR 양쪽 면허 관계를 확인했다. NEP 세력 탈퇴 뒤 두 협정 국민정신과 양쪽 관계의 정리를 확인했다(`:129–135`). 거절·730일 자연 만료까지 시험한 것은 아니다.
- 네 지역 사업 모두 두 회차의 예정 89일 활성·무지급과 완료 검사 시 첫 +1·누적 +2를 다시 통과했다(`:139–163`).

MAN·fixture·신규 HOK 오류는 각각 0건이다. 전체 오류는 물리 730행·시각 레코드 713개이며 rename 오류 6건을 포함한다. `END` 뒤 사용자 ESC로 조작이 중단된 동안 게임 로그는 `1937.05.10.17`까지 진행했고, 보존 시 프로세스가 없었다. **정확한 종료 시각·원인은 미확인**이며 빈 crash 디렉터리만으로 정상 종료를 단정하지 않는다. assertion 종료 뒤의 이 진행을 별도 장기 플레이 검증으로 집계하지 않는다.

| NEP alternate 보존 로그 | SHA-256 |
|---|---|
| `logs/game.log` | `4AB7BDDE320D398B090046C19358D1883B0D2C11E7227CBAD850700789C7217B` |
| `logs/error.log` | `91532CF1284FC8047FD0EABCF538D9BB63596286A4EC235F59B9E6B7C293D09D` |

네 로그 모두 복사 중 안정적이었다. 프로세스 부재 확인 뒤 `harness-nepal/cleanup-alternate.json`에 임시 파일 두 개의 해시 대조·제거와 한국 production 20개 입력의 해시 불변을 기록했다. 이후 fixture 없는 한국 새 게임 확인은 다음 절에 분리한다.

## C1-KOR-clean-final: 임시 파일 없는 한국 UI 확인

임시 두 파일을 제거한 뒤 02:06:25에 시작한 PID `55740`, 체크섬 `27e6`의 새 한국 게임이다. 실제 구성은 앞선 C1과 같은 RT56+RT56 Korean Translation+호환판이다. `.local-artifacts/runtime/2026-09-22/C1-KOR-clean-final/initial/`에 02:07:59의 초기 로그·구성을 보존했다. province 13,569개와 history 로드를 확인했으며 fixture setup/game 기록은 각각 0건이었다. **초기 보존본에 한해** 오류 698행·시각 레코드 681개, MAN·fixture·신규 HOK 오류 각각 0건이다.

다음은 실행 담당자가 UI에서 확인한 사실이며 감사자가 독립적으로 후반 화면을 판독한 기록은 아니다. `final/observation.json`에 전달받은 관측과 한계를 보존했다.

- 초기 정치력 1 등 정상 새 게임 상태로 시작했고 fixture의 중점 58개 강제 완료 상태가 없었다. `우리황실사랑회`(UI 7일), `라디오 미디어 장악`(UI 21일)을 정상 진행하여 완료했고 한국어 이벤트·UI를 확인했다.
- `1936.02.28.13`에 원화평가절하를 정상 UI에서 선택했으며 35일과 730일 효과 표시를 확인했다. `1936.04.15.12`에 완료 창을 관측했다. 이는 실제 완료 시각을 측정한 기록이 아니며, 저장된 중점 진행일수가 적용돼 정확히 35일 경과 후 완료됐다고 주장하지 않는다.
- 최종 일시정지 관측은 `1936.04.28.22`, 정치력 73·안정도 40%·전쟁 지지도 11%·공장 14였다. 국민정신 tooltip의 제목 `원화평가절하`, 소비재 공장 변동치 −5.0%·안정도 −5.00%·`21 3월, 1938에 제거됨`을 확인했다. 이 상태의 모든 수치 변화를 단일 중점 보상에 귀속하지 않는다.
- 이번 clean 실행에서는 수동 저장·재로드를 하지 않았다. 담당자는 메뉴의 종료 확인 뒤 게임 창·프로세스가 없는 것을 확인했다고 보고했다. 이후 launcher playset 복원은 ESC로 실행되지 않았다.

후반 최종 로그 보존 전에 **02:18:32에 시작한 별도 PID `54556`이 live logs를 덮어썼다**. 실행 주체는 미확인이며 담당자는 자신이 재실행하지 않았다고 보고했다. 별도 자료는 `unattributed-launch-021832/`에 보존하고 clean 실행의 최종 증거로 사용하지 않았다. 따라서 1월부터 4월 28일까지의 전체 MAN·fixture·신규 HOK·총 오류 수는 복구해 집계할 수 없으며, 초기 0건을 후반까지 확대하지 않는다.

## 최종 정적 검사와 정리 기록

두 fixture의 임시 파일 제거·production 입력 불변 기록과 README 확정 뒤 원장을 재생성하고 aggregate를 실행했다. `.local-artifacts/audits/2026-09-22/static-validation-final.txt`는 **20 PASS / 0 WARNING / 0 ERROR, exit 0**, SHA-256 `098F8AA8807CAB593DD71F6931B12107574F9EEEF60E0D5A71918770AAC424E5`다. 최종 원장은 1,031행·donor 동일 경로 충돌 73개·기존 분류 수를 유지했고 SHA-256은 `61AE7C953D9E029CD8012A52ACFFB4D2539B5947A0A49DA80B7E3BC3CE418452`다. 이 정적 결과는 clean 후반 로그 부재를 보완하는 엔진 증거가 아니다.

## 후속 실행과 남은 범위

MAN 첫 정의 복원은 실패했고 후속 조건 적용 뒤 두 C1 fixture에서는 반복 오류가 재현되지 않았다. 기본 fixture에서 생략됐던 취소·협정은 NEP alternate에서 위 범위만큼 확인했다. 임시 파일 없는 한국 새 게임의 UI 진행과 최종 정적 검증도 확인했으나 후반 로그 집계는 불가능하다. 번역 없는 C0 KOR·한국 고문 고용 분기는 별도 검증 대상이다.

지역 사업 네 곳의 반복 보상·조기 지급 부재, 평안 취소·복구, 두 선택지의 중점·국민정신과 협정 수락·탈퇴 정리는 위 범위에서 검증했다. UI 비용·선행 조건, 협정 거절·자연 만료, DLC/OOB/기술 분기, 3개 AI 지원 계획의 실제 선택, 만주 15주와 대일 강화, 해군·보급·항공·음성, 전체 한국어 UI, 과거 세이브·장기 진행·멀티플레이는 여전히 남아 있다. 임시 저장의 같은 프로세스 내 재로드를 정상 파일 저장·새 프로세스 재로드 또는 기존 세이브 호환 보장으로 확대하지 않는다.

이 문서 작성과 감사는 외부 파일을 읽고 승인된 로그 사본을 저장소 내부에 보존한 작업이다. 감사 담당자는 생산 파일·원본·외부 설정·세이브를 수정하거나 게임을 조작하지 않았고 Git commit·push·게시를 수행하지 않았다.
