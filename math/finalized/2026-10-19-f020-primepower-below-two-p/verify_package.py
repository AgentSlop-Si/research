#!/usr/bin/env python3
"""Verify documentary integrity without executing any scientific checker."""
from pathlib import Path
import hashlib,json,re

def main():
    root=Path(__file__).resolve().parent
    read=lambda p:json.loads((root/p).read_text())
    sha=lambda p:hashlib.sha256((root/p).read_bytes()).hexdigest()
    allow=read('PRESERVATION_ALLOWLIST.json'); paths=allow['files']
    assert allow['repository']=='AgentSlop-Si/research'
    assert allow['public_prefix']=='math/finalized/2026-10-19-f020-primepower-below-two-p'
    assert paths==sorted(set(paths))
    assert all(not Path(p).is_absolute() and '..' not in Path(p).parts for p in paths)
    assert not any(p.is_symlink() for p in root.rglob('*'))
    assert sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file())==paths
    manifest=read('MANIFEST.json')
    assert manifest['excluded_from_this_hash_list']==['MANIFEST.json','SEAL.json']
    assert sorted(e['path'] for e in manifest['files'])==sorted(set(paths)-{'MANIFEST.json','SEAL.json'})
    for e in manifest['files']:
        assert (root/e['path']).stat().st_size==e['bytes'] and sha(e['path'])==e['sha256'],e['path']
    seal=read('SEAL.json')
    for name,key in [('MANIFEST.json','manifest_sha256'),('PRESERVATION_ALLOWLIST.json','allowlist_sha256'),('FINAL_ACCEPTANCE.json','acceptance_sha256'),('OWNER_DISPOSITION.json','owner_disposition_sha256')]:
        assert sha(name)==seal[key]
    assert seal['accepted_range']=='0<=b<min(2p,p^s), p odd prime, s>=1'
    assert seal['accepted_characteristic_zero_collision'] is False
    assert seal['unrestricted_ordinary_guard_closed'] is False
    assert seal['broad_owner_closures']==0 and seal['owner_status']=='TO RESEARCH' and seal['owner_priority']==58
    assert seal['historical_novelty_claim'] is False and seal['scientific_reruns_during_packaging'] is False and seal['external_writes'] is False
    bindings=read('COPY_BINDINGS.json')['files']; by_path={e['public_path']:e for e in bindings}
    assert len(bindings)==len(by_path)==27
    for e in bindings:
        assert e['transformation']=='EXACT_COPY'
        assert sha(e['public_path'])==e['source_sha256']==e['public_sha256']
        assert (root/e['public_path']).stat().st_size==e['source_bytes']==e['public_bytes']
    for directory,n in [('candidate',9),('review',16)]:
        m=read(directory+'/MANIFEST.json'); assert len(m['files'])==n
        assert {directory+'/'+e['path'] for e in m['files']}|{directory+'/MANIFEST.json'}=={p for p in by_path if p.startswith(directory+'/')}
        for e in m['files']:
            b=by_path[directory+'/'+e['path']]
            assert e['sha256']==b['source_sha256'] and e['bytes']==b['source_bytes']
            assert b['source_manifest_sha256']==sha(directory+'/MANIFEST.json')
    a=read('FINAL_ACCEPTANCE.json')
    for key in ['candidate_manifest','review_manifest','accepted_proof','review','verdict']:
        assert sha(a[key+'_path'])==a[key+'_sha256']
    assert a['candidate_manifest_sha256']=='6a0c2cf641ff4a54ce98b9b83f2463f4ffa34425da4b4305fa995be8e615634a'
    assert a['review_manifest_sha256']=='fa65a6542328a40af8fcd163d5224e5e120c4387ca33e551676cb7fc5770a502'
    assert a['accepted_proof_sha256']=='4e68e5e6b9fe2c372cff20ca78de54deb2151ecf0f4e040780edd4c3cf537b79'
    v=read('review/VERDICT.json')
    assert v['verdict']=='ACCEPT' and v['author_manifest_sha256']==a['candidate_manifest_sha256']
    assert v['author_report_sha256']==a['accepted_proof_sha256'] and v['independent_checks']==208 and v['author_replay_checks']==418
    assert v['blocking_issues']==[] and v['status_preserved']=={'F020':'open','priority':58,'F023':'alias of F020'}
    for src,dst in [('MANIFEST.json','sources/candidate_manifest.json'),('REPORT.md','sources/candidate_report.md'),('CHECKS.json','replay/CHECKS.json'),('check_hensel_extension.py','replay/check_hensel_extension.py'),('check_run.log','replay/replay_run.log'),('sources/uniform_guards_report.md','sources/uniform_guards_report.md'),('sources/metric_obstruction_report.md','sources/metric_obstruction_report.md')]:
        assert sha('candidate/'+src)==sha('review/'+dst)
    c=read('candidate/CHECKS.json'); assert c['count']==418 and c['all_passed'] is True and len(c['checks'])==418 and all(x['passed'] for x in c['checks'])
    i=read('review/INDEPENDENT_CHECKS.json'); assert i['passed']==208 and len(i['checks'])==208 and all(x['passed'] for x in i['checks'])
    iv=read('review/INPUT_VERIFICATION.json'); assert iv['all_passed'] is True and len(iv['files'])==9 and all(x['passed'] for x in iv['files'])
    assert iv['author_checks_replay_byte_identical'] is True and iv['author_replay_check_count']==418
    p=read('PROJECTION_DISCLOSURE.json'); assert p['privacy_projected_files']==0 and p['files']==[] and p['source_path_adaptations'] is False
    d=read('OWNER_DISPOSITION.json')
    assert d['owner_id']=='F020' and d['alias_id']=='F023' and d['recommended_owner_status']=='TO RESEARCH' and d['recommended_owner_priority']==58
    assert d['owner_closures']==0 and d['priority_changes']==0 and d['no_new_owner_or_census_entry'] is True
    assert d['unrestricted_ordinary_guard_closed'] is False and d['historical_novelty_claim'] is False
    forbidden=[r'https?://docs[.]google[.]com/spreadsheets/d/',r'"spreadsheet_id"\s*:',r'sediment://',r'libfile_',r'"download_url"\s*:',r'Bearer\s+[A-Za-z0-9]',r'/root/',r'dream_notes',r'cloud_threads']
    for name in paths:
        f=root/name;assert f.suffix.lower() in {'.json','.md','.py','.log'}
        if name=='verify_package.py':continue
        assert not any(re.search(pattern,f.read_text()) for pattern in forbidden),name
    print(json.dumps({'status':'PASS','files':len(paths),'manifest_entries_verified':len(manifest['files']),'copy_bindings_verified':len(bindings),'accepted_independent_checks':208,'accepted_author_checks':418,'privacy_projections':0,'broad_owner_closures':0,'scope_checks':'PASS','bounded_privacy_scan':'PASS','scientific_reruns':False},indent=2))

if __name__=='__main__':main()
