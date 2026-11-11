#!/usr/bin/env python3
"""Reproduce the reviewed Korean-American defence-sharing update over the RT56 port."""
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

#20261111_kpopmodder: Preserve earlier port bytes while integrating the author's bilateral defence module.
ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / 'docs/upstream/hok-us-defense-update-20261111'
LOCK_PATH = ROOT / 'tools/hok_us_defense_update_lock.json'
FOCUS, EVENTS = 'common/national_focus/korea.txt', 'events/korea.txt'
ENGLISH = 'localisation/english/HOK_KOR_us_defense_l_english.yml'
OLD = frozenset((FOCUS, EVENTS))
PATHS = OLD | frozenset((
    'common/ideas/HOK_KOR_us_defense_ideas.txt',
    'common/scripted_effects/HOK_KOR_us_defense_effects.txt',
    'common/scripted_triggers/HOK_KOR_us_defense_triggers.txt',
    'events/HOK_KOR_us_defense_events.txt',
    'interface/HOK_KOR_us_defense_event_pictures.gfx',
    'interface/HOK_KOR_us_defense_ideas.gfx', ENGLISH,
    'localisation/korean/HOK_KOR_us_defense_l_korean.yml',
    *(f'gfx/event_pictures/HOK_KOR/us_defense/{name}.dds' for name in
      ('us_defense_talks', 'us_defense_agreement_news', 'us_defense_dominion', 'us_defense_dominion_news')),
    *(f'gfx/interface/ideas/HOK_KOR/us_defense/HOK_KOR_{name}_{tier}.dds'
      for name in ('us_defense_cost_sharing', 'korean_defense_contribution') for tier in (1, 2)),
))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def canonical_name(relative: str | Path) -> str:
    path = Path(str(relative).replace('\\', '/'))
    resolved = (ROOT / path).resolve()
    name = resolved.relative_to(ROOT.resolve()).as_posix()
    return next((p for p in PATHS if p.casefold() == name.casefold()), name)


@lru_cache(maxsize=1)
def lock() -> dict:
    config = json.loads(LOCK_PATH.read_text(encoding='utf-8'))
    if (config.get('format') != 1 or config.get('revision') != '2026-11-11-us-defense-v1'
            or config.get('base_commit') != '39e8e7e5bc3dbdcf52d8c8acc04a92c97cd0b2f5'
            or config.get('source_commit') != 'e2009b635d79c80a67fed0370d5fe36a823b656f'
            or set(config.get('outputs', {})) != PATHS):
        raise ValueError('unreviewed US defence revision, source or output inventory')
    for name, record in config['outputs'].items():
        expected = 'THREE_WAY_MERGE' if name in OLD else 'ASSET_COPY' if name.endswith('.dds') else 'ADD'
        if (record['classification'] != expected
                or not re.fullmatch('[A-F0-9]{64}', record['sha256']) or record['size'] <= 0
                or (name in OLD and (record.get('previous_snapshot') != 'compat_before/' + name
                    or not re.fullmatch('[A-F0-9]{64}', record.get('previous_sha256', ''))))
                or (name not in OLD and record.get('previous_sha256') is not None)):
            raise ValueError(f'unreviewed US defence output contract: {name}')
    return config


def frozen(relative: str, expected: str, size: int | None = None) -> bytes:
    path = (SNAPSHOT / relative).resolve()
    path.relative_to(SNAPSHOT.resolve())
    data = path.read_bytes()
    if sha(data) != expected or (size is not None and len(data) != size):
        raise ValueError(f'US defence frozen input drift: {relative}')
    return data


def previous_bytes(relative: str | Path) -> bytes:
    record = lock()['outputs'][canonical_name(relative)]
    return frozen(record['previous_snapshot'], record['previous_sha256'])


