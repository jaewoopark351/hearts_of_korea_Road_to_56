# RT56 2026-11-08 자동 갱신의 별도 입력 계층

이 계층을 수정·재생성·검증할 때 [AGENTS.md](../../../AGENTS.md), [한국 콘텐츠 구현 기록](../../implementation/2026-11-08-hok-upstream-content-port.md), [호스트 잠금](../../../tools/rt56_host_update_lock.json), [이식 결정](../../decisions/0008-november-rt56-host-update.md)을 먼저 읽는다. 한국 콘텐츠32개와 기존15주 분할의 이전 입력·출력 핀은 이 갱신의 새 기준으로 덮어쓰지 않는다.

## 원본과 사본

- 설치 원본: `C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968`. Steam 관리·읽기 전용이다.
- 이전 manifest: `7553774178744855191`. 11월8일22:04:14 KST 시작한 기존 C0-02까지의 기준이다.
- 현재 manifest: `1963361040482473746`. Steam 로그의22:20:17 감지,22:20:53 다운로드 시작,22:21:27 완료로 자동 갱신을 확인했다. 이 작업의 도구가 설치 원본을 수정한 결과가 아니다.
- 전체 감사 사본: `C:\hoi\test\hok-rt56-upstream-20261108-01\host-drift\rt56-1963361040482473746\`. 28,746파일·1,373,729,636바이트를 전후 경로·크기·SHA-256·디렉터리와 비교했다. 감사용 사본이며 기존 활성 source cache를 대체하지 않는다.
- 전체 검증/차이 인덱스: 같은 외부 `host-drift/verification.json`, `current-full-before.json`, `current-full-after.json`, `audit-copy-full.json`, `baseline-covered-diff-full.json`.

이전 목록4,806개는 전체 RT56가 아니라 선택 텍스트 폴더·확장자와 일부 지도/루트 파일의 지문이었다. 같은 수집 범위에서184개 변경·8개 삭제·25개 신규·4,614개 동일이다. 현재 전체 중 이전에 수집하지 않은23,923경로를 모두 신규라고 부르지 않는다.

## 저장소 안의 유지 입력

| 경로 | 역할 |
|---|---|
| `host/` | 새 manifest의 병합 대상4개 원문. 한국 외 콘텐츠의 직접 기준 |
| `compat_before/` | 새 호스트 대응 직전 호환판4개. HOK 카드·전용 MIO 보호·기존 한국 연결과 이전 출력 해시의 기준 |
| `previous_host/` | 이전755의 SEA/JAP 원문2개. 과거 외부 `hok-rt56-state-split-20261107-01/host-before/rt56/`와 이전 잠금 SHA가 일치하는 사본 |
| `legacy_shared/` | 기존 생성기의755 기반9주 중간 출력2개. 이전47출력을 정확히 재생하는 명시적 입력이며 새 runtime은 아님 |
| `host-current-inputs.json` | 같은 수집 범위의 새4,823경로 지문. 삭제8개는 잠금에 별도 기록 |
| `host-transition.json` | 이전/현재 지문과184/8/25의 경로별 구분. 공개 문서용 출처 인덱스이며 실제 효과 판정이 아님 |
| `ledger_before.csv` | 한국 콘텐츠32개 통합까지의 원장. 새4행 변경의 정확한 조상 |

각 파일의 SHA-256과 역할은 잠금의 `files`, `outputs`, `legacy_bridge`, `legacy_shared_inputs`로 연결한다. 이전755 원문이 없는 일반 변경 파일은 해시 전환만 기록한다. 특히 generic MIO의 기존 포트는755 직전에도 더 오래된 호스트 원문을 포함했으므로, 최신196 전체 MIO에 기존 한국 제외 한 항목만 합성한다.755 MIO 원문을 복구했다고 주장하지 않는다.

자원탐사 검사에 쓰이는 RT56 `localisation/english/wtt_decisions_l_english.yml`도 기록된 A86B…→C833…의 정확한 전환만 허용한다. 새 원문의 `prospect_for_resources`, `prospect_for_resources_desc`, `repeatable_decision_tt`는 각각1개이며 영어 값으로 존재하고 포트에서 덮어쓰지 않는다. 새 RT56 영어 전체와 HOK 탐사4키의 충돌은 없으며 기존 탐사6출력은 이번 작업 시작 때와 동일하다. 옛 RT56 A86B… 본문은 확보하지 못했으므로 문구 전체의 이전/현재 차이를 복구했다고 주장하지 않는다. 새 원문을 상속하며 자원탐사 잠금 자체와 HOK 보상·비용·문구는 변경하지 않는다.

## 생성과 검증 경계

`tools/rt56_host_update.py`는 한국 콘텐츠32개 뒤에 호스트4개만 추가로 합성한다. 이전47개와32개 잠금은 보존하며, 정확히 등록된 새 최종/중간 바이트만 이전 바이트로 역투영할 수 있다. 다른 manifest·이전/현재 해시 쌍·독립 수정 파일은 거부한다. 현재의4,823개 물리 입력·삭제8개·한국32개·지도24개·L-08 보호 해시도 따로 확인한다.

시험 helper·보고서·미리보기는 `C:\hoi\test\hok-rt56-upstream-20261108-01\host-adaptation\`에 둔다. 새 실행 driver는 `new-host-session/driver/session.py`, 별도 백업·실행별 증거는 `new-host-session/session/`에 있다. 이전 `session/`의 실행과 결과를 새 호스트의 통과로 읽지 않는다. 실제 진행·UI·효과·저장/재로드·복구 결과는 구현 기록에서 별도로 갱신한다.
