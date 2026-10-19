"""Full PRNG and structural audit of the retained per-trial failed prefix.
Every split gate is additionally reexecuted by replay_prefix.py; this audit uses only inert JSON.
"""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;state=202610192024;MASK=2**64-1;draws=nodes=candidates=zeros=hits=0;hist={};last=None
for line in (R/'PREFIX_LEDGER.jsonl').open():
 row=json.loads(line);assert row['rng_before']==state;v=[]
 for _ in range(31):
  state^=(state<<13)&MASK;state^=state>>7;state^=(state<<17)&MASK;state&=MASK;v.append(state%53);draws+=1
 assert row['rng_after']==state
 if row.get('zero_draw'):
  assert not any(v);zeros+=1;continue
 assert row['trial']==nodes and row['y']==v and any(v);nodes+=1
 assert not hits,'Search must stop at first split candidate'
 for x in row['gate_roots']:
  assert len(x['lambda'])==31 and len(x['H'])==8
  assert x['H'][-1]==[1]+[0]*30
  assert x['nonzero_constant']==any(x['H'][0])
  if x['nonzero_constant']:candidates+=1
  assert not x['fully_splits'] or x['nonzero_constant']
  if x['fully_splits']:hits+=1;last=(row,x)
 assert row['cumulative_candidates']==candidates and row['hit']==bool(hits)
 hist[len(row['gate_roots'])]=hist.get(len(row['gate_roots']),0)+1
assert hits==1
out=json.loads((R/'NONSTABLE_CANDIDATE.json').read_text());row,x=last
assert all(out[k]==row[k] for k in ['trial','y']) and out['candidates']==candidates and out['H']==x['H'] and out['lambda']==x['lambda']
assert out['nonzero_nodes']==nodes and out['coefficient_draws']==draws and out['zero_draws']==zeros and nodes<=100000
receipt={'verdict':'PASS','seed':202610192024,'cap':100000,'nonzero_cross_nodes':nodes,'zero_nodes_skipped':zeros,'coefficient_draws':draws,'nonzero_constant_candidates':candidates,'fully_splitting_candidates_before_stop':hits,'first_hit_trial':row['trial'],'gate_root_count_histogram':hist,'prefix_sha256':hashlib.sha256((R/'PREFIX_LEDGER.jsonl').read_bytes()).hexdigest(),'scope':'Exact PRNG/ledger structure. Split falsity for prefix additionally requires the deterministic arithmetic replay.'}
(R/'PREFIX_AUDIT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
