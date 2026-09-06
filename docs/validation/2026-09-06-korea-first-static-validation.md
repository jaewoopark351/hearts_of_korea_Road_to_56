# 2026-09-06 한국 우선 후속 정적 검증

> 후속 감사에서 별도 map/buildings 항구 coverage 공백을 발견했다. 항구 7행 보정과 현재 정적 결과는 [한국 해안 항구 배치 closure 보정](../implementation/2026-09-06-map-building-closure-fix.md)을 본다. 아래 결과는 이 수정 전 당시 기록이다.

## 판정

**한국 자산·KOR 기술 gate 통과 / aggregate clean 미달**

- 결과: `15 PASS / 0 WARNING / 1 ERROR`
- 유일한 오류: donor 현행 song 목록에 등록되지 않은 `music/Minshu_ikki.ogg`가 작업 중 다시 나타나 Korea-only pruning과 불일치
- HOI4 런타임: 미실행

## 실행 명령

```powershell
python -B tools\build_korean_assets.py --check
python -B tools\migrate_doctrines.py --check
python -B tools\prune_rt56_owned_files.py --check
python -B tools\build_integration_manifest.py --check
python -B tools\validate_port.py
```

첫 네 개의 대상 검사는 통과했다. aggregate validator에서 통과한 항목은 다음과 같다.

- RT56 기반 지도 합성
- 공용·동아시아 override 재현성
- HOK-first 한국 음성·기본 항공기 자산 재현성
- RT56-owned pruning
- HOK ID·교리/기술 migration
- 1,014행 integration manifest
- 133개 Paradox Script 파일 구조
- 현재 descriptor 정적 계약
- 폐기 runtime ID/token
- localisation 36개 파일, 3,614개 key
- HOK event localisation/picture 참조
- 주요 논리 ID 유일성
- 필수 KOR merge assertion

실패한 항목은 `prune_non_korean_content.py --check` 하나다. 출력의 마지막 차이는 다음과 같다.

```text
present   music/Minshu_ikki.ogg
```

이 파일은 20:13:59에 다시 생성됐고 donor와 같은 byte copy다. donor `hok_music.asset`에는 일본 민주화 테마로 정의돼 있지만, donor commit `b3ec30e`는 `hok_songs.txt`에서 `JAP_proclaim_the_republic`만 조건으로 하던 등록 블록을 제거했다. 같은 이름의 `KOR_minshu_ikki` focus도 존재하지만 음악 재생 효과는 없다. 기존 포팅에서는 삭제된 구형 JAP focus의 고아 곡으로 분류했으나, 동시 사용자 변경과 새 HOK 보존 원칙 사이의 선택이 필요하므로 자동 삭제하지 않았다.

## 한국 자산 검증 범위

- HOK WAV 18개가 donor SHA-256과 일치
- HOK 기본 항공기 mesh 3개와 texture 9개가 donor SHA-256과 일치
- donor `sound/voice_korea.asset` 부재
- compat `sound/r56_vo_Korean.asset` 재현성
- HOK `Positive_005`, 재생 목록과 `volume=1.0` 포함
- RT56-only WAV 두 개를 merged registry가 참조하지 않음
- `hok_rt56_` 기본 항공기 mesh/entity ID가 pinned RT56 source에서 미사용
- HOK graphic DB가 새 entity를 소비
- medium entity가 RT56 `supply` state를 유지

## KOR 기술 검증 범위

- `bba_early_transport_plane`, `early_transport_plane`이 compat `set_technology`에서 제거됨
- 두 ID가 pinned RT56의 활성 기술 정의에 없음
- RT56 `transport_plane_equipment_1`이 `active = yes`
- 임의의 1940 수송기 기술이나 dummy alias를 부여하지 않음

## 한계

정적 검사는 exact-path override의 실제 VFS 승자, 엔진 asset registration, 음성 출력, DDS UV, 3D 모델 scale/animation, 새 게임 crash, paused map, unpause, localisation UI, AI, save와 multiplayer를 증명하지 않는다. 19:20 로그는 이번 보정 전 산출물이다.
