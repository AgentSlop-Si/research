"""New bounded exact screen of all 24x24 Hamiltonian order pairs; no uploaded code."""
import importlib.util,itertools,json
from pathlib import Path
spec=importlib.util.spec_from_file_location('own_gate',str(Path(__file__).with_name('_projective_gate_helpers.py')))
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h);h.p=241
n=5;omega=91;B=h.target(n,omega);ident=list(range(n));cycles=[]
for tail in itertools.permutations(range(1,n)):
    cyc=[0]+list(tail);pp=[0]*n
    for i,j in zip(cyc,cyc[1:]+cyc[:1]):pp[i]=j
    cycles.append(dict(cycle=cyc,permutation=pp))
assert len(cycles)==len({tuple(x['permutation'])for x in cycles})==24
results=[]
for a,ca in enumerate(cycles):
    for b,cb in enumerate(cycles):
        rel=h.extract(B,ident,ca['permutation'],ident,cb['permutation'])
        answer=h.solve_rows(n,rel,finite=False)
        results.append(dict(first=a,second=b,**answer))
counts={}
for x in results:counts[x['status']+':'+x.get('reason','survivor')]=counts.get(x['status']+':'+x.get('reason','survivor'),0)+1
out=dict(prime=241,omega=omega,N=n,B=B,cycles=cycles,pairs=len(results),counts=counts,survivors=[[x['first'],x['second']]for x in results if x['status']=='PASS'],results=results)
Path(__file__).with_name('ORDER_SCREEN_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items()if k not in ('results','cycles','B')},indent=2))
