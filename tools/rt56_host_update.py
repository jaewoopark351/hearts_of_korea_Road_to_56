#!/usr/bin/env python3
"""Reproduce the explicitly reviewed RT56 November host transition.

Older layer locks remain historical contracts. Only exact registered physical
inputs and intermediate/final bytes may cross this separately pinned layer.
"""
from __future__ import annotations

import argparse
import csv
from functools import lru_cache
import hashlib
import io
import json
from pathlib import Path
import re
import sys

#20261108_kpopmodder: Keep the Steam host update separate from the HOK content update.
ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / 'tools/rt56_host_update_lock.json'
SNAPSHOT = ROOT / 'docs/upstream/rt56-host-update-20261108'
RT56 = Path(r'C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968')
BOOKMARK = 'common/bookmarks/the_gathering_storm.txt'
MIO = 'common/military_industrial_organization/organizations/00_generic_organization.txt'
SEA = 'common/on_actions/14_sea_on_actions.txt'
JAP = 'history/countries/JAP - Japan.txt'
PATHS = frozenset((BOOKMARK, MIO, SEA, JAP))
CIVIC = 'events/HOK_KOR_civic_events.txt'


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


@lru_cache(maxsize=1)
def lock() -> dict:
    data = json.loads(LOCK_PATH.read_text(encoding='utf-8'))
    if (data['format'] != 1 or data['previous_manifest'] != '7553774178744855191'
            or data['workshop_manifest'] != '1963361040482473746'):
        raise ValueError('unreviewed RT56 host transition')
    return data


def frozen(relative: str) -> bytes:
    path = (SNAPSHOT / relative).resolve()
    path.relative_to(SNAPSHOT.resolve())
    data = path.read_bytes()
    if sha(data) != lock()['files'][relative]['sha256']:
        raise ValueError(f'host transition frozen input drift: {relative}')
    return data


def current_manifests() -> list[str]:
    acf = (RT56.parents[2] / 'appworkshop_394360.acf').read_text(encoding='utf-8-sig')
    entries = re.findall(r'"820260968"\s*\{([^{}]+)\}', acf)
    return [m for entry in entries for m in re.findall(r'"(?:latest_)?manifest"\s*"(\d+)"', entry)]


def verify_manifest() -> None:
    entries = current_manifests()
    if len(entries) < 2 or any(m != lock()['workshop_manifest'] for m in entries):
        raise ValueError('RT56 transition installed/latest manifest drift')


def approved_manifest_transition(previous: str, actual: list[str]) -> bool:
    if not LOCK_PATH.is_file():
        return False
    return (previous == lock()['previous_manifest'] and len(actual) >= 2
            and all(m == lock()['workshop_manifest'] for m in actual))


def approved_input_transition(provider: str, relative: str, previous: str, actual: str) -> bool:
    if not LOCK_PATH.is_file():
        return False
    record = lock()['legacy_bridge'].get(provider.upper() + '/' + relative)
    if not record or record['previous_sha256'] != previous or record['sha256'] != actual:
        return False
    verify_manifest()
    return True


def approved_runtime_revision(relative: str, previous: str, actual: str) -> bool:
    """Accept only the reviewed recovery display revision over its old host-preservation pin."""
    #20261109_kpopmodder: Preserve the original32 hashes and bridge only the two recovery wrappers explicitly approved later.
    revisions = lock().get('approved_runtime_revisions', {})
    if set(revisions) != {CIVIC} or relative != CIVIC:
        return False
    record = revisions[CIVIC]
    if (record.get('previous_sha256') != previous or record.get('sha256') != actual
            or record.get('event_ids') != [3, 13]
            or record.get('source_lock') != 'tools/hok_upstream_content_lock.json'):
        return False
    source = json.loads((ROOT / record['source_lock']).read_text(encoding='utf-8'))
    output = source['outputs'][relative]
    revisions = [item for item in output.get('revision_history', [])
                 if item.get('sha256') == previous and item.get('snapshot_path') == record.get('previous_snapshot')]
    return (source.get('civic_recovery_event_wrappers') == [3, 13]
            and output['sha256'] == actual and previous in output.get('accepted_previous_outputs', [])
            and len(revisions) == 1
            and sha((ROOT / 'docs/upstream/hok-content-update-20261108' / record['previous_snapshot']).read_bytes()) == previous)


def legacy_shared_inputs() -> dict[str, bytes]:
    if not LOCK_PATH.is_file():
        return {}
    verify_manifest()
    records = lock()['legacy_shared_inputs']
    if set(records) != {SEA, JAP}:
        raise ValueError('historical shared input allowlist drift')
    return {name: frozen(record['snapshot_path']) for name, record in records.items()}


