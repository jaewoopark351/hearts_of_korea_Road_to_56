#!/usr/bin/env python3
"""Build the complete donor-to-compat integration classification ledger.

The input tree is read-only.  The generated CSV covers every non-Git,
non-documentation file in the pinned HOK donor snapshot and refuses to rely on
the default ADD/ASSET_COPY rules for any exact-path RT56 collision.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from build_rt56_map import HOK_ROOT, REPO_ROOT, RT56_ROOT


OUTPUT = REPO_ROOT / "docs/audits/2026-09-06-production-file-classification.csv"
EXPECTED_DONOR_FILES = 1014
EXPECTED_RT56_COLLISIONS = 73

BINARY_SUFFIXES = {
    ".anim",
    ".bmp",
    ".dds",
    ".mesh",
    ".ogg",
    ".png",
    ".tga",
    ".wav",
}


@dataclass(frozen=True)
class Rule:
    integration_class: str
    outputs: tuple[str, ...] = ()
    reason: str = ""


def same_path(integration_class: str, reason: str) -> Rule:
    return Rule(integration_class, ("{same}",), reason)


EXPLICIT: dict[str, Rule] = {
    # Project/release metadata is authored for the successor, not inherited.
    "AGENTS.md": same_path("OVERRIDE", "신규 포트의 작업·안전·검증 계약"),
    "README.md": same_path("OVERRIDE", "신규 포트의 사용자 안내와 현재 상태"),
    "descriptor.mod": same_path("OVERRIDE", "RT56 전용 의존성과 신규 업로드 정체성"),

    # RT56/global systems that must not be shadowed by stale donor copies.
    "common/difficulty_settings/00_difficulty.txt": Rule(
        "USE_RT56", reason="현재 RT56 난이도 정의가 공용 시스템을 소유"
    ),
    "common/on_actions/04_mtg_on_actions.txt": Rule(
        "USE_RT56", reason="현재 RT56 MTG on_action을 그대로 사용"
    ),
    "gfx/loadingscreens/load_10.dds": Rule(
        "USE_RT56", reason="공유 RT56 로딩 화면을 중복 선적하지 않음"
    ),
    "gfx/loadingscreens/load_11.dds": Rule(
        "USE_RT56", reason="공유 RT56 로딩 화면을 중복 선적하지 않음"
    ),
    "gfx/models/units/planes/KOR_plane_heavy_diffuse.dds": same_path(
        "ASSET_COPY", "HOK 한국 대형기 mesh와 짝을 이루는 원본 diffuse payload"
    ),
    "gfx/models/units/planes/KOR_plane_light_diffuse.dds": same_path(
        "ASSET_COPY", "HOK 한국 경량기 mesh와 짝을 이루는 원본 diffuse payload"
    ),
    "gfx/models/units/planes/KOR_plane_medium_diffuse.dds": same_path(
        "ASSET_COPY", "HOK 한국 중형기 mesh와 짝을 이루는 원본 diffuse payload"
    ),
    "sound/voice_korea.asset": Rule(
        "THREE_WAY_MERGE",
        ("sound/r56_vo_Korean.asset",),
        "RT56 category/compressor에 HOK 음원·재생 목록·volume을 병합한 단일 registry",
    ),

    # Optional non-Korean challenge modules are deliberately outside scope.
    "common/ai_strategy/FIN_finppong.txt": Rule(
        "USE_RT56", reason="한국 전용 포트에서 FIN 도전 모듈 제외"
    ),
    "common/characters/MON_mongppong.txt": Rule(
        "USE_RT56", reason="한국 전용 포트에서 MON 도전 모듈 제외"
    ),
    "common/on_actions/finnppong_on_actions.txt": Rule(
        "USE_RT56", reason="한국 전용 포트에서 FIN 도전 모듈 제외"
    ),
    "common/on_actions/mongppong_on_actions.txt": Rule(
        "USE_RT56", reason="한국 전용 포트에서 MON 도전 모듈 제외"
    ),
    "common/on_actions/sibbppong_on_actions.txt": Rule(
        "USE_RT56", reason="한국 전용 포트에서 SIB 도전 모듈 제외"
    ),
    "common/units/names_divisions/MON_names_divisions.txt": Rule(
        "USE_RT56", reason="RT56 몽골 편제명 정의를 유지"
    ),
    "history/countries/MON - Mongolia.txt": Rule(
        "USE_RT56", reason="RT56 몽골 국가사를 유지"
    ),
    "gfx/interface/decisions/decision_cat_generic_greater_mongolia.dds": Rule(
        "USE_RT56", reason="제외된 MON 도전 모듈의 미사용 자산"
    ),
    "gfx/interface/decisions/decision_cat_generic_unite_mongolia.dds": Rule(
        "USE_RT56", reason="제외된 MON 도전 모듈의 미사용 자산"
    ),
    "gfx/event_pictures/newsj_event_001.dds": Rule(
        "USE_RT56", reason="호출되지 않는 일본 전용 뉴스 이벤트와 함께 제외"
    ),
    "gfx/event_pictures/newsj_event_002.dds": Rule(
        "USE_RT56", reason="호출되지 않는 일본 전용 뉴스 이벤트와 함께 제외"
    ),
    "gfx/event_pictures/newsj_event_003.dds": Rule(
        "USE_RT56", reason="호출되지 않는 일본 전용 뉴스 이벤트와 함께 제외"
    ),
    "gfx/event_pictures/newsj_event_004.dds": Rule(
        "USE_RT56", reason="호출되지 않는 일본 전용 뉴스 이벤트와 함께 제외"
    ),
    "gfx/event_pictures/newsk_event_022.dds": Rule(
        "USE_RT56", reason="제외된 FIN 도전 이벤트 newsk.27의 고아 그림 자산"
    ),

    # Shared text databases are regenerated from the current host and reviewed HOK delta.
    "common/bookmarks/the_gathering_storm.txt": same_path(
        "THREE_WAY_MERGE", "RT56 bookmark base에 HOK 한국 시작 블록만 병합"
    ),
    "common/characters/KOR.txt": same_path(
        "THREE_WAY_MERGE", "HOK와 RT56의 한국 인물 정의를 논리 ID별 병합"
    ),
    "common/countries/colors.txt": Rule(
        "THREE_WAY_MERGE",
        ("common/countries/zz_hok_rt56_colors.txt",),
        "공용 전체 파일 대신 HOK 고유 색상만 추가 파일로 분리",
    ),
    "common/countries/cosmetic.txt": Rule(
        "THREE_WAY_MERGE",
        ("common/countries/zz_hok_rt56_cosmetic.txt",),
        "공용 전체 파일 대신 HOK 고유 cosmetic 정의만 분리",
    ),
    "common/decisions/JAP.txt": same_path(
        "THREE_WAY_MERGE", "현재 일본 결정에 필요한 한국 독립 delta를 리베이스"
    ),
    "common/decisions/KOR.txt": same_path(
        "THREE_WAY_MERGE", "현재 바닐라 한국 결정에 새 한국 state 집합만 병합"
    ),
    "common/intelligence_agencies/00_intelligence_agencies.txt": Rule(
        "THREE_WAY_MERGE",
        ("common/intelligence_agencies/zz_hok_rt56_intelligence_agencies.txt",),
        "공용 전체 파일 대신 HOK 한국 기관만 추가",
    ),
    "common/military_industrial_organization/organizations/00_generic_organization.txt": same_path(
        "THREE_WAY_MERGE", "RT56 generic MIO base에 HOK 한국 제외 조건만 병합"
    ),
    "common/military_industrial_organization/organizations/KOR_organization.txt": same_path(
        "THREE_WAY_MERGE", "RT56 소유권·가용 조건과 HOK 항공 MIO 설계를 병합"
    ),
    "common/names/00_names.txt": Rule(
        "THREE_WAY_MERGE",
        ("common/names/zz_hok_rt56_names.txt",),
        "공용 전체 파일 대신 HOK 고유 이름 목록만 추가",
    ),
    "common/national_focus/china_shared_TSR.txt": same_path(
        "THREE_WAY_MERGE", "현재 RT56 중국 공유 중점에 HOK 한국 delta를 병합"
    ),
    "common/on_actions/14_sea_on_actions.txt": same_path(
        "THREE_WAY_MERGE", "현재 RT56 SEA on_action에 한국 독립 연결만 병합"
    ),
    "common/peace_conference/ai_peace/SOV.txt": same_path(
        "THREE_WAY_MERGE", "현재 바닐라 평화 AI에 전체 한국 state 집합만 병합"
    ),
    "common/peace_conference/ai_peace/USA.txt": same_path(
        "THREE_WAY_MERGE", "현재 바닐라 평화 AI에 전체 한국 state 집합만 병합"
    ),
    "common/scripted_effects/SP_scripted_effects.txt": same_path(
        "THREE_WAY_MERGE", "현재 바닐라 특수 프로젝트 effect에 HOK 한국 분기만 병합"
    ),
    "common/scripted_triggers/JAP_scripted_triggers.txt": same_path(
        "THREE_WAY_MERGE", "현재 바닐라 일본 trigger에 독립 한국 state 집합만 병합"
    ),
    "common/scripted_triggers/unit_medals_scripted_triggers.txt": same_path(
        "THREE_WAY_MERGE", "현재 훈장 trigger 집합에 HOK 한국 trigger만 병합"
    ),
    "common/units/names_divisions/KOR_names_divisions.txt": same_path(
        "THREE_WAY_MERGE", "HOK 편제명과 RT56 KOR_MOT_01을 병합"
    ),
    "common/units/names_ships/KOR_ship_names.txt": same_path(
        "THREE_WAY_MERGE", "HOK 함명과 RT56 함종 그룹을 병합"
    ),
    "events/ElectionEvents.txt": same_path(
        "THREE_WAY_MERGE", "현재 선거 이벤트에 HOK 한국 분기만 병합"
    ),
    "events/SEA_Japan.txt": same_path(
        "THREE_WAY_MERGE", "현재 SEA 일본 이벤트에 한국 독립 delta를 병합"
    ),
    "events/WTT_Japan.txt": same_path(
        "THREE_WAY_MERGE", "현재 WTT 일본 이벤트에 한국 독립 delta를 병합"
    ),
    "history/countries/JAP - Japan.txt": same_path(
        "THREE_WAY_MERGE", "현재 일본 국가사에 독립 한국을 위한 최소 delta 적용"
    ),
    "history/general/generic_advisors.txt": same_path(
        "THREE_WAY_MERGE", "현재 generic advisor base에 필요한 한국 제외 조건만 병합"
    ),
    "history/units/JAP_1936_naval.txt": Rule(
        "USE_RT56", reason="낡은 donor OOB를 싣지 않고 현재 RT56 항목을 유지"
    ),
    "history/units/JAP_1936.txt": same_path(
        "THREE_WAY_MERGE", "현재 바닐라 OOB에 독립 한국을 위한 주둔 재배치만 병합"
    ),
    "history/units/JAP_1936_nsb.txt": same_path(
        "THREE_WAY_MERGE", "현재 바닐라 NSB OOB에 한국 주둔 재배치만 병합"
    ),
    "history/units/JAP_1936_naval_legacy.txt": same_path(
        "THREE_WAY_MERGE",
        "현재 바닐라 legacy naval OOB에 쓰시마 배치만 병합",
    ),

    # Logical asset collisions are pruned even though the physical paths differ.
    "gfx/entities/_HoK_units_planes.asset": same_path(
        "THREE_WAY_MERGE",
        "충돌하는 HOK 기본 항공 entity를 hok_rt56_ ID로 이전하고 RT56 supply state 병합",
    ),
    "gfx/entities/kor_planes.gfx": same_path(
        "THREE_WAY_MERGE", "충돌하는 HOK 기본 항공 mesh를 hok_rt56_ 고유 ID로 복원"
    ),
    "gfx/interface/equipmentdesigner/graphic_db/00_hok_plane_icons.txt": same_path(
        "THREE_WAY_MERGE", "삭제된 장비 참조와 HOK 고유 항공 entity 소비 경로를 이전"
    ),

    # Explicit Korea ownership where the host definition is intentionally replaced.
    "common/ideas/korea.txt": same_path(
        "OVERRIDE", "HOK 한국 아이디어 설계가 이 포트의 의도적 소유 영역"
    ),
    "common/national_focus/korea.txt": same_path(
        "OVERRIDE", "HOK 한국 중점 트리를 ID 마이그레이션 후 의도적으로 제공"
    ),
    "history/countries/KOR - Korea.txt": same_path(
        "OVERRIDE", "독립 HOK 한국의 1936 시작 국가사를 의도적으로 제공"
    ),
    "interface/frontendmainviewbg.gfx": same_path(
        "OVERRIDE", "신규 포트의 HOK 브랜딩 배경을 의도적으로 사용"
    ),

    # The global Korean map is synthesized from RT56 plus the pixel/reference delta.
    "map/buildings.txt": same_path("BINARY_MERGE", "RT56 전역 buildings에 이식된 한국 참조 합성"),
    "map/definition.csv": same_path("BINARY_MERGE", "RT56 definition base에 새 province 34개 합성"),
    "map/provinces.bmp": same_path("BINARY_MERGE", "RT56 bitmap base에 HOK 한국 픽셀 delta 합성"),
    "map/railways.txt": same_path("BINARY_MERGE", "RT56 전역 railway에 이식된 한국 연결 합성"),
    "map/strategicregions/186-Korea.txt": same_path(
        "BINARY_MERGE", "RT56 전략 지역에 이식된 한국 province membership 합성"
    ),
    "map/supply_nodes.txt": same_path("BINARY_MERGE", "RT56 전역 supply node에 한국 참조 합성"),
    "map/unitstacks.txt": same_path("BINARY_MERGE", "RT56 전역 unit stack에 한국 위치 합성"),
    "history/states/525-South Korea.txt": same_path(
        "BINARY_MERGE", "RT56 state 525를 한국 지형 delta에 맞춰 재구축"
    ),
    "history/states/527-North Korea.txt": same_path(
        "BINARY_MERGE", "RT56 state 527을 한국 지형 delta에 맞춰 재구축"
    ),
    "history/states/528-Nagasaki.txt": same_path(
        "BINARY_MERGE", "RT56 state 528을 쓰시마 분리에 맞춰 재구축"
    ),
    "history/states/1028 - Hamgyong.txt": Rule(
        "BINARY_MERGE", ("history/states/918-Hamgyong.txt",), "충돌 state 1028을 918로 이전"
    ),
    "history/states/1029 - Gangwon.txt": Rule(
        "BINARY_MERGE", ("history/states/1144-Gangwon.txt",), "충돌 state 1029를 1144로 이전"
    ),
    "history/states/1030 - Gyeongsang.txt": Rule(
        "BINARY_MERGE", ("history/states/920-Gyeongsang.txt",), "충돌 state 1030을 920으로 이전"
    ),
    "history/states/1031 - Chungcheong Jeolla.txt": Rule(
        "BINARY_MERGE", ("history/states/1145-Chungcheong.txt",), "복합 donor state에서 충청 state 1145 재구축"
    ),
    "history/states/1082 - Jeolla.txt": Rule(
        "BINARY_MERGE", ("history/states/919-Jeolla.txt",), "충돌 state 1082를 919로 이전"
    ),
    "history/states/1083 - Hwanghae.txt": Rule(
        "BINARY_MERGE", ("history/states/917-Hwanghae.txt",), "충돌 state 1083을 917로 이전"
    ),
    "history/states/1084 - Jeju.txt": Rule(
        "BINARY_MERGE", ("history/states/1146-Jeju.txt",), "충돌 state 1084를 1146으로 이전"
    ),
    "history/states/1085 - Tsushima.txt": Rule(
        "BINARY_MERGE", ("history/states/1147-Tsushima.txt",), "충돌 state 1085를 1147로 이전"
    ),
}


# RT56 ships these exact HOK/RT56 paths.  HOK art is kept deliberately, but
# classified as provenance-bearing assets instead of pretending it is a text override.
HOK_ASSET_OVERRIDES = {
    "gfx/flags/KOR_communism.tga",
    "gfx/flags/KOR_democratic.tga",
    "gfx/flags/KOR_fascism.tga",
    "gfx/flags/KOR_neutrality.tga",
    "gfx/flags/medium/KOR_communism.tga",
    "gfx/flags/medium/KOR_fascism.tga",
    "gfx/flags/medium/KOR_neutrality.tga",
    "gfx/flags/small/KOR_communism.tga",
    "gfx/flags/small/KOR_fascism.tga",
    "gfx/flags/small/KOR_neutrality.tga",
}
for _path in HOK_ASSET_OVERRIDES:
    EXPLICIT[_path] = same_path(
        "ASSET_COPY", "HOK 고유 한국 시각 정체성 자산; 출처를 유지해 의도적으로 선적"
    )
EXPLICIT["thumbnail.png"] = same_path(
    "OVERRIDE", "별도 호환판 Workshop 항목을 위해 제작한 호환판 전용 썸네일"
)
EXPLICIT["thumbnail_full.png"] = same_path(
    "OVERRIDE", "별도 호환판 식별을 위해 제작한 호환판 전용 원본 크기 썸네일"
)

for _index in range(1, 6):
    EXPLICIT[f"sound/kor/kor_Idle_{_index:03d}.wav"] = same_path(
        "ASSET_COPY", "HOK 한국 음성 payload; 논리 ID는 병합 registry가 단독 등록"
    )
for _kind, _count in (("Neutral", 4), ("Positive", 5), ("Retreat", 4)):
    for _index in range(1, _count + 1):
        EXPLICIT[f"sound/kor/kor_{_kind}_{_index:03d}.wav"] = same_path(
            "ASSET_COPY", "HOK 한국 음성 payload; 논리 ID는 병합 registry가 단독 등록"
        )

for _size in ("", "medium/", "small/"):
    for _tag in ("JAP_yamato_kyowakoku", "JAP_daiwa_mingoku", "JAP_fuso_gasshukoku"):
        EXPLICIT[f"gfx/flags/{_size}{_tag}.tga"] = Rule(
            "USE_RT56", reason="runtime 참조가 없는 비한국 일본 cosmetic flag를 제외"
        )

for _focus in (
    "proclaim_the_republic",
    "oppose_peace_preservation_law",
    "integrate_nanyo_gunto",
    "joint_staff_office",
    "demand_sagaren",
    "free_election_in_taiwan",
    "memories_of_taisho_democracy",
    "purge_the_militarists",
    "rok_jpn_free_trade_agreement",
    "develop_home_island",
):
    EXPLICIT[f"gfx/interface/goals/focus_JAP_{_focus}.dds"] = Rule(
        "USE_RT56", reason="runtime 참조가 없는 비한국 일본 focus 자산을 제외"
    )

for _path in (
    "gfx/interface/ideas/idea_jap_joint_staff_office.dds",
    "gfx/interface/ideas/idea_jap_tachikawa.dds",
    "gfx/event_pictures/report_event_jap_fuse_tatsuji.dds",
    "gfx/event_pictures/report_event_japanese_people_protest.dds",
    "gfx/leaders/JAP/portrait_Japan_jnlc.dds",
    "gfx/leaders/JAP/Portrait_Japan_Tatsuji_Fuse.dds",
    "gfx/leaders/JAP/Portrait_Japan_Tadamichi_kuribayashi.dds",
    "gfx/interface/ideas/idea_Japan_Tadamichi_kuribayashi.dds",
    "gfx/leaders/JAP/Portrait_Japan_Sigesaburo_miyazaki.dds",
    "gfx/interface/ideas/idea_Japan_Sigesaburo_miyazaki.dds",
    "gfx/leaders/JAP/Portrait_Japan_Shin_Yoshida.dds",
    "gfx/interface/ideas/idea_Japan_Shin_Yoshida.dds",
    "gfx/leaders/JAP/Portrait_Japan_Mitsumasa_Yonai.dds",
    "gfx/interface/ideas/idea_Japan_Mitsumasa_Yonai.dds",
    "gfx/leaders/JAP/Portrait_Japan_Masatomi_Kimura.dds",
    "gfx/interface/ideas/idea_Japan_Masatomi_Kimura.dds",
    "gfx/leaders/JAP/Portrait_Japan_Renya_Mutaguchi.dds",
    "gfx/interface/ideas/idea_Japan_Renya_Mutaguchi.dds",
    "gfx/leaders/JAP/Portrait_Japan_Tamon_Yamaguchi.dds",
    "gfx/interface/ideas/idea_Japan_Tamon_Yamaguchi.dds",
    "gfx/interface/decisions/decision_cat_jap_unite_karafuto.dds",
    "gfx/event_pictures/report_event_jap_rok_jpn_talks.dds",
    "gfx/interface/goals/focus_kor_japanese_trade.dds",
    "gfx/flags/RAJ_bharat_democratic.tga",
):
    EXPLICIT[_path] = Rule(
        "USE_RT56", reason="runtime 참조가 없는 비한국 donor 자산을 제외"
    )

EXPLICIT["music/Minshu_ikki.ogg"] = Rule(
    "USE_RT56",
    reason=(
        "삭제된 HOK JAP 민주화 경로의 song 조건만 있었고 KOR focus에는 재생 "
        "연결이 없는 고아 OGG; 최종 소유권 확인 전 기존 범위 밖 판정 유지"
    ),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def donor_files() -> list[Path]:
    result = []
    for path in HOK_ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(HOK_ROOT)
        if relative.parts[0] in {".git", "docs"}:
            continue
        result.append(path)
    return sorted(result, key=lambda path: path.relative_to(HOK_ROOT).as_posix().lower())


def resolve_rule(relative: str, suffix: str, rt_collision: bool) -> Rule:
    rule = EXPLICIT.get(relative)
    if rule is not None:
        return rule
    if rt_collision:
        raise RuntimeError(f"unclassified exact-path RT56 collision: {relative}")
    if suffix.lower() in BINARY_SUFFIXES:
        return same_path("ASSET_COPY", "RT56과 같은 경로가 없는 HOK 고유 자산; provenance 유지")
    return same_path("ADD", "RT56과 같은 경로가 없는 HOK 고유 콘텐츠/메타데이터")


def output_description(relative: str, rule: Rule) -> tuple[str, str, str]:
    if rule.integration_class == "USE_RT56":
        host = RT56_ROOT / relative
        if host.is_file():
            return f"RT56:{relative}", sha256(host), "OMITTED_HOST_OWNED"
        return "(omitted; RT56/vanilla scope retained)", "", "OMITTED_OUT_OF_SCOPE"

    outputs = tuple(relative if item == "{same}" else item for item in rule.outputs)
    if not outputs:
        outputs = (relative,)
    hashes: list[str] = []
    for item in outputs:
        path = REPO_ROOT / item
        if not path.is_file():
            raise RuntimeError(f"classified output is missing: {relative} -> {item}")
        hashes.append(sha256(path))
    if rule.integration_class == "ASSET_COPY":
        donor_hash = sha256(HOK_ROOT / relative)
        if outputs != (relative,) or hashes != [donor_hash]:
            raise RuntimeError(
                f"ASSET_COPY must preserve donor bytes at the same path: {relative}"
            )
    hash_cell = hashes[0] if len(hashes) == 1 else " | ".join(
        f"{path}={digest}" for path, digest in zip(outputs, hashes)
    )
    status = "GENERATED" if rule.integration_class in {"THREE_WAY_MERGE", "BINARY_MERGE"} else "SHIPPED"
    return " | ".join(outputs), hash_cell, status


def build_csv() -> tuple[bytes, Counter[str], int]:
    files = donor_files()
    if len(files) != EXPECTED_DONOR_FILES:
        raise RuntimeError(
            f"donor file count changed: expected {EXPECTED_DONOR_FILES}, got {len(files)}"
        )

    rows: list[dict[str, str]] = []
    counts: Counter[str] = Counter()
    collision_count = 0
    donor_relatives: set[str] = set()
    for source in files:
        relative = source.relative_to(HOK_ROOT).as_posix()
        donor_relatives.add(relative)
        rt_collision = (RT56_ROOT / relative).is_file()
        collision_count += int(rt_collision)
        rule = resolve_rule(relative, source.suffix, rt_collision)
        output_path, output_hash, status = output_description(relative, rule)
        counts[rule.integration_class] += 1
        rows.append(
            {
                "source_path": relative,
                "integration_class": rule.integration_class,
                "status": status,
                "exact_path_rt56_collision": "yes" if rt_collision else "no",
                "output_path": output_path,
                "reason": rule.reason,
                "donor_sha256": sha256(source),
                "output_sha256": output_hash,
            }
        )

    unknown_rules = sorted(set(EXPLICIT) - donor_relatives)
    if unknown_rules:
        raise RuntimeError(f"classification rules reference missing donor files: {unknown_rules}")
    if collision_count != EXPECTED_RT56_COLLISIONS:
        raise RuntimeError(
            f"RT56 collision baseline changed: expected {EXPECTED_RT56_COLLISIONS}, got {collision_count}"
        )

    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream,
        fieldnames=(
            "source_path",
            "integration_class",
            "status",
            "exact_path_rt56_collision",
            "output_path",
            "reason",
            "donor_sha256",
            "output_sha256",
        ),
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8"), counts, collision_count


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    expected, counts, collisions = build_csv()
    current = OUTPUT.read_bytes() if OUTPUT.is_file() else None
    summary = ", ".join(f"{key}={counts[key]}" for key in sorted(counts))
    if current == expected:
        print(f"unchanged {OUTPUT.relative_to(REPO_ROOT).as_posix()} {sha256(OUTPUT)}")
    elif args.apply:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        temporary = OUTPUT.with_name(OUTPUT.name + ".tmp")
        temporary.write_bytes(expected)
        temporary.replace(OUTPUT)
        print(f"written   {OUTPUT.relative_to(REPO_ROOT).as_posix()} {sha256(OUTPUT)}")
    else:
        print(f"mismatch  {OUTPUT.relative_to(REPO_ROOT).as_posix()}")
        return 1
    print(f"files={sum(counts.values())} collisions={collisions} {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
