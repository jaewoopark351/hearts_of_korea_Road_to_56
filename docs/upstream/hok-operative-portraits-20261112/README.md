# 2026-11-12 한국 신규 첩보원 초상화 선택 입력

한국 첩보원 그림·목록·소스 잠금을 수정·재생성·검증하기 전에 이 안내, [로컬 첩보원 통합 기록](../../implementation/2026-11-12-korean-operative-portrait-port.md), [소스 manifest](source-manifest.json), 기존 [과학자·이름 통합 기록](../../implementation/2026-11-12-korean-scientist-update-port.md)과 [개발 자료 안내](../../HOK_DEVELOPMENT_ARTIFACT_ARCHIVE.md)를 읽는다. 이름·고정 인물 표시·공유 소비자를 다루면 [변경 영향 절차](../../HOK_CHANGE_COVERAGE_REVIEW.md)와 [현지화 검토 스킬](../../skills/hok-rt56-localisation-review/SKILL.md)을 함께 따른다. 이 capsule은 최신 첩보원 그림과 출처·선조 입력을 유지한다.

| 위치 | 원본·사본·활성 입력의 역할 |
|---|---|
| `C:/hoi/hearts_of_korea/` | 읽기 전용 donor 원본. `feat/korean-focus-expansion-ai@f1282d701bc47e47c119ca31faa6082e9e6ed1e6` 위 미커밋 첩보원 목록·GFX·DDS8개와 관련 문서를 선택했다. |
| `source/<원본 상대 경로>` | 한국 초상화 목록1개·전용 GFX1개·DDS8개, 총10개의 정확한 donor 사본. 현재 검은 중절모·정장·코트와 불투명 회색 배경 revision을 동결한다. |
| `documents/<원본 상대 경로>` | donor AGENTS·첩보원 계획·자산 manifest·최초 구현/후속 복장·배경 기록2개, 총5개 문서의 정확한 사본. 두 제작 단계와 각 실행 조건의 이력을 유지한다. |
| `compat_before/portraits/00_portraits_KOR.txt` | 호환판 `7e29ce80158dfad1635d427f61e5c8b964088adf`의 기존 과학자 포함 한국 목록.1,051바이트·SHA `5E13A8CED8ECEDD70DE77614739C6C2315D98498DE16471ED8BF6363CC2746CC`인 정확한 선조 입력이다. |
| [source-manifest.json](source-manifest.json) | 원본/사본의 역할·SHA·크기·실제 줄바꿈·DDS 규격, donor dirty 상태와 호환판 기준을 고정한다. source10·documents5·선조1개는 복사 전후 원본과 사본 해시가 일치했다. |
| manifest의 `prior_scientist_contract` | 기존 `tools/hok_scientist_update_lock.json` v2의 지문과 실제11출력 지문. 기존 이름·과학자 입력과 출력을 보존하며 현재 소유 계층을20출력으로 확장하는 기준이다. |
| manifest의 `references` | 설치된 RT56 초상화 registry·현지 모집, 바닐라 DLC schema/GFX·생성 효과·현지 모집과 UI 배경, 호환판 고정 첩보원 연결의 읽기 전용 경로·SHA·크기16개다. source 사본과 구분한다. |
| `C:/hoi/test/hok-rt56-operative-update-20261112-01/` | 이번 호환판의 새 baseline·백업·진단·검증 결과 위치. 최초 source/문서 캡처를 기존 게임 실행의 증거로 사용하지 않는다. |
| `C:/hoi/test/hok-operative-portraits-20261112-01/art/generated/` | donor 최초 AI 생성 인물의 외부 원본 보존 위치. 현재 이미지 편집의 얼굴·인물 참조 입력이다. |
| `C:/hoi/test/hok-operative-outfit-background-20261112-01/art/` | donor 후속 편집의 선택 PNG·프롬프트·변환·검수 기록의 기존 보존 위치. 현재 복장·불투명 배경 DDS의 출처다. |
| `C:/hoi/test/hok-rt56-source-cache/sources/` | 별도의 역사적 활성 입력 캐시. 이번 capsule을 추가해 기존 고정 입력과 지문을 보존한다. |

