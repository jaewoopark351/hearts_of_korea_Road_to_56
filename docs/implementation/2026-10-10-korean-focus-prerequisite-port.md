# 2026-10-10 한국 중점 선행 조건 업데이트 이식

## 요청과 결과

사용자의 “원본 업데이트 되었어 / 베낄 수 있겠어?”를 최신 HOK 변경의 구현 요청으로 해석했다. 원본의 마지막 이식 commit 062a602 이후 유일한 commit af6fccf의 한국 중점 6개만 기존 포트 생성기의 마지막 계층으로 이식했다. 원본 전체 runtime을 복사하거나 RT56 공용 시스템을 다시 이식하지 않았다. 실제 runtime 변경 파일은 common/national_focus/korea.txt 하나이며 관리 output 406개 중 나머지 405개는 바이트 그대로다.

이번 변경은 원본의 의도적인 선행 조건 개선이다. 채굴 중점의 요구 조건은 유지하고 표시만 바꾸며, 다른 5개 중점의 진입 조건은 원본과 같이 완화한다. 파서나 RT56 버전 수선으로 설명하지 않는다. 지도·지역 대응·아이디어·결정·현지화·그림·효과·기간·좌표·AI·기존 저장 ID를 추가로 바꾸지 않았다.

## 작업 시작 기준선

| 항목 | 확인값 |
|---|---|
| 호환판 | feat/korean-focus-update-20260922 @ ecc5f0fceefd6ef2d13d7a5958228b2427f7f5dc, 시작 시 clean |
| 원본 | feat/korean-focus-expansion-ai @ af6fccf2248311c01565c796555ed334ec685015, clean |
| 직전 원본 | 062a60287e00ac11352c38bca0fca1ae556e7801 |
| 조사 시각 | 2026-10-10 21:25:55 KST |
| 설치 HOI4 | Steam build 25205862, revision c01a3d507f10bd8c713e88234de69ca110618138 |
| 최신 로그 버전 | Operation Postern v1.19.3.0.c01a (92cd), 2026-10-10 19:12 KST donor 단독 실행 |
| RT56 | item 820260968, installed/latest manifest 7553774178744855191 |
| RT56 업데이트 | 2026-10-09 08:58:55 KST |
| RT56 한국 중점 | SHA-256 A80FBC767C21902FC56EBBCA35DC3C120700E527B52EA98F3CFDF5221EB0EF90, 이전 한국 base와 동일 |
| OS / 언어 / GUI | Windows 11 x64, l_korean, GUI scale 1.000000 |
| 사용자 데이터 | `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV` |
| DLC | 최신 donor 로그의 active 36개; dlc_load.json disabled DLC 없음 |

현재 active playset 국뽕한국 test01은 donor 단독이다. 저장된 HOK RT56 Audit C0 20260922는 RT56 → RT56 Korean Translation → 호환판, Road to 56 한국 test01은 호환판 → RT56 → RT56 Korean Translation 순서를 기록하며 두 target 모두 donor가 없다. 현재 설정을 그대로 읽었으며 변경하거나 게임을 실행하지 않았다. 목록 순서는 유효 파일 우선순위의 엔진 증거가 아니다. 현재 donor 로그의 checksum·36 DLC를 호환판 실행 결과로 전용하지 않는다.

호환판 repository와 물리 launcher descriptor는 이 worktree, 1.19.*, RT56 + Korean Language, 기존 호환판 item 3796816200을 유지한다. 원본 item 3793992662나 historical HOK item 2898629778을 이식하지 않았다. RT56의 history/states·map/strategicregions replacement, 번역의 localisation replacement와 선언 의존성/실제 target 언어층 불일치를 확인했다. 최종 localisation 계약은 기존과 같이 미확정이다.

Descriptor SHA-256: 호환판 D68DCE620EA3DDDE422F26F2E5155E4D52F35AC4B2EBE1224DC71E07035141CB, launcher A486F1BD484486BE9BE4668E61C7B7B8DAC292C2E7474EC0258BF6F02C885BF4, donor 3FBC6868A7D95BACD6B55AF71593A61AF3A7EADA5654D46CC4C828422ECA032A, RT56 5B323861ABD63E31CB896277E3EA58BA4BCD9FCEEDA957B50792065E42E03F61, Korean Language F5813D345DD0FC01E80F68B65901B1D060A238336D3D2A89EAA8404A40329346, RT56 Korean Translation A0508F4A91AF911917AD3A84BF829CB38ED1557DD8F9643A010F1AEE36F48D6C.

## 선택 변경과 네 소스 검토

