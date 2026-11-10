#!/usr/bin/env python3
"""Reproduce the exact Korean host merge, English names, and reviewed dependency edge."""
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
import subprocess
import sys

#20261110_kpopmodder: Preserve HOK equipment names and explicitly name the RT56 successors without changing equipment or research.
ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / 'tools/hok_equipment_localisation_lock.json'
SNAPSHOT = ROOT / 'docs/upstream/hok-equipment-localisation-20261110'
LOCALES = ('english', 'korean')
CONFLICT_KEYS = (
    'KOR_motorized_equipment_1',
    'KOR_mechanized_equipment_1', 'KOR_mechanized_equipment_1_short',
    'KOR_mechanized_equipment_2', 'KOR_mechanized_equipment_2_short',
    'KOR_mechanized_equipment_3', 'KOR_mechanized_equipment_3_short',
    'KOR_amphibious_mechanized_equipment_1', 'KOR_amphibious_mechanized_equipment_1_short',
    'KOR_amphibious_mechanized_equipment_2', 'KOR_amphibious_mechanized_equipment_2_short',
    'KOR_motorized_rocket_equipment_1', 'KOR_motorized_rocket_equipment_1_short',
)
ADDITIONAL_KEYS = ('KOR_mechanized_equipment_x', 'KOR_mechanized_equipment_x_short',
                   'KOR_mechanized_equipment_x_2', 'KOR_mechanized_equipment_x_2_short')
GUARD_KEYS = ('KOR_motorized_equipment_0', 'KOR_motorized_equipment_0_short',
              'KOR_motorized_equipment_1_short')
