#!/usr/bin/env python3
"""Reproduce the selected Korean recruitment portraits and name-pool exclusions."""
from __future__ import annotations

import argparse
import csv
from functools import lru_cache
import hashlib
import io
import json
from pathlib import Path
import re
import struct
import sys


#20261112_kpopmodder: Preserve the audited donor artwork and bounded KOR delta above unchanged historical inputs.
ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "docs/upstream/hok-scientist-update-20261112"
NAME_SNAPSHOT = ROOT / "docs/upstream/hok-scientist-name-exclusions-20261112"
OPERATIVE_SNAPSHOT = ROOT / "docs/upstream/hok-operative-portraits-20261112"
LOCK_PATH = ROOT / "tools/hok_scientist_update_lock.json"
NAMES_SOURCE = "common/names/00_names.txt"
NAMES = "common/names/zz_hok_rt56_names.txt"
PORTRAITS = "portraits/00_portraits_KOR.txt"
GFX = "interface/HOK_KOR_scientist_portraits.gfx"
OPERATIVE_GFX = "interface/HOK_KOR_operative_portraits.gfx"
SPRITES = {
    f"GFX_HOK_KOR_scientist_{gender}_{number:02}":
        f"gfx/leaders/scientists/HOK_KOR/portrait_HOK_KOR_scientist_{gender}_{number:02}.dds"
    for gender in ("female", "male") for number in range(1, 5)
}
OPERATIVE_SPRITES = {
    f"GFX_HOK_KOR_operative_{gender}_{number:02}":
        f"gfx/leaders/operatives/HOK_KOR/portrait_HOK_KOR_operative_{gender}_{number:02}.dds"
    for gender in ("female", "male") for number in range(1, 5)
}
OLD = frozenset((NAMES, PORTRAITS))
SCIENTIST_PATHS = frozenset((NAMES, PORTRAITS, GFX, *SPRITES.values()))
OPERATIVE_ADDITIONS = frozenset((OPERATIVE_GFX, *OPERATIVE_SPRITES.values()))
PATHS = SCIENTIST_PATHS | OPERATIVE_ADDITIONS
SOURCE_PATHS = (SCIENTIST_PATHS - {NAMES}) | {NAMES_SOURCE}
DOCUMENTS = frozenset((
    "AGENTS.md", "docs/HOK_KOREAN_SCIENTIST_PORTRAIT_PLAN.md",
    "docs/data/HOK_KOREAN_RANDOM_NAME_LOCALISATION_MANIFEST.json",
    "docs/data/HOK_KOREAN_SCIENTIST_PORTRAIT_ASSET_MANIFEST.json",
    "docs/incidents/2026-11-12-korean-random-name-localisation.md",
    "docs/incidents/2026-11-12-korean-scientist-portraits.md",
))
REFERENCES = frozenset((
    "RT56/descriptor.mod", "RT56/common/names/00_names.txt",
    "RT56/portraits/00_portraits.txt", "RT56/portraits/r56_portraits.txt",
    "RT56/portraits/02_tiger_portraits.txt", "RT56/portraits/00_portraits_operatives.txt",
    "VANILLA/launcher-settings.json", "VANILLA/common/names/00_names.txt",
    "VANILLA/portraits/998_scientist_portraits.txt", "VANILLA/interface/_scientists_portraits.gfx",
))
EXCLUSION_NOTE = "#20261112_kpopmodder: Remove Geunhye from the shared KOR female-name pool at user request."
FOLLOWUP_NOTE = "#20261112_kpopmodder: Exclude verified modern-politician name combinations from the shared KOR name pool."
EXCLUDED_NAMES = {
    "male": ("Gun", "Woong", "Yoon-Gi", "Yoongi", "Jaeyoung", "Jinho", "Jiwon", "Jungho", "Junghoon",
             "Minseok", "Minsoo", "Sanghoon", "Sungho", "Sunghoon", "Sungmin"),
    "female": ("Bora", "Ji-young", "Kyung-hee", "Jiyoung", "Kyunghee"),
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def canonical_name(relative: str | Path) -> str:
    path = (ROOT / Path(str(relative).replace("\\", "/"))).resolve()
    name = path.relative_to(ROOT.resolve()).as_posix()
    return next((known for known in PATHS if name.casefold() == known.casefold()), name)


@lru_cache(maxsize=1)
def lock() -> dict:
    config = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    if (config.get("format") != 1 or config.get("revision") != "2026-11-12-scientists-v3"
            or config.get("base_commit") != "51ac53cbe8c25eeb203b6f6914ce53b0a5cc2c58"
            or config.get("source_commit") != "cdc022eee15fbf7404d4cb30cf2d0102d29e550c"
            or config.get("source_kind") != "reviewed-working-tree-snapshot"
            or config.get("workshop_manifest") != "1963361040482473746"
            or config.get("game_version") != "Operation Postern v1.19.4.2.2da5 (0bdb)"
            or set(config.get("outputs", {})) != PATHS):
        raise ValueError("unreviewed scientist source, host or output inventory")
    for name, record in config["outputs"].items():
        classification = "THREE_WAY_MERGE" if name == NAMES else "ADD"
        if name.endswith(".dds"):
            classification = "ASSET_COPY"
        if (record.get("classification") != classification or record.get("size", 0) <= 0
                or not re.fullmatch("[A-F0-9]{64}", record.get("sha256", ""))):
            raise ValueError(f"unreviewed scientist output contract: {name}")
        if name in OLD:
            if (record.get("previous_snapshot") != "compat_before/" + name
                    or not re.fullmatch("[A-F0-9]{64}", record.get("previous_sha256", ""))
                    or record.get("previous_size", 0) <= 0):
                raise ValueError(f"unreviewed scientist predecessor: {name}")
        elif record.get("previous_snapshot") is not None or record.get("previous_sha256") is not None:
            raise ValueError(f"scientist addition has a false predecessor: {name}")
    followup = config.get("name_exclusions", {})
    if (followup.get("snapshot_root") != "docs/upstream/hok-scientist-name-exclusions-20261112"
            or followup.get("previous_source_manifest_sha256") != config["source_manifest_sha256"]
            or followup.get("intermediate_output_sha256") != "F06C9DE9A35C43A86BA7B76AD447A7E511060A035B2F396C659F8459A320F781"
            or followup.get("intermediate_output_size") != 4733
            or followup.get("excluded_names") != {gender: list(values) for gender, values in EXCLUDED_NAMES.items()}
            or followup.get("final_counts") != {"male": 56, "female": 11, "surnames": 14}):
        raise ValueError("unreviewed additional Korean name exclusions or intermediate output")
    operative = config.get("operative_update", {})
    if (operative.get("snapshot_root") != "docs/upstream/hok-operative-portraits-20261112"
            or operative.get("source_commit") != "f1282d701bc47e47c119ca31faa6082e9e6ed1e6"
            or operative.get("compatibility_base_commit") != "7e29ce80158dfad1635d427f61e5c8b964088adf"
            or operative.get("source_kind") != "reviewed-working-tree-snapshot"
            or operative.get("previous_lock_sha256") != "0AAF49DBCAA34D60DBF63EF063EA11FD2854D0C041CF6C76A7A59DA127738AA3"
            or operative.get("previous_portrait_sha256") != "5E13A8CED8ECEDD70DE77614739C6C2315D98498DE16471ED8BF6363CC2746CC"
            or operative.get("previous_portrait_size") != 1051):
        raise ValueError("unreviewed operative source or scientist portrait predecessor")
    return config


def frozen(relative: str, expected: str, size: int | None = None, *, root: Path = SNAPSHOT) -> bytes:
    path = (root / relative).resolve()
    path.relative_to(root.resolve())
    data = path.read_bytes()
    if sha(data) != expected or (size is not None and len(data) != size):
        raise ValueError(f"scientist frozen input drift: {relative}")
    return data


@lru_cache(maxsize=1)
def manifest() -> dict:
    config = lock()
    result = json.loads(frozen("source-manifest.json", config["source_manifest_sha256"]))
    if (result.get("schema_version") != 1 or result.get("source_commit") != config["source_commit"]
            or result.get("compatibility_baseline", {}).get("commit") != config["base_commit"]
            or set(result.get("sources", {})) != SOURCE_PATHS
            or set(result.get("documents", {})) != DOCUMENTS
            or set(result.get("references", {})) != REFERENCES):
        raise ValueError("scientist snapshot inventory or ancestry drift")
    for group, prefix in (("sources", "source/"), ("documents", "documents/")):
        for name, record in result[group].items():
            if record["snapshot"] != prefix + name:
                raise ValueError(f"scientist snapshot source path drift: {name}")
            frozen(record["snapshot"], record["sha256"], record["size"])
    for name, record in result["references"].items():
        provider, relative = name.split("/", 1)
        root = Path(config["rt56_root" if provider == "RT56" else "vanilla_root"]).resolve()
        path = (root / relative).resolve()
        path.relative_to(root)
        data = path.read_bytes()
        if (Path(record["source_path"]).resolve() != path
                or sha(data) != record["sha256"] or len(data) != record["size"]):
            raise ValueError(f"scientist installed reference drift: {name}")
    game = Path(config["vanilla_root"]) / "launcher-settings.json"
    if json.loads(game.read_text(encoding="utf-8-sig"))["version"] != config["game_version"]:
        raise ValueError("scientist installed game-version drift")
    host = Path(config["rt56_root"])
    acf = (host.parents[2] / "appworkshop_394360.acf").read_text(encoding="utf-8-sig")
    entries = [dict(re.findall(r'"([^"\r\n]+)"\s*"([^"]*)"', body))
               for body in re.findall(r'"820260968"\s*\{([^}]+)\}', acf)]
    if (len(entries) != 2 or any(row.get("manifest") != config["workshop_manifest"] for row in entries)
            or entries[-1].get("latest_manifest") != config["workshop_manifest"]):
        raise ValueError("scientist installed/latest RT56 manifest drift")
    return result


def previous_bytes(relative: str) -> bytes:
    record = lock()["outputs"][relative]
    return frozen(record["previous_snapshot"], record["previous_sha256"], record["previous_size"])


def merge_names(source: bytes) -> bytes:
    from build_shared_overrides import one_block
    previous = previous_bytes(NAMES)
    newline = b"\r\n" if b"\r\n" in previous else b"\n"
    old = b"\t\t\tAejung Chaewon Hyeja Jiyoung Seongja Yeojin Kyunghee Geunhye" + newline
    new = ("\t\t\t" + EXCLUSION_NOTE).encode() + newline + old.replace(b" Geunhye", b"")
    if previous.count(old) != 1:
        raise ValueError("scientist KOR name-exclusion ancestor drift")
    result = previous.replace(old, new, 1)
    korean = one_block(result.decode("utf-8"), "KOR")
    if korean.replace("\r\n", "\n") != one_block(source.decode("utf-8-sig"), "KOR").replace("\r\n", "\n"):
        raise ValueError("selected donor KOR names extend beyond one reviewed exclusion")
    for field, expected in (("male", 71), ("female", 16), ("surnames", 14)):
        block = one_block(korean, field, top_level=False)
        if field != "surnames":
            block = one_block(block, "names", top_level=False)
        body = re.sub(r"#[^\r\n]*", "", block[block.index("{") + 1:-1])
        values = re.findall(r'"[^"\r\n]*"|[^\s{}=]+', body)
        if len(values) != expected or "Geunhye" in values or re.search(r"[\uac00-\ud7a3]", body):
            raise ValueError(f"scientist Romanized KOR name inventory drift: {field}")
    return result


@lru_cache(maxsize=1)
def initial_names() -> bytes:
    record = manifest()["sources"][NAMES_SOURCE]
    result = merge_names(frozen(record["snapshot"], record["sha256"], record["size"]))
    transition = lock()["name_exclusions"]
    if sha(result) != transition["intermediate_output_sha256"] or len(result) != transition["intermediate_output_size"]:
        raise ValueError("initial Korean name revision changed during the selected follow-up")
    return result


#20261112_kpopmodder: Prove the later twenty-name exclusion against the immutable first capture before changing the same output.
@lru_cache(maxsize=1)
def name_exclusions_manifest() -> dict:
    config = lock()["name_exclusions"]
    result = json.loads(frozen("source-manifest.json", config["source_manifest_sha256"], root=NAME_SNAPSHOT))
    documents = {"docs/data/HOK_KOREAN_RANDOM_NAME_LOCALISATION_MANIFEST.json",
                 "docs/incidents/2026-11-12-korean-random-name-localisation.md"}
    if (result.get("schema_version") != 1 or result.get("source_commit") != lock()["source_commit"]
            or set(result.get("sources", {})) != {NAMES_SOURCE}
            or set(result.get("documents", {})) != documents
            or result.get("predecessor", {}).get("source_manifest_sha256") != lock()["source_manifest_sha256"]
            or result["predecessor"].get("donor_name_sha256") != manifest()["sources"][NAMES_SOURCE]["sha256"]
            or result.get("selected_output", {}).get("path") != NAMES
            or result["selected_output"].get("sha256") != config["intermediate_output_sha256"]
            or result["selected_output"].get("size") != config["intermediate_output_size"]):
        raise ValueError("additional Korean name snapshot inventory or predecessor drift")
    for group, prefix in (("sources", "source/"), ("documents", "documents/")):
        for name, record in result[group].items():
            if record["snapshot"] != prefix + name:
                raise ValueError(f"additional Korean name snapshot path drift: {name}")
            frozen(record["snapshot"], record["sha256"], record["size"], root=NAME_SNAPSHOT)
    contract = result.get("final_name_contract", {})
    if ({field: contract.get(field) for field in ("male", "female", "surnames")} != config["final_counts"]
            or any(contract.get("additional_" + gender + "_removed") != list(values)
                   for gender, values in EXCLUDED_NAMES.items())):
        raise ValueError("additional Korean name source exclusion inventory drift")
    return result


def apply_name_exclusions() -> bytes:
    from build_shared_overrides import one_block
    earlier = manifest()["sources"][NAMES_SOURCE]
    later = name_exclusions_manifest()["sources"][NAMES_SOURCE]
    before = frozen(earlier["snapshot"], earlier["sha256"], earlier["size"]).decode("utf-8-sig")
    after = frozen(later["snapshot"], later["sha256"], later["size"], root=NAME_SNAPSHOT).decode("utf-8-sig")
    old_kor, new_kor = one_block(before, "KOR"), one_block(after, "KOR")
    source_newline = "\r\n" if "\r\n" in before else "\n"
    if (before.count(old_kor) != 1 or FOLLOWUP_NOTE in before
            or before.replace(old_kor, FOLLOWUP_NOTE + source_newline + new_kor, 1) != after):
        raise ValueError("additional donor name changes extend beyond KOR and its single contributor note")
    proof = old_kor
    for gender, excluded in EXCLUDED_NAMES.items():
        old_names = one_block(one_block(old_kor, gender, top_level=False), "names", top_level=False)
        new_names = one_block(one_block(new_kor, gender, top_level=False), "names", top_level=False)
        token_lists = []
        for block in (old_names, new_names):
            body = re.sub(r"#[^\r\n]*", "", block[block.index("{") + 1:-1])
            token_lists.append(re.findall(r'"[^"\r\n]*"|[^\s{}=]+', body))
        old_tokens, new_tokens = token_lists
        if (any(sum(token.strip('"') == value for token in old_tokens) != 1 for value in excluded)
                or [token for token in old_tokens if token.strip('"') not in excluded] != new_tokens
                or len(new_tokens) != lock()["name_exclusions"]["final_counts"][gender]):
            raise ValueError(f"additional Korean name deletion changes quoting, order or unselected names: {gender}")
        if proof.count(old_names) != 1:
            raise ValueError(f"ambiguous Korean name source block: {gender}")
        proof = proof.replace(old_names, new_names, 1)
    if proof != new_kor:
        raise ValueError("additional Korean name deletion changes surnames, callsigns or unrelated KOR statements")
    initial = initial_names()
    newline = "\r\n" if b"\r\n" in initial else "\n"
    old_output = old_kor.replace("\r\n", "\n").replace("\n", newline).encode()
    new_output = (FOLLOWUP_NOTE + newline + new_kor.replace("\r\n", "\n").replace("\n", newline)).encode()
    if initial.count(old_output) != 1:
        raise ValueError("additional Korean name exclusion lost its exact compatibility ancestor")
    return initial.replace(old_output, new_output, 1)


#20261112_kpopmodder: Extend the same Korean portrait owner while retaining every historical scientist and name pin.
@lru_cache(maxsize=1)
def operative_manifest() -> dict:
    config = lock()["operative_update"]
    result = json.loads(frozen("source-manifest.json", config["source_manifest_sha256"], root=OPERATIVE_SNAPSHOT))
    documents = {"AGENTS.md", "docs/HOK_KOREAN_OPERATIVE_PORTRAIT_PLAN.md",
                 "docs/data/HOK_KOREAN_OPERATIVE_PORTRAIT_ASSET_MANIFEST.json",
                 "docs/incidents/2026-11-12-korean-operative-portraits.md",
                 "docs/incidents/2026-11-12-korean-operative-outfit-background.md"}
    references = {
        "RT56/descriptor.mod", "RT56/portraits/00_portraits.txt", "RT56/portraits/r56_portraits.txt",
        "RT56/portraits/02_tiger_portraits.txt", "RT56/portraits/00_portraits_operatives.txt",
        "RT56/common/decisions/lar_agent_recruitment_decisions.txt", "VANILLA/launcher-settings.json",
        "VANILLA/dlc/dlc028_la_resistance/portraits/027_lar_portraits.txt",
        "VANILLA/dlc/dlc028_la_resistance/interface/lar_portraits.gfx",
        "VANILLA/documentation/effects_documentation.md",
        "VANILLA/common/decisions/lar_agent_recruitment_decisions.txt",
        "VANILLA/gfx/interface/naval_leader_selection_entry_bg.dds",
        "COMPAT/history/countries/KOR - Korea.txt", "COMPAT/interface/leader_portraits_HoK.gfx",
        "COMPAT/gfx/leaders/KOR/portrait_KOR_operative_Bonggil_Yoon.dds",
        "COMPAT/gfx/leaders/KOR/portrait_KOR_operative_Bongchang_Lee.dds",
    }
    prior = result.get("prior_scientist_contract", {})
    if (result.get("schema_version") != 1 or result.get("source_commit") != config["source_commit"]
            or result.get("compatibility_baseline", {}).get("commit") != config["compatibility_base_commit"]
            or set(result.get("sources", {})) != OPERATIVE_ADDITIONS | {PORTRAITS}
            or set(result.get("documents", {})) != documents
            or set(result.get("references", {})) != references
            or set(result.get("predecessors", {})) != {PORTRAITS}
            or prior.get("lock_sha256") != config["previous_lock_sha256"]
            or prior.get("revision") != "2026-11-12-scientists-v2"
            or set(prior.get("outputs", {})) != SCIENTIST_PATHS):
        raise ValueError("operative snapshot inventory or previous ownership drift")
    for group, prefix in (("sources", "source/"), ("documents", "documents/"), ("predecessors", "compat_before/")):
        for name, record in result[group].items():
            if record["snapshot"] != prefix + name:
                raise ValueError(f"operative snapshot path drift: {name}")
            frozen(record["snapshot"], record["sha256"], record["size"], root=OPERATIVE_SNAPSHOT)
    previous = result["predecessors"][PORTRAITS]
    if previous["sha256"] != config["previous_portrait_sha256"] or previous["size"] != config["previous_portrait_size"]:
        raise ValueError("operative snapshot lost the exact scientist portrait predecessor")
    for name, record in prior["outputs"].items():
        expected = previous if name == PORTRAITS else lock()["outputs"][name]
        if record["sha256"] != expected["sha256"] or record["size"] != expected["size"]:
            raise ValueError(f"operative update changed a historical scientist or name output pin: {name}")
    roots = {"RT56": Path(lock()["rt56_root"]), "VANILLA": Path(lock()["vanilla_root"]), "COMPAT": ROOT}
    for name, record in result["references"].items():
        provider, relative = name.split("/", 1)
        root = roots[provider].resolve()
        path = (root / relative).resolve()
        path.relative_to(root)
        data = path.read_bytes()
        if (Path(record["source_path"]).resolve() != path or sha(data) != record["sha256"]
                or len(data) != record["size"]):
            raise ValueError(f"operative fixed-content or installed reference drift: {name}")
    return result


def scientist_portraits() -> bytes:
    record = manifest()["sources"][PORTRAITS]
    result = frozen(record["snapshot"], record["sha256"], record["size"])
    config = lock()["operative_update"]
    if sha(result) != config["previous_portrait_sha256"] or len(result) != config["previous_portrait_size"]:
        raise ValueError("operative update changed the original scientist portrait input")
    verify_portraits(result)
    return result


def verify_portraits(source: bytes, *, role: str = "scientist") -> None:
    previous = previous_bytes(PORTRAITS) if role == "scientist" else scientist_portraits()
    lines = ["", f"\t#20261112_kpopmodder: Assign Korean-only portraits to newly recruited male and female {role}s.",
             f"\t{role} = {{"]
    for gender in ("female", "male"):
        lines.append(f"\t\t{gender} = {{")
        lines.extend(f'\t\t\t"GFX_HOK_KOR_{role}_{gender}_{number:02}"' for number in range(1, 5))
        lines.append("\t\t}")
    lines.extend(("\t}", ""))
    if not previous.endswith(b"\r\n}") or source != previous[:-1] + "\r\n".join(lines).encode() + b"}":
        raise ValueError(f"{role} portrait extension changes the earlier pools or reviewed role list")


def verify_assets(outputs: dict[str, bytes]) -> None:
    from build_shared_overrides import block_spans
    for gfx, sprites, mipmap in ((GFX, SPRITES, 1), (OPERATIVE_GFX, OPERATIVE_SPRITES, 0)):
        text = outputs[gfx].decode("utf-8")
        found = {}
        for start, end in block_spans(text, "spriteType", top_level=False):
            block = text[start:end]
            names = re.findall(r'\bname\s*=\s*"([^"]+)"', block)
            textures = re.findall(r'\btexturefile\s*=\s*"([^"]+)"', block)
            if len(names) != 1 or len(textures) != 1 or names[0] in found:
                raise ValueError("recruitment sprite registry has an ambiguous definition")
            found[names[0]] = textures[0]
        if found != sprites:
            raise ValueError(f"recruitment sprite-to-DDS inventory drift: {gfx}")
        for name in sprites.values():
            data = outputs[name]
            if (len(data) != 131168 or data[:4] != b"DDS " or struct.unpack_from("<I", data, 4)[0] != 124
                    or struct.unpack_from("<II", data, 12) != (210, 156)
                    or struct.unpack_from("<I", data, 28)[0] != mipmap
                    or struct.unpack_from("<8I", data, 76) != (32, 65, 0, 32, 0xFF0000, 0xFF00, 0xFF, 0xFF000000)):
                raise ValueError(f"recruitment DDS format drift: {name}")
            if gfx == OPERATIVE_GFX and data[131::4] != b"\xff" * (156 * 210):
                raise ValueError(f"operative portrait lost its selected opaque background: {name}")


def verify_collisions() -> None:
    sprite_pattern = re.compile(rb'\bname\s*=\s*"(GFX_HOK_KOR_(?:scientist|operative)_[^"]+)"')
    for root in (ROOT, Path(lock()["rt56_root"]), Path(lock()["vanilla_root"])):
        for path in (root / "interface").rglob("*.gfx"):
            if root == ROOT and path in (ROOT / GFX, ROOT / OPERATIVE_GFX):
                continue
            if sprite_pattern.search(path.read_bytes()):
                raise ValueError(f"scientist sprite collision: {path}")
        for path in (root / "portraits").glob("*.txt"):
            if root == ROOT and path == ROOT / PORTRAITS:
                continue
            if re.search(rb"(?m)^\s*KOR\s*=\s*\{", path.read_bytes()):
                raise ValueError(f"scientist KOR portrait registry collision: {path}")
        if root != ROOT:
            for name in PATHS:
                if (root / name).exists():
                    raise ValueError(f"scientist exact-path host collision: {root / name}")


@lru_cache(maxsize=1)
def build_outputs() -> dict[str, bytes]:
    sources = manifest()["sources"]
    outputs = {}
    for name in sorted(SCIENTIST_PATHS):
        source_name = NAMES_SOURCE if name == NAMES else name
        record = sources[source_name]
        data = frozen(record["snapshot"], record["sha256"], record["size"])
        outputs[name] = apply_name_exclusions() if name == NAMES else data
    verify_portraits(outputs[PORTRAITS])
    for name, record in operative_manifest()["sources"].items():
        outputs[name] = frozen(record["snapshot"], record["sha256"], record["size"], root=OPERATIVE_SNAPSHOT)
    verify_portraits(outputs[PORTRAITS], role="operative")
    for name, data in outputs.items():
        expected = lock()["outputs"][name]
        if sha(data) != expected["sha256"] or len(data) != expected["size"]:
            raise ValueError(f"recruitment generated output drift: {name}")
    verify_assets(outputs)
    verify_collisions()
    return outputs


def historical_bytes(relative: str | Path, data: bytes) -> bytes:
    name = canonical_name(relative)
    if name in OLD and sha(data) == lock()["outputs"][name]["sha256"]:
        if data != build_outputs()[name]:
            raise ValueError(f"scientist final-output proof failed: {name}")
        return previous_bytes(name)
    if name == NAMES and data == initial_names():
        return previous_bytes(name)
    if name == PORTRAITS and data == scientist_portraits():
        return previous_bytes(name)
    return data


def finalize_one(relative: str | Path, data: bytes) -> bytes:
    name = canonical_name(relative)
    if name not in PATHS:
        return data
    final = build_outputs()[name]
    accepted = (final, previous_bytes(name)) if name in OLD else (final,)
    if name == NAMES:
        accepted += (initial_names(),)
    elif name == PORTRAITS:
        accepted += (scientist_portraits(),)
    if data not in accepted:
        raise ValueError(f"unreviewed scientist predecessor: {name}")
    return final


def preflight_outputs(outputs: dict) -> None:
    seen = set()
    for relative, data in outputs.items():
        name = canonical_name(relative)
        if name not in PATHS:
            continue
        if name in seen:
            raise ValueError(f"duplicate scientist output: {name}")
        seen.add(name)
        final = build_outputs()[name]
        if data != final:
            raise ValueError(f"unregistered proposed scientist bytes: {name}")
        path = ROOT / name
        accepted = (final, previous_bytes(name)) if name in OLD else (final,)
        if name == NAMES:
            accepted += (initial_names(),)
        elif name == PORTRAITS:
            accepted += (scientist_portraits(),)
        if path.exists() and (not path.is_file() or path.read_bytes() not in accepted):
            raise ValueError(f"independently changed scientist runtime: {name}")
        if name in OLD and not path.is_file():
            raise ValueError(f"missing scientist predecessor: {name}")


def ledger_bytes(previous: bytes) -> bytes:
    outputs, config = build_outputs(), lock()
    if any((ROOT / name).read_bytes() != data for name, data in outputs.items()):
        raise ValueError("scientist ledger/runtime mismatch")
    reader = csv.DictReader(io.StringIO(previous.decode("utf-8"), newline=""))
    fields = reader.fieldnames
    if not fields or not {"source_path", "output_path", "output_sha256", "integration_class", "reason", "status"} <= set(fields):
        raise ValueError("scientist ledger schema drift")
    lines, start, seen = previous.splitlines(keepends=True), reader.line_num, set()
    chunks = [b"".join(lines[:start])]

    def encoded(row: dict) -> bytes:
        stream = io.StringIO(newline="")
        csv.DictWriter(stream, fieldnames=fields, lineterminator="\n").writerow(row)
        return stream.getvalue().encode("utf-8")

    def provenance(name: str) -> str:
        if name in OPERATIVE_ADDITIONS:
            record = operative_manifest()["sources"][name]
            return ("2026-11-12 Korean operative portraits: tools/hok_scientist_update_lock.json"
                    "; source_kind=reviewed-working-tree-snapshot; donor_head=" + config["operative_update"]["source_commit"]
                    + "; source_snapshot=docs/upstream/hok-operative-portraits-20261112/" + record["snapshot"]
                    + "; source_sha256=" + record["sha256"] + "; original HOK authorship retained")
        source_name = NAMES_SOURCE if name == NAMES else name
        record = manifest()["sources"][source_name]
        return ("2026-11-12 Korean scientist portraits and selected random-name exclusion: tools/hok_scientist_update_lock.json"
                "; source_kind=reviewed-working-tree-snapshot; donor_head=" + config["source_commit"]
                + "; source_snapshot=docs/upstream/hok-scientist-update-20261112/" + record["snapshot"]
                + "; source_sha256=" + record["sha256"] + "; original HOK authorship retained")

    def name_followup_suffix() -> str:
        source = name_exclusions_manifest()["sources"][NAMES_SOURCE]
        return ("; 2026-11-12 additional Korean name exclusions: tools/hok_scientist_update_lock.json"
                "; source_snapshot=docs/upstream/hok-scientist-name-exclusions-20261112/" + source["snapshot"]
                + "; source_sha256=" + source["sha256"] + "; intermediate_output_sha256="
                + config["name_exclusions"]["intermediate_output_sha256"]
                + "; removed_male_names=15; removed_female_names=5; final_name_counts=56/11/14")

    def operative_suffix() -> str:
        source = operative_manifest()["sources"][PORTRAITS]
        return ("; 2026-11-12 Korean operative portrait extension: tools/hok_scientist_update_lock.json"
                "; source_snapshot=docs/upstream/hok-operative-portraits-20261112/" + source["snapshot"]
                + "; source_sha256=" + source["sha256"] + "; previous_scientist_portrait_sha256="
                + config["operative_update"]["previous_portrait_sha256"] + "; scientist and original HOK authorship retained")

    def addition(name: str) -> dict:
        source = (operative_manifest() if name in OPERATIVE_ADDITIONS else manifest())["sources"][name]
        source_config = config["operative_update"] if name in OPERATIVE_ADDITIONS else config
        record = config["outputs"][name]
        row = {field: "" for field in fields}
        row.update(source_path=name, output_path=name, integration_class=record["classification"],
                   status="SHIPPED", exact_path_rt56_collision="no", output_sha256=record["sha256"],
                   donor_sha256=source["sha256"], donor_source_sha256=source["sha256"],
                   donor_source_commit=source_config["source_commit"], donor_source_checkout=source_config["source_kind"],
                   reason=provenance(name))
        if name.endswith(".dds"):
            row.update(artwork_source_kind="upstream-AI-generated-fictional-portrait",
                       artwork_source_base_commit=source_config["source_commit"], artwork_source_sha256=source["sha256"])
            row["reason"] += "; upstream AI-generated artwork reused byte-exactly; donor generation provenance retained in capsule documents"
            if name in OPERATIVE_ADDITIONS:
                row["artwork_source_kind"] = "upstream-AI-edited-fictional-operative-portrait"
                row["reason"] += "; current black-fedora and opaque-gray revision; donor initial generation and later image-editing provenance retained"
        return row

    for row in reader:
        raw, start = b"".join(lines[start:reader.line_num]), reader.line_num
        name = row["output_path"]
        if name not in PATHS:
            chunks.append(raw)
            continue
        if name in seen:
            raise ValueError(f"duplicate scientist ledger output: {name}")
        seen.add(name)
        if name not in OLD:
            if row != addition(name):
                raise ValueError(f"scientist addition ledger drift: {name}")
        else:
            record = config["outputs"][name]
            source_name = NAMES_SOURCE if name == NAMES else name
            suffix = "; " + provenance(name) + "; previous_output_sha256=" + record["previous_sha256"]
            if row["source_path"] != source_name or row["integration_class"] != record["classification"]:
                raise ValueError(f"scientist ledger ownership drift: {name}")
            if name == NAMES:
                followup = name_followup_suffix()
                if row["output_sha256"] == record["sha256"] and row["reason"].endswith(suffix + followup):
                    chunks.append(raw)
                    continue
                intermediate = config["name_exclusions"]["intermediate_output_sha256"]
                if row["output_sha256"] == intermediate and row["reason"].endswith(suffix):
                    row["reason"] += followup
                elif row["output_sha256"] == record["previous_sha256"] and suffix not in row["reason"]:
                    row["reason"] += suffix + followup
                else:
                    raise ValueError("additional Korean name ledger predecessor drift")
                row["output_sha256"] = record["sha256"]
                raw = encoded(row)
            else:
                followup = operative_suffix()
                if row["output_sha256"] == record["sha256"] and row["reason"].endswith(suffix + followup):
                    chunks.append(raw)
                    continue
                intermediate = config["operative_update"]["previous_portrait_sha256"]
                if row["output_sha256"] == intermediate and row["reason"].endswith(suffix):
                    row["reason"] += followup
                elif row["output_sha256"] == record["previous_sha256"] and suffix not in row["reason"]:
                    row["reason"] += suffix + followup
                else:
                    raise ValueError("operative portrait ledger predecessor drift")
                row["output_sha256"] = record["sha256"]
                raw = encoded(row)
        chunks.append(raw)
    if not OLD <= seen:
        raise ValueError("scientist ledger missing existing outputs")
    for name in sorted(PATHS - seen):
        chunks.append(encoded(addition(name)))
    return b"".join(chunks)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        outputs = build_outputs()
        preflight_outputs(outputs)
        pending = [(ROOT / name, data) for name, data in outputs.items()
                   if not (ROOT / name).is_file() or (ROOT / name).read_bytes() != data]
        if pending and not args.apply:
            raise ValueError("scientist runtime mismatches: " + ", ".join(str(path.relative_to(ROOT)) for path, _ in pending))
        for path, data in pending:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        print(f"PASS Korean recruitment update: 20 exact outputs; 16 portraits; KOR names 56/11/14; {len(pending)} written")
        return 0
    except (ValueError, KeyError, OSError, UnicodeError, struct.error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
