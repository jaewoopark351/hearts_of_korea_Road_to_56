# 한국 민주인사 지원과 비밀 정보국 확장 계획·구현

> 2026-11-19 민슈 잇키의 인간 일본 허용 — **코드 적용·소스 확인 / 실제 UI·내전·저장·멀티플레이 미검증**: 한국 중점 `KOR_minshu_ikki`의 일본 AI 전용 조건만 제거했다. 기존 한국 민주주의·독립국, 일본 비민주주의, 선행·35일·보상은 유지한다. 변경·검증 전에는 [현행 계약 24절](#24-minshu-ikki-player-japan)을 읽는다.

> 2026-11-19 중국 독재자 축출 조건·기간 — **코드 적용·소스 확인 / 실제 UI·진행·저장 미실행**: 실존하는 중국 `CHI`의 민주주의 지지도 **50% 이상(정확히 50% 포함)**을 중점 가용 조건과 생성 직전 guard에 공유하고, `cost = 10`으로 기본 **70일**을 적용했다. 다른 국가의 지지도 합산이나 현재 중국 대표국 지지도로 대체하지 않는다. 자치령·영토·전력·지도자 보상은 유지한다. 이후 변경·검증은 [최신 계약 23절](#23-shandong-focus-chi-support-and-duration)을 먼저 읽으며, 아래 35일 실행·자치령 전환 당시 소스 확인은 이번 새 조건/기간의 실행 증거가 아니다.

> 2026-11-19 산둥 자치령 전환 — **코드 적용·소스 확인 / 새 게임 실행·UI·저장 미실행**: 「중국 독재자 축출」로 생성되는 산둥 자유 공화국을 한국의 `autonomy_dominion`으로 설정한다. 원본 자치령의 `Together for Victory` 조건에 맞춰 중점·helper·안내를 함께 바꾸고, 영토·전력·지도자·전쟁·세력·후속 인정은 유지한다. 이 기능을 변경하거나 검증하기 전에는 [최신 계약 22절](#22-shandong-dominion-implementation)을 읽는다. 아래 17·19·21절의 피감독국 실행 관측은 전환 전 이력이며 이번 자치령의 런타임 통과가 아니다.

> 2026-11-19 산둥 지도자 웡원하오 — **구현·DLC 양분기 지연 출범·한국어 UI·새 저장 왕복 확인**: 설명·문서화 뒤 사용자가 별도로 구현을 승인했다. 산둥 전용 인물을 모집·승격하고 원본 이름·본체 초상화·예전 민주주의 역할을 재사용한다. 중국 원본 인물과 산둥의 나머지 출범 규칙은 유지한다. 이 기능을 변경하거나 검증하기 전에는 [현행 구현 21절](#21-shandong-weng-wenhao-leader-implementation)과 [실행 기록](incidents/2026-11-19-shandong-weng-wenhao.md)을 읽는다. [20절](#20-shandong-weng-wenhao-leader-design)은 초기 문서화 이력이며 아래 이전 실행은 이번 지도자 검증으로 재사용하지 않는다.

> 2026-11-19 산둥군벌 영토 기본 편입 — **구현·핵심 엔진·실제 중점 UI·새 저장 왕복 확인**: 후속 구현 승인을 받아 기존 본토·보호 조건을 통과한 SND 소유 주 전부를 지지도와 무관한 기본 영토로 선택한다. 기존 597·743 거점과 타국의 연결 영토·전력 지지도 규칙을 유지한다. 같은 최종 소스의 production 5사례와 실제 중점 완료·원래 모드 구성의 새 저장 재로드/추가 진행을 확인했다. 이 기능을 변경하거나 검증하기 전에는 [현행 계약 19절](#19-shandong-warlord-integration-implementation), [이번 구현·검증 기록](incidents/2026-11-19-shandong-full-integration.md), [지리·출처 목록](data/HOK_KOREAN_CHINESE_GOVERNMENT_STATE_GROUPS.json)을 먼저 읽는다. 17절의 이전 실행과 18절의 문서화 이력은 이번 검증 결과가 아니다.

> 2026-11-19 산둥군벌 영토 기본 편입안의 초기 문서화 이력 — **당시 코드 미반영·후속 구현은 19절**: 산둥 자유 공화국 출범 시 SND 소유 영토를 지지도와 무관한 기본 편입 대상으로 삼고, 기존 칭다오 거점과 다른 중국 국가·병력의 지지도 규칙 및 영토 보호를 유지하는 방향을 기록했다. 최초 논의·미정 범위를 검토할 때 [18절](#18-shandong-warlord-integration-design)을 읽고 이후 19절의 결정과 구분한다.

> 2026-11-19 산둥 정부 구현 — **구현·핵심 엔진·실제 UI·새 저장 재로드 확인**: 사용자가 초기 설명·문서화 뒤 별도로 전체 구현을 승인했다. 중국 본토 63주 핵심주, 보호된 산둥 거점과 연결 영토, 지지도에 따른 실제 육해공군·비축 귀순, 한국 피감독국 출범을 적용했다. 한국의 기존 전쟁명분을 유지하고 자동 선전포고·별도 공동 참전은 추가하지 않았다. 이 기능을 변경하거나 검증할 때 [현행 구현 계약 17절](#17-shandong-government-implementation), [지리 범위·출처 목록](data/HOK_KOREAN_CHINESE_GOVERNMENT_STATE_GROUPS.json), [구현·실행 기록](incidents/2026-11-19-shandong-democratic-government.md)을 먼저 읽는다. 아래 16절은 구현 전 문서화 이력이며 이전 14절의 실행 통과를 이번 검증으로 재사용하지 않는다.

> 2026-11-19 산둥 자유 공화국 후속 설계의 초기 문서화 이력 — **당시 미구현·후속 구현은 17절**: 출범 시 중국 본토 핵심주를 가진 한국 피감독국으로 설정하고, 민주주의 지지도에 따라 초기 영토·병력을 늘리는 방향을 기록했다. 추가 영토는 산둥 거점과 육지로 연결되는 중국 지역에서 고르며, **일본 측 소유·점령지와 만주 지역은 제외하고 한국이 소유하거나 통제하는 주는 이전하지 않는다**. 정확한 핵심주 범위와 배분 방식은 미정이다. 기존 한국의 중국·군벌 대상 전쟁명분을 유지하며 **자동 선전포고·별도 공동 참전 처리는 추가하지 않는다**. 이 후속 설계를 검토하거나 구현하기 전에는 [16절의 확정·미정 범위](#16-shandong-democratic-government-design)를 먼저 읽는다. 아래 기존 구현·실행 결과는 이 설계의 적용·검증 증거가 아니다.

> 2026-11-19 중국 군벌 대상 확장: 중국 지원·축출을 16태그로 정렬했고 동적 국가 배제 guard를 추가했다. 최종 소스 39확인/0·독립 소스 34/0, 최종 소스의 합성 native 3사례는 69 PASS/0 FAIL이다. 실제 UI·구 저장 재로드는 미검증이며 이어하기 인덱스 `continue_game.temp`의 원본 바이트 미보존·미복원 한계가 남는다. 단계별 증거와 복원 범위는 14절을 따른다.

> 2026-11-19 최신 수치 변경: 비밀 정보국의 이념 지지 임무만 +100%, 선전을 포함한 나머지 기존 +75% 여섯 보정은 +25%로 재조정했다. 현행 수치는 5절, 변경 범위·소스 확인과 미검증 항목은 13절을 따른다.

최초 작성·구현: 2026-11-18, 후속 갱신: **2026-11-19 (Asia/Seoul)**. 중국 16태그 확장 당시 상태: **중국 16태그 확장·핵심 합성 엔진 검증·최소/원래 구성 로드 확인 / 실제 UI·구 저장 재로드 미검증·이어하기 인덱스 복원 예외**. 소스 39확인/0·독립 소스 34/0·native 69/0·저장 판독 34/0은 각각 범위가 달라 합산하지 않는다. 보완 전 36/0·33/0과 none-clone 4FAIL은 14절의 이전 단계 이력이다. 정보국 재무장 선행 이관의 27확인/0은 11절, 두 봉기 중점의 맹주 조건 제거 12확인/0은 12절, 임무 수치 재조정은 13절을 따른다. 앞선 B8·762d·c212도 현재 중국 확장의 실행 결과로 재사용하지 않는다.

중국·일본 민주인사 지원의 진입을 「아시아 민주주의의 선봉」으로 옮겼고, 각 정치력 25로 180일 동안 일일 민주주의 성장 +0.10을 지원하는 반복 결정을 열었다. 「민슈 잇키」는 일본 민주주의 지지도에 비례하는 10~90% 분할값을 사용한다. 「비밀 정보국 확장」은 후속 요청에 따라 「재무장 시작」을 선행으로 삼는 공통 군사·정보 중점으로 옮겼다. 영국 원본 시각 자산의 내부 사본은 그대로 유지한다.

2026-11-18의 전체 구현 승인 단계에서 게임 코드·paired 현지화·시각 자산과 배치를 반영했다. 앞선 설명 전용·문서화 전용 단계에서는 코드 수정이나 검사를 하지 않았으며, 그 당시의 범위와 결과는 10절과 14절에 구분해 보존한다. 중국 16태그 확장은 그 뒤 별도 구현 승인을 받은 후속 범위다. 이 기록은 커밋·푸시·배포 승인이 아니다.

## 1. 기준 소스와 필수 자료

| 구분 | 2026-11-18 기준과 역할 |
|---|---|
| 작업 소스 | `C:\hoi\hearts_of_korea`; 권위 있는 개발 소스 |
| Git | `feat/korean-focus-expansion-ai`, 시작 HEAD `0c19f58fa7a9ff898196dcdbe46edfd0ad5fdbbc`; 최초 문서화 시작 시 clean, 구현 시작 시 앞서 작성한 Markdown 3개 변경 존재 |
| 설치 원본 V | `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV`; 읽기 전용 참고 |
| 설치 버전 | V의 `launcher-settings.json`: `Operation Postern v1.19.5.0.7c6c (c184)`; 런타임 버전·체크섬·DLC 구성은 구현 기록에서 별도로 확인 |
| descriptor | `supported_version="1.19.*"`, 의존성 `Korean Language`, successor `remote_file_id="3793992662"`; 변경하지 않음 |
| launcher 개발 모드 | 실제 사용자 데이터의 `mod/hearts of korea.mod`가 `C:/hoi/hearts_of_korea`를 직접 참조 |
| 실제 사용자 데이터 | `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV`; 게임이 만든 원본 저장·로그 위치 |
| 최초 문서화 시 활성 순서 | `dlc_load.json`: 저장소 → `Hearts of Korea English Translation Anime Modder's Edition`; 이후 테스트 선택·원복은 구현 기록 참조 |
| 영어 번역 | `C:\hoi\Hearts of Korea English Translation Anime Modder's Edition`; 이번에 수정하지 않음 |
| 언어·DLC | 현재 한국어 채널 `l_korean`; 설정의 `disabled_dlcs` 빈 배열과 실제 소유·활성·`has_dlc` 판정은 구분 |
| 외부 작업·증거 | `C:\hoi\test\hok-democratic-support-intelligence-20261118-01\`; helper·백업·검사·미리보기·실행 증거는 이 경로 아래 |

이 기능을 변경하거나 검증할 때 [변경 영향 검토 절차](HOK_CHANGE_COVERAGE_REVIEW.md), [현지화 검토 스킬](../.agents/skills/hok-localisation-review/SKILL.md), [주 참조 검토 스킬](../.agents/skills/hok-state-reference-review/SKILL.md)을 먼저 읽는다. 지원의 해금·운영 안내와 일본 내전의 대상 범위·분할을 함께 추적하기 위해 필요하다. 실제 실행 로그를 판정할 때는 [로그 검토 스킬](../.agents/skills/hok-log-review/SKILL.md)을 추가로 적용한다.

배치 변경 전에는 [배치 계획](HOK_KOREAN_FOCUS_LAYOUT_PLAN.md), [좌표 명세](HOK_KOREAN_FOCUS_LAYOUT_COORDINATES.md), [민주 압축 기록](HOK_KOREAN_DEMOCRATIC_FOCUS_COMPACTION_PLAN.md), [초기 압축 사건](incidents/2026-09-21-korean-focus-compact.md)을 읽는다. 보상은 [보상 기준](HOK_KOREAN_FOCUS_REWARD_GUIDELINES.md), 본문 두 채널은 [현지화 계약](incidents/2026-09-01-localisation-contract.md)을 따른다.

일본 내전의 범위를 바꿀 때는 [중국·일본 지도 정렬 정책](CHINA_JAPAN_VANILLA_ALIGNMENT_POLICY.md)과 [일본 민주 분기 통합 계획](HOK_JAPAN_DEMOCRATIC_BRANCH_INTEGRATION_PLAN.md)을 읽는다. 그 문서들의 과거 1.19.2 결과를 이번 1.19.5 기능의 검증으로 옮기지 않는다.

## 2. 선행과 배타 관계

구현한 진행은 다음과 같다. 지원을 건너뛰어 후속을 선봉에 직접 붙이지 않았다.

```text
아시아 민주주의의 선봉
├─ 중국 민주인사 지원 → 중국 독재자 축출
└─ 일본 민주인사 지원 → 민슈 잇키

재무장 시작
└─ 비밀 정보국 확장
```

| 대상 | 변경 전 기준선(시작 HEAD의 korea.txt 행) | 반영 내용 |
|---|---|---|
| `KOR_support_for_democracy_in_china` | 6957·6973–6976 | 선행을 `KOR_founding_of_the_asian_union`에서 `KOR_the_vanguard_of_asian_democracy`로 교체 |
| `KOR_support_for_democracy_in_japan` | 7144·7165–7168 | 같은 선행 교체 |
| 중국 초대 ↔ 중국 지원 | 6946·6976 | 양쪽 `mutually_exclusive` 선언 2곳 제거 |
| 일본 초대 ↔ 일본 지원 | 7133·7168 | 양쪽 선언 2곳 제거 |
| 중국 독재자 축출 | 7028·7050–7052 | 최초 단계는 중국 지원 선행·효과를 유지하며 부모 이동에 따라 배치 이동; 후속 16태그 전쟁명분 확장은 14절 |
| 민슈 잇키 | 7184·7206–7208 | 일본 지원 선행 유지; 내전 실행을 지지도 연동 helper로 연결 |

현재 정의는 [korea.txt](../common/national_focus/korea.txt)의 해당 ID를 기준으로 찾는다. 최초 11월 18일에 직접 바꾼 기존 중점 블록은 지원 2개·초대 2개·민슈 잇키의 **5개**, 새 정보국 중점은 **1개**다. 이후 중국 축출의 맹주 조건·전쟁명분 대상 변경은 12절·14절의 별도 범위다. 중국·일본 초대의 선행은 아시아 연합 창설이고, 「유럽의 해방」↔「아시아 연합 창설」 배타도 유지했다. 기존 중점 ID·기간·AI 가중치는 유지한다.

지원 중점에는 한국의 민주주의 정부·독립국 조건이 있고 일본 지원에는 일본의 비민주주의 조건이 있다. 후속 두 중점의 한국 민주주의·독립국 조건은 유지하며, 11월 19일 먼저 한국의 세력 맹주 조건을 제거했다. 중국 독재자 축출의 현행 추가 조건·70일 기간은 [23절](#23-shandong-focus-chi-support-and-duration)을 따른다. 민슈 잇키는 일본 비민주주의 조건을 유지하고, [24절 후속 변경](#24-minshu-ikki-player-japan)에서 일본 AI 전용 조건을 제거했다. 일본이 사람이어도 한국에서 선택할 수 있으며 기존 보상 효과는 유지한다.

## 3. 중국·일본 지원 결정과 기존 저장

두 지원 중점의 완료 효과는 각 결정의 해금 안내다. 실제 지원은 [지원 결정](../common/decisions/HOK_KOR_democratic_support.txt)에서 시작하며, [공유 범주](../common/decisions/categories/HOK_KOR_democratic_support.txt)는 어느 한 지원 중점을 완료하면 표시된다.

| 항목 | 일본 | 중국 |
|---|---|---|
| 결정 ID | `HOK_KOR_support_democracy_in_japan` | `HOK_KOR_support_democracy_in_china` |
| 실행국·비용 | 한국, 1회 정치력 25 | 한국, 전체 묶음 1회 정치력 25 |
| 대상 | 현존 JAP | 현존 CHI·PRC·SHX·GXC·YUN·XSM·SIK·GDC·SND·SIC·NXM·GSM·XIC·KHM·KUM·HBC |
| 효과·기간 | `KOR_democrat_sponsored_by_korea` 180일; 일일 민주주의 성장 +0.10 | 같은 정신·기간·효과를 현존 지정 대상 각각에 지급 |
| 반복 | 180일 종료 후 재사용, 별도 추가 대기 0일 | 같은 규칙 |
| 기존 지원 차단 | JAP에 같은 정신이 있으면 시작 불가 | 현존 지정 대상 중 하나라도 같은 정신이 있으면 묶음 전체 시작 불가 |

중국의 대상 계약은 CHI·PRC와 설치본 일반 군벌 14개를 합한 **고정 16태그이며 동적 내전국은 제외**한다. 실제 실행에서 현존 여부와 `tag` 검사만으로는 원본 소멸 뒤의 동적 국가를 배제하지 못해 `is_dynamic_country = no`를 추가했다. 보완 전 실패·보완 후 검증은 14절을 따른다. 신규 군벌 8개와 후속 KUM을 포함하며, 지원이 시작된 뒤 새로 등장한 나라에는 소급 지급하지 않고 다음 지원 실행에서 포함한다.

정치력 25와 성장 +0.10은 사용자 지정값이다. 180일은 최초 포르투갈 사례 참고 제안에서 출발하여 전체 구현 때 채택한 작업값이다. +0.10은 성장 보정이며 즉시 지지율 +10%p가 아니다. 별도 일일 유지비·안정도 손실·중일 지원 상호배타를 추가하지 않았다.

변경 전 두 중점은 공유 정신을 각각 280일 자동 지급했다(시작 HEAD [korea.txt](../common/national_focus/korea.txt) 6982–7021·7173–7178행). 이를 **정치력 25·180일의 반복 결정**으로 옮겼다. 공유 정의 [ideas/korea.txt](../common/ideas/korea.txt) 428–437행의 `democratic_drift = 0.1`은 그대로이며 별도 +0.10 정신을 중첩하지 않는다.

실행에는 한국의 민주주의·독립국 조건이 필요하다. 중국은 적어도 한 지정 대상이 존재해야 하며 소멸국은 건너뛴다. 유효 대상이 하나도 없을 때 비용만 낼 수 없고, 소멸국을 부활시키거나 KCH·MON 등 새 대상을 추가하지 않는다. 일본도 JAP 존재가 필요하다.

시작된 지원은 정권·외교관계가 바뀌어도 기존 정신의 잔여 기간을 유지한다. 별도 취소·환불·조기 회수·사후 민주정 검사나 매일 발동하는 on_action을 넣지 않았다. 나라가 소멸할 때 정신이 처리되는 엔진 동작까지 새로 보장하지 않는다.

기존 저장에서 두 중점의 완료 이력이 있으면 새 결정은 그 조건으로 자동 표시된다. 남아 있는 280일 지원은 줄이거나 연장하지 않는다. 그 정신이 끝날 때까지 재지원이 차단되며, 중국은 일부 대상 하나만 구 지원을 보유해도 새 묶음 전체가 기다린다. 지원 여부와 타이머의 새 플래그·저장 변수 이관을 만들지 않았다. 이 저장 정책의 소스 반영과 실제 변경 전 저장의 장기 재로드 검증은 구분한다.

공유 정신을 쓰는 태국 압박(시작 HEAD의 중점 파일 6691–6697행, SIA 280일)과 [events/korea.txt](../events/korea.txt)의 `kor_events.62`–`.65`(VIN·MAL·PHI·INS 각각 720일)는 보존했다. 공유 정의의 전역 변경은 이번 범위가 아니다.

참고 원본은 V의 `common/decisions/POR.txt` 2386행 `POR_stir_monarchist_sentiment_in_brazil`이다. 정치력 25·반복은 2410–2411행, 포르투갈의 180일 지원은 2437–2440행, 브라질 대상 임무의 `neutrality_drift = 0.1`·180일은 2483–2488행이다. 원본은 대상국 임무 방식이며 이번 구현은 기존 공유 기간제 국민정신을 재사용한다. 포르투갈의 일일 정치력 −0.5·브라질 주간 안정도 −0.01·전쟁 취소 조건을 복사하지 않았다.

## 4. 민슈 잇키의 지지도 연동

[일본 봉기 helper](../common/scripted_effects/HOK_KOR_democratic_intelligence_effects.txt)의 `HOK_KOR_japanese_democratic_uprising`은 **JAP 국가 scope**에서 실행한다. 실행 직전 `party_popularity@democratic`를 임시 변수 `HOK_KOR_japanese_democratic_revolt_share`로 읽고 다음 값으로 제한한다.

```text
p = 봉기 직전 일본 민주주의 지지도(0~1)
s = min(0.90, max(0.10, p))
size = army_ratio = navy_ratio = air_ratio = s
```

지지도 30%는 분할 기준 30%, 60%는 60%이며 10% 미만·90% 초과에서는 각각 10%·90%를 사용한다. `size`가 비축 물자 분할에도 사용되고 육군·해군·공군 비율은 각각 명시한다. 임시 변수를 영구 저장 변수로 남기지 않는다. 이번에 적용한 것은 이 입력값과 기존 개입 순서이며, 실제 엔진 분할이 각 항목을 어떻게 반올림하는지는 실행 증거로 따로 확인해야 한다.

`start_civil_war` 안에서 기존 `KJP_democratic` 외형·일반 중점 트리, 생성국의 한국 세력 편입, 한국 자동 참전을 순서대로 유지했다. 고정 주 목록·`states_filter`·추가 주 이전·코어·지도 수정은 넣지 않고 엔진의 자동 주 분할을 사용한다. 따라서 분할값 60%가 면적·인구·공장 각각의 정확한 60%나 특정 본토·항구 보유를 보장하지 않는다. 소유·통제 차이와 해외 영토 등은 엔진 실제 결과의 검증 항목이다.

V의 `documentation/effects_documentation.md` 8030–8059행은 `size`·병종별 비율·`states`·`states_filter`를 설명한다. `common/scripted_effects/NOR_scripted_effects.txt` 917–927행에는 지지도를 `size`로 쓰는 사례가 있고, 지지도 조회 범위는 `documentation/dynamic_variables_documentation.md` 722–726행을 참고했다. 변경 전 민슈 잇키가 분할 수치를 생략했을 때의 기본 동작을 지지도와 무관했다고 단정하지 않는다.

이 지지도 분할 변경은 일본에 한정한다. 중국 독재자 축출의 KCH 생성·영토 이전·`KOR_New_China_Government` 안내와 [기존 결정](../common/decisions/KOR_decision.txt)의 해금 조건은 보존했다. 중국의 전쟁명분 대상은 별도 후속 범위인 14절에서 16태그로 확장한다.

## 5. 비밀 정보국 확장

중점 `HOK_KOR_expand_secret_intelligence_service`는 현재 **「재무장 시작」(`KOR_begin_rearmament`)**을 직접 선행·상대 위치 기준으로 한다. 기준점 기본 (54,0)에 상대 (8,1)을 더한 **(62,1)**이며, 기존 공통 군사 사슬에는 정치 offset이 없어 SHOW·초기 HIDE·어느 정치 노선 완료 HIDE에서도 같은 위치를 유지한다. 이념에 따른 완료·숨김 조건은 제거하고 **`La Resistance` 보유 조건만** 유지한다. 실제 착수에는 재무장 시작 완료와 기존 항복 관련 조건이 여전히 적용된다.

**cost 5(기본 35일), AI 가중치 1, 보상 15값과 sprite·DDS는 유지**한다. 완료 때 정보기관이 없으면 설립하고, 기존 기관이 있으면 그대로 사용하며, [영구 국민정신](../common/ideas/HOK_KOR_democratic_intelligence.txt) `HOK_KOR_secret_intelligence_service_idea`(「비밀 정보국」)를 지급한다.

[한국 역사 AI 계획](../common/ai_strategy_plans/KOR_historical_strategy_plan.txt)의 정보국 항목도 독립당 직후에서 **재무장 시작 직후**로 이동했다. 다른 항목의 상대 순서·가중치·계획은 보존한다. 본문 paired 현지화는 정보국 중점 설명 한 키의 말미만 해외 정보망의 안정적인 운영이라는 공통 취지로 고쳤고 이름·효과 수치·다른 키는 유지했다. 현재 AI 경로의 실제 선택·35일 진행은 게임을 실행하지 않아 미검증이다.

원래의 독립당 선행·(120,6)/(85,6) 배치·민주 HIDE guard와 그 AI 목록에 대한 검증은 9절에 보존한다. 그 guard는 이번 후속 이관에서 제거했으며 현재 규칙으로 읽지 않는다.

| 요구 효과 | 새 정신 자체의 값 | 반영 키 |
|---|---|---|
| 요원 슬롯 | +2 | `operative_slot = 2` |
| 정보망 강도 획득량 | 고정 +10 | `intel_network_gain = 10` |
| 정보망 획득 계수 | +25% | `intel_network_gain_factor = 0.25` |
| 작전 속도 | +35% 목표 | `intelligence_operation_speed = 0.35`; 국가 보정 조회·저장 확인, 실제 속도 계산 미확인 |
| 작전 비용·위험도 | 각각 −35% | `operation_cost = -0.35`, `operation_risk = -0.35` |
| 작전 결과 | +25% | `operation_outcome = 0.25` |
| 아군 요원 피탐지 계수 | −35% | `own_operative_detection_chance_factor = -0.35` |
| 저항 소탕 | +25% | `root_out_resistance_effectiveness_factor = 0.25` |
| 사보타주·저항 강화 | 각각 +25% | `target_sabotage_factor = 0.25`, `boost_resistance_factor = 0.25` |
| 선전 | +25% | `propaganda_mission_factor = 0.25` |
| 이념 지지·성장 | +100% | `boost_ideology_mission_factor = 1.00` |
| 무역 지배·외교 압력 | 각각 +25% | `control_trade_mission_factor = 0.25`, `diplomatic_pressure_mission_factor = 0.25` |

위 표는 11월 19일 최종 사용자 요청에 따른 국민정신 자체의 최종값이다. 후속 요청으로 정보망 강도 획득의 고정값을 +25에서 **+10**으로 낮췄으며 별도 획득 계수 **+25%**는 유지했다. 고정값과 계수는 서로 다른 보정이다. 기존 고문·기관 업그레이드 등의 별도 효과는 별도 합산이며 위 표가 국가 전체 합계는 아니다. 이번 고정값 변경은 15절을 따른다.

작전 결과는 효율 보정으로 성공률 +25%p를 보장하지 않는다. 사보타주·저항 강화는 관련 작전 효율이며 모든 효과가 같은 종류의 상시 요원 임무는 아니다. 속도 키는 V의 `documentation/modifiers_documentation.md` 2977행에 있고, 초기 엔진 진단에서 국가 보정 0.35의 조회·저장을 확인했다. 실제 작전 소요일수·속도 계산은 미확인이다. **등록된 0.35의 조회·저장을 속도 검증 완료로 취급하거나 시간 −35%로 치환하지 않는다.**

요원 +2의 바닐라 사례는 `common/ideas/argentina.txt` 574행, 정보망 계수 +25%는 `common/ideas/SOV.txt` 971행이다. 일곱 임무·작전 효율 키는 `common/intelligence_agency_upgrades/intelligence_agency_upgrades.txt` 151·249–250·367–368·389–390행의 +0.25 사례를 참고했다.

영국 참고 원본은 `common/national_focus/uk.txt` 315–351행의 `ENG_expand_the_secret_intelligence_service_focus`다. 기관 자동 설립·영구 보상·DLC 표시 조건은 처음 설명 때의 참고안을 이번 구현에서 채택한 것이며 사용자 지정 수치의 출처와 구분한다. 영국의 요원 +1·안정도 등 보상을 별도로 복제하지 않았고 미보유 DLC의 대체 보상을 만들지 않았다.

## 6. 내부 시각 자산과 출처

영국 원화와 기존 소형 시민 아이콘 **6개를 바이트 그대로 프로젝트 내부에 복사**했다. 새 원화·AI 이미지·전체 재색칠·리샘플링을 만들지 않았다. 원본·프로젝트 사본·원저자·사용 근거·해시·마스크/오버레이 전체 사슬은 [자산 크레딧](HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_ASSET_CREDITS.md)과 [자산 매니페스트](data/HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_ASSET_MANIFEST.json)에 있다.

| 용도 | 원본·기존 파일 | 현재 내부 사본·참조 |
|---|---|---|
| 정보국 눈 문양 | V `gfx/interface/goals/focus_generic_secret_service_agency.dds` | `gfx/interface/goals/HOK_KOR/democratic_intelligence/secret_intelligence_service.dds`; `GFX_HOK_KOR_focus_secret_intelligence_service`; 원본 100×88 |
| 중점 광택 | V `gfx/interface/goals/shine_overlay.dds` | 같은 내부 폴더 `shine_overlay.dds`; 원본 87×88, 마스크는 내부 중점 DDS |
| 국민정신 | V `gfx/interface/ideas/generic_spy_intel.dds` | `gfx/interface/ideas/HOK_KOR/democratic_intelligence/secret_intelligence_service.dds`; `picture = HOK_KOR_secret_intelligence_service`; 원본 58×63 |
| 중국·일본 결정 행 | 기존 `gfx/interface/decisions/HOK_KOR/civic/influence_blue.dds` | `gfx/interface/decisions/HOK_KOR/democratic_support/support_democracy_in_china.dds`·`support_democracy_in_japan.dds`; 각 32×32 |
| 결정 범주 | 기존 `gfx/interface/decisions/HOK_KOR/civic/category.dds` | 같은 새 폴더 `category.dds`; 51×40 |

[일반 GFX](../interface/HOK_KOR_democratic_support_intelligence.gfx)·[광택 GFX](../interface/HOK_KOR_democratic_support_intelligence_shine.gfx)는 프로젝트 전용 이름과 내부 상대경로를 사용한다. 바닐라 전역 sprite를 덮어쓰지 않는다. 영국 원본의 `interface/goals.gfx` 3399–3400행, `interface/goals_shine.gfx` 21686행 이후, `common/ideas/britain.txt` 675–678행과 `interface/ideas.gfx` 673–674행의 출처 사슬을 기록했다.

사용자가 선정한 영국 눈 문양·MI6 그림을 그대로 보존하는 범위로 새 배경 색 가공은 하지 않았다. 이번 공통 군사 가지 이관에서도 이미지·sprite·마스크·광택 파일은 바꾸지 않았다. 결정 행은 기존 민주 파랑 RGB(53,91,126)의 저울을 공유하며, 범주는 기존 시민 헤더의 산업 회색을 유지한다. 기존 두 지원 중점의 원화는 교체하지 않는다. Paradox 원화와 Globvs / Ultimate HOI4 GFX 기여자의 원화를 계속개발 팀의 신규 창작으로 표시하지 않는다.

이미지 변경 전에는 [제작 방침](HOK_KOREAN_FOCUS_SPIRIT_ICON_PLAN.md), [색상 기준](HOK_KOREAN_FOCUS_ICON_COLOR_PLAN.md), [소형 결정 수리 기록](incidents/2026-09-22-korean-decision-icon-size.md), [개발 자료 보관 안내](HOK_DEVELOPMENT_ARTIFACT_ARCHIVE.md)를 먼저 읽는다. 이번 원본은 현재 설치본과 기존 프로젝트 완성본이며, 확인되지 않은 과거 외부 archive를 다시 찾거나 재실행했다고 기록하지 않는다.

## 7. 표시와 배치

지원 중점 두 개에 각각 `unlock_decision_tooltip`으로 해당 지원 결정의 해금을 표시한다. 실제 결정은 비용 25·180일·대상·+0.10·중복 차단·재사용·취소/환불 없음의 안내를 제공한다. 범주 전체 해금과 개별 결정 해금을 혼동하지 않는다.

본문 `localisation/korean/`·`localisation/english/`의 한국어 본문 계약과 UTF-8 BOM을 유지했다. 최초 구현에서 기존 지원·중국 축출·민슈 설명 4키와 민슈 효과 툴팁 1키를 변경하고 지원·정보국 paired 파일을 추가했다. 이번 재무장 이관에서는 정보국 중점 설명 한 키의 말미만 두 파일에서 동일하게 바꿨으며 BOM·기존 LF 줄 끝을 보존했다. 활성 영어 번역에는 신규 정보국 focus/idea 키가 없어 이번 설명을 덮어쓰지 않으며, 부모 `KOR_begin_rearmament`는 외부 English 파일의 「Begin Rearmament」와 본체 Korean의 「재무장 시작」으로 대응한다. 외부 번역은 수정하지 않았다. 현재 `l_korean`은 별도 한국어 채널을 사용하지만, 영어 채널에서는 기존 **5키가 낡은 영어 지원·봉기 설명/효과로 덮어쓰는 경로**가 범위 밖 미해결 항목으로 남는다. 한국어 소스 확인을 실제 UI나 활성 영어 채널의 검증으로 확대하지 않는다.

진행 선행과 `relative_position_id`를 함께 조정했다. 현재 **475개·절대 기준 7개·상대 배치 468개**, 직접 offset 7개와 전체 기본 범위 x0~211/y0~24·지속적 패널·바로가기는 유지한다. 이번 배치 차이는 [부분 좌표 delta](data/HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_LAYOUT.json)에 기록하며 전체 475개 스냅샷으로 표시하지 않는다.

| 중점 | 위치 기준·상대 x/y | 기본/SHOW·초기 HIDE | 민주 완료 HIDE |
|---|---|---|---|
| 중국 민주인사 지원 | 선봉 (116,6), (−6,1) | (110,7) | (75,7) |
| 중국 독재자 축출 | 중국 지원, (0,2) | (110,9) | (75,9) |
| 일본 민주인사 지원 | 선봉 (116,6), (−3,1) | (113,7) | (78,7) |
| 민슈 잇키 | 일본 지원, (0,2) | (113,9) | (78,9) |
| 비밀 정보국 확장 | 재무장 시작 (54,0), (8,1) | (62,1) | (62,1) |

중국·일본의 네 지원/후속 노드만 기존 `KOR_democracy_advance_forward` 소유의 −35x를 한 번 상속한다. 정보국은 `KOR_begin_rearmament`의 공통 군사 사슬로 옮겨 정치 offset을 상속하지 않으며 새 직접 offset도 없다. 민주 기본 범위는 x110~151/y2~24, 민주 완료 HIDE는 x75~116/y2~24다. 이번 (62,1) 정보국의 최소 사각형 모델 충돌 0·후손 없음·다른 474개 좌표 불변이라는 소스 결과와 실제 이름판·선·클릭·SHOW/HIDE 화면은 구분한다. 기존 [474개 좌표 JSON](data/HOK_KOREAN_SECOND_WAVE_COORDINATES.json)·[326개 이력 JSON](data/HOK_KOREAN_FOCUS_LAYOUT_COORDINATES.json)은 당시 기록 그대로 보존하며 이 delta를 적용하지 않은 현재 전체 좌표로 사용하지 않는다.

## 8. 변경 영향 처리 대장

| 기능·경로 | 처리 | 근거·남은 검증 |
|---|---|---|
| 지원 선행·초대와의 배타 4선언 | 수정 적용 | 선봉으로 재연결, 초대 선행·그 밖의 배타·가용 조건 유지 |
| 자동 280일 → 25/180일 결정 | 수정 적용·기존 7태그 단계 엔진 확인 | 기존 공유 정신 재사용; 당시 통제 실행에서 비용·지급·기간 경과 후 제거·재지급 확인. 16태그 확장의 실행 증거와 정확한 만료 경계는 별도 |
| 중국 16태그·JAP | 중국 확장·동적 국가 배제 반영·합성 엔진 확인·일본 유지 | none-clone 4FAIL 뒤 `is_dynamic_country = no` 추가. 최종 16국·0정식대상/clone·NCNS 비활성 사례 69/0은 14절; 정상 UI 진행과 구 저장은 미검증 |
| 기존 280일 정신·완료 중점 저장 | 의도적 유지·차단 적용 | 잔여 기간 보존, 일부 중국 대상만 기존 지원이어도 묶음 차단; 실제 구 저장 검증 미완료 |
| SIA·VIN·MAL·PHI·INS 공유 호출 | 의도적 유지 | 공유 정의·기존 기간·효과 보존 |
| 민슈 내전 | 수정 적용·주요 엔진 결과 확인 | 별도 fresh 합성 지지도 20%/70%에서 생성국 보유 주·육군·함정·항공 비교; 정확한 면적/산업/해공 비례는 미검증 |
| 민슈의 세력 편입·한국 참전 | 의도적 유지·엔진 확인 | 기존 생성국 scope·효과 순서 유지, 두 합성 내전의 동맹/자동 참전 확인 |
| 중국 독재자 축출의 KCH·주·전쟁명분·결정 | 전쟁명분 대상 소스 반영·나머지 유지 | 전쟁명분을 14절의 현존 16태그로 정렬. 일본 분할 공식·생성국·고정 주/코어·후속 재건 변경은 이번 범위 밖 |
| 정보국 신규 중점·정신·시각 자산 | 수정 적용 | 35일·AI 1·LaR·기관 설립·15보정·내부 이미지 통합 |
| 정보국의 역사 AI 계획 | 재무장 직후로 이동·소스 확인 | 다른 항목 상대 순서/가중치/계획 보존. 이전 c212는 독립당 단계 이력이며 이번 경로의 AI 진행은 미검증 |
| 정보국 선행·위치·가시성 | 재무장 이관 적용·소스 확인 | (62,1) 고정·정치 offset 없음·LaR만 유지. 민주 HIDE guard 제거; 이번 런타임/UI 미실행 |
| 작전 속도 +35% | 소스·국가 보정 조회/저장 확인, 실제 효과 미확인 | 등록값 0.35를 실제 작전시간 단축의 증거로 쓰지 않음 |
| 본문 두 채널·새 표시 | 수정 적용 | 동일 한국어 본문/BOM; 실제 UI 미관측 |
| 활성 영어 번역의 기존 5키 | 제외·미해결 | 외부 번역 저장소 미수정, 영어 경로에서 낡은 내용이 덮어쓸 수 있음 |
| 배치·기존 좌표 스냅샷 | 수정 적용·이력 유지 | 부분 delta 5노드; 과거 JSON 두 개 미수정, 실제 UI 검증 남음 |
| 원본·Workshop·지도·코어 | 제외 | 원본 읽기 전용, 필요한 선정 DDS만 복사; 지도/주 목록 수정 없음 |

## 9. 재무장 이관 전 독립당 단계의 검증 이력

**이 절의 엔진 결과와 정적 75/0·60/0 등은 재무장 이관 이전 독립당 배치의 소스에 속한다.** B8/762d·c212를 현재 재무장 선행의 실행 증거로 쓰지 않는다. 이번 후속 변경은 [11절](#11-2026-11-19-재무장-시작-선행으로-이관)의 소스 비교 27확인·미해결 0까지이며 게임·UI를 실행하지 않았다.

최종 가시성 보완 뒤 정적 검토를 재실행해 **75 PASS / 0 FAIL**을 확인했다. 앞선 72/0은 AI 계획 통합 전, 종전 75/0은 가시성 보완 전 단계로 보존한다. 독립 중점 소스 **38 PASS / 0 FAIL**, HIDE 보완 뒤 독립 소스 **60 PASS / 0 FAIL**, AI 통합 독립 **5 PASS / 0 FAIL**, 낮은/높은 지지도 네이티브 **13개 관측**, 기간 통제 **40 PASS / 0 FAIL**은 범위와 소스가 달라 합산하지 않는다. 최종 60/0의 조건 행렬은 실제 SHOW/HIDE UI 관측이 아니다. 자산의 6개 원본 바이트·치수/알파·내부 참조·유일 sprite와 paired BOM/본문을 확인했고 실제 크기 외부 미리보기를 검수했다. 이 결과는 실제 효과·UI·저장 검증을 대신하지 않는다.

소스 식별자는 서로 다른 종류다. `common/national_focus/korea.txt`의 가시성 보완 전 SHA-256은 `e30428b406f210ccef8b5d5e7db436a1103b832a65cc427d191451b713ef7aef`, 보완 뒤 최종 읽기 SHA-256은 **`b8b427df8e8a73820156a6abcff6632b60c89e2fb68c317b96f24ef2e694584d`**다. `c212`는 그 이전 AI 완료 실행의 게임 체크섬이며 파일 해시가 아니다. 두 파일 소스·실행 결과를 바꿔 쓰지 않는다.

루트의 `support-clean-v2` 초기 엔진 진단은 **20 PASS / 0 FAIL**이다. `1936.1.2.1` 네이티브 저장에서 수혜 8개국의 남은 지원 179일, 두 결정의 정치력 25 비용과 정보기관·국민정신을 확인했다. 국가 작전 속도 보정 0.35의 조회·저장도 확인했으나 실제 작전 소요일수는 시험하지 않았다. 이 초기 결과는 앞의 두 정적 검사와 합산하지 않는다.

`support-clean-v2`에서는 7월 3일에도 지원이 존재했고, 두 결정의 실행 횟수 1→2·남은 기간 177~178일을 네이티브 저장에서 확인했다. 단순한 지원 부재를 기대했던 만료 판정 **4개 FAIL은 그대로 보존**한다. AI의 추가 실행·기간 재시작이 관측되었으므로 이를 곧바로 최초 지원이 만료되지 않은 production 결함으로 귀속하지 않는다.

별도 `support-expiry-controlled`(PID 16468, 체크섬 `776a`)는 **40 PASS / 0 FAIL**로 완료·종료했다. production의 결정 AI 1은 유지하고 **외부 시험 사본에서만 AI 0**으로 자동 재구매를 통제했다. `1936.1.2.1` → `1936.7.3.1` → `1936.7.5.1` 네이티브 저장에서 8개국의 지원 정신 수 **1→0→1**, 남은 기간 **179일→없음→179일**, 두 결정의 실행 횟수 **1→1→2**, 재실행 비용 각각 **정치력 25**를 확인했다. 이는 기간 경과 후 제거와 재실행의 엔진 증거이며 정확히 180일째 어느 시각에 제거됐는지의 경계 측정이나 실제 UI 클릭·구 저장 재로드 검증은 아니다.

내전은 **별도 fresh 실행에서 지지도를 합성한 뒤 helper를 직접 호출**했다. 두 실행의 네이티브 민주정부 `D04`를 비교한 관측은 다음과 같다.

| 일본 민주주의 지지도 | 민주정부 보유 주 | 민주정부 육군 사단 | 민주정부 함정 | 민주정부 항공기 |
|---|---|---|---|---|
| 20% | 4 | 12 | 83 | 141 |
| 70% | 12 | 42 | 118 | 543 |

시작 일본 육군 60개 중 12→42개가 민주정부에 배분됐고, 두 실행의 세력 편입·한국 자동 참전도 확인했다. 이 결과는 높은 지지도에서 민주정부의 주·군대가 더 많아진 해당 합성 사례의 증거다. 주의 정확한 면적·인구·산업 비율, 해군·공군의 정확 비례, 정상 중점 진행이나 장기 AI를 검증했다고 주장하지 않는다.

첫 `focus-ai` 실행은 초기 상태만 확인한 뒤 새 중점을 선택하지 못한 채 미완료 종료됐으며 그 이력은 보존한다. 이후 역사 AI 목록을 통합한 `focus-ai-production`(PID 14000, 가시성 보완 전 체크섬 `c212`)에서는 **부모만 합성 완료하고 목표 중점은 강제 완료하지 않았다.** 외부 AI 계획 없이 production AI 목록으로 `1936.1.2.1`의 새 중점 진행도 2에서 `1936.2.5.1`의 완료 이력·정보기관·국민정신으로 이어진 결과를 확인했다. 시작 `1936.1.1.24`·완료 `1936.2.4.24` marker도 보존하지만 이를 정확히 840시간의 실측이라고 주장하지 않는다. 기본 35일 중점의 AI 선택·누적 완료 증거이며 사용자 UI 선택이나 전체 독립당 경로의 자연 진행은 아니다.

11월 19일 HIDE 가시성 보완 뒤 최종 `production-only`(PID 24356)는 원래의 **저장소 → 영어 번역 두 모드, `l_korean`, DLC 37개, speed 0**으로 전체 재시작했다. 최종 B8 소스에서 체크섬 **`762d`**, 일시정지 새 게임 **`1936.1.1.12`**와 `RestoreDeviceObjects` 완료를 확인했다. 변경 대상의 새 파싱·등록 오류는 발견되지 않았으나 최종 raw 오류는 **9개**다. 다른 등록 모드 descriptor 관련 7개·현지화 충돌 1개·기존 buildings 관련 66858행 invalid argument 1개를 구분했으며 전체 무오류라고 주장하지 않는다.

소유 PID 24356의 종료를 확인했고 임시 모드 pointer를 제거했다. 원래 `dlc_load.json`·`settings.txt` 두 파일은 각각 시작 시 SHA-256과 정확히 일치하게 복원했고, 기존 저장 **99개 전체의 SHA-256은 불변**이다. 최종 프로세스 조회에서 HOI4·dowser·Paradox Launcher·GameOverlayUI·crash_reporter는 모두 없고 기존 Steam PID 13492는 유지했다. Steam의 실제 Play 버튼/Running 표시 복귀는 UI 연결 불가로 확인하지 못했다.

최종 로드와 정리의 실행별 증거는 [구현·검증 기록](incidents/2026-11-18-korean-democratic-support-intelligence.md)과 아래 외부 색인을 따른다. UI 호스트 연결을 사용할 수 없어 실제 중점·결정·정신 화면은 관측하지 못했고, 변경 전 저장 재로드·작전 실제 소요일수·정확한 만료 시각·장기 AI·다른 DLC/언어·멀티플레이도 미검증이다. 가시성 보완 전의 엔진 결과나 최종 일시정지 로드를 새 UI·모든 경로 검증으로 확대하지 않는다.

| 층 | 필요한 확인 | 현재 한계 |
|---|---|---|
| 소스 | 선행·양방향 배타·결정 운영·보정 키·scope·참조·좌표·두 채널·자산 | 위 정적 확인 반영; 실제 작동 보장 아님 |
| 로드·UI | 최종 소스 등록과 결정·해금·툴팁·아이콘·광택·SHOW/HIDE | guard 뒤 최종 두 모드 전체 재시작/일시정지 로드 확인; 실제 UI는 호스트 사용 불가로 미관측 |
| 실제 효과 | 비용 25·현존 대상 +0.10·기간 경과/재사용·구 타이머 차단·내전 낮은/높은 지지도 분할·정보국 보정 | 초기 지원·비용·등록 보정·합성 내전 및 AI 통제의 제거/재지원 확인; 정확한 만료 경계·작전 소요일수 등은 미검증 |
| 저장 | 새 지원 잔여 기간·완료 이력·변경 전 280일 보존·일부 중국 구 지원·실제 재로드 | 미완료; 일반 구 저장 호환을 보장하지 않음 |
| 기타 | 역사 AI 통합 후 선택·기본 35일 누적 완료·장기 AI·다른 DLC/언어·멀티플레이 | 초기 미완료 종료 보존; guard 전 production AI 선택·완료 확인, 정확 840시간·전체 경로 자연 진행·나머지는 미검증 |

## 10. 최초 문서화 단계와 자료 위치 이력

같은 2026-11-18의 최초 설명 요청은 “코드 수정하지 말고 설명만”, 이후 요청은 “문서화 작업만 진행해줘”였다. 당시에는 이 계획서·README·2차 확장 계획의 Markdown **3개만** 작성/갱신했고 게임 코드·현지화·자산·설정·저장·Git 이력을 바꾸지 않았다. 코드·설치 문서·자산 선언·번역 문자열을 읽고 문서 내용·링크·diff만 확인했으며, 게임·테스트·진단 helper·이미지·manifest를 만들거나 실행하지 않았다. 이 사실은 당시 단계의 결과이며 현재 구현 단계의 미실행 주장으로 재사용하지 않는다.

당시 미정이었던 신규 ID·35일·AI·DLC 세부·지원 방식/반복/구 타이머 정책·지지도 clamp·병종 비율·배치·내부 자산 사본은 현재 2~8절의 결정으로 채웠다. 11월 19일 HIDE 가시성을 보완했다. 작전 실측·UI·만료의 정확 경계·구 저장 등 남은 검증과, 합성 내전·통제 만료/재지원·목표 강제 완료 없는 production AI 진행에서 확인한 결과는 9절에서 구분한다. 최초 문서의 변경 전 행 번호와 1.19.5 원본 참고 위치는 출처 역할로 보존했다.

최초 구현 단계 문서 갱신 전 Markdown 사본은 `C:\hoi\test\hok-democratic-support-intelligence-20261118-01\assets\docs-before\`에 보존했다. 자산 helper·개별 PNG·실제 크기 연락시트·검사 결과는 같은 작업의 `assets\` 아래다. 이전 `.local-artifacts` 기록을 찾아야 할 때는 [개발 자료 보관 안내](HOK_DEVELOPMENT_ARTIFACT_ARCHIVE.md)의 현재 매핑을 따르며, 이번에는 그 과거 archive를 사용하지 않았다.

그 외 실행 증거의 기준 경로는 같은 외부 작업 루트다. 게임 생성 원본은 1절의 실제 사용자 데이터에 있고, 아래 `runs/`의 로그·저장은 증거 사본이다. 이 색인은 파일 위치·출처를 유지하기 위한 것이며 시험 자료를 저장소나 업로드 패키지에 복사하라는 뜻이 아니다.

| 외부 작업 루트 아래 경로 | 역할 |
|---|---|
| `validation/source-checks.json`, 같은 폴더의 `source-check-history.json`·`source-checks-superseded-*.json` | 최종 75/0과 이전 실패·오탐·소스 단계 보존 |
| `validation/focus-source-independent-review.json`, 같은 폴더의 `postguard-source-review.json` | 이전 38/0·최종 B8 소스 60/0을 구분한 독립 확인 |
| `validation/support-expiry-controlled-summary.json`, 같은 폴더의 `support-expiry-controlled-initial.json`·`support-expiry-controlled-expired.json`·`support-expiry-controlled-rebought.json` | AI 통제의 제거·재지원 40/0과 세 시점 원값 |
| `validation/uprising-low-high-comparison.json` | 별도 fresh 합성 내전의 13개 네이티브 비교 |
| `validation/focus-ai-production-summary.json` | guard 전 c212의 목표 강제 완료 없는 AI 진행 |
| `runs/production/process.json`, 같은 production 폴더의 `process-exit.json`·`capture-20261118T150605Z/`·`capture-20261118T150609Z/` | 최종 762d 실행·종료와 수집한 로그/저장 사본 |
| `baseline/profile-hashes.json`, `baseline/save-hashes.json`, `restoration.json` | 시작 시 설정·기존 저장의 기준 해시와 두 설정 파일 정확한 복원·임시 pointer 제거 |
| `final-process-profile-observation.json` | 2026-11-19 00:15:14 +09:00 최종 재조회: 원래 설정 두 해시 일치·관련 5종 프로세스 0·기존 Steam 13492 유지·임시 pointer 없음. 실제 Steam Play 표시는 미관측 |
| `final-inventory.json` | 최종 변경 파일·해시의 유지용 실행 색인. 이전 작성본과 루트의 최종 재작성 결과를 구분 |

기존 `docs/assets/korean-fascist-mobilization-validation-20260923/`의 시험 PNG 4개(`hide-upper.png`, `normal-completion.png`, `normal-progress.png`, `show-upper.png`)는 정리 미결이며 이동·삭제하지 않았다. 새 helper·테스트·백업·실행 자료는 [프로젝트 규칙](../AGENTS.md)에 따라 위 외부 작업 경로에만 둔다. 이번 작업은 커밋·푸시·업로드를 포함하지 않는다.


## 11. 2026-11-19 재무장 시작 선행으로 이관

사용자의 후속 요청에 따라 정보국의 직접 선행·위치 기준을 `KOR_independent_party_in_power`에서 **`KOR_begin_rearmament`**로 바꿨다. 기본 (120,6)·민주 완료 HIDE (85,6)에서 **모든 SHOW/HIDE 정치 상태의 (62,1)**로 이동했다. 부모 (54,0) + 상대 (8,1)이며 정치 offset이 없는 공통 군사 가지다. 민주 HIDE guard를 제거하고 LaR만 유지해 정치 선택 때문에 사라지지 않는다. 35일·보상·AI 가중치·국민정신·아이콘·광택은 바꾸지 않았다.

재무장 이관 단계의 focus 소스 SHA-256은 **`3d17d626fda303f48ae3f5d4c7505f61eeab63518aa849057c7a3bc80135d032`**다. 후속 맹주 조건 제거 뒤의 소스는 12절을 따른다. `B8`는 이전 독립당/HIDE guard 소스, `762d`는 그 이전 단계의 최종 로드 체크섬, `c212`는 그보다 앞선 AI 완료 실행 체크섬이다. 이번 이관은 게임을 실행하지 않았으므로 새 체크섬을 기록하지 않는다.

새 외부 작업 루트는 **`C:\hoi\test\hok-intelligence-rearm-parent-20261119-01\`**다. `baseline/`의 이전 runtime 사본과 `after/`의 변경 뒤 사본을 비교했고, **20개 runtime 파일 중 정확히 4개**(중점·AI·paired 설명 2개)만 바뀌었다. `baseline_docs/`에는 이 작업의 편집 전 Markdown 5개와 부분 좌표 JSON을 파일명 그대로 보존했다. 원본 게임·Workshop·이전 실행 증거는 수정하지 않는다.

`source-review.json`은 **27확인·미해결 0**이다. 475개 ID·선언 순서, 다른 474개 중점 정의/좌표, 기간·보상·가중치, offset 7개·전체 범위를 보존하고, 새 (62,1)의 모델 충돌 0·후손 없음·모든 SHOW/HIDE 정치 완료 상태의 고정 좌표와 LaR-only 조건을 확인했다. 이는 소스/모델 확인이며 실제 선·이름판·클릭·DLC 표시·현재 경로의 정상 AI 진행을 입증하지 않는다.

최초 **26확인·미해결 1**은 `La Resistance`의 인용부호를 보존하는 parser 토큰과 기대값을 다르게 비교한 감사식 실수였다. `source-review-initial-quoted-token-mismatch.json`에 남겼고 그 한 항목의 기대값을 직접 파싱 결과에 맞춰 교정해 27/0으로 확인했다. 이 교정을 production 소스 추가 변경이나 게임 오류 수리로 기록하지 않는다.

현재 구현과 위치는 [부분 좌표 delta](data/HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_LAYOUT.json)를 따른다. 이전 독립당 단계의 전체 검증은 9절 및 [기존 구현·검증 사건 기록](incidents/2026-11-18-korean-democratic-support-intelligence.md)에 남긴다. **이번 이관의 게임 실행·실제 UI·구 저장 재로드·작전 실측은 미실행/미검증**이다. 기존 시험 PNG 4개는 정리 범위가 없어 그대로 두며, 커밋·푸시·업로드를 하지 않았다.

## 12. 2026-11-19 두 봉기 중점의 한국 세력 맹주 조건 제거

이 절의 표·해시는 맹주 조건 제거 당시의 이력이다. 이후 중국 조건·기간은 [23절](#23-shandong-focus-chi-support-and-duration), 일본 AI 제한 제거는 [24절](#24-minshu-ikki-player-japan)로 구분한다.

사용자 요청으로 `KOR_overthrow_the_chinese_dictators`(중국 독재자 축출)와 `KOR_minshu_ikki`(민슈 잇키)의 `available` 안에 있는 `KOR = { is_faction_leader = yes }` 조건을 각각 제거했다. 한국의 민주주의 정부·독립국 조건과 상대국 조건은 유지했다. 자동 조건 툴팁에서 해당 맹주 요구가 빠지는 소스 변경이며 별도 현지화 문구를 삭제한 작업은 아니다.

| 경로 | 처리 | 확인·남은 범위 |
|---|---|---|
| 두 중점의 한국 세력 맹주 조건 | 수정 적용 | 각 1개, 총 2개 제거 |
| 한국 민주주의·독립국, 중국 지도국 존재·비민주주의, 일본 AI·비민주주의 | 의도적 유지 | 나머지 `available` 조건 소스 동일 |
| 선행·35일·배치·아이콘·AI·중국 생성국/전쟁명분·일본 봉기 비율 | 의도적 유지 | 조건 외 중점 필드와 공용 helper 불변 |
| 기존 `add_to_faction`·자동 참전 효과 | 의도적 유지·새 분기 미확인 | 비맹주·무세력 상태에서 실행 검증하지 않음; 새 세력 자동 창설이나 기존 동맹 외교 처리 추가 없음 |
| 후속 `KOR_New_China_Government` 결정 | 의도적 유지 | `common/decisions/KOR_decision.txt`의 독립국·KCH와 같은 세력·CHI가 KOR 종속국인 조건은 유지. 축출 중점의 조건 제거가 결정의 즉시 사용을 보장하지 않음 |
| 본체 두 언어·활성 영어 번역 | 의도적 유지 | 관련 이름/설명/효과 안내에는 맹주 조건의 수동 문구가 없어 현지화 파일 변경 없음. 활성 영어의 기존 아시아 연합 서술·낡은 효과 안내는 기존 범위 밖 미해결 항목으로 유지 |
| 지도·주 이전·코어와 다른 중점의 맹주 조건 | 제외 | 이번 조건 제거 요청 밖이며 수정 없음 |

이 단계 당시 focus 소스 SHA-256은 **`5ce8aa0fe1aff5d2d4b59a330a69b6838d70d14edbc4381e360ce70e07a8a80d`**다. 외부 작업은 `C:\hoi\test\hok-uprising-no-faction-leader-20261119-01\`이며, `baseline/`은 이번 요청 직전 작업 소스 사본, `baseline.json`은 기존 runtime 20파일의 해시, `source-review.json`은 변경 후 비교다. `after/`는 변경 뒤 사본이고 `final-inventory.json`은 현재 소스·문서의 위치/해시와 사본 일치 여부를 기록한다. **12확인·미해결 0**은 475개 ID·순서 보존, 해당 두 중점의 맹주 조건만 제거, 그 밖의 가용 조건·보상·다른 473개 중점 정의·CRLF 및 runtime 나머지 19파일 불변을 확인한 소스 결과다.

설치 원본 `documentation/effects_documentation.md` 2293–2300행은 `add_to_faction`을 국가 scope의 세력 편입 효과로 설명하지만 비맹주·무세력에서의 동작은 명시하지 않는다. 이번에는 보상 효과를 변경하거나 게임을 실행하지 않았으므로 새 허용 분기의 실제 세력 편입·한국 참전, UI·저장 재로드는 미검증이다. 이전 맹주 상태의 엔진 성공을 새 상태의 검증으로 재사용하지 않는다. 기존 시험 PNG 4개는 정리 미결로 유지했고 커밋·푸시·업로드는 하지 않았다.

## 13. 2026-11-19 첩보 임무 보정 재조정

최종 사용자 정정에 따라 `HOK_KOR_secret_intelligence_service_idea`의 기존 +75% 일곱 값 중 **이념 지지만 +100%**, **선전·저항 소탕·사보타주·저항 강화·무역 지배·외교 압력은 각각 +25%**로 바꿨다. 앞서 언급된 선전 +100% 안은 정정으로 대체됐으며 소스에 적용하지 않았다. 이는 기존 값에 더하는 추가 보상이 아닌 국민정신 자체의 최종 수치다.

수정은 [정보국 국민정신](../common/ideas/HOK_KOR_democratic_intelligence.txt)의 일곱 숫자와 인접 기여 주석에 한정했다. 나머지 여덟 보정·요원 슬롯·기관 설립·35일 중점·재무장 선행·기존 봉기 조건 변경·AI·국민정신 ID/이미지는 유지했다. 본체 두 언어의 이름·설명에는 기존 +75% 숫자가 없고 수치는 자동 보정 툴팁을 사용하므로 현지화 파일을 수정하지 않았다. 다른 국민정신·고문·기관 업그레이드의 +75%는 이번 범위 밖이다.

외부 작업은 `C:\hoi\test\hok-intelligence-mission-rebalance-20261119-01\`다. `baseline/`은 이번 요청 직전 작업 소스/문서 사본, `baseline.json`은 runtime 20파일의 기준 해시다. `source-review.json`에 소스 비교 결과, `after/`와 `final-inventory.json`에 변경 후 사본과 최종 위치/해시를 기록한다. 이전 일곱 +75% 상태의 엔진 관측은 9절의 역사적 증거이며 새 수치의 실행 결과로 재사용하지 않는다. 이번에는 게임·UI·실제 임무·저장 재로드를 실행하지 않았다. 기존 시험 PNG 4개는 정리 미결로 유지했고 커밋·푸시·업로드를 하지 않았다.

<a id="14-2026-11-19-최신-중국-군벌-대상-누락-검토미구현-확장안"></a>

## 14. 2026-11-19 최신 중국 군벌 대상 16태그 확장

최초에는 **검토 후 문서화 전용**으로 누락과 향후 확장안만 기록했으며 당시 소스는 `CHI·PRC·SHX·GXC·YUN·XSM·SIK`의 **7태그**였다. 그 문서화 단계에서는 코드·현지화·테스트·게임을 변경하거나 실행하지 않았다. 이후 사용자가 별도로 16태그 확장을 승인했으며, 아래는 그 구현 계약과 현재 검증 상태다. 앞선 미구현 판정을 현재 구현 상태로 혼동하지 않는다.

### 기준과 누락 대상

설치 원본 `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\`의 `launcher-settings.json` 4–5행은 **Operation Postern v1.19.5.0.7c6c (c184)**다. 이 버전 표기를 최신 온라인 배포 여부나 현재 실행 중인 게임의 체크섬으로 확대 해석하지 않는다. 저장소는 `C:\hoi\hearts_of_korea`, 검토 기준은 `feat/korean-focus-expansion-ai`·HEAD `0c19f58fa7a9ff898196dcdbe46edfd0ad5fdbbc`의 기존 미커밋 작업 소스다.

설치본 `common/scripted_triggers/CHI_scripted_triggers.txt` 124–140행의 `is_chinese_warlord`는 **14군벌**을 정의한다. HOK가 포함했던 기존 군벌은 `SHX·GXC·YUN·XSM·SIK` 다섯 곳이며 CHI·PRC는 별도 주요국이다. 이번에 추가하는 누락 9태그는 다음과 같다.

| 태그 | 바닐라 한국어 표시명 | 구분·이번 처리 |
|---|---|---|
| GDC | 광동군벌 | NCNS 신규 시작 군벌, 지원·전쟁명분 대상에 추가 |
| SND | 산동군벌 | 동일 |
| SIC | 사천군벌 | 동일 |
| NXM | 영하 마가 | 동일 |
| GSM | 감숙 마가 | 동일 |
| XIC | 동북군 / 서안 | 동일 |
| KHM | 화전 마가 | 동일 |
| HBC | 기찰정무위원회 | 동일 |
| KUM | 쿠물 칸국 | 후속 봉기국, 현존할 때 같은 대상에 포함하며 과거 지원 소급 없음 |

추가 태그 등록은 설치본 `common/country_tags/00_countries.txt` 356–366행, NCNS의 추가 시작 군벌 8개 선택 항목은 `common/bookmarks/the_gathering_storm.txt` 1207–1394행에서 확인했다. 한국어 명칭은 `localisation/korean/countries_l_korean.yml`의 각 태그 항목을 따르며 XIC의 비동맹 표시는 동북군, 일반 표시는 서안이다. NCNS 활성화 때 중국·광서·서북삼마·신강에서 군벌을 분리한 변경은 [공식 NCNS 패치 노트](https://forum.paradoxplaza.com/forum/developer-diary/no-compromise-no-surrender-patch-notes.1868750/)에도 명시돼 있다. 국가 등록·군벌 분류·DLC별 시작 국가 수는 서로 다른 집계다.

KUM은 시작 군벌 8개와 구분한다. 설치본 `history/states/760-Dabancheng.txt` 10–14행에서 초기 소유자는 SIK이고 KUM 코어가 있으며, `events/SEA_Warlords.txt` 221–240행의 `SEA_warlords.4`에는 KUM으로 주 760을 이전하고 `KUM_uprising` 병력을 불러오는 후속 봉기 효과가 있다. 이벤트의 전체 호출·발화 조건과 실제 봉기 실행은 확인하지 않았다. 또한 구 `WTT_china_political_struggle_triggers.txt` 165–180행의 군벌 정의는 **KUM을 제외한 13개**이므로 이를 사용하면 최신 일반 14군벌 집합과 달라진다.

### 구현 계약과 영향 처리 대장

고정 집합은 **`CHI·PRC·SHX·GXC·YUN·XSM·SIK·GDC·SND·SIC·NXM·GSM·XIC·KHM·KUM·HBC`**의 16태그다. [전용 공용 트리거](../common/scripted_triggers/HOK_KOR_chinese_democratic_support_triggers.txt)의 `HOK_KOR_is_chinese_democratic_support_target`는 국가 scope에서 `exists = yes`·`is_dynamic_country = no`·16개 `tag` 목록을 함께 판정한다. 초안의 존재·태그 검사만으로 동적 국가가 제외된다는 추론은 아래 none-clone 사례로 반증돼 명시적인 guard를 더했다. 설치본 `documentation/triggers_documentation.md` 5462–5470행은 국가 scope의 `is_dynamic_country`를 설명한다. 별도 scripted effect는 추가하지 않는다.

지원 효과의 16개 명단은 동적 이름 조회 `[TAG.GetName]` 대신 정적 국가 현지화 참조를 사용한다. 기본은 `$TAG$`이고, CHI와 같은 일반 이름을 피하기 위해 PRC는 `$PRC_communism$`, 동북군 표시는 XIC의 `$XIC_neutrality$`를 사용한다. 16개 키가 설치본 한국어·영어에 존재함을 확인했다. 이는 정식 대상 목록의 표시 정책이며 기존 GetName의 실제 UI 결함을 입증했다는 뜻이 아니다. 실제 화면에서 이름 치환·줄바꿈을 관측하지는 못했다.

| 기능·사용처 | 반영 위치·계약 | 처리·남은 확인 |
|---|---|---|
| 지원 대상 존재 검사 | [지원 결정](../common/decisions/HOK_KOR_democratic_support.txt)의 `any_country`에서 공용 트리거 호출 | 수정 적용·소스 확인: 현존 대상 1개 이상 필요, 0개면 비용만 내는 실행 차단 |
| 기존 지원 중복 차단 | 같은 파일의 `NOT`/`any_country`와 공용 트리거 | 수정 적용·소스 확인: 16태그 중 현존 대상 하나에만 기존 공유 정신이 있어도 묶음 전체 차단 |
| 실제 180일 지원 지급 | 같은 파일의 `every_country`와 공용 트리거 | 수정 적용·소스 확인: 실행 때 현존하는 대상 각각에 기존 정신 지급, 전체 묶음 비용은 25 |
| 대상국 툴팁·결정 설명 | [한국어](../localisation/korean/HOK_KOR_democratic_support_l_korean.yml)·[paired English](../localisation/english/HOK_KOR_democratic_support_l_english.yml)의 `HOK_KOR_democratic_support_china_effect_tt`·결정 `_desc` | 수정 적용·소스 확인: 현존 16태그·한 번의 비용·기간·기존 지원 차단을 실제 계약에 맞춤 |
| 축출 중점의 전쟁명분 | [한국 중점](../common/national_focus/korea.txt)의 `KOR_overthrow_the_chinese_dictators` 보상 | 수정 적용·소스 확인: 공용 트리거로 `every_country`를 돌며 `ROOT` 한국이 `PREV` 대상에 기존 전쟁명분 생성 |
| 축출 효과 안내 | [한국어](../localisation/korean/korea_focus_l_korean.yml)·[paired English](../localisation/english/korea_focus_l_english.yml)의 `KOR_overthrow_the_chinese_dictators_tt` | 수정 적용·소스 확인: 실제 전쟁명분 범위를 16태그와 정렬, KCH 보상은 유지 |
| 현재 중국 지도국 검사 | 중점의 기존 `WTT_current_china_leader` 조건 | 의도적 유지: 기존 존재·정부 검사이며 새 고정 집합과 역할이 다름 |
| 후속 중국 재건 결정 | [KOR_decision.txt](../common/decisions/KOR_decision.txt) 1322·1334행, CHI 종속국 조건·CHI만 합병 | 별도 범위·현행 유지: 군벌 전체 자동 합병 기능으로 해석하지 않음 |
| 활성 영어 번역의 구 설명/효과 안내 | `C:\hoi\Hearts of Korea English Translation Anime Modder's Edition\localisation\english\korea_focus_l_english.yml`의 기존 중국 관련 키 | 미해결·이번 수정 제외: 실제 영어 표시를 별도로 대조해야 함 |
| KCH·MAN·MEN·RNG 및 주변국 | HOK 생성국·협력국 등으로 위 일반 14군벌과 별개 | 의도적 제외: 고정 16태그 밖이며 자동 추가하지 않음 |
| 중국 봉기 고정 주·코어·지도·군벌 병합 정책 | 기존 보상·후속 결정 | 이번 구현 범위 밖, 정상 판정이나 수정으로 취급하지 않음 |
| 일본 지원·민슈·정보국·AI·배치·시각 자산 | 기존 관련 모듈 | 의도적 유지: 이번 중국 대상 확장에 포함하지 않음 |

정치력 25·기간 180일·일일 민주주의 성장 +0.10·잔여 타이머·반복 대기와 기존 가용 조건은 유지한다. 소멸국을 부활시키지 않으며, 실행 뒤 새로 등장한 KUM 등에 과거 지원을 소급하지 않는다. 다음 지원을 구입할 때 현존하면 포함한다. 신규 대상 하나에만 구 지원이 남아 있어도 묶음 차단 대상이며, 별도 매일 검사·자동 갱신·환불·취소 정책은 추가하지 않는다.

### 자료 위치와 현재 검증 상태

이번 외부 작업 경로는 `C:\hoi\test\hok-chinese-warlord-expansion-20261119-01\`다. `baseline/source/`에 변경 직전 runtime 20파일과 문서 4개(본 계획·README·2차 계획·이전 사건 기록) 사본, `baseline.json`에 기준 해시·출처를 보존했다. 원본 게임·Workshop·외부 영어 번역 저장소는 읽기 전용이다. 사용자 게임 PID 23236이 실행 중인 상태를 발견했으며 문서 작업자가 게임·설정·프로세스를 조작하지 않았다.

최종 `validation/source-review.json`은 guard·정적 표시 명단을 포함한 **39확인·미해결 0**의 범위 제한 소스 비교다. 보완 전 **36확인·미해결 0** 결과와 helper는 `validation/before-dynamic-guard-source-review.json`·`validation/before-dynamic-guard-source_review.py`, 이전 트리거·지원 현지화 2파일은 `before-dynamic-guard/`에 따로 보존했다. 기존 runtime 20파일 중 결정·중점·paired 현지화 4파일을 합한 **기존 6파일**과 **새 트리거 1파일**이 영향 범위이며 나머지 기존 14파일의 해시는 동일하다. 두 paired 본문의 일치·UTF-8 BOM·기존 줄바꿈 보존을 확인했다. 최초 helper가 CRLF 정규식 파싱에서 낸 `KeyError`는 `validation/source-review-initial-error.json`에 보존했고 메모리 파싱만 교정했다. 이를 게임 오류나 생산 소스 수정으로 처리하지 않는다.

| 소스·단계 | SHA-256 |
|---|---|
| 현재 공용 트리거·guard 포함 | `f68c3ea786fe95fa77cae7d4a9283586874b37eec1f4db1790777fcaf336b316` |
| 보완 전 공용 트리거 | `57a0676ddd98d00ad0d4b81aef4ec2eb77aa29d86c08084d21f3303b165f544a` |
| 현재 지원 결정·guard 전후 동일 | `0c5f4b297608fdf411e87fa627c1fe28ab94b4523cfa631aff6148fffa7bc6cf` |
| 현재 한국 중점·guard 전후 동일 | `ab3b4e2bd501e30f5cd8e94eb23671c48fd7d8877c916113fe3ae3d30d4fb967` |

독립 `validation/source-checks.json`은 guard와 정적 현지화 참조를 포함한 **34 PASS·0 FAIL**이다. 이전 33/0은 `validation/source-checks-superseded-20261118T171024811398Z.json`에 보존했다. 최종 루트 39항목과 범위가 달라 합산하지 않으며, 두 소스 보고서는 엔진 등록·scope 실행·가용성·지급·실제 UI·저장 동작의 증거가 아니다.

보완 전 native none-clone 사례에서는 **4FAIL**을 확인했다. 저장에서 CHI 소유 주는 0, `original_tag = CHI`인 D04 소유 주는 1이었고, 한국의 전쟁명분 수혜국은 D04였다. 원본 CHI가 소멸한 조건에서 `tag = CHI`가 동적 국가를 가리키는 엔진 동작이 입증됐다. 처음 의심한 정식 CHI 재사용·fixture 설정 오류 가설은 반증됐으며 이 실패를 정상 판정으로 지우지 않는다. 명시적 동적 국가 guard 적용 전/후 소스와 fresh 재실행을 분리한다.

### 합성 native 실행과 단계별 결과

시작 당시 사용자 게임 PID 23236은 우리가 종료하지 않았고, 이후 CIM에서 해당 게임이 없음을 관측했다. 종료 주체·사용자의 저장 행동은 미관측이며, 그 뒤 별도 승인으로 진단용 새 게임을 실행했다. 국가 생성·소멸과 중점 보상은 강제 준비/실행이며 `activate_decision`도 실제 UI 가용 조건을 강제하는 클릭 증거가 아니다. 복사한 가용 조건은 한국 scope에서 별도로 평가했다. 일반 시험 구성은 Korean Language → HOK → 외부 probe이며 사용자 원래 두 모드 구성과 구분한다.

| 소스·사례 | 결과 | 확인 범위·한계 |
|---|---|---|
| 보완 전 57a·all-sixteen | 43 PASS·0 FAIL | 정식 16개국 각 지원·한국 명분·정치력 25; 원본 CHI가 살아 있는 clone만 비교한 초기 사례 |
| 보완 전 57a·only-added | 33 PASS·0 FAIL | 기존 7개국 소멸·신규 시작 8개국만 존재. GDC 구 지원 279일과 묶음 차단을 보존하고, fixture가 지원을 수동 제거한 뒤 8개국 각 179일·정치력 25·8개 명분 확인. 정상 만료나 중국 지도국 조건을 만족한 중점 착수 증거가 아님 |
| 보완 전 57a·none-clone | 3 PASS·4 FAIL | 정식 16개국 소멸 뒤 D04가 잘못 포함되는 실제 결함; 원본 실패 보존 |
| 보완 전 57a·초기 late-kum | 42 PASS·17 FAIL | 7월 3일 구매 기록 2·잔여 177일로 자율 재구매가 먼저 실행돼 예상 부재 17항목 실패. 강제 세 번째 호출은 가용성을 건너뛰어 정치력 25를 쓰고 기존 175일을 유지했으므로 정상 재구매로 해석하지 않음 |
| 보완 전 57a·late-kum-controlled | 60 PASS·0 FAIL | 외부 AI 제어와 실제 실행 canary를 확인한 별도 실행. 1월 2일 15국 각 179일/KUM 부재 → 1월 4일 KUM 등장·소급 없음·기존 15국 177일 → 7월 3일 16국 지원 없음 → 7월 5일 16국 각 179일. 구매 1→1→2·각 정치력 25; 정확한 180일 만료 경계는 미측정 |
| 최종 f68·none-clone-final | 6 PASS·0 FAIL | 정식 16태그 소멸·CHI 원태그 D04만 존재해도 지원 가용성 없음·clone 명분 없음; native 체크섬 7b5a |
| 최종 f68·all-sixteen-final | 44 PASS·0 FAIL | 16개국 각 179일·정치력 25·한국 actor의 16개 명분, clone 배제. clone에만 280일 구 지원을 둬도 정식 묶음을 막지 않음을 확인한 뒤 그 진단용 정신을 제거하고 구매; 체크섬 6880 |
| 최종 f68·no-ncns-final | 19 PASS·0 FAIL | 실제 NCNS 비활성 판정, 현존 기존 7개국 각 179일·정치력 25·7개 명분, 부재 KUM 부활 없음; 체크섬 b7d9 |

**최종 f68 세 사례만 69 PASS·0 FAIL**이며 구 소스의 60/0·초기 실패와 섞지 않는다. 독립 `validation/native-evidence-checks.json`의 **34 PASS·0 FAIL**은 직렬화된 저장의 국가·타이머·구매 기록·명분 등을 대조한 결과로, guard 전 기간 증거와 guard 후 대상 증거를 구분한다. 소스 검사 34/0과 이름이 같은 수치일 뿐 같은 검사가 아니다.

저장은 OneDrive 경로에서 이름 변경이 실패한 뒤 남은 완전한 `HOI4txt` `_temp.hoi4`를 확인한 것이다. `TEST_FAIL_*` 파일명은 의도한 native capture 경로이며 결과는 별도 PASS/FAIL 표식으로 판정했다. 정상 UI 저장·재로드·기존 캠페인 이관·정확한 만료 경계·멀티플레이는 입증하지 않는다. 실제 UI 도구는 fresh 연결 2회·reset 1회 뒤에도 pipe에 연결하지 못해 결정 클릭·명단 치환·줄바꿈을 관측하지 않았다.

최종 guard 소스를 probe 없이 최소 Korean Language → HOK(PID 19048)와 원래 `enabled_mods`의 HOK → English 두 모드(PID 25772)로 각각 전체 재시작했고, 1936년 1월 1일 일시정지 로드를 확인했다. 두 실행의 raw 오류는 각각 **9개**(등록 descriptor 7·현지화 충돌 1·기존 buildings 66858행 invalid argument 1)이며 전체 무오류를 주장하지 않는다. 이 둘은 저장을 만들지 않아 런타임 체크섬을 관측하지 못했으며 probe 저장의 체크섬을 대신 붙이지 않는다. 합성 clone/기존 KCH 생성에 연관될 수 있는 경고와 장기 진행의 `Scope does not have a Leader` assertion은 별개다. 특히 후자의 정확한 호출 귀속은 stack·clean 장기 비교가 없어 미확정이다.

### 보존·복원과 외부 증거 위치

착수 당시의 `baseline/profile/`과 실제 실행 직전의 **`baseline/pre-test-profile/`**을 구분하며 복원 기준은 후자다. 최신 로그 사본은 `baseline/pre-test-logs/`다. 최종 `validation/final-verification.json`·`validation/final-save-preservation.json`에서 **기존 저장 109개 SHA 전부 동일·변경 0**, 원래 존재한 **settings.txt·dlc_load.json 두 파일 SHA 일치**, 원래 없던 **pdx_settings.json·user_settings.config·continue_game.json의 부재 복원**을 확인했다. 임시 모드 pointer 제거·진단 PID 10개 종료·`hoi4.exe` 0개를 확인했으며 정상 UI 종료라고 주장하지 않는다. 독립 `root-final-observation.json`의 UTC 2026-11-18 17:21:38(한국 11월 19일 02:21) 재조회에서도 두 실제 설정 해시·보조 3파일 부재·pointer 부재와 hoi4/dowser/ParadoxLauncher/GameOverlayUI/crash_reporter 5종 0개를 확인했다. 원래 저장 109개는 앞선 보고서를 참조하며 이 재조회에서 해시를 중복 실행하지 않았다. Steam Play의 실제 UI 표시는 미관측이다.

**복원 예외는 사용자 데이터의 `continue_game.temp` 이어하기 인덱스다.** 원본은 142바이트로 관측됐지만 처음 백업 목록에 빠졌고, 뒤늦은 helper의 한국어 경로 손상으로 부재라고 잘못 기록한 사이 첫 capture가 덮었다. 원본 바이트를 보존하지 못해 복원하지 않았으며, 읽었던 일부 헤더로 원본을 추정 재구성하지 않는다. 실패 manifest·교정 실패·첫 capture 뒤 사본은 외부에 보존했다. `baseline/resume-index-after-first-capture/`는 원본 백업이 아니다. 이 예외를 두 설정 파일이나 109개 원 저장의 보존 결과와 섞어 전체 원복 완료라고 표시하지 않는다. 새 시험 저장 원본 **15개**는 실제 사용자 데이터 `save games/`에 남기고 외부 증거 사본과 대응시켰다.

| 외부 경로(이번 TASK 기준) | 역할 |
|---|---|
| `baseline.json`·`baseline/source/` | 변경 전 working tree·runtime 20파일·문서 4개 원본 대응 사본 |
| `before-dynamic-guard/`·`validation/before-dynamic-guard-source-review.json` | 보완 전 트리거/현지화와 36항목 이력 |
| `validation/source-review.json`·`validation/source-checks.json` | 최종 39항목·독립 소스 34항목 |
| `validation/DIAGNOSTIC_SCOPE.md`·`validation/native-summary.json` | 외부 probe/AI 제어·강제 호출 범위, 각 실행/로그/저장/capture 대응 |
| `validation/*-initial.json`·`validation/only-added-*.json`·`validation/late-kum-controlled-*.json` | 실제 저장 판독과 단계별 관측; 구/최종 소스는 summary의 실행별 해시로 구분 |
| `validation/native-evidence-checks.json`·`validation/final-verification.json` | 독립 저장 판독 34항목과 최종 native/로드/복원·남은 한계 종합 |
| `validation/final-save-preservation.json`·`restoration-*.json` | 기존 109개 보존·새 원본 15개 목록과 실행별 복원 결과 |
| `root-final-observation.json` | 최종 설정/부재 상태·5종 프로세스·pointer 독립 재조회; 저장 해시는 기존 보고서 참조 |
| `final-source-inventory.json`·`after/source/` | 문서 freeze 뒤 생성하는 최종 runtime 21개·문서 4개의 소스 사본/해시 대장 |

이전 중국 7태그와 JAP의 8국 엔진 관측, B8/762d·c212는 이번 확장 증거로 재사용하지 않는다. 기존 시험 PNG 4개는 별도 정리 미결로 유지했으며 커밋·푸시·업로드를 하지 않았다.

## 15. 2026-11-19 정보망 강도 획득 고정값 조정

사용자 요청으로 [비밀 정보국 국민정신](../common/ideas/HOK_KOR_democratic_intelligence.txt)의 `intel_network_gain`을 **25 → 10**으로 바꿨다. 별도 `intel_network_gain_factor = 0.25`(+25%)와 나머지 14개 보정은 유지했다. 이념 지지 +100%·선전 등 여섯 보정 +25%, 중점의 선행·35일·기관 설립·국민정신 ID·아이콘도 이번 변경 범위에 포함하지 않는다.

수정은 고정값 한 곳과 인접 기여 주석, 본 문서의 현행 표·설명·기록에 한정했다. 국민정신 설명에는 +25라는 수동 숫자가 없고 보정값은 자동 툴팁을 사용하므로 현지화 파일은 변경하지 않았다. 이전 +25 상태의 엔진 관측은 과거 이력으로 보존하며 +10의 실행 증거로 재사용하지 않는다. 이번에는 소스 차이만 확인했고 게임·UI·저장 재로드를 실행하지 않았다.

외부 기록은 `C:\hoi\test\hok-intelligence-network-gain-20261119-01\`이다. `before/`는 이번 요청 직전 코드·문서 사본, `baseline.json`은 관련 runtime 21파일의 기준 해시다. `after/`와 `change-summary.json`에 최종 사본·해시·범위 확인을 기록한다. 기존 다른 작업과 시험 PNG 4개는 그대로 유지했으며 커밋·푸시·업로드를 하지 않았다.

<a id="16-shandong-democratic-government-design"></a>

## 16. 2026-11-19 산둥 자유 공화국 후속 설계 — 초기 문서화·구현 전 이력

사용자가 설명 전용으로 검토한 뒤 **문서화 작업만** 요청한 후속 방향이다. 현재 게임 코드에 적용한 변경이나 구현 승인이 아니다. 이번 편집은 본 문서의 상단 안내와 이 절에 한정하며, 이전 1–15절의 소스·검증 이력은 당시 범위로 보존한다.

### 현재 소스와 문제

기준 저장소는 `C:\hoi\hearts_of_korea`, 브랜치는 `feat/korean-focus-expansion-ai`, HEAD는 `0c19f58fa7a9ff898196dcdbe46edfd0ad5fdbbc`다. 기존 미커밋 민주인사 지원·정보국 작업이 있는 working tree를 읽었으며, 새 기준으로 되돌리거나 기존 변경을 정리하지 않았다.

- [중국 지원 결정](../common/decisions/HOK_KOR_democratic_support.txt)은 현존하는 16태그에 기간제 민주주의 성장 정신을 지급한다. [중국 독재자 축출](../common/national_focus/korea.txt)의 `KOR_overthrow_the_chinese_dictators` 보상은 그 지지도를 조회하지 않고 KCH를 생성해 산둥 597·칭다오 743의 영토·핵심주를 지정하고, 한국의 세력 편입 효과와 기존 전쟁명분을 처리한다. 현재 생성 보상에는 피감독국 지정이나 별도 공동 참전 효과가 없다.
- [중국 신정부 인정 결정](../common/decisions/KOR_decision.txt)의 `KOR_New_China_Government`는 한국 독립·KCH와 같은 세력·CHI가 한국 종속국이라는 조건 뒤 KCH의 CHI 합병·`KCH_china` 외형·넓은 중국 지역 핵심주를 처리한다. 현재 지원으로 높인 지지도는 이 조건·보상에도 반영되지 않는다.
- 대상은 HOK 생성국 **산둥 자유 공화국 KCH**다. 바닐라 **산둥군벌 SND**와 다른 국가이며, SND 자체의 시작 핵심주·후속 군벌 중점은 이번 변경 방향에 포함하지 않는다. 명칭은 [기존 국가 현지화](../localisation/korean/replace/HoK_countries_l_korean.yml)의 `KCH_democratic`을 기준으로 유지한다.

위 내용은 이번 설명 단계에서 읽은 소스의 연결이다. 게임 내 생성국의 실제 영토·핵심주·외교 상태나 정상 진행을 새로 관측한 결과가 아니다.

### 확정한 방향과 명시적 제외

| 항목 | 후속 설계 계약 | 현재 상태 |
|---|---|---|
| 출범 시점·주체 | 「중국 독재자 축출」 완료 시 산둥 자유 공화국 KCH가 출범하는 기존 흐름을 사용한다. 국가·중점 ID는 유지한다. | 방향 확정·미구현 |
| 출범 시 핵심주 | 산둥에 기반을 두되 출범부터 중국 본토 핵심주를 가진 민주 대안정부로 설정한다. 핵심주 부여와 실제 영토 소유권 이전은 구분한다. | 방향 확정·정확한 대상 목록 미정 |
| 기본 영토와 지원 성과 | 산둥을 기본 출범 거점으로 삼고, 중국 세력의 민주주의 지지도가 높을수록 더 많은 초기 영토·병력을 확보하는 방향으로 연결한다. 추가 영토는 산둥 거점과 육지로 연결되는 중국 지역에서 선정하며, 아래 보호·제외 규칙을 우선한다. | 방향·연결 원칙 확정·조회 대상·규모·선정 알고리즘 미정 |
| 국가 지위 | 중점 완료에 따른 출범부터 한국을 종주국으로 하는 **피감독국**으로 설정한다. 일반적인 독립 동맹국 출범안 대신 사용자가 선택한 방향이다. | 방향 확정·미구현 |
| 한국의 전쟁명분 | 한국이 기존과 같이 현존 중국·군벌 대상의 `puppet_wargoal_focus`를 얻는 흐름을 유지한다. 명분을 받는 주체는 한국이며 대상은 14절의 동적 국가를 제외한 고정 16태그다. | 기존 효과 유지 |
| 전쟁 시작·참전 | **자동 선전포고·별도의 자동 공동 참전 효과나 상시 전쟁 연동은 추가하지 않는다.** 피감독국의 참전은 일반 외교·게임 규칙에 맡기며, 반드시 한국과 함께 참전한다고 보장하지 않는다. | 사용자 명시적 제외·이번 설계에 넣지 않음 |

피감독국 선택과 공동 참전 보장은 별개다. 설치 원본 V의 `common/autonomous_states/supervised_state.txt` 14행에는 `can_decline_call_to_war = yes`가 있다. 설명 단계에서 제안했던 별도 공동 참전 연결은 사용자가 거절했으므로, 향후 구현자가 이를 기능 보완으로 다시 추가해서는 안 된다. 전쟁명분 획득을 즉시 전쟁 개시로 바꾸지도 않는다.

<a id="16-shandong-connected-territory"></a>

### 2026-11-19 추가 확정: 연결 영토와 이전 보호·제외

사용자가 지지도에 따른 초기 영토 확대의 의미를 확인하면서 **만주국 등 일본 영토 제외**, **한국이 점령한 만주 영토 보호**를 명시한 뒤 문서화만 요청했다. 아래는 그 후속 설명을 반영한 출범 영토 설계이며, 기존 게임 코드의 현재 동작이나 실행 검증 결과가 아니다.

- **연결된 중국 영토:** 산둥의 기본 거점에서 출발해 육지로 이어지는 중국 지역을 추가 편입 대상으로 고른다. 멀리 떨어진 군벌의 지지도가 높다는 이유만으로 고립된 영토를 바로 이전하지 않는다. 지지도는 편입 규모에 반영하되 정확한 비율·최대 규모·주 선정·확장 순서·해협 등 특수 인접의 판정 방식은 미정이다.
- **일본 측 영토 제외:** 일본의 직할령·점령지 및 만주국 등 일본 측 종속국이 소유하거나 통제하는 주는 후보에서 제외한다. 중국국이 명목상 소유해도 일본 측이 통제하면 이전하지 않는다. 지원 대상국이라는 사실만으로 일본 측 소유·통제 제외를 우회하지 않는다.
- **만주 지역 자체 제외:** 만주는 별도의 지리적 영토 제외 범위로 관리한다. 현재 소유국이 만주국인지 여부만 검사하지 않으며, 한국이나 다른 나라가 소유·점령하게 되어도 만주를 추가 영토로 가져오지 않는다. 정확한 현행 주 목록은 아직 작성하지 않았고, 구현 전에 현행 지도 기준으로 명세해야 한다.
- **한국 소유·통제 보호:** 한국이 소유하거나 현재 통제하는 주는 어느 한 조건만 충족해도 이전하지 않는다. 한국 소유지만 외국이 점령 중인 주, 중국국 명목 소유지만 한국군이 점령 중인 주, 한국이 점령한 만주 지역도 포함한다. 소유국·통제국을 각각 확인하며 중국 핵심주라는 이유로 이 보호를 해제하지 않는다.
- **최초 산둥 거점에도 동일 적용:** 추가 편입뿐 아니라 출범 시의 고정 영토 지정에도 위 보호·제외를 적용한다. 현재 코드의 산둥 597·칭다오 743 강제 이전을 그대로 남겨 보호 대상 영토를 가져오는 우회는 허용하지 않는다. 기본 거점 전부가 보호·제외되어 출범할 자리가 없으면 어떻게 처리할지는 미정이며, 이를 이유로 보호를 풀거나 다른 지역을 임의로 가져오지 않는다.
- **판정 순서와 범위 분리:** 영토 후보의 보호·제외를 먼저 적용한 뒤 연결성과 배분을 판단하는 방향이다. 제외·보호된 주 자체를 편입해 연결을 만드는 방식은 허용하지 않는다. 구체적인 연결 경로 판정과 소유·통제 조회 시점은 후속 설계에 남긴다. 핵심주 부여 목록·병력 귀순 계산·영토 이전 목록은 각각 구분한다. 이번 영토 제외가 미정인 핵심주 목록이나 병력 공식을 확정한 것은 아니다.

한국 피감독국 출범, 기존 한국의 현존 16태그 대상 전쟁명분, 자동 선전포고·별도 공동 참전 미추가는 유지한다. 위 영토 후보 제한을 지원 대상·전쟁명분 대상의 축소나 지도 변경으로 확대하지 않는다. 해당 보호·제외·연결 규칙의 소스 적용과 실제 지도·효과·저장 검증은 모두 미수행이다.

### 구현 전에 남은 설계 항목

1. **중국 본토 핵심주 범위:** 현재 재건 결정의 목록 또는 CHI 코어 전체를 그대로 정답으로 확정하지 않았다. 현행 지도에서 포함할 주와 만주·타이완 등 경계 지역의 처리, 산둥의 현재 구성, 기존 후속 핵심주 부여와의 관계를 먼저 명세해야 한다. 이 방향은 중국 지도나 시작 소유권 전반을 변경하는 승인이 아니다.
2. **지지도 조회·분배:** 어느 중국국을 대상으로 언제 지지도를 읽을지, 실제 보유 영토·병력에 어떤 비율과 상하한·반올림을 적용할지 미정이다. 중국 16태그에는 CHI·PRC와 14군벌이 함께 있으므로 군벌만 조회할지 같은 지원 집합 전체를 조회할지도 구분해야 한다. 일본의 10–90% 공식을 중국 각국에 그대로 적용하거나, 군벌마다 고정 최소 영토·사단을 지급하는 방식은 확정하지 않았다.
3. **영토·병력 확보 방식:** 산둥과 연결되는 영토를 고르고 일본 측·만주·한국 소유 또는 통제 주를 제외하는 원칙은 위 추가 확정 항목으로 기록했다. 주 단위 배분·소국의 전 영토 상실·연결 확장 순서·제3국 점령·기본 거점 전체 차단 시의 처리는 미정이다. 최초 설명에서는 산둥 인접 영토안이 미채택 추천이었으나, 이번 후속 확인으로 연결 영토 원칙을 구체화했다. 병력은 별도 설계이며 실제 전력 이관 또는 신규 편성 여부, 귀순 공식·계수·상한·육해공 및 비축 장비 범위와 전국 병력 집결은 확정하지 않았다. 여러 내전국을 생성·병합하는 방식도 승인안이 아니다. 원소유국과의 관계 문제를 별도 자동 선전포고·공동 참전으로 해결하는 설계는 위 제외 사항을 따른다.
4. **피감독국·후속 결정 통합:** 설치 원본 피감독국 정의의 `allowed`에는 `Man the Guns` 조건이 있다. 해당 DLC 유무에 따른 생성·대체 정책은 아직 정하지 않았다. 기존 세력 편입과 한국의 무세력·비맹주 상태, 생성국 참조, `KOR_New_China_Government`의 CHI 종속·KCH 동맹 조건 및 합병·외형·핵심주 처리가 새 출범 방식과 맞는지도 후속 검토해야 한다. 이 문서화는 기존 결정 조건 완화나 기완료 저장의 소급 변경을 확정하지 않는다.

### 영향 처리와 이번 확인 범위

| 기능·사용처 | 이번 문서 처리 | 이후 필요한 확인 |
|---|---|---|
| `KOR_overthrow_the_chinese_dictators` 생성·핵심주·국가 지위 | 수정 방향 기록·코드 미적용 | 대상 주 목록·생성 scope·한국 피감독국 지위·DLC 경로 |
| 중국 지원 결정·공용 16태그 트리거 | 기존 지원 비용·기간·대상 검사는 유지, 후속 지지도 활용은 미정 | 최종 조회 집합·기존 지원과의 연결·지지도 경계 |
| 출범 영토의 연결·보호·제외 | 연결된 중국 영토 원칙, 일본 측·만주 제외와 한국 소유 또는 통제 주 보호를 문서에 확정·코드 미적용 | 실제 주 목록·기본 거점 차단·소유/통제 경계·연결 판정 |
| 한국의 기존 전쟁명분 | 의도적 유지 | 구현 시 기존 한국 actor·종류·현존 16태그 범위 보존 |
| 별도 자동 선전포고·공동 참전 연결 | 사용자 요청으로 제외 | 추가하지 않았는지 소스 차이 확인 |
| `KOR_New_China_Government`와 기완료 저장 | 통합·이관 정책 미확인, 현재 코드 유지 | 후속 결정과 출범 핵심주 중복·외교 조건·기존 저장 처리 |
| KCH 이름·효과 안내·언어 채널 | 기존 현지화 유지, 설명 변경은 미적용 | 구현 시 피감독국·핵심주·명분 안내와 양 채널·활성 영어 덮어쓰기 대조 |
| 바닐라 SND·일본 지원·민슈 잇키·정보국·배치·시각 자산 | 이번 후속 설계에서 제외 | 이번 문서가 해당 기능의 변경이나 새 검증을 뜻하지 않음 |

이번에는 관련 소스·기존 기록을 읽고 대화의 확정·미정·거절 사항을 문서와 대조했다. 새 게임·진단·게임플레이 검사·UI 관측·효과 실행·저장 비교를 하지 않았으며, helper·백업·새 증거 파일도 만들지 않았다. 문서 외 코드·현지화·이미지·설정은 편집하지 않았고 커밋·푸시·업로드를 수행하지 않았다. 기존 시험 PNG 4개는 별도 정리 미결이며 이번 범위에서 이동·삭제하지 않는다. 14절의 과거 native 검증을 이 미구현 설계의 검증으로 재사용하지 않는다.

<a id="17-shandong-government-implementation"></a>

## 17. 2026-11-19 산둥 자유 공화국 구현

이 절은 SND 전면 편입 전 최초 출범 구현과 그 소스의 실행 이력이다. 현재 계약·후속 검증은 [19절](#19-shandong-warlord-integration-implementation)을 먼저 읽는다.

사용자가 16절의 설명을 인용한 뒤 원본·원작·로그 위치를 제공하고 `AGENTS.md, /docs 읽고 구현해줘`라고 요청했다. 이 단계는 앞선 설명·문서화 전용과 구분되는 **계속개발 구현**이다. 미정이던 항목은 아래처럼 구체화했으며 기존 ID·기간·AI·배치·이미지와 중국 지원 결정의 비용·기간·16태그 범위는 보존한다. Git 커밋·푸시·업로드는 이번 승인에 포함되지 않는다.

### 기준과 파일 역할

- 작업 소스는 `C:\hoi\hearts_of_korea`, 브랜치 `feat/korean-focus-expansion-ai`, HEAD `0c19f58fa7a9ff898196dcdbe46edfd0ad5fdbbc`의 기존 미커밋 작업이다. 설치 원본은 `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV`, 버전은 `Operation Postern v1.19.5.0.7c6c (c184)`다. 원작 Workshop `2898629778`은 읽기 전용 출처이며 작업·업로드 대상이 아니다.
- launcher 개발 pointer는 저장소를 직접 로드한다. 시작 설정은 HOK → 외부 English 번역이며 `disabled_dlcs`는 빈 배열이다. 해당 설정과 실제 native DLC 조회·시험 선택은 서로 구분한다.
- 실제 사용자 데이터는 `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV`다. 이번 외부 TASK는 `C:\hoi\test\hok-shandong-democratic-government-20261119-01\`이며 `baseline-source/`에 편집 전 7파일, `source-baseline.json`에 runtime 1,591파일 해시·Git 상태가 있다. `runtime/baseline/`에는 현재 로그, 실제 설정·이어하기 색인 등 11원본의 검증 사본과 **기존 저장 124개·약 9.10GB**의 해시 목록을 보존했다. 이전 작업의 109개와 이번 124개를 같은 기준선으로 표시하지 않는다.

| 파일 | 현행 역할 |
|---|---|
| [기존 한국 중점](../common/national_focus/korea.txt)의 `KOR_overthrow_the_chinese_dictators` | MtG·KCH 부재·적격 거점 조건과 진행 중 무효화 취소, 고유 효과 안내·결정 해금, 새 형성 helper 호출. 기존 한국의 16태그 전쟁명분 루프 유지 |
| [새 지리·안전 트리거](../common/scripted_triggers/HOK_KOR_chinese_government_state_triggers.txt) | 본토 63주·중국 donor·소유/통제 보호·형성 가능 여부 |
| [새 형성 효과](../common/scripted_effects/HOK_KOR_chinese_government_effects.txt) | 지지도·주 수 snapshot, 연결 선택, 한 생성국의 핵심주·거점·병력·피감독 지위와 임시 상태 정리 |
| [기존 중국 인정 결정](../common/decisions/KOR_decision.txt)의 `KOR_New_China_Government` | 기존 조건·CHI 합병·국가명·비용을 보존하고 핵심주 처리를 공통 63주 helper로 연결 |
| 기존 `korea_focus_l_korean.yml`·`korea_focus_l_english.yml` | 기존 중국 축출 설명·효과 키의 한국어 본문 갱신, 나머지 키 보존 |
| 새 `HOK_KOR_chinese_government_l_korean.yml`·`HOK_KOR_chinese_government_l_english.yml` | 가용 안내 3키와 고유 `HOK_KOR_chinese_government_effect_tt`. 본체 두 채널의 한국어 본문 계약·BOM 유지 |

### 지리·보호와 거점

본토 지리 집합은 기존 KCH 재건 핵심주와 현행 CHI 분할을 대조한 **63주**다. 기존 집합에서 326·591·610·728·729를 제외하고 283·287·743·759·760을 보완했다. 601 참도는 현 CHI 코어가 아니라 TIB 소유지만 기존 KCH 본토 핵심주 범위를 보존해 유지한다. 핵심주를 부여해도 소유권은 이전하지 않으며, TIB는 16태그 donor가 아니므로 이 핵심주만으로 TIB 영토·병력을 가져오지 않는다.

만주 제외는 328·610·714·715·716·717·745·761이다. 타이완 524·하이난 591·홍콩 326·광저우만 728·마카오 729도 본토 편입 집합에서 제외했다. 지리 목록·원본/프로젝트 파일·해시·현지명·접경 근거는 [유지되는 범위·출처 목록](data/HOK_KOREAN_CHINESE_GOVERNMENT_STATE_GROUPS.json)에 둔다.

형성·추가 편입은 중국 지원 대상 16태그 중 현존 비동적 국가만 대상으로 하며 일본 직접·2단계 종속 관계를 제외한다. **소유국과 통제국 모두 적격 중국 donor여야 하고, 한국 소유 또는 한국 통제 중인 주는 어느 한 조건만 충족해도 차단**한다. 여기에 `is_fully_controlled_by = CONTROLLER`를 요구해 주 전체를 현재 중국 측 통제국 한 곳이 완전히 통제해야 한다. 한국·일본 또는 다른 국가가 일부 프로빈스만 통제하는 혼합 통제 주도 통째로 제외한다. 이 검사는 최초 산둥 거점에도 적용하고 실제 추가 이전 직전에 재확인한다. 최초 부분 통제 진단에서 대표 통제국과 `is_controlled_by`만으로는 한국·일본의 비승점 프로빈스 점령을 놓치는 두 실패를 확인해 강화했다. 교정 후에는 실제 중점 보상 실행 뒤에도 한국 1084·일본 1001 프로빈스 통제와 해당 주 1038·598의 원소유가 보존되는 것을 확인했다. 일본 소유·점령지, 만주국 등 일본 측 영토와 한국 점령지를 핵심주 또는 기본 보상이라는 이유로 가져오지 않는다.

기본 거점은 적격인 597·743이다. 597은 743·1038·598과 육지로 접하고 743은 597에만 접한다. 따라서 597이 차단되어 743만 출범하면 그 보호된 597을 경유해 내륙을 편입하지 않는다. 본토 63주 안에는 바닐라 해상 특별 인접 쌍이 없고 하이난 연결의 상대 주 591도 제외된다. 엔진 이웃 판정과 실제 편입의 대조는 native 검증에서 구분한다.

MtG가 없거나 기존 KCH가 있거나, 안전한 최초 거점의 원소유국을 병력 이관까지 유지할 수 없으면 중점 착수를 막는다. 최초 거점은 적격 597·743 중 원소유국이 다른 주 1개 이상을 보유한 곳만 사용할 수 있다. 597이 이 조건을 만족하면 먼저 사용하고, 아니면 743을 먼저 확보한다. 원소유국의 마지막 주가 되는 거점은 병력 이관 뒤 이전하므로 한 주짜리 군벌도 다른 최초 거점이 있으면 참여할 수 있다. 두 거점 모두 단일 주 국가의 마지막 영토이거나 보호·제외되어 최초 거점을 잡을 수 없으면 차단한다. 진행 도중 조건을 잃으면 취소한다. 강제 보상 호출에서도 형성 helper는 같은 조건을 다시 확인한다. 일반 puppet은 참전 거절·인력 공유 등 규칙이 피감독국과 다르므로 자동 대체하지 않는다. 기존 KCH를 덮어쓰거나 새 clone을 추가로 만들지 않는다.

### 지지도·영토·병력의 실행 순서

1. 한국 scope에서 현존 적격 국가의 중점 완료 시 민주주의 지지도를 `p = min(0.90, max(0, 지지도))`로 읽고, 보호·제외를 통과하는 소유 주 수 `N`을 snapshot한다. 지지도를 합산하거나 군벌별 최소 사단을 새로 지급하지 않는다.
2. 국가별 영토 예산은 `N × p`다. 적격 597·743은 기본 거점으로 선택하면서 원소유국의 예산에서 각각 1씩 차감한다. 추가 주는 남은 예산이 1 이상일 때만 고르므로 추가 이전 상한은 `max(0, floor(N × p) − 기본 거점 수)`다. 기본 거점 자체는 이 정수 예산보다 클 수 있다.
3. 후보 주가 이미 선택한 영토와 이웃인지 확인하며 범위를 늘린다. 이전할 주를 모두 선택하기 전에는 소유권을 바꾸지 않으므로 다른 국가의 수치·소유권 변화로 뒤의 배분이 재계산되지 않는다. 한 번의 형성에 최대 63회, 진척이 없으면 즉시 종료하는 제한 루프를 사용한다. 멀리 떨어진 주나 보호·제외 주를 빼앗아 예산을 억지로 채우지 않는다. `every_state`의 평가 순서가 최종 선정에 미치는 영향과 정확한 엔진 배분은 native 증거로 따로 기록한다.
4. `original_tag = KCH`인 동적 국가 하나를 만들고 **실제 생성국을 임시 global event target으로 저장하고 효과 종료 전에 지운다**. 최초 native 실행에서 생성 자식의 local event target이 바깥으로 전달되지 않는 것을 확인해 교정한 방식이다. 민주정부와 63주 핵심주를 설정하며 먼저 원소유국이 즉시 소멸하지 않는 안전한 거점과 그 수도를 지정한다. 이 절의 KCH는 바닐라 SND와 다른 국가다.
5. 실제 선택된 영토가 있는 국가만 donor가 된다. 사용자가 후속 선택에서 **육해공군을 같은 비율로 귀순**시키기로 명시했다. 따라서 `p > 0`인 참여국에만 `size`·육군·해군·공군·비축 장비/연료 비율을 모두 `p`로 명시하고 기존 지휘관은 원국에 유지한다. 지지도가 0이면 이관 명령 자체를 실행하지 않는다. 주·사단·함정·항공기 수는 엔진의 단위별 분배·반올림을 따르므로 각 수량의 정확한 비례나 특정 함선의 귀순을 보장하지 않는다. 무작위 고정 사단 생성이나 전국의 고립 국가에서 병력만 가져오는 보상은 넣지 않는다. 최초 검증에서는 첫 거점 이전으로 소멸한 donor의 병력 이관이 엔진에서 거부됐고, 영토 0인 새 수혜국에 병력을 먼저 주는 통제도 거부됐다. 따라서 위 최초 거점 선택 조건으로 이관 시점까지 모든 참여국과 수혜국이 실제 영토를 갖도록 순서를 교정했다. 교정 후 단일 주 donor도 다른 안전한 거점과 최소 공군 기지가 확보된 최종 native 사례에서 실제 귀순 뒤 마지막 주를 이전하는 것을 확인했다.

   공군 이관은 수혜국 자체 비행장이 있어야 실제 실행되는 조건을 독립 통제로 확인했다. 양수 p의 참여국에 배치 공군이 있을 때, 이미 선택한 주 중 기존 비행장이 있고 이전 뒤에도 원소유국이 남는 주를 먼저 확보한다. 영토 예산을 재차 차감하지 않으며 보호·연결 조건도 우회하지 않는다. 그러한 기존 기지가 없으면 이미 확보한 수도 거점에 비행장 1단계만 즉시 보충한다. 이는 공군 귀순을 성립시키는 의도적인 최소 건물 지원이며 기존 기지를 사용할 수 있거나 귀순할 배치 공군이 없을 때는 새 기지를 추가하지 않는다. 한국·동맹의 기지 접근권만으로는 이관되지 않는 별도 통제도 확인했다. 최종 native에서는 기존 기지 재사용·수도 기지 보충·단일 주 기지 donor·0% 무기지의 각 경로를 구분해 재검증했다.

6. 나머지 선택 영토를 새 정부로 이전하고 한국을 종주국으로 `autonomy_supervised_state`를 설정한다. `end_wars = no`·`end_civil_wars = no`로 기존 전쟁을 임의 종료하지 않으며 기존 세력 편입을 연결한다. 최종 별도 사례에서 한국 무세력(NCNS 제외) 출범과 비맹주 상태의 후속 인정까지 확인했다. 모든 DLC 조합을 확인한 것은 아니다.
7. 선택·후보 state flag와 국가의 snapshot·참여 표식·비율·예산 및 한국의 루프 변수를 같은 효과 안에서 정리한다. 소멸 donor도 포함하기 위해 병력 이관과 국가 정리에 `every_possible_country`를 사용한다. 매일 실행되는 on_action이나 영구 지지도 누적 변수를 만들지 않는다.

형성 helper 밖의 기존 루프가 한국에 현존 16태그 대상 괴뢰화 전쟁명분을 준다. 해당 대상 필터·한국 actor·명분 종류는 보존했다. **`start_civil_war`·`declare_war_on`·`add_to_war` 또는 자동 참전 on_action은 추가하지 않았다.** 피감독국의 참전은 일반 외교 규칙을 따른다.

### 후속 결정·표시·기존 저장

중국 인정 결정은 기존처럼 CHI만 합병하고 `KCH_china` 외형으로 바꾼다. 한국 독립·KCH와 같은 세력·CHI가 한국 종속국이라는 조건과 비용 0·일회성은 유지한다. 군벌 전체 합병·조건 완화·기존 완료 이력 초기화는 하지 않는다. 새 핵심주 helper를 재사용하지만 기존 저장에 이미 있는 추가 핵심주를 제거하지 않으며 기완료 중점 보상도 자동 소급하지 않는다.

초기 육군·비축만 귀순시키는 구현에서는 해군 비율 0을 명시해도 함정이 옮겨지는 엔진 결과를 확인했다. 기본 `size = 0`, 별칭 `naval_ratio`, 변수 0 입력 가설도 분리 통제로 검토했지만 보존을 입증하지 못했다. 이후 미정이던 범위에 대해 사용자가 육해공 동일 비율을 선택했으므로 현재 계약은 위 공통 비율이며, 해공군 원국 유지 안내는 제거했다. 이전 해군 보존 실패를 최종 공통 비율 검증으로 바꾸어 표시하지 않는다.

가용 3키는 초기 편집에서 기존 `korea_focus` paired 파일에 넣었다가, 활성 영어 번역의 동명 파일 덮어쓰기에서도 남도록 새 dedicated paired 파일로 옮겼다. 새 고유 효과 안내도 이 파일에 둔다. 현재 외부 번역에는 동명 dedicated 파일이 없다. 외부 번역의 영어 채널에는 원래 `_desc`의 오래된 본문이 남아 있다. 다만 원래 두 모드 구성의 실제 `l_korean` UI에서는 새 한국어 설명·고유 효과 안내·가용 조건이 표시됐다. 영어 채널 UI는 별도 미검증이며 외부 저장소는 수정하지 않았다. 현지화 최초 쓰기의 PowerShell 대소문자 변수 충돌은 발견 직후 외부 baseline 원문에서 교정했고 잘못된 중간 파일·교정 범위는 TASK의 `localisation/first-write-error/`·`source-checks.json`에 보존했다.

이번 변경에는 새 중점·국민정신·결정·아이콘·좌표·AI 가중치가 없으며 기존 시각 자산을 유지한다. 지도 파일·원본·Workshop 설치본은 편집하지 않는다.

### 검증 상태와 증거

현재 상태는 **구현·핵심 엔진·실제 UI·새 저장 재로드 확인**이다. 최종 같은 8개 runtime 파일을 고정한 6개의 독립 native 사례에서 낮은/높은 지지도, 기존 비행장 재사용·수도 기지 보충·단일 주 donor·0% 귀순, NCNS 제외 무세력 출범, 비맹주의 CHI 한정 후속 인정을 확인했다. 낮은 20%와 높은 70% 사례는 같은 초기 전력에서 KCH의 7주·21사단·4함·26기와 42주·170사단·6함·185기로 차이를 보였다. 각 검사는 관측 범위가 달라 소스 검사나 이전 실행의 PASS 수와 합산하지 않는다. 보호·고립·중복·차단과 실제 부분 프로빈스 통제 검사는 해당 소스·조건을 실행 기록에서 따로 구분한다.

실제 UI에서 중점을 직접 시작해 보통 시간 진행으로 완료했고, 새 가용 조건·효과·인정 결정 해금과 산둥 자유 공화국의 민주정부·한국 피감독국 표시를 확인했다. 선행 조건·정치·지지도는 외부 fixture로 준비한 실행이므로 지원 결정 누적과 전체 정치 경로의 정상 완주를 주장하지 않는다. 원래 HOK→외부 영어 번역 구성의 새 프로세스에서 첫 UI 저장을 실제 불러와 같은 지위와 완료 중점을 확인한 뒤 1936.2.21.3까지 진행하고 다시 저장했다. 첫 텍스트 저장에서는 본토 63코어·42주 및 효과용 임시 표식/변수·global target 부재를 판독했다. 둘째 저장은 원래 설정에 따른 HOI4bin5 원본으로 보존했으며 내부 구조 재판독이나 둘째 파일의 재로드는 하지 않았다.

이 사용자 데이터 경로에서는 두 UI 저장 모두 정상 이름으로의 rename 오류로 `_temp.hoi4`가 남았다. 첫 `_temp`의 실제 재로드는 성공했지만 이름 변경 오류 자체를 해결한 것은 아니다. 정확한 35일 달력 경과·진행 중 조건 상실 취소·영어 채널 UI·MtG 미보유 실행·기존 캠페인 저장 호환·장기 AI·멀티플레이는 미검증이다. 설정·기존 저장·프로세스·Steam의 최종 정리 결과는 아래 구현 기록을 따른다.

검증 결과와 소스 해시·baseline 대비 로그·실제 저장·UI·정상 진행·설정 복원·소유 프로세스 종료는 [이번 구현 기록](incidents/2026-11-19-shandong-democratic-government.md) 및 TASK의 `runtime/`에 기록한다. 과거 14절의 69/0 또는 다른 소스의 결과를 이번 통과로 표시하지 않는다. 기존 시험 PNG 4개는 별도 정리 미결이며 이번 작업에서 이동·삭제하지 않는다.

<a id="18-shandong-warlord-integration-design"></a>

## 18. 2026-11-19 산둥군벌 영토 기본 편입 후속안 — 문서화만·미구현

### 요청과 현행 구현의 구분

사용자는 별도로 존재하는 산둥군벌 SND의 영토를 산둥 자유 공화국 출범 때 전부 편입하는 안을 제안했고, 설명을 받은 뒤 **「문서화 작업만 진행해줘」**라고 요청했다. 이번 범위는 아래 후속 설계와 2차 확장 계획의 안내 갱신이다. 17절의 기존 구현을 보존하며, 이번 요청은 코드·현지화·지도·설정 변경이나 게임 실행·테스트·정리·커밋·푸시·업로드를 승인하지 않는다.

문서화 당시 기준은 `C:\hoi\hearts_of_korea`, 브랜치 `feat/korean-focus-expansion-ai`, HEAD `0c19f58fa7a9ff898196dcdbe46edfd0ad5fdbbc`의 기존 미커밋 작업이다. 당시 실행 효과는 17절의 계약이었으며 SND 영토 전면 편입은 반영되지 않았다. 후속 구현은 19절로 구분한다. 이 후속안의 대상·표시를 변경할 때는 [변경 영향 검토 절차](HOK_CHANGE_COVERAGE_REVIEW.md), [주 참조 검토 스킬](../.agents/skills/hok-state-reference-review/SKILL.md), [현지화 검토 스킬](../.agents/skills/hok-localisation-review/SKILL.md)을 먼저 읽는다.

### 현재 소스에서 확인한 출발점

설치 원본은 17절과 같은 `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV`이며 설치 메타데이터 기준 버전은 `Operation Postern v1.19.5.0.7c6c (c184)`다. 아래는 **1936년 시작·No Compromise, No Surrender 활성 조건의 소스 확인**으로, 새 실행 관측이 아니다. 저장소에는 아래 세 주와 SND 국가 이력의 덮어쓰기 파일이 없고, 현재 descriptor에 `replace_path`도 없어 설치본을 상속한다.

| 대상 | 설치 원본의 위치·의미 | 현행 출범 효과와 차이 |
|---|---|---|
| 산둥 597 | `history/states/597-Shandong.txt` 18–24행: DLC 조건에서 SND로 이전 | 현재도 보호 조건을 통과하면 기본 거점 |
| 지난 1038 | `history/states/1038 - Jinan.txt` 18–24행: 같은 조건에서 SND로 이전. `history/countries/SND - Shandong.txt` 1행은 수도 1038 | 현재는 SND의 지지도 예산·육지 연결에 따른 추가 편입 대상이라 SND에 남을 수 있음 |
| 칭다오 743 | `history/states/743-Qingdao.txt` 11행은 CHI 소유, 14–19행은 DLC 조건의 SND 핵심주 부여 | 현재도 보호 조건을 통과하면 기본 거점. SND 핵심주라는 이유로 SND 소유라고 기록하지 않음 |

[현행 출범 효과](../common/scripted_effects/HOK_KOR_chinese_government_effects.txt)는 597·743을 기본 선택한 뒤 원소유국의 지지도 예산에서 차감하고, 나머지를 연결된 주 중에서 고른다. 따라서 정상 시작의 SND 본거지인 597·1038 전부를 기본 지급하는 규칙과는 다르다. SND와 출범국 KCH는 별도 국가이며 이 구분과 안정 ID를 유지한다.

### 기록할 후속 방향

1. **SND 영토를 새 정부의 기본 기반으로 편입한다.** 「중국 독재자 축출」 완료로 KCH가 출범할 때, 그 시점에 SND가 실제 소유한 영토를 기본 편입 대상으로 삼고 SND의 민주주의 지지도에 따른 영토 예산은 적용하지 않는 방향이다. SND 핵심주 전체를 다른 소유국에서 가져오는 규칙은 아니다. 시작 소유가 그대로이고 보호 조건을 통과한다면 597·1038이 기본 편입된다. 본거지 밖 정복지·고립지와 기존 지리·연결 제한의 우선순위는 아래 미정 항목을 따른다.
2. **기존 칭다오 거점을 유지한다.** 743이 CHI 소유인 경우에도 기존 보호·적격 조건을 통과하면 기본 편입하는 방향이다. 이에 따라 위 정상 시작 조건에서 예상하는 기본 영토는 597·1038·743의 세 주다. 이 세 주가 어떤 소유·점령 상태에서도 무조건 지급된다는 뜻은 아니다.
3. **다른 중국 국가의 영토는 지지도에 따라 추가 편입한다.** 기존 중국 지원 대상 16태그와 본토 63주 집합을 기준으로, 민주주의 지지도·원소유국별 예산·육지 연결에 따른 추가 편입을 유지한다. SND의 기본 편입을 이유로 CHI나 다른 군벌의 영토 전부를 넘기지 않는다. 기본 영토가 늘어남에 따라 연결 후보가 달라질 수 있으므로 예전 실행의 주 수를 새 기대값으로 재사용하지 않는다.
4. **병력·비축 귀순은 기존 지지도 규칙을 유지한다.** 영토가 실제 편입되는 국가의 양수 지지도 비율 p(최대 90%)를 육군·해군·공군·비축 장비·연료에 공통 적용하고, 기존 지휘관은 원국에 유지하는 계약을 보존하는 방향이다. SND 영토 전부 편입이 전력 100% 귀순을 뜻하지 않는다. p=0의 이관 명령 생략과 SND 소멸 후 잔여 전력의 실제 처리는 구분하며 후자는 미확인이다.
5. **기존 보호 규칙을 우선한다.** 한국 소유 또는 통제 지역, 일본 및 일본 측 종속국의 소유·통제 지역, 만주 등 기존 제외 지역은 기본 편입에서도 가져오지 않는다. 부분 프로빈스 점령을 포함한 완전 통제 검사도 유지한다. 보호 때문에 SND 영토가 남는 경우에는 SND 소멸을 보장하지 않으며, 남은 주를 합병 효과로 우회 취득하지 않는다.
6. 기존 한국 피감독국 지위·본토 핵심주·칭다오 거점·전쟁명분과 「하나의 중국 인정」의 CHI 한정 합병 계약을 유지한다. 자동 선전포고·별도 공동 참전·다른 군벌의 일괄 합병·기완료 저장 소급 처리는 추가하지 않는다. 중점 ID·기간·선행·AI·배치·시각 자산과 지도 자체의 변경도 이 후속 방향에 포함하지 않는다.

### 영향 후보와 처리 구분

아래의 `수정`은 **후속 구현 때 필요한 제안**이며 이번에 해당 코드를 바꿨다는 뜻이 아니다.

| 후보·경로 | 처리 | 의도·현재 근거와 남은 확인 |
|---|---|---|
| 출범 helper의 SND 기본 선택·1038 및 SND 소유 주 | 수정 — 제안 | 지지도 예산과 별도로 기본 편입하도록 설계. 현재는 597·743만 기본 선택 |
| 기존 743 거점과 CHI의 나머지 영토 | 의도적 유지 | 743의 별도 기본 거점은 유지하고 다른 CHI 영토는 기존 지지도·연결 규칙 적용 |
| 타 중국 donor·16태그 공용 필터·본토/보호 트리거 | 의도적 유지 | [donor·지리·보호 트리거](../common/scripted_triggers/HOK_KOR_chinese_government_state_triggers.txt)와 [16태그 필터](../common/scripted_triggers/HOK_KOR_chinese_democratic_support_triggers.txt)가 기준. 본거지 밖 SND 영토와의 충돌은 아래 미정 항목 |
| 중점의 가용·유지·취소와 최초 거점·공군기지·마지막 주 이전 | 미확인 | [중점 호출부](../common/national_focus/korea.txt)의 `KOR_overthrow_the_chinese_dictators`와 형성 helper의 안전한 첫 거점 조건을 함께 검토해야 함. 현행 생존 donor·기지 확보 순서가 전면 편입에서도 성립하는지 미검증 |
| 전력 이관·SND 소멸·임시 표식 정리 | 의도적 유지 / 소멸 시 실제 결과 미확인 | 지지도 비율·이관 후 마지막 주 이전·효과 내 정리 원칙 유지. 소멸에 따른 잔여 자산 자동처리가 비율 계약을 훼손하는지 확인 필요 |
| 중점 효과·설명·가용 안내 | 수정 — 제안 / 조건 문구 미확인 | `HOK_KOR_chinese_government_effect_tt`, 기존 `KOR_overthrow_the_chinese_dictators_tt`·`_desc`와 가용 안내를 대조할 대상. 본체 `HOK_KOR_chinese_government_l_*`·`korea_focus_l_*`의 두 채널 및 외부 번역 경로를 함께 다뤄 기본 편입과 비례 귀순을 구분해야 함 |
| 후속 인정 결정·기존 저장 | 의도적 유지 | [기존 결정](../common/decisions/KOR_decision.txt)의 `KOR_New_China_Government`는 CHI 한정 합병과 공용 63주 핵심주 부여 유지. 기완료 보상 자동 소급 없음 |
| SND 시작 이력·상속 군벌 콘텐츠·지도·시각 자산 | 제외 — 변경 대상 아님 | 시작 영토나 SND 태그를 사전에 없애는 안이 아님. 후속 구현에서는 상속 사건·on_action의 SND 존재/부재 접점을 읽어야 하며 재생성 불가를 이번에 입증하지 않음 |

현행 중점은 고유 효과 키를 사용하며, [기존 한국어 효과 안내](../localisation/korean/HOK_KOR_chinese_government_l_korean.yml)는 아직 모든 기본 거점을 지지도 예산에서 차감하는 기존 규칙을 설명한다. 외부 번역 위치는 17절의 `C:\hoi\Hearts of Korea English Translation Anime Modder's Edition`이며 동명 `localisation/english/korea_focus_l_english.yml`에는 이전 `_tt`·`_desc` 본문이 남아 있다. 후속 표시를 구현할 때 [두 채널 계약](incidents/2026-09-01-localisation-contract.md)을 먼저 읽고 본체의 전용 키·기존 키와 활성 번역을 함께 대조한다. 이번에는 이 파일들을 수정하거나 새 UI 관측을 하지 않았다.

### 구현 전 남은 결정과 검증 범위

- **본거지 밖 소유지:** SND 소유 영토 전부를 기본 기반으로 삼는 방향을 597·1038 두 주만의 고정 지급으로 축소 확정하지 않는다. 다만 SND가 정복한 고립지나 현행 63주 집합 밖 영토가 있으면 기존 육지 연결·지리 제외 원칙과 충돌하므로 적용 우선순위를 구현 전에 확정해야 한다. 만주·한국·일본 측 영토 보호를 풀어 해결하지 않는다.
- **SND 부재·보호된 거점:** NCNS 비활성 또는 전쟁·합병으로 SND가 없는 경우, SND 영토가 전부 보호 대상인 경우, 최초 거점이 마지막 주인 경우의 가용·취소·출범 경로는 미정이다. 현행 597·743 경로가 있다는 사실을 새 설계의 확정 대체 경로로 바꾸어 기록하지 않는다.
- **귀순과 국가 소멸:** 병력 이관 전에 원국을 소멸시키지 않는 원칙과 수혜국의 영토·공군기지 확보 조건을 함께 만족하도록 순서를 구체화해야 한다. 낮은 지지도·0%에서 SND 잔여 부대·함정·항공기·비축이 어떻게 처리되는지는 새 전면 편입 조건에서 확인하지 않았다. 지휘관 원국 유지 계약과 소멸의 관계도 미확인이다.
- **후속 검증:** 구현이 별도로 승인되면 기본 세 주·낮은/높은/0% 지지도·한국/일본의 전체 및 부분 점령·SND 부재/확장·마지막 주·전력과 비축의 실제 전후 값을 구분하고, 중점 착수/취소·완료 UI·새 저장 왕복을 변경 범위에 맞춰 선정한다. 이는 예정 항목이며 이번에 실행한 검사가 아니다.

이번 완료 범위는 기존 문서·관련 소스의 읽기 대조와 이 절·2차 확장 계획의 안내 문장 확인이다. 게임플레이 검사·게임 실행·로그/저장 분석은 수행하지 않았고, 새 시험 산출물이나 helper·백업을 만들지 않았다. [17절의 구현 기록](incidents/2026-11-19-shandong-democratic-government.md)과 외부 `C:\hoi\test\hok-shandong-democratic-government-20261119-01\`은 **이전 소스의 증거**이며 이번 설계의 검증 자료가 아니다. 기존 저장소 시험 PNG 4개는 같은 기록의 위치 목록대로 정리 미결이며 이번 문서화에서 이동·삭제하지 않는다.

<a id="19-shandong-warlord-integration-implementation"></a>

## 19. 2026-11-19 산둥군벌 영토 기본 편입 구현

18절의 문서화·후속 설명 뒤 사용자가 전체 흐름을 인용하고 `AGENTS.md, /docs 읽고 구현해줘`라고 요청하여 **계속개발 구현**으로 전환했다. 이전 문서화 범위를 구현 승인으로 소급하지 않는다. 현재 상태는 **구현·핵심 엔진·실제 중점 UI·새 저장 왕복 확인**이며, 실제 검증·복원 결과는 [이번 기록](incidents/2026-11-19-shandong-full-integration.md)을 따른다. 최종 production 5사례·실제 시작/시간 진행/완료·원래 모드 구성의 새 저장 재로드 뒤 79게임시간 진행/재저장을 확인했고 기존 저장 157개·profile 11개와 Steam 플레이 상태도 보존·복원했다. `_temp` rename 오류와 기존 캠페인·장기·멀티 등의 미검증 범위는 구분한다.

### 현행 계약과 이전 미정 항목의 결정

- 기존 적격 597·743을 기본 선택하고, 기존 본토 63주 집합·완전 통제·한국/일본 측 보호 검사를 통과한 **SND 실제 소유 주 전부**를 지지도와 무관하게 기본 선택한다. 1936년 시작 구성이 유지되면 597·1038·743 세 주가 기본 기반이다. 1038의 역할은 이전 추가 후보에서 SND 소유일 때의 기본 편입으로 바뀌었으며 독립 bootstrap 거점은 아니다.
- SND의 **적격 본토 정복지·고립지도 포함**하고, 기존 지리 집합 밖·만주·한국/일본 보호 지역은 제외한다. 다른 중국국의 추가 영토는 이 새 기본 영토와 육지로 연결된 곳에서 기존 국가별 지지도 예산으로 고른다. 고립 SND 영토도 확장 출발점이 될 수 있는 의도적 차이다.
- SND 부재 시 기존 597·743 fallback을 유지한다. 둘 다 안전한 첫 거점이 아니면 기존처럼 차단한다. MtG·KCH 부재·진행 중 조건 상실 취소·35일·AI·배치·기존 전쟁명분은 보존한다.
- 선택 완료 → KCH 생성·63주 핵심주 → 안전한 거점·공군기지 → 참여국의 양수 지지도 p(최대 90%)로 육해공·비축/연료 귀순 → 소멸이 확실한 SND의 미귀순 장비·수송선·연료 처리 → 마지막 주를 포함한 나머지 영토 이전 → 한국 피감독국·세력 → 임시 자료 정리 순서다. p=0은 이관 명령을 생략하며 지휘관은 귀순 대상에서 제외한다. 잔여 처리는 참여 SND의 남은 소유 주가 하나 이상이고 모두 선택·현재 이전 가능할 때만 적용하며, 보호 주가 남은 SND와 다른 국가는 처리하지 않는다. 이는 소멸의 자동 자산 추가 승계를 막기 위한 보정이다. 입력 비율과 함정 등 실제 단위별 수량·소멸 뒤 지휘관 처리는 구분한다.
- 기존 CHI 한정 인정 결정·기완료 보상 비소급·지도·시작 이력·다른 분기와 시각 자산을 보존한다. 자동 전쟁·별도 공동 참전을 추가하지 않는다.

최종 zero/high·실제 UI 첫/재로드 후 저장 4개에서 기존 SND 군 지휘관 두 명이 SND 역사/지휘관 기록에 남고 D04/KCH 명부에는 자동 등록되지 않은 것을 확인했다. 이 관측은 지휘관의 사후 생존이나 UI 선택 가능성을 보장하지 않는다. 세부 ID·저장별 출처는 이번 구현 기록과 외부 `source-review/snd-commander-final-save-readback.json`을 따른다.

### 파일·출처·검증의 구분

이번 runtime 변경은 [출범 효과](../common/scripted_effects/HOK_KOR_chinese_government_effects.txt) 1파일과 기존/고유 효과 안내 paired 4파일이다. 효과에는 후보·미선택·소유국 SND를 검사하는 9줄과, 비례 귀순 뒤 소멸 예정 SND의 잔여 자산만 처리하는 24줄을 추가했다. 수송선만은 공식 getter와 음수 장비 효과로 별도 처리하고 새 값에는 비영속 임시 변수 API를 쓴다. 트리거·중점 호출부·인정 결정은 이번 시작 baseline과 바이트 동일하게 유지한다. 현지화는 본체 두 채널의 한국어 본문·BOM·줄끝을 보존하며 설명 `_desc`와 가용 안내는 유지한다. 효과에는 SND 소멸 때의 미귀순 장비·수송선·연료 폐기를 명시했다. 외부 번역의 기존 영어 본문은 이번 수정 대상이 아니며 고유 효과 키·실제 UI·영어 채널 한계를 각각 기록한다.

이번 외부 TASK는 `C:\hoi\test\hok-shandong-full-integration-20261119-01\`이다. `source-baseline.json`·`baseline-source/`는 편집 전 runtime 1,595파일 해시와 관련 13파일 사본, `runtime/baseline/`는 profile·로그 사본과 기존 저장 **157개·약 11.44GB**의 위치·해시 목록이다. 이전 `C:\hoi\test\hok-shandong-democratic-government-20261119-01\`과 그 시작의 124개 저장은 별도 시점의 기록이다. helper·probe·시험 저장 증거·UI·검사 출력은 이번 외부 TASK를 사용하며 기존 자료를 이동하지 않는다.

최종 효과의 정확한 두 삽입·총 33줄 delta와 기존 가용/취소·트리거 보존은 `source-review/implementation-final-r3-delta.json`, 최종 현지화는 `source-review/localisation-review-final-r3.json`을 따른다. 최초 9줄 소스·27줄 r2와 소멸 보정 최종 r3의 관측을 구분한다. 독립 소멸 통제, production 형성, 실제 UI·정상 중점 진행·새 저장 왕복·설정/기존 저장/프로세스/Steam 복원은 [이번 구현 기록](incidents/2026-11-19-shandong-full-integration.md)에서 실제 수행 여부와 결과를 구분한다. 이전 17절의 성공 횟수나 UI를 이번 소스 결과로 재사용하지 않는다. 기존 시험 PNG 4개는 별도 정리 미결이며 이 작업에서도 이동·삭제하지 않는다.

<a id="20-shandong-weng-wenhao-leader-design"></a>

## 20. 2026-11-19 산둥 지도자 웡원하오 지정안 — 초기 문서화 이력

사용자는 장쥔마이 검토 뒤 **웡원하오(Weng Wenhao)를 산둥 자유 공화국 지도자로 사용**하기로 선택했다. 중국과 산둥에 같은 인물이 동시에 등장하는 것을 명시적으로 허용했고, 변경 대상은 산둥 지도자뿐이라고 한정한 다음 `문서화 작업만 진행해줘`라고 요청했다. 이 절을 처음 작성한 당시 상태는 **설계 결정 기록 / 게임 코드·현지화·에셋 미수정 / 지도자 지정 미구현**이었다. 이 초기 문서화 자체는 구현·실행 승인이 아니며, 이후 별도 승인과 구현은 [21절](#21-shandong-weng-wenhao-leader-implementation)에 구분한다.

당시 [출범 효과](../common/scripted_effects/HOK_KOR_chinese_government_effects.txt)는 민주정부를 만들지만 웡원하오를 지정하지 않았다. [이전 실제 UI·저장 기록](incidents/2026-11-19-shandong-full-integration.md)에서 확인한 지도자는 `D04_huang_tian` / Huang Tian과 `GFX_portrait_asia_generic_4`였으며, 이는 그 실행에서 자동 생성된 사례이지 고정 지도자 이름이 아니다. 초기 문서화 단계에서는 그 소스를 수정하지 않았다.

### 확정한 범위

- 산둥 전용 캐릭터 ID에 원본 웡원하오의 이름·초상화와 예전 민주주의 지도자 역할을 재사용하는 방향이다. 실제 ID는 구현 때 기존 프로젝트 명명 규칙에 맞춰 정하되 원본 `CHI_weng_wenhao` ID는 보존한다. 장쥔마이 지정안은 최종 선택이 아니며 어느 후보도 이번에 구현하지 않았다.
- **원본 CHI 인물의 국적을 옮기거나 삭제·은퇴시키지 않는다.** 기존 중국의 중점·민주화 사건·지도자·정치고문 설정을 그대로 두고, 같은 인물의 양국 병존을 허용한다. 중복을 막으려고 중국 콘텐츠를 바꾸는 것은 이번 범위에 포함하지 않는다.
- 지도자 이름은 기존 `CHI_weng_wenhao` 표시 키, 대형 초상화는 본체의 `GFX_portrait_chi_weng_wenhao`를 우선 재사용한다. 기본 게임 자산이므로 이 초상화 자체에 NCNS DLC를 새로 요구하거나 이미지를 새로 제작·복사할 필요는 없다. 산둥 출범의 기존 MtG 조건은 별개로 유지한다.
- 민주주의 역할의 참고 원본은 NCNS 미사용 분기의 `socialism`이다. 이는 민주주의의 하위 이념이며 공산주의 정부로 바꾸는 안이 아니다. 원본의 NCNS 정치고문 역할·`CHI_geologist_trait`, 장쥔마이의 특성이나 추가 정책·보상 보너스를 함께 이식하는 안은 포함하지 않는다. 지도자 특성에 따른 기존/신규 효과 차이는 후속 구현 시 따로 확인한다.
- [19절의 출범 계약](#19-shandong-warlord-integration-implementation)은 유지한다. 영토·보호 조건·핵심주·국가별 지지도 계산·육해공군/비축/연료 귀순·잔여 자산 처리·전쟁명분·자동 선전포고 금지·한국 피감독국/세력·중국 인정 결정·중점 조건/기간/AI/배치·국명·지도는 이번 변경 대상이 아니다. 민슈 잇키나 원본 스페인 내전의 전쟁 처리를 중국에 이식하는 작업도 포함하지 않는다.

### 원본 출처와 현재 상태

읽기 기준은 설치본 `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\`다. `launcher-settings.json` 4–5행의 버전은 **Operation Postern v1.19.5.0.7c6c (c184)**이며 이 설치본 소스에 한정한 확인이다. 이 경로는 읽기 전용 원본이며 향후 구현도 작업 저장소에서 해야 한다. 문서화 시작 시 저장소는 `feat/korean-focus-expansion-ai`, HEAD `0c19f58fa7a9ff898196dcdbe46edfd0ad5fdbbc`였고 기존 미커밋 작업을 보존했다.

다음 경로는 위 설치 원본에 상대적이다. 행 번호는 이번 읽기 시점 기준이다.

| 출처 | 확인한 의미 |
|---|---|
| `common/characters/CHI.txt` 3218–3273행 | `CHI_weng_wenhao` 정의. NCNS 사용 분기에서는 `CHI_geologist_trait` 정치고문, 미사용 분기에서는 `socialism` 국가지도자다. 예전 지도자 정의에는 명시적 특성이 없고 만료일은 `1965.1.1.1`이다. 따라서 현재 게임에서 완전히 미사용인 인물은 아니다. |
| `history/countries/CHI - China.txt` 164행 | 원본 CHI가 DLC 분기 밖에서 `CHI_weng_wenhao`를 모집한다. 원본 모집을 제거하지 않는 계약의 근거다. |
| `common/ideologies/00_ideologies.txt` 3–14행 | `socialism`이 `democratic` 아래에 정의돼 있다. |
| `interface/_leader_portraits.gfx` 1297–1304행 | 대형 `GFX_portrait_chi_weng_wenhao`와 소형 `GFX_idea_CHI_weng_wenhao`의 본체 자산 등록. 대형은 `gfx/leaders/CHI/Portrait_China_weng_wenhao.dds`를 가리킨다. |
| `gfx/leaders/CHI/Portrait_China_weng_wenhao.dds` | 본체 대형 초상화 파일 존재를 읽기 확인했다. 새 에셋을 생성하거나 원본 파일을 수정하지 않았다. |
| `localisation/korean/nsb_characters_l_korean.yml` 262행 | 원본 한국어 이름 `CHI_weng_wenhao`는 “웡원하오”다. 실제 활성 언어별 UI 표시는 이번 문서화에서 관측하지 않았다. |

앞선 읽기 검토에서는 설치 원본의 중점·사건·결정·scripted effect에서 웡원하오 ID/이름의 직접 참조를 찾지 못했다. 이는 **현행 민주화 중점의 명시적 지도자 후보로 사용하지 않는 옛 지도자**라는 후보 선정 근거이며, 고문·비DLC 지도자까지 미사용이라는 뜻은 아니다. NCNS를 사용하면 CHI 고문과 산둥 지도자가, 사용하지 않으면 중국 민주화 시 양국 지도자가 같은 인물로 존재할 수 있다. 이 병존은 사용자가 허용한 결과다.

### 영향 후보와 후속 확인

| 후보 | 처리 | 의도·확인 범위 |
|---|---|---|
| 산둥 전용 웡원하오의 이름·초상화·민주주의 지도자 지정 | 수정 — 후속 구현 제안, 현재 미반영 | 산둥의 기존 자동 생성 지도자 대신 지정할 대상. [출범 효과](../common/scripted_effects/HOK_KOR_chinese_government_effects.txt)의 실제 생성국 scope에 적용하는 위치와 기존 지도자 역할 교체는 구현 때 확인한다. |
| 원본 `CHI_weng_wenhao`의 두 DLC 분기·모집·중국 콘텐츠 | 의도적 유지 | 소속 이동·삭제·역할 변경 없이 보존하고 동일 인물 병존을 허용한다. |
| 본체 이름 키·초상화 자산 | 의도적 재사용 / 원본 편집 제외 | 대소문자·물리 경로·활성 언어별 표시를 후속 구현에서 대조한다. 새 표시 키가 필요하면 [두 언어 채널 계약](incidents/2026-09-01-localisation-contract.md)을 먼저 읽고 적용한다. 초상화 재사용 구현 전에는 [개발 자료·이미지 출처 안내](HOK_DEVELOPMENT_ARTIFACT_ARCHIVE.md)를 읽는다. |
| 영토·군대·장비·전쟁·피감독국·중점·결정·지도·국명 | 제외 — 기존 계약 유지 | 지도자 교체를 이유로 19절의 게임 규칙을 변경하지 않는다. |
| 특성·선거/만료 후 지도자·이미 출범한 저장 | 미확인 — 후속 구현 시 범위 확인 | 기존 선거 설정을 유지한다. 원본 만료일 이후 처리와 기완료 저장의 자동 교체를 이번에 확정하거나 검증하지 않았으며, 별도 소급·마이그레이션 효과를 추가하지 않는다. |

향후 구현이 승인되면 확인할 대상은 산둥 출범 시 웡원하오의 이름·대형 초상화·민주정부 지도자 표시, 원본 CHI 인물과 두 DLC 분기의 보존, 지도자 특성의 효과 차이와 필요한 저장/후계 범위다. 이는 예정 확인이며 이번 문서화에서 게임플레이 검사·실제 UI·효과 실행·저장 왕복을 수행했다는 뜻이 아니다.

초기 문서화 때에는 이 절과 문서 상단·2차 확장 계획·README의 안내만 갱신했다. 당시 게임 코드·현지화·에셋·설정은 수정하지 않았고, 게임·테스트·검사 스크립트·빌드·패키징·커밋·푸시·업로드를 실행하지 않았다. helper·시험 보고서·백업도 만들지 않았다. 19절의 실행 기록과 외부 증거는 지도자 지정 전 소스의 이력이며 이 안의 UI·저장 검증으로 재사용하지 않는다. 기존 시험 PNG 4개의 정리 미결도 유지하고 이동·삭제하지 않는다.

<a id="21-shandong-weng-wenhao-leader-implementation"></a>

## 21. 2026-11-19 산둥 전용 웡원하오 지도자 — 구현

상태: **구현·DLC 양분기 지연 출범·한국어 UI·새 저장 왕복 확인**. 사용자가 20절의 설명을 인용하고 `AGENTS.md, /docs 읽고 구현해줘`라고 별도로 승인했다. 실제 변경은 [전용 캐릭터](../common/characters/HOK_KCH_characters.txt) `HOK_KCH_weng_wenhao`, KCH 시작 이력의 전용 인물 모집, [출범 효과](../common/scripted_effects/HOK_KOR_chinese_government_effects.txt)의 생성 child 안 이동·승격이다. 처음 두 파일 안의 출범 시 직접 모집에서 발견한 엔진의 시작 시점 경고를 반영해 원본 일본 민주 내전처럼 초기화와 출범 시 이동을 분리한다. 이름 키 `CHI_weng_wenhao`, 본체 대형 초상화 `GFX_portrait_chi_weng_wenhao`, 민주주의 하위 이념 `socialism`과 원본 만료일을 재사용하며 명시적 특성·고문·새 보너스는 없다.

원본 중국 인물의 소속·모집·DLC별 고문/민주지도자 역할을 유지한다. 같은 인물이 양국에 존재하는 것은 허용된 결과다. 기존 영토·전력·전쟁·피감독국·중점·결정 규칙을 바꾸지 않으며 이미 출범한 저장을 자동 교체하지 않는다. 실제 UI·효과·저장과 범위별 미검증은 [이번 구현 기록](incidents/2026-11-19-shandong-weng-wenhao.md)을 따른다.

이번 외부 작업은 `C:\hoi\test\hok-shandong-weng-wenhao-20261119-01\`이며, 초기 편집 전 `source-before.json`·`formation-before.txt`, r1 두 파일과 최종 r2 세 production 소스의 최소 변경 확인 `implementation/source-contract.json`·`source-contract-r2.json`, 독립 검토 `review/`, 설정·로그·저장과 실행 `runtime/`, 실제 화면 `ui/`를 구분한다. 이전 `hok-shandong-full-integration-20261119-01`의 실행은 이번 지도자 검증으로 사용하지 않는다.

<a id="22-shandong-dominion-implementation"></a>

## 22. 2026-11-19 산둥 자유 공화국의 한국 자치령 출범

상태: **코드 적용·소스 확인, 실제 자치령 출범·외교 UI·저장 왕복은 미실행**. 사용자가 산둥 자유 공화국을 자치령으로 정했다. 대상은 「중국 독재자 축출」의 새 정부 생성 효과다. 기존 저장에서 이미 출범한 정부를 자동으로 전환하는 효과나 결정을 추가하지 않았다.

### 지위와 변경 범위

- [형성 효과](../common/scripted_effects/HOK_KOR_chinese_government_effects.txt)의 한국 Country scope `set_autonomy`에서 `autonomy_supervised_state`를 `autonomy_dominion`으로 바꿨다. 실제 생성국 event target, `end_wars = no`, `end_civil_wars = no`, 뒤의 세력 편입과 임시 자료 정리는 유지한다. 국가를 재생성하거나 전력·영토 이전을 다시 실행하지 않는다.
- 설치 원본 `common/autonomous_states/dominion.txt`의 ID와 `allowed`는 자치령·`Together for Victory`를 정의한다. 기존 `Man the Guns`는 `supervised_state.txt`의 요구였으므로 [중점 가용 조건](../common/national_focus/korea.txt)과 [형성 guard](../common/scripted_triggers/HOK_KOR_chinese_government_state_triggers.txt)를 TfV로 함께 교체했다. 자치령 도입에 필요한 의도적 조건 변경이며, 다른 기능의 MtG 분기는 건드리지 않는다. DLC 미충족 때 다른 괴뢰 단계로 자동 대체하지 않는다.
- 기존 `HOK_KOR_chinese_government_mtg_tt` ID는 호환성을 위해 유지하고 표시값만 TfV로 바꿨다. 전용 효과 키와 구 `KOR_overthrow_the_chinese_dictators_tt`에도 한국의 자치령으로 안내한다. 본체 Korean/English 두 채널의 한국어 본문·BOM·키·토큰을 유지한다.
- 바닐라 자치령 정의를 그대로 사용한다. 두 지위 모두 독자 선전포고 금지·참전 요청 거절 가능·`autonomy_manpower_share = 0.0`이며, 자치령의 첩보장 허용·자치도·이념/평화 점수 등의 원본 규칙도 따라온다. 피감독국의 보정을 자치령에 복제하거나 원본 자치령 파일을 수정하지 않았다. `min_freedom_level = 0.8`을 초기 자치도·상한으로 오해해 별도 수치를 넣지 않고 기존 `freedom_level` 생략을 유지한다.
- 중점 ID·기간·선행·민주주의/독립 조건·취소·AI·배치·결정 해금, 본토 63코어·SND 기본 영토·타국 연결 선택·지지도 귀순/잔여 처리, 전용 웡원하오·국명·전쟁명분·자동 선전포고/별도 참전 미추가와 「하나의 중국 인정」의 기존 CHI 한정 계약은 그대로다.

### 근거와 표시 영향 대장

설치 원본은 `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\`, 메타데이터 `Operation Postern v1.19.5.0.7c6c (c184)`다. `dominion.txt:2,77–118`, `supervised_state.txt:42–71`, `documentation/effects_documentation.md:6586–6600`과 `events/DOD_Hungary.txt:388`의 같은 런타임 명령을 읽어 대조했다. 원본과 Workshop 관리 사본은 수정하지 않았다. 정상 중점의 민주·독립 KOR 조건은 자치령의 파시즘 종주국·일본/중국 예외와 충돌하지 않는다. 강제 호출·모든 DLC 조합의 실제 엔진 관측까지 뜻하지 않는다.

| 후보·접점 | 처리 | 확인 범위·남은 항목 |
|---|---|---|
| 출범 `set_autonomy` | 수정 — 자치령 ID, 원래 한국/생성국 scope 유지 | 설치 명령 계약·바닐라 예제와 소스 대조. 실제 새 자치령 생성 미실행 |
| 중점 available·취소와 `can_form` | 수정 — 두 진입 조건을 TfV로 맞춤 | 나머지 조건·호출자·보상·순서 보존. 실제 무MtG/TfV 충족·미충족 진행은 미검증 |
| DLC·전용 효과·구 중점 효과 안내 | 수정 — 고유 키 3개, 본체 파일 4개 | Korean/English 본문·기여 주석·BOM·토큰 확인. 새 UI는 미관측 |
| 기존 `_mtg_tt`라는 키 이름 | 의도적 유지 — 표시 ID 보존 | 값은 TfV. 이름을 근거로 옛 MtG 조건을 복구하지 않음 |
| 영토·전력·지도자·중점 기타·인정 결정 | 의도적 유지 | 이번 7 production 파일의 지정 구간 외 변경 없음. 이전 실행은 당시 소스에 한정 |
| 현재 보조 모드·영어 번역 | 활성 보조 모드의 관련 덮어쓰기 후보 없음. 비활성 외부 번역 수정 제외 | 조회된 선택은 HOK → HOK anime → Anime History, `l_korean`, `disabled_dlcs=[]`. 저장된 선택과 실제 엔진 로드는 구분하며 외부 영어 번역 재선택 시 옛 안내를 별도 검토 |
| 기존 출범 저장·자치도 수치 강제·자치 규칙 재설계 | 제외 | 자동 소급·수치 보정·원본 DB 수정 없음 |
| 실제 새 효과·외교 화면·새 저장 재로드·장기/MP | 미확인 | 현재 사용자 게임을 유지해 이번 실행으로 검증하지 않음 |

[산둥 구조도](architecture/shandong-government.md)의 D15–D17과 [State 이전 순서](architecture/states/ownership-and-transfer.md)의 S09를 현행 명칭/조건에 맞췄다. 관계가 같은 D18 지도자 흐름과 S07/S08 그래프는 유지하고 S08의 진입 조건 설명 본문만 TfV로 바꿨다. 이전 피감독국 사건 기록의 UI·저장 관측은 수정하지 않았다.

### 소스 상태·검증·후속

기준 branch는 `feat/korean-focus-expansion-ai`, HEAD `0c19f58fa7a9ff898196dcdbe46edfd0ad5fdbbc`와 기존 미커밋 작업이다. `descriptor.mod`와 실제 launcher pointer는 `1.19.*`·기존 의존/후속 Workshop ID를 유지하고, pointer는 이 저장소 `C:/hoi/hearts_of_korea`를 직접 읽는다. ID·업로드 설정은 변경하지 않았다.

이번 외부 작업 폴더는 `C:\hoi\test\shandong-dominion-20261119\`다. `source-before\`의 production 7파일 원본, `dlc_load.before.json`·`launcher-mod.before.txt`, `apply_dominion_patch.py`·`source-patch.json`을 구분한다. 7파일·13개 지정 치환 구간의 역치환이 원본 바이트와 같고 BOM을 보존했다. 독립 검토도 JSON 결과만 재인용하지 않고 실제 7개 백업/현행 diff와 4개 현지화 파일의 BOM·헤더·동일 기여 주석·값을 직접 읽어 요청 밖 변경을 찾지 못했다. 이 수량은 소스 패치의 경계 확인이며 게임 효과 시험 수가 아니다.

다이어그램 helper·템플릿·원본 배포 파일은 앞선 `state-diagrams-always-dark-20261119`에서 이번 폴더로 필요한 파일만 복사하고 중간 출력·프로필을 새 폴더에 뒀다. State 다크 이미지를 재생성한 뒤 S09의 정식 SVG/PNG와 기본 경로 다크 사본 4개 및 manifest를 반영하고 실제 S09 이미지를 시각 확인했다. 원본 블록이 같은 S01/S07의 렌더 내부 SVG ID 차이는 이전과 같은 그림 원본으로 보존했다. `diagram-manifest.before.json`·`diagram-changed-files.json`은 생성 전 기준/초기 후보이며, 최종 구분은 `finalize_diagrams.py`·`diagram-final-changes.json`에 남겼다. 현재 문서 그림은 50파일·4,593,058바이트이며 파생물 경로와 원본/도구 해시는 [manifest](architecture/states/images/manifest.json)를 따른다. 이 표시는 자치령 효과의 게임 UI 관측이 아니다.

초기 조회 시 사용자 소유 HOI4 PID **24336**이 실행 중이어서 종료·재실행·설정 변경·프로브 삽입·저장/로그 조작을 하지 않았다. 후반 조회에는 해당 프로세스가 보이지 않았으며 에이전트가 종료한 결과가 아니다. 이번 검증은 지정 소스의 최소 변경·설치 원본 계약·독립 읽기 검토와 문서 이미지 확인 범위로 마감한다. 수정 전 실행의 화면을 새 코드의 증거로 사용하지 않는다. 후속 게임 검증 시 새 baseline·소스 고정·별도 이름의 강제 출범/실제 UI·저장 재로드로 자치령을 확인한다. 실제 태그를 D04 등으로 고정하지 않고 `original_tag = KCH`인 유일한 영토 보유국과 KOR의 종속 관계를 대조해야 한다. 이전 helper를 쓸 때 `control_native.py --case production`의 옛 2모드 목록이나 과거 baseline을 현재 환경에 적용하지 않는다.

게임플레이 로드·UI·효과·저장 검증은 후속 미검증으로 유지한다. 기존 시험 PNG 4개의 정리 미결도 그대로이며 커밋·푸시·업로드는 하지 않는다.

최종 `final-source-summary.json`에서 지정 production 7파일이 패치 후 해시와 일치(불일치 0)하고 launcher pointer·DLC 선택 파일은 작업 전 사본과 같음을 확인했다. 이 보존 확인은 사용자 게임의 새 실행·소스 등록을 뜻하지 않는다.

<a id="23-shandong-focus-chi-support-and-duration"></a>

## 23. 2026-11-19 중국 민주주의 지지도 50%·70일 중점

상태: **코드 적용·소스/독립 읽기 확인, 실제 경계값 UI·70일 진행·취소·저장 검증 미실행**. 사용자가 「중국 독재자 축출」에 중국 민주주의 지지도 50% 이상 조건과 35→70일을 요청했다. 대상 중점은 `KOR_overthrow_the_chinese_dictators`다.

### 현재 조건과 기간

- [한국 중점](../common/national_focus/korea.txt)의 `cost`를 5에서 **10**으로 바꿨다. 설치 원본 `common/defines/00_defines.lua`의 `NFocus.FOCUS_POINT_DAYS = 7`에 따른 기본 기간은 **70일**이다. 실제 보정·저장 진행도와 완료 시각을 새로 관측한 결과는 아니다.
- [공유 조건](../common/scripted_triggers/HOK_KOR_chinese_government_state_triggers.txt) `HOK_KOR_chinese_government_has_chi_democracy`는 고정 국가 `CHI`에서 `exists = yes`와 `NOT = { democratic < 0.50 }`를 검사한다. 민주주의 정부 여부와 지지도는 별개이며 다른 중국 국가·현재 대표국·한국의 지지도를 이 수치로 대신하지 않는다.
- 중점 `available`은 새 현지화 키 `HOK_KOR_chinese_government_chi_democracy_tt`로 중국 존재와 50% 이상 조건을 안내한다. `can_form`도 같은 공유 조건을 사용하므로, 형성 효과의 snapshot·변수 변경·국가 생성 이전에 다시 확인한다. 기존 원국별 지지도·90% 상한·영토/전력 비례 계산은 그대로다.
- 기존 TfV·KCH 부재·안전한 거점, 한국 민주/독립, `WTT_current_china_leader`의 존재·비민주정부 조건은 각각 유지한다. CHI가 민주정부가 되었더라도 현재 대표국 조건을 임의로 완화하지 않는다.
- `cancel_if_invalid = yes`, `continue_if_invalid = no`를 유지했다. 따라서 진행 중 CHI 소멸이나 지지도 50% 미만도 기존 취소 설정의 적용 대상이다. 실제 취소 평가 시점은 미검증이다. 기완료 중점을 초기화하거나 기존 출범국을 재생성하는 처리는 추가하지 않는다.

| 소스상 기대 판정 | 새 CHI 조건 |
|---|---|
| 실존 CHI의 지지도 49.9% | 차단 |
| 실존 CHI의 지지도 정확히 50% | 통과 — 다른 기존 조건도 충족해야 시작 가능 |
| 실존 CHI의 지지도 50.1% | 통과 — 다른 기존 조건은 별도 |
| CHI가 없거나 다른 군벌만 50% 이상 | 차단 |

이 표는 원본 trigger 계약과 부정 논리에서 도출한 기대값이며 실행 시험의 통과표가 아니다. 설치 `documentation/triggers_documentation.md`의 `ideology_support_trigger`는 COUNTRY의 `<Ideology> < <float>`를, `not`는 조건 부정을 정의한다. `dynamic_variables_documentation.md`의 정당 지지도 범위는 0–1이다. 설치 `common/national_focus/switzerland.txt`의 `available`에도 `democratic < 0.50` 예가 있다. 미확인인 `democratic >=` 문법이나 `> 0.49` 근사치를 사용하지 않았다.

### 변경 영향과 보존

| 후보 | 처리·확인 |
|---|---|
| 중점 기간·가용 조건·공유 형성 guard | 수정 — cost 10, CHI 공유 조건 정의와 두 호출. 실제 백업/현행 소스와 설치 원본 계약 대조 |
| 새 조건 표시 | 수정 — Korean/English paired 파일에 같은 한국어 요건·동일 기여 주석·BOM 유지. 해당 문맥에서 검증하지 않은 현재 지지도 getter는 추가하지 않음 |
| 현재 활성 보조 모드 | HOK anime·Anime History의 관련 중점/조건 키 덮어쓰기 후보 없음. 비활성 외부 English Translation의 수정은 제외하고 재선택 시 새 키·구 설명 검토 필요 |
| 자치령·영토·지휘관 제외·병력/비축/연료·웡원하오·전쟁명분·세력·인정 | 의도적 유지 — [22절](#22-shandong-dominion-implementation) 및 기존 생성 효과는 이번 변경 대상 아님 |
| 취소 플래그·선행·좌표·AI·나머지 보상 | 의도적 유지 — 요청한 요건이 기존 가용/취소 체계에 참여. 기존 AI 가중치·전략·배치를 별도 조정하지 않음 |
| 강제 완료의 보상 전체 원자성 | 범위 제외 — `can_form` 실패는 형성 본문을 막지만 helper 밖의 기존 전쟁명분 루프까지 감싸지 않음 |
| 실제 UI·경계값·기간/취소 진행·구 저장/멀티플레이 | 미확인 — 과거 35일·이전 소스 검증을 재사용하지 않음 |

[산둥 구조도](architecture/shandong-government.md)의 D15/D17과 State 진입 조건 설명을 새 계약에 맞췄다. 효과 처리 순서·주 적격 관계가 같은 D16/D18/S07/S08/S09와 State 다크 PNG/SVG는 의도적으로 유지했다. 해당 원본 블록이 같으므로 파생 이미지를 재생성하지 않았다. 모든 Mermaid의 다크 설정도 유지한다.

외부 작업은 `C:\hoi\test\shandong-focus-support-20261119\`다. `source-before\`의 production 4파일·`dlc_load.before.json`, `apply_focus_patch.py`·`source-patch.json`을 구분한다. 지정 8치환 구간의 역치환이 원본 바이트와 일치했고 BOM/줄 끝을 유지했다. 독립 검토도 보고서 JSON 대신 실제 백업 4파일/현행 diff·paired UTF-8 BOM/헤더·기여 주석·조건/보상을 직접 읽어 범위 밖 차이를 찾지 못했다. 이 확인은 소스 검증이며 엔진 실행이 아니다.

branch `feat/korean-focus-expansion-ai`, HEAD `0c19f58fa7a9ff898196dcdbe46edfd0ad5fdbbc`와 기존 미커밋 작업을 보존한다. 대상 설치본은 1.19.5.0.7c6c(c184) 메타데이터이며 launcher pointer는 저장소를 직접 가리킨다. 조회된 선택은 HOK → HOK anime → Anime History, `disabled_dlcs=[]`다. 사용자 게임 PID **4052**가 실행 중이어서 종료·재실행·설정/저장/로그/프로브 변경을 하지 않았다. 실제 새 UI·70일 진행·취소·저장 확인은 후속 미검증으로 남긴다. 기존 시험 PNG 4개의 정리 미결도 유지하고 커밋·푸시·업로드는 하지 않는다.


<a id="24-minshu-ikki-player-japan"></a>

## 24. 2026-11-19 민슈 잇키의 인간 일본 허용

상태: **코드 적용·소스/독립 읽기 확인, 실제 UI·내전·저장·멀티플레이 미검증**. 사용자 요청으로 [한국 중점](../common/national_focus/korea.txt)의 `KOR_minshu_ikki` 안 `JAP = { is_ai = yes }` 조건 한 줄만 제거하고 기여 주석을 남겼다. 한국이 이 중점을 선택할 때 일본의 AI/사람 여부를 제한하지 않는 변경이다. 일본 플레이어에게 한국 중점을 부여하는 기능은 아니다.

| 후보·경로 | 처리·근거 |
|---|---|
| 한국 중점의 일본 AI 조건 | 수정 — `available`의 JAP 범위에서 `is_ai = yes`만 제거. 실제 백업/현행 diff에서 주석으로 대체한 한 줄 외 차이 없음 |
| 한국 민주주의·독립국, 일본 비민주주의, 일본 민주주의 지원 선행 | 의도적 유지 — 가용 조건과 선행 중점 동일 |
| 기본 35일(cost 5)·AI factor 1·좌표·아이콘·보상 | 의도적 유지 — 중점 블록의 다른 바이트 불변. 중국 축출의 CHI 50%·70일도 불변 |
| `HOK_KOR_japanese_democratic_uprising`와 후속 세력/참전 | 의도적 유지 — [봉기 helper](../common/scripted_effects/HOK_KOR_democratic_intelligence_effects.txt)의 지지도 10–90% 비율·민주 내전·외형·일반 중점·한국 세력 편입/참전은 동일하며 추가 AI guard 없음 |
| 이름·설명·효과 안내와 활성 보조 모드 | 의도적 유지 — 본체 Korean/English의 `KOR_minshu_ikki`, `_desc`, `_tt`에는 AI 전용 수동 문구 없음. 조회한 HOK anime·Anime History에 해당 정의/키 덮어쓰기 후보 없음. 비활성 외부 English Translation 편집은 제외 |
| 일본 자체 `HOK_JAP_pre_emptive_coup`와 그 분기 진입 조건 | 제외 — 별도 일본 중점이며 한국 봉기 helper가 호출하지 않음. 해당 중점 자체에는 AI 전용 가용 조건이 없고, 진입점의 기존 인간 전용 조건도 유지 |
| 구조·State 다이어그램 | 의도적 유지 — 현재 도표에 이번 AI 제한 표현이 없고 호출·scope·선행·지도 관계 불변. Mermaid·SVG/PNG·갤러리의 다크 설정을 유지하고 렌더링하지 않음 |
| 인간 일본의 조작국 승계·기존 진영·실제 내전과 멀티플레이 | 미확인 — 소스에는 플레이어를 봉기국으로 이동시키는 명령 없음. 기존 AI 일본 실행을 인간 일본 검증으로 재사용하지 않음 |

필수 확인은 이 한 줄의 직접 diff·기존 조건/보상·표시 경로 보존으로 정했다. 외부 작업은 `C:\hoi\test\minshu-player-japan-20261119\`이며 `source-before/`는 변경 직전 작업 소스·문서 사본, `apply_focus_patch.py`와 `source-patch.json`은 변경 구간/해시와 바이트 역치환 확인이다. 독립 검토도 실제 백업과 현행 diff 및 helper를 직접 읽었다. 이는 소스 확인이며 엔진 실행을 뜻하지 않는다. 최종 focus SHA-256은 `20c92cdd66e4863bf1c71375095df4a5ca12828c16834e363c50f097c8598783`다.

branch `feat/korean-focus-expansion-ai`, HEAD `0c19f58fa7a9ff898196dcdbe46edfd0ad5fdbbc`와 기존 미커밋 작업을 보존했다. 이번 조회의 설치 메타데이터는 **Operation Postern v1.20.0.0.8873 (0c4f)**이며, 저장소·launcher descriptor의 `supported_version="1.19.*"`는 변경하지 않았다. 앞 절의 1.19 기록과 시점을 구분하고 이번 한 줄 변경을 1.20 전체 호환 검증으로 해석하지 않는다. launcher pointer는 저장소를 가리키며 조회된 선택은 HOK → HOK anime → Anime History, `disabled_dlcs=[]`다. 이는 현재 프로세스가 실제 로드한 구성의 증명이 아니다.

실행 중인 사용자 게임 PID **26172**(2026-11-19 23:26:52 시작)는 종료·재실행·조작하지 않았고 설정·저장·로그·프로브도 변경하지 않았다. 실제 인간 일본 대상 가용 UI·봉기 결과·저장 왕복·멀티플레이는 후속 미검증이다. 기존 `docs/assets/korean-fascist-mobilization-validation-20260923/`의 시험 PNG 4개(815,391바이트)는 정리 미결로 보존했다. 커밋·푸시·업로드는 하지 않았다.
