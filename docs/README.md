# 문서 인덱스

이 폴더는 Hearts of Korea × The Road to 56 신규 호환 포트의 설계, 결정, 구현, 감사와 검증 기록을 보관한다.

## 현재 상태

- 1차 정적 포팅 구현: 완료
- 한국 콘텐츠 소유권: HOK 우선으로 확정, 중국·일본 자체 콘텐츠는 RT56 우선
- 한국 중점 업데이트: 한국 runtime20개 파일 반영 완료; 326개 중점과 보상·결정·이벤트·현지화·AI, 기존 지도·만주·대일 강화 보존. [구현 기록](implementation/2026-09-22-korean-focus-update-port.md)
- aggregate static gate: 최종 임시 파일 제거·README 확정·원장 재생성 뒤 `20 PASS / 0 WARNING / 0 ERROR`, exit 0. 이전 fixture 전 두 스냅샷과 별도 기록; 의미 검사 통과·회귀 변형 13개 거부
- 게임/launcher 런타임 검증: **범위를 한정한 부분 검증**. 초기 대조·첫 수선 실패 보존. 기본 fixture 118 PASS·1 FAIL·7 SKIP, NEP alternate 134 PASS·0 FAIL·0 SKIP; 두 실행의 MAN 오류 0건
- 최신 포트 실행 기록: [2026-09-22 C1·R0·C0 및 기본 fixture 증거](audits/2026-09-22-korean-update-runtime.md) — R0 저장·PRC 오류 재현, 기본 fixture의 네 지역 사업 두 회차·중점 보상 부분 검증; 전체 오류 0건이나 정상 저장 완료는 아님
- 현재 환경 관찰: donor `81d39fa`, RT56 manifest `7475007536894105204`, C1 HOI4 `1.19.3.0.c01a (940d)`·DLC 36개. 9월 21일 donor 단독 로그와 구분
- 과거 crash 사건: C1·C0는 9월 6일 실패 지점을 넘어 진행했으나 엔진·호스트도 바뀌어 항구 spawn 보정만으로 원인을 확정하지 않음; 사건은 Open
- 별도 MAN 참조 수선: 첫 정의 복원은 C0에서 실패. 후속으로 두 KOR 조건을 보호한 native advisor 검사 생성·정적 검증 완료, 기본 C1 진행에서 반복 오류 미재현; 모집·history·균형 유지
- 임시 파일 없는 한국 시험: 중점 3개 정상 UI 진행·완료와 원화평가절하 국민정신·한국어 표시 확인, 최종 UI 1936.04.28.22. 정확35일 경과·수동 저장은 미검증. 별도 새 프로세스가 로그를 덮어써 후반 오류 집계 불가; 초기 보존본과 UI 보고를 구분
- HOK 한국 음성: WAV 18개와 단일 병합 registry 정적 관리 완료; 새 registry의 실제 청취·duplicate/load 결과는 미검증
- 기존 HOK 세이브 지원: 주장하지 않음, 신규 게임 전용
- 게시/업로드: 기존 호환판 ID `3796816200`; 이번 구현 작업에서는 미실행

## 현재 기준 문서

| 분류 | 문서 | 상태 |
|---|---|---|
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
| 감사 | [1,123개 파일 분류 CSV](audits/2026-09-06-production-file-classification.csv) | 생성기가 관리하는 현재 행별 분류·Git/미커밋 출처·해시 원장 |
| 검증 | [정적 검증 기록](validation/2026-09-06-static-validation.md) | 1차 정책 당시 역사적 결과 |
| 검증 | [한국 우선 후속 정적 검증](validation/2026-09-06-korea-first-static-validation.md) | 당시 15 PASS와 미등록 `Minshu_ikki.ogg` pruning 오류 1건의 역사적 기록 |
| 결정 | [ADR-0001: 런타임 의존성과 로드 구성](decisions/0001-runtime-dependencies-and-load-order.md) | RT56 host 채택, 실제 localisation 구성 불일치 잔존 |
| 결정 | [ADR-0002: 지도 ID 마이그레이션](decisions/0002-map-id-migration.md) | 채택·정적 구현 완료 |
| 결정 | [ADR-0003: localisation 계약](decisions/0003-localisation-contract.md) | Pending Runtime |
| 결정 | [ADR-0004: HOK 한국 콘텐츠 우선 보존](decisions/0004-hok-korean-content-priority.md) | Accepted; 과거 음성·KOR DDS 소유권 결정을 대체 |
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
