# 2026-10-20 비전 1950 긴급 특별 건함계획 선택 이식

## 요청 범위와 출처

사용자가 업데이트된 `C:/hoi/hearts_of_korea`를 호환판에 가져오도록 요청했다. 최신 차이는 새 커밋이 아닌 donor `d4031aaa0c1f85bb89b0e6ca21d041beade8bd26` 위의 미커밋 변경이다. 비전 1950 후속 정책·국민정신·그림과 의도적인 기존 보상 강화를 선택 이식한다. 게임 버전 호환성 수리나 전체 donor 복원이 아니다.

- 호환판 시작: `feat/korean-focus-update-20260922@1cb07066bc929489293a21f9418f3d427cfab8a6`, 작업 트리 깨끗함.
- donor: `feat/korean-focus-expansion-ai@d4031aaa0c1f85bb89b0e6ca21d041beade8bd26`, 기존 수정 4개·신규 13개, 총 17파일을 해시로 고정했다.
- 잠금: [hok_shipbuilding_update_lock.json](../../tools/hok_shipbuilding_update_lock.json). 런타임 텍스트 7개·DDS 2개·출처 문서와 원본 PNG 등 8개를 [별도 보관본](../upstream/hok-emergency-shipbuilding-20261020/)으로 남긴다. 신규 README는 donor의 출처 기록으로만 보관하고 호환판 README는 포트 결과에 맞춰 요약했다.
- 이전 source lock과 영어 번역 잠금은 수정하지 않았다. 새 잠금은 역사 JSON의 원래 바이트 및 별도로 계산한 정확한 LF checkout 해시만 허용한다. Git 필터가 바꾸는 줄바꿈과 내용 변경을 구분하며 이전 잠금 검사는 그대로 유지한다.
- 원본·Workshop·게임 설치·launcher·사용자 데이터는 수정하지 않았다. 이번 요청에는 커밋·푸시·Workshop 작업이 포함되지 않는다.

## 현재 설치·실행 기준선

| 항목 | 2026-10-20 확인 |
| --- | --- |
| HOI4 | 설치/최신 로그 `1.19.3.0.c01a`, Steam build `25205862`; 기존 donor 실행 checksum `9278` |
| RT56 | `820260968`, manifest `7553774178744855191`, 업데이트 `2026-10-08T23:58:55Z` |
| OS·사용자 데이터 | Windows 11; `C:/Users/jaewo/OneDrive/문서/Paradox Interactive/Hearts of Iron IV` |
| 실제 활성 playset | `한국test01`: donor → 일반판 영어 번역; `l_korean`, 기존 로그의 DLC 36개 |
| 비활성 대상 playset | `Road to 56 한국 테스트`: 호환판 → RT56 한국어 번역 `2769576030` → RT56; donor 비활성, 일반판 영어 서브모드 제외 |
| descriptor | 호환판 item `3796816200`, RT56 + Korean Language 의존성 유지; donor item `3793992662` |

목록 순서는 launcher 기록이며 엔진의 유효 우선순위 증거가 아니다. 대상 playset의 RT56 한국어 번역은 `replace_path="localisation"`을 선언하고 선언된 Korean Language와 다르므로 최종 언어 계약은 계속 미결정이다. 실제 활성 구성과 새 로그는 donor 실행이다. 이를 이번 호환판의 runtime 검증으로 사용하지 않는다.

외부 `C:/hoi/test/hok-rt56-emergency-shipbuilding-20261020/host-baseline.json`은 descriptor·게임/장비·관련 호스트 파일·언어·DLC·playset·17개 donor 파일의 해시를 기록한다. 최종 재확인에서 donor 17개·RT56 manifest·관련 게임/호스트 내용은 그대로였다. 사용자의 병행 donor 실행으로 로그와 Steam appmanifest 메타데이터 해시는 바뀌었다. 실제 게임을 실행하거나 그 파일을 변경한 것은 이 이식 작업이 아니다.

## 구현과 보존

| 대상 | 분류 | 선택 변경 |
| --- | --- | --- |
| `common/national_focus/korea.txt` | 기존 `OVERRIDE` 유지 | `KOR_vision_1950` 보상에 개별 결정 해금 안내 두 줄 추가. 국민정신·해군 경험치 50·35일·선행 조건·배치·AI·나머지 트리 보존 |
| `common/ideas/korea.txt` | 기존 `OVERRIDE` 유지 | `KOR_vision_1950` 조선소 생산량 `0.2 → 0.3`. 의도적인 upstream 보상 강화이며 기존 ID·그림 유지 |
| `common/decisions/KOR_decision.txt` | 기존 `ADD` 유지 | 기존 비전 1950 분류에 반복 결정 18줄 추가. 기존 함대 목표 1~3단계·시민사회·RT56 지도/만주 병합 보존 |
| 신규 idea·GFX·영/한 현지화 4파일 | `ADD` | 국민정신 1개·sprite 2개·언어당 4키 추가 |
| 신규 DDS 2파일 | `ASSET_COPY` | donor의 결정·국민정신 payload를 바이트 그대로 복사 |

