#!/usr/bin/env python3
"""Reproduce the scoped English wording revision above immutable source layers."""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from functools import lru_cache
import hashlib
import io
import json
from pathlib import Path
import re
import sys

#20261109_kpopmodder: Translate corporate power semantically without renaming saved IDs or changing historical inputs.
ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / 'tools/hok_english_terminology_lock.json'
SNAPSHOT = ROOT / 'docs/upstream/hok-english-terminology-20261109'
PATHS = frozenset((
    'localisation/english/HOK_KOR_civic_focus_l_english.yml',
    'localisation/english/HOK_KOR_civic_state_l_english.yml',
    'localisation/english/HOK_KOR_civic_ui_l_english.yml',
    'localisation/english/HOK_KOR_fascist_procurement_l_english.yml',
    'localisation/english/korea_event_l_english.yml',
    'localisation/english/korea_focus_l_english.yml',
    'localisation/english/korea_ideas_l_english.yml',
    'localisation/english/replace/korea_decisions_l_english.yml',
))
ROW = re.compile(r'(?m)^([ \t]*([A-Za-z0-9_.-]+):(\d*)[ \t]+")((?:[^"\\\r\n]|\\[^\r\n])*)("[ \t]*(?:#[^\r\n]*)?\r?$)')
TOKENS = re.compile(r'\$[^$\r\n]+\$|\[[^\]\r\n]+\]|§.|£[A-Za-z0-9_]+|@[A-Z][A-Z0-9]{2}|\\[nrt"\\]')


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def canonical_name(relative: str | Path) -> str:
    name = str(relative).replace('\\', '/')
    return next((path for path in PATHS if path.casefold() == name.casefold()), name)


@lru_cache(maxsize=1)
def lock() -> dict:
    config = json.loads(LOCK_PATH.read_text(encoding='utf-8'))
    if (config.get('format') != 1 or config.get('revision') != '2026-11-09-chaebol-english-v1'
            or config.get('base_commit') != '95d801fddf8f98fe3641860c2cffa976fb91f5b5'
            or set(config.get('outputs', {})) != PATHS
            or sum(len(record['edits']) for record in config['outputs'].values()) != 43):
        raise ValueError('unreviewed English terminology revision or inventory')
    return config


def previous_bytes(relative: str) -> bytes:
    name = canonical_name(relative)
    record = lock()['outputs'][name]
    expected = SNAPSHOT.relative_to(ROOT).as_posix() + '/before/' + name
    if record['previous_snapshot'] != expected:
        raise ValueError(f'English terminology ancestor path drift: {name}')
    path = (ROOT / expected).resolve()
    path.relative_to(SNAPSHOT.resolve())
    data = path.read_bytes()
    if sha(data) != record['previous_sha256'] or len(data) != record['previous_size']:
        raise ValueError(f'English terminology frozen ancestor drift: {name}')
    return data


def verify_inputs() -> None:
    config = lock()
    for name, record in config['outputs'].items():
        previous_bytes(name)
        korean = name.replace('/english/', '/korean/').replace('_l_english.yml', '_l_korean.yml')
        if record['preserved_korean_path'] != korean or sha((ROOT / korean).read_bytes()) != record['preserved_korean_sha256']:
            raise ValueError(f'English terminology changed its Korean counterpart: {name}')
    host = Path(config['rt56_root'])
    acf = (host.parents[2] / 'appworkshop_394360.acf').read_text(encoding='utf-8-sig')
    entries = re.findall(r'"820260968"\s*\{([^{}]+)\}', acf)
    manifests = [m for entry in entries for m in re.findall(r'"(?:latest_)?manifest"\s*"(\d+)"', entry)]
    if len(manifests) < 2 or any(value != config['workshop_manifest'] for value in manifests):
        raise ValueError('English terminology RT56 installed/latest manifest drift')
    game = json.loads((Path(config['vanilla_root']) / 'launcher-settings.json').read_text(encoding='utf-8-sig'))
    if game['version'] != config['game_version']:
        raise ValueError('English terminology installed game-version drift')


