#!/usr/bin/env python3
"""Build the HOK-first Korean sound and basic-aircraft asset layer.

Binary payloads are copied byte-for-byte from the pinned HOK donor.  Logical
registries remain single-owner: the Korean voice registry shadows RT56 at the
same virtual path, while the three HOK aircraft meshes/entities use new
compatibility IDs instead of redefining RT56's KOR IDs.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
# [2026-09-22]_kpopmodder: Use the reviewed donor snapshot, excluding unrelated updates.
from source_snapshot import HOK_ROOT
RT56_ROOT = Path(
    r"C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968"
)
VANILLA_ROOT = Path(
    r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV"
)
LOCALISATION_ROOTS = (
    Path(r"C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\2743487021"),
    Path(r"C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\2769576030"),
)

DONOR_VOICE_REGISTRY = Path("sound/voice_korea.asset")
MERGED_VOICE_REGISTRY = Path("sound/r56_vo_Korean.asset")
MESH_REGISTRY = Path("gfx/entities/kor_planes.gfx")
ENTITY_REGISTRY = Path("gfx/entities/_HoK_units_planes.asset")
GRAPHIC_DB = Path("gfx/interface/equipmentdesigner/graphic_db/00_hok_plane_icons.txt")

VOICE_WAV_HASHES = {
    Path("sound/kor/kor_Idle_001.wav"): "EA99E7F94D80D2AF54A7CB75158845F576C33C905DA17A175179F064656A17E1",
    Path("sound/kor/kor_Idle_002.wav"): "2611BFF8210A00DB08AAC1083D9D4A7C0B93230182AB95BF1D0AF62BE7A86E6C",
    Path("sound/kor/kor_Idle_003.wav"): "E419F7D5B13CF8816261574A02BF6B390944CA88CEEC4DF93E3F9DC06B6C26C7",
    Path("sound/kor/kor_Idle_004.wav"): "423A9FFAAA30585346A1B4B628D227C37F9DD2EEEB200B79E9DADC135E215A1E",
    Path("sound/kor/kor_Idle_005.wav"): "E1B18119F7AB40F687518D61650BCBE70A15D6559EBA7BE309C3F00F15653442",
    Path("sound/kor/kor_Neutral_001.wav"): "9BCB5BD3107BC9741B2E033144E950E5AA22C8B902888771DE9EDE641182CDD1",
    Path("sound/kor/kor_Neutral_002.wav"): "0FE926756A983D9D32DB2F9486E9EF027C653172AAC199B3860BDF06603CAA33",
    Path("sound/kor/kor_Neutral_003.wav"): "C1659158694629BFA3B7408EDB4CD9160C42E4B5BFA54876BCF2816FA92D4F21",
    Path("sound/kor/kor_Neutral_004.wav"): "3F5DB06C0D43AD2E13070030A36012CC85DF428B861A15FF605D4E3C9C030AF9",
    Path("sound/kor/kor_Positive_001.wav"): "C32C773E24A7CBD5275675E9E70233310D5414DA99AECE8AB1DE3D5CF699FCDC",
    Path("sound/kor/kor_Positive_002.wav"): "CF15D8D741F3AD291CC76262F0CBF1835F817D1225AEAB26A1BEE2F1776E47D1",
    Path("sound/kor/kor_Positive_003.wav"): "C4BB33E674E6143C0B05AD4B6B5D2301AA4ADCE7EE25532E0EFBF1AD836392CC",
    Path("sound/kor/kor_Positive_004.wav"): "42AD6F6600E743FB55FC9A908EB6D2D92BED03756FB86F5A71459D66FB6F60AE",
    Path("sound/kor/kor_Positive_005.wav"): "6D00A237DE485634AEBD9B921DB82FC7611E7D0FAE0D03973039D562FD6F350B",
    Path("sound/kor/kor_Retreat_001.wav"): "2409B58C4A156E404D4A6066B2F5AB0F71C083C1EF2C4DB5A2EBACE9E66CF848",
    Path("sound/kor/kor_Retreat_002.wav"): "055C0F776D75EF220DFFCDC2D76436D85337BA2E81513D7F3F72DF7931E909A4",
    Path("sound/kor/kor_Retreat_003.wav"): "8EB7CBFD7AF83AC9A19BDCD5A23A838E87F861508EAE866750A766752056732B",
    Path("sound/kor/kor_Retreat_004.wav"): "72DCBC970CEA5CCDADE4E344BDA64A513C6717D96A0C0D0F1DFFE867E0F42A32",
}

PLANE_PAYLOAD_HASHES = {
    Path("gfx/models/units/planes/KOR_plane_heavy.mesh"): "801091369F40E139485DE0B19DA8C3052382F12A6CD5F04532BE8450BCFA181C",
    Path("gfx/models/units/planes/KOR_plane_heavy_diffuse.dds"): "928261DC72768191D4C8DBDDBC6086B788ADDD23B837F2485D4F90479BD3EE22",
    Path("gfx/models/units/planes/KOR_plane_heavy_normal.dds"): "93C2BEF24FA914F0A41B62F7E1774C55BAE70C3354EB92C318FCFCE0DDE5BFBA",
    Path("gfx/models/units/planes/KOR_plane_heavy_specular.dds"): "21A8237B71623BED37FC5E90127067BD77916A29094F3286EF8B8A17433F92B9",
    Path("gfx/models/units/planes/KOR_plane_light.mesh"): "4C9B8E03E258F3F686F8DAC0E40CBF4F12F26B7FC12001BD67E113178C31EDBD",
    Path("gfx/models/units/planes/KOR_plane_light_diffuse.dds"): "549C0347462CD950661C33A7698ADF4AC007841F0C38369B09912ABED02C5DEE",
    Path("gfx/models/units/planes/KOR_plane_light_normal.dds"): "76461891ECB63039C0D00157863295DDACB6D2882BD304C9B373906B0449C204",
    Path("gfx/models/units/planes/KOR_plane_light_specular.dds"): "AEBEA2814F0D9ADE66B3CEDA1DBBFF3C14470859CFE71AA4246C4D990E2125A5",
    Path("gfx/models/units/planes/KOR_plane_medium.mesh"): "630006DC33C56A090E4A1D65FAD5C17E5D69957EE29D47DFFBA944E324CFBAF2",
    Path("gfx/models/units/planes/KOR_plane_medium_diffuse.dds"): "F8468B21D0B8974964A42428D3D73A7ECB3DD78AF25A448BE5A858DD68E4C74C",
    Path("gfx/models/units/planes/KOR_plane_medium_normal.dds"): "CDEF99A8684C0EAD2A2DD31A2BC40103CEF8A60E5C1B3309EB46D05AACA2FADE",
    Path("gfx/models/units/planes/KOR_plane_medium_specular.dds"): "DED9AA9FB735A8B7BDFE1ACCD6C7C501E3CFF079A29CFFAC6C923B80FB1799D7",
}

SOURCE_HASHES = {
    HOK_ROOT / DONOR_VOICE_REGISTRY:
        "41837D11DAAC2369529C4BEAED29E1E44DBA66DD455016F12B8972B810E4389C",
    RT56_ROOT / MERGED_VOICE_REGISTRY:
        "F74123EFFA722D1111A1FA23CA3B921B55D4650A41ADE667ACDCD72E65565827",
    HOK_ROOT / MESH_REGISTRY:
        "4F344CCA7D5E7532E1209010E0974F3A532321A3D2110AAAA02AD122419B30C6",
    HOK_ROOT / ENTITY_REGISTRY:
        "90C1A5568C87404D3FF08360AF969651E3296066CF9F22E73ECA5942707E31BB",
    HOK_ROOT / GRAPHIC_DB:
        "E3E61E2EB055DCE0C1167AFFD77BD3158D79F8BACB889D86F8BA88E4525E3AAE",
    RT56_ROOT / "gfx/entities/r56_meshes_planes.gfx":
        "B6B1497E725F5BE137D938590560E451C31E93DA9360DC90A7175DE6201B48CB",
    RT56_ROOT / "gfx/entities/units_planes.asset":
        "3ACB570BF844D5F36DB36AB8D07DB6D9B067DA44C072A5BAFFBD8E370CB08A8B",
}
SOURCE_HASHES.update({HOK_ROOT / path: digest for path, digest in VOICE_WAV_HASHES.items()})
SOURCE_HASHES.update({HOK_ROOT / path: digest for path, digest in PLANE_PAYLOAD_HASHES.items()})

MESH_IDS = {
    "KOR_plane_light_mesh": "hok_rt56_KOR_plane_light_mesh",
    "KOR_plane_medium_mesh": "hok_rt56_KOR_plane_medium_mesh",
    "KOR_plane_heavy_mesh": "hok_rt56_KOR_plane_heavy_mesh",
}

ENTITY_IDS = {
    "KOR_light_plane_entity": "hok_rt56_KOR_light_plane_entity",
    "KOR_medium_plane_entity": "hok_rt56_KOR_medium_plane_entity",
    "KOR_heavy_plane_entity": "hok_rt56_KOR_heavy_plane_entity",
}

VOICE_EFFECT_IDS = {
    "KOR_infantry_idle",
    "KOR_infantry_neutral_combat",
    "KOR_infantry_positive_combat",
    "KOR_infantry_retreat",
    "KOR_infantry_move_out",
}

VOICE_SOUND_IDS = {
    *(f"kor_Idle_{index:03d}" for index in range(1, 16)),
    *(f"kor_Neutral_{index:03d}" for index in range(1, 5)),
    *(f"kor_Positive_{index:03d}" for index in range(1, 6)),
    *(f"kor_Retreat_{index:03d}" for index in range(1, 5)),
}

ACCEPTED_PRIOR_OUTPUT_HASHES = {
    MESH_REGISTRY: "C1ABE4168176562886EA4924D356272838F467548B4A6929D2D5974F1326BA93",
    ENTITY_REGISTRY: "11869B21E1F40701BE5DC32561554AD8E37AEC03D48398758269EE2FB986BD31",
    GRAPHIC_DB: "85C49967B2436E75B1C9C5EF0EFC8952FC7E3082CA1575570693659B3500A000",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def normalized_source(path: Path) -> tuple[str, bool, str]:
    data = path.read_bytes()
    bom = data.startswith(b"\xef\xbb\xbf")
    text = (data[3:] if bom else data).decode("utf-8")
    if "\r" in text.replace("\r\n", ""):
        raise ValueError(f"unsupported lone CR in {path}")
    newline = "\r\n" if "\r\n" in text else "\n"
    return text.replace("\r\n", "\n"), bom, newline


def encode_like(text: str, bom: bool, newline: str) -> bytes:
    payload = text.replace("\n", newline).encode("utf-8")
    return (b"\xef\xbb\xbf" if bom else b"") + payload


def replace_count(text: str, old: str, new: str, expected: int, label: str) -> str:
    count = text.count(old)
    if count != expected:
        raise ValueError(f"{label}: expected {expected} occurrence(s), found {count}")
    return text.replace(old, new)


def matching_brace(text: str, opening: int) -> int:
    depth = 0
    quoted = False
    escaped = False
    comment = False
    for index in range(opening, len(text)):
        char = text[index]
        if char == "\n":
            comment = False
            continue
        if comment:
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
    raise ValueError(f"unclosed block at offset {opening}")


def block_spans(text: str, key: str) -> list[tuple[int, int]]:
    pattern = re.compile(
        rf"(?m)^[ \t]*{re.escape(key)}[ \t]*=[ \t\r\n]*\{{"
    )
    spans = []
    for match in pattern.finditer(text):
        opening = text.find("{", match.start(), match.end())
        spans.append((match.start(), matching_brace(text, opening)))
    return spans


def named_block_span(text: str, key: str, name: str) -> tuple[int, int]:
    name_pattern = re.compile(rf"\bname[ \t]*=[ \t]*\"{re.escape(name)}\"")
    matches = []
    for start, end in block_spans(text, key):
        if name_pattern.search(text[start:end]):
            matches.append((start, end))
    if len(matches) != 1:
        raise ValueError(f"{key} {name!r}: expected one block, found {len(matches)}")
    return matches[0]


def first_block_span(text: str, key: str) -> tuple[int, int]:
    spans = block_spans(text, key)
    if not spans:
        raise ValueError(f"missing {key} block")
    return spans[0]


def verify_sources() -> None:
    errors = []
    for path, expected in SOURCE_HASHES.items():
        if not path.is_file():
            errors.append(f"missing source: {path}")
            continue
        actual = sha256(path)
        if actual != expected:
            errors.append(
                f"source drift: {path}\n  expected {expected}\n  actual   {actual}"
            )
    if errors:
        raise RuntimeError("\n".join(errors))


def verify_rt56_id_contract() -> str:
    mesh_text, _, _ = normalized_source(
        RT56_ROOT / "gfx/entities/r56_meshes_planes.gfx"
    )
    entity_text, _, _ = normalized_source(
        RT56_ROOT / "gfx/entities/units_planes.asset"
    )
    for old, new in MESH_IDS.items():
        named_block_span(mesh_text, "pdxmesh", old)
        if new in mesh_text or new in entity_text:
            raise ValueError(f"compatibility mesh ID already exists in RT56: {new}")
    for old, new in ENTITY_IDS.items():
        named_block_span(entity_text, "entity", old)
        if new in mesh_text or new in entity_text:
            raise ValueError(f"compatibility entity ID already exists in RT56: {new}")

    medium_start, medium_end = named_block_span(
        entity_text, "entity", "KOR_medium_plane_entity"
    )
    medium = entity_text[medium_start:medium_end]
    supply_start, supply_end = named_block_span(medium, "state", "supply")
    return medium[supply_start:supply_end]


def verify_namespaces_unoccupied() -> None:
    plane_ids = set(MESH_IDS.values()) | set(ENTITY_IDS.values())
    voice_ids = VOICE_SOUND_IDS | VOICE_EFFECT_IDS
    checks = [
        (RT56_ROOT, RT56_ROOT / "gfx", {".gfx", ".asset"}, plane_ids, set()),
        (
            ROOT,
            ROOT / "gfx",
            {".gfx", ".asset", ".txt"},
            plane_ids,
            {MESH_REGISTRY, ENTITY_REGISTRY, GRAPHIC_DB},
        ),
        (
            RT56_ROOT,
            RT56_ROOT / "sound",
            {".asset"},
            voice_ids,
            {MERGED_VOICE_REGISTRY},
        ),
        (
            ROOT,
            ROOT / "sound",
            {".asset"},
            voice_ids,
            {MERGED_VOICE_REGISTRY, DONOR_VOICE_REGISTRY},
        ),
        (VANILLA_ROOT, VANILLA_ROOT / "gfx", {".gfx", ".asset"}, plane_ids, set()),
        (VANILLA_ROOT, VANILLA_ROOT / "sound", {".asset"}, voice_ids, set()),
    ]
    for localisation_root in LOCALISATION_ROOTS:
        checks.extend(
            (
                (
                    localisation_root,
                    localisation_root / "gfx",
                    {".gfx", ".asset", ".txt"},
                    plane_ids,
                    set(),
                ),
                (
                    localisation_root,
                    localisation_root / "sound",
                    {".asset"},
                    voice_ids,
                    set(),
                ),
            )
        )

    for base, directory, suffixes, identifiers, excluded_relatives in checks:
        if not directory.is_dir():
            continue
        for path in directory.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in suffixes:
                continue
            relative = path.relative_to(base)
            if relative in excluded_relatives:
                continue
            try:
                text = path.read_bytes().decode("utf-8-sig")
            except UnicodeDecodeError:
                continue
            for identifier in identifiers:
                if re.search(
                    rf'(?m)^[^#\r\n]*\bname[ \t]*=[ \t]*"{re.escape(identifier)}"',
                    text,
                ):
                    raise ValueError(
                        f"compatibility registry ID {identifier!r} already exists in {path}"
                    )


def build_voice_registry() -> bytes:
    donor, _, _ = normalized_source(HOK_ROOT / DONOR_VOICE_REGISTRY)
    rt56, bom, newline = normalized_source(RT56_ROOT / MERGED_VOICE_REGISTRY)
    donor_start, donor_end = first_block_span(donor, "category")
    rt56_start, rt56_end = first_block_span(rt56, "category")
    donor_category = donor[donor_start:donor_end]
    rt56_category = rt56[rt56_start:rt56_end]

    effect_ref = re.compile(r"(?m)^[ \t]*(KOR_infantry_[A-Za-z0-9_]+)[ \t]*$")
    if set(effect_ref.findall(donor_category)) != VOICE_EFFECT_IDS:
        raise ValueError("donor Korean voice category membership changed")
    if set(effect_ref.findall(rt56_category)) != VOICE_EFFECT_IDS:
        raise ValueError("RT56 Korean voice category membership changed")
    if "compressor" not in rt56_category:
        raise ValueError("RT56 voice compressor contract is missing")

    donor_definitions = (donor[:donor_start] + donor[donor_end:]).strip()
    merged = (
        "# Generated by tools/build_korean_assets.py.\n"
        "# RT56 owns the current category/compressor schema; HOK owns the Korean "
        "samples, playback lists, weights, and volume.\n\n"
        + rt56_category.strip()
        + "\n\n"
        + donor_definitions
        + "\n"
    )
    return encode_like(merged, bom, newline)


def build_mesh_registry() -> bytes:
    text, bom, newline = normalized_source(HOK_ROOT / MESH_REGISTRY)
    for old, new in MESH_IDS.items():
        text = replace_count(
            text,
            f'name = "{old}"',
            f'name = "{new}"',
            1,
            f"HOK mesh ID {old}",
        )
    text = replace_count(
        text,
        "objectTypes = {\n",
        "objectTypes = {\n\t# Compatibility-local IDs keep HOK models without redefining RT56 KOR meshes.\n",
        1,
        "HOK plane registry header",
    )
    return encode_like(text, bom, newline)


def build_entity_registry(supply_state: str) -> bytes:
    text, bom, newline = normalized_source(HOK_ROOT / ENTITY_REGISTRY)
    for old, new in ENTITY_IDS.items():
        text = replace_count(
            text,
            f'name = "{old}"',
            f'name = "{new}"',
            1,
            f"HOK entity ID {old}",
        )
    for old, new in MESH_IDS.items():
        text = replace_count(
            text,
            f'pdxmesh = "{old}"',
            f'pdxmesh = "{new}"',
            1,
            f"HOK entity mesh reference {old}",
        )

    medium_start, medium_end = named_block_span(
        text, "entity", "hok_rt56_KOR_medium_plane_entity"
    )
    medium = text[medium_start:medium_end]
    bomb_start, bomb_end = named_block_span(medium, "state", "bomb")
    medium = medium[:bomb_end] + "\n" + supply_state + medium[bomb_end:]
    text = text[:medium_start] + medium + text[medium_end:]
    text = (
        "# HOK basic aircraft use compatibility-local IDs; the medium entity keeps "
        "RT56's current supply-drop state.\n\n"
        + text
    )
    return encode_like(text, bom, newline)


def build_graphic_db() -> bytes:
    text, bom, newline = normalized_source(HOK_ROOT / GRAPHIC_DB)
    for old, new, expected in (
        ("KOR_light_plane_entity", "hok_rt56_KOR_light_plane_entity", 2),
        ("KOR_medium_plane_entity", "hok_rt56_KOR_medium_plane_entity", 1),
        ("KOR_heavy_plane_entity", "hok_rt56_KOR_heavy_plane_entity", 1),
    ):
        text = replace_count(text, old, new, expected, f"HOK graphic model {old}")
    text = replace_count(
        text,
        "supersonic_fighter_equipment_1",
        "jet_fighter_equipment_x",
        1,
        "removed HOK supersonic equipment ID",
    )
    return encode_like(text, bom, newline)


def verify_voice_output(data: bytes) -> None:
    text = data.decode("utf-8-sig").replace("\r\n", "\n")
    for identifier in VOICE_EFFECT_IDS | VOICE_SOUND_IDS:
        count = len(
            re.findall(
                rf'\bname[ \t]*=[ \t]*"{re.escape(identifier)}"',
                text,
            )
        )
        if count != 1:
            raise ValueError(f"merged voice registry defines {identifier!r} {count} times")

    file_refs = {
        Path("sound") / match
        for match in re.findall(r'file[ \t]*=[ \t]*"(kor/[^"]+\.wav)"', text)
    }
    if file_refs != set(VOICE_WAV_HASHES):
        missing = sorted(set(VOICE_WAV_HASHES) - file_refs)
        extra = sorted(file_refs - set(VOICE_WAV_HASHES))
        raise ValueError(f"merged voice WAV set changed: missing={missing}, extra={extra}")
    if 'file = "kor/kor_Idle_006.wav"' in text:
        raise ValueError("merged voice registry still references RT56-only Idle_006 payload")
    if 'file = "kor/kor_Neutral_005.wav"' in text:
        raise ValueError("merged voice registry still references RT56-only Neutral_005 payload")
    if "kor_Positive_005" not in text:
        raise ValueError("merged voice registry omits HOK Positive_005")


def verify_plane_outputs(outputs: dict[Path, bytes]) -> None:
    mesh_text = outputs[MESH_REGISTRY].decode("utf-8-sig").replace("\r\n", "\n")
    entity_text = outputs[ENTITY_REGISTRY].decode("utf-8-sig").replace("\r\n", "\n")
    graphic_text = outputs[GRAPHIC_DB].decode("utf-8-sig").replace("\r\n", "\n")
    for old, new in MESH_IDS.items():
        if f'name = "{new}"' not in mesh_text or f'name = "{old}"' in mesh_text:
            raise ValueError(f"HOK mesh migration is incomplete: {old} -> {new}")
        if f'pdxmesh = "{new}"' not in entity_text:
            raise ValueError(f"HOK entity does not consume compatibility mesh {new}")
    for old, new in ENTITY_IDS.items():
        if f'name = "{new}"' not in entity_text or f'name = "{old}"' in entity_text:
            raise ValueError(f"HOK entity migration is incomplete: {old} -> {new}")
        if new not in graphic_text:
            raise ValueError(f"HOK graphic database does not consume {new}")
    medium_start, medium_end = named_block_span(
        entity_text, "entity", "hok_rt56_KOR_medium_plane_entity"
    )
    named_block_span(entity_text[medium_start:medium_end], "state", "supply")
    if "supersonic_fighter_equipment_1" in graphic_text:
        raise ValueError("removed supersonic equipment ID remains in HOK graphic database")


def build_outputs() -> dict[Path, bytes]:
    verify_sources()
    supply_state = verify_rt56_id_contract()
    verify_namespaces_unoccupied()
    outputs = {
        MERGED_VOICE_REGISTRY: build_voice_registry(),
        MESH_REGISTRY: build_mesh_registry(),
        ENTITY_REGISTRY: build_entity_registry(supply_state),
        GRAPHIC_DB: build_graphic_db(),
    }
    outputs.update({path: (HOK_ROOT / path).read_bytes() for path in VOICE_WAV_HASHES})
    outputs.update({path: (HOK_ROOT / path).read_bytes() for path in PLANE_PAYLOAD_HASHES})
    verify_voice_output(outputs[MERGED_VOICE_REGISTRY])
    verify_plane_outputs(outputs)
    return outputs


def preflight(outputs: dict[Path, bytes]) -> None:
    legacy = ROOT / DONOR_VOICE_REGISTRY
    if legacy.exists():
        raise RuntimeError(
            f"duplicate-prone donor registry must remain absent: {DONOR_VOICE_REGISTRY}"
        )
    errors = []
    for relative, expected in outputs.items():
        destination = (ROOT / relative).resolve()
        destination.relative_to(ROOT)
        if not destination.is_file():
            continue
        current = destination.read_bytes()
        if current == expected:
            continue
        accepted = ACCEPTED_PRIOR_OUTPUT_HASHES.get(relative)
        if accepted is None or sha256_bytes(current) != accepted:
            errors.append(f"refusing to overwrite independently changed file: {relative}")
    if errors:
        raise RuntimeError("\n".join(errors))


def apply(outputs: dict[Path, bytes]) -> None:
    preflight(outputs)
    for relative, expected in outputs.items():
        destination = (ROOT / relative).resolve()
        destination.relative_to(ROOT)
        if destination.is_file() and destination.read_bytes() == expected:
            print(f"unchanged: {relative.as_posix()}")
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(destination.name + ".hok-asset.tmp")
        temporary.write_bytes(expected)
        temporary.replace(destination)
        print(f"wrote: {relative.as_posix()}")


def check(outputs: dict[Path, bytes]) -> bool:
    ok = True
    legacy = ROOT / DONOR_VOICE_REGISTRY
    if legacy.exists():
        print(f"UNEXPECTED: {DONOR_VOICE_REGISTRY.as_posix()}")
        ok = False
    for relative, expected in outputs.items():
        destination = ROOT / relative
        if not destination.is_file():
            print(f"MISSING: {relative.as_posix()}")
            ok = False
        elif destination.read_bytes() != expected:
            print(f"MISMATCH: {relative.as_posix()}")
            ok = False
        else:
            print(f"OK: {relative.as_posix()}")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = build_outputs()
    if args.apply:
        apply(outputs)
        return 0
    return 0 if check(outputs) else 1


if __name__ == "__main__":
    raise SystemExit(main())
