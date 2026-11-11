#!/usr/bin/env python3
"""Reproduce the selected November 10 donor industry delta over the RT56 port."""
from __future__ import annotations

import argparse
import csv
from functools import lru_cache
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys

#20261110_kpopmodder: Keep the author's separate provincial investments and reward update above immutable earlier merges.
ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / 'docs/upstream/hok-industry-update-20261110'
LOCK_PATH = ROOT / 'tools/hok_industry_update_lock.json'
FOCUS = 'common/national_focus/korea.txt'
DECISIONS = 'common/decisions/HOK_KOR_industry_expansion.txt'
ENGLISH = 'localisation/english/HOK_KOR_industry_expansion_l_english.yml'
KOREAN = 'localisation/korean/HOK_KOR_industry_expansion_l_korean.yml'
PATHS = frozenset((FOCUS, DECISIONS, ENGLISH, KOREAN))
FOCUS_IDS = ('KOR_northern_development', 'KOR_southern_development',
             'KOR_central_region_development', 'KOR_gyeongbu_expressway',
             'KOR_gyeongui_expressway', 'HOK_KOR_pyeongan_machine_workshops',
             'HOK_KOR_chungcheong_supplier_network', 'HOK_KOR_gyeongsang_export_workshops')
STATE_MAP = {1028:918, 1029:1144, 1030:920, 1031:1145, 1082:919, 1083:917,
             1084:1146, 1085:1147, 1086:1148, 1087:1149, 1088:1150,
             1089:1151, 1090:1152, 1091:1153}
ROW = re.compile(r'(?m)^([ \t]*([A-Za-z0-9_.-]+):\d*[ \t]+")((?:[^"\\\r\n]|\\[^\r\n])*)("[^\r\n]*)$')

#20261111_kpopmodder: Keep the subsequent two-line nuclear reward separate from the immutable industry contract.
FISSION_LOCK_PATH = ROOT / 'tools/hok_fission_update_lock.json'
FISSION_SNAPSHOT = ROOT / 'docs/upstream/hok-fission-update-20261111'


@lru_cache(maxsize=1)
def fission_lock() -> dict:
    config = json.loads(FISSION_LOCK_PATH.read_text(encoding='utf-8'))
    if (config.get('format') != 1 or config.get('revision') != '2026-11-11-fission-v1'
            or config.get('base_commit') != '6931151ff3009127bf35564cd39eb9b2df88f508'
            or config.get('source_commit') != '1c2e5423c08677228fa89c0181535bc30fc5764d'
            or config.get('path') != FOCUS
            or config.get('focus_id') != 'HOK_KOR_fission_chain_reaction_experiments'
            or config.get('checkout') != 'crlf'
            or config.get('previous_sha256') != lock()['outputs'][FOCUS]['sha256']
            or config.get('classification') != 'THREE_WAY_MERGE'):
        raise ValueError('unreviewed fission source, target or predecessor')
    command = ['git', '-C', config['donor_root']]
    blob = subprocess.check_output(command + ['rev-parse', config['source_commit'] + ':' + FOCUS]).decode().strip()
    source = subprocess.check_output(command + ['cat-file', 'blob', blob])
    anchor = ('\t\t\t\tname = HOK_KOR_fission_chain_reaction_experiments\r\n'
              '\t\t\t\tahead_reduction = 2\r\n')
    addition = ('\t\t\t\t#20261111_kpopmodder: Add a 150% research bonus while preserving the two-year ahead-of-time reduction.\r\n'
                '\t\t\t\tbonus = 1.5\r\n')
    if (blob != config['source_blob'] or sha(source) != config['source_object_sha256']
            or b'\r' in source or config['anchor'] != anchor or config['added_lines'] != addition):
        raise ValueError('fission immutable source or two-line delta drift')
    before = source.replace(b'\n', b'\r\n')
    if (sha(before) != config['source_before_sha256'] or before.count(anchor.encode()) != 1
            or sha(before.replace(anchor.encode(), (anchor + addition).encode(), 1)) != config['source_sha256']):
        raise ValueError('fission reviewed donor delta drift')
    for relative, expected in config['documents'].items():
        path = (FISSION_SNAPSHOT / relative).resolve()
        path.relative_to(FISSION_SNAPSHOT.resolve())
        if sha(path.read_bytes()) != expected:
            raise ValueError(f'fission source-document drift: {relative}')
    for relative, record in config['host_inputs'].items():
        path = Path(lock()[record['provider'] + '_root']) / relative
        if sha(path.read_bytes()) != record['sha256']:
            raise ValueError(f'fission host/schema drift: {relative}')
    return config


