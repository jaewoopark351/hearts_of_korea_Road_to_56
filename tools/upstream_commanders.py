#!/usr/bin/env python3
"""Reproduce the selected Korean commander unlock and legacy-save guard."""
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

#20261114_kpopmodder: Keep the five-file commander delta terminal and reversible above unchanged source pins.
ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / 'docs/upstream/hok-commander-unlock-20261114'
LOCK_PATH = ROOT / 'tools/hok_commander_unlock_lock.json'
CHARACTERS = 'common/characters/KOR.txt'
FOCUS = 'common/national_focus/korea.txt'
HISTORY = 'history/countries/KOR - Korea.txt'
ENGLISH = 'localisation/english/HoK_start_game_setup_l_english.yml'
KOREAN = 'localisation/korean/HoK_start_game_setup_l_korean.yml'
PATHS = frozenset((CHARACTERS, FOCUS, HISTORY, ENGLISH, KOREAN))
IDS = ('KOR_Beomdo_Hong', 'KOR_Jwajin_Kim', 'KOR_Junggeun_Ahn')
TARGET = 'KOR_prepare_for_the_next_war'
MARKER = 'HOK_KOR_commander_focus_unlock_v1'
NOTE = b'#20261114_kpopmodder: Move the three commanders\' unlock notice to the next-war focus.'


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def canonical_name(relative: str | Path) -> str:
    path = (ROOT / Path(str(relative).replace('\\', '/'))).resolve()
    name = path.relative_to(ROOT.resolve()).as_posix()
    return next((p for p in PATHS if p.casefold() == name.casefold()), name)


@lru_cache(maxsize=1)
def lock() -> dict:
    config = json.loads(LOCK_PATH.read_text(encoding='utf-8'))
    if (config.get('format') != 1 or config.get('revision') != '2026-11-14-commander-unlock-v1'
            or config.get('base_commit') != 'b5308a027385cc021243a443ff49b728707e081e'
            or config.get('source_commit') != '0c19f58fa7a9ff898196dcdbe46edfd0ad5fdbbc'
            or config.get('ancestor_commit') != '065b5550448d6415901456503ef28b27f4530cc1'
            or config.get('workshop_manifest') != '1963361040482473746'
            or config.get('game_version') != 'Operation Postern v1.19.5.0.7c6c (c184)'
            or set(config.get('outputs', {})) != PATHS):
        raise ValueError('unreviewed commander source, host or output inventory')
    for name, record in config['outputs'].items():
        if (record.get('previous_snapshot') != 'compat_before/' + name
                or record.get('classification') != ({CHARACTERS:'THREE_WAY_MERGE', FOCUS:'THREE_WAY_MERGE',
                    HISTORY:'OVERRIDE', ENGLISH:'ADD', KOREAN:'ADD'}[name])
                or any(not re.fullmatch('[A-F0-9]{64}', record.get(k, '')) for k in ('sha256', 'previous_sha256'))):
            raise ValueError(f'unreviewed commander output contract: {name}')
    return config


def frozen(relative: str, expected: str, size: int | None = None) -> bytes:
    path = (SNAPSHOT / relative).resolve()
    path.relative_to(SNAPSHOT.resolve())
    data = path.read_bytes()
    if sha(data) != expected or (size is not None and len(data) != size):
        raise ValueError(f'commander frozen input drift: {relative}')
    return data


