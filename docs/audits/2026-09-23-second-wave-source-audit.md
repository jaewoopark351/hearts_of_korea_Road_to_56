# 2026-09-23 HOK 2차 입력·충돌·호스트 보존 감사

상태: **선택 소스·정적 충돌 감사 완료(`CONFIRMED`), 엔진 실행·유효 로드 우선순위 미검증(`UNPROVEN`)**. 게임을 실행하거나 donor·Workshop·게임 설치본·사용자 설정을 수정하지 않았다. 감사는 [이식 계획](../plans/2026-09-23-korean-second-wave-port-plan.md)의 134개 신규 중점과 연결 콘텐츠를 대상으로 한다.

## 입력 고정과 보존 경계

호환판 기준은 `feat/korean-focus-update-20260922@c84fd9faa543a9d2f3aabd8bebe7691984dc6cc3`이며, 기존 `AGENTS.md` 및 문서 변경을 보존했다. 선택 donor는 `be5fb40dbd8de33e5adbf65e808bcb0e8c283560`이다. 이식 전·후 donor HEAD가 같고 작업 트리는 깨끗했다. 원본 중점의 SHA-256은 `1CEDAF78903DB31D15E3837E20069B71BCA8FC674212B1D033F0D721B2B6735C`; 승인한 이전 호환판 중점은 `D33DC929878F3CBB2750164086D9B0120C2DAC2ED45B994C5384A720E8D15C22`다.

[별도 입력 잠금](../../tools/hok_second_wave_lock.json)은 아래 파일 각각의 commit·Git blob·Git 원본 SHA-256·명시적 checkout·실제 입력 SHA-256·크기를 기록한다. 새 snapshot은 `.local-artifacts/sources/hok-second-wave-be5fb40`에만 생성한다.

| 입력 묶음 | 수량 | 처리 |
|---|---:|---|
| runtime 텍스트 | 58 | 기존 `korea.txt` 1개 + 지원 텍스트 41개 + GFX 16개 |
| HOK DDS | 231 | 원본 bytes 보존, 재압축·재색칠 없음 |
| 출처·명세 문서 | 37 | [원본 문서 보존본](../upstream/hok-second-wave-be5fb40/README.md)에 byte-exact export |
| 합계 | 326 | 허용 목록 이외 파일을 cache에 받아들이지 않음 |

신규 runtime 288개는 이식 전에 호환판에 없었다. 기존 중점 파일만 승인한 이전 출력 해시를 기록한다. 전체 donor base·기존 20개 한국 overlay·초기 60/29 이미지 입력을 새 donor로 교체하지 않았다. 해당 역사 lock 해시는 계속 다음과 같다.

- `tools/hok_source_lock.json`: `436B730E92D58A33FBBBB913E064C3A0D6A904D069F61D8CDBE38DCCB28FC94B`
- `tools/hok_icon_lock.json`: `DBB2A37CAE0DB55171C393CDFDA3F24E9B09B65CEF224E81593310A9620C59A3`
- `tools/hok_second_wave_lock.json`: `FCBF178914F5D88894A3CDFB686E45D7E63DFFA6081113B58E0D415D152DE48D`
- 326개 source 경로 목록 SHA-256: `08CCAD1FD3C67200B3E4C63EE3FF33EE6CB570240B095DECC8E083A0FD64C18E`

## 검사한 공급자와 지문

`<STEAM>`은 `C:/Program Files (x86)/Steam/steamapps`다. 아래 경로는 실제 읽은 물리 경로이며, 표의 순서는 유효 로드 우선순위가 아니다. 두 번역 모드는 충돌 후보로 각각 조사했으며 동시 활성 구성을 승인하거나 지원한다고 결론 내리지 않는다.

| 공급자 | 실제 경로 | 해당 데이터베이스 검사 파일 수 | 신규 288개 경로 충돌 |
|---|---|---:|---:|
| 호환판 | `C:/hoi/hearts_of_korea_Road_to_56` | 78 | 0 |
| donor | `C:/hoi/hearts_of_korea` | 140 | 288개 원본 자신 |
| RT56 | `<STEAM>/workshop/content/394360/820260968` | 1,101 | 0 |
| vanilla | `<STEAM>/common/Hearts of Iron IV` | 1,028 | 0 |
| Korean Language | `<STEAM>/workshop/content/394360/2743487021` | 196 | 0 |
| RT56 Korean Translation | `<STEAM>/workshop/content/394360/2769576030` | 306 | 0 |

descriptor SHA-256:

| 공급자 | SHA-256 |
|---|---|
| 호환판 | `AA150D6CE82A7779C3D4C3FCDC962A82FA269327F005330B565723CA87BBE247` |
| donor | `3FBC6868A7D95BACD6B55AF71593A61AF3A7EADA5654D46CC4C828422ECA032A` |
| RT56 | `5B323861ABD63E31CB896277E3EA58BA4BCD9FCEEDA957B50792065E42E03F61` |
| Korean Language | `F5813D345DD0FC01E80F68B65901B1D060A238336D3D2A89EAA8404A40329346` |
| RT56 Korean Translation | `A0508F4A91AF911917AD3A84BF829CB38ED1557DD8F9643A010F1AEE36F48D6C` |

