# 2026-09-22 한국 중점 업데이트 이식 기록

상태: **한국 업데이트·MAN 후속 조건 반영 / 기본 fixture 118 PASS·1 FAIL·7 SKIP·NEP alternate 134 PASS·0 FAIL·0 SKIP / 임시 파일 없는 한국 UI 진행·최종 정적 20 PASS**. clean 실행의 후반 로그는 덮어써져 집계할 수 없다. 전체 실행 검증이나 릴리즈 준비 완료를 뜻하지 않는다.

이 문서는 [이식 계획](../plans/2026-09-22-korean-focus-update-port-plan.md)에 대한 사용자 구현 승인 이후의 변경을 기록한다. 한국 콘텐츠 반영과 갱신된 RT56 입력 대응을 구분하며, 코드 생성 완료를 플레이 가능 또는 호환성 검증 완료로 보고하지 않는다.

## 1. 범위와 기준선

| 항목 | 이번 작업의 기준 |
|---|---|
| 호환판 시작점 | `main@bfbba43c26022f3f64a88c2f1ec6600cb7f0d06f`; 앞선 계획·README 문서 변경을 보존 |
| 기존 HOK 기준 | `887930f6e88c80568d62dab9cfbe1ba8a498a252` |
| 한국 중점·지원 콘텐츠 | `da815305e3ce00186a487b3a378bf8536ff59146`의 19개 파일 |
| 한국 역사 AI | `118d7b53dfdbc120fcfe4b9d6792e66b2b519be7`의 1개 파일 |
| 조사한 donor HEAD | `81d39fadab9aaf75f3eb86873b39d2bec65c48d4`; 관련 한국 변경만 선택 |
| 현재 RT56 | Workshop `820260968`, manifest `7475007536894105204` |
| 설치 엔진 관찰값 | HOI4 `1.19.3.0.c01a`; 기존 `1.19.2.0.a729` 포트 실행과 구분 |
| 현재 실행 기록 | HOI4 `1.19.3.0.c01a (940d)`·DLC 36개. C1=RT56+RT56 Korean Translation+호환판, R0=RT56 단독, C0=RT56+첫 정의 복원 포함 호환판 |
| 쓰기 범위 | 호환 저장소의 runtime·도구·문서와 무시되는 로컬 입력 캐시 |
| 외부 입력 | donor·Workshop·바닐라는 읽기 전용. 승인된 게임 실행·새 임시 저장과 증거 보존은 실행 기록에서 구분 |

[C1·R0·C0 실행 감사](../audits/2026-09-22-korean-update-runtime.md)에 활성 구성·실제 경로·언어와 로그 해시를 기록했다. 9월 21일 donor 단독 실행은 포트 증거가 아니며 launcher 배열 순서를 데이터베이스의 유효 우선순위로 단정하지 않는다. C1의 번역 구성은 descriptor의 `Korean Language`와 달라 최종 언어 계약은 아직 미결정이다.

## 2. 고정 입력과 생성 소유권

[source_snapshot.py](../../tools/source_snapshot.py)와 [hok_source_lock.json](../../tools/hok_source_lock.json)은 기존 donor의 production/root 1,014개에 한국 업데이트 20개를 겹쳐 유효 입력 1,031개를 만든다. 20개 중 3개는 기존 파일의 새 개정이고 17개는 신규 파일이다. 최신 donor 전체를 복사하지 않으므로 별도 일본 민주 루트·일본 AI 연결·대만 변경은 들어오지 않는다.

- 기존 파일은 `887930f`의 Git blob을 사용한다. 한국 콘텐츠 19개는 `da81530`, 역사 AI 1개는 `118d7b5`로 출처를 구분한다.
- 경로별 commit·blob·SHA-256·checkout 방식을 고정한다. LF/CRLF 및 기존 혼합 개행은 기록된 방식으로 재현하고 최종 bytes의 SHA-256을 확인한다. 인코딩이나 개행을 일괄 정규화하지 않는다.
- 입력 캐시는 `.local-artifacts/sources/hok-887930f-korea-118d7b5`에 생성하며 Git에서 제외한다. 기존 캐시의 해시가 다르면 덮어쓰지 않고 중단한다.
- [build_korean_focus_update.py](../../tools/build_korean_focus_update.py)가 선택한 runtime 20개를 소유한다. [migrate_hok_ids.py](../../tools/migrate_hok_ids.py)의 일반 대상에서는 이 20개를 제외해 중복 생성 소유권을 피한다.
- 중점과 산업 결정은 기존 지도 ID 변환과 만주 보정을 적용한다. 나머지 18개는 선택한 donor bytes를 그대로 사용한다. 기존 출력에 독립 변경이 있거나 입력 해시가 달라지면 builder가 중단한다.

