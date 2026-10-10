#!/usr/bin/env python3
"""Independent inert ZIP/source audit. Never imports or executes archive members."""
from pathlib import Path,PurePosixPath
import hashlib,io,json,re,stat,zipfile

BASE=Path(__file__).resolve().parent
known=set(json.loads((BASE/'PRIOR_HASH_REFERENCE.json').read_text())['hashes'])
meta=json.loads((BASE/'SOURCE_IDENTITIES.json').read_text())
rows=[]; checks=[]; archives=[]
def sha(b): return hashlib.sha256(b).hexdigest()
def save_json(name,data): (BASE/name).write_text(json.dumps(data,indent=2)+'\n')
def walk(blob,chain,out,depth=0):
    assert depth<32
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        members={}
        for item in z.infolist():
            if item.is_dir(): continue
            rel=PurePosixPath(item.filename)
            assert not rel.is_absolute() and '..' not in rel.parts
            assert not stat.S_ISLNK(item.external_attr>>16)
            assert item.filename not in members,'Duplicate archive path'
            data=z.read(item); members[item.filename]=data
            dst=out/rel; dst.parent.mkdir(parents=True,exist_ok=True)
            if dst.exists(): assert dst.read_bytes()==data,'Extracted bytes differ'
            else: dst.write_bytes(data)
            rows.append({'archive':chain,'member':item.filename,'path':str(dst.relative_to(BASE)),
                         'sha256':sha(data),'bytes':len(data),'new_to_combined_prior':sha(data) not in known})
            if zipfile.is_zipfile(io.BytesIO(data)):
                walk(data,chain+'!'+item.filename,out/(item.filename+'.unpacked'),depth+1)
        for name,data in members.items():
            if PurePosixPath(name).name not in ('SHA256SUMS.txt','SHA256SUMS','MANIFEST.sha256'): continue
            for line in data.decode().splitlines():
                if not line.strip(): continue
                m=re.fullmatch(r'([0-9a-fA-F]{64})\s+\*?(.+)',line)
                assert m,(chain,name,line)
                target=m[2]; rel=PurePosixPath(target)
                assert not rel.is_absolute() and '..' not in rel.parts
                candidates={str(PurePosixPath(name).parent/rel),target}
                present=sorted(c for c in candidates if c in members)
                assert present,(chain,name,target,'Missing checksum target')
                hashes={sha(members[c]) for c in present}
                assert len(hashes)==1,(chain,name,target,'Ambiguous checksum target')
                actual=next(iter(hashes)); assert actual==m[1].lower(),(chain,name,target,'Failed checksum')
                checks.append({'archive':chain,'manifest':name,'target':target,'resolved_target':present[0],
                               'sha256':actual,'passed':True})
for s in meta:
    f=BASE/'sources'/s['filename']; data=f.read_bytes()
    assert len(data)==s['bytes'] and sha(data)==s['sha256']
    archives.append({**s,'sha256':sha(data),'identical_to_prior_source_content':sha(data) in known})
    walk(data,f.name,BASE/'extracted'/f.stem)
new={}
for r in rows:
    if r['new_to_combined_prior']: new.setdefault(r['sha256'],r)
summary={'top_level_archives':len(meta),'recursive_member_occurrences':len(rows),
         'unique_member_contents':len({r['sha256'] for r in rows}),'new_unique_member_contents':len(new),
         'embedded_manifest_checks':len(checks),'failed_manifest_checks':0,
         'new_text_data_contents':sum(not r['member'].endswith(('.zip','.pyc')) for r in new.values()),
         'new_nested_archives':sum(r['member'].endswith('.zip') for r in new.values()),
         'new_bytecode_contents':sum(r['member'].endswith('.pyc') for r in new.values()),
         'all_extracted_bytes_match':True,'uploaded_programs_executed':False}
for n,v in [('SOURCE_ARCHIVES.json',archives),('SOURCE_MEMBER_INVENTORY.json',rows),
            ('NEW_UNIQUE_CONTENT.json',list(new.values())),('SOURCE_MANIFEST_VERIFICATION.json',checks),
            ('PROVENANCE_SUMMARY.json',summary)]: save_json(n,v)
print(json.dumps(summary,indent=2))
