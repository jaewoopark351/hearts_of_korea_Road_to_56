# 2026-11-11 핵분열 연구 보너스 선택 입력

이 폴더는 유지할 출처 증거다. 재사용·생성기 수정·재생성 전 [구현 기록](../../implementation/2026-11-11-korean-fission-research-bonus-port.md)과 [새 잠금](../../../tools/hok_fission_update_lock.json)을 읽는다. 표시 의미를 검토할 때는 [변경 영향 절차](../../HOK_CHANGE_COVERAGE_REVIEW.md)를 따른다. 실제 적용·정적 검증 결과는 구현 기록에서 확인하며, 이 안내 자체는 검사 성공을 뜻하지 않는다.

| 위치·자료 | 역할 |
|---|---|
| `C:\hoi\hearts_of_korea` | 읽기 전용 원본. HEAD `1c2e5423c08677228fa89c0181535bc30fc5764d` 위의 미커밋 runtime 두 줄과 문서2개를 선택. HEAD의 지역 산업 변경은 기존 이식과 중복 적용하지 않음 |
| [민간 핵 연구 명세](documents/docs/HOK_KOREAN_CIVIL_NUCLEAR_RESEARCH_SPEC.md)·[원본 사건 기록](documents/docs/incidents/2026-10-31-korean-civil-nuclear-research.md) | 원본 문서2개의 증거 사본. 현재 두 줄 추가의 의도와 과거 실행 이력을 구별하며 SHA-256은 새 잠금으로 확인 |
| donor Git blob `af90f80d2228961e869eca7615aed6bce579d80c` | runtime의 불변 이전 입력. CRLF checkout으로 복원한 뒤 잠금의 정확한 anchor와 literal 추가 문자열로 현재 donor 입력을 재현. runtime 전체 복사본은 보관하지 않음 |
| [새 잠금](../../../tools/hok_fission_update_lock.json) | Git object·checkout 이전/이후·호환판 이전/최종 SHA, 분류, 두 줄 추가, 문서 해시와 vanilla/RT56 문맥 지문 |
| [생성기](../../../tools/upstream_industry_update.py) | 기존 산업 계층을 보존하며 새 최종 출력을 `current_outputs`로 구별하고, 정확히 입증된 바이트만 이전 산업 출력으로 역투영하도록 확장하는 소유 코드 |
| `C:\hoi\test\hok-rt56-fission-update-20261111-01\` | 별도 시험·프리뷰·진단·검증 결과 위치. 이 capsule·외부 활성 source cache와 역할이 다름 |

선택 대상은 `HOK_KOR_fission_chain_reaction_experiments`의 기존 `add_tech_bonus`에 넣는 `bonus = 1.5`와 기여 주석뿐이다. 기존 선행 감소2년·사용1회·`nuclear`·핵 혁신100%, 이름과 한영 현지화·조건·기간·AI·다른473개 중점은 유지한다. 원본 전체 복사, 그림·지도·기존 산업 재이식은 하지 않는다.

이전 산업 잠금과 capsule·과거 source pins·승인된 ID 이관·RT56 소유권은 보존한다. 원본 HOK 저작과 포트 통합 기여를 구별하며 이 출처 보관은 배포 패키지나 포괄적인 재배포 허가가 아니다. 실제 UI·연구 적용/소모·저장 검증은 미실행이며 게임 실행·사용자 설정 변경·Git·업로드 동작은 포함하지 않는다.