@lru_cache(maxsize=1)
def manifest() -> dict:
    config = lock()
    result = json.loads(frozen('source-manifest.json', config['source_manifest_sha256']))
    if (result.get('source_commit') != config['source_commit']
            or result.get('ancestor_commit') != config['ancestor_commit']
            or result.get('compatibility_base_commit') != config['base_commit']
            or set(result.get('sources', {})) != PATHS
            or set(result.get('predecessors', {})) != PATHS
            or set(result.get('documents', {})) != {'docs/HOK_KOREAN_COMMANDER_UNLOCK_TRANSFER_PLAN.md',
                'docs/HOK_KOREAN_SECOND_WAVE_PLAN.md', 'docs/incidents/2026-11-14-korean-commander-unlock-transfer.md'}):
        raise ValueError('commander source manifest inventory drift')
    for name, records in result['sources'].items():
        if set(records) != {'before', 'after'}: raise ValueError(f'commander source pair drift: {name}')
        for stage, record in records.items():
            if record['snapshot'] != ('before/' if stage == 'before' else 'runtime/') + name:
                raise ValueError(f'commander source path drift: {name}')
            frozen(record['snapshot'], record['sha256'], record['size'])
    for name, record in result['predecessors'].items():
        expected = config['outputs'][name]
        if record['snapshot'] != expected['previous_snapshot'] or record['sha256'] != expected['previous_sha256']:
            raise ValueError(f'commander predecessor contract drift: {name}')
        frozen(record['snapshot'], record['sha256'], record['size'])
    for record in result['documents'].values(): frozen(record['snapshot'], record['sha256'], record['size'])
    roots = {'RT56':Path(config['rt56_root']), 'VANILLA':Path(config['vanilla_root'])}
    if set(result.get('references', {})) != {
            'RT56/descriptor.mod', 'RT56/common/characters/KOR.txt', 'RT56/common/national_focus/korea.txt',
            'VANILLA/launcher-settings.json', 'VANILLA/documentation/triggers_documentation.md',
            'VANILLA/documentation/effects_documentation.md', 'VANILLA/common/characters/BEL.txt',
            'VANILLA/common/characters/SPR.txt', 'VANILLA/common/national_focus/belgium.txt'}:
        raise ValueError('commander host/schema reference inventory drift')
    for name, record in result['references'].items():
        provider, relative = name.split('/', 1)
        root = roots[provider].resolve()
        path = (root / relative).resolve()
        path.relative_to(root)
        raw = path.read_bytes()
        if (str(path) != record['original_path'] or sha(raw) != record['sha256'] or len(raw) != record['size']):
            raise ValueError(f'commander installed reference drift: {name}')
    game = json.loads((roots['VANILLA'] / 'launcher-settings.json').read_text(encoding='utf-8-sig'))
    if game['version'] != config['game_version']: raise ValueError('commander installed game version drift')
    acf = (roots['RT56'].parents[2] / 'appworkshop_394360.acf').read_text(encoding='utf-8-sig')
    entries = [dict(re.findall(r'"([^"\r\n]+)"\s*"([^"]*)"', body))
               for body in re.findall(r'"820260968"\s*\{([^}]+)\}', acf)]
    if (len(entries) != 2 or any(e.get('manifest') != config['workshop_manifest'] for e in entries)
            or entries[-1].get('latest_manifest') != config['workshop_manifest']):
        raise ValueError('commander installed/latest RT56 Workshop manifest drift')
    return result


def previous_bytes(relative: str) -> bytes:
    record = lock()['outputs'][relative]
    return frozen(record['previous_snapshot'], record['previous_sha256'])


def replace_once(data: bytes, before: bytes, after: bytes, label: str) -> bytes:
    if data.count(before) != 1: raise ValueError(f'ambiguous commander delta: {label}')
    return data.replace(before, after, 1)


def block_end(data: bytes, opening: int) -> int:
    depth, quoted, escaped, comment = 0, False, False, False
    for index in range(opening, len(data)):
        char = data[index]
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
    raise ValueError('unclosed commander source block')


def named_block(data: bytes, identifier: str) -> tuple[int, int]:
    hits = list(re.finditer(rb'(?m)^\t' + re.escape(identifier.encode()) + rb'\s*=\s*\{', data))
    if len(hits) != 1: raise ValueError(f'ambiguous commander character: {identifier}')
    hit = hits[0]
    return hit.start(), block_end(data, data.index(b'{', hit.start(), hit.end()))


def character_delta(data: bytes, before: bytes, after: bytes) -> tuple[bytes, bytes]:
    proof = before
    for identifier in IDS:
        start, end = named_block(before, identifier)
        old = before[start:end]
        start, end = named_block(after, identifier)
        new = after[start:end]
        proof = replace_once(proof, old, new, identifier + '/donor')
        start, end = named_block(data, identifier)
        current = data[start:end]
        if current.replace(b'\r\n', b'\n') != old:
            raise ValueError(f'unreviewed commander character predecessor: {identifier}')
        newline = b'\r\n' if b'\r\n' in current else b'\n'
        data = data[:start] + new.replace(b'\n', newline) + data[end:]
    return data, proof


