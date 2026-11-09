# 2026-11-09 검토 후속 수리의 고정 선행 입력

이 폴더는 후속 수리 생성기를 재현하거나 역사적 핀을 검증할 때 읽는다. 시험 출력·백업 작업 폴더가 아니라, 호환판 `f8fdd821cf80dd291b02a59b55e8d85fe558a9b3` 위의 승인된 수리에 필요한 **바이트 고정 source capsule**이다.

`before/`의 네 파일은 `C:\hoi\hearts_of_korea_Road_to_56`에서 수리 전에 확인한 런타임 출력이다. HOK donor나 RT56의 새 원본을 복사한 것으로 해석하지 않는다. 기존 통합 원장의 HOK·donor 개정·RT56·번역 출처와 저작자 표시는 유지된다. 이 폴더의 inherited 내용을 새 제작물로 표시하지 않는다.

- 원본 Git commit/blob, 원본 Git 바이트 해시, 관측한 checkout 바이트·크기와 이후 출력 해시는 [후속 잠금](../../../tools/hok_review_followup_lock.json)에 분리해 기록한다.
- [후속 생성 계층](../../../tools/review_followup.py)은 이 네 선행 파일에 제한된 수리만 적용한다. [독립 검사](../../../tools/check_review_followup.py)는 생성 모듈을 import하지 않고 허용한 표시 metadata·한영 키와 부유항 한 행의 변경을 대조한다.
- 과거 civic/분할/11월 콘텐츠/RT56 잠금과 그 source capsule은 수정하지 않는다. 등록된 새 최종 해시를 정확히 입증한 경우에만 이 폴더의 이전 바이트로 역투영한다.
- 현재 source cache `C:\hoi\test\hok-rt56-source-cache\sources\`와 별개다. 임시 도구·테스트 결과·UI 증거는 `C:\hoi\test\hok-rt56-review-followup-20261109-01\`에 저장하며 이 폴더에 넣지 않는다.

수리 범위와 미관측 UI 후보는 [수선 계획](../../plans/2026-11-09-localisation-state-review-followup-plan.md)을 따른다. 이 source capsule의 존재와 정적 재현은 실제 엔진 표시·효과·저장 호환성의 증거가 아니다.