RT56 Workshop manifest는 이식 전·후 `7475007536894105204`, `timeupdated=1788822864`였다. 설치 및 최신 manifest 기록이 모두 같은 값이었다. 신규 경로와 별개인 기존 `common/national_focus/korea.txt`는 의도적인 `OVERRIDE`를 유지하며 RT56 원본 SHA-256은 `A80FBC767C21902FC56EBBCA35DC3C120700E527B52EA98F3CFDF5221EB0EF90`이다. 비교한 외부 텍스트 **2,771개**와 존재하는 외부 descriptor를 빌드 후 다시 해시 비교했고 변경은 0개였다. 지역 대응에 사용하는 별도 vanilla·RT56 주 파일 및 지도 지문 검사도 통과했다.

## 논리 ID 감사

선택한 입력에서 선언 ID를 추출하고 해당 데이터베이스의 실제 파일 선언과 대조했다. 현지화는 English/Korean 채널을 구분하고, 결정 파일 바깥 범주 블록을 사업 정의로 중복 집계하지 않았다. 경로 비교는 파일 시스템에서 열거한 실제 대소문자와 함께 조사했다.

| 새 정의 종류 | 선택 개수 | 선택 묶음 내부 중복 | 예상 donor 위치 이외 충돌 |
|---|---:|---:|---:|
| 중점 | 134 | 0 | 0 |
| 국민정신 | 63 | 0 | 0 |
| 기간제 결정 | 18 | 0 | 0 |
| 결정 범주 | 4 | 0 | 0 |
| 주 동적 변동치 | 12 | 0 | 0 |
| sprite | 365 | 0 | 0 |
| English 현지화 키 | 479 | 0 | 0 |
| Korean 현지화 키 | 479 | 0 | 0 |

365개 sprite는 그림 231개와 중점 광택 134개를 구분한 값이다. 두 언어의 같은 키는 의도적인 언어별 대응이며 중복 오류가 아니다. 기존 326개 중점의 보상·배치·조건 보존은 이 신규 ID 충돌 감사와 별도의 의미 검사다.

## 공유 광택과 pruning

새 GFX에서 donor의 `gfx/interface/goals/HOK_KOR/shine_overlay.dds`를 복사하지 않는다. 생성기는 이 참조를 기존 공유 경로 `gfx/interface/goals/shine_overlay.dds`로 바꾸며 HOK-owned 그림과 마스크는 로컬에 둔다. 위 6개 공급자에서 공유 상대경로의 실제 파일을 확인한 결과 vanilla만 공급했다. SHA-256은 `BB416649358C73D34AACD46BAD61BC44211FAC8111627B56E25F385AD98F4448`이다.

`effectFile = "gfx/FX/buttonstate.lua"`는 설치 vanilla의 `interface/goals_shine.gfx`에도 사용되는 효과 식별자다. 같은 이름의 물리 `.lua` 파일 존재를 요구하지 않는다. 참고 vanilla `goals_shine.gfx` SHA-256은 `AAC48B27BB8ADADBBEF4AF5D3412C6FA8EF3A717E4165ACDE64E6668CFAE1EF0`, 설치 `gfx/FX/buttonstate.shader` SHA-256은 `1EDDB371702289F4CC9D9D565AEF21CF77C9261BD4324194295EEEA6309F413A`다. 실제 광택 렌더링은 게임에서 확인하지 않았다.

기존 [Korea-only pruning](../../tools/prune_non_korean_content.py)은 명시적 파일·sprite 목록만 처리한다. 신규 288개 경로와 해당 도구의 삭제·생성 대상 교집합은 **0**, 신규 365개 sprite와 삭제 ID 교집합도 **0**이다. 이번 신규 묶음을 보존하기 위해 기존 제거 범위를 넓히거나 축소할 필요가 없었다. 이 검사는 생성 결과를 메모리에서 읽고 비교했으며 pruning 적용·파일 삭제는 하지 않았다.

## 구현 교차 검토와 증거 한계

빌더·통합 원장·지역 변환을 교차 검토하면서 `.txt` 분기 안에서만 지역 변환을 호출하여 한영 `.yml` 설명 변환이 실행되지 않는 결함을 발견했다. 담당자가 호출을 분기 밖으로 옮기고 두 파일을 다시 생성했다. 이 감사 문서는 발견한 결함을 미해결 상태로 남겨두었다는 뜻이 아니며 최종 산출물 검사는 별도 aggregate 결과를 따른다.

세부 ID 위치와 검사한 모든 파일 해시는 로컬 근거 `.local-artifacts/second-wave/pre-import-collision-audit.json`에 보존했다(SHA-256 `1092B97838326E5056D7080949961335F0E3AD08E2D79BC1C2A7A4357B56DFC2`). 빌드 후 외부 해시 재확인·pruning 교집합 결과는 `.local-artifacts/second-wave/post-build-source-recheck.json`에 있다(SHA-256 `6E94779595E08FD9B0C990766C813DD8593CA5B95C0D9134FA41AA1D70BB2913`). 원시 사용자 설정·로그·계정 정보는 이 문서에 포함하지 않는다.

검사 범위는 선택한 논리 데이터베이스의 물리 `.txt`·`.gfx`·English/Korean `.yml` 파일이다. 모든 모드·DLC 압축 자산·엔진 내부 등록·새로 추가될 호스트 파일까지 전수 보장하지 않는다. snapshot 지문과 소스 수준 충돌 없음은 엔진 등록 성공, UI, 효과 scope, 정상 중점 진행, 결정 수명, AI, DLC, 저장 및 멀티플레이 검증을 대신하지 않는다. 현재 사용자 혼합 playset에서 이 호환판의 정상 실행을 증명했다고 하지 않는다.