[통합 분류 원장](../audits/2026-09-06-production-file-classification.csv)은 기존 경로를 유지하며 다시 생성했다. 기존 8개 컬럼 뒤에 `donor_source_commit`, `donor_source_blob`, `donor_source_sha256`, `donor_source_checkout`을 추가했다. 원장의 날짜가 붙은 파일명은 최신 donor 전체를 9월 6일에 감사했다는 의미가 아니다.

| 분류 | 현재 행 수 |
|---|---:|
| ADD | 136 |
| USE_RT56 | 63 |
| THREE_WAY_MERGE | 31 |
| OVERRIDE | 9 |
| BINARY_MERGE | 18 |
| ASSET_COPY | 774 |
| 합계 | 1,031 |

기존 분류는 유지하고 신규 17개만 ADD로 늘었다. 동일 경로 RT56 충돌 기준은 73개이며, 새 ADD 경로가 호스트와 충돌하면 재분류 검토 없이 통과시키지 않는다.

## 3. 한국 콘텐츠 반영

[한국 중점](../../common/national_focus/korea.txt)은 기존 266개 ID를 유지하고 산업·교육 20개, 군사 25개, 민주·외교 15개를 추가해 총 326개다. 최신 원본의 상대 배치 319개·절대 기준 7개와 바로가기를 반영했으며, 신규 가지를 기존 경로의 필수 선행으로 삽입하지 않는 원본 연결을 보존했다.

### 기간 집계의 기준 차이

이번 호환판의 `bfbba43` 대비 **cost 10 → 5 변경은 154개**다. 계획과 원본 최초 확장 기록의 152개는 원본의 확장 직전 작업 트리와 비교한 수치다. 그 작업 트리에는 다음 두 중점의 선행 단축이 이미 들어 있었지만 기존 호환판에는 둘 다 cost 10으로 남아 있었다.

- `KOR_the_vanguard_of_asian_democracy`
- `KOR_stop_moderate_diplomacy`

따라서 호환판 반영에서는 원본 최초 확장의 152개와 위 2개를 합친 154개가 70일에서 35일로 바뀐다. 신규 60개도 cost 5다. 이는 추가로 두 중점을 임의 조정한 것이 아니라 승인한 최신 donor 상태를 서로 다른 비교 기준으로 집계한 결과다.

### 보상·지원 콘텐츠·AI

- 최신 원본의 후속 37개 완료 보상 조정, 국민정신 29개(산업 11·군사 12·민주 6), 결정 10개·분류 3개, 외교 이벤트 6개와 관계 수정치 1개를 반영했다.
- 지역 산업 사업 4개는 회당 정치력 150·민간공장 5·90일의 순차 반복형이다. 동맹 공동개발은 회당 정치력 75·민간공장 2·180일이며 기존 비용·진행 중 중복 방지·조건 상실 시 무보상 정책을 보존한다.
- 실업·시민교육의 경기·전라·충청 공장 지급은 세 주의 소유·완전통제·부지를 착수와 완료 시 재검사하고 각 주에 슬롯 2·민간공장 2를 준다. 과거 완료 중점에 새 보상을 소급 지급하지 않는다.
- 산업·군사·민주·바로가기 현지화 4쌍을 함께 추가했다. English 채널도 한국어 본문을 쓰는 기존 HOK 계약이며 신규 영문 번역을 제공하는 변경이 아니다.
- [역사 AI 계획](../../common/ai_strategy_plans/KOR_historical_strategy_plan.txt)은 기본 목록 51개를 106개로 확장하고 방어전·만주 승전 후 아시아 연합 창설·창설 후 협력 지원 계획 3개를 추가했다. 양수 우선순위 대상은 고유 118개이며 그중 신규 확장 중점은 53개다. 이는 확정된 게임 일정이나 실제 AI 선택 검증 결과가 아니다.

원본의 **보병장비 한정 생산량 +10%와 상위 국민정신 승계는 미적용 상태를 유지**한다. 생산 비용 약 -9.09% 대안도 구현하지 않았다. 기간 단축과 보상 강화는 HOK의 의도적 후속 콘텐츠·균형 변경으로 기록하며 호환성 수리로 설명하지 않는다.

