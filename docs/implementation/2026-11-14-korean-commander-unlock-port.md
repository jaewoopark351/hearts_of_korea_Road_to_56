# 2026-11-14 한국 지휘관 해금 이관 선택 이식

상태: **5출력 구현 반영·독립 소스138/0·소유 계약76/0 / 전체 정적9 PASS·0 WARNING·기존85 ERROR / 실제 RT56 UI·지휘·저장 검증 대기**. 원본 업데이트를 호환판에 반영하라는 요청으로 HOK의 지휘관 해금 변경을 선택한다. 이 계층을 검토·수정·재생성·검증하기 전에 이 기록과 [선택 입력 안내](../upstream/hok-commander-unlock-20261114/README.md), [현지화 검토 스킬](../skills/hok-rt56-localisation-review/SKILL.md), [변경 영향 절차](../HOK_CHANGE_COVERAGE_REVIEW.md)를 읽는다. 이전 초상화·고정 인물 참조와 연결된 검사를 수정할 때에는 [과학자 통합 기록](2026-11-12-korean-scientist-update-port.md)과 [첩보원 통합 기록](2026-11-12-korean-operative-portrait-port.md)도 따른다.

## 범위와 기준

이번 요청은 원본의 최신 구현 반영이다. donor 전체 복사, RT56/엔진 전체 재기준화, 지도·그림·이름·의존성·사용자 설정 변경, 게임 실행·저장 이관, 정리·패키징·커밋·푸시·업로드는 수행하지 않는다. 기존 생성 경로를 확장하며 과거 source pins와 입력을 보존한다.

| 항목 | 이번 작업의 관측·역할 |
|---|---|
| 호환판 | `C:/hoi/hearts_of_korea_Road_to_56`, `feat/korean-focus-update-20260922@b5308a027385cc021243a443ff49b728707e081e`, 시작 시 clean |
| 읽기 전용 HOK 원본 | `C:/hoi/hearts_of_korea`, `0c19f58fa7a9ff898196dcdbe46edfd0ad5fdbbc`, 시작 시 clean |
| 비교 선조 | `065b5550448d6415901456503ef28b27f4530cc1`. 직전 첩보원 업데이트 이후 변경은 runtime5개·문서3개이며 이전 이름/그림을 다시 반영하지 않음 |
| 설치 게임 | `Operation Postern v1.19.5.0.7c6c (c184)`, 설치 `launcher-settings.json`의 값. 이번 호환판 실행 체크섬을 뜻하지 않음 |
| RT56 | 읽기 전용 Workshop820260968, manifest `1963361040482473746`; 관련 common/characters·national_focus·on_actions·history/countries·localisation 지문1,260개 기록 |
| 사용자 경로·선택 | `C:/Users/jaewo/OneDrive/문서/Paradox Interactive/Hearts of Iron IV`. 배열은 원본 HOK → HOK anime → Anime History(`1862018480`), 언어 `l_korean`, `disabled_dlcs=[]`. Korean Language는 descriptor의 선언과 현재 선택 배열을 구분함 |
| 실행 범위 한계 | 현재 선택은 RT56 호환판 대조 구성이 아니다. 배열을 유효 로드 우선순위나 이번 실행의 증거로 사용하지 않고 설정을 바꾸지 않음 |
| 새 외부 시험·백업·증거 | `C:/hoi/test/20261114-commander-unlock-port/`; `baseline.json`은 변경 전1,515runtime·donor1,861·기존capsule·도구·참조·사용자 metadata·cache 지문 |
| 과거 활성 source cache | `C:/hoi/test/hok-rt56-source-cache/sources/`,1,490개 유지 입력. 이번 시험 출력이나 새 capsule의 대체물이 아님 |

## 채택한 동작과 변경 영향 대장

기대 조건은 각 군사 역할에서 `중점 완료 OR (일반 국뽕 전역 표식 있음 AND 새 국가 표식 없음)`이다. 국가 역사는 새 게임에만 `HOK_KOR_commander_focus_unlock_v1`을 설정한다. 기존 저장에 표식을 소급 주입하거나 인물을 재생성하지 않는다. 새 기본·중견국·일반 국뽕 게임은 모두 대상 중점을 완료해야 하며, 새 표식이 없는 기존 일반 국뽕 저장은 이전 지휘관 접근을 유지하도록 하는 원본 의도를 채택한다. 이것은 소스 계약이며 현재 호환판의 실제 저장 호환 보증은 아니다.

