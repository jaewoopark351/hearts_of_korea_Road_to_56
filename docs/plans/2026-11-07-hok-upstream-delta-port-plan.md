# 2026-11-07 HOK 원본 업데이트 선택 이식 계획

**계획 작성 당시 상태 — 문서화 완료.** 이 문서는 당시의 읽기 전용 비교, 이식 범위와 검증 계획을 보존한다. 후속 승인으로 적용한 파일과 실제 확인 결과는 [구현 기록](../implementation/2026-11-07-hok-resource-prospecting-port.md)에서 확인한다.

## 비교 기준

| 항목 | 2026-11-07 KST 관측 |
| --- | --- |
| 호환판 | `C:\hoi\hearts_of_korea_Road_to_56`, `feat/korean-focus-update-20260922@062053b5fdea9b64174ccb03b04749601a2a083e`, 문서화 시작 시 Git 상태 깨끗함. 별도 Workshop ID `3796816200`, RT56 및 Korean Language 의존성. |
| 원본의 직전 이식 기준 | `5b2595531a376950d07ea264cdb0061b69e1f5ba`. 마지막으로 반영한 민주주의 배치와 유일한 고문 변경을 포함하는 원본 기준점이다. [배치 이식](../implementation/2026-11-01-korean-democratic-layout-port.md) · [고문 이식](../implementation/2026-11-01-ilhan-yu-financial-expert-port.md) |
| 이번 원본 | 읽기 전용 `C:\hoi\hearts_of_korea`, `feat/korean-focus-expansion-ai@f927b3a5defe046967413da05069a0f92823fbec`. `15d6e849f5ce003009122874b40d416091bb58b3`에 1.19.4.2 대응이 들어 있다. 강원·포항 구현은 `korea.txt` 수정과 미추적 런타임 파일 6개로 작업 트리에 남아 있다. |
| 설치 RT56 | Workshop `820260968`, 설치 및 최신 manifest `7553774178744855191`. 물리 경로는 `C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968`이다. |
| 설치 HOI4 및 기존 로그 | 런처 메타데이터 `Operation Postern v1.19.4.2.2da5 (0bdb)`, Steam build `26409260`. 기존 `system.log`의 `(0f96)`은 HOK 원본과 일반판 영어 번역을 사용한 실행이다. 이번 호환판 체크섬과 실제 로드 순서는 미관측이다. |

이 기간의 다른 원본 커밋은 개발 자료 보관 지침(`fd2ea27`), 이전 확인 기록(`ab0f6fb`), 원본 전용 로그 검토 스킬과 안내(`f927b3a`) 갱신이다.

## 강원 탄광·포항 제철소 확장

RT56의 `common/decisions/categories/00_decision_categories.txt`가 제공하는 `prospect_for_resources` 범주를 재사용한다. 설치 RT56의 `common/technologies/industry.txt`에 `construction2`가 있고 `localisation/english/wtt_decisions_l_english.yml`에 `repeatable_decision_tt`가 있다. 호환판의 기존 강원 주에는 석탄 자원이 있다. [원본 동작 명세](../../../hearts_of_korea/docs/HOK_KOREAN_REPEATABLE_RESOURCE_PROSPECTING_SPEC.md) · [강원 주 정의](../../history/states/1144-Gangwon.txt)

| 디시전 ID | 원본 주 → 호환판 주 | 완료 효과 |
| --- | --- | --- |
| `HOK_KOR_expand_gangwon_coal_mines` | 강원 `1029` → `1144` | 강원 기본 석탄 +9 |
| `HOK_KOR_expand_pohang_steelworks` | 경상 `1030` → `920` | 경상 기본 강철 +9. 착수에는 `KOR_pohang_iron__steel_company` 완료도 필요하다. |

