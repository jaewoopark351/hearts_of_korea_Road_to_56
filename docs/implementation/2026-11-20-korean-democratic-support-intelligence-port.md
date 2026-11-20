# 2026년 11월 20일 민주인사 지원과 산둥 정부 선택 이식

상태: **런타임28출력·지침/스킬·다크 구조도 구현 반영 · 선택 소스/UI/효과/새 저장 검증 기록 · 임시 설정 복원·기존175저장 보존 확인**. 전체 정적86오류와 실패한 자동 진단, 별도 수동 증거 및 미검증 범위를 아래에서 구분한다. 원본 콘텐츠와 AGENTS·스킬·구조 문서·다크 그림 체계를 함께 구현하라는 후속 요청에 따른다. [최초 콘텐츠 계획](../plans/2026-11-19-korean-democratic-support-intelligence-port-plan.md)과 구조도 도입 계획의 문서화 전용 상태는 이전 단계의 기록이다.

이 계층을 수정·재생성·검증하기 전에 이 문서, [원본 입력 안내](../upstream/hok-democratic-support-20261120/README.md), [지리 대응 기록](2026-11-20-chinese-government-state-mapping.md), [현지화 스킬](../skills/hok-rt56-localisation-review/SKILL.md), [변경 영향 절차](../HOK_CHANGE_COVERAGE_REVIEW.md)를 읽는다. 구조·호출·scope·표시·지도 관계를 바꿀 때는 구조 목차, 유지 안내와 다이어그램 스킬을 함께 읽는다. 실제 문서 그림의 확인 범위는 별도 도입 기록을 따른다.

## 승인 범위와 기준선

사용자는 콘텐츠 이식과 지침·다이어그램 체계의 전체 구현을 요청했다. HOK donor·RT56·설치 게임은 읽기 전용으로 유지하고 기존 한국 지도·이전 캐릭터/이름·RT56 일반 세계 콘텐츠를 보존한다. 커밋·푸시·패키징·Workshop 게시·업로드는 포함하지 않는다. 실제 사용자 프로필 임시 변경은 AGENTS의 별도 승인 경계에 따라 외부 준비와 실제 적용을 구분한다.

