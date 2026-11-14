# 2026-11-14 한국 지휘관 해금 이관 선택 입력

한국 지휘관 해금 조건·다음 전쟁 중점 안내·새 게임 표식을 수정하거나 재생성·검증하기 전에 [로컬 통합 기록](../../implementation/2026-11-14-korean-commander-unlock-port.md), [변경 영향 절차](../../HOK_CHANGE_COVERAGE_REVIEW.md), [현지화 검토 스킬](../../skills/hok-rt56-localisation-review/SKILL.md), [소스 manifest](source-manifest.json)와 [소유 잠금](../../../tools/hok_commander_unlock_lock.json)을 읽는다. 이 capsule은 생성기의 유지 입력이며 테스트 산출물 보관소가 아니다.

| 위치 | 원본·사본·활성 입력의 역할 |
|---|---|
| `C:/hoi/hearts_of_korea/` | 읽기 전용 HOK donor. 깨끗한 HEAD `0c19f58fa7a9ff898196dcdbe46edfd0ad5fdbbc`의 선택 runtime 5파일과 문서 3개를 보존한다. |
| `before/<원본 상대 경로>` | donor 선조 `065b5550448d6415901456503ef28b27f4530cc1`의 변경 전 Git blob 5개. 원래 Git 바이트·blob ID·SHA·크기를 유지한다. |
| `runtime/<원본 상대 경로>` | 선택 donor checkout 5개의 정확한 바이트 사본. 줄 끝을 LF로 정규화한 내용이 해당 커밋 Git blob과 일치함을 복사 시 확인했다. 원본 사본 자체는 정규화하지 않았다. |
| `compat_before/<원본 상대 경로>` | 호환판 `b5308a027385cc021243a443ff49b728707e081e`의 활성 출력 5개. 한국 인물·중점·역사와 한영 시작 설정 문구의 정확한 선조 입력이다. |
| `documents/<원본 상대 경로>` | donor 지휘관 이관 계획·두 번째 개발 계획·2026-11-14 사건 기록 3개의 정확한 사본. donor 실행 결과를 현재 RT56 이식의 실행 증거로 사용하지 않는다. |
| [source-manifest.json](source-manifest.json) | 위 18개 입력의 역할·원본/사본 경로·커밋·SHA·크기·BOM·실제 줄 끝과 설치 참조 9개를 기록한다. 설치 참조는 RT56 descriptor·한국 인물/중점 3개와 바닐라 버전·트리거/효과 문서·BEL/SPR 인물·벨기에 중점 6개이며 읽기 전용이다. |
| `C:/hoi/test/20261114-commander-unlock-port/` | 이번 호환판 baseline·백업·fixture·검사 보고서의 외부 위치. 기존 `C:/hoi/test/hok-rt56-source-cache/sources/`의 역사 입력과 역할을 구분한다. |

선택 동작은 홍범도·김좌진·안중근의 군사 역할을 `KOR_prepare_for_the_next_war` 완료로 해금하고, 새 국가 표식 `HOK_KOR_commander_focus_unlock_v1`이 없는 기존 일반 국뽕 저장의 사용을 유지하는 것이다. 새 게임 표식은 한국 국가 역사에서만 설정하며 기존 시작 모집과 다른 역할·능력·특성·그림은 유지한다. 중점 보상에는 세 인물의 native 해금 안내를 추가하고 일반 국뽕 설명에서 시작 지휘관 보장만 제거한다. 호환판 영어 본문은 기존 번역을 유지하면서 해당 한 문장만 제거한다. donor 영어 채널의 한국어 본문은 source로만 보존한다.

[소유 모듈](../../../tools/upstream_commanders.py)은 동결 donor 전후의 전체 차이가 선택 hunk와 일치함을 검증하고 호환판 선조에 같은 변경을 적용한다. 최종 5출력의 지문과 일치할 때만 역사 검사에 직전 출력을 제공한다. 기존 source pins·지도 이관·언어 계약·RT56 공유 시스템을 갱신하지 않는다. 원장은 기존 1,577행을 유지하면서 해당 5행의 출력 지문과 provenance 이유만 갱신하며 한국 인물 행의 RT56 연결/MAN 출력 지문은 보존한다.

현재 설치 metadata는 `Operation Postern v1.19.5.0.7c6c (c184)`, RT56 Workshop 820260968의 manifest는 `1963361040482473746`이다. 이 계층은 해당 현재 참조를 별도로 확인하며 과거 계층의 1.19.4.2 핀을 완화하지 않는다. 이번 작업의 실제 정적 확인과 기존 실패, 미실행 RT56 UI·정상 진행·저장 검증은 로컬 통합 기록을 따른다. donor의 기존 저장 시험은 RT56의 전체 저장 호환성이나 앞선 지도 이관의 새 게임 전용 경계를 바꾸지 않는다.
