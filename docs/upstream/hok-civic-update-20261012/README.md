# HOK 재벌·시민사회 업데이트 원본 기록 — 2026-10-12

source commit: d4031aaa0c1f85bb89b0e6ca21d041beade8bd26; base commit: 4d8241e3cd33ebbceaca9650ab36b9891a22b56d.

[독립 source lock](../../../tools/hok_civic_update_lock.json)은 수정된 한국 중점·기존 기업 주문 두 파일, 신규 runtime 29개, 변경된 원본 docs 23개의 immutable Git blob과 checkout·출력 해시를 고정한다. runtime/와 documents/docs/ 아래의 사본은 Git blob과 바이트 동일한 감사용 원료이며 production runtime으로 직접 로드되지 않는다. 이 README는 호환판이 추가한 안내이며 donor blob 사본이 아니다.

source_snapshot.py의 civic_update_lock/read_civic_source가 commit→path→blob→사본→checkout을 확인한다. 두 기존 output의 6개·3개 exact-byte hunk만 적용하며 donor 전체 diff를 재구성해 원본 변경 밖의 편집을 거부한다. 호환판의 기존 RT56 지도 ID, 만주 지역, 보상·그림·contributor notes는 hunk 밖에 남는다. 구 KOR_cooperation_with_the_jaebeol ID는 신규 shared-focus 원본에 유지되며 기존 한국 트리의 플레이 가능한 정의는 제거한다.

새 focus GFX의 shine_overlay 26개 참조는 기존 포트와 동일한 vanilla 공유 provider gfx/interface/goals/shine_overlay.dds로 연결한다. HOK 그림과 animationmask는 로컬 payload를 유지한다. 그 외 신규 28개 파일은 원본 checkout의 바이트를 그대로 유지한다. donor root README.md와 .gitattributes, descriptor, AGENTS.md와 이전 source locks는 가져오거나 갱신하지 않았다.

원본의 runtime·UI·저장·DLC 검증 기록은 donor 실행의 증거다. 이 호환판의 RT56 대조 결과나 일반 저장 호환 증명으로 재사용하지 않는다. 새 호환판 구현·검증 한계는 [이식 기록](../../implementation/2026-10-12-korean-civic-update-port.md)을 따른다.

문서·소재 사본 목록:

- [docs/HOK_KOREAN_CHAEBOL_CIVIL_SOCIETY_ASSET_CREDITS.md](documents/docs/HOK_KOREAN_CHAEBOL_CIVIL_SOCIETY_ASSET_CREDITS.md)
- [docs/HOK_KOREAN_CHAEBOL_CIVIL_SOCIETY_RESEARCH_PLAN.md](documents/docs/HOK_KOREAN_CHAEBOL_CIVIL_SOCIETY_RESEARCH_PLAN.md)
- [docs/HOK_KOREAN_CHAEBOL_CIVIL_SOCIETY_REVISION_PLAN.md](documents/docs/HOK_KOREAN_CHAEBOL_CIVIL_SOCIETY_REVISION_PLAN.md)
- [docs/HOK_KOREAN_CHAEBOL_CIVIL_SOCIETY_SPEC.md](documents/docs/HOK_KOREAN_CHAEBOL_CIVIL_SOCIETY_SPEC.md)
- [docs/HOK_KOREAN_FOCUS_LAYOUT_COORDINATES.md](documents/docs/HOK_KOREAN_FOCUS_LAYOUT_COORDINATES.md)
- [docs/HOK_KOREAN_SECOND_WAVE_PLAN.md](documents/docs/HOK_KOREAN_SECOND_WAVE_PLAN.md)
- [docs/assets/korean-civic-decision-icons/category.png](documents/docs/assets/korean-civic-decision-icons/category.png)
- [docs/assets/korean-civic-decision-icons/circle-democracy-mask.png](documents/docs/assets/korean-civic-decision-icons/circle-democracy-mask.png)
- [docs/assets/korean-civic-decision-icons/circle-democracy.png](documents/docs/assets/korean-civic-decision-icons/circle-democracy.png)
- [docs/assets/korean-civic-decision-icons/focuses-industry-mask.png](documents/docs/assets/korean-civic-decision-icons/focuses-industry-mask.png)
- [docs/assets/korean-civic-decision-icons/focuses-industry.png](documents/docs/assets/korean-civic-decision-icons/focuses-industry.png)
- [docs/assets/korean-civic-decision-icons/influence_blue.png](documents/docs/assets/korean-civic-decision-icons/influence_blue.png)
- [docs/assets/korean-civic-decision-icons/sources/CREDITS.txt](documents/docs/assets/korean-civic-decision-icons/sources/CREDITS.txt)
- [docs/assets/korean-civic-decision-icons/sources/Focus & National Spirits Pieces/Blueprints.png](documents/docs/assets/korean-civic-decision-icons/sources/Focus & National Spirits Pieces/Blueprints.png)
- [docs/assets/korean-civic-decision-icons/sources/Focus & National Spirits Pieces/Circular Arrows.png](documents/docs/assets/korean-civic-decision-icons/sources/Focus & National Spirits Pieces/Circular Arrows.png)
- [docs/assets/korean-civic-decision-icons/sources/Focus & National Spirits Pieces/Cog Wheel.png](documents/docs/assets/korean-civic-decision-icons/sources/Focus & National Spirits Pieces/Cog Wheel.png)
- [docs/assets/korean-civic-decision-icons/sources/Focus & National Spirits Pieces/Scales.png](documents/docs/assets/korean-civic-decision-icons/sources/Focus & National Spirits Pieces/Scales.png)
- [docs/assets/korean-civic-decision-icons/sources/Focus Backgrounds/Circle with Ribbon2.png](documents/docs/assets/korean-civic-decision-icons/sources/Focus Backgrounds/Circle with Ribbon2.png)
- [docs/assets/korean-civic-decision-icons/sources/National Spirit Backgrounds/Circle.png](documents/docs/assets/korean-civic-decision-icons/sources/National Spirit Backgrounds/Circle.png)
- [docs/data/HOK_KOREAN_CIVIC_DECISION_ICON_MANIFEST.json](documents/docs/data/HOK_KOREAN_CIVIC_DECISION_ICON_MANIFEST.json)
- [docs/data/HOK_KOREAN_SECOND_WAVE_COORDINATES.json](documents/docs/data/HOK_KOREAN_SECOND_WAVE_COORDINATES.json)
- [docs/incidents/2026-10-12-korean-civic-decision-icons.md](documents/docs/incidents/2026-10-12-korean-civic-decision-icons.md)
- [docs/incidents/2026-10-12-korean-civic-revision.md](documents/docs/incidents/2026-10-12-korean-civic-revision.md)
