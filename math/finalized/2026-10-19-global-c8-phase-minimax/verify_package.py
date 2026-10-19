#!/usr/bin/env python3
"""Check documentary integrity; never execute scientific checkers."""
from pathlib import Path
import hashlib,json,re

def main():
 root=Path(__file__).resolve().parent
 get=lambda p:json.loads((root/p).read_text())
 sha=lambda p:hashlib.sha256((root/p).read_bytes()).hexdigest()
 entries=lambda m:m['files'] if 'files' in m else [dict(path=k,**v) for k,v in m.items()]
 allow=get('PRESERVATION_ALLOWLIST.json');paths=allow['files']
 assert len(paths)==len(set(paths))
 assert all(not Path(p).is_absolute() and '..' not in Path(p).parts for p in paths)
 assert not any(p.is_symlink() for p in root.rglob('*'))
 assert sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file())==paths
 manifest=get('MANIFEST.json')
 assert sorted(x['path'] for x in manifest['files'])==sorted(set(paths)-{'MANIFEST.json','SEAL.json'})
 for e in manifest['files']:
  assert (root/e['path']).stat().st_size==e['bytes'] and sha(e['path'])==e['sha256'],e['path']
 seal=get('SEAL.json')
 for name,key in [('MANIFEST.json','manifest_sha256'),('PRESERVATION_ALLOWLIST.json','allowlist_sha256'),('FINAL_ACCEPTANCE.json','acceptance_sha256'),('OWNER_DISPOSITION.json','owner_disposition_sha256')]: assert sha(name)==seal[key]
 assert seal['accepted_global_value']=='sin(pi/16)' and seal['accepted_named_global_minimax_closed'] is True
 assert seal['broad_owner_closures']==0 and seal['owner_priority']==37 and seal['owner_status']=='TO RESEARCH'
 assert seal['historical_novelty_claim'] is False and seal['scientific_reruns_during_packaging'] is False and seal['external_writes'] is False
 binding=get('COPY_BINDINGS.json')['files'];by_path={e['public_path']:e for e in binding}
 assert len(by_path)==len(binding)==24
 for e in binding:
  assert e['transformation']=='EXACT_COPY'
  assert sha(e['public_path'])==e['public_sha256']==e['source_sha256']
  assert (root/e['public_path']).stat().st_size==e['public_bytes']==e['source_bytes']
 for directory in ['candidate','review']:
  fs=entries(get(directory+'/MANIFEST.json'))
  assert {directory+'/'+e['path'] for e in fs}|{directory+'/MANIFEST.json'}=={p for p in by_path if p.startswith(directory+'/')}
  for e in fs:
   b=by_path[directory+'/'+e['path']];assert e['sha256']==b['source_sha256'] and e['bytes']==b['source_bytes']
   assert b['source_manifest_sha256']==sha(directory+'/MANIFEST.json')
 a=get('FINAL_ACCEPTANCE.json')
 for key in ['candidate_manifest','review_manifest','accepted_proof','review','verdict']:
  assert sha(a[key+'_path'])==a[key+'_sha256']
 assert a['candidate_manifest_sha256']=='2a2c1d375e060694ebb9940c81d2e25aae7c74c4c96ef883ff15eb9841f95e41'
 assert a['review_manifest_sha256']=='386947029c45fc376f9f0db74add1ca525cee47b086f1e031ab0780790467d9d'
 assert a['accepted_proof_sha256']=='9a4408945946d283daefd1b8c06bc2dbe3c7c59f4f8f18cc2c66034155a31b3c'
 v=get('review/VERDICT.json');assert v['verdict']=='ACCEPT' and v['accepted_value']=='sin(pi/16)'
 assert v['frozen_candidate_proof_sha256']==a['accepted_proof_sha256']
 for n in ['PROOF.md','EXACT_GLOBAL_CHECKS.json','exact_global_checker.py','exact_global_stdout.txt']:
  assert sha('candidate/'+n)==sha('review/frozen_candidate/'+n)
 assert sha('candidate/REVIEW.md')==sha('review/REVIEW.md')
 assert sha('candidate/REVIEW_VERDICT.json')==sha('review/VERDICT.json')
 assert sha('candidate/EXACT_GLOBAL_CHECKS.json')==sha('candidate/exact_global_stdout.txt')
 assert sha('review/INDEPENDENT_RESULTS.json')==sha('review/independent_stdout.txt')
 assert get('candidate/EXACT_GLOBAL_CHECKS.json')['status']=='PASS'
 ir=get('review/INDEPENDENT_RESULTS.json');assert ir['status']=='PASS' and ir['generic_fourier_coefficients']==512 and ir['rank_one_minors']==784 and len(ir['mutation_controls'])==6 and all(ir['mutation_controls'].values())
 p=get('PROJECTION_DISCLOSURE.json');assert p['privacy_projected_files']==0 and p['files']==[] and p['source_path_adaptations'] is False
 supporting=get('SUPPORTING_SOURCE_BINDINGS.json')
 assert len(supporting['files'])==2
 for e in supporting['files']:assert e==by_path[e['public_path']] and e['source_manifest_sha256']==supporting['source_manifest_sha256']
 d=get('OWNER_DISPOSITION.json')
 assert d['owner_id']=='PHASE-DEFECT-RANK-20261011' and d['recommended_owner_status']=='TO RESEARCH' and d['recommended_owner_priority']==37 and d['owner_closures']==0 and d['priority_changes']==0
 assert d['no_new_owner_or_census_entry'] is True
 forbidden=[r'https?://docs[.]google[.]com/spreadsheets/d/',r'"spreadsheet_id"\s*:',r'sediment://',r'libfile_',r'"download_url"\s*:',r'Bearer\s+[A-Za-z0-9]',r'/root/',r'dream_notes',r'cloud_threads']
 for name in paths:
  f=root/name;assert f.suffix.lower() in {'.json','.md','.py','.txt'}
  if name=='verify_package.py':continue
  t=f.read_text();assert not any(re.search(pattern,t) for pattern in forbidden),name
 print(json.dumps({'status':'PASS','files':len(paths),'manifest_entries_verified':len(manifest['files']),'copy_bindings_verified':len(binding),'privacy_projections':0,'named_global_minimax_closed':True,'broad_owner_closures':0,'scope_checks':'PASS','bounded_privacy_scan':'PASS','scientific_reruns':False},indent=2))
if __name__=='__main__':main()
