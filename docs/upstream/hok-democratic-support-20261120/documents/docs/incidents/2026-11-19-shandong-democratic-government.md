# 2026-11-19 산둥 자유 공화국 출범·민주세력 귀순 구현 기록

이 기록은 **SND 전면 편입 전 소스의 구현·실행 이력**이다. SND 영토 전체 기본 편입이나 소멸 시 잔여 자산 처리를 변경·검증할 때는 [후속 구현 기록](2026-11-19-shandong-full-integration.md)과 [현행 계약 19절](../HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_PLAN.md#19-shandong-warlord-integration-implementation)을 먼저 읽는다. 아래 관측을 후속 소스의 통과로 재사용하지 않는다.

작성: **2026-11-19 (Asia/Seoul)**. 상태: **구현 소스·최종 6사례 네이티브 효과·실제 UI 완료 흐름·첫 새 저장의 fresh-process UI Load·설정/기존 저장 보존·Steam Play 복귀 확인**. 검증한 소스·사례·화면·저장 왕복 범위와 아래 미검증 항목을 구분한다.

최신 사용자 선택으로 **육군·해군·공군을 같은 비율로 귀순**시키는 계약을 확정했다. 현재 동결 소스는 실제 영토 합류 donor의 양수 지지도 비율 p를 `size`·`army_ratio`·`navy_ratio`·`air_ratio`·`stockpile_ratio`에 모두 적용하고 기존 지휘관을 원국에 유지한다. 앞선 해군·공군 보존 설계와 0 비율 실험은 아래 실패·의사결정 이력이며 현재 효과 계약이 아니다. 서비스 20%/70% 독립 통제와 기지 보정 후 최종 6사례를 아래에 소스별로 기록했다. 실제 UI에서 가용 조건·효과 안내·직접 시작 뒤 보통 시간 진행에 따른 완료·피감독국 표시를 관측했다. 첫 새 저장을 원래 playset의 완전히 새 프로세스에서 UI Load하여 정부·관계를 복원하고 며칠 진행·재저장한 범위도 확인했다. 명목 35일의 정확한 달력 경과·두 번째 저장의 재로드·변경 전 저장·모든 DLC·멀티플레이와 최종 원복은 아래에서 별도 판정한다.

사용자는 [기능 계획 16절](../HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_PLAN.md#16-shandong-democratic-government-design)의 전체 구상을 인용하고 `AGENTS.md, /docs 읽고 구현해줘`라고 요청했다. 앞선 설명·문서화 전용 단계에서 확정한 방향과 이번 구현 승인을 구분한다. 기존 「중국 독재자 축출」의 출범 보상을 확장하는 계속개발이며, 지도 자체 변경·별도 내전국의 대량 생성·자동 선전포고·별도 공동 참전·커밋·푸시·업로드는 범위에 포함하지 않는다.

이 기능의 주 목록·핵심주·영토 이전 조건을 변경할 때는 [변경 영향 검토 절차](../HOK_CHANGE_COVERAGE_REVIEW.md), [주 참조 검토 스킬](../../.agents/skills/hok-state-reference-review/SKILL.md)과 [유지되는 지리·출처 대장](../data/HOK_KOREAN_CHINESE_GOVERNMENT_STATE_GROUPS.json)을 먼저 읽는다. 이름·조건·효과 안내를 변경할 때는 [현지화 검토 스킬](../../.agents/skills/hok-localisation-review/SKILL.md)과 [두 채널 계약](2026-09-01-localisation-contract.md)을 적용한다. 실제 로그 오류나 원인을 판정할 때는 [로그 검토 스킬](../../.agents/skills/hok-log-review/SKILL.md)을 먼저 읽는다.

## 기준과 자료의 역할

| 구분 | 이번 기준·역할 |
|---|---|
| 개발 소스 | `C:\hoi\hearts_of_korea`; 권위 있는 working tree |
| 브랜치·HEAD | `feat/korean-focus-expansion-ai` / `0c19f58fa7a9ff898196dcdbe46edfd0ad5fdbbc` |
| 시작 작업 트리 | 기존 민주인사 지원·정보국 코드와 문서·현지화·시각 자산 변경이 있는 상태. 해당 작업을 보존하고 이번 delta를 적용 |
| 설치 원본 V | `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV`; 읽기 전용 구문·지도·효과 원본 |
| 설치 버전 | `launcher-settings.json`: `Operation Postern v1.19.5.0.7c6c (c184)`; 설치 메타데이터이며 새 실행 체크섬은 별도 기록 |
| 원작 구버전 | `C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\2898629778`; 읽기 전용 역사 출처. 편집·업로드 대상 아님 |
| 실제 사용자 데이터 | `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV`; 게임 원본 로그·저장 위치 |
| 외부 작업 TASK | `C:\hoi\test\hok-shandong-democratic-government-20261119-01\`; helper·백업·probe·로그/저장 증거 사본·검사 출력 위치 |
| 외부 영어 번역 | `C:\hoi\Hearts of Korea English Translation Anime Modder's Edition`; 활성 덮어쓰기 대조용이며 수정하지 않음 |

`TASK/source-baseline.json`은 구현 전 runtime 파일 **1,591개**의 해시와 시작 Git 상태를 기록한다. `TASK/baseline-source/`에는 중점·재건 결정·기존 중점 현지화 두 파일·본 계획·2차 계획·README의 **7개 사본**이 있다. 이 기준은 이전 16태그 지원 확장 작업의 기준·검사 수와 합산하지 않는다.

## 적용한 코드와 표시 경로

| 파일·ID | 이번 변경 | 유지·제외 |
|---|---|---|
| [한국 중점](../../common/national_focus/korea.txt)의 `KOR_overthrow_the_chinese_dictators` | MtG·KCH 부재·원소유국이 첫 이전 뒤 생존하는 산둥 bootstrap 거점 조건 추가, 가용성 상실 시 취소, 출범 helper 호출과 고유 효과 안내 연결 | ID·아이콘·좌표·선행·35일·AI 및 기존 한국의 16태그 전쟁명분 loop 유지 |
| [신규 상태·국가 판정](../../common/scripted_triggers/HOK_KOR_chinese_government_state_triggers.txt) | donor·63주 본토·이전 가능 주·첫 bootstrap 주·출범 가능 조건 분리 | 기존 지원 대상 공용 트리거 정의와 지원 비용·기간은 변경하지 않음 |
| [신규 출범 효과](../../common/scripted_effects/HOK_KOR_chinese_government_effects.txt) | 핵심주 helper, 원소유국별 지지도·영토 예산, 연결 주 선택, 단일 생성국·피감독국 지정, 조건부 비행장 확보, 실제 전력 귀순과 임시 자료 정리 | `start_civil_war`·`declare_war_on`·`add_to_war`·매일 on_action 추가 없음 |
| [기존 중국 재건 결정](../../common/decisions/KOR_decision.txt)의 `KOR_New_China_Government` | 핵심주 지급 목록을 출범과 같은 63주 helper로 연결 | 한국 독립·KCH 동맹·CHI 한국 종속 조건, CHI만 합병·`KCH_china` 외형·비용·일회성 유지. 다른 군벌 일괄 합병 추가 없음 |
| [기존 한국어 중점 현지화](../../localisation/korean/korea_focus_l_korean.yml)·[paired English 채널](../../localisation/english/korea_focus_l_english.yml) | 중국 축출 설명·기존 효과 안내 2키와 인접 기여 주석 변경 | 다른 키·기존 주석·BOM·CRLF 유지 |
| [고유 Korean 안내](../../localisation/korean/HOK_KOR_chinese_government_l_korean.yml)·[paired English 채널](../../localisation/english/HOK_KOR_chinese_government_l_english.yml) | 가용 조건 3키와 `HOK_KOR_chinese_government_effect_tt` 제공 | 본체 두 채널 모두 같은 한국어 본문. 외부 번역 저장소 편집 없음 |
| [지리·출처 대장](../data/HOK_KOREAN_CHINESE_GOVERNMENT_STATE_GROUPS.json) | 본토·만주 제외·섬/조차지·산둥 인접과 설치본 출처 기록 | runtime 효과 실행·면적 비율·게임 UI 검증 보고서가 아닌 유지 대장 |

## 지리와 보호 조건

출범 핵심주와 영토 후보의 기하 범위는 **63주**다. 기존 KCH 재건 범위를 근간으로 현행 중국 분할 주를 포함하고, 만주와 섬·외국 조차지를 제외했다. 전체 ID·각 주의 현재 이름·원본 역할은 [주 집합 대장](../data/HOK_KOREAN_CHINESE_GOVERNMENT_STATE_GROUPS.json)에 둔다.

**601 참도**는 현재 CHI 핵심주가 아니고 초기 TIB 소유지만 기존 KCH 재건 핵심주였으므로 의도적으로 유지한다. 이는 TIB를 지원·귀순 대상에 추가한다는 뜻이 아니다. 실제 영토 이전에는 아래 donor 소유·통제 조건을 별도로 적용한다.

만주 지리 제외는 **328·610·714·715·716·717·745·761**, 섬·외국 조차지 제외는 **326·524·591·728·729**다. 산둥 기본 거점은 기존 **597·743**을 유지한다. 원본 지도 경계에서 597↔743, 597↔1038의 육지 연결을 확인했으며, 기존 기본 거점을 지난 1038로 무조건 확대하지 않았다.

이전 가능한 주는 본토 63주 안에 있고 **소유국과 통제국이 각각 적격 중국 donor**여야 한다. 기존 정식 16태그·현존·동적 국가 제외 조건을 재사용하며, 일본의 직접 종속국과 일본 종속국의 종속국을 donor에서 제외한다. 한국 소유 또는 한국 통제 조건은 별도로 부정하여 어느 한쪽만 한국이어도 이전하지 않는다. 따라서 중국 명목 소유의 한국 점령지, 한국 소유의 외국 점령지, 일본 측 소유·통제 지역은 모두 영토 이전에서 빠진다.

이 판정은 추가 영토뿐 아니라 최초 597·743 지정에도 적용한다. 최종 `HOK_KOR_chinese_government_can_bootstrap_state`는 이전 가능 조건에 더해 **원소유국의 `num_owned_states > 1`**을 요구한다. 원국을 첫 영토 이전으로 소멸시키지 않고 실제 전력을 먼저 이관하기 위한 조건이다. `can_form`과 중점 가용성은 이 안전한 초기 거점이 597·743 중 하나 이상일 때만 허용한다. 두 거점 모두 마지막 주인 원소유국에 속하거나 보호·제외되어 이 조건을 만족하지 못하면 중점을 차단한다. 진행 중 안전한 거점 조건을 잃으면 `cancel_if_invalid = yes`·`continue_if_invalid = no`로 취소한다. 보호를 풀거나 다른 지역을 임의로 빼앗는 fallback은 추가하지 않았다.

## 지지도·영토 예산과 실행 순서

`HOK_KOR_form_chinese_democratic_government`의 입력은 한국 국가 scope다. 실행 시 donor마다 민주주의 지지도를 읽어 `p = clamp(party_popularity@democratic, 0, 0.90)`로 보관한다. 적격 소유 주 수 `N`을 세고 영토 예산을 `N × p`로 설정한다. 선택할 때마다 원소유국 예산에서 1을 빼며, 추가 선택은 잔여 예산이 1 이상일 때만 하므로 소수 잔여분은 추가 주를 만들지 않는다.

적격 597·743은 기본 거점으로 먼저 선택하되 각 원소유국의 예산을 소모한다. 예산보다 기본 거점 수가 많아도 그 적격 거점은 보존하며, 그 경우 해당국의 추가 편입은 없다. 따라서 기본 거점을 제외한 추가 주 수는 `floor(N × p)`에 기초하지만, 전체 영토가 모든 경우 정확히 그 비율이 된다고 설명하지 않는다.

원소유권을 바꾸기 전에 후보·선택 표식을 이용해 연결된 주를 계획한다. 각 추가 주는 선택된 주와 인접해야 하며, 고립된 원거리 고지지도 국가에서 바로 영토를 떼어오지 않는다. 반복은 진전 여부와 **최대 63회**로 제한한다. 선택된 주가 각 donor 예산을 소비하므로 국가별 지지도를 단순 합산하거나 군벌 수만큼 최소 주를 지급하지 않는다.

선택이 끝나면 `create_dynamic_country = { original_tag = KCH }`로 하나의 새 정부를 만들고 실제 생성국을 `save_global_event_target_as = HOK_KOR_chinese_democratic_government`로 저장한다. 생성국 자식 scope에서 저장한 일반 event target이 이 호출 경로의 바깥 효과에 전달되지 않은 최초 실패를 교정한 방식이다. 민주정부·핵심주를 지정한 뒤 원국이 생존할 수 있는 첫 거점 하나와 수도를 확보한다. **597이 bootstrap 조건을 만족하면 597, 그렇지 않으면 bootstrap 가능한 743**을 첫 거점으로 사용한다. 공군 귀순이 필요한데 자체 비행장이 없으면 선택된 기존 비행장 주를 안전하게 먼저 이전하고, 불가능하면 확보한 KCH 수도에 조건부 비행장 1단계를 지원한다. 모든 참여국의 전력을 한 번씩 이관한 뒤 나머지 기본 거점과 선택 영토를 이전한다. 마지막에 피감독국·기존 세력 편입을 처리하고 임시 주/국가 표식과 예산·비율·반복 변수를 정리하며, 생성국 global target도 `clear_global_event_target`으로 지운다.

위 구문·scope의 근거는 설치본 `documentation/effects_documentation.md`의 `create_dynamic_country` 3033–3043행, `transfer_units_fraction` 8348–8377행, `while_loop_effect` 8573–8587행과 `documentation/triggers_documentation.md`의 `any_neighbor_state` 1497–1504행이다. 실제 생성국 target 저장·사용은 `events/France.txt` 1208–1210·1353–1360행, 반복·인접 주 조회는 `common/scripted_effects/ITA_scripted_effects.txt` 3103–3120행 및 `events/LAR_occupation.txt` 276–301행의 같은 게임 버전 사례를 참고했다. 소스 구문 근거와 실제 엔진 처리 결과는 구분한다.

## 실제 전력 귀순·국가 지위·기존 저장

실제 선택 영토가 있는 donor만 참여국으로 표시한다. 최종 효과는 **p > 0인 참여국만** 실행하며, `size`·`army_ratio`·`navy_ratio`·`air_ratio`·`stockpile_ratio`를 모두 같은 `var:HOK_KOR_chinese_government_share`로 지정한다. p는 앞서 읽은 민주주의 지지도의 0–0.90 제한값이며 **육해공·비축 장비·연료의 공통 입력 비율**이다. p = 0이면 이관 명령 자체를 건너뛴다. `keep_unit_leaders_trigger = { always = yes }`로 기존 지휘관은 원국에 유지한다. 고정 사단이나 새 물자를 군벌 수만큼 생성하지 않는다. 실제 병종별 반올림·함정/항공기·장비·연료 분배는 최종 소스의 독립 통제와 출범 사례에서 확인하며, 명령의 입력값만으로 정확한 모든 자산 비율을 보장하지 않는다.

첫 기본 거점 이전으로 한 주짜리 donor가 소멸하면 그 뒤 전력 이관이 유효한 원국을 요구하여 실패하는 현상이 네이티브 사례에서 확인됐다. `every_possible_country`로 순회하는 것만으로는 엔진의 non-existing 국가 거부를 해결하지 못했다. 새 국가에 먼저 전력을 보내고 나중에 첫 영토를 주는 대안도, 0주 생성국이 non-existing 수혜국으로 거부되는 독립 사례로 성립하지 않았다. 따라서 최종 소스는 첫 donor가 이전 뒤에도 남을 수 있는 bootstrap 거점을 요구하고 전력을 먼저 이관한 뒤 나머지 영토를 옮기는 순서를 사용한다. 정리 순회는 소멸국의 임시 표식·변수도 지우기 위해 `every_possible_country`를 유지한다.

한국 scope에서 생성국에 `autonomy_supervised_state`를 지정한다. `set_autonomy`의 전쟁 종료 기본값에 의존하지 않고 `end_wars = no`·`end_civil_wars = no`를 명시한다. 피감독국은 일반 규칙상 참전 요청을 거절할 수 있으며 자동 공동 참전을 보장하지 않는다. MtG가 없을 때 일반 puppet으로 조용히 대체하지 않고 해당 출범 중점을 차단하는 정책을 선택했다. 기존 KCH가 존재해도 중복 clone·강제 지위 변경을 피하도록 차단한다.

한국이 받는 기존 `puppet_wargoal_focus` loop는 공용 16태그 검사·한국 ROOT actor·PREV target을 보존한다. 영토 보호·제외 때문에 기존 지원 대상이나 전쟁명분 대상을 줄이지 않았다. 별도 선전포고·참전 연결은 없다.

기완료 중점 저장에 정부를 재생성하거나 핵심주·영토·병력을 소급 지급하는 migration은 추가하지 않았다. 이후 기존 재건 결정을 정상 실행할 때는 새 공통 핵심주 helper를 사용하지만, 이미 끝낸 결정을 재개방하지 않는다. 실제 변경 전 저장의 로드·진행·재저장·재로드는 아직 별도 검증 대상이다.

## 현지화 이관과 정적 확인

가용 조건 키 `HOK_KOR_chinese_government_mtg_tt`·`HOK_KOR_chinese_government_no_existing_tt`·`HOK_KOR_chinese_government_seed_tt`는 최초에 기존 `korea_focus_l_*` 두 파일에 추가했다. 외부 번역이 같은 파일명을 통째로 덮는 경로를 고려해 새 `HOK_KOR_chinese_government_l_*` 두 파일로 옮겼고, 고유 보상 키 `HOK_KOR_chinese_government_effect_tt`도 같은 파일에 추가했다. 중점은 이 고유 보상 키를 사용한다. 기존 중국 축출 `_desc`·`_tt`의 수정 본문은 기존 paired 파일에 유지했다.

새 두 파일은 본체 언어 계약에 따라 각각 locale header만 다르고 한국어 본문이 같으며, 동일한 기여 주석을 header 바로 뒤에 둔다. 현재 외부 영어 번역에는 새 동명 파일이 없다. 따라서 고유 가용·효과 안내는 새 경로로 제공한다. **영어 locale의 기존 중국 축출 설명은 외부 영어 채널의 오래된 본문이 우선할 수 있는 소스상 제한**이 남지만, 이를 실제 한국어 UI의 덮어쓰기 오류로 보고하지 않는다. 외부 번역 저장소는 수정하지 않았다. 원래 HOK+외부 English Translation playset의 실제 한국어 UI에서는 새 설명·새 효과·조건부 비행장·보호·개별 인정 결정 해금과 피감독국 툴팁이 표시됐다. 영어 UI·모든 차단 분기·모든 해상도의 줄바꿈과 높이까지 확인한 것은 아니다.

최초 현지화 쓰기에서 PowerShell 변수명의 대소문자 구분이 없다는 점을 놓쳐 `taskNewline`·`taskNewLine`이 충돌했다. 즉시 UTF-8 재읽기에서 잘못된 주석·키 삽입을 발견했고, 외부 baseline의 정확한 원문에서 변수명을 분리해 교정했다. 오류 사본은 `TASK/localisation/first-write-error/`, 고유 파일 이관 전 사본은 `before-dedicated/`에 보존했다. 이 도구 쓰기 오류를 게임 parser 오류나 런타임 통과 이력으로 바꾸지 않는다.

`TASK/localisation/source-checks.json`은 고유 파일 이관 당시 네 현지화 파일의 BOM·CRLF, 각 언어 채널 본문 일치, 새 네 키의 단일 정의, 기존 파일에서 허용된 두 키와 새 기여 주석 외의 원문 동일성을 확인한다. 이관 전 결과는 `source-checks-before-dedicated.json`에 보존했다. `TASK/geography/geography-inventory.json`은 현재 설치본 주/지도 출처와 경계 조사를, `independent-source-review.json`은 원문 보존·scope·한 주 donor·정리 순회의 소스 검토를 기록한다. 검토 범위가 다르므로 수치를 합산하지 않는다. 이관 당시 현지화 보고서를 이후 육해공 공통 비율·bootstrap 조건 문구까지 포함한 최종 소스 확인으로 재사용하지 않는다.

## 최초 네이티브 실패와 소스 교정

최초 `low` 합성 실행에서 root와 런타임 담당은 다음 두 오류군을 확인했다. 원래 실행의 로그·저장·소스 관측은 `TASK/runtime/runs/low/` 아래에 보존한다. 이 실패를 조용한 후속 실행이나 소스 교정 사실로 덮어 통과로 바꾸지 않는다.

| 최초 실패 | 관측·원인 범위 | 교정과 남은 확인 |
|---|---|---|
| 독립 donor의 overlord scope | 독립국에는 유효한 overlord가 없는데 중첩 부정 안에서 해당 scope를 평가하여 오류가 반복됨 | `is_subject = yes`인 경우에만 `overlord`를 평가하는 trigger `if`로 분리. 문서 `triggers_documentation.md:5166`의 같은 문맥 근거를 적용. 교정 소스의 실행 확인은 후속 사례와 구분 |
| 생성국 event target의 외부 참조 | `create_dynamic_country` 자식에서 일반 `save_event_target_as`로 잡은 생성국이 바깥 효과에서 `Undefined event target`으로 참조되지 않음 | 생성국은 `save_global_event_target_as`로 잡고 helper 끝에서 명시적으로 삭제. 바닐라의 비슷한 일반 target 예제가 이 호출 경로의 전달까지 보장하지 않았음을 기록 |

최초 실행 종료·원복 뒤 `low-r2`·`high-r2`·`protection-r2`를 별도 실행했다. r2에서 정부·평화·63주 핵심주 등 주요 관측이 통과했지만 함정 부수 이관 결함이 남아 있었으므로 최종 통과로 합치지 않는다. 그 뒤 `size = 0`을 추가한 r3 검증을 시작했으며, 아래는 r2 이력과 교정 후 검증 대기를 분리한 기록이다.

## r2 관측과 추가 교정 — 최종 소스 증거와 구분

`low-r2`·`high-r2`는 독립국 overlord guard와 생성국 global target 교정 뒤의 소스로 실행했다. 생성국의 정부·한국 피감독국 지위·평화·63주 핵심주 등 native 판정은 통과했지만, **함정을 이관하지 않아야 한다는 조건은 실패**했다.

| r2 사례 | 실제 저장 관측 | 판정·한계 |
|---|---|---|
| `low-r2` | KCH 7주·육군 21개 사단·함정 3척 | 지지도별 분배의 이전 소스 관측. 함정 3척은 의도하지 않은 부수 이관이므로 이 실행을 최종 전력 보존 통과로 사용하지 않음 |
| `high-r2` | KCH 42주·육군 170개 사단·함정 3척 | 낮은 지지도 사례와 별도 실행. 함정 부수 이관 실패를 유지하며 최종 소스의 분배 수치로 재사용하지 않음 |
| `protection-r2` | 한국 소유·한국 통제, 일본 통제, 만주국 소유, CHI 소유로 바꾼 만주 지리, 일본 종속 HBC의 보호·제외 관측 통과 | 보호 조건의 r2 소스 관측. 아래 전쟁명분 기대 불일치 1건과 분리 |

함정 이관 효과에는 이미 `navy_ratio = 0`이 있었으나 생성국에 예상 밖의 3척이 있었다. 당시에는 기본 `size` 생략과 0 비율 조합의 엔진 처리 관련 가능성을 확인하기 위해 root가 `size = 0`을 명시했다. **이것은 r2 당시의 교정 가설이며, 아래 low-r3 재현으로 단독 설명이 반증됐다.** 명시한 육군·비축 비율은 그대로 유지했다. r2의 주·사단·함정 값은 r3나 그 뒤 통제 결과에 섞지 않는다.

`protection-r2`의 `NO_JAPANESE_WARGOAL`은 **1 FAIL**로 보존한다. 기존 정식 16태그 전쟁명분 loop에서 일본 종속국을 목표로 지정한 명분이 엔진에서 종주국 JAP 대상에 반영되는 관측과, 「일본 대상 명분이 없어야 함」이라는 진단 기대가 일치하지 않았다. 새 자동 선전포고·공동 참전 효과를 넣은 것이 아니며, production의 기존 명분 loop는 유지한다. 다음 probe에서는 이 값을 정보 관측으로 분리할 예정이며 원래 FAIL을 삭제하거나 소급 통과로 바꾸지 않는다. 정확한 실행별 수치·관측 필드는 root의 runtime JSON 대조로 후속 보완한다.

r2에는 시장 `HasCachedTradeInfluence` assertion과 OneDrive 경로의 저장 이름 변경 오류도 있었다. 강제 시작·합성 세계 준비라는 진단 조건과 함께 기록하며, 현재 원인은 미확정이다. 이를 산둥 production 코드의 확정 원인이나 무관한 원본 결함으로 단정하지 않는다. 완전한 `_temp.hoi4` 사본 판독과 정상 UI 저장·최종 이름 확정·재로드는 다른 검증 층이다.

첫 finisher는 collect 뒤 stdout의 cp949 인코딩 오류로 stop 전에 중단됐다. 이후 실제 소유 PID를 확인하여 해당 게임을 종료하고 profile을 원복했으며, helper 출력은 UTF-8로 교정했다. 오류 시 collect까지 수행된 결과와 그 뒤 수동 종료·복원을 구분한다. 이 도구 제어 오류를 게임 기능 실패나 최종 전체 원복 완료로 대신 표시하지 않는다.

이 r2 절은 이전 소스의 이력이다. 아래 low-r3의 함정 재현과 후속 독립 통제, 단일 주 donor 소멸 시 전력 비율, 당시 해공 보존 목표, 실제 UI·35일 정상 중점 진행·저장 재로드와 최종 프로세스/설정/이어하기/기존 저장 보존 결과를 이 절의 통과로 대신하지 않는다.

## r3의 함정 재현과 독립 통제 준비

`size = 0`을 명시한 `low-r3`에서도 KCH에 **함정 3척**이 있는 결과가 다시 관측됐다. 따라서 「기본 size 생략 때문에 해군 0 비율에 기본값이 적용됐다」는 단독 설명은 **반증**됐다. 크기 기본값을 명시한 소스라는 사실만으로 해군 보존을 통과 처리하지 않는다. 당시 production은 해군·공군 0을 의도했지만 함정의 기대 부재는 검증되지 않았다. 이 문장은 이전 설계에 대한 판정이며 아래 최신 육해공 공통 비율 소스의 계약과 구분한다.

동시에 항공 집계는 런타임 담당의 비교에서 **CHI 132·GDC 131·JAP 831·KOR 150, 생성 KCH 0**으로 유지됐다. 이 관측은 함정의 예상 밖 존재와 구분하며, 모든 환경의 항공 이관 의미를 확정한 결과로 확대하지 않는다.

당시에는 정적 OOB의 CHI 9척과 저장에서 본 6척의 시간 기준이 달랐을 가능성을 고려해 실제 직전 수량을 측정하는 통제를 추가했다. 아래 서비스 20%/70% 통제에서는 실제 `num_ships` 직전 9척을 기록했으므로, 그 통제의 9→5·9→3 감소는 정적 OOB 추정이 아닌 실행 변수 관측이다. 이를 직전 snapshot이 없던 이전 실행의 초기 수량 증거로 소급하지 않는다. 함정 비율의 정확한 엔진 내부 처리나 모든 경우의 반올림 규칙은 확정하지 않는다.

root와 런타임 담당은 첫 seed 소멸 사례 뒤 **기존 CHI → 기존 KOR**의 독립 이관 통제를 준비해 수행했다. 이 통제는 새 국가 생성이나 영토 이전 없이 실제 함정 수를 전후 기록하고, `size = 0`, `army_ratio = 0.2`, `stockpile_ratio = 0.2`, `navy_ratio = 0`, `air_ratio = 0`인 명령 자체를 분리한다. 새 국가 생성·원국 소멸 순서와 전력 이관 효과를 구분하려고 실제 전후 값을 기록했으며, 그 결과는 아래 0 비율 통제 이력에 분리한다.

이 r3 단계의 원인 가설·통제 준비는 위 시점의 이력으로 남긴다. 이후 독립 통제 결과와 사용자 선택은 아래 별도 절을 따른다. r2·r3의 원래 실패를 삭제하거나 최신 소스 성공으로 재분류하지 않는다.

## 0 비율 통제 이력과 최신 육해공 공통 귀순 결정

기존 CHI → 기존 KOR의 `navy-zero` 독립 통제에서도 해군 0 보존 기대가 실패했다. 이는 생성국이나 영토 이전 없이 명령 자체를 분리한 결과로 보존한다. `naval_ratio`라는 다른 이름을 쓰는 대안은 **unexpected token**으로 반증됐으므로 production 구문으로 채택하지 않았다.

변수에 0을 넣어 전달하는 `navy-varzero` 시도에서 한 번 PASS가 관측됐지만, 같은 형태의 fresh 반복에서는 FAIL이 재현됐다. 앞선 잘못된 별칭 진단의 잔여 영향만으로 차이를 설명하려는 가설도 이 반복으로 지지되지 않았다. 일회 PASS를 안정적인 0 비율 우회법이나 엔진 원인 확정으로 일반화하지 않는다. 초기 low/r2/r3·별칭 오류·변수 0의 상반된 결과는 각각의 실행 소스와 로그·저장으로 보존한다.

이 불확실성을 숨기는 함정 회수·해군 전부 이전 후 임의 복원 등의 우회는 추가하지 않았다. 이후 사용자가 미정이었던 귀순 병종 범위를 **「육해공군을 같은 비율로 귀순」**으로 명시했다. 따라서 최종 설계는 기술적으로 0 보존 문제가 해결됐다는 주장이 아니라, 사용자 결정에 따라 육해공·비축을 공통 p로 이관하는 별도 단계다. 앞선 해군·공군 보존 문구와 실패 기준은 그 이전 설계의 이력으로만 남긴다.

같은 전력 입력의 20%·70% 서비스 독립 통제와 기지 보정 전 출범·보호·차단 사례를 실행했으며, 실제 값과 남은 공군 문제는 아래 절에 분리한다. 최종 동결 runtime 범위는 기존 중점·재건 결정·기존 현지화 두 파일의 4개 변경과 새 효과·상태 트리거·고유 현지화 두 파일의 4개 추가를 합한 **8파일**이다. 해당 소스의 새 관측·체크섬·원복 결과는 root가 후속 기록하며, 이전 소스 결과를 최종 통과로 재사용하지 않는다.

## 공통 비율 소스의 부분 통제·재건 관측 — 공군 미해결

런타임 담당과 대조한 아래 두 사례의 출범 효과 소스 SHA-256은 `782d261593b13f4e36f34a92a5cf7add9aec4d3a65a5abb9c09e4acd205d2522`다. 각 사례의 실제 네이티브 판정과 저장 판독만 기록하며, 공군 수정 이후의 소스나 실제 UI·저장 재로드 결과로 재사용하지 않는다. 판정 횟수는 반복 실행한 native 관측 수이며 고유 기능 수가 아니다.

| 사례·증거 | 확인된 결과 | 제한·남은 항목 |
|---|---|---|
| `partial-control-final`, `capture-20261119T043929995167Z` | **15 PASS / 0 FAIL**. 실제 production predicate와 보상을 사용해 한국의 province 1084·일본의 province 1001 통제 및 주 1038·598의 기존 소유가 유지됨을 확인. KCH 출범 영토는 597·743만 확보 | 이 합성 부분 통제 조건의 보호 결과. 모든 지도·외교 조합의 검증이나 정상 중점 진행이 아님 |
| `recognition-final`, `capture-20261119T044141513718Z` | **682 PASS / 4 FAIL**. 비맹주 한국의 연합국 소속, 인정 조건·CHI 합병·`KCH_china` 외형·63주 핵심주·자동 전쟁 부재의 지정 native 관측은 통과 | 다른 네 군벌 생존에 대한 무조건 기대 4 FAIL을 아래에 보존. 전체 실행을 0 FAIL로 보고하지 않음 |

인정 사례에서는 등록된 비축 장비 **type 0**을 1,000,000으로 준비하고 실행 직전 변수로 확인했다. 저장의 CHI 비축은 **1,000,000 → 300,000.6**, 생성국 D04의 해당 장비는 **700,330**으로 기록돼 실제 감소·증가를 확인했다. 이는 `runtime/recognition-final-metrics.json`·`recognition-final-context.json`의 지정 장비 관측이다. 이전 `high-final`의 비축 준비·수혜 기대 FAIL을 이 결과로 소급 삭제하거나 모든 장비 종류의 분배 보장으로 확대하지 않는다.

`RECOGNITION_OTHER_PRC_SURVIVES`·`OTHER_SHX_SURVIVES`·`OTHER_NXM_SURVIVES`·`OTHER_HBC_SURVIVES`의 **4 FAIL**은 「최초에 있던 군벌은 인정 뒤에도 모두 존재해야 함」이라는 무조건 기대에서 발생했다. 같은 실행의 **인정 직전 존재·주 수를 측정하지 않았으므로**, 인정 결정이 이들을 합병했다는 원인 판정도 성립하지 않는다. 유사 조건의 이전 `high-r3` 출범 전용 결과에서도 해당 네 나라의 소유 주가 이미 빈 목록이어서 정부 형성 단계의 소멸 가능성이 강하게 지지되지만, 이는 동일 실행의 전단계 직접 증거가 아니다. `recognition-final-r2`에는 결정 실행 직전의 존재·주 수 snapshot을 넣어 비교하도록 준비했다. 원래 4 FAIL은 유지한다.

기지 보정 전 `low-final` 저장에서 항공은 CHI **132**, GDC **131**, 생성 KCH **0**으로 남았다. 이후 기존 KOR 수혜와 신규 KCH의 no-airbase/with-airbase·동맹 기지 통제로 조건을 분리한 결과와 교정은 아래 절을 따른다. **기지 보정 소스는 아래 low/high-air-final에서 공군 26기/185기 귀순을 확인했고, 다른 최종 사례는 진행 중**이다. 부분 통제 15/0이나 재건의 지정 관측 통과로 이 미해결을 덮지 않는다.

## 공통 비율 독립 통제와 기지 보정 전 출범 수치

기존 CHI → 기존 KOR로 같은 p를 입력한 서비스 통제의 실제 `hok_sdg_*_before/after/delta` 변수를 읽었다. 이는 새 KCH 출범 helper 자체가 아니라 이관 명령을 분리한 통제다. `service20`의 source effect 해시는 `1d6cf50aeb2444a8e70504e90efc86ae4e59db94e5ae038d5a731c19a3caa9d7`, `service70`은 `782d261593b13f4e36f34a92a5cf7add9aec4d3a65a5abb9c09e4acd205d2522`로 다르며, 각 probe의 공통 비율 명령과 저장 증거를 각각 보존한다.

| 통제 입력 | CHI → KOR 육군 | CHI → KOR 함정 | CHI → KOR 배치 항공기 | 연료 실제 이동 |
|---|---|---|---|---|
| `service20`, p = 0.20 | CHI 85→68, KOR 22→39: 17개 사단 이동 | CHI 9→5, KOR 21→25: 4척 이동 | CHI 132→106, KOR 150→176: 26기 이동 | CHI −3.67487k, KOR +3.67486k |
| `service70`, p = 0.70 | CHI 85→26, KOR 22→81: 59개 사단 이동 | CHI 9→3, KOR 21→27: 6척 이동 | CHI 132→40, KOR 150→242: 92기 이동 | CHI −12.86287k, KOR +12.86286k |

명령에 같은 p를 입력해도 함정 9척에서 4척/6척이 이동했으므로, 모든 병종의 결과 개수가 정확히 p와 일치한다고 단정하지 않는다. 기존 장착 장비도 CHI −2,784/KOR +2,784 및 CHI −9,616/KOR +9,616으로 각각 관측됐다. 이 두 서비스 통제에서 준비하려던 비축 장비는 실행 직전 0이어서 비축 증여 기대가 각각 **4 PASS/1 FAIL**로 남았다. 그 FAIL은 등록된 type 0을 1,000,000으로 준비한 아래 재건 사례의 별도 성공 관측과 구분한다.

기지 보정 전 공통 p 출범 사례는 `runtime/low-final-metrics.json`과 같은 저장 원문을 읽은 `runtime/engine-high-final-metrics.json`에서 다음과 같았다. 이 사례 이름의 `final`은 당시 실행 label이며 아래 기지 보정 소스의 최종 완료를 뜻하지 않는다.

| 출범 사례 | KCH 소유 주 | KCH 육군 | KCH 함정 | KCH 배치 항공기 | 원래 native 판정 |
|---|---:|---:|---:|---:|---|
| `low-final`, p = 0.20 | 7 | 21개 사단 | 4척 | 0기 | 606 PASS/2 FAIL; 비축 준비·수혜 기대 두 항목 실패 |
| `high-final`, p = 0.70 | 42 | 170개 사단 | 6척 | 0기 | 602 PASS/2 FAIL; 비축 준비·수혜 기대 두 항목 실패 |

두 사례에서 CHI 항공은 132→132, GDC 항공은 131→131이었다. 이 결과가 기존 KOR 수혜 통제의 공군 이동과 다르므로 새 국가의 착륙 기지 등 조건을 분리했다. 위 네이티브 판정 목록에 공군 미수혜를 실패로 검사하지 않았더라도 실제 0기 관측을 숨기거나 기능 전체 통과로 보고하지 않는다.

## 신규국 공군 조건 분리와 비행장 확보 순서 교정

초기 `airbase-control`은 직접 조건 검사 두 곳이 유효하지 않아 그 로그의 해당 단정을 검증 근거로 쓰지 않는다. 실제 getter 변수와 저장은 CHI **132→132→106**, KCH **0→0→26**을 기록했다. 잘못된 진단 조건을 교정한 **`airbase-control-r3`**에서도 같은 실제 수치가 재현됐고 기지 0/양수의 유효 조건 검사를 확인했다. 단계는 새 KCH의 597만 보유·비행장 0 → 공통 p = 0.20 이관 → 외부 probe가 같은 소유 주에 비행장 1을 합성 추가 → 동일 명령 재실행이다. 반복 이관과 probe의 합성 건물은 원인 분리용이며 production을 두 번 이관하는 설계가 아니다.

기술·변형 종류의 고정 문제라면 같은 생성국에 비행장만 추가한 뒤의 공군 수혜를 설명하기 어렵다. 이 통제 조건에서는 공군 이관 시 수혜국이 가진 비행장 여부가 중요한 조건임이 강하게 지지된다. 모든 엔진 내부 조건이나 다른 버전의 동작까지 일반화하지 않는다.

`allied-airbase`는 자체 비행장이 없는 KCH 597에 먼저 한국 피감독국·같은 세력 지위를 설정하고 공통 p = 0.20을 한 번 적용했다. 실제 CHI **132→132**, KCH **0→0**이어서 한국의 기지 접근만으로 충분하다는 가설은 반증됐다. 이 사례의 다른 전력은 이동했지만 공군은 받지 못했으며, 외교 지정 순서만 바꿔 해결했다고 설명하지 않는다.

이후 출범 효과를 SHA-256 **`82c6dfa60cb75f8a9b2e4574dc3b10b8303b4f37543a82a1bac2fef7fcba18b5`**로 교정했다. 공군이 배치된 양수 p 참여국이 있을 때, 이미 선택한 영토 중 기존 비행장 주를 **원소유국을 소멸시키지 않는 bootstrap 조건**으로 먼저 이전한다. KCH에 비행장이 생기면 추가 선이전은 하지 않는다. 그래도 KCH 소유 비행장이 없으면, 이미 안전하게 확보한 **KCH 수도 주에 비행장 1단계만 즉시 건설**한 뒤 donor마다 공통 비율 이관을 한 번 실행한다.

이 조건부 비행장 1단계는 **영구 건물 자산이 늘어나는 의도적인 계속개발 효과**다. 공군 귀순을 성립시키는 최소 지원으로 기록하며 무해한 호환성 수정으로 숨기지 않는다. 기존 선택 비행장을 확보할 수 있거나 양수 p의 배치 공군이 없으면 새 기지를 주지 않는다. 한국·일본·만주 보호와 기존 선택 영토·예산을 우회하지 않고, map/history의 시작 건물이나 다른 나라의 비행장을 변경하지 않는다.

state scope의 즉시 비행장 건설 구문은 설치본 `events/NSB_Soviet.txt` 5380–5387행, 국가에서 수도 state로 전환하는 구문은 `common/scripted_effects/ITA_scripted_effects.txt` 2895행의 같은 문맥 사례를 근거로 삼았다. 교정 뒤 저지지도 출범·공군과 나머지 최종 사례는 아래 새 실행에서 확인했고, 실제 UI 관측과 저장 후속 확인은 각각 별도 절에 기록한다. 위 서비스 통제나 기지 보정 전 수치를 새 소스 통과로 재사용하지 않는다.

## 비행장 보정 소스의 최종 6사례 — UI·저장 후속 확인

출범 효과 **`82c6dfa60cb75f8a9b2e4574dc3b10b8303b4f37543a82a1bac2fef7fcba18b5`**와 공항 안내를 포함한 현재 runtime 소스를 사용한 아래 사례를 이전 `*-final` label의 기지 보정 전 실행과 구분한다. 기록된 실행 시작·종료 SHA는 해당 `source-stability.json`에서 동일하다. 이 manifest는 `.txt/.yml/.lua/.mod/.gfx`의 텍스트/runtime 코드 **348파일** 범위이며 바이너리를 포함한 전체 runtime 자산 해시라는 뜻이 아니다. native FAIL 0은 전체 error.log 무오류·실제 UI·정상 진행·저장 재로드 통과라는 뜻이 아니다.

| 사례·증거 | 실제 관측·필수 조건 | 상태·제한 |
|---|---|---|
| `low-air-final`, `capture-20261119T050007122368Z` | **native FAIL 0**. KCH 7주·육군 21개 사단·함정 4척·배치 항공기 26기. CHI 항공 132→106. 선택한 기존 743 비행장을 전력 이관 전에 확보했고 597의 신규 비행장 0 조건을 확인 | 현재 기지 순서 보정 소스의 저지지도 합성 사례 확인. 보호·차단·DLC 조합·UI·재로드는 각각 별도 확인 |
| `high-air-final`, `capture-20261119T050210857854Z` | **native FAIL 0**, 시작·종료 runtime SHA 동일. KCH 42주·육군 170개 사단·함정 6척·배치 항공기 185기. CHI 항공 132→39, GDC 131→39, KCH 185로 합계 263기 보존. 기존 743 비행장 사용·597 신규 공항 0 확인 | 같은 고정 초기 자산의 고지지도 출범 사례. 후속 인정·공항 fallback·단일 주·p=0 등과 구분 |
| `airport-fallback-final`, `capture-20261119T050342842141Z` | **native FAIL 0**, 시작·종료 runtime SHA 동일. 한국이 743을 보유하고 CHI가 597·1038 두 주를 가진 p = 70% 조건에서 KCH는 597만 확보하고 수도 비행장 1단계 지급. 한국 743·CHI 1038 보존. CHI 공군 132→40, KCH 92기 | 기존 비행장 주를 가져올 수 없는 조건부 건설 경로의 실제 관측. 함정 9척 이동은 아래 한계로 분리 |
| `airport-single-last-final`, `capture-20261119T050511941286Z` | **native FAIL 0**, 시작·종료 runtime SHA 동일. CHI가 743 한 주와 배치 항공기 132기를 가진 조건에서 743 선이전을 막고 SND의 597을 bootstrap으로 사용. 597 비행장 1단계 지원 뒤 KCH에 공군 92기를 이관한 다음 743을 이전·CHI 소멸. KCH 2주·64개 사단·6척·92기, SND의 1038 보존·8→3개 사단 확인 | 마지막 주 donor를 전력 이관 전에 소멸시키지 않는 분기의 실제 확인. 소멸국의 미귀순 잔여 자산 총량 보존은 검증 주장에서 제외 |
| `no-ncns-air-final`, `capture-20261119T050652167983Z` | **native FAIL 0**, 시작·종료 runtime SHA 동일. 실제 NCNS 비활성·p = 0·무세력 한국에서 KCH가 한국 피감독국으로 두 기본 거점만 확보하고 양국 무세력을 유지. KCH 육군·함정·배치 항공기·소총 비축 모두 0, 597 신규 공항 0. CHI 57개 사단·9척·132기·부대 소총 23,920 전후 동일 | NCNS 비활성·지지도 0·무세력의 합성 조합. MtG 비활성이나 모든 DLC 조합의 증거로 사용하지 않음 |
| `recognition-air-final`, `capture-20261119T050824205536Z` | **682 native PASS occurrences / 0 FAIL**, 시작·종료 runtime SHA 동일. 비맹주·연합국 한국에서 CHI가 한국 종속국이 되기 전 차단→종속 후 가용→CHI만 흡수·KCH 외형 변경·63주 핵심주·보상 직후 평화 확인. 인정 직전 현존한 검사 대상 10국의 존재·주 수 유지 | PRC·SHX·NXM·HBC는 인정 직전부터 부재였음을 같은 실행의 snapshot으로 확인. 실제 UI 결정 클릭·기존 저장 재로드와 구분 |

같은 사례의 등록된 type 0 소총 비축은 **CHI 1,000,000→800,000**, **KCH 200,000**이었다. 모든 donor와 KCH의 비축 및 부대 장착 소총을 합친 값은 실행 전후 **1,030,949로 정확히 동일**해 이 지정 자산의 보존을 확인했다. 같은 low 사례의 전체 donor+KCH 육군 237개 사단·함정 9척·배치 항공기 263기도 전후 정확히 동일했다. 다른 장비·모든 시점·장기 생산을 포함한 전역 자산 보존으로 확대하지 않는다. 근거는 `runtime/low-air-final-metrics.json`과 해당 capture의 실제 저장 사본·실행별 source 안정성 기록이다.

고지지도 사례의 CHI type 0 소총 비축은 **1,000,000→300,000.6**, 생성국은 **700,330**이었다. 생성국 값에는 여러 donor의 수혜가 합쳐져 있으므로 이 두 숫자만으로 stock-only 총량 보존을 주장하지 않는다. 근거는 `runtime/high-air-final-metrics.json`이다.

같은 고정 초기 자산에서 p = 20%→70%로 올렸을 때 KCH 결과는 **7→42주, 21→170개 사단, 4→6척, 26→185기**였다. 서로 다른 fresh 합성 실행의 지정 결과이며 동일 난수 seed나 모든 주·병종의 정확한 비율을 보장하지 않는다.

공항 fallback 사례에서는 CHI가 첫 597 이전으로 모든 항구를 잃는 합성 조건도 포함됐다. 실제 함정은 **CHI 9→0, KCH 9**였다. 공통 입력 p = 70%와 최종 함정 수가 정확히 70%라는 주장은 다르며, 이 사례를 정확한 함정 개수 비율의 통과로 사용하지 않는다. 영토 이전·항구 상실·네이티브 조건과의 인과는 아직 확정하지 않았고, 함정을 회수하거나 다른 비율로 강제로 맞추는 우회는 추가하지 않았다.

단일 주 CHI 사례에서는 743에 기존 비행장이 있어도 원국의 마지막 주이므로 전력 이전 전에 가져오지 않았다. SND의 안전한 597에서 필요한 비행장을 마련하여 귀순을 먼저 끝낸 뒤 마지막 주를 옮긴 결과다. 그 뒤 원국이 소멸하며 남는 비귀순 전력·비축의 엔진 처리는 전체 자산 보존 주장에 포함하지 않는다.

최종 `recognition-air-final`은 인정 직전 snapshot을 실제로 측정했다. PRC·SHX·NXM·HBC가 그 시점에 이미 부재였고, 당시 존재한 검사 대상 10국의 존재·주 수가 인정 뒤 유지되어 기존 무조건 생존 기대의 문제를 새 사례에서 분리했다. 원래 `recognition-final`의 4 FAIL을 소급 삭제하지 않으며, 서로 다른 실행의 전단계 증거를 혼용하지 않는다.

비행장 보정 소스의 **최종 6사례는 각각 native FAIL 0**이고, 실행별 runtime source bytes·시작/종료 SHA 안정성은 `runtime/final-native-index.json`에서 확인한다. 반복 cleanup·핵심주 확인 때문에 native occurrence 수는 고유 기능 수가 아니며 서로 합산하지 않는다. 실제 UI에서 직접 시작·일반 시간 진행·완료 팝업·새 정부를 확인한 범위는 아래에 별도로 기록한다. 명목 35일의 정확한 달력 경과·새 저장의 실제 UI Load·root의 최종 원복을 이 네이티브 결과로 대신하지 않는다.

## 실제 UI의 직접 시작·시간 진행과 첫 로컬 저장

root는 `-ai_testing` 없이 표시된 게임에서 `KOR_support_for_democracy_in_china` 등 선행 준비만 합성 완료하고, 축출 중점은 미완료로 둔 상태에서 UI를 조작했다. `1936.1.1.12`의 상세창은 명목 **35일**, 가용 조건의 초록 표시, 한국어로 해석된 피감독국·90% 상한·육해공/비축/연료·영토 보호·비행장 지원·기존 전쟁명분·개별 결정 해금 안내를 보여줬다. `-debug`에 따른 엔진 중점 ID 표시는 따로 구분한다. 증거는 `ui/01-focus-conditions-effects.png`와 `ui/observations.json`이다.

root는 실제 **Start**를 직접 클릭하여 활성 진행 막대를 확인하고, 속도를 올려 일시정지를 해제했다. 이후 일반 게임 시간 진행에서 막대가 증가했고 완료 팝업이 나타났다. 이 축출 중점의 강제 완료·console 효과·직접 출범 명령은 사용하지 않았다. 증거는 `ui/02-focus-progress.png`·`ui/03-natural-focus-completed.png`다. 선행 준비를 합성했으므로 전체 민주인사 지원 경로와 자연 지지도 축적을 새 게임부터 검증했다는 뜻은 아니다.

**정확히 35일이 달력상 경과했다고 판정하지 않는다.** Start 관측은 `1936.1.1.12`이며, 첫 UI 저장의 KOR→D04 피감독국 시작과 D04 세력 가입 필드는 `1936.2.4.1`을 기록한다. 저장은 축출 완료를 직렬화했지만 정확한 중점 완료일 필드나 완료일 로그를 제공하지 않는다. 팝업은 2월 5일 이후 화면에서 관측했다. 명목 기간과 초기 누적 진행도의 관계·원인은 아직 확정하지 않았다. 근거는 `runtime/ui-saves/first-ui-save/focus-and-government-time.json`이다.

완료 팝업이 열린 동안 Space가 게임을 멈추지 않아 시간이 더 진행됐다. root는 팝업을 닫고 실제 일시정지 버튼을 클릭하여 **1936.2.16.23**의 정지를 확인했다. 같은 화면에서 산둥 자유 공화국 이름·민주정부·같은 세력·한국 종주국 깃발을 확인했고, **피감독국 툴팁에 선전포고 불가**가 한국어로 표시됐다. `ui/04-supervised-state.png`는 이 관측의 증거이며 주별 핵심주·모든 외교 행동의 UI 검증을 대신하지 않는다.

실제 로컬 Save는 고유 기본 이름 `KOR_1936_02_16_23`의 기존 파일 부재를 두 번 확인한 뒤 클릭했다. 생성된 게임 원본은 `KOR_1936_02_16_23_temp.hoi4` **72,719,521바이트**, SHA-256 `20bca7bd267bbc9671caa3b4cfc50a988f7eda97e3693a56294ae160f6994b82`이며 완전한 `HOI4txt` header와 text tail을 확인했다. 정식 파일명으로의 rename은 `errno 2`로 계속 실패해 정식 파일은 없었다. 원본은 덮어쓰지 않고 `runtime/ui-saves/first-ui-save/`에 사본·manifest를 보존했다. 완전한 임시 파일과 완료 중점 직렬화는 실제 UI Load 성공의 증거가 아니다.

root는 게임의 **Quit→OK**를 직접 선택했고 Sky에서 게임 surface 부재를 관측했다. 첫 UI 프로세스의 종료·설정 복원은 런타임 담당이 별도로 수행한 뒤 아래의 원래 두 모드 playset·no-probe 새 프로세스에서 실제 UI Load를 진행했다. 첫 Quit 관측만으로 기존 저장 124개 해시·이어하기 인덱스·Steam 상태의 최종 보존을 완료 처리하지 않는다.

## 원래 playset의 새 프로세스 UI Load·진행·재저장

첫 UI 실행을 종료하고 원래 **HOK+외부 English Translation 두 모드**, **no-probe·no-ai_testing** 구성으로 프로세스를 완전히 재시작했다. root는 PID **10004**의 Local Load 목록에서 실제 `KOR_1936_02_16_23_temp.hoi4`를 선택하고 **Load**를 클릭했다. **1936.2.16.23**의 세계가 실제 복원됐으며, 산둥 자유 공화국의 민주정부·한국 종주국·피감독국 툴팁과 선전포고 불가 안내가 유지됐다. 증거는 `ui/05-load-selected.png`·`ui/06-reloaded-supervised-state.png`와 `ui/observations.json`이다. 이 첫 새 저장의 실제 UI Load 성공을 기록하며, 정식 파일명 rename 성공으로 바꾸어 기록하지 않는다.

불러온 세계를 일반 시간 조작으로 며칠 더 진행한 뒤 실제 pause를 확인한 날짜는 **1936.2.21.3**이다. 출범 helper나 강제 중점 완료를 실행하지 않았다. 축출 중점의 완료 표시와 고유 효과 안내·조건부 비행장·영토 보호·개별 인정 결정 해금이 한국어로 표시됐고, **새 한국어 설명도 실제로 보였다**. 외부 영어 채널의 오래된 설명은 source상 영어 locale 제한이며 이 한국어 UI 관측의 오류가 아니다. 증거는 `ui/07-reload-advanced.png`·`ui/08-original-playset-completed-effects.png`·`ui/09-original-playset-focus-panel.png`다.

읽기 전용 첫 저장 판독 `runtime/ui-first-save-contract.json`은 D04의 `original_tag = KCH`·민주주의·`autonomy_supervised_state`·KOR 축출 완료·실제 42주 소유·소스와 일치하는 63주 핵심주·임시 선택/예산/target 이름 부재를 기록한다. 첫 저장의 163개 사단·6척·184기 같은 군사 수치는 게임 시간이 흐른 이 저장 시점의 관측이다. 즉시 보상 native 수치와 다른 날짜를 비교해 모든 자산이 불변이라고 주장하지 않는다.

root는 고유 기본 이름 **`KOR_1936_02_21_03`**으로 Local Save를 클릭하여 dialog가 닫힌 것을 관측하고 **Quit→OK**로 정상 종료했으며 Sky의 게임 목록이 비었다. 수집된 두 번째 원본은 `KOR_1936_02_21_03_temp.hoi4` **46,890,774바이트**, SHA-256 `2f06c1c9091d72cb8b976e0a9126e805a764f249674f89793d950031a343baa7`이다. 첫 text 저장과 달리 **`HOI4bin5` binary 형식**이며, 사본과 manifest는 `runtime/ui-saves/after-reload-ui-save/`에 보존했다. `ui/10-resaved-after-reload.png`와 observations가 실제 클릭·종료의 근거다. 이 재저장을 또 다른 새 프로세스에서 불러온 것은 아니므로 두 번째 파일의 추가 재로드 성공·binary 내용 완전 판독을 주장하지 않는다.

## 검증 범위와 남은 항목

최초 low·r2·low-r3·0 비율 통제·원국/수혜국 소멸의 실패 이력과 공통 비율 소스의 부분 통제·재건 관측을 위에 기록했다. **비행장 확보 순서를 보정한 최종 6사례, 실제 UI의 직접 시작·시간 진행·완료·정부 표시, 원래 playset 새 프로세스에서 첫 새 저장의 실제 UI Load·며칠 진행·재저장을 구분해 확인했다. 명목 35일의 정확한 경과·두 번째 저장의 재로드·변경 전 저장과 장기 조합 검증은 미완료**다. 준비된 helper·지정 관측의 PASS만으로 전체 기능 통과를 선언하지 않는다. 실제 실행 소스 해시·체크섬·구성·관측값과 소유 프로세스 종료·설정/기존 저장 보존 결과는 각각의 외부 증거로 구분한다. Steam의 정상 종료·재시작 뒤 초록 Play 복귀도 root가 실제 UI로 확인했다.

| 검증 층 | 현재 상태·남은 항목 |
|---|---|
| 소스 | 위 scope·원문 보존·현지화·지리 대조를 수행. 실제 변경 8파일은 독립 freeze05·최종 6 native/두 UI 세션의 18 launch/capture·최종 원문 SHA가 모두 동일. 요약 inventory의 최초 수동 선택 오류와 교정을 아래에 구분 |
| 합성 네이티브 효과 | 기지 보정 후 최종 6사례가 각각 native FAIL 0. 저/고지지도·기존기지/조건부 건설·단일 주·p=0/NCNS 비활성/무세력·인정 snapshot을 위에 사례별 기록. 이전 소스 실패·반복 판정 수와 합산하지 않음 |
| 실제 UI | 가용 조건의 초록 표시·한국어 효과 안내·명목 35일·직접 Start·진행 막대·완료 팝업·KCH 민주정부/한국 피감독국/선전포고 불가 툴팁 확인. 원래 playset/no-probe 재로드 뒤 새 한국어 설명·완료 표시·고유 효과 안내 확인. 차단 상태 UI·주별 핵심주 UI·영어 및 모든 툴팁 배치는 미확인 |
| 정상 진행 | 선행 지원만 합성 준비한 뒤 해당 중점을 직접 시작하고 일반 시간 진행으로 완료되는 흐름 확인. 초기 누적 진행도 원인과 정확한 35일 달력 경과는 미확정. 자연 지지도 축적·전체 선행 경로·취소·AI 선택은 미확인 |
| 저장 | 첫 72,719,521바이트 HOI4txt 임시 원본을 원래 playset/no-probe fresh process의 Local Load로 실제 복원. 정부·종주/피감독 관계·완료 중점 유지, 며칠 진행과 두 번째 고유 UI Save·Quit 확인. 46,890,774바이트 HOI4bin5 임시 재저장 수집. 정식 이름 rename 실패·두 번째 저장 재로드·변경 전 캠페인·장기 진행은 미해결/미검증 |
| DLC·외교 조합 | 재건 사례의 비맹주·연합국 조건과 최종 no-NCNS/p=0/무세력 조합을 각각 확인. 원래 playset 한국어 UI·재로드 확인은 모든 기존 KCH/DLC 차단 조합을 대신하지 않음. no-NCNS와 no-MtG를 혼동하지 않음 |
| 멀티플레이 | 별도 동기화·OOS 검증 미수행. 체크섬만으로 호환성 주장하지 않음 |

## 진단 이후 AI 선전포고의 관측 범위

root의 2026-11-19 14:00(Asia/Seoul) 로그 관측에서는 `low-air-final`의 보상 직후 초기 native 판정 뒤, 게임 날짜 **1936.1.2.2**에 KOR AI/HMI 선전포고와 **1936.1.3.3**에 KCH 선전포고가 이어졌다. 해당 실행은 `-ai_testing`으로 일반 AI를 진행시킨 합성 진단이다. 즉시 보상과 이후 일반 AI의 전쟁명분 사용·외교 행동을 서로 다른 시점으로 기록한다.

이 관측을 production에 `declare_war_on`·`add_to_war`가 추가됐다는 증거로 해석하지 않으며, 반대로 전체 실행이 계속 평화였다고 표시하지도 않는다. 보상 직후 평화 관측, 명시적 자동 전쟁 효과의 소스 부재, 실제 플레이어의 전쟁 선택은 각각 별도 확인이다. root의 후속 실제 UI 실행은 `-ai_testing` 없이 진행했고, 선행만 합성 준비한 뒤 플레이어의 Start와 보통 시간 진행으로 축출 중점 완료를 관측했다. 이 결과와 해당 합성 실행의 AI 후속 선전포고를 혼합하지 않으며, 플레이어의 모든 전쟁 선택 경로를 검증했다는 뜻으로 확대하지 않는다.

## 외부 증거와 최종 보존 기록

런타임 준비 담당은 실제 사용자 데이터의 작은 top-level 파일 **11개**를 `TASK/runtime/baseline/profile/`에 복사했다. `profile-manifest.json`에는 `settings.txt`·`dlc_load.json`·실제 `pdx_settings.txt`·게임플레이 설정과 **142바이트 `continue_game.temp` 원본**을 포함하고, 원래 없던 보조 파일도 구분한다. 이전 작업에서 이어하기 인덱스 원본을 보존하지 못했던 한계와 달리 이번에는 실행 전 정확한 사본이 있다.

기존 저장은 `TASK/runtime/baseline/save-inventory.json`에 **124개·9,103,511,323바이트**로 해시를 기록했으며 원본 저장을 복사하거나 덮어쓰지 않았다. 이 집합은 이전 사건의 109개 역사적 저장과 동일한 집계가 아니다. pre-launch 로그 사본은 `runtime/baseline/logs/`와 `log-manifest.json`, 프로세스 착수 관측은 `runtime/baseline/processes.json`에 있다. 준비 시 기존 HOI4 실행이 없었음을 기록했지만 실제 실행 직전 재확인은 별도다.

`TASK/runtime/DIAGNOSTIC_SCOPE.md`는 합성 준비·강제 효과 호출과 정상 진행을 구분한다. 새 probe·controller·검사 결과·로그/저장 증거 사본은 이 외부 경로 아래에 두고, 게임이 만든 원본은 실제 사용자 데이터에 둔다. 무단 게임·설정 조작이나 base-game·Workshop·외부 번역 편집을 정당화하는 문서가 아니다.

| TASK 상대 경로 | 원본·사본·이력 역할 |
|---|---|
| `source-baseline.json`·`baseline-source/` | 이번 구현 전 runtime 1,591개 해시와 7개 소스/문서 사본 |
| `geography/geography-inventory.json`·`geography/independent-source-review.json` | 지리·원본 구문·정적 범위·scope 검토 이력 |
| `localisation/first-write-error/` | 잘못된 최초 쓰기 사본. baseline 원본이나 최종 소스가 아님 |
| `localisation/before-dedicated/`·`localisation/source-checks-before-dedicated.json` | 고유 파일로 가용 안내를 옮기기 전 사본·소스 확인 |
| `localisation/source-checks.json` | 고유 파일 이관 당시 네 현지화 파일의 정적 확인. 이후 공통 귀순·bootstrap 문구의 최종 확인과 구분 |
| `runtime/baseline/profile/`·`runtime/baseline/profile-manifest.json`·`runtime/baseline/summary.json` | 실제 사용자 설정·이어하기 원본 사본과 준비 단계 기록 |
| `runtime/baseline/save-inventory.json` | 기존 저장 124개의 원본 위치·크기·해시 목록 |
| `runtime/baseline/logs/`·`runtime/baseline/log-manifest.json` | 실행 전 로그 증거 사본·출처. 새 소스 실행 결과가 아님 |
| `runtime/DIAGNOSTIC_SCOPE.md` | 준비 범위·예정 사례·실행/종료/복원 통제 |
| `runtime/native-summary.json` | 실행별 소스 해시·capture·native PASS/FAIL 원본 이력. 서로 다른 소스·반복 판정을 무분별하게 합산하지 않음 |
| `runtime/recognition-final-metrics.json`·`runtime/recognition-final-context.json` | 지정 저장의 장비·국가·소유 주·외교 상태 판독. 정상 저장 재로드나 인정 직전 snapshot 증거가 아님 |
| `runtime/service20-metrics.json`·`runtime/service70-metrics.json` | 기존 CHI→KOR 명령의 실제 전후 서비스·연료 getter 관측 |
| `runtime/low-final-metrics.json`·`runtime/engine-high-final-metrics.json` | 기지 보정 전 출범 저장의 실제 영토·전력 getter/소유 주 판독 |
| `runtime/airbase-control-metrics.json`·`runtime/airbase-control-r3-metrics.json`·`runtime/allied-airbase-metrics.json` | 최초 잘못된 조건·교정한 기지 조건·동맹 기지 가설을 각 실행의 실제 변수와 구분한 원인 분리 자료 |
| `runtime/low-air-final-metrics.json`·`runtime/runs/low-air-final/` | 기지 보정 후 저지지도 실제 저장·전후 자산·native 판정·source 안정성. 이전 low-final과 구분 |
| `runtime/high-air-final-metrics.json`·`runtime/runs/high-air-final/` | 기지 보정 후 고지지도 실제 저장·전후 자산·native 판정·source 안정성. 이전 high-final과 구분 |
| `runtime/airport-fallback-final-metrics.json`·`runtime/runs/airport-fallback-final/` | 한국 743 보호·597 비행장 1단계 지원과 실제 공군 귀순. 항구 전부 상실 시 함정 전체 이동 관측과 정확 비율 한계 포함 |
| `runtime/airport-single-last-final-metrics.json`·`runtime/runs/airport-single-last-final/` | 기존 비행장의 마지막 주 선이전 차단·전력 귀순 후 영토 이전/원국 소멸 순서의 실제 기록 |
| `runtime/no-ncns-air-final-metrics.json`·`runtime/runs/no-ncns-air-final/` | 실제 NCNS 비활성·p=0·한국/KCH 무세력 조합과 전력 미이관 관측 |
| `runtime/recognition-air-final-metrics.json`·`runtime/runs/recognition-air-final/` | 최종 출범·비맹주 인정 조건·인정 직전/직후 존재·주 수 snapshot·CHI만 합병의 실제 관측 |
| `runtime/final-native-index.json` | 최종 6사례별 실제 capture·source bytes·시작/종료 SHA 안정성·판정 색인. UI/재로드/전체 원복 완료를 대신하지 않음 |
| `ui/observations.json`·`ui/01-focus-conditions-effects.png`·`ui/02-focus-progress.png`·`ui/03-natural-focus-completed.png`·`ui/04-supervised-state.png` | root의 실제 가용/효과·Start·일반 시간 진행·완료 팝업·피감독국 UI·로컬 Save·Quit 관측. 정확한 35일 경과·재로드 완료를 뜻하지 않음 |
| `runtime/ui-saves/first-ui-save/save-manifest.json`·`runtime/ui-saves/first-ui-save/focus-and-government-time.json`·동일 폴더의 `KOR_1936_02_16_23_temp.hoi4` | UI 생성 임시 원본의 위치·크기·해시·text 완결성과 축출 완료/정부 관계 날짜의 판독 사본. 후속 실제 UI Load 성공은 아래 observations/PNG로 별도 증명 |
| `ui/05-load-selected.png`·`ui/06-reloaded-supervised-state.png`·`ui/07-reload-advanced.png`·`ui/08-original-playset-completed-effects.png`·`ui/09-original-playset-focus-panel.png`·`ui/10-resaved-after-reload.png` | 원래 두 모드/no-probe 새 프로세스의 실제 Local Load·정부/관계 유지·일반 진행·완료 중점/새 한국어 설명/고유 효과·재저장 관측 |
| `runtime/ui-first-save-contract.json` | 실제 첫 UI text 저장의 국가·완료 중점·42주 소유·63주 핵심주·임시 자료 부재의 읽기 판독. 날짜가 다른 native 즉시 자산과 불변을 주장하지 않음 |
| `runtime/ui-saves/after-reload-ui-save/save-manifest.json`·동일 폴더의 `KOR_1936_02_21_03_temp.hoi4` | 원래 playset에서 진행·재저장한 binary 임시 원본의 위치·크기·해시·형식 사본. 두 번째 파일 추가 재로드/완전 판독 증거는 아님 |
| `runtime/final-save-preservation.json`·`runtime/restoration-20261119T054056370212Z.json` | 기존 124개 원본 저장 해시 불변·신규 33개 분리·baseline 11파일 해시 일치·원래 없던 보조 파일 부재·probe pointer/게임 프로세스 부재의 최종 확인 |
| `runtime/final-source-preservation.json`·`runtime/final-task-source-copy/`·`runtime/final-source-preservation-scope-01-superseded.json` | 실제 delta 8파일의 freeze05/최종 6 native·두 UI 세션의 18 launch/capture/현재 SHA 일치와 최종 원문 사본. 최초 수동 inventory 8파일 선택 오류 보고서는 폐기하지 않고 superseded로 보존 |
| `documentation/final-source-and-records/native-manifest-scope-index.json` | 독립 QA가 최종 6런 각각의 348-file manifest에서 실제 delta 8파일 모두의 존재와 freeze05 해시 일치를 개별 대조. 48개 대조를 UI·바이너리 전체 검증으로 확대하지 않음 |
| `runtime/runs/ui-ready/process-exit.json`·`runtime/runs/original-playset/process-exit.json` | 두 UI 소유 PID의 정상 퇴장 뒤 부재·강제 종료 없음. Steam 표시 상태는 별도 UI 증거로 확인 |
| `ui/11-steam-play-restored.png`·`ui/observations.json`의 `steam-play-restored` | 정상 Stop 후 Stopping·Downloads 대기열/다른 게임 부재 대조·Steam 정상 Exit/재실행·HOI4 초록 Play 복귀의 실제 UI 관측 |

최종 독립 QA는 `TASK/geography/final-closeout-review.json`에, 실제 runtime 8파일과 유지 기록 5파일의 원본·사본·SHA-256 대응은 `TASK/documentation/final-source-and-records/manifest.json`에 보존했다. 최종 6 native의 원본 manifest에서 실제 변경 8파일을 대조한 범위는 `TASK/documentation/final-source-and-records/native-manifest-scope-index.json`, 런타임 종료·복원·Steam 표시의 마감 색인은 `TASK/runtime/RUNTIME_CLOSEOUT.md`를 따른다. 이번 소스·문서 QA는 상대링크 214개의 파일·anchor, JSON·UTF-8 및 동결 소스/기록 사본을 확인한 것이며, 서로 다른 소스·native·UI·저장 검증 수를 합산하거나 전체 엔진·바이너리 검증을 뜻하지 않는다.

네이티브 실행별 PID·로그/저장 원본과 사본 대응·모드 구성·소스 안정성은 위 runtime 색인에 보존했다. 실제 UI의 직접 시작·시간 진행·완료·정부 툴팁·첫 로컬 Save·원래 playset의 새 프로세스 UI Load·며칠 진행·재저장·정상 Quit는 위 별도 절과 `ui/observations.json`에 기록했다. 명목 35일의 정확한 달력 경과·두 번째 저장의 추가 재로드·변경 전 저장·장기/DLC/멀티플레이는 미검증이다. 소유 프로세스 부재·설정/이어하기 원복·기존 124개 저장 해시 보존은 아래 최종 증거로 확인했으며, Steam 표시도 정상 종료·재시작 뒤 **초록 Play 복귀를 실제 확인**했다. 정상 Quit나 첫 저장의 Load 성공을 전체 무오류·모든 조합의 호환성으로 확대하지 않는다.

### 프로세스·설정·기존 저장의 최종 대조

`runtime/final-save-preservation.json`의 **2026-11-19 05:41:49 UTC** 최종 대조는 시작 시 기록한 기존 저장 **124개 모두 SHA-256 불변, 변경 0개**를 확인했다. 기존 저장을 추가 진단에 로드하거나 덮어쓰지 않았다. 새로 생긴 **33개·2,340,456,234바이트**는 이번 `TEST_FAIL_HOK_SDG` 진단 원본 31개와 고유 UI 원본 2개이며 예상 밖 신규 파일은 없다. 진단 이름의 `TEST_FAIL` 접두사는 수집 명명 규칙이므로 개별 실행의 최종 FAIL 판정을 대신하지 않는다. 게임 생성 원본은 실제 사용자 저장 폴더에 유지하고 증거 사본·위치/해시는 TASK에 보존했으며 이번 문서 작업에서 이동·삭제하지 않았다.

같은 보고서의 baseline **11개 profile 파일 모두 SHA 일치**에는 `settings.txt`·`dlc_load.json`·실제 `pdx_settings.txt`와 **142바이트 `continue_game.temp`**가 포함된다. 처음 없던 `pdx_settings.json`·`user_settings.config`·`continue_game.json`은 다시 부재이며 probe pointer도 없다. `restoration-20261119T054056370212Z.json`은 마지막 복원 작업과 `games = []`를 기록한다. 런타임 담당의 두 UI `process-exit.json`에서 PID **24500·10004**는 모두 **Already exited**, `termination = null`로 수집돼 이 마지막 종료 단계에서 강제 종료를 하지 않았음을 확인한다. 실제 Quit→OK 조작은 root의 UI 관측이 별도로 증명한다.

`runtime/final-source-preservation.json`의 **2026-11-19 05:45:12 UTC 교정본**은 독립 `geography/independent-source-review-final-freeze-05.json`의 실제 변경 8파일 목록을 자동으로 사용했다. 중점·결정·출범 effect·state trigger·고유 정부 현지화 2파일·base `korea_focus_l_*` 2파일의 freeze05 해시가 **최종 6 native와 두 UI 세션의 18개 launch/capture 지점 및 최종 원문**에 모두 일치한다. 원문은 `runtime/final-task-source-copy/`에 보존했다. 독립 QA도 `documentation/final-source-and-records/native-manifest-scope-index.json`에서 최종 6 native의 manifest 각각에 실제 8파일이 포함되고 freeze05와 일치함을 48개 항목으로 대조했다.

최초 수동 요약 inventory는 base `korea_focus_l_*` 2파일 대신 유지된 `HOK_KOR_democratic_support_l_*` 2파일을 선택하는 보고서 오류가 있었다. 원래 348파일 manifest에는 실제 base 중점 현지화가 처음부터 포함됐으므로 기존 실행을 다른 소스로 바꾸거나 재실행한 것이 아니다. 잘못된 요약은 `runtime/final-source-preservation-scope-01-superseded.json`에 보존하고 정확한 8파일로 요약·최종 사본을 교정했다. 이 수집 범위는 텍스트/runtime 코드 348파일이며 전체 바이너리 자산 검증으로 확대하지 않는다.

마지막 original-playset 로그 사본은 `runtime/runs/original-playset/capture-20261119T054043650305Z/logs/`, 첫 UI 로그는 `runtime/runs/ui-ready/capture-20261119T052549138992Z/logs/`다. 런타임 담당은 마지막 로그에서 수정 검사 파일의 parser/invalid-scope 오류가 없음을 보고했지만, 기존 descriptor·현지화 충돌·map building 항목과 OneDrive의 random/continue/save rename 오류는 남아 있다. 조용한 전체 로그나 OneDrive 오류 해결로 확대하지 않는다. 게임 프로세스가 없는데 Steam이 Stopping에 남은 현상은 다음 UI 절차로 별도 종료했다. root는 정상 Stop→확인 뒤에도 Stopping인 것을 확인하고 Downloads의 0 bps·queue 0·완료 항목 HOI4뿐임과 다른 active 게임이 없음을 직접 확인했다. 이어 Steam 메뉴 Exit로 정상 종료하고 Steam 앱 부재를 확인한 뒤 기존 Steam 앱을 정상 실행했다. Library의 HOI4에서 **초록 Play 복귀**를 실제 관측했다. 증거는 `ui/11-steam-play-restored.png`와 `ui/observations.json`의 `steam-play-restored` 항목이다. OS 재시작이나 다른 앱 강제 종료는 수행하지 않았다.

기존 저장소의 시험 PNG **4개·총 815,391바이트(796.3 KiB)**는 별도 정리 미결이며 이번 구현에서 이동·삭제하지 않는다. 위치·개별 크기는 다음과 같고, 외부 `TASK/geography/independent-source-review-final-freeze-05.json`의 QA inventory에 보존했다.

| 기존 시험 자료 | 크기 |
|---|---:|
| [hide-upper.png](../assets/korean-fascist-mobilization-validation-20260923/hide-upper.png) | 200,095바이트 |
| [normal-completion.png](../assets/korean-fascist-mobilization-validation-20260923/normal-completion.png) | 194,137바이트 |
| [normal-progress.png](../assets/korean-fascist-mobilization-validation-20260923/normal-progress.png) | 217,201바이트 |
| [show-upper.png](../assets/korean-fascist-mobilization-validation-20260923/show-upper.png) | 203,958바이트 |

원작자·기존 자산·안정 ID를 보존하고, 관련 없는 게임플레이·배치·이미지·다른 이념 경로를 수정하지 않았다. 커밋·푸시·업로드를 수행하지 않았다.
