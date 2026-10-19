#!/usr/bin/env python3
"""Documentary integrity verifier. Does not execute scientific source programs."""
from pathlib import Path
import hashlib,json,re
EXPECTED_SOURCES=[{'package': 'alg036_nondivisible_extrema_20261019_1005', 'label': 'gaussian/candidate', 'manifest': 'MANIFEST.sha256', 'manifest_sha256': '02e0521e58cbea22ab9241efc945d2e487160a68b9ef419322ba96cb00113735'}, {'package': 'alg036_equality_gap_review_20261019_1003', 'label': 'gaussian/review', 'manifest': 'MANIFEST.sha256', 'manifest_sha256': '894e4b7266fb8cea03b80ab86442f8c4391f90fea21e75604cc6a03e22d44cf1'}, {'package': 'sparse_mixedprime_2q_classification_20261019_1002', 'label': 'mixedprime/candidate', 'manifest': 'MANIFEST.json', 'manifest_sha256': 'e4fbbf3512c5093ae10247c74ba74fd0badb783af2a192945c4d3a3e435f0879', 'seal': 'SEAL.sha256', 'omitted_files': [{'path': 'sources/preserved_owner_gate_REVIEW.md', 'bytes': 15533, 'sha256': 'd0fdaf76f64395c59b1d12eeb1545cd82958618b27a01a784495a2d412d7eb71', 'reason': 'Private retained native workbook metadata, row/range mappings, census and old cell-update proposal. Scientific sections 3 and 5 are retained in a separate verbatim excerpt projection.'}], 'seal_sha256': 'f21b5448ee5dc70fa3b54b8e9aacb34672347c6ec5e8174d2d703e61b893ff06'}, {'package': 'review_twoprime_mask_family_20261019_1008', 'label': 'mixedprime/review', 'manifest': 'MANIFEST.json', 'manifest_sha256': '0aa5775c09dffd4108b8edf14def34036f83177d86375c71c4b884c00fe0dc86', 'seal': 'SEAL.sha256', 'seal_sha256': '483c57c496797083f07a28ce515a0bebe71ba04973eaaf586a07308864fd7216'}, {'package': 'phase_cyclic_family_20261019_1001', 'label': 'cyclic/candidate', 'manifest': 'MANIFEST.json', 'manifest_sha256': 'a1d1a3eb5b8451f0c4cd309782034e5b768fcdcc994ade9d5d69cb42704fd31a'}, {'package': 'phase_cyclic_review_20261019_1011', 'label': 'cyclic/review', 'manifest': 'MANIFEST.json', 'manifest_sha256': 'a05779aae43c7ce0bbd6e7c2353ccacf39134f4dc00ca7cc8ed70e3574f0b0ba'}]
PREFIX='math/finalized/2026-10-19-cyclic-mixedprime-gaussian-extrema'
def manifest_entries(path):
 if path.suffix=='.sha256':
  return [{'path':line.split('  ',1)[1],'sha256':line.split('  ',1)[0]} for line in path.read_text().splitlines() if line]
 data=json.loads(path.read_text()); entries=data.get('files',data) if isinstance(data,dict) else data
 if isinstance(entries,dict): return [dict(path=k,**v) for k,v in entries.items()]
 return [dict(e,path=e.get('path',e.get('name'))) for e in entries]
