# 2026-09-06 1차 포트 정적 검증

> 이 문서는 1차 정책 당시의 역사적 검증 기록이다. ADR-0004 후속 결과는 [한국 우선 후속 정적 검증](2026-09-06-korea-first-static-validation.md)을 본다.
>
> 후속 감사에서 이 검사가 coastal province와 `naval_base_spawn` 좌표 coverage를 확인하지 않았음이 드러났다. 항구 7행 보정과 새 gate는 [한국 해안 항구 배치 closure 보정](../implementation/2026-09-06-map-building-closure-fix.md)에 기록하며, 아래 역사적 결과는 소급 변경하지 않는다.

## 판정

- aggregate static gate: **PASS 15 / WARN 0 / ERROR 0**
- Python 도구 구문 검사: 통과
- 작성한 문서·도구·descriptor 대상 diff whitespace 검사: 통과
- HOI4 실행/엔진 파싱: 미실행
- 런타임 호환 판정: **미검증**

이 결과는 저장소 산출물이 고정된 donor/RT56/바닐라 입력에서 재현되고, 구현한 정적 invariant를 만족한다는 뜻이다. launcher가 올바른 모드를 로드하거나 게임이 시작·진행된다는 뜻은 아니다.

## 기준선

| 항목 | 값 |
|---|---|
| 작업 기준 commit | `main@70aaba43a98fd429378ec1a67d4398f16330e101` |
| 작업 트리 | 미커밋 구현 변경 있음 |
| HOK donor | `main@887930f6e88c80568d62dab9cfbe1ba8a498a252`, clean/read-only |
| RT56 Workshop manifest | `3323396725579032799` |
| RT56 descriptor SHA-256 | `5B323861ABD63E31CB896277E3EA58BA4BCD9FCEEDA957B50792065E42E03F61` |
| 대상 로그의 HOI4 | `1.19.2.0.a729`, Steam build `23969257` |
| 최신 로그 | 구현 전 2026-09-06 14:06 실행; 이후 실행 없음 |

## 실행 명령

```powershell
python tools\validate_port.py
python -B -c "import ast,pathlib; files=list(pathlib.Path('tools').glob('*.py')); [ast.parse(p.read_text(encoding='utf-8'), filename=str(p)) for p in files]"
git diff --check -- README.md AGENTS.md descriptor.mod docs tools
```

최종 Python 구문 검사는 파일을 쓰지 않는 AST parse로 수행했다. 이전 검사 중 생긴 `tools/__pycache__`는 제거했고, aggregate validator도 하위 생성기를 `-B`로 실행하므로 최종 트리에 cache가 없다.

## Aggregate gate 결과

`python tools\validate_port.py`의 최종 결과:

1. RT56 기반 map 합성 재현
2. shared/global override 합성 재현
3. East Asia override와 현재 일본 OOB/평화 AI 리베이스 재현
4. RT56 소유 파일 삭제 상태 재현
5. 비한국 FIN/MON/SIB 및 고아 자산 pruning 재현
6. HOK province/state/event/achievement/localisation ID 이식 재현
7. HOI4 1.19 교리 마이그레이션 재현
8. donor 1,014개 integration manifest 재현
9. Paradox Script 132개 UTF-8 파일의 괄호·따옴표 구조 검사
10. descriptor의 RT56-only dependency와 금지 필드 부재
11. 폐기 ID·모듈·빈 event picture token 부재
12. localisation 36개 파일, 3,614개 key의 BOM/header/내부 중복 검사
13. 주요 HOK event의 영어·한국어 키와 picture 참조 확인
14. state/event/focus tree/focus/character/MIO/achievement 논리 ID 중복 검사
15. 필수 KOR 인물·AI·MIO·이름·map·`PHI_free` localisation merge assertion

출력 요약은 `SUMMARY pass=15 warning=0 error=0`이었다.

