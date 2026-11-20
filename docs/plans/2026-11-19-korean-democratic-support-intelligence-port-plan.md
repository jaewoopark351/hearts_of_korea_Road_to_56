# 2026년 11월 19일 원본 민주인사 지원과 산둥 정부 이식 계획

작성일: **2026-11-20, Asia/Seoul**. 대상은 2026-11-19 원본 업데이트다. 최초 문서화 당시 상태: **문서화만 승인 · 신규 콘텐츠 미이식 · 당시 정적 검사와 게임 실행 미실시**.

2026-11-20 후속 구현: 사용자가 콘텐츠와 지침·구조도 체계의 전체 구현을 승인했다. runtime28출력과 RT56 본토64주 대응을 생성 계층에 반영했으며 실제 검사·실행·저장 상태는 [구현 기록](../implementation/2026-11-20-korean-democratic-support-intelligence-port.md)을 따른다. 아래 미이식·미실행·제안 표는 최초 계획 이력이며 최종 적용/검증 판정으로 사용하지 않는다.

원본의 민주인사 지원·비밀 정보국·산둥 정부 업데이트는 기존 호환판 위에 선택 이식할 수 있다. 중국 지역 집합과 생성 파일 소유권, 영어 표시를 호환판에 맞춰 병합해야 한다. 현재 설치 메타데이터는 HOI4 1.20.0이고 RT56·호환판의 지원 선언은 1.19.*이므로, 콘텐츠 이식 가능성과 실제 1.20 실행 호환성을 구분한다.

사용자의 “문서화 작업만 진행해줘” 요청에 따른 계획이다. 게임 코드·그림·생성기·잠금·원장·descriptor·캐시·사용자 설정을 수정하지 않는다. 구현·시험·게임 실행·정리·커밋·푸시·게시를 승인하는 문서가 아니다.

2026-11-20 후속 문서화: 원본 AGENTS.md·SKILL.md·다이어그램에 대응하는 호환판 체계는 [별도 도입 계획](2026-11-20-architecture-diagram-adoption-plan.md)에 기록했다. 이 업데이트의 구조 문서·지침·그림을 실제로 도입하기 전에 그 계획을 읽는다. 현재 구현과 산둥 이식 예정, 생성 과정과 게임 수명주기, 지침/원본/파생물의 역할을 구분하며 실제 도입은 후속 작업으로 남는다.

## 1. 후속 작업 전에 읽을 자료