def main():
 root=Path(__file__).resolve().parent
 sha=lambda p:hashlib.sha256((root/p).read_bytes()).hexdigest()
 read=lambda p:json.loads((root/p).read_text())
 allow=read('PRESERVATION_ALLOWLIST.json');paths=allow['files']
 assert allow['repository']=='AgentSlop-Si/research' and allow['public_prefix']==PREFIX
 assert paths==sorted(set(paths))
 assert all(not Path(p).is_absolute() and '..' not in Path(p).parts for p in paths)
 assert not any(p.is_symlink() for p in root.rglob('*'))
 assert paths==sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file())
 m=read('MANIFEST.json');assert m['excluded_from_this_hash_list']==['MANIFEST.json','SEAL.json']
 assert sorted(e['path'] for e in m['files'])==sorted(set(paths)-{'MANIFEST.json','SEAL.json'})
 for e in m['files']:assert sha(e['path'])==e['sha256'] and (root/e['path']).stat().st_size==e['bytes'],e['path']
 seal=read('SEAL.json')
 for name,key in [('MANIFEST.json','manifest_sha256'),('PRESERVATION_ALLOWLIST.json','allowlist_sha256'),('FINAL_ACCEPTANCE.json','acceptance_sha256'),('OWNER_DISPOSITIONS.json','owner_dispositions_sha256')]:assert sha(name)==seal[key]
 assert seal['status']=='SEALED_LOCAL_PUBLICATION_PACKET'
 assert seal['owner_closures']==seal['priority_changes']==seal['census_change']==0
 assert not seal['historical_novelty_claim'] and not seal['scientific_reruns_during_packaging'] and not seal['external_writes']
 bindings=read('COPY_BINDINGS.json')['files']; by_path={e['public_path']:e for e in bindings}
 assert len(by_path)==len(bindings)
 for e in bindings:
  assert e['transformation']=='EXACT_COPY'
  assert sha(e['public_path'])==e['source_sha256']==e['public_sha256']
  assert (root/e['public_path']).stat().st_size==e['source_bytes']==e['public_bytes']
 for source in EXPECTED_SOURCES:
  prefix=source['label']; mp=prefix+'/'+source['manifest'];assert sha(mp)==source['manifest_sha256']
  es=manifest_entries(root/mp); omitted={e['path']:e for e in source.get('omitted_files',[])}; expected={prefix+'/'+e['path'] for e in es if e['path'] not in omitted}|{mp}
  if source.get('seal'):
   sp=prefix+'/'+source['seal'];expected.add(sp);assert sha(sp)==source['seal_sha256']
   assert (root/sp).read_text().strip()==source['manifest_sha256']+'  '+source['manifest']
  assert expected=={p for p in by_path if p.startswith(prefix+'/')}
  for e in es:
   if e['path'] in omitted:
    om=omitted[e['path']];assert e['sha256']==om['sha256'] and e['bytes']==om['bytes']
    assert not (root/prefix/e['path']).exists()
   else:
    b=by_path[prefix+'/'+e['path']];assert e['sha256']==b['source_sha256']
    if 'bytes' in e: assert e['bytes']==b['source_bytes']
  for p in expected:assert by_path[p]['source_manifest_sha256']==source['manifest_sha256']
 a=read('FINAL_ACCEPTANCE.json');assert a['scientific_acceptance']=='INHERITED_FROM_PRESERVED_INDEPENDENT_REVIEWS'
 assert set(a['results'])=={'gaussian','mixedprime','cyclic'}
 for key,e in a['results'].items():
  for field in ['candidate_manifest','review_manifest','accepted_proof','review','verdict']:assert sha(e[field+'_path'])==e[field+'_sha256']
  assert e['independently_accepted'] and not e['owner_closure']
 g=a['results']['gaussian'];gv=read(g['verdict_path'])
 assert gv['status']=='ACCEPTED_SCOPED' and gv['proof_corrections_required']==[]
 assert gv['candidate_manifest_sha256']==g['candidate_manifest_sha256'] and gv['candidate_report_sha256']==g['accepted_proof_sha256']
 assert gv['owner']=='ALG-036' and gv['retained_priority']==34
 assert sha('gaussian/review/CANDIDATE_MANIFEST.sha256')==g['candidate_manifest_sha256']
 assert not g['exact_nondivisible_optimizer_closed'] and not g['computable_gap_claimed']
 s=a['results']['mixedprime'];sv=read(s['verdict_path'])
 assert sv['verdict']=='PASS' and sv['independent_checks_passed']
 assert sv['candidate_manifest_sha256']==s['candidate_manifest_sha256'] and sv['candidate_report_sha256']==s['accepted_proof_sha256']
 assert sv['owner_status']=='TO RESEARCH' and sv['owner_priority']==42
 assert not s['all_mixedprime_necessity_closed'] and not s['full_support_classification_claimed']
 c=a['results']['cyclic'];cv=read(c['verdict_path'])
 assert cv['verdict']=='ACCEPT' and cv['analytic_proof_status']=='Independently accepted in full; no mathematical correction required'
 assert cv['frozen_candidate_manifest_sha256']==c['candidate_manifest_sha256'] and cv['frozen_candidate_proof_sha256']==c['accepted_proof_sha256']
 assert cv['all_candidate_manifest_entries_hash_and_size_verified']
 assert cv['exact_witness_orders']==list(range(4,49,4))+[64]
 assert not c['smaller_rank_attainment_closed'] and not c['odd_order_attainment_closed']
 od=read('OWNER_DISPOSITIONS.json');assert od['owner_closures']==od['priority_changes']==od['census_change']==0
 assert not od['historical_novelty_claim']
 assert set(od['owners'])=={'ALG-036','M-SPARSE-DEFECT','PHASE-DEFECT-RANK-20261011'}
 for owner,priority in [('ALG-036',34),('M-SPARSE-DEFECT',42),('PHASE-DEFECT-RANK-20261011',37)]:
  d=od['owners'][owner];assert d['status']=='TO RESEARCH' and d['priority']==priority and not d['owner_closure'];assert d['preserved'] and d['remaining']
 preservation=read('ACCEPTED_RESULT_PRESERVATION.json');assert preservation['older_results_reopened'] is False
 assert preservation['full_third_party_paper_bodies_included'] is False
 for e in preservation['selected_exact_support_copies']:assert e['public_path'] in by_path
 spreserved=od['owners']['M-SPARSE-DEFECT']['preserved']
 assert any('class of invertible M' in v and 'attained iff sigma_d>0' in v for v in spreserved)
 assert any('Lang Lemma 3.3' in v and 'Li-Lim' in v for v in spreserved)
 omissions=read('OMISSIONS.json');assert len(omissions['omitted_manifest_declared_source_files'])==1
 omitted=omissions['omitted_manifest_declared_source_files'][0]
 assert omitted['public_path_not_published']=='mixedprime/candidate/sources/preserved_owner_gate_REVIEW.md'
 assert omitted['sha256']=='d0fdaf76f64395c59b1d12eeb1545cd82958618b27a01a784495a2d412d7eb71' and omitted['bytes']==15533
 assert not (root/omitted['public_path_not_published']).exists()
 projection=read('PROJECTION_DISCLOSURE.json');assert projection['privacy_projected_files']==1 and not projection['source_path_adaptations']
 assert len(projection['files'])==1;pb=projection['files'][0]
 assert pb['source_sha256']==omitted['sha256'] and pb['source_bytes']==omitted['bytes']
 assert pb['source_manifest_sha256']==s['candidate_manifest_sha256']
 assert sha(pb['public_path'])==pb['public_sha256'] and (root/pb['public_path']).stat().st_size==pb['public_bytes']
 text=(root/pb['public_path']).read_text();start3=text.index('## 3. M-SPARSE-DEFECT:');start5=text.index('## 5. Immutable retained links')
 segments=[text[start3:start5],text[start5:]]
 assert [x['source_section'] for x in pb['segments']]==['3','5']
 for segment,b in zip(segments,pb['segments']):
  assert hashlib.sha256(segment.encode()).hexdigest()==b['excerpt_sha256'] and len(segment.encode())==b['excerpt_bytes']
  assert b['transformation']=='VERBATIM_CONTIGUOUS_EXCERPT'
 assert pb['scientific_text_within_selected_sections_edited'] is False
 assert pb['public_path'] not in by_path
 assert not any(x in text for x in ['## 1. Sources and read coverage','## 4. Exact scope','Private local evidence only','Candidate field classes are:'])
 pc=read('PACKAGING_CHECKS.json');assert pc['source_file_sets_complete'] is False and pc['explicit_private_support_omissions']==1
 assert pc['source_exact_copies']==63 and pc['support_exact_copies']==10 and pc['scientific_proofs_and_final_reviews_complete']
 forbidden=[r'https?://docs[.]google[.]com/spreadsheets/d/',r'"spreadsheetId"\s*:',r'"spreadsheet_id"\s*:',r'sediment://',r'libfile_',r'"download_url"\s*:',r'Bearer\s+[A-Za-z0-9]',r'-----BEGIN[^\n]*PRIVATE KEY-----',r'/root/',r'dream_notes',r'cloud_threads',r'Private local evidence only',r'Candidate field classes are:',r'(?:Catalogue|Research overview|novelity breakthough) [A-Z]+[0-9]+:[A-Z]+[0-9]+']
 for name in paths:
  if name=='verify_package.py':continue
  content=(root/name).read_text()
  assert not any(re.search(pattern,content) for pattern in forbidden),name
 print(json.dumps({'status':'PASS','files':len(paths),'manifest_entries_verified':len(m['files']),'exact_copies':len(bindings),'explicit_private_support_omissions':1,'verbatim_scientific_projections':1,'frozen_scientific_sources':len(EXPECTED_SOURCES),'scope_checks':'PASS','bounded_privacy_scan':'PASS','scientific_reruns':False,'owner_closures':0,'external_writes':False},indent=2))
if __name__=='__main__':main()