| focus ID | 원본과 동일한 변경 | 유지되는 주요 조건 |
|---|---|---|
| HOK_KOR_cmn_ore_classification | 함경도 완료 검사를 별도 prerequisite로 이동해 운산·함경도 두 AND 연결 표시 | 두 중점 모두 완료, 내전 없음 |
| HOK_KOR_cmn_export_invoices | 경공업 수출 지원 완료 조건 제거 | 원화 평가절하 선행, 내전 없음 |
| HOK_KOR_cm_court_clerks | 사법부 독립 완료 조건 제거 | 총리 지명 선행/완료, 민주, 내전 없음 |
| HOK_KOR_cm_public_patronage | 현대의 세종대왕 완료 조건 제거 | 총리 지명 선행/완료, 민주, 내전 없음 |
| HOK_KOR_nrsc_military_administration | 세계위에 군림하는 대한 완료 조건 제거 | 참모 규정 선행, 파시즘, 을해군란 완료, 내전 없음, 실제 비핵심 주 완전 통제 |
| HOK_KOR_nrsc_interservice_liaison | 선군주의 완료 조건 제거 | 구국위원회 권한 강화 선행, 파시즘, 을해군란 완료, 내전 없음 |

F4의 civil_supply_offices·claims_accounts·civil_administration_rules는 계속 KOR_korea_reigns_above_the_world를, F5의 joint_logistics_board·joint_dispatch_records·service_supply_rules는 계속 KOR_prussia_in_the_far_east를 요구한다. 연락반의 기존 을해군란 완료 검사도 남는다. 병렬 모듈 전체나 후속 조건을 일괄 완화하지 않았다.

생산 파일과 원본의 직전/최신 immutable focus blob을 비교했다. 대상 6개 ID는 RT56·vanilla 중점 DB 및 두 언어 mod에서 충돌하지 않는다. RT56 한국 중점 파일은 기존 pin과 바이트 동일하다. Vanilla에 korea.txt는 없으며 설치 generic.txt:58 및 :277–278의 같은 national_focus 문맥에서 prerequisite와 여러 sibling prerequisite 구조를 확인했다. Vanilla generic SHA-256은 DA7D2AD989FE174A904838D55481BCFD07D652940260466259CB27DD21893768이다. available은 country trigger 문맥을 유지하고 existing any_controlled_state의 ROOT/주 scope를 그대로 둔다.

분류는 한국 트리의 기존 OVERRIDE를 유지한다. ADR-0004의 한국 HOK 우선 소유권에 따라 해당 authored delta를 가져오고, RT56 한국 tree를 선택하는 대안은 채택하지 않았다. 최신 source manifest로 일반 RT56 world rebase가 완료됐다는 뜻은 아니다.

## 독립 출처와 생성기

[새 lock](../../tools/hok_focus_prerequisite_update_lock.json)은 여섯 개 before/after span, 두 Git blob, 원본 LF/CRLF 해시, 직전/최종 포트 해시를 고정한다. 기존 source/artwork/second-wave/policy/localisation/material/prose/tooltip lock 8개는 수정하지 않는다. 원본 AGENTS는 이전 이식 때와 동일한 3DB3917841B773F1264EDD310916FD8CB676A963331C500C9C6EEDBE7832FF40이므로 지침을 다시 동기화하지 않았다.

| 바이트 | SHA-256 |
|---|---|
| 최신 source LF blob b646b92912c81e78219830efd4e76a7e881086df | 877AA911F613E26F3351BB3A2E4EC8110D20BB9404911F945A5B526DBF2923A3 |
| 최신 source CRLF checkout | E2C2E7B028D8D6D922114C68474B7A569D2AA11CBCF109CA20A4168CACFF47CA |
| 직전 source blob 7cc1d3c41f643ef65db5b88d1b7ad7696f109be5 | 377787CD86EC6E51A153215FD596EC3752BC9486B0F92E856F4569C218A93B2A |
| 직전 포트 출력 | 4A349FE1631C7A79B178C24C241F00F3E20C20F3B59E061FE1FE6B59DB5F74E1 |
| 최종 포트 출력 | EB78279B778326F1EC6B08932533CE2FDEEA618C6872610A0A7746E0FDE50AD4 |

source_snapshot.py는 실제 immutable source diff가 여섯 span과 정확히 같은지 검증한다. 생성기는 기존 tooltip 이후에 이 계층을 적용하고 알려진 직전 output만 교체한다. 생성된 production 파일은 손으로 수정하지 않았다. checker는 독립 ordered AST로 보상·기간·좌표·AI와 나머지 중점/연결이 그대로인지 확인하고, 기존 material/tooltip 보존 검사는 새 계층을 정확히 역변환한 ancestor와 비교한다. .gitattributes는 새 lock LF와 문서 byte-exact 계약만 추가한다.

