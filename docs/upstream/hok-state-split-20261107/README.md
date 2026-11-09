# 한국 주 분할 선택 입력 보관본

이 디렉터리는 2026-11-07 한국 15주 분할의 **유지 관리용 출처·재현 입력**이다. 시험 로그·보고서·fixture·프리뷰를 보관하는 디렉터리가 아니다. 입력을 사용하거나 위치·출처·잠금을 바꾸기 전에 [프로젝트 지침](../../../AGENTS.md), [ADR-0006](../../decisions/0006-korean-state-split-integration.md), [구현 기록](../../implementation/2026-11-07-korean-state-split-port.md)을 읽는다. 과거 외부 캐시 위치를 해석할 때는 [개발 자료 안내](../../HOK_DEVELOPMENT_ARTIFACT_ARCHIVE.md)를 먼저 읽는다.

## 원본·사본·실행 출력의 역할

| 경로 | 역할 |
|---|---|
| `C:\hoi\hearts_of_korea` | 읽기 전용 donor 원본. branch `feat/korean-focus-expansion-ai`, HEAD `0d73d49726abbfa435c73f1bf8cc24d4a5af014b` 위의 미커밋 분할을 선택. 이 HEAD만 checkout해 새 입력을 얻을 수 없음 |
| [before/](before/) | 존재하는 34개 변경 파일의 donor HEAD 바이트. 원본 전후 차이의 기준 사본이며 포트의 이전 출력은 아님 |
| [runtime/](runtime/) | donor 작업 트리에서 선택한 런타임 입력 42개. 이름과 달리 이 폴더 자체가 엔진의 활성 모드 경로는 아님 |
| [compat_before/](compat_before/) | 호환판 `3d9355b70152794ed974dcf183323c24206d900a`의 필요한 이전 입력 48개. 초기 46개와 후속 연구망 한영 파일 2개. 기존 출력·지도와 역변환 비교용 사본 |
| [documents/](documents/) | 원본 분할 계획·확정 배분표·원본 구현/검증 기록 3개. 원본 실행 결과와 포트 실행 결과를 구별 |
| [분할 잠금](../../../tools/hok_state_split_lock.json) | source 전후 바이트·크기·출처, compat 입력, 현재 물리 host/schema 지문, 최종 47출력의 이전/중간/최종 해시 원장 |
| [포트 대응표](../../data/HOK_KOREAN_STATE_SPLIT_PORT_MAPPING.json) | donor와 포트의 ID·표시 키·province·수혜 주·분배를 연결하는 유지 관리용 문서. 시험 결과 파일이 아님 |
| 호환판 root의 `common/`, `events/`, `history/`, `localisation/`, `map/` | 생성기가 최종 바이트를 출력하는 실제 작업 소스. 이 보관본 경로로 launcher를 돌리지 않음 |
| `C:\hoi\test\hok-rt56-state-split-20261107-01\` | 이번 외부 helper·검사·백업·프리뷰·승인된 실행 준비/증거. 이 디렉터리를 source cache나 배포 파일로 사용하지 않음 |

기존 활성 캐시 `C:\hoi\test\hok-rt56-source-cache\sources\`의 세 트리는 그대로 유지한다. 이번 보관본을 그 위에 덮지 않고 원본/host에도 쓰지 않는다. 기존 `.local-artifacts`의 역사적 위치 변경을 이번 새 입력 동결 작업과 혼동하지 않는다.

## 파일 수와 재현 범위

donor 수정 38개·미추적 11개에서 지침·문서 변경을 제외한 런타임 42개만 선택했다. 기존 런타임 수정 34개와 신규 주 6개·현지화 2개다. 초기 포트 45출력은 추가 소비자 `events/WTT_PRC.txt`, `events/r56_japan.txt`와 쓰시마 이름 참조 수선을 포함한다. 후속 연구망 기존 한영 파일 2개의 주 이름 참조 보완을 더한 현재 범위는 **47출력**이다. 이 다섯 추가 변경은 donor 런타임 입력 42개에 포함되지 않는다.

새 포트 경로는 주 6개, 이름 파일 2개, 현재 RT56 기반 일본 중점 1개로 9개다. 나머지 38개는 기존 경로 변경이며 연구망 두 파일도 여기에 포함된다. 파일 수는 원본·출력·원장 행마다 기준이 다르다. 이 보관본 전체를 게임 root에 복사하지 않는다. donor 일본/중국 전체 파일은 설계 delta의 입력이며 RT56 소유 내용을 대체하는 완성 출력이 아니다.

| 동결 문서 | SHA-256 |
|---|---|
| [원본 계획](documents/docs/HOK_KOREAN_STATE_SPLIT_PLAN.md) | `3E83E5C5711EABB5260142F5A4AD01A0966A5F46DF426328380EDE9CC9F83768` |
| [원본 확정 대응표](documents/docs/data/HOK_KOREAN_STATE_SPLIT_MAPPING.json) | `53F3B824AB4349F74C5635F49FCD3E3FB1847FDC624E90FC367A7A26CB8EB373` |
| [원본 구현·검증 기록](documents/docs/incidents/2026-11-07-korean-state-split-implementation.md) | `8287D24A7B3FF0EA6195F9EDE6D5A8838ACCA2614D37D1243FA54973F98DDB02` |

런타임 42개의 개별 SHA-256·바이트 수는 잠금의 `sources`에 있다. `before_sha256`은 donor HEAD, `after_sha256`은 선택한 미커밋 donor 바이트다. `compat_before_sha256`은 같은 상대 경로의 이전 포트가 있을 때만 기록되며 donor 원본 해시와 같다는 뜻이 아니다. 출력 경로가 달라지는 새 주는 `outputs`의 실제 포트 경로와 대응표를 따른다.

`current_inputs`는 설치 RT56/vanilla의 물리 입력 1,193개를 고정한다. 공유 출력의 `host_provider`/`host_base_sha256`는 물리 출처와 해시이고 `host_intermediate_sha256`는 기존 HOK 연결을 합성한 메모리 바이트다. 최종 `sha256` 및 이전 포트 `previous_sha256`와 각각 구별한다. 예를 들어 현재 RT56 일본 중점 물리 파일과 최종 HOK 지역 병합 파일은 별도 해시를 갖는다. 중간 출력 해시를 설치 파일 해시로 대조하지 않는다.

## 실제 확인과 사용 경계

[분할 생성기](../../../tools/korean_state_split.py)는 동결 입력·현재 호스트·ID 충돌을 확인하고 최종 출력을 재현한다. [한국 콘텐츠 변환](../../../tools/korean_state_split_content.py)은 이전 포트 위에 선택 hunk와 번역만 적용하고, [공유 변환](../../../tools/korean_state_split_shared.py)은 현재 host 기반의 한국 연결만 합성한다. 새 주 줄바꿈은 기존 부모의 형식을 따르고 HOK 표시 키 접미사는 변환하지 않는다. 생성 결과물을 손으로 고치거나 역사적 핀을 최신 바이트로 바꿔 통과시키지 않는다.

초기 45출력의 확인은 입력/출력 동결, 독립 소스 검사 초기 7,170/0·필드 확장 후 7,180/0, 공유 의미 검사 42/0, 콘텐츠 16개 재생·역변환, 474개 중점 중 23개 지역 변경과 보호 필드 보존, 기존 기능/영어 검사다. 후속 47출력의 전체 정적 검사는 `static-final-47.txt`에서 19 PASS / 0 WARNING / 11 기존 ERROR이며 English import와 분할 provenance gate가 통과했다. 서로 겹치는 검사 수를 합산하지 않는다.

초기 검사 뒤 건물의 소수 표기와 신규 앵커 분류의 검사 공백을 찾아 수선했으므로 7,170/0을 모든 필드 보존 증거로 쓰지 않는다. 실제 신규 172행 중 170개를 선택하고 기존 한국 배치 546개의 비ID 필드를 보존한다. 경남의 원본 공군기지·로켓 표시 두 행만 별도 복원하며 209개 재부모화 행을 일괄 복원하지 않는다. 세부 필드/변형 거부의 후속 확인은 구현 기록에서 별도로 구별한다.

적용 전 전체 검사 17/0/11의 역사적 host/descriptor 부채는 별도다. 최종 포트 suite의 190 PASS / 0 MISMATCH / 10 UNVERIFIED와 실제 UI·저장·복구 및 DLC·멀티플레이 등의 한계는 [구현 기록의 실행 절](../../implementation/2026-11-07-korean-state-split-port.md#실제-실행-결과)에서 확인한다. source 보관본이나 원본의 결과 자체가 포트의 실행 통과를 입증하지 않는다.

현재 물리 RT56 `common/bookmarks/blitzkrieg.txt`는 1939 시나리오를 지원하지 않는다고 명시한다. 원본 및 포트의 1939 날짜 이력 소스 보존을 지원되는 host bookmark나 실제1939 진행의 증거로 사용하지 않는다. 실제 UI의 가용성·숨김/차단은 별도 관측으로 기록하며 날짜를 강제하지 않는다.

동결 문서의 원래 상대 링크는 donor의 문서 문맥을 보존한다. 모든 참조 문서를 이 폴더에 복제한 것은 아니므로, 보관본에 없는 참조는 읽기 전용 donor의 해당 문서 또는 위에 명시한 포트 기록을 확인한다. 원본 문서의 과거 미결·실행 결과를 포트의 현재 결과로 대체하지 않는다.

이 보관은 source attribution과 재현을 위한 사본이며 새 자산 생성·테스트 실행·캐시 수정·배포·업로드를 자동 승인하지 않는다. HOK 저작·설계와 RT56/vanilla의 기존 기여 및 크레딧은 그대로 유지한다. 이 작업에서 커밋·푸시·Workshop 게시를 수행하지 않았다.
