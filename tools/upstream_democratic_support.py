#!/usr/bin/env python3
"""Reproduce the selected democratic support, intelligence and Shandong port."""
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

#20261120_kpopmodder: Keep the reviewed democratic module terminal, reproducible and reversible over the existing RT56 port.
ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / 'docs/upstream/hok-democratic-support-20261120'
LOCK_PATH = ROOT / 'tools/hok_democratic_support_lock.json'
MAPPING_PATH = ROOT / 'docs/data/HOK_KOREAN_CHINESE_GOVERNMENT_RT56_MAPPING.json'
FOCUS = 'common/national_focus/korea.txt'
DECISIONS = 'common/decisions/KOR_decision.txt'
AI = 'common/ai_strategy_plans/KOR_historical_strategy_plan.txt'
HISTORY = 'history/countries/KCH - Korean China.txt'
JAPANESE_EFFECTS = 'common/scripted_effects/HOK_KOR_democratic_intelligence_effects.txt'
JAPANESE_NONLEADER_ADAPTATION = '2026-11-20-japanese-nonleader-faction-route-v1'
JAPANESE_PRE_ADAPTATION_SHA256 = 'F2A255FB9AB4194B9E24AB908B0CD8F20BE6C1CE973AE0A4F4FF83D86D72D1F6'
ENGLISH = 'localisation/english/korea_focus_l_english.yml'
KOREAN = 'localisation/korean/korea_focus_l_korean.yml'
OLD = frozenset((FOCUS, DECISIONS, AI, HISTORY, ENGLISH, KOREAN))
PATHS = OLD | frozenset((
    'common/characters/HOK_KCH_characters.txt',
    'common/decisions/HOK_KOR_democratic_support.txt',
    'common/decisions/categories/HOK_KOR_democratic_support.txt',
    'common/ideas/HOK_KOR_democratic_intelligence.txt',
    'common/scripted_effects/HOK_KOR_chinese_government_effects.txt',
    'common/scripted_effects/HOK_KOR_democratic_intelligence_effects.txt',
    'common/scripted_triggers/HOK_KOR_chinese_democratic_support_triggers.txt',
    'common/scripted_triggers/HOK_KOR_chinese_government_state_triggers.txt',
    'interface/HOK_KOR_democratic_support_intelligence.gfx',
    'interface/HOK_KOR_democratic_support_intelligence_shine.gfx',
    *(f'localisation/{language}/HOK_KOR_{topic}_l_{language}.yml'
      for language in ('english', 'korean')
      for topic in ('chinese_government', 'democratic_intelligence', 'democratic_support')),
    'gfx/interface/decisions/HOK_KOR/democratic_support/category.dds',
    'gfx/interface/decisions/HOK_KOR/democratic_support/support_democracy_in_china.dds',
    'gfx/interface/decisions/HOK_KOR/democratic_support/support_democracy_in_japan.dds',
    'gfx/interface/goals/HOK_KOR/democratic_intelligence/secret_intelligence_service.dds',
    'gfx/interface/goals/HOK_KOR/democratic_intelligence/shine_overlay.dds',
    'gfx/interface/ideas/HOK_KOR/democratic_intelligence/secret_intelligence_service.dds',
))
CHANGED_FOCUSES = ('KOR_invite_china', 'KOR_support_for_democracy_in_china',
    'KOR_overthrow_the_chinese_dictators', 'KOR_invite_japan',
    'KOR_support_for_democracy_in_japan', 'KOR_minshu_ikki')
NEW_FOCUS = 'HOK_KOR_expand_secret_intelligence_service'
NOTE = '#20261120_kpopmodder: Integrate democratic support, intelligence and Shandong with RT56 geography.'


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def canonical_name(relative: str | Path) -> str:
    path = (ROOT / Path(str(relative).replace('\\', '/'))).resolve()
    name = path.relative_to(ROOT.resolve()).as_posix()
    return next((p for p in PATHS if p.casefold() == name.casefold()), name)