| 작업 조건 | 먼저 읽을 자료와 용도 |
|---|---|
| 이식 범위나 진행 상태를 판단할 때 | [AGENTS.md](../../AGENTS.md), [변경 영향 검토 절차](../HOK_CHANGE_COVERAGE_REVIEW.md). 최신 요청 모드, 기능·호출자·분기별 처리와 소스/UI/효과/저장 증거 구분을 따른다. |
| 한국 경로와 RT56 일반 콘텐츠의 소유권을 판단할 때 | [ADR-0004](../decisions/0004-hok-korean-content-priority.md). KCH·KJP도 한국 경로의 산출물이면 한국 콘텐츠이며, 일반 CHI·JAP·세계 공유 정의는 RT56을 보존한다. |
| 지역 집합·수도·핵심주·영토 이전을 설계할 때 | [주 참조 검토 스킬](../skills/hok-rt56-state-reference-review/SKILL.md), [ADR-0002](../decisions/0002-map-id-migration.md), [ADR-0006](../decisions/0006-korean-state-split-integration.md), [한국 주 대응표](../data/HOK_KOREAN_STATE_SPLIT_PORT_MAPPING.json), [ADR-0007](../decisions/0007-november-content-integration.md). 기존 한국 지도와 난징·중국 지역 적응을 보존한다. |
| 표시·번역·내부 표식의 노출을 다룰 때 | [현지화 검토 스킬](../skills/hok-rt56-localisation-review/SKILL.md), [ADR-0003](../decisions/0003-localisation-contract.md), [영어 이식 기록](../implementation/2026-10-20-english-localisation-import.md). 영어/한국어 역할과 실제 번역 덮어쓰기를 구분한다. |
| 기존 중점·캐릭터·history·현지화 출력을 수정하거나 재생성할 때 | [지휘관 이식의 생성 소유권·검증 기록](../implementation/2026-11-14-korean-commander-unlock-port.md), [해당 선택 입력](../upstream/hok-commander-unlock-20261114/README.md). 최신 최종 출력·정확한 선조·역투영 계약과 이전 계층을 보존한다. |
| 원본의 최종 게임 동작을 해석할 때 | 원본 [기능 계획](../../../hearts_of_korea/docs/HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_PLAN.md). 정보국의 재무장 선행은 11절, 자치령·CHI 50%/70일·인간 일본은 22–24절을 우선하며 앞선 설계·실행과 구분한다. |
| 산둥 영토·전력·지도자와 과거 실행 근거를 해석할 때 | 원본 [지리 목록](../../../hearts_of_korea/docs/data/HOK_KOREAN_CHINESE_GOVERNMENT_STATE_GROUPS.json), [전면 편입 기록](../../../hearts_of_korea/docs/incidents/2026-11-19-shandong-full-integration.md), [웡원하오 기록](../../../hearts_of_korea/docs/incidents/2026-11-19-shandong-weng-wenhao.md). 바닐라 지도·이전 피감독국 단계의 증거를 현재 RT56 결과로 사용하지 않는다. |
| 그림을 복사·변경하거나 과거 제작 입력을 재사용할 때 | [개발 자료·소스 캐시 안내](../HOK_DEVELOPMENT_ARTIFACT_ARCHIVE.md), 원본 [그림 출처](../../../hearts_of_korea/docs/HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_ASSET_CREDITS.md), [그림 매니페스트](../../../hearts_of_korea/docs/data/HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_ASSET_MANIFEST.json). 완성 DDS·원본 권리·전용 sprite·공유 엔진 참조의 역할을 구분한다. |
| 새 원본 구조 문서를 참고하거나 도표 도입을 검토할 때 | 원본 [구조 문서 인덱스](../../../hearts_of_korea/docs/architecture/README.md), [유지보수 안내](../../../hearts_of_korea/docs/architecture/maintenance.md). 원본 전용 지도·언어·생성 구조를 호환판 구조로 오인하지 않는다. 도표 도입 자체는 이번 작업에 포함하지 않는다. |

원본 링크는 `C:\hoi\hearts_of_korea`의 읽기 전용 현재 파일이다. 아래 커밋을 출처 기준으로 삼으며 이번에는 새로운 `docs/upstream/` 사본이나 manifest를 만들지 않았다. 원본이 갱신되면 현재 파일을 이 계획의 동결 입력으로 간주하지 말고 다시 비교한다.

## 2. 문서화 기준선

| 항목 | 읽기 확인값과 한계 |
|---|---|
| 호환판 | `C:\hoi\hearts_of_korea_Road_to_56`, `feat/korean-focus-update-20260922@9a01955785bcdd827c9c85522537a0bfc57ed654`. 문서 작업 시작 시 작업 트리 clean. |
| 마지막 반영 원본 | `0c19f58fa7a9ff898196dcdbe46edfd0ad5fdbbc`. 11월 14일 지휘관 해금 이식 기록의 기준이다. |
| 최신 원본 | `C:\hoi\hearts_of_korea`, `f180bc8089e2a17f310b1fafa091d3f152063df3`. 이번 조회 시 작업 트리 clean. |
| 새 게임 콘텐츠 커밋 | `f2356e2a2c6db9048e18a4dde41454865f10742a`, 민주인사 지원·산둥 정부 구현. |
| 새 구조 문서 커밋 | `f180bc8089e2a17f310b1fafa091d3f152063df3`, 구조 문서와 다크 도표. |
| 설치 게임 메타데이터 | `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\launcher-settings.json`의 `Operation Postern v1.20.0.0.8873 (0c4f)`, `rawVersion=1.20.0.0`. 실행 체크섬이나 이번 게임 관측이 아니다. |
| RT56 호스트 | `C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968`. `appworkshop_394360.acf`의 설치/상세 manifest 모두 `1963361040482473746`, size `1373729636`, timeupdated `1794141719`. 11월 14일 기록과 manifest는 같지만 전체 파일 해시가 같다고 새로 입증한 것은 아니다. |
| 지원 선언 | 현재 호환판과 RT56 descriptor 모두 `supported_version="1.19.*"`. 설치 1.20과의 차이는 재기준화·검증 필요 사항이며 확정된 실행 실패 판정은 아니다. |
| 현재 호환판 descriptor | `The Road to 56`, `Korean Language`, `The Road to 56 Korean Translation` 의존성과 기존 호환판 ID `3796816200`. broad replace_path·launcher 전용 path는 없다. 이번에는 변경하지 않는다. |
| ID의 역할 | 역사적 HOK `2898629778`, donor revision `3793992662`는 출처, RT56 `820260968`은 호스트다. 어느 것도 호환판 업로드 대상이 아니다. 기존 호환판 ID의 확인은 게시 승인이 아니다. |
| 실행 구성 | 이번에는 플레이세트·현재 프로세스의 실제 로드 경로·DLC·언어 우선순위를 새로 입증하지 않았다. 원본 일반판의 보조 모드를 호환판 의존성으로 가져오지 않는다. |

