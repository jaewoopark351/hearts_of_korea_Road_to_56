#!/usr/bin/env python3
"""Reproduce the reviewed Korean state split over the recorded RT56 port base.

Frozen inputs, current host fingerprints and final output hashes are separate.
No live donor, user profile, test directory or Workshop file is ever written.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
import sys

#20261107_kpopmodder: Keep the six-region migration as an independently reversible final integration layer.
ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / 'docs/upstream/hok-state-split-20261107'
LOCK_PATH = ROOT / 'tools/hok_state_split_lock.json'
RT56 = Path(r'C:\Program Files (x86)\Steam\steamapps\workshop\content\394360\820260968')
VANILLA = Path(r'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV')
PROVINCES = {n: n + 121 for n in range(13414,13448)}
OLD_STATES = {1028:918,1029:1144,1030:920,1031:1145,1082:919,1083:917,1084:1146,1085:1147}
NEW_STATES = {1086:1148,1087:1149,1088:1150,1089:1151,1090:1152,1091:1153}
SPLIT_PARENTS = {527,917,918,919,920,1145}
KOREAN_BEFORE = {525,527,917,918,919,920,1144,1145,1146}
KOREAN_AFTER = KOREAN_BEFORE | set(NEW_STATES.values())
STATE_NAMES = {527:'527-North Korea.txt',917:'917-Hwanghae.txt',918:'918-Hamgyong.txt',919:'919-Jeolla.txt',920:'920-Gyeongsang.txt',1145:'1145-Chungcheong.txt',1148:'1148-Gyeongsangnam.txt',1149:'1149-Chungcheongbuk.txt',1150:'1150-Jeollanam.txt',1151:'1151-Pyeonganbuk.txt',1152:'1152-Hamgyeongbuk.txt',1153:'1153-Hwanghaebuk.txt'}
_NUMBER = re.compile(rb'(?<![A-Za-z0-9_.])-?\d+(?![A-Za-z0-9_.])')

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()

@lru_cache(maxsize=1)
def lock() -> dict:
    data=json.loads(LOCK_PATH.read_text(encoding='utf-8'))
    if data['format'] != 1 or data['source_commit'] != '0d73d49726abbfa435c73f1bf8cc24d4a5af014b':
        raise ValueError('unreviewed Korean state-split source')
    if {int(k):v for k,v in data['new_state_ids'].items()} != NEW_STATES:
        raise ValueError('state-split persistent IDs changed')
    return data

def state_mapping() -> dict[int,int]:
    return {**PROVINCES,**OLD_STATES,**NEW_STATES}

def _frozen(group: str, relative: str, expected: str | None = None) -> bytes:
    path=(SNAPSHOT/group/relative).resolve()
    path.relative_to(SNAPSHOT.resolve())
    data=path.read_bytes()
    if expected and sha(data) != expected:
        raise ValueError(f'state-split frozen input drift: {group}/{relative}')
    return data

def read_before(relative: str) -> bytes:
    return _frozen('before',relative,lock()['sources'][relative]['before_sha256'])

def read_after(relative: str) -> bytes:
    return _frozen('runtime',relative,lock()['sources'][relative]['after_sha256'])

def compat_before(relative: str) -> bytes:
    return _frozen('compat_before',relative,lock()['compat_inputs'][relative]['sha256'])

def historical_bytes(relative: str | Path, data: bytes) -> bytes:
    """Undo only a hash-verified final update for independent older contracts."""
    #20261108_kpopmodder: Reverse the separately reviewed Steam host layer before older content contracts.
    from rt56_host_update import historical_bytes as host_historical
    data=host_historical(relative,data)
    #20261108_kpopmodder: Verify and reverse the exact subsequent content layer before the unchanged split contract.
    from upstream_content_update import historical_bytes as content_historical
    data=content_historical(relative,data)
    name=Path(relative).as_posix()
    if not LOCK_PATH.exists(): return data
    record=lock().get('outputs',{}).get(name)
    if not record or not record.get('previous_sha256'): return data
    if sha(data)==record['sha256']:
        result=compat_before(name)
        if sha(result)!=record['previous_sha256']: raise ValueError(f'bad historical split reversal: {name}')
        return result
    return data

def finalize_one(relative: str | Path, data: bytes) -> bytes:
    """Let an earlier generator retain ownership without erasing this layer."""
    #20261108_kpopmodder: Preserve the new final content layer even for inherited files outside the split allowlist.
    from upstream_content_update import finalize_one as content_finalize
    from rt56_host_update import finalize_one as host_finalize, historical_generator_input
    def finish(payload: bytes) -> bytes:
        return host_finalize(relative,content_finalize(relative,payload))
    data=historical_generator_input(relative,data)
    name=Path(relative).as_posix()
    if not LOCK_PATH.exists(): return finish(data)
    record=lock().get('outputs',{}).get(name)
    if not record: return finish(data)
    digest=sha(data)
    if digest==record['sha256']: return finish(data)
    allowed={record.get('previous_sha256'),record.get('host_intermediate_sha256')}
    if digest not in allowed:
        raise ValueError(f'unreviewed preceding split-generator output: {name}')
    return finish(_verified_final(name))

def _verified_final(name: str) -> bytes:
    result=build_outputs()[name]
    if sha(result)!=lock()['outputs'][name]['sha256']:
        raise ValueError(f'unreviewed final split-generator output: {name}')
    return result

def finalize_outputs(outputs: dict, *, owner: str) -> dict:
    """Apply the final layer only to this generator's reviewed output family."""
    result={name:finalize_one(name,data) for name,data in outputs.items()}
    if not LOCK_PATH.exists() or not lock().get('outputs'): return result
    if owner=='focus': additions=[p for p in lock()['outputs'] if p.endswith('HOK_KOR_state_split_l_english.yml') or p.endswith('HOK_KOR_state_split_l_korean.yml')]
    elif owner=='map': additions=[p for p in lock()['outputs'] if p.startswith('history/states/') and not lock()['outputs'][p].get('previous_sha256')]
    elif owner=='east-asia': additions=['common/national_focus/japan.txt']
    else: additions=[]
    path_keys=bool(outputs) and isinstance(next(iter(outputs)),Path)
    for name in additions:
        result[Path(name) if path_keys else name]=_verified_final(name)
    #20261108_kpopmodder: Add only owner-scoped new content outputs after the prior split layer.
    from upstream_content_update import finalize_outputs as content_finalize_outputs
    return content_finalize_outputs(result,owner=owner)

