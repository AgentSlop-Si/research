from pathlib import Path
import json
P=Path(__file__).resolve().parent
D=json.loads((P/'ALL_MONOMIAL_MINORS.json').read_text());L=json.loads(Path('research_cycle_1635/v34_independent_audit/source/extracted/fft_cyclotomic_zero_forcing_v34/topology_11.json').read_text())['layers']
old={e for c in D['certificates'] if c['order']==1 for e in c['edges']};new={e for c in D['certificates'] for e in c['edges']}
counts=[len({e for e in new if e//33==l}) for l in range(3)]
Arows={L[0][e][0] for e in new if e<33};Ccols={L[2][e-66][1] for e in new if e>=66}
missing=set(range(11))-Arows;assert missing=={0}
choices=[i for i,(r,s) in enumerate(L[0]) if r==0]
assert len(new)==63 and counts==[21,21,21] and Ccols==set(range(11)) and choices==[0,11,22]
gauges=[min(e for e in new if e<33 and L[0][e][0]==v) for v in sorted(Arows)]
gauges+=[min(e for e in new if e>=66 and L[2][e-66][1]==v) for v in sorted(Ccols)]
assert len(gauges)==21 and len(set(gauges))==21
out={'status':'PASS','old_mandatory_edges':len(old),'new_mandatory_edges':len(new),'mandatory_counts_by_layer':counts,'mandatory_edge_indices':sorted(new),'added_indices':sorted(new-old),'globally_safe_21_gauge_edges':gauges,'remaining_chart_gauge_choices':choices,'reason_three_charts_cover':'A is invertible because CBA=F11 is invertible. Thus row0 ofA cannot be zero, and at least one of its allowed edges0,11,22 is nonzero. Each chart normalizes that edge in addition to the21 global mandatory gauge edges.','scope':'Nonvanishing and algebraic chart coverage only; these gauges are not asserted integral or unit-valued.'}
(P/'MANDATORY_EDGE_REVIEW.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