원본의 변경 명세·candidate metadata·사건 기록 7개를 [별도 snapshot](../upstream/hok-prerequisite-update-20261010/README.md)에 Git blob 바이트 그대로 보존했다. 원본의 초기 UI 관찰과 정상 진행 미검증은 원본의 기록이며 포트 증거로 복사하지 않는다.

## 기존 RT56 source drift와 원장 보존

RT56은 이전 pinned manifest 7475007536894105204에서 업데이트됐다. 직접 선언된 RT56/vanilla 입력 해시 56개 중 49개가 일치하고 RT56 7개가 달랐다. Vanilla 17/17, RT56 32/39 일치다. 이는 이번 donor 이식 이전에 존재한 host drift이며 기존 assertion을 새 hash로 덮어쓰지 않았다.

| RT56 path | 기존 pin | 현재 SHA-256 |
|---|---|---|
| common/decisions/JAP.txt | 1FADB70D82C806EFE8A3112B81FDE3665E52B96160376AD7D74784BAC2A9B5F3 | 750E82102C3B7F09F8861B5FC61D043A44E9CD8055DF98810B63F7042082F96E |
| history/countries/JAP - Japan.txt | 799186C2BC9B9CD45340AEBD6038DC7B29DAFD89DB5B4E3E77BC9AF62F62E405 | D9F98076E334CD7ABC2F1A1B2DBC74C4909900C81695AD2E26A1825C8AF08206 |
| map/railways.txt | 0CFEF6244DF5A04A8EBE0C1027C27287C375F31CBDA94F265FC549DF6CC61547 | 52E60257F9490A27E7AC6EFD07BDD34FD46B0FBE82D2BA55A5558F25C1A7392D |
| common/military_industrial_organization/organizations/00_generic_organization.txt | C701A3CFF92AF46925932241E156B9B5F340FAEDCF228BB103F74B985F6F5D35 | 02A80CAB1C40E5F8F4065F14A8D151795F896F134170D9ED16008D2DFDFB8AC0 |
| common/bookmarks/the_gathering_storm.txt | 064C1ABB1475B8EBFD4E53CAB3D4DCE77CE37B4BE0A0A9EE6EA53988FB36F3B9 | 5227DA7C5FE362AB8A4FCA1F5B99321B125FA933D05E19A8239BDA223286C0F6 |
| history/general/generic_advisors.txt | 4EA203FEF355255ABB28A7E59DCEDD3926C764D5CC4844C2B3D9B2269A65923C | D4B58E25672F0E6F91D531BDC01B1E3769A5E2F41E992B580816CD8E726D99B6 |
| history/countries/GER - Germany.txt | 563BBCD053E90E193DD30A9D1BF515609E2E260451E911AA81D3A1012F074101 | 4911E0AFA6A49739C352F9A383C99E0DA2D4A41C5E43460E983E1D30A0358228 |

원장에 기록된 exact-path 충돌 73개도 현재 host와 비교했다. 과거 host-base와 현재 파일이 다른 행은 7개이며, 위 direct-pin 목록의 GER 대신 common/intelligence_agencies/00_intelligence_agencies.txt가 포함된다. 해당 기관 파일의 과거 hash는 D27517C12FF352C7AF1ACF63CFACF9AB30365CB7C676529F51167281F5261435, 현재 hash는 28F74F81FACDC4D59E8079783CD37DD3C9F677DCB75D11B50380FFFF2B8397AD다. 두 목록의 합집합은 RT56 8개 경로이며, 두 조사 범위의 7개 수량을 전체 변경 파일 수로 오해하지 않는다.

원장은 이번에 변경하지 않은 generated output의 실제 제작 base를 유지해야 한다. 기존 generator의 live RT56 hash 기록을 그대로 쓰면 과거 bookmark·JAP·advisor·railway output을 새 RT56 base에서 합성한 것처럼 잘못 기록한다. 그래서 새 lock에 ecc5f0f의 immutable 원장 blob a335a17c05f02131d94aa75c679f783b76493ca7, SHA-256 5E0BD5F54302B405E11EAA8465FB52524716A17AA85433F1D7853F2616AA9DEB를 별도로 고정했다. 원장 생성기는 host가 달라졌어도 output이 이 과거 원장과 바이트 동일할 때만 과거 host-base hash를 보존한다. 같은 host drift 상태에서 changed output은 rebase 검토 없이 받아들이지 않는다. USE_RT56 행은 실제 사용 중인 live host를 기록한다. 이 provenance 보정은 기존 input assertion을 통과시키지 않으며 RT56 gameplay 파일을 갱신하지 않는다.

