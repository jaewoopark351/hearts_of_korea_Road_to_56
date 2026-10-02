# 2026-10-03 원료 순환체계 업데이트 이식

상태: **선택 이식·생성·해당 module의 정적 검사 완료. aggregate는 20 PASS / 0 WARNING / 1 기존 ERROR. 이번 변경의 호환판 실행 검증은 미실행이며 UNPROVEN.** 아래 기준선은 2026-10-03 00:04 KST 전후에 읽기 전용으로 관측한 값이며, 작업 전 검사와 최종 검사를 구분한다.

## 범위와 동작

사용자는 `C:\hoi\hearts_of_korea`의 최신 업데이트를 검토한 뒤 “베껴줘”라고 요청했다. 이 작업은 2026-10-02 원료 순환체계 묶음을 현재 RT56 호환판에 선택 이식한다. 전체 donor 복사나 다른 중점·정책의 재설계가 아니다. 원본·Workshop·설치본·사용자 데이터·런처·로그·저장은 읽기 전용이며, 커밋·푸시·업로드는 별도 요청 범위다.

| 항목 | 이식 전 | 선택한 donor 동작 |
|---|---|---|
| 원료 순환체계 I | 자원 획득 +15%, 자원 부족 불이익 −10% | 최종 +30% / −30% |
| 원료 순환체계 II | 자원 획득 +25%, 자원 부족 불이익 −20% | 최종 +60% / −60% |
| 긴급 시설 확충 | 없음 | 정치력 150으로 별도 +30% / −30% 국민정신을 즉시 90일간 추가 |

사용자 지정 수치는 변경 후 최종값이다. I와 II의 기존 교체 구조를 보존하며, II 활성 중 긴급 지원을 사용한 이 정책 묶음의 합계는 +90% / −90%다. 국가 전체의 자원·생산량을 고정하는 값은 아니다.

신규 범주·디시전·국민정신의 `allowed`는 `original_tag = KOR`다. 범주·디시전은 `HOK_KOR_cmn_closed_material_cycle` 완료로 보인다. 사용 조건은 같은 중점 완료, II 보유, 비내전·비항복, 임시 정신 부재다. 일반 전쟁 중에는 사용 가능하다. `cost = 150`으로 한 번 지불하고 `add_timed_idea`로 즉시 지급한다. `days_remove = 90`, `days_re_enable = 0`, `fire_only_once = no`를 보존한다. 활성 중 재사용·중첩·기간 갱신을 막고 만료 후 별도 대기 없이 반복하도록 작성돼 있다. 취소·종료는 임시 정신만 제거하며, 내전·항복·II 상실 시 취소되고 정치력은 환급하지 않는다. AI는 donor의 가중치 0.5와 정치력 150 이상 조건을 유지한다.

새 flag·variable·on_action·주 효과는 없다. 기존 G2 산업 연구 150% 1회·채굴 연구 100% 1회·정치력 150, 460개 중점의 ID·선행 조건·좌표·기간·AI, 다른 만주 사업의 공유 제한·대기·비용을 보존하는 것이 이식 계약이다. 지도·history·중국/일본 공유 콘텐츠·descriptor·Workshop 신원은 이 변경 대상이 아니다.

## 현재 기준선

