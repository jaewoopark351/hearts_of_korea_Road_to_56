# 민주인사 지원·비밀 정보국 시각 자산 출처

작성: 2026-11-18 (Asia/Seoul). [기능 계획](HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_PLAN.md)의 한국 신규 정보국 중점·국민정신과 중국·일본 지원 결정에 연결하는 이미지 6개를 기록한다. 이번 작업은 **선정된 기존 완성본의 바이트 그대로 복사와 프로젝트 전용 GFX 연결**이다. 신규 원화·AI 이미지·재색칠·리샘플링을 만들지 않았으며, 기존 지원 중점의 원화와 다른 소비자는 바꾸지 않았다.

소스·출력 SHA-256, 치수·채널·알파, sprite·picture, 원본 선언, 검사 범위는 [전용 자산 매니페스트](data/HOK_KOREAN_DEMOCRATIC_SUPPORT_INTELLIGENCE_ASSET_MANIFEST.json)에 기록한다. 신규 게임 효과와 실제 UI 검증은 이 자산 출처 기록만으로 통과 처리하지 않는다.

## 영국 중점과 국민정신

읽기 전용 원본은 `C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV`의 `Operation Postern v1.19.5.0.7c6c (c184)` 설치본이다. 원저작은 **Paradox Interactive 및 해당 권리자**에게 있으며 개별 그림의 작가 이름은 확인되지 않았다. 영국 원본을 계속개발 팀의 신규 원화나 공개 소재 팩으로 표시하지 않는다.

