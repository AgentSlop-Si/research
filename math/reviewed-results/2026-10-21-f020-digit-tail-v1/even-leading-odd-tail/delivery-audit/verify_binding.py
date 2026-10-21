#!/usr/bin/env python3
"""Read-only exact detached-audit inventory and main-archive binding."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,re
ROOT=Path(__file__).resolve().parent

def need(x,m):
    if not x:raise ValueError(m)
def H(b):return hashlib.sha256(b).hexdigest()
def pairs(ps):
    d={}
    for k,v in ps:
        need(k not in d,'Duplicate JSON key');d[k]=v
    return d
def load(p):return json.loads(p.read_bytes(),object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in()).throw(ValueError('Nonfinite JSON')))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--expect-manifest',required=True);ap.add_argument('main_archive',type=Path);a=ap.parse_args()
    need(re.fullmatch('[0-9a-f]{64}',a.expect_manifest) is not None,'Trusted audit manifest digest required')
    need(not ROOT.is_symlink() and not any(p.is_symlink() for p in ROOT.rglob('*')),'Symlink forbidden')
    need(H((ROOT/'MANIFEST.json').read_bytes())==a.expect_manifest,'Trusted audit manifest mismatch')
    m=load(ROOT/'MANIFEST.json');s=load(ROOT/'SEAL.json');need(s['manifest_sha256']==a.expect_manifest,'Audit seal mismatch');seen={'MANIFEST.json','SEAL.json'}
    for row in m['files']:
        n=row['path'];p=PurePosixPath(n);need(n==str(p) and not p.is_absolute() and '..' not in p.parts and '\\' not in n and ':' not in n and n not in seen,'Unsafe or duplicate audit path');seen.add(n);b=(ROOT/n).read_bytes();need(type(row['bytes'])is int and len(b)==row['bytes'] and H(b)==row['sha256'],'Audit member mismatch')
    need({p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}==seen,'Audit file inventory mismatch')
    need(not any(p.is_dir() for p in ROOT.rglob('*')),'Unexpected audit directory')
    v=load(ROOT/'VERDICT.json');need(v['verdict']=='ACCEPTED_PUBLIC_BYTES_WITHIN_EXACT_STATED_SCOPE','Nonaccepting audit verdict');b=a.main_archive.read_bytes();need(type(v['main_archive']['bytes'])is int and len(b)==v['main_archive']['bytes'] and H(b)==v['main_archive']['sha256'],'Main archive does not match audit')
    print(json.dumps({'status':'PASS','audit_manifest_sha256':a.expect_manifest,'main_archive_sha256':H(b)},sort_keys=True))
if __name__=='__main__':main()
