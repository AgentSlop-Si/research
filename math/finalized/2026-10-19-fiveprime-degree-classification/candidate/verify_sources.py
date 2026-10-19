"""Verify frozen synthesis sources. No historical scientific checker is executed."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())
def dump(name,x): (HERE/name).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')

def verify():
    bindings=read(HERE/'SOURCE_BINDINGS.json')
    for x in bindings['copied_sources']:
        a,b=Path(x['source']),HERE/x['copy']
        assert len(b.read_bytes())==x['bytes']
        assert sha(a)==sha(b)==x['sha256'],x
    packets=[]
    for x in bindings['dependencies']:
        base=Path(x['candidate_directory'])
        assert sha(base/'REPORT.md')==x['expected_report_sha256']
        assert sha(base/'MANIFEST.json')==x['expected_manifest_sha256']
        review=Path(x['review_directory'])/'REVIEW.md'
        body=review.read_text()
        assert x['expected_report_sha256'] in body or x['label']=='M'
        assert x['expected_manifest_sha256'] in body
        verdict=Path(x['review_directory'])/'VERDICT.json'
        if verdict.exists():
            v=read(verdict)
            assert v.get('verdict',v.get('status'))=='PASS'
            assert v['candidate_report_sha256']==x['expected_report_sha256']
            assert v['candidate_manifest_sha256']==x['expected_manifest_sha256']
        else:
            assert x['label']=='E' and 'ACCEPT all four' in body
        m=read(base/'MANIFEST.json'); entries=m.get('files',m.get('entries'))
        if isinstance(entries,dict): entries=[{'path':k,'sha256':v} for k,v in entries.items()]
        for e in entries:
            p=base/e['path']; assert sha(p)==e['sha256'],str(p)
            if 'bytes' in e: assert len(p.read_bytes())==e['bytes'],str(p)
        sb=read(base/'SOURCE_BINDINGS.json')
        if isinstance(sb,dict): sb=sb['copied_sources']
        for e in sb:
            orig=Path(e.get('source',e.get('source_path',e.get('original_path'))))
            copied=base/e.get('copy',e.get('frozen_copy',e.get('frozen_path')))
            assert sha(orig)==sha(copied)==e['sha256'],str(orig)
        seal=base/'SEAL.sha256'
        if seal.exists(): assert x['expected_manifest_sha256'] in seal.read_text()
        else: assert x['label']=='E'
        packets.append({'label':x['label'],'candidate_directory':str(base),'candidate_report_sha256':sha(base/'REPORT.md'),'candidate_manifest_sha256':sha(base/'MANIFEST.json'),'review_sha256':sha(review),'candidate_files_verified':len(entries),'original_source_copies_verified':len(sb),'accepted_report_and_manifest_binding':'PASS'})
    owner=read(HERE/'sources/O_selected_record.json')
    assert owner['stable_id']=='M-SPARSE-DEFECT' and owner['status']=='TO RESEARCH' and owner['priority']==42
    assert sha(HERE/'sources/O_selected_record.json')=='5e83ba9af8f8b392162bb12209555b4bddc8b42d7f7007318c2b1eaa64b08bee'
    assert sha(HERE/'sources/O_phase20_audit.md')=='e7413d1d591cfae89647304a88b1ca664dea9602dd86fec79a58688f346a7946'
    out={'result':'PASS','source_copies_verified':len(bindings['copied_sources']),'dependencies':packets,'candidate_files_verified':sum(x['candidate_files_verified'] for x in packets),'original_source_copies_verified':sum(x['original_source_copies_verified'] for x in packets),'original_owner_verified':True,'historical_checker_executed':False,'new_scientific_test_counts_claimed':False,'external_writes':False,'scope':'Provenance integrity and acceptance bindings; mathematical synthesis is the symbolic proof in REPORT.md, pending its own independent review.'}
    dump('SOURCE_VERIFICATION.json',out)
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': verify()
