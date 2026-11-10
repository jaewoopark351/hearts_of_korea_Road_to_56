# 문서 인덱스

이 폴더는 Hearts of Korea × The Road to 56 신규 호환 포트의 설계, 결정, 구현, 감사와 검증 기록을 보관한다.

현지화·표식/변수 표시 또는 주·프로빈스 참조를 검토하거나 변경하기 전에는 [변경 영향 검토 절차](HOK_CHANGE_COVERAGE_REVIEW.md)와 그 절차에서 연결하는 분야별 로컬 스킬을 읽는다. 2026-11-09 지침 도입은 문서 전용이며 기존 콘텐츠의 전수 감사나 추가 런타임 검증 결과가 아니다.

## 현재 상태

- 2026-11-10 연구·장비 일본식 이름: **v6 구현·선택한 한영 구성의 범위 UI·수집·임시 설정 복구와 별도 승인된 외부 등록파일 영구 동기화 완료**. 자체 정적39/0·독립35/0, aggregate28 PASS·0 WARNING·기존11 ERROR(exit1)다. KO07과 EN04에서 각각 수정15/17문구·3guard·JAP 대표7표시 불일치0,99수집 사본·3출력 무결·기존82저장 차이0·새 저장0을 확인했다. EN03 중단은 정상 종료 미관측·장비명 검증0의 별도 이력으로 보존한다. 영어17키·RTK 동일 경로 한국어1,308키 병합·저장소 RTK 의존성을 사용하며 대상17값 외1,291키·나머지 원문 바이트와 기존3guard·장비 성능·기술을 보존한다. 1953년형2키는 한영 모두 소스 전용이고 광범위한 replace_path는 추가하지 않았다. 임시 시험 종료 후 원본304바이트·사용자 metadata6개를 복구한 뒤, 별도 영구 승인으로 외부 `.mod`에 시험과 같은 RTK 의존성37바이트만 다시 반영했다. 현재 외부 파일은341바이트이며 그 파일 외 metadata는 원본이다. RTK 없는 한국어·모든 번역 조합과 최종 Workshop 의존성·재배포 계약은 확정하지 않는다. 이 계층 조사·수정·재생성·검증 전 [구현·실패 이력·실제 확인 상태](implementation/2026-11-10-korean-equipment-localisation-repair.md)와 [최초 계획](plans/2026-11-10-korean-equipment-localisation-repair-plan.md)을 읽는다. v1–v5 실패·EN2 화면 유실·기존11오류를 후속 결과로 덮지 않는다.

- 2026-11-10 원본 지역 산업 업데이트: **기존4출력 선택 구현·범위 정적 확인 완료 / 실행 검증 대기**. 5중점 보상 강화·남북 독립 투자3개 추가·한영 각16값을 반영하고 연구망 함남 표시는 이미 적용돼 유지했다. 독립 정적219/0, aggregate **27 PASS / 0 WARNING / 11 기존 ERROR**로 사전과 오류 본문이 같다. 이번 계층 수정·재생성·검증 전 [변경 범위·처리 대장·실제 확인 상태](implementation/2026-11-10-korean-industry-update-port.md)와 [선택 입력 안내](upstream/hok-industry-update-20261110/README.md)를 읽는다. 기존 실행 결과를 새 업데이트의 검증으로 사용하지 않는다.

- 2026-11-09 재벌 영어 표현: 영어 8파일·43개 값을 `corporate oligarchs`/`conglomerates`로 문맥에 맞게 수정하고 AGENTS·현지화 스킬에 의미·논조 번역 지침을 추가했다. 기존 식별자·한국어·게임플레이와 과거 입력은 유지한다. 해당 문구 수정·재생성 전 [구현·소스/검사 기록](implementation/2026-11-09-chaebol-english-terminology.md)과 [유지 입력 안내](upstream/hok-english-terminology-20261109/README.md)를 읽는다. 이번 작업은 새 게임 실행이나 기존 미검증 UI 항목의 통과가 아니다.

