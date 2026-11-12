# 2026-11-12 한국 신규 과학자·이름 선택 입력

2026-11-12 후속 기록. 이 capsule은 초기 `Geunhye`1개 제외 시점의 남성71·여성16·성14개 입력과 초상화를 보존한다. 작업 중 추가 갱신된 이름은 [별도 후속 capsule](../hok-scientist-name-exclusions-20261112/README.md)에 동결했으며 현재 최종 이름은 남성56·여성11·성14개다. 현재 구현·검증 상태는 [로컬 통합 기록](../../implementation/2026-11-12-korean-scientist-update-port.md)을 따른다. 아래 source/docs와 초기 manifest의 정확한 바이트·지문은 유지하며 아래 수치는 초기 선택 단계의 기록으로 읽는다.

한국 신규 과학자 초상화와 무작위 이름 후보 제외를 수정·재생성·검증하기 전에 [호환판 구현·검증 기록](../../implementation/2026-11-12-korean-scientist-update-port.md), [소스 manifest](source-manifest.json), [변경 영향 절차](../../HOK_CHANGE_COVERAGE_REVIEW.md)를 읽는다. 그림 원본이나 과거 외부 경로를 조회할 때는 [개발 자료 안내](../../HOK_DEVELOPMENT_ARTIFACT_ARCHIVE.md)를 함께 따른다. 이 폴더는 동결한 선택 입력과 출처 기록을 유지한다.

| 위치 | 원본·사본·활성 입력의 역할 |
|---|---|
| `C:/hoi/hearts_of_korea/` | 읽기 전용 donor 원본. `feat/korean-focus-expansion-ai@cdc022eee15fbf7404d4cb30cf2d0102d29e550c` 위 미커밋 이름·초상화 변경과 새 GFX·DDS8개를 선택했다. 원본 위치와 내용을 보존한다. |
| `source/<원본 상대 경로>` | 선택 당시 donor runtime11개 파일의 정확한 바이트. 이름 파일·한국 초상화 목록·전용 GFX·DDS8개를 보존한다. 이름 전체 파일은 선택 delta의 근거로 사용한다. |
| `documents/<원본 상대 경로>` | donor AGENTS·과학자 계획·자산/이름 manifest·사건 기록2개, 총6개 문서의 정확한 사본. donor의 실행·저장·애니 서브모드 관측은 해당 소스와 구성의 이력이다. |
| `compat_before/<호환판 상대 경로>` | [소유 잠금](../../../tools/hok_scientist_update_lock.json)이 관리하는 호환판 이전 출력. 기존 한국 이름과 육군·해군 목록을 보존하며 선택 delta만 적용하는 선조 입력이다. |
| [source-manifest.json](source-manifest.json) | 원본/사본 경로·역할·SHA-256·크기, donor dirty 상태, 호환판 기준과 설치된 RT56/바닐라 참조 지문을 기록한다. source와 documents 사본을 복사 직후 원본 해시와 대조했다. |
| [소유 생성기](../../../tools/upstream_scientists.py)·[선택 잠금](../../../tools/hok_scientist_update_lock.json) | 동결 source와 이전 출력을 검사해11출력을 재현한다. 실제 말단 바이트와 일치할 때만 기존 검사를 위해 직전 출력으로 역투영하며 선택 입력·출력·원장 분류를 고정한다. |
| `C:/hoi/test/hok-scientist-portraits-20261112-01/art/` | donor에서 보존한 선택 생성 PNG·프롬프트·변환 기록의 기존 외부 위치. [원본 자산 manifest](documents/docs/data/HOK_KOREAN_SCIENTIST_PORTRAIT_ASSET_MANIFEST.json)가 개별 원본·변환·DDS를 대응한다. |
| `C:/hoi/test/hok-rt56-scientist-update-20261112-01/` | 이번 호환판 작업의 새 baseline·백업·진단·검증 결과 위치. donor 원본 보관 경로와 구분한다. |
| `C:/hoi/test/hok-rt56-source-cache/sources/` | 기존 생성기의 별도 고정 입력 캐시. 이번 source capsule은 새 선택 계층이며 역사적 캐시와 source pins를 보존한다. |

초기 캡처 당시 선택한 이름은 **로마자 남성71·여성16·성14개, 총101개**다. donor는 한글 직접 표기를 시험한 뒤 사용자 요청으로 원래 로마자 표기로 복원하고 `Geunhye` 한 항목만 제외했다. 문서 중간의 한글102항목·여성17개와 성공 화면은 그 이전 소스의 이력이다. `HOK_KOR_RANDOM_NAME_` 부분 키 방식은 실제 모집에서 원시 키가 표시됐으므로 채택 입력에서 제외한다. 고정 과학자4명의 기존 ID와 현지화는 기존 소비 경로를 따른다.

초상화는 기존 donor가 AI 생성한 가상 한국 과학자 남성4장·여성4장을 바이트 그대로 재사용한다. donor 기록의 규격은156×210·uncompressed BGRA32·mipmap1·각131,168바이트다. 생성 프롬프트·선택 원본·crop/변환·도구의 모델명 미노출을 자산 manifest에 보존한다. 이번 이식의 기여는 기존 그림의 선택 복사와 호환판 registry·생성 계층 통합이다.

호환판 대상은 기존 한국 이름 출력·한국 초상화 목록2개와 신규 GFX1개·DDS8개, 총11출력이다. 이름은 공용 전체 파일을 적재하지 않고 기존 `zz_hok_rt56_names.txt`의 KOR 여성 후보 한 항목에만 선택 delta를 적용한다. 초상화는 기존 KOR 정의 안에 scientist 남녀 목록을 추가하고 HOK 전용 sprite8개를 연결한다. 기존 고정 과학자·육군/해군·RT56 공용/타국 풀의 보존을 실제 생성 검사에서 확인한다.

원본의 HOK+애니 정상 모집 표본과 일부 임시 저장 재로드 관측은 호환판의 실제 RT56 실행 결과로 사용하지 않는다. 원본에서도 최초 즉시 저장의 남성 미표시와 저장 rename 오류가 미해결이며 최종 이름 제외 후 실행은 미실시다. 현재 호환판의 적용 상태·정적 결과·UI/저장 한계는 구현 기록을 따른다. 이 capsule의 보존과 해시 대조는 runtime 검증과 별개다.

보관 donor AGENTS는 출처 증거로 유지한다. 활성 지침은 호환판 [AGENTS.md](../../../AGENTS.md)의 조건부 읽기와 로컬 구현 기록이다. 공개 배포 자료와 크레딧의 선택은 별도 release allowlist에서 결정한다.
