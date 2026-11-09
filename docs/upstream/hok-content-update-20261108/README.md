# 2026-11-08 원본 콘텐츠의 선택 입력과 재현 경로

이 폴더는 donor `596b221bb994d93fce552d3ee1ba70fa9b5640f1`에서 선택한 출처 사본과 기존15주 포트/현재 호스트의 재현 입력이다. **관리용 소스 입력**이며 테스트 출력이나 엔진 활성 모드 폴더가 아니다. 최초 문서화 뒤 사용자가 구현을 승인하여 만들었다.

후속 이식·재생성·출처 비교 전 [계획](../../plans/2026-11-08-hok-upstream-content-port-plan.md), [ADR-0007](../../decisions/0007-november-content-integration.md), [구현 기록](../../implementation/2026-11-08-hok-upstream-content-port.md), [새 잠금](../../../tools/hok_upstream_content_lock.json)을 읽는다. 이전 분할 입력은 [별도 안내](../hok-state-split-20261107/README.md)를 따른다.

| 위치 | 역할 |
|---|---|
| `C:\hoi\hearts_of_korea` | 원본, branch `feat/korean-focus-expansion-ai@596b221`, 이번 선택 당시 clean. 읽기 전용이며 runtime 의존성이 아님 |
| `runtime/` | 추가 검토36개 donor 경로의 정확한 checkout 바이트. 32개 출력의 직접/변환 소스와 유지·제외 후보를 함께 보존. 이 전체를 게임 root로 복사하지 않음 |
| `before/` | 해당 파일이 존재할 때 `0d73d49726abbfa435c73f1bf8cc24d4a5af014b`의 Git raw blob. 이전 미커밋 분할이나 포트 출력과 구분 |
| `compat_before/` | 기존 포트16개 선택 입력과 L-08 무수정 보호용1개. 실제 현재15주 포트의 사본이며 역투영/구형7개 보호에 사용 |
| `host/rt56/` | 물리 RT56 SOV 효과의 정확한 사본. 기존 한국 경계 정리 접점4곳 외 전체 보존 |
| `host/vanilla/` | 물리 vanilla `state_groups.txt`의 정확한 사본. 코민테른 한국 항목 하나 외 전체 보존 |
| `documents/` | 원본 명세·배분/그림 manifest·실행 이력·검토 지침13개. 원본 문맥과 과거 결과를 보존하며 호환판 지침/새 실행의 증거로 대체하지 않음 |
| [source-manifest.json](source-manifest.json) | 원본/사본 경로·크기·SHA-256·선택 커밋/Git blob·raw hash와 별도 host 입력의 원본/사본 대응 |
| `ledger_before.csv` | 새 콘텐츠 적용 전의 최종15주 분할 원장. 기존 source/host/영문/그림 기여와 변경되지 않은 행을 보존하는 기준 |
| `C:\hoi\test\hok-rt56-upstream-20261108-01\` | 실제 이번 테스트 helper·backup·preview·로그/화면/저장 사본·검사 보고서. source cache나 runtime 입력으로 참조하지 않음 |

개별 출력의 공급자·분류·source_path·이전/최종 SHA-256·소유 생성기는 새 잠금에 있다. `inputs[*].sha256`은 기존 포트 사본, `outputs[*].sha256`은 최종 생성 바이트, `host_inputs`는 현재 물리 RT56/vanilla 입력이다. 서로 다른 역할의 같은 상대 경로를 동일 소스라고 취급하지 않는다. 호스트 입력2개는 `THREE_WAY_MERGE`이며 donor의 짧은 override 파일과 실제 출력 경로가 다르다.

13개 CNDP DDS는 원본의 새 도형/지리 윤곽 도안에서 만든32×32 자산을 바이트 보존해 이식했다. 원작 HOK·vanilla 지도 계통과 kpopmodder의 신규 도안/연결 기여를 구분한다. 실제 SVG/PNG/레시피 위치와13개 해시는 보존된 [그림 출처](documents/docs/HOK_KOREAN_CNDP_ARTWORK.md), [아이콘 manifest](documents/docs/data/HOK_KOREAN_CNDP_ICON_MANIFEST.json)를 따른다. 그림을 다시 가공하거나 과거 `.local-artifacts` 경로를 해석할 때 [호환판 자료 안내](../../HOK_DEVELOPMENT_ARTIFACT_ARCHIVE.md)를 먼저 읽는다. 기존 활성 캐시 `C:\hoi\test\hok-rt56-source-cache\sources\` 세 트리와 기존 archive는 수정하지 않았다.

원본 문서의 내부 상대 링크는 donor 문맥을 보존한다. 여기 없는 참조는 읽기 전용 donor의 대응 문서에서 찾는다. `documents/AGENTS.md`의 donor 정체성·개인사·언어 정책은 출처 기록일 뿐 호환판 공통 지침을 바꾸지 않는다. 두 호스트 파일의 기존 코드·기여와 필요한 고지도 유지하며 이 자료가 포괄 재배포 허가나 업로드 승인을 뜻하지 않는다.