@lru_cache(maxsize=1)
def lock() -> dict:
    result = json.loads(LOCK_PATH.read_text(encoding='utf-8'))
    if (result.get('format') != 1 or result.get('revision') != '2026-11-20-democratic-support-v1'
            or result.get('base_commit') != '9a01955785bcdd827c9c85522537a0bfc57ed654'
            or result.get('source_commit') != 'f180bc8089e2a17f310b1fafa091d3f152063df3'
            or result.get('ancestor_commit') != '0c19f58fa7a9ff898196dcdbe46edfd0ad5fdbbc'
            or set(result.get('outputs', {})) != PATHS):
        raise ValueError('unreviewed democratic revision, source or output inventory')
    japanese = result['outputs'][JAPANESE_EFFECTS]
    if (japanese.get('source_adaptation') != JAPANESE_NONLEADER_ADAPTATION
            or japanese.get('integration_predecessor_sha256') != JAPANESE_PRE_ADAPTATION_SHA256
            or japanese.get('integration_predecessor_size') != 851):
        raise ValueError('unreviewed Japanese nonleader adaptation predecessor')
    return result


def frozen(relative: str, expected: str, size: int | None = None) -> bytes:
    path = (SNAPSHOT / relative).resolve()
    path.relative_to(SNAPSHOT.resolve())
    data = path.read_bytes()
    if sha(data) != expected or (size is not None and len(data) != size):
        raise ValueError(f'democratic frozen input drift: {relative}')
    return data


@lru_cache(maxsize=1)
def manifest() -> dict:
    config = lock()
    result = json.loads(frozen('source-manifest.json', config['source_manifest_sha256']))
    if (result['source_commit'] != config['source_commit']
            or result['ancestor_commit'] != config['ancestor_commit']
            or result['compatibility_base_commit'] != config['base_commit']
            or set(result['sources']) != PATHS or set(result['predecessors']) != OLD):
        raise ValueError('democratic source manifest contract drift')
    for name, pair in result['sources'].items():
        if set(pair) != ({'before', 'after'} if name in OLD else {'after'}):
            raise ValueError(f'democratic source pair drift: {name}')
        for stage, record in pair.items():
            if record['snapshot'] != ('before/' if stage == 'before' else 'runtime/') + name:
                raise ValueError(f'democratic source path drift: {name}')
            frozen(record['snapshot'], record['sha256'], record['size'])
    for name, record in result['predecessors'].items():
        if record['snapshot'] != 'compat_before/' + name:
            raise ValueError(f'democratic predecessor path drift: {name}')
        frozen(record['snapshot'], record['sha256'], record['size'])
    for record in result['documents'].values():
        frozen(record['snapshot'], record['sha256'], record['size'])
    for reference in config['references'].values():
        path = Path(reference['original_path'])
        raw = path.read_bytes()
        if sha(raw) != reference['sha256'] or len(raw) != reference['size']:
            raise ValueError(f'democratic current host/schema drift: {path}')
    host = Path(config['rt56_root'])
    acf = (host.parents[2] / 'appworkshop_394360.acf').read_text(encoding='utf-8-sig')
    entries = re.findall(r'"820260968"\s*\{([^{}]+)\}', acf)
    versions = [v for entry in entries for v in re.findall(r'"(?:latest_)?manifest"\s*"(\d+)"', entry)]
    if len(versions) < 2 or any(v != config['workshop_manifest'] for v in versions):
        raise ValueError('democratic installed/latest RT56 manifest drift')
    version = json.loads((Path(config['vanilla_root']) / 'launcher-settings.json').read_text(encoding='utf-8-sig'))['version']
    if version != config['game_version']:
        raise ValueError('democratic installed game-version drift')
    for name in PATHS - OLD:
        if any((Path(config[provider + '_root']) / name).exists() for provider in ('rt56', 'vanilla')):
            raise ValueError(f'democratic unreviewed host path collision: {name}')
    return result