@lru_cache(maxsize=1)
def current_outputs() -> dict[str, bytes]:
    outputs = dict(build_outputs())
    config = fission_lock()
    before = outputs[FOCUS]
    anchor, addition = config['anchor'].encode(), config['added_lines'].encode()
    start, end = reward(before.decode('utf-8'), config['focus_id'])
    if (sha(before) != config['previous_sha256'] or before.count(anchor) != 1
            or anchor.decode() not in before.decode('utf-8')[start:end]):
        raise ValueError('fission bonus is outside the reviewed focus reward')
    after = before.replace(anchor, anchor + addition, 1)
    if sha(after) != config['sha256'] or len(after) != config['size']:
        raise ValueError('fission final-output drift')
    outputs[FOCUS] = after
    return outputs


def fission_historical(relative: str | Path, data: bytes) -> bytes:
    if canonical_name(relative) == FOCUS and sha(data) == fission_lock()['sha256']:
        if data != current_outputs()[FOCUS]:
            raise ValueError('fission final-output proof failed')
        return build_outputs()[FOCUS]
    return data


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def canonical_name(relative: str | Path) -> str:
    name = str(relative).replace('\\', '/')
    return next((path for path in PATHS if path.casefold() == name.casefold()), name)


@lru_cache(maxsize=1)
def lock() -> dict:
    config = json.loads(LOCK_PATH.read_text(encoding='utf-8'))
    if (config.get('format') != 1 or config.get('revision') != '2026-11-10-industry-v1'
            or config.get('base_commit') != '287c5a22f264075bac65505e0a3e9d8a29ff24f3'
            or config.get('source_commit') != '596b221bb994d93fce552d3ee1ba70fa9b5640f1'
            or set(config.get('outputs', {})) != PATHS
            or tuple(config.get('focus_ids', ())) != FOCUS_IDS
            or {int(k):v for k,v in config.get('state_mapping', {}).items()} != STATE_MAP):
        raise ValueError('unreviewed industry update revision, source, inventory or map')
    return config


def frozen(relative: str, expected: str) -> bytes:
    path = (SNAPSHOT / relative).resolve()
    path.relative_to(SNAPSHOT.resolve())
    data = path.read_bytes()
    if sha(data) != expected:
        raise ValueError(f'industry frozen input drift: {relative}')
    return data


def previous_bytes(relative: str) -> bytes:
    name = canonical_name(relative)
    record = lock()['outputs'][name]
    if record['previous_snapshot'] != 'compat_before/' + name:
        raise ValueError(f'industry ancestor path drift: {name}')
    return frozen(record['previous_snapshot'], record['previous_sha256'])