def remap(data: bytes) -> bytes:
    mapping=state_mapping()
    return _NUMBER.sub(lambda m:str(mapping[int(m[0])]).encode() if int(m[0]) in mapping else m[0],data)

def _map_building_row(row: bytes) -> bytes:
    fields=row.split(b';')
    if len(fields)!=7: raise ValueError(f'malformed donor display row: {row!r}')
    state=int(fields[0]);fields[0]=str(state_mapping().get(state,state)).encode()
    linked=int(fields[6])
    if linked in PROVINCES:fields[6]=str(PROVINCES[linked]).encode()
    return b';'.join(fields)

def split_spec() -> dict:
    return json.loads(_frozen('documents','docs/data/HOK_KOREAN_STATE_SPLIT_MAPPING.json',lock()['mapping_sha256']).decode('utf-8'))

def state_outputs() -> dict[str,bytes]:
    result={}
    for parent in split_spec()['parents']:
        for child in parent['children']:
            relative=child['file']
            state_id=state_mapping().get(child['id'],child['id'])
            parent_id=state_mapping().get(parent['old_id'],parent['old_id'])
            template=compat_before('history/states/'+STATE_NAMES[parent_id])
            newline=b'\r\n' if b'\r\n' in template else b'\n'
            data=remap(read_after(relative)).replace(b'\r\n',b'\n').replace(b'\n',newline)
            # Keep logical name keys independent of state scope numbers.
            wanted=child['name_key'].encode()
            data,n=re.subn(rb'(?m)^(\s*name\s*=\s*)"[^"]+"',lambda m:m[1]+b'"'+wanted+b'"',data,count=1)
            if n!=1: raise ValueError(f'missing state name: {relative}')
            def hook(match):
                values=re.findall(rb'\d+',match[0])
                return match[0]+newline+b'\t\tadd_to_array = { state_victory_points = '+values[0]+b' }'
            if b'state_victory_points' in data: raise ValueError(f'unexpected donor VP array: {relative}')
            data=re.sub(rb'victory_points\s*=\s*\{[^{}]*\}',hook,data)
            result['history/states/'+STATE_NAMES[state_id]]=data
    return result

