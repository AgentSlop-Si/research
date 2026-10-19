from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((D/'input/candidate/MANIFEST.json').read_text())
for e in manifest['files']:
 p=D/'input/candidate'/e['path'];q=D/'author_replay'/e['path']
 assert sha(p)==e['sha256'] and p.read_bytes()==q.read_bytes(),e['path']
for n in ['FIXED_REPLAY.txt','FIXED_REPLAY.log','independent_minors.cpp','independent_chart.h','AUTHOR_FIXED_MINORS.txt']:
 assert (D/n).read_bytes()==(D/'cold_replay'/n).read_bytes(),n
assert (D/'AUTHOR_FIXED_MINORS.txt').read_bytes()==(D/'FIXED_REPLAY.txt').read_bytes()==(D/'INDEPENDENT_MINORS.txt').read_bytes()
stats={'labels':280,'embeddings':2,'nonzero_fixed_minors':560,'minor_order':126,'full_quotient_checks':70560,'direct_green_inversions':53760,'inverse_entry_comparisons':6881280,'duplicate_row_zero_controls':2}
cold={'status':'PASS','procedure':'Fresh separate-directory C++ rebuild, fixed author windows and all126 original columns, no replacement minors.','statistics_per_run':stats,'byte_identical_files':{n:sha(D/n) for n in ['FIXED_REPLAY.txt','FIXED_REPLAY.log','independent_minors.cpp','independent_chart.h','AUTHOR_FIXED_MINORS.txt']}}
(D/'COLD_REPLAY.json').write_text(json.dumps(cold,indent=2)+'\n')
author={'status':'PASS','candidate_manifest_sha256':sha(D/'input/candidate/MANIFEST.json'),'manifested_files_byte_identical':17,'full_window_quotient_checks':439040,'note':'Supplementary replay of inspected fresh author programs; independent acceptance uses separate direct-inverse reconstruction.'}
(D/'AUTHOR_REPLAY.json').write_text(json.dumps(author,indent=2)+'\n')
v={'verdict':'ACCEPT_NARROW','owner':'Q27','theorem':'All280 prescribed original-chart four-coordinate single-fully-free-branch guarded unit-phase slices are excluded from external invertible-complex monomial equivalence to F8.','candidate_manifest_sha256':sha(D/'input/candidate/MANIFEST.json'),'source_chart_sha256':sha(D/'input/candidate/sources/CHART.json'),'review_sha256':sha(D/'REVIEW.md'),'proof_obligations':{'original_six_guards_preserved':True,'fourteen_fixed_tree_gains_preserved':True,'stage_order_preserved':True,'complete_280_label_coverage':True,'characteristic_zero_divisibility':True,'H_support_dimension':27,'Q_support_dimension':126,'constant_in_Q_upper_space':True,'checked_coefficient_ring_homomorphisms':2,'all560_fixed_minor_residues_independently_reproduced':True,'global_polynomial_ideal_identity':'det(C) F=sum_j cofactor(C)_(j,0) P_j','no_silently_discarded_components':True},'independent_fixed_replay':stats,'clean_rebuild_identical':True,'source_code_hashes':{n:sha(D/n) for n in ['independent_structure.py','independent_minors.cpp','independent_compare_certificates.py']},'limits':['No full34-phase-fiber theorem','No other four-coordinate placements','No five-or-more-coordinate theorem','No owner closure','No priority change','No novelty or Fourier algorithm claim'],'external_writes':False}
# Human-readable strings retain normal number/word spacing.
v['theorem']=v['theorem'].replace('All280','All 280');v['limits'][0]='No full 34-phase-fiber theorem'
(D/'VERDICT.json').write_text(json.dumps(v,indent=2)+'\n')
required=['REVIEW.md','VERDICT.json','independent_structure.py','independent_chart.h','INDEPENDENT_STRUCTURE.json','INDEPENDENT_STRUCTURE.log','independent_minors.cpp','INDEPENDENT_MINORS.txt','INDEPENDENT_MINORS.log','independent_compare_certificates.py','AUTHOR_FIXED_MINORS.txt','FIXED_REPLAY.txt','FIXED_REPLAY.log','CERTIFICATE_COMPARISON.json','bind_frozen_candidate.py','FROZEN_CANDIDATE_BINDING.json','COLD_REPLAY.json','AUTHOR_REPLAY.json','seal_review.py']
required += [str(p.relative_to(D)) for p in (D/'input').rglob('*') if p.is_file()]
r={'schema':'q27-four-phase-independent-review-v1','candidate_manifest_sha256':v['candidate_manifest_sha256'],'verdict':'ACCEPT_NARROW','files':[{'path':n,'bytes':(D/n).stat().st_size,'sha256':sha(D/n)} for n in sorted(required)]}
(D/'MANIFEST.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'verdict':v['verdict'],'candidate_manifest_sha256':v['candidate_manifest_sha256'],'review_manifest_sha256':sha(D/'MANIFEST.json'),'review_files':len(r['files']),'review_bytes':sum(x['bytes'] for x in r['files']),'fixed_minors':560}))
