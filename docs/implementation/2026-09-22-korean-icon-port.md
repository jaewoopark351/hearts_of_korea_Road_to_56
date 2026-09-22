# 2026-09-22 HOK 한국 아이콘·작업 규칙 이식

상태: **이미지·연결·AGENTS 반영 / 대상 정적 검사 통과 / 전체 정적 19 PASS·0 WARNING·기존 불일치 1 ERROR / 새 이미지의 포트 런타임 미실행**.

## 범위와 동작

사용자는 자신이 원본 HoK 제작자임을 밝혔으며, 앞선 읽기 전용 검토 후 `C:\hoi\hearts_of_korea`의 새 이미지와 작업 규칙 이식을 요청했다. 한국 중점 60개와 국민정신 정의 29개에 전용 그림·분야별 배경색·강화 단계 표시를 적용한다. 이번 작업은 시각 업데이트이며 게임플레이 수정이나 호환성 복구를 주장하지 않는다.

| 대상 | 이식 내용 | 분류 |
|---|---|---|
| `gfx/interface/goals/HOK_KOR/` | 최신 색상 DDS 60개, 원본과 바이트 동일 | ASSET_COPY |
| `gfx/interface/ideas/HOK_KOR/` | 최신 색상 DDS 29개, 원본과 바이트 동일 | ASSET_COPY |
| `interface/HOK_KOR_focus_icons.gfx` | 일반 sprite 60개 | ADD |
| `interface/HOK_KOR_focus_icons_shine.gfx` | 광택 sprite 60개 | ADD |
| `interface/HOK_KOR_spirit_icons.gfx` | 국민정신 sprite 29개 | ADD |
| `common/national_focus/korea.txt` | 새 중점 60개의 `icon`과 이식 주석만 변경 | 기존 OVERRIDE 유지, 시각 delta |
| `common/ideas/HOK_KOR_{industry,military,democratic}_expansion.txt` | `picture` 11·12·6개와 이식 주석만 변경 | 기존 ADD 유지, 시각 delta |
| `AGENTS.md` | 사용자 저작자 정보, HOK 아트 제작·상대경로·출처·색상 규칙 | 포트 지침의 선별 병합 |

기존 중점 266개, 한국·만주 지도 ID 변환, RT56 만주 15개 주 처리, 독립당 부분동원령 보상, 중점 효과·기간·배치·AI 및 국민정신 수치를 보존한다. 새 아이콘의 게임 ID는 기존 `HOK_KOR_`를 유지한다. 기존 사용자 변경인 한국 시작 history와 부분동원령 관련 수정도 유지했다.

## 기준선과 출처

- 포트 작업 시작: `feat/korean-focus-update-20260922` / `d2bd30358e15ada7c2768d536409ec282ce4ecda`. 중점·한국 history·생성기·검사·원장 등에 기존 미커밋 변경이 있었으며 이번 diff와 구분한다.
- 원본: `feat/korean-focus-expansion-ai` / `698b6eb160efbaa04a4d43846330ba002f5e8cc7`. 새 그림과 연결은 **이 커밋에 포함되지 않은 작업 트리 변경**이다.
- [아이콘 입력 잠금](../../tools/hok_icon_lock.json)은 DDS/GFX 92개, 연결 소스 4개, 관련 문서·갤러리 37개의 정확한 크기와 SHA-256을 기록한다. `base_commit`은 당시 HEAD이며 이 파일들이 해당 커밋에 들어 있다는 뜻이 아니다.
- 원본 아이콘 매니페스트 SHA-256: `F2A3861583EB540E872B1D722A0B620E6F5B2D570003A2D9FCF0F87EB60FCDE9`.
- RT56: Workshop `820260968`, manifest `7475007536894105204`, `timeupdated=1788822864`. descriptor SHA-256 `5B323861ABD63E31CB896277E3EA58BA4BCD9FCEEDA957B50792065E42E03F61`.
- 현재 설치·기존 실행 증거: HOI4 `1.19.3.0.c01a (5e4e)`, build `2026-09-09 09:10:08`, Windows 11, DLC 36개, `l_korean`, OneDrive 문서의 HOI4 사용자 데이터. 이 로그는 2026-09-22 13:10의 **원본 단독 실행**이다.
- 현재 launcher 목록은 `mod/hearts of korea.mod` 하나, 물리 경로는 원본 저장소다. 이번 이식에서는 설정을 변경하거나 게임을 실행하지 않았다. 기존 포트 C1/C0와 구분하며, 포트 테스트에서는 원본을 끄고 RT56+포트 구성을 사용해야 한다.
- 포트 descriptor와 launcher descriptor의 기존 ID `3796816200`, `The Road to 56`·`Korean Language` 의존성을 유지한다. RT56 번역의 localisation replacement와 언어 계약은 이번 작업에서 변경하지 않는다.

## 생성과 재현

기존 gameplay Git 스냅샷 1,031개를 변경하지 않고 별도 artwork 입력을 겹친다. [source_snapshot.py](../../tools/source_snapshot.py)의 `--import-icons`는 잠금과 정확히 일치하는 원본 파일만 `.local-artifacts/sources/hok-icons-20260922`에 복사한다. 파일이 다르면 덮어쓰거나 해시를 자동 갱신하지 않는다. 원본 파일·Git 상태는 수정하지 않는다.

