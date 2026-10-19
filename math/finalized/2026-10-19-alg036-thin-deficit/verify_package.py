#!/usr/bin/env python3
"""Verify documentary integrity and scope, without executing research programs."""
from pathlib import Path
import hashlib,json,re

def main():
    root=Path(__file__).resolve().parent
    read=lambda p:json.loads((root/p).read_text())
    sha=lambda p:hashlib.sha256((root/p).read_bytes()).hexdigest()
    allow=read('PRESERVATION_ALLOWLIST.json'); paths=allow['files']
    assert paths==sorted(set(paths))
    assert all(not Path(p).is_absolute() and '..' not in Path(p).parts for p in paths)
    assert not any(p.is_symlink() for p in root.rglob('*'))
    assert sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file())==paths
    man=read('MANIFEST.json')
    assert sorted(x['path'] for x in man['files'])==sorted(set(paths)-{'MANIFEST.json','SEAL.json'})
    for e in man['files']:
        assert sha(e['path'])==e['sha256'] and (root/e['path']).stat().st_size==e['bytes'],e['path']
    seal=read('SEAL.json')
    for name,key in [('MANIFEST.json','manifest_sha256'),('PRESERVATION_ALLOWLIST.json','allowlist_sha256'),('FINAL_ACCEPTANCE.json','acceptance_sha256'),('OWNER_DISPOSITION.json','owner_disposition_sha256')]:
        assert sha(name)==seal[key]
    assert seal['accepted_selected_thin_deficit_gate_closed'] is True
    assert seal['broad_owner_closures']==0 and seal['owner_priority']==34 and seal['owner_status']=='TO RESEARCH'
    assert seal['historical_novelty_claim'] is False and seal['scientific_reruns_during_packaging'] is False and seal['external_writes'] is False
    bindings=read('COPY_BINDINGS.json')['files']; by_path={e['public_path']:e for e in bindings}
    assert len(by_path)==len(bindings)==25
    expected={'candidate':'829f407ab9681470de0838856ee64eb9611e56214d6f893a2f1bc63e6f4776b5','review':'863507f193ea7582097ebac677fa37b96288470ec007f3da869d8506819ac784'}
    for label,h in expected.items():
        m=label+'/MANIFEST.sha256';assert sha(m)==h
        declared={}
        for line in (root/m).read_text().splitlines():
            digest,rel=line.split('  ',1)
            assert rel not in declared and not Path(rel).is_absolute() and '..' not in Path(rel).parts
            declared[rel]=digest;assert sha(label+'/'+rel)==digest
        assert {label+'/'+r for r in declared}|{m}=={p for p in by_path if p.startswith(label+'/')}
    for e in bindings:
        assert e['transformation']=='EXACT_COPY'
        assert sha(e['public_path'])==e['source_sha256']==e['public_sha256']
        assert (root/e['public_path']).stat().st_size==e['source_bytes']==e['public_bytes']
        assert e['source_manifest_sha256']==expected[e['public_path'].split('/')[0]]
    a=read('FINAL_ACCEPTANCE.json');v=read('review/VERDICT.json')
    for key in ['candidate_manifest','review_manifest','accepted_report','review','verdict']:
        assert sha(a[key+'_path'])==a[key+'_sha256']
    assert a['candidate_manifest_sha256']==expected['candidate'] and a['review_manifest_sha256']==expected['review']
    assert a['accepted_report_sha256']=='ae348fde6e14b20f3bb7227a7c56c37d979136a5eed1540de933bf940e97b851'
    assert a['review_sha256']=='1ec251108495327dc66c5fbef1fde769e0d6d49b3f3bfa5babe7c847e67feb50'
    assert v['review_status']=='ACCEPTED_SCOPED' and v['required_corrections']==[] and v['unresolved_lemma_in_selected_scope'] is None
    assert v['candidate_manifest_sha256']==expected['candidate'] and v['candidate_report_sha256']==a['accepted_report_sha256']
    assert a['accepted_result']==v['accepted_result'] and a['accepted_consequences']==v['accepted_consequences'] and a['excluded_claims']==v['excluded_claims']
    assert sha('candidate/MANIFEST.sha256')==sha('review/CANDIDATE_MANIFEST.sha256')
    assert sha('candidate/controls/check_thin_deficit.py')==sha('review/controls/author_replay/check_thin_deficit.py')
    assert sha('candidate/controls/RESULTS.json')==sha('review/controls/author_replay/RESULTS.json')==v['author_results_sha256']
    author=read('candidate/controls/RESULTS.json');stdout=read('review/controls/author_replay/stdout.json')
    assert all(author[key]==value for key,value in stdout.items())
    for p in ['candidate/controls/RESULTS.json','review/controls/independent_checks.json','review/controls/window_sphere_checks.json','review/controls/audit_sources.json']:
        assert read(p)['status']=='PASS'
    assert v['inspected_author_replay']=='PASS_BYTE_IDENTICAL' and v['primary_source_independently_verified'] is True
    for s in read('candidate/SOURCE_MANIFEST.json')['sources']:
        if 'local_copy' in s:
            p='candidate/'+s['local_copy'];assert sha(p)==s['sha256'] and (root/p).stat().st_size==s['bytes']
    d=read('OWNER_DISPOSITION.json')
    assert d['owner_id']=='ALG-036' and d['recommended_owner_status']=='TO RESEARCH' and d['recommended_owner_priority']==34
    assert d['owner_closures']==d['priority_changes']==0 and d['no_new_owner_or_census_entry'] is True
    projection=read('PROJECTION_DISCLOSURE.json')
    assert projection['privacy_projected_files']==0 and projection['files']==[] and projection['source_path_adaptations'] is False
    assert read('OMISSIONS.json')['omitted_manifest_declared_source_files']==[]
    forbidden=[r'https?://docs[.]google[.]com/spreadsheets/d/',r'"spreadsheet_id"\s*:',r'sediment://',r'libfile_',r'"download_url"\s*:',r'Bearer\s+[A-Za-z0-9]',r'/root/',r'dream_notes',r'cloud_threads']
    for p in paths:
        f=root/p;assert f.suffix.lower() in {'.md','.json','.py','.sha256','.txt'}
        if p=='verify_package.py':continue
        assert not any(re.search(pattern,f.read_text()) for pattern in forbidden),p
    print(json.dumps({'status':'PASS','files':len(paths),'manifest_entries_verified':len(man['files']),'copy_bindings_verified':len(bindings),'accepted_manifests_verified':2,'selected_thin_deficit_gate_closed':True,'broad_owner_closures':0,'privacy_projections':0,'scope_checks':'PASS','bounded_privacy_scan':'PASS','scientific_reruns':False},indent=2))

if __name__=='__main__':main()
