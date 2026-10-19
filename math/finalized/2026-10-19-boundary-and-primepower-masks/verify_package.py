#!/usr/bin/env python3
"""Verify only publication integrity, privacy boundaries and inherited acceptance."""
from pathlib import Path
import hashlib,json,re
EXPECTED_SOURCES = [{'label': 'f020/candidate', 'manifest_sha256': 'eb31526958e004a90a531f7a857679faa9515fdb50146343fda23a50fbd9c9cb'}, {'label': 'f020/review', 'manifest_sha256': 'de575d3bb75149adcef8dd6f53ca4931cda23ac5ddaeb19a4f99da2aed6cd775'}, {'label': 'sparse/candidate', 'manifest_sha256': '5f615de544e85ab0d64da17c9fbc101cdb48022c4a25be9696622e033af797c8', 'seal_name': 'SEAL.sha256', 'seal_sha256': '534e252d70ca415c879367ff58534029230e309225911f61c7f7059518f859b0'}, {'label': 'sparse/review', 'manifest_sha256': 'afb66c17f2bff7e4e009507dc583392f98b31906bce3e70c13c6d7f5dc5ba67f', 'seal_name': 'SEAL.sha256', 'seal_sha256': '858911fdd183096898ad936f5d26bbb7410eb6829c2e2ca0c95d1dd6a749c9ad'}]
PREFIX = 'math/finalized/2026-10-19-boundary-and-primepower-masks'
def main():
 root=Path(__file__).resolve().parent
 sha=lambda p:hashlib.sha256((root/p).read_bytes()).hexdigest()
 read=lambda p:json.loads((root/p).read_text())
 allow=read('PRESERVATION_ALLOWLIST.json'); paths=allow['files']
 assert allow['repository']=='AgentSlop-Si/research' and allow['public_prefix']==PREFIX
 assert paths==sorted(set(paths))
 assert all(not Path(p).is_absolute() and '..' not in Path(p).parts for p in paths)
 assert not any(p.is_symlink() for p in root.rglob('*'))
 assert paths==sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file())
 m=read('MANIFEST.json'); assert m['excluded_from_this_hash_list']==['MANIFEST.json','SEAL.json']
 assert sorted(x['path'] for x in m['files'])==sorted(set(paths)-{'MANIFEST.json','SEAL.json'})
 for e in m['files']:
  assert sha(e['path'])==e['sha256'] and (root/e['path']).stat().st_size==e['bytes'],e['path']
 seal=read('SEAL.json')
 for name,key in [('MANIFEST.json','manifest_sha256'),('PRESERVATION_ALLOWLIST.json','allowlist_sha256'),('FINAL_ACCEPTANCE.json','acceptance_sha256'),('OWNER_DISPOSITIONS.json','owner_dispositions_sha256')]: assert sha(name)==seal[key]
 assert seal['status']=='SEALED_LOCAL_PUBLICATION_PACKET'
 assert seal['broad_owner_closures']==0 and seal['priority_changes']==0 and seal['census_change']==0
 assert seal['scientific_reruns_during_packaging'] is False and seal['external_writes'] is False
 bindings=read('COPY_BINDINGS.json')['files']; by_path={e['public_path']:e for e in bindings}
 assert len(by_path)==len(bindings)
 for e in bindings:
  assert e['transformation']=='EXACT_COPY'
  assert sha(e['public_path'])==e['source_sha256']==e['public_sha256']
  assert (root/e['public_path']).stat().st_size==e['source_bytes']==e['public_bytes']
 for source in EXPECTED_SOURCES:
  prefix=source['label']; mp=prefix+'/MANIFEST.json'; assert sha(mp)==source['manifest_sha256']
  sm=read(mp); es=sm if isinstance(sm,list) else sm['files']
  expected={prefix+'/'+e['path'] for e in es}|{mp}
  if source.get('seal_sha256'):
   sp=prefix+'/'+source['seal_name']; expected.add(sp); assert sha(sp)==source['seal_sha256']
   if source['seal_name']=='SEAL.sha256': assert (root/sp).read_text().strip()==sha(mp)+'  MANIFEST.json'
  assert expected=={p for p in by_path if p.startswith(prefix+'/')}
  for e in es:
   b=by_path[prefix+'/'+e['path']]
   assert e['sha256']==b['source_sha256'] and e.get('bytes',e.get('size'))==b['source_bytes']
  for p in expected: assert by_path[p]['source_manifest_sha256']==source['manifest_sha256']
 a=read('FINAL_ACCEPTANCE.json'); assert a['scientific_acceptance']=='INHERITED_FROM_PRESERVED_INDEPENDENT_REVIEWS'
 assert set(a['results'])=={'f020','sparse'}
 for key,e in a['results'].items():
  for field in ['candidate_manifest','review_manifest','accepted_proof','review','verdict']: assert sha(e[field+'_path'])==e[field+'_sha256']
  v=read(e['verdict_path']); assert v['verdict']==({'f020':'ACCEPT','sparse':'ACCEPT_PRIMEPOWER_THEOREM_WITH_SCOPE_QUALIFICATION'}[key])
  assert e['independently_accepted'] is True and e['broad_owner_closure'] is False
 f=a['results']['f020']; v=read(f['verdict_path'])
 assert v['candidate_manifest_sha256']==f['candidate_manifest_sha256'] and v['candidate_report_sha256']==f['accepted_proof_sha256']
 assert v['independent_exact_assertions']==195 and v['all_independent_assertions_passed'] is True and v['blocking_issues']==[]
 assert f['accepted_range']=='0<=b<p^s and b<=2p, p odd prime, s>=1'
 assert f['boundary_new_theorem']=='b=2p, p odd prime, s>=2'
 assert f['claims_beyond_2p'] is False and f['discriminant_valuation']=='v_t(Disc_X P_(2p))=p(4p-3), v_t(q-1)=1'
 c=read('f020/candidate/CHECKS.json'); assert c['status']=='PASS' and c['assertions']==74
 ic=read('f020/review/INDEPENDENT_CHECKS.json'); assert ic['all_passed'] is True and ic['total_assertions']==195
 assert len(ic['checks'])==195 and all(e['pass'] for e in ic['checks'])
 s=a['results']['sparse']; assert s['accepted_range']=='N=p^a, p prime, a>=1, 1<=d<=N'
 assert s['necessary_and_sufficient_degree']=='d=p^b, 0<=b<=a; proper d<N iff b<a'
 assert s['mixed_prime_necessity_closed'] is False and s['exact_nonsharp_optima_closed'] is False
 assert s['optimal_quantitative_gap_rates_closed'] is False and s['full_square_block_classification'] is False
 sv=read(s['verdict_path']); cb=sv['candidate_binding']
 assert cb['candidate_manifest_sha256']==s['candidate_manifest_sha256'] and cb['candidate_report_sha256']==s['accepted_proof_sha256']
 assert sv['owner_status']=='TO RESEARCH' and sv['owner_priority']==42
 assert sv['independent_positive_cases']==53 and sv['independent_descent_gram_entries']==181444
 assert sv['candidate_replay_byte_identical_outputs']==3 and sv['external_writes'] is False
 assert all(x=='PASS' for x in sv['proof_obligations'].values())
 assert sv['scope_qualification'] and s['scope_qualification'] and s['inherited_quantitative_corollary']
 replay=read('sparse/review/CANDIDATE_REPLAY_COMPARISON.json'); assert len(replay)==3
 for e in replay:
  assert e['byte_identical'] is True
  assert sha('sparse/candidate/'+e['path'])==e['sha256']==sha('sparse/review/candidate_replay/'+e['path'])
 for pth in [p for p in by_path if p.startswith('sparse/candidate/')]:
  relative=pth[len('sparse/candidate/'):]
  assert sha(pth)==sha('sparse/review/candidate_frozen/'+relative)
 retained=read('ACCEPTED_RESULT_PRESERVATION.json'); assert len(retained['results'])==4
 assert retained['source_wording_correction']

 od=read('OWNER_DISPOSITIONS.json'); assert set(od['owners'])=={'F020','M-SPARSE-DEFECT'}
 for owner,priority in [('F020',58),('M-SPARSE-DEFECT',42)]:
  d=od['owners'][owner]; assert d['status']=='TO RESEARCH' and d['priority']==priority and d['owner_closure'] is False
 assert od['owners']['F020']['alias']=='F023'
 assert od['owner_closures']==0 and od['priority_changes']==0 and od['census_change']==0 and od['historical_novelty_claim'] is False
 p=read('PROJECTION_DISCLOSURE.json'); assert p['privacy_projected_files']==0 and p['source_path_adaptations'] is False
 omissions=read('OMISSIONS.json'); assert omissions['omitted_manifest_declared_source_files']==[]
 forbidden=[r'https?://docs[.]google[.]com/spreadsheets/d/',r'"spreadsheet_id"\s*:',r'sediment://',r'libfile_',r'"download_url"\s*:',r'Bearer\s+[A-Za-z0-9]',r'/root/',r'dream_notes',r'cloud_threads']
 for name in paths:
  if name=='verify_package.py': continue
  assert not any(re.search(pattern,(root/name).read_text()) for pattern in forbidden),name
 print(json.dumps({'status':'PASS','files':len(paths),'manifest_entries_verified':len(m['files']),'exact_source_copies':len(bindings),'frozen_sources':len(EXPECTED_SOURCES),'scope_checks':'PASS','bounded_privacy_scan':'PASS','scientific_reruns':False,'broad_owner_closures':0,'external_writes':False},indent=2))
if __name__=='__main__': main()