[build_korean_focus_update.py](../../tools/build_korean_focus_update.py)는 기존 20개 입력의 지도·만주·부분동원 보정을 먼저 적용한 뒤 승인된 60/29개 그림 참조만 바꾸고 DDS/GFX 92개를 복사한다. 수정 전 포트 출력 4개의 해시를 고정하여 독립 변경을 덮어쓰지 않는다. 입력의 출처와 검증된 출력은 별도이며 원본 `korea.txt` 전체를 포트에 덮어쓰지 않는다.

```text
python tools/source_snapshot.py --import-icons
python tools/build_korean_focus_update.py
python tools/build_integration_manifest.py --apply
python tools/validate_port.py
```

입력이 준비된 뒤의 `--check`는 원본 최신 작업 트리를 자동 수입하지 않고 고정 캐시를 확인한다. 새 입력을 선택하려면 별도 출처·merge 검토가 필요하다. 이 환경에서는 PATH에 `python`이 없어 기존 Codex runtime의 Python 실행 파일을 절대경로로 사용했다. 도구나 패키지를 새로 설치하지 않았다.

[통합 원장](../audits/2026-09-06-production-file-classification.csv)은 기존 1,031행과 새 자산 92행을 합쳐 1,123행이다. ASSET_COPY 863, ADD 139, THREE_WAY_MERGE 31, OVERRIDE 9, BINARY_MERGE 18, USE_RT56 63이며 기존 exact-path RT56 충돌은 73개다. 새 artwork 96개 관련 행에 `artwork_source_kind`, `artwork_source_base_commit`, `artwork_source_sha256`를 추가했다. 미커밋 자산의 Git commit/blob 열은 비워 두어 출처를 오인하지 않게 한다.

## 아트 규칙·문서

원본의 [크레딧](../HOK_KOREAN_FOCUS_ICON_CREDITS.md), [매니페스트](../data/HOK_KOREAN_FOCUS_ICON_MANIFEST.json), [색상 비교](../assets/korean-focus-icon-colors/index.html), 계획 및 작업 기록을 보존했다. 이 문서들의 이전 실행 결과는 원본에서 수행한 작업의 기록이며 포트의 실행 증거가 아니다. 외부 소재는 Ultimate HOI4 GFX 고정 커밋 `3626dc83c8573d6603fa497138090b04b64a15ba`에서 채택한 48개 부품이며, 보존된 upstream CREDITS와 가공 내역을 유지한다.

복사한 두 계획서의 선행 설계 링크 4곳은 포트에 없는 역사적 문서를 가리키므로 형제 원본 저장소의 해당 문서로 연결했다. 이 링크는 이 작업 공간의 `C:\hoi\hearts_of_korea`를 전제로 하며, 공개 문서 패키지를 준비할 때 별도 정리해야 한다. 문서 링크 외 내용과 나머지 35개 문서·갤러리 파일은 원본 바이트를 유지한다.

AGENTS의 새 로컬 이미지 규칙은 HOK 전용 payload·sprite에 적용한다. RT56 소유 콘텐츠의 모든 그림을 복제하도록 확대하지 않는다. 광택은 목표 vanilla와 동일한 공용 `gfx/interface/goals/shine_overlay.dds`와 `gfx/FX/buttonstate.lua` 효과 식별자를 유지한다. 후자는 실제 `.lua` 파일의 존재를 요구하는 파일 참조로 바꾸지 않는다. vanilla `goals.gfx:9581`, `goals_shine.gfx:67004`, `ideas.gfx:530`을 schema counterpart로 확인했다.

## 검증과 남은 범위

- 새 sprite prefix와 상대경로를 포트·RT56·vanilla·두 언어 모드에서 조사했다. 새 등록 이전 충돌 없음.
- `check_korean_focus_update.py --check`: **PASS**. 60/29 매핑, DDS 89개 해시·BGRA32·알파·크기, sprite 149개·공용 광택 참조, 네 스크립트의 순서 보존 의미 비교 및 기존 게임플레이 계약을 검사했다.
- 독립 byte 역비교: **PASS**. 새 그림 참조와 이번 주석 60/6/11/12개만 되돌리면 작업 전 네 파일과 바이트 단위로 동일하다.
- 전체 `validate_port.py`: **19 PASS / 0 WARNING / 1 ERROR**. `migrate_doctrines.py --check`만 기존 KOR history 불일치로 실패한다. `[Man the Guns]` 분기의 `set_war_support = 0.1#20260922_kpopmodder`는 생성기 기대 `0.05`와 다르다. 이식 전 원장의 KOR 출력 해시와 현재 파일 해시가 `243FC1FBDE8DB75B82CCFEBD6BB01CA7001DABCD944CA8534E7324413705BE30`으로 일치하므로 이번 이미지 이식 이전의 변경임을 확인했다. 기존 게임플레이 변경을 되돌리거나 검사를 약화하지 않았다.
- 새 아이콘의 RT56 포트 UI, 중점 잠금·진행·완료·광택, 국민정신 획득·교체·수혜국 표시, 세이브·멀티플레이는 **NOT RUN**.

원본·Steam·게임 설치본·사용자 설정에 쓰지 않았으며 commit, push, 업로드 또는 Workshop metadata 변경을 하지 않았다.
