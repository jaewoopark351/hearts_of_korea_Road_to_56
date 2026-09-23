# 고정 HOK 2차 업데이트 출처 자료

이 폴더의 원본 문서 37개는 HOK donor 커밋 `be5fb40dbd8de33e5adbf65e808bcb0e8c283560`에서 선택하여 **바이트 그대로** 보존했다. 출처는 읽기 전용 `C:/hoi/hearts_of_korea`이며, 각 문서의 Git blob, checkout 방식, SHA-256과 크기는 [입력 잠금](../../../tools/hok_second_wave_lock.json)의 `documentation`에 기록한다. 원본 `docs/` 아래 상대 위치를 이 폴더 아래에 그대로 유지한다.

이 문서들이 설명하는 게임 동작, 검수, 이미지 수량, 좌표와 제안은 해당 시점 **HOK 원본의 기록**이다. RT56 호환판의 구현 결과나 실제 실행 검증을 뜻하지 않는다. 현재 이식 범위와 통합 결정은 [호환판 이식 계획](../../plans/2026-09-23-korean-second-wave-port-plan.md) 및 호환판 구현 기록을 따른다. 원본의 저자·공개 팩·개별 출처 표시는 보존하며, HOK 원작자라는 사용자의 현재 확인을 과거 문서의 인적 서술로 덮어쓰지 않는다.

원본 자료의 상대 링크는 수정하지 않았다. 이 선별 보존본에 포함되지 않은 `assets/` 접촉표, 과거 사건 문서, 제작 스크립트, `.local-artifacts/`와 원시 검수 자료는 원본 저장소의 동명 위치를 가리키는 역사적 참조다. 이 폴더에 없다는 이유로 게임 runtime 파일이 누락되었다고 해석하지 않는다. 개별 출처 문서의 참조를 보려면 위 고정 커밋에서 원본 상대경로를 확인한다. 원시 로그·세이브·개인 설정과 전체 donor는 복사하지 않았다.

공유 광택은 원본 문서의 `gfx/interface/goals/HOK_KOR/shine_overlay.dds` 로컬 사본을 가져오지 않고, 호환판에서 유지하는 vanilla 공급 경로 `gfx/interface/goals/shine_overlay.dds`를 사용한다. 이 변환은 호환판 생성기가 소유하며 원본 출처 문서는 수정하지 않는다. 그림 연결 전체가 독립적인 자산 묶음이라고 주장하지 않는다.

선별 문서는 `tools/source_snapshot.py --export-second-wave-docs`가 생성한다. `--check`는 37개 문서의 원본 바이트를 확인하며, 다르거나 없는 문서를 조용히 덮어쓰지 않는다. 이 README는 호환판의 보존 경계를 설명하는 별도 문서다.