def _province_states(states: dict[str,bytes]) -> dict[int,int]:
    import build_rt56_map as geo
    effective={}
    for path in (RT56/'history/states').glob('*.txt'):
        state,provinces=geo.parse_state(path.read_bytes(),str(path));effective[state]=provinces
    for relative in lock()['compat_state_inputs']:
        state,provinces=geo.parse_state(compat_before(relative),relative);effective[state]=provinces
    for relative,data in states.items():
        state,provinces=geo.parse_state(data,relative);effective[state]=provinces
    owners={}
    for state,provinces in effective.items():
        for province in provinces:
            if province in owners: raise ValueError(f'duplicate effective province {province}')
            owners[province]=state
    return owners

def building_output(states: dict[str,bytes]) -> bytes:
    """Keep reviewed Korean placements; rebase every non-Korean host row."""
    import build_rt56_map as geo
    before=compat_before('map/buildings.txt')
    bitmap=compat_before('map/provinces.bmp')
    definition=compat_before('map/definition.csv')
    owner=_province_states(states)
    definitions=geo.parse_definition(definition)
    colors={(v[0],v[1],v[2]):p for p,v in definitions.items()}
    meta=geo.bmp_metadata(bitmap)
    target=KOREAN_AFTER|{1147}
    previous_targets=KOREAN_BEFORE|{1147}
    rows=geo.normalized_nonempty_lines(before)
    host=geo.normalized_nonempty_lines((RT56/'map/buildings.txt').read_bytes())
    host_rows=set(host)
    selected=[]
    for row in rows:
        if int(row.split(b';',1)[0]) not in previous_targets: continue
        fields,province=geo.sample_building_province(row,bitmap,colors,meta)
        destination=owner.get(province)
        if fields[1]==b'floating_harbor' and fields[6]!=b'0':
            destination=owner.get(PROVINCES.get(int(fields[6]),int(fields[6])),destination)
        if destination not in target:
            # Existing host floating-harbor rows can carry Korean parent IDs
            # while sampling distant provinces; leave those host bytes alone.
            if row in host_rows:
                continue
            raise ValueError(f'Korean placement moved outside target map: {row!r}, province {province}')
        fields[0]=str(destination).encode()
        selected.append(b';'.join(fields))
    # Add only the author's new display rows, never the donor global database.
    old=Counter(row.split(b';',1)[1] for row in geo.normalized_nonempty_lines(read_before('map/buildings.txt')))
    new_rows=[]
    adapted=0
    source_additions=0
    for row in geo.normalized_nonempty_lines(read_after('map/buildings.txt')):
        rest=row.split(b';',1)[1]
        if old[rest]: old[rest]-=1;continue
        source_additions+=1
        fields=row.split(b';')
        if int(fields[0]) not in {527,1028,1030,1031,1082,1083,*NEW_STATES}: continue
        mapped=_map_building_row(row)
        #20261107_kpopmodder: Move one new display anchor into the same Korean province under the preserved RT56 geometry.
        if mapped==b'1152;industrial_complex;4834.00;10.95;1372.50;4.24;0':
            mapped=b'1152;industrial_complex;4836.50;10.95;1372.50;4.24;0'
            adapted+=1
        # Reparented existing source rows are already covered by the prior port.
        rest=mapped.split(b';',1)[1]
        if any(existing.split(b';',1)[1]==rest for existing in selected): continue
        f,p=geo.sample_building_province(mapped,bitmap,colors,meta)
        if f[1]==b'floating_harbor' and f[6]!=b'0': p=PROVINCES.get(int(f[6]),int(f[6]))
        if owner.get(p)!=int(f[0]): raise ValueError(f'new display row wrong state: {mapped!r}; sampled province {p}, state {owner.get(p)}')
        if f[1] in {b'air_base',b'rocket_site_spawn'} and any(x.split(b';')[:2]==f[:2] for x in selected+new_rows):
            continue
        new_rows.append(mapped)
    # Host rows outside the restored Korean geometry remain current RT56 bytes.
    if adapted!=1: raise ValueError('reviewed Hamgyeongbuk display anchor changed')
    if source_additions!=172: raise ValueError(f'unreviewed donor display additions: {source_additions}')
    #20261107_kpopmodder: Retained RT56 Gyeongsang air/rocket sites lie in the northern child; restore only two audited southern source sites.
    southern_sites=(b'1086;air_base;4810.00;11.45;1239.00;4.32;0',
                    b'1086;rocket_site_spawn;4817.00;9.90;1237.00;4.79;0')
    source_rows=geo.normalized_nonempty_lines(read_after('map/buildings.txt'))
    for southern in southern_sites:
        if source_rows.count(southern)!=1:
            raise ValueError('reviewed South Gyeongsang source site changed')
        site=_map_building_row(southern);kind=site.split(b';')[1]
        if not any(r.split(b';')[:2]==[b'1148',kind] for r in selected+new_rows):
            fields,province=geo.sample_building_province(site,bitmap,colors,meta)
            if owner.get(province)!=1148 or definitions[province][3][4]!=b'land':
                raise ValueError('South Gyeongsang site is outside the child state')
            new_rows.append(site)
    selected_rest={r.split(b';',1)[1] for r in selected}
    kept=[]
    for row in host:
        fields,province=geo.sample_building_province(row,bitmap,colors,meta)
        linked=owner.get(int(fields[6])) if fields[1]==b'floating_harbor' and fields[6]!=b'0' else None
        if owner.get(province) in target or linked in target or row.split(b';',1)[1] in selected_rest:
            continue
        kept.append(row)
    merged=kept+selected+new_rows
    duplicates={row:count for row,count in Counter(merged).items() if count>1}
    inherited=Counter(host)
    introduced={row:count for row,count in duplicates.items() if count>inherited[row]}
    if introduced: raise ValueError(f'new duplicate merged building row: {list(introduced.items())[:5]}')
    missing=geo.coastal_without_naval_base_spawn(merged,bitmap,definition)
    baseline=geo.coastal_without_naval_base_spawn(host,(RT56/'map/provinces.bmp').read_bytes(),(RT56/'map/definition.csv').read_bytes())
    if missing-baseline: raise ValueError(f'new missing coastal spawn {sorted(missing-baseline)}')
    for kind,required in [(b'air_base',target),(b'rocket_site_spawn',KOREAN_AFTER-{1146})]:
        counts=Counter(int(r.split(b';')[0]) for r in merged if r.split(b';')[1]==kind)
        bad={s:counts[s] for s in required if counts[s]!=1}
        if bad: raise ValueError(f'state-split site count {kind!r}: {bad}')
    return geo.join_rt_lines(merged,False)

