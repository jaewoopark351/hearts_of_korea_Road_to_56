#!/usr/bin/env python3
"""Independently inspect the four-file RT56 manifest196 host adaptation.

Only the recorded source/AST contracts are checked. This tool never calls the
host-update generator, changes files, launches HOI4, or proves runtime behavior.
The old manifest755 locks remain historical inputs beneath this final layer.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import re

from check_upstream_content import Entry, Inspector, RT56_ROOT, children, one, parse, scalar, select, walk


#20261108_kpopmodder: Check current host preservation independently of the four rebase transformations.
ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT = "docs/upstream/rt56-host-update-20261108"
LOCK = "tools/rt56_host_update_lock.json"
PREVIOUS_MANIFEST = "7553774178744855191"
CURRENT_MANIFEST = "1963361040482473746"
BOOKMARK = "common/bookmarks/the_gathering_storm.txt"
MIO = "common/military_industrial_organization/organizations/00_generic_organization.txt"
SEA = "common/on_actions/14_sea_on_actions.txt"
JAP = "history/countries/JAP - Japan.txt"
KOREAN_MIO = "common/military_industrial_organization/organizations/KOR_organization.txt"
CIVIC = "events/HOK_KOR_civic_events.txt"
PATHS = {BOOKMARK, MIO, SEA, JAP}
KOREAN_STATES = {525, 527, 917, 918, 919, 920, 1144, 1145, 1146, 1148, 1149, 1150, 1151, 1152, 1153}
# The inherited resistance-DM selector deliberately excludes Gyeonggi525.
SEA_STATES = KOREAN_STATES - {525}
HOST_KOREAN_HISTORY = {525, 527, 917, 918, 919, 920}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest().upper()


def replace_entry(nodes: tuple[Entry, ...], original: Entry, replacement: Entry | None) -> tuple[Entry, ...]:
    result = []
    for node in nodes:
        if node == original:
            if replacement is not None:
                result.append(replacement)
        elif isinstance(node.value, tuple):
            result.append(Entry(node.key, node.op, replace_entry(node.value, original, replacement)))
        else:
            result.append(node)
    return tuple(result)


def resistance_selector(nodes: tuple[Entry, ...]) -> Entry:
    candidates = []
    for _, node in walk(nodes):
        if node.key != "every_state" or not isinstance(node.value, tuple):
            continue
        grants = select(node.value, "add_dynamic_modifier")
        if any(Entry("modifier", "=", "KOR_resistance_against_colonial_rule_dm") in children(grant) for grant in grants):
            candidates.append(one(children(one(node.value, "limit")), "OR"))
    if len(candidates) != 1:
        raise ValueError(f"expected one Korean resistance-DM selector, found {len(candidates)}")
    return candidates[0]


class HostInspector(Inspector):
    def __init__(self, root: Path, payloads: dict[str, bytes] | None = None):
        super().__init__(root, payloads)
        self.snapshot = root / SNAPSHOT
        self.config = json.loads((root / LOCK).read_text(encoding="utf-8"))

    def frozen(self, relative: str) -> bytes:
        path = (self.snapshot / relative).resolve()
        if not path.is_relative_to(self.snapshot.resolve()):
            raise ValueError("host adaptation snapshot path escaped its source capsule")
        return path.read_bytes()

    def host(self, relative: str) -> tuple[Entry, ...]:
        return parse(self.frozen(self.config["outputs"][relative]["host_snapshot"]))

    def before(self, relative: str) -> tuple[Entry, ...]:
        return parse(self.frozen(self.config["outputs"][relative]["previous_snapshot"]))

    def bookmark(self) -> None:
        original, current, previous = self.host(BOOKMARK), self.ast(BOOKMARK), self.before(BOOKMARK)
        host_bookmark = one(children(one(original, "bookmarks")), "bookmark")
        current_bookmark = one(children(one(current, "bookmarks")), "bookmark")
        previous_bookmark = one(children(one(previous, "bookmarks")), "bookmark")
        self.check("current host has no pre-existing Korean country card", not select(children(host_bookmark), "KOR"))
        card = one(children(current_bookmark), "KOR")
        self.check("one Korean card retains the complete previous HOK AST", card == one(children(previous_bookmark), "KOR"))
        self.check("all current host bookmark metadata and other country cards retained", replace_entry(current, card, None) == original)
        self.check("1936 bookmark date and default country retained", one(children(current_bookmark), "date") == one(children(host_bookmark), "date") and one(children(current_bookmark), "default_country") == one(children(host_bookmark), "default_country"))

    def mio(self) -> None:
        original, current = self.host(MIO), self.ast(MIO)
        host_tank, current_tank = one(original, "generic_tank_organization"), one(current, "generic_tank_organization")
        allowed = one(children(current_tank), "allowed")
        exclusion = parse("NOT = { tag = KOR }")[0]
        self.check("generic tank has exactly one dedicated Korean exclusion", children(allowed).count(exclusion) == 1)
        without_exclusion = Entry(allowed.key, allowed.op, tuple(n for n in children(allowed) if n != exclusion))
        normalized_tank = Entry(current_tank.key, current_tank.op, tuple(without_exclusion if n == allowed else n for n in children(current_tank)))
        self.check("all current host generic MIO definitions and traits retained", tuple(normalized_tank if n == current_tank else n for n in current) == original)
        self.check("generic tank non-allowed fields retained", tuple(n for n in children(current_tank) if n.key != "allowed") == tuple(n for n in children(host_tank) if n.key != "allowed"))
        feature_lock = json.loads((self.root / "tools/hok_feature_update_lock.json").read_text(encoding="utf-8"))
        korean_record = feature_lock["runtime_text"][KOREAN_MIO]
        self.check("dedicated Korean MIO file retains its historical feature output hash", sha(self.read(KOREAN_MIO)) == korean_record["output_sha256"])
        historical_korean_raw = (self.root / korean_record["output_snapshot_path"]).read_bytes()
        self.check("historical Korean MIO expectation matches its existing source pin", sha(historical_korean_raw) == korean_record["output_sha256"])
        historical_korean = parse(historical_korean_raw)
        korean = self.ast(KOREAN_MIO)
        self.check("fifteen dedicated Korean MIO IDs retained", len(korean) == len({n.key for n in korean}) == 15)
        for node in korean:
            self.check(f"dedicated Korean allowed contract retained: {node.key}", one(children(node), "allowed") == one(children(one(historical_korean, node.key)), "allowed"))

    def sea(self) -> None:
        original, current, previous = self.host(SEA), self.ast(SEA), self.before(SEA)
        host_selector, current_selector, old_selector = map(resistance_selector, (original, current, previous))
        old_ids = [int(scalar(n)) for _, n in walk(children(old_selector)) if n.key == "state"]
        current_ids = [int(scalar(n)) for _, n in walk(children(current_selector)) if n.key == "state"]
        self.check("inherited fourteen-state sea selector inventory is explicit", set(old_ids) == SEA_STATES and len(old_ids) == 14)
        self.check("sea Korean AST delta retained without adding capital525", current_selector == old_selector and set(current_ids) == SEA_STATES and len(current_ids) == 14)
        self.check("all current host sea callbacks, other countries and effect order retained", replace_entry(current, current_selector, host_selector) == original)
        self.check("only one Korean resistance-DM grant remains", sum(n.key == "modifier" and n.value == "KOR_resistance_against_colonial_rule_dm" for _, n in walk(current)) == 1)

    def japan(self) -> None:
        original, current, previous = self.host(JAP), self.ast(JAP), self.before(JAP)
        expected_body = parse("start_resistance = yes set_compliance = 15 set_resistance = 1 set_garrison_strength = 1.0")
        initial_korean = [n for n in original if n.key in {str(s) for s in HOST_KOREAN_HISTORY}]
        self.check("current host Korea history baseline: six identical initial resistance blocks", len(initial_korean) == 6 and all(children(n) == expected_body for n in initial_korean))
        dated = one(current, "1939.3.14")
        old_dated = one(previous, "1939.3.14")
        self.check("Japanese annexation-date Korean block retains the previous HOK AST", dated == old_dated)
        self.check("1939 annexation group contains fifteen unique Korean states", {n.key for n in children(dated)} == {str(s) for s in KOREAN_STATES} and len(children(dated)) == 15)
        for node in children(dated):
            self.check(f"dated Korean resistance values: {node.key}", children(node) == expected_body)
        self.check("independent1936 Korea receives no unconditional Japanese resistance initialisation", not any(n.key in {str(s) for s in KOREAN_STATES} for n in current))
        host_other = tuple(n for n in original if n not in initial_korean)
        port_other = tuple(n for n in current if n != dated)
        self.check("all other current Japanese history data and order retained", port_other == host_other)

    def logical_ids(self) -> None:
        registrations = []
        for relative, provider, raw in self.effective_sources("common/bookmarks"):
            for _, node in walk(parse(raw)):
                if node.key == "bookmark" and isinstance(node.value, tuple):
                    names = select(node.value, "name")
                    if names and scalar(names[0]) == "GATHERING_STORM_NAME":
                        registrations.append({"path": relative, "provider": provider, "korean_cards": len(select(node.value, "KOR"))})
        self.check("one effective Gathering Storm bookmark with one Korean card", len(registrations) == 1 and registrations[0]["korean_cards"] == 1, json.dumps(registrations))
        selected = {n.key for n in self.host(MIO)} | {n.key for n in self.ast(KOREAN_MIO)}
        occurrences = {key: [] for key in selected}
        for relative, provider, raw in self.effective_sources("common/military_industrial_organization/organizations"):
            for node in parse(raw):
                if node.key in occurrences and isinstance(node.value, tuple):
                    occurrences[node.key].append({"path": relative, "provider": provider})
        for key, definitions in sorted(occurrences.items()):
            self.check(f"one effective MIO registration: {key}", len(definitions) == 1, json.dumps(definitions))

    def source_contracts(self) -> None:
        config = self.config
        self.check("separately identified755-to196 host transition", config["format"] == 1 and config["previous_manifest"] == PREVIOUS_MANIFEST and config["workshop_manifest"] == CURRENT_MANIFEST)
        self.check("exact four-file final output inventory", set(config["outputs"]) == PATHS)
        for relative, record in config["files"].items():
            self.check(f"frozen host-adaptation input hash: {relative}", sha(self.frozen(relative)) == record["sha256"])
        for relative, record in config["outputs"].items():
            self.check(f"final current-host runtime hash: {relative}", sha(self.read(relative)) == record["sha256"])
            self.check(f"current host counterpart hash: {relative}", sha(self.frozen(record["host_snapshot"])) == record["host_sha256"])
            self.check(f"previous physical port output hash: {relative}", sha(self.frozen(record["previous_snapshot"])) == record["previous_sha256"])
        for key, count in (("preserved_content_hashes", 32), ("preserved_map_hashes", 24)):
            self.check(f"{key}: expected preservation inventory", len(config[key]) == count)
            for relative, expected in config[key].items():
                current = sha(self.read(relative))
                bridge = config.get("approved_runtime_revisions", {}).get(relative, {}) if key == "preserved_content_hashes" else {}
                self.check(f"{key}: {relative}", current == expected or
                           (relative == CIVIC and bridge.get("previous_sha256") == expected and bridge.get("sha256") == current))
        #20261109_kpopmodder: Independently bind the single later display repair without rewriting historical content pins.
        revisions = config.get("approved_runtime_revisions", {})
        self.check("host preservation has exactly one explicit civic recovery revision", set(revisions) == {CIVIC})
        bridge = revisions.get(CIVIC, {})
        source = json.loads((self.root / "tools/hok_upstream_content_lock.json").read_text(encoding="utf-8"))
        output = source["outputs"][CIVIC]
        self.check("civic revision exact current/previous pair and migration scope",
                   bridge.get("previous_sha256") == config["preserved_content_hashes"][CIVIC]
                   and bridge.get("sha256") == output["sha256"] == sha(self.read(CIVIC))
                   and bridge.get("event_ids") == source.get("civic_recovery_event_wrappers") == [3, 13]
                   and bridge.get("source_lock") == "tools/hok_upstream_content_lock.json"
                   and bridge.get("previous_sha256") in output.get("accepted_previous_outputs", []))
        previous_path = self.root / "docs/upstream/hok-content-update-20261108" / bridge.get("previous_snapshot", "MISSING")
        self.check("civic original output snapshot retains the old host-preservation pin",
                   sha(previous_path.read_bytes()) == config["preserved_content_hashes"][CIVIC])
        ledger_revisions = config.get("accepted_ledger_revisions", [])
        self.check("ledger bridge retains one explicitly reviewed predecessor pair",
                   len(ledger_revisions) == 1 and ledger_revisions[0].get("previous_sha256") == config["ledger_before_sha256"]
                   and ledger_revisions[0].get("runtime_path") == CIVIC)
        original_ledger = self.frozen("ledger_before.csv")
        lines = original_ledger.splitlines(keepends=True)
        reader = csv.DictReader(io.StringIO(original_ledger.decode("utf-8"), newline=""))
        fields = reader.fieldnames
        reader.fieldnames
        start, changed, chunks = reader.line_num, 0, [lines[0]]
        for row in reader:
            raw = b"".join(lines[start:reader.line_num])
            start = reader.line_num
            if row["output_path"] == CIVIC:
                self.check("original civic ledger output retains its exact old pin", row["output_sha256"] == bridge.get("previous_sha256"))
                row["output_sha256"] = bridge.get("sha256", "MISSING")
                stream = io.StringIO(newline="")
                csv.DictWriter(stream, fieldnames=fields, lineterminator="\n").writerow(row)
                raw = stream.getvalue().encode("utf-8")
                changed += 1
            chunks.append(raw)
        self.check("approved ledger revision changes only one civic output cell",
                   changed == 1 and len(ledger_revisions) == 1
                   and sha(b"".join(chunks)) == ledger_revisions[0].get("sha256"))
        for relative, expected in config.get("preserved_runtime_hashes", {}).items():
            self.check(f"preserved runtime hash: {relative}", sha(self.read(relative)) == expected)
        for relative in ("tools/hok_upstream_content_lock.json", "tools/hok_state_split_lock.json"):
            previous = json.loads((self.root / relative).read_text(encoding="utf-8"))
            self.check(f"historical host manifest pin retained: {relative}", previous["workshop_manifest"] == PREVIOUS_MANIFEST)
        self.check("legacy shared intermediates retain two bounded owners", set(config["legacy_shared_inputs"]) == {SEA, JAP})
        for relative, record in config["legacy_shared_inputs"].items():
            self.check(f"legacy shared snapshot hash: {relative}", sha(self.frozen(record["snapshot_path"])) == record["sha256"])

    def live_host(self) -> None:
        config = self.config
        inventory_raw = self.frozen(config["inventory_snapshot"])
        self.check("current-host inventory hash", sha(inventory_raw) == config["files"][config["inventory_snapshot"]]["sha256"])
        inventory = json.loads(inventory_raw)
        self.check("recorded current-host selection has4823 files", len(inventory) == 4823)
        for relative, record in inventory.items():
            path = RT56_ROOT / relative
            self.check(f"physical196 host selection: {relative}", path.is_file() and path.stat().st_size == record["size"] and sha(path.read_bytes()) == record["sha256"])
        self.check("historical eight removed paths retained as an explicit inventory", len(config["removed_paths"]) == 8)
        for relative in config["removed_paths"]:
            self.check(f"removed host path is not resurrected: {relative}", not (RT56_ROOT / relative).exists() and not (self.root / relative).exists() and relative.casefold() not in self._payload_keys)
        transition = json.loads(self.frozen("host-transition.json"))
        expected_bridges = {"RT56/" + row["path"]: {
            "previous_sha256": row["before"]["sha256"], "sha256": row["after"]["sha256"], "size": row["after"]["size"]}
            for row in transition["changed"]}
        self.check("legacy source bridges are exactly the184 audited changed hash pairs",
                   len(expected_bridges) == transition["changed_count"] == 184 and config["legacy_bridge"] == expected_bridges)
        for key, record in config["legacy_bridge"].items():
            provider, relative = key.split("/", 1)
            self.check(f"legacy source bridge matches physical196 input: {relative}", provider == "RT56" and record["previous_sha256"] != record["sha256"] and sha((RT56_ROOT / relative).read_bytes()) == record["sha256"])
        acf = (RT56_ROOT.parents[2] / "appworkshop_394360.acf").read_text(encoding="utf-8-sig")
        groups = re.findall(r'"820260968"\s*\{([^{}]+)\}', acf)
        manifests = [value for group in groups for value in re.findall(r'"(?:latest_)?manifest"\s*"(\d+)"', group)]
        self.check("installed and available host manifests remain196", len(manifests) >= 2 and all(value == CURRENT_MANIFEST for value in manifests))
        app = (RT56_ROOT.parents[3] / "appmanifest_394360.acf").read_text(encoding="utf-8-sig")
        self.check("recorded Steam build retained", re.search(r'"buildid"\s*"(\d+)"', app)[1] == config["steam_build"])


def inspect_payloads(payloads: dict[str, bytes] | None = None, *, root: Path = ROOT,
                     check_live_host: bool = True) -> list[dict]:
    """Inspect disk with optional in-memory relative-path overrides for fixtures."""
    inspector = HostInspector(Path(root), payloads)
    for label, function in (("Korean bookmark/current host preservation", inspector.bookmark),
                            ("generic and dedicated Korean MIO preservation", inspector.mio),
                            ("sea fourteen-state Korean delta", inspector.sea),
                            ("Japanese dated fifteen-state Korean delta", inspector.japan),
                            ("effective logical registration inventory", inspector.logical_ids),
                            ("host adaptation source contracts", inspector.source_contracts)):
        inspector.section(label, function)
    if check_live_host:
        inspector.section("physical current-host inventory", inspector.live_host)
    inspector.results.append({"status": "UNVERIFIED", "check": "current196 host runtime integration",
                              "detail": "Source/AST only; bookmark UI, MIO access, startup modifiers, dated history, effects and saves require separately recorded cold-run evidence."})
    return inspector.results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="read actual files and the physical target host; never write files")
    args = parser.parse_args()
    if not args.check:
        parser.error("--check is required")
    results = inspect_payloads()
    counts = Counter(row["status"] for row in results)
    for row in results:
        if row["status"] != "PASS":
            print(f"{row['status']} {row['check']}: {row['detail']}")
    print(f"Independent RT56 host source checks: {counts['PASS']} PASS / {counts['FAIL']} FAIL / {counts['UNVERIFIED']} runtime UNVERIFIED")
    print("The four source merges do not establish engine, UI, effect or save compatibility.")
    return int(bool(counts["FAIL"]))


if __name__ == "__main__":
    raise SystemExit(main())