이 보호 조건은 호환판의 기존 지도 ID 이관·주 분할과 새 게임 한정 조건을 대체하지 않는다. 일반 HOK 저장을 RT56 호환판 저장으로 변환하거나 지원한다는 뜻도 아니다.

| 기능·ID/키와 소비자 | 처리·기대 의미 | 근거·확인 한계 |
|---|---|---|
| `KOR_Beomdo_Hong.field_marshal.visible` | **수정**: 중점 또는 기존 국뽕 저장 보호 조건 | 원본 최종 `0c19f58`의 역할 한 블록만 선택. 능력·특성·초상화·ID 유지 |
| `KOR_Jwajin_Kim.corps_commander.visible`, `KOR_Junggeun_Ahn.corps_commander.visible` | **수정**: 같은 조건 | 다른 역할·개인 상태를 재설정하지 않음 |
| 한국 국가 역사 시작부 | **수정**: 새 국가 표식 한 개 | 국가 scope에서 기존 CNDP 표식 뒤에 추가. 세 인물의 기존 `recruit_character`와 고정 과학자·첩보원 모집 유지 |
| `KOR_prepare_for_the_next_war.completion_reward` | **수정**: 세 `show_unit_leaders_tooltip` 추가 | 국민정신·홍범도 정치고문 안내 유지. 툴팁 자체를 실제 역할 해금 효과로 간주하지 않음 |
| 같은 중점의 기간·선행·배치·아이콘·AI·후속 연결 | **의도적 유지** | `cost=5`, 자유당/독립당 OR 선행, AI1 유지. 좌표·게임플레이 추가 변경 없음 |
| 홍범도 정치고문·`beomdo_hong`·`KOR_minister_of_defense` | **의도적 유지**: 기존 중점 완료 조건으로 고용 가능 | 무료/자동 임명·새 보직 없음. 원수와 실제 동시 사용은 별도 실행 필요 |
| `GOOKPPONG_ENABLED_TEXT_DESC`, Korean/English | **수정**: 세 지휘관을 시작부터 가진다는 안내 제거 | 양 채널1키씩. 기존 다른 시작 강화 문구·색상/치환/줄바꿈 토큰과 영어 역할 유지 |
| 중점 이름·서사, 인물 이름·GFX·고정 초상화 | **의도적 유지** | 기존 이름과 엔진 역할 툴팁 재사용. 새 이름·그림·전역 표시 키 없음 |
| `kor_hok_gookppong_enabled_flag`의 연구 슬롯 bypass2개·특수부대 보상2개 | **의도적 유지** | 이번 중점에서 전역 플래그를 설정·삭제하지 않음 |
| `hok_game_rules.txt`, 일반/중견국 시작 on_action | **의도적 유지** | 일반/중견국 표식·영토·기술·공장·병력·장비의 기존 처리 유지 |
| 다른 정치 경로·완료 후 정부 변경 | **의도적 유지** | 미완료 대체 해금 수단을 추가하지 않으며 완료 뒤 현 정부를 새 회수 조건으로 사용하지 않음 |
| RT56 shared/world·지도·이전 과학자/첩보원·이름·애니 | **제외** | 새 upstream delta 밖. RT56/RTK에서 대상 ID·새 flag·중점·시작 설명 키 중복은 검색 범위에서 발견하지 못함. 애니 조합 유효 정의는 미확인 |
| 실제 UI·부대 지휘·정상 선행 정치 진행·고문 동시 역할·시간 경과·기존/신규 저장 | **미확인** | RT56+호환판 cold run과 저장별 관측 필요. 정적 진리표를 실제 엔진 평가로 보고하지 않음 |

국가 표식은 역사 초기화와 군사 `visible` 조건만을 위한 내부 저장 구분이다. 새 플레이어 표시 키를 만들지 않고, 공개 해금 안내는 중점의 기존 이름·역할 툴팁을 사용한다. 새 표시 경로와 실제 한영 화면·국뽕 설명의 활성 번역 우선순위는 별도 실행 검증 대상이다.

## 원본 근거와 생성 소유권

