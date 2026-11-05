# 2026-11-05 로컬 테스트 산출물 외부 보관

사용자의 `.local-artifacts` 이동 요청에 따라 첫 단계에서 테스트·실행 증거, 감사 자료, 이전 파일 백업과 임시 작업 문서를 외부에 보관하고, 활성 생성기 입력인 `sources/`는 당시 경로에 유지했다. 후속 전체 이동 요청으로 이 입력도 별도의 활성 외부 캐시로 옮겨 저장소의 `.local-artifacts`를 완전히 제거했다. 아래에 두 단계의 결과를 구분해 기록한다. 작업 기준은 `feat/korean-focus-update-20260922@fd1fec24b7098ae59307ab56189a93b31ad93a91`이며, 작업 전에 있던 `AGENTS.md` 문서 변경을 보존했다.

## 경로 대응

| 구분 | 위치 |
|---|---|
| 이전 기준 경로 | `C:\hoi\hearts_of_korea_Road_to_56\.local-artifacts\` |
| 외부 보관 기준 경로 | `C:\hoi\test\hok-rt56-artifact-archive-20261105-01\.local-artifacts\` |
| 첫 단계에서 유지했던 생성기 입력 | `C:\hoi\hearts_of_korea_Road_to_56\.local-artifacts\sources\` |
| 후속 이동 후 활성 생성기 입력 | `C:\hoi\test\hok-rt56-source-cache\sources\` |
| 후속 소스 이동 확인 기록 | `C:\hoi\test\hok-rt56-source-relocation-20261105-01\` |

옮긴 항목은 `2026-09-23-second-wave-geography/`, `audits/`, `git/`, `korean-icon-port-20260922/`, `material-cycle-20261003/`, `runtime/`, `second-wave/`, `second-wave-port-20260923/`, `commit-message-20260922.txt`, `policy-update-commit-message.txt`다. 모든 하위 상대경로를 그대로 보존했다. 예를 들어 과거 문서의 `.local-artifacts/runtime/2026-09-22/`는 이제 외부 보관 기준 경로 아래의 `runtime/2026-09-22/`에서 찾는다. 역사적 문서의 옛 경로·검증 결과는 일괄 수정하지 않았으며 고유 증거도 폐기하지 않았다.

## 첫 단계 보존과 확인

외부 사본 **587파일·25,387,224 bytes**의 상대경로·크기·SHA-256을 원본과 대조한 후, 허용된 원본 항목만 제거했다. 제거 후 외부 사본을 다시 확인했다. 최종 확인 시각은 2026-11-05 22:49 KST이며, 기록은 [verification.json](C:/hoi/test/hok-rt56-artifact-archive-20261105-01/verification.json)에 있다. 파일별 해시는 [archived-files.csv](C:/hoi/test/hok-rt56-artifact-archive-20261105-01/archived-files.csv), 제거 전 확인은 같은 외부 작업 디렉터리의 `verification-before-remove.json`에 보관했다. 이동 도우미 `archive.ps1`과 원장·디렉터리 목록도 그 외부 디렉터리에만 있다.

첫 단계 종료 시 저장소의 `.local-artifacts`에는 `sources/`만 남았다. **1,490파일·201,424,389 bytes**와 기존 해시가 유지됐으며, 당시 내역은 [preserved-source-files.csv](C:/hoi/test/hok-rt56-artifact-archive-20261105-01/preserved-source-files.csv)에 있다. 세 입력 `hok-887930f-korea-118d7b5`, `hok-icons-20260922`, `hok-second-wave-be5fb40`은 당시 [source_snapshot.py](../../tools/source_snapshot.py)의 저장소 내부 경로 상수에서 소비했다. 이들은 감사된 소스·그림 입력이며 테스트 산출물 정리 대상으로 취급하지 않았다.

첫 단계에서는 게임 콘텐츠·생성기·설정을 변경하지 않았고, 게임플레이 validator, 게임 실행, 커밋·푸시·게시·업로드를 수행하지 않았다. 이 확인은 파일 보관의 무결성 확인이며 게임 동작 검증이 아니다.

## 후속 활성 소스 캐시 이동과 전체 폴더 제거

후속 요청은 저장소에 남은 `sources/`까지 옮겨 `.local-artifacts` 전체를 제거하는 범위다. 감사된 입력을 폐기하지 않고 `C:\hoi\test\hok-rt56-source-cache\sources\`로 복사했다. 이 경로는 과거 테스트 증거를 보관한 첫 단계 archive와 별개인 **활성 생성기 입력 캐시**다. 외부 캐시 기준 경로의 `README.txt`에도 이 역할과 임의 정리 금지를 명시했다. 테스트 보고서·그림 처리 중간물·새 그림 출력의 저장 위치로 사용하지 않으며 기존 소스 핀과 입력 해시를 유지한다.

| 이전 상대경로 | 현재 활성 캐시 상대경로 |
|---|---|
| `.local-artifacts/sources/hok-887930f-korea-118d7b5/` | `sources/hok-887930f-korea-118d7b5/` |
| `.local-artifacts/sources/hok-icons-20260922/` | `sources/hok-icons-20260922/` |
| `.local-artifacts/sources/hok-second-wave-be5fb40/` | `sources/hok-second-wave-be5fb40/` |

오른쪽 상대경로의 기준은 `C:\hoi\test\hok-rt56-source-cache\`다. 각 하위 경로·대소문자·내용을 그대로 보존했다. 과거 그림 manifest·출처·레시피의 저장소 `.local-artifacts/sources/<상대경로>` 참조는 이제 외부 활성 캐시의 `sources/<상대경로>`로 해석하며, 기존 테스트 증거 참조는 첫 단계의 역사적 archive로 해석한다. 과거 문서를 일괄 치환하거나 두 외부 저장소의 역할을 합치지 않는다.

복사한 **1,490파일·201,424,389 bytes·하위 디렉터리 160개**의 경로·크기·SHA-256을 원본과 대조한 뒤, 지정된 저장소 원본과 빈 `.local-artifacts` 루트만 제거했다. 제거 후 외부 입력의 해시가 유지되고 옛 루트가 존재하지 않음을 확인했다. 완료 시각은 **2026-11-05 23:14 KST**이며 최종 [relocation-record.json](/C:/hoi/test/hok-rt56-source-relocation-20261105-01/relocation-record.json)의 UTC 시각은 `2026-11-05T14:14:10.4566538Z`다. 제거 전 확인은 같은 외부 디렉터리의 `verification-before-remove.json`, 파일별 크기·해시는 `source-files.csv`, 하위 디렉터리 목록은 `source-directories.json`에 보관했다. 이동 도우미와 검증 출력도 이 외부 증거 디렉터리에만 있다.

두 단계 전체로는 **2,077파일·226,811,613 bytes**를 보존했다. 첫 단계의 587파일은 역사적 archive에, 나머지 1,490파일은 활성 외부 소스 캐시에 있다. 저장소 `.local-artifacts`에는 남은 파일이나 디렉터리가 없으며 새 소스 import·테스트·그림 작업으로 이를 다시 만들지 않는다.

## 생성기 경로와 검증 범위

`tools/source_snapshot.py`의 `SOURCE_CACHE_ROOT`를 `C:\hoi\test\hok-rt56-source-cache\sources`로 두고 기존 `HOK_ROOT`, `ICON_ROOT`, `SECOND_WAVE_ROOT`가 이 기준을 사용하도록 바꿨다. `README.md`와 `AGENTS.md`의 현재 작업 경로도 갱신했다. immutable Git 객체·소스 lock·입력 해시·기존 runtime 출력은 바꾸지 않았다. 실제 import 경로 확인은 세 입력이 모두 외부 캐시로 해석됨을 확인했다.

이동 전 aggregate 검사는 **20 PASS / 0 WARNING / 7 ERROR**, 이동 후 검사는 **21 PASS / 0 WARNING / 6 ERROR**였다. 남은 6개 source-pin·descriptor 오류의 문자열은 이동 전과 모두 같고, 새 오류는 0개다. 앞선 문서 sync로 생긴 `AGENTS.md` 통합 원장 불일치 1개는 기존 생성기로 현재 문서 메타데이터를 재생성해 해소했다. 전체 검사 통과를 주장하지 않으며 기존 6개 오류 수리는 이번 경로 이동 범위에 포함하지 않는다.

소스 snapshot·통합 원장 gate는 통과했다. 통합 원장 1,505행의 순서·분류와 나머지 필드는 보존했고, `AGENTS.md`·`README.md` 두 행의 `output_sha256`만 갱신했다. 전체 검사 뒤에도 저장소 `.local-artifacts`가 다시 생기지 않았다. RT56 manifest `7553774178744855191`과 descriptor 해시는 이번 이동 전후 동일하다. 상세 출력은 [final-validation.txt](/C:/hoi/test/hok-rt56-source-relocation-20261105-01/final-validation.txt), 전후 결과 대조는 [validation-comparison.json](/C:/hoi/test/hok-rt56-source-relocation-20261105-01/validation-comparison.json), 원장 행 차이는 [manifest-row-diff.json](/C:/hoi/test/hok-rt56-source-relocation-20261105-01/manifest-row-diff.json)에 있다.

파일 이동 무결성과 생성기 입력 경로 확인을 게임 동작 검증으로 간주하지 않는다. 이번 이동에서 HOI4를 실행하거나 게임·launcher 설정을 변경하지 않았으며 커밋·푸시·게시·업로드도 수행하지 않았다.