@lru_cache(maxsize=1)
def manifest() -> dict:
    config = lock()
    result = json.loads(frozen('source-manifest.json', config['source_manifest_sha256']))
    if set(result['sources']) != PATHS or set(result['ancestors']) != OLD:
        raise ValueError('US defence source inventory drift')
    for group in ('sources', 'ancestors', 'documents'):
        for name, record in result[group].items():
            prefix = {'sources': 'runtime/', 'ancestors': 'donor_head/', 'documents': 'documents/'}[group]
            if record['snapshot'] != prefix + name:
                raise ValueError(f'US defence source path drift: {name}')
            frozen(record['snapshot'], record['sha256'], record['size'])
    translation = result['translation']
    if translation['snapshot'] != 'translation_source/' + ENGLISH:
        raise ValueError('US defence English source path drift')
    frozen(translation['snapshot'], translation['sha256'], translation['size'])
    for name in OLD:
        previous_bytes(name)
    for name, record in result['host_inputs'].items():
        if record['provider'] not in ('rt56', 'vanilla'):
            raise ValueError(f'US defence host provider drift: {name}')
        base = Path(config[record['provider'] + '_root']).resolve()
        path = (base / name).resolve()
        path.relative_to(base)
        raw = path.read_bytes()
        if sha(raw) != record['sha256'] or len(raw) != record['size']:
            raise ValueError(f'US defence host/schema drift: {name}')
    host = Path(config['rt56_root'])
    acf = (host.parents[2] / 'appworkshop_394360.acf').read_text(encoding='utf-8-sig')
    entries = re.findall(r'"820260968"\s*\{([^{}]+)\}', acf)
    versions = [v for e in entries for v in re.findall(r'"(?:latest_)?manifest"\s*"(\d+)"', e)]
    if len(versions) < 2 or any(v != config['workshop_manifest'] for v in versions):
        raise ValueError('US defence installed/latest RT56 manifest drift')
    game = json.loads((Path(config['vanilla_root']) / 'launcher-settings.json').read_text(encoding='utf-8-sig'))
    if game['version'] != config['game_version']:
        raise ValueError('US defence installed game-version drift')
    for name in PATHS - OLD:
        if any((Path(config[p + '_root']) / name).exists() for p in ('rt56', 'vanilla')):
            raise ValueError(f'US defence unreviewed host path collision: {name}')
    return result


def block_span(text: str, key: str) -> tuple[int, int]:
    match = re.search(r'(?m)^[ \t]*' + re.escape(key) + r'\s*=\s*\{', text)
    if match is None:
        raise ValueError(f'US defence missing block: {key}')
    depth, quoted, escaped, comment = 0, False, False, False
    for i in range(match.end() - 1, len(text)):
        char = text[i]
        if comment:
            if char == '\n': comment = False
        elif quoted:
            if escaped: escaped = False
            elif char == '\\': escaped = True
            elif char == '"': quoted = False
        elif char == '#': comment = True
        elif char == '"': quoted = True
        elif char == '{': depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0: return match.start(), i + 1
    raise ValueError(f'US defence unclosed block: {key}')


def identified(text: str, kind: str, identifier: str) -> tuple[int, int]:
    found = []
    for match in re.finditer(r'(?m)^[ \t]*' + kind + r'\s*=\s*\{', text):
        _, end = block_span(text[match.start():], kind)
        end += match.start()
        if re.search(r'(?m)^\s*id\s*=\s*' + re.escape(identifier) + r'\s*$', text[match.start():end]):
            found.append((match.start(), end))
    if len(found) != 1:
        raise ValueError(f'US defence definition is not unique: {identifier}')
    return found[0]


def section(text: str, key: str, *, note: bool = False) -> tuple[int, int]:
    start, end = block_span(text, key)
    if note:
        before = text[:start]
        line = before.rstrip('\r\n').rsplit('\n', 1)[-1]
        if not line.lstrip().startswith('#20261111_kpopmodder:'):
            raise ValueError(f'US defence contributor note missing: {key}')
        start -= len(line) + (2 if before.endswith('\r\n') else 1)
    return start, end


