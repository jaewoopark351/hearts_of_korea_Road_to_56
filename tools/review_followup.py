#!/usr/bin/env python3
"""Reproduce the exact civic-display and inland-marker follow-up revision."""
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

#20261109_kpopmodder: Keep the four reviewed repairs reversible above unchanged content, split and host contracts.
ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / 'tools/hok_review_followup_lock.json'
SNAPSHOT = ROOT / 'docs/upstream/hok-review-followup-20261109'
PATHS = frozenset((
    'common/scripted_effects/HOK_KOR_civic_effects.txt',
    'localisation/english/HOK_KOR_civic_state_l_english.yml',
    'localisation/korean/HOK_KOR_civic_state_l_korean.yml',
    'map/buildings.txt',
))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


#20261109_kpopmodder: Treat Windows case aliases as the same protected relative output in every entry point.
def canonical_name(relative: str | Path) -> str:
    name = str(relative).replace('\\', '/')
    return next((path for path in PATHS if path.casefold() == name.casefold()), name)


@lru_cache(maxsize=1)
def lock() -> dict:
    result = json.loads(LOCK_PATH.read_text(encoding='utf-8'))
    if (result.get('format') != 1 or result.get('revision') != '2026-11-09-review-followup-v1'
            or result.get('base_commit') != 'f8fdd821cf80dd291b02a59b55e8d85fe558a9b3'
            or set(result.get('outputs', {})) != PATHS):
        raise ValueError('unreviewed follow-up revision or output inventory')
    return result


def previous_bytes(relative: str) -> bytes:
    record = lock()['outputs'][relative]
    path = (SNAPSHOT / record['previous_snapshot']).resolve()
    path.relative_to(SNAPSHOT.resolve())
    if record['previous_snapshot'] != 'before/' + relative:
        raise ValueError('follow-up ancestor path drift')
    data = path.read_bytes()
    if sha(data) != record['previous_sha256']:
        raise ValueError(f'follow-up frozen ancestor drift: {relative}')
    return data


def verify_inputs() -> None:
    for relative in PATHS:
        previous_bytes(relative)
    config = lock()
    host = Path(config['rt56_root'])
    acf = (host.parents[2] / 'appworkshop_394360.acf').read_text(encoding='utf-8-sig')
    entries = re.findall(r'"820260968"\s*\{([^{}]+)\}', acf)
    manifests = [m for entry in entries for m in re.findall(r'"(?:latest_)?manifest"\s*"(\d+)"', entry)]
    if len(manifests) < 2 or any(value != config['workshop_manifest'] for value in manifests):
        raise ValueError('follow-up RT56 installed/latest manifest drift')
    game = json.loads((Path(config['vanilla_root']) / 'launcher-settings.json').read_text(encoding='utf-8-sig'))
    if game['version'] != config['game_version']:
        raise ValueError('follow-up installed game-version drift')


@lru_cache(maxsize=1)
def build_outputs() -> dict[str, bytes]:
    from review_followup_content import apply_civic_numeric
    from review_followup_map import apply_map
    verify_inputs()
    result = {}
    for relative, record in lock()['outputs'].items():
        before = previous_bytes(relative)
        after = apply_map(relative, apply_civic_numeric(relative, before))
        if sha(after) != record['sha256']:
            raise ValueError(f'unreviewed follow-up generated output: {relative}')
        result[relative] = after
    return result


def historical_bytes(relative: str | Path, data: bytes) -> bytes:
    """Reverse only the registered final bytes; unrelated/unknown bytes stay raw."""
    #20261112_kpopmodder: Prove the Korean recruitment portraits and name exclusions before checking their historical inputs.
    from upstream_scientists import historical_bytes as scientist_historical
    data = scientist_historical(relative, data)
    #20261112_kpopmodder: Prove the city-news revision before checking unchanged historical output contracts.
    from upstream_capture_news import historical_bytes as capture_historical
    data = capture_historical(relative, data)
    #20261110_kpopmodder: Preserve old descriptor pins only after proving the exact dependency-edge output.
    from korean_equipment_localisation import descriptor_historical_bytes
    data = descriptor_historical_bytes(relative, data)
    #20261110_kpopmodder: Prove and reverse the later industry revision before checking unchanged repair ancestry.
    from upstream_industry_update import historical_bytes as industry_historical
    data = industry_historical(relative, data)
    #20261109_kpopmodder: Prove the later English terminology revision before enforcing this unchanged repair contract.
    from english_terminology import historical_bytes as terminology_historical
    data = terminology_historical(relative, data)
    name = canonical_name(relative)
    if not LOCK_PATH.is_file() or name not in PATHS:
        return data
    record = lock()['outputs'][name]
    if sha(data) == record['sha256']:
        if data != build_outputs()[name]:
            raise ValueError(f'follow-up final-output proof failed: {name}')
        return previous_bytes(name)
    return data