| 항목 | 읽기 전용 관측 |
|---|---|
| 호환판 branch / HEAD | `feat/korean-focus-update-20260922` / `825bb411b2e12ce1d5f9545d7a24ad82fc7dcdfa` |
| 호환판 작업 시작 상태 | `git status --short` 빈 출력, clean |
| donor branch / HEAD | `feat/korean-focus-expansion-ai` / `8609d0b61e4c00e6be6c204dcf31cfa41150664e` |
| donor 실제 선택 원본 | HEAD 위의 2026-10-02 미커밋 수정·신규 파일. HEAD 자체에 이 변경이 있다는 뜻이 아님 |
| HOI4 설치 metadata | `Operation Postern v1.19.3.0.c01a (5632)`, raw version `1.19.3.0`, Steam build `25205862` |
| RT56 Workshop | `820260968`, installed/latest manifest `7475007536894105204`, timeupdated `1788822864` |
| RT56 descriptor SHA-256 | `5B323861ABD63E31CB896277E3EA58BA4BCD9FCEEDA957B50792065E42E03F61` |
| 기존 사용자 게임 | `hoi4.exe` PID `24460`, 생성 `2026-10-02 23:55:44 KST`; 조사 시 실행 중 |
| 그 게임의 로그 | `system.log` 23:56:31의 `1.19.3.0.c01a (16fe)`, DLC 36개·mod 3개. 이번 변경 후 cold-run 결과가 아님 |
| OS / 설정 | Windows 11 x64, `l_korean`, 논리 해상도 1280×720, GUI 1.0 |
| 실제 사용자 데이터 | `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV` |
| 런처 active playset | 읽기 전용 SQLite 질의로 확인한 `Road to 56 한국 테스트` |
| 기록된 enabled 순서 | 위치 0 호환판, 1 `The Road to 56 Korean Translation` (`2769576030`), 2 RT56 (`820260968`) |
| donor 활성 여부 | `dlc_load.json`와 active playset의 활성 목록에 없음 |

`dlc_load.json`의 `disabled_dlcs=[]`와 실제 로그의 DLC 36개를 구분해 확인했다. 위 순서는 런처에 기록된 목록이며, 파일별 유효 우선순위를 증명한 것은 아니다. 실행 중인 사용자 게임을 종료·재시작하거나 콘솔로 조작하지 않았다.

호환판 repository descriptor는 `0.1.0-dev`, `supported_version="1.19.*"`, `The Road to 56`와 `Korean Language` 의존성을 선언하고 호환판 ID `3796816200`을 기록한다. `replace_path`·launcher `path`는 없다. 외부 호환판 `.mod`는 같은 내용에 `path="C:/hoi/hearts_of_korea_Road_to_56"`가 추가돼 있다. donor descriptor와 donor launcher `.mod`는 donor ID `3793992662`와 `Korean Language`를 선언하며 런처 경로는 `C:/hoi/hearts_of_korea`다. 원작 `2898629778`, donor `3793992662`, RT56 `820260968`을 호환판 upload ID로 가져오지 않는다.

RT56 descriptor의 `replace_path="history/states"`, `replace_path="map/strategicregions"`는 호스트 기존 설정이다. 현재 활성 RT56 번역은 `replace_path="localisation"`을 선언한다. 선언된 Korean Language (`2743487021`, `supported_version="1.17.*"`)는 설치돼 있지만 활성 목록에는 없다. 이 작업은 두 번역을 교체·결합하지 않고 기존 한·영 locale header와 한국어 본문 계약을 유지한다. 최종 localisation 의존성 계약과 새 문자열의 실제 유효 우선순위는 아직 실행으로 확정하지 않았다.

## 선택 원본과 생성 소유권

미커밋 파일은 Git HEAD만으로 재현할 수 없으므로 [선택 사본](../upstream/hok-material-cycle-20261003/README.md)과 [독립 lock](../../tools/hok_material_cycle_lock.json)에 실제 checkout 바이트·크기·해시와 출처를 고정했다. runtime text 6개·DDS 3개, 출처 문서·manifest·선택 그림 원본 11개, 총 20개 선택 입력이다. 기존 전역 donor lock·2차 확장 lock를 최신 donor 전체로 바꾸지 않는다. 생성기는 고정한 원본에 근거해 기존 출력의 검토된 부분만 병합한다. 생성 runtime 파일에 수동 패치를 덧붙이지 않는다.