선택 파일의 실제 checkout 바이트를 SHA-256으로 읽어 기록했다. Git 커밋의 blob 바이트와 Windows checkout 줄 끝을 혼동하지 않는다. 아래 지문은 전체 runtime 검증이나 새 소스 잠금의 생성 결과가 아니다.

| 파일 | SHA-256 |
|---|---|
| 호환판 `descriptor.mod` | `FA0058A9E90B6BBEEA4433F31723406ED1CAB513E6273B00C11A26C7AFE96C8E` |
| RT56 `descriptor.mod` | `5B323861ABD63E31CB896277E3EA58BA4BCD9FCEEDA957B50792065E42E03F61` |
| donor `common/national_focus/korea.txt` | `20C92CDD66E4863BF1C71375095DF4A5CA12828C16834E363C50F097C8598783` |
| donor `common/scripted_effects/HOK_KOR_chinese_government_effects.txt` | `D5A17EB6A4A0D8C008A4990BAEFA32DA4E5FFDA8A820B24C1E0D1BAB1CDF93BE` |
| donor `common/scripted_triggers/HOK_KOR_chinese_government_state_triggers.txt` | `0C8BB27A9400C755C3053F6A896C9052F525F72412DD9E00CCC050CBAB722921` |

## 3. 28개 런타임 경로의 이식 후보

`0c19f58..f180bc8`의 Git 경로 차이는 **107개 = runtime 28개 + 문서·지침 등 79개**다. runtime은 **기존 경로 수정 6개·신규 22개**, 형식으로는 텍스트 22개·DDS 6개다. 원본의 변경 수이며 호환판 최종 출력 수나 이식 완료 수가 아니다.

아래 분류는 후속 충돌·생성 소유권 검토를 위한 제안이다. 기존 경로의 현재 원장 분류는 유지하고 그 위의 HOK delta만 갱신한다. 신규 `ADD`·`ASSET_COPY`도 실제 동일 경로·논리 ID·권리·참조를 확인한 뒤 확정한다.

