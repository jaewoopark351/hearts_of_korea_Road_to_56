# ADR-0003: Localisation 런타임 계약

## 상태

- 기록일: 2026-09-06
- 상태: **Pending Runtime**
- 저장소 정적 정책: 채택
- 최종 권장 플레이세트: 미결정

> 2026-09-06 19:20 후속 상태: 저장소와 launcher descriptor는 현재 `The Road to 56` 및 `Korean Language`를 선언한다. 실제 실행은 `The Road to 56 Korean Translation`을 활성화하고 `Korean Language`를 활성화하지 않았다. 따라서 아래 “RT56만 dependency”는 1차 구현 당시 결정 기록이며 현재 파일 상태가 아니다. 어느 구성을 최종 지원할지는 여전히 미결정이다.

## 맥락

HOK donor descriptor는 `Korean Language`를 필수 의존성으로 선언했다. 반면 2026-09-06 14:06 실패 플레이세트는 `The Road to 56 Korean Translation`을 사용했고, 이 번역 모드는 `replace_path="localisation"`을 선언한다. 두 구성의 실제 로드 결과를 비교하지 않은 채 한쪽을 필수 dependency로 고정하면 HOK 키가 숨거나 RT56 번역이 사라질 수 있다.

## 현재 결정

1. 저장소 `descriptor.mod`는 `The Road to 56`만 필수 dependency로 선언한다.
2. HOK donor, Korean Language와 RT56 Korean Translation은 현재 필수 dependency로 선언하지 않는다.
3. compat에는 필요한 HOK `l_english`와 `l_korean` 파일을 함께 둔다.
4. 기존 localisation key, `$KEY$` 치환, 아이콘·색상 토큰과 UTF-8 BOM을 보존한다.
5. 두 한국어 모드를 한 플레이세트에서 함께 켜는 것을 기본값으로 가정하지 않는다.

정적 검사에서는 36개 localisation 파일, 3,614개 key의 BOM, locale header와 compat 내부 중복이 통과했고 주요 HOK event 및 `PHI_free` cosmetic tag의 영·한 키가 존재함을 확인했다. 제거한 MON 도전 모듈이 기본 몽골 국명을 덮어쓰던 8개 키, runtime 참조가 없는 일본 공화국 cosmetic 9개, RAJ cosmetic 1개와 미등록 일본 음악 1개도 양 locale에서 제외했다. 이는 launcher/engine이 그 파일을 실제로 선택하거나 UI에 올바르게 표시한다는 증거가 아니다.

## 필요한 대조군

| ID | 구성 | 확인 목적 |
|---|---|---|
| R0 | RT56 | host의 기본 키와 경고 기준 |
| R1-KL | RT56 + Korean Language | donor의 과거 언어 계약 확인 |
| R1-RTK | RT56 + RT56 Korean Translation | `replace_path`가 host 번역에 미치는 영향 확인 |
| C0 | RT56 + compat | compat 자체 영·한 키와 fallback 확인 |
| C1-KL | RT56 + Korean Language + compat | Korean Language 지원 여부 |
| C1-RTK | RT56 + RT56 Korean Translation + compat | RT56 번역과 compat 키 공존 여부 |

각 조합에서 launcher의 실제 물리 경로와 로드 순서를 기록하고 영어·한국어 UI에서 다음을 확인한다.

- KOR 국가명, state명, focus, decision, event, idea, character와 MIO 문자열
- `$KEY$`, colour/icon token과 줄바꿈 렌더링
- 누락 key 표출, 잘못된 fallback과 중복 override
- RT56 Korean Translation을 켰을 때 HOK key가 숨는지 여부
- 번역 모드 없이도 최소 영어 UI가 완결되는지 여부

## 보류된 결정

런타임 결과에 따라 다음 중 하나를 후속 ADR로 확정한다.

- RT56 + Korean Language + compat
- RT56 + RT56 Korean Translation + compat
- compat 자체 locale을 기본으로 두고 번역 모드를 선택 지원

현재 외부 launcher `.mod`는 과거 Korean Language-only dependency를 유지해 저장소 descriptor와 불일치한다. 이 파일은 읽기 전용 범위라 수정하지 않았다. C0/C1 시험 전에 launcher 항목을 재가져오거나 별도 허가로 갱신하고 경로·의존성을 재확인해야 한다.

런타임 비교가 끝나기 전에는 어느 한국어 모드도 “공식 필수 구성”으로 문서화하지 않는다.
