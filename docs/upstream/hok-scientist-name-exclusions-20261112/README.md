# 2026-11-12 한국 생성 이름의 추가 제외 입력

이 이름 계층을 수정·재생성·검증하기 전에 [호환판 구현 기록](../../implementation/2026-11-12-korean-scientist-update-port.md), [소스 manifest](source-manifest.json), [초기 선택 입력 안내](../hok-scientist-update-20261112/README.md)와 [소유 잠금](../../../tools/hok_scientist_update_lock.json)을 읽는다. 표시·공유 소비자의 범위 판단은 [변경 영향 절차](../../HOK_CHANGE_COVERAGE_REVIEW.md)와 [현지화 검토 스킬](../../skills/hok-rt56-localisation-review/SKILL.md)을 따른다.

초기 과학자 이식은 로마자 남성71·여성16·성14개 중 `Geunhye`만 제외한 donor 상태를 동결했다. 구현 도중 원본의 이름 파일과 유지 문서2개가 추가 갱신됐고, 새 donor 기록은 사용자가 지적한 현대 정치인 실명 중복을 피하도록 이름 토큰20개를 더 제외한다. 같은 이름 업데이트의 최신 선택 입력으로 새 사본을 보존한다. 최종 pool은 **남성56·여성11·성14개, 총81개**다.

| 위치 | 원본·사본·활성 입력의 역할 |
|---|---|
| `C:/hoi/hearts_of_korea/` | 원본 donor. HEAD `cdc022eee15fbf7404d4cb30cf2d0102d29e550c` 위 미커밋 이름·문서 갱신 상태를 읽는다. |
| `source/common/names/00_names.txt` | 최신 이름 원본의 정확한 사본. SHA `32AA863816EE3EACC02AA448E9CCBF0A4FCDB1AF92809CE23BDF2CC5DD096B9F`,481,844바이트다. KOR 선택 delta와 다른 블록의 보존 근거로 사용한다. |
| `documents/docs/data/HOK_KOREAN_RANDOM_NAME_LOCALISATION_MANIFEST.json` | donor 최종56/11/14개와 추가 제외20개·순서·표시 범위·이전 작업 이력을 기록한 정확한 사본이다. |
| `documents/docs/incidents/2026-11-12-korean-random-name-localisation.md` | donor의 사용자 요청·확인한 실명 중복 자료·후속 제외·실행 미검증을 기록한 정확한 사본이다. |
| [source-manifest.json](source-manifest.json) | 선택3입력의 원본/사본 경로·SHA·크기·dirty 상태와 초기 capsule/중간 출력의 지문을 고정한다. 복사 전후 원본과 사본 SHA가 일치했다. |
| `../hok-scientist-update-20261112/` | 초기 초상화·`Geunhye`1개 제외 시점의 immutable capsule이다. manifest SHA `47E296C2ED93A084A9F076C23467F0B9A0FBA7B82C62E2178A5532B0A1896D8C`와 source/docs를 그대로 유지한다. 호스트/schema·그림 출처도 이 초기 기록을 따른다. |
| `C:/hoi/test/hok-rt56-scientist-update-20261112-01/` | 이번 호환판의 기존 외부 작업 경로. 처음 baseline 이후 생긴 donor3입력 차이는 동시 원본 갱신으로 별도 기록한다. |
| `C:/hoi/test/hok-scientist-modern-name-exclusions-20261112-01/` | donor가 남긴 별도 추가 제외 전 사본·정적 확인 기록의 원래 위치다. 이번 호환판 검증 결과와 구분한다. |

추가 남성 제외15개는 `Gun`, `Woong`, `Yoon-Gi`, `Yoongi`, `Jaeyoung`, `Jinho`, `Jiwon`, `Jungho`, `Junghoon`, `Minseok`, `Minsoo`, `Sanghoon`, `Sungho`, `Sunghoon`, `Sungmin`이다. 추가 여성 제외5개는 `Bora`, `Ji-young`, `Kyung-hee`, `Jiyoung`, `Kyunghee`다. 앞서 제외한 `Geunhye`도 유지한다. 이름과 성을 독립 선택하는 기존 구조에서 이름 토큰을 제거하므로 해당 이름은 남은 모든 성과의 조합에서 빠진다. 공유 KOR pool을 쓰는 과학자 외 신규 인물에도 적용된다.

기존14개 성, 남은 이름의 철자·순서·인용 형태와 다른 국가 블록을 유지한다. 특정 정치인으로 추정해 후보를 더 삭제하거나 모든 현대 정치인과의 우연한 중복을 제거했다고 주장하지 않는다. 실명 중복 선정 근거는 정확히 보관한 donor 문서의 확인 범위를 따른다.

manifest의 `selected_output`에 있는4,733바이트·SHA `F06C9DE9A35C43A86BA7B76AD447A7E511060A035B2F396C659F8459A320F781`은 초기 `Geunhye`1개 제외 v1의 중간 출력이다. 최신81항목의 최종 생성 출력은 소유 잠금과 구현 기록에서 별도로 고정한다. 초기 source manifest와 v1 결과를 새 이름 상태의 증거로 바꾸지 않는다.

donor는 추가 제외 후 게임을 실행하지 않았고 이번 사본 보존도 실제 RT56 모집·UI·저장 검증을 수행하지 않았다. source 차이와 정적 결과·실제 실행은 구현 기록에서 각각 확인한다. 신규 그림8개와 고정 과학자4명의 변경 범위는 초기 초상화 선택 계약을 따른다.