def merge_focus(before: bytes, donor_before: bytes, donor_after: bytes) -> bytes:
    text = before.decode('utf-8')
    newline = '\r\n' if b'\r\n' in before else '\n'
    old, new = (data.decode('utf-8').replace('\r\n', '\n').replace('\n', newline)
                for data in (donor_before, donor_after))
    for identifier in ('KOR_rok_us_mutual_defense_treaty', 'KOR_usfk'):
        a, b = identified(old, 'focus', identifier)
        c, d = identified(new, 'focus', identifier)
        x, y = identified(text, 'focus', identifier)
        u, v = section(old[a:b], 'completion_reward')
        p, q = section(text[x:y], 'completion_reward')
        n, m = section(new[c:d], 'completion_reward', note=True)
        if text[x+p:x+q] != old[a+u:a+v]:
            raise ValueError(f'US defence focus predecessor drift: {identifier}')
        text = text[:x+p] + new[c+n:c+m] + text[x+q:]
    x, y = identified(text, 'focus', 'KOR_katusa')
    c, d = identified(new, 'focus', 'KOR_katusa')
    if re.search(r'(?m)^\s*available\s*=', text[x:y]):
        raise ValueError('US defence KATUSA already has an availability block')
    n, m = section(new[c:d], 'available', note=True)
    anchor, _ = block_span(text[x:y], 'ai_will_do')
    return (text[:x+anchor] + new[c+n:c+m] + newline + text[x+anchor:]).encode('utf-8')


def merge_events(before: bytes, donor_before: bytes, donor_after: bytes) -> bytes:
    text = before.decode('utf-8')
    newline = '\r\n' if b'\r\n' in before else '\n'
    old, new = (data.decode('utf-8').replace('\r\n', '\n').replace('\n', newline)
                for data in (donor_before, donor_after))
    for identifier in ('kor_events.45', 'kor_events.46', 'kor_events.47'):
        a, b = identified(old, 'country_event', identifier)
        c, d = identified(new, 'country_event', identifier)
        x, y = identified(text, 'country_event', identifier)
        normalize = lambda chunk: re.sub(r'(\bid\s*=\s*)KOR_events\.(46|47)\b', r'\1kor_events.\2', chunk)
        if text[x:y] != normalize(old[a:b]):
            raise ValueError(f'US defence event predecessor drift: {identifier}')
        text = text[:x] + normalize(new[c:d]) + text[y:]
    return text.encode('utf-8')


@lru_cache(maxsize=1)
def build_outputs() -> dict[str, bytes]:
    sources = manifest()
    outputs = {}
    for name, record in sources['sources'].items():
        data = frozen(record['snapshot'], record['sha256'], record['size'])
        if name in OLD:
            ancestor = sources['ancestors'][name]
            old = frozen(ancestor['snapshot'], ancestor['sha256'], ancestor['size'])
            data = (merge_focus if name == FOCUS else merge_events)(previous_bytes(name), old, data)
        elif name == ENGLISH:
            tr = sources['translation']
            data = frozen(tr['snapshot'], tr['sha256'], tr['size'])
        expected = lock()['outputs'][name]
        if sha(data) != expected['sha256'] or len(data) != expected['size']:
            raise ValueError(f'US defence generated-output drift: {name}')
        outputs[name] = data
    return outputs


def historical_bytes(relative: str | Path, data: bytes) -> bytes:
    name = canonical_name(relative)
    if name in OLD and sha(data) == lock()['outputs'][name]['sha256']:
        if data != build_outputs()[name]: raise ValueError(f'US defence final proof failed: {name}')
        return previous_bytes(name)
    return data


def finalize_one(relative: str | Path, data: bytes) -> bytes:
    name = canonical_name(relative)
    if name not in PATHS: return data
    record = lock()['outputs'][name]
    if sha(data) not in {record['sha256'], record.get('previous_sha256')}:
        raise ValueError(f'unreviewed US defence predecessor: {name}')
    return build_outputs()[name]


def finalize_outputs(outputs: dict, *, owner: str) -> dict:
    result = {name: finalize_one(name, data) for name, data in outputs.items()}
    path_keys = bool(outputs) and isinstance(next(iter(outputs)), Path)
    if owner == 'focus':
        for name in sorted(PATHS - OLD):
            if not any(canonical_name(p) == name for p in result): result[Path(name) if path_keys else name] = build_outputs()[name]
    return result


def preflight_outputs(outputs: dict) -> None:
    seen = set()
    for relative, data in outputs.items():
        name = canonical_name(relative)
        if name not in PATHS: continue
        if name in seen: raise ValueError(f'duplicate US defence output: {name}')
        seen.add(name)
        if data != build_outputs()[name]: raise ValueError(f'unregistered proposed US defence bytes: {name}')
        path, record = ROOT / name, lock()['outputs'][name]
        if path.exists() and (not path.is_file() or sha(path.read_bytes()) not in
                             {record['sha256'], record.get('previous_sha256')}):
            raise ValueError(f'independently changed US defence runtime: {name}')
        if name in OLD and not path.is_file(): raise ValueError(f'missing US defence predecessor: {name}')


