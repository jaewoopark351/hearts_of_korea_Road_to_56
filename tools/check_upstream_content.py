#!/usr/bin/env python3
"""Independently inspect the selected 2026-11-08 port's physical source bytes.

This is an ordered Clausewitz AST/source check. It does not run the game or
prove UI rendering, executed rewards, elapsed timers or save compatibility.
The generator and its transformation modules are deliberately not imported.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import struct
from typing import Callable, Iterator


#20261108_kpopmodder: Derive independent source expectations from the frozen allocation, prior port and host snapshots.
ROOT = Path(__file__).resolve().parent.parent
VANILLA_ROOT = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV")
RT56_ROOT = Path(r"C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968")
SNAPSHOT = "docs/upstream/hok-content-update-20261108"
DECISIONS = "common/decisions/KOR_decision.txt"
FOCUSES = "common/national_focus/korea.txt"
TRIGGERS = "common/scripted_triggers/HOK_KOR_cndp_triggers.txt"
COUNTRY = "HOK_KOR_cndp_state_projects_v1"
SUCCESS = "HOK_KOR_cndp_developed_v1"
FOCUS = "KOR_comprehensive_national_development_plan"
LEGACY = tuple("KOR_develop_" + r for r in (
    "jeolla", "gyeongsang", "chungcheong", "hwanghae", "pyeongan", "gangwon", "hamgyeong"))
STATE_MAP = {527: 527, 1028: 918, 1029: 1144, 1030: 920, 1031: 1145,
             1082: 919, 1083: 917, 1086: 1148, 1087: 1149, 1088: 1150,
             1089: 1151, 1090: 1152, 1091: 1153}
PROVINCE_MAP = dict(zip(range(13414, 13448), range(13535, 13569)))
_LEX = re.compile(r'#[^\r\n]*|"(?:\\.|[^"\\])*"|[{}]|[=!<>?]+|[^\s{}=!<>?#"\ufeff]+')
_ROWS = re.compile(r'^ ([A-Za-z0-9_.]+):0 "((?:\\.|[^"\\\r\n])*)"[ \t]*\r?$', re.M)


@dataclass(frozen=True)
class Entry:
    key: str | None
    op: str | None
    value: str | tuple["Entry", ...]


def parse(data: bytes | str) -> tuple[Entry, ...]:
    """Keep duplicate keys, anonymous list values, operators and effect order."""
    text = data.decode("utf-8-sig") if isinstance(data, bytes) else data.lstrip("\ufeff")
    tokens = []
    end = 0
    for match in _LEX.finditer(text):
        if text[end:match.start()].strip():
            raise ValueError("unrecognised Clausewitz source between tokens")
        end = match.end()
        if not match[0].startswith("#"):
            tokens.append(match[0])
    if text[end:].strip():
        raise ValueError("unrecognised Clausewitz source suffix")
    position = 0

    def block(nested: bool) -> tuple[Entry, ...]:
        nonlocal position
        result = []
        while position < len(tokens):
            key = tokens[position]
            position += 1
            if key == "}":
                if not nested:
                    raise ValueError("unexpected closing brace")
                return tuple(result)
            if key == "{":
                result.append(Entry(None, None, block(True)))
                continue
            if position < len(tokens) and tokens[position] in {"=", "<", ">", "<=", ">=", "!=", "?="}:
                op = tokens[position]
                position += 1
                if position == len(tokens):
                    raise ValueError("missing assignment value")
                value = tokens[position]
                position += 1
                if value == "}":
                    raise ValueError("closing brace used as assignment value")
                result.append(Entry(key, op, block(True) if value == "{" else value))
            else:
                result.append(Entry(None, None, key))
        if nested:
            raise ValueError("unclosed Clausewitz block")
        return tuple(result)

    return block(False)


def children(entry: Entry) -> tuple[Entry, ...]:
    if not isinstance(entry.value, tuple):
        raise ValueError(f"expected a block: {entry.key}")
    return entry.value


def select(nodes: tuple[Entry, ...], key: str) -> list[Entry]:
    return [n for n in nodes if n.key == key]


def one(nodes: tuple[Entry, ...], key: str) -> Entry:
    found = select(nodes, key)
    if len(found) != 1:
        raise ValueError(f"expected one {key}, found {len(found)}")
    return found[0]


def scalar(node: Entry) -> str:
    if not isinstance(node.value, str):
        raise ValueError(f"expected scalar: {node.key}")
    return node.value[1:-1] if node.value.startswith('"') else node.value


def walk(nodes: tuple[Entry, ...], path: tuple[str, ...] = ()) -> Iterator[tuple[tuple[str, ...], Entry]]:
    for node in nodes:
        yield path, node
        if isinstance(node.value, tuple):
            yield from walk(node.value, path + ((node.key or "[]"),))


def identified(nodes: tuple[Entry, ...], key: str) -> dict[str, Entry]:
    found = [n for path, n in walk(nodes) if n.key == key and isinstance(n.value, tuple)
             and (key != "country_event" or not path)
             and (key != "focus" or path in ((), ("focus_tree",)))]
    result = {scalar(one(children(n), "id")): n for n in found}
    if len(result) != len(found):
        raise ValueError(f"duplicate {key} IDs")
    return result


def rewrite(nodes: tuple[Entry, ...], operation: Callable[[Entry], Entry | None]) -> tuple[Entry, ...]:
    result = []
    for node in nodes:
        if isinstance(node.value, tuple):
            node = Entry(node.key, node.op, rewrite(node.value, operation))
        replacement = operation(node)
        if replacement is not None:
            result.append(replacement)
    return tuple(result)


def expand_expected(nodes: tuple[Entry, ...], keys: set[str], previous: set[int], additions: tuple[int, ...]) -> tuple[tuple[Entry, ...], int]:
    """Construct ordered regional expectations from the recorded previous set."""
    result, count = [], 0
    for node in nodes:
        if isinstance(node.value, tuple):
            body, nested_count = expand_expected(node.value, keys, previous, additions)
            node = Entry(node.key, node.op, body)
            count += nested_count
        result.append(node)
    for key in keys:
        indices = [i for i, n in enumerate(result) if n.key == key and isinstance(n.value, str) and scalar(n).isdecimal()]
        if indices and {int(scalar(result[i])) for i in indices} == previous and len(indices) == len(previous):
            position = indices[-1] + 1
            result[position:position] = [Entry(key, "=", str(value)) for value in additions]
            count += 1
    return tuple(result), count


def _rows(raw: bytes) -> dict[str, str]:
    matches = _ROWS.findall(raw.decode("utf-8-sig"))
    result = dict(matches)
    if len(result) != len(matches):
        raise ValueError("duplicate localisation keys")
    return result


class Inspector:
    def __init__(self, root: Path, payloads: dict[str, bytes] | None):
        self.root = root
        self.payloads = {relative.replace("\\", "/"): data for relative, data in (payloads or {}).items()}
        self._payload_keys = {relative.casefold(): relative for relative in self.payloads}
        self.snapshot = root / SNAPSHOT
        self.results: list[dict] = []

    def read(self, relative: str) -> bytes:
        key = self._payload_keys.get(relative.replace("\\", "/").casefold())
        raw = self.payloads[key] if key is not None else (self.root / relative).read_bytes()
        #20261109_kpopmodder: Independently prove exact review deltas before auditing unchanged historical contracts.
        from check_review_followup import historical_bytes as review_historical
        return review_historical(relative, raw)

    def effective_sources(self, directory: str) -> Iterator[tuple[str, str, bytes]]:
        """Inventory the recorded vanilla -> RT56 -> port relative-path shadow.

        Virtual payload files are part of the final port layer, including names
        absent from disk. This source model does not claim observed precedence
        for other mods, replacement paths or an unrecorded launcher playset.
        """
        effective: dict[str, tuple[str, str, Path | None]] = {}
        for provider, source_root in (("vanilla", VANILLA_ROOT), ("RT56", RT56_ROOT), ("port", self.root)):
            folder = source_root / directory
            if not folder.is_dir():
                raise ValueError(f"missing {provider} global registry directory: {directory}")
            for source in sorted(folder.rglob("*")):
                if source.is_file() and source.suffix.casefold() == ".txt":
                    relative = source.relative_to(source_root).as_posix()
                    effective[relative.casefold()] = (relative, provider, source)
        prefix = directory.casefold().rstrip("/") + "/"
        for relative in self.payloads:
            if relative.casefold().startswith(prefix) and relative.casefold().endswith(".txt"):
                effective[relative.casefold()] = (relative, "port payload", None)
        for relative, provider, source in sorted(effective.values()):
            yield relative, provider, self.read(relative) if source is None or provider == "port" else source.read_bytes()

    def ast(self, relative: str) -> tuple[Entry, ...]:
        return parse(self.read(relative))

    def before(self, relative: str) -> tuple[Entry, ...]:
        return parse((self.snapshot / "compat_before" / relative).read_bytes())

    def check(self, label: str, condition: bool, detail: str = "") -> None:
        self.results.append({"status": "PASS" if condition else "FAIL", "check": label, "detail": detail})

    def section(self, label: str, function: Callable[[], None]) -> None:
        try:
            function()
        except (ValueError, KeyError, OSError, UnicodeError, struct.error, StopIteration, IndexError) as error:
            self.check(label, False, str(error))

    def cndp(self) -> None:
        allocation = json.loads((self.snapshot / "documents/docs/data/HOK_KOREAN_CNDP_STATE_PROJECTS.json").read_text(encoding="utf-8-sig"))
        projects = allocation["projects"]
        self.check("allocation has thirteen unique project IDs", len(projects) == len({p["decision"] for p in projects}) == 13)
        category = children(one(self.ast(DECISIONS), "KOR_decision_CNDP_category"))
        triggers = self.ast(TRIGGERS)
        expected_ids = {p["decision"] for p in projects}
        self.check("exact CNDP project inventory", {n.key for n in category if (n.key or "").startswith("HOK_KOR_cndp_develop_")} == expected_ids)
        province_parent = {}
        for path in (self.root / "history/states").glob("*.txt"):
            state = children(one(self.ast(path.relative_to(self.root).as_posix()), "state"))
            state_id = int(scalar(one(state, "id")))
            for province in children(one(state, "provinces")):
                province_id = int(scalar(province))
                if province_id in province_parent:
                    raise ValueError(f"province assigned to two states: {province_id}")
                province_parent[province_id] = state_id
        for project in projects:
            region, identifier = project["region"], project["decision"]
            state = STATE_MAP[project["state"]]
            territory = f"HOK_KOR_cndp_{region}_territory_trigger"
            benefit = f"HOK_KOR_cndp_{region}_benefit_trigger"
            room = project["requires_effective_space"]
            availability = f"has_tech = construction3 num_of_civilian_factories_available_for_projects > {project['minimum_available_civilians'] - 1} {territory} = yes"
            cancellation = f"NOT = {{ {territory} = yes }}"
            completion_limit = f"{territory} = yes"
            if room:
                availability += f" custom_trigger_tooltip = {{ tooltip = HOK_KOR_cndp_meaningful_space {state} = {{ {benefit} = yes }} }}"
                cancellation += f" {state} = {{ NOT = {{ {benefit} = yes }} }}"
                completion_limit += f" {state} = {{ {benefit} = yes }}"
            reward = ""
            target = project["target_category"]
            if target:
                reward += f"if = {{ limit = {{ HOK_KOR_cndp_below_{target}_trigger = yes }} set_state_category = {target} }} "
            if project["extra_slots"]:
                reward += f"add_extra_state_shared_building_slots = {project['extra_slots']} "
            if project["coal"]:
                reward += f"add_resource = {{ type = coal amount = {project['coal']} }} "
            for donor_province in project["victory_points"]:
                province = PROVINCE_MAP.get(donor_province, donor_province)
                reward += f"add_victory_points = {{ province = {province} value = 1 }} "
                self.check(f"{identifier}: VP province {province} belongs to state {state}", province_parent.get(province) == state)
            reward += f"set_state_flag = {SUCCESS}"
            expected = parse(f"""{identifier} = {{
                icon = GFX_HOK_KOR_decision_cndp_{region} allowed = {{ tag = KOR }}
                visible = {{ has_country_flag = {COUNTRY} has_completed_focus = {FOCUS} {state} = {{ NOT = {{ has_state_flag = {SUCCESS} }} }} }}
                available = {{ {availability} }} highlight_states = {{ highlight_state_targets = {{ state = {state} }} }}
                fire_only_once = no cost = {project['political_power']} days_remove = {project['days']}
                modifier = {{ civilian_factory_use = {project['civilian_use']} }}
                cancel_trigger = {{ OR = {{ {cancellation} }} }} cancel_effect = {{ }}
                remove_effect = {{ if = {{ limit = {{ {completion_limit} }} {state} = {{ {reward} }} }} }}
            }}""")[0]
            actual = one(category, identifier)
            for field in ("allowed", "visible", "available", "highlight_states", "fire_only_once", "cost", "days_remove", "modifier", "cancel_trigger", "cancel_effect", "remove_effect"):
                self.check(f"{identifier}: {field} contract", one(children(actual), field) == one(children(expected), field))
            self.check(f"{identifier}: complete ordered definition", actual == expected)
            expected_territory = parse(f"""{territory} = {{ hidden_trigger = {{ has_country_flag = {COUNTRY} }} has_capitulated = no
                {state} = {{ is_owned_by = ROOT is_fully_controlled_by = ROOT NOT = {{ has_state_flag = {SUCCESS} }} }} }}""")[0]
            self.check(f"{identifier}: shared territory and single-completion gate", one(triggers, territory) == expected_territory)
            if room:
                body = "HOK_KOR_cndp_has_factory_expansion_room_trigger = yes"
                if target:
                    body += f" HOK_KOR_cndp_below_{target}_trigger = yes"
                self.check(f"{identifier}: demonstrable benefit gate", one(triggers, benefit) == parse(f"{benefit} = {{ {body} }}")[0])
        budgets = {"political_power": sum(p["political_power"] for p in projects),
                   "civilian_factory_days": sum(p["civilian_use"] * p["days"] for p in projects),
                   "explicit_extra_slots": sum(p["extra_slots"] for p in projects),
                   "coal": sum(p["coal"] for p in projects), "victory_points": sum(len(p["victory_points"]) for p in projects)}
        self.check("independent project budget", budgets == {k: allocation["budget"][k] for k in budgets})
        definition = next(line.split(";") for line in self.read("map/definition.csv").decode("utf-8-sig").splitlines() if line.startswith("13559;"))
        self.check("Haeju province13559 is coastal land in state917", province_parent.get(13559) == 917 and definition[4:6] == ["land", "true"])
        self._helpers(triggers)
        self._legacy_and_focuses(category, [p["decision"] for p in projects])
        self._artwork(projects)

    def _helpers(self, triggers: tuple[Entry, ...]) -> None:
        categories = ["wasteland", "enclave", "tiny_island", "pastoral", "small_island", "rural", "large_island", "town", "large_town", "city", "large_city"]
        for target in ("town", "large_town", "city", "large_city"):
            body = " ".join("has_state_category = " + c for c in categories[:categories.index(target)])
            key = "HOK_KOR_cndp_below_" + target + "_trigger"
            self.check(f"category {target}: no equal/higher category downgrade", one(triggers, key) == parse(f"{key} = {{ OR = {{ {body} }} }}")[0])
        pairs = []
        for building in ("arms_factory", "industrial_complex"):
            for size in range(20):
                pairs.append(f"AND = {{ free_building_slots = {{ building = {building} size > {size} include_locked = yes }} NOT = {{ free_building_slots = {{ building = {building} size > {size} include_locked = no }} }} }}")
        key = "HOK_KOR_cndp_has_factory_expansion_room_trigger"
        self.check("factory room predicate: forty matched locked/unlocked queries", one(triggers, key) == parse(f"{key} = {{ OR = {{ {' '.join(pairs)} }} }}")[0])

    def _legacy_and_focuses(self, category: tuple[Entry, ...], new_ids: list[str]) -> None:
        old_category = children(one(self.before(DECISIONS), "KOR_decision_CNDP_category"))
        guard = parse(f"NOT = {{ has_country_flag = {COUNTRY} }}")[0]
        for key in LEGACY:
            current = one(category, key)
            visible = children(one(children(current), "visible"))
            self.check(f"legacy {key}: one generation exclusion", visible.count(guard) == 1)
            normalized = rewrite((current,), lambda n: Entry(n.key, n.op, tuple(c for c in children(n) if c != guard)) if n.key == "visible" and isinstance(n.value, tuple) else n)
            self.check(f"legacy {key}: original post-split contract retained", normalized == (one(old_category, key),))
        old_focuses, current_focuses = identified(self.before(FOCUSES), "focus"), identified(self.ast(FOCUSES), "focus")
        self.check("474 focus IDs retained", len(old_focuses) == len(current_focuses) == 474 and old_focuses.keys() == current_focuses.keys())
        permitted = {FOCUS: {"completion_reward"}, "KOR_port_fortification": {"completion_reward"},
                     "KOR_fall_of_the_sun": {"available"}, "KOR_freedom_to_indochina": {"available"}}
        for key, old in old_focuses.items():
            current = current_focuses[key]
            ignored = permitted.get(key, set())
            original_fields = tuple(c for c in children(old) if c.key not in ignored)
            current_fields = tuple(c for c in children(current) if c.key not in ignored)
            self.check(f"focus protection {key}", current_fields == original_fields)
        focus_reward = children(one(children(current_focuses[FOCUS]), "completion_reward"))
        unlocks = " ".join("unlock_decision_tooltip = " + key for key in new_ids)
        legacy_unlocks = " ".join("unlock_decision_tooltip = " + key for key in LEGACY)
        expected = parse(f"if = {{ limit = {{ hidden_trigger = {{ has_country_flag = {COUNTRY} }} }} {unlocks} }} else = {{ {legacy_unlocks} }}")
        self.check("CNDP focus: exact generation-dependent 13/7 notices", focus_reward == expected)
        history = self.ast("history/countries/KOR - Korea.txt")
        marker = Entry("set_country_flag", "=", COUNTRY)
        self.check("new-game history contains one root generation marker", history.count(marker) == 1 and sum(n == marker for _, n in walk(history)) == 1)
        old_history = self.before("history/countries/KOR - Korea.txt")
        self.check("country history otherwise preserved", tuple(n for n in history if n != marker) == old_history)
        fort = current_focuses["KOR_port_fortification"]
        grants = [(path, n) for path, n in walk(children(fort)) if n.key == "add_building_construction"]
        targets = [(next((int(k) for k in reversed(path) if k.isdecimal()), None), int(scalar(one(children(n), "province"))), int(scalar(one(children(n), "level")))) for path, n in grants]
        self.check("Haeju coastal fort: state917/province13559 and six other three-level ports", len(targets) == 7 and (917, 13559, 3) in targets and all(level == 3 for _, _, level in targets) and not any(p == 13540 for _, p, _ in targets))
        def haeju(node: Entry) -> Entry:
            if node.key == "1144" and isinstance(node.value, tuple) and any(n.key == "province" and n.value == "13540" for _, n in walk(node.value)):
                return Entry("917", node.op, rewrite(node.value, lambda n: Entry(n.key, n.op, "13559") if n.key == "province" and n.value == "13540" else n))
            return node
        self.check("Haeju fort complete reward otherwise unchanged", (fort,) == rewrite((old_focuses["KOR_port_fortification"],), haeju))
        for identifier, command, old_states, extra in (
            ("KOR_fall_of_the_sun", "controls_state", {282, 528, 529, 530, 531, 532, 533, 534, 535, 536}, (1105, 1106, 1107)),
            ("KOR_freedom_to_indochina", "has_full_control_of_state", {670, 671, 286, 741}, (924, 925, 926, 927, 928)),
        ):
            expected, count = expand_expected((old_focuses[identifier],), {command}, old_states, extra)
            if identifier == "KOR_freedom_to_indochina":
                targets = (670, 671, 286, 741, 924, 925, 926, 927, 928)
                regional_conditions = " ".join(f"owns_state = {s} has_full_control_of_state = {s}" for s in targets)
                fri = parse(f"FRI = {{ is_subject_of = FRA {regional_conditions} }}")[0]
                vin = parse("VIN = { is_subject_of = FRA }")[0]
                def add_host_subject(node: Entry) -> Entry:
                    if node.key == "OR" and isinstance(node.value, tuple) and vin in node.value:
                        position = node.value.index(vin) + 1
                        return Entry(node.key, node.op, node.value[:position] + (fri,) + node.value[position:])
                    return node
                expected = rewrite(expected, add_host_subject)
            self.check(f"{identifier}: exact regional addition, other effects retained", count == 1 and expected == (current_focuses[identifier],))

    def _artwork(self, projects: list[dict]) -> None:
        gfx_path = "interface/HOK_KOR_cndp_icons.gfx"
        sprites = [n for _, n in walk(self.ast(gfx_path)) if n.key == "SpriteType"]
        names = [scalar(one(children(n), "name")) for n in sprites]
        self.check("thirteen dedicated unique CNDP sprites", len(names) == len(set(names)) == 13)
        all_gfx = {path.relative_to(self.root).as_posix() for path in (self.root / "interface").rglob("*.gfx")}
        all_gfx.update(relative for relative in self.payloads if relative.startswith("interface/") and relative.endswith(".gfx"))
        global_names = []
        for relative in all_gfx:
            raw = self.read(relative)
            if b"GFX_HOK_KOR_decision_cndp_" in raw:
                global_names.extend(scalar(n) for _, n in walk(parse(raw)) if n.key == "name" and isinstance(n.value, str) and scalar(n).startswith("GFX_HOK_KOR_decision_cndp_"))
        self.check("no CNDP sprite logical duplicates in production interfaces", Counter(global_names) == Counter(names))
        for project in projects:
            region = project["region"]
            name = "GFX_HOK_KOR_decision_cndp_" + region
            sprite = sprites[names.index(name)]
            relative = "gfx/interface/decisions/HOK_KOR/cndp/cndp_" + region + ".dds"
            self.check(f"{region}: dedicated texture path", scalar(one(children(sprite), "texturefile")) == relative)
            raw = self.read(relative)
            self.check(f"{region}: original donor DDS bytes", raw == (self.snapshot / "runtime" / relative).read_bytes())
            self.check(f"{region}: 32x32 BGRA32 DDS", len(raw) == 4224 and raw[:4] == b"DDS " and struct.unpack_from("<I", raw, 4)[0] == 124 and struct.unpack_from("<II", raw, 12) == (32, 32) and struct.unpack_from("<I", raw, 88)[0] == 32)

    def civic(self) -> None:
        paths = {"common/decisions/HOK_KOR_civic_decisions.txt": 18,
                 "common/scripted_triggers/HOK_KOR_civic_triggers.txt": 1,
                 "events/HOK_KOR_civic_events.txt": 10}
        lock_path = self.root / "tools/hok_upstream_content_lock.json"
        lock = json.loads(lock_path.read_text(encoding="utf-8")) if lock_path.exists() else {}
        recovery = lock.get("civic_recovery_event_wrappers", [])
        #20261109_kpopmodder: Require the two confirmed recovery repairs rather than accepting an optional migration declaration.
        self.check("recovery wrapper migration is exactly .3/.13", recovery == [3, 13])
        wrapper = parse("hidden_effect = { HOK_KOR_sync_civic_state = yes }")[0]
        for relative, expected_count in paths.items():
            nodes = self.ast(relative)
            metadata = [(n, one(children(n), "tooltip")) for _, n in walk(nodes) if n.key in {"check_variable", "add_to_variable"} and select(children(n), "tooltip")]
            self.check(f"{relative}: exact numeric metadata count", len(metadata) == expected_count)
            for command, tooltip in metadata:
                body = children(command)
                variable = scalar(one(body, "var")) if select(body, "var") else next(c.key for c in body if (c.key or "").startswith("HOK_KOR_"))
                if command.key == "add_to_variable":
                    suffix = "change"
                elif select(body, "compare"):
                    suffix = "at_least" if scalar(one(body, "compare")) == "greater_than_or_equals" else "INVALID"
                else:
                    op = next(c.op for c in body if c.key == variable)
                    suffix = {"<": "below", ">": "above"}.get(op, "INVALID")
                self.check(f"{relative}: {variable} metadata semantics", scalar(tooltip) == f"{variable}_{suffix}_tt")

            def strip(nodes: tuple[Entry, ...]) -> tuple[Entry, ...]:
                result = []
                for node in nodes:
                    if node == wrapper:
                        result.extend(children(node))
                    elif isinstance(node.value, tuple):
                        body = strip(node.value)
                        if node.key in {"check_variable", "add_to_variable"}:
                            body = tuple(c for c in body if c.key != "tooltip")
                        result.append(Entry(node.key, node.op, body))
                    else:
                        result.append(node)
                return tuple(result)
            self.check(f"{relative}: gameplay AST and order preserved", strip(nodes) == self.before(relative))
            if relative.startswith("events/"):
                events, previous = identified(nodes, "country_event"), identified(self.before(relative), "country_event")
                counts = {int(key.split(".")[-1]): sum(n == wrapper for _, n in walk(children(value))) for key, value in events.items()}
                expected = {1: 1, 2: 3, 11: 1, 12: 3, **{key: 1 for key in recovery}}
                self.check("civic sync wrappers: eight source calls plus explicit recovery migrations", {k: v for k, v in counts.items() if v} == expected)
                for key in (3, 13):
                    identifier = f"HOK_KOR_CIVIC.{key}"
                    self.check(f"recovery event .{key}: declared source state", events[identifier] == previous[identifier] if key not in recovery else strip((events[identifier],)) == (previous[identifier],), "unchanged" if key not in recovery else "display wrapper only; actual UI requires runtime evidence")
                    immediate = children(one(children(events[identifier]), "immediate"))
                    self.check(f"recovery event .{key}: only final immediate sync is hidden",
                               immediate[-1:] == (wrapper,) and sum(n == wrapper for _, n in walk(immediate)) == 1
                               and not any(n.key == "HOK_KOR_sync_civic_state" for n in immediate))
                record = lock["outputs"][relative]
                revision = next((item for item in record.get("revision_history", [])
                                 if item.get("status") == "ENGINE_CONFIRMED_RECOVERY_UI_OVERFLOW"), {})
                old_raw = (self.snapshot / revision.get("snapshot_path", "MISSING")).read_bytes()
                self.check("recovery original generated output is preserved by exact source hash",
                           hashlib.sha256(old_raw).hexdigest().upper() == revision.get("sha256")
                           and revision.get("sha256") in record.get("accepted_previous_outputs", []))

                def flatten_hidden(items: tuple[Entry, ...]) -> tuple[Entry, ...]:
                    result = []
                    for item in items:
                        if item == wrapper:
                            result.extend(children(item))
                        elif isinstance(item.value, tuple):
                            result.append(Entry(item.key, item.op, flatten_hidden(item.value)))
                        else:
                            result.append(item)
                    return tuple(result)
                self.check("recovery revision retains every ordered effect, option, cost and metadata",
                           flatten_hidden(nodes) == flatten_hidden(parse(old_raw)))
        legacy = "common/decisions/HOK_KOR_democratic_expansion.txt"
        self.check("L08 allied industry decision file unchanged", self.ast(legacy) == self.before(legacy))
        self.results.append({"status": "UNVERIFIED", "check": "civic actual tooltip rendering, colour, option access, selected effects and 365-day expiry", "detail": "This checker inspects source only; use separately recorded runtime evidence."})

    def locales(self) -> None:
        prefixes = ("HOK_KOR_civic_state", "HOK_KOR_cndp_state_development", "HOK_KOR_democratic_expansion")
        tokens = lambda value: re.findall(r"\$[^$]+\$|\[\?[^]]+\]|§.|\\n", value)
        civic_keys = {"HOK_KOR_chaebol_influence", "HOK_KOR_civic_influence", "HOK_KOR_institutional_capture", "HOK_KOR_procurement_corruption", "HOK_KOR_prosecutor_defence_prepared"}
        for variable, suffixes in (("HOK_KOR_chaebol_influence", ("below", "above", "at_least")), ("HOK_KOR_civic_influence", ("below", "above", "at_least", "change")), ("HOK_KOR_institutional_capture", ("below", "change")), ("HOK_KOR_procurement_corruption", ("change",))):
            civic_keys.update(variable + "_" + suffix + "_tt" for suffix in suffixes)
        for prefix in prefixes:
            languages = {}
            for locale in ("english", "korean"):
                relative = f"localisation/{locale}/{prefix}_l_{locale}.yml"
                raw = self.read(relative)
                self.check(f"{relative}: BOM and established header", raw.startswith(b"\xef\xbb\xbf") and raw.decode("utf-8-sig").splitlines()[0] == f"l_{locale}:")
                rows = _rows(raw)
                languages[locale] = rows
                if locale == "english":
                    self.check(f"{relative}: English prose", not re.search(r"[\uac00-\ud7a3]", raw.decode("utf-8-sig")))
                if prefix == "HOK_KOR_civic_state":
                    old = _rows((self.snapshot / "compat_before" / relative).read_bytes())
                    self.check(f"{relative}: fifteen additions and retained earlier prose", set(rows) - set(old) == civic_keys and all(rows[k] == v for k, v in old.items()))
                elif prefix == "HOK_KOR_cndp_state_development":
                    allocation = json.loads((self.snapshot / "documents/docs/data/HOK_KOREAN_CNDP_STATE_PROJECTS.json").read_text(encoding="utf-8-sig"))
                    required_keys = {"HOK_KOR_cndp_project_rules", "HOK_KOR_cndp_meaningful_space", SUCCESS}
                    required_keys.update(p["decision"] + suffix for p in allocation["projects"] for suffix in ("", "_desc"))
                    self.check(f"{relative}: 29 exact project/rule/status keys", set(rows) == required_keys and sum("$HOK_KOR_cndp_project_rules$" in v for v in rows.values()) == 13)
                    expected_rule = "Cancelled projects can be restarted, but Political Power is not refunded. Completion rewards are granted once per state." if locale == "english" else "취소 시 정치력은 반환되지 않으며 재착수할 수 있습니다. 완료 보상은 주마다 한 번만 지급됩니다."
                    self.check(f"{relative}: no refund, restart and once-per-state guidance", rows["HOK_KOR_cndp_project_rules"] == expected_rule)
                else:
                    old = _rows((self.snapshot / "compat_before" / relative).read_bytes())
                    changed = {k for k in old if rows.get(k) != old[k]}
                    self.check(f"{relative}: education description only", set(old) == set(rows) and changed == {"HOK_KOR_technical_civic_schools_desc"})
            required = civic_keys if prefix == "HOK_KOR_civic_state" else set(languages["english"]) if prefix == "HOK_KOR_cndp_state_development" else {"HOK_KOR_technical_civic_schools_desc"}
            self.check(f"{prefix}: paired required keys", required <= languages["english"].keys() and required <= languages["korean"].keys())
            for key in sorted(required):
                self.check(f"paired localisation tokens: {key}", tokens(languages["english"][key]) == tokens(languages["korean"][key]))
        en = _rows(self.read("localisation/english/HOK_KOR_civic_state_l_english.yml"))
        self.check("beneficial civic growth uses positive colour format", en["HOK_KOR_civic_influence_change_tt"].endswith("$RIGHT|+=0$"))
        self.check("capture and corruption growth use harmful colour format", all(en[f"{v}_change_tt"].endswith("$RIGHT|-=0$") for v in ("HOK_KOR_institutional_capture", "HOK_KOR_procurement_corruption")))
        school = "HOK_KOR_technical_civic_schools_desc"
        english_school = _rows(self.read("localisation/english/HOK_KOR_democratic_expansion_l_english.yml"))[school]
        phrases = ("ownership and full control of Gyeonggi, both Jeolla states and both Chungcheong states",
                   "Gyeonggi, North Jeolla and South Chungcheong need building space",
                   "each gains two building slots and two civilian factories", "one 25% electronics research bonus")
        self.check("English civic school meaning: whole-region gates and three conserved recipients", all(phrase in english_school for phrase in phrases))
        korean_path = "localisation/korean/HOK_KOR_democratic_expansion_l_korean.yml"
        self.check("Korean civic school meaning matches reviewed donor clarification", _rows(self.read(korean_path))[school] == _rows((self.snapshot / "runtime" / korean_path).read_bytes())[school])

    def host(self) -> None:
        soviet = "common/scripted_effects/SOV_scripted_effects.txt"
        original = parse((self.snapshot / "host/rt56" / soviet).read_bytes())
        source_effect = one(original, "SOV_start_civil_war")
        endpoints = [n for _, n in walk(children(source_effect)) if n.key in {"attacker", "defender"} and n.value == "918"]
        self.check("host baseline has four inherited Korean endpoints", len(endpoints) == 4)
        expected_effect = Entry(source_effect.key, source_effect.op, rewrite(children(source_effect), lambda n: Entry(n.key, n.op, "1152") if n.key in {"attacker", "defender"} and n.value == "918" else n))
        expected = tuple(expected_effect if n == source_effect else n for n in original)
        self.check("entire RT56 Soviet database preserved except four Korean endpoints", self.ast(soviet) == expected)
        endpoint_pairs = [children(n) for _, n in walk(children(one(self.ast(soviet), "SOV_start_civil_war"))) if n.key == "has_border_war_between"]
        pairs = {(scalar(one(n, "attacker")), scalar(one(n, "defender"))) for n in endpoint_pairs}
        self.check("Soviet Korean border cleanup covers both 1152/408 directions", {("1152", "408"), ("408", "1152")} <= pairs)
        constants = "common/script_constants/state_groups.txt"
        original_constants = parse((self.snapshot / "host/vanilla" / constants).read_bytes())
        def border(node: Entry) -> Entry:
            if node.key == "comintern_starting_border":
                return Entry(node.key, node.op, tuple(Entry(None, None, "1152") if n == Entry(None, None, "1028") else n for n in children(node)))
            return node
        self.check("entire state-group host database preserved except Korean border entry", self.ast(constants) == rewrite(original_constants, border))
        self.check("no duplicate donor-only Soviet overlay introduced", not (self.root / "common/scripted_effects/00_HOK_KOR_state_reference_effects.txt").exists() and "common/scripted_effects/00_HOK_KOR_state_reference_effects.txt" not in self.payloads)
        self.check("excluded Mongolian module remains absent", not (self.root / "common/on_actions/mongppong_on_actions.txt").exists() and "common/on_actions/mongppong_on_actions.txt" not in self.payloads)
        china = "common/national_focus/china_shared_TSR.txt"
        self.check("Chinese general host content remains unchanged", self.ast(china) == self.before(china))
        japan = "common/national_focus/japan.txt"
        before, current = identified(self.before(japan), "focus"), identified(self.ast(japan), "focus")
        self.check("Japanese host focus inventory retained", current.keys() == before.keys())
        target = "JAP_prepare_for_peninsular_warfare"
        self.check("Japanese non-Korean focuses unchanged", all(current[key] == value for key, value in before.items() if key != target))
        before_fields = tuple(n for n in children(before[target]) if n.key != "completion_reward")
        current_fields = tuple(n for n in children(current[target]) if n.key != "completion_reward")
        self.check("Japanese Korean focus protected fields retained", before_fields == current_fields)
        added = parse("""IF = { limit = { 917 = { state_is_fully_controlled_by_ROOT_subject_or_faction_member = yes } }
            917 = { add_building_construction = { type = bunker level = 3 province = { id = 1003 } instant_build = yes } } }""")[0]
        self.check("Japanese Haeju fort uses its own actual-control guard", sum(n == added for _, n in walk((current[target],))) == 1)
        def restore_japanese_fort(node: Entry) -> Entry | None:
            if node == added:
                return None
            if node.key == "province" and node.value == (Entry("id", "=", "4052"),):
                return Entry(node.key, node.op, (Entry("id", "=", "4052"), Entry("id", "=", "1003")))
            return node
        self.check("Japanese Korean fort split otherwise retains full host definition", rewrite((current[target],), restore_japanese_fort) == (before[target],))
        kch = "history/countries/KCH - Korean China.txt"
        old = self.before(kch)
        expected_kch = tuple(Entry(n.key, n.op, "1114") if n.key == "capital" else n for n in old)
        self.check("KCH capital-only correction to RT56 Nanjing1114", self.ast(kch) == expected_kch)
        self._regions()
        self._diplomacy()

    def _regions(self) -> None:
        decisions = self.ast(DECISIONS)
        regions = {
            "KOR_liberation_of_indochina": {671, 670, 741, 286, 924, 925, 926, 927, 928},
            "KOR_liberation_of_philippine": {623, 327, 625, 624, 627, 626, 628, 1108, 1109, 1110},
            "KOR_liberation_of_indonesia": {672, 334, 335, 673, 667, 668, 669, 446, 738, 909, 974, 975, 976, 977, 978, 1126, 1127, 1128, 1135, 1137, 1142, 1143},
            "KOR_liberation_of_maleisia": {336, 333, 914, 915, 916, 951, 960, 1014, 1129, 1130, 1131},
            "KOR_liberation_of_pamanyungan": {522, 520, 519, 521, 285, 517, 518, 674, 870, 871, 872, 873},
            "KOR_liberation_of_aotearoa": {723, 284, 1136, 1139, 1140},
        }
        for key, expected in regions.items():
            block = next(n for _, n in walk(decisions) if n.key == key)
            groups = []
            for _, parent in walk((block,)):
                if isinstance(parent.value, tuple):
                    for command in ("controls_state", "set_state_controller", "transfer_state"):
                        values = [int(scalar(c)) for c in select(parent.value, command) if isinstance(c.value, str) and scalar(c).isdecimal()]
                        if values:
                            groups.append(values)
            self.check(f"{key}: four complete ordinary/civil-war/control paths", len(groups) == 4 and all(set(group) == expected and len(group) == len(expected) for group in groups))
            prior_block = next(n for _, n in walk(self.before(DECISIONS)) if n.key == key)
            prior_groups = [set(int(scalar(c)) for c in select(parent.value, "controls_state")) for _, parent in walk((prior_block,)) if isinstance(parent.value, tuple) and select(parent.value, "controls_state")]
            prior = prior_groups[0]
            additions = tuple(sorted(expected - prior))
            normalized, count = expand_expected((prior_block,), {"controls_state", "set_state_controller", "transfer_state"}, prior, additions)
            # Source insertion order is a provenance detail; explicitly compare
            # each resulting list in order elsewhere and keep non-list AST here.
            def erase_new(node: Entry) -> Entry | None:
                if node.key in {"controls_state", "set_state_controller", "transfer_state"} and isinstance(node.value, str) and scalar(node).isdecimal() and int(scalar(node)) in additions:
                    return None
                return node
            self.check(f"{key}: other branch effects retained", count == 4 and rewrite((block,), erase_new) == (prior_block,))

    def _diplomacy(self) -> None:
        relative = "events/korea.txt"
        before, current = identified(self.before(relative), "country_event"), identified(self.ast(relative), "country_event")
        self.check("Korean event inventory unchanged", current.keys() == before.keys())
        #20261108_kpopmodder: Reject the observed option-scope parser regression independently of territory-list correctness.
        invalid_options = [
            {"event": identifier, "option": scalar(one(children(option), "name")), "unsupported_key": "available"}
            for identifier, event in current.items()
            for option in select(children(event), "option")
            if select(children(option), "available")
        ]
        self.check("event option schema: no unsupported available key", not invalid_options,
                   json.dumps(invalid_options, ensure_ascii=False))
        self.check("unrelated Korean events retain full AST", all(current[key] == value for key, value in before.items() if key not in {"kor_events.62", "kor_events.63"}))
        targets = (670, 671, 286, 741, 924, 925, 926, 927, 928)
        holders = []
        for holder in ("FRA", "VIN", "FRI"):
            conditions = "is_subject_of = FRA " if holder != "FRA" else ""
            conditions += " ".join(f"owns_state = {s} has_full_control_of_state = {s}" for s in targets)
            holders.append(f"{holder} = {{ {conditions} }}")
        guard = parse("OR = { " + " ".join(holders) + " }")[0]
        old_event = before["kor_events.62"]
        old_option = next(n for n in children(old_event) if n.key == "option" and scalar(one(children(n), "name")) == "kor_events.62.a")
        expanded, count = expand_expected(children(old_option), {"transfer_state"}, {670, 671, 286, 741}, (924, 925, 926, 927, 928))
        def add_vietnam_cores(node: Entry) -> Entry:
            if node.key == "VIN" and isinstance(node.value, tuple):
                anchor = parse("741 = { add_core_of = VIN }")[0]
                if anchor not in node.value:
                    raise ValueError("Indochina acceptance missing original Laos core anchor")
                at = node.value.index(anchor) + 1
                additions = parse(" ".join(f"{s} = {{ add_core_of = VIN }}" for s in (924, 925, 926)))
                return Entry(node.key, node.op, node.value[:at] + additions + node.value[at:])
            return node
        expanded = rewrite(expanded, add_vietnam_cores)
        indices = [i for i, n in enumerate(expanded) if n.key in {"VIN", "KOR"}]
        begin, end = indices[0], indices[-1] + 1
        expected_option = Entry("option", "=", expanded[:begin] + (
            Entry("trigger", "=", (guard,)),
            Entry("if", "=", (Entry("limit", "=", (guard,)),) + expanded[begin:end]),
        ) + expanded[end:])
        expected_event = Entry(old_event.key, old_event.op, tuple(expected_option if n == old_option else n for n in children(old_event)))
        self.check("Indochina acceptance: exact guarded nine-state transfer and retained effects", count == 1 and current["kor_events.62"] == expected_event)
        singapore = parse("if = { limit = { 336 = { is_owned_by = ENG is_core_of = MAL is_fully_controlled_by = ENG } } transfer_state = 336 }")[0]
        def malaya(node: Entry) -> Entry:
            if node.key == "MAL" and isinstance(node.value, tuple):
                indices = [i for i, n in enumerate(node.value) if n.key == "set_cosmetic_tag"]
                if len(indices) != 1:
                    raise ValueError("Malaya acceptance cosmetic anchor is not unique")
                at = indices[0]
                return Entry(node.key, node.op, node.value[:at] + (singapore,) + node.value[at:])
            return node
        self.check("Malaya acceptance: guarded British Singapore only, other effects retained", (current["kor_events.63"],) == rewrite((before["kor_events.63"],), malaya))

    def integrity(self) -> None:
        lock = json.loads((self.root / "tools/hok_upstream_content_lock.json").read_text(encoding="utf-8"))
        digest = lambda raw: hashlib.sha256(raw).hexdigest().upper()
        for relative, record in lock["inputs"].items():
            self.check(f"frozen prior port hash: {relative}", digest((self.snapshot / record["snapshot_path"]).read_bytes()) == record["sha256"])
        for category in ("preserved_map_hashes", "preserved_runtime_hashes"):
            for relative, expected in lock.get(category, {}).items():
                self.check(f"{category}: {relative}", digest(self.read(relative)) == expected)
        self.check("new output scope leaves map, state history and host caps intact", not any(relative.startswith(("map/", "history/states/", "common/defines/", "common/state_category/", "common/buildings/")) for relative in lock["outputs"]))

    def global_registrations(self) -> None:
        #20261108_kpopmodder: Count logical definitions across all effective filenames, including virtual fixture additions.
        for directory, identifier, expected_parent in (
            ("common/scripted_effects", "SOV_start_civil_war", ()),
            ("common/script_constants", "comintern_starting_border", ("state_groups",)),
        ):
            registrations = []
            files = 0
            for relative, provider, raw in self.effective_sources(directory):
                files += 1
                if identifier.encode("ascii") not in raw:
                    continue
                registrations.extend({"path": relative, "provider": provider}
                                     for path, node in walk(parse(raw))
                                     if path == expected_parent and node.key == identifier and isinstance(node.value, tuple))
            self.check(f"effective global registration: {identifier}", len(registrations) == 1,
                       json.dumps({"effective_files": files, "definitions": registrations}, ensure_ascii=False))
        short = "common/script_constants/zzzz_HOK_KOR_state_reference_constants.txt"
        self.check("short donor-only state-group overlay remains absent",
                   not (self.root / short).exists() and short.casefold() not in self._payload_keys)


def inspect_payloads(payloads: dict[str, bytes] | None = None, *, root: Path = ROOT) -> list[dict]:
    """Inspect physical files with optional relative-path byte overrides for fixtures."""
    inspector = Inspector(Path(root), payloads)
    for label, function in (("CNDP source contracts", inspector.cndp), ("civic display source contracts", inspector.civic),
                            ("localisation source contracts", inspector.locales), ("foreign host preservation", inspector.host),
                            ("frozen source and preserved map hashes", inspector.integrity),
                            ("effective global registration inventory", inspector.global_registrations)):
        inspector.section(label, function)
    return inspector.results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="inspect actual runtime files; never write outputs")
    args = parser.parse_args()
    if not args.check:
        parser.error("--check is required; this tool never builds or repairs files")
    results = inspect_payloads()
    counts = Counter(r["status"] for r in results)
    for result in results:
        if result["status"] != "PASS":
            print(f"{result['status']} {result['check']}: {result['detail']}")
    print(f"Independent upstream source checks: {counts['PASS']} PASS / {counts['FAIL']} FAIL / {counts['UNVERIFIED']} runtime UNVERIFIED")
    print("Static source inspection only; UI, executed effects, elapsed periods and saves require separate evidence.")
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