| 항목 | 기준과 역할 |
|---|---|
| 호환판 | `C:\hoi\hearts_of_korea_Road_to_56`, `feat/korean-focus-update-20260922@9a01955785bcdd827c9c85522537a0bfc57ed654` |
| 시작 시 기존 변경 | `docs/README.md`와 두 이식/도입 계획의 앞선 문서화 변경을 보존했다. 작업 시작을 clean으로 기술하지 않는다. |
| 원본 HOK | 읽기 전용 `C:\hoi\hearts_of_korea`, `f180bc8089e2a17f310b1fafa091d3f152063df3`, 선택 콘텐츠 커밋 `f2356e2a2c6db9048e18a4dde41454865f10742a` |
| 마지막 반영 원본 | `0c19f58fa7a9ff898196dcdbe46edfd0ad5fdbbc`. 이후 runtime28경로의 delta를 선택했다. |
| 게임 | 설치 메타데이터 `Operation Postern v1.20.0.0.8873 (0c4f)`. 새 선택 계층의 입력 기준이며 실제 게임 체크섬이나 전체1.20 호환 확인이 아니다. |
| RT56 | Workshop820260968, 설치/상세 manifest `1963361040482473746`. descriptor는1.19.*을 선언한다. |
| 호환 descriptor | 기존 `1.19.*`, RT56·Korean Language·RT56 Korean Translation 의존성, 기존 호환판 ID3796816200을 유지한다. |
| 외부 TASK | `C:\hoi\test\hok-rt56-democratic-architecture-20261120-01\`. helper·보고서·백업·시험 입력·문서 렌더링 중간물은 이곳에만 둔다. |
| 시작 자료 | `baseline.json`은 호환판2,526파일·원본 변경108파일·기존cache1,490파일·관련host2,112파일·설치참조6개·사용자top-level12개와 저장175개의 크기/mtime 목록을 구분한다. 초기 저장 목록은 전체 저장 SHA 검증이 아니다. `baseline-source/`는 수정 전 도구·문서·대상 기존runtime의 외부 사본이다. |

현재 설치 게임과 기존1.19 입력 지문 차이를 이번 콘텐츠 통과를 위해 면제하거나 과거 source pins에 덮어쓰지 않는다. 전체 엔진/호스트 재기준화와 이번 선택 계층은 별도 범위다.

## 입력과 생성 소유권

[선택 capsule](../upstream/hok-democratic-support-20261120/README.md)은 원본 checkout28개, 이전 Git blob6개, 호환판 직전6개와 선택 문서·크레딧12개를 보존한다. 소스 manifest와 영어26키·안내/자산 출처를 합쳐56파일이다. Git blob의 LF와 실제 checkout의 CRLF를 구분하며 `.gitattributes`의 `-text`로 사본을 보존한다. 기존 capsule과 활성 source cache를 대체하지 않는다.

| 입력 | SHA-256 |
|---|---|
| `source-manifest.json` | `7231250FD522A790C9D692CC710BF298314C0FD1C7C304188824E6B1625F46AC` |
| `english-translations.json` | `07EC0ACC5E688ACD861254F1A1F2DF32B3C7FF88B81E350DA5A1B70EAD39EF05` |
| 중국 지리 대응 JSON | `2672A5C295B2010D95B20013C69FB723DF474245CC0156A59DDA4A4EEED1480A` |

[upstream_democratic_support.py](../../tools/upstream_democratic_support.py)와 [독립 잠금](../../tools/hok_democratic_support_lock.json)이28개의 최종 바이트를 소유한다. 기존6개는 정확한 직전 사본에 범위 delta를 적용하고 신규22개는 선택 입력·영어·지리 적응으로 생성한다. 등록된 이전/최종 바이트만 최종화하며 임의 변경·중복 경로·외부 경로는 거부한다. 최종 바이트를 실제 생성 결과와 대조한 뒤에만 이전 계층으로 역투영한다.

이 계층은 `upstream_commanders`의 역투영·최종화·preflight와 `upstream_us_defense.finalize_outputs`의 한국 중점 소유 경로에 연결된다. 영어 의미 계층의 보존 한국어도 새 delta를 정확히 역투영한 뒤 과거 해시로 검사한다. `source_snapshot`의 영어 파일 허용 목록에는 고정한 신규3파일만 추가하고 실제locale8출력을 확인한다. `validate_port.py`는 새 raw gate를 과거 투영보다 먼저 실행한다. 이전 생성기·잠금·캐시의 source pin을 완화하지 않는다.

기존 원장의 분류를 유지한다. 중점·재건 결정은 `THREE_WAY_MERGE`, 역사 AI·KCH history·기존focus현지화는 현재 원장의 `ADD`이며, 신규텍스트16개는 `ADD`, DDS6개는 `ASSET_COPY`다. 선택 원장 갱신은 기존6행의 지문/사유와 신규22행을 다루며 이전 기여·분류·출처를 보존한다. 전체 원장 생성 성공 여부와 구분한다.

## 동작과 변경 영향 대장

| 기능·ID/소비자 | 처리와 구현 동작 | 실제 확인 상태 |
|---|---|---|
| 중국·일본 민주 지원 중점 | **변경**. 민주 선봉을 선행/배치 기준으로 사용하고 초대와의 배타를 제거. 자동280일 정신을 해당25PP/180일 반복 결정 해금으로 전환 | 소스·생성 출력·한영 해금 UI 확인. 인간KOR의 실제 결정 표시·만료 뒤 일본 UI재구매는 아래 별도 기록. 첫 해금/결정은 강제 |
| 중국 지원 결정·16태그 helper | **변경**. 실존하는 정식16태그를 묶어 지원. 하나라도 기존 지원이 남으면 재구매 차단, 현재 타이머 보존·새 출현국 소급 없음 | RT56 공급자16개 확인. 초기 영토14국의 지원·후기16후보 모두 지원 부재와 중국만 강제 반복을 확인. GDC/KUM은 초기 비영토·미지원. 정상 AI 재사용 판정은 아님 |
| 일본 지원 결정 | **변경**. JAP 존재와 기존 지원 부재를 검사하고180일 지원 | 실제 초기 지원→만료, 한국 민주/독립·JAP존재·지원부재 조건/25PP·180일 툴팁 확인. 같은 일시정지 시각의 직접 구매로 UI정치력107→82와 새180일 지원 표시 확인 |
| 공유 `KOR_democrat_sponsored_by_korea`의 다른 호출자 | **의도적 유지**. 태국·VIN/MAL/PHI/INS 등 이전 경로·정신 수치를 일괄 변경하지 않음 | 범위 밖 파일·관계 보존 |
| 정보국 중점·정신·AI | **변경**. 재무장 시작 선행, La Resistance 전용. 기관이 없으면 생성하고 영구 정신 부여. 요원+2, 정보망 증가10·별도25%, 이념 지원100% 등 원본 최종 수치 유지 | 한영 UI·아이콘·35일·선행 관계, 기존 기관의 실제 슬롯1→3와 기관 부재에서 신규 생성·최대3슬롯/정신을 확인. 선행을 강제한 timer 실행에서 UI로 선택하고 자연 경과로 완료·기관0/3·정신을 확인. 취소한 이전 중점의4일 보존이 있어 새로35일 전부 걸렸다는 측정이나 정상 캠페인·장기 AI 검증은 아님 |
| 중국 축출·생성 직전 guard | **변경**. 실존 CHI 민주 지지도50% 이상·TfV·기존KCH 부재·안전한597/743을 공유. 기본70일, 조건 상실 취소. 한국 민주/독립·대표국 조건 유지하고 한국 맹주 조건 제거 | 실제 강제 조건에서49.9% 차단·50.0/50.1% 허용. 한영70일·조건 UI 확인. 정상70일 진행·도중 취소는 별도 |
| 본토 집합·코어·후속 인정 | **변경**. 원본63주의 의도를 RT56 실제64주로 대응. Gyarong1075 포함, 만주15주·섬/조차지5주 제외. 수도1114 보존 | 독립 지역118/0와 실제 새 저장의 정확한64코어·제외20주 무코어를 확인. 지도·state history 수정 없음 |
| 산둥 기본 영토·추가 선택 | **변경**. 안전한 기본 거점과 적격SND 소유 본토 전부 선택. 타국별 적격주수×지지도(0–90%) 예산과 연결 확장. 반복 상한64 | 실제 SND3주 생성과 한국 소유597·통제1117 보호, 두 거점 차단 후 칭다오743 단독 출범을 확인. 모든 영토 조합의 정상 진행을 검증한 것은 아님 |
| 동적KCH·전력·비축 | **변경**. 거점/공군기지 확보 후 양수 비율의 육해공·비축/연료, 나머지 영토 이전. 완전 소멸 예정SND의 잔여 장비/수송선/연료만 정리. 지휘관 귀순 제외 | 실제0% 이전0,70%에서18→12사단·소총70만·수송선70 확인. 별도CHI50% fixture의85사단/9척/96기→42사단/5척/47기, 공군기지0→1와 실제743배치를 확인. 연료69.9959449%의 명목치 차이는 원인 미확인 |
| 웡원하오 | **변경**. 전용`HOK_KCH_weng_wenhao`를 KCH history에 등록하고 실제 생성국으로 이동·승격 | 기존CHI 캐릭터와 다른 ID. 실제D08의 소유·국적·지도자와 초상화/외교 UI 확인. 구 저장 초기화는 미검증 |
| 자치령·세력·인정 | **변경/유지**. 최종`autonomy_dominion`·TfV, 전쟁 유지·세력 연결·CHI 한정 인정 계약. `_mtg_tt` 키는 유지하고 값은 TfV | 관측된 동적D08 하나·한국 자치령 저장/UI·재호출 무변화 확인. 실제 인정 결정 후CHI16주만 같은D08로 병합·`KCH_china` 확인. 동적태그를 사전 고정하지 않음 |
| 민슈 잇키·일본 helper | **변경**. 지지도10–90% 내전/전력 비율, 기존 한국 세력/참전 연결. 한국 맹주·일본 AI 전용 조건 제거, 한국 민주/독립·일본 비민주·35일 유지 | 상하한·중간값 AI 사례와 인간50% 사례의 봉기·세력·한국 참전을 확인. 비맹주 초대는 실제 맹주 호출로 수선. 실제 자산 개수를 매개변수와 같은 정확한 비율로 표현하지 않음. 인간 자산 native/저장·MP·정상35일 중점은 별도 |
| 한영 표시·그림 | **변경**. 영어26키(신규20·기존6) 의미 번역, paired note·BOM·토큰 유지. DDS6개와 전용sprite/광택 연결 | 원본바이트·치수/알파·소스표시와 한영 중점/지원 해금/산둥 조건 UI 확인. 모든 변형·광택 상태를 실제 관측한 것은 아님 |
| 기존 한국15주·지휘관/과학자/첩보원·외국/공유 시스템 | **의도적 유지/제외**. 새 지도·이름·초상화·일반CHI/JAP·전역자치 정의를 변경하지 않음 | 새로운 소급 저장 이관·일괄 rebalance 없음 |

기존 재건 결정의 코어 목록이 공유 본토 helper로 바뀌면서 원본의 새 본토/제외 계약을 적용한다. 이전 목록에 있던 섬·조차지·만주를 몰래 유지하거나 RT56에서 같은 숫자인 유럽 주를 코어로 사용하지 않는다. 지역 범위가 만드는 게임플레이 차이와 단순 ID 유효성은 구분한다.

C1 실제 툴팁에서 기존 인정 결정 제목은 「산둥 민주공화국」인데 출범 국명은 「산둥 자유 공화국」인 문구 차이를 관측했다. **의도적으로 유지한 기존 donor 문구**로 분류했다. 양 언어의`KOR_New_China_Government` 제목은 이번 선택 delta 이전에도 같았고 RTK 덮어쓰기가 아니다. 잘못된 국가/효과 대상으로 이어지는 근거는 없으며, 인정 후`KCH_china`의 「중화민주공화국」은 별도 국명이다. 원본 문구 수선은 이번26키 번역과 분리하며 검토·한영1키씩의 수선 후보는 외부`geography/qa/recognition-title-review.json`에 남겼다.

## 영어와 자산 출처

donor의 영어 채널 한국어는 원본 사본에 그대로 보관하고 최종 출력의26값만 영국 영어로 옮겼다. `Free Republic of Shandong`, 자치령/TfV, 비용·기간·재사용·50% 조건과 지지도·전력 비율의 의미를 맞춘다. 기존 비대상 영어와 한국어 값·표식/변수·호출 ID는 보존한다. 신규locale는3쌍이며 기존focus한영2개를 포함한8출력이다.

그림6개는 [자산 출처 기록](../upstream/hok-democratic-support-20261120/ASSET_PROVENANCE.md)을 따른다. 영국 정보국·MI6·광택3개는 Paradox/해당 권리자, 지원 결정3개는 기존 시민사회 완성본과 Globvs/Ultimate HOI4 GFX 계열 출처를 보존한다. 새 원화·재색칠·재압축을 만들지 않았다. 전용texture·mask·overlay는 로컬이며 공유 `gfx/FX/buttonstate.lua`는 기존 엔진 공급자다.

## 실제 검사와 남은 검증

| 확인 | 실제 결과·자료 위치 | 한계 |
|---|---|---|
| 전용 생성기 | `--apply`28written → `--check`PASS·0written,64주 | raw 출력 재현이며 엔진 등록/효과 아님 |
| 영어·자산 입력 | `capsule/english-and-assets-report.json`,26키·보호 토큰/수치·DDS6원본바이트·치수/알파 | 실제 UI 아님 |
| 지리 독립 확인 | `geography/independent-region-checks.json`,118 PASS/0 FAIL | source/bitmap 의미 대응. 엔진 점령·인접 평가 아님 |
| 독립 포트 확인 | `geography/qa/independent-port-review.json`,265 PASS/0 FAIL | 순서 AST·비대상focus보존·guard/키/sprite·변조 거부. 정상 게임 진행 아님 |
| 배치 명세 | [475개 좌표·배치 기록](2026-11-20-democratic-support-layout.md), `geography/qa/layout-source-checks.json`,2011 PASS/0 FAIL·18상태 | 소스 모델의 anchor/순환·범위·제한된 사각형 확인. 실제 선/아이콘/이름판·클릭/shine 아님 |
| 전체 정적 최초 사후 | 수정 전8/0/86 → 최초 사후9/0/86 | 단순 개수 일치가 원인 일치를 뜻하지 않음. 아래 보정 이력 참조 |
| 전체 정적 최종 | `static-final.txt`,9 PASS/0 WARNING/86 ERROR, exit1. `static-comparison-final.json`: 신규/해소 원인0·기존 원인 multiset 동일 | 설치/역사 입력·번역 계약 등 기존 실패를 유지한 결과. 전체 통과가 아님 |
| 문서 그림 | 구조도 도입 기록 | 게임 UI·효과·저장 검증과 별개 |
| 일본 비맹주 수선 후 전체 정적 | `architecture/final-qa/static-post-faction-fix.txt`,477.77초·exit1·9 PASS/0 WARNING/86 ERROR. `static-comparison-post-faction-fix.json`: 신규/해소 원인0·기존86원인 multiset 동일 | 수선 전 전체 기록을 보존한 별도1회. 전체 통과·릴리즈 판정이 아님 |
| 실제 R0/C0/C1·후속 실행 | 별도 승인 후R0 독일 지도·1월2일 진행, C0/C1 한영 한국 지도·새 정보국 그림/효과·지원 해금·산둥 조건 UI와 정상 종료를 확인. 외부`runtime/runs/`·`runtime/ui/`·두 UI index | 아래 사례별 실제 강제 효과·새 저장·제한된 재로드·실패/수선 이력을 따름. 정상 캠페인·구 저장 호환 판정과 구분 |

전체 정적 최초 비교에서 영어 의미 계층이 새 한국어focus값을 원래 보존 위반으로 보고하는 새 원인3곳을 확인했다. 같은86이라는 개수만으로 기존 실패와 같다고 처리하지 않았다. 새 계층의 정확한 역투영을 한국어 보존 확인과 영어preflight에 연결해 기존 게임버전 지문 실패로 돌아가는 것을 확인했다. 새 영어 파일 허용 목록도 고정한3파일로 확장했다. 최초 보고서는 `static-after-first.txt`·`static-comparison.json`에 보존하며 최종 전체 결과는 후속 확인으로 구분한다.

최종 전체 검사를 다시 실행한 결과는9/0/86이다. 비교에서 traceback/현지화 위치의 행 번호만 정규화하고 오류 문구·키·경로·횟수를 유지했으며 작업 전과 원인 multiset이 같았다. 이전11월14일의9/0/85는1.19.5 당시 결과이고, 이번 시작1.20의8/0/86과 구분한다. 이 결과가 실제 엔진에서 새 기능이 정상 작동한다는 증거는 아니다.

원장의 신규 행을 현재 상태에서 다시 적용하는 멱등성 검사도 보완했다.1599행·선택28행에 대해 직전 상태에서의 전환과 현재 상태의 재적용이 같았다. 도구만 보완한 뒤 독립 재실행`architecture/final-qa/static-post-ledger.txt`도9/0/86·exit1이며, `static-comparison-post-ledger.json`의 신규/해소 원인은0이다. 새 출력 검사와 문서 원장 검사도 쓰기 없이 통과했다.

일본 비맹주 수선 뒤 전체 검사를 한 번 더 수행했으며 위의 수선 후 결과가 최신이다. 기존86원인은 그대로이고 새 일본 helper의 raw 출력·생성 소유 계약이 통과했다. 독립 수선 검토는 `architecture/final-qa/japanese-nonleader-source-review.json`의14 PASS·0 FAIL, 정확한 직전/최종 바이트 및 거부·원장 재적용 확인은 `runtime/nonleader-fix-r16/independent-structure-check.json`에 구분한다.

## 게임 실행 준비와 사용자 데이터 경계

과거 `-userdir`·복제 설치 격리 시도가 실제 사용자 설정/로그를 갱신한 근거는 [11월7일 기록](2026-11-07-hok-resource-prospecting-port.md)과 [11월10일 기록](2026-11-10-korean-equipment-localisation-repair.md)에 있다. 이를 안전한 격리로 재시도하지 않았다.

외부`runtime/`에는 신선한 프로필9개·기존 로그 백업, 기존 저장175개·12,735,692,750바이트의 SHA 목록, 후보 프로필8개·probe5개와 승인 guard가 있는`session.py`를 준비했다. 이는 초기`baseline.json`의 저장size/mtime목록보다 넓은 별도 읽기 확인이다. 실제 사용자 경로의`settings.txt`·`pdx_settings.txt`·`dlc_load.json` 임시 교체, 새 시험`.mod`, 게임이 생성하는 로그/새 시험 저장/metadata와 원상복구는 별도 승인 여부를 기록한 뒤 수행한다. 준비 자체는 승인·로드·실제 효과의 통과가 아니다.

준비 후 사용자가 **「임시 변경·게임 실행·복원 허용」**으로 별도 승인했다. 승인 범위와 원문 참조는 외부`runtime/user-approval.json`에 기록했다. 실제 사용자 폴더를 사용하는 시험이며 격리 실행으로 표현하지 않는다. 각 실행의 설정·모드 목록·로그·새 시험 저장과 마지막 복원 결과를 분리해 수집한다.

### 실제 실행 기록

외부`runtime/RUN_INDEX.md`의17회 실행·각`runs/<case>/`의 실제 프로필/fixture 사본·지문·로그·안정 복사한 새 저장과`runtime/ui/`를 근거로 구분한다. 실행별 실패와 후속 수선/수동 확인을 보존하며 마지막 프로필 복원 판정은 아래 별도 기록을 따른다.

| 사례 | 실제 관측 | 한계·후속 |
|---|---|---|
| R0 | RT56만 활성화, GER로 세계지도 진입·1936.1.2까지 시간 진행 후 정상 종료. 엔진1.20.0.0.8873 체크섬`ca6d` | 설치 메타데이터`0c4f`와 구분 |
| C0 영어·C1 한국어 | RT56+호환판, 한국어 구성은 RTK도 활성화. 체크섬`a044`. KOR 새 게임의 세계지도·중점 UI, 정보국35일·그림·효과, 지원 결정 해금, 산둥70일·CHI50%·TfV·거점/보호/이전 안내 관측 후 정상 종료 | C1 재무장 시작은 기존20% 초과 조건이 초기15%에서 막힘. 정상 중점 완료를 주장하지 않음 |
| `chi-boundary` r4 | 강제 조건/중점 시험9 PASS·0 FAIL. CHI49.9%차단·50%/50.1%허용, 실제 정보국 중점·정신·기존 기관 유지·슬롯+2. 새1936.1.4.1 저장92,615,965바이트 | `geography/qa/native-chi-effects-02.json`: 저장의 슬롯1→3/증가2·기관`is_created=yes`/정원3·정신 확인. 실제 기관 UI도0/3. 기관이 없는 경우의 생성은 이 사례의 증거가 아님 |
| `formation-zero` r6 | **무효인 fixture**. 일본 종속국 설정 뒤 CHI 지지도가13.3%로 초기화되어 진입 조건부터 실패. 두 실제 저장에서 새 정부 없이 세 거점은SND, 합성 부대10개도SND에 남음 | `geography/qa/native-zero-r6-invalid-fixture-conclusion.json`에 실패와 후속 연쇄 실패를 보존. 생산 결함으로 판정하지 않음. 지지도를 최종 종속 설정 뒤 다시50%로 만드는`formation-zero-r9`는 별도 이름/프로세스/저장으로 재시험 |
| `formation-zero-r9` | 네이티브 PASS 발생1209회·FAIL0, 두 실제 저장의 독립 대조66 PASS·0 FAIL. 이번 생성국D08/원태그KCH 하나, 정확64코어·제외20 무코어, 웡·민주정·한국 자치령. SND의18사단·소총100만·수송선100·연료45.375k에서 즉시 이전0. 실제 자치령/웡 UI 관측 | `geography/qa/native-zero-r9-independent-verdict-01.json`. 첫 저장은597/743/1117 소유. 이후743/592를SND로 의도적으로 되돌려 다른 출범 요건을 열고 재호출해도 정부1개·자산 변화0. 두 번째 저장의743가SND인 것은 시험 준비다. 포병·해공군 양수 입력, 통제권, 자연 진행·재로드의 통과로 확대하지 않음 |
| `formation-positive` r10 | 네이티브 PASS 발생1299회·FAIL0. 세 저장의 독립 대조77 PASS·0 FAIL. SND18→12사단·고유 합성 부대7개, 소총100만→70만·수송선100→70. 세 거점 소유와 완전 통제 관측값1. 같은D08·64코어·웡·자치령 및 재호출 변화0 유지. 인정의 전 세계 소유권 변화는CHI16주→같은D08에 한정, `KCH_china` 적용 | `geography/qa/native-positive-r10-independent-verdict-01.json`. 즉시 연료45.375k→31.76066k(69.9959449%): 명목70%보다 원시연료1.84 적은 차이의 원인은 미확인. 포병·해공군 양수 입력은0으로 별도 미검증. 종료는 담당 driver의`CloseMainWindow`요청이며 root의 실제 UI 종료 관측·자연 종료·충돌로 기록하지 않음. 해당 기록을 보존하고 driver의 활성 게임 종료 기능을 차단 |
| `protection` r12b | 네이티브 PASS 발생600회·FAIL0, 새 저장 하나의 독립 대조54 PASS·0 FAIL. 두 거점 차단 후743만D08 소유·수도,597은KOR 소유·1117은SND 소유/KOR 통제로 보존.743 공군기지1과 실제47기 배치. CHI85사단·9척·96기→D08의42·5·47과 잔류CHI43·4·49로 합계 보존 | `geography/qa/native-protection-r12b-independent-verdict-01.json`. 기지 사전0과 첫 호출 차단은 실행 로그, 최종 영토·기지·전력은 저장 근거로 구분. nominal50%를 서비스별 정확한50% 배분으로 표현하지 않음. root Jan4.12 화면 기록 후 titlebarX 정상 종료·창 부재 확인 |
| `japan-10` r4 | 실제7 PASS·0 FAIL, 독립30 PASS·0 FAIL. 실제 반군D08/원태그JAP·민주정·`KJP_democratic`, 한국과 같은 세력·일본과 전쟁·한국 참전. 사전60사단/207척/831기에서 반군 즉시6/18/74와 후속 원JAP54/189/757로 합계 보존. 기관이 없던KOR에 기관 생성·새 정신·최대3슬롯 확인 | `architecture/final-qa/japan-review/japan-10-independent-verdict-01.json`. 실행JAP는AI. 해공군 관측 분율은 약8.70%/8.90%이므로 정확10%라고 쓰지 않음. 원JAP 즉시 잔류 getter·사후 조작국 표식은 이 fixture에 없으며 후속 native 관측과 구분. 비축 비율은 명시하지 않은 원본 계약 유지 |
| `japan-50` r13, 수선 전 | **유효 조건의 실제 실패**. 실제5 PASS·1 FAIL, 독립26 PASS·1 FAIL. ENG·KOR가 같은 세력이고 한국은 비맹주이나 민주 반군D08은 어느 세력에도 없음. 반군 생성·일본과 전쟁·한국 참전은 성공. 즉시 육해공은 반군29/87/386 + 원JAP31/120/445 = 사전60/207/831 | `architecture/final-qa/japan-review/japan-50-independent-verdict-01.json`. 실패 원본/fixture/native/UI를 보존하고 재실행은 다른 이름 사용. 사후 양측AI. 이후 native 원JAP 항공410과 즉시445의 차이35는 원인 미확인인 후속 관측이며 새 배분 결함으로 단정하지 않음 |
| `japan-50-r16`, 수선 후 | 실제7 PASS·0 FAIL, 독립32 PASS·0 FAIL. 새 저장에서 ENG·KOR·민주 반군D08이 같은 세력이며 반군 가입일도 존재. 한국 비맹주·영국 맹주 유지와 한국 참전을 확인. 즉시 육해공29/87/386 +31/120/445는 수선 전과 동일 | `architecture/final-qa/japan-review/japan-50-r16-independent-verdict-01.json`. 고유Jan4 저장93,140,416바이트·SHA`8D6128905C8C2F5432307316F9606957ADE65EE9ED621AECBF4FE77C2A1DA715`. root 실제속도5bar 설정 후Jan11.07 UI 기록·정상 종료. 명령줄 속도 선언과 실제 UI속도는 구분 |
| `japan-90` | 실제5 PASS·0 FAIL, 독립28 PASS·0 FAIL. 실제 민주 지지도1.0에서 helper 호출. 사전60사단/207척/831기→반군53/141/677 + 즉시 원JAP7/66/154로 합계 보존. 반군·한국 같은 세력/한국 참전, 사전·양쪽 사후AI 확인 | `architecture/final-qa/japan-review/japan-90-independent-verdict-01.json`. native 원JAP 항공141과 즉시154의 차이는 후속 관측으로 분리. source의 .90 상한과 단위 개수의 정확90% 배분을 동일시하지 않음. native 뒤 원JAP 패배 개요 화면을 관측하고 root 정상 종료 |
| `japan-human-50-r14` | AI시험 옵션 없이 실행7 PASS·0 FAIL, 독립26 PASS·0 FAIL. helper 직전 명시적 인간 전제 및 원JAP 전후`is_ai=no`, 반군AI를 확인. 한국 비맹주·반군 세력 가입·전쟁·한국 참전, Jan3/Jan23 실제 PlayerJapan 툴팁 관측 | `architecture/final-qa/japan-review/japan-human-50-r14-independent-verdict-01.json`. 이 실행의 native는 정확0. 인간 자산 수치·동적태그·저장 검증에 다른 AI 사례를 전용하지 않음. KOR 중점의 정상 선택/35일 완료 증거와도 구분 |
| `positive-reload-r14` | 실제69 PASS·0 FAIL, 독립50 PASS·0 FAIL. 실제 메뉴에서 초기positive Jan4 저장을 불러오고 새Jan5 저장 생성. 같은D08·웡의 native ID/소유·한국 자치령·정확64코어/제외20·세 거점·전체12부대 ID/이름과 고유SND7개,84검토 주 소유자 보존 | `geography/qa/native-reload-r14-independent-verdict-01.json`. 초기 SHA`0F9517FCDF2651383D467F1910A19A0C7706FCE1E17AF88082468DF3783F3697`→새 SHA`55783C03385355046157BA7C61219894C4D8F1587E861CC44CF15D36C304A455`. 선택 출력27개 동일/일본helper1개 변경·진단fixture교체/옛pending .5 log-only 조건에 한정. 기존175저장 미로드·구 저장 호환 판정 아님. root 로드된 지도·웡 외교 UI와 정상 종료 확인 |
| `chinese-nonleader-r18` | 실제10 PASS·0 FAIL, 독립34 PASS·0 FAIL. 한국 비맹주·영국 맹주·CHI50% 조건의 실제 생성 과정에서 ENG/KOR/D08 같은 세력, 한국 자치령·웡·민주정·64코어/제외20·세 거점 확인 | `geography/qa/native-chinese-nonleader-r18-independent-verdict-01.json`. Jan4 새 저장92,851,451바이트·SHA`26ABC3D195496031014D8B36C4DBE48A3C69B9F09DCB0B906DAD497C78EBA82D`. 중국 helper는 변경 없이 유지. 전체 과정의 성공이며 자치 설정과 명시적 초대 중 어느 명령이 가입을 수행했는지는 분리하지 않음. root Mar3.08 화면·정상 종료는 부수적 진행 기록이며 장기 캠페인 검증이 아님 |
| `support-timers` r17 | 실제35 PASS·2 FAIL을 보존. Jan3.12 두 결정의 강제 실행 즉시 합계500→450PP. Jan4 저장은 영토가 있는 중국14국+JAP 지원179일. root Jan4.23 정보국 UI선택, observer Jan5.10 진행→Feb4.03 완료, Feb12.15 실제 새 정신·기관0/3 확인. **만료 검사2 FAIL**, Jul4 저장은 중국178일·JAP179일로 재활성 혼입. Jul16.03 UI 중국166일·JAP167일 | `geography/qa/native-timer-r17-independent-verdict-01.json`·`architecture/final-qa/timer-r17-cost-ai-review-01.json`. AI시험에서 억제용 enable flag를 설정하지 않은 진단 준비 결함. 후기 observer는 정신 존재만 보고100→100PP/차감0/hour0에서 반응해 실제 만료·수동 재구매를 입증하지 못함. 최초 만료 순간·재활성 주체도 확정하지 않음. 두 저장/실패를 보존하고 root 정상 종료. 정보국 완료는 별도 유효하나 선행 강제·이전 중점4일 보존으로 완전 정상 캠페인이나 새35일 전부 경과를 주장하지 않음. 생산 코드는 수정하지 않고 인간KOR 재시험으로 분리 |
| `support-timers-human-r19` | AI시험 옵션·억제 전략 없는 실제 인간KOR. 초기20 PASS 뒤 실제Jul3.11 인간/양쪽 지원부재 확인23 PASS, root Jul3.23 만료 저장. Jul4.10 중국만 강제 반복·JAP부재/재사용차단/인간 전제까지39 PASS. **자동 관측기 FAIL1·FINAL 없음**은 그대로 보존. root Jul10.21 일시정지에서 일본25PP 구매 버튼을 한 번 눌러 정치력 정수표시107→82·일본180일/중국174일을 관측하고 같은 시각 세 번째 저장 | `geography/qa/native-timer-r19-independent-verdict-01.json`: 세 저장의 중국14+JAP173일→중국16후보+JAP 모두 지원 부재→중국14는174일/JAP180일을 독립 대조. 보관 UI의 같은 시각107→82도 직접 확인. 독립142개 근거 일관성 검사는 자동 PASS와 합산하지 않음. 초기 중점/결정과 중국 반복은 강제, 중간PP100 재설정·시간 경과가 있어 저장 간 PP나 오래된 observer100을 직접25 차감으로 계산하지 않음. 최종rawPP82.206·observer168·after/delta/FINAL 부재를 유지하며 자동진단 실패 원인은 미확정 |

r19는 실제 Local SaveGame에서 아래 이름을 새로 입력했으며 엔진이`_temp.hoi4`를 붙였다. 원본과 안정 사본의 동일성은`runtime/r19-manual-capture-receipt.json`, 독립 상태 판정은 위 별도 보고서를 따른다. 세 사본은 외부`runtime/runs/support-timers-human-r19/capture-20261119T191630890603Z/`에 보존한다. 실제 최초 만료 전환의 정확한 엔진 tick까지 측정한 것은 아니다.

| 실제 게임 생성 파일 | 저장 시각 | SHA-256 |
|---|---|---|
| `HOK_DSI_r19_initial_temp.hoi4` | 1936.1.10.22 | `1D50E68C2945306D591D7B9E1972990F9F796662077DCB3004D2E87BD126550F` |
| `HOK_DSI_r19_expiry_temp.hoi4` | 1936.7.3.23 | `216D52AA0F2917DA7B65C00E7121247997231378985004D93B76CEB4F8BECE0B` |
| `HOK_DSI_r19_rebuy_temp.hoi4` | 1936.7.10.21 | `7694F3F2FA0811B0E5D0D7456AF73F261074E6BB1911366E093C81F4FC641B59` |

### 일본 비맹주 세력 호출 수선

원본에서 가져온 `KOR = { add_to_faction = PREV }`는 현재 대상 환경에서 한국이 비맹주일 때 반군을 초대하지 못했다. 한국·영국의 실제 세력 소속과 반군의 미가입이 저장에도 남아 있으므로 단순 툴팁이나 시험 조건식 문제로 분류하지 않는다. 한국 맹주 조건 제거에 필요한 후속 연결 수선으로 별도 기록한다.

한국이 실제 세력에 가입한 비맹주일 때만 `faction_leader = { add_to_faction = PREV.PREV }`를 사용하도록 생성 적응을 구현했다. 문맥은 새 반군→한국→실제 맹주이므로 두 단계 앞이 반군이다. 그 밖의 경로는 기존 한국의`add_to_faction = PREV`를 유지하며, `add_to_war`는 한국 문맥에 남긴다. 무세력 한국의 기존 동작을 새로 설계하지 않는다. 당시 미검증이던 중국 비맹주 경로는 위의 별도`chinese-nonleader-r18`에서 전체 과정 성공을 확인했으므로 추가 수정하지 않았다.

고정 원본851바이트·SHA`F2A255FB9AB4194B9E24AB908B0CD8F20BE6C1CE973AE0A4F4FF83D86D72D1F6`에서 정확한 한 블록만 교체한다. 최종 일본 helper는1118바이트·SHA`8684B6498B3866B102676E1B995BBCAFE306984B708B7720777FB5472C2C8A5C`이며 나머지27출력과 비율·참전·ID는 보존한다. owner·잠금·원장의 해당1행에 이 정확한 선행 출력과 적응 사유를 등록했다. 원본 capsule과 과거 소스 핀은 그대로다. `runtime/nonleader-fix-r16/`에 직전4파일·패치·전후 지문을 보존했다. 별도 새 `japan-50-r16`의 실행과 저장에서 세력 가입 수선을 확인했고, 수선 후 전체 검사도 기존86원인이 동일하다.

## 검증 판정과 별도 범위

선택한 콘텐츠28출력과 생성 소유권·영어·그림·배치·AI 연결, AGENTS·로컬 스킬·구조도 체계를 구현했다. 한영 UI, CHI 지지도 경계, 정부/자치령/웡/영토와 전력 이전, 일본 AI·인간 봉기와 비맹주 수선, 새 저장의 제한된 cold reload를 위 조건에서 확인했다. 지원 만료·재구매도 실패한 자동 진단을 지우지 않고 인간KOR의 실제 UI와 세 저장으로 독립 대조했다. 문서 QA는 `architecture/final-qa/documentation-final-review-03.json`에서24문서·상대링크668개와 갤러리264링크,32 Mermaid·64그림·manifest·소스 근거의 불일치0을 확인했다. AGENTS descriptor 지침 정정 뒤 문서 전용 원장 갱신/검사도 통과했다(`final-documentation-ledger-refresh.json`).

전체 정적 검사는 여전히 기존86오류로 exit1이며 전체1.20/RT56 재기준화나 릴리즈 통과를 뜻하지 않는다. 정상 캠페인에서 중국70일/일본35일 중점의 선택부터 완료·도중 취소까지 전 과정, 모든 지리/배치 변형, 양수 포병 이전, 지원 후 새 출현국·정권/외교 변경의 모든 분기, 장기 AI·멀티플레이·DLC 부재·기존175저장 이관은 검증하지 않았다. 새 저장 한 개의 재로드는 구 저장 호환의 증거가 아니다. 명목70%와 관측 연료의 미세 차이 및 일본 후속 항공기 수 차이의 원인도 미확정으로 유지한다. 원본 소스·UI·강제 효과·정상 달력 경과·저장·문서 렌더의 증거를 서로 대체하지 않는다.

## 자료와 보존

실제 게임 실행은 모두 끝냈다. 최종`runtime/FINAL_RUNTIME_RECEIPT.json`과`preservation-20261119T191651236591Z.json`에서 기존175저장과 이번 게임이 만든 원본20개의 크기/SHA 변경0, 선택한 프로필/metadata12개 전부 보존, 임시 pointer 부재와 게임/launcher 프로세스 부재를 확인했다. `restoration-20261119T191633417009Z.json`은10개 설정의 존재/부재·내용 복구를 기록한다. 원래 저장175개는 로드하거나 덮어쓰지 않았고, 새 시험 원본은 실제 사용자 폴더에 남겨 외부 증거 사본과 구분한다. 게임이 생성한 원본 로그와 시험 전/후 외부 사본도 별도 역할이다.

마지막`runtime/final-target-recheck.json`은 로컬 설치/캐시의 RT56 manifest 관측3값 모두`1963361040482473746`, 게임 설치 메타데이터`Operation Postern v1.20.0.0.8873 (0c4f)`, 이전 vanilla 참조6개의 크기/SHA 일치를 확인했다. 온라인 최신 버전 조회나 설치 전체 검사를 했다는 뜻은 아니다. r19 세 저장의 정확한 이름·`HOI4txt`·안정 원본/사본 해시는`runtime/r19-manual-capture-receipt.json`의 별도 PASS이고, 자동39 PASS/1 FAIL·FINAL 없음·strict collect exit1은 그대로 보존했다.

마지막 읽기 전용 소스 감사`architecture/final-qa/source-preservation-final.json`도 PASS다. runtime1515→1537, 기존6수정·신규22·삭제0·28출력 밖 변경0·잠금 불일치0, donor선택108/cache1490/RT56선택2112/game참조6/기존pycache21의 크기/SHA와 cache/pycache 목록·두 HEAD·donor clean·시작 자료 보존을 다시 확인했다. 새 시험 산출물 후보는0이며 AGENTS 문서 전용 원장 변경은 runtime과 구분한다. 아래 r16 감사는 당시의 별도 결과로 유지한다.

일본 helper 수선 후의 별도 읽기 전용 대조는 `architecture/final-qa/source-preservation-after-r16.json`이다. 시작1515→현재1537, 기존6수정·신규22·삭제0, 허용28출력 밖 runtime변경0·최종 잠금 불일치0을 확인했다. 고정 선택 경로인 donor108·RT56 2112·설치 게임6개와 활성cache1490·기존pycache21개의 크기/SHA, cache/pycache 목록, 두 HEAD와 donor clean 상태가 유지됐다. donor/host/game 전체 디렉터리의 전수 해시 검사로 확대하지 않는다. 병행 문서 변경은 별도 스냅샷이며, 이 결과는 사용자 프로필·저장의 마지막 복구 확인을 대신하지 않는다.

TASK의`baseline.json`·`baseline-source/`, `static-before.txt`·`static-after-first.txt`·`static-comparison.json`, `capsule/`, `geography/`, `architecture/`, `runtime/`는 시작 자료·각 하위 작업·실제 수행 결과를 구분한다. 최종 원장·보존·실행 검사는 해당 보고서와 이 문서의 후속 기록으로 남긴다. 실제 시험용 파일과 렌더링 helper를 저장소나 업로드 패키지에 넣지 않는다.

독립 보존 대조`architecture/final-qa/preservation.json`에서 runtime은1,515→1,537파일, 기존6개 수정·22개 추가·삭제0이며 소유한28출력 밖 변경0이다. 원본 선택108개·고정cache1,490개·RT56선택2,112개·게임참조6개·기존pycache21개의 크기와 SHA가 시작 자료와 같았다. 두 저장소 HEAD도 유지했다. 이 대조는 실제 사용자 프로필을 임시 변경한 게임 실행 중의 원상복구 확인을 대신하지 않는다.

기존`tools/__pycache__/`21파일·1,088,888바이트는 정리 미결이다. 새 실행에는`-B`/외부pycache설정을 사용하며 기존 캐시를 삭제하지 않는다. 활성source cache와 이전capsule·외부기록은 입력/출처로 보존한다. 커밋·푸시·게시·업로드는 수행하지 않는다.