def ledger_bytes(previous: bytes) -> bytes:
    outputs, config = build_outputs(), lock()
    if any((ROOT / name).read_bytes() != data for name, data in outputs.items()):
        raise ValueError('US defence ledger/runtime mismatch')
    reader = csv.DictReader(io.StringIO(previous.decode('utf-8'), newline=''))
    fields = reader.fieldnames
    if not fields or not {'source_path', 'output_path', 'output_sha256', 'integration_class', 'reason', 'status'} <= set(fields):
        raise ValueError('US defence ledger schema drift')
    lines, start, seen = previous.splitlines(keepends=True), reader.line_num, set()
    chunks = [b''.join(lines[:start])]
    reason = '; 2026-11-11 Korean-American defence sharing: tools/hok_us_defense_update_lock.json; original HOK authorship retained'
    def encoded(row):
        stream = io.StringIO(newline='')
        csv.DictWriter(stream, fieldnames=fields, lineterminator='\n').writerow(row)
        return stream.getvalue().encode('utf-8')
    def addition(name):
        source, record = manifest()['sources'][name], config['outputs'][name]
        row = {field: '' for field in fields}
        values = dict(source_path=name, output_path=name, integration_class=record['classification'], status='SHIPPED',
                      exact_path_rt56_collision='no', output_sha256=record['sha256'], donor_sha256=source['sha256'],
                      donor_source_sha256=source['sha256'], donor_source_commit=config['source_commit'],
                      donor_source_checkout='reviewed-working-tree-snapshot', reason=reason.lstrip('; ') + '; source_kind=reviewed-working-tree-snapshot' +
                      f'; source_snapshot=docs/upstream/hok-us-defense-update-20261111/{source["snapshot"]}')
        if name == ENGLISH:
            tr = manifest()['translation']
            values['reason'] += f'; English source={tr["source_root"]}; source_kind={tr["source_kind"]}; commit={tr["source_commit"]}; sha256={tr["sha256"]}; translation authorship retained'
            values.update(english_translation_source_commit=tr['source_commit'], english_translation_source_relative=ENGLISH,
                          english_translation_source_sha256=tr['sha256'], english_translation_classification=record['classification'],
                          english_translation_source_snapshot_path='docs/upstream/hok-us-defense-update-20261111/' + tr['snapshot'],
                          english_translation_lock='tools/hok_us_defense_update_lock.json')
        row.update({key:value for key,value in values.items() if key in row})
        return row
    for row in reader:
        raw, start = b''.join(lines[start:reader.line_num]), reader.line_num
        name = row['output_path']
        if name not in PATHS: chunks.append(raw); continue
        if name in seen: raise ValueError(f'duplicate US defence ledger output: {name}')
        seen.add(name)
        if name not in OLD:
            if row != addition(name): raise ValueError(f'US defence addition ledger drift: {name}')
        else:
            record = config['outputs'][name]
            suffix = reason + '; previous_output_sha256=' + record['previous_sha256']
            if row['integration_class'] != record['classification']: raise ValueError(f'US defence ownership drift: {name}')
            if row['output_sha256'] != record['sha256'] or not row['reason'].endswith(suffix):
                if row['output_sha256'] != record['previous_sha256'] or reason in row['reason']:
                    raise ValueError(f'US defence ledger predecessor drift: {name}')
                row['output_sha256'], row['reason'] = record['sha256'], row['reason'] + suffix
                raw = encoded(row)
        chunks.append(raw)
    if not OLD <= seen: raise ValueError('US defence ledger missing existing rows')
    for name in sorted(PATHS - seen): chunks.append(encoded(addition(name)))
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
        pending = [(ROOT / name, data) for name, data in outputs.items() if not (ROOT / name).is_file() or (ROOT / name).read_bytes() != data]
        if pending and not args.apply: raise ValueError('US defence runtime mismatches: ' + ', '.join(str(p) for p,_ in pending))
        for path, data in pending:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        print(f'PASS US defence update: 18 exact outputs; 3 focus blocks, 3 treaty events, 16 additions; {len(pending)} written')
        return 0
    except (ValueError, KeyError, OSError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__': raise SystemExit(main())
