#!/usr/bin/env python3
"""Materialize the reviewed HOK base plus the selected Korean update.

Gameplay inputs use immutable Git objects. The separately reviewed artwork
uses an explicit hash-pinned working-tree snapshot; neither source is modified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from functools import lru_cache
from pathlib import Path

# [2026-09-22]_kpopmodder: Pin the old donor and selected Korean commits separately.
REPO_ROOT = Path(__file__).resolve().parents[1]
DONOR_ROOT = Path(r"C:\hoi\hearts_of_korea")
LOCK_PATH = Path(__file__).with_name("hok_source_lock.json")
#20261105_kpopmodder: Keep all audited generator inputs outside the mod tree after artifact relocation.
SOURCE_CACHE_ROOT = Path(r"C:\hoi\test\hok-rt56-source-cache\sources")
HOK_ROOT = SOURCE_CACHE_ROOT / "hok-887930f-korea-118d7b5"
BASE_COMMIT = "887930f6e88c80568d62dab9cfbe1ba8a498a252"
CONTENT_COMMIT = "da815305e3ce00186a487b3a378bf8536ff59146"
UPDATE_COMMIT = "118d7b53dfdbc120fcfe4b9d6792e66b2b519be7"
AI_PATH = "common/ai_strategy_plans/KOR_historical_strategy_plan.txt"


#20261107_kpopmodder: Project only a verified final split output before enforcing unchanged historical layer locks.
def _historical_runtime(relative: str | Path, data: bytes) -> bytes:
    from korean_state_split import historical_bytes
    return historical_bytes(Path(relative).as_posix(), data)

# [2026-09-22]_kpopmodder: Keep uncommitted artwork provenance separate from the immutable gameplay base.
ICON_LOCK_PATH = Path(__file__).with_name("hok_icon_lock.json")
ICON_ROOT = SOURCE_CACHE_ROOT / "hok-icons-20260922"
ICON_MANIFEST = "docs/data/HOK_KOREAN_FOCUS_ICON_MANIFEST.json"

#20260923_kpopmodder: Isolate the reviewed second-wave delta from the historical world and artwork inputs.
SECOND_WAVE_COMMIT = "be5fb40dbd8de33e5adbf65e808bcb0e8c283560"
SECOND_WAVE_LOCK_PATH = Path(__file__).with_name("hok_second_wave_lock.json")
SECOND_WAVE_ROOT = SOURCE_CACHE_ROOT / "hok-second-wave-be5fb40"
SECOND_WAVE_FOCUS_PATH = "common/national_focus/korea.txt"
SECOND_WAVE_DOCUMENTATION_ROOT = REPO_ROOT / "docs/upstream/hok-second-wave-be5fb40"

#20260923_kpopmodder: Reconstruct the reviewed 17-file policy delta without trusting the donor's later working tree.
POLICY_UPDATE_LOCK_PATH = Path(__file__).with_name("hok_policy_update_lock.json")
POLICY_UPDATE_DOCUMENTATION_ROOT = REPO_ROOT / "docs/upstream/hok-policy-update-20260923"


#20260926_kpopmodder: Pin only the reviewed localisation commit, preserving every historical gameplay/artwork input.
LOCALISATION_UPDATE_COMMIT = "8609d0b61e4c00e6be6c204dcf31cfa41150664e"
LOCALISATION_UPDATE_LOCK_PATH = Path(__file__).with_name("hok_localisation_update_lock.json")


#20261003_kpopmodder: Preserve the approved uncommitted material-cycle module as an exact local source snapshot.
MATERIAL_CYCLE_LOCK_PATH = Path(__file__).with_name("hok_material_cycle_lock.json")
MATERIAL_CYCLE_SNAPSHOT_ROOT = "docs/upstream/hok-material-cycle-20261003"
MATERIAL_CYCLE_TEXT_PATHS = (
    "common/ideas/HOK_KOR_common_followup.txt",
    "common/decisions/HOK_KOR_common_followup.txt",
    "common/decisions/categories/HOK_KOR_common_followup.txt",
    "interface/HOK_KOR_material_cycle_icons.gfx",
    "localisation/english/HOK_KOR_common_followup_l_english.yml",
    "localisation/korean/HOK_KOR_common_followup_l_korean.yml",
)
MATERIAL_CYCLE_ASSET_PATHS = (
    "gfx/interface/decisions/HOK_KOR/material_cycle/cmn_emergency_material_cycle.dds",
    "gfx/interface/decisions/HOK_KOR/material_cycle/cmn_material_cycle_projects.dds",
    "gfx/interface/ideas/HOK_KOR/material_cycle/cmn_emergency_material_cycle_boost.dds",
)
MATERIAL_CYCLE_DOCUMENTATION_PATHS = (
    "docs/HOK_KOREAN_REGIONAL_COMMON_FOLLOWUP_SPEC.md",
    "docs/HOK_KOREAN_MATERIAL_CYCLE_REWARD_SPEC.md",
    "docs/HOK_KOREAN_MATERIAL_CYCLE_ICON_CREDITS.md",
    "docs/data/HOK_KOREAN_MATERIAL_CYCLE_ICON_MANIFEST.json",
    "docs/incidents/2026-10-02-korean-material-cycle.md",
    "docs/assets/korean-material-cycle-icons/sources/CREDITS.txt",
    "docs/assets/korean-material-cycle-icons/sources/Circle.png",
    "docs/assets/korean-material-cycle-icons/sources/Circular Arrows.png",
    "docs/assets/korean-material-cycle-icons/sources/Factories2.png",
    "docs/assets/korean-material-cycle-icons/sources/Steel.png",
    "docs/assets/korean-material-cycle-icons/sources/clock-original.png",
)
MATERIAL_CYCLE_RUNTIME_PATHS = MATERIAL_CYCLE_TEXT_PATHS + MATERIAL_CYCLE_ASSET_PATHS

#20261003_kpopmodder: Freeze only the author's reviewed decision/spirit prose after the existing material-cycle layer.
PROSE_UPDATE_BASE_COMMIT = "43dbb38ac2553942e898e6093a2a46f0430995fc"
PROSE_UPDATE_LOCK_PATH = Path(__file__).with_name("hok_prose_update_lock.json")
PROSE_UPDATE_SNAPSHOT_ROOT = "docs/upstream/hok-prose-update-20261003"
PROSE_UPDATE_DOCUMENTATION_PATHS = (
    "docs/HOK_KOREAN_DECISION_SPIRIT_PROSE_PLAN.md",
    "docs/incidents/2026-10-03-korean-decision-spirit-prose.md",
)


#20261005_kpopmodder: Pin only the committed two-line decision notice, keeping every historical source lock intact.
FOCUS_TOOLTIP_COMMIT = "062a60287e00ac11352c38bca0fca1ae556e7801"
FOCUS_TOOLTIP_LOCK_PATH = Path(__file__).with_name("hok_focus_tooltip_update_lock.json")


@lru_cache(maxsize=1)
def focus_tooltip_update_lock() -> dict:
    lock = json.loads(FOCUS_TOOLTIP_LOCK_PATH.read_text(encoding="utf-8"))
    if (lock["format"], lock["source_kind"], lock["source_commit"], lock["base_commit"],
            lock["path"], lock["focus_id"], lock["decision_id"], lock["checkout"]) != (
        1, "immutable-git-objects", FOCUS_TOOLTIP_COMMIT, "272e7a2f4f30f4739c23440a9f271bbd0acf9878",
        SECOND_WAVE_FOCUS_PATH, "HOK_KOR_cmn_closed_material_cycle",
        "HOK_KOR_cmn_emergency_material_cycle", "crlf"
    ):
        raise ValueError("unreviewed focus decision-tooltip revision or target")
    payloads = []
    for commit_key, blob_key, hash_key in (
        ("base_commit", "base_blob", "base_object_sha256"),
        ("source_commit", "blob", "object_sha256"),
    ):
        blob = subprocess.check_output(git_command() + ["rev-parse", f"{lock[commit_key]}:{lock['path']}"]).decode().strip()
        data = subprocess.check_output(git_command() + ["cat-file", "blob", lock[blob_key]])
        if blob != lock[blob_key] or sha256(data) != lock[hash_key] or b"\r" in data:
            raise ValueError("focus decision-tooltip immutable source drift")
        payloads.append(data)
    base, updated = payloads
    addition = ("\n".join(lock["added_lines"]) + "\n").encode("utf-8")
    if len(lock["added_lines"]) != 2 or lock["added_lines"][1] != "\t\t\tunlock_decision_tooltip = " + lock["decision_id"]:
        raise ValueError("focus decision-tooltip must contain only its contributor note and existing decision notice")
    anchor = focus_tooltip_anchor()
    focus_start = base.index(("\t\tid = " + lock["focus_id"] + "\n").encode())
    focus_end = base.index(b"\n\t}\n", focus_start)
    if (base.count(anchor) != 1 or not focus_start < base.index(anchor) < focus_end
            or updated != base.replace(anchor, anchor + addition, 1)
            or sha256(updated.replace(b"\n", b"\r\n")) != lock["source_sha256"]):
        raise ValueError("focus decision-tooltip changed more than the reviewed two-line source delta")
    return lock


def focus_tooltip_anchor() -> bytes:
    return (b"\t\t\tif = { limit = { has_idea = HOK_KOR_cmn_material_cycle_1 } "
            b"swap_ideas = { remove_idea = HOK_KOR_cmn_material_cycle_1 add_idea = HOK_KOR_cmn_material_cycle_2 } } "
            b"else = { add_ideas = HOK_KOR_cmn_material_cycle_2 }\n")


def apply_focus_tooltip_update(data: bytes) -> bytes:
    lock = focus_tooltip_update_lock()
    if sha256(data) != lock["previous_output_sha256"]:
        raise ValueError("unreviewed pre-tooltip focus output")
    newline = b"\r\n" if b"\r\n" in data else b"\n"
    anchor = focus_tooltip_anchor().replace(b"\n", newline)
    addition = ("\n".join(lock["added_lines"]) + "\n").encode().replace(b"\n", newline)
    if data.count(anchor) != 1:
        raise ValueError("focus decision-tooltip reward anchor is not unique")
    updated = data.replace(anchor, anchor + addition, 1)
    if sha256(updated) != lock["output_sha256"]:
        raise ValueError("focus decision-tooltip output differs from the reviewed merge")
    return updated


def remove_focus_tooltip_update(data: bytes) -> bytes:
    #20261005_kpopmodder: Check historical contracts against the exact ancestor without accepting unrelated focus edits.
    #20261107_kpopmodder: Keep the historical tooltip pin strict below the separate split layer.
    data = _historical_runtime(SECOND_WAVE_FOCUS_PATH, data)
    lock = focus_tooltip_update_lock()
    if sha256(data) != lock["output_sha256"]:
        raise ValueError("unreviewed current focus decision-tooltip output")
    newline = b"\r\n" if b"\r\n" in data else b"\n"
    addition = ("\n".join(lock["added_lines"]) + "\n").encode().replace(b"\n", newline)
    if data.count(addition) != 1:
        raise ValueError("focus decision-tooltip notice is missing or duplicated")
    previous = data.replace(addition, b"", 1)
    if sha256(previous) != lock["previous_output_sha256"]:
        raise ValueError("focus decision-tooltip reversal changed historical gameplay")
    return previous


#20261010_kpopmodder: Pin six prerequisite edits independently of all historical world and gameplay inputs.
FOCUS_PREREQUISITE_COMMIT = "af6fccf2248311c01565c796555ed334ec685015"
FOCUS_PREREQUISITE_LOCK_PATH = Path(__file__).with_name("hok_focus_prerequisite_update_lock.json")
FOCUS_PREREQUISITE_IDS = (
    "HOK_KOR_nrsc_military_administration", "HOK_KOR_nrsc_interservice_liaison",
    "HOK_KOR_cm_court_clerks", "HOK_KOR_cm_public_patronage",
    "HOK_KOR_cmn_export_invoices", "HOK_KOR_cmn_ore_classification",
)


def _replace_focus_prerequisite_lines(data: bytes, edit: dict, reverse: bool = False) -> bytes:
    newline = b"\r\n" if b"\r\n" in data else b"\n"
    before, after = ("after_lines", "before_lines") if reverse else ("before_lines", "after_lines")
    old = "\n".join(edit[before]).encode("utf-8").replace(b"\n", newline)
    new = "\n".join(edit[after]).encode("utf-8").replace(b"\n", newline)
    identifier = ("\t\tid = " + edit["focus_id"]).encode() + newline
    if data.count(identifier) != 1 or data.count(old) != 1:
        raise ValueError(f"prerequisite update target is not unique: {edit['focus_id']}")
    start = data.index(identifier)
    end = data.index(newline + b"\t}" + newline, start)
    if not start < data.index(old) < end or data.index(old) + len(old) > end:
        raise ValueError(f"prerequisite update escaped its focus: {edit['focus_id']}")
    return data.replace(old, new, 1)


@lru_cache(maxsize=1)
def prerequisite_update_lock() -> dict:
    lock = json.loads(FOCUS_PREREQUISITE_LOCK_PATH.read_text(encoding="utf-8"))
    if (lock["format"], lock["source_kind"], lock["source_commit"], lock["base_commit"],
            lock["path"], lock["checkout"], lock["snapshot_root"]) != (
        1, "immutable-git-objects", FOCUS_PREREQUISITE_COMMIT, FOCUS_TOOLTIP_COMMIT,
        SECOND_WAVE_FOCUS_PATH, "crlf", "docs/upstream/hok-prerequisite-update-20261010"
    ) or tuple(edit["focus_id"] for edit in lock["edits"]) != FOCUS_PREREQUISITE_IDS:
        raise ValueError("unreviewed focus prerequisite revision or target inventory")
    if lock["previous_output_sha256"] != focus_tooltip_update_lock()["output_sha256"]:
        raise ValueError("prerequisite overlay must follow the exact historical tooltip output")
    payloads = []
    for commit_key, blob_key, hash_key in (
        ("base_commit", "base_blob", "base_object_sha256"),
        ("source_commit", "blob", "object_sha256"),
    ):
        blob = subprocess.check_output(git_command() + ["rev-parse", f"{lock[commit_key]}:{lock['path']}"]).decode().strip()
        data = subprocess.check_output(git_command() + ["cat-file", "blob", lock[blob_key]])
        if blob != lock[blob_key] or sha256(data) != lock[hash_key] or b"\r" in data:
            raise ValueError("focus prerequisite immutable source drift")
        payloads.append(data)
    expected = payloads[0]
    for edit in lock["edits"]:
        expected = _replace_focus_prerequisite_lines(expected, edit)
    if expected != payloads[1] or sha256(expected.replace(b"\n", b"\r\n")) != lock["source_sha256"]:
        raise ValueError("focus prerequisite source changed outside the six reviewed edits")
    changed_docs = subprocess.check_output(git_command() + [
        "diff", "--name-only", lock["base_commit"], lock["source_commit"], "--", "docs"
    ]).decode().splitlines()
    if sorted(lock["documentation"]) != changed_docs or len(changed_docs) != 7:
        raise ValueError("focus prerequisite documentation inventory mismatch")
    snapshot_root = (REPO_ROOT / lock["snapshot_root"]).resolve()
    for relative, record in lock["documentation"].items():
        if record["snapshot_path"] != "documents/" + relative:
            raise ValueError(f"unsafe prerequisite snapshot path: {relative}")
        target = (snapshot_root / record["snapshot_path"]).resolve()
        target.relative_to(snapshot_root)
        blob = subprocess.check_output(git_command() + ["rev-parse", f"{lock['source_commit']}:{relative}"]).decode().strip()
        raw = subprocess.check_output(git_command() + ["cat-file", "blob", record["blob"]])
        if (blob != record["blob"] or len(raw) != record["size"] or sha256(raw) != record["sha256"]
                or target.read_bytes() != raw):
            raise ValueError(f"focus prerequisite source documentation drift: {relative}")
    return lock


def apply_focus_prerequisite_update(data: bytes) -> bytes:
    lock = prerequisite_update_lock()
    if sha256(data) != lock["previous_output_sha256"]:
        raise ValueError("unreviewed pre-prerequisite focus output")
    updated = data
    for edit in lock["edits"]:
        updated = _replace_focus_prerequisite_lines(updated, edit)
    if sha256(updated) != lock["output_sha256"]:
        raise ValueError("focus prerequisite output differs from the reviewed merge")
    return updated


def remove_focus_prerequisite_update(data: bytes) -> bytes:
    #20261010_kpopmodder: Recover the byte-exact tooltip ancestor for existing preservation gates.
    #20261107_kpopmodder: Keep the historical prerequisite pin strict below the separate split layer.
    data = _historical_runtime(SECOND_WAVE_FOCUS_PATH, data)
    lock = prerequisite_update_lock()
    if sha256(data) != lock["output_sha256"]:
        raise ValueError("unreviewed current focus prerequisite output")
    previous = data
    for edit in reversed(lock["edits"]):
        previous = _replace_focus_prerequisite_lines(previous, edit, reverse=True)
    if sha256(previous) != lock["previous_output_sha256"]:
        raise ValueError("focus prerequisite reversal changed historical gameplay")
    return previous



#20261010_kpopmodder: Keep the royal prerequisite, supply-layout and courier-lifetime delta separate from prior locks.
ROYAL_UPDATE_COMMIT = "4d8241e3cd33ebbceaca9650ab36b9891a22b56d"
ROYAL_UPDATE_LOCK_PATH = Path(__file__).with_name("hok_royal_update_lock.json")
ROYAL_IDEA_PATH = "common/ideas/HOK_KOR_royal_followup.txt"
ROYAL_FOCUS_IDS = (
    "HOK_KOR_am_petition_calendar", "HOK_KOR_am_granary_ledgers", "HOK_KOR_am_relief_dispatches",
    "HOK_KOR_am_regimental_returns", "HOK_KOR_am_nco_examinations", "HOK_KOR_am_reserve_cadre",
    "HOK_KOR_am_mobilization_review", "HOK_KOR_am_technical_memorials",
    "HOK_KOR_am_civil_service_practicum", "HOK_KOR_am_merit_registers",
    "HOK_KOR_hw_dispatch_codes", "HOK_KOR_hw_courier_relays", "HOK_KOR_hw_signal_logs",
    "HOK_KOR_hw_relay_exercises", "HOK_KOR_hw_provincial_inventory",
)
ROYAL_IDEA_IDS = ("HOK_KOR_hw_courier_service_1", "HOK_KOR_hw_courier_service_2")


def _replace_royal_lines(data: bytes, edit: dict, kind: str, *, source: bool = False, reverse: bool = False) -> bytes:
    newline = b"\r\n" if b"\r\n" in data else b"\n"
    before, after = ("after_lines", "before_lines") if reverse else ("before_lines", "after_lines")
    if source and "source_" + before in edit:
        before, after = "source_" + before, "source_" + after
    old = "\n".join(edit[before]).encode("utf-8").replace(b"\n", newline)
    new = "\n".join(edit[after]).encode("utf-8").replace(b"\n", newline)
    if kind == "focus":
        identifier = ("\t\tid = " + edit["id"]).encode() + newline
        closing = newline + b"\t}" + newline
    elif kind == "idea":
        identifier = ("\t\t" + edit["id"] + " = {").encode() + newline
        closing = newline + b"\t\t}" + newline
    else:
        raise ValueError(f"unreviewed royal definition kind: {kind}")
    if data.count(identifier) != 1:
        raise ValueError(f"royal update target is missing or duplicated: {edit['id']}")
    start = data.index(identifier)
    end = data.index(closing, start)
    block = data[start:end]
    if not old or block.count(old) != 1:
        raise ValueError(f"royal update span is missing or duplicated inside its definition: {edit['id']}")
    return data[:start] + block.replace(old, new, 1) + data[end:]


@lru_cache(maxsize=1)
def royal_update_lock() -> dict:
    lock = json.loads(ROYAL_UPDATE_LOCK_PATH.read_text(encoding="utf-8"))
    if (lock["format"], lock["source_kind"], lock["source_commit"], lock["base_commit"], lock["snapshot_root"]) != (
        1, "immutable-git-objects", ROYAL_UPDATE_COMMIT, FOCUS_PREREQUISITE_COMMIT,
        "docs/upstream/hok-royal-update-20261010"
    ) or set(lock["runtime_text"]) != {SECOND_WAVE_FOCUS_PATH, ROYAL_IDEA_PATH}:
        raise ValueError("unreviewed royal update revision or runtime inventory")
    expected_locks = {
        "tools/hok_source_lock.json", "tools/hok_icon_lock.json", "tools/hok_second_wave_lock.json",
        "tools/hok_policy_update_lock.json", "tools/hok_localisation_update_lock.json",
        "tools/hok_material_cycle_lock.json", "tools/hok_prose_update_lock.json",
        "tools/hok_focus_tooltip_update_lock.json", "tools/hok_focus_prerequisite_update_lock.json",
    }
    if set(lock["preserved_historical_locks"]) != expected_locks:
        raise ValueError("royal update historical lock inventory changed")
    for relative, expected in lock["preserved_historical_locks"].items():
        if sha256((REPO_ROOT / relative).read_bytes()) != expected:
            raise ValueError(f"historical source lock changed during royal update: {relative}")
    if (lock["runtime_text"][SECOND_WAVE_FOCUS_PATH]["previous_output_sha256"] != prerequisite_update_lock()["output_sha256"]
            or lock["rt56_base_sha256"] != prerequisite_update_lock()["rt56_base_sha256"]):
        raise ValueError("royal update must preserve the exact prerequisite ancestor and Korean host base")
    for relative, record in lock["runtime_text"].items():
        kind, identifiers = ("focus", ROYAL_FOCUS_IDS) if relative == SECOND_WAVE_FOCUS_PATH else ("idea", ROYAL_IDEA_IDS)
        if (record["kind"], record["checkout"], record["output_checkout"]) != (kind, "crlf", "crlf") or tuple(
            edit["id"] for edit in record["edits"]
        ) != identifiers:
            raise ValueError(f"unreviewed royal definition inventory: {relative}")
        payloads = []
        for commit_key, blob_key, hash_key in (
            ("base_commit", "base_blob", "base_object_sha256"),
            ("source_commit", "blob", "object_sha256"),
        ):
            blob = subprocess.check_output(git_command() + ["rev-parse", f"{lock[commit_key]}:{relative}"]).decode().strip()
            raw = subprocess.check_output(git_command() + ["cat-file", "blob", record[blob_key]])
            if blob != record[blob_key] or sha256(raw) != record[hash_key] or b"\r" in raw:
                raise ValueError(f"royal update immutable source drift: {relative}")
            payloads.append(raw)
        updated = payloads[0]
        for edit in record["edits"]:
            updated = _replace_royal_lines(updated, edit, kind, source=True)
        if updated != payloads[1] or sha256(updated.replace(b"\n", b"\r\n")) != record["source_sha256"]:
            raise ValueError(f"royal source changed outside the reviewed definitions: {relative}")
        if kind == "idea" and sha256(payloads[0].replace(b"\n", b"\r\n")) != record["previous_output_sha256"]:
            raise ValueError("royal idea overlay must follow the unchanged original reward definitions")
    changed_docs = subprocess.check_output(git_command() + [
        "diff", "--name-only", lock["base_commit"], lock["source_commit"], "--", "docs"
    ]).decode().splitlines()
    if sorted(lock["documentation"]) != changed_docs or len(changed_docs) != 7:
        raise ValueError("royal update documentation inventory mismatch")
    snapshot_root = (REPO_ROOT / lock["snapshot_root"]).resolve()
    for relative, record in lock["documentation"].items():
        if record["snapshot_path"] != "documents/" + relative:
            raise ValueError(f"unsafe royal snapshot path: {relative}")
        target = (snapshot_root / record["snapshot_path"]).resolve()
        target.relative_to(snapshot_root)
        blob = subprocess.check_output(git_command() + ["rev-parse", f"{lock['source_commit']}:{relative}"]).decode().strip()
        raw = subprocess.check_output(git_command() + ["cat-file", "blob", record["blob"]])
        if (blob != record["blob"] or len(raw) != record["size"] or sha256(raw) != record["sha256"]
                or target.read_bytes() != raw):
            raise ValueError(f"royal update source documentation drift: {relative}")
    return lock


def apply_royal_update(relative: str | Path, data: bytes) -> bytes:
    relative = Path(relative).as_posix()
    record = royal_update_lock()["runtime_text"][relative]
    if sha256(data) != record["previous_output_sha256"]:
        raise ValueError(f"unreviewed pre-royal output: {relative}")
    updated = data
    for edit in record["edits"]:
        updated = _replace_royal_lines(updated, edit, record["kind"])
    if sha256(updated) != record["output_sha256"]:
        raise ValueError(f"royal output differs from the reviewed RT56 merge: {relative}")
    return updated


def remove_royal_update(relative: str | Path, data: bytes) -> bytes:
    #20261010_kpopmodder: Recover byte-exact prior outputs for every unchanged historical preservation gate.
    relative = Path(relative).as_posix()
    #20261107_kpopmodder: Verify final split bytes before comparing the unchanged royal ancestor.
    data = _historical_runtime(relative, data)
    record = royal_update_lock()["runtime_text"][relative]
    if sha256(data) != record["output_sha256"]:
        raise ValueError(f"unreviewed current royal output: {relative}")
    previous = data
    for edit in reversed(record["edits"]):
        previous = _replace_royal_lines(previous, edit, record["kind"], reverse=True)
    if sha256(previous) != record["previous_output_sha256"]:
        raise ValueError(f"royal reversal changed historical gameplay: {relative}")
    return previous



#20261012_kpopmodder: Preserve the immutable Korean civic module as a separate delta over the royal RT56 merge.
CIVIC_UPDATE_COMMIT = "d4031aaa0c1f85bb89b0e6ca21d041beade8bd26"
CIVIC_UPDATE_LOCK_PATH = Path(__file__).with_name("hok_civic_update_lock.json")
CIVIC_UPDATE_SNAPSHOT_ROOT = "docs/upstream/hok-civic-update-20261012"
CIVIC_UPDATE_TEXT_PATHS = (
    "common/decisions/HOK_KOR_civic_decisions.txt",
    "common/decisions/KOR_decision.txt",
    "common/decisions/categories/HOK_KOR_civic_categories.txt",
    "common/focus_inlay_windows/HOK_KOR_civic_influence_inlay_window.txt",
    "common/ideas/HOK_KOR_civic_ideas.txt",
    "common/national_focus/HOK_KOR_civic_legacy_focus.txt",
    "common/national_focus/korea.txt",
    "common/on_actions/HOK_KOR_civic_on_actions.txt",
    "common/scripted_effects/HOK_KOR_civic_effects.txt",
    "common/scripted_localisation/HOK_KOR_civic_influence_scripted_loc.txt",
    "common/scripted_triggers/HOK_KOR_civic_triggers.txt",
    "events/HOK_KOR_civic_events.txt",
    "interface/HOK_KOR_civic_decisions.gfx",
    "interface/HOK_KOR_civic_events.gfx",
    "interface/HOK_KOR_civic_focus.gfx",
    "interface/HOK_KOR_civic_influence.gfx",
    "interface/HOK_KOR_civic_influence.gui",
    "localisation/english/HOK_KOR_civic_focus_l_english.yml",
    "localisation/english/HOK_KOR_civic_state_l_english.yml",
    "localisation/english/HOK_KOR_civic_ui_l_english.yml",
    "localisation/korean/HOK_KOR_civic_focus_l_korean.yml",
    "localisation/korean/HOK_KOR_civic_state_l_korean.yml",
    "localisation/korean/HOK_KOR_civic_ui_l_korean.yml",
)
CIVIC_UPDATE_ASSET_PATHS = (
    "gfx/event_pictures/HOK_KOR/civic/report_event_fighters.dds",
    "gfx/event_pictures/HOK_KOR/civic/report_event_generic_parliament.dds",
    "gfx/interface/HOK_KOR/civic/button_94x31.dds",
    "gfx/interface/HOK_KOR/civic/pol_leader_frame.dds",
    "gfx/interface/HOK_KOR/civic/tiled_window_small.dds",
    "gfx/interface/HOK_KOR/civic/tiled_window_thin_border2.dds",
    "gfx/interface/decisions/HOK_KOR/civic/category.dds",
    "gfx/interface/decisions/HOK_KOR/civic/influence_blue.dds",
)
CIVIC_UPDATE_RUNTIME_PATHS = CIVIC_UPDATE_TEXT_PATHS + CIVIC_UPDATE_ASSET_PATHS
CIVIC_UPDATE_MODIFIED_PATHS = (SECOND_WAVE_FOCUS_PATH, "common/decisions/KOR_decision.txt")


def _replace_civic_lines(data: bytes, edit: dict, *, source: bool = False, reverse: bool = False) -> bytes:
    newline = b"\r\n" if b"\r\n" in data else b"\n"
    before, after = ("after_lines", "before_lines") if reverse else ("before_lines", "after_lines")
    if source:
        before, after = "source_" + before, "source_" + after
    old = ("\n".join(edit[before]) + "\n").encode("utf-8").replace(b"\n", newline)
    new = ("\n".join(edit[after]) + "\n").encode("utf-8").replace(b"\n", newline)
    if not old or data.count(old) != 1:
        raise ValueError("civic update span is missing or duplicated")
    return data.replace(old, new, 1)


@lru_cache(maxsize=1)
def civic_update_lock() -> dict:
    lock = json.loads(CIVIC_UPDATE_LOCK_PATH.read_text(encoding="utf-8"))
    if (lock["format"], lock["source_kind"], lock["source_commit"], lock["base_commit"], lock["snapshot_root"]) != (
        1, "immutable-git-objects", CIVIC_UPDATE_COMMIT, ROYAL_UPDATE_COMMIT, CIVIC_UPDATE_SNAPSHOT_ROOT
    ) or set(lock["runtime_text"]) != set(CIVIC_UPDATE_TEXT_PATHS) or set(lock["runtime_assets"]) != set(CIVIC_UPDATE_ASSET_PATHS):
        raise ValueError("unreviewed civic source revision or runtime inventory")
    if lock["runtime_paths_sha256"] != sha256("\n".join(sorted(CIVIC_UPDATE_RUNTIME_PATHS)).encode()):
        raise ValueError("civic runtime inventory fingerprint mismatch")
    expected_locks = set(royal_update_lock()["preserved_historical_locks"]) | {"tools/hok_royal_update_lock.json"}
    if set(lock["preserved_historical_locks"]) != expected_locks:
        raise ValueError("civic update historical source-lock inventory changed")
    for relative, expected in lock["preserved_historical_locks"].items():
        if sha256((REPO_ROOT / relative).read_bytes()) != expected:
            raise ValueError(f"historical source lock changed during civic update: {relative}")
    if (lock["runtime_text"][SECOND_WAVE_FOCUS_PATH]["previous_output_sha256"] != royal_update_lock()["runtime_text"][SECOND_WAVE_FOCUS_PATH]["output_sha256"]
            or lock["rt56_base_sha256"] != royal_update_lock()["rt56_base_sha256"]):
        raise ValueError("civic update must retain the reviewed royal ancestor and Korean host base")
    changed = subprocess.check_output(git_command() + [
        "diff", "--name-only", lock["base_commit"], lock["source_commit"]
    ]).decode().splitlines()
    if (set(changed) != set(CIVIC_UPDATE_RUNTIME_PATHS) | set(lock["documentation"]) | {".gitattributes", "README.md"}
            or lock["excluded_source_paths"] != [".gitattributes", "README.md"]
            or len(lock["documentation"]) != 23
            or lock["documentation_paths_sha256"] != sha256("\n".join(sorted(lock["documentation"])).encode())):
        raise ValueError("civic update source diff or documentation inventory changed")

    statuses = dict(line.split("\t", 1)[::-1] for line in subprocess.check_output(git_command() + [
        "diff", "--name-status", lock["base_commit"], lock["source_commit"]
    ]).decode().splitlines())
    if statuses != lock["source_status"] or any(
        statuses[relative] != ("M" if relative in CIVIC_UPDATE_MODIFIED_PATHS else "A")
        for relative in CIVIC_UPDATE_RUNTIME_PATHS
    ):
        raise ValueError("civic source additions/modifications changed")
    snapshot_root = (REPO_ROOT / CIVIC_UPDATE_SNAPSHOT_ROOT).resolve()
    for group in ("runtime_text", "runtime_assets", "documentation"):
        for relative, record in lock[group].items():
            expected_path = ("documents/" if group == "documentation" else "runtime/") + relative
            if record["snapshot_path"] != expected_path or Path(relative).is_absolute() or ".." in Path(relative).parts:
                raise ValueError(f"unsafe civic snapshot path: {relative}")
            target = (snapshot_root / record["snapshot_path"]).resolve()
            target.relative_to(snapshot_root)
            blob = subprocess.check_output(git_command() + ["rev-parse", f"{lock['source_commit']}:{relative}"]).decode().strip()
            raw = subprocess.check_output(git_command() + ["cat-file", "blob", record["blob"]])
            raw_hash = record["sha256"] if group == "documentation" else record["object_sha256"]
            raw_size = record["size"] if group == "documentation" else record["raw_size"]
            if blob != record["blob"] or sha256(raw) != raw_hash or len(raw) != raw_size or target.read_bytes() != raw:
                raise ValueError(f"civic immutable source or snapshot drift: {relative}")
            if group == "documentation":
                continue
            source = checkout_bytes(raw, record)
            if sha256(source) != record["source_sha256"] or len(source) != record["size"]:
                raise ValueError(f"civic source checkout mismatch: {relative}")
            if relative.endswith(".yml") and not source.startswith(b"\xef\xbb\xbf" + f"l_{Path(relative).parts[1]}:".encode()):
                raise ValueError(f"civic localisation BOM/header mismatch: {relative}")

            expected_transform = [{
                "before": "gfx/interface/goals/HOK_KOR/shine_overlay.dds",
                "after": "gfx/interface/goals/shine_overlay.dds", "count": 26,
                "reason": "Preserve the existing shared vanilla shine provider; HOK masks and primary images remain local."
            }] if relative == "interface/HOK_KOR_civic_focus.gfx" else []
            if record.get("transformations", []) != expected_transform:
                raise ValueError(f"unreviewed civic asset transformation: {relative}")
            if relative not in CIVIC_UPDATE_MODIFIED_PATHS:
                output = source
                for edit in expected_transform:
                    before, after = edit["before"].encode(), edit["after"].encode()
                    if output.count(before) != edit["count"]:
                        raise ValueError(f"civic shared shine count mismatch: {relative}")
                    output = output.replace(before, after)
                if sha256(output) != record["output_sha256"] or len(output) != record["output_size"]:
                    raise ValueError(f"civic addition transform fingerprint mismatch: {relative}")
            if relative in CIVIC_UPDATE_MODIFIED_PATHS:
                base_blob = subprocess.check_output(git_command() + ["rev-parse", f"{lock['base_commit']}:{relative}"]).decode().strip()
                base = subprocess.check_output(git_command() + ["cat-file", "blob", record["base_blob"]])
                if base_blob != record["base_blob"] or sha256(base) != record["base_object_sha256"] or len(base) != record["base_raw_size"]:
                    raise ValueError(f"civic immutable ancestor drift: {relative}")
                expected_count = 6 if relative == SECOND_WAVE_FOCUS_PATH else 3
                if len(record["edits"]) != expected_count or any(
                    edit["before_lines"] != edit["source_before_lines"] or edit["after_lines"] != edit["source_after_lines"]
                    for edit in record["edits"]
                ):
                    raise ValueError(f"unreviewed civic source/port edit inventory: {relative}")
                for edit in record["edits"]:
                    base = _replace_civic_lines(base, edit, source=True)
                if base != raw:
                    raise ValueError(f"civic source changed outside the reviewed byte spans: {relative}")
            elif "previous_output_sha256" in record or "edits" in record:
                raise ValueError(f"civic addition unexpectedly replaces an existing output: {relative}")
    return lock


def read_civic_source(relative: str | Path) -> bytes:
    relative = Path(relative).as_posix()
    lock = civic_update_lock()
    record = {**lock["runtime_text"], **lock["runtime_assets"]}[relative]
    raw = (REPO_ROOT / lock["snapshot_root"] / record["snapshot_path"]).read_bytes()
    if sha256(raw) != record["object_sha256"] or len(raw) != record["raw_size"]:
        raise ValueError(f"civic frozen source drift: {relative}")
    return checkout_bytes(raw, record)


def apply_civic_update(relative: str | Path, data: bytes) -> bytes:
    relative = Path(relative).as_posix()
    if relative not in CIVIC_UPDATE_MODIFIED_PATHS:
        raise ValueError(f"civic overlay may only change its two reviewed existing outputs: {relative}")
    record = civic_update_lock()["runtime_text"][relative]
    if sha256(data) != record["previous_output_sha256"]:
        raise ValueError(f"unreviewed pre-civic output: {relative}")
    for edit in record["edits"]:
        data = _replace_civic_lines(data, edit)
    if sha256(data) != record["output_sha256"]:
        raise ValueError(f"civic output differs from the reviewed RT56 merge: {relative}")
    return data


def remove_civic_update(relative: str | Path, data: bytes) -> bytes:
    #20261012_kpopmodder: Recover exact historical outputs for preservation checks without admitting unrelated edits.
    relative = Path(relative).as_posix()
    #20261107_kpopmodder: Verify final split bytes before comparing the unchanged civic ancestor.
    data = _historical_runtime(relative, data)
    if relative not in CIVIC_UPDATE_MODIFIED_PATHS:
        raise ValueError(f"civic reversal may only restore its two reviewed existing outputs: {relative}")
    record = civic_update_lock()["runtime_text"][relative]
    if sha256(data) != record["output_sha256"]:
        raise ValueError(f"unreviewed current civic output: {relative}")
    for edit in reversed(record["edits"]):
        data = _replace_civic_lines(data, edit, reverse=True)
    if sha256(data) != record["previous_output_sha256"]:
        raise ValueError(f"civic reversal changed historical gameplay: {relative}")
    return data


@lru_cache(maxsize=1)
def material_cycle_lock() -> dict:
    lock = json.loads(MATERIAL_CYCLE_LOCK_PATH.read_text(encoding="utf-8"))
    if (lock["format"], lock["source_kind"], lock["base_commit"], lock["snapshot_root"]) != (
        1, "frozen-working-tree-snapshot", LOCALISATION_UPDATE_COMMIT, MATERIAL_CYCLE_SNAPSHOT_ROOT
    ):
        raise ValueError("unreviewed material-cycle snapshot revision")
    groups = {
        "runtime_text": MATERIAL_CYCLE_TEXT_PATHS,
        "runtime_assets": MATERIAL_CYCLE_ASSET_PATHS,
        "documentation": MATERIAL_CYCLE_DOCUMENTATION_PATHS,
    }
    records = {}
    for group, allowed in groups.items():
        if set(lock[group]) != set(allowed):
            raise ValueError(f"material-cycle {group} allowlist mismatch")
        for relative, record in lock[group].items():
            expected_path = ("documents/" if group == "documentation" else "runtime/") + relative
            if record["snapshot_path"] != expected_path:
                raise ValueError(f"unsafe material-cycle snapshot path: {relative}")
            target = (REPO_ROOT / lock["snapshot_root"] / record["snapshot_path"]).resolve()
            target.relative_to((REPO_ROOT / MATERIAL_CYCLE_SNAPSHOT_ROOT).resolve())
            if not re.fullmatch(r"[A-F0-9]{64}", record["sha256"]) or record["size"] <= 0:
                raise ValueError(f"invalid material-cycle source fingerprint: {relative}")
            records[relative] = record
    if sha256("\n".join(sorted(records)).encode()) != lock["paths_sha256"]:
        raise ValueError("material-cycle snapshot inventory fingerprint mismatch")
    for relative, expected in lock["preserved_historical_locks"].items():
        if sha256((REPO_ROOT / relative).read_bytes()) != expected:
            raise ValueError(f"historical source lock changed during material-cycle port: {relative}")
    #20261003_kpopmodder: Prove each accepted checkout variant against the unchanged committed bytes, not a new content hash.
    for relative, record in lock["checkout_restoration"].items():
        if Path(relative).is_absolute() or any(part in (".", "..") for part in relative.split("/")) or any(c in relative for c in "\\:"):
            raise ValueError(f"unsafe checkout restoration path: {relative}")
        row = subprocess.check_output([
            "git", "-C", str(REPO_ROOT), "ls-tree", lock["compatibility_base_commit"], "--", relative
        ])
        if not row or row.split()[2].decode() != record["base_blob"]:
            raise ValueError(f"checkout restoration provenance mismatch: {relative}")
        raw = subprocess.check_output(["git", "-C", str(REPO_ROOT), "cat-file", "blob", record["base_blob"]])
        if b"\r" in raw or sha256(raw) != record["restored_output_sha256"] or sha256(
            raw.replace(b"\n", b"\r\n")
        ) != record["previous_output_sha256"]:
            raise ValueError(f"checkout restoration is not the original LF content: {relative}")
    return lock


def read_material_cycle_source(relative: str | Path) -> bytes:
    relative = Path(relative).as_posix()
    lock = material_cycle_lock()
    records = {path: record for group in ("runtime_text", "runtime_assets", "documentation")
               for path, record in lock[group].items()}
    record = records[relative]
    data = (REPO_ROOT / lock["snapshot_root"] / record["snapshot_path"]).read_bytes()
    if len(data) != record["size"] or sha256(data) != record["sha256"]:
        raise ValueError(f"material-cycle frozen source drift: {relative}")
    if relative.endswith(".yml") and not data.startswith(
        b"\xef\xbb\xbf" + f"l_{Path(relative).parts[1]}:".encode()
    ):
        raise ValueError(f"material-cycle localisation BOM/header mismatch: {relative}")
    return data


@lru_cache(maxsize=1)
def localisation_update_lock() -> dict:
    lock = json.loads(LOCALISATION_UPDATE_LOCK_PATH.read_text(encoding="utf-8"))
    if (lock["format"], lock["source_kind"], lock["commit"]) != (
        1, "immutable-git-objects", LOCALISATION_UPDATE_COMMIT
    ):
        raise ValueError("unreviewed localisation source revision")
    records = lock["runtime_text"]
    paths = sorted(records)
    changed = subprocess.check_output(git_command() + [
        "diff-tree", "--no-commit-id", "--name-only", "-r", LOCALISATION_UPDATE_COMMIT
    ]).decode().splitlines()
    if len(paths) != 28 or paths != changed or sha256("\n".join(paths).encode()) != lock["paths_sha256"]:
        raise ValueError("localisation update allowlist mismatch")
    for relative, record in records.items():
        if not re.fullmatch(r"localisation/(english|korean)/HOK_KOR_[a-z_]+_l_\1\.yml", relative):
            raise ValueError(f"unsafe localisation update path: {relative}")
        blob = subprocess.check_output(git_command() + [
            "rev-parse", f"{LOCALISATION_UPDATE_COMMIT}:{relative}"
        ]).decode().strip()
        if blob != record["blob"] or record["checkout"] != "raw":
            raise ValueError(f"localisation update provenance mismatch: {relative}")
    for relative, expected in lock["preserved_historical_locks"].items():
        if sha256((REPO_ROOT / relative).read_bytes()) != expected:
            raise ValueError(f"historical source lock changed during localisation update: {relative}")
    return lock


@lru_cache(maxsize=28)
def read_localisation_source(relative: str | Path) -> bytes:
    relative = Path(relative).as_posix()
    record = localisation_update_lock()["runtime_text"][relative]
    data = subprocess.check_output(git_command() + ["cat-file", "blob", record["blob"]])
    if len(data) != record["size"] or sha256(data) != record["sha256"] or sha256(data) != record["object_sha256"]:
        raise ValueError(f"localisation source hash mismatch: {relative}")
    language = Path(relative).parts[1]
    if not data.startswith(b"\xef\xbb\xbf" + f"l_{language}:\n".encode()):
        raise ValueError(f"localisation source BOM/header mismatch: {relative}")
    for number, line in enumerate(data.decode("utf-8-sig").splitlines()[1:], 2):
        if line.strip() and not line.lstrip().startswith("#") and not re.fullmatch(
            r'\s+[A-Za-z0-9_.-]+:\d+ "(?:[^"\\]|\\.)*"\s*', line
        ):
            raise ValueError(f"malformed localisation source: {relative}:{number}")
    return data


#20261003_kpopmodder: Keep the prose snapshot independent of the donor's later working-tree changes.
@lru_cache(maxsize=1)
def prose_update_lock() -> dict:
    lock = json.loads(PROSE_UPDATE_LOCK_PATH.read_text(encoding="utf-8"))
    if (lock["format"], lock["source_kind"], lock["base_commit"], lock["snapshot_root"]) != (
        1, "frozen-working-tree-snapshot", PROSE_UPDATE_BASE_COMMIT, PROSE_UPDATE_SNAPSHOT_ROOT
    ):
        raise ValueError("unreviewed prose snapshot revision")
    allowed = set(localisation_update_lock()["runtime_text"])
    if set(lock["runtime_text"]) != allowed or len(allowed) != 28 or set(lock["documentation"]) != set(PROSE_UPDATE_DOCUMENTATION_PATHS):
        raise ValueError("prose snapshot allowlist mismatch")
    records = {**lock["runtime_text"], **lock["documentation"]}
    if sha256("\n".join(sorted(records)).encode()) != lock["paths_sha256"] or lock["paths_sha256"] != "BA93B3E2B8E52D5E3C2DF653C78C3597C6084FA5AF8F3B8C7116156B534F83C4":
        raise ValueError("prose snapshot inventory fingerprint mismatch")
    if sha256("\n".join(sorted(allowed)).encode()) != lock["runtime_paths_sha256"]:
        raise ValueError("prose runtime inventory fingerprint mismatch")
    #20261003_kpopmodder: Verify the pinned base path/blob without consulting the donor's current HEAD or working files.
    rows = subprocess.check_output(git_command() + ["ls-tree", "-z", PROSE_UPDATE_BASE_COMMIT, "--", *sorted(records)])
    tree = {}
    for row in rows.split(b"\0"):
        if not row:
            continue
        metadata, relative = row.split(b"\t", 1)
        mode, kind, blob = metadata.decode().split()
        if kind != "blob" or mode not in ("100644", "100755"):
            raise ValueError(f"unsupported prose base object: {relative.decode()}")
        tree[relative.decode()] = blob
    counts = {"english": 0, "korean": 0}
    for group in ("runtime_text", "documentation"):
        for relative, record in lock[group].items():
            expected_path = ("runtime/" if group == "runtime_text" else "documents/") + relative
            if record["snapshot_path"] != expected_path:
                raise ValueError(f"unsafe prose snapshot path: {relative}")
            target = (REPO_ROOT / PROSE_UPDATE_SNAPSHOT_ROOT / record["snapshot_path"]).resolve()
            target.relative_to((REPO_ROOT / PROSE_UPDATE_SNAPSHOT_ROOT).resolve())
            if not re.fullmatch(r"[A-F0-9]{64}", record["sha256"]) or record["size"] <= 0:
                raise ValueError(f"invalid prose source fingerprint: {relative}")
            if tree.get(relative, "") != record["base_blob"]:
                raise ValueError(f"prose base path/blob provenance mismatch: {relative}")
            if record["base_blob"]:
                base = subprocess.check_output(git_command() + ["cat-file", "blob", record["base_blob"]])
                if sha256(base) != record["base_object_sha256"]:
                    raise ValueError(f"prose base object hash mismatch: {relative}")
            if group == "runtime_text":
                keys = record["changed_description_keys"]
                if (record["integration_class"] != "ADD" or len(keys) != len(set(keys))
                        or not all(key.endswith("_desc") for key in keys)
                        or not re.fullmatch(r"[A-F0-9]{64}", record["previous_output_sha256"])):
                    raise ValueError(f"unreviewed prose description changes: {relative}")
                counts[Path(relative).parts[1]] += len(keys)
    if counts != lock["changed_descriptions_per_channel"] or counts != {"english": 124, "korean": 124}:
        raise ValueError("prose update must contain 124 revised descriptions per channel")
    if lock["collision_audit"] != {name: {"exact_paths": [], "logical_ids": []} for name in ("rt56", "vanilla")}:
        raise ValueError("unreviewed prose host localisation collision")
    historical = {f"tools/hok_{name}_lock.json" for name in (
        "source", "second_wave", "policy_update", "icon", "localisation_update", "material_cycle"
    )}
    if set(lock["preserved_historical_locks"]) != historical:
        raise ValueError("prose historical source-lock allowlist mismatch")
    for relative, expected in lock["preserved_historical_locks"].items():
        if sha256((REPO_ROOT / relative).read_bytes()) != expected:
            raise ValueError(f"historical source lock changed during prose port: {relative}")
    if len(lock["preserved_runtime"]) != 381 or allowed & set(lock["preserved_runtime"]):
        raise ValueError("prose preserved-runtime allowlist mismatch")
    for relative, expected in lock["preserved_runtime"].items():
        path = Path(relative)
        if (path.is_absolute() or any(part in (".", "..") for part in relative.split("/"))
                or any(c in relative for c in "\\:") or not re.fullmatch(r"[A-F0-9]{64}", expected)):
            raise ValueError(f"unsafe prose preserved-runtime path/fingerprint: {relative}")
    return lock


def read_prose_source(relative: str | Path) -> bytes:
    relative = Path(relative).as_posix()
    lock = prose_update_lock()
    record = {**lock["runtime_text"], **lock["documentation"]}[relative]
    data = (REPO_ROOT / lock["snapshot_root"] / record["snapshot_path"]).read_bytes()
    if len(data) != record["size"] or sha256(data) != record["sha256"]:
        raise ValueError(f"prose frozen source drift: {relative}")
    if relative in lock["runtime_text"]:
        language = Path(relative).parts[1]
        if not data.startswith(b"\xef\xbb\xbf" + f"l_{language}:\r\n".encode()) or b"\n" in data.replace(b"\r\n", b""):
            raise ValueError(f"prose localisation BOM/header/CRLF mismatch: {relative}")
        keys = []
        for number, line in enumerate(data.decode("utf-8-sig").splitlines()[1:], 2):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            match = re.fullmatch(r'\s+([A-Za-z0-9_.-]+):\d+ "(?:[^"\\]|\\.)*"\s*', line)
            if match is None:
                raise ValueError(f"malformed prose localisation source: {relative}:{number}")
            keys.append(match[1])
        if (len(keys) != record["key_count"] or len(keys) != len(set(keys))
                or sha256("\n".join(keys).encode()) != record["keys_sha256"]
                or not set(record["changed_description_keys"]).issubset(keys)):
            raise ValueError(f"prose localisation key inventory mismatch: {relative}")
    return data


def verify_prose_snapshot() -> None:
    lock = prose_update_lock()
    expected = {record["snapshot_path"] for group in ("runtime_text", "documentation")
                for record in lock[group].values()} | {"README.md"}
    root = REPO_ROOT / lock["snapshot_root"]
    actual = {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}
    if actual != expected:
        raise ValueError(f"prose snapshot file inventory mismatch: {sorted(actual ^ expected)}")
    for group in ("runtime_text", "documentation"):
        for relative in lock[group]:
            read_prose_source(relative)


@lru_cache(maxsize=1)
def policy_update_lock() -> dict:
    lock = json.loads(POLICY_UPDATE_LOCK_PATH.read_text(encoding="utf-8"))
    if (lock["format"], lock["source_kind"], lock["base_commit"]) != (
        1, "reviewed-working-tree-delta", SECOND_WAVE_COMMIT
    ):
        raise ValueError("unreviewed policy update source revision")
    records = {**lock["runtime_text"], **lock["documentation"]}
    if len(lock["runtime_text"]) != 10 or len(lock["documentation"]) != 7 or len(records) != 17:
        raise ValueError("unexpected policy update inventory")
    digest = sha256("\n".join(sorted(records)).encode("utf-8"))
    if digest != lock["paths_sha256"] or digest != "4625FFACADB78451D9105BB25BC7B14558D6CA01B6D597AC13E91D7EEDB20E3F":
        raise ValueError("policy update allowlist mismatch")
    for relative in records:
        path = Path(relative)
        if path.is_absolute() or any(part in (".", "..") for part in relative.split("/")) or any(c in relative for c in "\\:"):
            raise ValueError(f"unsafe policy update source path: {relative}")
    for relative, expected in lock["preserved_historical_locks"].items():
        if sha256((REPO_ROOT / relative).read_bytes()) != expected:
            raise ValueError(f"historical source lock changed during policy update: {relative}")
    return lock


@lru_cache(maxsize=17)
def read_policy_source(relative: str | Path) -> bytes:
    relative = Path(relative).as_posix()
    lock = policy_update_lock()
    record = {**lock["runtime_text"], **lock["documentation"]}[relative]
    # Verify the base path as well as its blob; a new document must be absent in the base tree.
    rows = subprocess.check_output(git_command() + ["ls-tree", lock["base_commit"], "--", relative])
    blob = rows.split()[2].decode() if rows else ""
    if blob != record["base_blob"]:
        raise ValueError(f"policy update base provenance mismatch: {relative}")
    base = subprocess.check_output(git_command() + ["cat-file", "blob", blob]) if blob else b""
    if sha256(base) != record["base_object_sha256"]:
        raise ValueError(f"policy update base hash mismatch: {relative}")
    lines = base.decode("utf-8").replace("\r\n", "\n").splitlines(keepends=True)
    result, cursor = [], 0
    for start, end, replacement in record["edits"]:
        if not 0 <= cursor <= start <= end <= len(lines) or any("\r" in line for line in replacement):
            raise ValueError(f"invalid policy update line edit: {relative}")
        result.extend(lines[cursor:start])
        result.extend(replacement)
        cursor = end
    result.extend(lines[cursor:])
    mode = record["newline"]
    if mode not in ("lf", "crlf", "mixed"):
        raise ValueError(f"invalid policy update newline mode: {relative}")
    crlf_lines = set(record.get("crlf_lines", []))
    data = "".join(line.replace("\n", "\r\n") if mode == "crlf" or index in crlf_lines else line
                   for index, line in enumerate(result)).encode("utf-8")
    if len(data) != record["size"] or sha256(data) != record["sha256"]:
        raise ValueError(f"policy update reconstructed source mismatch: {relative}")
    return data


def export_policy_documents(check_only: bool = False) -> int:
    pending = {}
    lock = policy_update_lock()
    # Preflight all source bytes, including gameplay, before exporting any document.
    for relative in (*lock["runtime_text"], *lock["documentation"]):
        data = read_policy_source(relative)
        if relative not in lock["documentation"]:
            continue
        target = POLICY_UPDATE_DOCUMENTATION_ROOT / relative.removeprefix("docs/")
        if target.exists():
            if target.read_bytes() != data:
                raise ValueError(f"modified policy source document: {relative}")
        elif check_only:
            raise ValueError(f"policy source document missing: {relative}")
        else:
            pending[target] = data
    for target, data in pending.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as handle:
            handle.write(data)
    return len(pending)


@lru_cache(maxsize=1)
def icon_lock() -> dict:
    lock = json.loads(ICON_LOCK_PATH.read_text(encoding="utf-8"))
    if (lock["format"], lock["source_kind"], lock["base_commit"]) != (
        1, "uncommitted-working-tree", "698b6eb160efbaa04a4d43846330ba002f5e8cc7"
    ):
        raise ValueError("unreviewed artwork source-lock revision")
    if len(lock["runtime_assets"]) != 92 or len(lock["reference_inputs"]) != 4:
        raise ValueError("expected 89 textures, three registries and four reference inputs")
    for relative in icon_records(lock):
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts or "\\" in relative:
            raise ValueError(f"unsafe artwork source path: {relative}")
    return lock


def icon_records(lock: dict | None = None) -> dict:
    lock = icon_lock() if lock is None else lock
    return {relative: record for group in ("runtime_assets", "reference_inputs", "documentation")
            for relative, record in lock[group].items()}


def read_icon_source(relative: str | Path) -> bytes:
    relative = Path(relative).as_posix()
    record = icon_records()[relative]
    data = (ICON_ROOT / relative).read_bytes()
    if len(data) != record["size"] or sha256(data) != record["sha256"]:
        raise ValueError(f"artwork source drift: {relative}")
    return data


def ensure_icon_snapshot(check_only: bool = False) -> int:
    records = icon_records()
    existing = {path.relative_to(ICON_ROOT).as_posix() for path in ICON_ROOT.rglob("*") if path.is_file()}
    if existing - set(records):
        raise ValueError(f"unexpected artwork cache files: {sorted(existing - set(records))}")
    pending = {}
    for relative, record in records.items():
        target = ICON_ROOT / relative
        if target.exists():
            read_icon_source(relative)
            continue
        if check_only:
            raise ValueError(f"artwork cache missing: {relative}; run source_snapshot.py --import-icons")
        data = (DONOR_ROOT / relative).read_bytes()
        if len(data) != record["size"] or sha256(data) != record["sha256"]:
            raise ValueError(f"donor artwork differs from reviewed snapshot: {relative}")
        pending[relative] = data
    # Preflight every source before materializing any new cache file.
    for relative, data in pending.items():
        target = ICON_ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as handle:
            handle.write(data)
    return len(pending)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


@lru_cache(maxsize=1)
def source_lock() -> dict:
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    if (lock["format"], lock["base_commit"], lock["content_commit"], lock["update_commit"]) != (
        1, BASE_COMMIT, CONTENT_COMMIT, UPDATE_COMMIT
    ):
        raise ValueError("unreviewed donor source-lock revision")
    if len(lock["base"]) != 1014 or len(lock["overlay"]) != 20:
        raise ValueError("unexpected donor source-lock inventory")
    for relative in set(lock["base"]) | set(lock["overlay"]):
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts or "\\" in relative:
            raise ValueError(f"unsafe source path: {relative}")
    return lock


FOCUS_UPDATE_PATHS = tuple(source_lock()["overlay"])


def source_record(relative: str | Path, *, updated: bool = True) -> dict:
    relative = Path(relative).as_posix()
    lock = source_lock()
    if updated and relative in lock["overlay"]:
        return {**lock["overlay"][relative], "commit": UPDATE_COMMIT if relative == AI_PATH else CONTENT_COMMIT}
    return {**lock["base"][relative], "commit": BASE_COMMIT}


def checkout_bytes(payload: bytes, record: dict) -> bytes:
    mode = record["checkout"]
    if mode == "raw":
        result = payload
    elif mode == "lf":
        result = payload.replace(b"\r\n", b"\n")
    elif mode == "crlf":
        result = payload.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    elif mode == "crlf_except":
        lf_lines = set(record["lf_lines"])
        lines = payload.replace(b"\r\n", b"\n").splitlines(keepends=True)
        result = b"".join(line if index in lf_lines else line.replace(b"\n", b"\r\n") for index, line in enumerate(lines))
    else:
        raise ValueError(f"unknown checkout mode: {mode}")
    if sha256(result) != record["sha256"]:
        raise ValueError(f"source checkout hash mismatch: {record['blob']}")
    return result


def git_command() -> list[str]:
    return ["git", "-c", f"safe.directory={DONOR_ROOT.as_posix()}", "-C", str(DONOR_ROOT)]


@lru_cache(maxsize=1)
def verify_provenance() -> None:
    # [2026-09-22]_kpopmodder: Verify each claimed commit/path against its immutable Git blob.
    trees = {}
    for commit in (BASE_COMMIT, CONTENT_COMMIT, UPDATE_COMMIT):
        rows = subprocess.check_output(git_command() + ["ls-tree", "-rz", "--full-tree", commit])
        tree = {}
        for row in rows.split(b"\0"):
            if not row:
                continue
            meta, relative = row.split(b"\t", 1)
            mode, kind, blob = meta.decode().split()
            if kind == "blob" and mode in ("100644", "100755"):
                tree[relative.decode("utf-8")] = blob
        trees[commit] = tree
    lock = source_lock()
    for updated, records in ((False, lock["base"]), (True, lock["overlay"])):
        for relative in records:
            record = source_record(relative, updated=updated)
            if trees[record["commit"]].get(relative) != record["blob"]:
                raise ValueError(f"source provenance mismatch: {record['commit']}:{relative}")


def read_source_file(relative: str | Path, updated: bool = False) -> bytes:
    verify_provenance()
    record = source_record(relative, updated=updated)
    payload = subprocess.check_output(git_command() + ["cat-file", "blob", record["blob"]])
    return checkout_bytes(payload, record)


def ensure_source_snapshot(check_only: bool = False) -> int:
    verify_provenance()
    lock = source_lock()
    paths = sorted(set(lock["base"]) | set(lock["overlay"]))
    if len(paths) != 1031:
        raise ValueError("effective donor inventory must contain 1031 files")
    existing = {path.relative_to(HOK_ROOT).as_posix() for path in HOK_ROOT.rglob("*") if path.is_file()}
    unexpected = existing - set(paths)
    if unexpected:
        raise ValueError(f"unexpected source cache files: {sorted(unexpected)}")
    changed = 0
    for relative in paths:
        destination = HOK_ROOT / relative
        record = source_record(relative)
        if destination.is_file():
            if sha256(destination.read_bytes()) != record["sha256"]:
                raise ValueError(f"modified source cache; refusing overwrite: {relative}")
            continue
        if check_only:
            raise ValueError(f"source cache missing: {relative}; run tools/source_snapshot.py")
        data = read_source_file(relative, updated=True)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        changed += 1
    return changed


#20260923_kpopmodder: Verify both immutable Git provenance and explicitly reviewed checkout bytes for each selected input.
@lru_cache(maxsize=1)
def second_wave_lock() -> dict:
    lock = json.loads(SECOND_WAVE_LOCK_PATH.read_text(encoding="utf-8"))
    if (lock["format"], lock["source_kind"], lock["commit"]) != (
        1, "immutable-git-objects", SECOND_WAVE_COMMIT
    ):
        raise ValueError("unreviewed second-wave source-lock revision")
    if {group: len(lock[group]) for group in ("runtime_text", "runtime_assets", "documentation")} != {
        "runtime_text": 58, "runtime_assets": 231, "documentation": 37
    }:
        raise ValueError("unexpected second-wave source inventory")
    records = second_wave_records(lock)
    if len(records) != 326 or len({path.casefold() for path in records}) != len(records):
        raise ValueError("duplicate second-wave source paths")
    for relative, record in records.items():
        path = Path(relative)
        if path.is_absolute() or any(part in (".", "..") for part in relative.split("/")) or any(c in relative for c in "\\:"):
            raise ValueError(f"unsafe second-wave source path: {relative}")
        if record["commit"] != SECOND_WAVE_COMMIT:
            raise ValueError(f"unreviewed second-wave file commit: {relative}")
    paths_hash = sha256("\n".join(sorted(records)).encode("utf-8"))
    if paths_hash != lock["paths_sha256"] or paths_hash != "08CCAD1FD3C67200B3E4C63EE3FF33EE6CB570240B095DECC8E083A0FD64C18E":
        raise ValueError("second-wave allowlist mismatch")
    expected_new = (set(lock["runtime_text"]) | set(lock["runtime_assets"])) - {SECOND_WAVE_FOCUS_PATH}
    if set(lock["absent_before_import"]) != expected_new or len(expected_new) != 288:
        raise ValueError("second-wave previous-output inventory mismatch")
    if lock["accepted_previous_outputs"] != {
        SECOND_WAVE_FOCUS_PATH: "D33DC929878F3CBB2750164086D9B0120C2DAC2ED45B994C5384A720E8D15C22"
    }:
        raise ValueError("unreviewed previous Korean focus output")
    for relative, expected in lock["preserved_historical_locks"].items():
        if sha256((REPO_ROOT / relative).read_bytes()) != expected:
            raise ValueError(f"historical source lock changed during second-wave integration: {relative}")
    return lock


def second_wave_records(lock: dict | None = None) -> dict:
    lock = second_wave_lock() if lock is None else lock
    return {relative: record for group in ("runtime_text", "runtime_assets", "documentation")
            for relative, record in lock[group].items()}


@lru_cache(maxsize=1)
def verify_second_wave_provenance() -> None:
    rows = subprocess.check_output(git_command() + ["ls-tree", "-rz", "--full-tree", SECOND_WAVE_COMMIT])
    tree = {}
    for row in rows.split(b"\0"):
        if not row:
            continue
        meta, relative = row.split(b"\t", 1)
        mode, kind, blob = meta.decode().split()
        if kind == "blob" and mode in ("100644", "100755"):
            tree[relative.decode("utf-8")] = blob
    for relative, record in second_wave_records().items():
        if tree.get(relative) != record["blob"]:
            raise ValueError(f"second-wave source provenance mismatch: {SECOND_WAVE_COMMIT}:{relative}")


def read_second_wave_source(relative: str | Path) -> bytes:
    relative = Path(relative).as_posix()
    record = second_wave_records()[relative]
    verify_second_wave_provenance()
    data = (SECOND_WAVE_ROOT / relative).read_bytes()
    if len(data) != record["size"] or sha256(data) != record["sha256"]:
        raise ValueError(f"second-wave source cache drift: {relative}")
    return data


def ensure_second_wave_snapshot(check_only: bool = False) -> int:
    verify_second_wave_provenance()
    records = second_wave_records()
    existing = {path.relative_to(SECOND_WAVE_ROOT).as_posix() for path in SECOND_WAVE_ROOT.rglob("*") if path.is_file()}
    if existing - set(records):
        raise ValueError(f"unexpected second-wave source cache files: {sorted(existing - set(records))}")
    pending = {}
    for relative, record in records.items():
        target = SECOND_WAVE_ROOT / relative
        if target.exists():
            read_second_wave_source(relative)
            continue
        if check_only:
            raise ValueError(f"second-wave cache missing: {relative}; run source_snapshot.py --import-second-wave")
        payload = subprocess.check_output(git_command() + ["cat-file", "blob", record["blob"]])
        if sha256(payload) != record["object_sha256"]:
            raise ValueError(f"second-wave Git blob hash mismatch: {relative}")
        data = checkout_bytes(payload, record)
        if len(data) != record["size"]:
            raise ValueError(f"second-wave checkout size mismatch: {relative}")
        pending[relative] = data
    # Check the complete allowlist before creating any missing file, and never overwrite cached evidence.
    for relative, data in pending.items():
        target = SECOND_WAVE_ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as handle:
            handle.write(data)
    return len(pending)


#20260923_kpopmodder: Preserve selected upstream specifications and credits as byte-exact archival documents.
def export_second_wave_documents(check_only: bool = False) -> int:
    pending = {}
    for relative in second_wave_lock()["documentation"]:
        if not relative.startswith("docs/"):
            raise ValueError(f"unexpected second-wave document location: {relative}")
        data = read_second_wave_source(relative)
        target = SECOND_WAVE_DOCUMENTATION_ROOT / relative.removeprefix("docs/")
        if target.exists():
            if target.read_bytes() != data:
                raise ValueError(f"modified upstream document; refusing overwrite: {target.relative_to(REPO_ROOT)}")
            continue
        if check_only:
            raise ValueError(f"upstream document missing: {target.relative_to(REPO_ROOT)}; run source_snapshot.py --export-second-wave-docs")
        pending[target] = data
    for target, data in pending.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as handle:
            handle.write(data)
    return len(pending)


SECOND_WAVE_RUNTIME_PATHS = tuple(sorted(set(second_wave_lock()["runtime_text"]) | set(second_wave_lock()["runtime_assets"])))
SECOND_WAVE_ASSET_PATHS = tuple(second_wave_lock()["runtime_assets"])
SECOND_WAVE_SPRITE_PATHS = tuple(path for path in second_wave_lock()["runtime_text"] if path.startswith("interface/"))
SECOND_WAVE_SUPPORT_PATHS = tuple(path for path in second_wave_lock()["runtime_text"] if path != SECOND_WAVE_FOCUS_PATH and not path.startswith("interface/"))
SECOND_WAVE_DOCUMENTATION_PATHS = tuple(second_wave_lock()["documentation"])
#20261003_kpopmodder: Derive prose output ownership from the unchanged historical localisation allowlist.
PROSE_UPDATE_RUNTIME_PATHS = tuple(prose_update_lock()["runtime_text"])


#20261020_kpopmodder: Freeze only the author's emergency shipbuilding delta after the existing RT56 and English layers.
SHIPBUILDING_LOCK_PATH = Path(__file__).with_name("hok_shipbuilding_update_lock.json")
SHIPBUILDING_SNAPSHOT_ROOT = REPO_ROOT / "docs/upstream/hok-emergency-shipbuilding-20261020"
SHIPBUILDING_MODIFIED_PATHS = frozenset((SECOND_WAVE_FOCUS_PATH, "common/ideas/korea.txt", "common/decisions/KOR_decision.txt"))


@lru_cache(maxsize=1)
def shipbuilding_update_lock() -> dict:
    lock = json.loads(SHIPBUILDING_LOCK_PATH.read_text(encoding="utf-8"))
    if (lock["format"], lock["source_kind"], lock["source_commit"], lock["compatibility_base_commit"],
            len(lock["runtime_text"]), len(lock["runtime_assets"]), len(lock["documentation"])) != (
        1, "reviewed-working-tree-snapshot", "d4031aaa0c1f85bb89b0e6ca21d041beade8bd26",
        "1cb07066bc929489293a21f9418f3d427cfab8a6", 7, 2, 8
    ) or {p for p, r in lock["runtime_text"].items() if "previous_output_sha256" in r} != SHIPBUILDING_MODIFIED_PATHS:
        raise ValueError("unreviewed shipbuilding source revision or runtime inventory")
    expected_keys = {name + suffix for name in ("HOK_KOR_enact_emergency_special_shipbuilding", "HOK_KOR_emergency_special_shipbuilding") for suffix in ("", "_desc")}
    if set(lock["english_values"]) != expected_keys:
        raise ValueError("shipbuilding English translation key inventory drift")
    for relative, expected in lock["preserved_historical_locks"].items():
        #20261020_kpopmodder: Accept only the captured raw bytes or their separately pinned LF checkout, preserving JSON content across Git filters.
        data = (REPO_ROOT / relative).read_bytes()
        exact_lf = b"\r" not in data and sha256(data) == lock["preserved_historical_lock_lf_sha256"][relative]
        if sha256(data) != expected and not exact_lf:
            raise ValueError(f"shipbuilding changed a historical source lock: {relative}")
    return lock


def read_shipbuilding_source(relative: str) -> bytes:
    relative = Path(relative).as_posix()
    lock = shipbuilding_update_lock()
    records = {**lock["runtime_text"], **lock["runtime_assets"], **lock["documentation"]}
    record = records[relative]
    path = (REPO_ROOT / record["snapshot_path"]).resolve()
    path.relative_to(SHIPBUILDING_SNAPSHOT_ROOT.resolve())
    data = path.read_bytes()
    if len(data) != record["size"] or sha256(data) != record["sha256"]:
        raise ValueError(f"shipbuilding frozen source drift: {relative}")
    return data


def _shipbuilding_edits(data: bytes, record: dict, reverse: bool = False) -> bytes:
    newline = b"\r\n" if b"\r\n" in data else b"\n"
    for edit in reversed(record["edits"]) if reverse else record["edits"]:
        before, after = ("after_lines", "before_lines") if reverse else ("before_lines", "after_lines")
        old = ("\n".join(edit[before]) + "\n").encode().replace(b"\n", newline)
        new = ("\n".join(edit[after]) + "\n").encode().replace(b"\n", newline)
        if data.count(old) != 1:
            raise ValueError("shipbuilding hunk anchor missing or duplicated")
        data = data.replace(old, new, 1)
    return data


def apply_shipbuilding_update(relative: str, data: bytes) -> bytes:
    relative = Path(relative).as_posix()
    record = shipbuilding_update_lock()["runtime_text"].get(relative, {})
    if "previous_output_sha256" not in record:
        return data
    if sha256(data) != record["previous_output_sha256"]:
        raise ValueError(f"unreviewed pre-shipbuilding output: {relative}")
    result = _shipbuilding_edits(data, record)
    if sha256(result) != record["output_sha256"]:
        raise ValueError(f"shipbuilding merged output drift: {relative}")
    return result


def remove_shipbuilding_update(relative: str, data: bytes) -> bytes:
    relative = Path(relative).as_posix()
    #20261107_kpopmodder: Keep existing naval output hashes beneath a verified state-split reversal.
    data = _historical_runtime(relative, data)
    record = shipbuilding_update_lock()["runtime_text"].get(relative, {})
    if "previous_output_sha256" not in record:
        return data
    if sha256(data) != record["output_sha256"]:
        raise ValueError(f"shipbuilding output differs from reviewed merge: {relative}")
    result = _shipbuilding_edits(data, record, reverse=True)
    if sha256(result) != record["previous_output_sha256"]:
        raise ValueError(f"shipbuilding reversal changed historical output: {relative}")
    return result


def shipbuilding_addition(relative: str) -> bytes:
    relative = Path(relative).as_posix()
    lock = shipbuilding_update_lock()
    record = {**lock["runtime_text"], **lock["runtime_assets"]}[relative]
    if "previous_output_sha256" in record:
        raise ValueError(f"shipbuilding existing output requires a reviewed ancestor: {relative}")
    data = read_shipbuilding_source(relative)
    if relative.startswith("localisation/english/"):
        data = ENGLISH_ROW.sub(lambda row: row[1] + lock["english_values"][row[2]] + row[5],
                               data.decode("utf-8-sig")).encode("utf-8-sig")
    if sha256(data) != record["output_sha256"]:
        raise ValueError(f"shipbuilding addition output drift: {relative}")
    return data


def verify_shipbuilding_snapshot() -> None:
    lock = shipbuilding_update_lock()
    for group in ("runtime_text", "runtime_assets", "documentation"):
        for relative, record in lock[group].items():
            data = read_shipbuilding_source(relative)
            if "previous_output_sha256" in record:
                blob = subprocess.check_output(git_command() + ["rev-parse", f"{lock['source_commit']}:{relative}"]).decode().strip()
                original = subprocess.check_output(git_command() + ["cat-file", "blob", record["base_blob"]])
                if blob != record["base_blob"] or sha256(original) != record["base_object_sha256"]:
                    raise ValueError(f"shipbuilding immutable base drift: {relative}")
                if _shipbuilding_edits(original, record).replace(b"\r\n", b"\n") != data.replace(b"\r\n", b"\n"):
                    raise ValueError(f"shipbuilding donor changed outside the reviewed hunk: {relative}")
            elif group != "documentation":
                shipbuilding_addition(relative)
    print("PASS shipbuilding frozen source: 7 runtime text, 2 DDS, 8 source documents/assets; three reviewed source hunks")


#20261031_kpopmodder: Keep the new Korean systems as a reversible, immutable overlay over the reviewed RT56 outputs.
FEATURE_LOCK_PATH = Path(__file__).with_name("hok_feature_update_lock.json")
FEATURE_SNAPSHOT_ROOT = REPO_ROOT / "docs/upstream/hok-feature-integration-20261031"
FEATURE_COMMIT = "07de265c1e992abb6584bdfcdf140320188c07f9"
FEATURE_BASE_COMMIT = "860efe7a3513148dc6964b7e0e3dfafd19addfb7"


@lru_cache(maxsize=1)
def feature_update_lock() -> dict:
    lock = json.loads(FEATURE_LOCK_PATH.read_text(encoding="utf-8"))
    if (lock["format"], lock["source_commit"], lock["base_commit"]) != (1, FEATURE_COMMIT, FEATURE_BASE_COMMIT):
        raise ValueError("unreviewed Korean feature source revision")
    if (len(lock["runtime_text"]), len(lock["runtime_assets"]), len(lock["documentation"])) != (30, 28, 51):
        raise ValueError("Korean feature source allowlist changed")
    return lock


def _feature_archive(relative: str, digest: str) -> bytes:
    path = (REPO_ROOT / relative).resolve()
    path.relative_to(FEATURE_SNAPSHOT_ROOT.resolve())
    data = path.read_bytes()
    if sha256(data) != digest:
        raise ValueError(f"Korean feature snapshot drift: {relative}")
    return data


def read_feature_source(relative: str) -> bytes:
    name = Path(relative).as_posix()
    lock = feature_update_lock()
    record = {**lock["runtime_text"], **lock["runtime_assets"], **lock["documentation"]}[name]
    data = _feature_archive(record["snapshot_path"], record["sha256"])
    if len(data) != record["size"]:
        raise ValueError(f"Korean feature source size drift: {name}")
    return data


def _feature_edits(data: bytes, record: dict, reverse: bool = False) -> bytes:
    newline = b"\r\n" if b"\r\n" in data else b"\n"
    for edit in reversed(record["hunks"]) if reverse else record["hunks"]:
        old_key, new_key = ("after", "before") if reverse else ("before", "after")
        old = "\n".join(edit[old_key]).encode("utf-8").replace(b"\n", newline)
        new = "\n".join(edit[new_key]).encode("utf-8").replace(b"\n", newline)
        if not old or data.count(old) != 1:
            raise ValueError("Korean feature hunk is missing or duplicated")
        data = data.replace(old, new, 1)
    return data


def apply_feature_update(relative: str, data: bytes) -> bytes:
    name = Path(relative).as_posix()
    record = feature_update_lock()["runtime_text"].get(name, {})
    if "previous_output_sha256" not in record:
        return data
    if sha256(data) != record["previous_output_sha256"]:
        raise ValueError(f"unreviewed pre-feature output: {name}")
    result = _feature_edits(data, record)
    if sha256(result) != record["output_sha256"]:
        raise ValueError(f"Korean feature merged output drift: {name}")
    return result


def remove_feature_update(relative: str, data: bytes) -> bytes:
    name = Path(relative).as_posix()
    #20261107_kpopmodder: Preserve all feature hashes after recovering the exact pre-split output.
    data = _historical_runtime(name, data)
    #20261101_kpopmodder: Verify and reverse the placement-only overlay before checking the historical feature ancestor.
    data = remove_democratic_layout_update(name, data)
    record = feature_update_lock()["runtime_text"].get(name, {})
    if "previous_output_sha256" not in record:
        return data
    if sha256(data) != record["output_sha256"]:
        raise ValueError(f"Korean feature output differs from reviewed merge: {name}")
    result = _feature_edits(data, record, reverse=True)
    if sha256(result) != record["previous_output_sha256"]:
        raise ValueError(f"Korean feature reversal changed historical output: {name}")
    return result


def feature_addition(relative: str) -> bytes:
    name = Path(relative).as_posix()
    lock = feature_update_lock()
    record = {**lock["runtime_text"], **lock["runtime_assets"]}[name]
    if "previous_output_sha256" in record:
        raise ValueError(f"Korean feature existing file requires its reviewed ancestor: {name}")
    data = read_feature_source(name)
    translated = False
    for edit in record.get("transformations", []):
        if edit["kind"] == "english_translation":
            if not name.startswith("localisation/english/") or translated:
                raise ValueError(f"invalid Korean feature translation target: {name}")
            data = _feature_archive(edit["output_snapshot_path"], record["output_sha256"])
            translated = True
            continue
        if edit["kind"] != "persistent_id_migration" or edit["match"] != "numeric-token":
            raise ValueError(f"unreviewed Korean feature transformation: {name}")
        old, new = edit["before"].encode("utf-8"), edit["after"].encode("utf-8")
        data, count = re.subn(rb"(?<![0-9])" + re.escape(old) + rb"(?![0-9])", lambda _: new, data)
        if count != edit["count"]:
            raise ValueError(f"Korean feature transformation count drift: {name}")
    if record.get("output_checkout") == "crlf":
        data = data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    if "output_snapshot_path" in record and data != _feature_archive(record["output_snapshot_path"], record["output_sha256"]):
        raise ValueError(f"Korean feature addition differs from its reviewed transformations: {name}")
    if sha256(data) != record["output_sha256"]:
        raise ValueError(f"Korean feature addition drift: {name}")
    return data


def verify_feature_snapshot() -> None:
    lock = feature_update_lock()
    #20261031_kpopmodder: Reject drift in the current host/schema inputs without altering older unresolved source pins.
    roots = (("host_files", Path(r"C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968")),
             ("vanilla_files", Path(r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV")))
    for group, root in roots:
        for relative, expected in lock[group].items():
            path = (root / relative).resolve()
            path.relative_to(root.resolve())
            if sha256(path.read_bytes()) != expected:
                raise ValueError(f"Korean feature {group} source drift: {relative}")
    workshop = roots[0][1].parents[2] / "appworkshop_394360.acf"
    entries = re.findall(r'"820260968"\s*\{([^}]+)\}', workshop.read_text(encoding="utf-8"))
    manifests = [re.search(r'"manifest"\s*"(\d+)"', entry) for entry in entries]
    if not manifests or any(item is None or item[1] != lock["workshop_manifest"] for item in manifests):
        raise ValueError("Korean feature RT56 Workshop manifest drift")
    for group in ("runtime_text", "runtime_assets", "documentation"):
        for relative, record in lock[group].items():
            data = read_feature_source(relative)
            blob = subprocess.check_output(git_command() + ["rev-parse", f"{FEATURE_COMMIT}:{relative}"]).decode().strip()
            raw = subprocess.check_output(git_command() + ["cat-file", "blob", record["blob"]])
            if blob != record["blob"] or raw != data:
                raise ValueError(f"Korean feature immutable source drift: {relative}")
            if "previous_output_sha256" in record:
                base_blob = subprocess.check_output(git_command() + ["rev-parse", f"{FEATURE_BASE_COMMIT}:{relative}"]).decode().strip()
                original = subprocess.check_output(git_command() + ["cat-file", "blob", record["base_blob"]])
                if base_blob != record["base_blob"] or sha256(original) != record["base_object_sha256"]:
                    raise ValueError(f"Korean feature immutable base drift: {relative}")
                if _feature_edits(original, record) != data:
                    raise ValueError(f"Korean feature donor changed outside its reviewed hunks: {relative}")
                previous = _feature_archive(record["previous_snapshot_path"], record["previous_output_sha256"])
                apply_feature_update(relative, previous)
            elif group != "documentation":
                feature_addition(relative)
    print(f"PASS Korean feature source: {len(lock['runtime_text'])} runtime text, {len(lock['runtime_assets'])} assets, {len(lock['documentation'])} source records")


#20261101_kpopmodder: Freeze the author's uncommitted democratic placement changes separately from gameplay and prior source locks.
DEMOCRATIC_LAYOUT_LOCK_PATH = Path(__file__).with_name("hok_democratic_layout_lock.json")
DEMOCRATIC_LAYOUT_SNAPSHOT_ROOT = REPO_ROOT / "docs/upstream/hok-democratic-layout-20261101"


@lru_cache(maxsize=1)
def democratic_layout_lock() -> dict:
    lock = json.loads(DEMOCRATIC_LAYOUT_LOCK_PATH.read_text(encoding="utf-8"))
    if (lock["format"], lock["source_kind"], lock["source_commit"], lock["base_commit"],
            lock["compatibility_base_commit"]) != (
        1, "reviewed-working-tree-snapshot", FEATURE_COMMIT, FEATURE_COMMIT,
        "656d9b425a66d95f55d8c86f1b976b2e094cc4d8"
    ) or set(lock["runtime_text"]) != {SECOND_WAVE_FOCUS_PATH} or len(lock["documentation"]) != 6:
        raise ValueError("unreviewed democratic layout source revision or allowlist")
    record = lock["runtime_text"][SECOND_WAVE_FOCUS_PATH]
    if (record["sha256"], record["previous_output_sha256"]) != (
        "6562D4ACFD05F791026502A9AEACE3668D3C89869DF4279F75C2F1016763F163",
        feature_update_lock()["runtime_text"][SECOND_WAVE_FOCUS_PATH]["output_sha256"]
    ):
        raise ValueError("democratic layout must follow the exact reviewed Korean feature output")
    return lock


def _democratic_layout_archive(relative: str, digest: str) -> bytes:
    path = (REPO_ROOT / relative).resolve()
    path.relative_to(DEMOCRATIC_LAYOUT_SNAPSHOT_ROOT.resolve())
    data = path.read_bytes()
    if sha256(data) != digest:
        raise ValueError(f"democratic layout snapshot drift: {relative}")
    return data


def apply_democratic_layout_update(relative: str, data: bytes) -> bytes:
    if Path(relative).as_posix() != SECOND_WAVE_FOCUS_PATH:
        return data
    record = democratic_layout_lock()["runtime_text"][SECOND_WAVE_FOCUS_PATH]
    if sha256(data) != record["previous_output_sha256"]:
        raise ValueError("unreviewed pre-democratic-layout focus output")
    result = _feature_edits(data, record)
    if sha256(result) != record["output_sha256"]:
        raise ValueError("democratic layout output differs from its reviewed merge")
    return result


def remove_democratic_layout_update(relative: str, data: bytes) -> bytes:
    if Path(relative).as_posix() != SECOND_WAVE_FOCUS_PATH:
        return data
    #20261107_kpopmodder: Recover the exact preceding tree before the strictly pinned layout reversal.
    data = _historical_runtime(SECOND_WAVE_FOCUS_PATH, data)
    data = remove_prospecting_focus(data)
    record = democratic_layout_lock()["runtime_text"][SECOND_WAVE_FOCUS_PATH]
    if sha256(data) == record["previous_output_sha256"]:
        return data
    if sha256(data) != record["output_sha256"]:
        raise ValueError("unreviewed democratic layout focus output")
    previous = _feature_edits(data, record, reverse=True)
    if sha256(previous) != record["previous_output_sha256"]:
        raise ValueError("democratic layout reversal changed historical gameplay")
    return previous


def verify_democratic_layout_snapshot() -> None:
    lock = democratic_layout_lock()
    for group in ("runtime_text", "documentation"):
        for relative, record in lock[group].items():
            data = _democratic_layout_archive(record["snapshot_path"], record["sha256"])
            if len(data) != record["size"]:
                raise ValueError(f"democratic layout source size drift: {relative}")
            if group == "runtime_text":
                blob = subprocess.check_output(git_command() + ["rev-parse", f"{FEATURE_COMMIT}:{relative}"]).decode().strip()
                original = subprocess.check_output(git_command() + ["cat-file", "blob", record["base_blob"]])
                if blob != record["base_blob"] or sha256(original) != record["base_object_sha256"]:
                    raise ValueError("democratic layout committed donor ancestor drift")
                if _democratic_layout_archive(record["base_snapshot_path"], record["base_object_sha256"]) != original:
                    raise ValueError("democratic layout archived donor ancestor differs from its immutable Git object")
                if _feature_edits(original, record).replace(b"\r\n", b"\n") != data.replace(b"\r\n", b"\n"):
                    raise ValueError("donor layout changed outside the selected coordinate hunks")
                previous = _democratic_layout_archive(record["previous_snapshot_path"], record["previous_output_sha256"])
                expected = _democratic_layout_archive(record["output_snapshot_path"], record["output_sha256"])
                if apply_democratic_layout_update(relative, previous) != expected or remove_democratic_layout_update(relative, expected) != previous:
                    raise ValueError("democratic layout must reproduce and reverse its exact compatibility output")
    roots = (("host_files", Path(r"C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968")),
             ("vanilla_files", Path(r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV")))
    for group, root in roots:
        for relative, expected in lock.get(group, {}).items():
            path = (root / relative).resolve()
            path.relative_to(root.resolve())
            if sha256(path.read_bytes()) != expected:
                raise ValueError(f"democratic layout {group} source drift: {relative}")
    print("PASS democratic layout snapshot: one focus source, six source documents, exact coordinate merge and reversal")


#20261107_kpopmodder: Replay the prospecting delta without updating the historical gameplay or artwork pins.
PROSPECTING_LOCK_PATH = Path(__file__).with_name("hok_resource_prospecting_lock.json")
PROSPECTING_SNAPSHOT = REPO_ROOT / "docs/upstream/hok-resource-prospecting-20261107/runtime"
PROSPECTING_DECISIONS = "common/decisions/HOK_KOR_resource_prospecting.txt"
PROSPECTING_AUDIO = "music/Sinarirang.ogg"
POHANG_FOCUS_ID = b"\t\tid = KOR_pohang_iron__steel_company\r\n"
POHANG_REWARD = b"\t\tcompletion_reward = {\r\n"


@lru_cache(maxsize=1)
def prospecting_lock() -> dict:
    lock = json.loads(PROSPECTING_LOCK_PATH.read_text(encoding="utf-8"))
    if (lock["format"], lock["source_kind"], len(lock["additions"])) != (
        1, "reviewed-working-tree-snapshot", 6
    ) or lock["focus"]["previous_output_sha256"] != democratic_layout_lock()["runtime_text"][SECOND_WAVE_FOCUS_PATH]["output_sha256"]:
        raise ValueError("unreviewed Korean prospecting source or preceding focus output")
    return lock


def _prospecting_notice() -> bytes:
    return ("\r\n".join(prospecting_lock()["focus"]["notice"]) + "\r\n").encode("utf-8")


def _insert_prospecting_notice(data: bytes, state: bytes) -> bytes:
    if data.count(POHANG_FOCUS_ID) != 1:
        raise ValueError("expected one Pohang focus definition")
    offset = data.index(POHANG_REWARD, data.index(POHANG_FOCUS_ID)) + len(POHANG_REWARD)
    if not data.startswith(b"\t\t\t" + state + b" = {\r\n\t\t\t\tadd_resource = { ", offset):
        raise ValueError("Pohang focus reward anchor changed")
    return data[:offset] + _prospecting_notice() + data[offset:]


def apply_prospecting_focus(data: bytes) -> bytes:
    record = prospecting_lock()["focus"]
    if sha256(data) != record["previous_output_sha256"]:
        raise ValueError("unreviewed pre-prospecting focus output")
    result = _insert_prospecting_notice(data, b"920")
    if sha256(result) != record["output_sha256"]:
        raise ValueError("Pohang decision notice differs from the reviewed focus merge")
    return result


def remove_prospecting_focus(data: bytes) -> bytes:
    #20261107_kpopmodder: Recover the exact existing prospecting tree before checking its immutable notice hash.
    data = _historical_runtime(SECOND_WAVE_FOCUS_PATH, data)
    notice = _prospecting_notice()
    if notice not in data:
        return data
    record = prospecting_lock()["focus"]
    if sha256(data) != record["output_sha256"]:
        raise ValueError("unreviewed prospecting focus output")
    result = data.replace(notice, b"", 1)
    if sha256(result) != record["previous_output_sha256"]:
        raise ValueError("Pohang notice reversal changed the preceding focus output")
    return result


@lru_cache(maxsize=1)
def prospecting_additions() -> dict[Path, bytes]:
    lock = prospecting_lock()
    outputs = {}
    for relative, record in lock["additions"].items():
        path = (PROSPECTING_SNAPSHOT / relative).resolve()
        path.relative_to(PROSPECTING_SNAPSHOT.resolve())
        data = path.read_bytes()
        if sha256(data) != record["sha256"]:
            raise ValueError(f"prospecting snapshot drift: {relative}")
        if relative == PROSPECTING_DECISIONS:
            header, body = data.split(b"\r\n", 1)
            for old, new in ((b"1029", b"1144"), (b"1030", b"920")):
                body, count = re.subn(rb"\b" + old + rb"\b", new, body)
                if count != 6:
                    raise ValueError(f"prospecting state reference count changed: {old!r}")
            data = b"\r\n".join((header, lock["decision_note"].encode("utf-8"), body))
        elif path.suffix == ".yml":
            header, body = data.split(b"\r\n", 1)
            if header == b"\xef\xbb\xbfl_english:":
                for key, value in lock["english"].items():
                    pattern = rb'(?m)^ ' + re.escape(key.encode("ascii")) + rb':0 "[^"\r\n]*"(?=\r$)'
                    row = f' {key}:0 "{value}"'.encode("utf-8")
                    body, count = re.subn(pattern, lambda _: row, body)
                    if count != 1:
                        raise ValueError(f"prospecting translation key changed: {key}")
            elif header != b"\xef\xbb\xbfl_korean:":
                raise ValueError(f"unreviewed prospecting locale: {relative}")
            data = b"\r\n".join((header, lock["localisation_note"].encode("utf-8"), body))
        if sha256(data) != record["output_sha256"]:
            raise ValueError(f"prospecting output differs from its reviewed merge: {relative}")
        outputs[Path(relative)] = data
    return outputs


@lru_cache(maxsize=1)
def read_prospecting_audio() -> bytes:
    record = prospecting_lock()["audio"]
    revision = f"{record['source_commit']}:{PROSPECTING_AUDIO}"
    blob = subprocess.check_output(git_command() + ["rev-parse", revision]).decode().strip()
    data = subprocess.check_output(git_command() + ["cat-file", "blob", blob])
    if blob != record["source_blob"] or sha256(data) != record["sha256"]:
        raise ValueError("unreviewed Sinarirang donor source")
    return data


def verify_prospecting_snapshot() -> None:
    lock = prospecting_lock()
    revision = f"{lock['working_tree_base']}:{SECOND_WAVE_FOCUS_PATH}"
    source = subprocess.check_output(git_command() + ["show", revision])
    source = source.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    if sha256(_insert_prospecting_notice(source, b"1030")) != lock["focus"]["source_sha256"]:
        raise ValueError("Pohang notice differs from the reviewed donor working tree")
    prospecting_additions()
    read_prospecting_audio()


#20261020_kpopmodder: Reuse the reviewed English translation only for the port's existing keys and RT56-specific wording.
ENGLISH_TRANSLATION_LOCK_PATH = Path(__file__).with_name("hok_english_translation_lock.json")
ENGLISH_COMMENT_LOCK_PATH = Path(__file__).with_name("hok_english_comment_translation_lock.json")
ENGLISH_TRANSLATION_ARCHIVE = REPO_ROOT / "docs/upstream/hok-english-20261020"
ENGLISH_ROW = re.compile(r'(?m)^([ \t]*([A-Za-z0-9_.-]+):(\d*)[ \t]+")((?:[^"\\\r\n]|\\[^\r\n])*)("[ \t]*(?:#[^\r\n]*)?\r?$)')
ENGLISH_TOKENS = re.compile(r'\$[^$\r\n]+\$|\[(?:\?|[A-Z][A-Za-z0-9_]*\.|Get)[^\]\r\n]+\]|§.|£[A-Za-z0-9_]+|@[A-Z][A-Z0-9]{2}')


@lru_cache(maxsize=1)
def english_translation_lock() -> dict:
    lock = json.loads(ENGLISH_TRANSLATION_LOCK_PATH.read_text(encoding="utf-8"))
    if (lock["format"], lock["source_commit"], lock["compatibility_base_commit"],
            len(lock["source_files"]), len(lock["runtime_text"]), len(lock["adapted_values"])) != (
        1, "6f501200f723245636ecf3b246e0d3e74c490422", "bf2b997f9d7ddc1710533e9700b641f2fb9e8ce0", 37, 36, 52
    ):
        raise ValueError("unreviewed English translation source or inventory")
    return lock


@lru_cache(maxsize=1)
def english_comment_translation_lock() -> dict:
    records = json.loads(ENGLISH_COMMENT_LOCK_PATH.read_text(encoding="utf-8"))
    if (len(records) != 6 or records.keys() - english_translation_lock()["runtime_text"].keys()
            or sum(len(record["translations"]) for record in records.values()) != 19):
        raise ValueError("unreviewed English comment translation inventory")
    return records


def _english_archive(relative: str, digest: str) -> bytes:
    path = (REPO_ROOT / relative).resolve()
    path.relative_to(ENGLISH_TRANSLATION_ARCHIVE.resolve())
    data = path.read_bytes()
    if sha256(data) != digest:
        raise ValueError(f"English translation archive drift: {relative}")
    return data


def english_entries(data: bytes) -> dict[str, tuple[str, str]]:
    text = data.decode("utf-8-sig")
    rows = list(ENGLISH_ROW.finditer(text))
    entries = {row[2]: (row[3], row[4]) for row in rows}
    if len(rows) != len(entries):
        raise ValueError("duplicate English translation key")
    for line in text.splitlines()[1:]:
        if line.strip() and not line.lstrip().startswith("#") and ENGLISH_ROW.fullmatch(line) is None:
            raise ValueError(f"unparsed localisation line: {line[:100]}")
    return entries


@lru_cache(maxsize=1)
def _english_source_values() -> dict[str, tuple[str, str]]:
    values = {}
    for relative, record in english_translation_lock()["source_files"].items():
        data = _english_archive(record["snapshot_path"], record["sha256"])
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if blob != record["blob"] or not data.startswith(b"\xef\xbb\xbfl_english:"):
            raise ValueError(f"English immutable Git blob/header drift: {relative}")
        entries = english_entries(data)
        if values.keys() & entries.keys():
            raise ValueError(f"English source key collision: {relative}")
        values.update(entries)
    if len(values) != 2971:
        raise ValueError("English source key inventory drift")
    return values


@lru_cache(maxsize=None)
def english_translation_payload(relative: str) -> bytes:
    lock = english_translation_lock()
    record = lock["runtime_text"][relative]
    previous = _english_archive(record["previous_snapshot_path"], record["previous_output_sha256"])
    sources = _english_source_values()
    def translate(row: re.Match) -> str:
        key, version = row[2], row[3]
        if key in lock["adapted_values"]:
            value = lock["adapted_values"][key]
        else:
            source_version, value = sources[key]
            if source_version != version:
                raise ValueError(f"English key version drift: {relative}/{key}")
        #20261020_kpopmodder: Drop the one inherited trailing space on this translated line so the new diff passes whitespace checks.
        suffix = re.sub(r'[ \t]+(?=\r?$)', '', row[5]) if key == "KOR_anti_air_equipment_2" else row[5]
        return row[1] + value + suffix
    output = ENGLISH_ROW.sub(translate, previous.decode("utf-8-sig")).encode("utf-8-sig")
    if sha256(output) != record["output_sha256"]:
        raise ValueError(f"English translation output drift: {relative}")
    #20261107_kpopmodder: Translate inherited comments after verifying the original English output.
    comments = english_comment_translation_lock().get(relative, {})
    for original, translated in comments.get("translations", {}).items():
        if any(not line.lstrip().startswith("#") or "\n" in line or "\r" in line
               for line in (original, translated)):
            raise ValueError(f"English comment translation must stay commented out: {relative}")
        pattern = rb"(?m)^" + re.escape(original.encode("utf-8")) + rb"(?=\r?$)"
        output, count = re.subn(pattern, lambda _: translated.encode("utf-8"), output)
        if count != 1:
            raise ValueError(f"English comment translation expected one source line: {relative}")
    if comments and sha256(output) != comments["output_sha256"]:
        raise ValueError(f"English comment output drift: {relative}")
    return output


def apply_english_translation(relative: str, data: bytes) -> bytes:
    relative = Path(relative).as_posix()
    record = english_translation_lock()["runtime_text"].get(relative)
    if record is None:
        return data
    comments = english_comment_translation_lock().get(relative, {})
    if sha256(data) not in (record["previous_output_sha256"], record["output_sha256"],
                            comments.get("output_sha256")):
        raise ValueError(f"unreviewed pre-English localisation output: {relative}")
    return english_translation_payload(relative)


def remove_english_translation(relative: str, data: bytes) -> bytes:
    """Recover a byte-exact historical contract only after checking the final translation."""
    relative = Path(relative).as_posix()
    #20261107_kpopmodder: Verify only the new split layer before enforcing the unchanged English translation bytes.
    data = _historical_runtime(relative, data)
    record = english_translation_lock()["runtime_text"].get(relative)
    if record is None:
        return data
    if data != english_translation_payload(relative):
        raise ValueError(f"English localisation differs from reviewed translation: {relative}")
    return _english_archive(record["previous_snapshot_path"], record["previous_output_sha256"])


def verify_english_translation() -> None:
    from collections import Counter
    lock = english_translation_lock()
    source = _english_source_values()
    expected_paths = set(lock["runtime_text"])
    paths = {p.relative_to(REPO_ROOT).as_posix() for p in (REPO_ROOT / "localisation/english").rglob("*.yml")}
    additions = {p: r for p, r in shipbuilding_update_lock()["runtime_text"].items() if p.startswith("localisation/english/")}
    #20261031_kpopmodder: Extend English only by the reviewed new feature files, retaining every earlier translation contract.
    feature_english = {p: r for p, r in feature_update_lock()["runtime_text"].items() if p.startswith("localisation/english/")}
    prospecting_locales = {p.as_posix(): data for p, data in prospecting_additions().items() if p.suffix == ".yml"}
    prospecting_english = {p for p in prospecting_locales if p.startswith("localisation/english/")}
    #20261107_kpopmodder: Admit exactly one new English state-name file; retain every older file/key contract.
    from korean_state_split_content import additions as state_split_additions
    split_locales = state_split_additions()
    split_english = {"localisation/english/HOK_KOR_state_split_l_english.yml"}
    if set(split_locales) != split_english | {"localisation/korean/HOK_KOR_state_split_l_korean.yml"}:
        raise ValueError("state-split localisation pair allowlist changed")
    #20261108_kpopmodder: Admit only locked new English files; the separate content gate checks their actual bilingual contracts.
    from upstream_content_update import addition_paths as content_addition_paths, build_outputs as content_outputs
    content_english = {p for p in content_addition_paths('focus') if p.startswith('localisation/english/')}
    #20261110_kpopmodder: Admit one exact equipment override file without changing the historical translation inventory or source pins.
    from korean_equipment_localisation import build_outputs as equipment_outputs
    equipment_english = {p: data for p, data in equipment_outputs().items() if p.startswith('localisation/english/')}
    if set(equipment_english) != {'localisation/english/replace/zz_HOK_KOR_equipment_overrides_l_english.yml'}:
        raise ValueError('equipment override English file allowlist changed')
    if paths != expected_paths | additions.keys() | feature_english.keys() | prospecting_english | split_english | content_english | equipment_english.keys():
        raise ValueError("English output file inventory differs from the reviewed translation layers")
    for relative, expected in equipment_english.items():
        if (REPO_ROOT / relative).read_bytes() != expected:
            raise ValueError(f'equipment override English output drift: {relative}')
    for relative in content_english:
        if (REPO_ROOT/relative).read_bytes() != content_outputs()[relative]:
            raise ValueError(f'new CNDP English output drift: {relative}')
    hangul = re.compile(r"[\u1100-\u11ff\u302e-\u302f\u3130-\u318f\ua960-\ua97f\uac00-\ud7ff\uffa0-\uffdc]")
    for relative in sorted(paths):
        if hangul.search((REPO_ROOT / relative).read_text(encoding="utf-8-sig")):
            raise ValueError(f"Hangul remains in English localisation: {relative}")
    keys, changed, added = set(), set(lock["changed_common_keys"]), set(lock["port_only_keys"])
    if len(changed) != 25 or len(added) != 27 or changed & added or changed | added != lock["adapted_values"].keys():
        raise ValueError("English RT56-specific translation allowlist drift")
    for relative, record in lock["runtime_text"].items():
        #20261107_kpopmodder: Preserve historical translation and Korean-source hashes under exact split reversal.
        actual = _historical_runtime(relative, (REPO_ROOT / relative).read_bytes())
        remove_english_translation(relative, actual)
        korean_path = relative.replace("/english/", "/korean/").replace("_l_english.yml", "_l_korean.yml")
        korean = _historical_runtime(korean_path, (REPO_ROOT / korean_path).read_bytes())
        if sha256(korean) != lock["preserved_korean"][korean_path]:
            raise ValueError(f"English import changed its Korean source: {korean_path}")
        previous = _english_archive(record["previous_snapshot_path"], record["previous_output_sha256"])
        english_rows, korean_rows = english_entries(actual), english_entries(korean)
        if list(english_rows) != list(english_entries(previous)) or english_rows.keys() != korean_rows.keys():
            raise ValueError(f"English import changed keys/order: {relative}")
        if len(english_rows) != record["key_count"] or keys & english_rows.keys():
            raise ValueError(f"English output key count/collision: {relative}")
        keys.update(english_rows)
        for key, (version, value) in english_rows.items():
            kr_version, kr_value = korean_rows[key]
            if version != kr_version or Counter(ENGLISH_TOKENS.findall(value)) != Counter(ENGLISH_TOKENS.findall(kr_value)):
                raise ValueError(f"English protected token/version drift: {relative}/{key}")
            if value.count(r"\n") != kr_value.count(r"\n") or re.search(r"[\uac00-\ud7a3]", value):
                raise ValueError(f"English newline/untranslated Korean: {relative}/{key}")
    if (len(keys), len(keys & source.keys()), len(keys - source.keys()), len(source.keys() - keys)) != (2743, 2716, 27, 255):
        raise ValueError("English target/reuse/exclusion key inventory drift")
    if keys - source.keys() != added or source.keys() - keys != set(lock["excluded_source_keys"]):
        raise ValueError("English target contains an unreviewed source-only or missing port key")
    extra_keys = set()
    for relative in additions:
        data = (REPO_ROOT / relative).read_bytes()
        if data != shipbuilding_addition(relative):
            raise ValueError(f"shipbuilding English output drift: {relative}")
        korean_path = relative.replace("/english/", "/korean/").replace("_l_english.yml", "_l_korean.yml")
        korean = (REPO_ROOT / korean_path).read_bytes()
        if korean != shipbuilding_addition(korean_path):
            raise ValueError("shipbuilding Korean source drift")
        en_rows, ko_rows = english_entries(data), english_entries(korean)
        if en_rows.keys() != ko_rows.keys() or keys & en_rows.keys():
            raise ValueError("shipbuilding bilingual/new-English key collision")
        for key, (version, value) in en_rows.items():
            kr_version, kr_value = ko_rows[key]
            if (version != kr_version or Counter(ENGLISH_TOKENS.findall(value)) != Counter(ENGLISH_TOKENS.findall(kr_value))
                    or value.count(r"\n") != kr_value.count(r"\n") or re.search(r"[\uac00-\ud7a3]", value)):
                raise ValueError(f"shipbuilding English protected text drift: {key}")
        extra_keys.update(en_rows)
    if len(extra_keys) != 4:
        raise ValueError("shipbuilding English must add exactly four keys")
    print("PASS English translation: 37 files, 2747 keys; historical 2691 reused, 25 adapted, 27 port-only, 255 excluded; four shipbuilding strings translated")
    #20261107_kpopmodder: Check the prospecting locale pair under the same new-key and protected-token rules as the DLC features.
    new_keys = set()
    new_english_paths = (*feature_english, *sorted(prospecting_english))
    for relative in new_english_paths:
        korean_path = relative.replace("/english/", "/korean/").replace("_l_english.yml", "_l_korean.yml")
        if relative in prospecting_english:
            expected_english, expected_korean = prospecting_locales[relative], prospecting_locales[korean_path]
        else:
            expected_english, expected_korean = feature_addition(relative), feature_addition(korean_path)
        #20261107_kpopmodder: Restore only a hash-verified final split layer before enforcing the original feature/prospecting locale bytes.
        data = _historical_runtime(relative, (REPO_ROOT / relative).read_bytes())
        if data != expected_english:
            raise ValueError(f"new Korean English output drift: {relative}")
        korean = _historical_runtime(korean_path, (REPO_ROOT / korean_path).read_bytes())
        if korean != expected_korean:
            raise ValueError(f"new Korean Korean output drift: {korean_path}")
        en_rows, ko_rows = english_entries(data), english_entries(korean)
        if en_rows.keys() != ko_rows.keys() or (keys | extra_keys | new_keys) & en_rows.keys():
            raise ValueError(f"new Korean bilingual key collision: {relative}")
        for key, (version, value) in en_rows.items():
            kr_version, kr_value = ko_rows[key]
            if (version != kr_version or Counter(ENGLISH_TOKENS.findall(value)) != Counter(ENGLISH_TOKENS.findall(kr_value))
                    or value.count(r"\n") != kr_value.count(r"\n") or re.search(r"[\uac00-\ud7a3]", value)):
                raise ValueError(f"new Korean English protected text drift: {key}")
        new_keys.update(en_rows)
    print(f"PASS Korean feature and prospecting English: {len(new_english_paths)} files, {len(new_keys)} additional translated keys")
    #20261107_kpopmodder: Check the separately scoped new names without changing the historical key totals.
    for relative in split_english:
        korean_path = relative.replace("/english/", "/korean/").replace("_l_english.yml", "_l_korean.yml")
        data, korean = (REPO_ROOT / relative).read_bytes(), (REPO_ROOT / korean_path).read_bytes()
        if data != split_locales[relative] or korean != split_locales[korean_path]:
            raise ValueError("state-split bilingual state-name output drift")
        en_rows, ko_rows = english_entries(data), english_entries(korean)
        if len(en_rows) != 12 or en_rows.keys() != ko_rows.keys() or (keys | extra_keys | new_keys) & en_rows.keys():
            raise ValueError("state-split state-name key count or collision")
        if any(not key.startswith("HOK_KOR_STATE_") for key in en_rows):
            raise ValueError("state-split introduced a shared foreign-state localisation key")
    print("PASS Korean state-split English: one separate English file, twelve stable HOK-specific names; historical inventories preserved")
    #20261107_kpopmodder: Check the actual port-only successor-name substitutions as well as the unchanged historical feature contract.
    from korean_state_split import compat_before as split_compat_before
    from korean_state_split_content import port_localisation_outputs
    research_locales = port_localisation_outputs(split_compat_before)
    for relative, expected in research_locales.items():
        if (REPO_ROOT / relative).read_bytes() != expected:
            raise ValueError(f"state-split research-location locale drift: {relative}")
    print("PASS Korean research-location tooltips: two locale files; naval South Gyeongsang and nuclear South Hamgyeong; historical feature bytes preserved")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--english-check", action="store_true", help="check the pinned English import without rebuilding historical sources")
    parser.add_argument("--import-icons", action="store_true", help="materialize the reviewed artwork bytes without changing donor files")
    parser.add_argument("--import-second-wave", action="store_true", help="materialize only the reviewed second-wave Git inputs in a separate cache")
    parser.add_argument("--export-second-wave-docs", action="store_true", help="preserve the selected upstream specifications, icon manifests and credits byte-for-byte")
    parser.add_argument("--export-policy-docs", action="store_true", help="export the seven reviewed September 23 policy documents")
    args = parser.parse_args()
    if args.english_check:
        verify_english_translation()
        return 0
    changed = ensure_source_snapshot(check_only=args.check)
    print(f"HOK source snapshot: 1014 base + 20 selected overlay = 1031 files; created {changed}")
    icon_changes = ensure_icon_snapshot(check_only=not args.import_icons or args.check)
    print(f"HOK artwork snapshot: 92 assets + 4 reference inputs + documentation; created {icon_changes}")
    second_wave_changes = ensure_second_wave_snapshot(check_only=not args.import_second_wave or args.check)
    print(f"HOK second-wave snapshot: 58 runtime text + 231 DDS + 37 source documents; created {second_wave_changes}")
    if args.export_second_wave_docs or args.check or SECOND_WAVE_DOCUMENTATION_ROOT.exists():
        exported = export_second_wave_documents(check_only=not args.export_second_wave_docs or args.check)
        print(f"HOK second-wave upstream documents: 37 preserved; created {exported}")
    policy_documents = export_policy_documents(check_only=not args.export_policy_docs or args.check)
    print(f"HOK policy delta: 10 runtime inputs + 7 source documents verified; exported {policy_documents}")
    for relative in localisation_update_lock()["runtime_text"]:
        read_localisation_source(relative)
    print("HOK localisation update: 28 immutable Git inputs verified")
    #20261003_kpopmodder: Validate the complete frozen update independently of the donor's future changes.
    lock = material_cycle_lock()
    for group in ("runtime_text", "runtime_assets", "documentation"):
        for relative in lock[group]:
            read_material_cycle_source(relative)
    print("HOK material-cycle snapshot: 6 runtime text + 3 DDS + 11 source documents/assets verified")
    #20261003_kpopmodder: Verify all frozen prose bytes even after the live donor changes.
    verify_prose_snapshot()
    print("HOK prose snapshot: 28 runtime localisation + 2 source documents verified")
    focus_tooltip_update_lock()
    print("HOK focus decision-tooltip: immutable two-line source delta verified")
    prerequisite_update_lock()
    print("HOK focus prerequisites: six immutable source edits + seven source documents verified")
    civic_update_lock()
    print("HOK civic update: 23 runtime text + 8 DDS + 23 source documents/assets verified")
    verify_shipbuilding_snapshot()
    verify_feature_snapshot()
    verify_democratic_layout_snapshot()
    verify_prospecting_snapshot()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