def verify_inputs() -> None:
    config = lock()
    manifest = json.loads(frozen('source-manifest.json', config['source_manifest_sha256']))
    for name, record in manifest['sources'].items():
        frozen('donor_head/' + name, record['before_sha256'])
        frozen('donor_worktree/' + name, record['after_sha256'])
    for record in manifest['translation_sources'].values():
        frozen(record['copy'], record['sha256'])
    for name in PATHS:
        previous_bytes(name)
    for name, record in config['host_inputs'].items():
        path = Path(config[record['provider'] + '_root']) / name
        if sha(path.read_bytes()) != record['sha256']:
            raise ValueError(f'industry host/schema drift: {name}')
    host = Path(config['rt56_root'])
    acf = (host.parents[2] / 'appworkshop_394360.acf').read_text(encoding='utf-8-sig')
    entries = re.findall(r'"820260968"\s*\{([^{}]+)\}', acf)
    manifests = [m for entry in entries for m in re.findall(r'"(?:latest_)?manifest"\s*"(\d+)"', entry)]
    if len(manifests) < 2 or any(value != config['workshop_manifest'] for value in manifests):
        raise ValueError('industry RT56 installed/latest manifest drift')
    game = json.loads((Path(config['vanilla_root']) / 'launcher-settings.json').read_text(encoding='utf-8-sig'))
    if game['version'] != config['game_version']:
        raise ValueError('industry installed game-version drift')


def map_states(text: str) -> str:
    text = re.sub(r'(\bHoK state )(\d+)\b',
                  lambda m: m[1] + str(STATE_MAP.get(int(m[2]), int(m[2]))), text)
    text = re.sub(r'(?m)^(\s*)(\d+)(\s*=\s*\{)',
                  lambda m: m[1] + str(STATE_MAP.get(int(m[2]), int(m[2]))) + m[3], text)
    return re.sub(r'(\bstate\s*=\s*)(\d+)\b',
                  lambda m: m[1] + str(STATE_MAP.get(int(m[2]), int(m[2]))), text)


def block_span(text: str, key: str, start: int = 0) -> tuple[int, int]:
    match = re.search(r'(?m)^[ \t]*' + re.escape(key) + r'\s*=\s*\{', text[start:])
    if match is None:
        raise ValueError(f'industry missing block: {key}')
    begin = start + match.start()
    opening = start + match.end() - 1
    depth, quoted, escaped, comment = 0, False, False, False
    for i in range(opening, len(text)):
        char = text[i]
        if comment:
            if char == '\n': comment = False
            continue
        if quoted:
            if escaped: escaped = False
            elif char == '\\': escaped = True
            elif char == '"': quoted = False
            continue
        if char == '#': comment = True
        elif char == '"': quoted = True
        elif char == '{': depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0: return begin, i + 1
    raise ValueError(f'industry unclosed block: {key}')


def reward(text: str, focus_id: str) -> tuple[int, int]:
    matches = list(re.finditer(r'(?m)^\s*id\s*=\s*' + re.escape(focus_id) + r'\s*$', text))
    if len(matches) != 1:
        raise ValueError(f'industry focus ID is not unique: {focus_id}')
    return block_span(text, 'completion_reward', matches[0].end())


def source_text(group: str, name: str) -> str:
    return (SNAPSHOT / group / name).read_bytes().decode('utf-8-sig').replace('\r\n', '\n')


def apply_focus(before: bytes) -> bytes:
    text = before.decode('utf-8').replace('\r\n', '\n')
    donor_before = map_states(source_text('donor_head', FOCUS))
    donor_after = map_states(source_text('donor_worktree', FOCUS))
    for focus_id in FOCUS_IDS:
        old_start, old_end = reward(donor_before, focus_id)
        new_start, new_end = reward(donor_after, focus_id)
        start, end = reward(text, focus_id)
        if text[start:end] != donor_before[old_start:old_end]:
            raise ValueError(f'industry focus predecessor drift: {focus_id}')
        new = donor_after[new_start:new_end]
        if focus_id.startswith('KOR_'):
            new = '\t\t#20261110_kpopmodder: Apply the donor reward to each approved successor state.\n' + new
        text = text[:start] + new + text[end:]
    newline = b'\r\n' if b'\r\n' in before else b'\n'
    return text.encode('utf-8').replace(b'\n', newline)


