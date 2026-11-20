# 산둥 정부의 호출·선택·이전·인물 수명주기

기준: **2026-11-20, Asia/Seoul**. 호환판 `feat/korean-focus-update-20260922@9a01955785bcdd827c9c85522537a0bfc57ed654` 위 현재 미커밋 소스를 읽은 설명이다. 이번은 문서·도표만 상세화한다. 소스의 실행 순서와 이전 실제 관측·미검증을 구분하며 게임을 다시 실행하지 않는다.

[전체 목차](README.md) · [scope](domain-model.md) · [State 이전 상세](states/ownership-and-transfer.md) · [상세화 기록](../implementation/2026-11-20-architecture-detail-expansion.md) · [유지 안내](maintenance.md)

정본은 [출범 효과](../../common/scripted_effects/HOK_KOR_chinese_government_effects.txt), [공유 조건](../../common/scripted_triggers/HOK_KOR_chinese_government_state_triggers.txt), [공유 정식 중국국 필터](../../common/scripted_triggers/HOK_KOR_chinese_democratic_support_triggers.txt), [지리 대응 기록](../implementation/2026-11-20-chinese-government-state-mapping.md)이다. 포트의 본토 집합은 RT56 Gyarong1075를 포함한 64주다. 원본 63주를 번호만 치환한 집합이나 새 지도 재분할이 아니다.

<a id="d15-call-and-shared-guards"></a>

## D15 · 중점·공유 조건·공용 핵심주·후속 인정

실선은 효과 호출·결과, 점선은 조건 조회다. 중점 `available`과 helper 내부 `can_form`은 같은 전체 조건을 중복한 것이 아니다. `unlock_decision_tooltip`은 후속 결정 안내이며 국가 생성 효과가 아니다.

[![D15 · 산둥의 진입과 후속 인정 연결](images/D15.dark.png)](images/D15.dark.svg)

<details>
<summary>Mermaid 편집 원본</summary>

```mermaid
---
config:
  theme: dark
---
flowchart TB
    Support["KOR_support_for_democracy_in_china"] -->|prerequisite| Focus["KOR_overthrow_the_chinese_dictators<br/>cost10 / 기본70일 / invalid시 취소"]
    Focus -. available .-> Political["KOR 민주·독립 / 현 중국맹주 존재·비민주"]
    Focus -. available .-> Shared["TfV / CHI 존재·민주50% 이상<br/>KCH 부재 / 안전한 산둥 거점"]
    Focus -->|completion_reward| Form["form_chinese_democratic_government"]
    Form -. 본문 진입 limit .-> CanForm["can_form / 위 공유4조건 재검사"]
    CanForm -. 거점 조회 .-> Bootstrap["597 또는743 / can_bootstrap_state"]
    Bootstrap -. 조회 .-> Transfer["can_transfer_state"]
    Transfer -. 지역 .-> Mainland["RT56 본토64주"]
    Transfer -. 보호·통제 .-> Protected["KOR 소유·통제 제외 / 혼합 통제 제외"]
    Transfer -. owner와controller 각각 .-> Donor["is_donor"]
    Donor -. 국가 .-> Targets["현존 정식16태그 / 동적 복제 제외"]
    Donor -. 종속 .-> Japan["일본 직접·2단계 종속 제외"]
    Bootstrap -. 원국 존속 .-> Last["원소유국 소유 주 1 초과"]
    Form --> Create["선택 계획 / 동적 정부 생성 / 순서대로 이전"]
    Create --> Core["grant_mainland_cores"]
    Core --> AllCore["본토64주 State에 add_core_of<br/>이것만으로 소유권은 바뀌지 않음"]
    Focus --> Notice["KOR_New_China_Government 해금 안내"]
    Focus --> WarGoal["현존16대상에 한국의 puppet 전쟁목표"]
    Recognize["후속 KOR_New_China_Government"] -. visible .-> Completed["축출 중점 완료 이력"]
    Recognize -. available .-> Follow["KOR 독립 / KCH와 같은 세력<br/>CHI가 KOR 종속"]
    Recognize --> Annex["KCH에서 CHI만 annex_country"]
    Recognize --> Cosmetic["KCH_china cosmetic tag"]
    Recognize --> Core
```

