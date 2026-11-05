# HOK × RT56 개발 자료 보관·이미지 원본 탐색 안내

기록일: 2026-11-06. 이 문서는 호환판의 외부 개발 자료와 활성 소스 캐시 위치, 옛 경로의 대응 관계, 후속 이미지 작업의 자료 확인 절차를 관리한다. 이미지 제작·수정, 과거 입력·레시피 재사용, `.local-artifacts` 경로 해석 또는 기록된 자료 위치를 변경하기 전에 읽는다. 작업 권한과 공통 보존 규칙은 [AGENTS.md](../AGENTS.md)를 따른다.

## 1. 현재 위치와 역할

호환판의 옛 위치는 `C:\hoi\hearts_of_korea_Road_to_56\.local-artifacts\`다. 2026-11-05에 두 단계로 외부 이동을 마쳐 저장소의 해당 폴더를 제거했다. 소스 import·테스트·이미지 처리 출력용으로 다시 만들지 않는다.

| 자료 구분 | 현재 위치 | 사용 방법 |
|---|---|---|
| 호환판의 과거 테스트·로그·백업·작업 자료 | `C:\hoi\test\hok-rt56-artifact-archive-20261105-01\.local-artifacts\` | 옛 상대 경로를 유지한 읽기 전용 보관 자료 |
| 호환판의 활성 생성기 입력 | `C:\hoi\test\hok-rt56-source-cache\sources\` | 기존 lock과 해시로 고정한 입력 캐시. 임의 정리 대상이나 새 출력 위치로 사용하지 않음 |
| 활성 소스 이동 확인 기록 | `C:\hoi\test\hok-rt56-source-relocation-20261105-01\` | 이동 당시 파일 목록·해시·경로 확인·정적 검사 기록 |
| 프로젝트가 관리하는 그림 원본·크레딧·manifest | 저장소의 관련 `docs/assets/`, `docs/data/`, `docs/upstream/` 및 자산 문서 | 작업 대상의 현재 manifest와 출처 기록으로 필요한 파일을 확인 |
| 새 테스트·이미지 처리 중간물 | `C:\hoi\test\<새 작업 또는 실행 ID>\` | 새 작업마다 별도 위치를 정하고 원본과 보관 자료를 보존 |

활성 캐시는 [source_snapshot.py](../tools/source_snapshot.py)의 `SOURCE_CACHE_ROOT`를 통해 사용한다. 그 아래 세 입력은 `hok-887930f-korea-118d7b5`, `hok-icons-20260922`, `hok-second-wave-be5fb40`이다. `C:\hoi\test\hok-rt56-source-cache\README.txt`에도 활성 입력 역할을 명시했다. 기존 pinned 소스·내용·해시를 보존하며 테스트 보고서·미리보기·새 그림 출력과 구분한다.

보관 자료와 기록 파일은 일반 개발 중 읽기 전용 참고자료로 취급한다. 이는 운영체제의 읽기 전용 속성이나 ACL을 설정했다는 뜻이 아니다. 활성 캐시는 기존 결정적 소스 생성기와 lock 규칙을 따르며, 이 문서 자체는 보관 자료 수정·삭제·추가 이동, 소스 핀 변경 또는 스크립트 실행을 허가하지 않는다.

## 2. 파일 목록과 보관 당시 검증

첫 단계 기록의 기준은 `C:\hoi\test\hok-rt56-artifact-archive-20261105-01\`다.

| 기준 경로 아래 파일 | 용도 |
|---|---|
| `verification.json` | 첫 단계 원본·보관 위치와 복사·검증·제거 완료 결과 |
| `verification-before-remove.json` | 지정 원본을 제거하기 전 사본 대조 결과 |
| `archived-files.csv` | 보관 파일별 상대 경로·바이트 크기·SHA-256·원래 수정 시각 |
| `archived-directories.json` | 보관한 상대 디렉터리 구조 |
| `preserved-source-files.csv` | 첫 단계 당시 저장소에 남겼던 생성기 입력의 목록과 해시. 이 입력은 이후 활성 외부 캐시로 이동함 |

후속 소스 이동 기록의 기준은 `C:\hoi\test\hok-rt56-source-relocation-20261105-01\`다. `relocation-record.json`은 이전·이후 위치와 완료 결과, `verification-before-remove.json`은 제거 전 확인, `source-files.csv`는 입력 파일별 상대 경로·크기·SHA-256·원래 수정 시각, `source-directories.json`은 하위 디렉터리 구조를 담는다.

| 2026-11-05에 기록한 작업 | 파일 수 | 파일 합계 | 확인 범위 |
|---|---:|---:|---|
| 첫 단계 과거 산출물 보관 | 587 | 25,387,224바이트 | 원본·사본의 상대 경로·크기·SHA-256 대조 후 지정 원본 제거, 제거 후 사본 재확인 |
| 후속 활성 소스 캐시 이동 | 1,490 | 201,424,389바이트 | 기존 입력 목록과 원본·사본 대조, 하위 디렉터리 160개 확인, 제거 후 사본과 옛 루트 부재 확인 |
| 두 단계 합계 | 2,077 | 226,811,613바이트 | 과거 산출물과 활성 입력의 위치·역할을 구분해 보존 |

이는 보관·이동 당시의 기록이며, 후속 작업이 모든 파일의 해시를 다시 대조했다는 뜻으로 사용하지 않는다. 작업 순서, 시각과 당시 정적 검사 결과는 [2026-11-05 호환판 이동 감사](audits/2026-11-05-local-artifact-archive.md)를 따른다. 파일 보관 확인과 HOI4 게임 동작 검증도 구분한다.

## 3. 원본 모드의 별도 보관소

HOK donor의 옛 `C:\hoi\hearts_of_korea\.local-artifacts\` 자료는 다음 위치에 있다. 호환판의 원본 입력·합성 레시피가 donor에서 유래한 경우 해당 출처를 확인한 뒤 이 보관소를 참조한다.

| 자료 | 현재 위치 |
|---|---|
| donor의 이동한 원본 | `C:\hoi\test\archive-local-artifacts-20261105\original\.local-artifacts\` |
| donor의 추가 보존 사본 | `C:\hoi\test\archive-local-artifacts-20261105\.local-artifacts\` |
| donor의 위치·검증 기록 | `C:\hoi\test\archive-local-artifacts-20261105\archive-record.json` |
| donor의 파일 목록·해시 | `C:\hoi\test\archive-local-artifacts-20261105\source-manifest.json` |
| donor의 디렉터리 목록 | `C:\hoi\test\archive-local-artifacts-20261105\source-directories.json` |

원본 자료 탐색은 donor의 이동한 원본에서 시작하고, 필요한 파일이 없으면 추가 보존 사본과 manifest를 확인한다. 이 두 보관 트리는 donor의 자료이며 호환판 보관소의 추가 사본이 아니다. donor의 수량·검증 결과·작업 이력을 호환판의 결과로 합산하지 않는다. donor의 [개발 자료 보관 안내](../../hearts_of_korea/docs/HOK_DEVELOPMENT_ARTIFACT_ARCHIVE.md)도 읽기 전용 출처 문서다.

## 4. 과거 경로를 찾는 방법

자료의 원래 프로젝트를 출처 기록과 manifest로 먼저 확인한다. `docs/upstream/`에 복사된 donor 문서의 경로도 원래 donor를 기준으로 해석한다. 다음 표는 절대 경로와 `<PROJECT>/.local-artifacts/` 같은 과거 표기에도 동일하게 적용한다.

| 원래 프로젝트와 과거 상대 경로 | 현재 해석 |
|---|---|
| 호환판 `.local-artifacts/sources/<상대 경로>` | `C:\hoi\test\hok-rt56-source-cache\sources\<상대 경로>` |
| 호환판 `.local-artifacts/<그 밖의 상대 경로>` | `C:\hoi\test\hok-rt56-artifact-archive-20261105-01\.local-artifacts\<그 밖의 상대 경로>` |
| donor `.local-artifacts/<상대 경로>` | `C:\hoi\test\archive-local-artifacts-20261105\original\.local-artifacts\<상대 경로>` |

파일명 대소문자와 남은 상대 경로를 보존한다. 예를 들어 호환판의 옛 `.local-artifacts/sources/hok-icons-20260922/`는 활성 외부 캐시의 `sources/hok-icons-20260922/`에, `.local-artifacts/runtime/2026-09-22/`는 호환판 과거 보관소의 `runtime/2026-09-22/`에 대응한다. 역사적 문서·manifest·레시피의 경로를 일괄 치환하지 않고 이 대응표로 찾는다.

필요한 파일이 없거나 해시가 충돌하면 해당 자료의 파일 목록·해시 기록을 확인하고 문제 경로를 보고한다. 확인되지 않은 원본을 찾았다고 주장하거나 출처를 지어내지 않는다. 원본을 임의로 대체·재생성한 뒤 과거 자료인 것처럼 취급하지 않는다. 누락된 자료에 의존하는 작업은 멈추고, 독립적으로 가능한 승인 범위의 작업만 계속한다. 별도로 승인된 신규 이미지 제작은 그 작업의 범위와 출처 기록을 따른다.

## 5. 이미지 제작·수정 전 확인 순서

이미지 작업이 승인된 경우 다음 순서로 자료를 확인한다.

1. 현재 호환판의 완성 이미지, GFX·sprite 연결과 관련 명세·크레딧·manifest를 읽는다. 필요한 원본 이미지·프롬프트·합성 레시피·원출처·기록된 해시를 위 대응표와 현재 프로젝트 자료에서 찾는다. 대화 기억 대신 실제 파일로 작업 기준을 확인한다. 기존 신규 아이콘은 [아이콘 manifest](data/HOK_KOREAN_FOCUS_ICON_MANIFEST.json), [소재 크레딧](HOK_KOREAN_FOCUS_ICON_CREDITS.md), [색상 계획](HOK_KOREAN_FOCUS_ICON_COLOR_PLAN.md)도 대조한다.
2. 중간 출력은 새 `C:\hoi\test\<새 작업 또는 실행 ID>\`에서 만든다. 필요한 과거 입력만 새 작업 폴더에 복사하고 선택한 원래 위치와 해시를 기록한다. 역사적 보관소와 활성 소스 캐시를 새 이미지 작업 폴더로 사용하거나 덮어쓰지 않는다.
3. 과거 스크립트를 재사용하기 전에 내부에 고정된 입력·출력·보고서·미리보기·백업 경로를 읽는다. 과거 입력은 대응표로 찾고 새 출력은 현재 작업의 외부 경로로 설정한다. 저장소의 옛 `.local-artifacts`, 보관 원본·사본, 활성 캐시 또는 업로드 패키지에 이미지 작업 결과를 쓰는 스크립트를 그대로 실행하지 않는다. 레시피를 읽는 행위는 실행이나 추가 이미지 변경을 허가하지 않는다.
4. 승인 범위의 완성 런타임 이미지와 프로젝트 소유 GFX·상대 참조를 호환판에 통합한다. 필요한 선택 원본과 크레딧·manifest는 프로젝트의 관리 문서 위치에 보존하고, 실제 출처·선택한 입력·제작 또는 가공 방법·최종 해시·새 외부 작업 경로를 기록한다. HOK 내부 런타임 이미지 보관, 저작자·사용 조건, 결정적 생성, 상대 참조와 문서화된 RT56·vanilla 공유 이미지 예외를 유지한다.

## 6. 위치 변경 시 갱신

승인된 작업으로 위치가 바뀌면 이 문서의 이전·이후 경로, 원본·추가 사본·활성 캐시의 역할, manifest 위치, 경로 대응표와 실제 검증 결과를 함께 갱신한다. 기존 작업 결과와 새 확인 결과를 구분한다. 상세 실행 이력은 관련 감사 문서에 남긴다.

이 문서 자체의 위치를 바꾸면 [AGENTS.md](../AGENTS.md)의 상대 링크와 필수 열람 조건을 같은 문서 변경에서 갱신한다. 실제 테스트·중간 출력은 외부 작업 경로에 두고, 프로젝트에는 유지할 위치·출처 안내만 둔다. 이 안내는 Workshop 배포 허용 목록에 자동으로 포함되는 파일이나 이미지·게임 코드 변경 권한이 아니다.