def source(name: str, stage: str = 'after') -> bytes:
    record = manifest()['sources'][name][stage]
    return frozen(record['snapshot'], record['sha256'], record['size'])


def previous_bytes(name: str) -> bytes:
    record = manifest()['predecessors'][name]
    return frozen(record['snapshot'], record['sha256'], record['size'])


def replace_once(data: bytes, before: bytes, after: bytes, label: str) -> bytes:
    if data.count(before) != 1:
        raise ValueError(f'ambiguous democratic delta: {label}')
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
    raise ValueError('unclosed democratic block')


def span(data: bytes, identifier: str, *, focus: bool = False) -> tuple[int, int]:
    pattern = (rb'(?m)^\tfocus = \{\n\t\tid = ' + re.escape(identifier.encode()) + rb'\s*\n'
        if focus else rb'(?m)^[\t ]*' + re.escape(identifier.encode()) + rb'\s*=\s*\{')
    matches = list(re.finditer(pattern, data))
    if len(matches) != 1: raise ValueError(f'ambiguous democratic block: {identifier}')
    hit = matches[0]
    return hit.start(), block_end(data, data.index(b'{', hit.start(), hit.end()))


def region_ids() -> list[int]:
    raw = MAPPING_PATH.read_bytes()
    if sha(raw) != lock()['mapping_sha256']: raise ValueError('democratic geographic mapping drift')
    mapping = json.loads(raw)
    ids = mapping['mainland_state_ids']
    if (len(ids) != mapping['mainland_state_count'] or ids != sorted(set(ids))
            or mapping['seed_state_ids'] != [597, 743]
            or mapping.get('unresolved_geographic_mappings') != []):
        raise ValueError('democratic geographic coverage remains unresolved')
    return ids


def translations() -> dict[str, str]:
    raw = frozen('english-translations.json', lock()['translation_sha256'])
    result = json.loads(raw)
    if len(result) != 26: raise ValueError('democratic English key inventory drift')
    return result


def locale_output(name: str) -> bytes:
    raw = previous_bytes(name) if name in OLD else source(name)
    newline = b'\r\n' if b'\r\n' in raw else b'\n'
    header = b'l_english:' if '/english/' in name else b'l_korean:'
    raw = replace_once(raw, header + newline, header + newline + NOTE.encode() + newline, name + '/note')
    target_keys = set(translations())
    donor = source(name)
    # Only donor-changed values are permitted to replace the existing translated focus file.
    if name in OLD:
        old_values = dict(re.findall(rb'(?m)^\s*([^#\s:]+):\d*\s*"(.*)"\r?$', source(name, 'before')))
        values = dict(re.findall(rb'(?m)^\s*([^#\s:]+):\d*\s*"(.*)"\r?$', donor))
        target_keys = {key.decode() for key,value in values.items() if old_values.get(key) != value}
    for key in sorted(target_keys):
        pattern = rb'(?m)^(\s*' + re.escape(key.encode()) + rb':\d*\s*")(.*)("\r?$)'
        match = re.search(pattern, donor)
        if match is None:
            if name in OLD: raise ValueError(f'democratic donor locale key absent: {key}')
            continue
        value = translations()[key].encode() if '/english/' in name else match[2]
        found = list(re.finditer(pattern, raw))
        if len(found) != 1: raise ValueError(f'ambiguous democratic locale: {name}/{key}')
        hit = found[0]
        raw = raw[:hit.start(2)] + value + raw[hit.end(2):]
    return raw