</details>

조건의 정확한 경계는 다음과 같다.

| 항목 | 소스 계약 | 구분 |
|---|---|---|
| 중점 진입·유지 | [한국 중점](../../common/national_focus/korea.txt): 민주·독립 KOR, 현 중국맹주 존재·비민주, 공유4조건, `cancel_if_invalid=yes`·`continue_if_invalid=no` | 기본70일을 실제 관측 경과일과 동일시하지 않는다. 한국의 세력 맹주 조건은 제거됐다. |
| helper 재진입 | `can_form`: TfV, CHI 존재·민주 지지도50% 이상, KCH 부재, 안전 거점 | 외부 중점의 모든 정치 조건을 재구현하지 않는다. 이 조건 실패 시 helper 본문은 건너뛴다. 강제로 중점 효과를 호출하는 것은 정상 진행과 별도다. |
| 이전 적격·거점 | 본토·한국 보호·완전통제·적격 owner/controller; 거점은 원국 소유 주 1 초과 추가 | 일반 이전 가능한 마지막 주가 첫 거점으로도 가능하다는 뜻이 아니다. [S08](states/ownership-and-transfer.md#s08-transfer-eligibility)에서 확대한다. |
| 후속 인정 | [한국 결정](../../common/decisions/KOR_decision.txt)의 `KOR_New_China_Government` | CHI만 합병하고 같은 core helper를 호출한다. 모든 군벌 자동 합병·출범 helper 재호출이 아니다. |
| DLC tooltip의 옛 이름 | `HOK_KOR_chinese_government_mtg_tt`라는 안정 키 | 현재 실제 조건은 Together for Victory다. 키 이름에 남은 mtg를 Man the Guns 조건으로 해석하지 않는다. |

<a id="d16-formation-order"></a>

## D16 · 한국·원국·생성국의 실제 처리 순서

시퀀스는 효과 파일의 순서를 설명한다. 같은 비율을 입력하는 것과 각 사단·함정·항공기·비축의 실제 결과가 정확히 비례하는 것은 별도다. 생성국의 실제 태그는 고정하지 않는다.

[![D16 · 산둥 출범의 상세 시퀀스](images/D16.dark.png)](images/D16.dark.svg)

<details>
<summary>Mermaid 편집 원본</summary>

```mermaid
---
config:
  theme: dark
---
sequenceDiagram
    participant KOR as KOR 진입 국가
    participant Donor as 적격 원국들
    participant Land as 후보·선택 State
    participant New as 실제 생성국 original_tag KCH
    KOR->>KOR: can_form 재검사
    alt 공유 진입 조건 실패
        Note over KOR,New: helper 본문 미실행
    else 공유 진입 조건 충족
        KOR->>KOR: sponsor event target 저장
        KOR->>Donor: p를 0–90%로 clamp / snapshot
        Donor->>Land: 이전 적격 주에 candidate flag
        Land->>Donor: 적격 주 수 집계 / land_budget = 수×p
        KOR->>Land: 597·743 후보와 적격 SND 소유 본토 선택
        loop 새 선택 존재·남은 passes 이내 / 최대64회
            KOR->>Land: 미선택·원국 예산1 이상·선택 주 인접 후보
            Land->>Donor: selected / participant / 예산1 차감
            Land->>KOR: progress =1
        end
        KOR->>New: create_dynamic_country original_tag KCH
        activate New
        New->>New: 생성국 global target / 민주정치
        New->>New: 전용 Weng 소속 이동·승격 / 본토 core
        New->>Land: 안전한597 우선 또는743 이전 / 수도 설정
        deactivate New
        opt 양수p 참여국에 배치 항공기 있음
            KOR->>New: 생성국의 현재 소유 공군기지 조회
            opt 생성국 소유 공군기지 없음
                KOR->>Land: 선택된 안전한 기존 공군기지 후보 순회
                Land->>New: 아직 기지가 없을 때 후보 주 먼저 이전
            end
            opt 그 뒤에도 생성국 소유 공군기지 없음
                New->>New: 수도에 air_base 1 즉시 건설
            end
        end
        loop 참여 원국마다
            alt snapshot p 양수
                Donor->>New: transfer_units_fraction / 전력·비축 같은 p
                Note over Donor,New: 원국 지휘관 유지 trigger
            else p=0
                Note over Donor,New: 귀순 명령 생략
            end
        end
        opt SND 잔여 모든 주가 선택됨·현재 이전 가능
            KOR->>Donor: SND 미귀순 장비·연료·수송선 잔여 정리
        end
        KOR->>Land: 선택 주의 can_transfer_state 재검사
        Land->>New: 나머지 적격 선택 주 transfer_state
        KOR->>New: autonomy_dominion / 기존 전쟁 종료하지 않음
        KOR->>New: add_to_faction
        KOR->>Land: 본토 candidate·selected flag 제거
        KOR->>Donor: snapshot·participant·예산·share 제거
        KOR->>KOR: progress·passes·생성국 global target 제거
    end
```

</details>

생성 child가 저장한 `HOK_KOR_chinese_democratic_government` global event target은 이후 별도 효과 문맥에서 같은 생성국을 찾는 수단이다. 첫 거점과 먼저 넘길 공군기지는 bootstrap 조건으로 원국의 마지막 주를 보호한다. 뒤의 일반 이전은 각 주의 이전 적격을 다시 검사한다. 따라서 후보 선택 당시의 소유·통제만으로 나중 이전을 확정하지 않는다.

`set_autonomy`는 `end_wars=no`, `end_civil_wars=no`를 명시한다. 세력 연결의 실제 엔진 처리와 한국 비맹주 조합은 [기존 실행 기록](../implementation/2026-11-20-korean-democratic-support-intelligence-port.md)을 따른다. 도표만으로 모든 세력·전쟁·DLC 조합을 지원한다고 판단하지 않는다.

<a id="d17-territory-and-remainders"></a>

## D17 · 기본 영토·연결 확장·항공기·SND 잔여 분기

실선은 선택 또는 효과의 분기다. 점선은 정본 데이터·조건 조회다. 기본 영토와 지지도 예산을 쓰는 추가 영토는 서로 다른 규칙이다.

[![D17 · 선택과 자산 이전의 주요 분기](images/D17.dark.png)](images/D17.dark.svg)

<details>
<summary>Mermaid 편집 원본</summary>

```mermaid
---
config:
  theme: dark
---
flowchart TB
    Entry{"can_form 통과?"} -->|아니오| Stop["본문 미실행"]
    Entry -->|예| Snapshot["원국마다 p clamp 0–0.90<br/>candidate 수×p 예산 snapshot"]
    Snapshot --> Seed["597·743 중 후보 선택"]
    Seed --> SND["추가 적격 SND 소유 본토 전부 선택<br/>고립 영토·p0도 기본 영토"]
    SND --> Loop{"progress 양수이고 passes 남음?"}
    Loop -->|예| Reset["현재 pass 시작 / progress =0"]
    Reset --> More{"미선택 후보 / 예산1 이상<br/>선택 주와 인접?"}
    More -->|예| Select["selected·participant / 예산 -1<br/>sponsor progress =1"]
    More -->|아니오| Pass["현재 pass 종료 / passes -1"]
    Select --> Pass
    Pass --> Loop
    Loop -->|아니오 / 최대64회| Create["동적 정부·안전 거점·수도"]
    Create --> Air{"양수p 참여국의 배치 항공기 있음?"}
    Air -->|예| Base{"생성국 소유 air_base 있음?"}
    Base -->|아니오| Existing["선택·안전한 기존 기지 후보 순회<br/>기지가 없을 때 가능한 주 먼저 이전"]
    Existing --> AfterBase{"이후 소유 air_base 있음?"}
    AfterBase -->|아니오| Build["수도 air_base 1 즉시 건설"]
    AfterBase -->|예| Ratio
    Base -->|예| Ratio
    Build --> Ratio
    Air -->|아니오| Ratio{"참여 원국 p 양수?"}
    Ratio -->|예| Defect["같은 p로 병력·함대·항공·비축 귀순"]
    Ratio -->|아니오| Skip["귀순 명령 생략"]
    Defect --> Drain{"SND 잔여 모든 소유 주가<br/>selected이고 지금 이전 가능?"}
    Skip --> Drain
    Drain -->|예| Clear["SND 잔여 장비·연료·수송선 정리"]
    Drain -->|아니오| Keep["잔여 자산 보존"]
    Clear --> Rest["재검사 통과한 나머지 선택 주 이전"]
    Keep --> Rest
    Rest --> End["자치령·세력 / 임시 데이터 정리"]
    Mainland["포트 본토64주 / 제외20주 대응표"] -. 적격 후보의 지리 .-> Snapshot
```

</details>

- SND의 **소유 본토**만 기본 편입 후보이고, SND core만 있는 타국 영토를 자동 편입하지 않는다. 한국 보호·완전통제·일본 종속 제외 규칙은 SND에도 적용된다.
- 597·743은 candidate일 때 선택한다. 첫 이전은 597의 bootstrap 재검사 결과에 따라597 또는 대안743을 사용하며, 743에는 별도 재검사가 없다. p=0인 기본 영토 선택과 p=0인 전력 이전 생략을 구별한다.
- 연결 확장은 선택 표식에 대한 인접 검사와 원소유국 예산을 사용한다. 적격 SND의 고립 기본 영토도 연결 확장의 출발점이 될 수 있다.
- SND 잔여 정리는 귀순 뒤, 마지막 영토 이전 앞에서만 실행한다. 마지막 주를 먼저 이전하면 자동 승계가 끼어들 수 있다는 보호 계약이다. 다른 원국까지 잔여 정리를 확대하지 않는다.

정확한 본토·제외·seed·RT56 적응의 정본은 [기계 판독 대응표](../data/HOK_KOREAN_CHINESE_GOVERNMENT_RT56_MAPPING.json), [지리 기록](../implementation/2026-11-20-chinese-government-state-mapping.md), [선택 잠금](../../tools/hok_democratic_support_lock.json)이다. 이 도표의 64는 현 입력의 집합·반복 상한이며 미래 RT56 업데이트에도 자동 유효하다는 뜻이 아니다.

<a id="d18-character-lifecycle"></a>

## D18 · 전용 웡원하오의 정의·초기 모집·이동·승격·표시

실선은 정의·초기화·런타임 처리, 점선은 이름·초상화나 이전 scope 참조다. 동일한 역사 인물의 기존 CHI 토큰과 새 전용 토큰을 합치지 않는다.

[![D18 · 전용 인물의 상세 수명주기](images/D18.dark.png)](images/D18.dark.svg)

<details>
<summary>Mermaid 편집 원본</summary>

```mermaid
---
config:
  theme: dark
---
flowchart TB
    Definition["HOK_KCH_characters.txt<br/>HOK_KCH_weng_wenhao"] --> Role["country_leader / socialism<br/>expire1965 / id -1"]
    Definition --> History["KCH history recruit_character"]
    History --> Holder["전용 토큰을 보유한 Country"]
    Form["create_dynamic_country child<br/>original_tag KCH"] --> New["실제 생성국 / global event target 저장"]
    New --> Lookup["every_possible_country<br/>has_character HOK_KCH_weng_wenhao"]
    Holder --> Lookup
    Lookup --> Person["전용 Character scope"]
    Person --> Move["set_nationality PREV.PREV"]
    Person -. "PREV 보유국" .-> Holder
    Person -. "PREV.PREV 생성국" .-> New
    Move --> Promote["생성국 promote_character<br/>character 토큰 / ideology socialism"]
    Role -. 지도자 역할 정의 .-> Promote
    Promote --> Runtime["생성국 지도자 역할과 저장 상태"]
    Definition -. name .-> Name["CHI_weng_wenhao 표시 키"]
    Definition -. civilian large .-> Sprite["GFX_portrait_chi_weng_wenhao"]
    Name --> Display["활성 언어·RT56/바닐라 공급자 조회"]
    Sprite --> Display
    Old["기존 CHI 인물 토큰"] -. "별도 정의 / 이 helper가 옮기지 않음" .-> Definition
```

</details>

근거: [전용 인물](../../common/characters/HOK_KCH_characters.txt), [KCH 이력](<../../history/countries/KCH - Korean China.txt>), 출범 효과. `id=-1`은 정의에 있는 값이며 저장의 실제 숫자 캐릭터 ID를 약속하지 않는다. 이름·portrait sprite의 실제 공급자와 활성 덮어쓰기는 [표시 경로](presentation-assets.md)를 따른다. 기존 CHI 인물, 동적 국가 태그, 캐릭터 표시 이름을 동일한 식별자로 취급하지 않는다.

기출범 저장의 지도자를 자동 교체하거나 history를 소급 재실행하는 새 처리는 이 상세화에 없다. 새 모집·국적 이동·승격·표시·저장 복원을 각각 구분한다. 일본 비맹주 초대의 `PREV.PREV`는 이 인물 이동과 다른 호출 사슬이며 [D04](domain-model.md#d04-scope-context)를 따른다.

## 처리·증거·갱신 계약

| 후보 | 처리 | 현재 설명과 확인 경계 |
|---|---|---|
| D15 호출·공유 조건 | **문서 수정** | 중점 가용·helper 재검사·공통 core·후속 인정·별도 전쟁목표를 분리했다. |
| D16/D17 순서·분기 | **문서 수정** | 이관 전 snapshot, 기본/추가 영토, 공군기지 대안, 양수p 귀순, SND 잔여 정리, 마지막 영토 이전·정리까지 연결했다. |
| D18 인물 | **문서 수정** | 초기 정의·모집, 현재 보유국 조회, Character scope 이동과 생성국 승격을 분리했다. |
| 본토64·seed597/743·보호 규칙·p·stable ID·원국 지휘관 유지 | **의도적 유지** | 실제 포트 입력과 코드의 현재 계약을 설명한다. 새 지리·비율·DLC·자치 등급을 설계하지 않는다. |
| 원본63주 숫자 복사·CHI 기존 지도자 이동·동적 태그 고정·다른 원국 잔여 정리 | **제외** | 현재 소스와 포트 지리·인물·소유권 계약에 해당하지 않는다. |
| 엔진의 세부 자산 배분·소멸·모든 세력/전쟁/DLC 조합·기존 저장 | **미확인 또는 기존 실행 범위** | 소스와 그림만으로 보증하지 않는다. 아래 실제 실행 기록의 구성과 한정된 결과를 유지한다. |

[전체 이식 기록](../implementation/2026-11-20-korean-democratic-support-intelligence-port.md)은 CHI 경계값, 0%/양수 귀순, 보호 영토, 새 저장, 일본 비맹주 실패와 수선 후 결과, 중국 비맹주 사례 및 남은 미검증을 분리한다. 과거 원본 실행, 강제 효과, 정상 진행, 소스 읽기, 이번 그림 렌더링을 서로 합산하지 않는다. 호출·보호·선택·자산·인물 관계가 바뀌면 D15–18과 S07–09의 관련 정본을 함께 갱신한다.