- 원본의 `1029`와 `1030`은 RT56에서 각각 스웨덴의 Västerbotten과 Värmland다. 각 디시전의 표시 조건, 착수 판정, 지도 강조, 취소 판정, 보상 직전 재확인, 실제 자원 지급에 쓰이는 주 참조 6곳을 모두 대응시킨다. 지도와 주 history는 기존 호환판 파일을 사용한다. [지도 ID 결정](../decisions/0002-map-id-migration.md)
- 원본의 반복 규칙을 적용한다. 원래 태그 KOR에 한해 대상 주를 소유하면 표시한다. 건설 II 연구, 대상 주 소유와 완전 통제, 항복하지 않은 상태, 가용 민공 9개 이상을 착수 조건으로 둔다. 회당 정치력 25를 지불하고 민공 9개를 90일간 점유한다. 정상 완료 시 자원 +9가 영구 누적되며 별도 대기 기간이나 횟수 상한 없이 재착수할 수 있다. 항복·소유권 상실·완전 통제 상실로 취소되면 공장을 반환하고 자원 보상과 정치력 환급은 없다. AI는 기본 0.5, 정치력 80 미만에서 0, 해당 자원이 1 미만일 때 5배인 원본 조건을 따른다. [원본 디시전](../../../hearts_of_korea/common/decisions/HOK_KOR_resource_prospecting.txt)
- 기존 포항제철 중점의 `completion_reward`에 `unlock_decision_tooltip = HOK_KOR_expand_pohang_steelworks`를 추가한다. 실제 착수 제한은 디시전의 `has_completed_focus`에 두고, 중점의 경상 강철 +25, 선행 관계, 배치, 다른 보상은 보존한다. 생성 관리 중인 `korea.txt`에는 원본 전체 파일 대신 기존 생성 계층에 이 한 중점의 변경을 연결한다. [현재 중점](../../common/national_focus/korea.txt) · [기존 툴팁 이식 사례](../implementation/2026-10-05-focus-decision-tooltip-port.md) · [최신 중점 생성 입력 기록](../implementation/2026-11-01-korean-democratic-layout-port.md)
- 전용 GFX와 DDS 2개를 연결한다. 원본은 Paradox의 같은 게임용 소형 DDS를 그대로 복사해 전용 스프라이트에 연결했다. 석탄은 `33×32`, 강철은 `34×30`이다. 후속 이식 시 원출처, 같은 게임에서의 사용 범위, 크레딧 및 해시를 확인하고 RT56 화면에서 글자와 겹치거나 잘리는지 본다. [자산 크레딧](../../../hearts_of_korea/docs/HOK_KOREAN_RESOURCE_PROSPECTING_ASSET_CREDITS.md) · [자산 manifest](../../../hearts_of_korea/docs/data/HOK_KOREAN_RESOURCE_PROSPECTING_ASSET_MANIFEST.json) · [재사용 전 읽을 개발 자료 안내](../HOK_DEVELOPMENT_ARTIFACT_ARCHIVE.md)
- 양쪽 현지화 헤더에 이름과 설명 4키씩 연결한다. 원본의 최종 설명은 배경 문단만 남겼으며 `l_english`에도 한국어가 들어 있다. 호환판은 한국어 배경 문단을 유지하고 영어 채널에 영국식 영어 번역을 작성한다. 포항의 중점 조건과 기계적 수치는 조건·효과 툴팁에서 확인한다. RT56 한국어 번역의 `replace_path="localisation"`이 있는 구성에서 실제 표시도 확인한다. [원본 명세 12절](../../../hearts_of_korea/docs/HOK_KOREAN_REPEATABLE_RESOURCE_PROSPECTING_SPEC.md#12-2026-11-07-강원포항-설명문-간소화) · [호환판 영어 현지화 기준](../implementation/2026-10-20-english-localisation-import.md) · [언어 계약](../decisions/0003-localisation-contract.md)

## 신아리랑과 1.19.4.2 대응 범위

| 원본 변경 | 호환판 판정 |
| --- | --- |
| `music/Sinarirang.ogg` 48 kHz → 44.1 kHz | **`ASSET_COPY` 후보.** 호환판 기존 실행에서도 같은 샘플레이트 경고가 기록됐다. 새 음원 바이트만 교체하고 `music/hok_music.asset`의 곡 ID·경로·볼륨과 기존 크레딧을 사용한다. [원본 수리 기록](../../../hearts_of_korea/docs/incidents/2026-11-06-hok-runtime-compatibility-implementation.md) · [호환판 로그 감사](../audits/2026-09-23-second-wave-runtime.md) |
| 한국 순양함 보상의 `cl_tech` 삭제 | **현행 호환판 보상 유지.** 설치 RT56 `common/technology_tags/r56e_technology.txt`에 `cl_tech`가 있고 `common/technologies/naval.txt`의 경순양함 연구가 실제 사용한다. 호환판은 `cl_tech`와 `ca_tech`를 모두 적용한다. |
| 일본 방어 트리거 3개 | **별도 호스트 검토.** 바닐라 `common/ai_strategy/JAP.txt`에 호출이 있지만 RT56은 같은 경로의 AI 파일을 제공한다. 현재 설치 RT56과 호환판 검색에서는 해당 호출이 확인되지 않았다. 호출이 입증되면 기존 동아시아 생성기를 통해 한국 판정을 보존하며 검토한다. [동아시아 생성기](../../tools/build_east_asia_overrides.py) |
| 일본 민주 인물 등록, 몽골 국가 history, 핀란드 강화 on_action | **기존 RT56 소유권 및 제외 정책 적용.** 일본 민주 인물과 원본 shared focus는 호환판 범위 밖이다. 몽골 history는 RT56을 사용하며, 원본의 핀란드 강화 파일은 기존 정리 규칙의 제거 대상이다. [소유권 결정](../decisions/0004-hok-korean-content-priority.md) · [분류 규칙](../../tools/build_integration_manifest.py) · [제외 규칙](../../tools/prune_non_korean_content.py) |

## 출처 지문과 재현 경로

아래는 문서화 시점의 원본 작업 트리 SHA-256이다. `korea.txt` 전체 해시는 변경을 골라낼 출처를 식별하며, 적용 대상은 포항 해금 안내뿐이다. 구현이 승인되면 실제 바이트와 아래 지문을 다시 대조하고, 선택한 입력과 결과의 해시 및 분류를 통합 원장에 기록한다. 신규 디시전과 GFX·현지화는 `ADD`, 두 DDS는 `ASSET_COPY`, 중점은 기존 `THREE_WAY_MERGE` 위의 부분 병합이다.

| 원본 상대 경로 | SHA-256 |
| --- | --- |
| `common/decisions/HOK_KOR_resource_prospecting.txt` | `B586D91C5E78773962EFB3BCF6402985072746E6B854813E562D84F4380A2B52` |
| `common/national_focus/korea.txt` | `4BD558791B22433B2EA9D77B58FB1350DFDB3618DA036D3061AE9E7EFA57CEB1` |
| `interface/HOK_KOR_resource_prospecting_icons.gfx` | `587012CEBCC7CFF7642B38EE16D88DB96E4EBEF45F866256A8E0D61EE2BE6401` |
| `gfx/interface/decisions/HOK_KOR/resource_prospecting/gangwon_coal.dds` | `352A18868C7AA8297427CF05F88EB58DF21E067BB85B6B87FE84715636D3B0EA` |
| `gfx/interface/decisions/HOK_KOR/resource_prospecting/pohang_steel.dds` | `688461188713C346CFB7ECF366C64B714C7586ECD7CED64CD5851F9E28602A8A` |
| `localisation/korean/HOK_KOR_resource_prospecting_l_korean.yml` | `8A6C8DD889CF96D9DC58993A60BF86E549C46E05AAF871A7E307C0810A5EF89E` |
| `localisation/english/HOK_KOR_resource_prospecting_l_english.yml` | `EC7F5FEB840D7CFBBC42E4D7755140A090E480F981CAB7B750A8223108FF27D7` |
| `music/Sinarirang.ogg` | `5BC405F3943C2FBF0DDBD60B78D2C01096C622D982540F0CBEF951315FF1575E` |

호환판 비교 지문은 `common/national_focus/korea.txt`가 `DE7959986349B07C014C866B08E03DC2BF0AE81BE80E6AF29D92CF03F572B5B1`, `music/Sinarirang.ogg`가 `2E2209F5C257BD4695C8D74E110A79B7CD1313099F4FCECFD0C5FC6905271749`다. 설치 RT56의 자원 탐사 범주 파일 지문은 `1BF3E4C75C7E9C1D76871FA5DEB4BAAA2EF8C84B9375D8C1E4FC3CE682BD9B84`다.

## 실행 증거와 후속 확인

- **원본 기존 실행.** `C:\hoi\test\hok-resource-prospecting-20261106-01\`에는 포항 중점 조건 추가 전 두 사업을 각각 여섯 번 완료한 기록, 진행 중 저장 재로드, 영토 상실 취소가 있다. `C:\hoi\test\hok-pohang-focus-gate-20261107-01\`에는 준비된 조건에서 포항제철 미완료 차단과 강제 완료 후 허용, 90일 사업 두 회 완료, 경상 강철 추가분 `25 → 34 → 43`이 기록돼 있다. 두 시험은 원본 플레이셋에서 진행됐다. 이후 설명문 간소화는 소스에서만 확인했다. [초기 실행 기록](../../../hearts_of_korea/docs/incidents/2026-11-06-korean-repeatable-resource-prospecting.md) · [포항 연계 실행 기록](../../../hearts_of_korea/docs/incidents/2026-11-07-pohang-focus-gate.md)
- **후속 정적 검사.** 승인된 구현 전 원본과 RT56 지문, 실제 대상 플레이셋을 다시 확인한다. 이식 후 생성 결과, 주 참조 전부, 디시전·스프라이트·현지화 키 충돌, BOM과 헤더, 중점의 기존 +25와 해금 안내, 음원 파일과 등록을 확인한다. 마지막 전체 검사 기록은 **19 PASS / 0 WARNING / 8 ERROR**이며 소스 지문·영어 현지화·descriptor·원장 관련 기존 실패다. 작업 전후 결과를 분리해 기록한다. [기존 검사 기록](../HOK_DEVELOPMENT_ARTIFACT_ARCHIVE.md#13-두-pc에서-같은-문서해시를-사용할-때)
- **후속 호환판 실행.** RT56 단독 대조와 RT56 + 호환판 새 게임에서 원본이 비활성인지 확인한다. 포항 중점 전후 버튼과 기존 보상, 두 아이콘과 양쪽 언어, 정치력 24/25와 가용 민공 8/9 경계, 각 90일 완료와 반복, 해당 주 +9, 취소 시 공장 반환과 무보상·무환불, 진행 중 저장 재로드를 확인한다. 음원은 완전 재시작 후 재생과 샘플레이트 경고를 따로 본다. 강제 준비를 사용한 관측과 정상 연구·중점 진행을 구분하고, 확인하지 못한 저장·DLC·장기 AI·멀티플레이 범위를 기록한다.
- **자료 보관.** 승인된 후속 시험의 helper·백업·로그 사본·저장 사본은 사전에 지정한 `C:\hoi\test\<task-or-run-id>\`에 둔다. 확인된 활성 소스 캐시 `C:\hoi\test\hok-rt56-source-cache\sources\`는 별도 입력 경로다. 기존 `tools/__pycache__/`의 도구 캐시 21개(약 1.04 MiB, 검증기 캐시 포함)는 정리 대기 항목으로 남긴다. 이번에는 게임·검증기 실행, 시험 산출물 생성, 파일 이동·삭제를 수행하지 않았다.