재사용 근거는 [Paradox Interactive User Agreement](https://legal.paradoxplaza.com/eula)의 5절 User Generated Content를 2026-11-18 읽어 확인한 내용이다(문서의 최종 갱신 표시는 2026-01-21). 이 비상업 HOI4 모드에서 선정한 공식 출시 게임 자산을 사용하며, 원본 권리의 이전이나 독립적인 오픈소스 이미지 라이선스를 주장하지 않는다. 영국에서 참고한 정보국 중점은 `La Resistance` 조건 아래에 표시하고 원본 게임·DLC의 이용 권한을 우회하는 대체 콘텐츠로 배포하지 않는다.

| 용도 | 원본 선언·DDS | 이번 내부 사본·GFX |
|---|---|---|
| 눈 문양 중점 | `common/national_focus/uk.txt` 329행 → `interface/goals.gfx` 3399–3400행 → `gfx/interface/goals/focus_generic_secret_service_agency.dds` | `gfx/interface/goals/HOK_KOR/democratic_intelligence/secret_intelligence_service.dds`; `GFX_HOK_KOR_focus_secret_intelligence_service` |
| 중점 광택 | `interface/goals_shine.gfx` 21686–21714행; `gfx/interface/goals/shine_overlay.dds` | 같은 프로젝트 폴더의 `shine_overlay.dds`; `GFX_HOK_KOR_focus_secret_intelligence_service_shine` |
| 국민정신 그림 | `common/ideas/britain.txt` 675–678행 `ENG_mi6_ns`, `picture = generic_spy_intel` → `interface/ideas.gfx` 673–674행 → `gfx/interface/ideas/generic_spy_intel.dds` | `gfx/interface/ideas/HOK_KOR/democratic_intelligence/secret_intelligence_service.dds`; `picture = HOK_KOR_secret_intelligence_service`, `GFX_idea_HOK_KOR_secret_intelligence_service` |

세 파일의 소스·출력 바이트와 SHA-256이 각각 일치한다. 중점은 원본 100×88, 국민정신은 원본 **58×63**, 광택 오버레이는 원본 **87×88**을 유지한다. 국민정신을 신규 합성 이미지의 일반 기준인 60×68로 확대하지 않았다. 원본 국민정신 DDS의 헤더는 row pitch 대신 전체 선형 바이트 크기를 기록하는 `DDSD_LINEARSIZE` 형식이며, 이를 포함해 수정하지 않았다.

중점 광택의 회전·시간·혼합·배율은 영국 정의와 같고, 텍스처·두 마스크는 내부 중점 DDS를, 두 오버레이는 내부 광택 DDS를 참조한다. `gfx/FX/buttonstate.lua`는 이미지가 아닌 기존 엔진 효과 스크립트 참조다. [일반 GFX](../interface/HOK_KOR_democratic_support_intelligence.gfx)와 [광택 GFX](../interface/HOK_KOR_democratic_support_intelligence_shine.gfx)는 바닐라 전역 sprite를 덮어쓰지 않는 프로젝트 전용 이름을 사용한다.

민주 가지의 신규 배경 기준은 짙은 파랑이지만, 이번 정보국은 사용자가 선정한 영국 눈 문양·MI6 그림의 원형 보존을 우선한 재사용 범위다. 배경만 바꾸기 위한 추가 이미지 편집을 하지 않았으며, 이 예외를 기존 민주 아이콘 전체의 색상 변경으로 확대하지 않는다.

## 민주인사 지원 결정 소형 이미지

기존 [시민사회 자산 출처](HOK_KOREAN_CHAEBOL_CIVIL_SOCIETY_ASSET_CREDITS.md)와 [시민 결정 아이콘 매니페스트](data/HOK_KOREAN_CIVIC_DECISION_ICON_MANIFEST.json)의 완성 DDS를 그대로 재사용했다. 원화는 **Globvs / Ultimate HOI4 GFX contributors**, 기존 소형 합성·파랑 배경 가공은 **kpopmodder**의 기여다. 이번 작업의 기여는 선정·전용 파일 복사·새 sprite 연결이며 원화를 새로 그렸다는 뜻이 아니다.

고정 출처는 [Ultimate HOI4 GFX의 3626dc83c8573d6603fa497138090b04b64a15ba](https://github.com/Globvs/Ultimate-HOI4-GFX/tree/3626dc83c8573d6603fa497138090b04b64a15ba)다. 해당 팩의 [CREDITS 원문 보존본](assets/korean-civic-decision-icons/sources/CREDITS.txt)을 읽고 기여자 동의와 자유로운 사용 문구·크레딧을 확인했다. 원문 SHA-256은 `cf220dc66463d75163f7690ad77b02b662d0c05ca5d53dc62d33ed504512a7f5`다. 이 근거는 위 기존 합성물에 사용한 팩 소재에 한정하며, 별도 MIT·CC 라이선스나 기여자들이 속한 다른 모드 전체의 허가를 추정하지 않는다. 개별 부품과 개인 작가의 일대일 대응은 원문에 없다.

| 용도 | 기존 사본 | 새 전용 사본·sprite | 크기 |
|---|---|---|---|
| 지원 범주 | `gfx/interface/decisions/HOK_KOR/civic/category.dds` | `gfx/interface/decisions/HOK_KOR/democratic_support/category.dds`; `GFX_HOK_KOR_decision_category_democratic_support` | 51×40 |
| 일본 지원 행 | `gfx/interface/decisions/HOK_KOR/civic/influence_blue.dds` | 같은 새 폴더의 `support_democracy_in_japan.dds`; `GFX_HOK_KOR_decision_support_democracy_in_japan` | 32×32 |
| 중국 지원 행 | 같은 파란 시민영향 그림 | 같은 새 폴더의 `support_democracy_in_china.dds`; `GFX_HOK_KOR_decision_support_democracy_in_china` | 32×32 |

지원 행 두 개는 민주주의 지지 기반 지원이라는 같은 기능을 뜻하므로 파란 저울 소재를 공유한다. 원래 민주 배경 기준 RGB(53,91,126), 금속 테두리·저울·알파·32×32 크기를 그대로 유지한다. 범주는 기존 시민사회 협력 헤더의 설계도·톱니·순환 화살표와 산업 회색 배경을 그대로 채택했다. 이 헤더를 민주 파랑으로 새로 가공하지 않았으며 범주의 색이 파랑이라고 기록하지 않는다. 큰 중점·정신 DDS를 결정 행에 직접 연결하지 않았다.

## 확인과 남은 범위

정적 확인은 6개 최종 DDS의 소스 바이트 일치, 전체 SHA-256, 치수·BGRA32·알파·단일 프레임, 새 sprite의 저장소 내 유일성, 텍스처·마스크·오버레이의 대소문자 일치와 저장소 내부 경로 해석을 포함한다. 원본 파일과 기존 시민 DDS는 수정하지 않았다.

실제 텍스처 크기의 외부 연락시트에서 눈 문양·첩보원 그림·범주 헤더·파란 저울의 가독성과 투명 여백을 직접 확인했다. 이는 게임 화면이 아니다. 연락시트·개별 PNG 미리보기·DDS 검사 helper·실제 검사 결과는 `C:\hoi\test\hok-democratic-support-intelligence-20261118-01\assets\`에만 두었으며, 프로젝트 문서의 매니페스트는 그 위치와 출처를 찾는 유지용 색인이다. 과거 보관 경로의 합성기·원본 팩은 현재 확인되지 않아 재실행하거나 다시 찾았다고 기록하지 않았다.

이 하위 작업은 게임을 실행하지 않았다. 잠김·사용 가능·진행·완료·광택, 국민정신 툴팁, 결정의 가용·불가·진행 표시 및 타 모드의 실제 덮어쓰기는 후속 실행에서 검증해야 한다. 커밋·푸시·외부 게시를 하지 않았다.