- 2026-11-09 검토 후속 수선 **구현 적용 / 실제 UI 검증 차단 / 사용자 프로필 복구 완료 / OSK 창 잔존**: civic 수치 metadata6곳·한영 새 키1쌍과 내륙 부유항1행 제외를 네 출력에 반영했다. aggregate는 **25 PASS / 0 WARNING / 11 기존 ERROR**이며 최초 원장 실패와 저장 덮어쓰기 사건도 보존한다. R0/C0 smoke와 새 BASE raw16/0은 실제 CIV 효과·저장 왕복 완료가 아니다. UI 차단 뒤 사용자의 판단 위임에 따라 소유 게임에 `/F` 없는 종료 요청을 보내 PID 부재를 확인·수집했으며 정상 UI 메뉴 종료는 관측하지 않았다. 원래 metadata18개·저장75개·선택과 시험 `.mod` 부재를 복구하고 runtime1,476개 중 네 변경만 남김을 확인했다. 접근 거부로 OSK 창은 남았고 CIV 실제 표시·지급·guard/clamp·저장과 LOC-02/03은 미검증·후자 코드 유지다. 재개 전 [계획의 현재 상태](plans/2026-11-09-localisation-state-review-followup-plan.md)와 [구현·실행·사건·종료/복구 기록](implementation/2026-11-09-review-followup-repairs.md)을 읽는다. 최초 문서 전용 단계와 저장 사건을 뒤의 차이0으로 덮지 않는다.
- 2026-11-09 RT56 자동 갱신 대응 마감: 승인된 manifest `1963361040482473746`의 호스트4개와 HOK32개를 연결하고 지도24·기존 source pins·승인된 회복 수선을 보존했다. 실제 CNDP 비용/타이머·선택 저장·한영 회복 UI와 refs6을 각 한계 안에서 관측했고, 세션 종료·수집·프로필 복구 및 파일 보존 감사 **68/0**을 완료했다. 최종 aggregate는 **23 PASS / 0 WARNING / 11 기존 ERROR**다. PRC 경고군은 RT56 단독 재로드에서도 재현됐으며 근본 원인은 미확정이다. 첫 watcher 실패와 수선 전 overflow 등 과거 실패도 보존한다. [실제 상태·남은 한계](implementation/2026-11-08-hok-upstream-content-port.md), [ADR-0008](decisions/0008-november-rt56-host-update.md), [새 호스트 입력](upstream/rt56-host-update-20261108/README.md)을 읽는다.
- 2026-11-08 원본 `596b221` 후속 구현: **CNDP13·표시·한국/외국 참조32출력(기존13+신규19) 소스 통합과 선택 범위 실행·복구 완료**. 초기913/0/1 runtime UNVERIFIED와 aggregate21/0/11은 수선·새 호스트 대응 전 계층의 과거 기록이다. 현재의 확인 범위와 미검증 동작을 전체 호환성·무오류로 확대하지 않는다. FRI 인도차이나·Singapore·KCH1114·SOV/코민테른1152의 결정은 [ADR-0007](decisions/0007-november-content-integration.md), 실제 결과·증거·복구는 [구현 기록](implementation/2026-11-08-hok-upstream-content-port.md)을 따른다. 이 계층 수정·재생성·검증 전 해당 기록과 [선택 입력 안내](upstream/hok-content-update-20261108/README.md)를 읽는다.
- 2026-11-08 최초 문서화 이력: 기존 분할 donor42입력 중37개 동일·5개 추가 변경, 동결밖31개를 합친36경로를 검토 후보로 기록했다. [최초 이식 계획](plans/2026-11-08-hok-upstream-content-port-plan.md)은 당시 문서화 전용 결과이며 이후 승인된 구현·실행 결과와 구분한다. 후보36개 전체 복사나 지침 파일 동기화를 수행한 것으로 해석하지 않는다.
- 2026-11-07 한국 9→15주 분할과 연결 콘텐츠: **47출력·신규 경로9개 구현 및 이번 범위 검증·환경 복구 완료**(11월8일 KST). 전체 정적 **19 PASS / 0 WARNING / 11 기존 ERROR**, 지도/주 독립 정적 **7,180/0**, final suite **190 PASS / 0 MISMATCH / 10 UNVERIFIED**다. 영어 새 저장 cold reload·한국어 C1·국뽕 두 옵션과 보상/부분 상실/슬롯/반복/활성 저장 인게임 재로드를 각 범위로 확인했다. 미검증10개는 BASE 재로드 뒤 startup marker·fresh Verify 재클릭이며 모든 런타임 통과를 주장하지 않는다. 사후 원본42·host/schema1,193·출력47 지문은 일치했고 원래 프로필20개·저장43개를 복구/보존했다. 현재 RT56의 1939 미지원과 실제1936 카드만의 UI, 기존11개 정적 부채·새 게임 한정·배포 언어 계약 미확정은 유지한다. 주 분할을 수정하거나 검증하기 전에 [전체 계획](plans/2026-11-07-korean-state-split-port-plan.md), [ADR-0006](decisions/0006-korean-state-split-integration.md), [구현·검증 기록](implementation/2026-11-07-korean-state-split-port.md)을 읽는다.
- 2026-11-07 원본 업데이트 **강원·포항 반복 자원 확장과 신아리랑 44.1kHz 이식**. RT56 실제 게임에서 두 사업의 90일 완료 두 회차, 취소, 저장 재로드와 신아리랑 재생을 확인했다. [선택 이식 계획](plans/2026-11-07-hok-upstream-delta-port-plan.md) · [구현·검증 기록](implementation/2026-11-07-hok-resource-prospecting-port.md)
- 2026-10-12 원본 d4031aa 재벌·시민사회: **한국 runtime31개 선택 이식, playable472개·신규13중점·20정신·13결정/mission·11사건·영향력패널 반영**. 이전 생성 출력405개·RT56 지역 병합·historical lock10개 보존. Civic scoped 정적/회귀26개와 기존 royal/선행57개 통과, aggregate **18 PASS / 0 WARNING / 5 기존 ERROR**, 현재 실행 미검증. 기존 host drift·descriptor pin은 아래 [구현 기록](implementation/2026-10-12-korean-civic-update-port.md)에 구분했다. [472개 좌표 명세](HOK_KOREAN_CIVIC_LAYOUT_COORDINATES.md).
- 2026-10-11 미사일 기지: **함경918·충청1145의 HoK 우선 배치와 정적 검증 완료, 실제 UI 검증 대기**. RT56 위치3행 제외·HoK 함경1행 복원, buildings-only에서 철도 포함 동반 지도17개 보존. 외부 회귀34 PASS·독립 과거 정규화12개 변형 거부; aggregate 작업 전16/0/5 → 작업 후17/0/5(같은 기존 host drift4·descriptor pin1). 전체 지도·철도 source drift와 실행 증거는 별도 미완료다. 최초 문서화 전용 요청과 수정 전 지문을 [수정 계획](plans/2026-10-11-korean-rocket-site-fix-plan.md)에 보존하고, 후속 구현 승인·검사 결과를 [구현 기록](implementation/2026-10-11-korean-rocket-site-fix.md)에 구분했다.
- 2026-10-10 원본 `4d8241e` 왕정 업데이트: **A2/A3/A4·H2의 추가 완료 조건 제거, H1 물자 4중점 배치·선행 이동, 연락망 국민정신 I/II 형성 전 유지 반영**. 보상·기간·AI·RT56 지역 조건 보존, 460개 좌표 명세 추가. scoped 정적 통과·회귀57개 거부; aggregate **16 PASS / 0 WARNING / 5 ERROR**(기존 host drift4·시작부터 존재한 descriptor 바이트 pin1). 이번 호환판 실행 미검증. [구현 기록](implementation/2026-10-10-korean-royal-update-port.md), [포트 좌표 명세](HOK_KOREAN_ROYAL_LAYOUT_COORDINATES.md).
- 2026-10-10 원본 `af6fccf` 업데이트: **한국 중점 6개의 선행 조건 선택 이식**. 채굴의 두 AND 선행 연결 표시와 진입 조건 5개 완화, 보상·기간·좌표·AI·후속 조건 보존. 원본 문서 7개·독립 lock·원장 갱신, subsystem 통과·회귀51개 거부, aggregate **17 PASS / 0 WARNING / 4 기존 source drift ERROR**, 이번 실행 미검증. 최신 RT56 manifest `7553774178744855191`의 기존 공용 입력 7개 drift를 [구현 기록](implementation/2026-10-10-korean-focus-prerequisite-port.md)에 별도로 기록했다.
- 2026-10-05 최신 원본 변경: **폐쇄형 원료 순환체계 중점의 기존 긴급 결정 해금 툴팁 2줄 이식 완료**. donor `062a602`와 새 작성 지침을 선택 반영하고 기존 효과·조건·RT56 병합을 보존했다. aggregate **20 PASS / 0 WARNING / 1 기존 history ERROR**, 이번 UI·실행 미검증. descriptor의 내용 없는 checkout 개행 복원과 기존 원장 해시 갱신은 [구현 기록](implementation/2026-10-05-focus-decision-tooltip-port.md)에 구분했다.
- 2026-10-03 최신 설명 업데이트: **14쌍·28개 현지화 파일, 국민정신 88개·디시전 28개·범주 8개의 설명 124개/채널 선택 이식 완료**. 원료 순환의 보호 문안과 RT56 만주 지역 안내, 게임 로직·지도·그림을 보존했다. subsystem·회귀 35개 통과, aggregate **20 PASS / 0 WARNING / 1 기존 history ERROR**; 이번 UI·실행 미검증. 작업 전 19 PASS / 2 기존 ERROR와 원장 갱신을 [이식 기록](implementation/2026-10-03-korean-prose-update-port.md)에 구분했다.
- 2026-10-03 원료 순환체계 업데이트: **선택 이식·해당 module 정적 검사 완료, aggregate 20 PASS / 0 WARNING / 1 기존 ERROR. 이번 호환판 실행 검증 미실행**. 영구 I·II 보상 강화와 정치력 150의 별도 90일 긴급 지원, 전용 그림·현지화를 반영했다. 원장 1,417개·관리 output 406개, 의도적 회귀 35개 거부. [구현 기록](implementation/2026-10-03-korean-material-cycle-port.md)에 현재 source/playset, 작업 전 `9 PASS / 12 ERROR`와 별도 checkout 바이트 복구, 잔여 history 오류·whitespace 검사 제한을 기록한다.
- 2026-09-23 후속 한국 업데이트: **콘텐츠·이미지 병합 완료, 460개 중점. 실제 엔진 9개 시나리오 909 PASS / 0 FAIL / 0 SKIP; 신규 134개 중점·63개 국민정신 확인. 정적 20 PASS / 0 WARNING / 1 기존 ERROR**. 18개 사업·12개 주 효과·231개 그림을 선택 이식했다. 강제 효과와 기간 경과 검사의 범위·한계·초기 계측 실패는 [실행 감사](audits/2026-09-23-second-wave-runtime.md)에 구분했다. [구현 기록](implementation/2026-09-23-korean-second-wave-port.md), [지역 대응 ADR-0005](decisions/0005-korean-second-wave-regional-integration.md), [출처·충돌 감사](audits/2026-09-23-second-wave-source-audit.md). 정적 잔여 오류는 작업 전 KOR history 전쟁 지지도와 생성기의 불일치다. 아래 9월 22일 수치는 이전 326개 이식의 역사적 기록이다.
- 1차 정적 포팅 구현: 완료
- 한국 콘텐츠 소유권: HOK 우선으로 확정, 중국·일본 자체 콘텐츠는 RT56 우선
- 9월 22일 한국 중점 업데이트: 한국 runtime20개 파일 반영 완료; 당시 326개 중점과 보상·결정·이벤트·현지화·AI, 기존 지도·만주·대일 강화 보존. [구현 기록](implementation/2026-09-22-korean-focus-update-port.md)
- 9월 22일 aggregate static gate: 당시 최종 임시 파일 제거·README 확정·원장 재생성 뒤 `20 PASS / 0 WARNING / 0 ERROR`, exit 0. 이후 history 불일치가 있는 현재 결과와 구분; 의미 검사 통과·회귀 변형 13개 거부
- 9월 22일 게임/launcher 런타임 검증: **당시 범위를 한정한 부분 검증**. 초기 대조·첫 수선 실패 보존. 기본 fixture 118 PASS·1 FAIL·7 SKIP, NEP alternate 134 PASS·0 FAIL·0 SKIP; 두 실행의 MAN 오류 0건
- 이전 포트 실행 기록: [2026-09-22 C1·R0·C0 및 기본 fixture 증거](audits/2026-09-22-korean-update-runtime.md) — R0 저장·PRC 오류 재현, 기본 fixture의 네 지역 사업 두 회차·중점 보상 부분 검증; 전체 오류 0건이나 정상 저장 완료는 아님
- 9월 22일 구현 기록의 환경 관찰: donor `81d39fa`, RT56 manifest `7475007536894105204`, C1 HOI4 `1.19.3.0.c01a (940d)`·DLC 36개. 9월 21일 donor 단독 로그와 구분; 새 계획의 조사 기준선은 해당 문서에 별도 기록
- 과거 crash 사건: C1·C0는 9월 6일 실패 지점을 넘어 진행했으나 엔진·호스트도 바뀌어 항구 spawn 보정만으로 원인을 확정하지 않음; 사건은 Open
- 별도 MAN 참조 수선: 첫 정의 복원은 C0에서 실패. 후속으로 두 KOR 조건을 보호한 native advisor 검사 생성·정적 검증 완료, 기본 C1 진행에서 반복 오류 미재현; 모집·history·균형 유지
- 임시 파일 없는 한국 시험: 중점 3개 정상 UI 진행·완료와 원화평가절하 국민정신·한국어 표시 확인, 최종 UI 1936.04.28.22. 정확35일 경과·수동 저장은 미검증. 별도 새 프로세스가 로그를 덮어써 후반 오류 집계 불가; 초기 보존본과 UI 보고를 구분
- HOK 한국 음성: WAV 18개와 단일 병합 registry 정적 관리 완료; 새 registry의 실제 청취·duplicate/load 결과는 미검증
- 기존 HOK 세이브 지원: 주장하지 않음, 신규 게임 전용
- 게시/업로드: 기존 호환판 ID `3796816200`; 이번 구현 작업에서는 미실행

