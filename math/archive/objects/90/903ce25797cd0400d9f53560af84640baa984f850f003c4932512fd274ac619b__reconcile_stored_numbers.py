from pathlib import Path
import json
from decimal import Decimal as D
P=Path(__file__).parent;rows=json.loads((P/'STORED_RESULTS.json').read_text());evidence=[]
def record(suffix):
 r=next(x for x in rows if x['member_name'].endswith(suffix));return r,json.loads((P/r['snapshot']).read_text())
a,ka=record('fft_orbit_correction_research/kernel_spectrum/results/audit.json');b,ob=record('fft_orbit_correction_research/orbit_norm/results/orbit_audit.json');c,sf=record('fft_orbit_correction_research/sparse_forcing/results.json');d,cf=record('fft_orbit_correction_research/cycle_flow/results.json')
basis=ka['kernel_basis_vectors']+ka['full_fourier_basis_vectors']+ob['basis_vectors']+sf['forcing_basis_vectors']+cf['complete_basis_vectors'];assert basis==2254
evidence.append({'kind':'stored_component_count_reconciliation','claimed_launcher_basis_cases':2254,'recomputed_sum':basis,'spectrum_points':ka['spectrum_points'],'median_checks':cf['median_optimality_cases'],'sources':[x['snapshot'] for x in (a,b,c,d)],'status':'consistent_stored_values'})
r,obj=record('fft_new_material_fusion_checkpoint_20261009/fft_shrinking_fusion_review/results.json')
for x in obj['repacking_instrumentation']:
 blocks=(x['N']+x['B']-1)//x['B'];assert x['actual_scalar_packing_lane_visits']==2*blocks*x['G']*x['B'];assert x['packing_calls']==2*blocks*x['G'];assert x['minimum_2NG']==2*x['N']*x['G']
evidence.append({'kind':'stored_repacking_arithmetic','cases':len(obj['repacking_instrumentation']),'source':r['snapshot'],'status':'all_scalar_visit_equalities_consistent'})
r,obj=record('fft_new_material_fusion_checkpoint_20261009/fft_green_fusion_research/results.json')
for x in obj['gauges']['original_gauge_cases']:
 assert all(v['literal_add']-v['reported_add']==1 for v in x['literal_call_counts']);assert x['undercounted_additions']==x['gauge_calls']
evidence.append({'kind':'stored_gauge_undercount','cases':len(obj['gauges']['original_gauge_cases']),'source':r['snapshot'],'status':'one_missing_add_per_call_consistent'})
r,obj=record('fft_phase10_aot/benchmark_results.json')
for x in obj['benchmarks']:
 t=x['timings_ms'];assert abs(D(str(t['phase10_setup_ms']))+D(str(t['aot_native']))-D(str(t['aot_cold_total_ms'])))<=D('.002');assert abs(D(str(t['phase10_setup_ms']))+D(str(t['aot_shape']))-D(str(t['aot_shape_cold_total_ms'])))<=D('.002')
evidence.append({'kind':'stored_benchmark_cold_totals','rows':len(obj['benchmarks']),'source':r['snapshot'],'status':'consistent_with_rounded_setup_plus_stream_values','note':'No new timing validation; machine/binary provenance not established.'})
r,obj=record('fft_nonlinear_rank_research_2026-10-10/EXACT_CERTIFICATES.json')
w=obj['nonaffine_256']['witness'];assert w['exact_complex_fourier_rank']-w['capacity_bound']==w['rank_gap']==4
for x in obj['edit_robust'].values():assert x['exact_complex_fourier_rank']-x['perturbed_network_rank_bound_on_original_endpoint_sets']==x['strict_gap']>0
print(json.dumps(obj['edit_robust'],indent=2)[:10000])
evidence.append({'kind':'stored_nonlinear_rank_gaps','source':r['snapshot'],'nonaffine256_gap':4,'robust_gaps':{k:v['strict_gap'] for k,v in obj['edit_robust'].items()},'status':'certificate_arithmetic_consistent','note':'This reconciliation does not rerun the characteristic-zero rank oracle or network flow.'})
(P/'STORED_NUMBER_RECONCILIATION.json').write_text(json.dumps({'note':'Stored output arithmetic checked independently; historical PASS is not present execution or full proof.','checks':evidence},indent=2)+'\n');print('Checked',len(evidence),'stored evidence summaries')