추가 자산 참조 감사에서는 마지막 고아 decision/event/focus 그림 3개와 그 sprite 정의를 제거한 뒤 재검사했다. 감사한 자산 범위에서는 외부 launcher 불일치와 미실행 런타임 검증 외에 남은 정적 HIGH/MEDIUM/LOW finding이 없었다.

## 지도 정적 검사

- RT56 province `1–13534`와 전 세계 definition/RGB 보존
- HOK province `13414–13447` → `13535–13568`
- compat state 집합 `525`, `527`, `528`, `917–920`, `1144–1147`
- 정의되지 않은 province/state 참조와 중복 ID/RGB 검사
- bitmap/definition, state/strategic region membership closure
- building, railway, supply node, unit-stack 참조 closure
- HOK-vs-바닐라 한국 bitmap delta 1,889픽셀만 RT56 base에 합성

이는 실제 해안 판정, adjacency, 항구·철도·보급과 unit 위치의 엔진 동작을 증명하지 않는다.

## Source drift와 파일 분류

모든 생성기는 사용하는 외부 입력의 SHA-256을 고정한다. RT56/바닐라/donor source가 바뀌면 자동으로 새 결과를 수용하지 않고 검사를 실패시킨다.

[1,014개 분류 CSV](../audits/2026-09-06-production-file-classification.csv)는 모든 donor 프로덕션/root 파일을 다음처럼 분류한다.

| 분류 | 수 |
|---|---:|
| ADD | 119 |
| USE_RT56 | 85 |
| THREE_WAY_MERGE | 30 |
| OVERRIDE | 7 |
| BINARY_MERGE | 18 |
| ASSET_COPY | 755 |
| 합계 | 1,014 |

구현 전 RT56 exact-path 충돌 73개는 모두 명시 분류를 거쳤다. 바닐라와 같은 경로인 공용 파일도 vanilla-base `THREE_WAY_MERGE`로 추적한다.

## Whitespace 검사 해석

`git diff --check -- README.md AGENTS.md descriptor.mod docs tools`는 통과했다. 전체 `git diff --check`는 RT56/바닐라에서 리베이스한 대형 whole-file 산출물 안의 기존 trailing whitespace와 space-before-tab 때문에 종료 코드 1을 반환했다. 이 whitespace는 pinned host bytes에 포함된 부분이며, Paradox Script 동작·해시·upstream 비교를 흐리는 대량 정규화를 하지 않았다. 구조 검사는 별도로 통과했다.

## 남은 런타임 blocker와 위험

### HIGH — launcher descriptor 불일치

저장소 `descriptor.mod`는 `0.1.0-dev`, 새 표시명, RT56-only dependency다. 외부 사용자 데이터의 `mod/hearts_of_korea_Road_to_56.mod`는 여전히 `version="1.0.0"`, 과거 표시명, Korean Language-only dependency이며 저장소 path를 가리킨다. 외부 파일은 읽기 전용 범위라 수정하지 않았다.

C0/C1 실행 전에 launcher 항목을 재가져오거나 별도 허가로 갱신하고 실제 물리 경로와 dependency를 확인해야 한다.

### 미실행

- R0: RT56 단독
- R1: RT56 + 선택 localisation
- C0: RT56 + compat
- C1: RT56 + 선택 localisation + compat
- main menu, 한국 선택, 새 게임, 지도 진입과 unpause
- 정부·법·idea·focus·decision·event·OOB·equipment·character·portrait
- supply, railway, adjacency, 해안과 naval placement
- DLC별 경로, AI 장기 실행, save round trip와 multiplayer sync
- RT56 단독에서 이미 발생할 수 있는 항공기 icon scope 오류 등 host baseline 분리

따라서 이 기록은 “정적 포팅 1차 구현 완료”의 근거이지 “RT56 호환판 완료”의 근거가 아니다.

## Git과 외부 행동

- 커밋/푸시/tag/merge: 없음
- 게임 실행: 없음
- launcher/playset/user-data 수정: 없음
- Steam/Workshop 게시·업로드: 없음
- donor, RT56 Workshop와 HOI4 설치 원본 수정: 없음