def historical_generator_input(relative: str | Path, data: bytes) -> bytes:
    """Reverse only a registered current-host nine-state intermediate."""
    if not LOCK_PATH.is_file():
        return data
    name = Path(relative).as_posix()
    record = lock()['outputs'].get(name)
    if record and record.get('intermediate_sha256') == sha(data):
        return frozen(lock()['legacy_shared_inputs'][name]['snapshot_path'])
    return data


def historical_bytes(relative: str | Path, data: bytes) -> bytes:
    if not LOCK_PATH.is_file():
        return data
    record = lock()['outputs'].get(Path(relative).as_posix())
    if record and sha(data) == record['sha256']:
        return frozen(record['previous_snapshot'])
    return data


def bookmark_output(host: bytes, before: bytes) -> bytes:
    from build_shared_overrides import find_indented_block
    text, previous = host.decode('utf-8-sig'), before.decode('utf-8-sig')
    start, end = find_indented_block(previous, 'KOR')
    korean = previous[start:end]
    if 'history = "KOR_GATHERING_STORM_DESC"' not in korean:
        raise ValueError('previous Korean bookmark identity drift')
    if re.search(r'(?m)^\s*KOR\s*=\s*\{', text):
        raise ValueError('new host already owns a Korean bookmark')
    newline = '\r\n' if '\r\n' in text else '\n'
    korean = korean.replace('\r\n', '\n').replace('\n', newline)
    anchor = '\t\tCAN = {' + newline
    if text.count(anchor) != 1:
        raise ValueError('new host bookmark insertion anchor drift')
    return text.replace(anchor, korean + newline * 2 + anchor, 1).encode('utf-8')


def mio_output(host: bytes) -> bytes:
    from build_shared_overrides import block_spans
    text = host.decode('utf-8-sig')
    newline = '\r\n' if '\r\n' in text else '\n'
    spans = block_spans(text, 'generic_tank_organization', top_level=True)
    if len(spans) != 1:
        raise ValueError('new host tank MIO inventory drift')
    start, end = spans[0]
    block = text[start:end]
    anchor = '\tallowed = {' + newline
    if block.count(anchor) != 1 or 'tag = KOR' in block:
        raise ValueError('new host tank MIO Korean ownership changed')
    addition = '\t\tNOT = { tag = KOR } # HOK provides dedicated tank MIOs' + newline
    return (text[:start] + block.replace(anchor, anchor + addition, 1) + text[end:]).encode('utf-8')


def preview_outputs() -> dict[str, bytes]:
    from korean_state_split_shared import rebase_updated_host
    from korean_state_split import OLD_STATES, NEW_STATES
    result = {}
    for name, record in lock()['outputs'].items():
        host = frozen(record['host_snapshot'])
        if name == BOOKMARK:
            result[name] = bookmark_output(host, frozen(record['previous_snapshot']))
        elif name == MIO:
            result[name] = mio_output(host)
        else:
            result[name] = rebase_updated_host(name, host, OLD_STATES | NEW_STATES)
    return result


@lru_cache(maxsize=1)
def build_outputs() -> dict[str, bytes]:
    if set(lock()['outputs']) != PATHS:
        raise ValueError('host transition output allowlist drift')
    result = preview_outputs()
    for name, data in result.items():
        if sha(data) != lock()['outputs'][name]['sha256']:
            raise ValueError(f'host transition generated output drift: {name}')
    return result


def finalize_one(relative: str | Path, data: bytes) -> bytes:
    if not LOCK_PATH.is_file():
        return data
    name = Path(relative).as_posix()
    record = lock()['outputs'].get(name)
    if not record:
        return data
    if sha(data) not in {record['previous_sha256'], record['sha256']}:
        raise ValueError(f'unreviewed preceding host output: {name}')
    return build_outputs()[name]


def preflight_outputs(outputs: dict) -> None:
    if not LOCK_PATH.is_file():
        return
    indexed = {name.casefold(): r for name, r in lock()['outputs'].items()}
    touched = False
    for name, data in outputs.items():
        path = (ROOT / name).resolve()
        relative = path.relative_to(ROOT.resolve()).as_posix()
        record = indexed.get(relative.casefold())
        if not record:
            continue
        touched = True
        if sha(data) != record['sha256']:
            raise ValueError(f'unreviewed proposed host output: {relative}')
        if not path.is_file() or sha(path.read_bytes()) not in {record['previous_sha256'], record['sha256']}:
            raise ValueError(f'independently edited host output: {relative}')
    if touched:
        verify_inputs()