def apply_decisions(before: bytes) -> bytes:
    text = before.decode('utf-8').replace('\r\n', '\n')
    old = map_states(source_text('donor_head', DECISIONS))
    new = map_states(source_text('donor_worktree', DECISIONS))
    if text.count(old) != 1:
        raise ValueError('industry decision ancestor differs beyond the approved port note')
    updated = text.replace(old, new, 1)
    newline = b'\r\n' if b'\r\n' in before else b'\n'
    return updated.encode('utf-8').replace(b'\n', newline)


def apply_locale(name: str, before: bytes) -> bytes:
    text = before.decode('utf-8-sig').replace('\r\n', '\n')
    edits = lock()['locale_edits'][name]
    before_source = {m[2]:m[3] for m in ROW.finditer(source_text('donor_head', KOREAN))}
    after_source = list(ROW.finditer(source_text('donor_worktree', KOREAN)))
    changed = {m[2] for m in after_source if before_source.get(m[2]) != m[3]}
    if set(edits) != changed or len(changed) != 16:
        raise ValueError(f'industry localisation source inventory drift: {name}')
    for source in after_source:
        key = source[2]
        if key not in edits: continue
        edit = edits[key]
        if name == KOREAN and edit['after'] != source[3]:
            raise ValueError(f'industry Korean source meaning drift: {key}')
        matches = [m for m in ROW.finditer(text) if m[2] == key]
        if edit['before'] is not None:
            if len(matches) != 1 or matches[0][3] != edit['before']:
                raise ValueError(f'industry localisation predecessor drift: {key}')
            match = matches[0]
            text = text[:match.start(3)] + edit['after'] + text[match.end(3):]
        else:
            if matches: raise ValueError(f'industry duplicate new localisation key: {key}')
            previous_key = after_source[after_source.index(source)-1][2]
            anchor = [m for m in ROW.finditer(text) if m[2] == previous_key]
            if len(anchor) != 1: raise ValueError(f'industry new-key anchor missing: {key}')
            at = anchor[0].end()
            text = text[:at] + '\n ' + key + ':0 "' + edit['after'] + '"' + text[at:]
    header, rest = text.split('\n', 1)
    text = header + '\n#20261110_kpopmodder: Describe the separate northern and southern state industry projects.\n' + rest
    newline = b'\r\n' if b'\r\n' in before else b'\n'
    return text.encode('utf-8-sig').replace(b'\n', newline)


def preview_outputs() -> dict[str, bytes]:
    verify_inputs()
    return {name: (apply_focus(previous_bytes(name)) if name == FOCUS else
                   apply_decisions(previous_bytes(name)) if name == DECISIONS else
                   apply_locale(name, previous_bytes(name))) for name in sorted(PATHS)}


@lru_cache(maxsize=1)
def build_outputs() -> dict[str, bytes]:
    result = preview_outputs()
    for name, data in result.items():
        record = lock()['outputs'][name]
        if sha(data) != record['sha256'] or len(data) != record['size']:
            raise ValueError(f'industry generated output drift: {name}')
    return result


def historical_bytes(relative: str | Path, data: bytes) -> bytes:
    name = canonical_name(relative)
    data = fission_historical(name, data)
    if name in PATHS and sha(data) == lock()['outputs'][name]['sha256']:
        if data != build_outputs()[name]: raise ValueError(f'industry final-output proof failed: {name}')
        return previous_bytes(name)
    return data


def finalize_one(relative: str | Path, data: bytes) -> bytes:
    name = canonical_name(relative)
    if name not in PATHS: return data
    record = lock()['outputs'][name]
    allowed = {record['previous_sha256'], record['sha256']}
    if name == FOCUS: allowed.add(fission_lock()['sha256'])
    if sha(data) not in allowed:
        raise ValueError(f'unreviewed industry predecessor: {name}')
    return current_outputs()[name]