| 원본 상대 경로 | 원본 변경 | 후속 처리 제안 |
|---|---|---|
| `common/ai_strategy_plans/KOR_historical_strategy_plan.txt` | 수정 | 기존 한국 AI 병합에 정보국 순서만 반영 |
| `common/characters/HOK_KCH_characters.txt` | 신규 | `ADD`, 전용 웡원하오 정의·portrait 공급자 확인 |
| `common/decisions/HOK_KOR_democratic_support.txt` | 신규 | `ADD`, 중국·일본 지원 결정 |
| `common/decisions/KOR_decision.txt` | 수정 | 기존 인정 결정에 공용 코어 helper를 선택 병합 |
| `common/decisions/categories/HOK_KOR_democratic_support.txt` | 신규 | `ADD`, 지원 범주 |
| `common/ideas/HOK_KOR_democratic_intelligence.txt` | 신규 | `ADD`, 영구 정보국 정신 |
| `common/national_focus/korea.txt` | 수정 | 기존 생성 출력 위에 지원·봉기·정보국·선행·배치 delta 병합 |
| `common/scripted_effects/HOK_KOR_chinese_government_effects.txt` | 신규 | `ADD` 후보, 지역·동적 국가·전력 처리 적응 |
| `common/scripted_effects/HOK_KOR_democratic_intelligence_effects.txt` | 신규 | `ADD` 후보, 일본 봉기와 기존 한국 연결 대조 |
| `common/scripted_triggers/HOK_KOR_chinese_democratic_support_triggers.txt` | 신규 | `ADD` 후보, 정식 중국 16태그와 실존 조건 |
| `common/scripted_triggers/HOK_KOR_chinese_government_state_triggers.txt` | 신규 | `ADD` 후보, RT56 지리로 재정의 |
| `history/countries/KCH - Korean China.txt` | 수정 | 기존 난징 수도1114를 보존하며 전용 인물 모집만 병합 |
| `interface/HOK_KOR_democratic_support_intelligence.gfx` | 신규 | `ADD`, 일반 sprite5개 |
| `interface/HOK_KOR_democratic_support_intelligence_shine.gfx` | 신규 | `ADD`, 광택 sprite와 로컬 mask/overlay |
| `localisation/english/HOK_KOR_chinese_government_l_english.yml` | 신규 | `ADD` 후보, 실제 영어로 의미 번역 |
| `localisation/korean/HOK_KOR_chinese_government_l_korean.yml` | 신규 | `ADD` 후보, 한국어와 최종 TfV·자치령 안내 |
| `localisation/english/HOK_KOR_democratic_intelligence_l_english.yml` | 신규 | `ADD` 후보, 실제 영어로 의미 번역 |
| `localisation/korean/HOK_KOR_democratic_intelligence_l_korean.yml` | 신규 | `ADD` 후보, 한국어 |
| `localisation/english/HOK_KOR_democratic_support_l_english.yml` | 신규 | `ADD` 후보, 실제 영어로 의미 번역 |
| `localisation/korean/HOK_KOR_democratic_support_l_korean.yml` | 신규 | `ADD` 후보, 한국어 |
| `localisation/english/korea_focus_l_english.yml` | 수정 | 기존 영어를 보존하며 영향 문구만 의미 번역·병합 |
| `localisation/korean/korea_focus_l_korean.yml` | 수정 | 기존 표시·키를 보존하며 영향 문구 병합 |
| `gfx/interface/decisions/HOK_KOR/democratic_support/category.dds` | 신규 | `ASSET_COPY` 후보 |
| `gfx/interface/decisions/HOK_KOR/democratic_support/support_democracy_in_china.dds` | 신규 | `ASSET_COPY` 후보 |
| `gfx/interface/decisions/HOK_KOR/democratic_support/support_democracy_in_japan.dds` | 신규 | `ASSET_COPY` 후보 |
| `gfx/interface/goals/HOK_KOR/democratic_intelligence/secret_intelligence_service.dds` | 신규 | `ASSET_COPY` 후보 |
| `gfx/interface/goals/HOK_KOR/democratic_intelligence/shine_overlay.dds` | 신규 | `ASSET_COPY` 후보 |
| `gfx/interface/ideas/HOK_KOR/democratic_intelligence/secret_intelligence_service.dds` | 신규 | `ASSET_COPY` 후보 |

나머지79경로에는 기능·좌표·출처·사건 기록, 구조 설명·도표, README·AGENTS와 원본 `.agents` 스킬이 포함된다. 전부 호환판으로 복사하는 계획이 아니다. 이번에는 이 계획과 문서 인덱스만 작성하며, 후속 구현 때 필요한 원본 명세·그림 크레딧·지리 목록을 선택 보관한다. 원본의 새 지침·도표 스킬을 활성 로컬 지침으로 자동 채택하지 않는다.

## 4. 기능별 계약과 처리 대장

아래 **수정 제안**은 미적용이다. 현재 소스의 의도와 후속 필수 확인을 기록하며, 미확인을 정상 판정으로 바꾸지 않는다.