def focus_delta(data: bytes) -> bytes:
    newline = b'\r\n' if b'\r\n' in data else b'\n'
    # The historical focus preserves spaces before this line; anchor its content rather than indentation.
    hits = list(re.finditer(rb'(?m)^([\t ]*)show_ideas_tooltip = beomdo_hong\r?$', data))
    if len(hits) != 1: raise ValueError('commander target focus tooltip anchor drift')
    hit = hits[0]
    insertion = newline.join((b'', b'\t\t\t#20261114_kpopmodder: Show the three military roles unlocked by this focus.',
                             *(b'\t\t\tshow_unit_leaders_tooltip = ' + name.encode() for name in IDS)))
    # Match.end includes the CR in CRLF; append after the complete existing line ending.
    end = hit.end() - (1 if data[hit.end()-1:hit.end()] == b'\r' else 0)
    return data[:end] + insertion + data[end:]


def history_delta(data: bytes) -> bytes:
    newline = b'\r\n' if b'\r\n' in data else b'\n'
    anchor = b'##Korean start setup###'
    insertion = newline.join((b'#20261114_kpopmodder: Mark new games for focus-based commander unlocks while preserving legacy saves.',
                              b'set_country_flag = ' + MARKER.encode(), b'', anchor))
    return replace_once(data, anchor, insertion, 'new-game history marker')


def locale_delta(data: bytes, *, english: bool = False) -> bytes:
    newline = b'\r\n' if b'\r\n' in data else b'\n'
    header = b'l_english:' if english else b'l_korean:'
    data = replace_once(data, header + newline, header + newline + NOTE + newline, 'paired locale contributor note')
    pattern = rb'(?m)^( GOOKPPONG_ENABLED_TEXT_DESC:0 ")([^\r\n]*)("\r?$)'
    rows = list(re.finditer(pattern, data))
    if len(rows) != 1: raise ValueError('commander setup description key drift')
    row = rows[0]
    removed = (b' It also gains the capable generals Hong Beom-do, Kim Jwa-jin and Ahn Jung-geun, who are unavailable in the normal Korean start.'
               if english else ', 그리고 기존 한국에는 없는 좋은 성능의 장군 홍범도, 김좌진, 안중근을 추가로 가지고 시작합니다.'.encode())
    replacement = b'' if english else '을 가지고 시작합니다.'.encode()
    value = replace_once(row[2], removed, replacement, 'commander-only option promise')
    return data[:row.start(2)] + value + data[row.end(2):]


def preview_outputs() -> dict[str, bytes]:
    records = manifest()['sources']
    result = {}
    for name in sorted(PATHS):
        pair = {stage:frozen(record['snapshot'], record['sha256'], record['size']).replace(b'\r\n', b'\n')
                for stage,record in records[name].items()}
        before, after = pair['before'], pair['after']
        current = previous_bytes(name)
        if name == CHARACTERS:
            output, proof = character_delta(current, before, after)
        elif name == FOCUS:
            output, proof = focus_delta(current), focus_delta(before)
        elif name == HISTORY:
            output, proof = history_delta(current), history_delta(before)
        else:
            output = locale_delta(current, english=name == ENGLISH)
            # Both donor channels contain Korean; translate only the actual English output.
            proof = locale_delta(before.replace(b'l_english:', b'l_korean:'))
            if name == ENGLISH: proof = proof.replace(b'l_korean:', b'l_english:')
        if proof != after: raise ValueError(f'donor commander delta extends beyond reviewed hunks: {name}')
        result[name] = output
    return result


@lru_cache(maxsize=1)
def build_outputs() -> dict[str, bytes]:
    result = preview_outputs()
    for name, data in result.items():
        record = lock()['outputs'][name]
        if sha(data) != record['sha256'] or len(data) != record['size']:
            raise ValueError(f'commander generated output drift: {name}')
    return result


