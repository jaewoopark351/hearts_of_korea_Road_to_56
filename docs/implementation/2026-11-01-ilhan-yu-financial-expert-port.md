# 2026-11-01 유일한 재정 전문가 특성 선택 이식

## 범위와 출처

업데이트된 HOK 원본의 유일한 고문 특성을 호환판에 선택 이식한다. `KOR_economist`를 기존 원본/RT56 특성 `financial_expert`로 교체하는 의도적인 고문 효과 변경이다. 기존 효과에 소비재 혜택을 추가하는 변경이나 호환성 오류 수리로 기록하지 않는다.

- 호환판 시작: `feat/korean-focus-update-20260922@bd9aaea27a55005a3524842cb87d39cafa1d9860`, 작업 트리 깨끗함.
- donor: `feat/korean-focus-expansion-ai@f79cebfbb92518f478d8258bd406b52d3a1ae6d6` 위의 미커밋 변경. `common/characters/KOR.txt`의 특성 참조 한 줄을 교체하고 기여 주석 한 줄을 추가한 `2 insertion / 1 deletion`이다.
- donor 변경 후 `KOR.txt` SHA-256: `EC8EEEC8BA2A3055BE8F01466353A0575330C87660CE90E0663A461838D8C2D8`.
- 호환판 변경 전 `KOR.txt` SHA-256: `5BA8DD65773AF64E656697CB95B4C887A6231A603AE9C481334B4A5939A8BE31`.
- 호환판 변경 후 `KOR.txt` SHA-256: `53B0C839A1FC188C8D3AE062B4A5CF795574ABA41123B6E3333ED6028DDC5E0B`.
- donor [별도 구현 기록](../../../hearts_of_korea/docs/incidents/2026-11-01-ilhan-yu-financial-expert.md) SHA-256: `B21D4B882C6DABCF3E82EEFFA200EBDC314F1F5D0B1AEF491F8907FA9A4781CD`. 이 기록은 donor의 소스 대조이며 호환판 게임 실행 결과가 아니다.
- RT56: Workshop `820260968`, manifest `7553774178744855191`; 현재 `common/characters/KOR.txt` SHA-256 `979185140DA5A9CA57AC8399A47DA5EBFA9157C9FD2F2AACBD51E7E4E8C078CA`.

donor의 캐릭터 파일 전체를 덮지 않고 기존 RT56/HOK 병합 위의 유일한 advisor trait에만 적용한다. 기존 통합 원장의 `THREE_WAY_MERGE` 분류는 유지한다. 원장이 생성한 행과 캐릭터 runtime 파일의 생성 소유권은 별개이며, 현재 runtime 생성기의 출력 맵은 이 `KOR.txt`를 소유하지 않는다. 새 생성 체계나 의존성을 추가하지 않고 좁은 직접 수정과 기존 원장 갱신으로 기록한다.

## 설치와 실제 로드 구성

설치 기준은 `Operation Postern 1.19.4.1.99a5`, Steam build `26282552`, 기존 인벤토리 checksum `f584`다. RT56 manifest와 관련 물리 파일을 이번 비교에서 다시 확인했다. descriptor의 `supported_version`만으로 현재 버전이나 실행 성공을 판단하지 않는다.

| 항목 | 현재 읽기 전용 확인 |
|---|---|
| 활성 playset | `한국test01`: donor `C:/hoi/hearts_of_korea` → 일반판 영어 번역 `C:/hoi/Hearts of Korea English Translation Anime Modder's Edition` |
| 비활성 대상 playset | `Road to 56 한국 테스트`: enabled 위치 0 현재 호환판 → 1 RT56 Korean Translation `2769576030` → 2 RT56 `820260968`; donor 없음 |
| 언어·DLC | `l_korean`, `disabled_dlcs=[]`; 실제 보유·인식 DLC별 고용 효과를 검증한 목록이 아님 |
| 사용자 데이터 | `C:/Users/jaewo/OneDrive/문서/Paradox Interactive/Hearts of Iron IV` |
| 호환판 launcher | 현재 호환판 root, 기존 item `3796816200`, RT56 + Korean Language 의존성 유지 |

구성·descriptor·관련 출처 해시는 외부 `C:/hoi/test/hok-rt56-ilhan-yu-20261101/baseline-context.json`에 기록했다. 목록 순서는 엔진의 유효 우선순위 증거가 아니다. 대상의 RT56 Korean Translation은 선언된 Korean Language와 다른 모드이고 `replace_path="localisation"`을 사용하므로 최종 언어 계약은 계속 별도 실행 대조 대상이다. donor incident의 당시 활성 구성 서술을 현재 인벤토리로 사용하지 않는다.

이번에는 게임을 새로 실행하거나 launcher·선택 목록·설정·저장·설치본·Workshop을 변경하지 않았다. 원본과 RT56는 읽기 전용 출처이며 호환판에만 이번 runtime delta를 적용했다.

## 변경 효과와 보존

| 항목 | 직전 | 적용 |
|---|---|---|
| 유일한 고문 특성 참조 | `KOR_economist` | `financial_expert` |
| 해당 특성의 효과 | `production_factory_max_efficiency_factor=0.05`, 생산 효율 상한 +5% | `consumer_goods_factor=-0.15`, 소비재 공장 변동치 −15% |
| trait AI 평가 | `ai_will_do.factor=2` | 동일 |

