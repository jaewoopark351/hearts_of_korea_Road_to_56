# 2026-09-22 RT56·HOI4 입력 기준선 재검토

## 범위와 상태

한국 중점 업데이트에 앞서 기존 생성기의 입력 해시를 실제 설치 파일과 대조했다. 이 기록은 **source 감사와 검토된 pin 갱신**의 근거다. 이 감사에서는 생성기 build/check, aggregate validator와 HOI4 실행을 하지 않았다. 산출물 재생성과 정적·런타임 결과는 후속 구현 기록에서 별도로 확정한다.

- compatibility 기준: `main@bfbba43c26022f3f64a88c2f1ec6600cb7f0d06f` 및 이번 병행 구현의 미커밋 변경.
- RT56 item: `820260968`; 기존 manifest `3323396725579032799` → 현재 `7475007536894105204`.
- 실제 설치·실행 로그: HOI4 `1.19.3.0.c01a (d4e7)`, build time `2026-09-09 09:10:08`.
- 기존 source pin 200개: RT56 38개 중 9개 변경, vanilla 17개 중 1개 변경, 현재 donor 145개 중 2개 변경. 나머지는 SHA-256 일치다. 이 범위가 RT56 전체 파일 감사를 뜻하지는 않는다.
- 감사 종료 시 RT56·vanilla 55개 입력 hash와 RT56 manifest를 다시 읽었으며 감사 도중 변경은 없었다.
- donor의 `events/SEA_Japan.txt`와 `history/countries/TWN - Taiwan.txt` 변경은 한국 중점 이식 범위 밖이다. 이 두 pin을 최신 donor에 맞춰 갱신하지 않고, 별도 고정 donor 입력 구성에서 기존 내용을 유지한다.
- 재검토 자료: `.local-artifacts/audits/2026-09-22/`의 `source-pin-audit.json`, `source-pin-audit.csv`, `map-source-drift.json`, `building-placement-drift.json`, `current-host-map-baseline.json`. 이는 로컬 감사 자료이며 배포 산출물이 아니다.

## RT56 변경과 병합 결정

구 RT56 원본 전체 보존본 대신 기존 compatibility 생성 산출물과 생성기의 한국 변환을 함께 읽어 현 host 차이를 구분했다. 지도는 행 순서·공백 차이와 실제 행/좌표 차이를 분리했다. 다음 9개 입력은 현 RT56을 base로 사용하고 기존 한국 delta를 그대로 재적용한다.

| 입력 | 확인된 host 변경 | 보존할 한국 delta |
|---|---|---|
| `events/WTT_Japan.txt` | 국경전 승리·패배에서 `JAP_win_the_border_war_flag`/`JAP_lose_the_border_war_flag` 사용 | 한국 추가 주 집합, 쓰시마 이전, 기존 `921 → 920` 수정 |
| `map/buildings.txt` | 인도네시아 8개 주의 배치 변경, floating harbor 소속 3행 수정 | 한국 재분류 150행, HOK 21행, 항구 7행·air/rocket site 3행 복원 |
| `map/railways.txt` | `2 6 12299 13447 4424 7427 4412 10297`에서 `13447 → 13531` | 기존 한국 4개 경로 교체와 HOK 34행 추가 |
| `map/supply_nodes.txt` | `4608` 제거, `7421`·`13520` 추가 | HOK 보급 노드 6개 |
| `map/unitstacks.txt` | province `391, 3211, 6598, 9498`의 zoom 38 좌표 수정 | 이식한 HOK province의 536행 |
| `common/military_industrial_organization/organizations/00_generic_organization.txt` | BRA/MEX 등 국가 적용 조건, modern SPG, 경항공 CAS·연구 범주, 중폭격기 범주·아이콘 등 host 수정 | generic tank MIO의 KOR 제외 한 줄 |
| `common/scripted_triggers/unit_medals_scripted_triggers.txt` | 체코슬로바키아 훈장 trigger 추가와 aggregate 정리 | 한국 훈장 trigger·aggregate 등록 |
| `common/bookmarks/the_gathering_storm.txt` | 중국 참조를 `KMT_end_the_peoples_tutelage`, `KMT_redefine_democracy`로 갱신 | 기존 KOR bookmark 블록 |
| `history/general/generic_advisors.txt` | generic military adviser 대상에서 `GUK` 제외 | 한국 자체 인물을 가진 세 역할의 기존 제외 |

### 지도 세부 근거

RT56 `definition.csv`, `provinces.bmp`, 고정한 한국 state/region 입력은 기존 hash와 같다. 전체 현 RT56 province 최대 ID는 `13534`, state 최대 ID는 `1143`이다. 포트의 신규 province `13535–13568` 및 state `1144–1147`과 겹치지 않는다. 전체 RGB 수와 province 행 수는 각각 13,535개(ID 0 포함)다.

기존 생성 건물 71,905행에서 HOK 추가·복원 31행을 분리한 기존 host 행 수는 71,874행이다. 현 RT56은 71,863행으로 11행 줄었다. state 필드 뒤의 실제 배치를 비교하면 변경·삭제 356행과 변경·추가 345행은 모두 `668, 673, 909, 974, 975, 978, 1135, 1143`에 속하고, 한국 배치 자체의 변경은 없다. 같은 배치의 state 필드만 다른 153행 중 150행은 기존 한국 재분류이며, 나머지 3행은 현 host의 floating harbor 소속 변경 `872 → 521`, `871 → 522`, `668 → 975`다.