def historical_bytes(relative: str | Path, data: bytes) -> bytes:
    name = canonical_name(relative)
    if name in PATHS and sha(data) == lock()['outputs'][name]['sha256']:
        if data != build_outputs()[name]: raise ValueError(f'commander final-output proof failed: {name}')
        return previous_bytes(name)
    return data


def finalize_one(relative: str | Path, data: bytes) -> bytes:
    name = canonical_name(relative)
    if name not in PATHS: return data
    final = build_outputs()[name]
    if data not in (previous_bytes(name), final): raise ValueError(f'unreviewed commander predecessor: {name}')
    return final


def preflight_outputs(outputs: dict) -> None:
    seen = set()
    for relative, data in outputs.items():
        name = canonical_name(relative)
        if name not in PATHS: continue
        if name in seen: raise ValueError(f'duplicate commander output: {name}')
        seen.add(name)
        final = build_outputs()[name]
        if data != final: raise ValueError(f'unregistered proposed commander bytes: {name}')
        path = ROOT / name
        if not path.is_file() or path.read_bytes() not in (previous_bytes(name), final):
            raise ValueError(f'independently changed commander runtime: {name}')


def ledger_bytes(previous: bytes) -> bytes:
    config, outputs = lock(), build_outputs()
    if any((ROOT / name).read_bytes() != data for name,data in outputs.items()):
        raise ValueError('commander ledger/runtime mismatch')
    reader = csv.DictReader(io.StringIO(previous.decode('utf-8'), newline=''))
    fields = reader.fieldnames
    if not fields or not {'source_path', 'output_path', 'output_sha256', 'integration_class', 'reason'} <= set(fields):
        raise ValueError('commander ledger schema drift')
    lines, start, seen = previous.splitlines(keepends=True), reader.line_num, set()
    chunks = [b''.join(lines[:start])]
    for row in reader:
        raw, start = b''.join(lines[start:reader.line_num]), reader.line_num
        selected = set(row['output_path'].split(' | ')) & PATHS
        if not selected: chunks.append(raw); continue
        if len(selected) != 1: raise ValueError('ambiguous commander ledger row')
        name = selected.pop()
        record = config['outputs'][name]
        if name in seen or row['source_path'] != name or row['integration_class'] != record['classification']:
            raise ValueError(f'commander ledger ownership drift: {name}')
        seen.add(name)
        suffix = ('; 2026-11-14 selected commander unlock: tools/hok_commander_unlock_lock.json'
                  '; donor=' + config['source_commit'] + '; focus completion or unmarked legacy Super-Korea save'
                  '; previous_output_sha256=' + record['previous_sha256'] + '; original HOK authorship retained')
        old_hash, new_hash = record['previous_sha256'], record['sha256']
        if name == CHARACTERS:
            old_hash, new_hash = name + '=' + old_hash, name + '=' + new_hash
        current = row['output_sha256']
        if new_hash in current and row['reason'].endswith(suffix): chunks.append(raw); continue
        parts = current.split(' | ')
        if parts.count(old_hash) != 1 or suffix in row['reason']:
            raise ValueError(f'commander ledger predecessor drift: {name}')
        parts[parts.index(old_hash)] = new_hash
        row['output_sha256'], row['reason'] = ' | '.join(parts), row['reason'] + suffix
        stream = io.StringIO(newline='')
        newline = '\r\n' if raw.endswith(b'\r\n') else '\n'
        csv.DictWriter(stream, fieldnames=fields, lineterminator=newline).writerow(row)
        chunks.append(stream.getvalue().encode('utf-8'))
    if seen != PATHS: raise ValueError('commander ledger missing reviewed rows')
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
        pending = [(ROOT/name,data) for name,data in outputs.items() if (ROOT/name).read_bytes() != data]
        if pending and not args.apply: raise ValueError('commander runtime differs from reviewed output')
        for path,data in pending: path.write_bytes(data)
        print(f'PASS commander unlock: 3 military roles; 5 exact outputs; {len(pending)} written')
        return 0
    except (ValueError, KeyError, OSError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__': raise SystemExit(main())
