#!/usr/bin/env python3
"""Reproduce the November HOK content delta over the audited 15-state port.

This final layer never writes donor, host, cache or user-profile files. Historical
validators may reverse only its exact locked final bytes; raw outputs have their
own independent gate. No engine/runtime claims are made by this builder.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import sys

#20261108_kpopmodder: Keep CNDP, display repairs and host-aware references in a separately pinned reversible layer.
ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / 'docs/upstream/hok-content-update-20261108'
LOCK_PATH = ROOT / 'tools/hok_upstream_content_lock.json'
RT56 = Path(r'C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968')
VANILLA = Path(r'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV')

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()

@lru_cache(maxsize=1)
def lock() -> dict:
    data = json.loads(LOCK_PATH.read_text(encoding='utf-8'))
    if data['format'] != 1 or data['source_commit'] != '596b221bb994d93fce552d3ee1ba70fa9b5640f1':
        raise ValueError('unreviewed November content source')
    return data

def frozen(relative: str, expected: str | None = None) -> bytes:
    path = (SNAPSHOT / relative).resolve()
    path.relative_to(SNAPSHOT.resolve())
    data = path.read_bytes()
    if expected is not None and sha(data) != expected:
        raise ValueError(f'November frozen input drift: {relative}')
    return data

def verify_inputs() -> None:
    config = lock()
    manifest = json.loads(frozen('source-manifest.json',config['source_manifest_sha256']))
    for group in ('runtime','documents'):
        for relative, record in manifest[group].items():
            frozen(f'{group}/{relative}',record['sha256'])
    for relative, record in config['inputs'].items():
        frozen(record['snapshot_path'],record['sha256'])
    for relative, record in config.get('host_inputs',{}).items():
        source = (RT56 if record['provider']=='RT56' else VANILLA) / relative
        actual=sha(source.read_bytes())
        if actual != record['sha256']:
            from rt56_host_update import approved_input_transition
            if not approved_input_transition(record['provider'],relative,record['sha256'],actual):
                raise ValueError(f'November physical host/schema drift: {record["provider"]}/{relative}')
    acf = (RT56.parents[2]/'appworkshop_394360.acf').read_text(encoding='utf-8')
    entries = re.findall(r'"820260968"\s*\{([^{}]+)\}',acf)
    manifests = [m for entry in entries for m in re.findall(r'"(?:latest_)?manifest"\s*"(\d+)"',entry)]
    if len(manifests)<2 or any(m!=config['workshop_manifest'] for m in manifests):
        from rt56_host_update import approved_manifest_transition
        if not approved_manifest_transition(config['workshop_manifest'],manifests):
            raise ValueError('November RT56 installed/latest manifest drift')

def preview_outputs() -> dict[str,bytes]:
    """Build from immutable ancestors, never from the mutable runtime tree."""
    verify_inputs()
    from upstream_cndp import apply_cndp,cndp_additions
    from upstream_civic_display import apply_civic_display,civic_additions
    from upstream_state_references import apply_references,reference_additions
    donor = SNAPSHOT/'runtime'
    result = {}
    for relative, record in lock()['inputs'].items():
        before = frozen(record['snapshot_path'],record['sha256'])
        data = apply_references(relative,before,donor)
        data = apply_civic_display(relative,data,donor)
        data = apply_cndp(relative,data,donor)
        if data != before:
            result[relative] = data
    for additions in (reference_additions(donor),civic_additions(donor),cndp_additions(donor)):
        for relative,data in additions.items():
            if relative in result and result[relative] != data:
                raise ValueError(f'November duplicate generator ownership: {relative}')
            result[relative] = data
    return result

@lru_cache(maxsize=1)
def build_outputs() -> dict[str,bytes]:
    result = preview_outputs()
    records = lock()['outputs']
    if set(result) != set(records):
        raise ValueError('November runtime output allowlist drift')
    for relative,data in result.items():
        if sha(data) != records[relative]['sha256']:
            raise ValueError(f'November reviewed output drift: {relative}')
    return result

def historical_bytes(relative: str | Path, data: bytes) -> bytes:
    if not LOCK_PATH.exists():
        return data
    name = Path(relative).as_posix()
    record = lock().get('outputs',{}).get(name)
    if record and record.get('previous_sha256') and sha(data)==record['sha256']:
        return frozen(lock()['inputs'][name]['snapshot_path'],record['previous_sha256'])
    return data

def finalize_one(relative: str | Path, data: bytes) -> bytes:
    if not LOCK_PATH.exists():
        return data
    #20261109_kpopmodder: Nested older finalizers inspect the proven ancestor of a later review-final payload.
    from review_followup import historical_bytes as review_historical
    data=review_historical(relative,data)
    name = Path(relative).as_posix()
    record = lock().get('outputs',{}).get(name)
    if not record:
        return data
    if sha(data)==record['sha256']:
        return data
    if sha(data)!=record.get('previous_sha256'):
        raise ValueError(f'unreviewed ancestor for November content: {name}')
    return build_outputs()[name]

def addition_paths(owner: str | None = None) -> tuple[str,...]:
    if not LOCK_PATH.exists():
        return ()
    return tuple(name for name,record in lock().get('outputs',{}).items()
                 if record.get('previous_sha256') is None and (owner is None or record['owner']==owner))

def finalize_outputs(outputs: dict, *, owner: str) -> dict:
    result = {name:finalize_one(name,data) for name,data in outputs.items()}
    path_keys = bool(outputs) and isinstance(next(iter(outputs)),Path)
    for name in addition_paths(owner):
        result[Path(name) if path_keys else name] = build_outputs()[name]
    return result


def preflight_outputs(outputs: dict) -> None:
    """Reject unsafe destinations or independent edits before any writer runs.

    Older generators retain their established behavior for unrelated files.
    Content-owned files may only advance from their exact recorded ancestor
    or an explicitly reviewed earlier output revision (or remain final).
    Newly added files must be absent or an explicitly known output.
    """
    root = ROOT.resolve()
    records = lock().get('outputs', {}) if LOCK_PATH.exists() else {}
    # Windows resolves case variants to the same physical target; they must
    # not bypass a content-owned path's recorded-hash protection.
    records_by_name = {name.casefold(): record for name, record in records.items()}
    errors = []
    seen = set()
    for relative, data in outputs.items():
        destination = (root / Path(relative)).resolve()
        try:
            name = destination.relative_to(root).as_posix()
        except ValueError:
            errors.append(f'November output escapes repository: {destination}')
            continue
        if destination in seen:
            errors.append(f'November duplicate output destination: {name}')
            continue
        seen.add(destination)
        record = records_by_name.get(name.casefold())
        if not record:
            continue
        #20261109_kpopmodder: Admit only exact review-final bytes after proving their unchanged November ancestor.
        from review_followup import historical_bytes as review_historical
        if sha(review_historical(name,data)) != record['sha256']:
            errors.append(f'refusing unreviewed November output bytes: {name}')
            continue
        if destination.exists() and not destination.is_file():
            errors.append(f'November output is not a regular file: {name}')
            continue
        current = destination.read_bytes() if destination.is_file() else None
        digest = sha(review_historical(name,current)) if current is not None else None
        #20261109_kpopmodder: Accept only recorded prior generated revisions when advancing a reviewed parser or display repair.
        accepted={record['sha256'],record.get('previous_sha256'),*record.get('accepted_previous_outputs',[])}
        if digest not in accepted:
            errors.append(f'refusing independently changed runtime: {name}')
    if errors:
        raise ValueError('\n'.join(errors))
    from review_followup import preflight_outputs as review_preflight
    review_preflight(outputs)
    #20261108_kpopmodder: Protect the separate current-host outputs in every existing writer as well.
    from rt56_host_update import preflight_outputs as host_preflight
    host_preflight(outputs)


def ledger_bytes(previous: bytes) -> bytes:
    """Retain historical provenance and change only independently locked outputs."""
    if not LOCK_PATH.exists():
        return previous
    config = lock()
    if sha(previous)!=config['ledger_before_sha256']:
        raise ValueError('November predecessor ledger drift')
    reader=csv.DictReader(io.StringIO(previous.decode('utf-8'),newline=''))
    fields=reader.fieldnames
    #20261108_kpopmodder: Retain byte-exact CSV rows outside the explicitly changed output set.
    lines=previous.splitlines(keepends=True)
    reader.fieldnames
    start=reader.line_num
    raw_rows=[]
    rows=[]
    for row in reader:
        rows.append(row)
        raw_rows.append(b''.join(lines[start:reader.line_num]))
        start=reader.line_num
    originals=[dict(row) for row in rows]
    for relative,record in config['outputs'].items():
        actual=(ROOT/relative).read_bytes()
        #20261109_kpopmodder: Keep the November provenance layer on its exact ancestor before the later ledger delta.
        from review_followup import historical_bytes as review_historical
        actual=review_historical(relative,actual)
        if sha(actual)!=record['sha256']:
            raise ValueError(f'November ledger output drift: {relative}')
        matches=[row for row in rows if relative in row['output_path'].split(' | ')]
        if len(matches)>1:
            raise ValueError(f'November ambiguous ledger output: {relative}')
        if matches:
            row=matches[0]
            if row['output_sha256']!=record.get('previous_sha256'):
                raise ValueError(f'November lost prior ledger provenance: {relative}')
        else:
            if any(row['source_path']==relative for row in rows):
                raise ValueError(f'November duplicate ledger source: {relative}')
            row={field:'' for field in fields}
            row.update(source_path=relative,output_path=relative)
            rows.append(row)
        row.update(integration_class=record['classification'],output_sha256=record['sha256'],
                   status='GENERATED' if record['classification']=='THREE_WAY_MERGE' else 'SHIPPED',
                   exact_path_rt56_collision='yes' if (RT56/relative).is_file() else 'no')
        if record.get('host_provider')=='RT56':
            row['rt56_base_sha256']=record['host_sha256']
        provenance=record.get('source_path')
        if provenance:
            source=config['source_records'][provenance]
            row.update(previous_source_commit=row.get('donor_source_commit',''),
                       previous_source_sha256=row.get('donor_source_sha256',''),
                       donor_source_commit=config['source_commit'],donor_source_blob=source['git_blob'],
                       donor_sha256=source['sha256'],donor_source_sha256=source['sha256'],
                       donor_source_checkout='reviewed immutable November Git input')
        row['reason'] += ('; 2026-11-08 HOK content integration: lock=tools/hok_upstream_content_lock.json; '
                          f'previous_output_sha256={record.get("previous_sha256") or ""}; '
                          f'source={provenance or record.get("host_provider", "port")}; '
                          'CNDP/display/reference ownership and validation: docs/implementation/2026-11-08-hok-upstream-content-port.md')
    chunks=[lines[0]]
    for index,row in enumerate(rows):
        if index<len(originals) and row==originals[index]:
            chunks.append(raw_rows[index])
            continue
        stream=io.StringIO(newline='')
        csv.DictWriter(stream,fieldnames=fields,lineterminator='\n').writerow(row)
        chunks.append(stream.getvalue().encode('utf-8'))
    return b''.join(chunks)

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--apply',action='store_true')
    group.add_argument('--check',action='store_true')
    args=parser.parse_args()
    try:
        outputs=build_outputs()
        #20261109_kpopmodder: Preserve the explicit terminal review repair when this older writer is invoked directly.
        from review_followup import finalize_outputs as review_finalize_outputs
        outputs=review_finalize_outputs(outputs)
        preflight_outputs(outputs)
        pending=[]
        for relative,data in outputs.items():
            path=ROOT/relative
            current=path.read_bytes() if path.is_file() else None
            if current==data:
                continue
            if not args.apply:
                raise ValueError(f'November runtime mismatch: {relative}')
            #20261108_kpopmodder: Retain fail-closed protection while accepting a specifically recorded prior generated revision.
            record=lock()['outputs'][relative]
            accepted={record.get('previous_sha256'),*record.get('accepted_previous_outputs',[])}
            #20261114_kpopmodder: Admit only the verified immediate commander predecessor after the common preflight.
            from upstream_commanders import lock as commander_lock
            commander_record=commander_lock()['outputs'].get(relative)
            if commander_record:
                accepted.add(commander_record['previous_sha256'])
            if (sha(current) if current is not None else None) not in accepted:
                raise ValueError(f'refusing independently changed runtime: {relative}')
            pending.append((path,data))
        verify_inputs()
        for path,data in pending:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(data)
        print(f'PASS November HOK content: {len(outputs)} independently pinned outputs; prior 15-state map and source pins retained')
        return 0
    except (ValueError,KeyError,FileNotFoundError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr)
        return 1

if __name__=='__main__':
    raise SystemExit(main())