기존 세 파일은 donor 전체를 덮어쓰지 않았다. Git 기준의 원본 hunk 하나씩을 검증한 뒤 기존 호환판 출력에 적용했다. 세 hunk를 역적용하면 `1cb0706`의 정확한 checkout 바이트가 복원된다. 기존 영어 36파일·한국어 36파일은 전부 바이트 단위로 같다. 새 중점·지도 ID·변수·flag·사건·생활주기 hook은 추가하지 않았다. 플레이 가능한 중점 수는 기존 472개다.

`HOK_KOR_enact_emergency_special_shipbuilding`은 `KOR_vision_1950` 완료 뒤 표시·사용 가능하다. 회당 정치력 150, 즉시 180일 국민정신, 적용 중 사용 차단, 무제한 반복, 추가 cooldown 0, AI factor 1을 유지한다. 전쟁·연도·이념·함대 수량 조건은 추가하지 않는다. 분류 전체를 새로 해금한다고 표시하지 않는다.

`HOK_KOR_emergency_special_shipbuilding`은 전투함 선체 5개, 지원함·수리함·수송선의 8개 archetype에 `build_cost_ic = -0.5`, `instant = yes`를 준다. 이는 합산되는 비용 보정이다. 이미 다른 보정이 있는 화면 비용이 항상 정확히 절반이 된다고 약속하지 않는다. 만료 때 기존 영구 비전 1950 국민정신을 제거하는 효과는 없다. 적용 중 재사용 차단과 자연 만료를 별도 flag/반복 일일 스캔 없이 기존 조건과 engine timed idea로 처리한다.

## 문법·충돌·영어·그림

바닐라 `common/ideas/usa.txt:751–788`의 `bureau_of_ships_focus`, `common/decisions/ENG.txt:7205–7235`, `common/national_focus/bulgaria.txt:632`에서 해당 장비 비용 보너스·기간제 반복 결정·해금 툴팁 구문을 확인했다. RT56 `common/ideas/netherlands.txt:1125–1139`, `common/decisions/EGY.txt:274`에도 대응 사례가 있다. 전투함 5개와 수송선은 현재 RT56 장비, 지원함·수리함은 RT56가 교체하지 않는 설치 바닐라 파일에서 archetype을 확인했다.

새 gameplay/localisation/sprite ID는 호환판·RT56·바닐라와 설치된 두 한국어 모드에서 중복이 없었다. 현재 호스트의 같은 상대 경로 충돌 수 73개는 그대로다. 새 6파일은 호스트 경로를 덮지 않는다. 통합 원장은 기존 1,446행의 출처를 보존하고 6행을 추가해 1,452행이며, 기존 3행에는 별도 shipbuilding 출처 열·이전/최종 해시를 붙였다.

donor `l_english`는 한국어 본문이므로 그대로 복사하지 않았다. 신규 4값만 영국 영어로 번역하여 기존 2,743키 위에 더한다. 최종 각 locale은 37파일·2,747키다. 영어 제목은 `Launch the Emergency Special Shipbuilding Programme`와 `Emergency Special Shipbuilding Programme`; 비용·180일·무제한 반복·적용 중 차단·추가 대기 없음·색상·줄바꿈을 보존한다. 한국어는 donor와 바이트 단위로 같고 locale 헤더·BOM·동일 기여자 주석을 유지한다.

그림은 donor에서 기록한 AI 생성 원본을 선택 재사용했다. 이번 포트에서 새 그림을 생성하거나 기존 이미지를 재가공하지 않았다. [원본 크레딧](../upstream/hok-emergency-shipbuilding-20261020/documents/docs/HOK_KOREAN_EMERGENCY_SHIPBUILDING_ASSET_CREDITS.md)과 [원본 manifest](../upstream/hok-emergency-shipbuilding-20261020/documents/docs/data/HOK_KOREAN_EMERGENCY_SHIPBUILDING_ICON_MANIFEST.json)의 제작 도구·프롬프트·기여자·PNG/DDS 해시를 보존한다. 해당 보관본의 게임 관측은 donor의 역사 기록이다.

| 그림 | 포트 payload | 규격·연결 |
| --- | --- | --- |
| 결정 | `gfx/interface/decisions/HOK_KOR/emergency_shipbuilding/emergency_special_shipbuilding.dds` | 32×32 BGRA32·알파; `GFX_HOK_KOR_decision_emergency_special_shipbuilding` |
| 국민정신 | `gfx/interface/ideas/HOK_KOR/emergency_special_shipbuilding.dds` | 60×68 BGRA32·알파; `GFX_idea_HOK_KOR_emergency_special_shipbuilding` |