def verify_inputs() -> None:
    config=lock()
    for name,record in config['sources'].items():
        read_after(name)
        if 'before_sha256' in record: read_before(name)
    for name in config['compat_inputs']: compat_before(name)
    for key,record in config['current_inputs'].items():
        label,relative=key.split('/',1)
        path=(RT56 if label=='rt56' else VANILLA)/relative
        actual=sha(path.read_bytes())
        if actual!=record['sha256']:
            from rt56_host_update import approved_input_transition
            if not approved_input_transition(label,relative,record['sha256'],actual):
                raise ValueError(f'current host/schema drift: {key}')
    acf=(RT56.parents[2]/'appworkshop_394360.acf').read_text(encoding='utf-8-sig')
    entries=re.findall(r'"820260968"\s*\{([^}]+)\}',acf)
    manifests=[m for entry in entries for m in re.findall(r'"(?:latest_)?manifest"\s*"(\d+)\s*"',entry)]
    if len(manifests)<2 or any(m!=config['workshop_manifest'] for m in manifests):
        from rt56_host_update import approved_manifest_transition
        if not approved_manifest_transition(config['workshop_manifest'],manifests):
            raise ValueError('RT56 installed/latest Workshop manifest drift')
    for p in (RT56/'history/states').glob('*.txt'):
        match=re.search(rb'(?m)^\s*id\s*=\s*(\d+)',p.read_bytes())
        if match and int(match[1]) in NEW_STATES.values(): raise ValueError(f'new Korean state ID occupied by RT56: {p}')

