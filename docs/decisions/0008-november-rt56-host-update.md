# ADR-0008: 실행 도중 갱신된 RT56 호스트의 별도 재병합

결정일: 2026-11-08, Asia/Seoul. 사용자는 자동 갱신의 원인을 확인한 뒤 “새 RT 56에 맞춰서 대응하자”라고 명시적으로 범위를 확장했다. 기존 임시 프로필·실제 게임 검증 승인도 유지한다. 커밋·푸시·업로드는 포함하지 않는다.

이 작업을 이어갈 때 [AGENTS.md](../../AGENTS.md), [한국 콘텐츠 ADR-0007](0007-november-content-integration.md), [호스트 입력 안내](../upstream/rt56-host-update-20261108/README.md), [새 잠금](../../tools/rt56_host_update_lock.json)을 먼저 읽는다.

## 결정

1. Steam이 RT56 manifest를 `7553774178744855191`에서 `1963361040482473746`으로 갱신한 사실을 독립 기록한다. 설치 원본과 donor는 수정하지 않는다. 이전 대조/한국 실행은755에만 귀속하고196의 대조군부터 새 프로세스로 검증한다.
2. 이전 선택 목록에서 변경184·삭제8·신규25를 감사한다. 같은 상대 경로의 포트 충돌4개는 명시적 `THREE_WAY_MERGE`로 재생성하며, 나머지 호스트 변경은 RT56에서 상속한다. 다른 상대 경로의 논리 ID 충돌·삭제된 ID 소비도 별도 확인한다.
3. 새 북마크 전체에 이전 포트의 한국 카드1개를 보존한다. 새 generic MIO 전체에는 기존의 한국 전용 tank MIO 보호 조건1개만 합친다. 기존 포트의 오래된 비한국 MIO 내용을 최신 호스트 위에 유지하지 않는다.
4. SEA 공용 on_action은 새 호스트 전체에 기존의 한국14주 selector를 보존한다. 서울525를 새로 추가하지 않는다. 일본 history는 기존 HOK의1939.3.14 한국15주 저항 초기화를 보존하고, 그 밖의 새 일본 원문은 유지한다. 저항 payload4개·해군·인물·외국 효과를 임의로 바꾸지 않는다.
5. 새 호스트 계층은 한국 콘텐츠32개 뒤의 별도4출력이다. 기존15주 지도24개·한국32개·L-08은 보호한다. 이전47/32 source pins와 출력 해시를 바꾸지 않고, 고정된 이전 입력과 정확한 새 최종/중간 해시를 통해 기존 생성기가 역사적 결과를 재현하도록 연결한다.
6. 해시 전환은 이전/현재의 등록된 쌍과 manifest 계보만 허용한다. 옛 핀의 모든 mismatch를 무시하거나 임의 현재값으로 갱신하지 않는다. 이전부터 존재한 aggregate 부채와 새 호스트 대응의 정적/실행 검증을 구분한다.

## 검증 경계

4개 AST 보존·고정 출력 재현·기존47/32와 지도24개 보호, 새 논리 ID 대조, 새 RT56 단독/한국 cold run을 각각 확인한다. CNDP90/180일·취소/재착수·한영 UI·저장/재로드 검증은 소스 통과와 별개다. 과거9주 저장의 지도 이전, 모든 기존 저장, 장기 AI·다른 DLC 조합·멀티플레이 지원으로 확대하지 않는다. 실제 결과와 미검증 항목은 [구현 기록](../implementation/2026-11-08-hok-upstream-content-port.md)에 남긴다.

## 2026-11-09 후속 상태