| 기능·호출자·분기 | 원본의 최종 동작과 보존 범위 | 처리와 남은 확인 |
|---|---|---|
| 중국·일본 지원 중점 → 지원 결정 | 기존 자동280일 지원을 정치력25·180일 반복 결정으로 전환. 선행은 `KOR_the_vanguard_of_asian_democracy`, 초대 중점과 배타 제거. 실제 해금 안내는 해당 결정을 가리킴 | **수정 제안**. 비용·동시 중복 차단·만료 후 재사용·가용 대상·AI·해금 표시를 함께 병합. 중국은 실존 대상 중 하나라도 기존 정신이 남으면 묶음 재지원을 차단하며 기존 타이머를 갱신하거나 새 출현국에 소급 지급하지 않음 |
| 중국 지원 대상 helper | 실존하는 정식 중국16태그를 선별. 동적 내전국 전체에 무제한 확장하지 않음 | **수정 제안 / RT56 대상 미확인**. 각 태그의 현행 정의·대표국 체계·존재/부재와 다른 국적 수혜 여부 확인 |
| 기존 `KOR_democrat_sponsored_by_korea`와 다른 호출자 | 중국·일본의 새 결정이 기존 기간제 정신을 재사용 | **의도적 유지**. 태국·VIN/MAL/PHI/INS 등 다른 소비자·기존 수치를 지원 결정 전환에 맞춰 일괄 변경하지 않음 |
| 정보국 `HOK_KOR_expand_secret_intelligence_service` | `KOR_begin_rearmament` 선행·상대 기준, x8/y1, cost5. 최종 `allow_branch`는 La Resistance만 요구하며 옛 독립당·민주 가지 조건은 대체됨. 정보기관이 없으면 생성하고 영구 정신 부여 | **수정 제안**. 최종 정신의 요원+2·`intel_network_gain=10`·별도 증가율25%·이념 지원 효율+100% 등은 원문과 함께 이식. 과거 민주 가지 배치·SHOW/HIDE 제한을 복구하지 않음. 포트 실제 좌표·인접 가지·DLC·AI 순서 확인 |
| 중국 축출 `KOR_overthrow_the_chinese_dictators` | 실존 CHI의 민주 지지도50% 이상, TfV, 기존 KCH 부재, 안전한597/743 거점과 기존 한국 민주/독립·중국 대표국 조건. 한국의 세력 맹주 조건은 제거됨. cost10의 기본70일, 진행 중 조건 상실 취소·생성 직전 재검사 | **수정 제안**. 49.9/50.0/50.1%·CHI 부재·다른 군벌만 고지지도·진행 중 하락을 구분. helper 실패가 helper 밖 전쟁명분까지 원자적으로 취소한다고 설명하지 않음 |
| 산둥 출범·영토 선택 | `original_tag=KCH` 동적국가. 적격597/743과 적격 SND 소유 본토 전부를 기본 선택한 뒤, 다른 원소유국별 지지도(상한90%) 예산으로 연결된 후보 확장 | **수정 제안**. 새 태그 SND를 만드는 기능이 아님. 원소유국·통제국·일본 종속 보호·지역 제외·거점 소실·SND 부재 대안을 같은 지리 집합에 맞춤 |
| 전력·비축·소멸 처리 | 안전한 첫 거점 → 필요한 공군기지 → 양수 비율의 육해공·비축/연료 이전 → 나머지 영토 이전 순서. 원국의 마지막 주는 전력 이전 뒤 넘김. 완전 소멸할 SND만 잔여 장비·수송선·연료를 정리 | **수정 제안**. 지지도0·고지지도·부분 통제·마지막 주·비행장 fallback·SND 보호영토 잔존을 나누어 확인. 지휘관은 귀순 대상에서 제외하며 다른 국가까지 잔여 자산을 지우지 않음 |
| 전용 웡원하오 | `HOK_KCH_weng_wenhao`를 KCH history에서 모집하고 실제 생성국으로 이동·승격. 기존 CHI 웡원하오를 직접 차용하지 않음 | **수정 제안 / 기존 저장 미확인**. RT56 portrait·인물 ID 충돌·실제 생성국 소유·이전 저장의 초기화 상태 확인 |
| 자치령·세력·후속 인정 | 최종 종속 단계는 `autonomy_dominion`, 요구 DLC는 Together for Victory. 전쟁 유지·세력 연결·기존 CHI 한정 인정/합병·전쟁명분 계약 유지 | **수정 제안**. `_mtg_tt` 키는 안정 ID로 유지하되 표시값은 TfV. 피감독국으로 되돌리거나 자동 선전포고·기출범 저장 소급 전환을 추가하지 않음. 동적 KCH 탐색·비맹주/무세력·후속 결정은 실행 미확인 |
| `KOR_minshu_ikki` → 일본 봉기 helper | 일본 지지도10–90%로 제한한 내전·전력 비율, 후속 한국 세력/참전 연결. 한국의 세력 맹주 조건을 제거했고 마지막 추가 변경은 일본 AI 전용 제한 제거임. 기존 한국 민주/독립·일본 비민주·35일 조건 유지 | **수정 제안**. 인간 일본의 실제 조작국 승계·기존 진영·내전·저장·MP는 미확인. 플레이어를 봉기국으로 이동시키는 새 효과를 임의로 넣지 않음 |
| 한국15주·기존 지휘관 해금·과학자/첩보원 계층 | 이번 원본 delta가 해당 이전 설계를 대체하지 않음 | **의도적 유지**. 지도 ID·기존 저장 guard·이름·초상화·기존 RT56 외국 모집을 보존하며 관련 계층을 수정할 때만 해당 필수 기록을 추가로 읽음 |
| 일반 CHI/JAP·세계 지도·공유 시스템 | 한국 경로에 필요한 연결만 검토 | **제외**. donor 중국지도·일본 전체 트리·전역 자치 규칙 복사나 새 replace_path를 추가하지 않음 |