| 실제 donor 선택 입력 | SHA-256 |
|---|---|
| `common/ideas/HOK_KOR_common_followup.txt` | `5284448EF7A5851859828AA778994193DDBF2EAD70B04CAF1E0C0915E9F69CCB` |
| `common/decisions/HOK_KOR_common_followup.txt` | `0C0C035A970608CEDAC7DAD8D8353C463E8EDCB15104198E0BCD8B1193E7F605` |
| `common/decisions/categories/HOK_KOR_common_followup.txt` | `2219EF472748DD9957ADF296EFA0226BBD4D59B776BB32AA0B9705EE1699408E` |
| `interface/HOK_KOR_material_cycle_icons.gfx` | `570A2799B06ACC6CC0047CFDFC1C4C47733E07910C563A22C8AF16BF98095CA5` |
| `localisation/english/HOK_KOR_common_followup_l_english.yml` | `3EC2CE087F0D5DFCAF495AAA2267DDF621FE893E97202E817621E537DCB31E2B` |
| `localisation/korean/HOK_KOR_common_followup_l_korean.yml` | `7A4FF16EFD4D8FFC20010CC6260BCD04B2CB1482246AD73E97443FF3F2A19598` |
| donor `common/national_focus/korea.txt` (참조 전용) | `1CEDAF78903DB31D15E3837E20069B71BCA8FC674212B1D033F0D721B2B6735C` |

| runtime 대상 | integration 분류와 차이 |
|---|---|
| 기존 `common/ideas/HOK_KOR_common_followup.txt` | 기존 `ADD` 위의 reviewed overlay. 지정 I·II modifier와 신규 timed idea만 변경 |
| 기존 common followup locale 한 쌍 | 기존 `ADD` 위의 reviewed overlay. 설명 3개·신규 key 6개·기여자 주석. BOM·header·기존 key 보존 |
| 신규 decision·category·GFX | `ADD`. HOK 고유 ID와 local relative path, 각 registry는 단일 유효 정의 |
| 신규 DDS 3개 | `ASSET_COPY`. donor와 byte-identical, 재착색·재압축 없음 |

위 표는 파일 분류이며 신규 module의 runtime 검증 통과를 뜻하지 않는다. 정확한 output hash와 행별 출처는 생성 integration manifest/ledger에 기록한다.

이번 module의 runtime 9개 파일은 고정 donor 원본과 바이트 동일하게 반영했다. 기존 파일 3개(ideas와 locale 한 쌍)를 갱신하고 신규 파일 6개(decision·category·GFX와 DDS 3개)를 추가했으며, 중점 생성기의 관리 output은 400→406개가 됐다. 원료 정책 외의 수정은 아래에 기록한 checkout 재현성 수선으로 제한한다. 통합 원장은 1,411→**1,417개**로 생성·확인했다. 분류는 `ADD` 199, `ASSET_COPY` 1,097, `BINARY_MERGE` 18, `OVERRIDE` 9, `THREE_WAY_MERGE` 31, `USE_RT56` 63이며 기존 same-path host 충돌 73개를 유지한다. 새 manifest SHA-256은 `AFAE408338945E895E84DE417BCA562C76C2DFD4A4B75A4E87C6A69F665BCFF3`다.

checkout 초기 관측에서 호환판 중점 SHA-256은 `6F9F76036B21D22E9716ACE44C124D20BBF2CAF3751AAEE5313C758FC3B8F162`, descriptor는 `D68DCE620EA3DDDE422F26F2E5155E4D52F35AC4B2EBE1224DC71E07035141CB`였다. 기존 ideas는 `D49D791A028EBABF878F580623C257BB93CC6E05706A043488ECA72228AF87F6`, 영어 locale은 `D50ED048CD36BC8382CA5DB3E80A7F88FCC7749B1D199F624607ACEC43E7F606`, 한국어 locale은 `396D68AD69710AE22A2BEF1149CC31B6452D6274C5F21A919BE6870CC24C2752`였다. 이것은 아래 재현성 수선 전 checkout의 실제 바이트 기록이다. 새 module의 보존 gate는 기존 생성 output의 정확한 바이트를 복구한 뒤 별도로 고정한다. 이번 module은 주·province·국가 scope 전환을 추가하지 않으므로 새 지도 ID 변환은 필요 없다.

`console_history.txt`, `imgui.ini`와 원본의 개발 세션 설정은 이식하지 않는다. 문서·이미지 출처 원본은 증거이며 runtime 의존성이나 새 production 정의가 아니다.

## 문법·UI·그림 근거