def focus_output() -> bytes:
    current = previous_bytes(FOCUS)
    newline = b'\r\n' if b'\r\n' in current else b'\n'
    current = current.replace(b'\r\n', b'\n')
    before, after = (source(FOCUS, stage).replace(b'\r\n', b'\n') for stage in ('before', 'after'))
    for identifier in CHANGED_FOCUSES:
        start, end = span(before, identifier, focus=True)
        old = before[start:end]
        start, end = span(current, identifier, focus=True)
        if current[start:end] != old:
            raise ValueError(f'democratic focus has an unreviewed RT56 delta: {identifier}')
        start_new, end_new = span(after, identifier, focus=True)
        current = current[:start] + b'\t' + NOTE.encode() + b'\n' + after[start_new:end_new] + current[end:]
    start, end = span(after, NEW_FOCUS, focus=True)
    new = after[start:end]
    _, anchor_end = span(current, 'KOR_begin_rearmament', focus=True)
    current = current[:anchor_end] + b'\n\t' + NOTE.encode() + b'\n' + new + current[anchor_end:]
    return current.replace(b'\n', newline)


def preview_outputs() -> dict[str, bytes]:
    result = {}
    for name in sorted(PATHS):
        if name.startswith('localisation/'):
            data = locale_output(name)
        elif name == FOCUS:
            data = focus_output()
        elif name == AI:
            data = previous_bytes(name)
            newline = b'\r\n' if b'\r\n' in data else b'\n'
            anchor = b'\t\tKOR_begin_rearmament' + newline
            data = replace_once(data, anchor, anchor + b'\t\t' + NOTE.encode() + newline + b'\t\t' + NEW_FOCUS.encode() + newline, 'historical AI')
        elif name == HISTORY:
            data = previous_bytes(name)
            newline = b'\r\n' if b'\r\n' in data else b'\n'
            data = replace_once(data, b'capital = 1114 # Nanjing' + newline,
                b'capital = 1114 # Nanjing' + newline + NOTE.encode() + newline + b'recruit_character = HOK_KCH_weng_wenhao' + newline, 'KCH startup')
        elif name == DECISIONS:
            data = previous_bytes(name)
            newline = b'\r\n' if b'\r\n' in data else b'\n'
            normalized = data.replace(b'\r\n', b'\n')
            start, end = span(normalized, 'KOR_New_China_Government')
            block = normalized[start:end]
            # The reviewed recognition block changes only its repeated mainland-core list.
            if b'annex_country = { target = CHI }' not in block or b'set_cosmetic_tag = KCH_china' not in block:
                raise ValueError('democratic recognition contract drift')
            anchor = block.index(b'set_cosmetic_tag = KCH_china') + len(b'set_cosmetic_tag = KCH_china')
            inner_start, inner_end = span(block[anchor:], 'hidden_effect')
            inner_start, inner_end = inner_start + anchor, inner_end + anchor
            replacement = b'\t\t\t\t' + NOTE.encode() + b'\n\t\t\t\thidden_effect = { HOK_KOR_chinese_government_grant_mainland_cores = yes }'
            block = block[:inner_start] + replacement + block[inner_end:]
            data = (normalized[:start] + block + normalized[end:]).replace(b'\n', newline)
        else:
            data = source(name)
            if name.endswith('HOK_KOR_chinese_government_state_triggers.txt'):
                newline = b'\r\n' if b'\r\n' in data else b'\n'
                normalized = data.replace(b'\r\n', b'\n')
                start, end = span(normalized, 'HOK_KOR_chinese_government_is_mainland')
                block = b'HOK_KOR_chinese_government_is_mainland = {\n\tOR = {\n' + b''.join(f'\t\tstate = {state}\n'.encode() for state in region_ids()) + b'\t}\n}'
                data = (normalized[:start] + NOTE.encode() + b'\n' + block + normalized[end:]).replace(b'\n', newline)
            elif name.endswith('HOK_KOR_chinese_government_effects.txt'):
                data = replace_once(data, b'HOK_KOR_chinese_government_passes = 63',
                    f'HOK_KOR_chinese_government_passes = {len(region_ids())}'.encode(), 'bounded geographic expansion')
            elif name == JAPANESE_EFFECTS:
                newline = b'\r\n' if b'\r\n' in data else b'\n'
                before = b'\t\tKOR = {\n\t\t\tadd_to_faction = PREV\n'
                after = (b'\t\tKOR = {\n'
                    b"\t\t\t#20261120_kpopmodder: Invite the Japanese democratic rebel through Korea's existing faction leader when Korea is a member.\n"
                    b'\t\t\tif = {\n'
                    b'\t\t\t\tlimit = { is_in_faction = yes is_faction_leader = no }\n'
                    b'\t\t\t\tfaction_leader = { add_to_faction = PREV.PREV }\n'
                    b'\t\t\t} else = {\n'
                    b'\t\t\t\tadd_to_faction = PREV\n'
                    b'\t\t\t}\n')
                data = replace_once(data.replace(b'\r\n', b'\n'), before, after,
                    'Japanese nonleader faction invitation').replace(b'\n', newline)
        result[name] = data
    return result