한국 중점 행은 최신 donor 출처·최종 output과 unchanged Korean RT56 base를 기록하고 직전 tooltip 출처를 보존한다. 원장 row 수·분류·exact-path collision 수는 그대로다.

## 검증과 한계

- python -B tools/check_korean_second_wave.py --check: PASS. 여섯 source/runtime edit, AND grouping, 정부·내전·을해군란·통제 gate, 후속 정책 조건, 보상·기간·좌표·AI, 기존 material/prose ancestor, 자산·현지화·reference 검사를 통과했다.
- python -B tools/check_korean_second_wave.py --self-test: PASS, 51개 의도적 회귀 거부. 기존 35개와 신규 prerequisite 변형 16개를 메모리에서 검증했다. 잘못된 mining OR/AND·부모, 삭제 조건 재삽입, 보상 변경, 실제 통제·을해군란 조건 제거, 여섯 후속 정책 gate 제거 등을 거부했다.
- 원장 provenance helper: 현재 host drift의 unchanged output 7개는 과거 base를 보존, 같은 7개를 altered output으로 준 경우 모두 거부, USE_RT56로 준 경우 7개 모두 live hash 선택. 메모리 검사이며 production/file 쓰기 없음.
- python -B tools/build_integration_manifest.py --apply: 1,417행·충돌73개·분류 수량 유지, CSV diff는 한국 중점 1행뿐. 최종 원장 SHA-256 2BE36E7E1A1662CE3EAEC1263212E3EC430A1BA0E93AA32284A5F9AFF13E1AD7.
- 최종 python -B tools/validate_port.py: **17 PASS / 0 WARNING / 4 ERROR**, exit 1. source snapshot·한국 자산·pruning·ID 이식·한국 중점 생성·독립 의미 검사·원장·구조·descriptor·현지화·ID/reference 검사는 통과했다. 오류는 map synthesis의 railway, shared overrides의 공용 base, East Asia overrides의 JAP, doctrine migration의 GER source drift다. 새 중점 오류 또는 전체 clean 결과로 설명하지 않는다.
- 최초 aggregate는 16 PASS / 0 WARNING / 5 ERROR로 같은 source drift 4개와 stale 원장을 보고했다. 검사와 checker 편집 시간이 겹쳤으므로 엄밀한 clean pre-change 실행 증거로 사용하지 않는다. host source 차이는 독립 읽기 전용 hash inventory로 변경 전 확인했다. subsystem 최초 실행의 과거 prose ancestor 역변환 누락은 두 역사 보존 callsite를 함께 역변환하도록 수정한 후 최종 두 검사를 통과했다.
- 이전 기록의 KOR history MtG war support 0.1/0.05 생성 불일치는 그대로 남으며 이번 doctrine 검사는 먼저 GER source drift에서 멈춘다. 기존 history 문제의 해결로 보고하지 않는다.
- git diff --check: exit 0. 실제 runtime diff는 원본과 같은 여섯 span/19줄(13추가·6삭제)이며 파일 추가·삭제·encoding mass conversion이 없다. 기존 lock 8개·원본 clean HEAD/checkout·RT56 manifest/한국 tree hash를 변경 후 재확인했다.
- 모든 검사·진단 출력은 stdout 또는 메모리에서 확인했다. 새 test/diagnostic file·로그 사본·fixture·screenshot·save는 만들지 않았다. Python은 -B로 실행했다.


이번 작업은 source 이식과 정적 검증까지 수행한다. HOI4 실행, playset 전환, 설정·로그·세이브 변경, console 강제 효과, 실제 UI·35일 진행·취소·정치 선택 후 SHOW/HIDE·AI·장기 진행·DLC 대조·저장·멀티플레이는 미실행이며 UNPROVEN이다. 이번 narrow patch만으로 최신 RT56 전체 호환 또는 출시 준비 완료를 주장하지 않는다. 다음 별도 workstream은 위 두 인벤토리의 host drift 실제 delta와 생성 output을 새 RT56 base에서 검토·재병합하는 것이다.

이식·정적검증 완료 시점에는 Git commit·push·tag·Workshop publication/update를 수행하지 않았다. 원본·Steam·게임 설치·user-data는 읽기만 했으며 시작한 clean worktree에 이번 변경을 남겼다.