@lru_cache(maxsize=1)
def build_outputs() -> dict[str,bytes]:
    verify_inputs()
    from korean_state_split_content import content_paths,apply_content,additions,port_localisation_outputs
    from korean_state_split_shared import apply_shared,current_shared_inputs
    outputs=state_outputs()
    outputs['map/buildings.txt']=building_output(outputs)
    for relative in content_paths(): outputs[relative]=apply_content(relative,compat_before(relative))
    outputs.update(additions())
    #20261107_kpopmodder: Explain the exact naval/nuclear successor preferences without changing the facility effects.
    outputs.update(port_localisation_outputs(compat_before))
    from rt56_host_update import legacy_shared_inputs
    legacy=legacy_shared_inputs()
    for relative,data in current_shared_inputs(frozen_inputs=legacy or None).items():
        outputs[relative]=apply_shared(relative,data,OLD_STATES|NEW_STATES)
    # Separate, bounded correction for the already localized Tsushima key.
    relative='history/states/1147-Tsushima.txt'
    previous=compat_before(relative)
    if previous.count(b'name="STATE_1088"')!=1: raise ValueError('Tsushima legacy display anchor changed')
    outputs[relative]=previous.replace(b'name="STATE_1088"',b'name="STATE_1147"',1)
    return outputs

def main() -> int:
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--apply',action='store_true')
    group.add_argument('--check',action='store_true')
    args=parser.parse_args()
    try:
        outputs=build_outputs()
        records=lock()['outputs']
        if set(outputs)!=set(records): raise ValueError('state-split output allowlist changed')
        mismatches=[]
        pending=[]
        for name,data in outputs.items():
            record=records[name]
            if sha(data)!=record['sha256']: raise ValueError(f'unreviewed generated split output: {name}')
            #20261108_kpopmodder: Enforce actual final bytes while retaining immutable historical split hashes.
            from upstream_content_update import finalize_one as content_finalize
            data=content_finalize(name,data)
            from rt56_host_update import finalize_one as host_finalize
            data=host_finalize(name,data)
            path=ROOT/name
            current=path.read_bytes() if path.is_file() else None
            if current==data: continue
            if args.apply:
                allowed={record['sha256'],record.get('previous_sha256'),*record.get('accepted_previous_outputs',[])}
                if current is not None and sha(current) not in allowed:
                    raise ValueError(f'refusing independently modified output: {name}')
                pending.append((path,data))
            else: mismatches.append(name)
        if mismatches: raise ValueError(f'state-split runtime mismatches: {mismatches}')
        verify_inputs()
        for path,data in pending:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(data)
        print(f'PASS Korean state split: {len(outputs)} deterministic outputs; 15 Korean states; six collision-free IDs; preserved source layers')
        return 0
    except (ValueError,KeyError,FileNotFoundError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr);return 1

if __name__=='__main__': raise SystemExit(main())