## 5. 중국 지리 적응과 참조 누락 방지

원본 `HOK_KOR_chinese_government_is_mainland`는 바닐라 기반63주이며 `1032–1046`을 포함한다. 같은 번호가 RT56에서는 다른 지리이므로 숫자의 유효성만 확인해서는 안 된다.

| 구체적 접점 | 현재 근거 | 후속 처리 |
|---|---|---|
| donor trigger의1035·1038 | 원본 `common/scripted_triggers/HOK_KOR_chinese_government_state_triggers.txt:66,69`가 본토로 포함. 원본 `HOK_KOR_chinese_government_grant_mainland_cores`는 이 집합 전체에 코어 부여 | **수정 제안**. 그대로 이식하면 RT56 외국 지역까지 코어가 붙음 |
| RT56의 같은 번호 | `history/states/1035-Finnmark.txt:3,14`는 NOR, `1038-Kyme.txt:2,10`은 FIN 소유 이력 | **의도적 유지**. RT56 주를 중국으로 바꾸거나 재번호하지 않음 |
| 난징과 기존 KCH 수도 | RT56 `1114-Nanjing.txt`의11913, 포트 KCH history의1114. [기존 지역 적응 코드](../../tools/upstream_state_references.py)의 `CHINA_CORE_ADDITIONS=1111..1125`와 수도1114 처리 | **의도적 유지**. donor 수도1035를 다시 복사하지 않음 |
| 본토 helper·후속 코어·국가 생성 후보 | 새 helper의 코어 지급, 후보 수집·인접 확장·정리와 `KOR_New_China_Government`가 연결됨 | **수정 제안**. 같은 목적의 호출자가 같은 검토된 RT56 지역 집합을 소비하도록 연결 |
| 산둥 거점597/743·SND 기본 편입 | 원본의 안전한 첫 거점과 SND 부재 대안에 사용 | **의도적 유지 제안 / 실제 지리 미확인**. 현행 주의 province·인접·소유/완전통제·비행장을 확인하고 지역 의미가 같을 때 유지 |
| 선택 반복 상한63 | 원본63주 집합을 끝까지 순회하기 위한 유한 상한 | **수정 제안**. 확정한 RT56 집합의 크기·연결 확장에 맞춰 상한을 재검토하고 종료성을 보존. 기계적으로63을 고정하거나 무제한 반복으로 바꾸지 않음 |

전체 RT56 중국 대응표는 **미확정**이다. 기존 `1111–1125` 추가 목록은 조사 출발점이며 새63주를 무조건 1:1 치환하거나 최종 개수를 미리 확정하는 근거가 아니다. donor 지리 목록의 지역 의도·제외 지역, 실제 RT56 state/province 부모·인접 관계를 대조해 집합을 먼저 확정한다.

