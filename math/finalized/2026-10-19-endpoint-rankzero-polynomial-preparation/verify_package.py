#!/usr/bin/env python3
"""Documentary integrity only. Never import or execute any scientific checker."""
from pathlib import Path
import hashlib, json, re
ROOT=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(name): return json.loads((ROOT/name).read_text())
def entries(data):
    es=data.get('files',data.get('payloads',data))
    if isinstance(es,dict): return [dict(path=k,**(v if isinstance(v,dict) else {'sha256':v})) for k,v in es.items()]
    return [dict(x,path=x.get('path',x.get('name'))) for x in es]
def main():
    seal=read('SEAL.json'); manifest=read('MANIFEST.json'); allow=read('PRESERVATION_ALLOWLIST.json')
    for name,key in [('MANIFEST.json','manifest_sha256'),('PRESERVATION_ALLOWLIST.json','allowlist_sha256'),('FINAL_ACCEPTANCE.json','acceptance_sha256'),('OWNER_DISPOSITIONS.json','owner_dispositions_sha256')]: assert sha(ROOT/name)==seal[key],name
    actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
    assert not any(p.is_symlink() for p in ROOT.rglob('*'))
    assert actual==set(allow['files'])
    assert set(e['path'] for e in manifest['files'])==actual-{'MANIFEST.json','SEAL.json'}
    for e in manifest['files']: assert sha(ROOT/e['path'])==e['sha256'] and (ROOT/e['path']).stat().st_size==e['bytes'],e['path']
    binds=read('COPY_BINDINGS.json')
    assert len({e['public_path'] for e in binds['files']})==len(binds['files'])
    for e in binds['files']:
        assert e['transformation']=='EXACT_COPY'
        assert e['source_sha256']==e['public_sha256']==sha(ROOT/e['public_path'])
        assert e['source_bytes']==e['public_bytes']==(ROOT/e['public_path']).stat().st_size
    for s in binds['source_sets']:
        mp=ROOT/s['public_prefix']/s['manifest']
        assert sha(mp)==s['manifest_sha256']
        for e in entries(json.loads(mp.read_text())):
            p=mp.parent/e['path']; assert p.is_file() and sha(p)==e['sha256'],str(p)
            if 'bytes' in e:assert p.stat().st_size==e['bytes']
        for extra in s.get('seal_files',[]):assert sha(mp.parent/extra['path'])==extra['sha256']
    accept=read('FINAL_ACCEPTANCE.json')
    assert set(accept['results'])=={'endpoint','rankzero','polynomial'}
    expected={'endpoint':'0f712d2a44f41405de345ce44bd4a76f8d57ab467e5a61d2645363e1cb433453','rankzero':'4eff619bfde38551a47bf2e109307bb565e09eea5cc42d59213f9513023cb621','polynomial':'9e8b30f239ce33f99fbae74f9ad6ab82694e116e14b34f154611e4ac09e58cd2'}
    for k,e in accept['results'].items():
        assert e['independently_accepted'] and not e['owner_closure']
        for name in ['candidate_manifest','review_manifest','accepted_proof','review','verdict']:
            assert sha(ROOT/e[name+'_path'])==e[name+'_sha256']
        assert e['accepted_proof_sha256']==expected[k]
        v=read(e['verdict_path']);assert v['verdict'] in ['PASS','ACCEPT','SCOPED_ACCEPT']
        bound=v.get('candidate_proof_sha256',v.get('candidate_binding',{}).get('report_sha256'))
        assert bound==expected[k]
    scopes=read('OWNER_DISPOSITIONS.json')
    assert scopes['owner_closures']==scopes['priority_changes']==scopes['census_change']==0
    for owner,score in [('M-SPARSE-DEFECT',42),('PHASE-DEFECT-RANK-20261011',37),('ALG-EVEN-PRONY-EXTRA-POLE',42),('NF-03',37)]:
        e=scopes['owners'][owner]; assert e['status']=='TO RESEARCH' and e['priority']==score and not e['owner_closure']
    omissions=read('OMISSIONS.json'); assert not omissions['omitted_manifest_declared_source_files']
    assert read('PROJECTION_DISCLOSURE.json')['privacy_projected_files']==0
    bad=re.compile(r'https?://docs\.google\.com/spreadsheets|libfile_[A-Za-z0-9]+|file_000000[0-9a-f]+|Bearer\s+[A-Za-z0-9_.-]+',re.I)
    for p in ROOT.rglob('*'):
        if p.is_file() and p.suffix in ['.md','.json','.txt','.py','.stdout','.stderr'] and p.name!='verify_package.py':assert not bad.search(p.read_text()),str(p)
    readme=(ROOT/'README.md').read_text()
    for phrase in ['q<d<2q','period N/2','exact C8 rank-zero value','O~((N^8+Np)^3)','O~(N^9+Np)','not implemented','2^(2N^4)','42-cell/index batch']:assert phrase in readme,phrase
    assert not seal['external_writes'] and not seal['scientific_reruns_during_packaging']
    print(json.dumps({'status':'PASS','public_files':len(actual),'exact_copy_bindings':len(binds['files']),'frozen_source_sets':len(binds['source_sets']),'independent_acceptances':3,'owner_closures':0,'privacy_projections':0,'mathematical_programs_executed':False,'external_writes':False},indent=2))
if __name__=='__main__':main()
