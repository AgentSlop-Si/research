from __future__ import annotations
import csv, json
from pathlib import Path
from cross_ratio_gate import run_audit as cross_audit
from group_audit import run_audit as group_audit
from tensor_weil import direct_partial_fft_cost

ROOT=Path(__file__).resolve().parent
results={"group_audit":group_audit(),"cross_ratio_audit":cross_audit()}
(ROOT/'results.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
rows=[]
for p,n in ((3,2),(3,3),(3,4),(3,5),(5,2),(5,3),(5,4)):
    for r in range(n+1):
        d=direct_partial_fft_cost(p,n,r)
        rows.append({"p":p,"n":n,"dimension":p**n,"partial_rank":r,"row_nonzeros":p**r,
                     "dense_terms":d['dense_terms'],"writes":d['writes']})
with (ROOT/'OPERATION_LEDGER.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary={
  "status":"scoped exact theorem and obstruction; no faster cyclic FFT",
  "main_positive":"Sp(2n,p) Weil operators have partial-Fourier rank r=rank(B), with p^r nonzeros per row/column",
  "main_negative":"cyclic F_{p^n} is not monomially equivalent to any finite-field Weil operator for n>1",
  "sp4_3_group_size":results['group_audit']['sp4_3_size'],
  "sp4_3_rank_B_distribution":results['group_audit']['sp4_3_rank_B_distribution'],
  "tested_cyclic_dimensions":[9,27,25],
  "predecessor":"fft_metaplectic_bruhat_rigidity_v23.zip",
}
(ROOT/'RESULT_SUMMARY.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
