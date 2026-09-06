#!/usr/bin/env python3
"""Build the Hearts of Korea map delta on top of the pinned RT56 map.

The donor and Workshop trees are immutable inputs.  Every output is written
under this repository.  The script refuses to run when a pinned input hash no
longer matches, because silently rebuilding against a newer Workshop snapshot
would make the resulting port impossible to audit.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import struct
import sys
from collections import Counter, defaultdict
from decimal import Decimal, ROUND_FLOOR
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HOK_ROOT = Path(r"C:\hoi\hearts_of_korea")
RT56_ROOT = Path(
    r"C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968"
)
VANILLA_ROOT = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV")

EXPECTED_SHA256 = {
    HOK_ROOT / "map/definition.csv": "0DD53CE40928593FA59C4661863EA4257BDC1E3EC8FDA6D3F790C319A2F8F228",
    HOK_ROOT / "map/provinces.bmp": "A00EC0E8C18E9F405FC7E7EA59A77848870F03C79E9E5F78CF6E12272D867600",
    HOK_ROOT / "map/buildings.txt": "DA7A22BC7F3996FC89496BEE248B530FA7039917564AD50B09F6B05A7F574A53",
    HOK_ROOT / "map/railways.txt": "BF651E0ED911AE67BE40592115E3BACD96E30950E8D64302E19EA2FAF853FD0C",
    HOK_ROOT / "map/supply_nodes.txt": "E34602B74E50A9A77CA5995EB621111F81B70D8D3DA84FD6B175FA2BB0E7E396",
    HOK_ROOT / "map/unitstacks.txt": "2A794AAC4EFD8752E70FF1E72235A16904A2860B6C41D801EED8DF39AF2413D9",
    HOK_ROOT / "map/strategicregions/186-Korea.txt": "A52B44F8D1FF6CA2638666014E3C82EDAA19186BC047C131F27EFE3EAE97E80E",
    HOK_ROOT / "history/states/525-South Korea.txt": "D9AC2E47161042DDBB2C508C4B07C4C46B7A55F7C1B17B3F550394D59D2AF035",
    HOK_ROOT / "history/states/527-North Korea.txt": "10910C113D3411E38105BAD3A23E242E5BEFDC34BB86C2B36A2237A3A742A636",
    HOK_ROOT / "history/states/528-Nagasaki.txt": "7ED9DFE5BE88BC05B61B02186654AB9D422A76B72E8CB4391D1BFA2142FC8049",
    HOK_ROOT / "history/states/1028 - Hamgyong.txt": "AA78EBB97BE029CA741CD41AC60F7B47974EC05B7DE702CE199404EF453CF759",
    HOK_ROOT / "history/states/1029 - Gangwon.txt": "722BF8DF0B7D9AB8311B9AFFD6B96394F3BF55066312847B168459A0B4710854",
    HOK_ROOT / "history/states/1030 - Gyeongsang.txt": "4EE5219EA4927EE05D2D7BA0153EC86693A273F7D62C29CE6112FD2F8CC18C30",
    HOK_ROOT / "history/states/1031 - Chungcheong Jeolla.txt": "519A076648462C8D7A202CEE77879E2FCB31BC322A35F788F53702BCA12EBA67",
    HOK_ROOT / "history/states/1082 - Jeolla.txt": "42BED2B37CCE3109A5E71F03BDDFE1B3A3C08F5A79CA103F4A2CBA61C643AE7D",
    HOK_ROOT / "history/states/1083 - Hwanghae.txt": "3830F398FE1D316A70B719FCCA445EC9F94658F1230BCBFB059BA753C85E04FB",
    HOK_ROOT / "history/states/1084 - Jeju.txt": "4EB50FA4D264E6C619552E90F38E455671C22FFAB508AE8C9D4D004FCF220714",
    HOK_ROOT / "history/states/1085 - Tsushima.txt": "CE45376BB74D5AE944BCEBD7F964DE87AF9D025618FD863D385B2ED73836752F",
    RT56_ROOT / "map/definition.csv": "005BB6052AEDBAA85FFE4607B21398A33055624A78C2F822F116AE895B58393E",
    RT56_ROOT / "map/provinces.bmp": "B41B67B844407C70EB393E6979DCB8EE718BA76596ECEB2A9CCD38171156580F",
    RT56_ROOT / "map/buildings.txt": "5622673138F7269FA433E80CA19B49F5C48B52E7AA386568F4E6C3E96B0F99BB",
    RT56_ROOT / "map/railways.txt": "ECBDBFE17B5463019A3952F0B17887552F2AF6301D99F6BD5E22FEAA39566ECE",
    RT56_ROOT / "map/supply_nodes.txt": "45595220BDE8C7B7FC9CEAD07A0EB4C5F48370548B51C0950520AB58EF83716F",
    RT56_ROOT / "map/unitstacks.txt": "82C382B0D0BBF8944199A45A459BCB90B3A612E9D29996C1FC8BCE3C935998F4",
    RT56_ROOT / "map/strategicregions/186-Korea.txt": "7DE709723F219D435693D3C37641D724F1CBB1FB67C4CC99A4940F10533D2DCC",
    RT56_ROOT / "history/states/525-South Korea.txt": "2973C57539CF1FA9A8E09430C02AE76D0E27EB3F189E169C68A8F95B035B8772",
    RT56_ROOT / "history/states/527-North Korea.txt": "93B7536CDADDC263EF73E7A93DBD7E4233CF7E69FA46DAF9685A251A1B9E2E77",
    RT56_ROOT / "history/states/528-Nagasaki.txt": "85D237EF932FC45F0CF152F107A7BDEB9BAB362C32F842010D5BDB53E649458A",
    RT56_ROOT / "history/states/917-Hwanghae.txt": "D11EDC8E0CDCA2A604CFA0CC535E9033E696E23C911DA1CDAD09F171C8B23D82",
    RT56_ROOT / "history/states/918-Hamgyong.txt": "B057B15D33E068D27C32C176BF79A717154E8323205AD6E512308A24872B527B",
    RT56_ROOT / "history/states/919-Jeolla.txt": "F6E8DCC3ECB96A9E6C25E535816F5FC967E05CB5A743F4695169A126555CB064",
    RT56_ROOT / "history/states/920-Gyeongsang.txt": "DED093FD53A6D61672582D27945FD0F9F17BFC707C76768C9E433A380B14C4BB",
    VANILLA_ROOT / "map/provinces.bmp": "E131D30E5DCB13D9C2A8598F820A2DE0AE9828F3A24F2BDDC1BCFFF40F71660A",
    VANILLA_ROOT / "map/buildings.txt": "4A336B6245026FCC693ED2BE7AE316A164135585AEC945EA190E32B8E65F4094",
    VANILLA_ROOT / "map/railways.txt": "86CC3FBA40F39442BB4BF883A51740951C09073C5234E6B7B744D966FA2EE455",
}

# RT56 currently ends at province 13534.  HOK RGB values are globally unique
# in that snapshot, so only the numeric IDs have to move.
PROVINCE_ID_MAP = {old: 13535 + (old - 13414) for old in range(13414, 13448)}

# RT56 already owns the semantically equivalent Hwanghae, Hamgyong, Jeolla,
# and Gyeongsang states.  Reuse those stable IDs and allocate only states that
# RT56 does not have.
STATE_ID_MAP = {
    1028: 918,   # Hamgyong
    1029: 1144,  # Gangwon (new)
    1030: 920,   # Gyeongsang
    1031: 1145,  # Chungcheong (new)
    1082: 919,   # Jeolla
    1083: 917,   # Hwanghae
    1084: 1146,  # Jeju (new)
    1085: 1147,  # Tsushima (new)
}

HOK_STATE_SOURCES = {
    525: "525-South Korea.txt",
    527: "527-North Korea.txt",
    528: "528-Nagasaki.txt",
    1028: "1028 - Hamgyong.txt",
    1029: "1029 - Gangwon.txt",
    1030: "1030 - Gyeongsang.txt",
    1031: "1031 - Chungcheong Jeolla.txt",
    1082: "1082 - Jeolla.txt",
    1083: "1083 - Hwanghae.txt",
    1084: "1084 - Jeju.txt",
    1085: "1085 - Tsushima.txt",
}

STATE_OUTPUT_NAMES = {
    525: "525-South Korea.txt",
    527: "527-North Korea.txt",
    528: "528-Nagasaki.txt",
    917: "917-Hwanghae.txt",
    918: "918-Hamgyong.txt",
    919: "919-Jeolla.txt",
    920: "920-Gyeongsang.txt",
    1144: "1144-Gangwon.txt",
    1145: "1145-Chungcheong.txt",
    1146: "1146-Jeju.txt",
    1147: "1147-Tsushima.txt",
}

KOREA_STATE_IDS = set(STATE_OUTPUT_NAMES)
BUILDING_TARGET_STATES = KOREA_STATE_IDS - {528}
EXPECTED_OVERLAY_PIXELS = 1889
COASTAL_FALSE_PROVINCES = {4126, 7125, 7175, 7204, 10065}

# These seven donor rows are byte-for-byte vanilla placements, but the pinned
# RT56 buildings database no longer contains them.  A plain donor-vs-vanilla
# delta therefore drops ports that the restored HOK coastline needs.  Keep the
# allowlist narrow: hundreds of other vanilla-identical donor rows are absent
# from RT56 and must not be restored wholesale.
REQUIRED_KOREAN_COASTAL_SPAWN_ROWS = (
    (b"1030;naval_base_spawn;4825.00;9.78;1251.00;1.57;7932", 7121),
    (b"1030;naval_base_spawn;4826.00;9.70;1245.00;1.57;7932", 13556),
    (b"1030;naval_base_spawn;4816.00;9.50;1233.00;0.79;7932", 12060),
    (b"1030;naval_base_spawn;4804.00;9.50;1226.00;0.32;2708", 1054),
    (b"1031;naval_base_spawn;4778.00;9.50;1263.00;-2.36;2781", 13564),
    (b"1082;naval_base_spawn;4779.00;9.50;1238.00;-2.21;2781", 13546),
    (b"1030;naval_base_spawn;4825.00;9.90;1266.00;-4.51;7932", 11912),
)
EXPECTED_RT56_COASTAL_WITHOUT_SPAWN = {490, 1201, 10715}

# These placements have the same donor/vanilla relationship as the coastal
# rows above: the HOK geometry moved their original vanilla sites, while RT56
# omitted those exact rows.  Without narrowly restoring them, the generated
# Korean states have no valid air/rocket placement site at runtime.
REQUIRED_KOREAN_STATE_SITE_ROWS = (
    (b"1083;air_base;4766.00;9.53;1284.00;6.14;0", 13559),
    (b"1082;air_base;4781.00;9.70;1237.00;4.03;0", 13546),
    (b"1082;rocket_site_spawn;4785.00;9.70;1230.00;1.82;0", 10110),
)
REQUIRED_STATE_SITE_TYPES = (b"air_base", b"rocket_site_spawn")

EXPECTED_STATE_VICTORY_POINTS = {
    525: {7125, 7221, 12040, 13535},
    527: {4052, 11835, 6963, 13536},
    528: {1025, 9950, 10092},
    917: {13559},
    918: {6928, 6822, 848, 6944},
    919: {13551, 13545},
    920: {4056, 13557},
    1144: {13539},
    1145: {11977},
    1146: set(),
    1147: set(),
}


class BuildError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def verify_inputs() -> None:
    failures: list[str] = []
    for path, expected in EXPECTED_SHA256.items():
        if not path.is_file():
            failures.append(f"missing: {path}")
            continue
        actual = sha256_bytes(path.read_bytes())
        if actual != expected:
            failures.append(f"changed: {path}\n  expected {expected}\n  actual   {actual}")
    if failures:
        raise BuildError("Pinned source verification failed:\n" + "\n".join(failures))


def assert_output_path(relative: str) -> Path:
    path = (REPO_ROOT / relative).resolve()
    try:
        path.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise BuildError(f"output escapes repository: {path}") from exc
    return path


def write_if_changed(relative: str, data: bytes, apply: bool) -> str:
    path = assert_output_path(relative)
    current = path.read_bytes() if path.is_file() else None
    status = "unchanged" if current == data else "would-write"
    if apply and current != data:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(path.name + ".hok-rt56.tmp")
        temporary.write_bytes(data)
        temporary.replace(path)
        status = "written"
    return f"{status:11} {relative} {sha256_bytes(data)}"


def replace_numeric_tokens(data: bytes, mapping: dict[int, int]) -> bytes:
    result = data
    for old, new in sorted(mapping.items(), reverse=True):
        pattern = rb"(?<![0-9])" + str(old).encode() + rb"(?![0-9])"
        result = re.sub(pattern, str(new).encode(), result)
    return result


def parse_definition(data: bytes) -> dict[int, tuple[int, int, int, tuple[bytes, ...]]]:
    rows: dict[int, tuple[int, int, int, tuple[bytes, ...]]] = {}
    for raw_line in data.splitlines():
        if not raw_line.strip():
            continue
        fields = tuple(part.strip() for part in raw_line.split(b";"))
        if len(fields) < 8:
            raise BuildError(f"malformed definition row: {raw_line!r}")
        province_id = int(fields[0])
        if province_id in rows:
            raise BuildError(f"duplicate province ID {province_id}")
        rows[province_id] = (int(fields[1]), int(fields[2]), int(fields[3]), fields)
    return rows


def build_definition() -> bytes:
    rt_data = (RT56_ROOT / "map/definition.csv").read_bytes()
    hok_data = (HOK_ROOT / "map/definition.csv").read_bytes()
    rt_rows = parse_definition(rt_data)
    hok_rows = parse_definition(hok_data)

    expected_old = set(PROVINCE_ID_MAP)
    if not expected_old.issubset(hok_rows):
        raise BuildError("HOK custom province rows are incomplete")
    if set(PROVINCE_ID_MAP.values()) & set(rt_rows):
        raise BuildError("allocated province IDs are no longer free in RT56")

    rt_rgb = {(row[0], row[1], row[2]): province_id for province_id, row in rt_rows.items()}
    custom_rgb: set[tuple[int, int, int]] = set()
    additions: list[bytes] = []
    for old_id, new_id in PROVINCE_ID_MAP.items():
        red, green, blue, fields = hok_rows[old_id]
        rgb = (red, green, blue)
        if rgb in rt_rgb:
            raise BuildError(
                f"HOK RGB {rgb} for province {old_id} conflicts with RT56 province {rt_rgb[rgb]}"
            )
        if rgb in custom_rgb:
            raise BuildError(f"duplicate HOK custom RGB {rgb}")
        custom_rgb.add(rgb)
        additions.append(b";".join((str(new_id).encode(),) + fields[1:]))

    rebased_rows: list[bytes] = []
    changed_coastal: set[int] = set()
    for line in rt_data.splitlines():
        fields = line.split(b";")
        province_id = int(fields[0])
        if province_id in COASTAL_FALSE_PROVINCES:
            if fields[5].strip() != b"true":
                raise BuildError(
                    f"RT56 province {province_id} no longer has the expected coastal=true baseline"
                )
            fields[5] = b"false"
            line = b";".join(fields)
            changed_coastal.add(province_id)
        rebased_rows.append(line)
    if changed_coastal != COASTAL_FALSE_PROVINCES:
        raise BuildError(f"failed to update coastal provinces: {changed_coastal}")

    return b"\r\n".join(rebased_rows + additions) + b"\r\n"


def bmp_metadata(data: bytes) -> tuple[int, int, int, int, int]:
    if data[:2] != b"BM" or len(data) < 54:
        raise BuildError("provinces.bmp is not a supported BMP")
    pixel_offset = struct.unpack_from("<I", data, 10)[0]
    dib_size = struct.unpack_from("<I", data, 14)[0]
    width = struct.unpack_from("<i", data, 18)[0]
    height = struct.unpack_from("<i", data, 22)[0]
    planes = struct.unpack_from("<H", data, 26)[0]
    bits_per_pixel = struct.unpack_from("<H", data, 28)[0]
    compression = struct.unpack_from("<I", data, 30)[0]
    if dib_size < 40 or width <= 0 or height == 0:
        raise BuildError("unsupported BMP geometry")
    if planes != 1 or bits_per_pixel != 24 or compression != 0:
        raise BuildError(
            f"expected uncompressed 24-bit BMP, got planes={planes}, "
            f"bpp={bits_per_pixel}, compression={compression}"
        )
    row_stride = ((width * 3 + 3) // 4) * 4
    if pixel_offset + row_stride * abs(height) > len(data):
        raise BuildError("BMP pixel array exceeds file length")
    return pixel_offset, width, height, bits_per_pixel, row_stride


def build_provinces_bmp() -> tuple[bytes, Counter[int], int]:
    hok = (HOK_ROOT / "map/provinces.bmp").read_bytes()
    vanilla = (VANILLA_ROOT / "map/provinces.bmp").read_bytes()
    rt = bytearray((RT56_ROOT / "map/provinces.bmp").read_bytes())
    hok_meta = bmp_metadata(hok)
    vanilla_meta = bmp_metadata(vanilla)
    rt_meta = bmp_metadata(rt)
    if hok_meta != vanilla_meta or hok_meta != rt_meta:
        raise BuildError(
            f"BMP geometry mismatch: HOK={hok_meta}, vanilla={vanilla_meta}, RT56={rt_meta}"
        )

    definition = parse_definition((HOK_ROOT / "map/definition.csv").read_bytes())
    bgr_to_old_id = {
        bytes((definition[old][2], definition[old][1], definition[old][0])): old
        for old in PROVINCE_ID_MAP
    }
    rt_definition = parse_definition((RT56_ROOT / "map/definition.csv").read_bytes())
    allowed_bgr = {
        bytes((row[2], row[1], row[0])) for row in rt_definition.values()
    } | set(bgr_to_old_id)
    pixel_offset, width, height, _, row_stride = hok_meta
    counts: Counter[int] = Counter()
    overlay_pixels = 0
    for row in range(abs(height)):
        row_start = pixel_offset + row * row_stride
        for column in range(width):
            offset = row_start + column * 3
            colour = hok[offset : offset + 3]
            if colour != vanilla[offset : offset + 3]:
                if rt[offset : offset + 3] != vanilla[offset : offset + 3]:
                    x = column
                    top_y = abs(height) - 1 - row if height > 0 else row
                    raise BuildError(
                        f"RT56 changed inside the HOK overlay mask at x={x}, top-y={top_y}"
                    )
                if colour not in allowed_bgr:
                    raise BuildError(
                        f"HOK overlay colour {tuple(reversed(colour))} has no generated definition row"
                    )
                rt[offset : offset + 3] = colour
                overlay_pixels += 1
                old_id = bgr_to_old_id.get(colour)
                if old_id is not None:
                    counts[PROVINCE_ID_MAP[old_id]] += 1

    if set(counts) != set(PROVINCE_ID_MAP.values()):
        missing = sorted(set(PROVINCE_ID_MAP.values()) - set(counts))
        raise BuildError(f"custom provinces with no bitmap pixels: {missing}")
    if overlay_pixels != EXPECTED_OVERLAY_PIXELS:
        raise BuildError(
            f"expected {EXPECTED_OVERLAY_PIXELS} HOK overlay pixels, found {overlay_pixels}"
        )
    return bytes(rt), counts, overlay_pixels


def build_states() -> dict[str, bytes]:
    results: dict[str, bytes] = {}
    combined_map = {**PROVINCE_ID_MAP, **STATE_ID_MAP}
    for old_state, source_name in HOK_STATE_SOURCES.items():
        new_state = STATE_ID_MAP.get(old_state, old_state)
        if old_state == 528:
            source = RT56_ROOT / "history/states/528-Nagasaki.txt"
            data = source.read_bytes()
            province_pattern = re.compile(rb"(provinces\s*=\s*\{)(.*?)(\})", re.DOTALL)
            match = province_pattern.search(data)
            if not match:
                raise BuildError("could not locate RT56 state 528 province list")
            province_body, replacements = re.subn(
                rb"(?<![0-9])10011(?![0-9])", b"", match.group(2), count=1
            )
            if replacements != 1:
                raise BuildError("RT56 state 528 no longer contains Tsushima province 10011 once")
            data = data[: match.start(2)] + province_body + data[match.end(2) :]
            results[f"history/states/{STATE_OUTPUT_NAMES[new_state]}"] = data
            continue

        source = HOK_ROOT / "history/states" / source_name
        data = replace_numeric_tokens(source.read_bytes(), combined_map)
        if b"state_victory_points" in data:
            raise BuildError(f"donor state {old_state} unexpectedly already has RT56 VP hooks")

        def add_vp_hook(match: re.Match[bytes]) -> bytes:
            block = match.group(0)
            numbers = re.findall(rb"[0-9]+", re.sub(rb"#.*", b"", block))
            if len(numbers) < 2:
                raise BuildError(f"malformed victory-point block in state {old_state}: {block!r}")
            province = numbers[0]
            return block + b"\n\t\tadd_to_array = { state_victory_points = " + province + b" }"

        data = re.sub(rb"victory_points\s*=\s*\{[^{}]*\}", add_vp_hook, data)
        output_name = STATE_OUTPUT_NAMES[new_state]
        results[f"history/states/{output_name}"] = data
    if set(results) != {f"history/states/{name}" for name in STATE_OUTPUT_NAMES.values()}:
        raise BuildError("state output manifest is inconsistent")
    return results


def split_lines(data: bytes) -> list[bytes]:
    return data.replace(b"\r\n", b"\n").split(b"\n")


def join_rt_lines(lines: list[bytes], final_newline: bool) -> bytes:
    result = b"\r\n".join(lines)
    if final_newline:
        result += b"\r\n"
    return result


def first_semicolon_id(line: bytes) -> int | None:
    match = re.match(rb"\s*([0-9]+);", line)
    return int(match.group(1)) if match else None


def sample_building_province(
    line: bytes,
    provinces_bmp: bytes,
    rgb_to_province: dict[tuple[int, int, int], int],
    bmp_meta: tuple[int, int, int, int, int],
) -> tuple[list[bytes], int]:
    fields = line.split(b";")
    if len(fields) != 7:
        raise BuildError(f"malformed building-position row: {line!r}")
    pixel_offset, width, height, _, row_stride = bmp_meta
    x = int(Decimal(fields[2].decode()).to_integral_value(rounding=ROUND_FLOOR))
    z = int(Decimal(fields[4].decode()).to_integral_value(rounding=ROUND_FLOOR))
    if not 0 <= x < width or not 0 <= z < abs(height):
        raise BuildError(f"building coordinate outside map: {line!r}")
    offset = pixel_offset + z * row_stride + x * 3
    blue, green, red = provinces_bmp[offset : offset + 3]
    sampled_province = rgb_to_province.get((red, green, blue))
    if sampled_province is None:
        raise BuildError(f"building coordinate samples an undefined colour: {line!r}")
    return fields, sampled_province


def coastal_without_naval_base_spawn(
    lines: list[bytes],
    provinces_bmp: bytes,
    definition: bytes,
) -> set[int]:
    definition_rows = parse_definition(definition)
    rgb_to_province = {
        (row[0], row[1], row[2]): province_id for province_id, row in definition_rows.items()
    }
    bmp_meta = bmp_metadata(provinces_bmp)
    coastal_land = {
        province_id
        for province_id, row in definition_rows.items()
        if province_id != 0 and row[3][4] == b"land" and row[3][5] == b"true"
    }
    covered: set[int] = set()
    for line in lines:
        fields = line.split(b";")
        if len(fields) != 7:
            raise BuildError(f"malformed building-position row: {line!r}")
        if fields[1] != b"naval_base_spawn":
            continue
        _, sampled_province = sample_building_province(
            line, provinces_bmp, rgb_to_province, bmp_meta
        )
        covered.add(sampled_province)
    return coastal_land - covered


def states_without_building_site(
    lines: list[bytes], state_ids: set[int], site_type: bytes
) -> set[int]:
    covered: set[int] = set()
    for line in lines:
        fields = line.split(b";")
        if len(fields) != 7:
            raise BuildError(f"malformed building-position row: {line!r}")
        if fields[1] == site_type:
            covered.add(int(fields[0]))
    return state_ids - covered


def effective_province_states(state_outputs: dict[str, bytes]) -> dict[int, int]:
    states: dict[int, set[int]] = {}
    for path in (RT56_ROOT / "history/states").glob("*.txt"):
        state_id, provinces = parse_state(path.read_bytes(), str(path))
        states[state_id] = provinces
    for relative, data in state_outputs.items():
        state_id, provinces = parse_state(data, relative)
        states[state_id] = provinces
    return {province: state_id for state_id, provinces in states.items() for province in provinces}


def build_buildings(
    provinces_bmp: bytes,
    definition: bytes,
    state_outputs: dict[str, bytes],
) -> bytes:
    rt_data = (RT56_ROOT / "map/buildings.txt").read_bytes()
    donor_data = (HOK_ROOT / "map/buildings.txt").read_bytes()
    vanilla_data = (VANILLA_ROOT / "map/buildings.txt").read_bytes()
    rt_lines = normalized_nonempty_lines(rt_data)
    donor_lines = normalized_nonempty_lines(donor_data)
    vanilla_lines = normalized_nonempty_lines(vanilla_data)

    donor_old_states = set(HOK_STATE_SOURCES)
    donor_state_by_rest: dict[bytes, int] = {}
    for line in donor_lines:
        old_state = first_semicolon_id(line)
        if old_state not in donor_old_states:
            continue
        rest = line.split(b";", 1)[1]
        target_state = STATE_ID_MAP.get(old_state, old_state)
        previous = donor_state_by_rest.setdefault(rest, target_state)
        if previous != target_state:
            raise BuildError(f"ambiguous HOK building placement: {rest!r}")

    province_state = effective_province_states(state_outputs)
    definition_rows = parse_definition(definition)
    rgb_to_province = {
        (row[0], row[1], row[2]): province_id for province_id, row in definition_rows.items()
    }
    bmp_meta = bmp_metadata(provinces_bmp)

    rebased: list[bytes] = []
    reclassified = 0
    for line in rt_lines:
        fields, sampled_province = sample_building_province(
            line, provinces_bmp, rgb_to_province, bmp_meta
        )
        old_state = int(fields[0])
        sampled_state = province_state.get(sampled_province)
        geographic_target = sampled_state if sampled_state in BUILDING_TARGET_STATES else None
        linked_target = None
        if fields[1] == b"floating_harbor" and fields[6] != b"0":
            linked_state = province_state.get(int(fields[6]))
            if linked_state in BUILDING_TARGET_STATES:
                linked_target = linked_state
        donor_target = donor_state_by_rest.get(line.split(b";", 1)[1])
        candidates = {value for value in (linked_target, geographic_target, donor_target) if value is not None}
        if len(candidates) > 1:
            raise BuildError(
                f"building reclassification disagreement: linked={linked_target}, "
                f"bitmap={geographic_target}, donor={donor_target}, row={line!r}"
            )
        target_state = linked_target or geographic_target or donor_target
        if target_state is not None and target_state != old_state:
            fields[0] = str(target_state).encode()
            line = b";".join(fields)
            reclassified += 1
        rebased.append(line)
    if reclassified != 150:
        raise BuildError(f"expected 150 RT56 building rows to be reclassified, found {reclassified}")

    remaining_vanilla = Counter(line.split(b";", 1)[1] for line in vanilla_lines)
    additions: list[bytes] = []
    for line in donor_lines:
        rest = line.split(b";", 1)[1]
        if remaining_vanilla[rest]:
            remaining_vanilla[rest] -= 1
            continue
        old_state, remainder = line.split(b";", 1)
        new_state = STATE_ID_MAP.get(int(old_state), int(old_state))
        addition = str(new_state).encode() + b";" + remainder
        additions.append(replace_numeric_tokens(addition, PROVINCE_ID_MAP))
    if len(additions) != 21:
        raise BuildError(f"expected 21 HOK-only building rows, found {len(additions)}")

    donor_counts = Counter(donor_lines)
    vanilla_rest_counts = Counter(line.split(b";", 1)[1] for line in vanilla_lines)
    rt_rest_counts = Counter(line.split(b";", 1)[1] for line in rt_lines)
    topology_restorations: list[bytes] = []
    restored_provinces: set[int] = set()
    for source_line, expected_province in REQUIRED_KOREAN_COASTAL_SPAWN_ROWS:
        if donor_counts[source_line] != 1:
            raise BuildError(
                f"expected one pinned HOK coastal spawn row, found {donor_counts[source_line]}: "
                f"{source_line!r}"
            )
        old_state, remainder = source_line.split(b";", 1)
        if vanilla_rest_counts[remainder] != 1:
            raise BuildError(
                f"pinned HOK coastal spawn is no longer uniquely vanilla-identical: {source_line!r}"
            )
        if rt_rest_counts[remainder]:
            raise BuildError(f"RT56 now owns the required coastal spawn row: {source_line!r}")
        new_state = STATE_ID_MAP.get(int(old_state), int(old_state))
        restoration = replace_numeric_tokens(
            str(new_state).encode() + b";" + remainder, PROVINCE_ID_MAP
        )
        fields, sampled_province = sample_building_province(
            restoration, provinces_bmp, rgb_to_province, bmp_meta
        )
        if sampled_province != expected_province:
            raise BuildError(
                f"coastal spawn moved from expected province {expected_province} to "
                f"{sampled_province}: {restoration!r}"
            )
        sampled_state = province_state.get(sampled_province)
        if sampled_state != new_state:
            raise BuildError(
                f"coastal spawn state mismatch: row={new_state}, sampled={sampled_state}, "
                f"province={sampled_province}"
            )
        definition_fields = definition_rows[sampled_province][3]
        if definition_fields[4] != b"land" or definition_fields[5] != b"true":
            raise BuildError(
                f"required coastal spawn province is not coastal land: {sampled_province}"
            )
        linked_province = int(fields[6])
        linked_definition = definition_rows.get(linked_province)
        if linked_definition is None or linked_definition[3][4] != b"sea":
            raise BuildError(
                f"required coastal spawn has invalid sea link {linked_province}: {restoration!r}"
            )
        topology_restorations.append(restoration)
        restored_provinces.add(sampled_province)
    expected_restored = {province for _, province in REQUIRED_KOREAN_COASTAL_SPAWN_ROWS}
    if restored_provinces != expected_restored or len(topology_restorations) != 7:
        raise BuildError(
            f"expected seven Korean coastal spawn restorations {sorted(expected_restored)}, "
            f"found {sorted(restored_provinces)}"
        )

    state_site_restorations: list[bytes] = []
    restored_sites: set[tuple[int, bytes]] = set()
    for source_line, expected_province in REQUIRED_KOREAN_STATE_SITE_ROWS:
        if donor_counts[source_line] != 1:
            raise BuildError(
                f"expected one pinned HOK state site row, found {donor_counts[source_line]}: "
                f"{source_line!r}"
            )
        old_state, remainder = source_line.split(b";", 1)
        if vanilla_rest_counts[remainder] != 1:
            raise BuildError(
                f"pinned HOK state site is no longer uniquely vanilla-identical: {source_line!r}"
            )
        if rt_rest_counts[remainder]:
            raise BuildError(f"RT56 now owns the required state site row: {source_line!r}")
        new_state = STATE_ID_MAP.get(int(old_state), int(old_state))
        restoration = replace_numeric_tokens(
            str(new_state).encode() + b";" + remainder, PROVINCE_ID_MAP
        )
        fields, sampled_province = sample_building_province(
            restoration, provinces_bmp, rgb_to_province, bmp_meta
        )
        site_type = fields[1]
        if site_type not in REQUIRED_STATE_SITE_TYPES or fields[6] != b"0":
            raise BuildError(f"invalid required state site row: {restoration!r}")
        if sampled_province != expected_province:
            raise BuildError(
                f"state site moved from expected province {expected_province} to "
                f"{sampled_province}: {restoration!r}"
            )
        sampled_state = province_state.get(sampled_province)
        if sampled_state != new_state:
            raise BuildError(
                f"state site mismatch: row={new_state}, sampled={sampled_state}, "
                f"province={sampled_province}"
            )
        if definition_rows[sampled_province][3][4] != b"land":
            raise BuildError(
                f"required state site province is not land: {sampled_province}"
            )
        state_site_restorations.append(restoration)
        restored_sites.add((new_state, site_type))
    expected_sites = {(917, b"air_base"), (919, b"air_base"), (919, b"rocket_site_spawn")}
    if restored_sites != expected_sites or len(state_site_restorations) != 3:
        raise BuildError(
            f"expected Korean state site restorations {sorted(expected_sites)!r}, "
            f"found {sorted(restored_sites)!r}"
        )

    existing = Counter(rebased)
    restored_rows = topology_restorations + state_site_restorations
    duplicates = [line for line in additions + restored_rows if existing[line]]
    if duplicates:
        raise BuildError(f"HOK building rows already exist in RT56: {duplicates[:5]!r}")
    if len(set(additions + restored_rows)) != len(additions) + len(restored_rows):
        raise BuildError("duplicate HOK building rows in merged additions")
    merged = rebased + additions + restored_rows
    if len(merged) != 71905:
        raise BuildError(f"expected 71905 merged building rows, found {len(merged)}")

    rt_missing = coastal_without_naval_base_spawn(
        rt_lines,
        (RT56_ROOT / "map/provinces.bmp").read_bytes(),
        (RT56_ROOT / "map/definition.csv").read_bytes(),
    )
    if rt_missing != EXPECTED_RT56_COASTAL_WITHOUT_SPAWN:
        raise BuildError(
            f"RT56 coastal-spawn baseline changed: expected "
            f"{sorted(EXPECTED_RT56_COASTAL_WITHOUT_SPAWN)}, found {sorted(rt_missing)}"
        )
    merged_missing = coastal_without_naval_base_spawn(merged, provinces_bmp, definition)
    if merged_missing != rt_missing:
        raise BuildError(
            f"merged coastal-spawn coverage differs from RT56: "
            f"new missing={sorted(merged_missing - rt_missing)}, "
            f"unexpectedly covered={sorted(rt_missing - merged_missing)}"
        )

    rt_state_ids = set(effective_province_states({}).values())
    merged_state_ids = set(province_state.values())
    for site_type in REQUIRED_STATE_SITE_TYPES:
        rt_site_missing = states_without_building_site(rt_lines, rt_state_ids, site_type)
        if rt_site_missing:
            raise BuildError(
                f"RT56 {site_type.decode()} site baseline changed: "
                f"missing={sorted(rt_site_missing)}"
            )
        merged_site_missing = states_without_building_site(merged, merged_state_ids, site_type)
        if merged_site_missing:
            raise BuildError(
                f"merged states lack {site_type.decode()} sites: "
                f"missing={sorted(merged_site_missing)}"
            )
    return join_rt_lines(merged, final_newline=False)


def normalized_nonempty_lines(data: bytes) -> list[bytes]:
    return [line.rstrip() for line in split_lines(data) if line.strip()]


def build_railways() -> bytes:
    rt_data = (RT56_ROOT / "map/railways.txt").read_bytes()
    rt_lines = normalized_nonempty_lines(rt_data)
    old_routes = {
        b"2 4 11948 10110 4126 11977",
        b"4 4 11977 7204 7221 7125",
        b"2 5 7125 9981 848 10083 6928",
        b"4 5 7125 12040 11915 10065 4052",
    }
    found = old_routes & set(rt_lines)
    if found != old_routes:
        raise BuildError(f"RT56 Korean railway baseline changed; found {len(found)}/4 routes")
    kept = [line for line in rt_lines if line not in old_routes]

    donor_lines = normalized_nonempty_lines((HOK_ROOT / "map/railways.txt").read_bytes())
    vanilla_lines = normalized_nonempty_lines((VANILLA_ROOT / "map/railways.txt").read_bytes())
    remaining_vanilla = Counter(vanilla_lines)
    donor_additions: list[bytes] = []
    for line in donor_lines:
        if remaining_vanilla[line]:
            remaining_vanilla[line] -= 1
        else:
            donor_additions.append(line)
    remaining_donor = Counter(donor_lines)
    donor_removals: list[bytes] = []
    for line in vanilla_lines:
        if remaining_donor[line]:
            remaining_donor[line] -= 1
        else:
            donor_removals.append(line)
    if set(donor_removals) != old_routes or len(donor_removals) != 4:
        raise BuildError(f"unexpected HOK railway removals: {donor_removals!r}")
    # Four replacements plus thirty new local connections.
    if len(donor_additions) != 34:
        raise BuildError(f"expected 34 donor railway rows, found {len(donor_additions)}")
    rewritten = [replace_numeric_tokens(line, PROVINCE_ID_MAP) for line in donor_additions]
    duplicates = set(kept) & set(rewritten)
    if duplicates:
        raise BuildError(f"railway additions already exist in RT56: {sorted(duplicates)!r}")
    return join_rt_lines(kept + rewritten, final_newline=True)


def build_supply_nodes() -> bytes:
    rt_data = (RT56_ROOT / "map/supply_nodes.txt").read_bytes()
    rt_lines = normalized_nonempty_lines(rt_data)
    donor_lines = normalized_nonempty_lines((HOK_ROOT / "map/supply_nodes.txt").read_bytes())
    expected = [b"1 13418", b"1 13424", b"1 13436", b"1 11835", b"1 6963", b"1 6822"]
    if donor_lines[-6:] != expected:
        raise BuildError("HOK supply-node delta no longer matches the pinned six-row manifest")
    additions = [replace_numeric_tokens(line, PROVINCE_ID_MAP) for line in expected]
    merged = list(rt_lines)
    for line in additions:
        if line not in merged:
            merged.append(line)
    return join_rt_lines(merged, final_newline=True)


def build_unitstacks() -> bytes:
    rt_data = (RT56_ROOT / "map/unitstacks.txt").read_bytes()
    rt_lines = normalized_nonempty_lines(rt_data)
    donor_lines = normalized_nonempty_lines((HOK_ROOT / "map/unitstacks.txt").read_bytes())
    additions = [line for line in donor_lines if first_semicolon_id(line) in PROVINCE_ID_MAP]
    if len(additions) != 536:
        raise BuildError(f"expected 536 HOK unit-stack rows, found {len(additions)}")
    rewritten = []
    for line in additions:
        old_id, remainder = line.split(b";", 1)
        rewritten.append(str(PROVINCE_ID_MAP[int(old_id)]).encode() + b";" + remainder)
    merged = rt_lines + rewritten
    pairs = [(int(line.split(b";", 2)[1]), int(line.split(b";", 1)[0])) for line in merged]
    if len(pairs) != len(set(pairs)):
        raise BuildError("duplicate (zoom, province) pair in merged unit-stack rows")
    merged.sort(key=lambda line: (int(line.split(b";", 2)[1]), int(line.split(b";", 1)[0])))
    return join_rt_lines(merged, final_newline=True)


def build_strategic_region() -> bytes:
    data = (RT56_ROOT / "map/strategicregions/186-Korea.txt").read_bytes()
    pattern = re.compile(rb"(provinces\s*=\s*\{)(.*?)(\})", re.DOTALL)
    match = pattern.search(data)
    if not match:
        raise BuildError("could not locate RT56 strategic-region province list")
    existing = [int(value) for value in re.findall(rb"[0-9]+", match.group(2))]
    additions = list(PROVINCE_ID_MAP.values())
    if set(existing) & set(additions):
        raise BuildError("new HOK provinces already occur in RT56 strategic region 186")
    body = match.group(2).rstrip() + b" " + b" ".join(str(value).encode() for value in additions) + b" \r\n\t"
    return data[: match.start(2)] + body + data[match.end(2) :]


def parse_state(data: bytes, source: str) -> tuple[int, set[int]]:
    clean = re.sub(rb"#.*", b"", data)
    id_match = re.search(rb"\bid\s*=\s*([0-9]+)", clean)
    province_match = re.search(rb"\bprovinces\s*=\s*\{([^{}]*)\}", clean, re.DOTALL)
    if not id_match or not province_match:
        raise BuildError(f"could not parse state definition: {source}")
    return int(id_match.group(1)), {int(value) for value in re.findall(rb"[0-9]+", province_match.group(1))}


def validate_effective_states(state_outputs: dict[str, bytes], definition: bytes) -> None:
    states: dict[int, tuple[str, set[int]]] = {}
    for path in (RT56_ROOT / "history/states").glob("*.txt"):
        state_id, provinces = parse_state(path.read_bytes(), str(path))
        if state_id in states:
            raise BuildError(f"duplicate state ID {state_id} in RT56 baseline")
        states[state_id] = (str(path), provinces)
    for relative, data in state_outputs.items():
        state_id, provinces = parse_state(data, relative)
        states[state_id] = (relative, provinces)

    province_owners: dict[int, list[int]] = defaultdict(list)
    for state_id, (_, provinces) in states.items():
        for province_id in provinces:
            province_owners[province_id].append(state_id)
    duplicates = {province: owners for province, owners in province_owners.items() if len(owners) > 1}
    if duplicates:
        sample = list(sorted(duplicates.items()))[:20]
        raise BuildError(f"province membership duplicated across effective states: {sample}")

    definition_rows = parse_definition(definition)
    land = {
        province
        for province, row in definition_rows.items()
        if province != 0 and row[3][4] == b"land"
    }
    missing = sorted(land - set(province_owners))
    undefined = sorted(set(province_owners) - set(definition_rows))
    if missing or undefined:
        raise BuildError(
            f"effective state closure failed: missing land provinces={missing[:20]}, "
            f"undefined state provinces={undefined[:20]}"
        )
    for province in PROVINCE_ID_MAP.values():
        if len(province_owners.get(province, [])) != 1:
            raise BuildError(f"new province {province} is not owned by exactly one state")

    for relative, data in state_outputs.items():
        state_id, _ = parse_state(data, relative)
        static_vps = {
            int(numbers[0])
            for block in re.findall(rb"(?<!state_)\bvictory_points\s*=\s*\{[^{}]*\}", data)
            if (numbers := re.findall(rb"[0-9]+", re.sub(rb"#.*", b"", block)))
        }
        hook_vps = {
            int(value)
            for value in re.findall(
                rb"add_to_array\s*=\s*\{\s*state_victory_points\s*=\s*([0-9]+)\s*\}",
                data,
            )
        }
        expected_vps = EXPECTED_STATE_VICTORY_POINTS[state_id]
        if static_vps != expected_vps or hook_vps != expected_vps:
            raise BuildError(
                f"state {state_id} victory-point hook mismatch: "
                f"static={sorted(static_vps)}, hooks={sorted(hook_vps)}, "
                f"expected={sorted(expected_vps)}"
            )


def validate_map_references(outputs: dict[str, bytes]) -> None:
    definition_rows = parse_definition(outputs["map/definition.csv"])
    province_ids = set(definition_rows)

    for line in normalized_nonempty_lines(outputs["map/railways.txt"]):
        values = [int(value) for value in re.findall(rb"[0-9]+", line)]
        if len(values) < 2 or values[1] != len(values) - 2:
            raise BuildError(f"malformed railway row: {line!r}")
        bad = [value for value in values[2:] if value not in province_ids]
        if bad:
            raise BuildError(f"undefined railway provinces {bad}: {line!r}")

    for line in normalized_nonempty_lines(outputs["map/supply_nodes.txt"]):
        values = [int(value) for value in re.findall(rb"[0-9]+", line)]
        if len(values) != 2 or values[1] not in province_ids:
            raise BuildError(f"malformed or undefined supply-node row: {line!r}")

    for line in normalized_nonempty_lines(outputs["map/unitstacks.txt"]):
        province_id = first_semicolon_id(line)
        if province_id not in province_ids:
            raise BuildError(f"undefined unit-stack province {province_id}: {line!r}")


def build_all() -> tuple[dict[str, bytes], Counter[int], int]:
    definition = build_definition()
    provinces, pixel_counts, overlay_pixels = build_provinces_bmp()
    state_outputs = build_states()
    outputs = {
        "map/definition.csv": definition,
        "map/provinces.bmp": provinces,
        "map/buildings.txt": build_buildings(provinces, definition, state_outputs),
        "map/railways.txt": build_railways(),
        "map/supply_nodes.txt": build_supply_nodes(),
        "map/unitstacks.txt": build_unitstacks(),
        "map/strategicregions/186-Korea.txt": build_strategic_region(),
        **state_outputs,
    }
    validate_effective_states(state_outputs, definition)
    validate_map_references(outputs)
    return outputs, pixel_counts, overlay_pixels


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply", action="store_true", help="write generated files under the repository")
    mode.add_argument("--check", action="store_true", help="verify that repository files match generated output")
    args = parser.parse_args()

    try:
        verify_inputs()
        outputs, pixel_counts, overlay_pixels = build_all()
        messages = [write_if_changed(path, data, args.apply) for path, data in sorted(outputs.items())]
        if args.check:
            mismatches = [message for message in messages if message.startswith("would-write")]
            if mismatches:
                print("Generated-output mismatches:", file=sys.stderr)
                print("\n".join(mismatches), file=sys.stderr)
                return 1
        print("\n".join(messages))
        print(
            f"overlay-pixels {overlay_pixels}; custom-province-pixels {sum(pixel_counts.values())}; "
            f"new-provinces {len(pixel_counts)}; new-states 4; reused-RT56-states 4"
        )
        return 0
    except BuildError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
