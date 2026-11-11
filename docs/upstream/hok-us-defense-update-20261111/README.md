# 2026-11-11 한미 방위비 모듈 선택 입력

이 폴더는 출처·결정적 생성 입력의 유지 capsule이다. 해당 입력을 재사용·수정·재생성·검증하기 전 [구현 기록](../../implementation/2026-11-11-korean-us-defense-port.md), [잠금](../../../tools/hok_us_defense_update_lock.json), [source-manifest](source-manifest.json)를 읽는다. 표시/지역 판단은 [변경 영향 절차](../../HOK_CHANGE_COVERAGE_REVIEW.md), 그림 입력 조회는 [개발 자료 안내](../../HOK_DEVELOPMENT_ARTIFACT_ARCHIVE.md)를 먼저 따른다. 현재 적용·QA는 진행 중이며 아래 입력 보존은 실행 성공을 뜻하지 않는다.

| 원본·사본·활성 입력 | 역할·매핑 |
|---|---|
| `C:\hoi\hearts_of_korea` | 읽기 전용 원본. HEAD `e2009b635d79c80a67fed0370d5fe36a823b656f` 위 미커밋 한미 모듈18runtime·문서4·선택 PNG6개를 동결. 원본 위치/내용을 옮기지 않음 |
| `runtime/<원본 상대 경로>` | 선택 당시 원본18파일의 정확한 바이트. 기존 focus/event2개의 donor delta와 신규16개 입력. donor 영어 채널의 한국어 본문은 증거로 보존하며 최종 영어 출력으로 사용하지 않음 |
| `donor_head/<상대 경로>` | `korea.txt` 중점·사건2개의 HEAD Git blob. 미커밋 runtime과 대비할 선조이며 checkout 개행 사본과 구별 |
| `compat_before/<상대 경로>` | 호환판 `39e8e7e5bc3dbdcf52d8c8acc04a92c97cd0b2f5`의 기존2출력. RT56·ID 이관·이전 수선·핵분열 보너스를 보존할 병합/역투영 입력 |
| `translation_source/localisation/english/HOK_KOR_us_defense_l_english.yml` | 읽기 전용 일반판 영어 번역 HEAD `11ec9e2096af906a086f5c076949f2da1a1c790d` 위 미추적 파일의 동결본. 실제 영국 영어36키를 정확히 재사용하며 원본 루트·SHA·크기를 manifest에 기록. 별도 영어 모드를 의존성으로 추가하지 않음 |
| `documents/<원본 상대 경로>` | 명세·크레딧·자산 manifest·사건 기록4개와 채택 PNG6개를 보존. source capsule의 증거이며 문서에 기록된 donor 실행을 포트 결과로 바꾸지 않음 |
| [source-manifest](source-manifest.json)·[잠금](../../../tools/hok_us_defense_update_lock.json) | manifest는 각 원본/사본 역할·Git blob·SHA/크기·host/schema 공급자를 기록. 잠금은 manifest SHA와 최종18출력·이전 해시·분류를 고정 |
| [소유 생성기](../../../tools/upstream_us_defense.py) | 기존 포트 위의2병합과 신규16개를 생성하도록 통합 중. 기존 핵분열 뒤 terminal hook·정확한 역사 역투영을 사용하고 이전 source pins는 보존 |
| `C:\hoi\test\hok-rt56-us-defense-update-20261111-01\` | 새 시험·진단 helper/보고서/미리보기/백업. 이 capsule과 `C:\hoi\test\hok-rt56-source-cache\sources\`의 활성 역사 입력을 시험 출력으로 사용하지 않음 |

최종 대상은6사건·4정신·5effect·1trigger·한영 각36키·GFX2개·DDS8개와 기존 중점/사건2병합이다. DDS는8개 모두 `ASSET_COPY`, 새 코드/GFX/locale은 `ADD`, 기존2개는 `THREE_WAY_MERGE`로 관리한다. 이미 반영된 핵분열 보너스·지역 산업, donor README의 일반 안내는 이번 delta에서 제외한다.

채택 PNG6개와 [크레딧](documents/docs/HOK_KOREAN_US_DEFENSE_ASSET_CREDITS.md)·[자산 manifest](documents/docs/data/HOK_KOREAN_US_DEFENSE_ASSET_MANIFEST.json)는 AI 생성 원본·편집·DDS 변환·권리 귀속의 근거다. raw HOK/Paradox 국기 TGA/PNG는 읽기 전용 원본 참조로 남겨 이 capsule에 복사하지 않았다. 보관 문서의 그 참조 링크는 원본 provenance를 가리키며 여기서 해당 사본의 존재나 공개 배포 권한을 뜻하지 않는다. 이 폴더는 배포 패키지가 아니며 필요한 공개 크레딧·권리 고지는 별도 release allowlist에서 선택해야 한다.

실제 적용·정적 결과와 로드/UI·효과·저장 미검증 항목은 구현 기록을 따른다. 원본·현재 RT56 world/shared ownership·기존 ID/핀·cache를 보존하고 게임 실행·사용자 설정 변경·자료 정리·Git·업로드는 수행하지 않는다.