def preflight_outputs(outputs: dict) -> None:
    seen = set()
    for relative, data in outputs.items():
        path = (ROOT / relative).resolve()
        name = canonical_name(path.relative_to(ROOT))
        if path in seen: raise ValueError(f'duplicate industry output: {name}')
        seen.add(path)
        if name not in PATHS: continue
        record = lock()['outputs'][name]
        if data != current_outputs()[name]: raise ValueError(f'unreviewed proposed industry bytes: {name}')
        allowed = {record['previous_sha256'], record['sha256']}
        if name == FOCUS: allowed.add(fission_lock()['sha256'])
        if not path.is_file() or sha(path.read_bytes()) not in allowed:
            raise ValueError(f'independently changed industry runtime: {name}')


def ledger_bytes(previous: bytes) -> bytes:
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
            raise ValueError(f'industry ledger ownership drift: {name}')
        touched.add(name)
        reason = ('; 2026-11-10 selected donor industry update: tools/hok_industry_update_lock.json; '
                  f'previous_output_sha256={record["previous_sha256"]}; '
                  'independent provincial investments and selected successor-state rewards; original authorship retained')
        if fission_historical(name, (ROOT / name).read_bytes()) != build_outputs()[name]:
            raise ValueError(f'industry ledger runtime differs: {name}')
        if row['output_sha256'] == record['sha256'] and row['reason'].endswith(reason):
            chunks.append(raw)
            continue
        if row['output_sha256'] != record['previous_sha256']:
            raise ValueError(f'industry ledger predecessor hash drift: {name}')
        row['output_sha256'] = record['sha256']
        row['reason'] += reason
        stream = io.StringIO(newline='')
        csv.DictWriter(stream, fieldnames=fields, lineterminator='\n').writerow(row)
        chunks.append(stream.getvalue().encode('utf-8'))
    if touched != PATHS: raise ValueError('industry ledger missing reviewed outputs')
    return b''.join(chunks)


#20261111_kpopmodder: Append one provenance revision after the unchanged equipment ledger, preserving every other row.
def fission_ledger_bytes(previous: bytes) -> bytes:
    config = fission_lock()
    if (ROOT / FOCUS).read_bytes() != current_outputs()[FOCUS]:
        raise ValueError('fission ledger runtime mismatch')
    lines = previous.splitlines(keepends=True)
    reader = csv.DictReader(io.StringIO(previous.decode('utf-8'), newline=''))
    fields = reader.fieldnames
    start, chunks, touched = reader.line_num, [lines[0]], 0
    reason = ('; 2026-11-11 selected donor nuclear research bonus: tools/hok_fission_update_lock.json; '
              f'previous_output_sha256={config["previous_sha256"]}; '
              'one 150% nuclear research bonus with existing two-year ahead reduction; original HOK authorship retained')
    for row in reader:
        raw = b''.join(lines[start:reader.line_num])
        start = reader.line_num
        if row['output_path'] != FOCUS:
            chunks.append(raw)
            continue
        touched += 1
        if row['integration_class'] != config['classification']:
            raise ValueError('fission ledger ownership drift')
        if row['output_sha256'] == config['sha256'] and row['reason'].endswith(reason):
            chunks.append(raw)
            continue
        if row['output_sha256'] != config['previous_sha256'] or reason in row['reason']:
            raise ValueError('fission ledger predecessor drift')
        row['output_sha256'] = config['sha256']
        row['reason'] += reason
        stream = io.StringIO(newline='')
        csv.DictWriter(stream, fieldnames=fields, lineterminator='\n').writerow(row)
        chunks.append(stream.getvalue().encode('utf-8'))
    if touched != 1: raise ValueError('fission ledger target is not unique')
    return b''.join(chunks)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        outputs = current_outputs()
        preflight_outputs(outputs)
        pending = [(ROOT / name, data) for name, data in outputs.items() if (ROOT / name).read_bytes() != data]
        if pending and not args.apply: raise ValueError('industry runtime mismatches: ' + ', '.join(str(p) for p,_ in pending))
        for path, data in pending: path.write_bytes(data)
        print(f'PASS industry/fission updates: 4 exact outputs; preserved industry delta plus one 150% nuclear research bonus; {len(pending)} written')
        return 0
    except (ValueError, KeyError, FileNotFoundError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
