#!/usr/bin/env python3
"""Independent archive-data inventory and embedded hash verifier. Never executes members."""
from pathlib import Path, PurePosixPath
import hashlib, io, json, re, stat, zipfile

BASE=Path(__file__).resolve().parent
known=set(json.loads((BASE/'PRIOR_HASH_REFERENCE.json').read_text())['hashes'])
source_meta=json.loads((BASE/'SOURCE_ARCHIVES.json').read_text())
rows=[]; checks=[]
def sha(b): return hashlib.sha256(b).hexdigest()
def walk(blob, chain, out):
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        members={}
        for entry in z.infolist():
            if entry.is_dir(): continue
            rel=PurePosixPath(entry.filename)
            assert not rel.is_absolute() and '..' not in rel.parts
            assert not stat.S_ISLNK(entry.external_attr>>16)
            data=z.read(entry); members[entry.filename]=data
            dest=out/rel
            assert dest.is_file() and dest.read_bytes()==data, str(dest)
            rows.append({'archive':chain, 'member':entry.filename,'sha256':sha(data),
                         'size':len(data),'path':str(dest.relative_to(BASE)),
                         'new_to_combined_prior':sha(data) not in known})
            if data.startswith(b'PK\x03\x04'):
                walk(data, chain+'!'+entry.filename, out/(entry.filename+'.unpacked'))
        for name,data in members.items():
            if PurePosixPath(name).name not in ('SHA256SUMS.txt','SHA256SUMS','MANIFEST.sha256'): continue
            for line in data.decode().splitlines():
                if not line.strip(): continue
                match=re.fullmatch(r'([0-9a-fA-F]{64})\s+\*?(.+)',line)
                assert match, (name,line)
                target=match[2]
                candidates={str(PurePosixPath(name).parent/target),target}
                existing=sorted(t for t in candidates if t in members)
                assert existing, (chain,name,target,'no manifest target')
                hashes={sha(members[t]) for t in existing}
                assert len(hashes)==1, (chain,name,target,'ambiguous target')
                expected=match[1].lower(); actual=next(iter(hashes))
                assert expected==actual, (chain,name,target,'hash mismatch')
                checks.append({'archive':chain,'manifest':name,'member':target,
                               'resolved_member':existing[0],'expected':expected,
                               'actual':actual,'pass':True})
for source in source_meta:
    f=BASE/'sources'/source['filename']; blob=f.read_bytes()
    assert len(blob)==source['bytes'] and sha(blob)==source['sha256']
    walk(blob,f.name,BASE/'extracted')
declared=json.loads((BASE/'SOURCE_MEMBER_INVENTORY.json').read_text())
assert rows==declared, 'Inventory differs'
new={r['sha256']:r for r in reversed(rows) if r['new_to_combined_prior']}
assert list(new.values())==json.loads((BASE/'NEW_UNIQUE_CONTENT.json').read_text())
summary={'top_level_archives':len(source_meta), 'recursive_member_occurrences':len(rows),
         'unique_contents':len({r['sha256'] for r in rows}), 'byte_new_contents':len(new),
         'embedded_manifest_entries':len(checks), 'failed_manifest_entries':0,
         'all_extracted_bytes_match':True, 'uploaded_code_executed':False}
(BASE/'SOURCE_MANIFEST_VERIFICATION.json').write_text(json.dumps(checks,indent=2)+'\n')
(BASE/'PROVENANCE_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
