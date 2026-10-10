#!/usr/bin/env python3
"""New preservation helper; treats supplied programs only as uninterpreted bytes."""
from pathlib import Path
import hashlib, json, sys
OUT=Path(__file__).resolve().parent
SRC=Path('characteristic_two_chirp_guard_0320')
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def paths():
    inherited=json.loads((SRC/'SOURCE_HASHES_BEFORE.json').read_text())
    return sorted(set(map(Path,inherited))|{p for p in SRC.rglob('*') if p.is_file()})
def check_manifest(path):
    rows=[]
    for line in path.read_text().splitlines():
        digest, name=line.split(maxsplit=1)
        item=path.parent/name.lstrip('*')
        rows.append({'path':str(item),'expected':digest,'actual':h(item),'match':h(item)==digest})
    return {'manifest':str(path),'entries':rows,'all_valid':all(r['match'] for r in rows)}
phase=sys.argv[1]
snapshot={str(p):h(p) for p in paths()}
(OUT/f'INPUT_HASHES_{phase.upper()}.json').write_text(json.dumps(snapshot,indent=2)+'\n')
if phase=='before':
    reports=[check_manifest(p) for p in paths() if p.name=='MANIFEST.sha256']
    inherited=json.loads((SRC/'SOURCE_HASHES_BEFORE.json').read_text())
    report={'all_manifests_valid':all(r['all_valid'] for r in reports),'manifests':reports,
    'inherited_hashes_match_now':all(snapshot[p]==v for p,v in inherited.items()),
    'protected_paths':len(snapshot),'source_code_executed_imported_or_compiled':False}
    (OUT/'INPUT_SEAL_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    assert report['all_manifests_valid'] and report['inherited_hashes_match_now']
else:
    before=json.loads((OUT/'INPUT_HASHES_BEFORE.json').read_text())
    changes={p:{'before':before.get(p),'after':snapshot.get(p)} for p in before.keys()|snapshot.keys() if before.get(p)!=snapshot.get(p)}
    report={'protected_paths':len(snapshot),'unchanged':not changes,'changes':changes}
    (OUT/'PRESERVATION.json').write_text(json.dumps(report,indent=2)+'\n')
    assert not changes
print(json.dumps({'phase':phase,'protected_paths':len(snapshot),'success':True}))
