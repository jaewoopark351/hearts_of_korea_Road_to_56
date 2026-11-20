# 콘텐츠 호출·진행·배치와 기능별 시퀀스

기준: **2026-11-20, Asia/Seoul**. `feat/korean-focus-update-20260922@9a01955785bcdd827c9c85522537a0bfc57ed654` 위 현재 미커밋 작업 트리의 소스 설명이다. 이번은 문서·도표만 상세화하며 게임 코드·설정·검증 결과를 바꾸지 않는다.

[전체 목차](README.md) · [도메인과 scope](domain-model.md) · [산둥 사례](shandong-government.md) · [상세화 기록](../implementation/2026-11-20-architecture-detail-expansion.md) · [유지 안내](maintenance.md)

호출, 조건 조회, 진행 선행, 배치 기준은 서로 다른 관계다. 아래 도표는 주요 공용 경로와 실제 대표 기능을 상세히 연결한다. 전체 중점의 좌표·분기는 [좌표 명세](../HOK_KOREAN_FOCUS_LAYOUT_COORDINATES.md)와 각 정의를 정본으로 삼는다.

<a id="d05-call-and-reference"></a>

## D05 · 진입점에서 조건·효과·데이터까지

실선은 표시한 효과 호출·상태 변경, 점선은 조건 또는 ID 조회다. subgraph는 서로 다른 기능군이며 한 번의 실행에서 모두 호출된다는 뜻이 아니다.

[![D05 · 진입점과 공용 처리의 상세 관계](images/D05.dark.png)](images/D05.dark.svg)

<details>
<summary>Mermaid 편집 원본</summary>

```mermaid
---
config:
  theme: dark
---
flowchart TB
    subgraph Civic["시작·월간·시민사회"]
        Start["on_startup"] --> Register["register_legacy_civic_state"]
        Month["on_monthly_KOR"] --> Update["monthly_civic_update"]
        Update --> Register
        Register --> Init["initialize_civic_system / 기존 정책 once guard"]
        Update --> Drift["정책별 변수 증감 / sync_civic_state"]
        Drift -. 자격 조회 .-> Crisis["prosecutor_crisis_eligible"]
        Drift -->|위기 자격을 충족할 때만| Queue["pending flag / CIVIC.20 하루 후"]
        Queue --> Event["사건 선택지의 후속 효과"]
    end
    subgraph Projects["CNDP 결정"]
        CNDP["주별 결정의 visible / available / cancel / remove"] -. 반복 조회 .-> Territory["주별 territory_trigger"]
        Territory -. Country / State 조회 .-> Contract["v1 / 비항복 / 소유 / 완전통제 / 미완료"]
        CNDP --> Reward["remove_effect의 재검사 후 보상 / 주 완료 flag"]
    end
    subgraph Democracy["지원·출범·후속 인정"]
        SupportFocus["중국·일본 지원 중점 완료"] --> Notice["unlock_decision_tooltip"]
        Support["지원 결정 complete_effect"] -. 중국 대상 / 중복 차단 .-> Targets["16태그 공유 필터 / 기존 idea"]
        Support --> Timed["현존 대상 add_timed_idea 180일"]
        FormFocus["중국 축출 중점 completion_reward"] --> Form["form_chinese_democratic_government"]
        Form -. can_form / 이전 적격 .-> Gates["중국 공유 trigger"]
        Form --> Core["grant_mainland_cores"]
        Recognize["KOR_New_China_Government"] --> Annex["KCH에서 CHI만 annex_country"]
        Recognize --> Core
        JapanFocus["KOR_minshu_ikki / JAP scope"] --> Japan["japanese_democratic_uprising"]
        Japan --> Rebel["내전 / 반군 초대 / 한국 참전"]
    end
    subgraph Intelligence["공통 군사 가지"]
        Intel["정보국 중점 completion_reward"] --> Agency["기관 없을 때만 create_intelligence_agency"]
        Intel --> Idea["영구 정보국 idea / modifier"]
    end
    %% 그룹의 세로 배치 전용이며 게임 호출 관계가 아님
    Civic ~~~ Projects ~~~ Democracy ~~~ Intelligence
```

</details>

