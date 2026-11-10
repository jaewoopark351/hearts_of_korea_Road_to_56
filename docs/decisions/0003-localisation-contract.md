# ADR-0003: Localisation 런타임 계약

## 상태

- 기록일: 2026-09-06
- 상태: **Pending Runtime**
- 저장소 정적 정책: 채택
- 최종 권장 플레이세트: 미결정

### 2026-11-10 한국 연구·장비 이름 최초 검토와 후속 실행

한국 장비가 일본식 이름으로 보이는 문제를 조사하거나 수정·검증하기 전에 [한영 수선 계획](../plans/2026-11-10-korean-equipment-localisation-repair-plan.md)을 읽는다. 사용자가 요구한 후속 범위는 한국어·영어 모두이며, 최초 검토는 문서화만 수행했다. 당시 RT56 자체 영어와 한국어 번역의 `KOR_` 장비 키가 HOK와 상충하는 정의를 갖는 것을 확인했고, 사용자가 본 개별 UI의 최종 선택 정의는 미확인이었다. 이 최초 검토만으로 dependencies 변경·광범위한 replace_path·파일명 `zz_` 해결이나 한국어 번역의 필수 의존성화를 채택하지 않았다.

아래 과거 절의 시점별 descriptor·플레이세트 관측은 역사 기록으로 유지한다. 최초 검토 때 호환판 descriptor는 RT56와 Korean Language를 선언했다. 기존 [fixture-04-ko의 실제 공존 기록](../implementation/2026-11-08-hok-upstream-content-port.md#fixture-04-한국어-실행-결과)에서는 RT56 한국어 번역 활성 상태로 HOK 전용 한국어가 표시됐으므로, replace_path 선언만으로 HOK 전체 현지화가 제거된다고 단정하지 않는다. 일부 공존 UI의 확인과 최종 지원 언어 계약의 미결정 상태를 구분한다. 이 최초 안내는 런타임·설정·의존성·잠금·원장 변경이나 새 시험 결과가 아니었다.

이후 별도 승인된 [한영 장비명 구현](../implementation/2026-11-10-korean-equipment-localisation-repair.md)은 기존 장비 원문을 보존하고 한국 전용17값/언어를 재정의한다. v4 동일 경로 한국어1,308키 병합만으로는 KO03·KO04에서 실패했고, 실제 외부 descriptor에 RTK 의존성 한 줄만 추가한 KO05는 관측9문구가 정상으로 바뀌었다. 이 간선을 유지하며 한국어를 좁은17키로 줄인 v5는 KO06의 KLVT-2 전체 제목·해금 안내에서 다시 실패했다. 따라서 v6는 **영어17키·동일 경로 한국어1,308키 병합·정확한 RTK 의존성**을 함께 선택했다. 한국어의17값만 바꾸고 비대상1,291키·나머지 원문 바이트를 보존한다. 독립 소스 검토35/0, aggregate28 PASS/기존11 ERROR(exit1), KO07 한국어 수정15/17문구·보존3문구·JAP 대표7표시를 확인했다. 1953년형2키는 소스 전용이다. EN03은 장비명 관측 없이 중단됐으며 정상 UI 종료를 관측하지 못했다. 영어 재확인 EN04·최종 복구 결과는 구현 기록에 별도로 적는다.

저장소 descriptor는 기존 RT56·Korean Language 선언을 유지하며 `The Road to 56 Korean Translation`을 추가했다. 광범위한 `replace_path`는 추가하지 않았다. 최종 KO07·EN04에서 각각 수정15/17문구·보존3문구·JAP 대표7표시 불일치0을 확인했고, 두 실행 모두 정상 UI 종료·수집·기존82저장 차이0·새 저장0이다. 임시 외부 `.mod`는 원본304바이트·mtime으로, 나머지 사용자 metadata6개도 원본으로 복구했다. 복구 SHA `E0D4D449BE6AB3DF2EC951658BAF79B869BAA548EA5F152CD7395AAFECAED342`는 임시 시험의 종료 기록이며 영구 적용 기록이 아니다. 이후 사용자의 별도 `영구 반영해줘` 승인으로 외부 RTK 의존성37바이트만 영구 동기화했다. 현재 외부 `.mod`는341바이트·SHA `5D5FAB7036D3512BA01EEA4E40C912735A7145A3B7D232E2A7741D1EA7612733`로 시험한 후보와 같고 나머지 metadata는 원본이다. 영구 적용 영수증 `runtime-session/permanent-descriptor-sync/receipt.json`의 SHA는 `D0E130B0ADF78816A9C53C602316DB268D3B8D4E90213827E66C9569BFDAC648`이며 외부 작업 폴더의 세부 위치는 구현 기록을 따른다. 이 적용 뒤 게임을 다시 실행한 결과는 아니며 이미 확인한 후보의 같은 바이트를 동기화했다.

이 ADR 전체는 **Pending Runtime**이다. 차량17값의 선택 구성은 한국어 RT56+RTK+호환판, 영어 RT56+호환판이며 RTK 없는 한국어 구성은 지원 확인 범위에서 제외한다. Korean Language 동시 활성과 모든 번역·외국 GUI·최종 Workshop 의존성 계약까지 해결됐다고 확대하지 않는다. RTK의 replace_path와 descriptor 간선이 만드는 일반 엔진 정렬 규칙도 확정하지 않는다. 해당 계층을 수정·재생성·검증하기 전에 구현 기록과 선택 입력 안내를 읽는다.

### 2026-10-20 영어 채널 이식

호환판의 기존 `localisation/english` 36파일·2,743키를 실제 영국 영어로 교체했다. 일반판 영어 번역 `6f501200f723245636ecf3b246e0d3e74c490422`에서 한국어 원문이 같은 2,691개 값을 재사용하고, 원문이 다른 25개와 호환판 전용 27개는 RT56판에 맞췄다. 일반판 전용 255키는 포함하지 않는다. 한국어 채널·descriptor·의존성은 변경하지 않았다.

호환판 자체에 영어를 제공하는 결정이며, 별도 영어 서브모드를 필수 의존성으로 추가하지 않는다. 기존 일반판 영어 서브모드는 이전 주 ID와 일반판 전용 키를 정의하므로 호환판 영어 검증 구성에서 제외해야 한다. 현재 사용자의 플레이세트에는 그 서브모드와 `replace_path="localisation"`인 RT56 한국어 번역이 함께 활성화되어 있다. 이번 작업에서 플레이세트를 바꾸거나 게임을 실행하지 않았으므로 유효 로드 우선순위와 최종 한국어 의존성 계약은 계속 **Pending Runtime**이다.

출처·병합 판단·검증과 기존 정적 실패는 [영어 이식 기록](../implementation/2026-10-20-english-localisation-import.md)에 구분한다. 아래 2026-09-06 수치와 런타임 논의는 역사 기록이다.

같은 날 후속 [긴급 특별 건함계획 이식](../implementation/2026-10-20-korean-emergency-shipbuilding-port.md)에서 언어당 4키를 더해 현재 각 채널은 37파일·2,747키다. 기존 36파일의 바이트와 일반판 영어 255키 제외 정책은 유지한다. 신규 donor 영어 채널의 한국어 4값만 영국 영어로 번역했으며, 언어 모드 의존성이나 런타임 지원 상태는 바꾸지 않았다.

> 2026-09-06 19:20 후속 상태: 저장소와 launcher descriptor는 현재 `The Road to 56` 및 `Korean Language`를 선언한다. 실제 실행은 `The Road to 56 Korean Translation`을 활성화하고 `Korean Language`를 활성화하지 않았다. 따라서 아래 “RT56만 dependency”는 1차 구현 당시 결정 기록이며 현재 파일 상태가 아니다. 어느 구성을 최종 지원할지는 여전히 미결정이다.

## 맥락

HOK donor descriptor는 `Korean Language`를 필수 의존성으로 선언했다. 반면 2026-09-06 14:06 실패 플레이세트는 `The Road to 56 Korean Translation`을 사용했고, 이 번역 모드는 `replace_path="localisation"`을 선언한다. 두 구성의 실제 로드 결과를 비교하지 않은 채 한쪽을 필수 dependency로 고정하면 HOK 키가 숨거나 RT56 번역이 사라질 수 있다.

## 2026-09-06 1차 구현 당시 결정

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

이 절을 작성할 당시 외부 launcher `.mod`는 과거 Korean Language-only dependency를 유지해 저장소 descriptor와 불일치했다. 당시에는 읽기 전용 범위라 수정하지 않았다. 이후 실제 외부 파일의 시점별 의존성과 승인된 임시 시험·복구는 위 2026-11-10 구현 기록을 따른다. 다른 C0/C1 시험 전에 launcher 항목의 실제 경로·의존성을 재확인해야 한다.

런타임 비교가 끝나기 전에는 어느 한국어 모드도 “공식 필수 구성”으로 문서화하지 않는다.
