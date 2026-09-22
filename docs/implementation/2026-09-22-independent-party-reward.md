# 2026-09-22 독립당 단독 집권 부분 동원 보상

## 범위와 기준

사용자가 원본의 `KOR_independent_party_in_power` 완료 보상 업데이트 적용을 요청했다. 기존 민주주의 지지도·정당명 보상 뒤에 민간경제 또는 초기 동원일 때만 부분 동원을 지급한다. 이미 부분 동원·전쟁경제·총동원 또는 다른 경제법이면 유지한다. 중점 ID, 위치, 비용, 선행 조건, AI 가중치는 유지한다. 원본의 의도적 보상 강화이며 호환성 결함 수리로 분류하지 않는다.

- 작업 기준: `feat/korean-focus-update-20260922@d2bd30358e15ada7c2768d536409ec282ce4ecda`.
- 작업 전 변경: `history/countries/KOR - Korea.txt`의 Man the Guns 분기 전쟁 지지도 `0.05 -> 0.1`. 이번 작업은 해당 파일을 수정하지 않는다. 작업 전 SHA-256은 `243FC1FBDE8DB75B82CCFEBD6BB01CA7001DABCD944CA8534E7324413705BE30`이다.
- 설치 실행 로그: HOI4 `1.19.3.0.c01a (68ca)`, build `2026-09-09 09:10:08`, DLC 36개. 이 체크섬은 최신 donor 실행 기록이며 이번 변경의 호환판 실행 증거가 아니다.
- 호스트: RT56 `820260968`, manifest `7475007536894105204`.
- Windows 사용자 데이터: `C:/Users/jaewo/OneDrive/문서/Paradox Interactive/Hearts of Iron IV`; 언어 `l_korean`.
- 현재 `dlc_load.json`은 `mod/hearts of korea.mod` 하나를 가리키며 실제 경로는 donor다. 이번 작업은 게임을 실행하거나 playset을 바꾸지 않는다. 후속 호환판 실행은 donor 없는 RT56+호환판 구성으로 별도 검증해야 한다.
- 저장소 및 외부 호환판 descriptor는 RT56과 Korean Language 의존성을 선언하고 외부 path는 이 저장소를 가리킨다. RT56의 replace_path는 states/strategicregions, 별도 RT56 Korean Translation의 replace_path는 localisation이다. 기존 언어 계약은 이번 범위에서 변경하지 않는다.

## 출처와 병합 결정

`common/national_focus/korea.txt`는 기존 `OVERRIDE` 분류를 유지한다. 기존 20개 고정 donor 입력과 지도 ID·만주 병합을 보존하고 생성기에 이번 보상만 명시적으로 추가한다. 원장의 `donor_source_*`는 계속 고정 입력을 뜻하며 이번 후속 출처는 아래와 원장 reason에 별도로 기록한다.

| 참조 | SHA-256 |
|---|---|
| 기존 고정 donor 중점 입력 (`da815305e3ce00186a487b3a378bf8536ff59146`) | `49EC715410B6931E51A6ABB297F7BE17E85D75A1AF72F4A70155E7824A54F903` |
| 이번 donor 중점 (`698b6eb160efbaa04a4d43846330ba002f5e8cc7`) | `93D9478053E5F0A8C8EEEB72DAE7BFEDF5DDDAA8FB439BE528DBE81FAD01ACCA` |
| 변경 전 호환판 중점 | `1E14EBB08B466214967FEA0463A23D981716CE376A8A562172C979D299182F30` |
| RT56 `common/national_focus/korea.txt` | `A80FBC767C21902FC56EBBCA35DC3C120700E527B52EA98F3CFDF5221EB0EF90` |
| RT56 `common/ideas/_economic.txt` | `DF5D13CB03D713D54E5AF6C6EC3B5754F28CFD1908A24CB7BC6D71F751A7EC49` |
| vanilla `common/national_focus/bulgaria.txt` | `98002B892F0D85AF59CB16489068EF916BFD4D9934E16781F9D2B3D9BA9646CF` |

원본 중점 파일은 donor HEAD `698b6eb`에서 미커밋 변경이 없으며, 기존 중점 입력 commit과의 차이는 이 보상 11행뿐이다. 포트의 새 주석은 저장소의 날짜 표기 규칙에 맞춘다. 경제법은 RT56 `_economic.txt:89,111,268`의 기존 ID를 사용하며 새 정의를 만들지 않는다. 바닐라 `bulgaria.txt:7855–7859`에 같은 국가 범위 조건부 경제법 지급 사례가 있다. compatibility/donor/RT56/vanilla common 검색에서 해당 중점 ID 정의는 compatibility와 donor에 각각 하나, 경제법 정의는 RT56과 vanilla에 각각 하나다. RT56 전역 경제법 정의와 비한국 중점은 수정하지 않는다.

## 검증

변경 전 중점 생성기 `--check`는 20개 모두 통과했다. 통합 원장 `--check`는 변경 전부터 불일치였으며, 위의 기존 한국 국가사 변경을 구분해 보존했다.

- 생성기 실행은 중점 파일 하나만 갱신하고 나머지 19개 출력을 유지했다. 중점 diff는 기존 줄 수정·삭제 없이 완료 보상 11행 추가 하나뿐이다. 출력 SHA-256: `8585302A3BE4E66371A22FEC34602951AA2AF8EC171EAE38F193C9DFC48DFC49`.
- `check_korean_focus_update.py`는 기존 보상 순서·내용 보존, 정확히 하나의 조건부 부분 동원 지급, 민간경제·초기 동원 조건 통과와 부분 동원·전쟁경제·총동원·기타 경제법 조건 불통과를 검사한다. 제한된 소스 모델 검사이며 엔진 실행 증거가 아니다.
- `validate_port.py`: **19 PASS / 0 WARNING / 1 ERROR, exit 1**. 이번 중점의 재생성·의미 계약, 스크립트 구조, 참조·ID와 원장은 통과했다. 유일한 오류는 doctrine migration의 기존 한국 국가사 불일치다.
- `migrate_doctrines.py --check`는 KOR 하나만 불일치, KCH/KJP/RKY/TWN은 통과했다. 읽기 전용으로 예상 bytes와 대조한 결과 차이는 앞서 기록한 전쟁 지지도 한 줄뿐이다. 예상 SHA-256은 `A3026A212ACE14982986ABB7C10B86E8711ACC81972ED3F70172DCF37C7E103B`; 실제 파일은 작업 전 해시 그대로다. 이번 보상 작업에서 그 별도 게임플레이 변경을 수정하거나 승인된 생성 규칙으로 편입하지 않았다.
- 원장 재생성은 1,031행·동일 경로 충돌 73개·기존 분류 수를 유지했다. 중점 reason/hash 외에 기존 국가사 변경의 현재 출력 해시도 기록했다. 이 해시 기록은 국가사 변경을 수정하거나 검증 통과로 승인한 뜻이 아니다. 원장 SHA-256: `3BCC19BE38ED970A252D338B905105292D604AFF2C178B78B8D7DDA0E68CB499`.
- `git diff --check` 통과. 적용 후 donor 중점·RT56 중점·경제법 SHA-256과 RT56 manifest를 다시 확인했으며 모두 위 기준과 같다.
- 게임 실행·playset 변경·커밋·푸시·게시를 하지 않았다. 이전 한국 업데이트의 실행 결과는 이 새 보상에 대한 실행 증거가 아니다. 실제 중점 완료와 기존 세이브에서의 동작은 미검증이다.