@lru_cache(maxsize=1)
def build_outputs() -> dict[str, bytes]:
    outputs = preview_outputs()
    for name, data in outputs.items():
        record = lock()['outputs'][name]
        if sha(data) != record['sha256'] or len(data) != record['size']:
            raise ValueError(f'democratic generated output drift: {name}')
    return outputs


def historical_bytes(relative: str | Path, data: bytes) -> bytes:
    name = canonical_name(relative)
    if name in OLD and sha(data) == lock()['outputs'][name]['sha256']:
        if data != build_outputs()[name]: raise ValueError(f'democratic final-output proof failed: {name}')
        return previous_bytes(name)
    return data


def finalize_one(relative: str | Path, data: bytes) -> bytes:
    name = canonical_name(relative)
    if name not in PATHS: return data
    final = build_outputs()[name]
    accepted = accepted_predecessors(name, final)
    if data not in accepted: raise ValueError(f'unreviewed democratic predecessor: {name}')
    return final


def accepted_predecessors(name: str, final: bytes) -> tuple[bytes, ...]:
    if name in OLD:
        return final, previous_bytes(name)
    if name == JAPANESE_EFFECTS:
        predecessor = source(name)
        if (sha(predecessor) != JAPANESE_PRE_ADAPTATION_SHA256
                or len(predecessor) != lock()['outputs'][name]['integration_predecessor_size']):
            raise ValueError('Japanese nonleader adaptation source drift')
        return final, predecessor
    return (final,)


def finalize_outputs(outputs: dict, *, owner: str) -> dict:
    result = {name:finalize_one(name,data) for name,data in outputs.items()}
    if owner == 'focus':
        paths = bool(result) and isinstance(next(iter(result)), Path)
        for name in sorted(PATHS - OLD):
            result[Path(name) if paths else name] = build_outputs()[name]
    return result


def preflight_outputs(outputs: dict) -> None:
    seen = set()
    for relative, data in outputs.items():
        name = canonical_name(relative)
        if name not in PATHS: continue
        if name in seen: raise ValueError(f'duplicate democratic output: {name}')
        seen.add(name)
        if data != build_outputs()[name]: raise ValueError(f'unregistered proposed democratic bytes: {name}')
        path = ROOT / name
        allowed = accepted_predecessors(name, build_outputs()[name])
        if path.exists() and (not path.is_file() or path.read_bytes() not in allowed):
            raise ValueError(f'independently changed democratic runtime: {name}')
        if name in OLD and not path.is_file(): raise ValueError(f'missing democratic predecessor: {name}')