원본은 단순 focus-only 조건에서 기존 국뽕 저장을 불러와 시간이 지난 뒤 지휘관 비표시·군 지휘 해제를 재현했고, 이후 최종 legacy guard를 추가했다. 따라서 초기 조건만 이식하지 않고 최종 다섯 파일을 선택한다. 원본의 초기 세 설정 중점 완료·지휘/고문 관측과 최종 조건에서의 기존 저장150시간·새 국뽕106시간은 donor 구성의 이력이다. 최종 조건의 세 설정 완료 전 과정은 donor도 다시 실행하지 않았으므로 이번 포트 검증으로 계산하지 않는다. [동결할 원본 기록](../upstream/hok-commander-unlock-20261114/documents/docs/incidents/2026-11-14-korean-commander-unlock-transfer.md)

기존 소유자는 character의 `build_shared_overrides.py`, focus의 `build_korean_focus_update.py`, 국가 역사의 content/CNDP/doctrine 계층, 시작 안내의 `prune_non_korean_content.py`다. 후속 선택 계층은 [명시적 생성 모듈](../../tools/upstream_commanders.py)과 독립 잠금·capsule로 관리하며, 출력만 손으로 수정하거나 기존 캐시/잠금을 갱신하지 않는다. 역사 검사에는 정확한 최종 바이트일 때만 직전 바이트로 역투영하는 계약을 적용한다. 고정 첩보원 참조의 국가 역사 해시도 기존 선조를 보존한 같은 방식으로 대조한다.

분류는 기존 한국 character·focus의 `THREE_WAY_MERGE`, country history의 `OVERRIDE`, 시작 현지화 두 파일의 `ADD`를 유지한다. RT56의 동명 파일 전체를 donor 파일로 교체하지 않으며 대상 정의 밖의 이전 병합 바이트를 보존한다. 원장에서는 다중 출력인 character행의 KOR 해시만 바꾸고 MAN·host-reference 구성요소와 과거 provenance를 유지한다. 전체 원장 생성 성공 여부와 선택 행 갱신의 성공은 구분한다.

선택 capsule은20파일이다. donor 변경 전 Git blob5개·현재 checkout5개·호환판 선조5개·donor 문서3개·manifest·안내로 구성한다. 변경 전 Git 바이트와 실제 checkout의 CRLF를 구분하며 Git 속성 `-text`로 보존한다. 설치 참조9개는 RT56 3개·바닐라6개다. 원본/사본 역할과 원본 절대 경로·SHA·크기는 manifest, 출력5개의 이전/최종 지문은 [독립 잠금](../../tools/hok_commander_unlock_lock.json)에 있다. 기존803개 capsule 입력과 활성 source cache를 대체하지 않는다.

검토 중 이전 정상 출력에서 새 출력을 적용할 때 세 옛 writer의 별도 raw 해시 목록이 이를 거부하는 것을 격리 fixture에서 재현했다. focus builder preflight, content CLI의 한국 역사, state-split CLI의 한국 중점에 이번 잠금의 정확한 `previous_sha256`만 추가했다. 공통 commander preflight는 유지하며 임의 변경은 계속 거부한다. 기존 핀을 우회하지 않고 이 전환 수용 분기만 시험했으므로 역사적 생성기 전체가 현재 설치에서 성공한 것으로 기록하지 않는다.

## 검증 기록과 남은 범위

수정 전 `python -B tools/validate_port.py`는 exit1, **8 PASS / 0 WARNING / 85 ERROR**였다. 이전11월12일의26/0/16을 현재 결과로 사용하지 않는다. 현재 설치 게임1.19.5, RTK Workshop snapshot 변경, 역사적 vanilla/host 입력 차이와 기존 descriptor·원장 충돌 분류가 검사 실패를 만든다. RTK 계약 검사가 먼저 실패해 기존 장비 override의 중복 키들이 허용 계약을 확인받지 못한 보고도 포함한다. 숫자85를 독립적인 새 gameplay 결함85개로 해석하지 않는다. 이번 지휘관 delta의 수리 범위와 전체 엔진/호스트 재기준화는 구분한다.