ROW = re.compile(r'^\s*([^#\s][^:]*):([0-9]*)\s+"((?:[^"\\]|\\.)*)"\s*(?:#.*)?$')
TOKENS = re.compile(r'\$[^$\r\n]+\$|\[[^\]\r\n]+\]|§.|£[A-Za-z0-9_]+|\\[nrt"\\]')
NOTE = '#20261110_kpopmodder: Preserve HOK equipment names and name the RT56 successors in both languages.'
DESCRIPTOR = 'descriptor.mod'
DESCRIPTOR_NOTE = '#20261110_kpopmodder: Keep compatibility localisation after the active RT56 Korean translation.'
RTK_DEPENDENCY = 'The Road to 56 Korean Translation'
PREVIOUS_LEDGER_HASHES = (
    '45C2532953970A0EA5F6245349ABE6CECDECB4A9EBA3D4677761980B5B88DAE1',
    '7C507D6BF4E4FD0304061F6711A23485895BCE042B1655D1189C3060D774EC77',
    '58AC0D552EF271E4C16F815AE31529EF9588ED5B95B9BFBE1615E6ED5BE85811',
    '20C81600A57CD58A6B4181786E3B90FEA54EB4BEC707E32BC52DB683886FCD2E',
    '8B5C7E14A5180610D0042CD16B5FE00068D438B5A4A37FFCD5063D78A4F4D3F2',
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def original_path(locale: str) -> str:
    return f'localisation/{locale}/korea_equipment_l_{locale}.yml'


def output_path(locale: str) -> str:
    #20261110_kpopmodder: Keep the Korean exact-path merge proven with the explicit RTK dependency; retain the English payload.
    if locale == 'korean':
        return 'localisation/korean/replace/r56e_equip_motor_mech_l_korean.yml'
    return f'localisation/{locale}/replace/zz_HOK_KOR_equipment_overrides_l_{locale}.yml'


def superseded_output_path(locale: str) -> str:
    return f'localisation/{locale}/replace/HOK_KOR_equipment_overrides_l_{locale}.yml'


def superseded_paths() -> set[str]:
    return {superseded_output_path(locale) for locale in LOCALES} | {
        'localisation/replace/zz_HOK_KOR_equipment_overrides_l_korean.yml',
        'localisation/korean/replace/zz_HOK_KOR_equipment_overrides_l_korean.yml'}


def entries(data: bytes, locale: str) -> dict[str, tuple[str, str]]:
    if not data.startswith(b'\xef\xbb\xbfl_' + locale.encode() + b':'):
        raise ValueError(f'equipment locale BOM/header drift: {locale}')
    result = {}
    for number, line in enumerate(data.decode('utf-8-sig').splitlines(), 1):
        if not line.strip() or line.lstrip().startswith('#') or line == f'l_{locale}:':
            continue
        match = ROW.fullmatch(line)
        if match is None or match[1] in result:
            raise ValueError(f'equipment invalid/duplicate entry: {locale}:{number}')
        result[match[1]] = (match[2], match[3])
    return result


@lru_cache(maxsize=1)
def lock() -> dict:
    config = json.loads(LOCK_PATH.read_text(encoding='utf-8'))
    if (config.get('format') != 1 or config.get('revision') != '2026-11-10-equipment-localisation-v6-host-merge-dependency'
            or config.get('base_commit') != '2523bf455514c79a3538f0475dc922329afb185d'
            or tuple(config.get('conflict_keys', ())) != CONFLICT_KEYS
            or tuple(config.get('additional_keys', ())) != ADDITIONAL_KEYS
            or tuple(config.get('guard_keys', ())) != GUARD_KEYS
            or set(config.get('outputs', {})) != {output_path(locale) for locale in LOCALES} | {DESCRIPTOR}
            or set(config.get('superseded_outputs', {})) != superseded_paths()
            or config.get('filename_candidate', {}).get('previous_ledger_sha256') != PREVIOUS_LEDGER_HASHES[-1]
            or tuple(config.get('accepted_previous_ledger_sha256', ())) != PREVIOUS_LEDGER_HASHES
            or config.get('descriptor_input', {}).get('commit') != '2523bf455514c79a3538f0475dc922329afb185d'
            or config.get('descriptor_input', {}).get('blob') != '4c1fd9af7d752bef207285980fe9854a4f4086bd'
            or config.get('descriptor_input', {}).get('before_sha256') != 'AA150D6CE82A7779C3D4C3FCDC962A82FA269327F005330B565723CA87BBE247'
            or config.get('descriptor_input', {}).get('checkout') != 'raw'
            or config.get('korean_host_merge', {}).get('snapshot') != 'host/translation/localisation/korean/replace/r56e_equip_motor_mech_l_korean.yml'
            or config.get('korean_host_merge', {}).get('sha256') != '322541C886E096ECDC4C6F9EEA9DCE36EDA29911010EEE3B7B4AB482C0072974'
            or config.get('korean_host_merge', {}).get('entry_count') != 1308
            or config.get('korean_host_merge', {}).get('changed_kor_count') != 17
            or config.get('korean_host_merge', {}).get('preserved_non_kor_count') != 1291
            or not re.fullmatch(r'[A-F0-9]{64}', config.get('descriptor_projected_ledger_sha256', ''))):
        raise ValueError('unreviewed equipment localisation revision or scope')
    return config


def frozen(relative: str, expected: str) -> bytes:
    path = (SNAPSHOT / relative).resolve()
    path.relative_to(SNAPSHOT.resolve())
    data = path.read_bytes()
    if sha(data) != expected:
        raise ValueError(f'equipment frozen source drift: {relative}')
    return data


def original_bytes(locale: str) -> bytes:
    record = lock()['originals'][locale]
    return frozen(record['snapshot'], record['sha256'])


#20261110_kpopmodder: Preserve the exact translation input and prove that only the seventeen reviewed value spans change.
def korean_host_bytes() -> bytes:
    record = lock()['korean_host_merge']
    return frozen(record['snapshot'], record['sha256'])


def _korean_projection(data: bytes, *, has_note: bool) -> bytes:
    lines = data.decode('utf-8-sig').splitlines(keepends=True)
    if has_note:
        if len(lines) < 2 or lines[1] != NOTE + '\n':
            raise ValueError('equipment Korean merge contributor note drift')
        del lines[1]
    seen = set()
    for index, line in enumerate(lines):
        match = ROW.fullmatch(line.removesuffix('\n').removesuffix('\r'))
        if match and match[1] in (*CONFLICT_KEYS, *ADDITIONAL_KEYS):
            if match[1] in seen:
                raise ValueError('equipment Korean merge repeated target')
            seen.add(match[1])
            lines[index] = line[:match.start(3)] + '<HOK_KOR_EQUIPMENT_VALUE>' + line[match.end(3):]
    if seen != set(CONFLICT_KEYS) | set(ADDITIONAL_KEYS):
        raise ValueError('equipment Korean merge target coverage drift')
    return ''.join(lines).encode('utf-8-sig')


def verify_korean_merge(before: bytes, after: bytes, names: dict[str, tuple[str, str]]) -> None:
    source, merged = entries(before, 'korean'), entries(after, 'korean')
    if (len(source) != lock()['korean_host_merge']['entry_count'] or source.keys() != merged.keys()
            or {key for key in source if key.startswith('KOR_')} != names.keys()
            or sum(not key.startswith('KOR_') for key in source) != lock()['korean_host_merge']['preserved_non_kor_count']):
        raise ValueError('equipment Korean merged host key inventory drift')
    for key, value in source.items():
        if merged[key] != names.get(key, value):
            raise ValueError(f'equipment Korean merged value drift: {key}')
    if {key for key in source if source[key] != merged[key]} != names.keys():
        raise ValueError('equipment Korean merge semantic delta is not exactly the seventeen reviewed names')
    if _korean_projection(before, has_note=False) != _korean_projection(after, has_note=True):
        raise ValueError('equipment Korean merge changed bytes beyond its seventeen values and contributor note')


def _merge_korean_host(names: dict[str, tuple[str, str]]) -> bytes:
    before = korean_host_bytes()
    lines = before.decode('utf-8-sig').splitlines(keepends=True)
    for index, line in enumerate(lines):
        match = ROW.fullmatch(line.removesuffix('\n').removesuffix('\r'))
        if match and match[1] in names:
            version, value = names[match[1]]
            if version != match[2]:
                raise ValueError('equipment Korean host target version differs from HOK')
            lines[index] = line[:match.start(3)] + value + line[match.end(3):]
    if not lines or lines[0] != 'l_korean:\n' or any(line.rstrip('\r\n') == NOTE for line in lines):
        raise ValueError('equipment Korean host header or original note drift')
    lines.insert(1, NOTE + '\n')
    after = ''.join(lines).encode('utf-8-sig')
    verify_korean_merge(before, after, names)
    return after


#20261110_kpopmodder: Derive the descriptor from its exact immutable Git bytes and admit only the reviewed dependency insertion.
@lru_cache(maxsize=1)
def descriptor_before() -> bytes:
    config = lock()
    record = config['descriptor_input']
    command = ['git', '-C', str(config['roots']['compat'])]
    blob = subprocess.check_output(command + ['rev-parse', record['commit'] + ':' + DESCRIPTOR]).decode().strip()
    raw = subprocess.check_output(command + ['cat-file', 'blob', record['blob']])
    if (blob != record['blob'] or sha(raw) != record['object_sha256'] or len(raw) != record['object_size']
            or sha(raw) != record['before_sha256'] or len(raw) != record['before_size'] or b'\r' in raw):
        raise ValueError('equipment descriptor immutable input drift')
    return raw


def descriptor_bytes() -> bytes:
    before = descriptor_before()
    anchor = b'\t"Korean Language"\n'
    addition = ('\t' + DESCRIPTOR_NOTE + '\n\t"' + RTK_DEPENDENCY + '"\n').encode('utf-8')
    if before.count(anchor) != 1 or RTK_DEPENDENCY.encode() in before:
        raise ValueError('equipment descriptor dependency anchor drift')
    data = before.replace(anchor, anchor + addition, 1)
    record = lock()['outputs'][DESCRIPTOR]
    if sha(data) != record['sha256'] or len(data) != record['size'] or record['classification'] != 'OVERRIDE':
        raise ValueError('equipment descriptor registered output drift')
    return data


def descriptor_historical_bytes(relative: str | Path, data: bytes) -> bytes:
    """Reverse only the exact generated descriptor; leave every unknown payload raw."""
    if str(relative).replace('\\', '/').casefold() != DESCRIPTOR:
        return data
    return descriptor_before() if data == descriptor_bytes() else data


def _manifests(acf: str, item: str) -> list[str]:
    blocks = re.findall('"' + re.escape(item) + r'"\s*\{([^{}]+)\}', acf)
    return [value for block in blocks for value in re.findall(r'"(?:latest_)?manifest"\s*"(\d+)"', block)]


def verify_inputs() -> None:
    config = lock()
    manifest = json.loads(frozen('source-manifest.json', config['source_manifest_sha256']))
    for record in manifest['files'].values():
        frozen(record['snapshot'], record['sha256'])
    for locale in LOCALES:
        original = original_bytes(locale)
        if (ROOT / original_path(locale)).read_bytes() != original:
            raise ValueError(f'preserved HOK equipment source drift: {locale}')
    for relative, record in config['physical_inputs'].items():
        actual = (Path(config['roots'][record['provider']]) / record['relative']).read_bytes()
        if sha(actual) != record['sha256']:
            raise ValueError(f'equipment physical source drift: {record["provider"]}/{relative}')
    host = Path(config['roots']['rt56'])
    acf = (host.parents[2] / 'appworkshop_394360.acf').read_text(encoding='utf-8-sig')
    for item, expected in config['workshop_manifests'].items():
        values = _manifests(acf, item)
        if len(values) < 2 or any(value != expected for value in values):
            raise ValueError(f'equipment installed/latest manifest drift: {item}')
    game = json.loads((Path(config['roots']['vanilla']) / 'launcher-settings.json').read_text(encoding='utf-8-sig'))
    if game['version'] != config['game_version']:
        raise ValueError('equipment installed game-version drift')


def preview_outputs() -> dict[str, bytes]:
    verify_inputs()
    config = lock()
    result = {}
    for locale in LOCALES:
        source = entries(original_bytes(locale), locale)
        if any(key not in source for key in (*CONFLICT_KEYS, *GUARD_KEYS)) or any(key in source for key in ADDITIONAL_KEYS):
            raise ValueError(f'equipment original key inventory drift: {locale}')
        additions = config['new_values'][locale]
        if set(additions) != set(ADDITIONAL_KEYS):
            raise ValueError(f'equipment successor-name scope drift: {locale}')
        rows = [f'l_{locale}:', NOTE]
        for key in CONFLICT_KEYS:
            version, value = source[key]
            rows.append(f' {key}:{version} "{value}"')
        for key in ADDITIONAL_KEYS:
            value = additions[key]
            if not value or '"' in value or '\n' in value or TOKENS.search(value):
                raise ValueError(f'equipment invalid successor name: {locale}/{key}')
            rows.append(f' {key}:0 "{value}"')
        data = ('\r\n'.join(rows) + '\r\n').encode('utf-8-sig')
        parsed = entries(data, locale)
        if tuple(parsed) != (*CONFLICT_KEYS, *ADDITIONAL_KEYS):
            raise ValueError('equipment override key order/scope drift')
        if locale == 'english' and re.search(r'[\u1100-\u11ff\u3130-\u318f\uac00-\ud7ff]', data.decode('utf-8-sig')):
            raise ValueError('Korean text in equipment English output')
        result[output_path(locale)] = _merge_korean_host(parsed) if locale == 'korean' else data
    english, korean = (entries(result[output_path(locale)], locale) for locale in LOCALES)
    for key in english:
        if english[key][0] != korean[key][0] or Counter(TOKENS.findall(english[key][1])) != Counter(TOKENS.findall(korean[key][1])):
            raise ValueError(f'equipment paired version/token drift: {key}')
    result[DESCRIPTOR] = descriptor_bytes()
    return result


@lru_cache(maxsize=1)
def build_outputs() -> dict[str, bytes]:
    outputs = preview_outputs()
    for relative, data in outputs.items():
        record = lock()['outputs'][relative]
        expected_class = 'OVERRIDE' if relative == DESCRIPTOR else ('THREE_WAY_MERGE' if relative == output_path('korean') else 'ADD')
        if record['classification'] != expected_class or sha(data) != record['sha256'] or len(data) != record['size']:
            raise ValueError(f'equipment registered output drift: {relative}')
    return outputs


def intentional_duplicate(locale: str, key: str, paths: set[str]) -> bool:
    """Admit only the proven original/override pair; never arbitrary collisions."""
    locale = locale.removeprefix('l_')
    if locale not in LOCALES or key not in CONFLICT_KEYS:
        return False
    canonical = {str(path).replace('\\', '/') for path in paths}
    if canonical != {original_path(locale), output_path(locale)}:
        return False
    original = original_bytes(locale)
    if (ROOT / original_path(locale)).read_bytes() != original:
        return False
    outputs = build_outputs()
    if (ROOT / output_path(locale)).read_bytes() != outputs[output_path(locale)]:
        return False
    old = entries(original, locale)
    new = entries(outputs[output_path(locale)], locale)
    return old[key] == new[key]


def preflight(outputs: dict[str, bytes]) -> None:
    if set(outputs) != set(lock()['outputs']):
        raise ValueError('equipment writer output inventory drift')
    for relative, data in outputs.items():
        record = lock()['outputs'][relative]
        if sha(data) != record['sha256'] or len(data) != record['size']:
            raise ValueError(f'unregistered proposed equipment or descriptor bytes: {relative}')
        path = ROOT / relative
        if path.exists() and path.read_bytes() != data:
            if relative != DESCRIPTOR or path.read_bytes() != descriptor_before():
                raise ValueError(f'refusing independently changed equipment output: {relative}')
        if relative == DESCRIPTOR and not path.is_file():
            raise ValueError('equipment descriptor unexpectedly missing or not a regular file')
    #20261110_kpopmodder: Retire only exact generated predecessor files, preserving the active English path and any independent edit.
    for relative, record in lock()['superseded_outputs'].items():
        path = ROOT / relative
        if path.exists():
            raw = path.read_bytes()
            if sha(raw) != record['sha256'] or len(raw) != record['size']:
                raise ValueError(f'refusing independently changed superseded equipment output: {relative}')


def _ledger_parts(data: bytes) -> tuple[bytes, list[str], list[dict], list[bytes]]:
    reader = csv.DictReader(io.StringIO(data.decode('utf-8'), newline=''))
    fields = reader.fieldnames
    if not fields or not {'source_path', 'output_path', 'integration_class', 'reason', 'output_sha256'}.issubset(fields):
        raise ValueError('equipment ledger schema drift')
    lines = data.splitlines(keepends=True)
    start = reader.line_num
    header = b''.join(lines[:start])
    rows, chunks = [], []
    for row in reader:
        rows.append(row)
        chunks.append(b''.join(lines[start:reader.line_num]))
        start = reader.line_num
    return header, fields, rows, chunks


def _ledger_row(row: dict, fields: list[str]) -> bytes:
    stream = io.StringIO(newline='')
    csv.DictWriter(stream, fieldnames=fields, lineterminator='\n').writerow(row)
    return stream.getvalue().encode('utf-8')


#20261110_kpopmodder: Preserve the immutable 1541-row ledger while projecting only the two approved descriptor cells.
def preview_descriptor_ledger_base() -> bytes:
    before = frozen('ledger_before.csv', lock()['ledger_before_sha256'])
    header, fields, rows, chunks = _ledger_parts(before)
    matches = [i for i, row in enumerate(rows) if row['source_path'] == DESCRIPTOR]
    if len(rows) != 1541 or len(matches) != 1:
        raise ValueError('equipment descriptor ledger identity drift')
    index = matches[0]
    old = rows[index]
    if (old['output_path'] != DESCRIPTOR or old['integration_class'] != 'OVERRIDE'
            or old['status'] != 'SHIPPED' or old['output_sha256'] != sha(descriptor_before())):
        raise ValueError('equipment descriptor ledger ancestor drift')
    updated = dict(old)
    updated['output_sha256'] = sha(descriptor_bytes())
    updated['reason'] += ('; 2026-11-10 equipment localisation ordering edge: tools/hok_equipment_localisation_lock.json; '
                          'previous_output_sha256=' + sha(descriptor_before()) + '; '
                          'added_dependency=The Road to 56 Korean Translation; existing dependencies, identity and other descriptor fields retained')
    if {field for field in fields if old[field] != updated[field]} != {'output_sha256', 'reason'}:
        raise ValueError('equipment descriptor ledger projection changed an unapproved field')
    chunks[index] = _ledger_row(updated, fields)
    return header + b''.join(chunks)


def descriptor_ledger_base() -> bytes:
    data = preview_descriptor_ledger_base()
    if sha(data) != lock()['descriptor_projected_ledger_sha256']:
        raise ValueError('equipment registered descriptor ledger projection drift')
    return data


def _locale_ledger_rows(fields: list[str]) -> bytes:
    config = lock()
    outputs = build_outputs()
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
    for locale in LOCALES:
        relative = output_path(locale)
        original = config['originals'][locale]
        classification = config['outputs'][relative]['classification']
        row = {field: '' for field in fields}
        row.update(source_path=relative, output_path=relative, integration_class=classification,
                   status='GENERATED' if classification == 'THREE_WAY_MERGE' else 'SHIPPED',
                   exact_path_rt56_collision='no', output_sha256=sha(outputs[relative]),
                   reason=('2026-11-10 HOK equipment localisation; generator=tools/korean_equipment_localisation.py; '
                           'lock=tools/hok_equipment_localisation_lock.json; '
                           f'preserved_compat_source={original_path(locale)}; preserved_source_sha256={original["sha256"]}; '
                           '13 inherited HOK names and four compatibility-authored 1949/1953 names; '
                           'logical KOR overrides only; original HOK and translation authorship retained; '
                           'source capsule=docs/upstream/hok-equipment-localisation-20261110'))
        if locale == 'korean':
            row['reason'] += ('; exact translation-provider path merge; host_provider=RT56 Korean Translation; '
                              'host_base_sha256=' + config['korean_host_merge']['sha256'] + '; '
                              '1308 host keys retained, only 17 KOR values replaced, 1291 non-KOR values and raw bytes retained; '
                              'selected Korean configuration requires RTK; Korean without RTK is outside the preservation claim; '
                              'translation contributors retain authorship; public redistribution permission not established by this local merge; '
                              'v6 restores the exact v4 Korean payload after narrow v5 KO06 UI failure; '
                              'the registered descriptor retains the RTK dependency sufficient for KO05 nine-observable control')
        writer.writerow(row)
    return stream.getvalue().encode('utf-8')


def ledger_bytes(previous: bytes) -> bytes:
    """Project one descriptor row and append two exact localisation rows; reject all other changes."""
    config = lock()
    for relative, data in build_outputs().items():
        if (ROOT / relative).read_bytes() != data:
            raise ValueError(f'equipment ledger runtime mismatch: {relative}')
    old_base = frozen('ledger_before.csv', config['ledger_before_sha256'])
    new_base = descriptor_ledger_base()
    header, fields, rows, chunks = _ledger_parts(previous)
    if fields != _ledger_parts(old_base)[1]:
        raise ValueError('equipment ledger field inventory drift')
    # Descriptor is an existing row, not part of the two-row localisation tail.
    task_names = {output_path(locale) for locale in LOCALES} | config['superseded_outputs'].keys()
    first = next((i for i, row in enumerate(rows) if row['output_path'] in task_names), None)
    base = previous if first is None else header + b''.join(chunks[:first])
    if base not in (old_base, new_base):
        raise ValueError('equipment ledger base differs outside the exact descriptor projection')
    expected = new_base + _locale_ledger_rows(fields)
    if previous == expected:
        return previous
    if first is not None and sha(previous) not in config['accepted_previous_ledger_sha256']:
        raise ValueError('equipment existing task rows differ from registered migration')
    return expected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        outputs = build_outputs()
        preflight(outputs)
        pending = [(ROOT / name, data) for name, data in outputs.items()
                   if not (ROOT / name).is_file() or (ROOT / name).read_bytes() != data]
        superseded = [(ROOT / name, record) for name, record in lock()['superseded_outputs'].items() if (ROOT / name).exists()]
        if not args.apply and (pending or superseded):
            raise ValueError('equipment override filenames differ from the registered candidate; missing=' +
                             ', '.join(str(path) for path,_ in pending) + '; superseded=' +
                             ', '.join(str(path) for path,_ in superseded))
        for path, data in pending:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        for path, record in superseded:
            raw = path.read_bytes()
            if sha(raw) != record['sha256'] or len(raw) != record['size']:
                raise ValueError(f'superseded equipment output changed before retirement: {path}')
            path.unlink()
        print(f'PASS equipment localisation: English17 names, Korean1308 keys with17 KOR values changed and1291 non-KOR raw records preserved, and exact dependency descriptor; 13 bounded duplicate pairs, 3 preserved guards; {len(pending)} written, {len(superseded)} exact predecessor files retired; source checks do not prove actual load order')
        return 0
    except (ValueError, KeyError, FileNotFoundError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
