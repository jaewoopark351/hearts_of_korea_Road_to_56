#!/usr/bin/env python3
"""Remove optional FIN/MON/SIB challenge modules from the Korea-only port."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

from build_rt56_map import HOK_ROOT, REPO_ROOT


EXPECTED_SHA256 = {
    HOK_ROOT / "common/game_rules/hok_game_rules.txt": "D39496F15D4415F00D2DF15CD57A194C6DD53A6E764C37F823231C2483AC1425",
    HOK_ROOT / "events/NewsEvents_KOR.txt": "8690739B2DDF46A6369797312945D862AB74BDDCCFD6B532EDBCC92208E0163F",
    HOK_ROOT / "interface/decisions_HoK.gfx": "3D90FD8A9FF9E5FE5E5BB11D32D91D9990DB10859CCE4B85092F4D95F3531D21",
    HOK_ROOT / "interface/eventpictures_HoK.gfx": "961A425469B7B2C0EAEBE66305039E791358C2FEB27D44DA7EE58EEC7642E925",
    HOK_ROOT / "localisation/english/HoK_start_game_setup_l_english.yml": "F12C97A6ACE9BB59E60DBF3AA79DC423239D38F702AF946C47EB0EA08E32A44C",
    HOK_ROOT / "localisation/korean/HoK_start_game_setup_l_korean.yml": "5867CDC8315EE2A24840E6F359D0F95D8CC5EE1B6E6E12EAD37B345F5C0084F6",
    HOK_ROOT / "localisation/english/korea_event_l_english.yml": "A7B89819FC324A9339106F12E5C821F2FD95896CC2ADB382A6DC85F96EFDC25F",
    HOK_ROOT / "localisation/korean/korea_event_l_korean.yml": "56F93D319E9861E5D8B139CDA4579E490319DC41D27E067FCC0CE189500B6659",
    HOK_ROOT / "gfx/event_pictures/newsj_event_001.dds": "808DFBCB55359D28C6560EDD774555DCD299D0B766AECC0774E557924F3FF9DF",
    HOK_ROOT / "gfx/event_pictures/newsj_event_002.dds": "5B9CE881B697A0BC1CB9037E0610ACFC20FCFFFEAA3894F9849B699DEB188A50",
    HOK_ROOT / "gfx/event_pictures/newsj_event_003.dds": "B64228ED4255DCBC53BB6794822C6DDEB686917574ECC09D88FF2C6B8F42F6E1",
    HOK_ROOT / "gfx/event_pictures/newsj_event_004.dds": "7C0AD7DDF54CA65F5BFCBB884B5F3EF9E81F7DE177FD5B51B7959738F86A35BD",
    HOK_ROOT / "gfx/event_pictures/newsk_event_022.dds": "BCE6AF6BC2A096842580A9665E2814B99C935E3D172CA56A31A0F3C4049A45DC",
    HOK_ROOT / "gfx/flags/JAP_daiwa_mingoku.tga": "6C707DC9DF6214896B39FEE6DE01DCB645CDBEACEBC903D571EC3F1B028EFD80",
    HOK_ROOT / "gfx/flags/JAP_fuso_gasshukoku.tga": "6C707DC9DF6214896B39FEE6DE01DCB645CDBEACEBC903D571EC3F1B028EFD80",
    HOK_ROOT / "gfx/flags/JAP_yamato_kyowakoku.tga": "6C707DC9DF6214896B39FEE6DE01DCB645CDBEACEBC903D571EC3F1B028EFD80",
    HOK_ROOT / "gfx/flags/medium/JAP_daiwa_mingoku.tga": "444D9D77D8A14D0BF75B66B3036CA29F689BCCEB497168189037A3B57635308B",
    HOK_ROOT / "gfx/flags/medium/JAP_fuso_gasshukoku.tga": "B1231940D341EE304D41857AA58C05C50188A897725E2893C718DB60074C3BF5",
    HOK_ROOT / "gfx/flags/medium/JAP_yamato_kyowakoku.tga": "223187025F40506E07D66318BE4E5AF9393F9F3CC5676BB89D850FFB7DF3763A",
    HOK_ROOT / "gfx/flags/small/JAP_daiwa_mingoku.tga": "E68DB1EEA9185BE9359B6CF41C5DB10D2B2481184231C5FFFF5E1BBA0E107FF6",
    HOK_ROOT / "gfx/flags/small/JAP_fuso_gasshukoku.tga": "C390B5C862732A0ACFDD1B3F12543814FFE24CCA369848EB0B0123D9986BC027",
    HOK_ROOT / "gfx/flags/small/JAP_yamato_kyowakoku.tga": "75DFC554693DE87EF4D2172F2739DBF09DCD714260AC087A3C587E4272F013CB",
    HOK_ROOT / "interface/goals_HoK.gfx": "85BD6B1AB72FE37BA3D4D818CEA171B70278D1F55E2804F5A00854855C79E75E",
    HOK_ROOT / "interface/goals_shine_HoK.gfx": "DA7EDB72671EDDC1ED22D9D24113680B7FCC09CE3B084D9359C9CC3A4757557A",
    HOK_ROOT / "interface/ideas_HoK.gfx": "9AFDF0F9AB74EA11BE5AEDC10C682149929FFF7A5CD8D77F6CD675215DE00477",
    HOK_ROOT / "interface/characters_HoK.gfx": "3BB4D4E5B68B44034EA25996C5FB83BC7B81E71E0E55228AFF7F10D2732C8A30",
    HOK_ROOT / "common/country_leader/00_hok_traits.txt": "566525F070E9B5937FC1926FF273E2381C041CD3DD4312DA2EEC5404372B8DC9",
    HOK_ROOT / "music/hok_music.asset": "1FDAE5902FD0143264FA828FD079099EADF9944F896ABA7821A06ED64AD9B38D",
    HOK_ROOT / "localisation/english/HoK_music_l_english.yml": "F1A8C54BCB458110EEDDC8D130B66DF357665FFF54D82B2C2C8B3AF9E0F20D20",
    HOK_ROOT / "localisation/korean/HoK_music_l_korean.yml": "B910F4A1DAA56E6AD07246F1D755B1924FE1DBBB312E9AC8C2C422FF82EED72F",
    HOK_ROOT / "gfx/interface/goals/focus_JAP_proclaim_the_republic.dds": "9CA52154155A6DE49AF57AA8D1F000B4EB3FD496DCA55B73C5335651D8C2AE90",
    HOK_ROOT / "gfx/interface/goals/focus_JAP_oppose_peace_preservation_law.dds": "721B723A8ED1F1C27408F531E28D0FD5F2DF9F0AF9E1331E6EE95C86D616A25F",
    HOK_ROOT / "gfx/interface/goals/focus_JAP_integrate_nanyo_gunto.dds": "881ADC6BEA3FC107A160CDC4DE5C448858E9DDBF82C9FEA9D6E168D814FF068A",
    HOK_ROOT / "gfx/interface/goals/focus_JAP_joint_staff_office.dds": "005453E51C285384F77B5348DF701DFE1FD4758005B59A5D3E95CE738FF137B5",
    HOK_ROOT / "gfx/interface/goals/focus_JAP_demand_sagaren.dds": "F98B74BB9971F7E0392FC3ECBACB1B1B180AB93FBC3F5B0556BA08E77ECFC8D9",
    HOK_ROOT / "gfx/interface/goals/focus_JAP_free_election_in_taiwan.dds": "5A686972B381B6B40D59D48EA29D1D63691B7831549B852D40A2DD79EC8D987E",
    HOK_ROOT / "gfx/interface/goals/focus_JAP_memories_of_taisho_democracy.dds": "2B4CDB125B95DE01BB78C8B35AC405119AB1F5EF8BE103B7F733C55090AEE72B",
    HOK_ROOT / "gfx/interface/goals/focus_JAP_purge_the_militarists.dds": "FA4B1D0A5B2E86AA53BC2F8507F9184C290926E74EFC3E174DEC515AA4313848",
    HOK_ROOT / "gfx/interface/goals/focus_JAP_rok_jpn_free_trade_agreement.dds": "0B4F5BA4F4E511E4A9085EDC0F1382470B6E10E0A65F10D96E3688DE51593D4F",
    HOK_ROOT / "gfx/interface/goals/focus_JAP_develop_home_island.dds": "00FCA9A2942B2677CCA4BD692BDA638B7C7DA0FB6681E08963D7B094D4F3CB88",
    HOK_ROOT / "gfx/interface/ideas/idea_jap_joint_staff_office.dds": "26CC7E59A34690FF998EE0B1F221CD52B0E88B986B86B548CCB7A6FB094DB34A",
    HOK_ROOT / "gfx/interface/ideas/idea_jap_tachikawa.dds": "CEE214CC365663A6C93520B7C0DAFEF6E9AAE9EA4E54680209B205AAF548E4C5",
    HOK_ROOT / "gfx/event_pictures/report_event_jap_fuse_tatsuji.dds": "36F68911698D4C1B625A5FF143B439FF75A75D3E300E742145EDB586BC384E46",
    HOK_ROOT / "gfx/event_pictures/report_event_japanese_people_protest.dds": "865A86909510298413B82F26727C71A7D08D1C969B7AC89B4B35204ECA96CAD4",
    HOK_ROOT / "gfx/event_pictures/report_event_jap_rok_jpn_talks.dds": "A43285DED8650E561F1C00E7A1DF62409E5E6E65092058291F3C831D7F776126",
    HOK_ROOT / "gfx/leaders/JAP/portrait_Japan_jnlc.dds": "E2430A609EBBBD7C17D7106597938CEB9FE9CC68BCE95B27A3B2490ABE6D4645",
    HOK_ROOT / "gfx/leaders/JAP/Portrait_Japan_Tatsuji_Fuse.dds": "46F0051B4DC778A0CC790099B3D834BE324ED521D406ADABCC7AF25FD0D92F03",
    HOK_ROOT / "gfx/leaders/JAP/Portrait_Japan_Tadamichi_kuribayashi.dds": "598D2FE021DD56A6F8E2EF10A2563C47E2DAA5A4E3554174D1DCD55C68DABB10",
    HOK_ROOT / "gfx/interface/ideas/idea_Japan_Tadamichi_kuribayashi.dds": "EB70527B6693C0754C2940A30652C5A743013164CBC312EF6354F4FE03A0D354",
    HOK_ROOT / "gfx/leaders/JAP/Portrait_Japan_Sigesaburo_miyazaki.dds": "3B7E5F10D2D2D182AEA17537807CD2CC74D643F6FC7693E8324908E6DD43A3B8",
    HOK_ROOT / "gfx/interface/ideas/idea_Japan_Sigesaburo_miyazaki.dds": "C5BEEDE952EE6599C23044389F297B8BD6BF7C43357B1BDFD8E0C575BEF5C735",
    HOK_ROOT / "gfx/leaders/JAP/Portrait_Japan_Shin_Yoshida.dds": "079C35F4E0C379831DAA819DFE508BC793DE932E54543C6D5C773237284B12C7",
    HOK_ROOT / "gfx/interface/ideas/idea_Japan_Shin_Yoshida.dds": "53C12019A2AD4F1243FCD9EEE18BE5FFDFAD5543CBCA58F4AE3F7160EC61AAA3",
    HOK_ROOT / "gfx/leaders/JAP/Portrait_Japan_Mitsumasa_Yonai.dds": "78F6EA8B984549CF52F77B9C1973F305C6BB4E1654C05961116F004B5A84F1BA",
    HOK_ROOT / "gfx/interface/ideas/idea_Japan_Mitsumasa_Yonai.dds": "E4342DF4250086D29DF24AC74FBAE48D5D15EC1D3EE6DAF1BDC537F26E7DCD83",
    HOK_ROOT / "gfx/leaders/JAP/Portrait_Japan_Masatomi_Kimura.dds": "E25BA912A941874E245E6724F594219BF6F100AE4A1D2A82296443C0D374E2CE",
    HOK_ROOT / "gfx/interface/ideas/idea_Japan_Masatomi_Kimura.dds": "8248BD3281AA09D7E81D868443BB442A32590B43A3C4B440FA9FFAE64A25317C",
    HOK_ROOT / "gfx/leaders/JAP/Portrait_Japan_Renya_Mutaguchi.dds": "C0E87FE9C6A425B847668CF0930B144A8308BEEBB4D9889575A904B886E827FE",
    HOK_ROOT / "gfx/interface/ideas/idea_Japan_Renya_Mutaguchi.dds": "4880E53F8B7595E1C643505CEDC17E5B9798EAC5EC1D8236CE2389AA47BAB5A7",
    HOK_ROOT / "gfx/leaders/JAP/Portrait_Japan_Tamon_Yamaguchi.dds": "A0026CADDD54F4187BF48A47680131579CA8CEF0491DD50360F13E795A3D864D",
    HOK_ROOT / "gfx/interface/ideas/idea_Japan_Tamon_Yamaguchi.dds": "ACE8316E57EF6AEDC00B101F4F6A3BA5226E681B5F033F0231FC1F6FC7381302",
    HOK_ROOT / "gfx/interface/decisions/decision_cat_jap_unite_karafuto.dds": "6A2D7CC6E7AE5FF9BCD159C7D22F4BB930BF50A6997EDCBEEF2D04E867C6FE86",
    HOK_ROOT / "gfx/interface/goals/focus_kor_japanese_trade.dds": "22A53B4C53849131D97F2FD590554EF40ABEE385CF69BF96DEA01768DCB61BE3",
    HOK_ROOT / "gfx/flags/RAJ_bharat_democratic.tga": "A953F93B35A3DBAE61076526FE2A98CD6D8AE35CFDCCC30C6D6BA12D7C2157E9",
    HOK_ROOT / "music/Minshu_ikki.ogg": "BF69629EC53A3E4C422A8619E72C5A6BD86DEC5D9971D36289129641EEB65371",
}

REMOVE_FILES = (
    "common/ai_strategy/FIN_finppong.txt",
    "common/characters/MON_mongppong.txt",
    "common/on_actions/finnppong_on_actions.txt",
    "common/on_actions/mongppong_on_actions.txt",
    "common/on_actions/sibbppong_on_actions.txt",
    "history/countries/MON - Mongolia.txt",
    "common/units/names_divisions/MON_names_divisions.txt",
    "gfx/interface/decisions/decision_cat_generic_unite_mongolia.dds",
    "gfx/interface/decisions/decision_cat_generic_greater_mongolia.dds",
    "gfx/event_pictures/newsj_event_001.dds",
    "gfx/event_pictures/newsj_event_002.dds",
    "gfx/event_pictures/newsj_event_003.dds",
    "gfx/event_pictures/newsj_event_004.dds",
    "gfx/event_pictures/newsk_event_022.dds",
    "gfx/flags/JAP_daiwa_mingoku.tga",
    "gfx/flags/JAP_fuso_gasshukoku.tga",
    "gfx/flags/JAP_yamato_kyowakoku.tga",
    "gfx/flags/medium/JAP_daiwa_mingoku.tga",
    "gfx/flags/medium/JAP_fuso_gasshukoku.tga",
    "gfx/flags/medium/JAP_yamato_kyowakoku.tga",
    "gfx/flags/small/JAP_daiwa_mingoku.tga",
    "gfx/flags/small/JAP_fuso_gasshukoku.tga",
    "gfx/flags/small/JAP_yamato_kyowakoku.tga",
    "gfx/interface/goals/focus_JAP_proclaim_the_republic.dds",
    "gfx/interface/goals/focus_JAP_oppose_peace_preservation_law.dds",
    "gfx/interface/goals/focus_JAP_integrate_nanyo_gunto.dds",
    "gfx/interface/goals/focus_JAP_joint_staff_office.dds",
    "gfx/interface/goals/focus_JAP_demand_sagaren.dds",
    "gfx/interface/goals/focus_JAP_free_election_in_taiwan.dds",
    "gfx/interface/goals/focus_JAP_memories_of_taisho_democracy.dds",
    "gfx/interface/goals/focus_JAP_purge_the_militarists.dds",
    "gfx/interface/goals/focus_JAP_rok_jpn_free_trade_agreement.dds",
    "gfx/interface/goals/focus_JAP_develop_home_island.dds",
    "gfx/interface/ideas/idea_jap_joint_staff_office.dds",
    "gfx/interface/ideas/idea_jap_tachikawa.dds",
    "gfx/event_pictures/report_event_jap_fuse_tatsuji.dds",
    "gfx/event_pictures/report_event_japanese_people_protest.dds",
    "gfx/event_pictures/report_event_jap_rok_jpn_talks.dds",
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
    "gfx/interface/goals/focus_kor_japanese_trade.dds",
    "gfx/flags/RAJ_bharat_democratic.tga",
    "music/Minshu_ikki.ogg",
)

REMOVE_RULES = (
    "fin_finnppong_status",
    "mon_mongppong_status",
    "sov_sibbppong_status",
)

REMOVE_SPRITES = (
    "GFX_decision_cat_generic_greater_mongolia",
    "GFX_decision_cat_generic_unite_mongolia",
    "GFX_decision_cat_jap_unite_karafuto",
)

REMOVE_EVENT_SPRITES = (
    "GFX_newsk_event_022",
    "GFX_report_event_jap_fuse_tatsuji",
    "GFX_report_event_japanese_people_protest",
    "GFX_report_event_jap_rok_jpn_talks",
    "GFX_newsj_event_001",
    "GFX_newsj_event_002",
    "GFX_newsj_event_003",
    "GFX_newsj_event_004",
)

REMOVE_UNUSED_FOCUS_SPRITES = (
    "GFX_focus_JAP_proclaim_the_republic",
    "GFX_focus_JAP_oppose_peace_preservation_law",
    "GFX_focus_JAP_integrate_nanyo_gunto",
    "GFX_focus_JAP_joint_staff_office",
    "GFX_focus_JAP_demand_sagaren",
    "GFX_focus_JAP_free_election_in_taiwan",
    "GFX_focus_JAP_memories_of_taisho_democracy",
    "GFX_focus_JAP_purge_the_militarists",
    "GFX_focus_JAP_rok_jpn_free_trade_agreement",
    "GFX_focus_JAP_develop_home_island",
    "GFX_focus_KOR_japanese_trade",
)

REMOVE_JAP_IDEA_SPRITES = (
    "GFX_idea_jap_joint_staff_office",
    "GFX_idea_jap_tachikawa",
)

REMOVE_JAP_CHARACTER_SPRITES = (
    "GFX_Portrait_JAP_japanese_national_liberation_committee",
    "GFX_Portrait_JAP_tatsuji_fuse",
    "GFX_Portrait_JAP_tadamichi_kuribayashi",
    "GFX_Portrait_JAP_tadamichi_kuribayashi_small",
    "GFX_Portrait_JAP_sigesaburo_miyazaki",
    "GFX_Portrait_JAP_sigesaburo_miyazaki_small",
    "GFX_Portrait_JAP_shin_yoshida",
    "GFX_Portrait_JAP_shin_yoshida_small",
    "GFX_Portrait_JAP_mitsumasa_yonai_navy",
    "GFX_Portrait_JAP_mitsumasa_yonai_navy_small",
    "GFX_Portrait_JAP_masatomi_kimura",
    "GFX_Portrait_JAP_masatomi_kimura_small",
    "GFX_Portrait_JAP_renya_mutaguchi",
    "GFX_Portrait_JAP_renya_mutaguchi_small",
)

REMOVE_NON_KOREAN_TRAITS = (
    "JAP_japanese_national_liberation_committee_trait",
    "JAP_champion",
)

REMOVE_SETUP_LOCALISATION = {
    "FINNPPONG_STATUS",
    "RULE_OPTION_DEFAULT_FINNPPONG_DESC",
    "FINNPPONG_ENABLED_TEXT",
    "FINNPPONG_ENABLED_TEXT_DESC",
    "MONGPPONG_STATUS",
    "RULE_OPTION_DEFAULT_MONGPPONG_DESC",
    "MONGPPONG_ENABLED_TEXT",
    "MONGPPONG_ENABLED_TEXT_DESC",
    "SIBBPPONG_STATUS",
    "RULE_OPTION_DEFAULT_SIBBPPONG_DESC",
    "SIBBPPONG_ENABLED_TEXT",
    "SIBBPPONG_ENABLED_TEXT_DESC",
}

REMOVE_EVENT_LOCALISATION = {
    "newsk.27.title",
    "newsk.27.desc",
    "newsk.27.a",
    "newsk.27.b",
    "newsk.27.c",
}


class PruneError(RuntimeError):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def verify_sources() -> None:
    for path, expected in EXPECTED_SHA256.items():
        if not path.is_file():
            raise PruneError(f"missing pinned donor source: {path}")
        actual = sha256(path.read_bytes())
        if actual != expected:
            raise PruneError(f"pinned donor changed: {path}\nexpected {expected}\nactual   {actual}")


def matching_brace(text: str, opening: int) -> int:
    depth = 0
    quoted = False
    escaped = False
    comment = False
    for index in range(opening, len(text)):
        char = text[index]
        if comment:
            if char in "\r\n":
                comment = False
            continue
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == "#":
            comment = True
        elif char == '"':
            quoted = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index + 1
    raise PruneError(f"unclosed block at offset {opening}")


def block_spans(text: str, key: str) -> list[tuple[int, int]]:
    pattern = re.compile(rf"(?m)^[ \t]*{re.escape(key)}[ \t]*=[ \t]*\{{")
    result = []
    for match in pattern.finditer(text):
        opening = text.find("{", match.start(), match.end())
        result.append((match.start(), matching_brace(text, opening)))
    return result


def remove_named_block(text: str, key: str) -> str:
    spans = block_spans(text, key)
    if len(spans) != 1:
        raise PruneError(f"expected one donor block {key}, found {len(spans)}")
    start, end = spans[0]
    while end < len(text) and text[end] in " \t\r\n":
        end += 1
    return text[:start] + text[end:]


def build_game_rules() -> bytes:
    raw = (HOK_ROOT / "common/game_rules/hok_game_rules.txt").read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = (raw[3:] if bom else raw).decode("utf-8")
    for key in REMOVE_RULES:
        text = remove_named_block(text, key)
    if any(key in text for key in REMOVE_RULES):
        raise PruneError("non-Korean rule key remains after pruning")
    return (b"\xef\xbb\xbf" if bom else b"") + text.encode("utf-8")


def build_country_leader_traits() -> bytes:
    raw = (HOK_ROOT / "common/country_leader/00_hok_traits.txt").read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = (raw[3:] if bom else raw).decode("utf-8")
    for key in REMOVE_NON_KOREAN_TRAITS:
        text = remove_named_block(text, key)
    if any(key in text for key in REMOVE_NON_KOREAN_TRAITS):
        raise PruneError("orphan Japan trait remains after pruning")
    return (b"\xef\xbb\xbf" if bom else b"") + text.encode("utf-8")


def build_decision_gfx() -> bytes:
    raw = (HOK_ROOT / "interface/decisions_HoK.gfx").read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = (raw[3:] if bom else raw).decode("utf-8")
    removals = []
    for start, end in block_spans(text, "spriteType"):
        block = text[start:end]
        if any(f'name = "{name}"' in block for name in REMOVE_SPRITES):
            removals.append((start, end))
    if len(removals) != len(REMOVE_SPRITES):
        raise PruneError(f"expected {len(REMOVE_SPRITES)} unused decision sprites, found {len(removals)}")
    for start, end in reversed(removals):
        while end < len(text) and text[end] in " \t\r\n":
            end += 1
        text = text[:start] + text[end:]
    if any(name in text for name in REMOVE_SPRITES):
        raise PruneError("unused decision sprite name remains after pruning")
    return (b"\xef\xbb\xbf" if bom else b"") + text.encode("utf-8")


def build_gfx_without_named_sprites(
    relative: str, block_key: str, names: tuple[str, ...]
) -> bytes:
    raw = (HOK_ROOT / relative).read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = (raw[3:] if bom else raw).decode("utf-8")
    wanted = set(names)
    found: set[str] = set()
    removals: list[tuple[int, int]] = []
    for start, end in block_spans(text, block_key):
        block = text[start:end]
        match = re.search(r'(?m)^[ \t]*name[ \t]*=[ \t]*"([^"]+)"', block)
        if not match or match.group(1) not in wanted:
            continue
        name = match.group(1)
        if name in found:
            raise PruneError(f"duplicate removable sprite {name} in {relative}")
        found.add(name)
        removals.append((start, end))
    if found != wanted:
        raise PruneError(f"missing removable sprites in {relative}: {sorted(wanted - found)}")
    for start, end in reversed(removals):
        while end < len(text) and text[end] in " \t\r\n":
            end += 1
        text = text[:start] + text[end:]
    if any(name in text for name in wanted):
        raise PruneError(f"removed sprite token remains in {relative}")
    return (b"\xef\xbb\xbf" if bom else b"") + text.encode("utf-8")


def build_music_asset() -> bytes:
    relative = "music/hok_music.asset"
    raw = (HOK_ROOT / relative).read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = (raw[3:] if bom else raw).decode("utf-8")
    matches: list[tuple[int, int]] = []
    for start, end in block_spans(text, "music"):
        block = text[start:end]
        if re.search(r'(?m)^[ \t]*name[ \t]*=[ \t]*"Minshu_ikki"', block):
            matches.append((start, end))
    if len(matches) != 1:
        raise PruneError(f"expected one Minshu_ikki music block, found {len(matches)}")
    start, end = matches[0]
    while end < len(text) and text[end] in " \t\r\n":
        end += 1
    text = text[:start] + text[end:]
    if "Minshu_ikki" in text:
        raise PruneError("Minshu_ikki remains in generated music asset")
    return (b"\xef\xbb\xbf" if bom else b"") + text.encode("utf-8")


def build_eventpictures_gfx() -> bytes:
    raw = (HOK_ROOT / "interface/eventpictures_HoK.gfx").read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = (raw[3:] if bom else raw).decode("utf-8")
    removals = []
    for start, end in block_spans(text, "spriteType"):
        block = text[start:end]
        if any(f'name = "{name}"' in block for name in REMOVE_EVENT_SPRITES):
            removals.append((start, end))
    if len(removals) != len(REMOVE_EVENT_SPRITES):
        raise PruneError(
            f"expected {len(REMOVE_EVENT_SPRITES)} dead non-Korean news sprites, "
            f"found {len(removals)}"
        )
    for start, end in reversed(removals):
        while end < len(text) and text[end] in " \t\r\n":
            end += 1
        text = text[:start] + text[end:]
    if any(name in text for name in REMOVE_EVENT_SPRITES):
        raise PruneError("dead non-Korean news sprite remains after pruning")
    return (b"\xef\xbb\xbf" if bom else b"") + text.encode("utf-8")


def build_news_events() -> bytes:
    raw = (HOK_ROOT / "events/NewsEvents_KOR.txt").read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = (raw[3:] if bom else raw).decode("utf-8")
    remove_ids = {"newsk.27", "newsj.1", "newsj.2", "newsj.3", "newsj.4"}
    matches: dict[str, tuple[int, int]] = {}
    for start, end in block_spans(text, "news_event"):
        block = text[start:end]
        id_match = re.search(
            r"(?m)^[ \t]*id[ \t]*=[ \t]*([A-Za-z0-9_.-]+)[ \t]*(?:#.*)?\r?$",
            block,
        )
        if id_match and id_match.group(1) in remove_ids:
            identifier = id_match.group(1)
            if identifier in matches:
                raise PruneError(f"duplicate removable event {identifier}")
            matches[identifier] = (start, end)
    missing = remove_ids - set(matches)
    if missing:
        raise PruneError(f"missing events scheduled for removal: {sorted(missing)}")
    for start, end in sorted(matches.values(), reverse=True):
        while end < len(text) and text[end] in " \t\r\n":
            end += 1
        text = text[:start] + text[end:]
    if any(identifier in text for identifier in remove_ids):
        raise PruneError("removed FIN/Japan challenge event still referenced")
    if "fin_finnppong_option_enabled" in text:
        raise PruneError("removed FIN challenge flag still referenced")
    return (b"\xef\xbb\xbf" if bom else b"") + text.encode("utf-8")


def remove_localisation_keys(raw: bytes, keys: set[str]) -> bytes:
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = (raw[3:] if bom else raw).decode("utf-8")
    kept: list[str] = []
    removed: set[str] = set()
    pattern = re.compile(r"^[ \t]*([^#\s][^:]*):[0-9]+[ \t]+")
    for line in text.splitlines(keepends=True):
        match = pattern.match(line)
        if match and match.group(1) in keys:
            removed.add(match.group(1))
        else:
            kept.append(line)
    missing = keys - removed
    if missing:
        raise PruneError(f"missing localisation keys scheduled for removal: {sorted(missing)}")
    result = "".join(kept)
    if any(re.search(rf"(?m)^[ \t]*{re.escape(key)}:", result) for key in keys):
        raise PruneError("removed localisation key remains")
    return (b"\xef\xbb\xbf" if bom else b"") + result.encode("utf-8")


def build_setup_localisation(relative: str) -> bytes:
    raw = (HOK_ROOT / relative).read_bytes()
    result = remove_localisation_keys(raw, REMOVE_SETUP_LOCALISATION)
    old = (
        "게임 시작 전 난이도를 정예병으로 하고, 한국을 제외한 모든 국가들을 강화하고, "
        "중뽕옵션, 핀뽕옵션, 동시베리아 보급여건 강화 옵션 사용 시, 훨신 더 어려운"
    ).encode("utf-8")
    new = (
        "게임 시작 전 난이도를 정예병으로 하고 한국을 제외한 모든 국가를 강화하면, "
        "훨씬 더 어려운"
    ).encode("utf-8")
    if result.count(old) != 1:
        raise PruneError(f"expected one obsolete Ragnarok description in {relative}")
    result = result.replace(old, new)
    text = result.decode("utf-8-sig")
    newline = "\r\n" if "\r\n" in text else "\n"
    marker = ' hokRagnarok.6.a:0 "작은 고추(Little Red Pepper)의 매운 맛을 보여주마."'
    if text.count(marker) != 1 or "hokRagnarok.7.t:" in text:
        raise PruneError(f"unexpected Ragnarok localisation baseline in {relative}")
    addition = newline.join(
        (
            "",
            ' hokRagnarok.7.t:0 "전 세계의 결집"',
            ' hokRagnarok.7.d:0 "영국을 중심으로 세계 각국이 대한민국을 무너뜨리기 위한 하나의 전선으로 결집했습니다. 이제 물러설 곳은 없습니다."',
            ' hokRagnarok.7.a:0 "모두 덤벼라."',
        )
    )
    text = text.replace(marker, marker + newline + addition)
    return b"\xef\xbb\xbf" + text.encode("utf-8")


def build_event_localisation(relative: str) -> bytes:
    return remove_localisation_keys(
        (HOK_ROOT / relative).read_bytes(), REMOVE_EVENT_LOCALISATION
    )


def outputs() -> dict[str, bytes]:
    verify_sources()
    return {
        "common/game_rules/hok_game_rules.txt": build_game_rules(),
        "common/country_leader/00_hok_traits.txt": build_country_leader_traits(),
        "events/NewsEvents_KOR.txt": build_news_events(),
        "interface/decisions_HoK.gfx": build_decision_gfx(),
        "interface/eventpictures_HoK.gfx": build_eventpictures_gfx(),
        "interface/goals_HoK.gfx": build_gfx_without_named_sprites(
            "interface/goals_HoK.gfx", "SpriteType", REMOVE_UNUSED_FOCUS_SPRITES
        ),
        "interface/goals_shine_HoK.gfx": build_gfx_without_named_sprites(
            "interface/goals_shine_HoK.gfx",
            "SpriteType",
            tuple(f"{name}_shine" for name in REMOVE_UNUSED_FOCUS_SPRITES),
        ),
        "interface/ideas_HoK.gfx": build_gfx_without_named_sprites(
            "interface/ideas_HoK.gfx", "spriteType", REMOVE_JAP_IDEA_SPRITES
        ),
        "interface/characters_HoK.gfx": build_gfx_without_named_sprites(
            "interface/characters_HoK.gfx", "spriteType", REMOVE_JAP_CHARACTER_SPRITES
        ),
        "music/hok_music.asset": build_music_asset(),
        "localisation/english/HoK_music_l_english.yml": remove_localisation_keys(
            (HOK_ROOT / "localisation/english/HoK_music_l_english.yml").read_bytes(),
            {"Minshu_ikki"},
        ),
        "localisation/korean/HoK_music_l_korean.yml": remove_localisation_keys(
            (HOK_ROOT / "localisation/korean/HoK_music_l_korean.yml").read_bytes(),
            {"Minshu_ikki"},
        ),
        "localisation/english/HoK_start_game_setup_l_english.yml": build_setup_localisation(
            "localisation/english/HoK_start_game_setup_l_english.yml"
        ),
        "localisation/korean/HoK_start_game_setup_l_korean.yml": build_setup_localisation(
            "localisation/korean/HoK_start_game_setup_l_korean.yml"
        ),
        "localisation/english/korea_event_l_english.yml": build_event_localisation(
            "localisation/english/korea_event_l_english.yml"
        ),
        "localisation/korean/korea_event_l_korean.yml": build_event_localisation(
            "localisation/korean/korea_event_l_korean.yml"
        ),
    }


def safe_path(relative: str) -> Path:
    path = (REPO_ROOT / Path(relative)).resolve()
    try:
        path.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise PruneError(f"path escapes repository: {path}") from exc
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    generated = outputs()
    mismatches = False
    for relative, expected in generated.items():
        path = safe_path(relative)
        current = path.read_bytes() if path.is_file() else None
        if current == expected:
            print(f"unchanged {relative} {sha256(expected)}")
        elif args.apply:
            temporary = path.with_name(path.name + ".hok-korea-only.tmp")
            temporary.write_bytes(expected)
            temporary.replace(path)
            print(f"written   {relative} {sha256(expected)}")
        else:
            print(f"mismatch  {relative}")
            mismatches = True

    for relative in REMOVE_FILES:
        path = safe_path(relative)
        if path.is_dir():
            raise PruneError(f"refusing to remove a directory: {path}")
        if path.exists() and args.apply:
            path.unlink()
            print(f"removed   {relative}")
        elif path.exists():
            print(f"present   {relative}")
            mismatches = True
        else:
            print(f"absent    {relative}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