동일 설치본의 `common/decisions/AUS.txt` 255~305행은 기간제 정신·착수·취소·종료, `COG.txt` 2650~2701행은 반복 결정과 즉시 90일 정신, `CHI_decisions.txt` 3045~3046행은 진행과 0일 재사용 대기를 보여 준다. `common/ideas/indonesia.txt`의 `cancel`·`allowed_civil_war` 사례도 재확인했다. 모두 국가 범위의 해당 문맥 근거로 사용하고, 다른 Paradox 게임 문법을 도입하지 않는다. 설치 `modifiers_documentation.md` 3230·4474행과 기존 source의 두 modifier를 확인하되 문서 분류만으로 실제 자원 계산이나 하한을 추정하지 않는다.

| target reference | SHA-256 |
|---|---|
| vanilla `common/decisions/AUS.txt` | `619F5E7D922C7900C2CFE31B54DC37D32B7583DEDAE9F33336A430D753362EF0` |
| vanilla `common/decisions/COG.txt` | `7DECE4D71FA9BA1233D1983D1D82AB9B1EBAF007C2EBC64B4EBA36EF99082885` |
| vanilla `common/decisions/CHI_decisions.txt` | `EFCEC834A71901A5DA66EEF97F8B817D1B7299C36F16E48893FF9F3918039068` |
| vanilla `common/ideas/indonesia.txt` | `2540003403E1BE72C1FFAE32CD76320C695B3F5EBA8D9EFDCA4C4D0162E6E06B` |
| RT56 `common/ideas/korea.txt` | `F358082E803679A829A0474987450F630E727EDE19CDA13C7367DE529B457CDA` |
| RT56 `common/decisions/FRA.txt` | `689961D69605819FE20E83DEEDC0D9AF26EB1CF3DF94BB099C3236CAD8A7D95E` |
| vanilla `interface/countrydecisionview.gui` | `EEDEA36ADE734B67A23181A650464F9168BEADB0E024C0CEDF2112D1B097194E` |
| vanilla `interface/countrydecisionview.gfx` | `52E5D504383F91C0DA1D2E206C72E1F5DB726FFC052934652DE2EF457FB80A66` |
| RT56 `interface/r56_decisions.gfx` | `CB972E7AEFCE0DDA3AA09D7E05B17F71CE62A1AFEF0F50DADA0AFC1ACEF259AB` |
| RT56 `interface/countrypoliticsview.gui` | `E386D0838043C75F160ABA4C61555F04876491BBEED694677DDD0858609702BB` |

RT56에도 `FRA.txt` 3445~3446행의 `days_remove = 90`·`days_re_enable = 0` 사례가 있다. 이 예시를 복사해 공유 정의를 바꾸지 않는다. RT56에는 `interface/countrydecisionview.gui`의 same-path override가 없으며 이번 module은 scripted GUI를 추가하지 않는다. 설치 GUI의 category header 높이 58, icon 위치 `(10,16)`, 제목 x=74, 일반 decision row 높이 41과 icon anchor를 확인했다. 선택한 51×40 header·32×32 row의 크기와 여백은 이 구조에 맞지만 실제 게임의 줄간격·툴팁·가용/활성 상태 검수와 구분한다.

국민정신의 호스트 UI는 RT56 `countrypoliticsview.gui` 543~568행의 일반 59×68 slot과 과밀 33×34 slot을 확인했다. donor의 60×68 임시 정신 payload를 기존 HOK 정신과 같은 경로·sprite 방식으로 연결하고 공유 grid나 scaling을 바꾸지 않는다. 실제 이미지 여백·과밀 표시·툴팁은 실행 검수 대상으로 남긴다.

선택 DDS는 임시 정신 60×68, 행 32×32, 헤더 51×40이며 1 frame·BGRA32·명시적 alpha를 보존한다. 원본 I·II 이미지는 그대로 둔다. donor의 고정 Ultimate HOI4 GFX 원본·CREDITS와 직접 그린 시계, 산업색 처리·sprite 연결·해시는 선택 사본에 보존하며, kpopmodder의 donor 제작과 이번 compatibility 선택 이식을 구분한다. 이번 이식에서 새로운 그림을 생성하거나 원본을 재가공하지 않는다.

## 검증 결과와 한계