영토 이전·통제·핵심주·주둔군·수도는 별개로 검토한다. 특히 한국 소유/통제, 일본 및 직접·2단계 일본 종속 관계, 부분 통제, 본토 밖 섬·조차지·만주, SND가 정복한 본토와 남긴 보호영토를 구분한다. `ROOT/THIS/PREV/FROM`, owner/controller와 동적 생성국 event target의 scope도 호출 위치별로 기록한다.

## 6. 생성 소유권과 표시·그림 통합

기존 `korea.txt` 등은 여러 선택 이식과 최종 지휘관 계층의 생성·해시 잠금 대상이다. 원본 whole-file 복사나 최종 출력 수동 수정 대신 정확한 현재 포트 선조에 이번 delta를 적용하는 독립 계층을 설계한다. 후속 구현에서는 소유 source/lock·생성기·기존 writer의 전환/역투영·검사·pruning·통합 원장까지 함께 연결해야 한다. 기존 핀을 최신 원본으로 덮거나 이전 실패를 통과시키기 위해 해시 검사를 약화하지 않는다. 이번에는 그 파일들을 편집·실행하지 않았다.

영어 신규3파일과 기존 focus의 변경 문구는 실제 영어로 옮긴다. donor 영어 채널의 한국어 본문을 가져오지 않는다. 자치령·TfV·지원 비용/기간/재사용·50% 경계·생성국·지역·전력 비율의 의미와 키·토큰을 양 채널에서 맞추고 BOM·헤더·줄 끝을 보존한다. 기존 영어 `replace/HoK_countries_l_english.yml`의 `Free Republic of Shandong` 등 이미 채택한 국명도 대조한다. 한국어 RTK의 실제 덮어쓰기와 영어 RT56+포트 구성을 구분하며 일반판 영어 서브모드의 옛 지역 키를 유입시키지 않는다.

그림6개는 원본에서 선정한 기존 완성본을 그대로 재사용하는 후보이며 새 생성·재색칠은 계획하지 않는다. 영국 정보국·MI6·광택은 Paradox와 해당 권리자의 자산, 지원 결정은 기존 시민사회 DDS와 Globvs/Ultimate HOI4 GFX 계열 출처를 구분한다. 개별 사용 근거는 원본 크레딧·매니페스트를 따라 선택 보관한다. HOK 전용 sprite에서 저장소 내부 DDS·mask·overlay로 연결하고 공유 `gfx/FX/buttonstate.lua` 공급자는 따로 기록한다. 원본의 과거 치수·해시·검사 기록을 포트가 새로 확인한 결과로 쓰지 않는다.

원본의 상대 좌표·기준점과 도표도 그대로 포트 결과로 취급하지 않는다. 정보국과 이동한 지원 가지의 anchor 선언 순서·전체 상대 체인·조건부 offset·초대 가지·패널·AI 순서를 현재 포트에서 다시 계산한다. 배치를 구현할 때에는 AGENTS의 해당 원본 레이아웃 필수 문서와 최신 기능 명세를 함께 읽는다.

## 7. 검증 계획과 이미 알려진 한계