외부 근거 루트는 `C:\hoi\test\hok-rt56-upstream-20261108-01\`다. 새 host196 대응 뒤 aggregate23/0/11(`checks/aggregate-new-host-after-wtt-bridge.*`)에 이어 회복 수선 뒤에도 **23 PASS / 0 WARNING / 11 ERROR**, exit1이다(`checks/aggregate-after-civic-recovery-v2.*`). 같은 기존11개 오류와 옛 source pins를 보존했으며 전체 부채 해소를 주장하지 않는다. 새 R0·C0의 체크섬·오류·중점/인게임 재로드 기록은 위 구현 기록에서 이전755 실행과 구분한다.

후속 `r0-02-reload`의 RT56 단독 GER 저장/인게임 재로드에서도 PRC advisor18개+재로드 rotation1개를 재현했다. 저장 rename2개·종료 rotation2개를 포함한 최종687/651, 로그34개·원래 저장61개+백업61개·누적 새 저장7개 불일치0과 안정된12개 prefix 대조를 기록했다. GER 파일명/near line은 KOR 원문과 다르지만 그 값만 정규화한 동일 경고군이 확인됐다. 따라서 새 HOK만의 유일 원인이라는 설명은 DISPROVEN이고 엔진/RT56/저장 writer 근본 원인은 미확정이다. 근거는 `new-host-session/runtime-log-review/r0-02-reload-final-collected-20261108T171048UTC/{FINAL_REVIEW.md,reload-control-and-integrity.json}`이다.

fixture-01의 첫 갱신 전 watcher 실패는 보존·제외했고, 두 번째 시도의 실제13개 UI 착수와 정치력1050 소비·가용 민공 getter65 감소, 활성 저장13개 queue를 확인했다. fixture-02의 별도 cold active-save reload 후 정상 진행에서12개90일 경로와 강원180일 경로 종료를 관측했다. 일일 첫 비활성 시각은 정확한 만료 순간이 아니며, 합성 seed나 변화한 getter를 정상 진행·개별 점유 반환의 증거로 확대하지 않는다. 자연 종료 뒤 `.98` 복사 완료 보호 probe는 원래 타이머 재만료와 별개다. `new-host-session/analysis/native-completion/`의 literal18/0·고정 native 보상 계약163/0이 선택된 직렬화 필드의 일치를 확인했다. category base lookup+11·extra7·coal5·VP11은 누락 저장 값을0으로 대입한 절대 총량이 아니다. done/guard46/0은15주 state block SHA·11VP 필드·정치력1204.612·표식/빈 queue 불변을 확인했으며13개 전체 native callback 재실행 검사로 확대하지 않는다. 상세 근거 경로와 한계는 구현 기록에 보존한다.

추가 검증은 별도 `runtime-preparation-v2/`의17fixture/18manifest·39버튼/2범주로 준비했다. 원래9 payload·17버튼·production46 payload pin을 보존하고 V2 소스 검사243/0, 메모리 변이8/8 탐지와 독립 읽기 검토를 기록했다. root가 별도 작성한 `new-host-session/driver/session_v2.py`는 PREP 경로만 바꾸며 원래 새 호스트 세션/백업을 유지한다(`v2-driver-provenance.json`). 이후 최소 offsite V3는 기존 검사243/0을 완화하지 않은 소스475/0이었다. 이 준비 당시 미관측이었던 실제5/6은 후속 f04의 별도 결과로 기록한다.

f03는 **정상 종료·로그34개 최종 수집 완료**다. 원래 저장61개+백업61개 및 누적 시험 저장6개와 수집 사본의 불일치0이며,6개 중1개는 원본 동일 바이트 alias다. `(1bb3)`/DLC36/13,569 province를 기록했다.2026-11-09(KST) f03 종료 당시에는 후속 시험 때문에 복구 전이었고 현재 최종 복구는 아래에 따로 기록한다. 완료 시험 저장 cold load의13완료/활성0, 합성 NoC3 조건의 실제 UI 차단과 C3 지급 뒤 활성, PP74 차단과75 활성, 실제 전라북75PP UI 착수의75→0·가용 getter103→98·90일 timer를 확인했다. 해당 f03의 강원150은 활성 화면까지만이며 실제 착수는 후속 f04에서 확인했다. 처음 PP74로 이름 붙인 실제75 화면은74 근거에서 제외한다.97 idea의 가용102→103은 SETUP_NOT_AT_TARGET이며 생산 실패로 판정하지 않는다.

negative/partial의 fixture lifecycle에서 조건 상실 취소·완료 표식0·환급 jump 부재·조건 복구 후75PP 재시도를 각 범위로 관측했다. 부분 통제 상실1149/province13566은 여러 checkpoint에서 유지됐고 fixture의 명시 peace/controller 복구와 재시도를 분리했다. 이 사례들은 일반 mouse 착수나 재시도90일 완료·포화 보상·정상 seed 진행을 증명하지 않는다. 독립 근거는 `new-host-session/runtime-log-review/fixture-03-live-interim-20261108T162108UTC/negative-phase-independent-review.json`과 `new-host-session/runtime-log-review/fixture-03-partial-capture-20261108T163404UTC/partial-independent-review.json`이며 상세 경로·원시 prefix/행 범위는 구현 기록을 따른다. 구형 marker 전환과 강원150PP·가용5 점유 유지 및 슬롯 명목6설정 room1/0/0/0/1/0도 각 독립 review에 기록했다. 합성 구형 표식은 진짜 구형 저장이 아니며 무조건180일 기대 로그·종류별 query20은 정확한 타이머나 shared capacity25를 증명하지 않는다.

수선 전 f03의 영어 회복 `.3/.13`은 제목·설명이 보이지만 자동 sync 목록이 선택지를 화면 아래로 밀어내는 실제 overflow가 확인됐다. 원시 PNG2개와 당시 civic `CB091651…86F7`은 `new-host-session/runtime-log-review/fixture-03-final-collected-20261108T165108UTC/{final-integrity-and-ui-review.json,recovery-ui-raw/,loaded-source/}`에 고정했고 rocket 설명 부재라는 첫 판독은 철회했다. 회복 trigger 합성 seed와 air 미수락·최소화 뒤 rocket 직접 호출은 정상 계약 만료·수락이 아니다. 당시 최종 오류784/649는 초기667+PRC reload108+rotation9이며 선택 이름 관련0과 실제 UI 결함을 구분했다. 이 시점에 미관측이었던 후속 실행·최종 복구는 아래의 f04/f05 결과로 구분하며 당시 기록을 새 통과로 덮어쓰지 않는다.

수선은 회복 immediate sync 두 개의 hidden wrapper만 추가해 civic event를 `E0FC4A82…08B78`로 갱신했다. 나머지 runtime60·기존 host preserved32와 옛 source pins를 유지하고 정확한 승인 revision 한 쌍으로 연결한다. 독립 core917/0·host5216/0·wrapper 의미/전체 바이트 역변환은 소스 증거이며 실제 수선 UI는 후속 실행 대상이다. `runtime-preparation-v4/`는 V3 runtime18·43버튼·3범주·언어별96키를 그대로 쓰는 별도 준비본이다. 과거243/475는 변경·재실행하거나 현재 PASS로 재표기하지 않았고, V4 current778/0·메모리 변이14/14·보존257/0을 별도 기록했다. `new-host-session/driver/session_v4.py`는 PREP 외 정확한 revision-aware binding도 바꾼 사본이며 PREP-only가 아니다. 실제 diff·285입력 pin·pure resolver 양성2/음성9 및 읽기 전용 source 확인은 `v4-driver-provenance.json`·`v4-driver-preparation/`에 있고, 준비 작업은 프로필이나 게임을 조작하지 않았다.

이후 `fixture-04-ko`는 실제 `(57d3)`/DLC36/13,569 province로 **정상 종료·로그34개 수집을 완료**했다. V4+포트+RT56 한국어 번역+RT56으로 `.3/.13`의 한국어 전체 창·본문·acknowledgement 표시를 확인했고 root가 두 실제 버튼을 각각 클릭했다. `session/runs/fixture-04-ko/screenshots/{air-recovery-after.png,rocket-recovery-after.png}`는 f03의 이전 영어 overflow와 분리된 수선 후 한국어 근거다. 같은 실행의 시민사회 현재35·기관 장악망 해체의 기관 장악 -25/조달 비리 -10/시민사회 +5 툴팁은 기존 계약과 일치해 추가 수선하지 않았다. 이 합성 진입 UI를 정상 회복 만료나 영어 수선 검증으로 확대하지 않는다.

no150 fresh BASE seed 뒤 실제 갱신1.1.16의 가용5/C3보유/PP2000에서 **전북**의 `>5` 조건 빨강, 실제+1 요청 한 번과 갱신 뒤1.2.02의 가용6/civ10/PP2000에서 **강원**의 같은 조건 초록을 확인했다. 동일 버튼의 양쪽 경계를 모두 관측한 것은 아니다. 같은 paused1.2.02의 실제 강원 UI 착수는 PP2000→1850·180일 활성 행을 남겼다.1.2.11 snapshot의 가용1/강원 active1/done0은9게임시간 뒤이며 같은 순간의6→1 차분이나 완료 보상이 아니다.13개 한국어 결정 이름/비용 화면과 독립20로그·16prefix·PNG3해시는 `session/runs/fixture-04-ko/observations/independent-calibration/INDEPENDENT_REVIEW.json`에 연결한다. ledger1은 요청량이며 civ8→10의 단독 원인으로 단정하지 않고, 과거97 실패는 별도 보존한다.

선택한 구형15주 CNDP 미착수 alias는 GUI 지도2.5.02/PP43→정상15일3시간 진행2.20.05/PP61→새 `_temp` 저장→같은 프로세스 재로드 지도2.20.05/PP61을 확인했다. `observations/old15-real-carry/BOUNDED_SAVE_REVIEW.json`과 지도 PNG를 연결하며 cold 재시작·구형 활성/완료 CNDP·구9주 지도 이전·임의 기존 저장 지원으로 확대하지 않는다. alias의 이전SUITE 진단 흔적과 invalid decision2개·PAL portrait 저장 참조 경고2개는 보존했고 clean fixture provenance라고 하지 않는다. f04 최종716/674·현재36/fixture 관련0, 원래61+백업61·누적 시험9·로그34 불일치0, pre/post source6,607행 불일치0은 `runtime-log-review/fixture-04-ko-final-collected-20261108T180827UTC/FINAL_INTEGRITY_AND_OLD15.json`에 있다.

f05 PID848의 refs6은 매번 fresh BASE1936.1.1.12 paused에서 root가 진단 UI를 눌러 선택 PRE/POST **35/20/21/20/19/21 PASS, 합136/0**을 기록했다. `session/runs/fixture-05-en/observations/refs-progress-index.json`과 개별 독립 보고서에 연결한다. REF1은 원래 항구 요새화 중점의 강제 완료,11/13/15/21/22는 복사 수락 효과이며 native 외교 수락 선택지 클릭·1일 callback·정상 중점/후속 진행을 증명하지 않는다. Singapore 부정은 조건부 영토 이전만 차단하고 무조건 MAL/KOR 정치 효과는 유지했다. 현재 근거·한계 표는 [구현 기록](../implementation/2026-11-08-hok-upstream-content-port.md#현재-확인-범위와-남은-검증)에 유지하고 기존11개 부채의 수선 범위는 넓히지 않는다.

영어 civic는 합성 setup 뒤 같은 paused1.1.12에서 실제 native `.1.a/.11.b/.2.a/.12.b`를 순서대로 선택하고 고유 저장4개를 보존했다. seed PP2000 뒤 실제 저장1900/1900/1825/1875와 최종 C60/V40/I70/P70·stability0.45, raw60/0·queue16/0·교차27/0은 `observations/en-controlled-series/controlled-series-evidence-index.json`에 연결한다.8개 hover는 실제4선택과 구분하고, 항공 사고 종이 아래 프레임 잘림·초기 tooltip PNG 제외도 보존한다. 예약2개는 직렬화된 queue이며 자연 경과·후속 성공이 아니다.

별도 fresh BASE의 영어 `.3/.13`은 전체 창·ACK가 보이고 root가 실제 수락했다. 사이에 뜻하지 않은 숨김 `.20` → 공개 `.24` 경고와 ACK가 끼어 순수 pair가 아니다. 새 zzencivic 저장의 C60/V35/I55/P20·PP2000, 회복 raw15/0·queue4/0·맥락9/0과 추가 crisis flag1/pressure idea/active90일 mission은 `observations/en-recovery-with-warning-save/qualified-recovery-evidence-index.json`(SHA92BFE04E…63C581A7E)에 연결한다. 예약 queue 부재와 active mission은 별개이며 자연 회복·위기 기간이나 취소/만료를 증명하지 않는다. 선택한 한영 회복 UI에서 수선 전 overflow는 재현되지 않았다.

f05는 정상 종료·34로그/누적 시험14개 수집·원래61개 차이0으로 마쳤다. `observations/final-independent-closed-audit/closed-run-independent-audit.json`은12/0이며 원본/백업61개 본문 대조는 root 최종 감사에 연결한다. 최종 로그는 `observations/final-collected-error-classification.json`의812기록/655고유(초기667+PRC126+rename10+rotation9), 선택 HOK/fixture 관련0이다. PRC의 파일명/줄 번호까지 같은 exact signature와 R0-02에서 확인한 동일 경고군은 구분하며 전체 무오류를 주장하지 않는다.

`session/restoration.json`은19:07:05UTC에 설정/metadata/career·선택·기존 저장 복구와 소유 descriptor 부재를 기록했고 실제 Steam 녹색 플레이는 `session/steam-play-after-final-restoration.png`의 별도 UI 관측이다. `final-restoration-audits/20261108T191122.511968UTC-24704/audit.json`은 **68 PASS / 0 FAIL, exit0**(SHA26F9E447…8FB54368F)이다. profile62+backup62·원본61+backup61·임시 descriptor3개 부재·최종36/map24/L08·승인6,607행·donor36/docs13와 동결 사본·현재 host28,746 및 manifest196/build26409260 불변·게임/launcher 부재를 확인했다. 이는 명시한 파일/프로세스 보존 감사이며 게임 정상이나 모든 저장 호환성의 증거가 아니다. 활성 source-cache3개 전체 직접 재해시는 미수행이며6,607행의 활성 cache 경로0·helper 메모리 cache와 구분한다. 현재 실행·수집·복구·보존 감사의 미완료 항목은 없고, 동작 미검증과 기존11개 정적 부채는 구현 기록의 한계 표에 유지한다.
