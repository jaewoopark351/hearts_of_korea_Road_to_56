# 2026-11-19 산둥 전용 웡원하오 지도자 구현·검증

상태: **구현·DLC 양분기 지연 출범·한국어 UI·새 저장 왕복 확인**. 사용자가 [초기 설계 20절](../HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_PLAN.md#20-shandong-weng-wenhao-leader-design)의 설명 뒤 별도로 `AGENTS.md, /docs 읽고 구현해줘`라고 요청했다. 이전 문서화 전용 단계와 이번 구현을 구분한다. 지도자만 변경했으며 커밋·푸시·업로드는 수행하지 않았다. 새 게임 기준의 확인이며 구 캠페인의 자동 교체·마이그레이션은 포함하지 않는다.

## 기준·자료 위치

| 역할 | 위치·기준 |
|---|---|
| 작업 소스 | `C:\hoi\hearts_of_korea`, `feat/korean-focus-expansion-ai`, HEAD `0c19f58fa7a9ff898196dcdbe46edfd0ad5fdbbc`; 기존 미커밋 작업 보존 |
| 설치 원본 | `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV`; `Operation Postern v1.19.5.0.7c6c (c184)`, 읽기 전용 |
| 원작 출처 | `C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\2898629778`, 읽기 전용 역사 자료 |
| 실제 사용자 데이터 | `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV`; 게임 생성 로그·저장 원본 |
| 이번 외부 TASK | `C:\hoi\test\hok-shandong-weng-wenhao-20261119-01\`; 모든 helper·probe·백업·검사·화면·로그/저장 사본 |
| 이전 실행 자료 | `C:\hoi\test\hok-shandong-full-integration-20261119-01\`; 이전 출범 기능의 증거와 재사용 helper 출처. 이전 실행을 이번 지도자 검증으로 사용하지 않음 |
| 기존 활성 구성 | 저장소 HOK → `C:\hoi\Hearts of Korea English Translation Anime Modder's Edition`; 테스트 분기·실제 언어·DLC는 실행 기록에서 구분 |

`TASK/source-before.json`은 편집 전 저장소 1,890파일의 경로·크기·SHA-256이며 `.git`은 제외한다. `formation-before.txt`는 지도자 지정 전 효과 사본(SHA-256 `b9318ca802c0b4f266d7cb140761ba34e132d4cfa70384deb08e1a032a2de052`), `git-status-before.txt`는 기존 작업 상태다. 이 baseline은 이전 구현 때의 runtime 1,595파일 목록과 범위가 다르다. `runtime/baseline/`에는 profile 11파일 원문·현재 로그 사본과 기존 저장 171개·12,447,306,113바이트의 해시 목록을 둔다. 이전 시험 원본도 이번 시작 시에는 보존할 기존 저장이다.

## 변경·출처·후보 처리

| 기능·참조 | 처리 | 의미·근거 |
|---|---|---|
| [전용 캐릭터](../../common/characters/HOK_KCH_characters.txt) `HOK_KCH_weng_wenhao` | 수정 — 신규 정의 | 원본과 다른 ID. `name = CHI_weng_wenhao`, 대형 `GFX_portrait_chi_weng_wenhao`, 민주주의 하위 이념 `socialism`, 원본 만료 `1965.1.1.1`·`id = -1`. 명시적 특성·고문·군사 역할 없음 |
| [KCH 시작 이력](../../history/countries/KCH%20-%20Korean%20China.txt) | 수정 — 전용 인물 초기화만 | 엔진이 요구하는 시작 시점에 전용 인물을 모집한다. 기존 정치·선거·기술·1939 설정은 보존 |
| [출범 효과](../../common/scripted_effects/HOK_KOR_chinese_government_effects.txt)의 생성 child | 수정 — 전용 인물 이동·승격 | 민주주의 설정 바로 뒤 `every_possible_country`에서 전용 인물의 현 소속을 찾아 실제 생성국으로 `set_nationality`하고 명시 이념으로 승격. 원본 CHI 인물을 옮기지 않음 |
| 원본 `CHI_weng_wenhao`·CHI 모집·중국 중점/사건 | 의도적 유지 | 인물 이동·은퇴·삭제 없음. NCNS 고문, 미사용 시 예전 민주 지도자 역할과 양국 동일 인물 병존 허용 |
| 이름·대형 초상화 | 의도적 재사용 | 설치본 `nsb_characters_l_korean.yml:262`의 “웡원하오”, English 대응의 “Weng Wenhao”. `_leader_portraits.gfx:1297` → `gfx/leaders/CHI/Portrait_China_weng_wenhao.dds`(131,168바이트). 새 이미지·GFX·이름 키·현지화 파일 없음 |
| 외부 번역·선언된 Korean Language | 원본 편집 제외 / 관련 키 검토 | 활성 외부 번역에서 Weng 이름·sprite override 없음. 선언된 legacy dependency를 실제 활성화한 별도 실행의 검증으로 확대하지 않음 |
| 자동 인물의 특성·새 보너스 | 제외 — 이식하지 않음 | 이전 한 실행의 Huang Tian은 `financial_expert`였지만 매번 같은 인물·특성이라는 보장은 없음. 원본 옛 Weng 역할은 명시적 특성이 없어 해당 무작위 보너스를 보존하는 안이 아님. `CHI_geologist_trait`도 추가하지 않음 |
| 영토·전력·전쟁·종속·중점·결정·국명·지도 | 의도적 유지 | 이번 baseline 대비 다른 production 바이트와 효과 순서 보존 확인 대상. [19절 계약](../HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_PLAN.md#19-shandong-warlord-integration-implementation) 변경 없음 |
| 이미 출범한 저장 소급·장기 선거·1965 이후 | 제외 / 미검증 | 기존 저장 자동 교체·이민·후계 규칙 추가 없음. 기존 선거 허용·주기와 원본 만료일 유지. 새 저장 왕복과 구 캠페인 호환성은 별도 |

원본 역할은 설치 `common/characters/CHI.txt:3218`의 비NCNS 정의를 참고했다. 같은 ID의 NCNS instance는 `CHI_geologist_trait` 정치고문이므로 복제하지 않는다. `history/countries/CHI - China.txt:164`의 원본 모집도 그대로다. 설치 `documentation/effects_documentation.md:3033`의 생성 child, `:5696`의 모집, `:5149`의 승격과 원본 `JAP_scripted_effects.txt:2274` 이후의 동적 일본 민주국 인물 이동을 참고한다. `common/ideologies/00_ideologies.txt`에서 `socialism`은 민주주의 하위 이념이다.

일반 에셋 정책의 로컬 복사와 달리 이번에는 사용자가 선택한 **본체 초상화 직접 재사용·새 이미지 없음**의 명시적 범위를 따른다. 초기 두 파일 안에서 발견한 모집 시점 경고 때문에 전용 인물 초기화용 KCH 이력 한 곳을 더 수정한다. 세 파일 모두 지도자 기능에 한정한다. 원본 파일을 수정·복사하거나 그림·초상화 sprite를 새로 만들지 않는다. 원작자·본체 이미지의 저작자 표시는 바꾸지 않는다.

현지화 검토 시 [스킬](../../.agents/skills/hok-localisation-review/SKILL.md)·[변경 영향 절차](../HOK_CHANGE_COVERAGE_REVIEW.md)·[채널 계약](2026-09-01-localisation-contract.md)을, 초상화 출처를 다룰 때 [개발 자료 안내](../HOK_DEVELOPMENT_ARTIFACT_ARCHIVE.md)를 읽었다. 로그 검토는 [로그 스킬](../../.agents/skills/hok-log-review/SKILL.md)을 따른다.

## 확인 상태와 마감

**초기 r1 이력:** `implementation/source-contract.json`은 기존 효과에 정확히 6줄만 삽입됐고 이 삽입을 제거하면 baseline 바이트로 돌아감을 확인했다. r1 효과 SHA-256은 `0069024926dda7e0679f6b15d49c50a3e05dca55e511f91c9073e62d9a9ffdd5`, 캐릭터는 `57163327308f0ab3df25f480d3289e4df91d3b7c2e39b6ffcda01411fb8b352d`였다. r1 독립 소스 확인은 **31/31**이지만 시작 시 강제 출범의 19 PASS 뒤 `recruit_character should only happen in game/history files in order to be executed only at game start` 경고 2회를 발견했다. 시작 시 성공을 나중의 중점 완료 성공으로 대신하지 않으며, 이 소스·로그·검사 결과는 외부 TASK에 그대로 보존한다.

**후속 r2:** 원본 일본 민주 내전의 `every_possible_country` → `has_character` → 인물 scope의 `set_nationality = PREV.PREV` → 승격을 참고해 시작 이력 모집과 실제 출범 시 이동·승격으로 분리한다. `implementation/dynamic-character-canonical-patterns.json`에 원본 블록과 출처를 기록한다. 최종 소스·시간 경과 뒤 실행·DLC 두 분기는 별도로 확인한다.

최종 `implementation/source-contract-r2.json`은 최초 baseline 대비 효과에 **12줄**, KCH 이력에 **2줄**만 삽입됐고 전용 캐릭터 파일은 r1과 같음을 확인한다. 이력의 BOM·CRLF와 효과의 LF는 보존했다. 최종 SHA-256은 효과 `eb7f29879322e11f66ca22920fe871421aed3db19757f46d61ab20686b150fcd`, KCH 이력 `456dc618ab83caf9fecd53f50abe0a1295552d6304ebb3ba259602ec5da1bc54`, 캐릭터 `57163327308f0ab3df25f480d3289e4df91d3b7c2e39b6ffcda01411fb8b352d`다. 최초 두 파일 변경의 정적 성공이나 startup 성공을 최종 세 파일의 검증으로 대신하지 않는다.

최종 독립 `review/independent-source-localisation-portrait-r2.json`은 **27/27**이다. runtime 9개 루트의 기존 1,595파일에서 효과·KCH 이력만 바뀌고 캐릭터 하나가 추가돼 1,596개이며 나머지 runtime·현지화·interface·gfx는 불변이다. `COUNTRY` scope 문서만으로 모집 명령의 수명주기 적법성이 입증되지 않았다는 r1 한계도 보존했다. 기존 미출범 구 저장은 새 history 인물을 초기화하지 않았을 수 있어 이번 새 게임/새 저장 확인과 별도로 미검증이다. 소급 모집·마이그레이션을 추가하지 않는다.

지연 확인용 첫 `ncns-on-final` 실행에서는 외부 probe 이벤트의 선언을 `namespace`로 잘못 작성해 효과가 실행되지 않았다. 정식 `add_namespace`로 보조 이벤트만 교정하고 실패 로그·당시 source freeze를 보존했다. 이는 production 세 파일의 오류나 지연 형성 성공 증거가 아니며 최종 유효 실행과 합산하지 않는다.

| 확인 층·실행 | 실제 결과·증거 | 한계 |
|---|---|---|
| NCNS 미사용 `ncns-off-final` | 최종 r2, 새 프로세스, 1936.1.3.12의 지연 형성 **20 PASS / 0 FAIL**. 중국 원본의 비집권 `socialism` 역할·소속 보존. `runtime/ncns-off-final-readback.json`에서 D04 전용 인물·이름·초상화·역할, 기본 597/743·63코어 확인 | UI 렌더링은 이 분기에서 관측하지 않음 |
| NCNS 사용 `ui-final` | 최종 r2, 별도 새 프로세스, 시작 1936.1.1.12에서 root가 일반 시간 진행. 1936.1.3.12의 지연 형성 **20 PASS / 0 FAIL**. 중국 원본의 CHI 소속 정치고문 보존. 원본 민주정부·597/743/1038·피감독국 조건 확인 | 독립적인 강제 형성 fixture이며 실제 중점 Start→완료 검증이 아님. 중점 호출부는 불변이며 이전 정상 진행 기록과 구분 |
| 실제 한국어 UI | `ui/02-shandong-weng-before-save.png`: 1936.1.11.6 산둥 자유 공화국 외교 화면의 “웡원하오”, 원본 대형 초상화, 민주정부·다음 선거 1940.1 표시 | 선거 실제 실행·1965 만료 후계는 미검증. 화면의 raw `HOK_WWH_DIAGNOSTIC...` 세력명은 외부 fixture만의 임시 이름 |
| 첫 실제 UI 저장 | 게임 원본 `save games/KOR_1936_01_11_06_temp.hoi4`, **72,661,745바이트**, SHA-256 `666b434079b13226ee098b84ab1ea2223f3a5a6e800f4da635d3dabc70d0ba73`. `runtime/ui-saves/first-save/save-manifest.json`에 원본/사본 위치·해시. 실제 D04 전용 인물과 CHI 고문 병존 판독 | 저장 전 최종·`_temp` 이름 모두 부재 확인. OneDrive 이름 변경 문제로 `_temp` 원본이 남았으나 다음 실제 Local Load에 성공 |
| 전체 재시작·실제 Local Load | 원래 두 모드·probe 없는 새 프로세스 PID 9288에서 root가 첫 저장을 직접 선택·불러옴. `ui/06-selected-first-save-for-load.png`, `07-weng-after-fresh-load.png`에서 1936.1.11.6의 같은 이름·초상화·민주정부 확인 | 새 저장 왕복이며 구 캠페인 호환성 검증이 아님 |
| 재로드 후 진행·재저장 | 76시간 일반 진행 뒤 1936.1.14.10에도 같은 지도자 표시(`ui/08...png`). 별도 `KOR_1936_01_14_10_temp.hoi4`, **72,589,796바이트**, SHA-256 `a66874a93c0338c70036ed9286a7c86e05557b02e7ec8fb43dd2187b4893f52f`. `runtime/ui-saves/reloaded-resave/`에 사본·manifest | 두 번째 저장을 세 번째로 다시 로드하지 않음 |

두 유효 분기는 외부 `on_startup`에서 **이틀 뒤 숨김 이벤트만 예약**하고, 그 이벤트에서 민주 한국·시험 세력·모든 기존 donor 지지도 0을 준비한 뒤 실제 production helper를 호출했다. UI 실행에는 `ai_testing`·속도 defines가 없고 직접 시간 진행을 사용했다. OFF native의 합성 속도·검사 파일과 분리한다. `runtime/corrected-fixture-static-review.json`은 교정한 외부 이벤트의 원본 구문 대조이며 게임 효과 통과의 대체 증거가 아니다.

`runtime/ui-save-roundtrip-comparison.json`은 두 UI 저장의 D04·전용 캐릭터 ID 2090/type73, 중국 원본 ID 885/type73·각 소속·이름·초상화·역할·63코어 보존을 확인한다. 이전 출범의 정상 중점 진행·Huang Tian 화면은 이번 지도자 증거로 재사용하지 않는다.

첫 UI 게임 PID 5336과 재로드 게임 PID 9288은 root의 정상 Quit→OK 뒤 이미 종료돼 backend 강제 종료가 필요하지 않았다. 두 실행의 `process-exit.json`과 `ui/04...png`·`10...png`는 프로세스 확인과 UI 종료 관측을 구분한다. 첫 UI 종료 후 profile 원문·원래 모드 선택을 복원하고 probe pointer를 제거한 다음 PID 9288을 시작했다.

실제 엔진은 `Operation Postern v1.19.5.0.7c6c`, build `Nov 5 2026 14:46:04`다. 최종 OFF checksum은 **bab8**, 최종 ON UI는 **c9f6**, 원래 두 모드·no-probe 재로드는 **6731**이다. 설치 메타데이터의 c184와 활성 모드 checksum을 혼동하지 않는다. `runtime/native-summary.json`은 실행별 실제 version 행을 기록하며 앞선 상수 표기 draft는 별도 이력으로 보존했다. 이 차이로 멀티플레이 동기화를 검증했다고 주장하지 않는다.

유효 최종 형성 로그에서 새 캐릭터·이력·출범 효과의 파싱/모집 경고는 발견되지 않았다. 전체 로그 무오류라는 뜻은 아니다. descriptor 7개·OneDrive 이름 변경·AI 명령 경고는 이번 baseline에서도 비교되며, 최종 실행에서 관측한 현지화 충돌·`map/buildings` 66858·엔진 assertion은 그 관측 시점과 분리한다. OFF의 관련 이름 일치는 시험 저장의 이름 변경 오류였으며 별도의 `_HasCachedTradeInfluence` 엔진 assertion 1건도 보존한다. 이 assertion이나 전체 잔존 로그를 지도자 효과·기존 결함·원본 버그 중 하나로 일괄 귀속할 재현은 하지 않았다. r1 모집 경고 2회와 잘못된 namespace fixture 3건은 후속 유효 실행과 구분한다.

## 최종 보존·종료와 미검증 범위

- `runtime/final-save-preservation.json`: 시작 전 저장 **171/171 SHA-256 불변**, 이번 게임 생성 원본 **4개** 추가(초기 r1 native 1개·최종 OFF native 1개·실제 UI 2개). 원본은 실제 사용자 저장 위치에 두고 사본은 외부 TASK에 보존했다.
- 최종 profile **11/11** 원문 복원, 원래 없던 보조 이름 3개 부재, probe pointer 부재·게임 프로세스 없음. 실제 복원 시각·각 파일 결과는 runtime 복원 manifest를 따른다.
- `runtime/final-source-preservation.json`: 초상화 설정 폴더까지 포함한 runtime 10개 폴더는 **1,596→1,597**, descriptor·기존 thumbnail 3개를 더한 선택은 **1,600→1,601**이다. 앞선 독립 9개 폴더의 **1,595→1,596**과 집계 범위가 다르다. 어느 집합에서도 기존 효과·KCH 이력 변경과 새 캐릭터 추가 외 차이는 없으며 `portraits/00_portraits_KOR.txt`도 불변이다. 최종 3파일 freeze 일치·실행 시작/캡처 간 소스 안정 확인을 포함한다.
- 시작 전부터 Steam의 Running 표시가 남아 있었고, 최종 게임 프로세스 종료 뒤에도 정상 Stop이 Stopping에 머물렀다. 다른 실행 게임과 다운로드가 없음을 확인한 뒤 정상 Steam 종료·재실행으로 실제 녹색 **플레이** 버튼을 복원했다. `ui/00...png`, `11...png`–`14-steam-play-restored.png`, `ui/observations.json`은 root의 실제 관측이며 backend 프로세스 부재로 대체하지 않는다.
- 전체 실행 색인은 `runtime/evidence-index.json`, 합성 두 분기·실패 이력·로그 귀속은 `runtime/native-summary.json`, UI는 `ui/observations.json`을 따른다. 모든 임시 helper·probe·백업·증거는 이번 외부 TASK에 남기며 활성 게임 구성에는 probe를 남기지 않는다.
- `documentation/source-and-doc-check.json`: 편집 전 전체 저장소 **1,890→1,892파일**, 기존 파일 변경 5개·추가 2개·삭제 0개다. production 3개와 유지 문서 4개만 달라졌으며 다른 기존 파일의 SHA-256·Git branch/HEAD가 보존됐다. 수정한 문서 구간의 상대 링크·명시 anchor도 통과했다.

미검증: 기출범 구 캠페인 자동 교체, 미출범 구 저장의 새 history 캐릭터 초기화 호환성, 실제 선거·1965 만료 후계, 1939 시작·장기 AI, 다른 DLC 조합·legacy Korean Language 실제 활성 구성·영어 UI·멀티플레이. 이번 변경의 필수 새 게임 출범·표시·새 저장 왕복 확인과 범위 밖 항목을 구분한다. 추가 게임 실행은 하지 않으며 Git HEAD·branch·기존 작업을 보존하고 커밋·푸시·업로드도 하지 않았다.

저장소의 기존 `docs/assets/korean-fascist-mobilization-validation-20260923/` 시험 PNG 4개·815,391바이트는 정리 미결이며 이동·삭제하지 않는다. 이번 테스트 자료는 모두 외부 TASK에 둔다.