따라서 생성기의 총행수 assertion은 **71,863 + 21 + 7 + 3 = 71,894**로 갱신한다. 한국 재분류 수, 원본 행 allowlist, 중복·좌표·ID·coverage 검사는 그대로 둔다. 현 host bitmap을 직접 샘플한 coastal-without-port 집합도 기존 `{490, 1201, 10715}`와 같다. 이는 현 host 조사 결과이며 새 compatibility 산출물의 생성·coverage 검사를 대신하지 않는다.

## Vanilla 참조 입력

`common/doctrines/grand_doctrines/sea_grand_doctrines.txt`는 `migrate_doctrines.py`가 `new_convoy_raiding`의 top-level 존재를 확인하는 참조 입력이며 파일 내용을 복사하지 않는다. 현 파일에 해당 ID가 활성 상태이고 `folder = naval`, `xp_type = navy`, 기존 네 track을 사용하는 정의가 있음을 확인했다. RT56의 동일 상대경로 override는 없다. 기존 country-history migration과 기술 지급 내용은 바꾸지 않고 1.19.3 참조 hash만 고정한다.

구 vanilla 파일 전체 보존본은 확보하지 못했다. 이 결정은 생성기가 사용하는 ID 계약을 재확인한 것이며, 해군 교리의 모든 수치·동작이 이전 버전과 같다는 주장이 아니다.

## SHA-256 변경 기록

| source·상대경로 | 이전 | 현재 |
|---|---|---|
| RT56 `events/WTT_Japan.txt` | `F5CDB2146F9618D20B38CF085465BA541926059D3B359170ADFDE4635DA65418` | `E843DB20E3166F74D8303798ADB1CF5D3DE31475CC1C941051592F90362919C5` |
| RT56 `map/buildings.txt` | `5622673138F7269FA433E80CA19B49F5C48B52E7AA386568F4E6C3E96B0F99BB` | `807C419FEB4CB107BFE73EBFE82FEA01B895977751F01D604A3C8ACE1FB3B42E` |
| RT56 `map/railways.txt` | `ECBDBFE17B5463019A3952F0B17887552F2AF6301D99F6BD5E22FEAA39566ECE` | `0CFEF6244DF5A04A8EBE0C1027C27287C375F31CBDA94F265FC549DF6CC61547` |
| RT56 `map/supply_nodes.txt` | `45595220BDE8C7B7FC9CEAD07A0EB4C5F48370548B51C0950520AB58EF83716F` | `3C5D4998860ECFEBE8EF234D7756E450B0051D3D6C031C308855A84D3A41B1AD` |
| RT56 `map/unitstacks.txt` | `82C382B0D0BBF8944199A45A459BCB90B3A612E9D29996C1FC8BCE3C935998F4` | `CF3B8BB6736F61F216D5BB789024795135A62E49BD669BD94721091CE177018C` |
| RT56 `common/military_industrial_organization/organizations/00_generic_organization.txt` | `8208BE0FEF7FDFAF6AF5BC3F2D5D9E978968B62FFEF006922D34998034C8884B` | `C701A3CFF92AF46925932241E156B9B5F340FAEDCF228BB103F74B985F6F5D35` |
| RT56 `common/scripted_triggers/unit_medals_scripted_triggers.txt` | `1AB7D40F88B1206EF048FC7FCA9D5A8F31AEEE70794BCA33C3A568326E329054` | `A103BF15A3BA3F4A0788A7C14F97A575307C28DFFCEFBC2EAEE1718070E503BB` |
| RT56 `common/bookmarks/the_gathering_storm.txt` | `B51785BA529E1999560A5C2AF7C647C90F52D036F1115BEF0C4587D5CD78FCB1` | `064C1ABB1475B8EBFD4E53CAB3D4DCE77CE37B4BE0A0A9EE6EA53988FB36F3B9` |
| RT56 `history/general/generic_advisors.txt` | `8195C4530185414B23873DC25B3AD627E51970B5E4516273BD22F2DA650DA1AF` | `4EA203FEF355255ABB28A7E59DCEDD3926C764D5CC4844C2B3D9B2269A65923C` |
| vanilla `common/doctrines/grand_doctrines/sea_grand_doctrines.txt` | `CBDF40318B122C9CB54558348D7FC689787800A0CF9E14E16690EB3C5E738D88` | `110FDEAD1B621C4C54B54E58D9A78EF40A1EF4113A976FD3F6680E7A5BE0B5CF` |

## 실행 전제와 남은 검증

감사 시 기존 실행은 활성 DLC 36개·donor HOK 한 개이며 설정 언어는 `l_korean`이었다. 이 실행의 진행 로그는 포트 실행 증거가 아니다. compatibility 저장소·외부 launcher descriptor는 RT56와 Korean Language 및 compatibility item `3796816200`을 선언하며 외부 path는 이 저장소를 가리킨다. RT56 Korean Translation의 `replace_path="localisation"`과 최종 언어 계약은 별도 검증 대상으로 유지한다.

후속 구현은 새 입력으로 생성 재현·통합 원장·aggregate gate를 검사하고 donor 없는 R0/C0를 기록해야 한다. 이 감사만으로 기존 새 게임 크래시의 해소, 한국 중점·보상·AI 또는 새 지도 동작을 통과했다고 판정하지 않는다. 외부 원본·launcher·사용자 로그·세이브는 변경하지 않았고 커밋·푸시·게시도 하지 않았다.