| 경로 | 실제 정의·계약 | 생략하면 안 되는 차이 |
|---|---|---|
| 시작·월간 시민사회 | [on_actions](../../common/on_actions/HOK_KOR_civic_on_actions.txt), [효과](../../common/scripted_effects/HOK_KOR_civic_effects.txt), [공유 조건](../../common/scripted_triggers/HOK_KOR_civic_triggers.txt), [사건](../../events/HOK_KOR_civic_events.txt) | startup과 월간 모두 명시적 KOR 문맥을 쓴다. 초기화·옛 중점 등록은 once guard, 월간 수치는 정책 조건에 따라 다르다. 위기의 자격이 있을 때만 pending과 하루 뒤 사건을 설정한다. |
| CNDP | [결정](../../common/decisions/KOR_decision.txt), [trigger](../../common/scripted_triggers/HOK_KOR_cndp_triggers.txt) | 종료 보상은 `remove_effect`다. 지원 결정의 즉시 `complete_effect`와 혼동하지 않는다. [D25](#d25-cndp-sequence)에서 취소·종료를 구분한다. |
| 지원 | [중점](../../common/national_focus/korea.txt), [결정](../../common/decisions/HOK_KOR_democratic_support.txt), [필터](../../common/scripted_triggers/HOK_KOR_chinese_democratic_support_triggers.txt) | 중점은 해금 안내와 완료 이력을 제공하며 자동 지원금을 지급하지 않는다. 결정 visible은 `has_completed_focus`를 읽는다. |
| 중국 출범·인정 | [효과](../../common/scripted_effects/HOK_KOR_chinese_government_effects.txt), [조건](../../common/scripted_triggers/HOK_KOR_chinese_government_state_triggers.txt), 한국 결정 | 출범과 인정은 core helper만 공유한다. 인정 결정은 출범 helper 재실행이나 모든 군벌 합병이 아니다. |
| 일본 봉기·정보국 | [일본 helper](../../common/scripted_effects/HOK_KOR_democratic_intelligence_effects.txt), [정보국 idea](../../common/ideas/HOK_KOR_democratic_intelligence.txt) | 일본 내전은 CHI 문턱·중국 영토 선택과 별도다. 정보국은 La Résistance 가지이고 산둥은 TfV 진입 조건이다. |

<a id="d06-focus-prerequisite"></a>

## D06 · 직접 선행·상호 배타·별도 가용 조건

실선 화살표는 실제 `prerequisite`, 화살촉 없는 선은 `mutually_exclusive`, 점선은 별도 가용 조건이다. 선택한 민주 외교·지원 및 공통 군사 가지를 그린다. 연결하지 않은 부모 경로는 실제 소스에서 계속 읽는다.

[![D06 · 주요 중점의 선행과 별도 가용 조건](images/D06.dark.png)](images/D06.dark.svg)

<details>
<summary>Mermaid 편집 원본</summary>

```mermaid
---
config:
  theme: dark
---
flowchart TB
    Independent["KOR_independent_party_in_power"] --> Vanguard["KOR_the_vanguard_of_asian_democracy"]
    Vanguard --> ChinaSupport["KOR_support_for_democracy_in_china"]
    Vanguard --> JapanSupport["KOR_support_for_democracy_in_japan"]
    ChinaSupport --> ChinaForm["KOR_overthrow_the_chinese_dictators<br/>cost10 / 기본70일"]
    JapanSupport --> JapanRevolt["KOR_minshu_ikki<br/>cost5 / 기본35일"]
    Claim["KOR_claiming_northern_conquest"] --> Strike["KOR_preemptive_strike_on_manchuria"]
    Strike ---|mutually_exclusive| Alliance["KOR_rok_roc_alliance"]
    Claim --> Alliance
    Strike --> Europe["KOR_liberation_of_the_europe"]
    Strike --> Union["KOR_founding_of_the_asian_union"]
    Europe ---|mutually_exclusive| Union
    Union --> IndependentInvite["KOR_invitation_to_independent_asian_countries"]
    Union --> ChinaInvite["KOR_invite_china"]
    Union --> JapanInvite["KOR_invite_japan"]
    Politics["한국 민주·독립 / 대상 조건"] -. available .-> ChinaSupport
    Politics -. available .-> JapanSupport
    CHIGate["TfV / CHI 민주50% / KCH 부재<br/>안전한 거점 / 현 중국맹주 비민주"] -. available .-> ChinaForm
    JGate["한국 민주·독립 / JAP 비민주<br/>JAP 인간 제어 허용"] -. available .-> JapanRevolt
    Rearm["KOR_begin_rearmament"] --> Intel["HOK_KOR_expand_secret_intelligence_service"]
    DLC["La Resistance"] -. allow_branch .-> Intel
```

</details>

지원 중점과 초대 중점 사이에는 이전 배타 관계를 그리지 않는다. 현재 소스에서 제거된 관계이기 때문이다. 지원의 선행은 Vanguard, 초대의 선행은 Union으로 서로 다르다. 중국 출범 중점은 `cancel_if_invalid = yes`, `continue_if_invalid = no`이며 가용 조건이 유지되어야 한다. 공유 `can_form`은 효과 직전에 TfV·CHI50%·KCH 부재·안전 거점을 재검사하되 중점의 모든 추가 정치 조건을 그대로 복제한 것은 아니다.

근거는 [한국 중점](../../common/national_focus/korea.txt)과 [배치·선행 이식 기록](../implementation/2026-11-20-democratic-support-layout.md)이다. `ai_will_do`와 [역사 AI의 순서](../../common/ai_strategy_plans/KOR_historical_strategy_plan.txt)는 선행 관계와 별도다. 기본 기간은 해당 cost의 명목 기간이며 실제 진행 보정·은행 일수·선택일을 대체하지 않는다.

<a id="d07-focus-placement"></a>

## D07 · 실제 relative_position_id와 로컬 좌표

실선은 `relative_position_id` 사슬만 뜻한다. 노드의 `(x,y)`는 해당 부모에 대한 로컬 값이다. 점선은 추가로 읽어야 하는 배치 입력이다. 그림에서 상자가 놓인 위치 자체는 HOI4 좌표가 아니다.

[![D07 · 상대 배치와 최종 좌표의 입력](images/D07.dark.png)](images/D07.dark.svg)

<details>
<summary>Mermaid 편집 원본</summary>

```mermaid
---
config:
  theme: dark
---
flowchart TB
    Party["독립당 집권 anchor"] -->|relative_position_id| Vanguard["Vanguard / -5,2"]
    Vanguard -->|relative_position_id| CS["중국 지원 / -6,1"]
    Vanguard -->|relative_position_id| JS["일본 지원 / -3,1"]
    CS --> CF["중국 출범 / 0,2"]
    JS --> JR["일본 봉기 / 0,2"]
    Claim["북방 진출 anchor"] --> Strike["만주 선제타격 / 2,2"]
    Strike --> Europe["유럽 해방 / -2,2"]
    Strike --> Union["아시아 연합 / 1,2"]
    Union --> Invite["아시아 독립국 초대 / 0,2"]
    Union --> CI["중국 초대 / -2,2"]
    Union --> JI["일본 초대 / 2,2"]
    Rearm["재무장 시작 / 절대54,0"] --> Intel["정보국 / 8,1"]
    Ancestors["상위 anchor의 누적 좌표"] -. 입력 .-> Resolve["현재 조건에서 최종 좌표 해석"]
    Offset["조건부 offset / 정치 가지 HIDE·SHOW"] -. 입력 .-> Resolve
    Vanguard -. 사슬 입력 .-> Resolve
    Union -. 사슬 입력 .-> Resolve
    Intel -. 사슬 입력 .-> Resolve
    Resolve --> Layout["인접 중점·명판·아이콘·선의 실제 화면 확인"]
```

</details>

[좌표 정본](../HOK_KOREAN_FOCUS_LAYOUT_COORDINATES.md), [이번 로컬 배치 자료](../data/HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_PORT_LAYOUT.json), [한국 중점 소스](../../common/national_focus/korea.txt)를 함께 읽는다. 같은 부모를 쓰는 것과 같은 선행을 갖는 것은 별개다. 정보국은 공통 군사 가지로 이동했으므로 이전 민주 HIDE gate를 새 조건인 것처럼 복원하지 않는다. 이 도표는 전체 중점의 실제 화면 충돌 확인을 새로 수행했다는 뜻이 아니다.

<a id="d23-support-cycle"></a>

## D23 · 반복 민주 지원의 구매·중복 차단·만료

화살표는 정의에 따른 평가·효과 순서이며 사용자 조작을 새로 재현한 기록이 아니다. 중국은 공용 필터를 통과한 **현재 존재하는 정식 16태그 집합**, 일본은 JAP 한 국가를 대상으로 한다.

[![D23 · 지원 결정의 반복 주기](images/D23.dark.png)](images/D23.dark.svg)

<details>
<summary>Mermaid 편집 원본</summary>

```mermaid
---
config:
  theme: dark
---
sequenceDiagram
    participant Player as 플레이어 또는 AI
    participant KOR as KOR 결정 문맥
    participant Targets as 현재 적격 대상국
    participant Clock as 결정·국민정신 기간
    Player->>KOR: 중국 또는 일본 지원 중점 완료
    KOR->>KOR: 완료 이력과 unlock_decision_tooltip
    Player->>KOR: 지원 결정 조회
    KOR->>KOR: original_tag KOR·중점 이력·민주·독립 확인
    KOR->>Targets: 대상 존재와 기존 지원 idea 조회
    alt 대상 없음 또는 하나라도 기존 지원 남음
        KOR-->>Player: 현재 구매 불가
        Note over KOR,Targets: 기존 지원 기간을 덮어쓰지 않음
    else 가용 조건·정치력 충족
        Player->>KOR: 25 정치력으로 선택
        KOR->>Targets: complete_effect에서 add_timed_idea 180일
        KOR->>Clock: days_remove 180 / days_re_enable 0
        Note over Targets,Clock: 중국은 구매 당시 존재한 대상만 지급
        Clock->>Targets: 각 대상의 지원 idea 만료
        Clock->>KOR: 결정의 180일 활성 기간 종료
        Player->>KOR: 같은 조건으로 다시 구매 조회
        KOR->>Targets: 어떤 대상에도 지원 idea가 없는지 재확인
    end
```

</details>

[지원 결정](../../common/decisions/HOK_KOR_democratic_support.txt)의 중국·일본 두 블록과 [공유 필터](../../common/scripted_triggers/HOK_KOR_chinese_democratic_support_triggers.txt)를 정본으로 삼는다. 중국 지원은 동적 내전·협력정부 복제를 제외하며, 현존 대상 하나라도 기존 지원 idea가 남으면 묶음 구매가 차단된다. 예전 280일 지원이나 서로 다른 잔여 기간을 강제로 180일로 초기화하지 않는다. 활성 중간에 출현한 나라에 자동 지급하는 월간 처리도 없다. 일본 결정은 별도 존재·중복 검사이며 중국 timer와 공유하지 않는다.

과거 실제 지원 만료·재구매, 실패한 자동 진단과 별도 수동 증거는 [실행 기록](../implementation/2026-11-20-korean-democratic-support-intelligence-port.md)을 따른다. 이번 시퀀스 작성은 그 검증을 다시 실행한 것이 아니다.

<a id="d24-intelligence-sequence"></a>

## D24 · 정보국 중점과 기존 기관 재사용

기간선은 명목 중점 진행이다. 새 기관의 모든 세부 설정, 첩보원 자동 모집, 과학자·첩보원 초상화 처리까지 이 중점이 수행한다는 뜻이 아니다.

[![D24 · 정보국 중점의 조건과 완료 효과](images/D24.dark.png)](images/D24.dark.svg)

<details>
<summary>Mermaid 편집 원본</summary>

```mermaid
---
config:
  theme: dark
---
sequenceDiagram
    participant Tree as 한국 공통 군사 중점
    participant KOR as KOR 국가
    participant Agency as 정보기관
    participant Spirit as 전용 영구 국민정신
    Tree->>KOR: KOR_begin_rearmament 완료 이력 조회
    Tree->>KOR: La Resistance allow_branch 확인
    alt DLC 가지가 허용되지 않음
        Tree-->>KOR: 해당 가지 비허용
    else 선행 완료·가지 허용
        KOR->>Tree: 정보국 중점 선택 / cost5 기본35일
        Tree->>KOR: completion_reward
        KOR->>Agency: has_intelligence_agency 조회
        alt 기관 없음
            KOR->>Agency: create_intelligence_agency yes
        else 기관 이미 있음
            Note over KOR,Agency: 기존 기관 유지 / 생성 명령 생략
        end
        KOR->>Spirit: add_ideas HOK_KOR_secret_intelligence_service_idea
        Spirit->>KOR: operative_slot 2 및 정보·작전 modifier
        Note over KOR,Spirit: 기간제 idea가 아님 / removal_cost -1
    end
```

</details>

근거: [중점](../../common/national_focus/korea.txt)의 `HOK_KOR_expand_secret_intelligence_service`, [idea 정의](../../common/ideas/HOK_KOR_democratic_intelligence.txt), [역사 AI](../../common/ai_strategy_plans/KOR_historical_strategy_plan.txt). AI 목록은 재무장 뒤 정보국을 배치하지만 실제 선택·완료 시점은 게임 상황에 의존한다. 영구 idea의 `intel_network_gain = 10`과 `intel_network_gain_factor = 0.25`는 서로 다른 modifier다. 전체 수치를 도표에 재정의하지 않고 해당 파일에서 확인한다.

<a id="d25-cndp-sequence"></a>

## D25 · CNDP 전북 사업의 착수·취소·종료 재검사

실제 `HOK_KOR_cndp_develop_jeollabuk`를 예로 든다. 모든 사업의 비용·기간·보상까지 같은 것으로 일반화하지 않는다. 전북 State919와 승점 Province13550은 다른 종류의 ID다.

[![D25 · CNDP 사업의 조건과 일회 보상](images/D25.dark.png)](images/D25.dark.svg)

<details>
<summary>Mermaid 편집 원본</summary>

```mermaid
---
config:
  theme: dark
---
sequenceDiagram
    participant KOR as KOR 결정
    participant Gate as 전북 territory_trigger
    participant State as State919
    participant Clock as 90일 사업
    KOR->>KOR: v1 flag·국토개발 중점·주 미완료로 visible 확인
    KOR->>KOR: construction3·사용 가능 민공 5 초과 확인
    KOR->>Gate: available에서 공용 지역 조건 조회
    Gate->>State: 한국 소유·완전통제·미완료 확인
    Gate-->>KOR: v1·비항복과 주 조건 결과
    alt 가용 조건 실패
        KOR->>KOR: 착수 차단
    else 가용 조건 충족
        KOR->>Clock: 75 정치력 / 민공5 사용 / 90일
        loop 사업 중 cancel_trigger 평가
            KOR->>Gate: 같은 territory_trigger 재조회
        end
        alt 지역 조건 무효
            Clock->>KOR: 취소 / cancel_effect 빈 블록
            Note over KOR,State: 이 취소 효과에는 보상·완료 flag 없음
        else 기간 종료
            Clock->>KOR: remove_effect
            KOR->>Gate: 효과 직전 같은 지역 조건 재조회
            alt 최종 조건 유효
                KOR->>State: 낮은 등급이면 large_town
                KOR->>State: coal 1 / Province13550 VP 1 추가
                KOR->>State: developed_v1 flag 설정
            else 최종 조건 무효
                Note over KOR,State: 보상과 완료 표식 생략
            end
        end
    end
```

</details>

근거: [한국 결정](../../common/decisions/KOR_decision.txt), [CNDP trigger](../../common/scripted_triggers/HOK_KOR_cndp_triggers.txt), [KOR 시작 이력](<../../history/countries/KOR - Korea.txt>), [ADR-0007](../decisions/0007-november-content-integration.md), [실제 이식 기록](../implementation/2026-11-08-hok-upstream-content-port.md). 국가의 `HOK_KOR_cndp_state_projects_v1`과 주의 `HOK_KOR_cndp_developed_v1`은 저장 scope가 다르다. 새 게임은 13개 독립 사업 경로, 해당 국가 버전 표식 없는 저장은 기존 7개 지역 경로를 유지한다. 이 기능 guard는 옛 지도 저장의 마이그레이션이 아니다. 빈 `cancel_effect`에서 비용 환불 같은 미기재 효과를 만들어 설명하지 않는다.

## 처리 대장과 갱신 범위

| 기능·도표 | 처리 | 소스에서 확인한 의미·남은 범위 |
|---|---|---|
| D05 호출·공유 helper | **문서 수정** | 시작·월간 시민사회, CNDP, 중국 출범·인정, 지원·일본·정보국의 실제 진입점을 분리했다. |
| D06 선행·배타 / D07 배치 | **문서 수정** | 실제 부모·로컬 좌표·별도 가용 조건을 명시했다. 지원과 초대의 제거된 배타 관계는 복원하지 않는다. |
| D23–D25 시퀀스 | **문서 추가** | 지원 즉시 지급, 정보국 조건 생성, CNDP 종료 보상·취소·재검사를 각각 구분했다. |
| 기존 ID·비용·기간·공유 조건·완료 표식·AI | **의도적 유지** | 문서가 설명하는 runtime을 변경하지 않는다. 표시와 실제 효과는 별도 관측 대상이다. |
| 모든 중점·사건·DLC 경로의 전수 도식 | **제외** | 현재 주요 공용 구조와 세 기능의 실제 경로를 상세화한다. 생략한 개별 분기는 해당 코드·정본 명세로 연결한다. |
| 실제 선택·기간 경과·효과·새/기존 저장·장기 AI·MP | **미확인 또는 기존 기록 범위** | 이번은 읽기와 문서 작업이다. 이전 기록의 실행 조건·실패·한계를 새 도표 통과로 합산하지 않는다. |

호출자·공유 trigger·기간/취소·정치/DLC 조건이 바뀌면 관련 도표와 [변경 영향 절차](../HOK_CHANGE_COVERAGE_REVIEW.md)를 함께 대조한다. 개념적으로 같은 문구를 쓰더라도 `complete_effect`와 `remove_effect`, 정부 출범과 후속 인정의 효과를 하나로 합치지 않는다.

배치 안내: 독립 사례 그룹은 세로로 읽도록 정렬했다. Mermaid의 `~~~`는 보이지 않는 배치 제약이며 함수 호출·선행 조건·실행 순서를 추가하지 않는다.