소비재 **변동치 −15%**는 소비재 비율을 직접 15%p 낮춘다는 뜻이 아니다. 생산 효율 상한 혜택은 이 고문에게서 대체되며 두 특성을 함께 부여하거나 전역 보너스를 새로 추가하지 않는다. 실제 국가의 최종 소비재 수치는 경제법·다른 보정 등 해당 게임의 계산에 따라 달라지므로 고정 공장 수 감소를 약속하지 않는다.

현재 RT56 `common/country_leader/00_traits.txt:8514`와 설치 vanilla 같은 파일 `:8522`는 모두 `financial_expert`에 `consumer_goods_factor=-0.15`, AI factor 2를 정의한다. 설치본 `common/characters/ARG.txt:1889`의 정치 고문 역할도 같은 특성을 사용한다. 호환판은 기존 정의를 참조하며 전역 `00_traits.txt`를 복사·수정하지 않는다. 기존 HOK `common/country_leader/00_hok_traits.txt:158`의 `KOR_economist`도 다른 소비자를 위해 보존한다.

다음 계약은 그대로 유지한다.

- `KOR_Ilhan_Yu`, `name=KOR_ilhan_yu`, `idea_token=ilhan_yu`, 정치 고문 슬롯과 별도 비용을 지정하지 않는 기존 방식.
- `GFX_Portrait_KOR_Ilhan_Yu_small`, 이름·초상·sprite·asset 경로와 영어/한국어 현지화.
- `original_tag=KOR`, `KOR_eight_province_development_committee` 완료 해금 조건 및 해당 중점의 `show_ideas_tooltip=ilhan_yu`.
- `history/countries/KOR - Korea.txt`의 시작 `recruit_character=KOR_Ilhan_Yu`와 기존 모집·해고 흐름.
- 다른 캐릭터의 정의·순서·역할·조건·특성, RT56 병합과 기존 한국 콘텐츠 전체.

실제 수정은 donor의 기여 주석과 trait 참조 두 줄이다. 유일한 블록의 다른 바이트와 파일의 나머지를 보존하며, ID·namespace·파일명·로드 순서·저장 migration을 추가하지 않는다.

## 검증과 통합 원장

이전 전체 정적 결과는 **21 PASS / 0 WARNING / 6 ERROR**였다. 기존 여섯 실패는 map synthesis·Korean building placements·shared overrides·East Asia overrides·doctrine migration의 소스 drift 다섯 gate와 second-wave material-cycle의 `descriptor.mod` 보존 해시 gate다. 이번 고문 변경에서 그 핀이나 검사를 완화하지 않았다.

외부 `scope-audit.json`은 캐릭터 ID 73개·순서 보존, 유일한의 trait만 AST 교체, 해당 주석·특성의 정확한 역적용으로 이전 전체 원문 복원 및 변경 후 해시 `53B0C839…DDC5E0B` 일치를 확인했다. 기존 advisor의 다른 필드와 파일의 나머지는 바이트 그대로다. RT56와 vanilla의 해당 특성 값은 각각 `-0.15`, AI factor는 2로 확인했다. runtime 변경은 `common/characters/KOR.txt` 한 개다. 이는 소스·참조·원문 보존 확인이며 엔진 고용 효과 검증이 아니다.

기존 manifest 도구의 이 캐릭터 파일 사유에 donor commit·전체 소스 해시·incident 경로를 기록하고 원장을 재생성했다. 독립 `ledger-audit.json`은 **1,505행·같은 상대경로 충돌 73개·기존 분류**와 출처 키를 확인했다. 해당 KOR 행의 `reason`·`output_sha256`만 바뀌고 다른 1,504행은 그대로다. 같은 행의 RT56 base 해시와 기존 호스트 참조·MAN sibling 출력 두 개의 해시도 유지했다. metadata 도구 변경·CSV 갱신은 이 출처 기록을 재현하기 위한 변경이다.

최종 전체 정적 검사는 **21 PASS / 0 WARNING / 6 ERROR**다. 기존의 map·Korean building placements·shared overrides·East Asia·doctrine 소스 핀 다섯 실패와 descriptor 보존 해시 한 실패가 그대로이며 새 실패는 없다. script 216파일·locale 85파일·5,627키의 구조·현지화 검사와 이번 캐릭터 범위·참조·원장 검사는 통과했다. 이 결과는 전체 포트 정적 통과나 실제 고용 효과의 실행 검증을 뜻하지 않는다.

기존 donor/민주 배치 보관본과 source lock은 수정하지 않았다. 테스트·임시 도구·보고서는 외부 `C:/hoi/test/hok-rt56-ilhan-yu-20261101/`에 두고, 전체 결과는 `final-validation.txt`에 보존한다. 이번 작업에서 게임 실행·설정 변경·커밋·푸시·업로드는 수행하지 않았다.

donor incident는 새 게임·고용 UI·기존 저장을 실행하지 않은 소스·정적 대조다. 이전 민주 배치·기능 연동 실행을 이 고문 효과의 검증으로 재사용하지 않는다. 호환판에서의 해금 전 고용 차단, 정상 해금·고용 후 특성 표시와 소비재 효과, 고용한 상태의 저장 반영·해고/재고용·다른 모드/DLC·멀티플레이는 **UNPROVEN**이다. 기존 저장의 효과가 자동 갱신된다고 약속하거나 강제 migration을 넣지 않는다.

작업은 호환판의 작업 트리 변경으로 남긴다. 커밋·푸시·Workshop 게시·업로드는 이번 요청에 포함하지 않는다.