def verify_inputs() -> None:
    verify_manifest()
    for relative in lock()['files']:
        frozen(relative)
    inventory = json.loads(frozen(lock()['inventory_snapshot']))
    for name, record in inventory.items():
        path = RT56 / name
        if not path.is_file() or sha(path.read_bytes()) != record['sha256']:
            raise ValueError(f'current RT56 host input drift: {name}')
    for name in lock()['removed_paths']:
        if (RT56 / name).exists():
            raise ValueError(f'removed RT56 input reappeared: {name}')
    for group in ('preserved_content_hashes', 'preserved_map_hashes', 'preserved_runtime_hashes'):
        for name, digest in lock()[group].items():
            actual = sha((ROOT / name).read_bytes())
            if actual != digest and not (group == 'preserved_content_hashes'
                                         and approved_runtime_revision(name, digest, actual)):
                raise ValueError(f'host adaptation changed protected runtime: {name}')


def ledger_bytes(previous: bytes) -> bytes:
    if not LOCK_PATH.is_file():
        return previous
    digest = sha(previous)
    accepted = lock().get('accepted_ledger_revisions', [])
    if digest != lock()['ledger_before_sha256'] and not any(
            row.get('sha256') == digest and row.get('previous_sha256') == lock()['ledger_before_sha256']
            and row.get('runtime_path') == CIVIC for row in accepted):
        raise ValueError('host transition predecessor ledger drift')
    lines = previous.splitlines(keepends=True)
    reader = csv.DictReader(io.StringIO(previous.decode('utf-8'), newline=''))
    fields = reader.fieldnames
    reader.fieldnames
    start = reader.line_num
    rows, raw = [], []
    for row in reader:
        rows.append(row)
        raw.append(b''.join(lines[start:reader.line_num]))
        start = reader.line_num
    #20261109_kpopmodder: Reverse the single approved output cell and require the complete old predecessor ledger hash.
    if digest != lock()['ledger_before_sha256']:
        bridge = lock()['approved_runtime_revisions'][CIVIC]
        proof, matches = [lines[0]], 0
        for row, original in zip(rows, raw):
            if row['output_path'] == CIVIC:
                if row['output_sha256'] != bridge['sha256']:
                    raise ValueError('civic ledger revision output differs')
                restored = dict(row, output_sha256=bridge['previous_sha256'])
                stream = io.StringIO(newline='')
                csv.DictWriter(stream, fieldnames=fields, lineterminator='\n').writerow(restored)
                proof.append(stream.getvalue().encode('utf-8'))
                matches += 1
            else:
                proof.append(original)
        if len(accepted) != 1 or matches != 1 or sha(b''.join(proof)) != lock()['ledger_before_sha256']:
            raise ValueError('civic ledger revision changes more than its approved output cell')
    originals = [dict(row) for row in rows]
    for name, record in lock()['outputs'].items():
        matches = [row for row in rows if row['output_path'] == name]
        if len(matches) != 1 or matches[0]['output_sha256'] != record['previous_sha256']:
            raise ValueError(f'host transition ledger ancestor drift: {name}')
        row = matches[0]
        row.update(output_sha256=record['sha256'], rt56_base_sha256=record['host_sha256'],
                   integration_class='THREE_WAY_MERGE', status='GENERATED', exact_path_rt56_collision='yes')
        row['reason'] += '; 2026-11-08 RT56 host transition 7553774178744855191 -> 1963361040482473746; tools/rt56_host_update_lock.json; prior_output=' + record['previous_sha256']
    chunks = [lines[0]]
    for old, new, source in zip(originals, rows, raw):
        if old == new:
            chunks.append(source)
        else:
            stream = io.StringIO(newline='')
            csv.DictWriter(stream, fieldnames=fields, lineterminator='\n').writerow(new)
            chunks.append(stream.getvalue().encode('utf-8'))
    return b''.join(chunks)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        verify_inputs()
        outputs = build_outputs()
        preflight_outputs(outputs)
        pending = [(ROOT / name, data) for name, data in outputs.items() if (ROOT / name).read_bytes() != data]
        if pending and args.check:
            raise ValueError('host transition runtime mismatch: ' + ', '.join(str(p.relative_to(ROOT)) for p, _ in pending))
        verify_inputs()
        for path, data in pending:
            path.write_bytes(data)
        print('PASS RT56 host transition: four pinned merges; Korean content32 and map24 retained')
        return 0
    except (ValueError, KeyError, OSError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