아래는 **후속 구현·실행이 승인되었을 때 필요한 검증**이며 이번 통과표가 아니다. 실제 helper·보고서·백업·로그/저장/화면 증거 사본을 만들기 전에 `C:\hoi\test\<task-or-run-id>\`를 정하고 모든 출력 경로를 확인한다. 활성 source cache는 시험 출력으로 사용하지 않는다.

| 단계 | 필수 확인 | 현재 상태 |
|---|---|---|
| 소스 기준 | 게임1.20/대상 RT56·donor·포트 재지문, 대상 버전 문법/공유 정의, 파일/논리 ID 충돌, 기존 미해결 지문·descriptor 계약을 별도 분류 | 설치 메타데이터·선택 지문과 Git 차이만 읽음. 전체 재기준화 미실시 |
| 생성·정적 | 독립 계층 재현·이전 writer 전환·원장/pruning, 전체 지역 목록·참조·scope·반복 상한, 키/토큰/BOM·sprite/그림 경로, 최종 `tools/validate_port.py` | 미실행 |
| 로드·UI | RT56 대조군과 최소 포트 구성, donor 비활성·실제 물리 경로·언어·DLC 기록, 새 프로세스에서 중점 연결·지원 결정·정신·광택·툴팁 | 미실행 |
| 지원·정보국 | 해금 전/후, 비용·중복 차단·만료/재사용, 중국 대상 존재/부재, 기관 있음/없음·LaR 없음, 새 AI 순서·각 정치 경로의 배치 | 미실행 |
| 출범 조건 | CHI 49.9/50.0/50.1%·부재, 다른 군벌만 고지지도, TfV 없음/있음, 기존 KCH 존재, 거점 소실·부분 통제·진행 중 취소 | 미실행 |
| 영토·전력 효과 | SND 기본 편입/부재/보호영토 잔존, 일본 종속 보호·한국 영토 제외, 연결 확장·예산, p=0/양수/상한, 마지막 주·비행장 fallback·소멸 잔여 처리 | 미실행 |
| 지도자·후속 | 유일한 영토 보유 `original_tag=KCH` 실제 생성국의 인물·수도·코어·한국 자치령 관계, 무세력/비맹주, CHI 한정 인정과 일반 중국/일본 보존 | 미실행. 동적 태그를 KCH나D04로 고정해 판정하지 않음 |
| 일본·진행 | AI 일본과 인간 일본 각각의 가용/내전·실제 조작국·세력/참전, 정상 중점 진행과 강제 효과를 분리 | 미실행 |
| 저장·장기 | 새 저장 왕복, 변경 전 미출범/기출범 저장의 지도자 초기화·중점/관계 보존, AI·DLC·MP·장기 경로 | 미실행. 기존 한국 지도 이관의 새 게임 전용 경계를 완화하지 않음 |

원본의 앞선 지원·피감독국·전면 편입·웡원하오 실행은 해당 시점의 소스·일반판·게임 구성에 한정된다. 최종 정보국 재무장 배치, 자치령/TfV, CHI 50%·70일, 인간 일본 허용의 실제 실행은 원본 기록에서도 미실행·미검증으로 남아 있다. 이를 현재 RT56·1.20 통과로 합산하지 않는다.

호환판의 직전 전체 정적 결과는 **11월14일의 9 PASS / 0 WARNING / 기존85 ERROR**다. 게임·호스트·RTK 지문/계약 차이와 연쇄 보고를 포함하며 독립적인 새 게임플레이 결함85건을 뜻하지 않는다. 이번 문서 작업에서는 재실행하지 않았다. 기존 원장 전체 생성의 차단·실제 RT56 지휘관 UI/저장 미검증도 [당시 기록](../implementation/2026-11-14-korean-commander-unlock-port.md)의 한계로 남는다.

## 8. 후속 진행 순서와 이번 문서 변경

후속 구현을 승인받으면 먼저 정확한 대상 게임·RT56 기준과 기존 실패를 분리하고 중국 지역 대응표를 확정한다. 이어 선택 원본·현재 포트 선조·권리/출처를 보관하고, 지원/정보국과 산둥/일본 봉기를 각각 연결 가능한 모듈로 구현한다. 생성 소유권·영어·그림·배치·AI를 함께 통합한 다음 위 검증을 수행하고 실제 결과는 별도 구현 기록에 남긴다. 콘텐츠 수나 파일 재고를 그대로 일괄 이식하는 근거로 쓰지 않는다.

이번 변경은 이 계획과 [문서 인덱스](../README.md)뿐이다. runtime·도구·잠금·원장·AGENTS·descriptor·원본·Workshop·설치 게임·사용자 데이터는 수정하지 않는다. 문서 내용·링크 대상·변경 범위의 읽기 대조만 하며, 게임 검사/생성기/formatter·HOI4·새 진단 helper는 실행하지 않는다. 새 테스트/진단 파일이나 입력 사본도 만들지 않는다.

기존 `tools/__pycache__/` **21파일·1,088,888바이트**는 정리 미결로 남는다. 저장소 `.local-artifacts`는 앞선 이번 업데이트 검토에서 발견하지 못했다. 활성 입력 `C:\hoi\test\hok-rt56-source-cache\sources\`와 기존 외부 보관 자료는 시험 폐기물과 구분하며 위치·내용을 바꾸거나 전체 해시를 재검증하지 않았다. 커밋·푸시·게시·업로드는 수행하지 않는다.
