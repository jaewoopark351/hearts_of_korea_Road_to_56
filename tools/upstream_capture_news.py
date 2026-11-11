#!/usr/bin/env python3
"""Reproduce three reviewed Korean city-capture news triggers on the RT56 map."""
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

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / 'docs/upstream/hok-capture-news-update-20261112'
LOCK_PATH = ROOT / 'tools/hok_capture_news_update_lock.json'
EVENTS = 'events/NewsEvents_KOR.txt'
PATHS = frozenset((EVENTS,))
IDS = ('newsk.22', 'newsk.23', 'newsk.24')


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def canonical_name(relative: str | Path) -> str:
    path = (ROOT / Path(str(relative).replace('\\', '/'))).resolve()
    name = path.relative_to(ROOT.resolve()).as_posix()
    return EVENTS if name.casefold() == EVENTS.casefold() else name


@lru_cache(maxsize=1)
def lock() -> dict:
    config = json.loads(LOCK_PATH.read_text(encoding='utf-8'))
    if (config.get('format') != 1 or config.get('revision') != '2026-11-12-capture-news-v1'
            or config.get('base_commit') != '180ffad37821835be3338e66e27c755982a16468'
            or config.get('source_commit') != 'cdc022eee15fbf7404d4cb30cf2d0102d29e550c'
            or config.get('ancestor_commit') != '424e4d962803b5cc7a3667a7df4604fbd128733a'
            or config.get('workshop_manifest') != '1963361040482473746'
            or config.get('game_version') != 'Operation Postern v1.19.4.2.2da5 (0bdb)'
            or set(config.get('outputs', {})) != PATHS):
        raise ValueError('unreviewed capture-news source, host or output inventory')
    record = config['outputs'][EVENTS]
    if (record.get('classification') != 'ADD' or record.get('previous_snapshot') != 'compat_before/' + EVENTS
            or any(not re.fullmatch('[A-F0-9]{64}', record.get(key, ''))
                   for key in ('sha256', 'previous_sha256')) or record.get('size', 0) <= 0):
        raise ValueError('unreviewed capture-news output contract')
    return config


def frozen(relative: str, expected: str, size: int | None = None) -> bytes:
    path = (SNAPSHOT / relative).resolve()
    path.relative_to(SNAPSHOT.resolve())
    raw = path.read_bytes()
    if sha(raw) != expected or (size is not None and len(raw) != size):
        raise ValueError(f'capture-news frozen input drift: {relative}')
    return raw


@lru_cache(maxsize=1)
def manifest() -> dict:
    config = lock()
    result = json.loads(frozen('source-manifest.json', config['source_manifest_sha256']))
    if (result.get('source_commit') != config['source_commit']
            or result.get('ancestor_commit') != config['ancestor_commit']
            or result.get('compatibility_base_commit') != config['base_commit']
            or set(result.get('sources', {})) != {'donor_before', 'donor_after', 'compat_before', 'alignment_document'}):
        raise ValueError('capture-news source inventory drift')
    for record in result['sources'].values():
        frozen(record['snapshot'], record['sha256'], record['size'])
    expected_states = {608: 9843, 1114: 11913, 1116: 6999, 1035: None, 1037: None}
    if {row['state_id']: row['city_province'] for row in result['host_inputs'].values()} != expected_states:
        raise ValueError('capture-news host state inventory drift')
    host = Path(config['rt56_root']).resolve()
    for relative, record in result['host_inputs'].items():
        path = (host / relative).resolve()
        path.relative_to(host)
        raw = frozen(record['snapshot'], record['sha256'], record['size'])
        if path.read_bytes() != raw:
            raise ValueError(f'capture-news current RT56 input drift: {relative}')
        state = re.search(rb'(?m)^\s*id\s*=\s*(\d+)\b', raw)
        provinces = re.search(rb'\bprovinces\s*=\s*\{([^}]+)\}', raw)
        if state is None or int(state[1]) != record['state_id'] or provinces is None:
            raise ValueError(f'capture-news host state schema drift: {relative}')
        city = record['city_province']
        if city is not None and city not in {int(x) for x in re.findall(rb'\d+', provinces[1])}:
            raise ValueError(f'capture-news city parent drift: {relative}')
    game = result['game']
    raw = frozen(game['snapshot'], game['sha256'], game['size'])
    if (Path(game['original_path']).read_bytes() != raw
            or json.loads(raw.decode('utf-8-sig'))['version'] != config['game_version']):
        raise ValueError('capture-news installed game version drift')
    schema = result.get('schema_inputs', {})
    if set(schema) != {'documentation/triggers_documentation.md', 'common/national_focus/soviet.txt'}:
        raise ValueError('capture-news installed schema inventory drift')
    vanilla = Path(config['vanilla_root']).resolve()
    for relative, record in schema.items():
        path = (vanilla / relative).resolve()
        path.relative_to(vanilla)
        raw = path.read_bytes()
        if sha(raw) != record['sha256'] or len(raw) != record['size']:
            raise ValueError(f'capture-news installed schema source drift: {relative}')
    workshop = result['workshop']
    acf = Path(workshop['original_path']).read_text(encoding='utf-8-sig')
    entries = [dict(re.findall(r'"([^"\r\n]+)"\s*"([^"]*)"', body))
               for body in re.findall(r'"820260968"\s*\{([^}]+)\}', acf)]
    if (len(entries) != 2
            or any(entry.get('manifest', '').strip() != config['workshop_manifest'] for entry in entries)
            or entries[-1].get('latest_manifest', '').strip() != config['workshop_manifest']
            or workshop['manifest'] != config['workshop_manifest']):
        raise ValueError('capture-news installed RT56 Workshop manifest drift')
    return result