| 구분 | 이번 작업 상태 |
|---|---|
| 수정 전 aggregate static | **9 PASS / 0 WARNING / 12 ERROR**. `tools/hok_source_lock.json` 실제 바이트 해시가 2차 확장 pin과 달라 12개 gate가 연쇄 실패. 작업 시작 Git은 clean |
| 기준선 lock 바이트 조사·복원 | `core.autocrlf=true`의 checkout CRLF 변환으로 확인. source·second-wave·policy·localisation lock 4개를 raw HEAD와 동일한 LF로 복원하고 icon lock의 역사적 CRLF pin은 보존. 제한된 `.gitattributes`로 lock·신규 고정 사본의 바이트를 보존하며 기대 해시를 변경하지 않음 |
| 선택 source·참조·충돌·scope·modifier | 관련 gate PASS. 신규 HOK 정의·연결과 기존 정책 보존 계약 검사 |
| 생성 output·BOM·key·DDS·sprite·허용 diff | 9개 module 파일 frozen donor 바이트 일치, 관리 output 406개 검사 PASS |
| 구조·현지화 | 생산 UTF-8 텍스트 185개 구조 검사 PASS, locale 66개 파일·5,062 key 검사 PASS |
| 중점 subsystem `--check` | PASS |
| 중점 subsystem `--self-test` | 의도적 회귀 변형 35개 거부 (기존 24개 + 신규 원료 정책 11개) |
| 통합 manifest·ledger | 1,417개, 해당 generation gate PASS |
| `python tools/validate_port.py` 최종 | **20 PASS / 0 WARNING / 1 기존 ERROR**. 최초 12개 source·generation 연쇄 실패는 해소 |
| 작업 범위 whitespace | 신규 module·tools의 plain `git diff --check` PASS. 전체는 `git diff --ignore-space-at-eol --check` PASS; plain 전체 검사의 제한은 아래 기록 |
| late fingerprint·보존 | 선택 source 20개·runtime 9개·역사적 lock 5개·중점·descriptor·`map/buildings.txt`·KOR history 일치. RT56 manifest·descriptor도 최초 관측과 일치 |
| 호환판 cold-run·새 game·UI·정치력·기간·취소 | **미실행**. 기존 사용자 게임 실행 중이며 이 작업은 그 세션·설정·저장을 변경하지 않음 |

위 9/12는 이식 전에 실제 실행한 결과다. 2026-09-23의 20 PASS / 1 기존 ERROR 기록을 현재 baseline 대신 쓰지 않는다. lock의 논리적 내용은 변하지 않았으며, raw Git blob과 pin이 일치하는 바이트만 복원했다. 이 작은 재현성 수선은 신규 원료 정책·보상 이식과 별개인 선행 작업이다. 이어서 기존 생성 output·출처 archive의 checkout 개행 차이도 조사하며, 각 복원 범위와 검사 결과를 따로 기록한다.

기존 고정 source cache도 이 checkout에 없었다. 전역 1,031개·2차 확장 326개·아이콘 133개의 역사적 입력을 기존 lock의 불변 바이트와 해시로 복구했다. 아이콘 입력 중 121개는 현재 donor와 같고, 최신 donor와 다른 12개는 고정 donor Git commit `b9aefbcd4da68d5f0ef17a20271a7f6b452e4236`의 객체에서 복구했다. 기존 해시는 변경하지 않았다. 이는 최신 runtime tree를 복사한 작업과 다르다. 지리 검사기의 `ROOTS['donor']`가 동일하게 고정된 HOK source cache를 사용하도록 연결해, 최신 donor checkout의 CRLF만 달라진 `definition.csv`에 의존하지 않도록 했다. `GEOGRAPHY_HASHES`와 실제 지도·지리 대응·생성 결과는 변경하지 않는다.

기존 runtime output에서 실제로 확인한 개행 불일치는 69개였다. 이 중 common followup locale 2개는 이번 module의 새 본문으로 갱신했으며, 나머지 **67개는 개행만 복구**했다. 중점 생성기의 그대로 유지할 36개와 다른 기존 생성 output 31개다. 이전 source archive 27개도 고정 바이트로 복구했다. 비교는 pin과 Git blob에 근거하며 글자·순서·보상·조건을 바꾸지 않는다. `.gitattributes`는 역사적 lock·새 사본과 확인한 byte contract를 보존하기 위한 것이며 전역 텍스트 정리 규칙을 추가하지 않는다. 중점·descriptor·`map/buildings.txt`·KOR history 보존 해시는 새 lock의 `preserved_runtime`에서 다시 고정했다. KOR history는 `243FC1FBDE8DB75B82CCFEBD6BB01CA7001DABCD944CA8534E7324413705BE30`으로 동일하다.

