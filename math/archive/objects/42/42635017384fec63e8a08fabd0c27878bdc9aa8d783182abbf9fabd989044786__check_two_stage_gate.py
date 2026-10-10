"""Numerical corroboration of TWO_STAGE_GATE.md; the analytic proof is primary."""
from math import cos,pi,isclose
from pathlib import Path
import json
out=[]
for N in (1,2,3,4,5,6,7,8,16,32):
    squares=sorted(((5-4*cos((2*j+1)*pi/N))/(2-2*cos((2*j+1)*pi/N)) for j in range(N)),reverse=True)
    pairs=[a*b for a,b in zip(squares,reversed(squares))]
    nonconstant=not isclose(min(pairs),max(pairs),rel_tol=1e-10,abs_tol=1e-10)
    assert nonconstant==(N>=3 and N!=4)
    out.append({'N':N,'minimum_reverse_pair_product':min(pairs),'maximum_reverse_pair_product':max(pairs),'nonconstant':nonconstant})
Path(__file__).with_name('two_stage_gate_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
