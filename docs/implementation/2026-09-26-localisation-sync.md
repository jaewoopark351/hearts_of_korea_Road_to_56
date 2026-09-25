# 2026-09-26 원본 현지화 갱신 이식

## 요청 범위와 출처

원본 모드의 GitHub 커밋을 확인하고 수정된 현지화를 호환판에 옮기는 작업이다. 원본 작성자의 문장·결정 설명·문장부호 변경을 반영하며 게임플레이, 지도, 그림, descriptor와 언어 의존성은 변경하지 않는다.

- compatibility 시작 상태: `feat/korean-focus-update-20260922@32d87f88f07060a5d9110d01102dde36ea42d0af`, 작업 트리 깨끗함.
- donor: `C:/hoi/hearts_of_korea`, `feat/korean-focus-expansion-ai@8609d0b61e4c00e6be6c204dcf31cfa41150664e`, 작업 전후 깨끗함.
- GitHub 원격 브랜치도 읽기 전용 `git ls-remote`로 같은 HEAD 확인. fetch, checkout, commit, push는 하지 않았다.
- [원본 커밋](https://github.com/jaewoopark351/hearts-of-korea/commit/8609d0b61e4c00e6be6c204dcf31cfa41150664e): `fix(localisation): compact decision text and normalize punctuation`, 2026-09-26 02:28:31 +0900.
- 새 [출처 잠금](../../tools/hok_localisation_update_lock.json)은 28개 경로별 commit/blob/SHA-256/크기와 이식 전 출력 SHA-256을 기록한다. 네 기존 잠금 파일은 바꾸지 않았다. 기존 잠금과 동일한 정확한 바이트 검증 규칙을 유지한다.

## 설치·로드 기준선

Windows 설치 `launcher-settings.json`은 `Operation Postern v1.19.3.0.c01a (5632)`, Steam build `25205862`를 기록한다. 2026-09-26 02:18의 최신 `system.log`는 같은 버전, donor 실행 checksum `ebe8`, 활성 DLC 36개, 활성 모드 1개를 기록한다. 현재 `dlc_load.json`은 `mod/hearts of korea.mod` 하나만 활성화하고 실제 경로는 donor다. `disabled_dlcs=[]`, 언어는 `l_korean`이다. 이는 호환판 C0/C1 실행 증거가 아니다. 게임·플레이세트·사용자 설정을 조작하지 않았다.

RT56 item `820260968`의 manifest는 작업 전후 `7475007536894105204`이며 기록된 업데이트 시각은 `2026-09-07T23:14:24Z`다. [9월 22일 재기준선](../audits/2026-09-22-source-rebaseline.md)과 일치한다.

RT56 현지화 313파일의 목록 지문도 작업 전후 `9C89A0CB3459D09CB51231BA22FC10175FA793E550859D06838F552C5B305147`로 같다. 계산 방식은 각 파일의 `상대 POSIX 경로 + 탭 + 대문자 SHA-256`을 정렬해 줄바꿈으로 연결한 UTF-8 바이트의 SHA-256이며 마지막 줄바꿈은 없다.

현재 repository/외부 launcher descriptor는 RT56 + Korean Language, `1.19.*`, 호환판 item `3796816200`을 선언하며 외부 path는 이 저장소를 가리킨다. donor item은 `3793992662`다. RT56는 `history/states`, `map/strategicregions`를 대체한다. Korean Language `2743487021`은 `1.17.*`를 선언하며 replace_path가 없고, RT56 Korean Translation `2769576030`은 `1.19.*`, RT56 의존성, `replace_path="localisation"`을 선언한다. 두 번역 모드는 현재 비활성이다. 최종 언어 계약은 이번 작업으로 확정하지 않는다.

| descriptor | SHA-256 |
|---|---|
| compatibility | `AA150D6CE82A7779C3D4C3FCDC962A82FA269327F005330B565723CA87BBE247` |
| donor | `3FBC6868A7D95BACD6B55AF71593A61AF3A7EADA5654D46CC4C828422ECA032A` |
| RT56 | `5B323861ABD63E31CB896277E3EA58BA4BCD9FCEEDA957B50792065E42E03F61` |
| Korean Language | `F5813D345DD0FC01E80F68B65901B1D060A238336D3D2A89EAA8404A40329346` |
| RT56 Korean Translation | `A0508F4A91AF911917AD3A84BF829CB38ED1557DD8F9643A010F1AEE36F48D6C` |

## 검토와 병합 결정

`CONFIRMED`: 14개 한국어·영어 채널 쌍, 총 28파일에서 값 502개가 바뀐다. 두 채널은 기존 설계대로 동일한 한국어 본문을 유지한다. 파일당 키 집합과 순서가 같으며 총 1,420개 키가 보존된다. BOM, `$...$` 치환, `[FROM.GetName]`, 아이콘 참조도 유지한다. 색상 강조 축약, 대화 따옴표 이스케이프, 말줄임표 정리는 원본의 의도적인 변경이다.

축약된 결정 설명의 비용·기간·동시 수행·대기시간·취소·환급 규칙은 기존 공유 분류/착수/종료 툴팁과 호출 관계를 함께 검토했다. 원본 코드나 효과를 바꾸지 않고 작성자의 문구를 이식했다.

모든 대상은 기존 `ADD` 분류를 유지한다. RT56 313개, vanilla 2,083개, Korean Language 194개, RT56 Korean Translation 308개 현지화 파일을 조사하여 대상 경로 및 710개 고유 키와의 충돌이 없음을 확인했다. compat 66개와 donor 68개 현지화 파일에서도 대상 키는 선택된 28개 경로에만 있다. 호스트에 대응 정의가 없으므로 덮어쓸 RT56 본문은 없다.

26개 출력은 새 donor Git blob과 바이트 단위로 같다. `HOK_KOR_manchurian_followup` 두 파일은 [ADR-0005](../decisions/0005-korean-second-wave-regional-integration.md)의 기존 RT56 지역 안내를 재적용한다. 각 채널의 24개 설명 접미사, 전체 48개와 채널당 84개의 순서 있는 `$STATE_...$` 참조를 그대로 보존했다. 기존 지역 기여 주석도 유지한다.

기존 생성기의 지역 현지화 정규식은 새 원본의 `\"` 대화 따옴표를 처리하지 못했다. 이스케이프된 문자를 문자열 내부로 인식하도록 해당 정규식만 수정했다. 지역 집합·조건·게임플레이 변환은 바꾸지 않았다.

## 생성 및 검증

기존 `source_snapshot.py`, `build_korean_focus_update.py`, `korean_second_wave_geography.py`, `check_korean_second_wave.py`, `build_integration_manifest.py`를 갱신했다. 현지화 계층은 기존 정책 계층 다음에 적용한다. 이전 출력 해시·키 순서와 고정 commit/blob을 확인하며 다른 사용자 변경을 덮어쓰지 않는다. 런타임 파일은 생성기로만 썼고 통합 원장 1,411행 중 해당 28행의 출처를 갱신했다.

사용한 Python은 `C:/Users/jaewo/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`다.

| 확인 | 결과 |
|---|---|
| 쓰기 전 생성 미리보기 | 관리 출력 400개 중 정확히 현지화 28개만 변경 |
| 생성기·출처·통합 원장 | aggregate의 모든 관련 `--check` 통과 |
| 별도 출력 비교 | 502개 값 변경, 48개 지역 접미사 보존, 26파일 원본 바이트 일치 |
| 키·채널·인코딩 | 선택된 14쌍 본문 일치, 키/순서/BOM 유지; 전체 66파일·5,050키 검사 통과 |
| 전체 정적 검사 | `python tools/validate_port.py`: **20 PASS / 0 WARNING / 1 기존 ERROR** |
| diff 검사 | `git diff --check` 통과; 게임플레이·지도·그림·descriptor diff 없음 |

기존 ERROR는 `history/countries/KOR - Korea.txt`의 MtG 분기 전쟁 지지도 `0.1`과 교리 생성기 기대값 `0.05`의 불일치다. [직전 정책 이식 기록](2026-09-23-korean-policy-delta.md)과 같은 문제이며 이 파일의 SHA-256은 계속 `243FC1FBDE8DB75B82CCFEBD6BB01CA7001DABCD944CA8534E7324413705BE30`이다. 이번 범위에서 값이나 검사를 변경하지 않았다.

`UNPROVEN`: 실제 게임의 줄바꿈·따옴표·툴팁 높이·한국어 UI 렌더링, 언어 모드별 유효 로드 우선순위. 현재 donor-only 플레이세트를 호환판 검증으로 간주하지 않는다. 게임을 실행하지 않았으며 정상 진행, 저장, DLC 조합, AI, 멀티플레이 결과를 추가로 주장하지 않는다.

원본·Workshop·게임 설치·launcher·사용자 데이터는 수정하지 않았다. 커밋·푸시·게시 없이 이 작업 트리에 변경을 남겼다.