## 4. 유지한 호환 동작

[ADR-0002](../decisions/0002-map-id-migration.md)의 전체 province/state 매핑을 유지했다. 신규 지역 사업의 강원 `1029→1144`, 충청 `1031→1145`, 경상 `1030→920`은 착수·취소·보상·지도 강조에 모두 적용된다. 신규 시민교육의 전라 `1082→919`, 충청 `1031→1145`를 같은 방식으로 이전했고 경기 525는 유지했다.

만주 기존 8개 주와 RT56 분할주 `941–947`의 총 15개 처리를 보존했다. 중점 3개의 분리주의 완화·제거에 필요한 35개 행을 최신 트리에 다시 적용했다. 기존 만주 승전·만슐루스·국뽕 초기화·대일 강화 결정 및 이벤트의 보정도 유지한다. MAN의 종속 관계 소멸 때문에 강화 결정이 사라지지 않도록 한 조건과 잔존 MAN의 전쟁·일본 합병 조건을 원본 복사로 되돌리지 않았다.

일반 일본·중국 콘텐츠는 RT56 소유라는 [ADR-0004](../decisions/0004-hok-korean-content-priority.md)를 유지한다. 별도 donor 일본 업데이트와 `HOK_JAP_strengthen_civilian_government`에 연결된 donor AI 변경을 이번 한국 업데이트에 동반하지 않는다. RT56 KOR 전략과 기존 KOR history/OOB·폐기 기술 제거·단일 음성 registry·한국 항공기 고유 ID도 유지한다.

## 5. 갱신된 RT56 입력 대응

현재 manifest는 기존 `3323396725579032799`와 다르다. 입력 해시 차이를 무시하지 않고 현재 호스트 파일을 조사·재고정한 뒤 기존 생성 절차를 적용했다. 한국 중점 업데이트와 별도로 다음 9개 runtime 산출물이 현재 RT56 기준으로 달라졌다.

| 파일 | 소유·병합 범위 |
|---|---|
| `common/bookmarks/the_gathering_storm.txt` | 현재 호스트 bookmark와 기존 한국 시작 블록 |
| `common/military_industrial_organization/organizations/00_generic_organization.txt` | 현재 generic MIO와 기존 한국 제외 조건 |
| `common/scripted_triggers/unit_medals_scripted_triggers.txt` | 현재 훈장 trigger와 기존 한국 통합 |
| `events/WTT_Japan.txt` | 현재 일본 이벤트와 기존 한국 독립 연결 |
| `history/general/generic_advisors.txt` | 현재 generic advisor와 기존 한국 제외 조건 |
| `map/buildings.txt` | 현재 호스트 배치와 기존 한국 delta·항구 spawn 복원 |
| `map/railways.txt` | 현재 호스트 철도와 기존 한국 연결 |
| `map/supply_nodes.txt` | 현재 호스트 보급 거점과 기존 한국 참조 |
| `map/unitstacks.txt` | 현재 호스트 unit stack과 기존 한국 위치 |

`map/provinces.bmp`, `map/definition.csv`와 기존 한국 state 산출물은 이전 포트와 동일하다. 새 province/state를 할당하거나 한국 지형·지도 설계를 바꾸지 않았다. 텍스트 지도 4개의 호스트 갱신은 게임 내 보급·배치 검증과 구분한다.

### C1에서 발견한 기존 MAN 참조 누락의 별도 수선