| 확인 단계 | 실제 결과·외부 증거 |
|---|---|
| 독립 소스·조건·표시 계약 | `independent-qa.json`: **138 PASS / 0 FAIL**. 별도 ordered AST와 군사 조건48조합, 정치고문·모집·중점/다른 국뽕 소비자 보존, 다섯 출력의 정확한 역적용, 한영 의미·BOM·토큰과 설치 schema/예제·host ID 검색을 확인 |
| 선택 생성기·소유 계약 | `commander-owner-contracts.json`: **76 PASS / 0 FAIL**. 다섯 출력의 최종화·역투영·멱등성·미등록 수정/경로/별칭 거부, 도구10개의 메모리 구문 검사, 원장 재생/보존. 최초 `--apply`는5 written, 이후 `--check`·`--apply`·`--check`는0 written |
| 옛 writer의 정확한 이전 출력 수용 | `focus-preflight-transition-after.json`:3/3, `legacy-writer-admission-after.json`:6/6. 정상 이전/최종은 허용하고 임의 변경은 거부. `*-before.json`에 초기 거부를 보존. 외부 fixture이며 production source gate 성공을 뜻하지 않음 |
| 원장 독립 대조 | `ledger-independent-qa.json`:1,577행 유지, 대상5행의 `output_sha256`·`reason`만 변경. 다른 원시 행·기존 분류·출처와 character행 MAN/RT56 참조 해시 유지. 전체 원장 생성은 기존 `.gitignore` 충돌 등에서 차단됨 |
| 전체 정적 사후 | `static-after.txt`:exit1, **9 PASS / 0 WARNING / 기존85 ERROR**. `aggregate-comparison.json`:오류 원인 집합 동일·신규 원인0, 새 commander raw gate1개 통과. 원장 소스 traceback 한 곳의1265→1268행 이동은 원래 문장과 원인을 유지한 위치 차이로 별도 기록 |
| 런타임·원본·기존 입력 보존 | `preservation-after.json`:runtime1,515개 중 선택5개만 변경, 추가/삭제0. donor1,861·이전capsule803·cache1,490·host1,260과 감시한 설치 참조/사용자 metadata·descriptor 지문 유지. Git HEAD/브랜치 유지 |
| 실제 UI·정상 정치 진행·해금/지휘·고문 동시 사용·신규/기존 저장 | **미실행·미검증**. 현재 선택은 원본+애니 조합이며 호환판 대조 구성으로 전환하지 않음. donor 실행과 정적 진리표를 현재 RT56 엔진 결과로 합산하지 않음 |

최초 보존 비교는 ACF의 `timetouched`만 `1794591861`→`1794594820`으로 바뀐 것을 검출해 `preservation-first-acf-timetouched.json`에 pass=false로 남겼다. 현재/최신 RT56 manifest·업데이트 시각·크기와 감시한 host 파일 해시는 같다. 최종 보고서는 전체 ACF entry 동일성은 false로 유지하고 해당 접촉 시각을 별도 bookkeeping 차이로 기록하며 snapshot 동일성을 따로 검사한다. 이 작업 도구가 Steam ACF에 쓴 것은 아니며 변경 주체는 확인하지 않았다. 전체 ACF 바이트가 보존됐다고 주장하지 않는다.

`baseline.json`, `static-before.txt`·`static-after.txt`, 독립/소유 계약·전환 fixture·원장·보존 보고서와 helper는 모두 위 외부 작업 경로에 있다. 최종 변경의 `git diff --check`가 통과했다. 이전 도구3개에 보이는 Git LF→CRLF 안내는 원래 LF checkout 형식과 기존 속성의 조합이며 이번 수정에서 전체 줄 끝을 바꾸지 않았다. 실제 UI·해금/지휘·시간 경과와 기존 저장 재로드는 이 소스 이식의 정적 확인과 별도 미완료로 남긴다.

최초 전체 결과 비교 helper는 PowerShell이 만든 UTF-16LE 보고서를 UTF-8로 가정해 해독 전에 실패했다. 원래 보고서를 보존하고 BOM 판별만 수정했으며 validator를 다시 실행하거나 결과를 바꾸지 않았다. `aggregate-comparison-initial-encoding.json`은 최초 실패와 정정 근거를, 최종 비교 보고서는 실제 입력 인코딩과 원시/행 번호 정규화 차이를 함께 남긴다.

기존 정리 미결은 `tools/__pycache__/`21파일·1,088,888바이트다. `.local-artifacts`는 발견하지 못했다. 기존 파일을 이동·삭제하지 않고 새 helper·백업·진단 보고서는 위 외부 작업 폴더에 둔다. source capsule은 유지 생성 입력이며 테스트 출력과 구별한다. donor·Workshop·설치 게임·사용자 데이터·과거 cache와 Git HEAD를 보존하고 커밋·푸시·게시·업로드는 수행하지 않는다.