def ledger_bytes(previous: bytes) -> bytes:
    outputs = build_outputs()
    if any((ROOT / name).read_bytes() != data for name,data in outputs.items()):
        raise ValueError('democratic ledger/runtime mismatch')
    reader = csv.DictReader(io.StringIO(previous.decode('utf-8'), newline=''))
    fields = reader.fieldnames
    if not fields: raise ValueError('democratic ledger schema absent')
    lines, chunks, seen = previous.splitlines(keepends=True), [], set()
    start = reader.line_num
    chunks.append(b''.join(lines[:start]))
    reason = '; 2026-11-20 democratic support: tools/hok_democratic_support_lock.json; original HOK authorship retained'
    def encoded(row):
        stream = io.StringIO(newline='')
        csv.DictWriter(stream,fieldnames=fields,lineterminator='\n').writerow(row)
        return stream.getvalue().encode()
    def addition(name, *, pre_adaptation=False):
        record, source_record = lock()['outputs'][name], manifest()['sources'][name]['after']
        row = {field:'' for field in fields}
        values = dict(source_path=name,output_path=name,integration_class=record['classification'],status='SHIPPED',
            exact_path_rt56_collision='no',output_sha256=record['sha256'],donor_sha256=source_record['sha256'],
            donor_source_sha256=source_record['sha256'],donor_source_commit=lock()['source_commit'],
            donor_source_checkout='reviewed-clean-checkout',reason=reason.lstrip('; ') + '; previous_output_sha256=None'
                + '; source_snapshot=docs/upstream/hok-democratic-support-20261120/' + source_record['snapshot'])
        if name == JAPANESE_EFFECTS:
            if pre_adaptation:
                values['output_sha256'] = record['integration_predecessor_sha256']
            else:
                values['reason'] += ('; source_adaptation=' + record['source_adaptation']
                    + '; prior_integration_sha256=' + record['integration_predecessor_sha256'])
        row.update({key:value for key,value in values.items() if key in row})
        return row
    for row in reader:
        raw, start = b''.join(lines[start:reader.line_num]), reader.line_num
        selected = set(row['output_path'].split(' | ')) & PATHS
        if not selected: chunks.append(raw); continue
        if len(selected) != 1: raise ValueError('ambiguous democratic ledger output')
        name = selected.pop()
        record = lock()['outputs'][name]
        if name in seen: raise ValueError(f'duplicate democratic ledger output: {name}')
        seen.add(name)
        if name not in OLD:
            final_row = addition(name)
            if row == final_row:
                chunks.append(raw)
            elif name == JAPANESE_EFFECTS and row == addition(name, pre_adaptation=True):
                chunks.append(encoded(final_row))
            else:
                raise ValueError(f'democratic addition provenance drift: {name}')
            continue
        current = row['output_sha256']
        suffix = reason + '; previous_output_sha256=' + str(record.get('previous_sha256'))
        if current == record['sha256'] and row['reason'].endswith(suffix): chunks.append(raw); continue
        if name not in OLD or current != record['previous_sha256']:
            raise ValueError(f'democratic ledger predecessor drift: {name}')
        row['output_sha256'],row['reason'] = record['sha256'], row['reason'] + suffix
        chunks.append(encoded(row))
    if not OLD <= seen: raise ValueError('democratic ledger existing rows missing')
    for name in sorted(PATHS - seen):
        chunks.append(encoded(addition(name)))
    return b''.join(chunks)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--apply',action='store_true')
    mode.add_argument('--check',action='store_true')
    args = parser.parse_args()
    try:
        outputs = build_outputs()
        preflight_outputs(outputs)
        pending = [(ROOT/name,data) for name,data in outputs.items() if not (ROOT/name).is_file() or (ROOT/name).read_bytes() != data]
        if pending and not args.apply: raise ValueError('democratic runtime mismatches: ' + ', '.join(str(p) for p,_ in pending))
        for path,data in pending:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(data)
        print(f'PASS democratic support: 28 exact outputs; {len(region_ids())} RT56 mainland states; {len(pending)} written')
        return 0
    except (ValueError,KeyError,OSError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr)
        return 1


if __name__ == '__main__': raise SystemExit(main())
