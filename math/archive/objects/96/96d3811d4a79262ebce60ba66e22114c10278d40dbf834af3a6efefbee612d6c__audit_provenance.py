#!/usr/bin/env python3
"""Read-only nested ZIP audit, never executing archive members. Standard library."""
from pathlib import Path, PurePosixPath
from zipfile import ZipFile
import hashlib, io, json, re, os

ROOT=Path(__file__).resolve().parent
def digest(b):return hashlib.sha256(b).hexdigest()
def main():
    prior=set(json.loads((ROOT/'PRIOR_HASH_REFERENCE.json').read_text())['hashes'])
    ids=json.loads((ROOT/'SOURCE_IDENTITIES.json').read_text())
    inventory=[];checks=[];archives=[];new={};budget=0
    def visit(data,origin,depth=0):
        nonlocal budget
        assert depth<32
        with ZipFile(io.BytesIO(data)) as z:
            names=z.namelist();assert len(names)==len(set(names))
            payload={}
            for obj in z.infolist():
                path=PurePosixPath(obj.filename)
                assert not path.is_absolute() and '..' not in path.parts
                assert (obj.external_attr>>16)&0o170000 != 0o120000, 'symlink source'
                if obj.is_dir():continue
                budget+=obj.file_size;assert budget<250_000_000
                raw=z.read(obj);payload[obj.filename]=raw
                sha=digest(raw)
                row={'archive':origin,'member':obj.filename,'bytes':len(raw),'sha256':sha,'new_to_prior_source_union':sha not in prior}
                inventory.append(row)
                if sha not in prior:new.setdefault(sha,row)
            for name,raw in payload.items():
                if PurePosixPath(name).name.upper().startswith('SHA256SUMS'):
                    parent=PurePosixPath(name).parent
                    for no,line in enumerate(raw.decode().splitlines(),1):
                        if not line.strip() or line.lstrip().startswith('#'):continue
                        m=re.match(r'^([0-9a-fA-F]{64})\s+\*?(.+?)\s*$',line)
                        assert m,(origin,name,no,line)
                        wanted=m.group(2);choices=[str(parent/wanted),wanted]
                        target=next((x for x in choices if x in payload),None)
                        ok=target is not None and digest(payload[target])==m.group(1).lower()
                        checks.append({'archive':origin,'manifest':name,'line':no,'target':target or wanted,'ok':ok})
                        assert ok,(origin,name,no,wanted)
                if name.lower().endswith('.zip'):visit(raw,origin+'!/'+name,depth+1)
    for identity in ids:
        name=identity['file_name'];path=ROOT/'source_archives'/name
        if not path.exists():path=ROOT/'downloads'/name
        data=path.read_bytes();assert len(data)==identity['size_bytes'];assert digest(data)==identity['sha256']
        version=identity['version']
        if 'user.library-file-version' in os.listxattr(path):version=int(os.getxattr(path,'user.library-file-version'))
        archives.append({'filename':name,'library_file_id':identity['library_file_id'],'file_id':identity['file_id'],'version':version,'bytes':len(data),'sha256':digest(data)})
        visit(data,name)
    out={'status':'PASS','outer_archives':len(archives),'recursive_member_occurrences':len(inventory),'distinct_member_contents':len({x['sha256'] for x in inventory}),'byte_new_member_contents':len(new),'embedded_checksum_entries':len(checks),'embedded_checksum_failures':sum(not x['ok'] for x in checks),'uploaded_code_executed':False}
    for name,obj in [('SOURCE_ARCHIVES.json',archives),('SOURCE_MEMBER_INVENTORY.json',inventory),('NEW_UNIQUE_CONTENT.json',list(new.values())),('SOURCE_MANIFEST_VERIFICATION.json',{'summary':out,'entries':checks})]:
        (ROOT/name).write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