C1 로그에서 RT56 MAN 캐릭터의 `has_idea = kim_chang_ryong` 참조 오류를 확인했다. 포트의 `common/characters/KOR.txt`는 이번 한국 업데이트 전후에 동일하며 RT56의 해당 캐릭터 정의를 포함하지 않았다. 이번 업데이트에서 삭제된 항목으로 분류하지 않는다. 근거와 408건 오류 집계는 [실행 감사](../audits/2026-09-22-korean-update-runtime.md#분리해서-다룰-오류)에 남겼다.

[build_shared_overrides.py](../../tools/build_shared_overrides.py)는 현재 RT56 KOR SHA-256 `979185140DA5A9CA57AC8399A47DA5EBFA9157C9FD2F2AACBD51E7E4E8C078CA`를 고정하고 `KOR_kim_chang_ryong` 블록을 원본 그대로 추출해 [zz_hok_rt56_kor_host_references.txt](../../common/characters/zz_hok_rt56_kor_host_references.txt)에 등록했다. 기존 shared 출력 10개는 이 첫 시도 전후 동일하며 모집·history·MAN 조건과 균형은 바꾸지 않았다. 그러나 C0-GER-first의 시간 진행 중 같은 MAN 오류가 보존본에 1,678건 반복되어, **미모집 캐릭터의 정의 복원만으로 idea 참조가 유효해진다는 가설은 실패했다**. 첫 시점의 정적 통과를 수선 성공으로 해석하지 않는다.

후속 도구는 RT56 MAN SHA-256 `CFE4943CF980417F047F90E920B1171E1ABBBF1647AEF1E7DC58AE37B7F53BF0`를 고정하고 MAN의 두 KOR 조건만 `has_character` 조건부 guard와 character scope의 `is_hired_as_advisor` 검사로 바꾼다. donor에 MAN 파일이 없으므로 원장 생성기는 이 RT56 기반 출력을 기존 KOR 통합 행에 귀속한다. ESC 중단 당시에는 도구만 준비된 상태였으나, **사용자 재개 승인과 게임 종료 확인 후 `common/characters/MAN.txt` 및 원장을 생성하고 aggregate 20 PASS를 확인했다.** 한국 인물 미모집 정책과 나머지 MAN 내용을 유지하는 별도 호환 수선이며, 한국 업데이트 20개·호스트 갱신 9개와 구분한다. 기본 C1 fixture에서의 후속 관측은 아래에 별도로 기록한다.

## 6. 검증 결과와 남은 실행

| 항목 | 현재 기록 |
|---|---|
| 입력 캐시 | `source_snapshot.py --check` 통과; 고정 입력과 cache bytes 대조 |
| 한국 출력 생성 | builder preflight 통과, 20개 runtime 파일 생성 |
| 독립 원본 대조 | 18개 SHA-256 동일; 중점·산업 결정 차이는 승인된 ID 이전·만주 행·포트 주석으로 한정 |
| 신규 참조 조사 | 현재 RT56 common/events/localisation에서 `HOK_KOR_` 충돌 발견 없음; 신규 군사 기술 참조·KOR MIO 3개 존재 확인 |
| 통합 원장 | 1,031개 행, 출처 commit/blob/hash/checkout 기록 |
| aggregate 정적 검사 | 첫 정의 복원·후속 MAN 생성·최종 임시 파일 제거 및 README 확정 뒤 각각 `20 PASS / 0 WARNING / 0 ERROR`. 최종 결과는 `static-validation-final.txt`, exit 0 |
| 한국 중점 의미 검사 | `check_korean_focus_update.py --check` 통과; `--self-test`에서 13개 회귀 사례 모두 거부 |
| 공백 검사 | 도구·문서·README는 `git diff --check` 통과. 전체 차이에는 원본에서 계승한 중점 146곳·RT56 MIO 11곳의 trailing whitespace만 남음 |
| C1 HOI4 실행 | KOR 새 게임 진입·15일 진행·중점 하나 완료·같은 프로세스의 임시 저장 재로드 관측; MAN 수선 전 실행 |
| R0 대조 | RT56 단독 GER `1936.01.18 05`까지 진행·같은 프로세스의 임시 저장 재로드. 저장 이름 변경 실패·PRC 오류 재현, MAN 오류 0건 |
| C0 첫 수선 실행 | RT56+호환판 GER 지도 진입·시간 진행 성공. MAN 오류 1,678건으로 정의 복원만 하는 첫 시도 실패; C0 저장·재로드는 미실행 |
| 후속 실행 | 두 C1 fixture 실행 및 임시 파일 해시 대조·제거 완료. NEP alternate 134 PASS·0 FAIL·0 SKIP; fixture 없는 KOR 4월 28일까지 UI 진행 확인, 후반 로그 집계 불가 |
| 기존 세이브·멀티·DLC 분기·실제 AI | 이번 이식으로 검증하지 않음 |

중간 집계 `19 PASS / 0 WARNING / 1 ERROR`의 검사 모델 문제를 보완한 뒤 첫 MAN 정의 복원 시점의 20 PASS를 확인했고, 후속 MAN 조건 생성과 최종 정리 뒤에도 각각 별도로 20 PASS를 확인했다. 최종 로그 `.local-artifacts/audits/2026-09-22/static-validation-final.txt`의 SHA-256은 `098F8AA8807CAB593DD71F6931B12107574F9EEEF60E0D5A71918770AAC424E5`다. 원장 1,031행·충돌 73개와 분류 수는 유지된다. 회귀 사례를 거부한 결과는 검사가 해당 결함을 탐지한다는 증거이며 엔진 동작의 증거는 아니다. 역사 AI의 실제 선택 등은 여전히 미검증이다.

### 후속 C1 한국 기본 fixture의 결과

`.local-artifacts/runtime/2026-09-22/C1-KOR-harness-default/`의 로그·결과 요약을 기준으로 **118 PASS / 1 FAIL / 7 SKIP**다. 스크립트로 완료한 중점 58개, 최종 국민정신 17개 존재·이전/미선택 10개 부재, 시민교육 state 525·919·1145의 민간공장 +2가 통과했다. 네 지역 사업은 두 회차 모두 예정 89일 시점 활성·조기 지급 부재, 완료 검사에서 첫 +1·누적 +2가 통과했다. 정상 UI의 중점 기간·정치력 비용·모든 보상 수치를 검증한 것은 아니다.

실패는 RT56에서 영국 종속국인 BHU를 시험 세력에 넣지 못한 fixture 준비 조건 1건이며, 취소·협정 관련 7건은 생략됐다. 최종 `RESULT_FAIL`을 보존하고 production 결함이나 전체 통과로 바꾸지 않는다. 독립국 NEP를 사용하는 alternate 보완 시험은 아래에 분리한다.

MAN·fixture·신규 HOK 오류는 1월 1일부터 실행 담당자가 보고한 `1936.08.13.02`까지 각각 0건이다. 전체 오류는 710행으로 0건이 아니며 7월 엔진 자동저장에서 `_temp.hoi4` 생성과 rename 실패가 관측됐다. 종료 후 설치 해시와 대조하여 임시 on_action·event 두 파일을 제거했고 production 입력 해시는 그대로였다. 상세 한계와 해시는 [실행 감사](../audits/2026-09-22-korean-update-runtime.md#c1-kor-harness-default-man-후속-조건과-한국-기본-fixture)에 보존한다.

### NEP alternate 보완 결과

`.local-artifacts/runtime/2026-09-22/C1-KOR-harness-nepal-alternate/`는 **134 PASS / 0 FAIL / 0 SKIP**, `1936.07.04.11`의 `RESULT_PASS / END`를 기록했다. 반대 선택 중점 2개를 포함한 58개 완료로 두 fixture의 합집합은 신규 60개다. 평안 사업의 취소·무보상·주 복구·재착수, 관세·면허 협정 수락과 양방향 면허 관계, 세력 탈퇴 후 국민정신·관계 정리, 네 사업의 두 회차 보상과 조기 지급 부재를 확인했다. 정상 UI 비용·선행·기간, 협정 거절·자연 만료, 실제 AI 계획 검증과 구분한다.

MAN·fixture·신규 HOK 오류는 각각 0건이나 전체 오류는 730행이다. 시험 `END` 뒤 조작 중단 중 `1937.05.10.17`까지 로그가 진행했고 이후 프로세스 부재를 확인했으나 종료 원인은 미확인이다. 이를 정상 종료나 장기 안정성 증거로 확장하지 않는다. 임시 두 파일은 해시 대조 후 제거했고 한국 production 20개 해시는 유지됐다.

### 임시 파일 없는 한국 새 게임과 최종 정리

C1-KOR-clean-final(PID 55740, 체크섬 `27e6`)의 초기 로그에는 fixture 등록·실행 기록이 없고 MAN·fixture·신규 HOK 오류도 각각 0건이었다. 실행 담당자는 `우리황실사랑회`와 `라디오 미디어 장악`의 정상 진행·완료, 원화평가절하의 정상 UI 선택·완료 창·국민정신과 한국어 표시를 확인했다. 최종 UI는 `1936.04.28.22` 일시정지였다. 원화평가절하 tooltip은 소비재 −5%·안정도 −5%·1938.03.21 제거 예정으로 표시됐다. 저장된 중점 진행일수가 적용되어 정확 35일 경과를 측정한 것은 아니며 4월 15일은 완료 창의 관측일일 뿐이다. 이 clean 실행에서 수동 저장·재로드는 하지 않았다.

담당자의 종료 확인 이후 별도 PID 54556이 02:18:32에 시작해 live logs를 덮어썼다. 실행 주체는 미확인이고 새 실행 자료는 별도로 보존했다. 따라서 초기 698행·MAN/fixture/HOK 0건을 4월까지 확대하거나 후반 전체 오류 수를 확정할 수 없다. 이 한계와 UI 관측은 `C1-KOR-clean-final/final/observation.json` 및 [실행 감사](../audits/2026-09-22-korean-update-runtime.md#c1-kor-clean-final-임시-파일-없는-한국-ui-확인)에 기록했다. 최종 원장·정적 검증은 위 결과처럼 완료했고 Git commit·push·tag·게시 작업은 하지 않았다.

사전 실행에서 `-userdir`가 적용되지 않아 기존 donor가 로드된 것을 확인하고 해당 PID `50776`만 00:42:52에 종료했다. 시험 전 로그는 `.local-artifacts/runtime/2026-09-22/pre-test-donor-logs`, 이 실패 시도의 로그는 `ignored-userdir-donor-logs`에 구분하여 보존했다. 두 기록 모두 RT56 단독 control이나 RT56+포트의 런타임 결과로 집계하지 않는다. 이후 실제 C1의 로그·구성·해시는 `.local-artifacts/runtime/2026-09-22/C1-initial/`에 보존했다.

[실행 감사](../audits/2026-09-22-korean-update-runtime.md)에는 신규 지원 파일의 로더 등록, C1 한국 정치 화면과 `1936.01.16 07`까지의 진행을 기록했다. 전체 326개 중점과 신규 보상·AI를 모두 검증한 것은 아니다. 저장 최종 이름 변경 실패와 PRC advisor 재로드 오류는 R0에서도 재현되어 포트 없이 발생함을 확인했다. 파일 이름 변경의 구체적 환경 원인과 PRC의 엔진 내부 원인은 확정하지 않는다.

[9월 6일 새 게임 크래시](../incidents/2026-09-06-post-port-new-game-crash.md)의 실패 지점을 이번 C1·C0는 넘어 진행했다. R0 대조도 진행했으나 엔진과 호스트가 달라 항구 spawn 보정만으로 과거 사건의 원인을 확정하지 않는다.

후속 실행에서는 번역 없는 C0 한국과 아직 다루지 않은 중점 UI·선행·배타, 15개 만주 주와 대일 강화, 협정 거절·자연 만료, DLC 대체 보상, AI 지원 계획 전환을 확인한다. 선택할 언어 구성의 R1/C1 대조도 남아 있다. 세이브는 신규 게임 전용 정책을 유지하며 같은 프로세스의 임시 저장 재로드를 정상 파일 저장·새 프로세스 재로드나 기존 저장 호환성으로 설명하지 않는다.

## 7. 계승 경위·출처와 게시 정체성

사용자가 제공한 경위는 원작자의 업데이트가 중단되어 사용자가 계승·후속 개발을 진행하고, 원작자가 복귀하면 협의한다는 것이다. 이는 사용자 제공 설명으로 기록하며 원작 HOK와 후속 donor, RT56 및 이 호환판의 기여·정체성을 구분한다.

| 구분 | 항목과 출처 |
|---|---|
| 원작 HOK | Workshop [2898629778](https://steamcommunity.com/sharedfiles/filedetails/?id=2898629778), 원작자 `oixxta` — 원작 페이지의 제작자 표시 |
| 제공된 donor 개정 | Workshop `3793992662`; 이번 한국 업데이트의 직접 소스는 위 고정 Git 커밋 |
| RT56 | Workshop [820260968](https://steamcommunity.com/sharedfiles/filedetails/?id=820260968), 호스트·의존성 |
| 별도 호환판 | descriptor에 기록된 `3796816200`; 기존 항목과 구분하며 후속 게시 시 대상 재확인 |

원작 HOK의 저자·콘텐츠·주석과 donor 후속 개발 기여를 보존한다. RT56 병합과 이번 호환 이식의 기여는 별도로 표시한다. 원작 또는 RT56의 공식판이라는 표현을 새로 사용하지 않았다.

이번 구현에서 donor·Workshop·게임 설치 소스를 수정하지 않았다. 승인된 실행의 구성·새 임시 저장·로그 보존은 별도 실행 감사에 기록하며 기존 세이브를 변경하지 않는다. Git commit·push·tag와 외부 게시·업로드·Workshop 메타데이터 변경은 수행하지 않았다. runtime 파일의 구현 변경은 이 호환 저장소의 작업 트리에 남아 있다.