## 현재 기준 문서

| 분류 | 문서 | 상태 |
|---|---|---|
| 검토 절차 | [변경 영향·누락 방지와 지침 출처](HOK_CHANGE_COVERAGE_REVIEW.md) | 현지화·주 참조 검토/변경 전 읽음. 호환판 한영 정책·RT56 지도 기준·사용처별 처리·검증 단계 구분 |
| 계획·구현 | [한국 연구·장비 이름 한영 수선](plans/2026-11-10-korean-equipment-localisation-repair-plan.md) / [현재 구현·확인 기록](implementation/2026-11-10-korean-equipment-localisation-repair.md) | 해당 계층 수정·재생성·검증 전 읽음. 최초 문서 전용·v1–v5 실패 이력과 v6 병합+의존성의 실제 정적/UI/복구 결과를 구분 |
| 수선 계획·후속 구현 | [현지화·주 참조 검토 후속](plans/2026-11-09-localisation-state-review-followup-plan.md) / [수선·UI 차단·실제 복구 checkpoint](implementation/2026-11-09-review-followup-repairs.md) | 구현·재생성·검증/재개 전 읽음. 네 출력·정적25/0/11·저장 충돌 이력·BASE raw16/0·미검증 UI/효과·프로필 복구 완료와 OSK 창 잔존 구분 |
| 구현·결정 | [11월8일 콘텐츠 이식](implementation/2026-11-08-hok-upstream-content-port.md) / [ADR-0007](decisions/0007-november-content-integration.md) | 32출력·신규19경로 통합, 선택 범위 실제 실행·복구 및 미검증 한계 기록. 이 계층 수정·재생성·검증 전 읽음 |
| 원본 입력 | [11월8일 선택 입력·host·기존 포트](upstream/hok-content-update-20261108/README.md) | donor36·문서13·compat16+보호1·host2·이전 원장. 재현/출처/그림 재사용 전 읽음 |
| 계획·검토 | [11월8일 원본 추가 콘텐츠 이식](plans/2026-11-08-hok-upstream-content-port-plan.md) | 문서화만. CNDP13·표시·참조36후보의 반영/유지/제외/미확인, 주별 보상·저장 계약·생성 소유권·후속 검증 구분. 추가 내용 구현·검증 전 읽음 |
| 구현 | [한국 15주·연결 콘텐츠 이식](implementation/2026-11-07-korean-state-split-port.md) | 47출력·신규9경로·범위 구현/검증/복구 완료. 정적19 PASS/기존11 ERROR, final suite190 PASS/0 MISMATCH/10 UNVERIFIED. 새 게임 한정·1939 host미지원·출시 제약과 개별 증거 범위 구별 |
| 결정·대응표 | [ADR-0006](decisions/0006-korean-state-split-integration.md) / [포트 대응 JSON](data/HOK_KOREAN_STATE_SPLIT_PORT_MAPPING.json) | 신규 ID·기존 유지 ID·프로빈스·이름 키·배분·영토 예외. 분할 참조/생성기를 변경하기 전에 읽음 |
| 계획 | [한국 주 분할·연결 콘텐츠 전체 이식](plans/2026-11-07-korean-state-split-port-plan.md) | 최초 문서화 시점의 설계·순서·보존/변경 수치·검증 계약. 후속 구현·검증 결과는 별도 구현 기록 |
| 구현 | [2026-10-12 재벌·시민사회 이식](implementation/2026-10-12-korean-civic-update-port.md) | donor d4031aa·runtime31개·생성436개·원장1,446개; scoped static/회귀26개 통과, 실행 미검증 |
| 배치 | [재벌·시민사회 좌표](HOK_KOREAN_CIVIC_LAYOUT_COORDINATES.md) / [472개 JSON](data/HOK_KOREAN_CIVIC_LAYOUT_COORDINATES.json) | 13개 신규·2개 기존 이동·457개 위치 보존, 10개 SHOW/HIDE 상태 정적 기록 |
| 원본 기록 | [d4031aa 모듈·문서·소재](upstream/hok-civic-update-20261012/README.md) | runtime31개·문서/소재23개 immutable source, 기존 source pins 보존 |
| 계획 | [2026-10-11 한반도 미사일 기지 중복 배치](plans/2026-10-11-korean-rocket-site-fix-plan.md) | 최초 문서화 전용 계획·수정 전 지문 보존; 후속 구현 및 정적 완료, UI 대기 |
| 구현 | [2026-10-11 함경·충청 미사일 위치 선택](implementation/2026-10-11-korean-rocket-site-fix.md) | RT56 3행 제외·HoK 1행 복원, 동반 지도17개 보존; 회귀34 PASS·변형12개 거부, aggregate17 PASS/기존5 ERROR, UI 대기 |
| 구현 | [2026-10-10 왕정 선행·물자 배치](implementation/2026-10-10-korean-royal-update-port.md) | donor4d8241e; runtime2파일·scoped회귀57개, 정적16 PASS/기존5 ERROR, 실행 미검증 |
| 배치 | [호환판 왕정 좌표 명세](HOK_KOREAN_ROYAL_LAYOUT_COORDINATES.md) / [460개 JSON](data/HOK_KOREAN_ROYAL_LAYOUT_COORDINATES.json) | H1 네 개 이동·다른456개 보존; SHOW/초기HIDE/왕정완료HIDE 정적 명세, UI 미검증 |
| 원본 기록 | [4d8241e 왕정 명세·메타데이터](upstream/hok-royal-update-20261010/README.md) | immutable 변경 docs7개·독립 royal lock, historical pins 보존 |
| 구현 | [2026-10-10 한국 중점 선행 조건](implementation/2026-10-10-korean-focus-prerequisite-port.md) | donor af6fccf의 6개 중점·회귀51개; 정적17 PASS와 기존source drift4 ERROR, 실행 미검증 |
| 원본 기록 | [af6fccf 선행 조건 명세·메타데이터](upstream/hok-prerequisite-update-20261010/README.md) | immutable 변경 문서 7개·source/출력 해시·historical host provenance 보존 |
| 구현 | [2026-10-05 중점 결정 해금 툴팁](implementation/2026-10-05-focus-decision-tooltip-port.md) | donor062a602의 2줄·지침 선택 이식, 기존 gameplay 보존; 정적20 PASS와 기존history1 ERROR, 실행 미검증 |
| 구현 | [2026-10-03 국민정신·디시전 설명 업데이트](implementation/2026-10-03-korean-prose-update-port.md) | 설명124개/채널·28파일, runtime 나머지1,324개 동일; 정적20 PASS와 기존history1 ERROR, 실행 미검증 |
| 원본 기록 | [2026-10-03 최신 설명 동결본](upstream/hok-prose-update-20261003/README.md) | donor43dbb38 위 미커밋 locale28개·문서2개, immutable base·해시·보존lock 분리 |
| 구현 | [2026-10-03 원료 순환체계 업데이트 이식](implementation/2026-10-03-korean-material-cycle-port.md) | runtime 9개·관리 406개·원장 1,417개, 20 PASS / 1 기존 ERROR; 실행 미검증 |
| 구현 | [2026-09-23 한국 2차 업데이트 이식](implementation/2026-09-23-korean-second-wave-port.md) | 460중점·288개 신규 파일·정적20 PASS와 기존 오류1건; 후속 실행 감사 연결 |
| 감사 | [2026-09-23 선택 원본·호스트 충돌](audits/2026-09-23-second-wave-source-audit.md) | 288경로·신규 ID 충돌0, 원본·호스트 재확인 |
| 원본 기록 | [be5fb40 명세·그림 출처](upstream/hok-second-wave-be5fb40/README.md) | 37개 바이트 보존 사본; 원본 실행 기록과 포트 결과 구분 |
| 계획 | [2026-09-23 한국 2차 업데이트 전체 이식](plans/2026-09-23-korean-second-wave-port-plan.md) | 구현 전 계획 보존; 실제 결과는 위 구현 기록 |
| 대상 목록 | [2026-09-23 한국 업데이트 파일별 이식](plans/2026-09-23-korean-update-file-inventory.md) | 최신 원본과 현재 포트의 파일·자산 차이 및 잠정 분류 |
| 검증 계획 | [2026-09-23 한국 업데이트 검증](plans/2026-09-23-korean-update-validation-plan.md) | 작성 당시 검증 계약; 실제 결과는 아래 실행 감사 |
| 실행 범위 | [2026-09-23 실행 검증 범위](validation/2026-09-23-second-wave-runtime-request.md) | 후속 실제 실행 승인과 임시 설정 전환·원본 복원 범위 |
| 실행 감사 | [2026-09-23 한국 2차 확장 실제 실행](audits/2026-09-23-second-wave-runtime.md) | 9개 시나리오 909 PASS, 고유134중점·63정신; 계측 실패·잔여 오류·한계 별도 |
| 계획 | [2026-09-22 한국 중점 업데이트 이식](plans/2026-09-22-korean-focus-update-port-plan.md) | 조사 당시 계획; 실제 결과는 구현 기록으로 분리 |
| 구현 | [2026-09-22 한국 중점 업데이트 이식](implementation/2026-09-22-korean-focus-update-port.md) | 한국20개 파일·현재 RT56 재병합·재현 도구·검증 상태 |
| 감사 | [2026-09-22 RT56·HOI4 기준선 재검토](audits/2026-09-22-source-rebaseline.md) | 변경된 host/vanilla10개 입력의 근거와 해시 |
| 실행 감사 | [2026-09-22 한국 업데이트 런타임 증거](audits/2026-09-22-korean-update-runtime.md) | 기본 118/1/7·NEP 134/0/0, clean 한국 UI 진행·후반 로그 부재, 최종 정적 20 PASS와 잔여 범위 |
| 설계 | [포팅 아키텍처](PORTING_ARCHITECTURE.md) | 19:20 이전 산출물의 G2 crash 기록과 후속 정적 보정 반영; 재실행 대기 |
| 절차 | [포팅·검증 워크플로](PORTING_WORKFLOW.md) | 단계별 현재 진행 상태 포함 |
| 절차 | [HOK 한국 콘텐츠 우선 디버깅](KOREAN_CONTENT_DEBUGGING.md) | 현재 crash 격리와 보존 검증의 기준 절차 |
| 구현 | [2026-09-06 1차 포팅 구현](implementation/2026-09-06-first-port-batch.md) | 1차 구현 당시 스냅샷; 후속 음성 정책 전 |
| 구현 | [2026-09-22 한국 아이콘 이식](implementation/2026-09-22-korean-icon-port.md) | 중점60·국민정신29 그림·GFX·AGENTS; 정적19 PASS와 기존 history 불일치1건 |
| 구현 | [2026-09-06 한국 우선 자산·KOR 기술 보정](implementation/2026-09-06-korea-first-assets-and-kor-tech.md) | HOK 음성·기본 항공기 복원과 폐기 수송기 기술 정리 |
| 구현 | [2026-09-06 한국 해안 항구 배치 closure 보정](implementation/2026-09-06-map-building-closure-fix.md) | 누락 항구 spawn 7행과 RT56 대비 회귀 gate 추가 |
| 감사 | [통합 ledger](audits/2026-09-06-integration-ledger.md) | ADR-0004를 반영한 현재 ownership·merge 요약 |
| 감사 | [1,446개 파일 분류 CSV](audits/2026-09-06-production-file-classification.csv) | 생성기가 관리하는 현재 행별 분류·Git/미커밋 출처·호스트/출력 해시 원장 |
| 검증 | [정적 검증 기록](validation/2026-09-06-static-validation.md) | 1차 정책 당시 역사적 결과 |
| 검증 | [한국 우선 후속 정적 검증](validation/2026-09-06-korea-first-static-validation.md) | 당시 15 PASS와 미등록 `Minshu_ikki.ogg` pruning 오류 1건의 역사적 기록 |
| 결정 | [ADR-0001: 런타임 의존성과 로드 구성](decisions/0001-runtime-dependencies-and-load-order.md) | RT56 host 채택, 실제 localisation 구성 불일치 잔존 |
| 결정 | [ADR-0002: 지도 ID 마이그레이션](decisions/0002-map-id-migration.md) | 채택·정적 구현 완료 |
| 결정 | [ADR-0003: localisation 계약](decisions/0003-localisation-contract.md) | Pending Runtime |
| 결정 | [ADR-0004: HOK 한국 콘텐츠 우선 보존](decisions/0004-hok-korean-content-priority.md) | Accepted; 과거 음성·KOR DDS 소유권 결정을 대체 |
| 결정 | [ADR-0005: 2차 만주 정책·환제국 거점](decisions/0005-korean-second-wave-regional-integration.md) | 채택; 지리 대응·범위 차이 유지, 대표 거점과 지역 사업 엔진 검사는 실행 감사 참조 |
| 사건 | [2026-09-06 포팅 후 새 게임 접근 위반](incidents/2026-09-06-post-port-new-game-crash.md) | Open; 과거 재현 기록. 현재 C1·C0는 해당 지점을 넘었으나 과거 원인 판정은 남음 |