def previous_bytes() -> bytes:
    record = lock()['outputs'][EVENTS]
    return frozen(record['previous_snapshot'], record['previous_sha256'])


def block_end(raw: bytes, opening: int) -> int:
    depth, quoted, escaped, comment = 0, False, False, False
    for index in range(opening, len(raw)):
        char = raw[index]
        if comment:
            if char in (10, 13): comment = False
        elif quoted:
            if escaped: escaped = False
            elif char == 92: escaped = True
            elif char == 34: quoted = False
        elif char == 35: comment = True
        elif char == 34: quoted = True
        elif char == 123: depth += 1
        elif char == 125:
            depth -= 1
            if depth == 0: return index + 1
    raise ValueError('unclosed capture-news source block')


def trigger_span(raw: bytes, identifier: str, *, note: bool = False) -> tuple[int, int]:
    matches = []
    for event in re.finditer(rb'(?m)^news_event\s*=\s*\{', raw):
        end = block_end(raw, raw.index(b'{', event.start(), event.end()))
        body = raw[event.start():end]
        event_id = re.search(rb'(?m)^\s*id\s*=\s*([^\s#]+)', body)
        if event_id is not None and event_id[1].decode() == identifier:
            matches.append((event.start(), body))
    if len(matches) != 1: raise ValueError(f'capture-news event inventory drift: {identifier}')
    offset, body = matches[0]
    triggers = list(re.finditer(rb'(?m)^\ttrigger\s*=\s*\{', body))
    if len(triggers) != 1: raise ValueError(f'capture-news trigger inventory drift: {identifier}')
    trigger = triggers[0]
    start = offset + trigger.start()
    end = block_end(raw, raw.index(b'{', start, offset + trigger.end()))
    if note:
        line_end = start - 1 if raw[start - 1:start] == b'\n' else start
        line_start = raw.rfind(b'\n', 0, line_end) + 1
        if not raw[line_start:line_end].startswith(b'\t#20261112_kpopmodder: '):
            raise ValueError(f'capture-news source contributor note missing: {identifier}')
        start = line_start
    return start, end


def generated_bytes() -> bytes:
    records = manifest()['sources']
    before = frozen(records['donor_before']['snapshot'], records['donor_before']['sha256']).replace(b'\r\n', b'\n')
    after = frozen(records['donor_after']['snapshot'], records['donor_after']['sha256']).replace(b'\r\n', b'\n')
    proof, result = before, previous_bytes()
    for identifier in IDS:
        start, end = trigger_span(before, identifier)
        old = before[start:end]
        start, end = trigger_span(after, identifier, note=True)
        updated = after[start:end]
        if proof.count(old) != 1: raise ValueError(f'ambiguous donor trigger: {identifier}')
        proof = proof.replace(old, updated, 1)
        #20261112_kpopmodder: Retain the donor city/war pairs while using RT56 Nanjing1114 and Chongqing1116.
        if identifier == 'newsk.23':
            if updated.count(b'1035 = { is_owned_by = CHI }') != 1: raise ValueError('Nanjing source parent drift')
            updated = updated.replace(b'1035 = { is_owned_by = CHI }', b'1114 = { is_owned_by = CHI }')
        elif identifier == 'newsk.24':
            if updated.count(b'1037 = { is_owned_by = ') != 2: raise ValueError('Chongqing source parent drift')
            updated = updated.replace(b'1037 = { is_owned_by = ', b'1116 = { is_owned_by = ')
        start, end = trigger_span(result, identifier)
        current = result[start:end]
        if current.replace(b'\r\n', b'\n') != old:
            raise ValueError(f'unreviewed compatibility trigger predecessor: {identifier}')
        newline = b'\r\n' if b'\r\n' in current else b'\n'
        result = result[:start] + updated.replace(b'\n', newline) + result[end:]
    if proof != after: raise ValueError('donor capture-news delta extends beyond three reviewed triggers')
    if any(re.search(rb'(?m)^\s*id\s*=\s*' + re.escape(identifier) + rb'\s*$', result)
           for identifier in (b'newsk.27', b'newsj.1', b'newsj.2', b'newsj.3', b'newsj.4')):
        raise ValueError('capture-news update restored pruned content')
    return result