@lru_cache(maxsize=1)
def build_outputs() -> dict[str, bytes]:
    verify_inputs()
    outputs = {}
    for name, record in lock()['outputs'].items():
        before = previous_bytes(name)
        if not before.startswith(b'\xef\xbb\xbfl_english:'):
            raise ValueError(f'English terminology locale header/BOM drift: {name}')
        text = before.decode('utf-8-sig')
        rows = list(ROW.finditer(text))
        keys = [row[2] for row in rows]
        if len(keys) != len(set(keys)):
            raise ValueError(f'English terminology duplicate key: {name}')
        affected = {row[2] for row in rows if re.search(r'\bchaebol\b', row[4], re.I)}
        if affected != record['edits'].keys():
            raise ValueError(f'English terminology changed-key allowlist drift: {name}')
        seen = set()

        def translate(row: re.Match) -> str:
            edit = record['edits'].get(row[2])
            if edit is None:
                return row[0]
            seen.add(row[2])
            old, new = edit['before'], edit['after']
            if row[4] != old or old == new or re.search(r'\bchaebol\b|[\uac00-\ud7a3]', new, re.I):
                raise ValueError(f'English terminology source/translated meaning drift: {name}/{row[2]}')
            if (Counter(TOKENS.findall(old)) != Counter(TOKENS.findall(new))
                    or re.findall(r'\d+(?:\.\d+)?', old) != re.findall(r'\d+(?:\.\d+)?', new)):
                raise ValueError(f'English terminology changed tokens or numbers: {name}/{row[2]}')
            return row[1] + new + row[5]

        data = ROW.sub(translate, text).encode('utf-8-sig')
        if seen != record['edits'].keys() or sha(data) != record['sha256'] or len(data) != record['size']:
            raise ValueError(f'English terminology generated output drift: {name}')
        outputs[name] = data
    return outputs


def historical_bytes(relative: str | Path, data: bytes) -> bytes:
    """Only exact registered final bytes may stand in for the earlier contract."""
    name = canonical_name(relative)
    if name not in PATHS:
        return data
    if sha(data) == lock()['outputs'][name]['sha256']:
        if data != build_outputs()[name]:
            raise ValueError(f'English terminology final-output proof failed: {name}')
        return previous_bytes(name)
    return data


def finalize_one(relative: str | Path, data: bytes) -> bytes:
    name = canonical_name(relative)
    if name not in PATHS:
        return data
    record = lock()['outputs'][name]
    if sha(data) not in (record['previous_sha256'], record['sha256']):
        raise ValueError(f'unreviewed English terminology predecessor: {name}')
    return build_outputs()[name]


def preflight_outputs(outputs: dict) -> None:
    root, seen = ROOT.resolve(), set()
    for relative, data in outputs.items():
        path = (root / relative).resolve()
        name = canonical_name(path.relative_to(root))
        if path in seen:
            raise ValueError(f'duplicate English terminology output: {name}')
        seen.add(path)
        record = lock()['outputs'].get(name)
        if record is None:
            continue
        if data != build_outputs()[name]:
            raise ValueError(f'unreviewed proposed English terminology bytes: {name}')
        if not path.is_file() or sha(path.read_bytes()) not in (record['previous_sha256'], record['sha256']):
            raise ValueError(f'independently changed English terminology runtime: {name}')


def ledger_bytes(previous: bytes) -> bytes:
    """Retain earlier attribution and update only the eight reviewed output rows."""
    lines = previous.splitlines(keepends=True)
    reader = csv.DictReader(io.StringIO(previous.decode('utf-8'), newline=''))
    fields = reader.fieldnames
    start, chunks, touched = reader.line_num, [lines[0]], set()
    for row in reader:
        raw = b''.join(lines[start:reader.line_num])
        start = reader.line_num
        name = row['output_path']
        record = lock()['outputs'].get(name)
        if record is None:
            chunks.append(raw)
            continue
        if name in touched or row['integration_class'] != record['classification']:
            raise ValueError(f'English terminology ledger ownership drift: {name}')
        touched.add(name)
        reason = ('; 2026-11-09 English terminology: tools/hok_english_terminology_lock.json; '
                  f'previous_output_sha256={record["previous_sha256"]}; '
                  'corporate oligarchs as power-holders and conglomerates as companies; original authorship retained')
        if (ROOT / name).read_bytes() != build_outputs()[name]:
            raise ValueError(f'English terminology ledger runtime differs: {name}')
        if row['output_sha256'] == record['sha256'] and row['reason'].endswith(reason):
            chunks.append(raw)
            continue
        if row['output_sha256'] != record['previous_sha256']:
            raise ValueError(f'English terminology ledger predecessor hash drift: {name}')
        row['output_sha256'] = record['sha256']
        row['reason'] += reason
        stream = io.StringIO(newline='')
        csv.DictWriter(stream, fieldnames=fields, lineterminator='\n').writerow(row)
        chunks.append(stream.getvalue().encode('utf-8'))
    if touched != PATHS:
        raise ValueError('English terminology ledger missing reviewed outputs')
    return b''.join(chunks)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        outputs = build_outputs()
        preflight_outputs(outputs)
        pending = [(ROOT / name, data) for name, data in outputs.items() if (ROOT / name).read_bytes() != data]
        if pending and not args.apply:
            raise ValueError('English terminology runtime mismatches: ' + ', '.join(p.relative_to(ROOT).as_posix() for p, _ in pending))
        for path, data in pending:
            path.write_bytes(data)
        print(f'PASS English terminology: 8 exact outputs, 43 translated values, {len(pending)} written; keys, tokens, Korean and historical inputs retained')
        return 0
    except (ValueError, KeyError, FileNotFoundError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