def finalize_one(relative: str | Path, data: bytes) -> bytes:
    #20261112_kpopmodder: Keep the reviewed Korean recruitment portraits and name exclusions terminal for inherited writers.
    from upstream_scientists import finalize_one as scientist_finalize, historical_bytes as scientist_historical
    data = scientist_historical(relative, data)
    #20261112_kpopmodder: Keep the reviewed city-news triggers after every inherited output owner.
    from upstream_capture_news import finalize_one as capture_finalize
    #20261110_kpopmodder: Retain the exact terminal industry revision across every inherited output owner.
    from upstream_industry_update import finalize_one as industry_finalize, historical_bytes as industry_historical
    data = industry_historical(relative, data)
    #20261109_kpopmodder: Keep the independent English terminology revision terminal for every existing output owner.
    from english_terminology import finalize_one as terminology_finalize, historical_bytes as terminology_historical
    data = terminology_historical(relative, data)
    name = canonical_name(relative)
    if not LOCK_PATH.is_file() or name not in PATHS:
        return scientist_finalize(relative, capture_finalize(relative, industry_finalize(relative, terminology_finalize(relative, data))))
    record = lock()['outputs'][name]
    if sha(data) not in (record['previous_sha256'], record['sha256']):
        raise ValueError(f'unreviewed follow-up predecessor: {name}')
    return scientist_finalize(relative, capture_finalize(relative, industry_finalize(relative, terminology_finalize(relative, build_outputs()[name]))))


def finalize_outputs(outputs: dict) -> dict:
    return {relative: finalize_one(relative, data) for relative, data in outputs.items()}


def preflight_outputs(outputs: dict) -> None:
    #20261112_kpopmodder: Reject independent edits to the reviewed recruitment portraits and name outputs before inherited writes.
    from upstream_scientists import preflight_outputs as scientist_preflight
    scientist_preflight(outputs)
    #20261112_kpopmodder: Refuse independent news edits before an older writer can replace them.
    from upstream_capture_news import preflight_outputs as capture_preflight
    capture_preflight(outputs)
    #20261110_kpopmodder: Refuse unregistered industry payloads or independent runtime edits before any older writer runs.
    from upstream_industry_update import preflight_outputs as industry_preflight
    industry_preflight(outputs)
    from english_terminology import preflight_outputs as terminology_preflight, historical_bytes as terminology_historical
    terminology_preflight(outputs)
    root = ROOT.resolve()
    seen = set()
    for relative, data in outputs.items():
        path = (root / relative).resolve()
        name = canonical_name(path.relative_to(root))
        if path in seen:
            raise ValueError(f'duplicate follow-up output: {name}')
        seen.add(path)
        record = lock()['outputs'].get(name)
        if not record:
            continue
        if terminology_historical(name, data) != build_outputs()[name]:
            raise ValueError(f'unreviewed proposed follow-up bytes: {name}')
        if not path.is_file() or sha(terminology_historical(name, path.read_bytes())) not in (record['previous_sha256'], record['sha256']):
            raise ValueError(f'independently changed follow-up runtime: {name}')


def ledger_bytes(previous: bytes) -> bytes:
    """Change exactly four output cells/reasons; retain inherited attribution."""
    from english_terminology import historical_bytes as terminology_historical
    lines = previous.splitlines(keepends=True)
    reader = csv.DictReader(io.StringIO(previous.decode('utf-8'), newline=''))
    fields = reader.fieldnames
    reader.fieldnames
    start = reader.line_num
    chunks = [lines[0]]
    touched = set()
    for row in reader:
        raw = b''.join(lines[start:reader.line_num])
        start = reader.line_num
        name = row['output_path']
        record = lock()['outputs'].get(name)
        if not record:
            chunks.append(raw)
            continue
        if name in touched or row['integration_class'] != record['classification']:
            raise ValueError(f'follow-up ledger ownership drift: {name}')
        touched.add(name)
        reason = ('; 2026-11-09 bounded review follow-up: tools/hok_review_followup_lock.json; '
                  f'previous_output_sha256={record["previous_sha256"]}; '
                  'civic numeric display or one inland floating-harbor marker; original authorship retained')
        #20261109_kpopmodder: An idempotent ledger call must still reject independently changed runtime bytes.
        if sha(terminology_historical(name, (ROOT / name).read_bytes())) != record['sha256']:
            raise ValueError(f'follow-up ledger runtime differs: {name}')
        if row['output_sha256'] == record['sha256'] and row['reason'].endswith(reason):
            chunks.append(raw)
            continue
        if row['output_sha256'] != record['previous_sha256']:
            raise ValueError(f'follow-up ledger predecessor hash drift: {name}')
        row['output_sha256'] = record['sha256']
        row['reason'] += reason
        stream = io.StringIO(newline='')
        csv.DictWriter(stream, fieldnames=fields, lineterminator='\n').writerow(row)
        chunks.append(stream.getvalue().encode('utf-8'))
    if touched != PATHS:
        raise ValueError('follow-up ledger missing reviewed outputs')
    return b''.join(chunks)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        #20261109_kpopmodder: This older CLI must preserve the separately reviewed terminal English output.
        outputs = finalize_outputs(build_outputs())
        preflight_outputs(outputs)
        pending = [(ROOT / name, data) for name, data in outputs.items() if (ROOT / name).read_bytes() != data]
        if pending and not args.apply:
            raise ValueError('follow-up runtime mismatches: ' + ', '.join(p.relative_to(ROOT).as_posix() for p, _ in pending))
        for path, data in pending:
            path.write_bytes(data)
        print(f'PASS review follow-up: {len(outputs)} exact registered outputs; {len(pending)} written; source/host pins retained')
        return 0
    except (ValueError, KeyError, FileNotFoundError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