원본 크기/해시·DDS header·알파·sprite 경로·실제 크기 및 확대 미리보기를 확인했다. 설치 decision UI의 중심 `(30,19)`와 제목 x=63에 32×32 행 아이콘이 들어가는 정적 범위를 확인했다. 이는 RT56 실제 게임의 표시 관측이 아니다. 모든 새 HOK payload는 포트 내부 상대경로로 연결된다.

## 생성과 검증

기존 `source_snapshot.py`와 `build_korean_focus_update.py`에 기존 영어 계층 뒤의 shipbuilding 계층을 추가했다. 기존 검사에서는 정확한 새 출력 해시를 확인한 뒤에만 새 세 hunk를 되돌려 역사 계약을 검사한다. 기존 역사 source lock·그림·영어 계층을 다시 고정하거나 과거 assertion을 삭제하지 않았다. 신규 의미 검사는 독립 ordered AST와 실제 payload를 사용한다. Git 속성은 보관본을 `-text`, 새 잠금을 LF, 각 출력은 실제 생성 LF/CRLF에 맞춰 고정한다.

외부 검증 폴더는 `C:/hoi/test/hok-rt56-emergency-shipbuilding-20261020/`이며 도구는 기존 Codex Python으로 `-B`와 `PYTHONDONTWRITEBYTECODE=1`을 사용했다. 게임·설정·playset을 조작하지 않았고 runtime 진단을 추가하지 않았다.

| 검사 | 실제 결과 |
| --- | --- |
| 생성 | 기존 세 hunk + 신규 6파일만 runtime 변경 |
| 독립 바이트 대조 | 출처 17개·출력 9개 해시 일치, 역적용 세 파일 복원, 기존 locale 36+36 보존 |
| 신규 shipbuilding check/self-test | 통과; 비용·기간·8개 보너스·원래 보상·기존 단계·중첩/반복·그림/영어 등 45개 잘못된 변형 거부 |
| 기존 focus check/self-test | 통과; 22개 변형 거부 |
| 기존 civic check/self-test | 통과; 27개 변형 거부 |
| 기존 royal/prerequisite self-test | 통과; 57개 변형 거부 |
| ID migration `--list` | 통과; 18대상, 새 쓰기 0개 |
| 영어 전체 검사 | 통과; 37파일·2,747키, 기존 255키 제외·새 4키 번역·보호 토큰 유지 |
| manifest 생성 | 통과; 1,452행·기존 호스트 경로 충돌 73개 유지 |
| 전체 second-wave check/self-test | 기존 `descriptor.mod` 보존 assertion에서 중단; 완전 통과 주장 없음 |

최종 `python tools/validate_port.py`는 **20 PASS / 0 WARNING / 5 ERROR**다. source snapshot·건함 의미 검사·생성기·기존 영어·civic·ID migration·통합 원장과 전체 현지화 74파일·5,494키는 통과했다. 실패는 기존 RT56 railway·공용 시스템·동아시아·교리의 소스 핀 불일치 4개와 기존 material-cycle 보존 목록의 `descriptor.mod` 바이트 핀 1개다. 이 작업에서 해당 소스/핀을 고치거나 검사를 느슨하게 하지 않았다. 이번 범위의 정적 검증 통과와 포트 전체의 기존 오류를 구분한다. 전체 결과는 외부 `final-validation.txt`에 보관한다.

`git diff --check`가 통과했으며, 새 잠금의 LF와 실제 생성 runtime의 LF/CRLF 속성도 최종 확인했다. 일회성 출처 수집 스크립트는 검증 뒤 전용 테스트 경로와 생성 기록을 확인하고 삭제했다. 보고서·로그·이미지 미리보기 등 근거는 외부 폴더에 남긴다. 새 보관본 17개는 재현에 필요한 source 입력이다.

원본의 86개 검사나 HOK-only 게임 관측을 포트 결과로 합산하지 않는다. donor의 실제 정책 관측은 마지막 +20%→+30% 변경 전 기록이다. 원본 기록의 과거 +20% 보존 서술과 나중 +30% 변경 서술도 구분한다.

`UNPROVEN`: C0/C1 full restart·실제 UI·정상 선행 중점/35일 완료·해금 안내·정치력 149/150 경계·각 함종 비용·자연 만료/재사용·영구 +30% 표시·진행 중 생산·신규/변경 전 저장·DLC 비활성·AI 장기 반복·멀티플레이. 현재 사용자의 donor 실행은 이 목록을 검증하지 않는다. 필요한 대상 실행에는 donor를 빼고 RT56와 이 포트를 사용해야 하며 최종 언어 조합은 별도 대조가 필요하다.