@lru_cache(maxsize=1)
def build_outputs() -> dict[str, bytes]:
    result = generated_bytes()
    record = lock()['outputs'][EVENTS]
    if len(result) != record['size'] or sha(result) != record['sha256']:
        raise ValueError('capture-news generated output drift')
    return {EVENTS: result}


def historical_bytes(relative: str | Path, data: bytes) -> bytes:
    name = canonical_name(relative)
    if name in PATHS and sha(data) == lock()['outputs'][name]['sha256']:
        if data != build_outputs()[name]: raise ValueError('capture-news final-output proof failed')
        return previous_bytes()
    return data


def finalize_one(relative: str | Path, data: bytes) -> bytes:
    name = canonical_name(relative)
    if name not in PATHS: return data
    final = build_outputs()[name]
    if data not in (previous_bytes(), final):
        raise ValueError(f'unreviewed capture-news predecessor: {name}')
    return final


def preflight_outputs(outputs: dict) -> None:
    seen = set()
    for relative, data in outputs.items():
        name = canonical_name(relative)
        if name not in PATHS: continue
        if name in seen: raise ValueError('duplicate capture-news output')
        seen.add(name)
        final = build_outputs()[name]
        if data != final: raise ValueError('unregistered proposed capture-news bytes')
        path = ROOT / name
        if not path.is_file() or path.read_bytes() not in (previous_bytes(), final):
            raise ValueError('independently changed capture-news runtime')


def ledger_bytes(previous: bytes) -> bytes:
    record = lock()['outputs'][EVENTS]
    if (ROOT / EVENTS).read_bytes() != build_outputs()[EVENTS]:
        raise ValueError('capture-news ledger/runtime mismatch')
    reader = csv.DictReader(io.StringIO(previous.decode('utf-8'), newline=''))
    fields = reader.fieldnames
    if not fields or not {'source_path', 'output_path', 'output_sha256', 'reason', 'integration_class'} <= set(fields):
        raise ValueError('capture-news ledger schema drift')
    lines, start, seen = previous.splitlines(keepends=True), reader.line_num, False
    chunks = [b''.join(lines[:start])]
    suffix = ('; 2026-11-12 selected donor city-capture news: tools/hok_capture_news_update_lock.json'
              '; donor=cdc022eee15fbf7404d4cb30cf2d0102d29e550c; RT56 city parents=608/1114/1116'
              '; previous_output_sha256=' + record['previous_sha256'] + '; original HOK authorship retained')
    for row in reader:
        raw, start = b''.join(lines[start:reader.line_num]), reader.line_num
        if row['output_path'] != EVENTS: chunks.append(raw); continue
        if seen or row['source_path'] != EVENTS or row['integration_class'] != record['classification']:
            raise ValueError('capture-news ledger ownership drift')
        seen = True
        if row['output_sha256'] == record['sha256'] and row['reason'].endswith(suffix):
            chunks.append(raw); continue
        if row['output_sha256'] != record['previous_sha256'] or suffix in row['reason']:
            raise ValueError('capture-news ledger predecessor drift')
        row['output_sha256'], row['reason'] = record['sha256'], row['reason'] + suffix
        stream = io.StringIO(newline='')
        newline = '\r\n' if raw.endswith(b'\r\n') else '\n'
        csv.DictWriter(stream, fieldnames=fields, lineterminator=newline).writerow(row)
        chunks.append(stream.getvalue().encode('utf-8'))
    if not seen: raise ValueError('capture-news ledger row missing')
    return b''.join(chunks)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        outputs = build_outputs()
        preflight_outputs(outputs)
        pending = [(ROOT / name, data) for name, data in outputs.items() if (ROOT / name).read_bytes() != data]
        if pending and not args.apply: raise ValueError('capture-news runtime differs from reviewed output')
        for path, data in pending: path.write_bytes(data)
        print(f'PASS capture-news update: 3 trigger blocks; 1 output; {len(pending)} written')
        return 0
    except (ValueError, KeyError, OSError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__': raise SystemExit(main())