## 역사적 증거

| 분류 | 문서 | 의미 |
|---|---|---|
| 기준선 | [2026-09-06 프로젝트 기준선](baselines/2026-09-06-project-baseline.md) | 구현 전 source/playset/log 스냅샷 |
| 감사 | [구현 전 exact-path 충돌 73개](audits/2026-09-06-exact-path-collision-inventory.md) | pre-port 교집합 인벤토리 |
| 사건 | [2026-09-06 시작 크래시 조사](incidents/2026-09-06-startup-crash.md) | 14:06 실패 실행의 원인 증거 |

역사적 문서는 당시 관찰을 보존하며 후속 구현 때문에 자동으로 “해결됨”으로 바뀌지 않는다. 21:28/21:30 실행은 14:06의 지도·공용 파일 오류를 넘어섰지만 새 게임 시작에서 접근 위반이 계속됐다. 현재 C1의 진행 성공도 과거 엔진·호스트에서 발생한 원인을 특정 수정 하나로 확정하는 증거는 아니다.

## 문서 상태 규칙

- **현재 기준**: 후속 구현·결정에 맞춰 갱신하는 규범 문서.
- **특정 시점 스냅샷**: 해당 시각의 source, hash, 로그와 Git 상태만 설명한다.
- **ADR**: 결론과 보류 항목을 함께 보존한다. 결론 변경은 후속 ADR로 대체한다.
- **구현 기록**: 실제 변경과 정적 검사, 미실행 검증을 구분한다.
- **사건 기록**: 특정 실행 증거이며 정적 패치만으로 해결 완료로 바꾸지 않는다.

## donor와 외부 자료

`C:\hoi\hearts_of_korea`, RT56 Workshop 폴더와 HOI4 설치 폴더는 읽기 전용 입력이며 이 저장소의 생성기가 수정하지 않는다. 승인된 게임 실행의 구성·새 임시 저장·로그 보존은 [런타임 증거](audits/2026-09-22-korean-update-runtime.md)에 별도로 기록한다. 고정한 RT56 입력 파일의 해시가 바뀌면 검사가 실패하도록 설계했으며, manifest 변경과 관련 해시를 함께 확인해 새 기준선에서 병합을 다시 검토한다.