최종 잔여 ERROR는 이번 작업 전부터 있던 `migrate_doctrines.py`의 KOR history 생성 불일치다. 보존한 출력의 MtG 분기는 `set_war_support = 0.1`이고 생성기 기대값은 `0.05`다. 이 history 보상·생성기를 바꾸거나 검사 assertion을 약화하지 않았다. 따라서 aggregate 전체가 clean하게 통과했다고 보고하지 않는다. 기존 `20 PASS / 1 ERROR` 역사적 기록과 수치가 같아도 이번 결과는 복구·이식 뒤 실제로 재실행한 검사다.

전체 plain `git diff --check`는 바이트 그대로 복구한 과거 혼합 개행 파일 9개(archive 문서 8개와 `localisation/korean/NewsEvents_l_korean.yml`)의 기존 CR·행 끝 tab을 표시했다. 새 module과 tools의 검사 및 전체 `--ignore-space-at-eol --check`는 통과했지만, plain 전체 검사가 통과했다고 표현하지 않는다. byte-exact 출처·생성 계약을 깨뜨리는 whitespace 정리는 하지 않았다. Git이 개행을 정규화해 보여 주는 diff에서 module의 기존 변경 파일 3개 바깥에 나타나는 runtime 차이는 NewsEvents의 개행 복구뿐이며 gameplay delta는 없다.

종료 전 selected source 20개와 RT56 manifest·descriptor를 다시 fingerprint했다. donor의 `AGENTS.md`는 조사 후 외부에서 수정돼 dirty 상태가 되었으나 선택한 20개 입력은 바뀌지 않았다. 이 작업은 donor의 해당 변경을 만들거나 가져오지 않았다.

donor의 [2026-10-02 구현 기록](../upstream/hok-material-cycle-20261003/documents/docs/incidents/2026-10-02-korean-material-cycle.md)은 콘텐츠 정적 238 PASS, 이미지 37 PASS, donor만 활성인 새 한국 게임 초기 로드와 기존 대비 신규 오류 없음 결과를 기록한다. 이 결과는 이번 RT56 포트의 검사 통과가 아니다. 뒤의 설명문 수정에 앞선 검사·초기 로드이며, 수정 설명의 실제 줄바꿈도 검수되지 않았다. 해당 기록이 인용한 사용자 UI 사진은 II +60% / −60%, 별도 임시 정신 +30% / −30%와 제거 예정일 표시의 근거이며 정치력 지불·90일 자연 만료·재사용 증거로 확대하지 않는다.

후속 실제 검사는 RT56 control과 donor 없이 호환판을 켠 cold-run을 기록하고, 정상 I→II 진행, 해금 전·정치력 부족 차단, 실제 클릭의 정치력 150 1회 차감, 즉시 timed idea, 활성 중 재사용 차단, 89/90/91일 만료·II 보존·두 번째 재사용, 내전/항복/II 상실 취소를 구분해야 한다. 아이콘·새 문안·기간 표시와 실제 자원·원료 부족 생산 영향도 별도 관측 대상이다. 저장 재로드·기존 저장 호환·장기 AI·다른 DLC·다른 번역·멀티플레이는 정적 검사로 증명하지 않는다.

## 작업 기록

변경은 이 호환 저장소의 working tree에만 기록했다. donor·Workshop·HOI4 설치본·런처·사용자 세션은 수정하지 않았다. 커밋·푸시·업로드는 수행하지 않았다. 콘텐츠·정적 재현 검사를 완료했지만 실행 중인 기존 사용자 게임을 보존한 상태이므로 cold-run과 실제 보상·기간·UI 검증은 남아 있다. 다른 모드나 donor에서의 과거 성공을 이번 포트의 엔진 증거로 대체하지 않는다.