채택하는 그림은 남녀 각4명의 가상 한국 첩보원이다. donor가 처음 생성한 얼굴을 `image_gen.imagegen` 편집 입력으로 사용해 검은 중절모·정장·코트, 흰 셔츠·검은 넥타이와 불투명 회색 그라데이션 배경을 적용했다. 자산 manifest의 현재 revision은 `2026-11-12-outfit-and-opaque-background`이며 모델명은 도구에 노출되지 않았다. 초기 투명 배경 그림과 초기 실행 기록은 보관된 이전 단계로 읽는다. 이번 호환판은 최신 DDS를 정확한 바이트로 재사용한다.

실제 DDS8개는 모두156×210·uncompressed BGRA32·131,168바이트·mipmap 헤더0이며 알파 최솟값/최댓값이255다. 현재 donor manifest와8개 해시가 일치한다. 기존 과학자 DDS의 mipmap 헤더1·투명 배경과 다른 자산 계약이므로 첩보원 규격을 따로 유지한다. source GFX는 BOM 없는 UTF-8·CRLF35개·EOF 개행 있음, 한국 목록은 BOM 없는 UTF-8·CRLF55개·EOF 개행 없음이다. 선조 한국 목록은 CRLF39개·EOF 개행 없음이다.

변경 runtime은 기존 한국 목록1개에 `operative.female`·`operative.male`의 각4개 sprite를 추가하고 전용 GFX1개·DDS8개를 더하는10출력이다. 기존 이름·과학자 계층11출력 중 같은 한국 목록을 확장해 소유 출력은20개가 된다. 이름의 최종 로마자56/11/14항목, 고정 과학자, 육군·해군 목록은 기존 계약을 유지한다. donor의 최신 커밋에 포함된 과학자 GFX·DDS8개와 최종 이름 파일은 이전 선택 capsule과 일치한다.

윤봉길·이봉창은 기존 `history/countries/KOR - Korea.txt`의 La Resistance 조건과 개별 GFX·국적·특성·모집 설정을 유지한다. RT56의 외국 현지 모집은8개 생성 지점의 `nationalities = { FROM.OWNER }`·`portrait_tag_override = FROM.OWNER`를 기준으로 보존한다. 한국 소유 목록을 추가하며 공용 아시아 풀과 일반 타국 정의를 교체하지 않는다. 실제 선택과 cosmetic tag 상속은 source 확인·현재 RT56 실행 확인을 각각 기록한다.

donor 최초 구현에서는 정상 모집/채용·임시 저장 재시작 재로드·13개 cosmetic tag와 외국 기준 강제 생성 표본·애니 조합의 일부 화면을 기록했다. 최신 복장·배경 revision은 본체의 기존 저장·후보 UI에서8종을 확인했으며 새 저장은 시도하지 않았다. 현재 revision 애니 조합·자연 정치 경로·외국 현지 모집 결정·장기 진행·멀티플레이는 미검증이다. 최초 저장 rename 실패와 후속 기존 진단 저장의 함대 경고는 해당 donor 기록에 남아 있다. 이 이력은 새 RT56 이식의 실제 실행 결과와 구분한다.

정확한 프롬프트·선택 원본·이전/현재 그림 대응·SHA와 donor 실행 조건은 [자산 manifest](documents/docs/data/HOK_KOREAN_OPERATIVE_PORTRAIT_ASSET_MANIFEST.json), [최초 구현 기록](documents/docs/incidents/2026-11-12-korean-operative-portraits.md), [현재 복장·배경 기록](documents/docs/incidents/2026-11-12-korean-operative-outfit-background.md)을 따른다. 이 capsule에 진단 helper·로그·미리보기·임시 저장을 추가하지 않는다. 공개 배포 자료와 크레딧 선택은 별도 release allowlist를 따른다.

보관 AGENTS에는 donor `f1282d7`에 커밋된 역사적 이름 지침7줄과 그 위 미커밋 첩보원 조건부 읽기1행이 함께 있다. 호환판의 활성 지침은 [AGENTS.md](../../../AGENTS.md)에서 로컬 통합 기록을 가리키며 HOK 소유와 승인 범위에 맞춘다. 현재 이름81항목의 선택을 유지하고 근거·실명 중복 기록을 담은 보관 문서는 provenance로 보존한다.
