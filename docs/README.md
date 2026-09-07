# 문서 인덱스

이 폴더는 Hearts of Korea × The Road to 56 신규 호환 포트의 설계, 결정, 구현, 감사와 검증 기록을 보관한다.

## 현재 상태

- 1차 정적 포팅 구현: 완료
- 한국 콘텐츠 소유권: HOK 우선으로 확정, 중국·일본 자체 콘텐츠는 RT56 우선
- aggregate static gate: 만주 획득 경로 회귀 검사를 포함해 현재 `17 PASS / 0 WARNING / 0 ERROR`
- 게임/launcher 런타임 검증: 21:28 비한국 국가와 21:30 KOR의 `RT56 + compat` C0에서 동일 접근 위반 재현; 항구 배치 보정 뒤 재검증 대기
- 최신 HOI4 로그: 2026-09-06 21:30 실행 — 번역 모드 없이 13,569 province와 history 로드 후 singleplayer launch에서 접근 위반
- 현재 crash 후보: 합성 한국 해안의 `naval_base_spawn` 7행 누락은 확인·정적 수정됨; 동일 과거 stack과 항구 likely-crash 로그 때문에 인과는 `STRONGLY_SUPPORTED`, 런타임 확인 전 사건은 Open
- HOK 한국 음성: WAV 18개와 단일 병합 registry 정적 관리 완료; 새 registry의 실제 청취·duplicate/load 결과는 미검증
- 기존 HOK 세이브 지원: 주장하지 않음, 신규 게임 전용
- 게시/업로드: 기존 호환판 ID `3796816200`; 이번 만주 보정 작업에서는 미실행

## 현재 기준 문서

| 분류 | 문서 | 상태 |
|---|---|---|
| 설계 | [포팅 아키텍처](PORTING_ARCHITECTURE.md) | 19:20 이전 산출물의 G2 crash 기록과 후속 정적 보정 반영; 재실행 대기 |
| 절차 | [포팅·검증 워크플로](PORTING_WORKFLOW.md) | 단계별 현재 진행 상태 포함 |
| 절차 | [HOK 한국 콘텐츠 우선 디버깅](KOREAN_CONTENT_DEBUGGING.md) | 현재 crash 격리와 보존 검증의 기준 절차 |
| 구현 | [2026-09-06 1차 포팅 구현](implementation/2026-09-06-first-port-batch.md) | 1차 구현 당시 스냅샷; 후속 음성 정책 전 |
| 구현 | [2026-09-06 한국 우선 자산·KOR 기술 보정](implementation/2026-09-06-korea-first-assets-and-kor-tech.md) | HOK 음성·기본 항공기 복원과 폐기 수송기 기술 정리 |
| 구현 | [2026-09-06 한국 해안 항구 배치 closure 보정](implementation/2026-09-06-map-building-closure-fix.md) | 누락 항구 spawn 7행과 RT56 대비 회귀 gate 추가 |
| 감사 | [통합 ledger](audits/2026-09-06-integration-ledger.md) | ADR-0004를 반영한 현재 ownership·merge 요약 |
| 감사 | [1,014개 파일 분류 CSV](audits/2026-09-06-production-file-classification.csv) | 생성기가 관리하는 현재 행별 분류·해시 원장 |
| 검증 | [정적 검증 기록](validation/2026-09-06-static-validation.md) | 1차 정책 당시 역사적 결과 |
| 검증 | [한국 우선 후속 정적 검증](validation/2026-09-06-korea-first-static-validation.md) | 당시 15 PASS와 미등록 `Minshu_ikki.ogg` pruning 오류 1건의 역사적 기록 |
| 결정 | [ADR-0001: 런타임 의존성과 로드 구성](decisions/0001-runtime-dependencies-and-load-order.md) | RT56 host 채택, 실제 localisation 구성 불일치 잔존 |
| 결정 | [ADR-0002: 지도 ID 마이그레이션](decisions/0002-map-id-migration.md) | 채택·정적 구현 완료 |
| 결정 | [ADR-0003: localisation 계약](decisions/0003-localisation-contract.md) | Pending Runtime |
| 결정 | [ADR-0004: HOK 한국 콘텐츠 우선 보존](decisions/0004-hok-korean-content-priority.md) | Accepted; 과거 음성·KOR DDS 소유권 결정을 대체 |
| 사건 | [2026-09-06 포팅 후 새 게임 접근 위반](incidents/2026-09-06-post-port-new-game-crash.md) | Open; 21:28 GER·21:30 KOR 재현, 항구 배치 보정 후 cold test 대기 |

## 역사적 증거

| 분류 | 문서 | 의미 |
|---|---|---|
| 기준선 | [2026-09-06 프로젝트 기준선](baselines/2026-09-06-project-baseline.md) | 구현 전 source/playset/log 스냅샷 |
| 감사 | [구현 전 exact-path 충돌 73개](audits/2026-09-06-exact-path-collision-inventory.md) | pre-port 교집합 인벤토리 |
| 사건 | [2026-09-06 시작 크래시 조사](incidents/2026-09-06-startup-crash.md) | 14:06 실패 실행의 원인 증거 |

역사적 문서는 당시 관찰을 보존하며 후속 구현 때문에 자동으로 “해결됨”으로 바뀌지 않는다. 21:28/21:30 실행은 14:06의 지도·공용 파일 오류를 넘어섰지만 새 게임 시작에서 접근 위반이 계속됐다. 후속 항구 배치 수정도 cold test 전에는 사건을 해결됨으로 바꾸지 않는다.

## 문서 상태 규칙

- **현재 기준**: 후속 구현·결정에 맞춰 갱신하는 규범 문서.
- **특정 시점 스냅샷**: 해당 시각의 source, hash, 로그와 Git 상태만 설명한다.
- **ADR**: 결론과 보류 항목을 함께 보존한다. 결론 변경은 후속 ADR로 대체한다.
- **구현 기록**: 실제 변경과 정적 검사, 미실행 검증을 구분한다.
- **사건 기록**: 특정 실행 증거이며 정적 패치만으로 해결 완료로 바꾸지 않는다.

## donor와 외부 자료

`C:\hoi\hearts_of_korea`, RT56 Workshop 폴더, HOI4 설치 폴더, 사용자 데이터/launcher/log 폴더는 읽기 전용 입력이다. 이 저장소의 문서나 생성기가 그 외부 파일을 수정하지 않는다. RT56이 Steam을 통해 바뀌면 pinned hash 검사가 실패하도록 설계했으며, 그 경우 새 기준선에서 병합을 다시 검토한다.
