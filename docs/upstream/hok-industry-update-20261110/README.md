# 2026-11-10 지역 산업 업데이트 선택 입력

이 폴더는 유지할 출처·생성 입력이다. 프리뷰·시험·진단 결과는 `C:\hoi\test\hok-rt56-industry-update-20261110-01\`에 둔다. 이 입력을 재사용하거나 해당 계층을 수정·재생성하기 전 [구현·검증 기록](../../implementation/2026-11-10-korean-industry-update-port.md), [변경 영향 절차](../../HOK_CHANGE_COVERAGE_REVIEW.md), [새 잠금](../../../tools/hok_industry_update_lock.json)을 읽는다. 지도 대응을 판단할 때는 [ADR-0006](../../decisions/0006-korean-state-split-integration.md)과 그 결정의 이번 후속 예외를 따른다.

| 위치 | 역할 |
|---|---|
| `C:\hoi\hearts_of_korea` | 읽기 전용 원본. `596b221bb994d93fce552d3ee1ba70fa9b5640f1` 위의 미커밋 8파일을 선택했다. HEAD만으로 현재 업데이트를 복구할 수 없다. |
| `donor_head/` | 원본 8파일의 HEAD Git blob. 이전 포트 출력이나 checkout 개행 사본이 아니다. |
| `donor_worktree/` | 선택 당시 원본 8파일의 정확한 바이트. runtime 6개와 명세 2개다. 연구망 현지화 2개는 의도적 유지의 근거이며 실제 수정 출력이 아니다. |
| `compat_before/` | 호환판 `287c5a22f264075bac65505e0a3e9d8a29ff24f3`의 수정 대상 4파일. 이전 출력의 재현·보호·역투영 입력이다. |
| `translation_source/` | 일반판 영어 번역 `34f1c7740f2b152c97c9993413202bd3d14d8fe4` 위 미커밋 산업 현지화 1파일. 16값만 재사용하고 남북 지명은 포트의 기존 영어로 맞춘다. 이 서브모드를 runtime 의존성으로 추가하지 않는다. |
| [출처 목록](source-manifest.json) | 원본·사본·Git blob·크기·SHA-256·선택 상태를 구별하는 유지 기록. |
| [생성기](../../../tools/upstream_industry_update.py)·[잠금](../../../tools/hok_industry_update_lock.json) | 기존 포트 위의 8개 보상/해금 블록, 독립 산업 결정과 한영 문구만 합성한다. 이전/최종 해시·분류·확정 문구·host/schema 지문을 고정한다. |

원본 전체를 덮어쓰지 않는다. 기존 역사 계층·source pins·외부 active cache·기존 source capsule은 유지한다. 과거 보상 분배를 새 값으로 고쳐 기록하지 않으며, 이번 후속의 의도적인 보상 증가를 별도 기록한다. 지도/ID·시작 산업·연구망 효과·공용 sprite·descriptor는 이번 변경 대상이 아니다.

원본 HOK 저작, 기존 번역 기여와 kpopmodder의 포트 통합 기여를 유지한다. 이 capsule은 배포용 폴더나 포괄적인 재배포 허가가 아니다. 실제 정적·UI·효과·저장의 확인 범위는 구현 기록을 따른다.
