from pathlib import Path
import hashlib,json
ROOT=Path('ramified_chirp_squarefreeness_0341')
DIRS=[Path('[local workspace]')/x for x in ['diagonal_chirp_classification_0246','composite_chirp_research_0308','characteristic_two_chirp_guard_0320']]
hashfile=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]; paths=set()
for folder in DIRS:
    files=[p for p in folder.iterdir() if p.is_file()]; paths.update(files)
    manifest=folder/'MANIFEST.sha256'; entries=[]
    for line in manifest.read_text().splitlines():
        expected,name=line.split(maxsplit=1); p=folder/name.lstrip('*'); actual=hashfile(p)
        entries.append({'path':str(p),'valid':actual==expected})
        assert actual==expected,(p,expected,actual)
    checks.append({'folder':str(folder),'entries':len(entries),'all_valid':all(e['valid'] for e in entries)})
    for fname in ['SOURCE_HASHES_BEFORE.json','SOURCE_HASHES_AFTER.json']:
        j=json.loads((folder/fname).read_text())
        if isinstance(j,dict):
            for name,old in j.items():
                p=Path(name)
                if p.is_file() and isinstance(old,str) and len(old)==64:
                    assert hashfile(p)==old,(p,'prior preservation mismatch')
                    paths.add(p)
current={str(p):hashfile(p) for p in sorted(paths)}
before=ROOT/'SOURCE_HASHES_BEFORE.json'
if not before.exists():
    before.write_text(json.dumps(current,indent=2)+'\n')
    (ROOT/'INPUT_MANIFEST_CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n')
else:
    old=json.loads(before.read_text()); assert old==current
    (ROOT/'SOURCE_HASHES_AFTER.json').write_text(json.dumps(current,indent=2)+'\n')
    (ROOT/'PRESERVATION.json').write_text(json.dumps({'distinct_paths':len(current),'all_unchanged':True,'input_manifests':checks,'supplied_code_executed_or_imported':False},indent=2)+'\n')
print('Input seals verified:',len(current),'protected paths')
