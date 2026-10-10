# HOK 왕정 업데이트 원본 기록 — 2026-10-10

source commit: 4d8241e3cd33ebbceaca9650ab36b9891a22b56d; base commit: af6fccf2248311c01565c796555ed334ec685015.

[독립 source lock](../../../tools/hok_royal_update_lock.json)은 두 runtime Git blob과 원본 변경 docs7개의 immutable object SHA-256/크기/사본 경로를 고정한다. documents/docs 아래는 Git blob과 바이트 동일한 읽기 전용 증거 사본이다. source_snapshot.py의 royal_update_lock()이 각각 검사한다. 이 README는 호환판이 추가한 안내이며 donor blob 사본이 아니다.

중점·왕정 정신 runtime은 immutable Git objects에서 선택한 span으로만 기존 호환판 생성기에 반영한다. 원본 전체 runtime을 새 cache로 복사하지 않았다. 역사적 pins와 이전 사본은 그대로다. 원본 계획·좌표·incident의 실행 결과는 원본 전용이며 호환판의 실행 증거로 사용하지 않는다.

새 호환판 변경·정적 검사·실행 한계는 [이식 기록](../../implementation/2026-10-10-korean-royal-update-port.md), 현재 포트 좌표는 [좌표 명세](../../HOK_KOREAN_ROYAL_LAYOUT_COORDINATES.md)를 따른다.

사본 목록:

- [docs/HOK_KOREAN_FOCUS_LAYOUT_COORDINATES.md](documents/docs/HOK_KOREAN_FOCUS_LAYOUT_COORDINATES.md)
- [docs/HOK_KOREAN_ROYAL_FOLLOWUP_SPEC.md](documents/docs/HOK_KOREAN_ROYAL_FOLLOWUP_SPEC.md)
- [docs/HOK_KOREAN_ROYAL_PREREQUISITE_LAYOUT_PLAN.md](documents/docs/HOK_KOREAN_ROYAL_PREREQUISITE_LAYOUT_PLAN.md)
- [docs/HOK_KOREAN_SECOND_WAVE_PLAN.md](documents/docs/HOK_KOREAN_SECOND_WAVE_PLAN.md)
- [docs/data/HOK_KOREAN_SECOND_WAVE_CANDIDATES.json](documents/docs/data/HOK_KOREAN_SECOND_WAVE_CANDIDATES.json)
- [docs/data/HOK_KOREAN_SECOND_WAVE_COORDINATES.json](documents/docs/data/HOK_KOREAN_SECOND_WAVE_COORDINATES.json)
- [docs/incidents/2026-10-10-korean-royal-prerequisites-layout.md](documents/docs/incidents/2026-10-10-korean-royal-prerequisites-layout.md)
