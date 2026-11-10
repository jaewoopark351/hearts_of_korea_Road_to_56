# 2026-11-10 원본 지역 산업 업데이트 이식

상태: **기존 4출력에 선택 구현 적용·범위 정적 확인 완료 / 실제 실행 검증 대기**. 최종 aggregate는 **27 PASS / 0 WARNING / 11 기존 ERROR**다. 이번 계층의 수정·재생성·출처 비교 전 이 문서와 [선택 입력 안내](../upstream/hok-industry-update-20261110/README.md), [잠금](../../tools/hok_industry_update_lock.json)을 읽는다. 현지화·지역 의미를 판단할 때 [변경 영향 절차](../HOK_CHANGE_COVERAGE_REVIEW.md)와 분야별 로컬 스킬을 적용한다.

## 요청과 기준

사용자는 업데이트된 `C:\hoi\hearts_of_korea`의 내용을 호환판으로 가져오도록 요청했다. 기존 RT56 통합 위에 선택한 원본 업데이트를 구현하고 정적으로 확인한다. 게임·launcher·사용자 데이터·플레이세트 변경이나 실행, Git commit/push·업로드는 수행하지 않는다.

| 항목 | 이번 관측 |
|---|---|
| 호환판 | `feat/korean-focus-update-20260922@287c5a22f264075bac65505e0a3e9d8a29ff24f3`, 시작 작업 트리 깨끗함 |
| 읽기 전용 donor | `feat/korean-focus-expansion-ai@596b221bb994d93fce552d3ee1ba70fa9b5640f1`, 미커밋 8파일. 그 이전 커밋된 업데이트는 이미 이식돼 있음 |
| 설치 게임 | Steam build `26409260`, `Operation Postern v1.19.4.2.2da5 (0bdb)`; 새 포트 실행 체크섬이 아님 |
| RT56 | 설치/latest manifest `1963361040482473746`, 기존 host-current-inputs 4,823경로 재비교 missing0/changed0 |
| 현재 사용자 구성 | `C:\Users\jaewo\OneDrive\문서\Paradox Interactive\Hearts of Iron IV`, 한국어·1280×720·GUI1.0, donor+일반판 영어 번역 선택, disabled DLC 없음. 포트 시험 구성이 아님 |
| 최신 로그 | 11월10일 03:13–03:18 원본 진단 실행, 엔진 `632f`·DLC36·province13,448. 이번 포트 결과로 사용하지 않음 |
| 외부 산출물 | `C:\hoi\test\hok-rt56-industry-update-20261110-01\`의 helper·baseline·preview·검사 보고서. 소스 입력은 위 capsule과 구별 |

저장소 descriptor/외부 `.mod`의 호환판 ID `3796816200`, RT56+Korean Language 의존성과 물리 포트 경로는 유지한다. 소스 Workshop ID로 업로드하지 않는다. 활성 번역 덮어쓰기·배포 언어 계약은 기존 미확정 상태다.

## 변경과 의도적 보상 증가

원본 변경 8파일에서 실제 runtime 출력은 기존 4파일이다. 네 파일 모두 기존 원장의 `THREE_WAY_MERGE` 분류를 유지한다. 한국 15주 지도와 persistent ID는 바꾸지 않는다.

| 기능·ID | 포트 대상·기대 변화 | 처리와 근거 |
|---|---|---|
| `KOR_northern_development` | 527·1151·918·1152 각 슬롯3, 합6→12 | 수정. 원본의 후속 도별 보상 강화 |
| `KOR_southern_development` | 919·1150·920·1148·1145·1149 각 슬롯2, 합6→12 | 수정. 원본의 후속 도별 보상 강화 |
| `KOR_central_region_development` | 525·1144·917·1153 각 슬롯2, 합6→8 | 수정. 경기·강원 보상은 기존 그대로 |
| `KOR_gyeongbu_expressway` | 경기525 기반시설1; 충남1145·충북1149·경북920·경남1148 각2, 합5→9 | 수정. 별도 철도·도로·지도 배치 변경 없음 |
| `KOR_gyeongui_expressway` | 경기525 기반시설1; 황남917·황북1153·평남527·평북1151 각2, 합5→9 | 수정. 기존 대공황 I→II 조건/효과 순서 보존 |
| 평안 투자 | 기존 평남527 + 신규 평북1151, 각 군수공장1·슬롯1 | 수정. 기존 `HOK_KOR_pyeongan_industry_project`·완료 flag 유지, 새 `HOK_KOR_pyeonganbuk_industry_project`는 독립 완료 flag |
| 충청 투자 | 기존 충남1145 + 신규 충북1149, 각 민간공장1·슬롯1 | 수정. 기존 `HOK_KOR_chungcheong_industry_project`와 새 `HOK_KOR_chungcheongbuk_industry_project` |
| 경상 투자 | 기존 경남1148 + 신규 경북920, 각 조선소1·슬롯1 | 수정. 기존 `HOK_KOR_gyeongsang_shipbuilding_project`와 새 `HOK_KOR_gyeongsangbuk_shipbuilding_project`; 각각 자기 주의 해안 조건 |
| 세 지역 중점 | 기존 남도와 신규 북도 두 결정의 해금 안내 | 수정. 실제 visible은 기존 중점 완료, 추가 사용 조건은 별도 유지 |
| 강원 투자 | 1144의 기존 사업·보상·취소 | 의도적 유지. 원본 변경 없음, 기존 블록 보존 |
| 연구망 핵 툴팁 | `$HOK_KOR_STATE_1028$`→함경남도/South Hamgyeong, helper 우선918 | 의도적 유지. 포트에 이미 반영돼 있음. 원본 새 문서/문구는 근거로만 보관 |
| 시작 history·지도·CNDP·시민사회·외국/공유 콘텐츠 | 기존 RT56+승인된 HOK 합성 | 제외. 이번 산업 업데이트의 대상 아님 |
| 활성 번역과 실제 결정 UI·비용/완료/취소·저장·AI | 새 포트 실행의 실제 동작 | 미확인. 정적 성공을 실행 증거로 확대하지 않음 |

이번 보상은 [ADR-0006](../decisions/0006-korean-state-split-integration.md)의 과거 고정 총량 분배를 되살리는 호환 수선이 아니라 **원본의 명시적인 후속 강화**다. 위 5중점과 3지역 결정만 그 보존 계약의 예외로 채택한다. 남북 투자를 동시에 진행할 수 있어 같은 90일 동안 두 번 비용을 내고 두 시설을 받을 수 있다. 기존 각 결정의 정치력150·90일·반복 가능·민공 미점유·취소 환급 없음·AI base1은 유지한다. 다른 주 상실은 해당 사업을 취소시키지 않고 대상 주 상실·슬롯 부족·항복이 취소/최종 재검사에 연결된다.

## 표시·범위·생성 소유권

한영 각 16값(기존10변경+신규6)을 반영한다. 중점 설명3·범주 설명1·남도 이름/설명6·북도 이름/설명6이다. 남도/북도 명시와 개별 대상 소유·완전통제·부지·해안·비용·기간·취소·반복 조건이 실제 코드와 이어진다. 다른 영어·한국어 값과 기존 키를 보존한다. 일반판 영어 작업 트리의 선택16값은 기존 `South/North Pyeongan`, `South/North Chungcheong`, `South/North Gyeongsang` 표기로 맞춘다.

새 결정3개와 새 완료 flag는 포트·현재 RT56·vanilla의 common/events/localisation에서 기존 충돌이 없다. `GFX_decision_generic_construction`은 원본이 선택한 기존 아이콘이며 vanilla `interface/decisions.gfx:733–734`에서 상속한다. 자산·공유 sprite를 새로 복사하거나 바꾸지 않는다. 같은 버전의 vanilla `common/national_focus/germany.txt`와 `sweden.txt`에서 슬롯/건설/해금 문맥을 비교했고 별도 새 문법을 도입하지 않았다.

[새 생성 계층](../../tools/upstream_industry_update.py)은 정확한 이전 포트4개와 donor 전후 입력을 사용한다. 중점은 검토된8개 completion_reward만 바꾸고 나머지 중점 조건·배치·기간·AI를 보존한다. 결정은 승인된 state 대응과 기존 포트 주석을 유지한다. 현재 runtime을 기대값으로 읽거나 과거 핀을 갱신하지 않는다. 기존 최종화 뒤에 새 계층을 연결하고 정확히 입증된 최종 바이트만 이전 바이트로 역투영한다. 미등록 수정은 preflight에서 거부한다. 통합 원장은 기존 출처/저작 열과 분류를 유지하면서 4행의 최종 해시·이번 변경 사유만 갱신한다.

## 검증 기록

필수 정적 확인은 5개 보상 배분·3개 해금, 7개 결정의 조건/대상/취소/최종 재검사·강원 보존, 기존 ID/flag·중점 보호 필드, 한영 16값·토큰·BOM/줄 끝·기존 문구, 결정적 생성/역투영/미등록 수정 거부, 이전 source/host/profile/runtime 보존과 전체 aggregate 전후 비교다. 실제 UI·효과·정상90일 진행·진행 중 저장 재로드는 실행 검증 대기이며 이번 포트 구현의 정적 확인으로 대체하지 않는다.

최초 aggregate는 통합 도구 편집과 겹쳐 새 모듈 import 실패를 포함했다(`static-before.txt`,18 PASS/0 WARNING/19 ERROR). 완전한 사전 기준선으로 사용하지 않는다. runtime을 변경하기 전에 HEAD 도구를 외부에서 읽기 전용으로 복원한 별도 기준선을 수집한다. 이후 결과는 여기에 추가하며 최초 실패를 덮지 않는다.

기존 정리 미결 산출물은 `tools/__pycache__/` 21파일·1,088,888바이트(약1.04MiB)다. 이번 작업에서는 이동·삭제하지 않는다. `.local-artifacts`는 없고 기존 외부 active source cache/보관소는 유지한다. 새 시험 출력은 외부 작업 폴더에만 둔다.

### 이번 실제 수행 결과

| 검사·작업 | 결과·근거와 한계 |
|---|---|
| 수정 전 깨끗한 도구 기준선 | HEAD 도구30개를 외부에 보존하고 원래 `__file__`/하위 도구 경로만 지정해 **26 PASS / 0 WARNING / 11 ERROR**, exit1. 실행 전후 runtime1,476파일 차이0. `static-pristine-before.txt`, receipt와 export provenance를 보존. 최초 동시 편집 결과와 구별 |
| 적용 전 독립 소스 QA | **217 PASS / 0 FAIL**, `qa/independent-preview-qa.json`. 새 변환 함수를 기대값 생성에 사용하지 않음 |
| 적용 | 새 생성기 `--apply`로4개 출력 기록, scoped 원장 생성기로4행 갱신 |
| 실제 디스크 독립 소스 QA | **219 PASS / 0 FAIL**, `qa/independent-runtime-qa.json`. 여기서 runtime은 파일 경로를 뜻하며 게임 실행이 아님. 474중점·보상/해금8블록 외 보호 필드와 배치·7결정·강원 블록·32문구·연구망·ID 충돌·아이콘 공급자를 확인 |
| 생성 계층 연결·수정 거부 | **65 PASS / 1 기존 host drift 차단**, `integration-hook-preview.json`. 이전/최종 바이트·별칭·역투영·완전한 최종화·미등록 바이트 거부·November32/분할47 dry build 확인. 전체 한국 생성기 경로는 기존 `00_generic_organization.txt` feature pin drift에서 차단됐으며 통과로 기재하지 않음 |
| 변경 보존 감사 | `final-preservation.json` PASS. 시작 지문1,477개 중 지정4개만 변경, 과거 source/lock696개 차이0, 현재 RT564,823개 차이0, donor8입력·사용자 설정·branch/HEAD 보존. 이전 원장1,541행 중4행의 최종 해시/사유 셀만 변경 |
| 저장 위치·diff | 기존 pycache21개·1,088,888바이트 유지, `.local-artifacts` 없음. `git diff --check` 통과. 새 시험/프리뷰는 외부 작업 폴더에만 생성 |
| 적용 후 연결 재검토 | **6 PASS / 0 FAIL**, `integration-hook-final-review.json`. 현재 최종 바이트·새/이전 preflight·원장 멱등성과 무수정 확인 |
| 최종 aggregate | **27 PASS / 0 WARNING / 11 기존 ERROR**, exit1, `static-after.txt`. 새 raw 산업 gate·기존 영어/후속 수선/November/분할/scoped 원장 등 통과. `aggregate-comparison.json`에서 사전11개와 오류 본문이 같음을 확인. 비교할 때 캡처별 인코딩을 읽고 traceback 도구 절대경로/행번호만 정규화함 |

지도·시작 history·영토 ID·기존 연구망·다른 언어 문구·시민사회 수선·재벌 영어 계층은 유지했다. 원본·Workshop·게임 설치·launcher/user-data는 수정하지 않았다. 실제 UI, 90일 완료/취소/재착수·동시 사업·새/기존 저장·장기 AI·다른 DLC·멀티플레이는 미검증이며 새 게임 기준의 기존 저장 정책을 바꾸지 않는다. 기존 실패11개와 이전 UI 미확인 사항은 이번 이식으로 해소됐다고 주장하지 않는다. 커밋·푸시·게시·업로드는 수행하지 않았다.
